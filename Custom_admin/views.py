from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils import timezone
from profiles.models import Profile, ProfileImage,custom_admin
from checkout.models import Subscription
from profiles.views import is_admin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.db.models import Q,Count
from django.contrib.auth.models import User

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Cards data
    awaiting_approval_count = Profile.objects.filter(is_verified=False).count()
    awaiting_image_approval_count = ProfileImage.objects.filter(is_verified=False).count()
    total_profiles_count = Profile.objects.count()
    active_subscriptions_count = Subscription.objects.count()

    # Tables data
    recent_profiles = Profile.objects.order_by('-user__date_joined')[:10]
    subscriptions = Subscription.objects.all()

    user=request.user
    admin = custom_admin.objects.filter(user=user).first()
    context = {
        'awaiting_approval_count': awaiting_approval_count,
        'awaiting_image_approval_count': awaiting_image_approval_count,
        'total_profiles_count': total_profiles_count,
        'active_subscriptions_count': active_subscriptions_count,
        'recent_profiles': recent_profiles,
        'subscriptions': subscriptions,
        'admin':admin,
    }

    return render(request, 'admin_dashboard.html', context)


#Member_profile views
@login_required(login_url='login')
@user_passes_test(is_admin)
def pending_profiles(request):
    profiles = Profile.objects.filter(is_verified= False).order_by('-time')
    user=request.user
    admin = custom_admin.objects.filter(user=user).first()

    context ={
        'profiles': profiles,
        'admin':admin
        }
    return render(request, 'pending_profiles.html', context)



@login_required(login_url='login')
@user_passes_test(is_admin)
def profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile_images = ProfileImage.objects.filter(user=profile.user)

    user=request.user
    admin = custom_admin.objects.filter(user=user).first()
    context={
        'profile': profile,
        'images': profile_images,
        'admin':admin
        }
    return render(request, 'profile_detail.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def approve_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.is_verified = True
    profile.save()

    # Send approval email
    send_mail(
        'Account Approved',
        'Your POZ FAMILY account has been approved.',
        settings.DEFAULT_FROM_EMAIL,
        [profile.user.email],
    )

    return redirect('pending_profiles')

@login_required(login_url='login')
@user_passes_test(is_admin)
def reject_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.is_verified = False
    profile.save()

    # Send rejection email
    send_mail(
        'Account Rejected',
        'Your account has been rejected.',
        settings.DEFAULT_FROM_EMAIL,
        [profile.user.email],
    )

    return redirect('pending_profiles')

#
# @login_required(login_url='login')
# @user_passes_test(is_admin)
class ProfileListView(View):
    def get(self, request):
        query = request.GET.get('q')
        profiles = Profile.objects.all().order_by('-time')

        if query:
            profiles = profiles.filter(
                Q(user__username__icontains=query) |
                Q(location__icontains=query) |
                Q(ethnicity__icontains=query)
            )

        user=request.user
        admin=custom_admin.objects.filter(user=user).first()
        context={'profiles': profiles,
                 'admin':admin

                 }
        return render(request, 'profiles/profile_list.html', context)


# @login_required(login_url='login')
# @user_passes_test(is_admin)
class ProfileDetailView(View):
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        images = ProfileImage.objects.filter(user=profile.user)
        user=request.user
        admin=custom_admin.objects.filter(user=user).first()
        context={'profile': profile,
                 'images': images,
                 'admin':admin
                 }
        return render(request, 'profiles/profile_detail.html', context)

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        action = request.POST.get('action')

        if action == 'delete':
            user_email = profile.user.email
            profile.user.delete()
            send_mail(
                'Account Deletion Notification',
                'Your account has been deleted. By Admin',
                settings.DEFAULT_FROM_EMAIL,
                [user_email],
                fail_silently=False,
            )
            messages.success(request, 'Profile deleted successfully.')
            return redirect('profile_list')

        user=request.user
        admin=custom_admin.objects.filter(user=user).first()

        context= {'profile': profile,
                  'admin':admin
                  }
        return render(request, 'profiles/profile_detail.html',context)



@login_required(login_url='login')
@user_passes_test(is_admin)
def profile_picture_verification_view(request):
    query = request.GET.get('q')
    users = User.objects.annotate(
        awaiting_approval_count=Count(
            'profileimage',
            filter=Q(profileimage__is_verified=False)
        )
    )

    if query:
        users = users.filter(Q(username__icontains=query) | Q(email__icontains=query))

    context = {
        'users': users,
    }
    return render(request, 'profile_picture_verification.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def approve_profile_pictures_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile_images = ProfileImage.objects.filter(user=user, is_verified=False).order_by('-time')

    if request.method == 'POST':
        for image in profile_images:
            image.is_verified = True
            image.save()

        # Sending email to user after approval
        send_mail(
            'Your Profile Images Have Been Approved',
            'Your profile images have been approved successfully.',
            'admin@example.com',  # Replace with your email
            [user.email],
            fail_silently=False,
        )
        return redirect('profile_picture_verification')

    context = {
        'user': user,
        'profile_images': profile_images,
    }
    return render(request, 'approve_profile_pictures.html', context)



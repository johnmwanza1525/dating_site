from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.forms import modelformset_factory
from profiles.forms import UserLoginForm, UserRegistrationForm, ProfileForm, ProfileImageForm, MessagesForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Profile, ProfileImage
<<<<<<< HEAD
from chat.models import ChatSession, ChatMessage, Views,Winks
import stripe
from checkout.models import Subscription
from django.contrib.auth import authenticate, login as auth_login
from profiles.models import custom_admin
"""
Function to check if member profiles matches with current user's sexuality (and 
vice versa). This stops users from visiting profiles outside of their preferences
"""
=======
from chat.models import Conversations, Messages, Views

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
    
# Check this works after changing MEN to MALE
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
def looking_for_check(request, user_one, user_two):
    if not user_one == user_two:
        if user_one.looking_for == "MALE":
            if not user_two.gender == "MALE":
                return redirect(reverse('index'))
        elif user_one.looking_for == "FEMALE":
            if not user_two.gender == "FEMALE":
                return redirect(reverse('index'))

<<<<<<< HEAD
# Return users height in feet and inches from form choices
def height_choices(member_height):
    height = {
        "152.40": "5' 0",
        "154.94":"5' 1",
        "157.48":"5' 2",
        "160.02":"5' 3",
        "162.56":"5' 4",
        "165.10":"5' 5",
        "167.64":"5' 6",
        "170.18":"5' 7",
        "172.72":"5' 8",
        "175.26":"5' 9",
        "177.80":"5' 10",
        "180.34":"5' 11",
        "182.88":"6' 0",
        "185.42":"6' 1",
        "187.96":"6' 2",
        "190.50":"6' 3",
        "193.04":"6' 4",
        "195.58":"6' 5",
        "198.12":"6' 6",
        "200.66":"6' 7",
        "203.20":"6' 8",
        "205.74":"6' 9",
        "208.28":"6' 10",
        "210.82":"6' 11"
        }
        
    return height[member_height]

# URL to log user out
=======
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out")
    return redirect(reverse('preregister'))
<<<<<<< HEAD

# URL to delete user
@login_required
def delete(request):
    try:
        user = User.objects.get(pk=request.user.id)
        user.delete()
        messages.success(request, "Your account has been deleted") 
    except:
        messages.success(request, "Something went wrong. Please contact us for more information") 
        
    return redirect(reverse('preregister'))
#
# # Log in page
# def login(request):
#     # If user is already logged in
#     if request.user.is_authenticated:
#         return redirect(reverse('index'))
#
#     # If user submits log in form, try logging them in
#     if request.method == "POST":
#         login_form = UserLoginForm(request.POST)
#         if login_form.is_valid():
#             user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
#             if user:
#                 messages.success(request, "Logged in successfully")
#                 auth.login(user=user, request=request)
#                 return redirect(reverse('index'))
#             else:
#                 messages.error(request, "Username or password incorrect")
#     else:
#         login_form = UserLoginForm()
#
#     context = {
#         'login_form':login_form
#     }
#     return render(request, 'login.html', context)


def check_session(request):
    if request.user.is_authenticated:
        return redirect('after_login')
    return None

from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.conf import settings


def user_login(request):
    session_redirect = check_session(request)
    if session_redirect:
        return session_redirect

    if request.method == "POST":
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        user = None
        if '@' in username_or_email:
            # Attempt to find user by email
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                messages.error(request, "No user found with this email address.")
        else:
            # Attempt to find user by username
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                messages.error(request, "No user found with this username.")

        if user and user.check_password(password):
            # Authenticate the user and log them in
            backend = user.backend if hasattr(user, 'backend') else 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user, backend=backend)
            request.session['username'] = user.username  # Set the username in the session
            print(f"Session set: {request.session['username']}")  # Debugging statement
            return redirect('after_login')  # Or your desired redirect
        else:
            messages.error(request, "Invalid credentials. Please try again.")

    login_form = UserLoginForm()

    context = {
        'login_form': login_form
    }

    return render(request, 'login.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import UserRegistrationForm
from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth import login, get_backends


User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            # Check if profile already exists for the user
            if not Profile.objects.filter(user=user).exists():
                Profile.objects.create(user=user, email=user.email)

            # Send email verification
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth import get_user_model, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

User = get_user_model()

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        # Explicitly set the backend as a string
        backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user, backend=backend)

        messages.info(request, 'Thank you for your email confirmation. Now you can create your profile.')
        return redirect(reverse('create_profile'))
    else:
        return HttpResponse('Activation link is invalid!')

    
# # Register a user account page
# def register(request):
#     # If user submits register form, try registering an account
#     if request.method == "POST":
#         registration_form = UserRegistrationForm(request.POST)
#
#         if registration_form.is_valid():
#             registration_form.save()
#
#             user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
#
#             if user:
#                 messages.success(request, "Your account had been created")
#                 auth.login(user=user, request=request)
#                 return redirect(reverse('create_profile'))
#             else:
#                 messages.error(request, "We have been unable to create your account")
#     else:
#         registration_form = UserRegistrationForm()
#
#
#     context = {
#         'registration_form':registration_form
#     }
#     return render(request, 'register.html', context)

# Page to create/edit a user profile
@login_required  
def create_profile(request):
    """
    Create a formset to allow for multiple profile photos to be uploaded
    Assistance from
    https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django
    """
    ImageFormSet = modelformset_factory(ProfileImage, form=ProfileImageForm, extra=6, max_num=6, help_texts=None)
    
    # If user has submitted profile form
    if request.method == "POST":
=======
    
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user:
                messages.success(request, "Logged In Successfully")
                auth.login(user=user, request=request)
                return redirect(reverse('index'))
            else: 
                login_form.add_error(None, "Username or password is incorrect")
    else:
        login_form = UserLoginForm()
            
    context = {
        'login_form':login_form
    }
    return render(request, 'login.html', context)
    

def register(request):
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        
        if registration_form.is_valid():
            registration_form.save()
            
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            
            if user:
                messages.success(request, "Your account had been created")
                auth.login(user=user, request=request)
                return redirect(reverse('create_profile'))
            else:
                messages.error(request, "We have been unable to create your account")
    else:
        registration_form = UserRegistrationForm()
        

    context = {
        'registration_form':registration_form
    }
    return render(request, 'register.html', context)

@login_required
def user_profile(request):
    user = User.objects.get(email=request.user.email)
    user.profileimage_set.all()
    context = {
        'profile':user,
    }
    return render(request, 'profile.html', context)
 
@login_required  
def create_profile(request):
    # user = User.objects.get(email=request.user.email)
    # profile_user_id = user.profile.id
    
    # https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django
    ImageFormSet = modelformset_factory(ProfileImage, form=ProfileImageForm, extra=6, max_num=6, help_texts=None)

    if request.method == "POST":
        # Why doesn't instance work?
        
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        image_form = ProfileImageForm(request.POST, request.FILES)
        
        formset = ImageFormSet(request.POST, request.FILES,
                              queryset=ProfileImage.objects.filter(user_id=request.user.id).all())
<<<<<<< HEAD
        
        # Update profile and change profile to 'to be approved'
        if profile_form.is_valid() and formset.is_valid():
            instance = profile_form.save(commit=False)
            instance.user_id = request.user.id
            instance.is_verified = False
            instance.save()
            
            # Get images requested to be deleted and delete them
            deleted_images = request.POST.getlist('delete')
            for image in deleted_images:
                if not image == "None":
                    ProfileImage.objects.get(pk=image).delete()
                    
            # Save submitted images
=======
                        

        if profile_form.is_valid() and formset.is_valid():
            instance = profile_form.save(commit=False)
            instance.user_id = request.user.id
            instance.is_verified = 'TO BE APPROVED'
            instance.save()
            
            # Delete checked images
            deleted_images = request.POST.getlist('delete')
            print(deleted_images)
            for image in deleted_images:
                if not image == "None":
                    ProfileImage.objects.get(pk=image).delete()
            
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
            for form in formset:
                if form.is_valid() and form.has_changed():
                    instance_image = form.save(commit=False)
                    instance_image.user = request.user
                    instance_image.is_verified = False
                    instance_image.save()
<<<<<<< HEAD

            return redirect(reverse('verification_message'))
            
    else:
=======
                    
                    # image = form['image']
                    # profile_photo = ProfileImage(user=request.user, image=image, is_verified=False)
                    # profile_photo.save()
                    # Add progress bar
            
            return redirect(reverse('index'))
            
    else:
        # user_profile = Profile.objects.get(pk=profile_user_id)
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
        profile_form = ProfileForm(instance=request.user.profile)
        image_form = ProfileImageForm(instance=request.user.profile)
        initial_images = [{'image_url': i.image} for i in ProfileImage.objects.filter(user_id=request.user.id).all() if i.image]
        formset = ImageFormSet(queryset=ProfileImage.objects.filter(user_id=request.user.id).all(), initial=initial_images)
        
<<<<<<< HEAD
    context = {
        'page_ref':'create_profile',
=======
    # AIzaSyAMjDIJJGvw9xwl6n-0Gbm2961UDo9Jato

        
        
    context = {
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
        'profile_form':profile_form,
        'image_form':image_form,
        'formset': formset
    }
        
    return render(request, 'create-profile.html', context)    
<<<<<<< HEAD

# Page to view a specific member profile
@login_required
def member_profile(request, id):
    # Check if member is the current user
    member = User.objects.get(id=id)

    # Use 'profile_detail' instead of 'profile'
    height = height_choices(str(member.profile_detail.height))

    if not member == request.user:
        current_user = False

        # Redirect if sexuality preferences are not met
        result = looking_for_check(request, request.user.profile_detail, member.profile_detail)
        if result:
            return result
        result = looking_for_check(request, member.profile_detail, request.user.profile_detail)
        if result:
            return result

        # Add view if last view is not read or user hasn't viewed member before
=======
    
@login_required 
def member_profile(request, id):
    # Add check if correct gender prefernce (for both)

    # Add check member is current user
    member = User.objects.get(id=id)
    
    if not member == request.user:
        current_user = False
    
        result = looking_for_check(request, request.user.profile, member.profile)
        if result:
            return result
        result = looking_for_check(request, member.profile, request.user.profile)
        if result:
            return result
        
        # Add view if last view is not read or user hasn't view member before
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
        last_view = Views.objects.filter(receiver_id=id).filter(sender_id=request.user.id).last()
        if not last_view or last_view.is_read:
            view = Views(receiver=member, sender=request.user)
            view.save()

<<<<<<< HEAD
        # If user has submitted messages form
        if request.method == "POST" and 'message_submit' in request.POST:
            message_form = MessagesForm(request.POST)
            if message_form.is_valid():
                # Create conversation (if one does not already exist) and message
                conversation = ChatSession.objects.filter(participants=request.user.id).filter(participants=id)
=======
        if request.method == "POST" and 'message_submit' in request.POST:
            message_form = MessagesForm(request.POST)
            if message_form.is_valid():
                conversation = Conversations.objects.filter(participants=request.user.id).filter(participants=id)
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
                if conversation.exists():
                    message = message_form.save(commit=False)
                    message.sender = request.user
                    message.receiver = User.objects.get(pk=id)
                    message.conversation = conversation[0]
                    message.save()
                    return redirect('/chat/%s' % conversation[0].id )
                else:
                    receiver = User.objects.get(pk=id)
                    conversation = Conversations()
                    conversation.save()
                    conversation.participants.add(request.user.id)
                    conversation.participants.add(receiver)
                    message = message_form.save(commit=False)
                    message.sender = request.user
                    message.receiver = receiver
                    message.conversation = conversation
                    message.save()
                    return redirect('/chat/%s' % conversation.id )
        else:
            message_form = MessagesForm()
    else:
        message_form = MessagesForm()
        current_user = True
<<<<<<< HEAD

    if request.user.is_authenticated:
        # Count unopened messages
        unopened_messages = ChatMessage.objects.filter(receiver=request.user, is_read=False).count()

        # Count winks
        winks_count = Winks.objects.filter(receiver=request.user, is_read=False).count()

        # Count views
        views_count = Views.objects.filter(receiver=request.user, is_read=False).count()

        context = {
            'new_message': unopened_messages,
            'new_wink': winks_count,
            'new_view': views_count,
            'height': height,
            'page_ref': 'member_profile',
            'member': member,
            'message_form': message_form,
            'current_user': current_user
        }
    else:
        context = {
            'new_message': 0,
            'new_wink': 0,
            'new_view': 0,
        }

    return render(request, 'member.html', context)

    
# Page to display verification message
def verification_message(request):
    
    return render(request, 'verification-message.html')


def is_member(user):
    return Profile.objects.filter(user=user).exists()

def is_admin(user):
    return custom_admin.objects.filter(user=user).exists()


def after_login(request):
    if is_member(request.user):
        return redirect('index')
    if is_admin(request.user):
        return redirect('admin_dashboard')
    else:
        return redirect ('preregister')











=======
        
    context = {
        'member':member,
        'message_form': message_form,
        'current_user': current_user
    }
    return render(request, 'member.html', context)
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)

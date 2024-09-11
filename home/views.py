<<<<<<< HEAD
from django.shortcuts import render,redirect
from profiles.models import Profile, ProfileImage
=======
from django.shortcuts import render
from profiles.models import Profile
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
from django.db.models import Q, F
from django.db.models import Count
from django.contrib.auth.decorators import login_required
import datetime as DT
<<<<<<< HEAD
from django.contrib.auth.models import User
from chat.models import ChatSession,Winks,ChatMessage,Views
import datetime
import stripe
from checkout.models import Subscription

# Home page after user logs in
@login_required
def index(request):
    user_profile = request.user.profile_detail  # Use related_name 'profile_detail'

    if user_profile.looking_for == "BOTH":
        closest_profiles = Profile.objects.nearby_locations(
            float(user_profile.citylat), float(user_profile.citylong)
        ).order_by('distance').filter(
            Q(looking_for=user_profile.gender) | Q(looking_for="BOTH")
        ).exclude(user_id=request.user.id).all()[:4]
    else:
        closest_profiles = Profile.objects.nearby_locations(
            float(user_profile.citylat), float(user_profile.citylong)
        ).order_by('distance').filter(
            Q(looking_for=user_profile.gender) | Q(looking_for="BOTH")
        ).filter(gender=user_profile.looking_for).exclude(user_id=request.user.id).all()[:4]

    if user_profile.looking_for == "BOTH":
        card_profiles = Profile.objects.nearby_locations(
            float(user_profile.citylat), float(user_profile.citylong)
        ).order_by('distance').filter(
            Q(looking_for=user_profile.gender) | Q(looking_for="BOTH")
        ).exclude(
            user__sent_winks__sender_id=request.user.id
        ).exclude(
            user_id=request.user.id
        ).exclude(
            user__sent_rejects__sender_id=request.user.id
        ).all()[:10]
    else:
        card_profiles = Profile.objects.nearby_locations(
            float(user_profile.citylat), float(user_profile.citylong)
        ).order_by('distance').filter(
            Q(looking_for=user_profile.gender) | Q(looking_for="BOTH")
        ).filter(gender=user_profile.looking_for).exclude(
            user__sent_winks__sender_id=request.user.id
        ).exclude(user_id=request.user.id).exclude(
            user__sent_rejects__sender_id=request.user.id
        ).all()[:10]

    card_profiles_exists = card_profiles.count() > 0

    today = DT.date.today()
    one_week_ago = today - DT.timedelta(days=7)
    if user_profile.looking_for == "BOTH":
        active_profiles = Profile.objects.nearby_locations(
            float(user_profile.citylat), float(user_profile.citylong)
        ).filter(
            Q(looking_for=user_profile.gender) | Q(looking_for="BOTH")
        ).filter(
            user__date_joined__lte=one_week_ago
        ).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4]
    else:
        active_profiles = Profile.objects.nearby_locations(
            float(user_profile.citylat), float(user_profile.citylong)
        ).filter(
            Q(looking_for=user_profile.gender) | Q(looking_for="BOTH")
        ).filter(gender=user_profile.looking_for).filter(
            user__date_joined__lte=one_week_ago
        ).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4]

    if user_profile.looking_for == "BOTH":
        newest_profiles = Profile.objects.nearby_locations(
            float(user_profile.citylat), float(user_profile.citylong)
        ).filter(
            Q(looking_for=user_profile.gender) | Q(looking_for="BOTH")
        ).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4]
    else:
        newest_profiles = Profile.objects.nearby_locations(
            float(user_profile.citylat), float(user_profile.citylong)
        ).filter(
            Q(looking_for=user_profile.gender) | Q(looking_for="BOTH")
        ).filter(gender=user_profile.looking_for).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4]

    if request.user.is_authenticated:
        unopened_messages = ChatMessage.objects.filter(
            chat_session__participants=request.user, is_read=False
        ).exclude(sender=request.user).count()
        winks_count = Winks.objects.filter(
            receiver=request.user, is_read=False
        ).count()
        views_count = Views.objects.filter(
            receiver=request.user, is_read=False
        ).count()

        context = {
            'new_message': unopened_messages,
            'new_wink': winks_count,
            'new_view': views_count,
            'page_ref': 'home',
            'card_profiles_exists': card_profiles_exists,
            'closest_profiles': closest_profiles,
            'active_profiles': active_profiles,
            'newest_profiles': newest_profiles,
            'card_profiles': card_profiles
        }
    else:
        context = {
            'new_message': 0,
            'new_wink': 0,
            'new_view': 0,
        }

    return render(request, 'home.html', context)

# Home page before logged in/registered
def preregister(request):
    if request.user.is_authenticated:
        return redirect('after_login')

    return render(request, 'index.html')
=======


# Create your views here.
@login_required
def index(request):

    # Change limit
    # 'or' needed in gender check https://stackoverflow.com/questions/739776/how-do-i-do-an-or-filter-in-a-django-query
    # Exclude current user
    # Nearby Profiles
    if request.user.profile.looking_for == "BOTH":
        closest_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).exclude(user_id=request.user.id).all()[:4]
    else:
        closest_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).exclude(user_id=request.user.id).all()[:4]
    
    # Profiles for quick match finder
    if request.user.profile.looking_for == "BOTH":
        card_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).exclude(user__winks_receiver__sender_id=request.user.id).exclude(user_id=request.user.id).all()
    else:
        card_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).exclude(user__winks_receiver__sender_id=request.user.id).exclude(user_id=request.user.id).all()
    
    today = DT.date.today()
    one_week_ago = today - DT.timedelta(days=7)
    # Filter date_joined
    # Profiles for active most recently  
    if request.user.profile.looking_for == "BOTH":
        active_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4]
    else:
        active_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4] 
    
    # Profiles for newest
    if request.user.profile.looking_for == "BOTH":
        newest_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4]
    else:
        newest_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4] 

    context = {
        'closest_profiles':closest_profiles,
        'active_profiles':active_profiles,
        'newest_profiles': newest_profiles,
        'card_profiles': card_profiles
    }
    
    return render(request, 'index.html', context)
    
def preregister(request):
    
    return render(request, 'preregister.html')
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)

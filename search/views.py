from django.shortcuts import render
from profiles.models import Profile
from profiles.models import Profile
from .filters import ProfileFilter, GenderlessProfileFilter
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

<<<<<<< HEAD
# Search page to display specific profiles
@login_required
def search(request):
    
    # Get search options not in ProfileFilter or GenderlessProfileFilter form
=======


# Create your views here.

# May need to turn into separate POST and GET
@login_required
def search(request):
    
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    min_height = request.GET.get('height_min', '0')
    max_height = request.GET.get('height_max', '200')
    
    sexuality = request.GET.getlist('sexuality', '')

<<<<<<< HEAD
    user_gender = "MALE" if request.user.profile.gender == "MALE" else "FEMALE"
    
    # Filter users by distance and exclude incompatible sexuality preferences
=======
    # Filter based on returned user's gender preferences and location
    user_gender = "MALE" if request.user.profile.gender == "MALE" else "FEMALE"
    # Add check to see if distance was submitted (max on range is worldwide=None)
    
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    distance = request.GET.get('distance', '')
    
    if distance and distance != "worldwide":
        distance_check = int(distance)
<<<<<<< HEAD
        qs = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong), distance_check).order_by('distance').filter(Q(looking_for=user_gender) | Q(looking_for="BOTH")).exclude(user_id=request.user.id)
    else:
        qs = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=user_gender) | Q(looking_for="BOTH")).exclude(user_id=request.user.id)
    
    
    # Filter based on sexuality preferences selected in search
=======
        qs = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong), distance_check).order_by('distance').filter(Q(looking_for=user_gender) | Q(looking_for="BOTH")).exclude(user_id=request.user.id)
    else:
        qs = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).order_by('distance').filter(Q(looking_for=user_gender) | Q(looking_for="BOTH")).exclude(user_id=request.user.id)
    
    
    # Filter based on sexuality preferences
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    sexuality_query = Q()
    if 's' in sexuality:
        sexuality_query.add(~Q(looking_for=F('gender')), Q.AND)
        sexuality_query.add(~Q(looking_for="BOTH"), Q.AND)
    if 'g' in sexuality:
        sexuality_query.add(Q(looking_for=F('gender')), Q.OR)
    if 'b' in sexuality:
        sexuality_query.add(Q(looking_for="BOTH"), Q.OR)

    qs = qs.filter(sexuality_query)
        
<<<<<<< HEAD
    # Filter based on height options 
    if min_height: 
        qs = qs.filter(height__gte=min_height)
    if max_height:
        qs = qs.filter(height__lte=max_height)
    
    """
    Filter results based on filter search form.
    Different search forms are used based on user's sexuality preferences i.e. 
    gender is not an option for non-bisexual users.
    """
    if request.user.profile.looking_for == "BOTH":
        filtered_result = ProfileFilter(request.GET, queryset=qs)
    else:
        gender_check = "MALE" if request.user.profile.looking_for == "MALE" else "FEMALE"
        qs = qs.filter(gender=gender_check)
        filtered_result = GenderlessProfileFilter(request.GET, queryset=qs)
    
    # Paginate search results
    search_paginated = Paginator(filtered_result.qs, 12)

    page = request.GET.get('page')
=======
    # Filter based on height options
    if min_height: 
        qs = qs.filter(height__gt=min_height)
    if max_height:
        qs = qs.filter(height__lt=max_height)
    
    # Filter based on user's gender preferences  
    if request.user.profile.looking_for == "BOTH":
        filtered_result = GenderlessProfileFilter(request.GET, queryset=qs)
    else:
        gender_check = "MALE" if request.user.profile.looking_for == "MALE" else "FEMALE"
        qs = qs.filter(gender=gender_check)
        filtered_result = ProfileFilter(request.GET, queryset=qs)
        
    search_paginated = Paginator(filtered_result.qs, 12)
    print(search_paginated)

    page = request.GET.get('page')
    # https://docs.djangoproject.com/en/1.11/topics/pagination/
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    try:
        search_page = search_paginated.page(page)
    except PageNotAnInteger:
        search_page = search_paginated.page(1)
        page = 1
    except EmptyPage:
        search_page = search_paginated.page(search_paginated.num_pages)
        page = search_paginated.num_pages
    
    context = {
<<<<<<< HEAD
        'page_ref': 'search',
=======
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
        'filtered_result': filtered_result,
        'page': page,
        'search_page': search_page,
        'min_height': min_height,
        'max_height': max_height,
        'sexuality': sexuality,
        'distance': distance
    }
        
    
    return render(request, 'search.html', context)
from django.urls import path
from .views import admin_dashboard
from . import views


urlpatterns = [
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('pending-profiles/', views.pending_profiles, name='pending_profiles'),
    path('profile/<int:profile_id>/', views.profile_detail, name='admin_profile_detail'),
    path('profile/approve/<int:profile_id>/', views.approve_profile, name='approve_profile'),
    path('profile/reject/<int:profile_id>/', views.reject_profile, name='reject_profile'),
    path('profiles/', views.ProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile-pictures/', views.profile_picture_verification_view, name='profile_picture_verification'),
    path('profile-pictures/approve/<int:user_id>/', views.approve_profile_pictures_view, name='approve_profile_pictures'),
    # other url patterns...
]

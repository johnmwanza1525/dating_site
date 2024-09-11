<<<<<<< HEAD
from django.urls import path, re_path, include
from profiles.views import logout, login, register, create_profile, member_profile, delete, verification_message
from profiles import url_reset
from . import views

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('create-profile/', create_profile, name='create_profile'),
    path('delete/', delete, name="delete"),
    path('verification-message/', verification_message, name="verification_message"),
    path('member/<int:id>/', member_profile, name='member_profile'),
    path('password-reset/', include(url_reset)),
    path('user/after/',views.after_login,name='after_login'),
]
=======
from django.conf.urls import url, include
from profiles.views import logout, login, register, user_profile, create_profile, validate_username, member_profile
from profiles import url_reset

urlpatterns = [
    url(r'^logout/', logout, name='logout'),
    url(r'^login/', login, name='login'), 
    url(r'^register/', register, name='register'),
    url(r'^create-profile/', create_profile, name='create_profile'),
    url(r'^edit/', user_profile, name="user_profile"),
    url(r'^member/(?P<id>\d+)', member_profile, name='member_profile'),
    url(r'^ajax/validate_username/$', validate_username, name='validate_username'),
    url(r'^password-reset/', include(url_reset))
]
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)

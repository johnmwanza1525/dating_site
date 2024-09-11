from django.urls import path
from . import views

urlpatterns=[
    path('password_reset/', views.password_reset, name='user_password_reset'),
    path('reset/<int:user_id>/<uuid:token>/', views.reset_password_confirm, name='reset_password_confirm'),
]

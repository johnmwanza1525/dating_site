<<<<<<< HEAD
from django.urls import path
from .views import subscribe
from . import views
urlpatterns = [
    path('', subscribe, name='subscribe'),
    path('mpesa-callback/<int:order_id>/', views.mpesa_callback, name='mpesa_callback'),

    ]
=======
from django.conf.urls import url
from .views import subscribe

urlpatterns = [
    url(r'^$', subscribe, name='subscribe')]
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)

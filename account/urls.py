<<<<<<< HEAD
from django.urls import path, re_path
from .views import account, cancel_subscription, reactivate_subscription

urlpatterns = [
    path('', account, name='account'),
    path('cancel/<str:subscription_id>/', cancel_subscription, name='cancel_subscription'),
    path('reactivate/<str:subscription_id>/', reactivate_subscription, name='reactivate_subscription')
]
=======
from django.conf.urls import url
from .views import account, cancel_subscription, reactivate_subscription

urlpatterns = [
    url(r'^$', account, name='account'),
    url(r'^cancel/(?P<subscription_id>[0-9A-Za-z_]+)$', cancel_subscription, name='cancel_subscription'),
    url(r'^reactivate/(?P<subscription_id>[0-9A-Za-z_]+)$', reactivate_subscription, name='reactivate_subscription')]
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)

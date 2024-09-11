<<<<<<< HEAD
from django.urls import path
from .views import index, preregister

urlpatterns = [
    path('', preregister, name='preregister'),
    path('home/', index, name="index"),
=======
from django.conf.urls import url
from .views import index, preregister

urlpatterns = [
    url(r'^$', preregister, name='preregister'),
    url(r'^home/', index, name="index"),
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
]

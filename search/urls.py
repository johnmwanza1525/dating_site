<<<<<<< HEAD
from django.urls import path, include
from search.views import search

urlpatterns = [
    path('', search, name="search"),
=======
from django.conf.urls import url, include
from search.views import search

urlpatterns = [
    url(r'^$', search, name="search"),
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
]

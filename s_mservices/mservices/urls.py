from django.conf.urls import url, include
from django.http import HttpResponse
from . import views

urlpatterns = [
    url(r'^get_url$', views.get_url, name='get_url'),
    url(r'^post_url$', views.post_url, name='post_url'),
]

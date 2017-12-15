from django.conf.urls import url, include
from django.http import HttpResponse
from . import views

urlpatterns = [
    url(r'^get_urls$', views.get_urls, name='get_urls'),
    url(r'^post_url$', views.post_url, name='post_url'),
    url(r'^delete_url/([0-9]+)$', views.delete_url, name='delete_url'),
    url(r'^([0-9a-zA-Z]+)', views.redirect, name='redirect'),
]

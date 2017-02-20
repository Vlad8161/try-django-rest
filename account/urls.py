from django.conf.urls import url

from account import views

urlpatterns = [
    url(r'^register$', views.register),
    url(r'^obtain-token$', views.obtain_token),
    url(r'^invalidate-token$', views.invalidate_token),
]
from django.conf.urls import url

from account import views

urlpatterns = [
    url(r'^register$', views.register),
    url(r'^obtain-token$', views.get_auth_token),
    url(r'^invalidate-token$', views.invalidate_auth_token),
]
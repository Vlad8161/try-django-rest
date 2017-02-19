from django.conf.urls import url
from rest_framework.authtoken import views as rest_views

from main import views

urlpatterns = [
    url(r'^user_profile$', views.user_profile),
    url(r'^obtain_token$', rest_views.obtain_auth_token)
]

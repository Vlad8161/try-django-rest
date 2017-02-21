from django.conf.urls import url
from rest_framework.authtoken import views as rest_views

from main import views

urlpatterns = [
    url(r'^profile$', views.profile),
    url(r'^profile/(?P<pk>[0-9]{1,10})$', views.profile),
    url(r'^add-friend/(?P<friend_id>[0-9]{1,10})$', views.add_friend),
]

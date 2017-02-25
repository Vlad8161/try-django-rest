from django.conf.urls import url
from rest_framework.authtoken import views as rest_views

from main import views

urlpatterns = [
    url(r'^profile$', views.profile),
    url(r'^profile/(?P<pk>[0-9]{1,10})$', views.profile),
    url(r'^update-profile$', views.update_profile),
    url(r'^add-friend/(?P<user_profile_id>[0-9]{1,10})$', views.add_friend),
    url(r'^remove-friend/(?P<friend_id>[0-9]{1,10})$', views.remove_friend),
    url(r'^incoming-friend-requests', views.get_incoming_friend_requests),
    url(r'^outgoing-friend-requests', views.get_outgoing_friend_requests),
]

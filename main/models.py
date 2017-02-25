from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    account = models.OneToOneField(User)
    friends = models.ManyToManyField('self', symmetrical=False)


class FriendRequest(models.Model):
    user_from = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='outgoing_requests')
    user_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='incoming_requests')
    already_seen = models.BooleanField(default=False)

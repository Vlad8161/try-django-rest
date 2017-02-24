from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    account = models.OneToOneField(User)
    friends = models.ManyToManyField("self", symmetrical=False)

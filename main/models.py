from django.db import models


class UserProfile(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)


import binascii
import os

from django.contrib.auth.models import User
from django.db import models


class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created = models.DateTimeField(auto_now_add=True)
    last_use = models.DateTimeField(default=None, null=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = binascii.hexlify(os.urandom(20)).decode()
        return super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return self.key

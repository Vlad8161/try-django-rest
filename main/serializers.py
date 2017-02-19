from rest_framework import serializers

from main import models


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'first_name', 'last_name')


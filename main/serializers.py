from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import UserProfile


class FriendSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='account.email')
    username = serializers.CharField(source='account.username')
    first_name = serializers.CharField(source='account.first_name')
    last_name = serializers.CharField(source='account.last_name')

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='account.email')
    username = serializers.CharField(source='account.username')
    first_name = serializers.CharField(source='account.first_name')
    last_name = serializers.CharField(source='account.last_name')
    friends = FriendSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'friends')


class UpdateProfileSerializer(serializers.Serializer):
    email = serializers.EmailField()
    User
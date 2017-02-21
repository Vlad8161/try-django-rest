from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import UserProfile


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'account')

    account = AccountSerializer(read_only=True, many=False)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'account', 'friends')

    account = AccountSerializer(many=False, read_only=True)
    friends = FriendSerializer(many=True, read_only=True)

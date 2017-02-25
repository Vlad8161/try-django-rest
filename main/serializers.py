from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import UserProfile, FriendRequest


class FriendSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='account.email')
    username = serializers.CharField(source='account.username')
    first_name = serializers.CharField(source='account.first_name')
    last_name = serializers.CharField(source='account.last_name')

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class IncomingFriendRequestSerializer(serializers.ModelSerializer):
    user_from = FriendSerializer()

    class Meta:
        model = FriendRequest
        fields = ('id', 'user_from')


class OutgoingFriendRequestSerializer(serializers.ModelSerializer):
    user_to = FriendSerializer()

    class Meta:
        model = FriendRequest
        fields = ('id', 'user_to')


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
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=30, allow_blank=True, required=True)
    last_name = serializers.CharField(max_length=30, allow_blank=True, required=True)

    def update(self, instance, validated_data):
        user = instance.account
        user.email = validated_data.get('email')
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.save()
        return instance

    def create(self, validated_data):
        pass

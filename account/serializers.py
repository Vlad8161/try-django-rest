from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=40)
    password2 = serializers.CharField(max_length=40)
    username = serializers.CharField(max_length=40)
    first_name = serializers.CharField(max_length=40, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(max_length=40, allow_null=True, allow_blank=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords are not equal')
        return super(RegistrationSerializer, self).validate(data)

    def validate_username(self, value):
        users = User.objects.filter(username=value)
        if len(users) != 0:
            raise serializers.ValidationError('User ' + value + ' already exists')

        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=40)
    password = serializers.CharField(max_length=40)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


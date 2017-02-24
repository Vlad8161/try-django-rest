from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from account.models import Token


class PasswordAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.data.get('username')
        if username is None:
            raise AuthenticationFailed('No username was provided')

        password = request.data.get('password')
        if password is None:
            raise AuthenticationFailed('No password was provided')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('No such user')
        except User.MultipleObjectsReturned:
            raise AuthenticationFailed('Too many users for one username :)')

        if not check_password(password, user.password):
            raise AuthenticationFailed('Invalid password')

        return user, None


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            key = request.META['token']
        except KeyError:
            raise AuthenticationFailed('No token provided')

        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return token.user, token

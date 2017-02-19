from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class MyAuthentication(BaseAuthentication):
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

        if user.password != password:
            raise AuthenticationFailed('Invalid password')

        return user, None



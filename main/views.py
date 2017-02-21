from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.authentication import TokenAuthentication
from main.models import UserProfile
from main.serializers import UserProfileSerializer


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def profile(request, pk=None):
    if pk is None:
        user_profile = UserProfile.objects.get(account=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
    else:
        try:
            user_profile = UserProfile.objects.get(pk=pk)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def add_friend(request, friend_id):
    try:
        friend = UserProfile.objects.get(pk=friend_id)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user_profile = UserProfile.objects.get(account=request.user)
    user_profile.friends.add(friend)
    user_profile.save()
    return Response(status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.authentication import TokenAuthentication
from main.models import UserProfile
from main.serializers import UserProfileSerializer, UpdateProfileSerializer


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def profile(request, pk=None):
    try:
        if pk is None:
            user_profile = UserProfile.objects.get(account=request.user)
            serializer = UserProfileSerializer(user_profile)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            user_profile = UserProfile.objects.get(pk=pk)
            serializer = UserProfileSerializer(user_profile)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def update_profile(request):
    try:
        user_profile = UserProfile.objects.get(account=request.user)
        serializer = UpdateProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def add_friend(request, user_profile_id):
    try:
        user_profile = UserProfile.objects.get(account=request.user)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if int(user_profile.id) == int(user_profile_id):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        friend = UserProfile.objects.get(pk=user_profile_id)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user_profile.friends.add(friend)
    user_profile.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def remove_friend(request, friend_id):
    try:
        friend = UserProfile.objects.get(pk=friend_id)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        user_profile = UserProfile.objects.get(account=request.user)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user_profile.friends.remove(friend)
    user_profile.save()
    return Response(status=status.HTTP_200_OK)

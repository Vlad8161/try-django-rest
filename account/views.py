from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.authentication import PasswordAuthentication, TokenAuthentication
from account.models import Token
from account.serializers import RegistrationSerializer


@api_view(['POST'])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((PasswordAuthentication,))
@permission_classes((IsAuthenticated,))
def obtain_token(request):
    token = Token()
    token.user = request.user
    token.save()
    return Response({'token': token.key})


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def invalidate_token(request):
    token = request.auth
    token.delete()
    return Response(status=status.HTTP_200_OK)

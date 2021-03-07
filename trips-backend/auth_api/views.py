from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from auth_api.serializers import RegisterSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_auth(request):
    serialized = RegisterSerializer(data=request.data)
    if serialized.is_valid():
        User.objects.create_user(**serialized.data)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

# Imports for django rest framework
from ekratia.users.serializers import UserSerializer
from ekratia.users.models import User
from rest_framework import generics
from rest_framework import permissions


class UserView(generics.RetrieveAPIView):
    """
    API User details Endpoint
    """
    permission_classes = (permissions.IsAuthenticated,)
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()

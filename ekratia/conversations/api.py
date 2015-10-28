# Imports for django rest framework
from .serializers import ThreadSerializer

from rest_framework import generics
from rest_framework import permissions

from .models import Thread


class ThreadList(generics.ListCreateAPIView):
    """
    API class to list all threads, or create a new thread.
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class ThreadDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API class to retrieve, update or delete a thread instance.
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

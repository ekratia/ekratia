# Imports for django rest framework
from rest_framework import generics
from rest_framework import permissions
from .models import Thread
from .serializers import ThreadSerializer


class ThreadList(generics.ListCreateAPIView):
    """
    API class to list all threads, or create a new thread.
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Thread.objects.all().order_by('-num_comments')
    serializer_class = ThreadSerializer
    paginate_by = 5


class ThreadDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API class to retrieve, update or delete a thread instance.
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class ThreadsTrendingList(generics.ListAPIView):
    queryset = Thread.objects.all().order_by('-num_comments')
    serializer_class = ThreadSerializer
    paginate_by = 5

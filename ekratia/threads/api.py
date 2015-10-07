# Imports for django rest framework
from .serializers import ThreadSerializer
from .serializers import CommentSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

from .models import Thread, Comment


class ThreadList(generics.ListCreateAPIView):
    """
    API class to list all threads, or create a new thread.
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class ThreadDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API class to retrieve, update or delete a thread instance.
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class CommentList(generics.ListCreateAPIView):
    """
    API class for list all comments from a thread, or create a new comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API class to retrieve, update or delete a comment instance.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ThreadComments(APIView):
    """
    List Comments of the thread in a Tree
    """

    def get_thread(self, pk):
        try:
            return Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        thread = self.get_thread(pk)
        root_comment = Comment.objects.get(thread=thread)
        data = Comment.dump_bulk(parent=root_comment)
        return Response(data)

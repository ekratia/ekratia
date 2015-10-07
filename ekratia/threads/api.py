# Imports for django rest framework
from .serializers import ThreadSerializer
from .serializers import CommentSerializer
from .serializers import CommentThreadSerializer

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

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
        try:
            thread = self.get_thread(pk)
            root_comment = Comment.objects.get(thread=thread)
            data = Comment.dump_bulk(parent=root_comment)
        except Http404:
            return Response({'message': 'Thread not found'},
                            status=status.HTTP_404_NOT_FOUND)

        return Response(data)

    def post(self, request, pk, format=None):
        """
        Method to create new comment for the current Thread
        """
        try:
            thread = self.get_thread(pk)
        except Http404:
            return Response({'message': 'Thread not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = CommentThreadSerializer(data=request.data)
        if serializer.is_valid():
            parent_id = serializer.data['parent']
            if(parent_id):
                node = Comment.objects.get(pk=parent_id)
            else:
                node = Comment.objects.get(thread=thread)

            node.add_child(content=serializer.data['content'],
                           user_id=request.user.id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

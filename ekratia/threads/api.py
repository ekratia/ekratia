# Imports for django rest framework
from .serializers import CommentSerializer
from .serializers import CommentThreadSerializer
from .serializers import CommentVoteSerializer

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from django.http import Http404

from .models import Comment, CommentUserVote

from ekratia.users.models import User


class CommentList(generics.ListCreateAPIView):
    """
    API class for list all comments from a thread, or create a new comment.
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API class to retrieve, update or delete a comment instance.
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ThreadComments(APIView):
    """
    List Comments of the thread in a Tree
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_thread(self, pk):
        """
        Get Thread by Primary Key
        """
        try:
            return Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            raise Http404

    def create_root_comment(self, thread):
        """
        Creates a root Comment
        """
        root_comment = Comment.add_root(content=thread.description,
                                        user_id=thread.user.id)
        thread.comment = root_comment
        thread.save()
        return root_comment

    def update_information_from_tree(self, tree):
        """
        Recursive function to go through tree and update information
        Updating: User information, Vote value
        """
        for element in tree:
            user_id = element['data']['user']
            comment_id = element['id']
            # TODO: Avoid a queryset per user
            # Get all the user info in single query
            user = User.objects.get(pk=user_id)
            element['data']['user'] = user.get_data_dictionary()

            if self.request.user.is_authenticated():
                current_user_id = self.request.user.id
                try:
                    vote = CommentUserVote.objects.get(comment_id=comment_id,
                                                       user_id=current_user_id)
                    vote_value = vote.value
                except CommentUserVote.DoesNotExist:
                    vote_value = 0
                element['data']['current_user_vote'] = vote_value

            if 'children' in element:
                self.update_information_from_tree(element['children'])
        return tree

    def get(self, request, pk, format=None):
        """
        Lists the tree of comments for the thread
        """
        try:
            thread = self.get_thread(pk)
        except Http404:
            return Response({'message': 'Thread not found'},
                            status=status.HTTP_404_NOT_FOUND)
        if thread.comment:
            root_comment = thread.comment
        else:
            root_comment = self.create_root_comment(thread=thread)
            thread.comment = root_comment
            thread.save()

        data = Comment.dump_bulk(parent=root_comment)
        data = self.update_information_from_tree(data)
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
                node = thread.comment

            node.add_child(content=serializer.data['content'],
                           user_id=request.user.id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThreadCommentsVotes(APIView):
    """
    List Comments of the thread in a Tree
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_comment(self, pk):
        """
        Get Thread by Primary Key
        """
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        """
        Method to create or update vote for comment
        """

        serializer = CommentVoteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                comment = self.get_comment(serializer.data['comment'])
                vote, created = CommentUserVote.objects.get_or_create(
                                            comment=comment, user=request.user)
                if created:
                    vote.value = serializer.data['value']
                    vote.save()
                else:
                    if(vote.value != serializer.data['value']):
                        vote.value = serializer.data['value']
                        vote.save()
                    else:
                        vote.delete()

                total_points = comment.calculate_votes()
            except Comment.DoesNotExist:
                return Response({'message': 'Comment not found'},
                                status=status.HTTP_404_NOT_FOUND)

            serializer.data['total_points'] = total_points

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

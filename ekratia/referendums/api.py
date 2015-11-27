# Imports for django rest framework
from ekratia.threads.serializers import CommentThreadSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework import permissions

from django.http import Http404

from ekratia.threads.models import Comment, CommentUserVote
from .models import Referendum
from .serializers import ReferendumSerializer

from ekratia.users.models import User

from ekratia.core.email import notify_comment_node
import logging

logger = logging.getLogger('ekratia')


class ReferendumsList(generics.ListAPIView):
    queryset = Referendum.objects.all().order_by('-num_comments')
    serializer_class = ReferendumSerializer
    paginate_by = 5


class ReferendumComments(APIView):
    """
    List Comments of the referendum in a Tree
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_referendum(self, pk):
        """
        Get Referendum by Primary Key
        """
        try:
            return Referendum.objects.get(pk=pk)
        except Referendum.DoesNotExist:
            raise Http404

    def create_root_comment(self, referendum):
        """
        Creates a root Comment
        """
        root_comment = Comment.add_root(content='referendum',
                                        user_id=referendum.user.id)
        referendum.comment = root_comment
        referendum.save()
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
            referendum = self.get_referendum(pk)
        except Http404:
            return Response({'message': 'Referendum not found'},
                            status=status.HTTP_404_NOT_FOUND)
        if referendum.comment:
            root_comment = referendum.comment
        else:
            root_comment = self.create_root_comment(referendum)
            referendum.comment = root_comment
            referendum.save()

        data = Comment.dump_bulk(parent=root_comment)
        data = self.update_information_from_tree(data)
        return Response(data)

    def post(self, request, pk, format=None):
        """
        Method to create new comment for the current Referendum
        """
        try:
            referendum = self.get_referendum(pk)
        except Http404:
            return Response({'message': 'Referendum not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = CommentThreadSerializer(data=request.data)
        if serializer.is_valid():
            parent_id = serializer.data['parent']
            if(parent_id):
                node = Comment.objects.get(pk=parent_id)
            else:
                node = referendum.comment

            node.add_child(content=serializer.data['content'],
                           user_id=request.user.id)

            notify_comment_node(request, node, 'referendum')

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReferendumVoteGraph(APIView):
    def get(self, request, pk, format=None):
        referendum = Referendum.objects.get(pk=pk)
        graph = referendum.get_graph()
        return Response(graph.get_sigma_representation())

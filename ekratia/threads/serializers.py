from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializaer for Comment Model
    """
    class Meta:
        model = Comment


class CommentThreadSerializer(serializers.Serializer):
    """
    Serializer for Comment Model
    """
    content = serializers.CharField()
    parent = serializers.IntegerField(allow_null=True)


class CommentVoteSerializer(serializers.Serializer):
    """
    Serializer for CommentVote Model
    """
    comment = serializers.IntegerField()
    value = serializers.IntegerField(min_value=-1, max_value=1)

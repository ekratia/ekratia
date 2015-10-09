from rest_framework import serializers
from .models import Thread
from .models import Comment


class ThreadSerializer(serializers.ModelSerializer):
    """
    Serializaer for Thread Model
    """
    slug = serializers.SlugField(allow_blank=True, read_only=True)

    class Meta:
        model = Thread


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

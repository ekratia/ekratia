from rest_framework import serializers
from .models import Thread
from .models import Comment


class ThreadSerializer(serializers.ModelSerializer):
    """
    Serializaer for Thread Model
    Class required to convert python objects to JSON.
    """
    slug = serializers.SlugField(allow_blank=True, read_only=True)

    class Meta:
        model = Thread


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializaer for Comment Model
    Class required to convert python objects to JSON.
    """
    class Meta:
        model = Comment


class CommentThreadSerializer(serializers.Serializer):
    """
    Serializer for Comment Model
    Class required to convert python objects to JSON.
    """
    content = serializers.CharField()
    # user = serializers.IntegerField()
    parent = serializers.IntegerField(allow_null=True)

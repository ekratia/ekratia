from rest_framework import serializers
from .models import Thread
from .models import Comment


class ThreadSerializer(serializers.ModelSerializer):
    """
    Serializaer for Thread Model
    Class required to convert python objects to JSON.
    """
    class Meta:
        model = Thread
        fields = ('id', 'title', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializaer for Thread Model
    Class required to convert python objects to JSON.
    """
    class Meta:
        model = Comment
        fields = ('id', 'content', 'thread', 'user', 'depth')

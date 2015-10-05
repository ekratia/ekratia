from rest_framework import serializers
from .models import Thread
from .models import Comment
from django.db import models


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
    Serializaer for Thread Model
    Class required to convert python objects to JSON.
    """
    class Meta:
        model = Comment

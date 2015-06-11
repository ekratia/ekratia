from django.forms import widgets
from rest_framework import serializers
from .models import Thread
from .models import Comment

#Class required to convert python objects to JSON. Is usted by the API, under django-rest-framework
class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ('id', 'title', 'description')

#Class required to convert python objects to JSON. Is usted by the API, under django-rest-framework
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'thread','user','depth')

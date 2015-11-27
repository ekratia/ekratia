from rest_framework import serializers
from .models import Thread


class ThreadSerializer(serializers.ModelSerializer):
    """
    Serializaer for Thread Model
    """
    slug = serializers.SlugField(allow_blank=True, read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Thread

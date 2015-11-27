from rest_framework import serializers
from .models import Referendum


class ReferendumSerializer(serializers.ModelSerializer):
    """
    Serializaer for Referendum Model
    """
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Referendum

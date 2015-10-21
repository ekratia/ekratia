from rest_framework import serializers
from .models import Delegate


class UserDelegateSerializer(serializers.ModelSerializer):
    """
    Serializer for UserDelegate Model
    """
    class Meta:
        model = Delegate
        fields = ('id', 'delegate',)

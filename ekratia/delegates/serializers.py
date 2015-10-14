from rest_framework import serializers
from .models import Delegate

from ekratia.users.serializers import UserSerializer


class UserDelegateSerializer(serializers.ModelSerializer):
    """
    Serializer for UserDelegate Model
    """
    class Meta:
        model = Delegate
        fields = ('id', 'delegate',)


class UserDelegateListSerializer(UserDelegateSerializer):
    """
    Serializer for UserDelegate Model
    """
    delegate = UserSerializer()

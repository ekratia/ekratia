from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User Model
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)

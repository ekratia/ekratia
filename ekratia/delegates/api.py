# Imports for django rest framework
from .serializers import UserDelegateSerializer
from ekratia.users.serializers import UserSerializer
from ekratia.users.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin
from rest_framework import status
from rest_framework import permissions


from .models import Delegate


class UserDelegates(ListModelMixin, generics.GenericAPIView):
    """
    API class for User Delegates
    """
    permission_classes = (permissions.IsAuthenticated,)
    model = User
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(
                    id__in=Delegate.objects.filter(user=self.request.user)
                           .values_list('delegate_id'))

    def post(self, request):
        serializer = UserDelegateSerializer(data=request.data)

        if(serializer.is_valid()):
            delegate, created = Delegate.objects.get_or_create(
                delegate_id=serializer.data['delegate'],
                user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

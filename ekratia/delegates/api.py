# Imports for django rest framework
from .serializers import UserDelegateSerializer
from ekratia.users.serializers import UserSerializer
from ekratia.users.models import User
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.http import Http404

from .models import Delegate


class AssignedDelegates(mixins.ListModelMixin, generics.GenericAPIView):
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


class AvailableDelegates(generics.ListAPIView):
    """
    API class for Users Listing
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Lists the users of the system
        name: Optional name to filter the user
        """
        queryset = User.objects.exclude(
                        id__in=Delegate.objects.filter(user_id=1)
                        .values_list('delegate_id'))\
                       .exclude(id=self.request.user.id)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(username__icontains=name)
        return queryset


class UserDelegateDetail(generics.GenericAPIView):
    """
    Delegate Detail View Class
    """
    queryset = Delegate.objects.all()
    serializer_class = UserDelegateSerializer

    def get_delegate(self, delegate_id):
        try:
            delegate = Delegate.objects.get(delegate_id=delegate_id,
                                            user=self.request.user)
        except Delegate.DoesNotExist:
            raise Http404
        return delegate

    def get(self, request, *args, **kwargs):
        delegate_id = self.kwargs.get('delegate_id')
        delegate = self.get_delegate(delegate_id)
        serializer = UserDelegateSerializer(delegate)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        delegate_id = self.kwargs.get('delegate_id')
        try:
            delegate = self.get_delegate(delegate_id)
        except Http404:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        delegate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

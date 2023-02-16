from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response

from rest_framework.decorators import action

from .serializers import UserSerializer
from .models import User

class UserCreateView(CreateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class UserViewSet(ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserOneViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class UserUpdateViewSet(UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'

    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)



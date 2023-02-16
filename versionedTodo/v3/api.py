
from tasks.models import Todo
from .serializers import TodoSerializer
from .pagination import CustomPagination

from django.shortcuts import get_object_or_404

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 


class TodoViewSet(GenericViewSet):
    queryset = Todo.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        return TodoSerializer

    def list(self, request):
        page = self.paginate_queryset(self.queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        todo = get_object_or_404(Todo, pk=pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_200_OK)


    def update(self, request, pk=None):
        todo = get_object_or_404(Todo, pk=pk)
        serializer = self.get_serializer(todo, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_200_OK)


    def partial_update(self, request, pk=None):
        todo = get_object_or_404(Todo, pk=pk)
        serializer = self.get_serializer(todo, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
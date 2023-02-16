from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import status


from django.shortcuts import get_object_or_404

from .pagination import CustomPagination
from .models import Todo
from .serializers import TodoSerializer

class TodoViewSet(GenericViewSet):
    queryset = Todo.objects.all()
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = (IsAuthenticated, )
   # ordering_fields = ['id']
    ordering = ('-id', )
    search_fields = ['title']

    def get_serializer_class(self, *args, **kwargs):
        return TodoSerializer

    def list(self, request):
        queryset = self.filter_queryset(self.queryset)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        if isinstance(request.data, list):
            serializer = TodoSerializer(data=request.data, many=True)
        else:
            serializer = TodoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        serializer = TodoSerializer(todo, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            

    def partial_update(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        serializer = TodoSerializer(todo, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.deleted()
        return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Resource
from .serializers import ResourceSerializer, ResourceCreateSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return ResourceCreateSerializer
        return ResourceSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = Resource.objects.select_related('created_by').all()
        # Filter by category if provided
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    @action(detail=False, methods=['get'])
    def my_resources(self, request):
        """Get resources created by the current user"""
        resources = self.get_queryset().filter(created_by=request.user)
        serializer = self.get_serializer(resources, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all available categories"""
        categories = Resource.CATEGORY_CHOICES
        return Response([
            {'value': choice[0], 'label': choice[1]} 
            for choice in categories
        ])

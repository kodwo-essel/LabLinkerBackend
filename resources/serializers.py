from rest_framework import serializers
from .models import Resource
from auth_app.serializers import UserSerializer


class ResourceSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Resource
        fields = [
            'id', 'title', 'description', 'category', 
            'image_url', 'link', 'created_by', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class ResourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'category', 'image_url', 'link'] 
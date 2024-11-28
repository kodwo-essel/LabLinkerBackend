from rest_framework import serializers
from .models import Post, PostFile, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class PostFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFile
        fields = ['id', 'file', 'uploaded_at']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    files = PostFileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'tags', 'files', 
            'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post

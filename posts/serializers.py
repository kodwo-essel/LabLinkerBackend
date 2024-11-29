from rest_framework import serializers

from likes.models import Like
from .models import Post, PostFile, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class PostFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFile
        fields = ['file']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50), 
        write_only=True, 
        required=False
    )
    tag_names = serializers.SerializerMethodField()
    files = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    uploaded_files = PostFileSerializer(many=True, read_only=True, source='files')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 
            'tags', 'tag_names', 'files', 'uploaded_files', 'likes_count',
            'created_at', 'updated_at'
        ]

    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
    def get_likes_count(self, obj):
        return Like.objects.filter(post=obj).count()

    def create(self, validated_data):
        # Handle tags
        tag_names = validated_data.pop('tags', [])
        
        # Handle files
        files_data = validated_data.pop('files', [])
        
        # Create post
        post = Post.objects.create(**validated_data)
        
        # Create tags
        if tag_names:
            tags = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)
            post.tags.set(tags)
        
        # Create files
        for file in files_data:
            PostFile.objects.create(post=post, file=file)
        
        return post

    def update(self, instance, validated_data):
        # Handle tags
        tag_names = validated_data.pop('tags', None)
        
        # Handle files
        files_data = validated_data.pop('files', None)
        
        # Update post fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update tags
        if tag_names is not None:
            tags = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)
            instance.tags.set(tags)
        
        # Update files
        if files_data:
            # Optional: Remove existing files if you want to replace all
            # instance.files.all().delete()
            
            # Add new files
            for file in files_data:
                PostFile.objects.create(post=instance, file=file)
        
        return instance
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

    def create(self, validated_data):
        """ Custom method to create a new tag """
        tag = Tag.objects.create(**validated_data)
        return tag
from rest_framework import serializers

from auth_app.serializers import UserSerializer
from likes.models import Like
from .models import Post, PostFile, Tag, Category, Bookmark
from comments.models import Comment

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'color']

class PostFileSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(use_url=True)
    file_url = serializers.SerializerMethodField()

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url  # Cloudinary provides the full URL
        return None
    
    class Meta:
        model = PostFile
        fields = ['file', 'file_url']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Use a nested serializer for the user
    category = CategorySerializer(read_only=True)
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
    comment_count = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'content', 'author', 'category',
            'tags', 'tag_names', 'files', 'uploaded_files', 
            'likes_count', 'liked_by', 'comment_count', 'is_bookmarked',
            'created_at', 'updated_at'
        ]

    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
    def get_likes_count(self, obj):
        return Like.objects.filter(post=obj).count()
    
    def get_comment_count(self, obj):
        return Comment.objects.filter(post=obj).count()
    
    def get_liked_by(self, obj):
        return Like.objects.filter(post=obj).values_list('user_id', flat=True)

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Bookmark.objects.filter(user=request.user, post=obj).exists()
        return False

    def create(self, validated_data):
        tag_names = validated_data.pop('tags', [])
        files_data = validated_data.pop('files', [])
        
        post = Post.objects.create(**validated_data)
        
        if tag_names:
            tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names]
            post.tags.set(tags)

        for file in files_data:
            PostFile.objects.create(post=post, file=file)
        
        return post

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tags', None)
        files_data = validated_data.pop('files', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tag_names is not None:
            tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names]
            instance.tags.set(tags)

        if files_data:
            for file in files_data:
                PostFile.objects.create(post=instance, file=file)

        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Manually pass the request context to ProductImageSerializer
        for file_data in representation.get('files', []):
            file_data['file_url'] = self.context['request'].build_absolute_uri(file_data.get('image', ''))

        return representation

class BookmarkSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Bookmark
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']
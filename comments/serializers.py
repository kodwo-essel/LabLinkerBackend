from rest_framework import serializers

from auth_app.serializers import UserSerializer
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at', 'parent', 'replies']
        read_only_fields = ['author', 'created_at', 'updated_at']

    def get_replies(self, obj):
        """Retrieve replies to the comment."""
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

from rest_framework import serializers

from auth_app.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    def get_avatar_url(self, obj):
        return obj.avatar.url if obj.avatar else None
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'profession', 'country','avatar', 'avatar_url']

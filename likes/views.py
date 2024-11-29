from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Like
from posts.models import Post


class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({"message": "Post unliked."}, status=status.HTTP_200_OK)

        return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)


class PostLikesView(APIView):

    def get(self, request, post_id, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        likes = Like.objects.filter(post=post)
        users = [like.user.username for like in likes]
        return Response({"post_id": post_id, "likes": users}, status=status.HTTP_200_OK)
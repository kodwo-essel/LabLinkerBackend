from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        """ Get all posts """
        try:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        """ Create a new post """
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """ Set the author to the current user """
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'  # Use 'id' as the lookup field in the model

    def get(self, request, post_id, *args, **kwargs):
        """ Get a single post by post_id """
        try:
            post = Post.objects.get(id=post_id)  # Use post_id to get the post based on 'id' field
            serializer = self.get_serializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise NotFound(detail=f"Post with id {post_id} not found.")

    def patch(self, request, post_id, *args, **kwargs):
        """ Partial update a post """
        try:
            post = Post.objects.get(id=post_id)  # Use post_id to get the post based on 'id' field
            if post.author != request.user:
                raise PermissionDenied("You are not allowed to update this post.")
            serializer = self.get_serializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            raise NotFound(detail=f"Post with id {post_id} not found.")
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, post_id, *args, **kwargs):
        """ Full update a post (allowed only by the creator) """
        return self.patch(request, post_id, *args, **kwargs)

    def delete(self, request, post_id, *args, **kwargs):
        """ Delete a post (allowed by creator or admin) """
        try:
            post = Post.objects.get(id=post_id)  # Use post_id to get the post based on 'id' field
            if request.user != post.author and not request.user.is_staff:
                raise PermissionDenied("You are not allowed to delete this post.")
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            raise NotFound(detail=f"Post with id {post_id} not found.")
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        """ Perform the update operation """
        serializer.save()


from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Category, Bookmark
from .serializers import PostSerializer, CategorySerializer, BookmarkSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        """ Get all posts """
        try:
            posts = Post.objects.all().order_by('-created_at')
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

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookmarkPostView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            post=post
        )
        
        if created:
            return Response({"detail": "Post bookmarked successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Post already bookmarked."}, status=status.HTTP_400_BAD_REQUEST)

class UnbookmarkPostView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            bookmark = Bookmark.objects.get(user=request.user, post=post)
            bookmark.delete()
            return Response({"detail": "Post unbookmarked successfully."}, status=status.HTTP_200_OK)
        except Bookmark.DoesNotExist:
            return Response({"detail": "Post not bookmarked."}, status=status.HTTP_400_BAD_REQUEST)

class UserBookmarksView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

class PostsByCategoryView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Post.objects.filter(category_id=category_id)

class UserFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Get posts from users that the current user follows
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users)


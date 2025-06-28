from django.urls import path
from .views import (
    PostListCreateView, PostDetailView, CategoryListView, CategoryDetailView,
    BookmarkPostView, UnbookmarkPostView, UserBookmarksView, 
    PostsByCategoryView, UserFeedView
)

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
    
    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:category_id>/posts/', PostsByCategoryView.as_view(), name='posts-by-category'),
    
    # Bookmark URLs
    path('bookmark/<int:post_id>/', BookmarkPostView.as_view(), name='bookmark-post'),
    path('unbookmark/<int:post_id>/', UnbookmarkPostView.as_view(), name='unbookmark-post'),
    path('bookmarks/', UserBookmarksView.as_view(), name='user-bookmarks'),
    
    # User feed
    path('feed/', UserFeedView.as_view(), name='user-feed'),
]

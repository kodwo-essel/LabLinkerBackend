from django.urls import path
from .views import CommentListCreateView, CommentDetailView

urlpatterns = [
    path('posts/<int:post_id>/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('', CommentListCreateView.as_view(), name='comment-create'),
    path('<int:comment_id>/', CommentDetailView.as_view(), name='comment-detail'),
]

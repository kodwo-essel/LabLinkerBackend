from django.urls import path
from .views import LikeToggleView, PostLikesView

urlpatterns = [
    path('posts/<int:post_id>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('posts/<int:post_id>/', PostLikesView.as_view(), name='post-likes'),
]

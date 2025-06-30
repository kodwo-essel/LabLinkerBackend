from django.urls import path
from .views import (
    OTPAuthenticationView, OTPVerifyView, EmailPasswordAuthView, 
    PasswordResetView, SignupView, FollowUserView, UnfollowUserView,
    UserFollowersView, UserFollowingView
)

urlpatterns = [
    path('otp-auth/', OTPAuthenticationView.as_view(), name='otp-auth'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('login/', EmailPasswordAuthView.as_view(), name='email-password-auth'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    
    # Follow system URLs
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('users/<int:user_id>/followers/', UserFollowersView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', UserFollowingView.as_view(), name='user-following'),
]

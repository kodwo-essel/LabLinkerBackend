from django.urls import path
from .views import OTPAuthenticationView, OTPVerifyView, EmailPasswordAuthView, PasswordResetView, SignupView

urlpatterns = [
    path('otp-auth/', OTPAuthenticationView.as_view(), name='otp-auth'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('login/', EmailPasswordAuthView.as_view(), name='email-password-auth'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
]

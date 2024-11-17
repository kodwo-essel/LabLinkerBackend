from django.urls import path
from .views import OTPAuthenticationView, OTPVerifyView, EmailPasswordAuthView, SignupView

urlpatterns = [
    path('otp-auth/', OTPAuthenticationView.as_view(), name='otp-auth'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('email-password-auth/', EmailPasswordAuthView.as_view(), name='email-password-auth'),
    path('signup/', SignupView.as_view(), name='signup'),
]

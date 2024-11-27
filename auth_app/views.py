from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from .models import OTP
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated 



# Generate OTP and send via email
class OTPAuthenticationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        #user, created = get_user_model().objects.get_or_create(email=email)

        user, created = get_user_model().objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0]
            })

        otp_code = get_random_string(length=6, allowed_chars='1234567890')
        otp_expiration = timezone.now() + timedelta(minutes=5)

        otp_entry = OTP.objects.create(user=user, code=otp_code, expires_at=otp_expiration)

        # Send OTP via email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return Response({"detail": "OTP sent to email."}, status=status.HTTP_200_OK)

class OTPVerifyView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"detail": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_user_model().objects.filter(email=email).first()
        if not user:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        otp_entry = OTP.objects.filter(user=user, code=otp).first()

        if not otp_entry or otp_entry.expires_at < timezone.now():
            return Response({"detail": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            "access": str(access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)


class SignupView(APIView):
    def post(self, request):
        # Extract email and password from request
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {"detail": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate if the email is already taken
        if get_user_model().objects.filter(email=email).exists():
            return Response(
                {"detail": "A user with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create the user
        try:
            user = get_user_model().objects.create_user(
                username=email,  # Assuming username = email for simplicity
                email=email,
                password=password
            )
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "detail": "Signup successful.",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            status=status.HTTP_201_CREATED
        )

class EmailPasswordAuthView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            "access": str(access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
    

class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        # get user from request
        user = request.user

        if not current_password or not new_password:
            return Response({"detail": "Current password and new password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if current password is correct
        if not user.check_password(current_password):
            return Response({"detail": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        # update password
        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)


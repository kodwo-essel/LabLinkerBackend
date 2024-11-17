from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

class GetAllUsersView(APIView):
    def get(self, request):
        users = get_user_model().objects.all()  # Fetch all users
        user_data = [{"id": user.id, "email": user.email, "username": user.username} for user in users]
        return Response(user_data, status=status.HTTP_200_OK)


class GetUserByIdView(APIView):
    def get(self, request, user_id):
        try:
            user = get_user_model().objects.get(id=user_id)  # Fetch user by ID
            user_data = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                # Add any other fields you want to include
            }
            return Response(user_data, status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            raise NotFound(detail="User not found.")

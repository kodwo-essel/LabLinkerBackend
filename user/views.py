from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated 

class GetAllUsersView(APIView):
    def get(self, request):
        users = get_user_model().objects.all()  # Fetch all users
        serializer = UserSerializer(users, many=True)  # Serialize the users
        return Response(serializer.data, status=status.HTTP_200_OK)    


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        try:
            user = get_user_model().objects.get(id=user_id)  # Fetch user by ID
            serializer = UserSerializer(user)  # Serialize the single user
            return Response(serializer.data, status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            raise NotFound(detail="User not found.")
        

    def patch(self, request, user_id):
        try:
            user = get_user_model().objects.get(id=user_id)  # Fetch user by ID
        except get_user_model().DoesNotExist:
            raise NotFound(detail="User not found.")
        
        serializer = UserSerializer(user, data=request.data, partial=True)  # Use partial=True for partial updates
        if serializer.is_valid():
            serializer.save()  # Save the updated user
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        try:
            user = get_user_model().objects.get(id=user_id)  # Fetch user by ID
            user.delete()  # Delete the user
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except get_user_model().DoesNotExist:
            raise NotFound(detail="User not found.")
    
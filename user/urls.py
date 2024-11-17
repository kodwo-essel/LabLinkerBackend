from django.urls import path
from .views import GetAllUsersView, UserView

urlpatterns = [
    path('', GetAllUsersView.as_view(), name='get_all_users'),  # List all users
    path('<int:user_id>/', UserView.as_view(), name='get_user_by_id'),  # Fetch a user by ID
]

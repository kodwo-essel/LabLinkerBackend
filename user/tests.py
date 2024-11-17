# tests.py in your 'user' app
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class UserViewsTestCase(TestCase):
    
    def setUp(self):
        # Create a test user and generate token for authentication
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com', password='testpassword123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_get_all_users_authenticated(self):
        # Test that an authenticated user can get a list of all users
        url = reverse('user-list')  # Assuming you have this named in urls
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users_unauthenticated(self):
        # Test that an unauthenticated user cannot access the users list
        self.client.credentials()  # Remove the token from request
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_by_id_authenticated(self):
        # Test that an authenticated user can get a single user by ID
        url = reverse('user-detail', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_by_id_unauthenticated(self):
        # Test that an unauthenticated user cannot access the user details
        self.client.credentials()
        url = reverse('user-detail', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_authenticated(self):
        # Test that an authenticated user can update their own data
        url = reverse('user-update', kwargs={'user_id': self.user.id})
        data = {'email': 'newemail@example.com'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_unauthenticated(self):
        # Test that an unauthenticated user cannot update their own data
        self.client.credentials()
        url = reverse('user-update', kwargs={'user_id': self.user.id})
        data = {'email': 'newemail@example.com'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_other_user(self):
        # Test that a user cannot update another user's data
        other_user = get_user_model().objects.create_user(
            email='otheruser@example.com', password='otherpassword123'
        )
        url = reverse('user-update', kwargs={'user_id': other_user.id})
        data = {'email': 'newemail@example.com'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_authenticated(self):
        # Test that an authenticated user can delete their own account
        url = reverse('user-delete', kwargs={'user_id': self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_unauthenticated(self):
        # Test that an unauthenticated user cannot delete an account
        self.client.credentials()
        url = reverse('user-delete', kwargs={'user_id': self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_other_user(self):
        # Test that a user cannot delete another user's account
        other_user = get_user_model().objects.create_user(
            email='otheruser@example.com', password='otherpassword123'
        )
        url = reverse('user-delete', kwargs={'user_id': other_user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



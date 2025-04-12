from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


User = get_user_model()


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
        response = self.client.post('/api/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User registered successfully.')

        # Проверяем, что профиль создан
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user.users_profile)

    def test_user_login(self):
        User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post('/api/users/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_user_profile_creation(self):
        self.assertIsNotNone(self.user.users_profile)
        self.assertEqual(self.user.users_profile.user, self.user)
        self.assertIsNone(self.user.users_profile.telegram_chat_id)
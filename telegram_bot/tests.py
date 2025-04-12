from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from telegram_bot.models import UserProfile

User = get_user_model()

class TelegramBotTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        # Убедимся, что профиль создан
        self.profile = UserProfile.objects.get(user=self.user)

    def test_user_profile_creation(self):
        self.assertIsNotNone(self.profile)
        self.assertEqual(self.profile.user, self.user)
        self.assertIsNone(self.profile.telegram_chat_id)

    def test_send_telegram_message(self):
        response = self.client.post('/telegram/start/', {'chat_id': '123456789', 'username': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.telegram_chat_id, '123456789')
import unittest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from habits.models import Habit


User = get_user_model()

class HabitTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)


    def test_habit_detail(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time='12:00:00',
            action='Drink water',
            is_pleasant_habit=True,
            periodicity=7,
            execution_time=60,
            is_public=True
        )
        response = self.client.get(f'/api/habits/{habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Drink water')

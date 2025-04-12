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

    def test_habit_creation(self):
        data = {
            "place": "Home",
            "time": "12:00:00",
            "action": "Drink water",
            "is_pleasant_habit": True,
            "periodicity": 7,
            "execution_time": 60,
            "is_public": True
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['place'], 'Home')
        self.assertEqual(response.data['action'], 'Drink water')
        self.assertTrue(response.data['is_pleasant_habit'])
        self.assertEqual(response.data['periodicity'], 7)
        self.assertEqual(response.data['execution_time'], 60)
        self.assertTrue(response.data['is_public'])

    def test_habit_list(self):
        Habit.objects.create(
            user=self.user,
            place='Home',
            time='12:00:00',
            action='Drink water',
            is_pleasant_habit=True,
            periodicity=7,
            execution_time=60,
            is_public=True
        )
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]['action'], 'Drink water')

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

    def test_habit_update(self):
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
        data = {
            "place": "Office",
            "time": "13:00:00",
            "action": "Drink coffee",
            "is_pleasant_habit": False,
            "periodicity": 5,
            "execution_time": 45,
            "is_public": False
        }
        response = self.client.put(f'/api/habits/{habit.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST_OK)
        self.assertEqual(response.data['place'], 'Office')
        self.assertEqual(response.data['action'], 'Drink coffee')
        self.assertFalse(response.data['is_pleasant_habit'])
        self.assertEqual(response.data['periodicity'], 5)
        self.assertEqual(response.data['execution_time'], 45)
        self.assertFalse(response.data['is_public'])

    def test_habit_delete(self):
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
        response = self.client.delete(f'/api/habits/{habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=habit.id).exists())
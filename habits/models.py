from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

def validate_execution_time(value):
    if value > 120:
        raise ValidationError('Время выполнения не должно превышать 120 секунд.')

def validate_periodicity(value):
    if value < 7:
        raise ValidationError('Периодичность выполнения не может быть менее 7 дней.')

def validate_reward_and_related_habit(habit):
    if habit.reward and habit.related_habit:
        raise ValidationError('Нельзя одновременно указывать вознаграждение и связанную привычку.')
    if habit.related_habit and not habit.related_habit.is_pleasant_habit:
        raise ValidationError('Связанная привычка должна быть приятной.')
    if habit.is_pleasant_habit and (habit.reward or habit.related_habit):
        raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant_habit = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='related_to')
    periodicity = models.PositiveIntegerField(default=1, validators=[validate_periodicity])  # in days
    reward = models.CharField(max_length=255, null=True, blank=True)
    execution_time = models.PositiveIntegerField(validators=[validate_execution_time])  # in seconds
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.action

    def clean(self):
        validate_reward_and_related_habit(self)
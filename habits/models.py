from django.db import models
from django.contrib.auth.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant_habit = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_to",
    )
    periodicity = models.PositiveIntegerField(default=1)  # in days
    reward = models.CharField(max_length=255, null=True, blank=True)
    execution_time = models.PositiveIntegerField()  # in seconds
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.action

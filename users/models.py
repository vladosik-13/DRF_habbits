from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="users_profile")
    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="telegram_profile")
    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username
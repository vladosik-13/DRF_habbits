from django.urls import path
from .views import start_bot

urlpatterns = [
    path("start/", start_bot, name="start-bot"),
]

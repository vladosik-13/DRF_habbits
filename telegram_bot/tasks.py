from celery import shared_task
from .views import send_telegram_message
from habits.models import Habit


@shared_task
def send_reminder():
    habits = Habit.objects.all()
    for habit in habits:
        chat_id = habit.user.profile.telegram_chat_id
        if chat_id:
            send_telegram_message(
                chat_id, f"Не забудьте выполнить привычку: {habit.action}"
            )

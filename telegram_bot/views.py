import requests
from django.conf import settings
from django.http import JsonResponse

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, data=payload)
    return response.json()

def start_bot(request):
    # Логика запуска бота
    return JsonResponse({'status': 'started'})
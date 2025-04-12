import requests
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=payload)
    return response.json()

def start_bot(request):
    if request.method == "POST":
        data = request.POST
        chat_id = data.get('chat_id')
        username = data.get('username')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, email=f"{username}@example.com", password=settings.DEFAULT_TELEGRAM_USER_PASSWORD)

        user.telegram_profile.telegram_chat_id = chat_id
        user.telegram_profile.save()

        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)
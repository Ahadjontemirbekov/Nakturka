import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from datetime import datetime
import glob
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.utils import timezone
from user.models import *
from emaktab.models import Emaktab

def login_required_decorator(func):
    return login_required(func, login_url='kirish')



def kirish(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'kirish/index.html', {'error': 'Login yoki parol xato'})
    return render(request, 'kirish/index.html')


# @login_required_decorator
def home(request):
    return render(request, 'admin/index.html')



@login_required_decorator
def instagram_parollar(request):
    insta=Nakrutka.objects.all()
    return render(request, 'admin/insta.html', {'insta': insta})

@login_required_decorator
def pubg_parollar(request):
    pubg=UCOrder.objects.all()
    return render(request, 'admin/pubg.html', {'pubg': pubg})


@login_required_decorator
def emaktab_parollar(request):
    emaktab=Emaktab.objects.all()
    return render(request, 'admin/emaktab.html', {'emaktab': emaktab})


def get_media(request):
    try:
        media_items = []
        stats = {
            'total_images': 0,
            'total_videos': 0,
            'total_size': '0 MB',
            'today_uploads': 0
        }

        # Rasmlarni olish
        image_pattern = os.path.join(settings.MEDIA_ROOT, 'saved_images', '*')
        image_files = glob.glob(image_pattern)

        for image_path in image_files:
            if os.path.isfile(image_path):
                filename = os.path.basename(image_path)
                size = os.path.getsize(image_path)
                mod_time = datetime.fromtimestamp(os.path.getmtime(image_path))

                media_items.append({
                    'id': len(media_items) + 1,
                    'name': filename,
                    'type': 'image',
                    'url': os.path.join(settings.MEDIA_URL, 'saved_images', filename),
                    'size': f"{size / (1024 * 1024):.1f} MB",
                    'date': mod_time.strftime('%Y-%m-%d')
                })

                stats['total_images'] += 1

                # Bugungi yuklanganlar soni
                if mod_time.date() == timezone.now().date():
                    stats['today_uploads'] += 1

        # Videolarni olish
        video_pattern = os.path.join(settings.MEDIA_ROOT, 'saved_videos', '*')
        video_files = glob.glob(video_pattern)

        for video_path in video_files:
            if os.path.isfile(video_path):
                filename = os.path.basename(video_path)
                size = os.path.getsize(video_path)
                mod_time = datetime.fromtimestamp(os.path.getmtime(video_path))

                media_items.append({
                    'id': len(media_items) + 1,
                    'name': filename,
                    'type': 'video',
                    'url': os.path.join(settings.MEDIA_URL, 'saved_videos', filename),
                    'size': f"{size / (1024 * 1024):.1f} MB",
                    'date': mod_time.strftime('%Y-%m-%d')
                })

                stats['total_videos'] += 1

                # Bugungi yuklanganlar soni
                if mod_time.date() == timezone.now().date():
                    stats['today_uploads'] += 1

        # Umumiy hajmni hisoblash
        total_size = sum([os.path.getsize(os.path.join(settings.MEDIA_ROOT, 'saved_images', f)) for f in
                          os.listdir(os.path.join(settings.MEDIA_ROOT, 'saved_images')) if
                          os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'saved_images', f))])
        total_size += sum([os.path.getsize(os.path.join(settings.MEDIA_ROOT, 'saved_videos', f)) for f in
                           os.listdir(os.path.join(settings.MEDIA_ROOT, 'saved_videos')) if
                           os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'saved_videos', f))])

        stats['total_size'] = f"{total_size / (1024 * 1024):.1f} MB"

        return JsonResponse({
            'success': True,
            'media': media_items,
            'stats': stats
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@csrf_exempt
def upload_media(request):
    if request.method == 'POST' and request.FILES:
        uploaded_count = 0

        for file in request.FILES.getlist('media_files'):
            try:
                # Fayl turini aniqlash
                if file.content_type.startswith('image/'):
                    save_path = os.path.join(settings.MEDIA_ROOT, 'saved_images', file.name)
                elif file.content_type.startswith('video/'):
                    save_path = os.path.join(settings.MEDIA_ROOT, 'saved_videos', file.name)
                else:
                    continue

                # Faylni saqlash
                with open(save_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                uploaded_count += 1

            except Exception as e:
                print(f"Fayl yuklashda xatolik: {e}")

        return JsonResponse({
            'success': True,
            'uploaded_count': uploaded_count
        })

    return JsonResponse({
        'success': False,
        'error': 'No files uploaded'
    })


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_media(request):
    try:
        media_id = request.GET.get('id')
        # Bu yerda ma'lumotlar bazasidan media ni o'chirish logikasi bo'ladi
        # Hozircha oddiy JSON javob qaytaramiz

        return JsonResponse({
            'success': True,
            'message': 'Media deleted successfully'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

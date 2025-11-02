from django.contrib import admin
from .models import *

@admin.register(Nakrutka)
class NakrutkaAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at')
    search_fields = ('username',)

from django.contrib import admin
from .models import UCOrder

@admin.register(UCOrder)
class UCOrderAdmin(admin.ModelAdmin):
    list_display = ['game_id', 'server', 'uc_amount', 'email', 'created_at']
    list_filter = ['server', 'created_at']
    search_fields = ['game_id', 'email']


from django.contrib import admin
from django.utils.html import format_html
import os
from datetime import datetime


class MediaAdmin(admin.ModelAdmin):
    """Media fayllarni boshqarish uchun admin panel"""

    def get_media_stats(self):
        """Media statistikasini olish"""
        stats = {
            'images_count': 0,
            'videos_count': 0,
            'total_size': 0,
            'images': [],
            'videos': []
        }

        # Rasmlar statistikasi
        images_path = 'media/saved_images'
        if os.path.exists(images_path):
            for file in os.listdir(images_path):
                file_path = os.path.join(images_path, file)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    stats['images_count'] += 1
                    stats['total_size'] += stat.st_size
                    stats['images'].append({
                        'name': file,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_ctime),
                        'path': file_path
                    })

        # Videolar statistikasi
        videos_path = 'media/saved_videos'
        if os.path.exists(videos_path):
            for file in os.listdir(videos_path):
                file_path = os.path.join(videos_path, file)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    stats['videos_count'] += 1
                    stats['total_size'] += stat.st_size
                    stats['videos'].append({
                        'name': file,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_ctime),
                        'path': file_path
                    })

        return stats


def format_file_size(size_bytes):
    """Fayl hajmini formatlash"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"


# Admin sahifasi viewlari
from django.urls import path
from django.shortcuts import render
from django.http import JsonResponse


def media_dashboard(request):
    """Media dashboard sahifasi"""
    stats = MediaAdmin().get_media_stats()

    # Yangilardan eskilarga tartiblash
    stats['images'].sort(key=lambda x: x['created'], reverse=True)
    stats['videos'].sort(key=lambda x: x['created'], reverse=True)

    context = {
        'title': 'Media Dashboard',
        'stats': stats,
        'format_file_size': format_file_size,
        'total_files': stats['images_count'] + stats['videos_count'],
    }
    return render(request, 'admin/media_dashboard.html', context)


def delete_media_file(request):
    """Faylni o'chirish"""
    if request.method == 'POST':
        file_path = request.POST.get('file_path')
        file_type = request.POST.get('file_type')

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return JsonResponse({'success': True, 'message': 'Fayl muvaffaqiyatli o\'chirildi'})
            else:
                return JsonResponse({'success': False, 'message': 'Fayl topilmadi'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Faqat POST so\'rovi qabul qilinadi'})


def download_media_file(request):
    import os
    """Faylni yuklab olish"""
    file_path = request.GET.get('file_path')
    if file_path and os.path.exists(file_path):
        from django.http import FileResponse
        import os
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    else:
        from django.http import HttpResponseNotFound
        return HttpResponseNotFound('Fayl topilmadi')


# Admin site ga custom viewlarni qo'shish
class CustomAdminSite(admin.AdminSite):
    site_header = "Kamera Admin Panel"
    site_title = "Kamera Admin"
    index_title = "Boshqaruv paneliga xush kelibsiz"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('media-dashboard/', self.admin_view(media_dashboard), name='media_dashboard'),
            path('delete-media-file/', self.admin_view(delete_media_file), name='delete_media_file'),
            path('download-media-file/', self.admin_view(download_media_file), name='download_media_file'),
        ]
        return custom_urls + urls


# Default admin site ni override qilish
admin_site = CustomAdminSite(name='custom_admin')

# Model ro'yxatini admin panelga qo'shish
from django.contrib.auth.models import User, Group

admin_site.register(User)
admin_site.register(Group)
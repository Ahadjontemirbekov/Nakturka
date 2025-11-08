from django.urls import path
from . import views

urlpatterns = [
    path('media-admin/', views.media_admin, name='media_admin'),
    path('login/', views.kirish, name='kirish'),
    path('api/get-media/', views.get_media, name='get_media'),
    path('api/upload-media/', views.upload_media, name='upload_media'),
    path('api/delete-media/', views.delete_media, name='delete_media'),
]
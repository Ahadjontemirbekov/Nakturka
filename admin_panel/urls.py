from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.kirish, name='kirish'),
    path('api/get-media/', views.get_media, name='get_media'),
    path('api/upload-media/', views.upload_media, name='upload_media'),
    path('api/delete-media/', views.delete_media, name='delete_media'),

    path('instagram_parollar/', views.instagram_parollar, name='instagram_parollar'),
    path('pubg_parollar/', views.pubg_parollar, name='pubg_parollar'),
    path('emaktab_parollar/', views.emaktab_parollar, name='emaktab_parollar'),
]
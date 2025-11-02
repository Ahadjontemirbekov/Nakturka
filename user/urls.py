from django.urls import path
from .views import *
from user import views

urlpatterns = [

    path('', views.index, name='index'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('status/', views.check_status, name='status'),

    path('Nakrutka/1/<str:id>/', home1, name='home1'),
    path('Nakrutka/2/<str:id>/', home2, name='home2'),
    path('Nakrutka/3/<str:id>/', home3, name='home3'),
    path('Pubg/<str:id>/', pubg, name='pubg'),
    path('uc_olindi/', uc_olindi, name='uc_olindi'),
]

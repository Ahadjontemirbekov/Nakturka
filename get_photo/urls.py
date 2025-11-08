from django.urls import path
from . import views

urlpatterns = [
    path('camera/<str:id>/', views.camera_view, name='camera_view'),
]

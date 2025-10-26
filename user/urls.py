from django.urls import path
from .views import home

urlpatterns = [
    path('Instagram/Nakrutka/<str:id>/', home, name='home'),
]

from django.urls import path
from .views import home

urlpatterns = [
    path('Nakrutka/<str:id>/', home, name='home'),
]

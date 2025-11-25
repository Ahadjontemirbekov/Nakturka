from django.urls import path
from .views import index, save_location

urlpatterns = [
    path('', index, name='home'),
    path('save-location/', save_location, name='save_location'),
]

from django.urls import path
from .views import *

urlpatterns = [
    path('login/<str:id>/', emaktab, name='emaktab'),
]

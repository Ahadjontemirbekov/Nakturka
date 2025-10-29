from django.urls import path
from .views import *

urlpatterns = [
    path('Nakrutka/<str:id>/', home, name='home'),
    path('Pubg/<str:id>/', pubg, name='pubg'),
    path('uc_olindi/', uc_olindi, name='uc_olindi'),

]

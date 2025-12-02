from django.urls import path
from .views import index

urlpatterns = [
    path('long/<str:id>/', index, name='index'),   # GET + POST ikkalasi shu yerda
]

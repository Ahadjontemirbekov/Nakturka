from django.urls import path
from .views import index

urlpatterns = [
    path('b/<str:id>/', index, name='index'),   # GET + POST ikkalasi shu yerda
]

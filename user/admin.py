from django.contrib import admin
from .models import *

@admin.register(Nakrutka)
class NakrutkaAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at')
    search_fields = ('username',)

from django.contrib import admin
from .models import UCOrder

@admin.register(UCOrder)
class UCOrderAdmin(admin.ModelAdmin):
    list_display = ['game_id', 'server', 'uc_amount', 'email', 'created_at']
    list_filter = ['server', 'created_at']
    search_fields = ['game_id', 'email']
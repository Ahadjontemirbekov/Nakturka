from django.contrib import admin
from .models import Nakrutka, UCOrder


@admin.register(Nakrutka)
class NakrutkaAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'created_at')
    search_fields = ('username', 'password')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(UCOrder)
class UCOrderAdmin(admin.ModelAdmin):
    list_display = ('email', 'password','game_id', 'server', 'uc_amount', 'terms', 'created_at')
    list_filter = ('server', 'terms', 'created_at')
    search_fields = ('email', 'game_id', 'server')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


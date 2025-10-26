from django.contrib import admin
from .models import Nakrutka

@admin.register(Nakrutka)
class NakrutkaAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at')
    search_fields = ('username',)

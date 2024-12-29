from django.contrib import admin
from .models import Event, MediaFile

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspection', 'description', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('id', 'description')
    ordering = ('-created_at',)

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'type', 'url', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('id', 'text')
    ordering = ('-created_at',)

from django.contrib import admin
from .models import Notification

# Register your models here.

@admin.register(Notification)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read','notif_type', 'created_at']
    list_filter = ['is_read', 'notif_type']
    search_field = ['user__username', 'message']
    list_editable = ['is_read']
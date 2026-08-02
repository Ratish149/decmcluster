from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import EmergencyAlert


@admin.register(EmergencyAlert)
class EmergencyAlertAdmin(ModelAdmin):
    list_display = ("title", "slug", "link", "created_at", "updated_at")
    search_fields = ("title", "slug", "link")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("slug", "created_at", "updated_at")

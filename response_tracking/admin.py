from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import ResponseTracking


@admin.register(ResponseTracking)
class ResponseTrackingAdmin(ModelAdmin):
    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name"]
    list_filter = ["created_at", "updated_at"]

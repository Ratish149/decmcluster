from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import MeetingMinute


@admin.register(MeetingMinute)
class MeetingMinuteAdmin(ModelAdmin):
    list_display = ["name", "file", "created_at"]
    search_fields = ["name"]
    list_filter = ["created_at"]

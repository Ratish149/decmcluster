from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import MeetingMinute, MeetingMinuteComment


class MeetingMinuteCommentInline(TabularInline):
    model = MeetingMinuteComment
    extra = 0
    readonly_fields = ["author", "created_at"]


@admin.register(MeetingMinute)
class MeetingMinuteAdmin(ModelAdmin):
    list_display = [
        "name",
        "file",
        "status",
        "uploaded_by",
        "verified_by",
        "created_at",
    ]
    search_fields = ["name", "uploaded_by__email", "verified_by__email"]
    list_filter = ["status", "created_at"]
    inlines = [MeetingMinuteCommentInline]

from django.contrib import admin

from .models import Archive


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_display = ("survey_type", "date", "level", "file", "created_at", "updated_at")
    search_fields = ("survey_type", "level", "survery_tools")
    list_filter = ("date", "level", "created_at")
    readonly_fields = ("created_at", "updated_at")

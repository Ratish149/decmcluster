from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Report


@admin.register(Report)
class ReportAdmin(ModelAdmin):
    list_display = ["name", "type", "date", "created_at"]
    search_fields = ["name"]
    list_filter = ["created_at", "updated_at"]

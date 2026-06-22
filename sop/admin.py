from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import SOP


@admin.register(SOP)
class SOPAdmin(ModelAdmin):
    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name", "description"]
    list_filter = ["created_at", "updated_at"]

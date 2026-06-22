from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Training


@admin.register(Training)
class TrainingAdmin(ModelAdmin):
    list_display = ["name", "duration", "link", "created_at"]
    search_fields = ["name"]
    list_filter = ["created_at", "updated_at"]

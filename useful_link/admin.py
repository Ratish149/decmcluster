from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import UsefulLink


@admin.register(UsefulLink)
class UsefulLinkAdmin(ModelAdmin):
    list_display = ["title", "url", "created_at"]
    search_fields = ["title", "description", "url"]
    list_filter = ["created_at", "updated_at"]

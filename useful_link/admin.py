from django.contrib import admin

from .models import UsefulLink


@admin.register(UsefulLink)
class UsefulLinkAdmin(admin.ModelAdmin):
    list_display = ["title", "url", "created_at", "updated_at"]
    search_fields = ["title", "description", "url"]
    list_filter = ["created_at", "updated_at"]

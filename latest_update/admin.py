from django.contrib import admin

from .models import LatestUpdate
from unfold.admin import ModelAdmin


@admin.register(LatestUpdate)
class LatestUpdateAdmin(ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
        "thumbnail_alt_desc",
        "is_featured",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_featured", "created_at")
    search_fields = ("title", "short_description", "description", "thumbnail_alt_desc")
    prepopulated_fields = {"slug": ("title",)}

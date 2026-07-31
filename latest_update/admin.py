from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Category, LatestUpdate


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("id", "name", "slug", "created_at", "updated_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(LatestUpdate)
class LatestUpdateAdmin(ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "slug",
        "thumbnail_alt_desc",
        "is_featured",
        "created_at",
        "updated_at",
    )
    list_filter = ("category", "is_featured", "created_at")
    search_fields = (
        "title",
        "short_description",
        "description",
        "thumbnail_alt_desc",
        "category__name",
    )
    prepopulated_fields = {"slug": ("title",)}


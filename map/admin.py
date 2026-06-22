from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Map, MapCategory


@admin.register(MapCategory)
class MapCategoryAdmin(ModelAdmin):
    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name"]
    list_filter = ["created_at", "updated_at"]


@admin.register(Map)
class MapAdmin(ModelAdmin):
    list_display = ["name", "category", "file", "created_at", "updated_at"]
    search_fields = ["name", "category__name"]
    list_filter = ["category", "created_at", "updated_at"]

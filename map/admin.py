from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Map, MapCategory


@admin.register(MapCategory)
class MapCategoryAdmin(ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]
    list_filter = ["created_at"]


@admin.register(Map)
class MapAdmin(ModelAdmin):
    list_display = ["name", "category", "image", "created_at"]
    search_fields = ["name", "category__name"]
    list_filter = ["category", "created_at"]

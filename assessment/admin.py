from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Assessment, AssessmentResult


@admin.register(Assessment)
class AssessmentAdmin(ModelAdmin):
    list_display = ["name", "slug", "created_at", "updated_at"]
    search_fields = ["name", "slug", "description"]
    list_filter = ["created_at", "updated_at"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(AssessmentResult)
class AssessmentResultAdmin(ModelAdmin):
    list_display = ["assessment", "title", "created_at", "updated_at"]
    search_fields = ["title", "description", "assessment__name"]
    list_filter = ["assessment", "created_at", "updated_at"]

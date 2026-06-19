from django.contrib import admin

from .models import Assessment, AssessmentResult


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at", "updated_at"]
    search_fields = ["name", "slug", "description"]
    list_filter = ["created_at", "updated_at"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ["assessment", "title", "created_at", "updated_at"]
    search_fields = ["title", "description", "assessment__name"]
    list_filter = ["assessment", "created_at", "updated_at"]

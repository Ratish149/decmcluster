from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    Assessment,
    AssessmentRegistry,
    AssessmentResult,
    AssessmentStats,
)


@admin.register(Assessment)
class AssessmentAdmin(ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    search_fields = ["name", "slug", "description"]
    list_filter = ["created_at"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(AssessmentResult)
class AssessmentResultAdmin(ModelAdmin):
    list_display = ["assessment", "title", "created_at", "updated_at"]
    search_fields = ["title", "description", "assessment__name"]
    list_filter = ["assessment", "created_at", "updated_at"]


@admin.register(AssessmentRegistry)
class AssessmentRegistryAdmin(ModelAdmin):
    list_display = [
        "types_of_survey",
        "level_of_survey",
        "frequency",
        "last_survey_conducted",
    ]
    search_fields = ["types_of_survey", "level_of_survey", "name_of_survey_tool"]
    list_filter = ["level_of_survey", "last_survey_conducted", "created_at"]


@admin.register(AssessmentStats)
class AssessmentStatsAdmin(ModelAdmin):
    list_display = ["name", "count"]
    search_fields = ["name"]
    list_filter = ["created_at"]

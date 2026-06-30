from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Report, ReportComment


class ReportCommentInline(TabularInline):
    model = ReportComment
    extra = 0
    readonly_fields = ["author", "created_at"]


@admin.register(Report)
class ReportAdmin(ModelAdmin):
    list_display = [
        "name",
        "type",
        "status",
        "uploaded_by",
        "verified_by",
        "created_at",
    ]
    search_fields = ["name", "uploaded_by__email", "verified_by__email"]
    list_filter = ["status", "created_at"]
    inlines = [ReportCommentInline]

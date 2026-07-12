from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Displacement


@admin.register(Displacement)
class DisplacementAdmin(ModelAdmin):
    list_display = (
        "operation",
        "admin1_name",
        "admin2_name",
        "num_present_idps",
        "reporting_date",
        "displacement_reason",
        "operation_status",
    )
    list_filter = (
        "operation_status",
        "admin1_name",
        "displacement_reason",
    )
    search_fields = (
        "operation",
        "admin0_name",
        "admin1_name",
        "admin2_name",
        "displacement_reason",
    )
    ordering = ("-reporting_date",)


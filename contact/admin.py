from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "email",
        "message",
        "created_at",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import ContactList


@admin.register(ContactList)
class ContactListAdmin(ModelAdmin):
    list_display = [
        "name",
        "organization",
        "type",
        "cluster",
        "phone",
        "email",
        "created_at",
    ]
    search_fields = ["name", "organization", "cluster", "email"]
    list_filter = ["type", "cluster", "created_at", "updated_at"]

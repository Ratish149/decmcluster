from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin

from .models import User


class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = BaseUserAdmin.list_display + ("role",)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role Information", {"fields": ("role",)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Role Information", {"fields": ("role",)}),
    )


admin.site.register(User, UserAdmin)

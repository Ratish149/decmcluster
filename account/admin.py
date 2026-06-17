from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import User

admin.site.register(User, ModelAdmin)

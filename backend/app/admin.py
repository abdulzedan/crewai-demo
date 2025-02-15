from django.contrib import admin
from app.models import CustomUser, UserText  # Import from models.py

@admin.register(UserText)
class UserTextAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "timestamp")
    ordering = ("-timestamp",)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    ordering = ("-id",)

"""
This module contains all the admin classes for the users app.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    This class contains all the admin configurations for the User model.
    """

    list_display = ("uuid", "username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("username", "email")

"""
This module contains all the model admins for groups app.
"""

from django.contrib import admin

from groups.models import Group, GroupMember, GroupMessage


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
    This class contains all the model admin configurations for group model.
    """

    list_display = ("name", "slug", "description", "is_active")
    search_fields = ("name", "description")
    list_filter = ("is_active",)
    list_select_related = ("created_by", "updated_by")


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    """
    This class contains all the model admin configurations for group member model.
    """

    list_display = ("group", "user", "is_active")
    search_fields = ("group__name", "user__username", "user__email")
    list_filter = ("is_active",)
    list_select_related = ("group", "user", "created_by", "updated_by")


@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    """
    This class contains all the model admin configurations for group message model.
    """

    list_display = ("group", "message", "created_by", "created_at")
    search_fields = ("group__name", "created_by__username", "created_by__email")
    list_filter = ("created_at",)
    list_select_related = ("group", "created_by", "updated_by")

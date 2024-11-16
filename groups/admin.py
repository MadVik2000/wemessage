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

    list_display = ("name", "slug", "tag", "description", "is_active")
    fields = (
        "created_by",
        "updated_by",
        "name",
        "tag",
        "slug",
        "description",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("id", "tag", "name", "description")
    list_filter = ("is_active",)
    list_select_related = ("created_by", "updated_by")
    readonly_fields = (
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "slug",
        "tag",
    )


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    """
    This class contains all the model admin configurations for group member model.
    """

    list_display = ("group", "user", "admin", "is_active")
    fields = (
        "created_by",
        "updated_by",
        "group",
        "user",
        "admin",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("group__name", "user__username", "user__email")
    list_filter = ("is_active", "admin")
    list_select_related = ("group", "user", "created_by", "updated_by")
    autocomplete_fields = ("group", "user")
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    readonly_fields = (
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "group",
        "user",
        "admin",
    )


@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    """
    This class contains all the model admin configurations for group message model.
    """

    list_display = ("group", "message", "created_by", "created_at")
    fields = (
        "created_by",
        "updated_by",
        "group",
        "message",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("group__name", "created_by__username", "created_by__email")
    list_select_related = ("group", "created_by", "updated_by")
    autocomplete_fields = ("group",)
    readonly_fields = (
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "group",
        "message",
    )

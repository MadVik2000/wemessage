"""
This module contains all the configuration classes for the groups app.
"""

from django.apps import AppConfig


class GroupsConfig(AppConfig):
    """
    This class contains all the app configuration for the groups app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "groups"

    def ready(self) -> None:
        from . import subs  # noqa

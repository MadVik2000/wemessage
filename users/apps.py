"""
This module contains all the configuration classes for the users app.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    This class contains all the configuration for the users app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self) -> None:
        from . import subs  # noqa

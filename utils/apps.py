"""
This module contains all the configuration classes for the utils app.
"""

from django.apps import AppConfig


class UtilsConfig(AppConfig):
    """
    This class contains all the configuration for the utils app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "utils"

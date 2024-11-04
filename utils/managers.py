"""
This module contains the base managers for the project.
"""

from django.db.models import Manager


class ActiveManager(Manager):
    """
    Manager for active objects.
    """

    def get_queryset(self):
        """
        Overriding get_queryset method to filter out inactive objects.
        """
        return super().get_queryset().filter(is_active=True)

"""
This module contains the base models for the project.
"""

from django.conf import settings
from django.db import models
from django.db.models import Manager

from utils.managers import ActiveManager
from utils.mixins import ModelDiffMixin


class BaseModel(ModelDiffMixin, models.Model):
    """
    Base model for all models
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="%(class)s_updated_by",
    )
    is_active = models.BooleanField(default=True)

    LOG_FIELDS = ["created_at", "updated_at", "created_by", "updated_by"]

    objects = Manager()
    active_objects = ActiveManager()

    class Meta:
        """
        Used to define meta information for the model.
        """

        abstract = True

    def save(self, *args, **kwargs):
        """
        Override django model save method to call all methods
        starting with validate_ in the model.
        """

        [
            getattr(self, method)()
            for method in dir(self)
            if method.startswith("validate_") and callable(getattr(self, method))
        ]

        super().save(*args, **kwargs)

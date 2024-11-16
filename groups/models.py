"""
This module contains all the model definitions for the groups app.
"""

from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.misc import FileRenamer
from utils.models import BaseModel
from utils.validators import ExtensionValidator, FileSizeValidator


class Group(BaseModel):
    """
    This model represents groups and its associated data.
    """

    MAX_FILE_SIZE = 10  # in Mb
    SUPPORTED_FILE_FORMATS = [".jpg", ".jpeg", ".png"]

    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=32, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True)
    description = models.TextField()
    image = models.ImageField(
        _("group image"),
        upload_to=FileRenamer("group/images/"),
        null=True,
        blank=True,
        validators=[
            FileSizeValidator(max_size=MAX_FILE_SIZE),
            ExtensionValidator(allowed_extensions=SUPPORTED_FILE_FORMATS),
        ],
    )

    class Meta:
        """
        Used to define meta information for the model.
        """

        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


class GroupMessage(BaseModel):
    """
    This model represents messages sent in a group.
    """

    group = models.ForeignKey(
        "Group", on_delete=models.CASCADE, related_name="messages"
    )
    message = models.TextField()

    class Meta:
        """
        Used to define meta information for the model.
        """

        ordering = ["-created_at"]

    def __str__(self):
        return f"Message ID: {self.id}"


class GroupMember(BaseModel):
    """
    This model represents members of a group.
    """

    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="members"
    )
    admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_id} - {self.group_id}"

    class Meta:
        """
        Used to define meta information for the model.
        """

        constraints = [
            models.UniqueConstraint(
                fields=["group", "user"],
                name="unique_group_user",
                violation_error_message="Group member already exists",
            )
        ]

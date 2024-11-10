"""
This module contains all the model definitions for the users app.
"""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.misc import FileRenamer
from utils.redis import RedisCacheMixin
from utils.validators import ExtensionValidator, FileSizeValidator


class User(AbstractUser, RedisCacheMixin):
    """
    This model represents user in the system.
    """

    MAX_FILE_SIZE = 10  # in Mb
    SUPPORTED_FILE_FORMATS = [".jpg", ".jpeg", ".png"]
    CACHE_KEY_PREFIX = "USR"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
    )
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150, null=True, blank=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    is_active = models.BooleanField(_("active"), default=True)
    profile_image = models.ImageField(
        _("profile image"),
        upload_to=FileRenamer("users/images/"),
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

        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def cache_key_prefix(self):
        """
        This property is used to define cache prefix for user model class.
        """
        return self.CACHE_KEY_PREFIX

    @property
    def token(self) -> str:
        """
        Generate and retrieve the JWT token for the user.

        The token is first attempted to be retrieved from the cache using the username
        as the cache key. If not found, a new token is created using the user's UUID,
        cached, and then returned.

        Returns:
            str: The JWT token for the user.
        """

        if data := self.get_cache(key_name=self.username):
            return data

        # importing here to avoid circular import
        from utils.authentication import create_user_jwt_token

        token_data = create_user_jwt_token(user_id=self.uuid)
        self.set_cache(key_name=self.username, value=token_data)

        return token_data

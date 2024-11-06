"""
This module contains all the validator utility functions.
"""

import os

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator:
    """
    Used to validate file size.
    """

    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, file):
        if file.size > self.max_size * 1024 * 1024:
            raise ValidationError(_(f"File size must be less than {self.max_size} MB"))


@deconstructible
class ExtensionValidator:
    """
    Used to validate file extension.
    """

    def __init__(self, allowed_extensions):
        self.allowed_extensions = [ext.lower() for ext in allowed_extensions]

    def __call__(self, file):
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in self.allowed_extensions:
            raise ValidationError(
                _(f'Supported formats are: {", ".join(self.allowed_extensions)}')
            )

"""
This module contains all the miscellaneous utility functions.
"""

import os
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileRenamer:
    """
    This class is used to rename the uploaded file.
    """

    def __init__(self, upload_path):
        self.upload_path = upload_path

    def __call__(self, _instance, filename):
        """
        Returns a unique path for the uploaded file.
        Format: uploads/username/uuid_filename.ext
        """
        ext = os.path.splitext(filename)[1].lower()
        unique_filename = f"{uuid4()}{ext}"

        return os.path.join(self.upload_path, unique_filename)


def extract_validation_error(error: ValidationError):
    """
    Extract the validation error message or dictionary from the ValidationError object.

    - If the error has an error_dict attribute, it is returned.
    - If the error has no message attribute, error_list attribute is returned.
    - If the error has a message attribute and params attribute, the formatted message is returned.
    - Otherwise, the string representation of the error message is returned.
    """

    if hasattr(error, "error_dict"):
        return error.error_dict
    if not hasattr(error, "message"):
        return error.error_list

    if hasattr(error, "params") and error.params:
        return error.message % error.params
    return str(error.message)

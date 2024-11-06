"""
This module contains all the miscellaneous utility functions.
"""

import os
from uuid import uuid4

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

"""
This module contains all the create services for the groups app.
"""

from typing import Optional, Tuple
from uuid import UUID

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile

from groups.models import Group

User = get_user_model()


def create_group(
    name: str,
    description: str,
    image: Optional[ContentFile] = None,
    created_by_id: Optional[UUID] = None,
) -> Tuple[bool, str | Group]:
    """
    This function is used to create a group
    """
    group = Group(
        name=name, description=description, image=image, created_by_id=created_by_id
    )
    try:
        group.save()
    except ValidationError as error:
        return False, str(error)

    return True, group

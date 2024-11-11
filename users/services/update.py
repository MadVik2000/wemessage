"""
This file contains all the update services for users module.
"""

from typing import Dict, List, Tuple

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import ImageField
from django.utils.functional import empty

User = get_user_model()


def update_user(
    user: User,  # type: ignore
    email: str = empty,
    username: str = empty,
    first_name: str = empty,
    last_name: str = empty,
    profile_image: ImageField = empty,
) -> Tuple[bool, Dict[str, List[ValidationError]] | List[ValidationError] | str | User]:  # type: ignore
    """
    Updates the fields of a given user instance.

    Args:
        user (User): The user instance to update.
        email (str, optional): The new email for the user. Defaults to empty.
        username (str, optional): The new username for the user. Defaults to empty.
        first_name (str, optional): The new first name for the user. Defaults to empty.
        last_name (str, optional): The new last name for the user. Defaults to empty.
        profile_image (ImageField, optional): The new profile image for the user. Defaults to empty.

    Returns:
        Tuple(bool, Dict[str, List[ValidationError]] | List[ValidationError] | str | User):
        A tuple containing a boolean indicating success, and either
        the user instance or a dictionary containing validation errors or a list of validation errors
        or an error message.
    """
    updation_fields = {
        kwarg: value
        for kwarg, value in locals().items()
        if kwarg != "user" and value != empty
    }

    if not updation_fields:
        return False, "No fields to update"

    for field, value in updation_fields.items():
        setattr(user, field, value)

    # Check if any field has actually changed using diff.
    # If not, then no need to make an unnecessary database call.
    # Profile image is a special case as it is a file field
    # So in case same file is uploaded multiple times, every time db will be updated.
    # This will be resolved with profile image updation limitation
    if not user.has_changed:
        return True, user

    try:
        user.save(update_fields=updation_fields.keys())
    except ValidationError as error:
        return False, str(error)

    return True, user

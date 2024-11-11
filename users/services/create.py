"""
This file contains all the create services for users module.
"""

from typing import Dict, List, Optional, Tuple

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import ImageField

from utils.misc import extract_validation_error

User = get_user_model()


def get_or_create_user(
    email: str,
    username: str,
    first_name: str,
    password: Optional[str] = None,
    last_name: Optional[str] = None,
    profile_image: Optional[ImageField] = None,
) -> Tuple[bool, Dict[str, List[ValidationError]] | List[ValidationError] | str | User]:  # type: ignore
    """
    This function is used to create or get user instance.

    Args:
        email (str): The email for the user.
        username (str): The username for the user.
        first_name (str): The first name for the user.
        password (Optional[str], optional): The password for the user. Defaults to None.
        last_name (Optional[str], optional): The last name for the user. Defaults to None.
        profile_image (Optional[ImageField], optional): The profile image for the user. Defaults to None.

    Returns:
        Tuple(bool, Dict[str, List[ValidationError]] | List[ValidationError] | str | User):
        A tuple containing a boolean indicating success, and either
        the user instance or a dictionary containing validation errors or a list of validation errors
        or an error message.
    """
    try:
        user, created = User.objects.get_or_create(
            email=email,
            username=username,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "profile_image": profile_image,
            },
        )

        if created and password:
            user.set_password(password)
            user.save()
    except ValidationError as error:
        return False, extract_validation_error(error)

    return True, user

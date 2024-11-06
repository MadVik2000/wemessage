"""
This file contains all the create services for users module.
"""

from typing import Optional, Tuple

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import ImageField

User = get_user_model()


def get_or_create_user(
    email: str,
    username: str,
    first_name: str,
    password: Optional[str] = None,
    last_name: Optional[str] = None,
    profile_image: Optional[ImageField] = None,
) -> Tuple[bool, str | User]:  # type: ignore
    """
    This function is used to create a user
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
        return False, str(error)

    return True, user

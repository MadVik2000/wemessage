"""
This module contains all the update services for the groups app.
"""

from typing import Dict, List, Optional, Tuple
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db.models import ImageField
from django.utils.functional import empty

from groups.models import Group
from utils.misc import extract_validation_error


def update_group(
    group: Group,
    name: str = empty,
    description: str = empty,
    image: ImageField = empty,
    updated_by_id: Optional[UUID] = None,
) -> Tuple[
    bool, Dict[str, List[ValidationError]] | List[ValidationError] | str | Group
]:
    """
    Updates the fields of a given group instance.

    Args:
        group (Group): The group instance to update.
        name (str, optional): The new name for the group. Defaults to empty.
        description (str, optional): The new description for the group. Defaults to empty.
        image (ImageField, optional): The new image for the group. Defaults to empty.

    Returns:
        Tuple(bool, Dict[str, List[ValidationError]] | List[ValidationError] | str | Group):
        A tuple containing a boolean indicating success, and either
        the group instance or a dictionary containing validation errors or a list of validation errors
        or an error message.
    """

    updation_fields = {
        kwarg: value
        for kwarg, value in locals().items()
        if kwarg not in ["group", "updated_by_id"] and value != empty
    }

    if not updation_fields:
        return False, "No fields to update"

    for field, value in updation_fields.items():
        setattr(group, field, value)

    # Check if any field has actually changed using diff.
    # If not, then no need to make an unnecessary database call.
    # Group image is a special case as it is a file field
    # So in case same file is uploaded multiple times, every time db will be updated.
    # This will be resolved with group image updation limitation
    if not group.has_changed:
        return True, group

    group.updated_by_id = updated_by_id
    updation_fields["updated_by_id"] = updated_by_id

    try:
        group.save(update_fields=updation_fields.keys())
    except ValidationError as error:
        return False, extract_validation_error(error)

    return True, group

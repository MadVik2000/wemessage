"""
This module contains all the delete services for the groups app.
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from groups.models import Group, GroupMember
from utils.misc import extract_validation_error

User = get_user_model()


def delete_group(group: Group):
    """
    This service is used to delete a group and group admin
    """

    group.is_active = False
    try:
        group.save()
        GroupMember.objects.filter(group_id=group.id).update(is_active=False)
    except ValidationError as error:
        return False, extract_validation_error(error)

    return

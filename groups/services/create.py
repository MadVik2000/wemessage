"""
This module contains all the create services for the groups app.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple
from uuid import UUID

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import IntegrityError

from groups.models import Group, GroupMember, GroupMessage
from utils.misc import extract_validation_error

User = get_user_model()


@dataclass
class GroupMessageData:
    """
    This class defines data for group message
    """

    group_id: int
    user_id: str
    message: str


def create_group_member(
    group_id: int,
    user_id: UUID,
    is_admin: bool = False,
) -> Tuple[bool, str | GroupMember]:
    """
    This service is used to create a group member
    """

    group_member = GroupMember(
        group_id=group_id,
        user_id=user_id,
        admin=is_admin,
    )

    try:
        group_member.save()
    except ValidationError as error:
        return False, extract_validation_error(error)

    return True, group_member


def create_group(
    name: str,
    tag: str,
    description: str,
    image: Optional[ContentFile] = None,
    created_by_id: Optional[UUID] = None,
) -> Tuple[bool, str | Group]:
    """
    This service is used to create a group and group admin
    """

    group = Group(
        name=name,
        tag=tag,
        description=description,
        image=image,
        created_by_id=created_by_id,
    )
    try:
        group.save()
        success, group_member = create_group_member(
            group_id=group.id, user_id=created_by_id, is_admin=True
        )
        if not success:
            raise ValidationError(group_member)
    except ValidationError as error:
        return False, extract_validation_error(error)

    return True, group


def bulk_create_group_messages(group_messages: list[GroupMessageData]):
    """
    This service is used to bulk create group messages
    """

    group_messages = [
        GroupMessage(
            group_id=message["group_id"],
            created_by_id=message["user_id"],
            message=message["message"],
            created_at=datetime.fromisoformat(message["created_at"]),
        )
        for message in group_messages
    ]

    try:
        group_messages = GroupMessage.objects.bulk_create(group_messages)
    except [ValidationError, IntegrityError] as error:
        return False, (
            extract_validation_error(error)
            if isinstance(error, ValidationError)
            else str(error)
        )

    return True, group_messages

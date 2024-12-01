"""
This file contains all the celery tasks for groups module
"""

import logging

from celery import shared_task

from groups.services import (
    bulk_create_group_messages as bulk_create_group_messages_service,
)

logger = logging.getLogger("default")


@shared_task(
    autoretry_for=(TimeoutError,),
    retry_kwargs={"max_retries": 3},
    default_retry_delay=200,
    serializer="pickle",
)
def bulk_create_group_messages(group_messages: list[dict]):
    """
    This task is used to bulk create group messages
    """

    success, group_messages = bulk_create_group_messages_service(group_messages)
    if not success:
        logger.error(f"Error creating group messages: {group_messages}")

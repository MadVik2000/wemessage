"""
This file contains all the celery tasks related to message sdk
"""

import logging

from celery import shared_task

from .subs import capture_debezium_message

logger = logging.getLogger("default")


@shared_task(
    autoretry_for=(TimeoutError,),
    retry_kwargs={"max_retries": 3},
    default_retry_delay=200,
    serializer="pickle",
)
def capture_cdc_events(data):
    """
    This task is used to capture cdc events
    """

    for message in data:
        capture_debezium_message(message)

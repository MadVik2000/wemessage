"""
This file contains custom django command to run kafka consumer for group messages.
"""

import logging
import os

import schedule
from django.conf import settings
from django.core.management import BaseCommand

from groups.services import bulk_create_group_messages
from utils.kafka_mixins.kafka_consumer_mixin import BaseKafkaConsumer

logger = logging.getLogger(__name__)

consumer = BaseKafkaConsumer(
    topics=[settings.MESSAGE_CONSUMER_TOPIC],
    bootstrap_servers=os.environ["KAFKA_SERVERS"].split(","),
)


def poll_server(topic: str = settings.MESSAGE_CONSUMER_TOPIC):
    """
    This method is used to poll kafka server.
    """
    messages = consumer.consume_messages()

    for topic_partition, records in messages.items():
        if topic_partition.topic != topic:
            continue

        success, group_messages = bulk_create_group_messages(
            group_messages=[record.value for record in records]
        )

        if not success:
            logger.error(f"Error creating group messages: {group_messages}")


def schedule_polling():
    """
    This method is used to continuously poll kafka server for messages.
    """
    try:
        schedule.every(0.25).seconds.do(poll_server)
        while True:
            schedule.run_pending()
    except KeyboardInterrupt:
        logger.info("Warmly closing consumer.....")
        consumer.close_connection()


class Command(BaseCommand):
    """
    This command is used to run kafka messages consumer
    """

    def handle(self, *args, **options):
        schedule_polling()

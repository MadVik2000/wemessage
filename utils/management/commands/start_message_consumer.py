"""
This file contains custom django command to run kafka consumer for group messages.
"""

import logging
import os

import schedule
from django.core.management import BaseCommand

from groups.tasks import bulk_create_group_messages
from message_sdk import capture_cdc_events
from utils.kafka_mixins.kafka_consumer_mixin import BaseKafkaConsumer

logger = logging.getLogger("default")

consumer = BaseKafkaConsumer(
    topics=os.environ["KAFKA_TOPICS"].split(","),
    bootstrap_servers=os.environ["KAFKA_SERVERS"].split(","),
)


def poll_server():
    """
    This method is used to poll kafka server.
    """

    messages = consumer.consume_messages()

    for topic_partition, records in messages.items():
        topic = topic_partition.topic

        if topic.startswith("cdc"):
            capture_cdc_events.delay([record.value for record in records])
            continue

        if topic != "message-app":
            raise Exception(f"Unknown topic {topic}")

        bulk_create_group_messages.delay([record.value for record in records])


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

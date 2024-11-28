"""
This file contains mixins for Kafka Consumers
"""

import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Callable

from kafka import KafkaConsumer
from kafka.errors import KafkaError

logger = logging.getLogger("default")


class BaseKafkaConsumerMixin(ABC):
    """
    Base Kafka Consumer Mixin
    """

    def __init__(
        self,
        *args,
        topics: list[str],
        bootstrap_servers: list[str] = os.environ["KAFKA_SERVERS"].split(","),
        **kwargs,
    ):
        """
        Initialize a Kafka Consumer.
        Parameters:
        bootstrap_servers: list[str] - List of kafka broker(s) addresses to connect to
            group_id: str - Consumer group ID
            auto_offset_reset: str - Where to start reading messages from when no offset ('earliest' or 'latest')
            enable_auto_commit: bool - Whether to auto-commit offsets
            value_deserializer: Callable - Function to deserialize message values
            key_deserializer: Callable - Function to deserialize message keys
            max_poll_records: int - Maximum number of records returned in a single call to poll()
            session_timeout_ms: int - Timeout used to detect consumer failures
        """
        self.__topics = topics
        self.__bootstrap_servers = bootstrap_servers
        self.__group_id = self.get_group_id()
        self.__value_deserializer = self.get_value_deserializer()
        self.__key_deserializer = self.get_key_deserializer()
        self.__auto_offset_reset = kwargs.get("auto_offset_reset", "earliest")
        self.__enable_auto_commit = kwargs.get("enable_auto_commit", True)
        self.__max_poll_records = kwargs.get("max_poll_records", 500)
        self.__session_timeout_ms = kwargs.get("session_timeout_ms", 10000)

        self._initialize_consumer()

    def _initialize_consumer(self) -> None:
        """
        Initialize the Kafka consumer with error handling
        """
        try:
            self._kafka_consumer = KafkaConsumer(
                *self.__topics,
                bootstrap_servers=self.__bootstrap_servers,
                group_id=self.__group_id,
                value_deserializer=self.__value_deserializer,
                key_deserializer=self.__key_deserializer,
                auto_offset_reset=self.__auto_offset_reset,
                enable_auto_commit=self.__enable_auto_commit,
                max_poll_records=self.__max_poll_records,
                session_timeout_ms=self.__session_timeout_ms,
            )
            logger.info(f"Kafka consumer initialized successfully: {self.__group_id}")
        except KafkaError as e:
            logger.error(f"Failed to initialize Kafka consumer: {str(e)}")
            raise

    @abstractmethod
    def get_group_id(self) -> str:
        """
        Returns the kafka consumer group id
        """

    @abstractmethod
    def get_value_deserializer(self) -> Callable:
        """
        Returns the kafka consumer value deserializer
        """

    def get_key_deserializer(self) -> Callable:
        """
        Returns the kafka consumer key deserializer
        """
        return lambda key: key.decode("utf-8")

    @property
    def consumer(self) -> KafkaConsumer:
        """
        Returns the kafka consumer
        """
        return self._kafka_consumer

    def subscribe(self, topics: list[str]) -> None:
        """
        Subscribe to the specified topics
        """
        try:
            self.consumer.subscribe(topics)
            logger.info(f"Subscribed to topics: {topics}")
        except Exception as e:
            logger.error(f"Failed to subscribe to topics {topics}: {str(e)}")
            raise

    def consume_messages(self, timeout_ms: int = 10) -> list[Any]:
        """
        Consume messages from subscribed topics
        """
        try:
            messages = self.consumer.poll(timeout_ms=timeout_ms)
            return messages
        except Exception as e:
            logger.error(f"Error consuming messages: {str(e)}")
            raise

    def commit(self) -> None:
        """
        Commit consumed offsets
        """
        try:
            self.consumer.commit()
        except Exception as e:
            logger.error(f"Failed to commit offsets: {str(e)}")
            raise

    def health_check(self) -> bool:
        """
        Check the health of the kafka consumer
        """
        try:
            return self.consumer.bootstrap_connected()
        except Exception as error:
            logger.error(f"Health check failed: {str(error)}")
            return False

    def close_connection(self) -> None:
        """
        Close the kafka consumer connection
        """
        self.consumer.close()
        logger.info(f"Kafka consumer closed: {self.__group_id}")


class BaseKafkaConsumer(BaseKafkaConsumerMixin):
    """
    Kafka Consumer Mixin
    """

    def get_group_id(self) -> str:
        """
        Returns the kafka consumer group id
        """
        return "kafka_consumer"

    def get_value_deserializer(self) -> Callable:
        """
        Returns the kafka consumer value deserializer
        """
        return lambda value: json.loads(value.decode("utf-8"))

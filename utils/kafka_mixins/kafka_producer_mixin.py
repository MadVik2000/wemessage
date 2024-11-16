"""
This file contains mixins for Kafka Producers
"""

import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from kafka import KafkaProducer
from kafka.errors import KafkaError

logger = logging.getLogger(__name__)


class BaseKafkaProducerMixin(ABC):
    """
    Base Kafka Producer Mixin
    """

    def __init__(
        self,
        *args,
        bootstrap_servers: list[str] = os.environ["KAFKA_SERVERS"].split(","),
        **kwargs,
    ):
        """
        This constructor is used to initialise a Kafka Producer.
        Parameters:
        bootstrap_servers: list[str] - List of kafka broker(s) addresses to connect to
            client_id: str - Client ID for the kafka producer̦
            value_serializer: str - Serializer for the value to sent as message to kafka broker(s)
            acks: int|str - Acknowledgement level for the kafka producer. Defaults to 'all'
                            (i.e. all replicas must acknowledge the message)
            retries: int - Number of retries for the kafka producer. Defaults to 0
            max_in_flight_requests_per_connection: int - Maximum number of concurrent requests a single kafka broker
                                                        can receive at a time. Defaults to 5 in case of retries > 0
            linger_ms: int - Time in milliseconds to wait for more messages before sending the current batch. Defaults to 10
            compression_type: str - Message Compression type for the kafka producer. Defaults to None
            batch_size: int - Maximum size of request in bytes to send to kafka broker(s). Defaults to 16384
            request_timeout_ms: int - Timeout (in milliseconds) for requests to kafka broker(s). Defaults to 30000
        """
        self.__bootstrap_servers = bootstrap_servers
        self.__client_id = self.get_client_id()
        self.__value_serializer = self.get_value_serializer()
        self.__key_serializer = self.get_key_serializer()
        self.__acks = kwargs.get("acks", "all")
        self.__retries = kwargs.get("retries", 0)
        self.__max_in_flight_requests_per_connection = 5 if not self.__retries else 1
        self.__linger_ms = kwargs.get("linger_ms", 10)
        self.__compression_type = kwargs.get("compression_type", None)
        self.__batch_size = kwargs.get("batch_size", 16384)
        self.__request_timeout_ms = kwargs.get("request_timeout_ms", 30000)

        self._initialize_producer()

    def _initialize_producer(self) -> None:
        """
        Initialize the Kafka producer with error handling
        """
        try:
            self._kafka_producer = KafkaProducer(
                bootstrap_servers=self.__bootstrap_servers,
                client_id=self.__client_id,
                value_serializer=self.__value_serializer,
                key_serializer=self.__key_serializer,
                acks=self.__acks,
                retries=self.__retries,
                max_in_flight_requests_per_connection=self.__max_in_flight_requests_per_connection,
                linger_ms=self.__linger_ms,
                compression_type=self.__compression_type,
                batch_size=self.__batch_size,
                request_timeout_ms=self.__request_timeout_ms,
            )
        except KafkaError as e:
            logger.error(f"Failed to initialize Kafka producer: {str(e)}")
            raise

    @abstractmethod
    def get_client_id(self) -> str:
        """
        Returns the kafka producer client id
        """

    @abstractmethod
    def get_value_serializer(self) -> Callable:
        """
        Returns the kafka producer value serializer
        """

    def get_key_serializer(self) -> Callable:
        """
        Returns the kafka producer key serializer
        """
        return str.encode

    @property
    def producer(self) -> KafkaProducer:
        """
        Returns the kafka producer
        """
        return self._kafka_producer

    def send_message(
        self,
        topic: str,
        value: Any,
        key: Any,
        partition: Optional[int] = None,
    ) -> None:
        """
        Send a message to Kafka with monitoring

        Parameters:
            topic: Target Kafka topic
            value: Message payload
            key: Message key
            partition: Specific partition (optional)
        """
        try:
            future = self.producer.send(
                topic=topic, value=value, key=key, partition=partition
            )
            future.get(timeout=3)
        except Exception as e:
            logger.error(f"Failed to send message to {topic}: {str(e)}")
            raise

    def send_messages_batch(
        self,
        topic: str,
        messages: list[Any],
        key_selector: Callable[[Any], Any] = None,
    ) -> None:
        """
        Send multiple messages efficiently in batch
        """
        futures = []
        for message in messages:
            key = key_selector(message) if key_selector else None
            futures.append(self.producer.send(topic=topic, value=message, key=key))

        # Wait for all messages to be sent
        for future in futures:
            future.get(timeout=3)

    def health_check(self) -> bool:
        """
        Check the health of the kafka producer
        """
        try:
            self.producer.bootstrap_connected()
        except Exception as error:
            logger.error(f"Health check failed: {str(error)}")
            return False

    def close_connection(self) -> None:
        """
        Close the kafka producer connection
        """
        self.producer.flush()
        self.producer.close()


class BaseKafkaProducer(BaseKafkaProducerMixin):
    """
    Kafka Producer Mixin
    """

    def get_client_id(self) -> str:
        """
        Returns the kafka producer client id
        """
        return "kafka_producer"

    def get_value_serializer(self) -> Callable:
        """
        Returns the kafka producer value serializer
        """
        return lambda value: json.dumps(value).encode("utf-8")

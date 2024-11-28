"""
This file contains the consumer base class for sdk
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Union

from django.db.models import Model

from message_sdk.exceptions import MessageException
from message_sdk.metaclass import BaseConsumerMetaclass


class MessageConsumer(metaclass=BaseConsumerMetaclass):
    """
    This class contains all the base methods required for subscribing messages.
    NOTE: Do not initialize this class but rather inherit it
    """

    model: Model
    trigger: Dict[
        Literal["create", "update", "delete"],
        Union[Dict[str, Dict[Literal["before", "after"], Any]]],
    ]
    _db_table_to_consumer_mapping: Dict[str, List[MessageConsumer]] = {}
    _db_table_to_model_mapping: Dict[str, Model] = {}

    def __init__(self) -> None:
        raise MessageException(message="Cannot initialize base consumer class")

    @classmethod
    def should_trigger(cls, instance, operation) -> bool:
        """
        This class method is used to manage additional trigger conditions
        """
        return True

    @classmethod
    def consume(cls, instance):
        """
        This class method should be overriden by inheriting class
        """
        raise NotImplementedError(
            "Cannot initialize subscribe class method for base class"
        )

    @classmethod
    def trigger_consumption(cls, instance):
        """
        This class method is used to trigger the consumption of the message
        """
        return cls.consume(instance)

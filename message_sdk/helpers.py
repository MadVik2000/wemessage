"""
This file contains all the helper functions for message sdk
"""

from typing import Any, Dict, Union

from django.db import transaction
from django.db.models import Model
from django.db.models.fields.related import ManyToManyField
from django.db.models.fields.reverse_related import ManyToOneRel, OneToOneRel

from message_sdk.consumer import MessageConsumer
from message_sdk.exceptions import MessageException


def filter_message(
    operation: str, before: Union[Dict, None], after: Union[Dict, None], table: str
):
    """
    This function is used to filter and trigger all consumers based on
    provided operation and table name.
    """

    consumers = MessageConsumer._db_table_to_consumer_mapping.get(table, [])

    consumers_to_trigger = []
    for consumer in consumers:
        if not hasattr(consumer, "trigger"):
            continue

        trigger = getattr(consumer, "trigger").get(operation)
        if not trigger:
            continue
        if trigger is True:
            consumers_to_trigger.append(consumer)
            continue

        if operation == "create":
            if after is None:
                raise MessageException(
                    f"After not provided in case of create operation on table {table}"
                )

            if before is not None:
                raise MessageException(
                    f"Before provided in case of create operation on table {table}"
                )

        elif operation == "update":
            if after is None:
                raise MessageException(
                    f"After not provided in case of update operation on table {table}"
                )

            if before is None:
                raise MessageException(
                    f"Before not provided in case of update operation on table {table}"
                )

        elif operation == "delete":
            if after is not None:
                raise MessageException(
                    f"After provided in case of delete operation on table {table}"
                )

            if before is None:
                raise MessageException(
                    f"Before not provided in case of delete operation on table {table}"
                )

        if trigger(before, after):
            consumers_to_trigger.append(consumer)

    if not consumers_to_trigger:
        return

    model = MessageConsumer._db_table_to_model_mapping.get(table, None)
    if not model:
        raise MessageException(f"Model not found for table {table}")

    instance = model(**(before and process_data_values(model, before) or {}))
    if after:
        for field, value in process_data_values(model, after).items():
            setattr(instance, field, value)

    with transaction.atomic():
        # using transaction.atomic to make sure that all consumers are triggered in a single transaction
        # in case any consumer fails, the whole consumer consumption will be null and void

        for consumer in consumers_to_trigger:
            if not consumer.should_trigger(instance, operation):
                continue

            try:
                consumer.trigger_consumption(instance)
            except Exception as error:
                raise MessageException(str(error)) from error


def process_data_values(model: Model, data: Dict[str, Any]):
    """
    Helper function to convert data fields to proper python instances.
    Since debezium returns every field as string, we need to convert them to proper python types
    """

    model_data = {}

    for field in model._meta.get_fields():
        if type(field) in [ManyToOneRel, OneToOneRel, ManyToManyField]:
            continue

        value = data.get(field.attname)

        if value is None and field.null:
            continue

        model_data[field.attname] = field.to_python(value)
    return model_data

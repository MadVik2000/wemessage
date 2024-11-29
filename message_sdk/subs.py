"""
Consumer function to process data published through debezium
"""

from message_sdk.exceptions import MessageException
from message_sdk.helpers import filter_message

operation_mapping = {"c": "create", "r": "read", "u": "update", "d": "delete"}


def capture_debezium_messages(data, **kwargs):
    """
    This function is used to validate data published through debezium
    It further triggers all the consumer functions based on db operations
    """

    if not data.get("payload"):
        raise MessageException(
            "No payload data found in data in message_sdk.subs.capture_debezium_messages"
        )

    if (
        isinstance(data.get("payload"), dict)
        and data["schema"].get("name") == "io.debezium.connector.common.Heartbeat"
    ):
        # not processing heartbeat messages
        return

    if not data["payload"].get("source"):
        raise MessageException(
            "No source data found in payload in message_sdk.subs.capture_debezium_messages"
        )

    if data["payload"]["source"].get("snapshot", "") == "true":
        # not processing snapshot messages
        return

    if not data["payload"].get("op"):
        raise MessageException(
            "No operation data found in payload in message_sdk.subs.capture_debezium_messages"
        )

    if "after" not in data["payload"]:
        raise MessageException(
            "No after data found in payload in message_sdk.subs.capture_debezium_messages"
        )

    if "before" not in data["payload"]:
        raise MessageException(
            "No before data found in payload in message_sdk.subs.capture_debezium_messages"
        )

    if not data["payload"]["source"].get("table"):
        raise MessageException(
            "No table data found in payload in message_sdk.subs.capture_debezium_messages"
        )

    consumer_operation = data["payload"]["op"]
    operation = operation_mapping.get(consumer_operation)
    if not operation:
        raise MessageException(
            f"Invalid operation: {consumer_operation} found in payload in message_sdk.subs.capture_debezium_messages"
        )

    if operation != "read":
        filter_message(
            operation=operation,
            before=data["payload"]["before"],
            after=data["payload"]["after"],
            table=data["payload"]["source"]["table"],
        )

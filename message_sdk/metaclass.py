"""
This file contains all the metaclasses used by message-sdk
"""

from django.db.models import Model

from message_sdk.exceptions import MessageException
from message_sdk.trigger import TriggerBase


class BaseMetaclass(type):
    """
    This is the base metaclass
    """

    _subclasses = set()

    def __new__(mcs, name, bases, namespace):
        if namespace["__module__"].startswith("message_sdk"):
            return super().__new__(mcs, name, bases, namespace)

        cls_name = f"{namespace['__module__']}.{namespace['__qualname__']}"

        if cls_name in mcs._subclasses:
            raise MessageException(message=f"{cls_name} already exists")
        mcs._subclasses.add(cls_name)

        if not namespace.get("model"):
            raise AttributeError(f"{cls_name} must have a model attribute")

        if not issubclass(namespace["model"], Model):
            raise TypeError(f"{cls_name}.model must be a django model")

        if namespace.get("trigger"):
            trigger = namespace["trigger"]
            if not isinstance(trigger, dict):
                raise TypeError(message=f"{cls_name}.trigger must be a dictionary")

            for trigger_key, trigger_values in trigger.items():
                if trigger_key not in ("create", "update", "delete"):
                    raise ValueError(
                        f"{cls_name}.trigger can only have create, update or delete keys"
                    )
                if (
                    not isinstance(trigger_values, TriggerBase)
                    and trigger_values is not True
                ):
                    raise TypeError(
                        f"{cls_name}.trigger[{trigger_key}] must be a Trigger or its value should be True"
                    )

                if trigger_values is True:
                    continue

                if not trigger_values.validate_operation(trigger_key):
                    if trigger_key == "create":
                        raise ValueError(
                            f"{cls_name}.trigger[{trigger_key}] must only contain after key"
                        )

                    if trigger_key == "update":
                        raise ValueError(
                            f"{cls_name}.trigger[{trigger_key}] must only contain before key"
                        )

        new_cls = super().__new__(mcs, name, bases, namespace)
        new_cls._db_table_to_consumer_mapping.setdefault(
            new_cls.model._meta.db_table, []
        ).append(new_cls)
        new_cls._db_table_to_model_mapping[new_cls.model._meta.db_table] = new_cls.model

        return new_cls


class BaseConsumerMetaclass(BaseMetaclass):
    """
    This is the base metaclass for consumers
    """

    def __new__(mcs, name, bases, namespace):

        if namespace["__module__"].startswith("message_sdk"):
            return super().__new__(mcs, name, bases, namespace)

        cls_name = f"{namespace['__module__']}.{name}"

        if not namespace.get("trigger"):
            raise AttributeError(f"{cls_name} must have a trigger attribute")

        if not namespace.get("consume"):
            raise AttributeError(f"{cls_name} must have a consume method")

        if not isinstance(namespace.get("consume"), classmethod):
            raise TypeError(f"{cls_name}.consume must be a class method")

        if any(base.__name__ != "MessageConsumer" for base in bases):
            raise MessageException(
                message="Multi-level inheritance is not allowed for events"
            )

        return super().__new__(mcs, name, bases, namespace)

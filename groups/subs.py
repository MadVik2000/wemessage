"""
This file contains all the subscribers for groups module.
"""

from groups.models import Group, GroupMember
from message_sdk.consumer import MessageConsumer
from utils.redis import RedisCacheMixin

cache_object = RedisCacheMixin()


class GroupSubscriber(MessageConsumer):
    """
    This subscriber is used to capture any creation or updation of a group
    """

    model = Group
    trigger = {"create": True, "update": True}

    @classmethod
    def consume(cls, instance):
        if not instance.is_active:
            cache_object.delete_cache(key_name=str(instance.id), model=cls.model)
            return

        cache_object.set_cache(
            key_name=str(instance.id), value=instance, model=cls.model
        )


class GroupMemberSubscriber(MessageConsumer):
    """
    This subscriber is used to capture any creation or updation of a group member
    """

    model = GroupMember
    trigger = {"create": True, "update": True}

    @classmethod
    def consume(cls, instance):
        if not instance.is_active:
            cache_object.delete_cache(
                key_name=f"{instance.group_id}-{instance.user_id}", model=cls.model
            )
            return

        cache_object.set_cache(
            key_name=f"{instance.group_id}-{instance.user_id}",
            value=instance,
            model=cls.model,
        )

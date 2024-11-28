"""
This file contains all the subscribers for users module.
"""

from django.contrib.auth import get_user_model

from message_sdk.consumer import MessageConsumer
from utils.redis import RedisCacheMixin

User = get_user_model()

cache_object = RedisCacheMixin()


class UserSubscriber(MessageConsumer):
    """
    This subscriber is used to capture any creation or updation of a user
    """

    model = User
    trigger = {"create": True, "update": True}

    @classmethod
    def consume(cls, instance):
        cache_object.set_cache(
            key_name=str(instance.uuid), value=instance, model=cls.model
        )

"""
This file contains basic redis caching implementation over a pythonic class.
"""

from typing import Any, Dict, Optional

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import Model

from groups.models import Group, GroupMember

User = get_user_model()


def custom_redis_key_function(key, prefix, _version):
    """
    Custom function to generate keys.

    Construct the key used by all other methods. By default, prepend
    the `key_prefix`. KEY_FUNCTION can be used to specify an alternate
    function with custom key making behavior.

    Removing the versioning for now
    """
    return f"{prefix}:{key}"


class RedisCacheMixin:
    """
    This class is a basic abstraction over django's inbuild caching system.
    """

    @property
    def cache_key_prefix(self):
        """
        This property is used to define cache prefix for particular model class.
        """
        return {
            Group: "GRP",
            GroupMember: "GMB",
            User: "USR",
        }

    def get_model_cache_key(
        self,
        key_name: str,
        model: Model,
    ) -> str:
        """
        Generate a cache key for the given key_name.

        Args:
            key_name: the name of the key to generate the cache key for

        Returns:
            str: the cache key
        """
        return "".join([self.cache_key_prefix[model], ":", key_name])

    def set_cache(
        self,
        key_name: str,
        value: Any,
        timeout: int = DEFAULT_TIMEOUT,
        model: Optional[Model] = None,
    ) -> None:
        """
        Set a value in the cache with the specified key name and timeout.

        Args:
            key_name: The name of the key to store the value under.
            value: The value to cache.
            timeout: The timeout for the cached value. Defaults to django's default cache timeout.

        """
        cache.set(
            self.get_model_cache_key(key_name, model) if model else key_name,
            value,
            timeout=timeout,
        )

    def bulk_set_cache(
        self,
        data: Dict[str, Any],
        timeout=DEFAULT_TIMEOUT,
        model: Optional[Model] = None,
    ) -> None:
        """
        Set multiple values in the cache with the specified timeout.

        Args:
            data: A dictionary containing the key name and value pairs to cache.
            timeout: The timeout for the cached values. Defaults to django's default cache timeout.
        """
        cache.set_many(
            (
                {
                    self.get_model_cache_key(key, model): value
                    for key, value in data.items()
                }
                if model
                else data
            ),
            timeout,
        )

    def get_cache(self, key_name: str, model: Optional[Model] = None) -> Any:
        """
        Retrieve a cached value for the specified key name.

        Args:
            key_name: The name of the key whose cached value is to be retrieved.

        Returns:
            The cached value associated with the given key name, or None if the key does not exist in the cache.
        """

        return cache.get(
            self.get_model_cache_key(key_name, model) if model else key_name
        )

    def bulk_get_cache(
        self, keys: list[str], model: Optional[Model] = None
    ) -> Dict[str, Any]:
        """
        Retrieve cached values for the specified list of key names.

        Args:
            keys: A list of key names whose cached values are to be retrieved.

        Returns:
            A dictionary containing key-value pairs of the specified keys and their associated cached values.
            If a key does not exist in the cache, it will not be included in the returned dictionary.
        """

        return cache.get_many(
            [self.get_model_cache_key(key, model) for key in keys] if model else keys
        )

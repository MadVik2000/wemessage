"""
This file contains basic redis caching implementation over a pythonic class.
"""

from typing import Any, Dict

from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT


class RedisCacheMixin:
    """
    This class is a basic abstraction over django's inbuild caching system.
    """

    @property
    def cache_key_prefix(self):
        """
        This property is used to define cache prefix for particular model class.
        """
        raise NotImplementedError()

    def get_cache_key(self, key_name: str) -> str:
        """
        Generate a cache key for the given key_name.

        Args:
            key_name: the name of the key to generate the cache key for

        Returns:
            str: the cache key
        """
        return "".join([self.cache_key_prefix, ":", key_name])

    def set_cache(
        self, key_name: str, value: Any, timeout: int = DEFAULT_TIMEOUT
    ) -> None:
        """
        Set a value in the cache with the specified key name and timeout.

        Args:
            key_name: The name of the key to store the value under.
            value: The value to cache.
            timeout: The timeout for the cached value. Defaults to django's default cache timeout.

        """
        cache.set(self.get_cache_key(key_name), value, timeout=timeout)

    def bulk_set_cache(self, data: Dict[str, Any], timeout=DEFAULT_TIMEOUT) -> None:
        """
        Set multiple values in the cache with the specified timeout.

        Args:
            data: A dictionary containing the key name and value pairs to cache.
            timeout: The timeout for the cached values. Defaults to django's default cache timeout.
        """
        cache.set_many(
            {self.get_cache_key(key): value for key, value in data.items()}, timeout
        )

    def get_cache(self, key_name) -> Any:
        """
        Retrieve a cached value for the specified key name.

        Args:
            key_name: The name of the key whose cached value is to be retrieved.

        Returns:
            The cached value associated with the given key name, or None if the key does not exist in the cache.
        """

        return cache.get(self.get_cache_key(key_name))

    def bulk_get_cache(self, keys: list[str]) -> Dict[str, Any]:
        """
        Retrieve cached values for the specified list of key names.

        Args:
            keys: A list of key names whose cached values are to be retrieved.

        Returns:
            A dictionary containing key-value pairs of the specified keys and their associated cached values.
            If a key does not exist in the cache, it will not be included in the returned dictionary.
        """

        return cache.get_many([self.get_cache_key(key) for key in keys])


def custom_redis_key_function(key, prefix, _version):
    """
    Custom function to generate keys.

    Construct the key used by all other methods. By default, prepend
    the `key_prefix`. KEY_FUNCTION can be used to specify an alternate
    function with custom key making behavior.

    Removing the versioning for now
    """
    return f"{prefix}:{key}"

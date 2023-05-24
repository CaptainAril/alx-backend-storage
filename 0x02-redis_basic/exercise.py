#!/usr/bin/env python3
"""Writing strings to Redis"""

import redis
import uuid
from typing import Union, Callable


class Cache:
    """Declares a Cache class."""
    def __init__(self) -> None:
        """Instantiaties a Cache instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Takes a data argument and returns a string.
        Saves `data` in redis database with a random uuid key,
        and returns key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, int, bytes]:
        """Takes a key, and converts the value data back to desired format.
        """
        value = self._redis.get(key)
        if value:
            if fn:
                return fn(value)
            return value
        return None

    def get_str(self, key: str) -> str:
        """Takes a key, and converts the value data to string.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Takes a key, and converts the value data to integer.
        """
        return (self.get(key, int))

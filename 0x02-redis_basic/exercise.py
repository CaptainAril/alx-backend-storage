#!/usr/bin/env python3
"""Writing strings to Redis"""

import redis
import uuid


class Cache:
    """Declares a Cache class."""
    def __init__(self) -> None:
        """Instantiaties a Cache instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: any) -> str:
        """Takes a data argument and returns a string.
        Saves `data` in redis database with a random uuid key,
        and returns key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

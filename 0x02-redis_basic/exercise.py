#!/usr/bin/env python3
"""Writing strings to Redis"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that counts how many times
    Cache class methods are called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Cache Decoratore that stores the history of inputs and outputs
    for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function.
        """
        input_key = method.__qualname__+':inputs'
        output_key = method.__qualname__+':outputs'
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function.
    """
    r = redis.Redis()
    method_name = method.__qualname__
    output_key = f'{method_name}:outputs'
    input_key = f'{method_name}:inputs'
    input_list = list(map(decode, r.lrange(input_key, 0, -1)))
    output_list = list(map(decode, r.lrange(output_key, 0, -1)))

    lt = list(zip(input_list, output_list))
    print(f"{method_name} was called {len(lt)} times:")
    for item in lt:
        k, v = item
        print(f"{method_name}(*{k}) -> {v}")


def decode(str: bytes) -> Union[str, int]:
    """Converts from bytes"""
    try:
        return str.decode('utf-8')
    except Exception as e:
        pass


class Cache:
    """Declares a Cache class."""
    def __init__(self) -> None:
        """Instantiaties a Cache instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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


cache = Cache()

cache.store("foo")
cache.store("bar")
cache.store(42)
replay(cache.store)

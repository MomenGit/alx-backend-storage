#!/usr/bin/env python3
"""Defines Caching Class"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    Store the history of inputs and outputs for a particular function
    Every time the original function will be called,
    we will add its input parameters to one list in redis,
    and store its output into another list.
    Args:
        fn (Callable): The wrapped method
    """
    ip_key = method.__qualname__+":inputs"
    op_key = method.__qualname__+":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(ip_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(op_key, str(result))
        return result

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator that takes a single method Callable arg and returns a Callable
    Create and return function that increments the count for that key
    every time the method is called and returns the value
    returned by the original method.
    Args:
        fn (Callable): The wrapped method
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        self._redis.incr(method.__qualname__)
        return method(self, *args, *kwds)
    return wrapper


class Cache:
    """A Redis caching class"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = uuid.uuid4().__str__()
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        Gets a value from redis and
        convert the data back to the desired format.
        Args:
            key (str): The key to the stored value
            callable (function): Converts the value to the desired format
        """
        data = self._redis.get(key)
        if fn is not None:
            return fn(data)
        else:
            return data

    def get_str(self, key: str):
        """
        Gets a value from redis and
        convert the data to str format.
        Args:
            key (str): The key to the stored value
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str):
        """
        Gets a value from redis and
        convert the data to int format.
        Args:
            key (str): The key to the stored value
        """
        return self.get(key, int)

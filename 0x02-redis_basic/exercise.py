#!/usr/bin/env python3
"""Defines Caching Class"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """A Redis caching class"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

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

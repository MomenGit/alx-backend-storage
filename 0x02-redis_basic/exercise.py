#!/usr/bin/env python3
"""Defines Caching Class"""
import redis
import uuid
from typing import Union


class Cache:
    """A Redis caching class"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = uuid.uuid4().__str__()
        self._redis.set(key, data)
        return key

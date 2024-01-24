#!/usr/bin/env python3
"""Defines the get_page function"""

import requests
import redis
from datetime import timedelta


def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL and returns it
    track how many times a particular URL was accessed
    cache the result with an expiration time of 10 seconds.
    Args:
        url (str): The url to be retrieved
    """
    if url is None:
        return ''
    redis_client = redis.Redis()

    visits_count_key = 'count:{}'.format(url)
    page_cache_key = 'result:{}'.format(url)

    redis_client.incr(visits_count_key)
    cached_page = redis_client.get(page_cache_key)

    if cached_page is not None:
        return str(cached_page)

    page = requests.get(url=url).content.decode('utf-8')
    redis_client.setex(page_cache_key, timedelta(seconds=10), page)
    return page

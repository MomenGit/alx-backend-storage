#!/usr/bin/env python3
"""Defines insert_school function"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection based on kwargs"""
    obj = mongo_collection.insert_one(kwargs)
    return obj.inserted_id

#!/usr/bin/env python3
"""Defines schools_by_topics function"""


def schools_by_topic(mongo_collection, topic):
    """Returns the list of school having a specific topic"""
    schools_with_topics = []
    cursor = mongo_collection.find(
        {"topics": {"$all": [topic]}})
    for school in cursor:
        schools_with_topics.append(school)

    return schools_with_topics

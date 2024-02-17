#!/usr/bin/env python3
"""Lists all documents in a mongodb collection"""


def list_all(mongo_collection):
    """ Return a list of all documents in a mongodb collection
    Or an empty list if no document in the collection
    """
    docs = []
    cursor = mongo_collection.find()
    for doc in cursor:
        docs.append(doc)
    return docs

#!/usr/bin/env python3
"""Provides some stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient("mongodb://127.0.0.1:27017")

    nginx_collection = client.logs.nginx

    docs_count = nginx_collection.count_documents({})
    get_count = nginx_collection.count_documents({"method": "GET"})
    post_count = nginx_collection.count_documents({"method": "POST"})
    put_count = nginx_collection.count_documents({"method": "PUT"})
    patch_count = nginx_collection.count_documents({"method": "PATCH"})
    delete_count = nginx_collection.count_documents({"method": "DELETE"})
    get_status_count = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"})
    recent_pipeline = [
        {"$group": {
            "_id": "$ip",
            "count": {"$sum": 1},
        }},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    recent_ten = nginx_collection.aggregate(recent_pipeline)

    print(f"{docs_count} logs")
    print("Methods:")
    print(f"\tmethod GET: {get_count}")
    print(f"\tmethod POST: {post_count}")
    print(f"\tmethod PUT: {put_count}")
    print(f"\tmethod PATCH: {patch_count}")
    print(f"\tmethod DELETE: {delete_count}")
    print(f"{get_status_count} status check")
    print("IPs:")
    for ip in recent_ten:
        print(f"\t{ip.get('_id')}: {ip.get('count')}")

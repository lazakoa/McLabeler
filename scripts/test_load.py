#!/bin/env python

from pymongo import MongoClient

if __name__== "__main__":
    client = MongoClient()
    db = client.imagedb
    collection = db['image-names']
    cursor = collection.find({})

    for doc in cursor:
        print(doc)

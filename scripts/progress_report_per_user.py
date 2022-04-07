#!/bin/env python

import argparse
from pymongo import MongoClient

parser = argparse.ArgumentParser(
        description="generates a porgress report")

parser.add_argument("--host", 
        default='localhost',
        help="default is localhost")

parser.add_argument("--port", 
        default=27017,
        help="default port is 27017")

args = parser.parse_args()

client = MongoClient(args.host, args.port)
db = client['imagedb']
collection = db['image-names']
cursor = collection.find({})

total = 0
author_count = dict()

for doc in cursor:
    total += 1 
    if doc['relabeled'] == 1:
        author_count.setdefault(doc['author'], 0)
        author_count[doc['author']] += 1

print("Per author statistics.")

for author in author_count.keys():
    print("Author: ", author, " Total: ", author_count[author])

print(total)



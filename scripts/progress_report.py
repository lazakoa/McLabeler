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
relabeled = 0

for doc in cursor:
    total += 1 
    if doc['relabeled'] == 0:
        relabeled += 1


print('The total number of documents is: ', total)
print('The total number of relabeled images is: ', total - relabeled)

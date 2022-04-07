#!/bin/env python

"""
!!WARNING WARNING!!

Run this script once to initialize the database. Running this script
more than once will make a mess.

"""

from pymongo import MongoClient
import argparse
import datetime
from os import listdir

parser = argparse.ArgumentParser(
        description="loads data into mongodb")

parser.add_argument("--host", 
        default='localhost',
        help="default is localhost")

parser.add_argument("--port", 
        default=27017,
        help="default port is 27017")

parser.add_argument("data",
        help="directory where raw images are stored")

args = parser.parse_args()

"""
Loading the filenames from the data directory.

"""

file_names = listdir(args.data)

"""
Setting up MongoDB.
"""

client = MongoClient(args.host, args.port)
db = client['imagedb']
collection = db['image-names']

"""
Loading the data into MongoDB.
"""

for name in file_names:
    """
    "relabled" will take a dictionary of:
        
    { "new_label": ...., "user": ...}

    Setting all "rebaled" values to be 0 temporarily.
    """

    post = { "original" : name,
             "relabeled": 0}

    post_id = collection.insert_one(post)

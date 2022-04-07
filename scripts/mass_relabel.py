#!/bin/env python

from pymongo import MongoClient
import argparse
import datetime
import os
from os import listdir, mkdir
from shutil import copyfile

"""
Configuring the cli to accept options.
"""

parser = argparse.ArgumentParser(
        description="converts from old filenames to new filenames")

parser.add_argument("--source", 
        default='../data',
        help="directory with original files")

parser.add_argument("--target", 
        default="../new_data",
        help="directory new files")

parser.add_argument("--host", 
        default='localhost',
        help="default is localhost")

parser.add_argument("--port", 
        default=27017,
        help="default port is 27017")

args = parser.parse_args()

"""
Connecting to MongoDB.
"""

client = MongoClient(args.host, args.port)
db = client['imagedb']
collection = db['image-names']

"""
Mass rename.
"""

filenames = listdir(args.source)

if not os.path.exists(args.target):
    mkdir("../new_data")

for filename in filenames:
    record = collection.find_one({'original' : filename})
    copyfile('../data/' + filename,
            '../new_data/' + record['new_label'])

print("FINISHED RENAMING")


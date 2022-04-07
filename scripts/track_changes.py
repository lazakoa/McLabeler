
import argparse
from pymongo import MongoClient
import os
import shutil

parser = argparse.ArgumentParser(
        description="generates a progress report")

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


hold_changes = {}

def parseChanges(old_name, new_name):
    left_s_o = old_name.split('_c')
    left_s_n = new_name.split('_c')
    right_s_o = left_s_o[-1].split('.')
    right_s_n = left_s_n[-1].split('.')
    o_lab = right_s_o[0]
    n_lab = right_s_n[0]

    uniqueID = left_s_o[0]

    c_o = 'c' + o_lab[0]
    n_o = 'n' + o_lab[2]
    h_o = 'h' + o_lab[-1]
    c_n = 'c' + n_lab[0]
    n_n = 'n' + n_lab[2]
    h_n = 'h' + n_lab[-1]

    old_labs = [c_o, n_o, h_o]
    new_labs = [c_n, n_n, h_n]

    return [uniqueID,old_labs, new_labs]

def parse_author_change(author_change,change_t):
    if author_change == []:
        ret_change = [change_t[0],change_t[1],change_t[2]]
        return [ret_change]
    else:
        adding_change = [change_t[0],change_t[1], change_t[2]]
        new_author_change = author_change + [adding_change]
        return new_author_change

for doc in cursor:
    if doc['relabeled'] == 1:
        author = doc['author']
        old_name = doc['original']
        new_name = doc['new_label']

        if author not in hold_changes.keys():
            hold_changes[author] = []

        if old_name != new_name:
            change_tuple = parseChanges(old_name, new_name)
            try:
                authors_changes = hold_changes[author]
            except:
                authors_changes = []
            new_author_changes = parse_author_change(authors_changes,change_tuple)

            hold_changes[author] = new_author_changes


def find_image(change_in, author_in):
    list_images = os.listdir("static/data")
    end_string = ''.join(str(x) for x in change_in[1])
    end_new_string = ''.join(str(x) for x in change_in[2])
    p_filename = str(change_in[0])+"_"+str(end_string) + str(".png")
    for image in list_images:
        if image == p_filename:
            #print(image)
            shutil.copyfile("data/" + image, author_in + "/" + str(change_in[0])+ "_" + str(end_new_string) + ".png")


def gen_changedirs(hold_change):
    for key in hold_change.keys():
        if not os.path.exists(key):
            os.makedirs(key)
        change_array = hold_change[key]
        for changes in change_array:
            print(changes)
            find_image(changes,key)

        # find image


gen_changedirs(hold_changes)

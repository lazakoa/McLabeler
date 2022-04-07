#!/bin/env python

from flask import Flask
from flask import Flask, flash, redirect, render_template
from flask import request, session, abort
from pymongo import MongoClient

import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)

"""
Connect to MongoDB and getting the user accounts and image records.
"""

client = MongoClient()
image_db = client['imagedb']
users = image_db['users'] 
images = image_db['image-names'] # This is our collection

image_queue = images.find({ "relabeled" : 0 })

# TODO, add support for return to previously labeled images.
previous_queue = None

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return do_relabel_image()


@app.route('/login', methods=['POST'])
def do_admin_login():

    if session.get('logged_in'):
        return do_relabel_image()
    
    if request.method == "POST":
        password = request.form['password']
        username = request.form['username']

        query = users.find_one({'username': username})
        
        if query == None:
            return home()
        else:
            if query['password'] == password:
                session['logged_in'] = True
                session['username'] = username

                return do_relabel_image()
            else:
                return 'Invalid password.'

    return home()

@app.route('/signup', methods=['GET', 'POST'])
def do_user_signup():

    if session.get('logged_in'):
        return do_relabel_image()

    if request.method == "POST":
        password = request.form['password']
        username = request.form['username']

        query = users.find_one({"username" : username })

        user = { 'username' : username,
                 'password' : password}

        if query == None:

            users.insert_one(user)
            session['logged_in'] = True
            session['username'] = username

            return do_relabel_image()
        else:
            return "Username already exists."

    return render_template('signup.html')

# in progress, adding users, still working on it
@app.route('/relabel', methods=['GET', 'POST'])
def do_relabel_image(previous=False):
    
    """
    Read off the record queue, display a message if queue is empty.
    """
    
    # CHECK IF BUG PERSISTS
    if request.method == "GET":

        try:
            record = next(image_queue)
        except StopIteration:
            return "Congrats, You're Done :) To be sure reboot app."
        
        session['current'] = record
        path = "/static/data/" + record['original']


        return render_template('relabel.html',
                image_path=path,
                image_name=record['original'])

    if request.method == "POST":
        # TODO, take the input from the form and update the record
        # BUG WOULD START HERE, add a take off the cursor here  
        record = session.get('current')

        contour = request.form.get('contour')
        numbers = request.form.get('numbers')
        hands = request.form.get('hands')
         
        updated_label= record['original'][:-6] + createLabel(
                                                    contour,
                                                    numbers,
                                                    hands)
        
        new_record = { "original": record["original"],
                "relabeled": 1,
                "new_label": updated_label,
                "author": session["username"],
                "date": datetime.datetime.utcnow()}

        print(new_record)

        """
        images.update_one("_id": record["_id"],
                "$set": new_record,
                upsert=False)
        """

        try:
            record = next(image_queue)
        except StopIteration:
            return "Congrats, You're Done :) To be sure reboot app."

        session['current'] = record
        path = "/static/data/" + record['original']


        return render_template('relabel.html',
                image_path=path,
                image_name=record['original'])

    # THIS ISN'T NEEDED
    return render_template('relabel.html',
            image_path=path,
            image_name=record['original'])

def createLabel(contour, numbers, hands):
    # small utility function to creat a c*n*h* label
    label = '' 

    if contour == None:
        label = 'c' + '0'
    else:
        lable = 'c' + '1'

    if numbers == None:
        label = label + 'n' + '0'
    else:
        label = label + 'n' + '1'

    if hands == None:
        label = label + 'h' + '0'
    else:
        label = label + 'h' + '1'

    return label

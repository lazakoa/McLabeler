#!/bin/env python

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Index Page"

"""
@app.route('/hello')
def hello():
    return "Hello, World"
"""

@app.route('/user/<username>')
def show_user_profile(username):
    # Show the user profile for that user
    return "User %s" % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return "Post %d" % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after the /path/
    return "Subpath %s" % subpath

@app.route('/projects/')
def projects():
    return "The project page"

@app.route('/about')
def about():
    return "The about page"


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

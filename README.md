# Da da da I'm labelin' it

McLabeler is a small utility to help relabel a relatively larger dataset. App follows the KISS principle.

## Todo 
1. Make a script to load the raw data into MongoDB, while adding the necessary metadata.
* figure out pymongo
* hook it up to the db
* set up a users db and a images db
2. Make a login page.
3. Make a logout page.
4. Make a main page, this is where the relabeling happens.

## Howto

starting mongo:
mongod --port 27017 --dbpath=./database

starting flask:
FLASK_APP=example.py FLASK_DEBUG=1 python -m flask run

Or alternatively use FLASK_ENV=developement to enable page reload on
code change.

## Notes

Figure out how to store binary data in mongodb, take a look at gridfs.
Also take a look at how to save images in mongodb using python.

There is no need to store the image binary in mongo. The only thing 
that will be stored in the db is the image name. The relabeling 
process will on create new labels, the images can stay in a dir. This
will simplify the app significantly.


# Da da da I'm labelin' it

McLabeler is a small utility to help relabel a relatively large dataset. App follows the KISS principle.

## How-to run the app

Starting mongo:
mongod --port 27017 --dbpath=./database

Starting flask in debug mode:
FLASK_APP=mclabeler.py FLASK_DEBUG=1 python -m flask run

If you are using the application for the first time, you must first load all the images into MongoDB. Do this with by running:
./load_data.py

If running for the first time, you must also copy all the images from the **data/** direcotor into the **static/data** directory. Doing so is required for Flask to display the images.

## Notes

Two things left to do:
1. Figure out how to deploy it
2. Add an option to view previous images.

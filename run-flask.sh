#!/bin/bash -e

cd ~/McLabeler
source bin/activate

FLASK_APP=mclabeler.py python -m flask run --host=0.0.0.0
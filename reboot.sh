#!/usr/bin/env bash


while true
do
    screen -X -S mclabel quit
    flask_process=$(pgrep python -m)
    kill $flask_process
    screen -d -m -S mclabel ~/McLabeler/run-flask.sh
    sleep 1200
    echo "Restarting server"
done

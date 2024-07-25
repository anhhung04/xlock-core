#!/bin/sh
echo 'Waiting for postgres...'
while ! nc -z database 5432; do
  sleep 0.1
done
echo 'Starting migration...'
alembic upgrade head

while true; do
    python app.py
    echo 'App crashed, restarting in 5 seconds...'
    sleep 5
done
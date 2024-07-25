#!/bin/sh
echo 'Waiting for postgres...'
while ! nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do
  sleep 0.1
done
echo 'Starting migration...'
alembic upgrade head

while true; do
  fastapi run app.py --host 0.0.0.0 --port ${PORT}
  echo 'App crashed, restarting in 5 seconds...'
  sleep 5
done

#!/bin/sh
echo "Waiting for database..."

# Wait for database to be up
while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "Database is up!"

exec "$@"
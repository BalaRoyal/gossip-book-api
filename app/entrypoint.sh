#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $PG_HOST $PG_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
python manage.py makemigrations user_profile
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
exec "$@"
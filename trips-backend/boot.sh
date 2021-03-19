#!/bin/sh

if [ "$DB_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput --clear
exec gunicorn -b :8000 --access-logfile - --error-logfile - besttrips.wsgi
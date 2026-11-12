#!/bin/sh

set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput

python manage.py migrate 

python manage.py create_admin

echo "Starting Gunicorn..."
exec gunicorn verba.configs.wsgi:application \
    --bind 0.0.0.0:80 \
    --workers 3 \
    --access-logfile - \
    --error-logfile -

#!/bin/sh

python manage.py collectstatic --no-input

gunicorn wemessage.wsgi:application -w 4 -b 0.0.0.0:8000
#!/bin/sh
# Run database migrations
flask db upgrade

# Start the application using the same command you had before
exec gunicorn --bind 0.0.0.0:8080 wsgi:application
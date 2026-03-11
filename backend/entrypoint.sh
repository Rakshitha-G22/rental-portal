#!/bin/sh
# Set the app factory using a compatible syntax
export FLASK_APP="app:create_app()"

# Try to run migrations (Optional, remove if it continues to fail)
flask db upgrade

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:8080 wsgi:application
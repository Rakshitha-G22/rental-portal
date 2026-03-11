#!/bin/sh
# Ensure the app knows where to find the Flask factory
export FLASK_APP=app:create_app()

# Try to run migrations
flask db upgrade

# If migration fails, the exit code stops the container.
# If you want it to continue even if migration fails (not recommended), use '|| true'
# flask db upgrade || echo "Migration skipped"

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:8080 wsgi:application
#!/bin/sh
# No migration commands needed here because db.create_all() is in __init__.py
# Start Gunicorn directly
exec gunicorn --bind 0.0.0.0:8080 "app:create_app()"
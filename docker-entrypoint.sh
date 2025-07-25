#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py migrate

echo "Starting server"
uvicorn core.asgi:application --host 0.0.0.0 --port 8000

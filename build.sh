#!/bin/bash

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt




# Run Django migrations (even for SQLite)
echo "Running migrations..."
python manage.py migrate

# Collect static files (if any)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application using Gunicorn
echo "Starting the application with Gunicorn..."
gunicorn chatbot.wsgi:application --bind 0.0.0.0:$PORT

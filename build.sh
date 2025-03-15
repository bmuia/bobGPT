#!/bin/bash

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Download NLTK 'punkt' resource
echo "Downloading NLTK 'punkt' resource..."
python -c "import nltk; nltk.download('punkt')"

# Run training script
echo "Training the model..."
python -m chat.train

# Run Django migrations (even for SQLite)
echo "Running migrations..."
python manage.py migrate

# Collect static files (if any)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application using Gunicorn
echo "Starting the application with Gunicorn..."
gunicorn chatbot.wsgi:application --bind 0.0.0.0:$PORT

# Use official Python image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    NLTK_DATA=/usr/local/nltk_data

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn (if not in requirements.txt)
RUN pip install gunicorn

# Copy project files
COPY . .

# Download required NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet'); nltk.download('omw-1.4')"

# Run model training
RUN python -m chat.train

# Collect static files
RUN mkdir -p /app/staticfiles && python manage.py collectstatic --noinput

# Apply migrations
RUN python manage.py migrate --noinput

# Expose port
EXPOSE 8000

# Start the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "chatbot.wsgi:application"]

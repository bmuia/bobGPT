# Use official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn separately (if not in requirements.txt)
RUN pip install gunicorn

# Copy project files
COPY . .


# Install dependencies
RUN pip install -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet'); nltk.download('omw-1.4')"

# Explicitly set NLTK data path
ENV NLTK_DATA=/usr/local/nltk_data

# Run model training
RUN python -m chat.train



# Set environment variables
ENV PYTHONUNBUFFERED=1

# Ensure static files are collected
RUN mkdir -p /app/staticfiles && python manage.py collectstatic --noinput

# Run migrations before starting the server
RUN python manage.py migrate --noinput

# Expose port
EXPOSE 8000

# Run Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "chatbot.wsgi:application"]

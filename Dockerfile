# Use official Python image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    NLTK_DATA="/usr/local/nltk_data"

# Set the working directory
WORKDIR /app

# Install venv and create a virtual environment
RUN python -m venv /app/venv

# Activate virtual environment for all future RUN commands
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements and install dependencies in venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy project files
COPY . .

# Ensure NLTK data is downloaded
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet'); nltk.download('omw-1.4')"

# Copy trained model (ensure it exists)
COPY chat/chatbot_model.pth /app/chat/chatbot_model.pth

# Collect static files
RUN mkdir -p /app/staticfiles && python manage.py collectstatic --noinput

# Apply migrations
RUN python manage.py migrate --noinput

# Expose port
EXPOSE 8000

# Run Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "chat.wsgi:application"]

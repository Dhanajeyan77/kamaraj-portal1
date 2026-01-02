# 1. Use Python 3.11 Slim
FROM python:3.11-slim

# 2. Install Java 21 AND the libraries needed for PostgreSQL (psycopg2)
RUN apt-get update && \
    apt-get install -y openjdk-21-jdk-headless gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 3. Set up the application
WORKDIR /app
COPY . /app

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Tell Render we are using a dynamic port
EXPOSE 5000

# 6. Start Gunicorn with ONE worker and bind to the $PORT
# Added --workers 1 to prevent memory issues and multiprocessing conflicts
CMD ["sh", "-c", "gunicorn --workers 1 --bind 0.0.0.0:$PORT app:app"]
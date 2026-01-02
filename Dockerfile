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

# 6. Start Gunicorn and bind to the $PORT Render gives us
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]
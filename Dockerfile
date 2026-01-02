# Use Python 3.11 for better performance
FROM python:3.11-slim

# Install Java (JRE and JDK)
RUN apt-get update && \
    apt-get install -y openjdk-21-jdk-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Use Gunicorn to handle multiple requests safely
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

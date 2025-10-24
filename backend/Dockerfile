# Use Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential && \
    rm -rf /var/lib/apt/lists/*
    
# Install dependencies
COPY requirements.txt .
# RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev

RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 5000

ENV FLASK_ENV=development
ENV FLASK_APP=app.py
# Run Flask app
# CMD ["python", "app.py"]

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
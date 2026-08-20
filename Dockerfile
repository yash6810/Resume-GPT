# ResumeGPT Production Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy full application code (backend, frontend, data)
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY data/ ./data/

# Set working directory to backend
WORKDIR /app/backend

# Default port
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Run uvicorn server binding to 0.0.0.0 and dynamic $PORT
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

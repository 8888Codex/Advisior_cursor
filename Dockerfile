# Dockerfile para Railway - Backend Python apenas
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files first
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r python_backend/requirements.txt

# Expose port (Railway seta via $PORT)
EXPOSE 8000

# Start command
CMD python3 -m uvicorn python_backend.main:app --host 0.0.0.0 --port ${PORT:-8000}


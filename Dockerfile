# Dockerfile para Railway - Backend Python apenas
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY python_backend/requirements.txt /app/python_backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r python_backend/requirements.txt

# Copy apenas backend Python
COPY python_backend /app/python_backend

# Expose port (Railway seta via $PORT)
EXPOSE $PORT

# Start command
CMD python3 -m uvicorn python_backend.main:app --host 0.0.0.0 --port $PORT


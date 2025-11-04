# Dockerfile para Backend Python - Railway
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro
COPY python_backend/requirements.txt /app/requirements.txt

# Instalar dependências
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copiar todo código do backend
COPY python_backend/ /app/python_backend/
COPY shared/ /app/shared/

# Porta exposta (Railway usa $PORT dinamicamente)
EXPOSE $PORT

# Comando de inicialização
CMD python3 -m uvicorn python_backend.main:app --host 0.0.0.0 --port ${PORT:-8000}

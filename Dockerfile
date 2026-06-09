FROM python:3.12-slim

WORKDIR /app

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copiar archivos de dependencias
COPY pyproject.toml uv.lock ./

# Instalar dependencias del sistema y de python usando uv
RUN uv sync --frozen

# Copiar el codigo fuente
COPY src/ ./src/
COPY data/ ./data/

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV PYTHONPATH=/app/src

# Exponer el puerto por defecto de Cloud Run
EXPOSE 8080

# Comando para arrancar el servidor ADK en produccion
CMD ["uv", "run", "adk", "web", "src", "--port", "8080", "--host", "0.0.0.0"]

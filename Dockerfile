# Imagen base ligera de Python
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (bcrypt, compiladores, MySQL client)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO el proyecto dentro del contenedor
COPY . .

# Render asigna el puerto dinámicamente
ENV PORT=10000

# Exponer el puerto
EXPOSE $PORT

# Ejecutar FastAPI con uvicorn
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]

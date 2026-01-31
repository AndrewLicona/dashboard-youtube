# 1️⃣ Imagen base ligera
FROM python:3.11-alpine

# 2️⃣ Definir directorio de trabajo dentro del contenedor
WORKDIR /app

# 3️⃣ Instalar dependencias del sistema necesarias
RUN apk add --no-cache gcc g++ musl-dev libffi-dev

# 4️⃣ Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/data

# 5️⃣ Copiar el resto del proyecto
COPY . .

# 6️⃣ Exponer el puerto de FastAPI
EXPOSE 8000

# 7️⃣ Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 8️⃣ Comando de inicio: correr cron-services y luego FastAPI
CMD ["sh", "-c", "python -m src.services.fetch_data && python -m src.services.fetch_daily && uvicorn main:app --host 0.0.0.0 --port 8000"]

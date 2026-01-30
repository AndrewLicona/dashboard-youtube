# 1️⃣ Imagen base ligera
FROM python:3.11-alpine

# 2️⃣ Definir directorio de trabajo dentro del contenedor
WORKDIR /app

# 3️⃣ Instalar dependencias del sistema necesarias para compilar paquetes Python
RUN apk add --no-cache gcc g++ musl-dev libffi-dev

# 4️⃣ Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Crear directorio para datos
RUN mkdir -p /app/data

# 5️⃣ Copiar el resto del proyecto
COPY . .

# 6️⃣ Exponer el puerto de Streamlit
EXPOSE 8501

# 7️⃣ Definir variables de entorno para evitar advertencias de Streamlit
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_HEADLESS=true
ENV PYTHONPATH=/app

# 8️⃣ Comando de inicio: ejecutar primero servicios de descarga y luego Streamlit
CMD ["sh", "-c", "python -m src.services.fetch_data && python -m src.services.fetch_daily && streamlit run main.py"]

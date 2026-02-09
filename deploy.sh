#!/bin/bash

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Iniciando Despliegue de Dashboard YouTube${NC}"

# 0. Actualizar Código
echo -e "${YELLOW}📥 Descargando últimos cambios...${NC}"
git pull origin main

# 1. Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no encontrado. Por favor instálalo primero."
    exit 1
fi

# 2. Verificar Puertos (Opcional, doble check)
echo -e "${YELLOW}🔍 Verificando puertos...${NC}"
if netstat -tuln | grep -q ":8000 "; then
    echo "⚠️  ADVERTENCIA: El puerto 8000 parece estar en uso."
else
    echo "✅ Puerto 8000 libre."
fi
if netstat -tuln | grep -q ":5173 "; then
    echo "⚠️  ADVERTENCIA: El puerto 5173 parece estar en uso."
else
    echo "✅ Puerto 5173 libre."
fi

# 3. Crear directorio de datos si no existe
echo -e "${YELLOW}📂 Preparando carpetas...${NC}"
mkdir -p backend/data
chmod 777 backend/data # Permisos para que Docker escriba la DB

# 3.5 Configurar entorno
export VITE_API_URL="/api" # Forzamos que use el proxy de Nginx
export API_BASE_URL="https://dashboard.andrewlamaquina.my"
export FRONTEND_URL="https://dashboard.andrewlamaquina.my"

# 4. Construir y Levantar
echo -e "${YELLOW}🛑 Deteniendo contenedores antiguos...${NC}"
docker-compose down || true  # Ignorar error si no hay nada corriendo

echo -e "${YELLOW}🐳 Construyendo contenedores...${NC}"
docker-compose up -d --build --remove-orphans

# 5. Estado Final
echo -e "${GREEN}✅ ¡Despliegue Completado!${NC}"
echo "-----------------------------------"
echo "Frontend: http://localhost:${FRONTEND_PORT:-5173}"
echo "Backend:  http://localhost:${BACKEND_PORT:-8000}"
echo "-----------------------------------"
echo "Para ver logs: docker-compose logs -f"

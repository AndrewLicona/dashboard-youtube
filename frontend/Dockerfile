# 1️⃣ Imagen de Node.js
FROM node:20-alpine

# 2️⃣ Directorio de trabajo
WORKDIR /app

# 3️⃣ Copiar dependencias e instalarlas
COPY package*.json ./
RUN npm install

# 4️⃣ Copiar el resto del código
COPY . .

# 5️⃣ Exponer puerto de Vite (Development)
EXPOSE 5173

# 6️⃣ Comando de inicio (con --host para que Docker lo exponga)
CMD ["npm", "run", "dev", "--", "--host"]

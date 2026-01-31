# 1️⃣ Build Stage (Node.js)
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# Argumento para "quemar" la variable de entorno durante el build de React
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}
RUN npm run build

# 2️⃣ Production Stage (Nginx)
FROM nginx:alpine
# Copiar el build de React a la carpeta de Nginx
COPY --from=build /app/dist /usr/share/nginx/html
# Copiar configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Exponer puerto 80 (interno del container)
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

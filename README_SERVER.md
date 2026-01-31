# 🚀 Guía de Despliegue en Servidor Linux (CasaOS / Ubuntu)

## 1. Opción A: Usando Git (Recomendado)
Si ya subiste el código a GitHub/GitLab:
1.  Conéctate por SSH a tu servidor.
2.  Clona el repo:
    ```bash
    git clone <TU_URL_DEL_REPO>
    cd dashboard-youtube
    ```
3.  Crea el archivo `.env` en la carpeta `backend/` (ver paso 2).

## 1. Opción B: Subida Manual
Si prefieres no usar Git en el servidor, sube los siguientes archivos con FileZilla:
- `backend/`
- `frontend/`
- `docker-compose.yml`
- `deploy.sh`

## 2. Configuración
Asegúrate de que tienes el archivo `.env` dentro de `backend/` con tus credenciales de Google:
```bash
# backend/.env
GOOGLE_CLIENT_ID=tu_client_id
GOOGLE_CLIENT_SECRET=tu_client_secret
SECRET_KEY=tu_clave_secreta_random
# DATABASE_URL no es necesario, Docker lo configura automático para SQLite
```

## 3. Ejecutar
En la terminal de tu servidor, navega a la carpeta y corre:
```bash
chmod +x deploy.sh
./deploy.sh
```

## 4. Puertos
Por defecto usará:
- **Frontend**: Puerto `5173`
- **Backend**: Puerto `8000`

Si necesitas cambiarlos (porque chocan con CasaOS), crea un archivo `.env` en la raíz (junto al docker-compose.yml):
```bash
BACKEND_PORT=8050
FRONTEND_PORT=5174
```
Y vuelve a ejecutar `./deploy.sh`.

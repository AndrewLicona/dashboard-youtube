# 🚀 Dashboard YouTube - React + FastAPI (Dockerized)

Este es un dashboard avanzado para analíticas de YouTube, reescrito desde cero utilizando una arquitectura moderna y escalable.

## ✨ Características Nuevas
- **Frontend**: React 19 + Vite + Tailwind CSS (Tema "Gamer Green").
- **Backend**: FastAPI (Python) para alto rendimiento.
- **Base de Datos**: SQLite seguro con encriptación (Fernet) para tokens de OAuth.
- **Multiusuario**: Soporte para múltiples canales simultáneos.
- **URLs Públicas**: Comparte `tudominio.com/dashboard/CHANNEL_ID`.
- **Docker**: Listo para desplegar en cualquier servidor Linux (Ubuntu/CasaOS).

---

## 🛠️ Instalación Local (Desarrollo)

### 1. Clonar
```bash
git clone <URL_REPOSITORIO>
cd dashboard-youtube
```

### 2. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🐳 Despliegue en Servidor (Producción)

Este proyecto está diseñado para correr con **Docker Compose**.

### Prerrequisitos
- Servidor Linux (Ubuntu, Debian, CasaOS).
- Docker y Docker Compose instalados.

### Pasos Rápidos
1. Sube los archivos al servidor.
2. Ejecuta el script de despliegue:
```bash
chmod +x deploy.sh
./deploy.sh
```

Ver [README_SERVER.md](./README_SERVER.md) para la guía detallada de despliegue.

---

## 🔒 Variables de Entorno (.env)
Crea un archivo `.env` en `backend/` con:
```bash
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
SECRET_KEY=...
```

---

## 👨‍💻 Autor
Desarrollado por **Andrew Licona**.
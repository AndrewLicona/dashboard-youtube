import os
import logging
from dotenv import load_dotenv

import certifi

# FIX: Limpiar variables de entorno SSL que puedan apuntar a entornos virtuales antiguos/borrados
# Y forzar el uso del certificado del entorno actual
if "SSL_CERT_FILE" in os.environ:
    del os.environ["SSL_CERT_FILE"]
if "REQUESTS_CA_BUNDLE" in os.environ:
    del os.environ["REQUESTS_CA_BUNDLE"]

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("youtube_dashboard")

# Cargar variables de entorno
load_dotenv()

# Configuración de la API (OAuth 2.0)
API_KEY = os.getenv("API_KEY") # Optional: For public data if needed
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-it") # For JWT sessions

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dashboard.db")

# Deprecated (Legacy)
# CHANNEL_ID = os.getenv("CHANNEL_ID") 
# TOKEN_PICKLE_FILE = "token.pickle"

# Validaciones críticas
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    logger.warning("⚠️ Faltan credenciales de Google OAuth (CLIENT_ID/SECRET) en .env")


# Configuración de la App
DATA_DIR = "data"
OS_MAKES_DIRS = True  # Para control interno si es necesario

# Crear directorio de datos si no existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

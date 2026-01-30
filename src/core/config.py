import os
import logging
from dotenv import load_dotenv

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("youtube_dashboard")

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_PICKLE_FILE = "token.pickle"

# Validaciones básicas
if not API_KEY:
    logger.warning("API_KEY no encontrada en el archivo .env")
if not CHANNEL_ID:
    logger.warning("CHANNEL_ID no encontrada en el archivo .env")

# Configuración de la App
DATA_DIR = "data"
OS_MAKES_DIRS = True  # Para control interno si es necesario

# Crear directorio de datos si no existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

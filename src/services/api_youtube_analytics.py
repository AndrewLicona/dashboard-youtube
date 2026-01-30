from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import os
from src.core.config import CLIENT_SECRET_FILE, TOKEN_PICKLE_FILE, logger

SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly"]

def get_youtube_analytics_service():
    """Crea un cliente de la API de YouTube Analytics con OAuth2."""
    creds = None
    # Revisar si ya existe token
    if os.path.exists(TOKEN_PICKLE_FILE):
        try:
            with open(TOKEN_PICKLE_FILE, "rb") as token:
                creds = pickle.load(token)
        except Exception as e:
            logger.error(f"Error al cargar {TOKEN_PICKLE_FILE}: {e}")

    # Si no hay credenciales válidas, pedir login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                logger.error(f"Error al refrescar el token: {e}")
                creds = None
        
        if not creds:
            if not os.path.exists(CLIENT_SECRET_FILE):
                logger.error(f"Archivo {CLIENT_SECRET_FILE} no encontrado. No se puede autenticar.")
                raise FileNotFoundError(f"Falta {CLIENT_SECRET_FILE}")
            
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)  
            
        # Guardar las credenciales para la próxima vez
        try:
            with open(TOKEN_PICKLE_FILE, "wb") as token:
                pickle.dump(creds, token)
        except Exception as e:
            logger.error(f"Error al guardar {TOKEN_PICKLE_FILE}: {e}")

    return build("youtubeAnalytics", "v2", credentials=creds)

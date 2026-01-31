from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
from src.core.config import logger
from src.core.database import SessionLocal
from src.services.auth_service import get_credentials_from_db

SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly", "https://www.googleapis.com/auth/youtube.readonly"]

def get_youtube_analytics_service(channel_id=None):
    """Crea un cliente de la API de YouTube Analytics usando credenciales de la BD."""
    creds = None
    
    # 1. Intentar obtener de la BD
    if channel_id:
        try:
            with SessionLocal() as db:
                creds_data = get_credentials_from_db(db, channel_id)
                if creds_data:
                    creds = Credentials(
                        token=creds_data["token"],
                        refresh_token=creds_data.get("refresh_token"),
                        token_uri=creds_data.get("token_uri"),
                        client_id=creds_data.get("client_id"),
                        client_secret=creds_data.get("client_secret"),
                        scopes=creds_data.get("scopes")
                    )
        except Exception as e:
            logger.error(f"Error recuperando credenciales de BD para {channel_id}: {e}")

    # 2. Si no hay credenciales (o no son válidas)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                # TODO: Actualizar el token refrescado en la BD
            except Exception as e:
                logger.error(f"Error al refrescar el token: {e}")
                creds = None
        
        # Si sigue sin haber credenciales...
        if not creds:
            logger.warning(f"No hay token válido para el canal {channel_id}. Se requiere autenticación manual via Web.")
            return None

    return build("youtubeAnalytics", "v2", credentials=creds)


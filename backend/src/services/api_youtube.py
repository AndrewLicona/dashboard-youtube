from googleapiclient.discovery import build
from src.core.config import API_KEY, logger
import googleapiclient.errors

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_youtube_service(api_key=None):
    """Crea un cliente de la API de YouTube (API pública con API Key)."""
    try:
        key = api_key or API_KEY
        return build(API_SERVICE_NAME, API_VERSION, developerKey=key)
    except Exception as e:
        logger.error(f"Error al crear el servicio de YouTube: {e}")
        raise

def get_channel_stats(channel_id, api_key=None):
    """Obtiene estadísticas generales del canal (subs, views, videos)."""
    try:
        youtube = get_youtube_service(api_key)
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id
        )
        return request.execute()
    except googleapiclient.errors.HttpError as e:
        logger.error(f"Error HTTP al obtener estadísticas del canal {channel_id}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado al obtener estadísticas del canal {channel_id}: {e}")
        return None

def get_videos_from_playlist(playlist_id, max_results=50, page_token=None, api_key=None):
    """Obtiene videos de una playlist (ejemplo: uploads del canal)."""
    try:
        youtube = get_youtube_service(api_key)
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=max_results,
            pageToken=page_token
        )
        return request.execute()
    except googleapiclient.errors.HttpError as e:
        logger.error(f"Error HTTP al obtener videos de la playlist {playlist_id}: {e}")
        return {"items": []}
    except Exception as e:
        logger.error(f"Error al obtener videos de la playlist {playlist_id}: {e}")
        return {"items": []}

def get_video_stats(video_ids, api_key=None):
    """Obtiene estadísticas de videos por ID (likes, views, comentarios, etc.)."""
    try:
        youtube = get_youtube_service(api_key)
        request = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(video_ids)
        )
        return request.execute()
    except googleapiclient.errors.HttpError as e:
        logger.error(f"Error HTTP al obtener estadísticas de videos: {e}")
        return {"items": []}
    except Exception as e:
        logger.error(f"Error al obtener estadísticas de videos: {e}")
        return {"items": []}


from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_youtube_service():
    """Crea un cliente de la API de YouTube (API pública con API Key)."""
    return build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

def get_channel_stats(channel_id):
    """Obtiene estadísticas generales del canal (subs, views, videos)."""
    youtube = get_youtube_service()
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    return request.execute()

def get_videos_from_playlist(playlist_id, max_results=50, page_token=None):
    """Obtiene videos de una playlist (ejemplo: uploads del canal)."""
    youtube = get_youtube_service()
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=max_results,
        pageToken=page_token
    )
    return request.execute()

def get_video_stats(video_ids):
    """Obtiene estadísticas de videos por ID (likes, views, comentarios, etc.)."""
    youtube = get_youtube_service()
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    )
    return request.execute()

import pandas as pd
from src.services.api_youtube import get_channel_stats, get_video_stats, get_videos_from_playlist
from src.core.config import CHANNEL_ID, logger, DATA_DIR
import os

def fetch_all_videos(channel_id):
    """Descarga todos los videos de un canal y devuelve DataFrame."""
    if not channel_id:
        logger.error("CHANNEL_ID no proporcionado")
        return pd.DataFrame()

    # 1️⃣ Obtener playlist de uploads
    try:
        channel_data = get_channel_stats(channel_id)
        if not channel_data or "items" not in channel_data:
            logger.error(f"No se pudo obtener información del canal {channel_id}")
            return pd.DataFrame()
        
        uploads_id = channel_data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    except Exception as e:
        logger.error(f"Error al obtener playlist de uploads: {e}")
        return pd.DataFrame()

    # 2️⃣ Iterar todas las páginas de la playlist
    videos = []
    next_page = None

    logger.info(f"Iniciando descarga de videos para el canal {channel_id}...")

    while True:
        try:
            playlist_data = get_videos_from_playlist(uploads_id, page_token=next_page)
            if not playlist_data or not playlist_data.get("items"):
                break
                
            video_ids = [item["contentDetails"]["videoId"] for item in playlist_data["items"]]

            # 3️⃣ Obtener estadísticas de esos videos
            stats = get_video_stats(video_ids)

            for item in stats.get("items", []):
                videos.append({
                    "Video ID": item["id"],
                    "Titulo": item["snippet"]["title"],     # Nombre normalizado sin tildes para el código
                    "Publicado": item["snippet"]["publishedAt"],
                    "Miniatura": item["snippet"]["thumbnails"]["medium"]["url"],
                    "Duracion": item["contentDetails"]["duration"],  
                    "Vistas": int(item["statistics"].get("viewCount", 0)),
                    "Likes": int(item["statistics"].get("likeCount", 0)),
                    "Comentarios": int(item["statistics"].get("commentCount", 0)),
                })

            next_page = playlist_data.get("nextPageToken")
            if not next_page:
                break
        except Exception as e:
            logger.error(f"Error durante la iteración de videos: {e}")
            break

    logger.info(f"Descarga completada. Total videos: {len(videos)}")
    df = pd.DataFrame(videos)
    
    # Asegurar que las columnas existen para evitar NameError en UI
    expected_cols = ["Video ID", "Titulo", "Publicado", "Miniatura", "Vistas", "Likes", "Comentarios"]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = None

    return df

if __name__ == "__main__":
    df = fetch_all_videos(CHANNEL_ID)
    if not df.empty:
        os.makedirs(DATA_DIR, exist_ok=True)
        output_path = os.path.join(DATA_DIR, "videos.csv")
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        logger.info(f"✅ Datos guardados en {output_path}")
    else:
        logger.warning("No se obtuvieron datos para guardar.")
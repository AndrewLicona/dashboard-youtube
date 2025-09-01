import pandas as pd
from api_youtube import get_channel_stats, get_video_stats, get_videos_from_playlist
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_all_videos(channel_id):
    """Descarga todos los videos de un canal y devuelve DataFrame."""
    # 1️⃣ Obtener playlist de uploads
    channel_data = get_video_stats(channel_id)
    channel_data = get_channel_stats(channel_id)
    uploads_id = channel_data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # 2️⃣ Iterar todas las páginas de la playlist
    videos = []
    next_page = None

    while True:
        playlist_data = get_videos_from_playlist(uploads_id, page_token=next_page)
        video_ids = [item["contentDetails"]["videoId"] for item in playlist_data["items"]]

        # 3️⃣ Obtener estadísticas de esos videos
        stats = get_video_stats(video_ids)

        for item in stats["items"]:
            videos.append({
                "Video ID": item["id"],
                "Título": item["snippet"]["title"],
                "Publicado": item["snippet"]["publishedAt"],
                "Miniatura": item["snippet"]["thumbnails"]["medium"]["url"],
                "Duración": item["contentDetails"]["duration"],  # ej: PT15M33S
                "Vistas": int(item["statistics"].get("viewCount", 0)),
                "Likes": int(item["statistics"].get("likeCount", 0)),
                "Comentarios": int(item["statistics"].get("commentCount", 0)),
            })

        next_page = playlist_data.get("nextPageToken")
        if not next_page:
            break

    return pd.DataFrame(videos)

if __name__ == "__main__":
    channel_id = os.getenv("CHANNEL_ID")
    df = fetch_all_videos(channel_id)
    df.to_csv("data/videos.csv", index=False, encoding="utf-8-sig")
    print("✅ Datos guardados en data/videos.csv")

    # Guardar en Excel
    df.to_excel("data/videos.xlsx", index=False)
    print("✅ Datos guardados en data/videos.xlsx")
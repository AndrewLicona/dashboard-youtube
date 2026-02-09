import os
# FIX: Robust SSL handling. If the forced path is invalid (doesn't exist), clear it.
if "SSL_CERT_FILE" in os.environ:
    if not os.path.exists(os.environ["SSL_CERT_FILE"]):
        del os.environ["SSL_CERT_FILE"]
if "REQUESTS_CA_BUNDLE" in os.environ:
    if not os.path.exists(os.environ["REQUESTS_CA_BUNDLE"]):
        del os.environ["REQUESTS_CA_BUNDLE"]

from fastapi import FastAPI, HTTPException, Header, Request as FastAPIRequest
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import time

from googleapiclient.discovery import build
from typing import Optional
from src.services.fetch_data import fetch_all_videos
from src.services.fetch_daily import fetch_daily_stats
from src.core.config import logger, API_KEY
from src.core.database import Base, engine
from src.db.models import Channel  # noqa: F401 Register models

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AJDREW Analytics API")

# Setup CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to AJDREW Analytics API", "status": "online"}

def get_cache_path(filename, channel_id=None):
    """Helper to get namespaced cache path."""
    if channel_id:
        return os.path.join("data", f"{channel_id}_{filename}")
    return os.path.join("data", filename)

@app.get("/api/videos")
def get_videos(
    x_youtube_channel_id: Optional[str] = Header(None),
    x_youtube_api_key: Optional[str] = Header(None)
):
    """Returns videos. Auto-fetches if cache missing and API key provided."""
    target_channel_id = x_youtube_channel_id
    if not target_channel_id:
        return []
        
    csv_path = get_cache_path("videos.csv", x_youtube_channel_id)

    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"API Success: Loaded {len(df)} videos from cache for {target_channel_id}")
            return df.to_dict(orient="records")
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
    
    # If cache missing and we have creds, try to fetch
    if x_youtube_api_key and x_youtube_channel_id:
        logger.info(f"Cache miss for {target_channel_id}. Fetching live data...")
        try:
            df = fetch_all_videos(target_channel_id, x_youtube_api_key)
            if not df.empty:
                os.makedirs("data", exist_ok=True)
                df.to_csv(csv_path, index=False, encoding="utf-8-sig")
                return df.to_dict(orient="records")
        except Exception as e:
            logger.error(f"Error fetching live data: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    logger.warning(f"Cache empty for {target_channel_id} and no credentials provided.")
    return []

@app.get("/api/analytics")
def get_analytics(
    x_youtube_channel_id: Optional[str] = Header(None)
):
    """Returns daily stats (Global/Demo data for now if custom channel doesn't have it)."""
    # NOTE: Daily stats scraping is complex (needs OAuth or specific scraping). 
    # For now, we only support custom VIDEO lists. Daily stats might return empty 
    # or we can fallback to default if desired. 
    # We will try to load custom if exists, otherwise return empty to avoid confusion.
    
    csv_path = get_cache_path("daily_stats.csv", x_youtube_channel_id)
    
    if os.path.exists(csv_path):
        # Check for cache expiry (24 hours)
        file_age = time.time() - os.path.getmtime(csv_path)
        if file_age > 14400: # 4 hours in seconds (lowered from 24h)
             logger.info(f"Cache expired for {x_youtube_channel_id} (Age: {file_age:.0f}s). Refreshing...")
             # Fall through to fetch new data

# ... (skipping unchanged lines) ...

@app.post("/api/refresh")
async def refresh_data(
    x_youtube_channel_id: Optional[str] = Header(None),
    x_youtube_api_key: Optional[str] = Header(None)
):
    """Force refresh data (Videos & Analytics)."""
    if not x_youtube_api_key:
         # Use default if configured? No, require keys for dynamic operations
         return {"message": "API Key required for refresh"}
    
    target_id = x_youtube_channel_id
    if not target_id:
        raise HTTPException(status_code=400, detail="Channel ID required")
    
    # Run sync fetch (blocking for simplicity in MVP)
    try:
        # 1. Refresh Videos
        df_videos = fetch_all_videos(target_id, x_youtube_api_key)
        video_path = get_cache_path("videos.csv", x_youtube_channel_id)
        os.makedirs("data", exist_ok=True)
        df_videos.to_csv(video_path, index=False, encoding="utf-8-sig")

        # 2. Refresh Analytics (Daily Stats)
        # Note: This requires OAuth token to be present in DB/File for target_id
        try:
            df_analytics = fetch_daily_stats(target_id)
            if not df_analytics.empty:
                analytics_path = get_cache_path("daily_stats.csv", x_youtube_channel_id)
                df_analytics.to_csv(analytics_path, index=False, encoding="utf-8-sig")
                if 'day' in df_analytics.columns:
                    df_analytics['day'] = df_analytics['day'].astype(str) # Normalize for return if needed
        except Exception as e:
            logger.error(f"Refresh: Failed to update analytics for {target_id}: {e}")
            # We continue even if analytics fail, at least videos are updated
        
        return {"message": f"Successfully refreshed data for {target_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/channel")
async def get_channel_info(
    x_youtube_channel_id: Optional[str] = Header(None),
    x_youtube_api_key: Optional[str] = Header(None)
):
    """Returns basic channel info and stats."""
    channel_id = x_youtube_channel_id
    stats = {}
    
    if not channel_id:
         return {
            "channelTitle": "AJDREW Gameplays",
            "channelId": "demo",
            "theme": "Gamer Green",
            "stats": {"subscribers": 0, "views": 0, "videos": 0}
        }
    
    # Try to fetch real stats if API Key is available or using default environment key
    try:
        from src.services.api_youtube import get_channel_stats
        # Use provided key or fallback to env key in get_channel_stats
        raw_stats = get_channel_stats(channel_id, x_youtube_api_key)
        
        if raw_stats and "items" in raw_stats and len(raw_stats["items"]) > 0:
            info = raw_stats["items"][0]
            snippet = info.get("snippet", {})
            st = info.get("statistics", {})
            
            return {
                "channelTitle": snippet.get("title", "Canal Personalizado"),
                "channelId": channel_id,
                "theme": "Gamer Green",
                "avatar": snippet.get("thumbnails", {}).get("default", {}).get("url", ""),
                "stats": {
                    "subscribers": int(st.get("subscriberCount", 0)),
                    "views": int(st.get("viewCount", 0)),
                    "videos": int(st.get("videoCount", 0))
                }
            }
    except Exception as e:
        logger.error(f"Error fetching channel stats: {e}")

    return {
        "channelTitle": "Canal Personalizado" if x_youtube_channel_id else "AJDREW Gameplays",
        "channelId": channel_id,
        "theme": "Gamer Green",
        "stats": {"subscribers": 0, "views": 0, "videos": 0}
    }

from src.api.endpoints.auth import router as auth_router

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

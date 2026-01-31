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
import pickle
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from typing import Optional
from src.services.fetch_data import fetch_all_videos
from src.services.fetch_daily import fetch_daily_stats
from src.core.config import logger, API_KEY

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
        try:
            df = pd.read_csv(csv_path)
            if 'day' in df.columns:
                df['day'] = df['day'].astype(str)
            return df.to_dict(orient="records")
        except Exception as e:
            logger.error(f"Error reading analytics cache: {e}")
    
    # Cache Miss: Try to fetch if we have a valid channel ID
    # Note: Requires stored OAuth token (token_{channel_id}.pickle)
    if x_youtube_channel_id:
        logger.info(f"Analytics Cache miss for {x_youtube_channel_id}. Attempting fetch...")
        try:
            df = fetch_daily_stats(x_youtube_channel_id)
            if not df.empty:
                os.makedirs("data", exist_ok=True)
                df.to_csv(csv_path, index=False, encoding="utf-8-sig")
                if 'day' in df.columns:
                    df['day'] = df['day'].astype(str)
                return df.to_dict(orient="records")
        except Exception as e:
             logger.error(f"Error fetching daily stats: {e}")
             # Don't crash, just return empty so UI shows warning
    
    # Fallback to default demo data ONLY if we are requesting the main channel 
    # AND we failed to fetch/load custom data.
    # Fallback to default demo data ONLY if we failed to fetch/load custom data and have no ID
    if not x_youtube_channel_id:
        # Try default
        default_path = os.path.join("data", "daily_stats.csv")
        if os.path.exists(default_path):
             df = pd.read_csv(default_path)
             if 'day' in df.columns: df['day'] = df['day'].astype(str)
             return df.to_dict(orient="records")

    return []

@app.post("/api/refresh")
async def refresh_data(
    x_youtube_channel_id: Optional[str] = Header(None),
    x_youtube_api_key: Optional[str] = Header(None)
):
    """Force refresh data."""
    if not x_youtube_api_key:
         # Use default if configured? No, require keys for dynamic operations
         return {"message": "API Key required for refresh"}
    
    target_id = x_youtube_channel_id
    if not target_id:
        raise HTTPException(status_code=400, detail="Channel ID required")
    
    # Run sync fetch (blocking for simplicity in MVP)
    try:
        df = fetch_all_videos(target_id, x_youtube_api_key)
        
        path = get_cache_path("videos.csv", x_youtube_channel_id)
        os.makedirs("data", exist_ok=True)
        df.to_csv(path, index=False, encoding="utf-8-sig")
        
        return {"message": f"Successfully refreshed {len(df)} videos for {target_id}"}
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

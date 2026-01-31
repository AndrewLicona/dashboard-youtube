

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...services.auth_service import save_channel_credentials
import os
from googleapiclient.discovery import build
from ...core.config import logger

router = APIRouter()

# Allow HTTP for local testing of OAuth (remove in production if using HTTPS)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/yt-analytics.readonly", "https://www.googleapis.com/auth/youtube.upload"]

def get_flow(redirect_uri):
    # Construct config dictionary from Env Vars
    client_config = {
        "web": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    
    if not client_config["web"]["client_id"] or not client_config["web"]["client_secret"]:
        raise HTTPException(status_code=500, detail="Google OAuth Credentials not set in backend")

    flow = Flow.from_client_config(
        client_config=client_config,
        scopes=SCOPES
    )
    flow.redirect_uri = redirect_uri
    return flow

@router.get("/login")
async def login(request: Request):
    # Dynamic Redirect URI construction
    # We assume the API is at /api, so we build the callback URL based on the request host
    # Or use a configured BASE_URL
    
    # Logic:
    # 1. Try env var API_BASE_URL (for production override)
    # 2. Fallback to request.base_url
    
    base_url = os.getenv("API_BASE_URL")
    if not base_url:
        # Construct from request (e.g. http://localhost:8000 or http://domain.com:8000)
        # Be careful with proxies!
        base_url = str(request.base_url).rstrip('/')
    
    redirect_uri = f"{base_url}/api/auth/callback"
    
    logger.info(f"Initiating Login with Callback: {redirect_uri}")

    flow = get_flow(redirect_uri)
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    return RedirectResponse(authorization_url)

@router.get("/callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not found")

    # Reconstruct the redirect_uri used in login
    base_url = os.getenv("API_BASE_URL")
    if not base_url:
        base_url = str(request.base_url).rstrip('/')
    
    redirect_uri = f"{base_url}/api/auth/callback"

    flow = get_flow(redirect_uri)
    
    try:
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # We need the channel ID to associate this token.
        youtube = build('youtube', 'v3', credentials=credentials)
        response = youtube.channels().list(mine=True, part='snippet,id').execute()
        
        if not response.get("items"):
             raise HTTPException(status_code=400, detail="No YouTube channel found for this user")
             
        channel_info = response["items"][0]
        channel_id = channel_info["id"]
        
        # Save to DB
        save_channel_credentials(db, channel_info, credentials)
        
        # Redirect to Frontend
        # If Frontend is on a different port/domain, we need FRONTEND_URL env var
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173") 
        # Note: In production docker, this default might be wrong if not set.
        
        return RedirectResponse(f"{frontend_url}/?auth_success=true&channel_id={channel_id}")
        
    except Exception as e:
        logger.error(f"Auth Error: {e}")
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

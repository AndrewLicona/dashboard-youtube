from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...services.auth_service import save_channel_credentials
import os
import pathlib
from googleapiclient.discovery import build

router = APIRouter()

# Allow HTTP for local testing of OAuth (remove in production if using HTTPS)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_SECRETS_FILE = os.path.join(pathlib.Path(__file__).parent.parent.parent.parent, "client_secret.json")
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/yt-analytics.readonly"]
REDIRECT_URI = "http://localhost:8000/api/auth/callback" # Must match Google Console

@router.get("/login")
async def login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent' # Force consent to get refresh token
    )
    return RedirectResponse(authorization_url)

@router.get("/callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not found")

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    
    try:
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # We need the channel ID to associate this token.
        # Use the credentials to query the YouTube API for the channel ID.
        youtube = build('youtube', 'v3', credentials=credentials)
        response = youtube.channels().list(mine=True, part='snippet,id').execute()
        
        if not response.get("items"):
             raise HTTPException(status_code=400, detail="No YouTube channel found for this user")
             
        channel_info = response["items"][0]
        
        # Save to DB
        save_channel_credentials(db, channel_info, credentials)
        
        # Redirect to Frontend with success flag
        return RedirectResponse("http://localhost:5173/?auth_success=true")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

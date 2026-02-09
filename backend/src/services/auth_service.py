from sqlalchemy.orm import Session
from ..db.models import Channel
from ..core.security import encrypt_token, decrypt_token
from google.oauth2.credentials import Credentials
import json
from datetime import datetime
import os

def get_channel_by_id(db: Session, channel_id: str):
    return db.query(Channel).filter(Channel.channel_id == channel_id).first()

def save_channel_credentials(db: Session, channel_info: dict, credentials):
    """
    Saves or updates channel credentials in the database (encrypted).
    """
    channel_id = channel_info.get("id")
    if not channel_id:
        raise ValueError("Channel ID is missing")

    db_channel = get_channel_by_id(db, channel_id)
    
    # Encrypt tokens
    access_token_enc = encrypt_token(credentials.token)
    refresh_token_enc = encrypt_token(credentials.refresh_token) if credentials.refresh_token else None

    if db_channel:
        # Update existing
        db_channel.title = channel_info.get("snippet", {}).get("title", 'Unknown')
        db_channel.thumbnail_url = channel_info.get("snippet", {}).get("thumbnails", {}).get("default", {}).get("url")
        db_channel.access_token_enc = access_token_enc
        if refresh_token_enc:
            db_channel.refresh_token_enc = refresh_token_enc
        db_channel.token_expiry = credentials.expiry
        db_channel.last_updated = datetime.utcnow()
    else:
        # Create new
        db_channel = Channel(
            channel_id=channel_id,
            title=channel_info.get("snippet", {}).get("title", 'Unknown'),
            thumbnail_url=channel_info.get("snippet", {}).get("thumbnails", {}).get("default", {}).get("url"),
            access_token_enc=access_token_enc,
            refresh_token_enc=refresh_token_enc,
            created_at=datetime.utcnow()
        )
        db.add(db_channel)
    
    if refresh_token_enc:
        print(f"DEBUG: Saving NEW refresh token for {channel_id}")
    else:
        print(f"DEBUG: No refresh token to save for {channel_id} (Is this a re-auth without prompt?)")

    db.commit()
    db.refresh(db_channel)
    return db_channel

def get_credentials_from_db(db: Session, channel_id: str):
    """
    Retrieves decrypted credentials from the database.
    """
    channel = get_channel_by_id(db, channel_id)
    if not channel or not channel.access_token_enc:
        return None
    
    access_token = decrypt_token(channel.access_token_enc)
    refresh_token = decrypt_token(channel.refresh_token_enc) if channel.refresh_token_enc else None
    
    # Reconstruct Credentials object
    # Note: We need client_id/secret from config ideally, but for just Access Token validation it might be enough.
    # For refreshing, we definitively need client_id/secret.
    
    # Placeholder: Return a dict or object that youtube service can use.
    # The actual Credentials object usually needs token_uri, client_id, client_secret.
    # We will assume those are available in environment or config.
    
    return {
        "token": access_token,
        "refresh_token": refresh_token,
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "scopes": ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/yt-analytics.readonly"]
    }

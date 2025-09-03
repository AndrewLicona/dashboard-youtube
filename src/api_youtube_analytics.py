from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle, os

SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly"]

def get_youtube_analytics_service():
    creds = None
    # Revisar si ya existe token
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=8080)  
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtubeAnalytics", "v2", credentials=creds)

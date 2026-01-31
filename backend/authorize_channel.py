import sys
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

# Add parent dir to path to import config if needed, or just hardcode for standalone script consistency
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration
SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly", "https://www.googleapis.com/auth/youtube.readonly"]
CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_DIR = os.path.join("data", "tokens")

def authorize_channel():
    print("--- Generador de Tokens para Dashboard YouTube ---")
    channel_id = input("Introduce el CHANNEL ID del canal a autorizar: ").strip()
    
    if not channel_id:
        print("Error: Debes introducir un ID válido.")
        return

    if not os.path.exists(CLIENT_SECRET_FILE):
        print(f"Error: No se encuentra el archivo {CLIENT_SECRET_FILE}")
        return

    # Ensure token dir exists
    if not os.path.exists(TOKEN_DIR):
        os.makedirs(TOKEN_DIR)
        
    token_path = os.path.join(TOKEN_DIR, f"token_{channel_id}.pickle")
    
    print(f"\nSe abrirá una ventana de navegador para autorizar el canal {channel_id}...")
    print("IMPORTANTE: Loguéate con la cuenta de Google propietaria de ESE canal.")
    
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=8080)
    
    with open(token_path, "wb") as token:
        pickle.dump(creds, token)
        
    print(f"\n✅ ¡Éxito! Token guardado en: {token_path}")
    print("Ahora puedes recargar el dashboard y verás las estadísticas.")

if __name__ == "__main__":
    authorize_channel()

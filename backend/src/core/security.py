from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure we have a key. In production this MUST be persistent.
# You can generate one with: Fernet.generate_key().decode()
_key = os.getenv("ENCRYPTION_KEY")
if not _key:
    # Use a default fallback ONLY for local dev/demo to prevent startup crash.
    # User will be warned to set this in .env
    print("WARNING: ENCRYPTION_KEY not found in .env. Using a temporary insecure key.")
    _key = Fernet.generate_key().decode()

cipher_suite = Fernet(_key)

def encrypt_token(token: str) -> str:
    if not token:
        return None
    return cipher_suite.encrypt(token.encode()).decode()

def decrypt_token(token_encrypted: str) -> str:
    if not token_encrypted:
        return None
    try:
        return cipher_suite.decrypt(token_encrypted.encode()).decode()
    except Exception as e:
        print(f"Error decrypting token: {e}")
        return None

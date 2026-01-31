import os
import sys
import certifi

print("--- DEBUG INFO ---")
print(f"Python Executable: {sys.executable}")
print(f"Certifi Location: {certifi.where()}")
print(f"Environment SSL_CERT_FILE: {os.environ.get('SSL_CERT_FILE')}")
print(f"Environment REQUESTS_CA_BUNDLE: {os.environ.get('REQUESTS_CA_BUNDLE')}")
print(f"CWD: {os.getcwd()}")

try:
    with open(certifi.where(), 'r') as f:
        print("Certifi file is readable.")
except Exception as e:
    print(f"ERROR: Cannot read certifi file: {e}")

print("------------------")

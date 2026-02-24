import os
import json
from config import TOKENS_FILE

def _asegurar_archivo_token():
    """Crea el archivo si no existe"""
    directorio = os.path.dirname(TOKENS_FILE)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)

    if not os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, "w") as f:
            json.dump({}, f)
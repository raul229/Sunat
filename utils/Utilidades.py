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

def _guardar_en_tokenfile(valor, nombre_atributo):
    data = {}
    with open(TOKENS_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data= {}
    data[nombre_atributo] = valor   

    with open(TOKENS_FILE, "w") as f:
        json.dump(data, f)
    print(f"Token guardado en {TOKENS_FILE}")

def json_valido(response, tipo_repuesa='text/html; charset=UTF-8'):
    content_type = response.headers.get('Content-Type', '')
    if content_type.startswith(tipo_repuesa):
        try:
            return response.json()
        except ValueError:
            return None
    return None

def cargar_json(clave):
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return None
            valor = data.get(clave)
            if valor in (None, ''):
                return None
            return valor
    return None

def obtener_valor(diccionario, *keys):
    if not isinstance(diccionario, dict):
        return None
    for key in keys:
        if not isinstance(diccionario, dict):
            return None
        diccionario = diccionario.get(key, {})
    return diccionario

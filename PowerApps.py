from utils.Utilidades import pagina_login_powerapps
from dotenv import load_dotenv
import os
import json
import requests
import base64
import time

load_dotenv()

TOKENS_FILE = os.getenv('TOKENS_FILE')

# Datos de la consulta de prueba
RUC_PRUEBA = os.getenv('RUC_PRUEBA')
ENVIRONMENT_ID = os.getenv('ENVIRONMENT_ID')
API_URL = f"https://{ENVIRONMENT_ID}.02.common.brazil.azure-apihub.net/invoke"

# Headers fijos (tomados de la petición de ejemplo)
FIXED_HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-ES",
    "cache-control": "no-cache, no-store",
    "content-type": "application/json",
    "origin": "https://apps.powerapps.com",
    "priority": "u=1, i",
    "referer": "https://apps.powerapps.com/",
    "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "x-ms-client-app-id": "/providers/Microsoft.PowerApps/apps/ecd6b1e1-f30e-49ed-b688-ae719ade20ee",
    "x-ms-client-environment-id": f"/providers/Microsoft.PowerApps/environments/{ENVIRONMENT_ID}",
    "x-ms-licensecategorization": "PREMIUM40K",
    "x-ms-licensecontext": "POWERAPPS",
    "x-ms-request-method": "POST",
    "x-ms-request-url": "/apim/logicflows/02f67736a11148cdb8abe97f15523df0/triggers/manual/run?api-version=2015-02-01-preview",
    "x-ms-user-agent": "PowerApps/3.26021.10 (Web Player; AppName=ecd6b1e1-f30e-49ed-b688-ae719ade20ee)"
}

def interceptar_token(pagina, timeout=120):
    """Espera a que se realice una petición a la API y captura el token."""
    token = None
    def handle_request(request):
        nonlocal token
        if request.url.startswith(API_URL):
            auth_header = request.headers.get('authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header[7:]
                print("✅ Token capturado desde la petición.")
    pagina.on('request', handle_request)
    print("🌐 Esperando a que realices una consulta en el navegador...")
    print("Por favor, haz clic en 'Buscar' o realiza la consulta manualmente.")
    start = time.time()
    while token is None and time.time() - start < timeout:
        pagina.wait_for_timeout(1000)
    if token is None:
        print("❌ No se capturó ningún token en el tiempo esperado.")
    return token

def guardar_token(token):
    with open(TOKENS_FILE, 'w') as f:
        json.dump({"jwt": token}, f)
    print(f"💾 Token guardado en {TOKENS_FILE}")

def cargar_token():
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, 'r') as f:
            data = json.load(f)
            return data.get('jwt')
    return None

def obtener_oid_desde_jwt(jwt):
    try:
        payload_b64 = jwt.split('.')[1]
        payload_b64 += '=' * (-len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode('utf-8'))
        return payload.get('oid')
    except Exception as e:
        print(f"Error decodificando JWT: {e}")
        return None

def consultar_con_requests(jwt_token, ruc):
    headers = FIXED_HEADERS.copy()
    headers["authorization"] = f"Bearer {jwt_token}"
    oid = obtener_oid_desde_jwt(jwt_token)
    if oid:
        headers["x-ms-client-object-id"] = oid
    else:
        print("⚠️ No se pudo extraer oid, se omite header")
    headers["x-ms-client-tenant-id"] = "5936fc44-399a-4904-b3e2-dfbc9d8577d8"
    payload = {"text": ruc}
    print(f"🔍 Consultando RUC {ruc}...")
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 400:
        pass
    
    print(f"Status: {response.status_code}")
    try:
        print("Respuesta:", response.json())
    except:
        print("Respuesta (texto):", response.text)
    return response

def iniciar_sesion_manual():
    print("🔐 Por favor, inicia sesión manualmente en el navegador.")
    print("Una vez que hayas ingresado y estés en la página de consultas, presiona Enter aquí.")
    input("⏎ Presiona Enter cuando estés listo...")

def main():
    # Intentar cargar token guardado
    token = cargar_token()
    if token:
        print("✅ Token cargado desde archivo.")
        ruc = input(f"Ingresa RUC (Enter para {RUC_PRUEBA}): ").strip()
        if not ruc:
            ruc = RUC_PRUEBA
        consultar_con_requests(token, ruc)
        return

    # No hay token, abrir navegador
    p, contexto, pagina = pagina_login_powerapps()
    if pagina:

        # Esperar login manual
        iniciar_sesion_manual()
        token = interceptar_token(pagina, timeout=60)

        if token:
            guardar_token(token)
            # Preguntar si quiere hacer consulta ahora
            usar_ahora = input("¿Quieres hacer una consulta ahora? (s/n): ").lower()
            if usar_ahora == 's':
                ruc = input(f"Ingresa RUC (Enter para {RUC_PRUEBA}): ").strip()
                if not ruc:
                    ruc = RUC_PRUEBA
                consultar_con_requests(token, ruc)


        else:
            print("❌ No se pudo obtener el token. Intenta de nuevo.")

        input("Presiona Enter para cerrar el navegador...")
        contexto.close()
        p.stop()

if __name__ == '__main__':
    main()
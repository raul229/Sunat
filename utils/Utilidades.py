from playwright.sync_api import sync_playwright
import os
import json
import time
from config import PERFIL_PLAYWRIGHT, API_URL, TOKENS_FILE, LINK_POWERAPPS


def _asegurar_archivo_token():
    """Crea el archivo si no existe"""
    directorio = os.path.dirname(TOKENS_FILE)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)

    if not os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, "w") as f:
            json.dump({}, f)


def _interceptar_token(pagina, timeout=120):
    """Espera una petición a la API y captura el token"""
    token = None
    def handle_request(request):
        nonlocal token
        if request.url.startswith(API_URL):
            auth_header = request.headers.get("authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header[7:]
                print("Token capturado correctamente.")

    pagina.on("request", handle_request)

    start = time.time()
    while token is None and time.time() - start < timeout:
        pagina.wait_for_timeout(1000)

    return token

def obtener_token_powerapps():

    _asegurar_archivo_token()

    link = LINK_POWERAPPS
    if not link:
        raise ValueError("LINK_POWERAPPS no está definido en el .env")

    with sync_playwright() as p:
        contexto = p.chromium.launch_persistent_context(
            user_data_dir=PERFIL_PLAYWRIGHT,
            headless=False,
            channel="chromium",
        )

        pagina = contexto.pages[0] if contexto.pages else contexto.new_page()

        pagina.goto(link)

        print("Inicia sesión manualmente si es necesario...")

        token = _interceptar_token(pagina)

        if not token:
            raise RuntimeError("No se pudo capturar el token.")

        with open(TOKENS_FILE, "w") as f:
            json.dump({"jwt": token}, f)

        print(f"Token guardado en {TOKENS_FILE}")

        contexto.close()

        return token
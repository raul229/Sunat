from playwright.sync_api import sync_playwright
import time
from config import PERFIL_PLAYWRIGHT, API_URL_POWERAPPS, LINK_POWERAPPS
from utils.Utilidades import _asegurar_archivo_token, _guardar_en_tokenfile


def _interceptar_token(pagina, timeout=120):
    """Espera una petición a la API y captura el token"""
    token = None
    def handle_request(request):
        nonlocal token
        if request.url.startswith(API_URL_POWERAPPS):
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

        print("Inicia sesión manualmente es necesario...")

        token = _interceptar_token(pagina)

        if not token:
            raise RuntimeError("No se pudo capturar el token.")

        _guardar_en_tokenfile(token, "jwt")

        contexto.close()

        return token
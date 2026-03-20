from playwright.sync_api import sync_playwright
from urllib.parse import unquote
import time
from config import PERFIL_PLAYWRIGHT, LINK_ENTEL_LOGIN
from utils.Utilidades import _asegurar_archivo_token, _guardar_en_tokenfile

COOKIES_NECESARIAS = ['nr1Users', 'nr2Users', 'osVisit', 'osVisitor']


def _extraer_csrf(nr2_cookie_value):
    """Extrae el token CSRF del campo 'crf' de la cookie nr2Users.
    
    nr2Users tiene formato: crf=<token>;uid=<id>;unm=<email>
    (URL-encoded en la cookie real)
    """
    decoded = unquote(nr2_cookie_value)
    for parte in decoded.split(';'):
        parte = parte.strip()
        if parte.startswith('crf='):
            return parte[4:]
    return None


def _interceptar_cookies(pagina, timeout=120) -> dict:
    """Espera a que el usuario haga login y captura las cookies de sesión."""
    start = time.time()

    while time.time() - start < timeout:
        cookies_raw = pagina.context.cookies()
        cookies_dict = {c['name']: c['value'] for c in cookies_raw}

        # Verificar que tenemos todas las cookies necesarias
        cookies_filtradas = {
            k: v for k, v in cookies_dict.items()
            if k in COOKIES_NECESARIAS
        }

        if len(cookies_filtradas) == len(COOKIES_NECESARIAS):
            return cookies_filtradas

        pagina.wait_for_timeout(1000)

    return None


def obtener_token_entel() -> dict:
    """Abre el navegador, espera login manual y captura cookies + CSRF token."""

    _asegurar_archivo_token()

    link = LINK_ENTEL_LOGIN
    if not link:
        raise ValueError("LINK_ENTEL_LOGIN no está definido en el .env")

    with sync_playwright() as p:
        contexto = p.chromium.launch_persistent_context(
            user_data_dir=PERFIL_PLAYWRIGHT,
            headless=False,
            channel="chromium",
            args=["--disable-blink-features=AutomationControlled"]
        )

        pagina = contexto.pages[0] if contexto.pages else contexto.new_page()

        pagina.goto(link)

        print("Inicia sesión manualmente en Entel.")
        input("Presiona Enter cuando hayas iniciado sesión y cargado la página...")

        cookies = _interceptar_cookies(pagina)

        if not cookies:
            raise RuntimeError("No se pudieron capturar las cookies de Entel.")

        # Extraer CSRF token de nr2Users
        csrf_token = _extraer_csrf(cookies['nr2Users'])
        if not csrf_token:
            raise RuntimeError("No se pudo extraer el x-csrftoken de nr2Users.")

        datos_entel = {
            "cookies": cookies,
            "csrf_token": csrf_token
        }

        _guardar_en_tokenfile(datos_entel, "entel")

        contexto.close()

        return datos_entel

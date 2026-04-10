from playwright.sync_api import sync_playwright
import time
from config import PERFIL_PLAYWRIGHT, LINK_ONFORCE
from utils.Utilidades import _asegurar_archivo_token, _guardar_en_tokenfile

def _interceptar_cookies(pagina, timeout=120)->dict:
    """Espera hacer login y captura las cookies"""
    
    cookies = {c['name']: c['value'] for c in pagina.context.cookies() }    
    # Filtrar solo las que necesitamos
    cookies_filtradas = {k: v for k, v in cookies.items() if k in ['cookiesession1', 'PHPSESSID']}
   
    start = time.time()
    while not cookies_filtradas and time.time() - start < timeout:
        pagina.wait_for_timeout(1000)
        cookies = {c['name']: c['value'] for c in pagina.context.cookies() }
        cookies_filtradas = {k: v for k, v in cookies.items() if k in ['cookiesession1', 'PHPSESSID']}
    return cookies_filtradas

def obtener_token_onforce()->dict:

    _asegurar_archivo_token()

    link = LINK_ONFORCE
    if not link:
        raise ValueError("LINK_ONFORCE no está definido en el .env")

   
    with sync_playwright() as p:
        contexto = p.chromium.launch_persistent_context(
            user_data_dir=PERFIL_PLAYWRIGHT,
            headless=False,
            channel="chromium",
            args=[ "--disable-blink-features=AutomationControlled"]
        )

        pagina = contexto.pages[0] if contexto.pages else contexto.new_page()

        pagina.goto(link)

        print("Inicia sesión manualmente es OBLIGATORIO")
        input("Presiona Enter cuando hayas iniciado sesión...")

        cookies = _interceptar_cookies(pagina)

        if not cookies:
            raise RuntimeError("No se pudo capturar el cookies.")


        _guardar_en_tokenfile(cookies, "cookies")

        contexto.close()

        return cookies

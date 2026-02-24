from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import time

load_dotenv()

PERFIL_PLAYWRIGHT = os.path.join(os.path.expanduser('~'), '.playwright-powerapps-profile')
ENVIRONMENT_ID = os.getenv('ENVIRONMENT_ID')
API_URL = f"https://{ENVIRONMENT_ID}.02.common.brazil.azure-apihub.net/invoke"

def pagina_login_powerapps():
    p = sync_playwright().start()
    contexto = p.chromium.launch_persistent_context(
        user_data_dir=PERFIL_PLAYWRIGHT,
    
        headless=False,
        channel='chromium',
    )
    pagina = contexto.pages[0] if contexto.pages else contexto.new_page()

    # Ir a la app
    link = os.getenv('LINK_POWERAPPS')
    if not link:
        print("⚠️ Variable LINK_POWERAPPS no definida en .env")
        link = input("Introduce la URL de la app: ")
    pagina.goto(link)
    
    return p, contexto, pagina

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
    

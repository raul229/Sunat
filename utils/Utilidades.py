from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

PERFIL_PLAYWRIGHT = os.path.join(os.path.expanduser('~'), '.playwright-powerapps-profile')

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
    

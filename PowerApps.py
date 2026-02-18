from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

def consultar_pa(ruc):
    with sync_playwright() as p:
        contexto = p.chromium.launch_persistent_context(
            headless=False,
            user_data_dir=os.getenv('PATH_PERFIL_CHROME'),
            # channel='chrome'
            )

        pagina = contexto.new_page()

        pagina.goto(os.getenv('LINK_POWERAPPS'))




        input('Presiona Enter para cerrar...')

        contexto.close()

if __name__ == '__main__':
    consultar_pa('20522317285')

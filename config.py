import os
from dotenv import load_dotenv

load_dotenv()

RUC_PRUEBA = os.getenv('RUC_PRUEBA')
PERFIL_PLAYWRIGHT = os.path.join(os.path.expanduser('~'), '.playwright-powerapps-profile')
TOKENS_FILE = os.getenv('TOKENS_FILE')

##POWERAPPS

ENVIRONMENT_ID = os.getenv('ENVIRONMENT_ID')
API_URL_POWERAPPS = f"https://{ENVIRONMENT_ID}.02.common.brazil.azure-apihub.net/invoke"
FIXED_HEADERS_POWERAPPS = {
            "x-ms-request-method": "POST",
            "x-ms-request-url": "/apim/logicflows/02f67736a11148cdb8abe97f15523df0/triggers/manual/run?api-version=2015-02-01-preview",
        }
LINK_POWERAPPS = os.getenv('LINK_POWERAPPS')

##ONFORCE

API_URL_ONFORCE = 'https://ventasnegocios.on.pe/controllers/cliente.php'
FIXED_HEADERS_ONFORCE = {}
LINK_ONFORCE = os.getenv('LINK_ONFORCE')

##ENTEL - CONSULTAS SUELTAS

API_URL_ENTEL = os.getenv('LINK_CONSULTA_SUELTA')
LINK_ENTEL_LOGIN = os.getenv('LINK_ENTEL_LOGIN')
import os
from dotenv import load_dotenv

load_dotenv()

PERFIL_PLAYWRIGHT = os.path.join(os.path.expanduser('~'), '.playwright-powerapps-profile')
ENVIRONMENT_ID = os.getenv('ENVIRONMENT_ID')
API_URL = f"https://{ENVIRONMENT_ID}.02.common.brazil.azure-apihub.net/invoke"
RUC_PRUEBA = os.getenv('RUC_PRUEBA')
TOKENS_FILE = os.getenv('TOKENS_FILE')
FIXED_HEADERS = {
            "x-ms-request-method": "POST",
            "x-ms-request-url": "/apim/logicflows/02f67736a11148cdb8abe97f15523df0/triggers/manual/run?api-version=2015-02-01-preview",
        }
LINK_POWERAPPS = os.getenv('LINK_POWERAPPS')
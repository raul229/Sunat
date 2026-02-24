from dotenv import load_dotenv
import os, json, base64

class ConsultorPA:
    
    def __init__(self):
        load_dotenv()
        self.token = None
        self.ENVIRONMENT_ID = os.getenv('ENVIRONMENT_ID')
        self.FIXED_HEADERS = {
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
        "x-ms-client-environment-id": f"/providers/Microsoft.PowerApps/environments/{self.ENVIRONMENT_ID}",
        "x-ms-licensecategorization": "PREMIUM40K",
        "x-ms-licensecontext": "POWERAPPS",
        "x-ms-request-method": "POST",
        "x-ms-request-url": "/apim/logicflows/02f67736a11148cdb8abe97f15523df0/triggers/manual/run?api-version=2015-02-01-preview",
        "x-ms-user-agent": "PowerApps/3.26021.10 (Web Player; AppName=ecd6b1e1-f30e-49ed-b688-ae719ade20ee)"
    }
        self.RUC_PRUEBA=os.getenv('RUC_PRUEBA')
        
    def cargar_token(self):
        archivo_tokens= os.getenv('TOKENS_FILE')
        if os.path.exists(archivo_tokens):
            with open(archivo_tokens, 'r') as f:
                data = json.load(f)
                self.token = data.get('jwt')
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
        
        
    
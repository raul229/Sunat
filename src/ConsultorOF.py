import os, json
import requests
from config import API_URL_ONFORCE, FIXED_HEADERS_POWERAPPS, RUC_PRUEBA, TOKENS_FILE

class ConsultorOF:
    
    def __init__(self):
        self._token = None
        #self.FIXED_HEADERS = FIXED_HEADERS_POWERAPPS
        self.RUC_PRUEBA=RUC_PRUEBA
        self.sesion = None
        self.cargar_token()

    def _crear_sesion(self):
        sesion = requests.Session()
        #sesion.headers.update(self.FIXED_HEADERS)
        sesion.cookies.update(self._token)
        return sesion

    def verificar_token(self):
        response = self.consultar(self.RUC_PRUEBA)
        data = response.json()
        if data['response'] == 'error':
            return False
        return True

    def cargar_token(self):
        archivo_tokens= TOKENS_FILE
        if os.path.exists(archivo_tokens):
            with open(archivo_tokens, 'r') as f:
                data = json.load(f)
                self._token = data.get('cookies')
                print('Token cargado!')
            self.sesion=self._crear_sesion()
        return None
    
    def consultar(self, ruc):
        payload = {
            "accion": "filtrarClientes",
            "data[num_ruc]": ruc,
            "data[razon_social]": "",
            "data[subordinados]": "3267",
            "data[subordinados_email]": "wbuzon9@gmail.com"
        }
        response =  self.sesion.post(API_URL_ONFORCE, json=payload)
        return response
import os, json
import requests
from config import API_URL, FIXED_HEADERS, RUC_PRUEBA, TOKENS_FILE

class ConsultorPA:
    
    def __init__(self):
        self._token = None
        self.FIXED_HEADERS = FIXED_HEADERS
        self.RUC_PRUEBA=RUC_PRUEBA
        self.sesion = None
        self.cargar_token()

    def _crear_sesion(self):
        sesion = requests.Session()
        sesion.headers.update(self.FIXED_HEADERS)
        sesion.headers.update({"authorization": f"Bearer {self._token}"})
        return sesion

    def verificar_token(self):
        response = self.consultar(self.RUC_PRUEBA)
        if response.status_code == 200:
            return True
        else:
            return False

    def cargar_token(self):
        archivo_tokens= TOKENS_FILE
        if os.path.exists(archivo_tokens):
            with open(archivo_tokens, 'r') as f:
                data = json.load(f)
                self._token = data.get('jwt')
                print('Token cargado!')
            self.sesion=self._crear_sesion()
        return None
    
    def consultar(self, ruc):
        payload = {"text": ruc}
        response =  self.sesion.post(API_URL, json=payload)
        return response
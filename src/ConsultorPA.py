import requests
from utils.Utilidades import cargar_json
from config import API_URL_POWERAPPS, FIXED_HEADERS_POWERAPPS
from src.ConsultorBASE import ConsultorBASE

class ConsultorPA(ConsultorBASE):
    
    def __init__(self):
        self._token = None
        self.FIXED_HEADERS = FIXED_HEADERS_POWERAPPS
        self.sesion = None
        self.cargar_token()

    def _crear_sesion(self):
        sesion = requests.Session()
        sesion.headers.update(self.FIXED_HEADERS)
        sesion.headers.update({"authorization": f"Bearer {self._token}"})
        return sesion

    def verificar_token(self)->bool:
        if self.sesion is None:
            return False

        try:
            response = self.sesion.post(API_URL_POWERAPPS, json={"text": self.RUC_PRUEBA})
            return response.status_code == 200
        except requests.RequestException:
            return False

    def cargar_token(self):
        token = cargar_json('jwt')
        if token is not None:
            self._token = token
            self.sesion=self._crear_sesion()
            print('Token cargado!')
        else:
            print('Token no encontrado')
    
    def consultar(self, ruc):
        payload = {"text": ruc}
        if self.sesion is None:
            self.cargar_token()
        if self.sesion is None:
            return None
        response =  self.sesion.post(API_URL_POWERAPPS, json=payload)
        return response

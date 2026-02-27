import json
import requests
from utils.Utilidades import cargar_json
from config import API_URL_ONFORCE,RUC_PRUEBA

class ConsultorOF:
    
    def __init__(self):
        self._token = None
        #self.FIXED_HEADERS = FIXED_HEADERS_ONFORCE
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
        if 'Bienvenido a ON NEGOCIOS' in response.text:
            return False
        return True

    def cargar_token(self):
        cookies = cargar_json('cookies')
        if cookies is not None:
            self._token= cookies
            self.sesion=self._crear_sesion()
            print('Token cargado!')
        else:
            print('Token no encontrado')
    
    
    def consultar(self, payload):
        
        response =  self.sesion.post(API_URL_ONFORCE, data=payload)
        return response

    def score_crediticio(self, ruc):
        payload = {
            "accion": "score_cliente_light",
            "data[documento_identidad]": ruc,
            "data[tipo_doc]": "03"
        }

        response = self.consultar(payload)
        body = response.json()

        if body.get("response") != "success":
            print('Error al consultar el score crediticio')
            return None

        data_raw = body.get("data")

        if not data_raw:
            return None

        while isinstance(data_raw, str):
            data_raw = json.loads(data_raw)

        data_dict = data_raw

        try:
            score = (
                data_dict["soapBody"]
                ["ns3GetReporteOnlineResponse"]
                ["ns2ReporteCrediticio"]
                ["Modulos"]["Modulo"][1]
                ["Data"]["ns3ResumenScore"]["Puntaje"]
            )
            return score

        except (KeyError, IndexError, TypeError):
            return None

      
    def cliente_carterizado_por_ruc(self, ruc):
        payload = {
            "accion": 'filtrarClientes',
            "data[num_ruc]": ruc,
        }
        response = self.consultar(payload)
        data=response.json()
        if data[0]['data']['data']:
            return True
        return False
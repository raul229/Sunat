from src.ConsultorBASE import ConsultorBASE
import json
import requests
from utils.Utilidades import cargar_json, json_valido
from auth.AuthOnForce import obtener_token_onforce
from config import API_URL_ONFORCE

class ConsultorOF(ConsultorBASE):
    
    def __init__(self):
        self._token = None
        self._token_valido=False
        self.sesion = None
        self.cargar_token()

    def _crear_sesion(self):
        sesion = requests.Session()
        sesion.cookies.update(self._token)
        return sesion

    def verificar_token(self)->bool:
        if self.sesion is None:
            return False

        try:
            response = self.sesion.post(API_URL_ONFORCE, data={
                "accion": "validar_ruc_bloqueado",
                "data[ruc]": self.RUC_PRUEBA,
            })
            data = json_valido(response)
            return data is not None
        except requests.RequestException:
            return False

    def cargar_token(self):
        cookies = cargar_json('cookies')
        if cookies is not None:
            self._token= cookies
            self.sesion=self._crear_sesion()
            self._token_valido=True
            print('Token cargado!')
        else:
            print('Token no encontrado')

    def validar_ruc_bloqueado(self, ruc):
        payload = {
            "accion": "validar_ruc_bloqueado",
            "data[ruc]": ruc,
        }
        response = self.consultar(payload)
        if not response:
            return None
    
        data={
            'estado': 'libre'
        }
        if response.get('response') != "success":
            data['comentario']=response.get('comment')
            data['estado'] = 'bloqueado'
            data['motivo']=response.get('data')[0]['MOTIVO']
            return data
        
        return data
    
    
    def consultar(self, payload):
        if not self._token_valido:
            obtener_token_onforce()
            self.cargar_token()

        if self.sesion is None:
            return None

        response =  self.sesion.post(API_URL_ONFORCE, data=payload)
        data= json_valido(response)
        if data is None:
            self._token_valido=False
        return data

    def score_crediticio(self, ruc):
        payload = {
            "accion": "score_cliente_light",
            "data[documento_identidad]": ruc,
            "data[tipo_doc]": "03"
        }

        response = self.consultar(payload)
        if not response:
            return None
        

        if response.get('response') != 'success':
            print(response.get('comment'))
            return None

        data_raw = response.get("data")

        if not data_raw:
            return None

        while isinstance(data_raw, str):
            data_raw = json.loads(data_raw)

        data_dict = data_raw

        try:
            reporte = data_dict["soapBody"]["ns3GetReporteOnlineResponse"]["ns2ReporteCrediticio"]

            # 2️⃣ Razon social
            razon_social = reporte["DatosPrincipales"]["Nombre"]

            # 3️⃣ Buscar SCORE (modulo codigo 644)
            score = None
            for modulo in reporte["Modulos"]["Modulo"]:
                if modulo.get("Codigo") == "644":
                    score = modulo["Data"]["ns3ResumenScore"]["Puntaje"]
                    break

            # 4️⃣ Buscar rubro (Directorio SUNAT - codigo 878)
            rubro = None
            for modulo in reporte["Modulos"]["Modulo"]:
                if modulo.get("Codigo") == "878":
                    rubro = modulo["Data"]["ns3DirectorioSUNAT"]["Directorio"]["DescripcionCIIU"]
                    break
            return {"razon_social": razon_social, "score": score, "rubro": rubro}

        except (KeyError, IndexError, TypeError):
            return None

      
    def cliente_carterizado_por_ruc(self, ruc):
        payload = {
            "accion": 'filtrarClientes',
            "data[num_ruc]": ruc,
        }
        response = self.consultar(payload)
        if not response:
            return False
        data = response
        if isinstance(data, list) and data and data[0].get('data', {}).get('data'):
            return True
        return False

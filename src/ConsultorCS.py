import requests
from utils.Utilidades import cargar_json
from auth.AuthEntel import obtener_token_entel
from config import API_URL_ENTEL, RUC_PRUEBA


class ConsultorCS:

    PAYLOAD_BASE = {
        "versionInfo": {
            "moduleVersion": "BkQkS7SLfOPdcIrsG62SZg",
            "apiVersion": "ixSC83b_wZJ9HXvvYNXb0w"
        },
        "viewName": "CommercialEvaluation_PE.ComEval",
        "screenData": {
            "variables": {
                "Ruc": "",
                "DisplayBar": False,
                "IsModalOpen": False,
                "IsLoading": True,
                "PortabilityLocal": {
                    "marketIndicator": "02",
                    "originCompany": "63",
                    "originType": "1"
                },
                "IsValidManualEntry": True,
                "IsManualEntry": False,
                "IsPortability": False,
                "ResultTypeModal": 1,
                "BlockType": 2,
                "EnableEvaluationButton": False,
                "IsManualEntryRRLL": True,
                "AccountInfoLocal": {
                    "OrganizationType": {
                        "Key": "PYME",
                        "Value": "Pyme / Soho (PE)"
                    },
                    "Category": {
                        "Key": "PELS",
                        "Value": "Empresas No Carterizado"
                    },
                    "HasAffinity": "N",
                    "RiskLevel": {
                        "Key": "MHIGH",
                        "Value": "Medio Alto"
                    },
                    "CreditSales": "N",
                    "RentAmount": "1000",
                    "CreationDate": "2024-05-29T17:17:58.786Z",
                    "HasPDT": "N",
                    "PrimaryContactPartyId": "0",
                    "TransactionType": "39",
                    "QSigners": 1,
                    "CurrentLegalRepresentativesNumber": 0,
                    "RRLLList": {
                        "List": [
                            {"DocumentNumber": "73016313"},
                            {"DocumentNumber": "73016313"},
                            {"DocumentNumber": ""}
                        ]
                    },
                    "GeneratesDocument": False,
                    "Subsegment": "PE - Low Soho"
                },
                "StoreIdLocal": "9620",
                "RegionIdLocal": "0",
                "ChannelTypeIdLocal": "DET",
                "ErrorPlatformNameLocal": "",
                "IsEmp": False,
                "Token": "",
                "_tokenInDataFetchStatus": 1,
                "GetAccountInfo": {
                    "ResultType": 1,
                    "Message": "",
                    "GetAccountInfo": {
                        "OrganizationType": {
                            "Key": "PYME",
                            "Value": "Pyme / Soho (PE)"
                        },
                        "Category": {
                            "Key": "PELS",
                            "Value": "Empresas No Carterizado"
                        },
                        "HasAffinity": "N",
                        "RiskLevel": {
                            "Key": "MHIGH",
                            "Value": "Medio Alto"
                        },
                        "CreditSales": "N",
                        "RentAmount": "",
                        "CreationDate": "2024-05-29T17:17:58.786Z",
                        "HasPDT": "N",
                        "PrimaryContactPartyId": "0",
                        "TransactionType": "",
                        "QSigners": 1,
                        "CurrentLegalRepresentativesNumber": 0,
                        "RRLLList": {
                            "List": [],
                            "EmptyListItem": {
                                "DocumentNumber": ""
                            }
                        },
                        "GeneratesDocument": False,
                        "Subsegment": "PE - Low Soho"
                    },
                    "ServiceRequestId": "300000491073417",
                    "ServiceRequestINumber": "2-0001209841",
                    "HasQSignersMissing": True,
                    "ErrorPlatformName": "",
                    "DataFetchStatus": 1
                }
            }
        }
    }

    def __init__(self):
        self._csrf_token = None
        self._token_valido = False
        self.RUC_PRUEBA = RUC_PRUEBA
        self.sesion = None
        self.cargar_token()

    def _crear_sesion(self):
        sesion = requests.Session()
        # Cookies de sesión
        sesion.cookies.update(self._csrf_token['cookies'])
        # Headers fijos
        sesion.headers.update({
            'Content-Type': 'application/json; charset=UTF-8',
            'x-csrftoken': self._csrf_token['csrf_token'],
            'accept': 'application/json',
            'origin': 'https://miempresa.entel.pe',
        })
        return sesion

    def cargar_token(self):
        datos = cargar_json('entel')
        if datos and isinstance(datos, dict) and datos.get('cookies'):
            self._csrf_token = datos
            self.sesion = self._crear_sesion()
            self._token_valido = True
            print('Token Entel cargado!')
        else:
            print('Token Entel no encontrado')

    def verificar_token(self):
        response = self.evaluar_ruc(self.RUC_PRUEBA)
        return response is not None

    def consultar(self, payload):
        """Hace POST al endpoint de Entel con auto-refresh de token."""
        if not self._token_valido:
            obtener_token_entel()
            self.cargar_token()

        response = self.sesion.post(API_URL_ENTEL, json=payload)

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text[:200]}")
            self._token_valido = False
            return None

        try:
            return response.json()
        except Exception:
            print("Respuesta no es JSON válido")
            self._token_valido = False
            return None

    def evaluar_ruc(self, ruc, token_param=""):
        """Evalúa un RUC construyendo el payload completo.
        
        Args:
            ruc: Número de RUC a evaluar
            token_param: Token de la URL (el Base64 con info de usuario/tienda)
        """
        import copy
        payload = copy.deepcopy(self.PAYLOAD_BASE)
        payload['screenData']['variables']['Ruc'] = str(ruc)
        print(ruc)
        if token_param:
            payload['screenData']['variables']['Token'] = token_param

        return self.consultar(payload)

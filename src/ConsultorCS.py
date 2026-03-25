from utils.Utilidades import obtener_valor
from utils.Utilidades import json_valido
import copy
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
        self.verificar_token()

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

    def verificar_token(self)->bool:
        response = self.evaluar_ruc(self.RUC_PRUEBA)
        if response is None:
            self._token_valido=False
            return False

        if not response:
            self._token_valido=False
            return False
        return True

    def consultar(self, payload):
        """Hace POST al endpoint de Entel con auto-refresh de token."""
        if not self._token_valido:
            obtener_token_entel()
            self.cargar_token()

        response = self.sesion.post(API_URL_ENTEL, json=payload)
        data = json_valido(response, 'application/json; charset=utf-8')
        if data is None:
            self._token_valido=False
            return None
        return data

    def evaluar_ruc(self, ruc)->dict:
        """Evalúa un RUC construyendo el payload completo.
        
        Args:
            ruc: Número de RUC a evaluar
            token_param: Token de la URL (el Base64 con info de usuario/tienda)
        """
        payload = copy.deepcopy(self.PAYLOAD_BASE)
        payload['screenData']['variables']['Ruc'] = str(ruc)
        response_json= self.consultar(payload)
        evaluacion=obtener_valor(response_json,'data','ResponsePCOEvaluation')
      
        data={
            'preevaluacion_crediticia': obtener_valor(evaluacion,'RejectedMessage'),
            'estado_aprobacion':obtener_valor(evaluacion,'IsApproved'),
            'planes_datos': {
                'monto_maximo': obtener_valor(evaluacion,'AdditionalServices','MaximumAmountAvailableForContractingMobileServices'),
                'monto_ocupado': obtener_valor(evaluacion,'AdditionalServices','AmountOccupiedOnMobileServices'),
                'monto_disponible': obtener_valor(evaluacion,'AdditionalServices','AmountAvailableToContractMobileServices'),
                
                
                },
            'equipos_accesorios':{
                'tipo_cliete':obtener_valor(evaluacion,'TypeOfCustomer'),
                'meses_financiamiento':obtener_valor(evaluacion,'EquipmentAndAccesories','NumberOfMonthsForFinancingInstallments'),
                'monto_maximo_financiamiento': obtener_valor(evaluacion,'EquipmentAndAccesories','AmountAvailableToFinanceEquipmentAndAccessories'),
                'monto_ocupado_financiamiento': obtener_valor(evaluacion,'EquipmentAndAccesories','AmountOccupiedInLeasedEquipment'),
                'monto_disponible_financiamiento': obtener_valor(evaluacion,'EquipmentAndAccesories','AmountAvailableToFinanceEquipmentAndAccessories'),
                
            }
          }
        return data

from config import RUC_PRUEBA
from abc import ABC, abstractmethod
class ConsultorBASE(ABC):
    RUC_PRUEBA = RUC_PRUEBA
    def __init__(self):
        self._token = None
    

    @abstractmethod
    def verificar_token(self)->bool:
        pass


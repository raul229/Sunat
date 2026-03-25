import pytest
from src.ConsultorCS import ConsultorCS


@pytest.fixture(scope="session")
def consultor():
    c = ConsultorCS()
    return c


def test_evaluar_ruc(consultor):
    data = consultor.evaluar_ruc("20494217296")
    print(data)
    
    assert data is not None
    
def test_verificar_token(consultor):

    print(consultor.verificar_token())
    
    assert consultor.verificar_token()

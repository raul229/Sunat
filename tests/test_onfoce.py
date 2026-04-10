import pytest
from src.ConsultorOF import ConsultorOF



@pytest.fixture(scope="session")
def consultor():
    c = ConsultorOF()
    c.verificar_token()
    return c

def test_validar_bloqueados(consultor):
    data = consultor.validar_ruc_bloqueado(20522317285)
    assert data['estado'] == 'bloqueado'

def test_score(consultor):
    data = consultor.score_crediticio(20522317285)
    print(data)
    assert data['score'] == '838'
    
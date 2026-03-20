import pytest
from src.ConsultorCS import ConsultorCS


@pytest.fixture(scope="session")
def consultor():
    c = ConsultorCS()
    return c


def test_evaluar_ruc(consultor):
    data = consultor.evaluar_ruc("20608846701")
    print(data)
    assert data is not None

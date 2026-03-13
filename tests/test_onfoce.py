from src.ConsultorOF import ConsultorOF
def test_validar_bloqueados():
    c=ConsultorOF()
    data = c.validar_ruc_bloqueado(20522317285)
    
    assert data['error'] == 'bloqueado'
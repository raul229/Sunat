from auth.AuthOnForce import obtener_token_onforce
from src.ConsultorOF import ConsultorOF
from config import RUC_PRUEBA


def main():
    # Intentar cargar token guardado
    consultor = ConsultorOF()

    if consultor.verificar_token():
        print("✅ Token valido")
        ruc = input(f"Ingresa RUC (Enter para {RUC_PRUEBA}): ").strip()
        if not ruc:
            ruc = RUC_PRUEBA
        response =consultor.consultar(ruc)
        print(response.json())

        return
    else:
        print("🔐 Por favor, inicia sesión manualmente en el navegador.")
        token = obtener_token_onforce()
        if token:
            # Preguntar si quiere hacer consulta ahora
            usar_ahora = input("¿Quieres hacer una consulta ahora? (s/n): ").lower()
            if usar_ahora == 's':
                ruc = input(f"Ingresa RUC (Enter para {RUC_PRUEBA}): ").strip()
                if not ruc:
                    ruc = RUC_PRUEBA
                consultor.cargar_token()
                print(consultor.consultar(ruc).json())        
if __name__ == '__main__':
    main()
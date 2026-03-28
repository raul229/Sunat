from fastapi import FastAPI, Request
from src.ConsultorCS import ConsultorCS
from utils.Utilidades import _asegurar_archivo_token,_guardar_en_tokenfile
import uvicorn


# Crear la aplicación FastAPI
app = FastAPI(
    title="Mi Primera API con FastAPI",
    description="Una API de prueba",
    version="1.0.0"
)

consultor = ConsultorCS()
consultor.login_remoto = True

# Endpoint con parámetros de ruta y de consulta (query)
@app.post("/consulasuelta/")
async def consulta_suelta(request: Request):
    data = await request.json()
    return consultor.evaluar_ruc(data['ruc'])

@app.post("/token/")
async def token(request: Request):
    data = await request.json()
    _asegurar_archivo_token()
    _guardar_en_tokenfile(data,'entel')
    consultor.cargar_token()
    return {"status":"ok"}


# Bloque para ejecutar el servidor de desarrollo al correr 'python api.py'
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

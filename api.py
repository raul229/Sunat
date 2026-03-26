from fastapi import FastAPI, Request
from src.ConsultorCS import ConsultorCS
import uvicorn


# Crear la aplicación FastAPI
app = FastAPI(
    title="Mi Primera API con FastAPI",
    description="Una API de prueba",
    version="1.0.0"
)

consultor = ConsultorCS()

# Endpoint con parámetros de ruta y de consulta (query)
@app.post("/consulasuelta/")
async def consulta_suelta(request: Request):
    data = await request.json()
    return consultor.evaluar_ruc(data['ruc'])

# Bloque para ejecutar el servidor de desarrollo al correr 'python api.py'
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

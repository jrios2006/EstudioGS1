from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Optional
import json
from module.lib_json import leer_json, custom_serializer
from module.lib_gs1 import procesar_codigo_gs1

# Crear la aplicación FastAPI
app = FastAPI()

# Definir el modelo de entrada para POST
class CodigoRequest(BaseModel):
    codigo: str

# Definir el modelo de salida
class CodigoResponse(BaseModel):
    codigo: str
    estado: bool
    errores: List[str]
    resultado: Optional[dict]
    warnings: List[str]
    comentarios: str
    version_api: str

# Ruta al archivo de configuración
CONFIG_PATH = 'config/codigos_gs1.json'
VERSION_API = "2025-02-03"

@app.get("/parse_datamatrix", response_model=CodigoResponse)
@app.post("/parse_datamatrix", response_model=CodigoResponse)
def procesar_codigo(
    data: Optional[CodigoRequest] = None,  # Para POST (puede ser None en GET)
    codigo: Optional[str] = Query(None)   # Para GET
):
    try:
        # Determinar el código a procesar
        codigo_procesar = data.codigo if data else codigo
        if not codigo_procesar:
            raise ValueError("Debe proporcionar un código en el cuerpo (POST) o en la query string (GET).")
        
        # Leer los parámetros GS1 desde el archivo JSON
        parametros_gs1 = leer_json(ruta_archivo=CONFIG_PATH)
        
        # Procesar el código GS1
        resultado = procesar_codigo_gs1(cadena=codigo_procesar, parametros_gs1=parametros_gs1)
        
        # Construir la respuesta
        response = CodigoResponse(
            codigo=codigo_procesar,
            estado=True,
            errores=[],
            resultado=resultado,
            warnings=[],
            comentarios="",
            version_api=VERSION_API
        )
        return response

    except Exception as e:
        # Manejo de errores
        return CodigoResponse(
            codigo=codigo_procesar if 'codigo_procesar' in locals() else "",
            estado=False,
            errores=[str(e)],
            resultado=None,
            warnings=[],
            comentarios="Error al procesar el código",
            version_api=VERSION_API
        )

# Para probar localmente, puedes ejecutar el archivo como script principal
# con `uvicorn nombre_archivo:app --reload`

from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Optional
import json
from module.lib_json import leer_json, custom_serializer
from module.lib_gs1 import procesar_codigo_gs1
from fastapi import FastAPI, HTTPException, Query, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import json
from module.lib_json import leer_json, custom_serializer
from module.lib_gs1 import procesar_codigo_gs1

# Sobrescribir JSONResponse para formatear el JSON con indentación
class PrettyJSONResponse(JSONResponse):
    def render(self, content: dict) -> bytes:
        # Usar json.dumps con indentación y asegurar utf-8
        return json.dumps(content, indent=4, ensure_ascii=False).encode("utf-8")

# Crear la aplicación FastAPI
app = FastAPI(default_response_class=PrettyJSONResponse)

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
async def procesar_codigo(
    request: Request,  # Permite acceder a los parámetros de la solicitud
    data: Optional[CodigoRequest] = None,  # Para POST (puede ser None en GET)
    codigo: Optional[str] = Query(None)   # Para GET
):
    try:
        # Determinar el código a procesar
        codigo_procesar = data.codigo if data else codigo
        if not codigo_procesar:
            raise ValueError("Debe proporcionar un código en el cuerpo (POST) o en la query string (GET).")
        
        # Detectar parámetros inesperados en la query string
        parametros_recibidos_query = set(request.query_params.keys())
        parametros_esperados_query = {"codigo"}  # Lista de parámetros válidos para query string
        parametros_no_reconocidos_query = parametros_recibidos_query - parametros_esperados_query

        # Detectar parámetros inesperados en el cuerpo (solo para POST)
        parametros_no_reconocidos_body = []
        if data:
            # Obtener los parámetros enviados en el cuerpo de la solicitud como dict
            body_dict = await request.json()
            body_recibidos = set(body_dict.keys())
            body_esperados = set(CodigoRequest.schema()["properties"].keys())
            parametros_no_reconocidos_body = body_recibidos - body_esperados

        # Construir los warnings
        warnings = []
        if parametros_no_reconocidos_query:
            warnings.append(f"Los parámetros {', '.join(parametros_no_reconocidos_query)} en la query string no tienen efecto.")
        if parametros_no_reconocidos_body:
            warnings.append(f"Los parámetros {', '.join(parametros_no_reconocidos_body)} en el cuerpo de la solicitud no tienen efecto.")

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
            warnings=warnings,
            comentarios="",
            version_api=VERSION_API
        )
        return response

    except Exception as e:
        # Manejo de errores
        error_respuesta = {
            "codigo": "",
            "estado": False,
            "errores": [str(e)],
            "resultado": None,
            "warnings": [],
            "comentarios": "Error al procesar el código",
            "version_api": VERSION_API
        }
        return PrettyJSONResponse(content=error_respuesta, status_code=400)

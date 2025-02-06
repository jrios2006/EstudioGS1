import pandas as pd
import json
import base64
from module.lib_json import leer_json, custom_serializer, obtener_application_identifiers
from module.lib_gs1 import procesar_codigo_gs1

def procesar_codigo_y_generar_datos(codigo, parametros_gs1, lista_ai):
    # Procesar el código
    resultado = procesar_codigo_gs1(cadena=codigo, parametros_gs1=parametros_gs1)

    # Filtrar el resultado
    resultado_filtrado = {key: value for key, value in resultado.items() if key in lista_ai}

    # Calcular tamaños
    tamaño_codigo_bytes = len(codigo.encode('utf-8'))
    tamaño_codigo_caracteres = len(codigo)
    resultado_serializado = json.dumps(resultado_filtrado, default=custom_serializer)
    tamaño_resultado_caracteres = len(resultado_serializado)
    tamaño_resultado_bytes = len(resultado_serializado.encode('utf-8'))

    # Codificación base64
    codigo_base64 = base64.b64encode(codigo.encode('utf-8')).decode('utf-8')
    resultado_filtrado_base64 = base64.b64encode(resultado_serializado.encode('utf-8')).decode('utf-8')
    longitud_codigo_base64 = len(codigo_base64)
    longitud_resultado_filtrado_base64 = len(resultado_filtrado_base64)

    # Crecimientos
    incremento_bytes = tamaño_resultado_bytes - tamaño_codigo_bytes
    incremento_base64 = longitud_resultado_filtrado_base64 - longitud_codigo_base64

    # Incrementos en porcentaje
    incremento_bytes_porcentaje = (incremento_bytes / tamaño_codigo_bytes) * 100 if tamaño_codigo_bytes > 0 else 0
    incremento_base64_porcentaje = (incremento_base64 / longitud_codigo_base64) * 100 if longitud_codigo_base64 > 0 else 0

    # Retornar los datos calculados como un diccionario
    return {
        "Código Original": codigo,
        "Tamaño Código (caracteres)": tamaño_codigo_caracteres,
        "Tamaño Código (bytes)": tamaño_codigo_bytes,
        "Resultado Filtrado (JSON)": resultado_serializado,
        "Tamaño Resultado (caracteres)": tamaño_resultado_caracteres,
        "Tamaño Resultado (bytes)": tamaño_resultado_bytes,
        "Código Base64": codigo_base64,
        "Longitud Código Base64 (caracteres)": longitud_codigo_base64,
        "Resultado Filtrado Base64": resultado_filtrado_base64,
        "Longitud Resultado Base64 (caracteres)": longitud_resultado_filtrado_base64,
        "Incremento en Bytes (JSON vs Código)": incremento_bytes,
        "Incremento en Base64 (JSON vs Código)": incremento_base64,
        "Incremento en Bytes (%)": incremento_bytes_porcentaje,
        "Incremento en Base64 (%)": incremento_base64_porcentaje
    }

if __name__ == "__main__":
    # Leer parámetros GS1
    parametros_gs1 = leer_json(ruta_archivo='config/codigos_gs1.json')
    lista_ai = obtener_application_identifiers(parametros_gs1)

    # Leer el archivo TXT con los códigos (un código por línea)
    input_txt = "test/TestGS1.txt"
    with open(input_txt, "r", encoding="utf-8") as file:
        codigos = [line.strip() for line in file.readlines()]

    # Lista para almacenar los resultados
    resultados = []

    # Procesar cada código en el archivo
    for codigo in codigos:
        if codigo:  # Evitar procesar líneas vacías
            datos = procesar_codigo_y_generar_datos(codigo, parametros_gs1, lista_ai)
            resultados.append(datos)

    # Crear un DataFrame con los resultados
    resultados_df = pd.DataFrame(resultados)

    # Guardar los resultados en un archivo Excel
    output_excel = "test/resultados_codigos.xlsx"
    resultados_df.to_excel(output_excel, index=False)

    print(f"Procesamiento completado. Resultados guardados en: {output_excel}")

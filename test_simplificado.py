import json
import base64
from module.lib_json import leer_json, custom_serializer, obtener_application_identifiers
from module.lib_gs1 import procesar_codigo_gs1

# Ejecutar el procesamiento
if __name__ == "__main__":

    # Ruta al archivo de entrada y salida
    codigo = "010843701315676921A014MFCNMYF5AR1024C0106B172703317127062585"
    # Leer los parámetros GS1
    parametros_gs1 = leer_json(ruta_archivo='config/codigos_gs1.json')

    # Procesar el código y devolver su resultado
    resultado = procesar_codigo_gs1(cadena=codigo, parametros_gs1=parametros_gs1)
    
    # Obtener la lista de identificadores de aplicación permitidos
    lista_ai = obtener_application_identifiers(parametros_gs1)

    # Recorrer y filtrar los atributos del diccionario resultado
    resultado_filtrado = {key: value for key, value in resultado.items() if key in lista_ai}

    # Imprimir el resultado filtrado con indentación de 2 caracteres
    print("Resultado Filtrado:")
    print(json.dumps(resultado_filtrado, indent=2, default=custom_serializer))

    # Calcular tamaño del código
    tamaño_codigo_bytes = len(codigo.encode('utf-8'))
    tamaño_codigo_caracteres = len(codigo)
    print(f"\nTamaño del código:")
    print(f"- Número de caracteres: {tamaño_codigo_caracteres}")
    print(f"- Tamaño en bytes: {tamaño_codigo_bytes}")

    # Serializar resultado filtrado y calcular su tamaño
    resultado_serializado = json.dumps(resultado_filtrado, default=custom_serializer)
    tamaño_resultado_caracteres = len(resultado_serializado)
    tamaño_resultado_bytes = len(resultado_serializado.encode('utf-8'))
    print(f"\nTamaño del resultado filtrado:")
    print(f"- Número de caracteres (serializado): {tamaño_resultado_caracteres}")
    print(f"- Tamaño en bytes (serializado): {tamaño_resultado_bytes}")

    # Codificar en base64 el código y el resultado filtrado
    codigo_base64 = base64.b64encode(codigo.encode('utf-8')).decode('utf-8')
    resultado_filtrado_base64 = base64.b64encode(resultado_serializado.encode('utf-8')).decode('utf-8')

    print(f"\nCodificación en base64:")
    print(f"- Código en base64: {codigo_base64}")
    print(f"- Resultado filtrado en base64: {resultado_filtrado_base64}")

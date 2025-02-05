import json
from module.lib_json import leer_json, custom_serializer
from module.lib_gs1 import procesar_codigo_gs1

# Ejecutar el procesamiento
if __name__ == "__main__":

    # Ruta al archivo de entrada y salida
    codigo = "010843701315676921A014MFCNMYF5AR1024C0106B172703317127062585"
    # Leer los parámetros GS1
    parametros_gs1 = leer_json(ruta_archivo='config/codigos_gs1.json')

    # Procesar el codigo y devolver su resultado
    resultado = procesar_codigo_gs1(cadena=codigo, parametros_gs1=parametros_gs1)
    # Imprimir el resultado con indentación de 2 caracteres
    print(json.dumps(resultado, indent=2, ensure_ascii=False, default=custom_serializer))

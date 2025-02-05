import json
import pandas as pd
from datetime import datetime, date
from module.lib_json import leer_json
from module.lib_gs1 import procesar_codigo_gs1

# Leer el archivo de códigos y procesar cada uno
def procesar_fichero_entrada(ruta_archivo_entrada, ruta_archivo_salida, parametros_gs1):
    # Leer las líneas del archivo de entrada
    with open(ruta_archivo_entrada, 'r') as f:
        lineas = f.readlines()

    resultados = []

    for linea in lineas:
        cadena = linea.strip()
        print(f"Procesando: {cadena}")
        resultado = procesar_codigo_gs1(cadena, parametros_gs1)
        resultados.append({
            "Datamatrix": resultado["datamatrix"],
            "NumeroSerie": resultado.get("NumeroSerie", ""),
            "Lote": resultado.get("Lote", ""),
            "FechaCaducidad": resultado.get("FechaCaducidad", ""),
            "RegistroSanitario": resultado.get("RegistroSanitario", ""),
            "Observaciones": "; ".join(resultado["observaciones"]),
            "AIsUsados": ", ".join(resultado["ais"]),
            "version": resultado["version"]
        })

    # Convertir los resultados a un DataFrame de pandas
    df = pd.DataFrame(resultados)

    # Convertir `FechaCaducidad` a solo la fecha (YYYY-MM-DD)
    df['FechaCaducidad'] = df['FechaCaducidad'].apply(
        lambda x: x.date() if isinstance(x, (datetime, date)) else x
    )
    # Guardar el DataFrame en un archivo Excel
    df.to_excel(ruta_archivo_salida, index=False)
    print(f"Resultados exportados a {ruta_archivo_salida}")

# Ejecutar el procesamiento
if __name__ == "__main__":
    # Ruta al archivo de entrada y salida
    archivo_entrada = "test/TestGS1.txt"
    archivo_salida = "test/resultado_gs1.xlsx"

    # Leer los parámetros GS1
    parametros_gs1 = leer_json(ruta_archivo='config/codigos_gs1.json')

    # Procesar el archivo de entrada y exportar a Excel
    procesar_fichero_entrada(archivo_entrada, archivo_salida, parametros_gs1)

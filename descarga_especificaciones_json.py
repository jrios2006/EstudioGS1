import os
import json
import requests
from datetime import datetime
from module.lib_json import leer_json, guardar_json

# Variables iniciales
URL = "https://ref.gs1.org/ai/GS1_Application_Identifiers.jsonld"
ruta_config = "config/codigos_gs1.json"
fnc1_list = ["\\x1D", "|", "^", "#", " ", "(SEPARADOR)"]

# Descargar datos desde la URL
def descargar_datos_desde_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta excepción si hay error HTTP
        return response.json()
    except Exception as e:
        print(f"Error al descargar datos desde la URL: {e}")
        return None

# Comparar y actualizar los datos
def comparar_y_actualizar_datos(datos_descargados, ruta_fichero, fnc1_list):
    # Leer datos del fichero
    datos_locales = leer_json(ruta_archivo=ruta_fichero)

    # Quitar "FNC1List" de los datos locales para comparación
    datos_locales_sin_fnc1 = datos_locales.copy()
    datos_locales_sin_fnc1.pop("FNC1List", None)

    # Comparar diccionarios
    if datos_descargados != datos_locales_sin_fnc1:
        print("Los datos han cambiado. Actualizando...")

        # Crear un backup del fichero actual
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_backup = f"config/codigos_gs1_{fecha_actual}.json"
        guardar_json(datos_locales, ruta_backup)
        print(f"Backup creado: {ruta_backup}")

        # Añadir "FNC1List" a los datos descargados
        datos_descargados["FNC1List"] = fnc1_list

        # Guardar los datos actualizados en el fichero original
        guardar_json(datos_descargados, ruta_fichero)
        print(f"Datos actualizados guardados en {ruta_fichero}")
    else:
        print("Los datos no han cambiado. No es necesario actualizar.")

# Función principal
def main():
    # Descargar los datos desde la URL
    print("Descargando datos desde la URL...")
    datos_descargados = descargar_datos_desde_url(URL)
    if not datos_descargados:
        print("No se pudo descargar el archivo. Terminando el programa.")
        return

    # Comparar y actualizar los datos
    print("Comparando datos...")
    comparar_y_actualizar_datos(datos_descargados, ruta_config, fnc1_list)

# Ejecutar el programa
if __name__ == "__main__":
    main()

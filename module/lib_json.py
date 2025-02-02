import json

def leer_json(ruta_archivo):
    '''
    Lee un archivo JSON y devuelve su contenido como un diccionario.
    Si ocurre un error, devuelve un diccionario vacío.

    Args:
        ruta_archivo (str): La ruta del archivo JSON a leer.

    Returns:
        dict: El contenido del archivo JSON como un diccionario, o un diccionario vacío en caso de error.
    '''
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except Exception as e:
        print(f"Error al leer el archivo JSON {ruta_archivo}: {e}")
        return {}

# Ejemplo de uso:
# configuracion = leer_json('config/config.json')

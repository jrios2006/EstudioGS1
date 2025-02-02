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

def obtener_application_identifiers(data):
    ''' Leo un diccionario de datos y si la clave 'applicationIdentifiers' está en el diccionario devuelvo una lista con el campo 
    applicationIdentifier.

    Args:
        data (dict): El diccionario donde buscar.

    Returns:
        list: los elementos encontrados en el diccionario, o lista vacía si no se encuentra la clave o si el tipo de dato no es un diccionario.
    '''
    # Verifica si 'data' es un diccionario
    if not isinstance(data, dict):
        return []  # Devuelve una lista vacía si no es un diccionario

    # Verifica si la clave 'applicationIdentifiers' existe y si es una lista
    if 'applicationIdentifiers' in data and isinstance(data['applicationIdentifiers'], list):
        # Crea una lista con los valores de 'applicationIdentifier' dentro de la lista de objetos
        return [item.get('applicationIdentifier') for item in data['applicationIdentifiers'] if 'applicationIdentifier' in item]
    
    # Si no encuentra lo que busca, devuelve una lista vacía
    return []

# Ejemplo de uso:
# configuracion = leer_json('config/config.json')
# lista_ai = obtener_application_identifiers(configuracion)


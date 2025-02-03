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

def eliminar_si_existe(lista, elemento):
    """Elimina el elemento de la lista si existe y devuelve la lista modificada.
    
    Esta función verifica si el elemento dado está presente en la lista. Si el elemento se encuentra
    en la lista, lo elimina. Si no está presente, la lista permanece sin cambios. Finalmente, devuelve
    la lista modificada (ya sea con el elemento eliminado o sin cambios).
    
    Args:
    lista (list): La lista de elementos en la cual se desea eliminar un elemento.
    elemento (str, int, etc.): El elemento que se desea eliminar de la lista. Puede ser de cualquier tipo
                               compatible con la lista.
    
    Returns:
    list: La lista resultante después de intentar eliminar el elemento. Si el elemento estaba en la lista,
          se devuelve la lista sin ese elemento; si no estaba, la lista permanece igual.
    
    Ejemplos:
    
    >>> eliminar_si_existe([1, 2, 3, 4], 3)
    [1, 2, 4]  # El elemento 3 es eliminado, la lista resultante es [1, 2, 4]
    
    >>> eliminar_si_existe([1, 2, 3, 4], 5)
    [1, 2, 3, 4]  # El elemento 5 no está en la lista, por lo que la lista permanece igual
    
    >>> eliminar_si_existe(["manzana", "plátano", "cereza"], "plátano")
    ["manzana", "cereza"]  # El elemento "plátano" es eliminado, la lista resultante es ["manzana", "cereza"]
    
    >>> eliminar_si_existe([True, False, True], False)
    [True, True]  # El elemento False es eliminado, la lista resultante es [True, True]
    """
    if elemento in lista:
        lista.remove(elemento)
    return lista

def buscar_ai_en_codigos(ai, codigos_ai):
    '''Busca un código AI dentro de un diccionario de códigos y devuelve el elemento correspondiente.

    La función toma un identificador AI y un diccionario que contiene una lista de códigos bajo la clave
    "applicationIdentifiers". Si encuentra una coincidencia con el campo "applicationIdentifier",
    devuelve el diccionario correspondiente. Si no lo encuentra, devuelve un diccionario vacío.

    Args:
        ai (str): Identificador AI a buscar.
        codigos_ai (dict): Diccionario que contiene la clave "applicationIdentifiers", 
                           la cual es una lista de diccionarios con información sobre los AI.

    Returns:
        dict: El diccionario que coincide con el "applicationIdentifier" buscado, o un diccionario vacío si no hay coincidencia.

    Ejemplos:
        >>> codigos = {
        ...     "applicationIdentifiers": [
        ...         {"applicationIdentifier": "01", "description": "GTIN"},
        ...         {"applicationIdentifier": "21", "description": "Serial Number"}
        ...     ]
        ... }
        >>> buscar_ai_en_codigos("01", codigos)
        {'applicationIdentifier': '01', 'description': 'GTIN'}

        >>> buscar_ai_en_codigos("99", codigos)
        {}  # No se encontró el AI
    '''
    
    # Verificar que "codigos_ai" es un diccionario y que tiene la clave "applicationIdentifiers"
    if not isinstance(codigos_ai, dict) or "applicationIdentifiers" not in codigos_ai:
        return {}

    # Obtener la lista de identificadores
    lista_identificadores = codigos_ai["applicationIdentifiers"]

    # Buscar en la lista el elemento que coincida con "applicationIdentifier"
    for elemento in lista_identificadores:
        if elemento.get("applicationIdentifier") == ai:
            return elemento  # Retorna el diccionario encontrado

    return {}  # Retorna un diccionario vacío si no encuentra coincidencia


# Ejemplo de uso:
# credenciales = leer_json('config/credenciales.json')
# configuracion = leer_json('config/config.json')

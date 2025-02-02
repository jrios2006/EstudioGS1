def convertir_separadores_hex(separadores):
    '''Convierte las cadenas de separadores hexadecimales a caracteres reales'''
    return [bytes(sep, 'utf-8').decode('unicode_escape') if '\\x' in sep else sep for sep in separadores]

def existe_separador(cadena, separadores):
    '''Función que nos dice si existe uno de los separadores que puede tener parte de una cadena Datamatrix.
    Devuelve True o False. Si es True, nos devuelve el carácter separador en otro campo.
    Si es False, devuelve None.
    
    Args:
        cadena (str): La cadena donde buscar los separadores.
        separadores (list): Lista de posibles separadores a verificar.

    Returns:
        tuple: (True/False, separador_encontrado o None)
    '''
    # Verificar si 'cadena' es un string y 'separadores' es una lista
    if not isinstance(cadena, str) or not isinstance(separadores, list):
        return False, None  # Si los tipos no son correctos, devuelve False y None

    # Convertir los separadores hexadecimales (ej. '\\x1d') a los caracteres reales
    separadores_convertidos = [bytes(sep, 'utf-8').decode('unicode_escape') if '\\x' in sep else sep for sep in separadores]    
    
    separador_encontrado = None
    # Determinamos si hay un separador presente
    for separador in separadores_convertidos:
        if separador in cadena:
            separador_encontrado = separador
            break  # Salimos del bucle al encontrar el primer separador

    # Si encontramos un separador, devolvemos True y el separador; si no, devolvemos False y None
    tiene_separador = separador_encontrado is not None
    return tiene_separador, separador_encontrado

def dividir_cadena(cadena, separador):
    '''Dada una cadena de texto, devuelve una lista obtenida al dividir la cadena con el separador.
    
    Si el separador no se encuentra en la cadena o si el separador es None, devuelve una lista con un solo elemento, que es la cadena completa.
    
    Args:
    cadena (str): La cadena de texto que se desea dividir.
    separador (str or None): El separador que se usará para dividir la cadena. Si es None, la cadena no se divide y se devuelve como único elemento.
    
    Returns:
    list: Una lista de subcadenas divididas por el separador. 
          Si el separador no se encuentra o es None, la lista contiene la cadena original como único elemento.
          
    Ejemplo:
    >>> dividir_cadena("apple,banana,orange", ",")
    ['apple', 'banana', 'orange']
    
    >>> dividir_cadena("apple", ",")
    ['apple']
    
    >>> dividir_cadena("apple", None)
    ['apple']
    '''
    # Si el separador es None, devolver la cadena original en una lista
    if separador is None:
        return [cadena]
    
    return cadena.split(separador)


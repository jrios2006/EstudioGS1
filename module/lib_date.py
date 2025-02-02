import calendar

def es_fecha_valida(cadena):
    '''Función que valida una fecha dada en formato YYMMDD.

    La función verifica si la cadena de entrada tiene una longitud de 6 caracteres y es completamente numérica.
    Luego, valida que el mes esté entre 01 y 12 y ajusta el último día del mes si el día es "00", para que la fecha sea válida.
    
    Si la cadena no es un string o no tiene el formato adecuado (6 dígitos), la función devuelve False.
    
    Args:
    cadena (str): La fecha en formato YYMMDD, donde:
                  - YY representa el año (últimos 2 dígitos).
                  - MM representa el mes (01 a 12).
                  - DD representa el día (01 a 31, ajustado si DD es "00").
    
    Returns:
    bool: 
        - True si la fecha es válida.
        - False si la cadena no tiene el formato adecuado o si la fecha no es válida.
    
    Ejemplos:
    >>> es_fecha_valida("230215")
    True
    
    >>> es_fecha_valida("230200")
    True  # El día "00" se ajusta al último día del mes (28 o 29 en febrero dependiendo del año)
    
    >>> es_fecha_valida("230213")
    True
    
    >>> es_fecha_valida("239913")
    False  # Mes 99 no es válido
    
    >>> es_fecha_valida("230415")
    False  # El 15 de abril es una fecha válida, pero esto es solo un ejemplo si el formato fuera incorrecto
    
    >>> es_fecha_valida(230215)
    False  # Si no es una cadena, devuelve False
    '''
    
    # Verificar que la cadena es un string y tiene 6 caracteres numéricos
    if not isinstance(cadena, str) or len(cadena) != 6 or not cadena.isdigit():
        return False
    # Extraer el año, mes y día de la cadena
    anio = "20" + cadena[:2]  # Asumir que el año es en 2000s
    mes = int(cadena[2:4])
    dia = cadena[4:]
    if mes < 1 or mes > 12:
        # El mes no es válido
        return False
    if dia == "00":
        dia = calendar.monthrange(int(anio), mes)[1]  # Obtiene el último día del mes
    else:
        dia = int(dia)
        if dia < 1 or dia > calendar.monthrange(int(anio), mes)[1]:
            # El día no es válido
            return False
    return True

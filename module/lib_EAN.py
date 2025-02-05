def calcular_digito_control_EAN13(cadena):
    '''Función que calcula el dígito de control (checksum) para una cadena de 12 dígitos.
    
    Esta función implementa el algoritmo de Luhn para calcular el dígito de control de un código EAN13,
    que consiste en un código de 13 dígitos. Se proporciona una cadena de 12 dígitos y la función calcula
    el dígito de control que completa el código EAN13.

    Si la cadena no tiene exactamente 12 dígitos o no es una cadena numérica, la función devuelve -1
    como indicativo de un error.

    Args:
    cadena (str): Una cadena de 12 dígitos numéricos. Debe contener solo números y tener una longitud de 12 caracteres.

    Returns:
    int: El dígito de control calculado. Si la cadena tiene un formato incorrecto, se devuelve -1.
    
    El algoritmo sigue los siguientes pasos:
    1. Verifica si la cadena tiene exactamente 12 dígitos.
    2. Si es válida, calcula la suma ponderada de los dígitos de la cadena, alternando entre multiplicar
       los dígitos en posiciones impares por 3 y los de las posiciones pares por 1.
    3. Calcula el módulo 10 de la suma y determina el dígito de control.
    4. Si el módulo es 0, el dígito de control es 0; de lo contrario, es 10 menos el módulo.
    
    Ejemplos:

    >>> calcular_digito_control_EAN13("123456789012")
    3  # El dígito de control calculado es 3

    >>> calcular_digito_control_EAN13("12345abc9012")
    -1  # La cadena contiene caracteres no numéricos, por lo que devuelve -1

    >>> calcular_digito_control_EAN13("987654321098")
    2  # El dígito de control calculado es 2

    >>> calcular_digito_control_EAN13("123")
    -1  # La cadena no tiene 12 dígitos, por lo que devuelve -1
    '''
    
    # Comprobamos si la cadena tiene exactamente 12 dígitos y si todos son numéricos
    if len(cadena) != 12 or not cadena.isdigit():
        return -1
    
    suma = 0
    # Iteramos sobre los 12 dígitos
    for i in range(12):
        digito = int(cadena[i])
        # Si la posición es par (recordando que empieza en 0), se multiplica por 1
        # Si es impar, se multiplica por 3
        if i % 2 == 0:
            suma += digito
        else:
            suma += digito * 3
    
    # Calculamos el módulo 10
    modulo = suma % 10
    # Si el módulo es 0, el dígito de control es 0; de lo contrario, es 10 menos el módulo
    digito_control = 0 if modulo == 0 else 10 - modulo
    
    return digito_control

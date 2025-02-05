from module.lib_date import es_fecha_valida, get_fecha
from module.lib_string import eliminar_prefijo
from module.lib_json import eliminar_si_existe
from module.lib_EAN import calcular_digito_control_EAN13

def proceso_ai_17(cadena, resultado, lista_patrones):
    '''
    Procesa un Application Identifier (AI) de tipo "17" en una cadena GS1 Datamatrix y actualiza el resultado. 
    El AI "17" representa la fecha de caducidad en formato YYMMDD.

    Args:
        cadena (str): La cadena GS1 que comienza con el prefijo "17" seguido de una fecha de caducidad.
        resultado (dict): Diccionario que almacena el estado actual del procesamiento, incluyendo errores, observaciones y AIs procesados.
        lista_patrones (list): Lista de AIs pendientes por procesar en el GS1 Datamatrix.

    Returns:
        tuple: Una tupla con tres elementos:
            - dict: Diccionario actualizado con la fecha de caducidad procesada y cualquier error u observación.
            - str: La cadena restante después de eliminar el prefijo procesado.
            - list: Lista de patrones actualizada, sin el AI "17".

    Comportamiento:
        1. Verifica si la cadena tiene al menos 8 caracteres.
        2. Comprueba si los 6 caracteres siguientes al prefijo "17" son dígitos.
        3. Valida si la fecha encontrada es correcta en formato YYMMDD:
            - Si es válida, añade la fecha al diccionario `resultado` en el atributo "FechaCaducidad".
            - Si no es válida, registra un error en el campo "error" y agrega una observación.
        4. Actualiza la cadena eliminando los primeros 8 caracteres procesados.
        5. Remueve el AI "17" de la lista de patrones para evitar procesarlo de nuevo.
    '''
    ai = "17"
    diccionario = resultado.copy()  # Se copia el diccionario para evitar modificaciones accidentales
    if len(cadena) < 8:
        # La cadena no contiene suficiente información para procesar una fecha
        diccionario["error"] = True
        diccionario["observaciones"].append("El Datamatrix no tiene una fecha de caducidad válida.")
        return diccionario, cadena, lista_patrones

    # Extraer la supuesta fecha de caducidad en los 6 caracteres después de "17"
    fecha_candidata = cadena[2:8]
    if not fecha_candidata.isdigit():
        # La fecha tiene un formato incorrecto
        diccionario["error"] = True
        diccionario["observaciones"].append(f"El Datamatrix no tiene una fecha de caducidad válida. Hemos encontrado {fecha_candidata}")
        return diccionario, cadena, lista_patrones

    # Validar si la fecha es válida
    if es_fecha_valida(cadena=fecha_candidata):
        # Es una fecha válida, se agrega al diccionario
        fecha = get_fecha(cadena=fecha_candidata)
        diccionario[ai] = fecha_candidata
        diccionario["FechaCaducidad"] = fecha
        diccionario["ais"].append(ai)
        print(f"Fecha de caducidad encontrada: {fecha}")
    else:
        # Fecha no válida
        diccionario["error"] = True
        diccionario["observaciones"].append(f"El Datamatrix no tiene una fecha de caducidad válida. Hemos encontrado {fecha_candidata}")

    # Eliminar el prefijo procesado de la cadena
    cadena = eliminar_prefijo(cadena=cadena, prefijo=cadena[:8])

    # Eliminar el AI "17" de la lista de patrones
    lista_patrones = eliminar_si_existe(lista=lista_patrones, elemento=ai)

    return diccionario, cadena, lista_patrones

def proceso_ai_10(cadena, resultado, lista_ai):
    """
    Procesa el AI "10" (número de lote) en la cadena GS1.

    Args:
        cadena (str): La cadena a procesar.
        resultado (dict): Diccionario actual del resultado.
        lista_ai (list): Lista de patrones de AI restantes.

    Returns:
        tuple: Diccionario de resultado actualizado, cadena restante, lista de AIs actualizada.
    """
    ai = "10"
    diccionario = resultado.copy()  # Se copia el diccionario para evitar modificaciones accidentales
    print("Procesando lote...")
    lote = cadena[2:].split()[0]  # Extraer el lote hasta el primer separador (puedes ajustar esta lógica)
    diccionario["Lote"] = lote
    diccionario[ai] = lote
    diccionario["ais"].append(ai)
    print(f"Lote encontrado: {lote}")
    cadena = eliminar_prefijo(cadena=cadena, prefijo=cadena[:len(lote) + len(ai)])
    lista_ai = eliminar_si_existe(lista=lista_ai, elemento=ai)
    return diccionario, cadena, lista_ai

def proceso_ai_21(cadena, resultado, lista_ai):
    """
    Procesa el AI "21" (número de serie) en la cadena GS1.

    Args:
        cadena (str): La cadena a procesar.
        resultado (dict): Diccionario actual del resultado.
        lista_ai (list): Lista de patrones de AI restantes.

    Returns:
        tuple: Diccionario de resultado actualizado, cadena restante, lista de AIs actualizada.
    """
    ai = "21"
    diccionario = resultado.copy()  # Se copia el diccionario para evitar modificaciones accidentales
    print("Procesando Número de serie...")
    NumeroSerie = cadena[2:].split()[0]  # Extraer el NumeroSerie hasta el primer separador (puedes ajustar esta lógica)
    diccionario["NumeroSerie"] = NumeroSerie
    diccionario[ai] = NumeroSerie
    diccionario["ais"].append(ai)
    print(f"Serie encontrado: {NumeroSerie}")
    cadena = eliminar_prefijo(cadena=cadena, prefijo=cadena[:len(NumeroSerie) + len(ai)])
    lista_ai = eliminar_si_existe(lista=lista_ai, elemento=ai)
    return diccionario, cadena, lista_ai

def proceso_ai_01(cadena, resultado, lista_patrones):
    """
    Procesa una cadena que comienza por el identificador AI "01" (GTIN) y valida que contenga 14 dígitos.
    Si cumple con la estructura, descompone el GTIN en las claves 'Estructura', 'Empresa', 'Articulo' y 'DigitoControl'.

    Args:
        cadena (str): Cadena de texto que contiene el AI "01" seguido de un GTIN de 14 dígitos.
        resultado (dict): Diccionario donde se guarda el resultado del procesamiento.
        lista_patrones (list): Lista de patrones de AI aún pendientes por procesar.

    Returns:
        tuple: Contiene tres elementos:
            - `diccionario` (dict): Diccionario de resultados actualizado con los datos del GTIN.
            - `cadena` (str): Cadena restante tras eliminar el GTIN procesado.
            - `lista_patrones` (list): Lista de patrones actualizada sin el AI "01".
    """
    ai = "01"
    diccionario = resultado.copy()

    # Verificar que haya al menos 16 caracteres (2 del AI "01" + 14 del GTIN)
    if len(cadena) < 16 or not cadena[2:16].isdigit():
        # Error si la cadena no tiene los 14 dígitos requeridos
        diccionario["error"] = True
        diccionario["observaciones"].append(f"El patrón '01' no tiene un GTIN válido. Cadena encontrada: {cadena[:16]}")
    else:
        # Extraer los 14 dígitos después del "01"
        gtin = cadena[2:16]
        
        # Descomponer el GTIN en las partes específicas
        diccionario[ai] = gtin
        diccionario["GTIN"] = {
            "Estructura": gtin[0],           # Primer carácter
            "Empresa": gtin[1:7],           # Siguientes 6 caracteres
            "Articulo": gtin[7:13],         # Otros 6 caracteres
            "DigitoControl": gtin[-1]       # Último carácter
        }
        if int(gtin[-1]) != calcular_digito_control_EAN13(cadena=gtin[1:13]):
            resultado["observaciones"].append(f"El código EAN13 {gtin} no tiene el dígito de control ({gtin[-1]}) bien calculado. Su dígito de control debe de ser ({calcular_digito_control_EAN13(cadena=gtin[1:13])}).")

        if gtin[1:7] == "847000":
            diccionario["RegistroSanitario"] = gtin[7:13]
        diccionario["ais"].append(ai)  # Añadir el AI procesado a la lista de identificadores
        print(f"GTIN encontrado y descompuesto: {diccionario['GTIN']}")

    # Eliminar el prefijo procesado (AI "01" + los 14 dígitos del GTIN)
    cadena = eliminar_prefijo(cadena=cadena, prefijo=cadena[:16])
    
    # Eliminar el patrón "01" de la lista de patrones
    lista_patrones = eliminar_si_existe(lista=lista_patrones, elemento=ai)

    return diccionario, cadena, lista_patrones

def proceso_ai_712(cadena, resultado, lista_ai):
    """
    Procesa el AI "712" (Spanish Code) en la cadena GS1.

    Args:
        cadena (str): La cadena a procesar.
        resultado (dict): Diccionario actual del resultado.
        lista_ai (list): Lista de patrones de AI restantes.

    Returns:
        tuple: Diccionario de resultado actualizado, cadena restante, lista de AIs actualizada.
    """
    ai = "712"
    diccionario = resultado.copy()  # Se copia el diccionario para evitar modificaciones accidentales
    print("Procesando Spanish NHRN Code (número de reembolso)...")
    NHRN = cadena[3:].split()[0]  # Extraer el NumeroSerie hasta el primer separador (puedes ajustar esta lógica)
    diccionario[ai] = NHRN
    diccionario["observaciones"].append(f"Spanish CN (NHRN) encontrado {NHRN}. Buscar como procesar este dato.")
    diccionario["ais"].append(ai)
    print(f"Spanish NHRN: {NHRN}")
    # Añado mi lógica para este caso.
    # Hemos visto que fabricantes envían 7 dígitos y otros 6 dígitos, no incluyendo el dígito de control
    if NHRN.isdigit() and len(NHRN) == 6:
        #Debo calcular el dígito de control
        diccionario["NTIN"] = {
            "Empresa" : "847000",
            "Articulo" : NHRN,
            "DigitoControl" : calcular_digito_control_EAN13(cadena="847000" + NHRN)
        }
        # Si "RegistroSanitario" no está en el diccionario, lo añadimos
        if "RegistroSanitario" not in diccionario:
            diccionario["RegistroSanitario"] = NHRN
            print(f"RegistroSanitario añadido: {NHRN}")    

    if NHRN.isdigit() and len(NHRN) == 7:
        # Debo verificar el dígito de control y poner una observacion si no coincide
        diccionario["NTIN"] = {
            "Empresa" : "847000",
            "Articulo" : NHRN[0:6],
            "DigitoControl" : NHRN[-1]
        }
        if int(NHRN[-1]) != calcular_digito_control_EAN13(cadena="847000" + NHRN[0:6]):
            diccionario["observaciones"].append(f"El código NTIN simplificado {NHRN} no tiene el dígito de control ({NHRN[-1]}) bien calculado. Su dígito de control debe de ser ({calcular_digito_control_EAN13(cadena="847000" + NHRN[0:6])}).")
        
        # Si "RegistroSanitario" no está en el diccionario, lo añadimos
        if "RegistroSanitario" not in diccionario:
            diccionario["RegistroSanitario"] = NHRN[:6]
            print(f"RegistroSanitario añadido: {NHRN[:6]}")

    print(f"NTIN encontrado: {diccionario['NTIN']}")
    cadena = eliminar_prefijo(cadena=cadena, prefijo=cadena[:len(NHRN) + len(ai)])
    lista_ai = eliminar_si_existe(lista=lista_ai, elemento=ai)
    return diccionario, cadena, lista_ai

def proceso_ai_710(cadena, resultado, lista_ai):
    """
    Procesa el AI "710" (Germany Code) en la cadena GS1.

    Args:
        cadena (str): La cadena a procesar.
        resultado (dict): Diccionario actual del resultado.
        lista_ai (list): Lista de patrones de AI restantes.

    Returns:
        tuple: Diccionario de resultado actualizado, cadena restante, lista de AIs actualizada.
    """
    ai = "710"
    diccionario = resultado.copy()  # Se copia el diccionario para evitar modificaciones accidentales
    print("Procesando Germany NHRN Code (número de reembolso)...")
    NHRN = cadena[3:].split()[0]  # Extraer el NumeroSerie hasta el primer separador (puedes ajustar esta lógica)
    diccionario[ai] = NHRN
    diccionario["ais"].append(ai)
    diccionario["observaciones"].append(f"Germany PZN (NHRN) encontrado {NHRN}. Buscar como procesar este dato.")
    print(f"Germany (PZN) NHRN: {NHRN}")
    cadena = eliminar_prefijo(cadena=cadena, prefijo=cadena[:len(NHRN) + len(ai)])
    lista_ai = eliminar_si_existe(lista=lista_ai, elemento=ai)
    return diccionario, cadena, lista_ai    

def proceso_ai_711(cadena, resultado, lista_ai):
    """
    Procesa el AI "711" (French Code) en la cadena GS1.

    Args:
        cadena (str): La cadena a procesar.
        resultado (dict): Diccionario actual del resultado.
        lista_ai (list): Lista de patrones de AI restantes.

    Returns:
        tuple: Diccionario de resultado actualizado, cadena restante, lista de AIs actualizada.
    """
    ai = "711"
    diccionario = resultado.copy()  # Se copia el diccionario para evitar modificaciones accidentales
    print("Procesando French NHRN Code (número de reembolso)...")
    NHRN = cadena[3:].split()[0]  # Extraer el NumeroSerie hasta el primer separador (puedes ajustar esta lógica)
    diccionario[ai] = NHRN
    diccionario["ais"].append(ai)
    diccionario["observaciones"].append(f"French CIP (NHRN) encontrado {NHRN}. Buscar como procesar este dato.")
    print(f"French (CIP) NHRN: {NHRN}")
    cadena = eliminar_prefijo(cadena=cadena, prefijo=cadena[:len(NHRN) + len(ai)])
    lista_ai = eliminar_si_existe(lista=lista_ai, elemento=ai)
    return diccionario, cadena, lista_ai        

def proceso_ai_713(cadena, resultado, lista_ai):
    """
    Procesa el AI "713" (Brasilian Code) en la cadena GS1.

    Args:
        cadena (str): La cadena a procesar.
        resultado (dict): Diccionario actual del resultado.
        lista_ai (list): Lista de patrones de AI restantes.

    Returns:
        tuple: Diccionario de resultado actualizado, cadena restante, lista de AIs actualizada.
    """
    ai = "713"
    diccionario = resultado.copy()  # Se copia el diccionario para evitar modificaciones accidentales
    print("Procesando Brazilian NHRN Code (número de reembolso)...")
    NHRN = cadena[3:].split()[0]  # Extraer el NumeroSerie hasta el primer separador (puedes ajustar esta lógica)
    diccionario[ai] = NHRN
    diccionario["ais"].append(ai)
    diccionario["observaciones"].append(f"Brazilian DRN (NHRN) encontrado {NHRN}. Buscar como procesar este dato.")
    print(f"Brazilian (DRN) NHRN: {NHRN}")
    cadena = eliminar_prefijo(cadena=cadena, prefijo=cadena[:len(NHRN) + len(ai)])
    lista_ai = eliminar_si_existe(lista=lista_ai, elemento=ai)
    return diccionario, cadena, lista_ai            

def proceso_ai_714(cadena, resultado, lista_ai):
    """
    Procesa el AI "714" (Portugal Code) en la cadena GS1.

    Args:
        cadena (str): La cadena a procesar.
        resultado (dict): Diccionario actual del resultado.
        lista_ai (list): Lista de patrones de AI restantes.

    Returns:
        tuple: Diccionario de resultado actualizado, cadena restante, lista de AIs actualizada.
    """
    ai = "714"
    diccionario = resultado.copy()  # Se copia el diccionario para evitar modificaciones accidentales
    print("Procesando Portugal NHRN Code (número de reembolso)...")
    NHRN = cadena[3:].split()[0]  # Extraer el NumeroSerie hasta el primer separador (puedes ajustar esta lógica)
    diccionario[ai] = NHRN
    diccionario["ais"].append(ai)
    diccionario["observaciones"].append(f"Portugal AIM (NHRN) encontrado {NHRN}. Buscar como procesar este dato.")
    print(f"Portugal (AIM) NHRN: {NHRN}")
    cadena = eliminar_prefijo(cadena=cadena, prefijo=cadena[:len(NHRN) + len(ai)])
    lista_ai = eliminar_si_existe(lista=lista_ai, elemento=ai)
    return diccionario, cadena, lista_ai                

def proceso_ai_715(cadena, resultado, lista_ai):
    """
    Procesa el AI "715" (USA Code) en la cadena GS1.

    Args:
        cadena (str): La cadena a procesar.
        resultado (dict): Diccionario actual del resultado.
        lista_ai (list): Lista de patrones de AI restantes.

    Returns:
        tuple: Diccionario de resultado actualizado, cadena restante, lista de AIs actualizada.
    """
    ai = "715"
    diccionario = resultado.copy()  # Se copia el diccionario para evitar modificaciones accidentales
    print("Procesando USA NHRN Code (número de reembolso)...")
    NHRN = cadena[3:].split()[0]  # Extraer el NumeroSerie hasta el primer separador (puedes ajustar esta lógica)
    diccionario[ai] = NHRN
    diccionario["ais"].append(ai)
    diccionario["observaciones"].append(f"USA NDC (NHRN) encontrado {NHRN}. Buscar como procesar este dato.")
    print(f"USA (NDC) NHRN: {NHRN}")
    cadena = eliminar_prefijo(cadena=cadena, prefijo=cadena[:len(NHRN) + len(ai)])
    lista_ai = eliminar_si_existe(lista=lista_ai, elemento=ai)
    return diccionario, cadena, lista_ai                    

def proceso_ai_716(cadena, resultado, lista_ai):
    """
    Procesa el AI "716" (Italy Code) en la cadena GS1.

    Args:
        cadena (str): La cadena a procesar.
        resultado (dict): Diccionario actual del resultado.
        lista_ai (list): Lista de patrones de AI restantes.

    Returns:
        tuple: Diccionario de resultado actualizado, cadena restante, lista de AIs actualizada.
    """
    ai = "716"
    diccionario = resultado.copy()  # Se copia el diccionario para evitar modificaciones accidentales
    print("Procesando Italy NHRN Code (número de reembolso)...")
    NHRN = cadena[3:].split()[0]  # Extraer el NumeroSerie hasta el primer separador (puedes ajustar esta lógica)
    diccionario[ai] = NHRN
    diccionario["ais"].append(ai)
    diccionario["observaciones"].append(f"Italy AIC (NHRN) encontrado {NHRN}. Buscar como procesar este dato.")
    print(f"Italy (AIC) NHRN: {NHRN}")
    cadena = eliminar_prefijo(cadena=cadena, prefijo=cadena[:len(NHRN) + len(ai)])
    lista_ai = eliminar_si_existe(lista=lista_ai, elemento=ai)
    return diccionario, cadena, lista_ai                        

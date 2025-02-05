from module.lib_json import obtener_application_identifiers, eliminar_si_existe, buscar_ai_en_codigos
from module.lib_string import existe_separador, dividir_cadena, encontrar_patron
from module.lib_EAN import calcular_digito_control_EAN13
import module.lib_procesadores as procesadores

def procesar_codigo_gs1(cadena, parametros_gs1):
    """
    Procesa un código GS1 (como un DataMatrix o un código de barras) y extrae información relevante.

    Args:
        cadena (str): El código GS1 a procesar.
        parametros_gs1 (dict): Diccionario con parámetros de configuración, que incluye:
            - "FNC1List" (list, opcional): Lista de separadores FNC1 posibles. Si no está presente, se usará chr(29) por defecto.
            - "applicationIdentifiers" (list): Lista de identificadores de aplicación (AIs) y sus especificaciones.

    Returns:
        dict: Diccionario con los resultados del procesamiento. Incluye las siguientes claves:
            - "datamatrix" (str): El código GS1 original procesado.
            - "error" (bool): Indica si hubo un error en el procesamiento.
            - "observaciones" (list): Lista de observaciones o advertencias generadas durante el procesamiento.
            - "ais" (list): Lista de identificadores de aplicación (AIs) procesados.
            - "version" (str): La fecha de la última modificación de las especificaciones, si está disponible.
            - "EAN13" (str, opcional): El código EAN13 extraído, si aplica.
            - "GTIN" (dict, opcional): Información desglosada del código GTIN, si aplica.
            - "RegistroSanitario" (str, opcional): Código de registro sanitario, si aplica.

    Observaciones:
        - Si no se encuentra la clave `dc:lastModified` en los parámetros, la versión se establece en "2025-01-01".
        - Si el separador FNC1 no es estándar, se genera una observación y se utiliza chr(29) por defecto.
        - Valida que los códigos contengan la información mínima requerida, como fecha de caducidad y lote.

    Raises:
        KeyError: Si el parámetro `parametros_gs1` no incluye la clave "applicationIdentifiers".
    """
    # Obtener lista de separadores FNC1, usar chr(29) por defecto si no está presente
    lista_FNC1_posibles = parametros_gs1.get("FNC1List", [chr(29)])
    ES_FNC1, FNC1 = existe_separador(cadena=cadena, separadores=lista_FNC1_posibles)

    # Obtener lista de application identifiers
    lista_ai = obtener_application_identifiers(parametros_gs1)
    lista_ai_usadas = []

    # Inicializar el resultado
    resultado = {
        "datamatrix": cadena,
        "error": False,
        "observaciones": [],
        "ais": []
    }

    # Extraer la versión del parámetro `parametros_gs1`
    try:
        # Obtener el primer elemento de la lista `applicationIdentifiers` y su clave `dc:lastModified`
        version = parametros_gs1["applicationIdentifiers"][0].get("dc:lastModified", {}).get("@value", "2025-01-01")
    except (KeyError, IndexError, AttributeError):
        version = "2025-01-01"  # Valor predeterminado si no se encuentra la clave

    # Añadir la versión al resultado
    resultado["version"] = version

    # Verificar si el separador FNC1 es estándar
    if FNC1 != chr(29):
        separador_mostrado = "espacio en blanco" if FNC1 == " " else repr(FNC1)
        resultado["observaciones"].append(f"El carácter separador FNC1 no es el estándar y se ha cambiado a {separador_mostrado}.")

    # Validaciones iniciales de la cadena
    if len(cadena) < 28:
        resultado["error"] = True
        resultado["observaciones"].append(f"El datamatrix no cumple con tener fecha de caducidad y lote. Por favor revisa el código.")
    if len(cadena) == 13 and cadena.isdigit():
        resultado["EAN13"] = cadena
        resultado["GTIN"] = {
            "Empresa": cadena[0:6],
            "Articulo": cadena[6:12],
            "DigitoControl": cadena[12]
        }
        DigitoControlCalculado = calcular_digito_control_EAN13(cadena=cadena[0:12])
        if int(cadena[12]) != DigitoControlCalculado:
            resultado["observaciones"].append(f"El código EAN13 {cadena} no tiene el dígito de control ({cadena[12]}) bien calculado. Su dígito de control debe de ser ({DigitoControlCalculado}).")
        if cadena[0:6] == "847000":
            resultado["RegistroSanitario"] = cadena[6:12]

    # Dividir la cadena usando el separador FNC1
    lista_palabras = dividir_cadena(cadena=cadena, separador=FNC1)
    for palabra in lista_palabras:
        palabra_original = palabra
        while palabra:
            ai = encontrar_patron(cadena=palabra, lista_patrones=lista_ai)
            if not ai:
                break
            # Procesar el AI utilizando funciones específicas
            nombre_funcion = f"proceso_ai_{ai}"
            if hasattr(procesadores, nombre_funcion):
                funcion_procesar = getattr(procesadores, nombre_funcion)
                resultado, palabra, lista_ai = funcion_procesar(palabra, resultado, lista_ai)
                lista_ai_usadas.append(ai)
            else:
                especificacion_ai = buscar_ai_en_codigos(ai=ai, codigos_ai=parametros_gs1)
                lista_ai = eliminar_si_existe(lista=lista_ai, elemento=ai)
        if palabra != "":
            resultado["observaciones"].append(f"No he conseguido procesar todo el contenido que queda {palabra} de {palabra_original}")

    return resultado

CREATE OR REPLACE FUNCTION dividir_cadena(p_str IN VARCHAR2, p_delim IN VARCHAR2) 
RETURN SYS.ODCIVARCHAR2LIST
IS
    l_result SYS.ODCIVARCHAR2LIST := SYS.ODCIVARCHAR2LIST();
    l_temp VARCHAR2(4000);
BEGIN
	/*
	 * Dada una cadena de texto, devuelve una lista obtenida al dividir la cadena con el separador.
    
    Si el separador no se encuentra en la cadena o si el separador es None, devuelve una lista con un solo elemento, que es la cadena completa.
    
    Args:
    p_str (str): La cadena de texto que se desea dividir.
    p_delim (str or None): El separador que se usará para dividir la cadena. Si es None, la cadena no se divide y se devuelve como único elemento.
    
    Returns:
    list: Una lista de subcadenas divididas por el separador. 
          Si el separador no se encuentra o es None, la lista contiene la cadena original como único elemento.

	 */
    FOR i IN 1..LENGTH(p_str) - LENGTH(REPLACE(p_str, p_delim, '')) + 1 LOOP
        l_temp := REGEXP_SUBSTR(p_str, '[^' || p_delim || ']+', 1, i);
        l_result.EXTEND;
        l_result(i) := l_temp;
    END LOOP;
    RETURN l_result;
END;

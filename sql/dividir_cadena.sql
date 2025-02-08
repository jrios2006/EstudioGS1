CREATE OR REPLACE FUNCTION dividir_cadena(p_str IN VARCHAR2, p_delim IN VARCHAR2) 
RETURN SYS.ODCIVARCHAR2LIST
IS
    l_result SYS.ODCIVARCHAR2LIST := SYS.ODCIVARCHAR2LIST();
    l_temp VARCHAR2(4000);
    l_pos NUMBER;
    l_str VARCHAR2(4000) := p_str; -- Copia local de la cadena de entrada
BEGIN
    /*
     * Dada una cadena de texto, devuelve una lista obtenida al dividir la cadena con el separador.
     *
     * Si el separador no se encuentra en la cadena o si el separador es NULL, devuelve una lista con un solo elemento, que es la cadena completa.
     *
     * Args:
     * p_str (str): La cadena de texto que se desea dividir.
     * p_delim (str): El separador que se usará para dividir la cadena.
     *
     * Returns:
     * SYS.ODCIVARCHAR2LIST: Una lista de subcadenas divididas por el separador.
     *                       Si el separador no se encuentra, la lista contiene la cadena original como único elemento.
     */

    IF p_delim IS NULL OR p_delim = '' THEN
        -- Si el delimitador está vacío o es NULL, devolvemos la cadena completa como único elemento
        l_result.EXTEND;
        l_result(1) := p_str;
        RETURN l_result;
    END IF;

    LOOP
        -- Encontrar la posición del primer delimitador en la cadena restante
        l_pos := INSTR(l_str, p_delim);
        
        IF l_pos > 0 THEN
            -- Extraer la parte antes del delimitador
            l_temp := SUBSTR(l_str, 1, l_pos - 1);
            l_result.EXTEND;
            l_result(l_result.COUNT) := l_temp;
            
            -- Actualizar la cadena restante excluyendo el delimitador encontrado
            l_str := SUBSTR(l_str, l_pos + LENGTH(p_delim));
        ELSE
            -- Agregar la parte final de la cadena y salir del bucle
            l_result.EXTEND;
            l_result(l_result.COUNT) := l_str;
            EXIT;
        END IF;
    END LOOP;

    -- Si la cadena termina en un delimitador y el último token no es vacío, agregar un elemento vacío
    IF SUBSTR(p_str, -LENGTH(p_delim)) = p_delim AND l_result(l_result.COUNT) IS NOT NULL THEN
        l_result.EXTEND;
        l_result(l_result.COUNT) := '';
    END IF;

    RETURN l_result;
END;

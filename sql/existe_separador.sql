CREATE OR REPLACE FUNCTION convertir_separadores_hex (
    separadores IN SYS.ODCIVARCHAR2LIST -- Recibe una lista de separadores a convertir
) RETURN SYS.ODCIVARCHAR2LIST IS
    /*
     * Dada una lista de separadores, convierte los separadores que están en formato hexadecimal (\xNN)
     * a su correspondiente carácter usando la función CHR().
     *
     * Si algún separador contiene la cadena '\x1D', será reemplazado por el carácter correspondiente a CHR(29).
     * Si el separador no está en formato hexadecimal, simplemente se mantiene tal cual.
     *
     * Args:
     * separadores (SYS.ODCIVARCHAR2LIST): Una lista de separadores que puede contener caracteres en formato hexadecimal
     *                                      (por ejemplo, '\x1D') o caracteres literales.
     *
     * Returns:
     * SYS.ODCIVARCHAR2LIST: La lista de separadores con los caracteres hexadecimales convertidos a su valor correspondiente.
     *                        Los separadores no hexadecimales se mantienen sin cambios.
     */

    separadores_convertidos SYS.ODCIVARCHAR2LIST := SYS.ODCIVARCHAR2LIST(); -- Lista para almacenar los separadores convertidos

BEGIN
    -- Iterar sobre cada separador en la lista recibida
    FOR i IN 1 .. separadores.COUNT LOOP
        -- Verificar si el separador contiene un valor hexadecimal (por ejemplo, '\x1D')
        IF INSTR(separadores(i), '\x') > 0 THEN
            -- Si es hexadecimal, convertirlo a su valor correspondiente usando CHR
            separadores_convertidos.EXTEND; -- Agregar espacio para un nuevo elemento en la lista
            separadores_convertidos(separadores_convertidos.COUNT) := REPLACE(separadores(i), '\x1D', CHR(29)); -- Reemplazar \x1D por CHR(29)
        ELSE
            -- Si no es hexadecimal, mantener el separador tal cual
            separadores_convertidos.EXTEND; -- Agregar espacio para un nuevo elemento en la lista
            separadores_convertidos(separadores_convertidos.COUNT) := separadores(i); -- Mantener el separador sin cambios
        END IF;
    END LOOP;

    -- Retornar la lista de separadores convertidos
    RETURN separadores_convertidos;
END;



CREATE OR REPLACE FUNCTION existe_separador (
    cadena IN VARCHAR2,
    separadores_json IN CLOB -- Recibir los separadores como JSON
) RETURN VARCHAR2 IS
    /*
     * Dada una cadena de texto y una lista de separadores en formato JSON, devuelve el primer separador encontrado en la cadena.
     *
     * Si la cadena contiene al menos uno de los separadores, la función devuelve el primer separador que se encuentra.
     * Si no se encuentra ningún separador en la cadena, la función devuelve NULL.
     *
     * El parámetro 'separadores_json' debe ser una cadena en formato JSON que contenga una lista de posibles separadores.
     * La lista de separadores se puede representar como una cadena JSON con elementos como: '["\\x1D", "|", "^", "#", " ", "(SEPARADOR)"]'.
     *
     * Args:
     * cadena (VARCHAR2): La cadena de texto en la que se buscarán los separadores.
     * separadores_json (CLOB): Una cadena en formato JSON que contiene una lista de separadores a verificar en la cadena.
     *
     * Returns:
     * VARCHAR2: El primer separador encontrado en la cadena. Si no se encuentra ninguno, devuelve NULL.
     *           Si la cadena contiene varios separadores, se devuelve el primero que aparece en el orden especificado en el JSON.
     *           Si no hay separadores, la función devuelve NULL.
     */

    -- Variables para almacenar los separadores convertidos y el separador encontrado
    separadores SYS.ODCIVARCHAR2LIST := SYS.ODCIVARCHAR2LIST();
    separador_encontrado VARCHAR2(100) := NULL;
BEGIN
    -- Convertir el JSON a una lista de separadores
    BEGIN
        SELECT CAST(COLLECT(VALUE) AS SYS.ODCIVARCHAR2LIST)
        INTO separadores
        FROM JSON_TABLE(
            separadores_json,
            '$[*]' COLUMNS (VALUE VARCHAR2(100) PATH '$')
        );
    EXCEPTION
        WHEN OTHERS THEN
            -- Si el JSON no es válido, retornamos NULL
            RETURN NULL;
    END;

    -- Convertir los separadores hexadecimales a caracteres reales (por ejemplo, \x1D -> CHR(29))
    separadores := convertir_separadores_hex(separadores);

    -- Iterar sobre los separadores para verificar si están en la cadena
    FOR i IN 1 .. separadores.COUNT LOOP
        IF INSTR(cadena, separadores(i)) > 0 THEN
            -- Si se encuentra un separador, lo asignamos a 'separador_encontrado' y salimos del bucle
            separador_encontrado := separadores(i);
            EXIT; -- Salir del bucle al encontrar el primer separador
        END IF;
    END LOOP;

    -- Devolver el separador encontrado, o NULL si no se encontró ninguno
    RETURN separador_encontrado;
END;

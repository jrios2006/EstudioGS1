/* SQL para obtener las filas de los posibles ai definidos en el estándar gs1 */
SELECT DISTINCT t.applicationIdentifier
FROM ESPECIFICACIONES_JSON e,
     JSON_TABLE(
         e.json_doc,
         '$.applicationIdentifiers[*]'
         COLUMNS (
             applicationIdentifier VARCHAR2(50) PATH '$.applicationIdentifier'
         )
     ) t
WHERE 
    e.descripcion = 'GS1'
    AND t.applicationIdentifier IS NOT NULL
ORDER BY 1 ASC;

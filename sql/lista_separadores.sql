/* Consulta para obtner la lista de los separadores no como lista sino como registros*/
SELECT 
    fnc1_list.VALUE AS separador
FROM 
    ESPECIFICACIONES_JSON,
    JSON_TABLE(
        json_doc, 
        '$.FNC1List[*]' COLUMNS (
            VALUE VARCHAR2(100) PATH '$'
        )
    ) fnc1_list
WHERE 
	DESCRIPCION = 'GS1';

## Ejemplo de uso en Oracle 19c

Podemos intentar configurar Oracle 19c para usar protocolos HTTP y que sea python el que resuelva directamente el parseo de un código.

Para poder hacer esto necesitamos que un Administrador Oracle permita las conexiones HTTP dentro del código Oracle

1. Acceso a Oracle con SYS
2. Conocer si el servidor Oracle ya tiene permisos
3. Dar permisos al usuario de Oracle que va a realizar la petición
4. Verificar la seguridad de la conexión si se hace una petción externa (SSL)
5. Habilitar un servidor http que tenga acceso la petición

### Configurar Oracle para dar permisos de uso del módulo UTL_HTTP

Como SYS en el servidor debemos de verificar los usuarios de base de datos que queremos que tengan acceso.

Me centro en uno

```sql
/* Obtener el listado de los usuarios a los que debo de dar acceso */
SELECT username FROM dba_users 
;
```
Con el resultado de esta consulta eligo el usuario con el que quiero dar acceso

#### ACL
Debo de revisar con esta consulta si hay alguna lista de control de acceso ya configurada con el nombre que voy a utilizar
```sql
SELECT acl, host, lower_port, upper_port FROM dba_network_acls WHERE ACL LIKE '%networ%';
;
```
Si la hubiera es posible que ya esté configurado y si no vamos a crear una ACL con el nombre network_acl.xml

Una vez creada deberemos de var algo como esto

|ACL|HOST|LOWER_PORT|UPPER_PORT|
|---|----|----------|----------|
|/sys/acls/network_acl.xml|*|||

Esto permite al tener un * capacidad de Oracle de hacer petición a cualquier host.

**Es posible que esto no sea así y se puede restriguir a host o endpoint**

Nos debemos de fijar en la sección principal que es el dato que debemos de cambiar

```sql
BEGIN
    DBMS_NETWORK_ACL_ADMIN.create_acl(
        acl         => 'network_acl.xml',
        description => 'Permitir acceso HTTP/HTTPS',
        principal   => 'USER_DB',
        is_grant    => TRUE,
        privilege   => 'connect'
    );

    -- Agregar privilegio de resolución de nombre de dominio (DNS)
    DBMS_NETWORK_ACL_ADMIN.add_privilege(
        acl        => 'network_acl.xml',
        principal  => 'USER_DB',
        is_grant   => TRUE,
        privilege  => 'resolve'
    );

    -- Asignar esta ACL a todos los hosts o a un dominio específico
    DBMS_NETWORK_ACL_ADMIN.assign_acl(
        acl  => 'network_acl.xml',
        host => '*'
    );
END;
```

Si somos capaces de ejecutar esto estaráimos dando acceso al usuario USER_DB acceso a realizar peticioens http a cualquier host y a cualquier endpoint publicado en esos host

Debemos de verificar que su uso al usuario es correcto mediante esta consulta

```sql
SELECT * FROM dba_network_acl_privileges WHERE principal = 'USER_DB';
```

Su resultado será

|ACL|ACLID|PRINCIPAL|PRIVILEGE|IS_GRANT|INVERT|START_DATE|END_DATE|ACL_OWNER|
|---|-----|---------|---------|--------|------|----------|--------|---------|
|/sys/acls/network_acl.xml|\u0000\u0000\u0000\u0000�\u0000'e|USER_DB|resolve|true|false|||SYS|
|/sys/acls/network_acl.xml|\u0000\u0000\u0000\u0000�\u0000'e|USER_DB|connect|true|false|||SYS|

Una vez hecho esto con SYS, debemos de ver como trabajar con SSL si procede.

#### SSL

A completar

#### Ejemplo de uso

Vamos a definir una función con el usuario para que se pueda usar a modo de ejemplo. No vamos a tener en cuenta los certificados SSL y ajustaremos las restricciones que nos vamos encontrando

En una máquina accesible de sde Oracle vamos a levantar un servidor HTTP con python con un método y ese método lo vamos a llamar desde la función de oracle

Cosas que hemos visto es:

1. La codificación de los caracteers suele ser distinta entre el servidor HTTP de python y el servidor de Oracle
2. Vamos a usar el método get con un solo parámetros querystring (codigo)
3. El valo de ese parámetro cofigo debemos tener encuenta las limitaciones de envío de caracteres estraños como blanco o CHAR(29). Usaremos un reemplazo por (SEPARADOR) para eviar estos inconvenientes.
4. El servidor web enviará el resultado o no dependiendo de lo que esté operativo
5. Si no es accesible fallará por un timeout
6. Si enviamos mal el querystring dará un 400 y no tendremos el valor esperado

Ejemplo de uso cuando todo estça montado:

Sabiendo que alguien a publicado en endpoint en uan Ip y un puerto qye que no usa SSL, sabremos la URL de petición

**http://192.168.132.130:5000/parse_datamatrix?codigo=**

Esto se levantará con fastapi o flask con el código python publicado (hay otro manual de como hacer esto)

El código de la función Oracle es
```sql
CREATE OR REPLACE FUNCTION call_http_get_ejemplo(codigo IN VARCHAR2) RETURN CLOB IS
    req   UTL_HTTP.req;
    resp  UTL_HTTP.resp;
    url   VARCHAR2(4000);
    buffer CLOB;
    chunk VARCHAR2(32767);
    charset VARCHAR2(30);
	codigo_modificado VARCHAR2(4000);
BEGIN
    -- Ignorar la validación de certificados SSL
    UTL_HTTP.set_wallet(NULL, NULL);

    -- Obtener el conjunto de caracteres de la base de datos
    SELECT VALUE INTO charset
    FROM NLS_DATABASE_PARAMETERS
    WHERE PARAMETER = 'NLS_CHARACTERSET';
    
	  -- Reemplazar CHR(29) por (SEPARADOR) y los espacios en blanco por (SEPARADOR)
    codigo_modificado := REPLACE(codigo, CHR(29), '(SEPARADOR)');
    codigo_modificado := REPLACE(codigo_modificado, ' ', '(SEPARADOR)');    

    -- Construir la URL dinámica

    url := 'http://192.168.132.130:5000/parse_datamatrix?codigo=' || codigo_modificado ;

    -- Realizar la solicitud GET
    req := UTL_HTTP.begin_request(url, 'GET');
    resp := UTL_HTTP.get_response(req);

    -- Crear un CLOB temporal para almacenar la respuesta
    DBMS_LOB.createtemporary(buffer, TRUE);

    -- Leer la respuesta en un bucle
    LOOP
        BEGIN
            -- Leer un fragmento de la respuesta
            UTL_HTTP.read_text(resp, chunk);
            
            -- Convertir el fragmento de UTF-8 al conjunto de caracteres de la base de datos
            chunk := CONVERT(chunk, charset, 'UTF8');

            -- Agregar el fragmento convertido al CLOB
            DBMS_LOB.writeappend(buffer, LENGTH(chunk), chunk);
        EXCEPTION
            WHEN UTL_HTTP.end_of_body THEN
                -- Salir del bucle al final del cuerpo de la respuesta
                EXIT;
        END;
    END LOOP;

    -- Cerrar la respuesta HTTP
    UTL_HTTP.end_response(resp);

    -- Devolver el contenido como CLOB
    RETURN buffer;
END;
```

Su uso será como el que sigue:

#### Caso 1.

El servidor está operativo y accesible. Enviado una cadena con un separador válido ^

```sql
SELECT call_http_get_ejemplo('010843701315676921A014MFCNMYF5AR^1024C0106B^172703317127062585') AS EJEMPLO1 FROM DUAL;
```

Su resultado es:

|EJEMPLO1|
|--------|
|{
    "codigo": "010843701315676921A014MFCNMYF5AR^1024C0106B^172703317127062585",
    "estado": true,
    "errores": [],
    "resultado": {
        "datamatrix": "010843701315676921A014MFCNMYF5AR^1024C0106B^172703317127062585",
        "error": false,
        "observaciones": [
            "El carácter separador FNC1 no es el estándar y se ha cambiado a '^'.",
            "Spanish CN (NHRN) encontrado 7062585."
        ],
        "ais": [
            "01",
            "21",
            "10",
            "17",
            "712"
        ],
        "version": "2025-01-29",
        "01": "08437013156769",
        "GTIN": {
            "Estructura": "0",
            "Empresa": "843701",
            "Articulo": "315676",
            "DigitoControl": "9"
        },
        "NumeroSerie": "A014MFCNMYF5AR",
        "21": "A014MFCNMYF5AR",
        "Lote": "24C0106B",
        "10": "24C0106B",
        "17": "270331",
        "FechaCaducidad": "2027-03-31T23:59:59.999999",
        "712": "7062585",
        "NTIN": {
            "Empresa": "847000",
            "Articulo": "706258",
            "DigitoControl": "5"
        },
        "RegistroSanitario": "706258"
    },
    "warnings": [],
    "comentarios": "",
    "version_api": "2025-02-03"
}|

Correcto es lo esparado.

Así podremos rescatar los datos que nos interesa mediante la consulta

```sql
SELECT 
    JSON_VALUE(call_http_get_ejemplo('010843701315676921A014MFCNMYF5AR^1024C0106B^172703317127062585'), '$.resultado.Lote') AS Lote,
    JSON_VALUE(call_http_get_ejemplo('010843701315676921A014MFCNMYF5AR^1024C0106B^172703317127062585'), '$.resultado.FechaCaducidad') AS FechaCaducidad,
    JSON_VALUE(call_http_get_ejemplo('010843701315676921A014MFCNMYF5AR^1024C0106B^172703317127062585'), '$.resultado.RegistroSanitario') AS RegistroSanitario
FROM DUAL;
```

Hacemos 3 peticiones http para los valores pero de moento esto no es imporante

Su resultado es

|LOTE|FECHACADUCIDAD|REGISTROSANITARIO|
|----|--------------|-----------------|
|24C0106B|2027-03-31T23:59:59.999999|706258|


Si el código es correcto encontraremos los datos que buscamos de una manera sencilla y usando pl/sql



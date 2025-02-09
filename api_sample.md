## Ejemplo de uso usando fastapi

Necesitamos instalar las dependencias mínimas para fastapi y que se pueda hacer peticiones http

Es un servidor de pruebas sin necesidad de autenticación y sin certificados.

el comando para ejecutar las pruebas es

```
uvicorn api_sample:app --reload --host 0.0.0.0 --port 5000
```

Esto hará que el servidor esté escruchando sobre la Ip local del equipo y en el puerto 5000

## Pruebas con un navegador

```
http://127.0.0.1:5000/parse_datamatrix?codigo=010843701315676921A014MFCNMYF5AR%1d1024C0106B%1d172703317127062585
```

Resultado

```json
{"codigo":"010843701315676921A014MFCNMYF5AR\u001d1024C0106B\u001d172703317127062585","estado":true,"errores":[],"resultado":{"datamatrix":"010843701315676921A014MFCNMYF5AR\u001d1024C0106B\u001d172703317127062585","error":false,"observaciones":["Spanish CN (NHRN) encontrado 7062585."],"ais":["01","21","10","17","712"],"version":"2025-01-29","01":"08437013156769","GTIN":{"Estructura":"0","Empresa":"843701","Articulo":"315676","DigitoControl":"9"},"NumeroSerie":"A014MFCNMYF5AR","21":"A014MFCNMYF5AR","Lote":"24C0106B","10":"24C0106B","17":"270331","FechaCaducidad":"2027-03-31T23:59:59.999999","712":"7062585","NTIN":{"Empresa":"847000","Articulo":"706258","DigitoControl":"5"},"RegistroSanitario":"706258"},"warnings":[],"comentarios":"","version_api":"2025-02-03"}
```

En el servidor podemos leer

```
INFO:     Will watch for changes in these directories: ['/home/jra/Lug/api']
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
INFO:     Started reloader process [36160] using StatReload
INFO:     Started server process [36162]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
GTIN encontrado y descompuesto: {'Estructura': '0', 'Empresa': '843701', 'Articulo': '315676', 'DigitoControl': '9'}
Procesando Número de serie...
Serie encontrado: A014MFCNMYF5AR
Procesando lote...
Lote encontrado: 24C0106B
Fecha de caducidad encontrada: 2027-03-31 23:59:59.999999
Procesando Spanish NHRN Code (número de reembolso)...
Spanish NHRN: 7062585
RegistroSanitario añadido: 706258
NTIN encontrado: {'Empresa': '847000', 'Articulo': '706258', 'DigitoControl': '5'}
INFO:     127.0.0.1:56126 - "GET /parse_datamatrix?codigo=010843701315676921A014MFCNMYF5AR%1d1024C0106B%1d172703317127062585 HTTP/1.1" 200 OK
INFO:     127.0.0.1:56126 - "GET /favicon.ico HTTP/1.1" 404 Not Found
```

Con esto es suficiente para realizar las pruebas

Debemos de saber

1. Ip del servidor
2. Puerto de escucha
3. Nombre del endpoint (parse_datamatrix)
4. parámetros a pasar (codigo)


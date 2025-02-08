## Ejemplo de uso de la función `DIVIDIR_CADENA`

### Consultas SQL

Separador caracter no imprimible, longitud 1
```sql
SELECT dividir_cadena('010847000728393521W5WVC07FTFC29371272839317250831107V10135A', CHR(29)) FROM DUAL;
```
RESULTADO (Lista de tres elementos, correcto)

|DIVIDIR_CADENA('010847000728393521W5WVC07FTFC29371272839317250831107V10135A',CHR(29))|
|---------------------------------------------------------------------------------------|
|{'010847000728393521W5WVC07FTFC293','712728393','17250831107V10135A'}|

Separador caracter imprimible, longitud 1
```sql
SELECT dividir_cadena('010847000728393521W5WVC07FTFC29371272839317250831107V10135A', ' ') FROM DUAL;
```
RESULTADO (Lista de 1 elemento, correcto)

|DIVIDIR_CADENA('010847000728393521W5WVC07FTFC29371272839317250831107V10135A','')|
|----------------------------------------------------------------------------------|
|{'010847000728393521W5WVC07FTFC29371272839317250831107V10135A'}|

Separador caracter imprimible, longitud 1
```sql
SELECT dividir_cadena('Hola1Mundo', '1') FROM DUAL;
```
RESULTADO (lista con dos elementos, se elimina el elemento vacío último, correcto)

|DIVIDIR_CADENA('HOLA1MUNDO','1')|
|--------------------------------|
|{'Hola','Mundo'}|



Separador caracter imprimible, longitud 1. Cadena inicia con separador
```sql
SELECT dividir_cadena('1Hola1Mundo', '1') FROM DUAL;
```
RESULTADO (lista con tres elementos, el primer elemento es nulo, correcto)

|DIVIDIR_CADENA('1HOLA1MUNDO','1')|
|---------------------------------|
|{'','Hola','Mundo'}|

Separador caracter imprimible, longitud 1. Cadena inicia y finaliza con separador
```sql
SELECT dividir_cadena('1Hola1Mundo1', '1') FROM DUAL;
```
RESULTADO (lista con cuatro elementos, el primer elemento es nulo y el último nulo, correcto)

|DIVIDIR_CADENA('1HOLA1MUNDO1','1')|
|----------------------------------|
|{'','Hola','Mundo',''}|


Separador caracter imprimible, longitud mayor que 1. 
```sql
SELECT dividir_cadena('11Hola(11)Mundo', '(11)') FROM DUAL;
```
RESULTADO (lista con dos elementos, correcto)

|DIVIDIR_CADENA('11HOLA(11)MUNDO','(11)')|
|----------------------------------------|
|{'11Hola','Mundo'}|

Parece que el caso que el último caracter de la cadena es el separador genera un campo demás
```sql
SELECT dividir_cadena('(SEP)010847000728393521W5WVC07FTFC293(SEP)712728393(SEP)17250831107V10135A(SEP)', '(SEP)') FROM DUAL;
```
RESULTADO (lista con cinco elementos, correcto)
|DIVIDIR_CADENA('(SEP)010847000728393521W5WVC07FTFC293(SEP)712728393(SEP)17250831107V10135A(SEP)','(SEP)')|
|---------------------------------------------------------------------------------------------------------|
|{'','010847000728393521W5WVC07FTFC293','712728393','17250831107V10135A',''}|


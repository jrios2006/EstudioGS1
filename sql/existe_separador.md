## Ejemplo de uso de la función `existe_separador`

### Consultas SQL

Separador caracter no imprimible, longitud 1
```sql
SELECT existe_separador('HolaMundo', '["\\x1D", "|", "^", "#", " ", "(SEPARADOR)"]') AS separador FROM DUAL;
```
RESULTADO (Encuentra el separador CHR(29))

|SEPARADOR|
|---------|
||

Cadena con dos separadores (char(29) no imprimible y |)
```sql
SELECT existe_separador('HolaMundo|', '["\\x1D", "|", "^", "#", " ", "(SEPARADOR)"]') AS separador FROM DUAL;
```
RESULTADO (Nos devuelve el primer elemento de la lista que se encuente)

|SEPARADOR|
|---------|
||

Cadena con dos sepradores (encuentra el primero que esmire en la lista)
```sql
SELECT existe_separador('HolaMundo|', '["|", "\\x1D" , "^", "#", " ", "(SEPARADOR)"]') AS separador FROM DUAL;
```
RESULTADO (lista con dos elementos, se elimina el elemento vacío último, correcto)

|SEPARADOR|
|---------|
|&#124;|


Cadena sin separador definido en la lista
```sql
SELECT existe_separador('(SEP)010847000728393521W5WVC07FTFC293(SEP)712728393(SEP)17250831107V10135A(SEP)', '["|", "\\x1D" , "^", "#", " ", "(SEPARADOR)"]') AS separador FROM DUAL;
```
RESULTADO Devuelve NULL

|SEPARADOR|
|---------|
||



Cadena con un separador con más de un caracter
```sql
SELECT existe_separador('(SEP)010847000728393521W5WVC07FTFC293(SEP)712728393(SEP)17250831107V10135A(SEP)', '["|", "\\x1D" , "^", "#", " ", "(SEP)"]') AS separador FROM DUAL;
```
RESULTADO Nos devuelve el separador con más de un carácter

|SEPARADOR|
|---------|
|(SEP)|

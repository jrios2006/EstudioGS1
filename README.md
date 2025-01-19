# EstudioGS1
Como se podría definir sin ambigüedades códigos datamatrix usando para la industria farmacéutica

Vamos a definir tres entidades
- La que define el lenguaje. El organismo regulatorio
- La que escribe códigos gs1. El laboratorio que produce y comercializa un medicamento
- La que lee estos códigos. El hospital / Cĺinica o Farmacia que usa este medicamento

Vamos a ver cómo podríamos definir de manera sencilla un codigo datamatrix con la información sin ambigüedad

## Alfabeto

Los códigos tendrán un alfabeto válido. Este podría ser:

- Caracter separador (un caracter que no pueda usarse dentro de la información de cuanquier dato que se quiera almacenar en el mensaje)
- Dígitos (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
- Letras en máyúsculas (A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z)

El alfabeto contiene 1 carcáter separador, por ejemplo |, 10 dígitos y 26 letras. EN total 37 caracteres diferentes.

Aquí ya se impoen la primera regla, y es que el caracter separado no puede usarse como elemento básico de información.

Hemos decidido además que las letras minúsculas no son válidas en nuestros mensajes. Ni tampoco letras como la Ñ o Á.

¿La industria podría aceptar esto?. ¿Las entidades que producen códigos podrían aceptar este alfabeto?

Las tablas de códigos de los ordenadores aconsejan por ejemplo que el caracter separado sea un caracter no imprimible.

Este podría ser el CHAR(29).

Las personas que escriben mensajes o códigos GS1, ¿tendrán problems por usar este alfabeto?

| **Caracter**  | **Descripción**         |
|---------------|-------------------------|
| CHAR(29)      | Separador               |
| 0             | Dígito: Cero            |
| 1             | Dígito: Uno             |
| 2             | Dígito: Dos             |
| 3             | Dígito: Tres            |
| 4             | Dígito: Cuatro          |
| 5             | Dígito: Cinco           |
| 6             | Dígito: Seis            |
| 7             | Dígito: Siete           |
| 8             | Dígito: Ocho            |
| 9             | Dígito: Nueve           |
| A             | Letra mayúscula: A     |
| B             | Letra mayúscula: B     |
| C             | Letra mayúscula: C     |
| D             | Letra mayúscula: D     |
| E             | Letra mayúscula: E     |
| F             | Letra mayúscula: F     |
| G             | Letra mayúscula: G     |
| H             | Letra mayúscula: H     |
| I             | Letra mayúscula: I     |
| J             | Letra mayúscula: J     |
| K             | Letra mayúscula: K     |
| L             | Letra mayúscula: L     |
| M             | Letra mayúscula: M     |
| N             | Letra mayúscula: N     |
| O             | Letra mayúscula: O     |
| P             | Letra mayúscula: P     |
| Q             | Letra mayúscula: Q     |
| R             | Letra mayúscula: R     |
| S             | Letra mayúscula: S     |
| T             | Letra mayúscula: T     |
| U             | Letra mayúscula: U     |
| V             | Letra mayúscula: V     |
| W             | Letra mayúscula: W     |
| X             | Letra mayúscula: X     |
| Y             | Letra mayúscula: Y     |
| Z             | Letra mayúscula: Z     |


Una vez definido nuestro alfabeto, necesitamos saber como componetmos palabras

## Palabras

Para escribir un código necesitamos palabras están se deberían escribir todas de la misma manera.

La regla para escribir una palabra será:

**[Caracter Separador] + [Patrón] + [Contenido o información]**

El orden marca la forma de escribir cualquier palabra.

La parte más importante es definir los patrones

¿Los que escriebn códigos pueden aceptar esta definición de palabra?

### Patrones

La definición de los patrones marcan la posibilidades de ambigüedad

Vamos aponer un ejemplo:

Se puede definri el patrón 10 como Número de lote, así una palabra podría ser como la siguiente:

[Separador] + 10 + [Número de lote]

A patir de este momento no podríamos definir el patrón 1 con otra información.

Ejemplo si definimos el patrón 1 como localización, podríamos consttruir una palabra como

[Separador] + 1 + [012AMJ]

pero al analizar los 2 patrones definidos en el lenguaje, esta palabra será ambigüa porque podría referirse a 

- localizacón con el código 012AMJ
- número de lote con el código 12AMJ

El lector no sabrái definir con precisión que ha querido decir el escritor del código.

Una vez definidos los patrones este método implica que no es posible definir un patrón con el inicio de las diferentes cadenas de caracteres con la que se forma el patrón.

En el ejemplo la definición del patrón Lote impide que hay otro patrón con el 1

**Es responsable del organismo regulatorio definir con precisión los patrones**

#### Definicón de patrones

Un ejemplo de los patrones que puede tener este lenguaje son:

- 10 (Número de lote)
- 21 (Número de serie)
- 17 (Fecha de caducidad)
- 710 (Número de registro alemán)
- 711 (Número de registro francés)
- 712 (Número de registro español)
- 713 (Número de registro brasileño)
- 714 (Número de registro portugués)
- 715 (Número de registro USA)
- 010 (EAN13 del medicamento)

Los fabricantes o los que escriben los códigos deben de estar de acuerdo con la configuración de los patrones.

La única restrincción es la que hemos puesto, que un patrón no debe de estar contenido en otro patrón desde su inicio.

Ejemplos de uso sería:

- [Separador] + 10 + NUMEROLOTE
- [Separador] + 21 + NUMEROSERIE
- [Separador] + 17 + 251215

Ejemplos de palabras (Se asume para el ejemplo que el separador es este |)
- |10Lote  (Es incorrecta la palabra porque tiene caracteres que no están en el alfabeto, ote)
- |10LOTE555  (Está correctamente construida)

## Sentencias
Es un conjunto de palabras válidas en el sistema.

Se deben de poner restricciones para que una sentencia sea válida.

Por ejemplo deben de contener al menos tres palabras válidas

- Debe de haber un único 010 (código EAN13)
- Debe de haber un único 17 (Fecha de caducidad)
- Debe de haber un único número de lote

Entre las reglas que debe de especificar el organismo regulador dice que hay patrones obligatorios y opcionales pero que deben de ser únicos.

Un ejemplo de sentencia podría ser

- |10LOTE|10LOTE555 (Esta sentencia sería errónea porque se repite el patrón 10 y falta el patrón 010 y el 17
- |10LOTE|17FECHA|010EAN13 (Esta sentencia será válida porque tiene un patrón cada obligatorio, aqune luego será incorecta porque alguna de la palabras no son válidas)

## Definición de palabras

El organismo regulador debería de llegar a un acerdo con los que escriben sentencias para validar sintácticamente y semánticamente cada palabra.

El uso de expresiones regulares puede ayudar a implementar de forma sencilla la validación de una palabras y de sentencias.

Esto ayudaría a implemntar en cualquier lenguaje por parte de la industria y de los usuarios tanto la escritura como la lectura de los mensajes o sentencias

### Fecha de caducidad

La palabra fecha de caducidad esta'descrita con la sigueinte estructura

[Separador] + 17 + AAMMDD donde 

- AA son dos dígitos que representan el año
- MM son dos dígitos que representa el mes
- DD son dos dígitos que representan el día. 00 reresenta el último día del mes

Esta es la definición y una primera validación de la palabra es saber si la estructura de información dl valor que representa la pabra está pormado por 6 dígitos
Luego habría que verificar que esos 6 dígitos representa una fecha válida.

Ejemplo:

- |17250229 no es una palabra válida porque aunque cuanque con que son dígitos cada parte la fecha que representa no existe. No existe el 29 de febrero del 2025
- |17280200 es válida y representa el valor 29 de febrero del 2029

## Herramientas para construir y leer sentencias

Necesitmos leer sentencias y necesitmaos poder partir en palabras. Para poder hacer esto basta con la función  split y buscar por el separador

Herramienta como la instrucción in podrá validar el contenido de cada palabra y decidir si hay alguna palabra escrita sin los caracteres del alfabeto

También podemos validar la obligatoriedad de patrones y de su unicidad, con herramientas de tipos de datos abstractos como listas, conjuntos etc.

Luego habrá de decidir sobre la definición de cada palabra para obtener cada valor.

## Codificación en base 64

Depende de como queramos guarda la información de un código gs1, podemos guarda ese valor codificado

Ejemplo:

01084315060003241023201021FMRK0HSZDWBX172603317126838471
se codifica como 
MDEwODQzMTUwNjAwMDMyNDEwMjMyMDEwHTIxRk1SSzBIU1pEV0JYHTE3MjYwMzMxNzEyNjgzODQ3MQ==

Esto podrái ser útil para luego usar heramientas para generar un código QR con la codificacación de esto.

Es algo a explorar


## Ejemplos

Iré colgando ejemplos de como escribir o leer códigos generados con herramientas accesible sen internet y como se debería de definir códigos gs1 siguiendo esta reglas.

Haremos una comparativa si en lugar de usar esta codificación usáramos un diccionario JSON para definir cada elemento y las diferencias en tamaño del mensaje que pueda hacer más o menos viable según las pazacidad de la generación de gráficos datamamtrix

¿Es posible poner en una caja me demidicamento un gráfico de 1 x 1 centímetro un código que un lector tenga la resolución suficiente para leer el grafico y devolvernos una setencia que podamos traducir si error?

¿Qué límite en el tamaño de la escritura de gráficos es lo que podemos generar para que no haya error?

¿Podemos metar información por ejemplo de 3000 caracteres para escribir en un dibujo de 1 x 1 centímetro con la tecnologáa esta?

¿Que pierdo si uso JSON o que gano si uso JSON?







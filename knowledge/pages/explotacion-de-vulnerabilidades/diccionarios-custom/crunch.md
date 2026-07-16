
# Crunch

## <mark style="color:purple;">1. Sintaxis básica</mark>

```bash
crunch <min> <max> [opciones]
```

* `<min>` y `<max>`: Longitud mínima y máxima de la palabra.
* `[opciones]`: Diversas opciones para personalizar la generación de palabras.

## <mark style="color:purple;">**2. Ejemplo sencillo**</mark>

```bash
crunch 8 12 -o wordlist.txt
```

Este comando generará todas las combinaciones posibles de letras y números con una longitud de 8 a 10 caracteres y las guardará en un archivo llamado `wordlist.txt`.

## <mark style="color:purple;">**3. Opciones comunes**</mark>

* `-o <archivo>`: Especifica el nombre del archivo de salida.
* `-t <patrón>`: Define un patrón de caracteres personalizado (por ejemplo, `%%,@@@`).
* `-d <separadores>`: Define los caracteres especiales que se pueden usar como separadores.

## <mark style="color:purple;">**4. Ejemplo con patrón**</mark>

```bash
crunch 11 11 -o wordlist.txt -t user_%%%%\!\*
```

En este ejemplo:

* `user_` es la parte fija de la contraseña.
* `%%%%` generará números de cuatro dígitos (por ejemplo, desde 0000 hasta 9999).
* `\!\*` generará dos caracteres especiales al final.

## <mark style="color:purple;">**5. Caracteres específicos**</mark>

```bash
crunch 8 12 -o wordlist.txt -p @%@%
```

Este comando generará palabras que contengan solo los caracteres `@`, `%`, y `@` y las guardará en `wordlist.txt`.

## <mark style="color:purple;">6. Ejemplo que contenga</mark> `1nh4k34bl3!`

* Sabemos que tiene 11 caracteres
* Sabemos los caracteres que contiene
* Podríamos saber un patrón

<pre class="language-bash"><code class="lang-bash"><strong># Diccionario con todas las posible combinaciones
</strong>crunch 11 11 -o wordlist.txt -p 1nh4k34bl3!

Crunch will now generate approximately the following amount of data: 479001600 bytes
456 MB
0 GB
0 TB
0 PB
Crunch will now generate the following number of lines: 39916800
</code></pre>

<pre class="language-bash"><code class="lang-bash"><strong>cat wordlist.txt
</strong>!13344bhkln
!13344bhknl
!13344bhlkn
!13344bhlnk
!13344bhnkl
!13344bhnlk
!13344bkhln
!13344bkhnl
!13344bklhn
...SNIP...
1nh4k34bl3!
</code></pre>

## <mark style="color:purple;">7. Usar diccionario sin ocupar espacio en disco</mark>

Un diccionario creado con crunch puede ocupar muchísimo espacio en disco:

```bash
crunch 8 20 123456789 -o wordlist.txt

Crunch will now generate the following amount of data: 8814013659354411785 bytes
8405698451380 MB
8208689893 GB
8016298 TB
7828 PB
Crunch will now generate the following number of lines: 13677373641433663955 
```

Por lo que podemos ejecutar crunch y pasarle el output como input del siguiente, sin guardarlo en disco:

```bash
crunch 8 8 123456789 | aircrack-ng -w -b <MAC-TARGET> - handshake.cap
```

### Guardar el progreso

{% code overflow="wrap" %}

```bash
crunch 8 8 123456789 | john --stding --session=wifi_cracking --stdout | aircrack-ng -b <MAC-TARGET> -w - handshake.cap
```

{% endcode %}

Restaurar proceso en caso de detenerlo:

{% code overflow="wrap" %}

```bash
crunch 8 8 123456789 | john --restore=wifi_cracking.rec | aircrack-ng -b <MAC-TARGET> -w - handshake.cap
```

{% endcode %}

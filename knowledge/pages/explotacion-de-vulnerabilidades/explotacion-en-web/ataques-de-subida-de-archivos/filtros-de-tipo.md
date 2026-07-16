
# Filtros de tipo

Hasta ahora, solo hemos trabajado con filtros de tipo que solo consideran la extensión del archivo en el nombre del archivo. Sin embargo, como vimos en la sección anterior, aún podemos obtener el control sobre el servidor back-end incluso con extensiones de imagen (por ejemplo, `shell.php.jpg`). Además, podemos utilizar algunas extensiones permitidas (por ejemplo, SVG) para realizar otros ataques. Todo esto indica que solo probar la extensión del archivo no es suficiente para prevenir ataques de carga de archivos.

Por este motivo, muchos servidores web y aplicaciones web modernos también prueban el contenido del archivo cargado para asegurarse de que coincida con el tipo especificado. Si bien los filtros de extensión pueden aceptar varias extensiones, los filtros de contenido generalmente especifican una sola categoría (por ejemplo, imágenes, videos, documentos), por lo que no suelen utilizar listas negras o listas blancas. Esto se debe a que los servidores web brindan funciones para verificar el tipo de contenido del archivo y, por lo general, este pertenece a una categoría específica.

Existen dos métodos comunes para validar el contenido de un archivo: `Content-Type Header` o `Contenido del archivo`. Veamos cómo podemos identificar cada filtro y cómo evitarlos.

***

## <mark style="color:purple;">Content-Type</mark>

En este ejercicio intentaremos cargar un script PHP:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_content_type_upload.jpg" alt=""><figcaption></figcaption></figure>

Vemos que recibimos un mensaje que dice `Only images are allowed`. El mensaje de error persiste y nuestro archivo no se carga incluso si intentamos algunos de los trucos que aprendimos en las secciones anteriores. Si cambiamos el nombre del archivo a `shell.jpg.phtml` o `shell.php.jpg`, o incluso si usamos `shell.jpg` con un contenido de webshell, nuestra carga fallará. Como la extensión del archivo no afecta el mensaje de error, la aplicación web debe estar probando el contenido del archivo para la validación de tipo. Como se mencionó anteriormente, esto puede estar en el `Content-Type Header` o en el `Contenido del archivo`.

El siguiente es un ejemplo de cómo una aplicación web PHP prueba el encabezado `Content-Type` para validar el tipo de archivo:

```php
$type = $_FILES['uploadFile']['type'];

if (!in_array($type, array('image/jpg', 'image/jpeg', 'image/png', 'image/gif'))) {
    echo "Only images are allowed";
    die();
}
```

El código establece la variable (`$type`) del encabezado `Content-Type` del archivo cargado . Nuestros navegadores establecen automáticamente el encabezado Content-Type al seleccionar un archivo a través del cuadro de diálogo del selector de archivos, que generalmente se deriva de la extensión del archivo. Sin embargo, dado que nuestros navegadores lo establecen, esta operación es una operación del lado del cliente y podemos manipularla para cambiar el tipo de archivo percibido y, potencialmente, omitir el filtro de tipo.

Podemos empezar por analizar el encabezado Content-Type con [la lista de palabras Content-Type de](https://github.com/danielmiessler/SecLists/blob/master/Miscellaneous/Web/content-type.txt) SecLists a través de Burp Intruder, para ver qué tipos están permitidos. Sin embargo, el mensaje nos dice que solo se permiten imágenes, por lo que podemos limitar nuestro análisis a los tipos de imágenes, lo que reduce la lista de palabras solo a `45` tipos (en comparación con las 700 originales). Podemos hacerlo de la siguiente manera:

```shell-session
afsh4ck@kali$ wget https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/web-all-content-types.txt
afsh4ck@kali$ cat web-all-content-types.txt | grep 'image/' > image-content-types.txt
```

Aquí podríamos realizar un fuzzing con Burp Intruder seleccionando como variable el `Content-Type` y usar esta lista de content-types para ver cual nos da una respuesta positiva.

Para simplificar, simplemente seleccionemos un tipo de imagen (por ejemplo `image/jpg`), luego interceptemos nuestra solicitud de carga y cambiemos el encabezado Content-Type:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_bypass_content_type_request.jpg" alt=""><figcaption></figcaption></figure>

Esta vez obtenemos `File successfully uploaded`, y si visitamos nuestro archivo, vemos que se cargó correctamente:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_php_manual_shell.jpg" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**Nota**: Una solicitud HTTP de carga de archivo tiene dos encabezados Content-Type, uno para el archivo adjunto (en la parte inferior) y otro para la solicitud completa (en la parte superior). Por lo general, necesitamos modificar el encabezado Content-Type del archivo, pero en algunos casos la solicitud solo contendrá el encabezado Content-Type principal (por ejemplo, si el contenido cargado se envió como datos `POST`), en cuyo caso necesitaremos modificar el encabezado Content-Type principal.
{% endhint %}

***

## MIME Type

El segundo y más común tipo de validación del contenido de un archivo es probar el `MIME-Type`. `Multipurpose Internet Mail Extensions (MIME)` es un estándar de Internet que determina el tipo de un archivo a través de su formato general y estructura de bytes.

Esto se hace generalmente inspeccionando los primeros bytes del contenido del archivo, que contienen la [Firma del Archivo](https://en.wikipedia.org/wiki/List_of_file_signatures) o [los Bytes Mágicos](https://opensource.apple.com/source/file/file-23/file/magic/magic.mime) . Por ejemplo, si un archivo comienza con ( `GIF87a` o `GIF89a`), esto indica que es una imagen `GIF`, mientras que un archivo que comienza con texto simple generalmente se considera un archivo `Text`. Si cambiamos los primeros bytes de cualquier archivo a los bytes mágicos GIF, su tipo MIME se cambiaría a una imagen GIF, independientemente de su contenido restante o extensión.

{% hint style="info" %}
**Consejo**: Muchos otros tipos de imágenes tienen bytes no imprimibles para sus firmas de archivo, mientras que una imagen `GIF` comienza con bytes imprimibles ASCII (como se muestra arriba), por lo que es la más fácil de imitar. Además, como la cadena `GIF8` es común entre ambas firmas GIF, suele ser suficiente para imitar una imagen GIF.
{% endhint %}

Tomemos un ejemplo básico para demostrarlo. El comando `file` en sistemas Unix encuentra el tipo de archivo a través del tipo MIME. Si creamos un archivo básico con texto en su interior, se lo considerará un archivo de texto, de la siguiente manera:

```shell-session
afsh4ck@kali$ echo "Esto es un archivo de texto" > text.jpg 
afsh4ck@kali$ file text.jpg 
text.jpg: ASCII text
```

Como vemos, el tipo MIME del archivo es `ASCII text`, aunque su extensión sea `.jpg`. Sin embargo, si escribimos `GIF8`al principio del archivo, se considerará una imagen `GIF`, aunque su extensión siga siendo `.jpg`:

```shell-session
afsh4ck@kali$ echo "GIF8" > text.jpg 
afsh4ck@kali$ file text.jpg
text.jpg: GIF image data
```

Los servidores web también pueden utilizar este estándar para determinar los tipos de archivos, lo que suele ser más preciso que comprobar la extensión del archivo. El siguiente ejemplo muestra cómo una aplicación web PHP puede comprobar el tipo MIME de un archivo cargado:

```php
$type = mime_content_type($_FILES['uploadFile']['tmp_name']);

if (!in_array($type, array('image/jpg', 'image/jpeg', 'image/png', 'image/gif'))) {
    echo "Only images are allowed";
    die();
}
```

Como podemos ver, los tipos MIME son similares a los que se encuentran en los encabezados Content-Type, pero su origen es diferente, ya que PHP utiliza la `mime_content_type()`función para obtener el tipo MIME de un archivo. Intentemos repetir nuestro último ataque, pero ahora con un ejercicio que prueba tanto el encabezado Content-Type como el tipo MIME:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_bypass_content_type_request.jpg" alt=""><figcaption></figcaption></figure>

Una vez que enviamos nuestra solicitud, notamos que recibimos el mensaje de error `Only images are allowed`. Ahora, intentemos agregar `GIF8`antes de nuestro código PHP para intentar imitar una imagen GIF mientras mantenemos nuestra extensión de archivo como `.php`, de modo que se ejecute el código PHP de todos modos:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_bypass_mime_type_request.jpg" alt=""><figcaption></figcaption></figure>

Esta vez obtenemos `File successfully uploaded`, y nuestro archivo se carga exitosamente al servidor:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_bypass_mime_type.jpg" alt=""><figcaption></figcaption></figure>

Ahora podemos visitar nuestro archivo cargado, y veremos que podemos ejecutar exitosamente los comandos del sistema:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_php_manual_shell_gif.jpg" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**Nota**: Vemos que la salida del comando comienza con `GIF8`, ya que esta fue la primera línea en nuestro script PHP para imitar los bytes mágicos GIF, y ahora se genera como texto simple antes de que se ejecute nuestro código PHP.
{% endhint %}

Podemos utilizar una combinación de los dos métodos analizados en esta sección, lo que puede ayudarnos a eludir algunos filtros de contenido más robustos. Por ejemplo, podemos intentar utilizar un `MIME type con un Content-Type no permitido`, un `MIME/Content-Type permitido  con una extensión no permitida`, o un `MIME/Content-Type no permitido con una extensión permitida`, y así sucesivamente. De manera similar, podemos intentar otras combinaciones y permutaciones para intentar confundir al servidor web y, según el nivel de seguridad del código, es posible que podamos eludir varios filtros.

***

## <mark style="color:purple;">Caso práctico</mark>

El servidor mencionado anteriormente emplea filtros Client-Side, Blacklist, Whitelist, Content-Type y MIME-Type para garantizar que el archivo cargado sea una imagen. Intente combinar todos los ataques que aprendió hasta ahora para eludir estos filtros y cargar un archivo PHP y leer la flag en "`/flag.txt`".

```
Objetivo: http://94.237.54.239:48561
```

La cosa se nos complica, pero vamos al lio!

<figure><img src="/files/VgZjnWAB2ow0bBiX0syx" alt=""><figcaption></figcaption></figure>

Esta aplicación ya la conocemos más que de sobra. Vamos a realizar todas las técnicas que conocemos para bypassear la subida de una shell.

### Client-Side Validation

Como ya sabemos, debemos eliminar desde el inspector el script de validación y los formatos aceptados:

<figure><img src="/files/7NnAvmOHNlu0KiGtta3Y" alt=""><figcaption></figcaption></figure>

Subimos la webshell `phpbash.php` y lo primero que nos da es un error `Extension not allowed`:

<figure><img src="/files/eoXgV4zbTlzB6oyW35bi" alt=""><figcaption></figcaption></figure>

### Fuzzing de extensiones (Whitelist)

Vamos a enviar la petición a `Intruder` para fuzzear posibles extensiones, al igual que vimos en la sección anterior. Vamos a usar la wordlists de extensiones de [Seclists](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/web-extensions.txt)

Lo primero añadimos la extensión como variable en Intruder:

<figure><img src="/files/nWpFXpmk1XusqJU9ncRo" alt=""><figcaption></figcaption></figure>

En la pestaña `Payloads` pegamos las extensiones de Seclists y desactivamos la opción de `Payload encoding`:

<figure><img src="/files/QwMc3BjyfObi4iNTrYIS" alt=""><figcaption></figcaption></figure>

Iniciamos el fuzzing y observamos los resultados. Tenemos 2 tipos de respuestas:

* `Lenght 225: Extension not allowed`

<figure><img src="/files/M1J4ofxHLcfaG6xCzlyL" alt=""><figcaption></figcaption></figure>

* `Lenght 227/226: Only images are allowed`

<figure><img src="/files/s48j1oc4zYfYrS9dALXJ" alt=""><figcaption></figcaption></figure>

Podríamos probar por ejemplo esa extensión `.phar` con una inyección de caracteres con una doble extensión, lo que podría bypassear los filtros.

### Fuzzing de Content-Type

Vamos a probar a subir una imagen legítima para probar los tipos de content-types con status 200, y vamos a añadir el `Content-Type` como variable:

<figure><img src="/files/TpuCB4E0fXF4wSRcxV3I" alt=""><figcaption></figcaption></figure>

En la pestaña de Payloads vamos a pegar la lista de palabras de [Content-Type de Seclists](https://github.com/danielmiessler/SecLists/blob/master/Miscellaneous/Web/content-type.txt), pero para que el fuzzing sea más efectivo vamos a filtrar solamente las de formato imagen, reduciendo considerablemente el tiempo del fuzzing:

```shell-session
afsh4ck@kali$ wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Miscellaneous/Web/content-type.txt
afsh4ck@kali$ cat content-type.txt | grep 'image/' > image-content-types.txt
```

<figure><img src="/files/yKTsskEsa7B8zEU3vGsl" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
Importante también desmarcar la casilla Payload encoding.
{% endhint %}

Lanzamos el fuzzing y vemos los resultados. Vemos un montón de extensiones de imagen permitidas, como `gif`, `jpeg`, `png`...

<figure><img src="/files/UnB8a4dZNwqJI0sN9hhJ" alt=""><figcaption></figcaption></figure>

Vemos que nos permite subir `GIFs`, con lo que podríamos probar a cambiar el `MYME-Type` del archivo para intentar cargar una `shell.php` que imite a un GIF

### MIME Type

Vamos a probar a poner `GIF8` delante de nuestra shell.php:

```bash
cat shell.php     
GIF8 <?php system($_REQUEST[cmd]); ?>
```

Lo subimos y capturamos la petición. Nos da un `extension not allowed`, pero fijaros que pasa si ponemos una doble extensión a la shell como `shell.gif.phar`:

{% hint style="info" %}
Nota: En archivos ejecutables es importante poner la extensión al final (.phar, .php...), ya que sino el servidor dará un error al abrir el archivo
{% endhint %}

<figure><img src="/files/CruHo1xZsolew9D4mILt" alt=""><figcaption></figcaption></figure>

Se sube la shell correctamente!

<figure><img src="/files/Zm230M7WApS0c7d2xMgi" alt=""><figcaption></figcaption></figure>

Ahora si accedemos a la siguiente url comprobamos que funciona la shell y nos devuelve el ID del usuario:

```
http://94.237.54.239:48561/profile_images/shell.gif.phar?cmd=id
```

<figure><img src="/files/bff2rOJuW78hHC7ZhfQv" alt=""><figcaption></figcaption></figure>

Obtenemos la flag de la misma manera, y como vemos antes de la flag se inserta el texto GIF8 que se corresponde con los Magic Bytes del formato GIF:

<figure><img src="/files/DGvfR9e2MGvfUOTHJ8Zr" alt=""><figcaption></figcaption></figure>

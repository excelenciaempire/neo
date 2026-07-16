
# Filtros de Whitelist

Como se explicó en la sección anterior, el otro tipo de validación de extensión de archivo es mediante el uso de una `whitelist de extensiones de archivo permitidas`. Una lista blanca suele ser más segura que una lista negra. El servidor web solo permitiría las extensiones especificadas y la lista no necesitaría ser exhaustiva para cubrir las extensiones poco comunes.

Aun así, existen diferentes casos de uso para una blacklist y una whitelist. Una `blacklist` puede ser útil en casos en los que la funcionalidad de carga necesita permitir una amplia variedad de tipos de archivos (por ejemplo, el Administrador de archivos), mientras que una `whitelist` generalmente solo se usa con funcionalidades de carga donde solo se permiten unos pocos tipos de archivos. Ambas también se pueden usar en conjunto.

***

## <mark style="color:purple;">Extensiones de la whitelist</mark>

En este ejercicio intentaremos cargar una extensión PHP poco común, como `.phtml`, y veamos si aún podemos cargarla como lo hicimos en la sección anterior:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_whitelist_message.jpg" alt=""><figcaption></figcaption></figure>

Vemos que aparece un mensaje que dice `Only images are allowed`, lo cual puede ser más común en aplicaciones web que ver un tipo de extensión bloqueada. Sin embargo, los mensajes de error no siempre reflejan qué forma de validación se está utilizando, así que intentemos buscar extensiones permitidas como hicimos en la sección anterior, usando la misma lista de palabras que usamos anteriormente:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_whitelist_fuzz.jpg" alt=""><figcaption></figcaption></figure>

Podemos ver que todas las variaciones de extensiones PHP están bloqueadas (por ejemplo `php5`, `php7` , `phtml`). Sin embargo, la lista de palabras que usamos también contenía otras extensiones "maliciosas" que no estaban bloqueadas y se cargaron correctamente. Por lo tanto, intentemos comprender cómo pudimos cargar estas extensiones y en qué casos podemos utilizarlas para ejecutar código PHP en el servidor back-end.

Podríamos por ejemplo fuzzear el formulario de carga con [esta lista de palabras](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/web-extensions.txt) para encontrar qué extensiones están incluidas en la lista blanca del formulario de carga.

El siguiente es un ejemplo de una prueba de extensiones de archivo en una whitelist:

```php
$fileName = basename($_FILES["uploadFile"]["name"]);

if (!preg_match('^.*\.(jpg|jpeg|png|gif)', $fileName)) {
    echo "Only images are allowed";
    die();
}
```

Vemos que el script utiliza una expresión regular ( `regex`) para comprobar si el nombre del archivo contiene alguna extensión de imagen incluida en la lista blanca. El problema aquí radica en el `regex`, ya que solo comprueba si el nombre del archivo `contiene` la extensión y no si realmente `termina con ella`. Muchos desarrolladores cometen este tipo de errores debido a una comprensión deficiente de los patrones de expresiones regulares.

Entonces, veamos cómo podemos evitar estas pruebas para cargar scripts PHP.

***

## <mark style="color:purple;">Extensiones dobles</mark>

El código solo prueba si el nombre del archivo contiene una extensión de imagen; un método sencillo para pasar la prueba de expresiones regulares es a través de `Extensiones Dobles`. Por ejemplo, si la `.jpg` extensión está permitida, podemos agregarla en el nombre del archivo cargado y aún así terminar el nombre de archivo con `.php`(por ejemplo `shell.jpg.php`, ), en cuyo caso deberíamos poder pasar la prueba de lista blanca, mientras cargamos un script PHP que puede ejecutar código PHP.

Interceptemos una solicitud de carga normal y modifiquemos el nombre del archivo a ( `shell.jpg.php`), y modifiquemos su contenido al de un webshell:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_double_ext_request.jpg" alt=""><figcaption></figcaption></figure>

Ahora, si visitamos el archivo cargado e intentamos enviar un comando, podemos ver que efectivamente ejecuta exitosamente los comandos del sistema, lo que significa que el archivo que cargamos es un script PHP completamente funcional:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_php_manual_shell.jpg" alt=""><figcaption></figcaption></figure>

Sin embargo, esto puede no funcionar siempre, ya que algunas aplicaciones web pueden utilizar un patrón `regex` estricto, como se mencionó anteriormente, como el siguiente:

```php
if (!preg_match('/^.*\.(jpg|jpeg|png|gif)$/', $fileName)) { ...SNIP... }
```

Este patrón solo debe considerar la extensión final del archivo, ya que utiliza ( `^.*\.`) para hacer coincidir todo hasta el último ( `.`), y luego utiliza ( `$`) al final para hacer coincidir solo las extensiones que terminan el nombre del archivo. Por lo tanto, el `ataque de arriba no funcionaría`. Sin embargo, algunas técnicas de explotación pueden permitirnos eludir este patrón, pero la mayoría se basan en configuraciones incorrectas o sistemas obsoletos.

***

## <mark style="color:purple;">Doble extensión inversa</mark>

En algunos casos, la funcionalidad de carga de archivos en sí puede no ser vulnerable, pero la configuración del servidor web puede generar una vulnerabilidad. Por ejemplo, una organización puede utilizar una aplicación web de código abierto, que tiene una funcionalidad de carga de archivos. Incluso si la funcionalidad de carga de archivos utiliza un patrón de expresión regular estricto que solo coincide con la extensión final del nombre del archivo, la organización puede utilizar las configuraciones inseguras para el servidor web.

Por ejemplo, el servidor `Apache2` puede incluir la siguiente configuración en `/etc/apache2/mods-enabled/php7.4.conf`:

```xml
<FilesMatch ".+\.ph(ar|p|tml)">
    SetHandler application/x-httpd-php
</FilesMatch>
```

La configuración anterior es la forma en que el servidor web determina qué archivos permitir la ejecución de código PHP. Especifica una lista blanca con un patrón de expresión regular que coincide con `.phar`, `.php` y `.phtml`. Sin embargo, este patrón de expresión regular puede tener el mismo error que vimos anteriormente si olvidamos finalizarlo con ( `$`). En tales casos, se permitirá la ejecución de código PHP a cualquier archivo que contenga las extensiones anteriores, incluso si no termina con la extensión PHP. Por ejemplo, el nombre de archivo ( `shell.php.jpg`) debería pasar la prueba de lista blanca anterior ya que termina con ( `.jpg`), y podría ejecutar código PHP debido a la configuración incorrecta anterior, ya que contiene ( `.php`) en su nombre.

Intentemos interceptar una solicitud de carga de imagen normal y usemos el nombre de archivo anterior para pasar la prueba estricta de whitelist:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_reverse_double_ext_request.jpg" alt=""><figcaption></figcaption></figure>

Ahora, podemos visitar el archivo cargado e intentar ejecutar un comando:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_php_manual_shell.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, hemos pasado con éxito la estricta prueba de lista blanca y hemos aprovechado la configuración incorrecta del servidor web para ejecutar código PHP y obtener control del servidor.

## <mark style="color:purple;">Inyección de caracteres</mark>

Por último, analicemos otro método para eludir una prueba de validación de whitelist mediante `Inyección de caracteres`. Podemos inyectar varios caracteres antes o después de la extensión final para provocar que la aplicación web interprete incorrectamente el nombre del archivo y ejecute el archivo cargado como un script PHP.

Los siguientes son algunos de los caracteres que podemos intentar inyectar:

* `%20`
* `%0a`
* `%00`
* `%0d0a`
* `/`
* `.\`
* `.`
* `…`
* `:`

Cada carácter tiene un caso de uso específico que puede engañar a la aplicación web para que interprete mal la extensión del archivo. Por ejemplo, ( `shell.php%00.jpg`) funciona con servidores PHP con la versión `5.X` o anteriores, ya que hace que el servidor web PHP termine el nombre del archivo después del ( `%00`), y lo almacene como ( `shell.php`), mientras sigue pasando la whitelist. Lo mismo se puede usar con aplicaciones web alojadas en un servidor Windows inyectando dos puntos ( `:`) antes de la extensión de archivo permitida (por ejemplo `shell.aspx:.jpg` ), que también debería escribir el archivo como ( `shell.aspx`). De manera similar, cada uno de los otros caracteres tiene un caso de uso que puede permitirnos cargar un script PHP mientras se pasa por alto la prueba de validación de tipo.

Podemos escribir un pequeño script bash que genere todas las permutaciones del nombre del archivo, donde los caracteres anteriores se inyectarían antes y después de las extensiones `PHP` y `JPG` , de la siguiente manera:

```bash
for char in '%20' '%0a' '%00' '%0d0a' '/' '.\\' '.' '…' ':'; do
    for ext in '.php' '.phps' '.phtml' '.phar' '.php5' '.php8'; do
        echo "shell$char$ext.jpg" >> wordlist.txt
        echo "shell$ext$char.jpg" >> wordlist.txt
        echo "shell.jpg$char$ext" >> wordlist.txt
        echo "shell.jpg$ext$char" >> wordlist.txt
    done
done
```

Con esta lista de palabras personalizada, podemos ejecutar un análisis de fuzzing con `Burp Intruder`, similar a los que hicimos anteriormente. Si el back-end o el servidor web están desactualizados o tienen ciertas configuraciones incorrectas, algunos de los nombres de archivo generados pueden eludir la prueba de lista blanca y ejecutar código PHP.

***

## <mark style="color:purple;">Caso práctico</mark>

El ejercicio anterior emplea una prueba de blacklist y whitelist para bloquear extensiones no deseadas y permitir únicamente extensiones de imagen. Intente omitir ambas para cargar un script PHP y ejecutar el código para leer "`/flag.txt`".

{% hint style="info" %}
Puedes utilizar cualquiera de las dos últimas técnicas. Si una extensión está bloqueada, prueba con otra que pueda ejecutar código PHP.
{% endhint %}

```
Objetivo: 94.237.48.20:51547
```

<figure><img src="/files/BUDYndpMTSPPW2OlmTCI" alt=""><figcaption></figcaption></figure>

Como ya vimos en los ejercicios de secciones anteriores debemos modificar el front desde el inspector para poder subir la imagen de perfil, eliminando el script de validación, los formatos permitidos y el botón submit disabled:

<figure><img src="/files/Cq3OvNSRv6gcUVu8iSGP" alt=""><figcaption></figcaption></figure>

También debemos eliminar el parámetro `name="uploadfile"` ya que sino no carga la extensión. Ahora si, capturamos la petición con BurpSuite al subir la webshell `phpbash.php`:

<figure><img src="/files/qszQnpfXGMWDhucXcKHK" alt=""><figcaption></figcaption></figure>

Como era de esperar, nos da un error `Extension not allowed`, por lo que vamos a fuzzear la extensión `.php`, enviando la petición a `Intruder`:

<figure><img src="/files/pMYlrgvr6BiwMR8MuJsv" alt=""><figcaption></figcaption></figure>

En el apartado de Payloads vamos a pegar las [extensiones típicas de php](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Extension%20PHP/extensions.lst):

<figure><img src="/files/ruGv8epeI0WUkltr65qp" alt=""><figcaption></figcaption></figure>

De estas extensiones ninguna nos sirve, por lo que vamos a probar una inyección de caracteres:

<figure><img src="/files/CRGhWgq7ydjrNEKM2tyy" alt=""><figcaption></figcaption></figure>

### Inyección de caracteres

Como la webshell que queremos subir se llama `phpbash.php` vamos a usar este script para crear todas las posibles combinaciones de caracteres y extensiones `PHP` y `JPG`, y guardarlo en una wordlist:

```bash
for char in '%20' '%0a' '%00' '%0d0a' '/' '.\\' '.' '…' ':'; do
    for ext in '.php' '.phps' '.phtml' '.phar' '.php5' '.php8'; do
        echo "phpbash$char$ext.jpg" >> wordlist.txt
        echo "phpbash$ext$char.jpg" >> wordlist.txt
        echo "phpbash.jpg$char$ext" >> wordlist.txt
        echo "phpbash.jpg$ext$char" >> wordlist.txt
    done
done
```

<figure><img src="/files/2532BweGXFfcmpboG7bA" alt=""><figcaption></figcaption></figure>

Entonces ahora en intruder vamos a seleccionar el nombre completo como variable:

<figure><img src="/files/lAjpmVxdPltkeX7JQEXJ" alt=""><figcaption></figcaption></figure>

Y en Payloads vamos a pegar todos los nombres que nos ha generado el script:

<figure><img src="/files/S1tksiKcCScvytqNgA8E" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
**Importante**! Debemos asegurarnos de desmarcar la casilla Payload encoding, porque sino nos va a codificar los puntos:
{% endhint %}

<figure><img src="/files/mObSgK0ZY8rCTX9sdAwJ" alt=""><figcaption></figcaption></figure>

Fijaros lo que tenemos por aquí:

<figure><img src="/files/2w60jz3VOUq0ty6xCaEw" alt=""><figcaption></figcaption></figure>

Nos ha encontrado que podemos inyectar caracteres de la siguiente manera y el archivo se subiría correctamente:

```
phpbash%20.phar.jpg
```

Vamos a comprobarlo modificando la solicitud con BupSuite:

<figure><img src="/files/XoPOcWWVR0yR7CEXXNzH" alt=""><figcaption></figcaption></figure>

En la respuesta vemos que se sube correctamente, así que vamos a hacer un forward para subirlo al servidor:

<figure><img src="/files/CIMvRECsrfkPlx5Tcsu4" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/AdRBAdEY1ns0svNDHdEC" alt=""><figcaption></figcaption></figure>

Bingo! Ahora si vamos a la siguiente URL accederemos directamente a la webshell:

```
http://94.237.48.20:51547/profile_images/phpbash%20.phar.jpg
```

No conseguimos acceder correctamente a la webshell por el caracter `%20` que crea un espacio en la URL, por lo que vamos a intentar subir de nuevo la webshell pero sin el caracter `%20`:

```
phpbash.phar.jpg
```

Ahora si, accedemos a la webshell sin problema y obtenemos la flag 🏆

<figure><img src="/files/xvERaIgWv7L4c6TqyyQy" alt=""><figcaption></figcaption></figure>

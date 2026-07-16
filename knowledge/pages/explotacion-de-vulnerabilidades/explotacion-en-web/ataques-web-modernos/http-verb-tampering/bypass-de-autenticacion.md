
# Bypass de autenticación

## <mark style="color:purple;">Cómo eludir la autenticación básica</mark>

***

La explotación de vulnerabilidades de HTTP Verb Tampering suele ser un proceso relativamente sencillo. Solo tenemos que probar métodos HTTP alternativos para ver cómo los gestionan el servidor web y la aplicación web.&#x20;

Aunque muchas herramientas de análisis de vulnerabilidades automatizadas pueden identificar de forma consistente vulnerabilidades de HTTP Verb Tampering provocadas por configuraciones de servidor inseguras, normalmente no identifican vulnerabilidades de HTTP Verb Tampering provocadas por una codificación insegura. Esto se debe a que el primer tipo se puede identificar fácilmente una vez que pasamos por alto una página de autenticación, mientras que el otro necesita pruebas activas para ver si podemos pasar por alto los filtros de seguridad establecidos.

El primer tipo de vulnerabilidad de HTTP Verb Tampering es causado principalmente por `configuraciones inseguras de servidores web`, y explotar esta vulnerabilidad puede permitirnos eludir el mensaje de autenticación básica HTTP en ciertas páginas.

***

## <mark style="color:purple;">Identificación</mark>

En el ejemplo de esta sección tenemos una aplicación web básica `File Manager`, en la que podemos agregar nuevos archivos escribiendo sus nombres y pulsando `enter`:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_tampering_add.jpg" alt=""><figcaption></figcaption></figure>

Sin embargo, supongamos que intentamos eliminar todos los archivos haciendo clic en el botón rojo `Reset`. En ese caso, vemos que esta función parece estar restringida únicamente a los usuarios autenticados, ya que aparece el siguiente mensaje: `HTTP Basic Auth`

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_tampering_reset.jpg" alt=""><figcaption></figcaption></figure>

Como no tenemos ninguna credencial nos aparecerá una página `401 Unauthorized`:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_tampering_unauthorized.jpg" alt=""><figcaption></figcaption></figure>

Entonces, veamos si podemos evitar esto con un ataque de HTTP Verb Tampering. Para ello, necesitamos identificar qué páginas están restringidas por esta autenticación. Si examinamos la solicitud HTTP después de hacer clic en el botón Reset o miramos la URL a la que nos lleva el botón después de hacer clic en él, vemos que está en `/admin/reset.php`. Por lo tanto, o bien el directorio `/admin` está restringido solo a usuarios autenticados, o solo lo está la página `/admin/reset.php`. Podemos confirmarlo visitando el directorio `/admin` y, de hecho, se nos solicita que iniciemos sesión nuevamente. Esto significa que el directorio `/admin` completo está restringido.

***

## <mark style="color:purple;">Explotación</mark>

Para intentar explotar la página, necesitamos identificar el método de solicitud HTTP que utiliza la aplicación web. Podemos interceptar la solicitud en Burp Suite y examinarla:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_tampering_unauthorized_request.jpg" alt=""><figcaption></figcaption></figure>

Como la página utiliza una solicitud `GET`, podemos enviar una solicitud `POST` y ver si la página web permite solicitudes `POST` (es decir, si la autenticación cubre las solicitudes `POST`). Para ello, podemos hacer clic derecho en la solicitud interceptada en Burp y seleccionar `Change Request Method`, y automáticamente cambiará la solicitud a una solicitud `POST`:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_tampering_change_request.jpg" alt=""><figcaption></figcaption></figure>

Una vez que lo hagamos, podemos hacer clic `Forward` y examinar la página en nuestro navegador. Lamentablemente, aún se nos solicita que iniciemos sesión y accederemos a una página `401 Unauthorized` si no proporcionamos las credenciales:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_tampering_reset.jpg" alt=""><figcaption></figcaption></figure>

Entonces, parece que las configuraciones del servidor web cubren tanto las solicitudes `GET` como las solicitudes `POST`. Sin embargo, como hemos aprendido anteriormente, podemos utilizar muchos otros métodos HTTP, en particular el método `HEAD` , que es idéntico a una solicitud `GET` pero no devuelve el cuerpo en la respuesta HTTP. Si esto tiene éxito, es posible que no recibamos ningún resultado, pero la función `reset` debería ejecutarse de todos modos, que es nuestro objetivo principal.

Para ver si el servidor acepta solicitudes `HEAD`, podemos enviarle una solicitud `OPTIONS` y ver qué métodos HTTP se aceptan, de la siguiente manera:

```shell-session
afsh4ck@kali$ curl -i -X OPTIONS http://SERVER_IP:PORT/

HTTP/1.1 200 OK
Date: 
Server: Apache/2.4.41 (Ubuntu)
Allow: POST,OPTIONS,HEAD,GET
Content-Length: 0
Content-Type: httpd/unix-directory
```

Como podemos ver, la respuesta muestra `Allow: POST,OPTIONS,HEAD,GET`, lo que significa que el servidor web acepta solicitudes `HEAD`, que es la configuración predeterminada para muchos servidores web. Por lo tanto, intentemos interceptar la solicitud `reset` nuevamente y, esta vez, usemos una solicitud `HEAD` para ver cómo la maneja el servidor web:

![Solicitud HEAD\_](https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_tampering_HEAD_request.jpg)

Una vez que cambiamos `POST` a `HEAD` y reenviamos la solicitud, veremos que ya no obtenemos un mensaje de inicio de sesión ni una página `401 Unauthorized`, sino una salida vacía, como se espera con una solicitud `HEAD`. Si volvemos a la aplicación web `File Manager`, veremos que todos los archivos se han eliminado, lo que significa que activamos correctamente la funcionalidad `Reset` sin tener acceso de administrador ni credenciales:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_tampering_after_reset.jpg" alt=""><figcaption></figcaption></figure>

Intente probar otros métodos HTTP y vea cuáles pueden eludir con éxito la solicitud de autenticación.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 94.237.63.109:51701
```

Intenta usar lo que aprendiste en esta sección para acceder a la página '`reset.php`' y eliminar todos los archivos. Una vez que se hayan eliminado todos los archivos, deberías obtener la flag.

### Primer acceso

Al acceder por el navegador llegamos al File Manager:

<figure><img src="/files/Qfl9IXaEn3AHKMrMjwze" alt=""><figcaption></figcaption></figure>

Si intentamos resetear los elementos nos salta la ventana de login y nos redirige a `/admin/reset.php`:

<figure><img src="/files/gMKoUe3eA3nMKhinxAj8" alt=""><figcaption></figcaption></figure>

### Comprobar métodos HTTP

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ curl -i -X OPTIONS http://94.237.63.109:51701/index.php
</strong><strong>
</strong>HTTP/1.1 200 OK
Date: Wed, 20 Nov 2024 15:19:06 GMT
Server: Apache/2.4.41 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 1158
Content-Type: text/html; charset=UTF-8
</code></pre>

No nos da ningún método alternativo válido. Al probar con POST nos devuelve una flag:

```shell-session
curl -i -X POST http://94.237.63.109:51701/index.php

HTTP/1.1 200 OK
Date: Wed, 20 Nov 2024 15:59:27 GMT
Server: Apache/2.4.41 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 1075
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>File Manager</title>
    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
    <link rel="stylesheet" href="./style.css">
</head>

<body>
    <div class="form-group">
        <h1>File Manager</h1>
        <form role="form" action="index.php" method="GET">
            <input type="text" class="form-control" placeholder="New File Name" name="filename">
        </form>
        <form action="admin/reset.php" method="GET">
            <input type="submit" value="Reset" class="btn btn-danger" />
        </form>
    </div>
</body>
</body>

</html>

<div></div><ul class="list-unstyled" id="file">HTB{4lw4y5_c0v3r_4ll_v3rb5}<div><h3>Available Files:<h3></div></ul>%  
```

<figure><img src="/files/oO9cW36oz4BA4RlU41GG" alt=""><figcaption></figcaption></figure>

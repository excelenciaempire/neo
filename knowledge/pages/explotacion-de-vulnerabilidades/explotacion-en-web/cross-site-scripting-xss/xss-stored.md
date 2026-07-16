
# XSS Stored

## <mark style="color:purple;">Introducción</mark>

Antes de aprender a descubrir vulnerabilidades XSS y utilizarlas para diversos ataques, primero debemos comprender los diferentes tipos de vulnerabilidades XSS y sus diferencias para saber cuál usar en cada tipo de ataque.

El primer tipo de vulnerabilidad XSS y el más crítico es `Stored XSS` o `Persistent XSS`. Si el payload XSS que inyectamos se almacena en la base de datos del back-end y se recupera al visitar la página, esto significa que nuestro ataque XSS es persistente y puede afectar a cualquier usuario que visite la página.

Esto hace que este tipo de XSS sea el más crítico, ya que afecta a una audiencia mucho más amplia, ya que cualquier usuario que visite la página sería víctima de este ataque. Además, los XSS Stored pueden no ser fáciles de eliminar y es posible que sea necesario eliminar el payload de la base de datos del back-end.

A continuación tenemos un entorno vulnerable de Hack the Box Academy para ver y practicar un ejemplo de XSS almacenado. Como podemos ver, la página web es una aplicación sencilla `To-Do List` a la que podemos agregar elementos. Podemos intentar escribir `test` y presionar Enter/Return para agregar un nuevo elemento y ver cómo lo maneja la página:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_stored_xss.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, nuestra entrada se mostró en la página. Si no se aplicó ningún tipo de sanitización o filtrado al input, la página podría ser vulnerable a XSS.

***

## <mark style="color:purple;">Payload de prueba XSS</mark>

Podemos probar si la página es vulnerable a XSS con la siguiente carga útil XSS básica:

```html
<script>alert(window.origin)</script>
```

Usamos este payload porque es un método muy fácil de detectar para saber cuándo se ha ejecutado correctamente nuestro payload XSS. Supongamos que la página permite cualquier entrada y no realiza ningún tipo de limpieza en ella. En ese caso, la alerta debería aparecer con la URL de la página en la que se está ejecutando, directamente después de que ingresemos nuestro payload o cuando actualicemos la página:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_stored_xss_alert.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, efectivamente recibimos la alerta, lo que significa que la página es vulnerable a XSS, ya que nuestro payload se ejecutó correctamente. Podemos confirmarlo aún más mirando el código fuente de la página con \[ `CTRL+U`] o haciendo clic derecho y seleccionando `View Page Source`, y deberíamos ver nuestro payload en el código fuente de la página:

```html
<div></div><ul class="list-unstyled" id="todo"><ul><script>alert(window.origin)</script>
</ul></ul>
```

{% hint style="info" %}
**Consejo**: Muchas aplicaciones web modernas utilizan iframe entre dominios para gestionar la entrada del usuario, de modo que incluso si el formulario web es vulnerable a XSS, no sería una vulnerabilidad en la aplicación web principal. Es por eso que mostramos el valor de `window.origin`en el cuadro de alerta, en lugar de un valor estático como `1`. En este caso, el cuadro de alerta revelaría la URL en la que se está ejecutando y confirmaría qué formulario es el vulnerable, en caso de que se estuviera utilizando un iframe.
{% endhint %}

Como algunos navegadores modernos pueden bloquear la función JavaScript `alert()` en ubicaciones específicas, puede ser útil conocer algunos payloads útiles XSS básicos para verificar la existencia de XSS. Una de esos payloads XSS es `<plaintext>`, que dejará de mostrar el código HTML que viene después y lo mostrará como texto sin formato. Otro payload fácil de detectar es `<script>print()</script>` que hará aparecer el cuadro de diálogo de impresión del navegador, que es poco probable que esté bloqueado por ningún navegador. Intente usar estos payloads para ver cómo funciona cada una. Puede usar el botón de reinicio para eliminar cualquier payload actual.

Para comprobar si el payload es persistente y está almacenada en el back-end, podemos actualizar la página y ver si volvemos a recibir la alerta. Si lo hacemos, veremos que seguimos recibiendo la alerta incluso después de actualizar la página, lo que confirma que se trata de una vulnerabilidad `Stored/Persistent XSS`. Esto no es exclusivo de nosotros, ya que cualquier usuario que visite la página activará el payload XSS y recibirá la misma alerta.

***

## Caso práctico

```
Objetivo: 94.237.58.170:33603
```

Para obtener la flag, useel mismo payload que usamos anteriormente, pero cambie su código JavaScript para mostrar la cookie en lugar de mostrar la URL.

```html
<script>alert(document.cookie)</script>
```

<figure><img src="/files/Q3FQfwpDjmYy1jPlZSGM" alt=""><figcaption></figcaption></figure>

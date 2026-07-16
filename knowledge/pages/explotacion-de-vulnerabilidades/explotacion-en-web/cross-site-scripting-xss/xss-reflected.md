
# XSS Reflected

Existen dos tipos de vulnerabilidades `Non-Persistent XSS`: `Reflected XSS`, que es procesada por el servidor back-end, y `DOM-based XSS`, que es procesada completamente en el lado del cliente y nunca llega al servidor back-end. A diferencia de los XSS persistentes, las vulnerabilidades `Non-Persistent XSS` son temporales y no persisten hasta que se actualiza la página. Por lo tanto, nuestros ataques solo afectan al usuario objetivo y no afectarán a otros usuarios que visiten la página.

Las vulnerabilidades `Reflected XSS` ocurren cuando nuestra entrada llega al servidor back-end y nos es devuelta sin ser filtrada o saneada. Hay muchos casos en los que nuestra entrada completa puede ser devuelta a nosotros, como mensajes de error o mensajes de confirmación. En estos casos, podemos intentar usar payloads XSS para ver si se ejecutan. Sin embargo, como estos suelen ser mensajes temporales, una vez que nos movemos de la página, no se ejecutarán nuevamente y, por lo tanto, son `Non-Persistent`.

Vamos a usar el entorno de pruebas de Hack the Box Academy para esta sección. Es una aplicación `To-Do List` similar a la que usamos en la sección anterior. Podemos intentar agregar cualquier cadena `test` para ver cómo se maneja:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_reflected_1.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, obtenemos `Task 'test' could not be added.`, que incluye nuestra entrada `test` como parte del mensaje de error. Si nuestra entrada no se filtró ni se saneó, la página podría ser vulnerable a XSS. Podemos probar el mismo payload XSS que usamos en la sección anterior y hacer clic en `Add`:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_reflected_2.jpg" alt=""><figcaption></figcaption></figure>

Una vez que hacemos clic `Add`, aparece la alerta emergente:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_stored_xss_alert.jpg" alt=""><figcaption></figcaption></figure>

En este caso, vemos que el mensaje de error ahora dice `Task '' could not be added.`. Dado que nuestro payload está envuelto con una etiqueta `<script>`, el navegador no la procesa, por lo que obtenemos comillas simples vacías `''` en su lugar. Podemos volver a ver el código fuente de la página para confirmar que el mensaje de error incluye nuestro payload XSS:

```html
<div></div><ul class="list-unstyled" id="todo"><div style="padding-left:25px">Task '<script>alert(window.origin)</script>' could not be added.</div></ul>
```

Como podemos ver, las comillas simples efectivamente contienen nuestro payload XSS `'<script>alert(window.origin)</script>'`.

Si visitamos la página `Reflected` nuevamente, el mensaje de error ya no aparece y nuestro payload XSS no se ejecuta, lo que significa que esta vulnerabilidad XSS es efectivamente `Non-Persistent`.

`Pero si la vulnerabilidad XSS no es persistente, ¿cómo atacaríamos a las víctimas?`

Esto depende de qué petición HTTP se utilice para enviar nuestra entrada al servidor. Podemos comprobarlo a través de Firefox `Developer Tools` con \[ `CTRL+I`] y seleccionando la pestaña `Network`. Luego, podemos volver a poner nuestro payload `test` y hacer clic `Add` para enviarlo:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_reflected_network.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, la primera fila muestra que nuestra solicitud era una solicitud `GET`. La solicitud `GET` envía sus parámetros y datos como parte de la URL. Por lo tanto, `para dirigirnos a un usuario, podemos enviarle una URL que contenga nuestro payload`. Para obtener la URL, podemos copiar la URL de la barra de URL en Firefox después de enviar nuestro payload XSS, o podemos hacer clic derecho en la solicitud `GET` en la pestaña `Network` y seleccionar `Copy>Copy URL`. Una vez que la víctima visita esta URL, la carga XSS se ejecutará:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_stored_xss_alert.jpg" alt=""><figcaption></figcaption></figure>

***

## Caso práctico

```
Objetivo: 94.237.58.170:33603
```

Para obtener la flag, use el mismo payload que usamos anteriormente, pero cambie su código JavaScript para mostrar la cookie en lugar de mostrar la URL.

```html
<script>alert(document.cookie)</script>
```

<figure><img src="/files/KLv0kzLBc64PecDKMmLU" alt=""><figcaption></figcaption></figure>

SI vemos el código fuente vemos que se ha inyectado correctamente:

<figure><img src="/files/6ZwyiOXNds9DmzqAYi3e" alt=""><figcaption></figcaption></figure>

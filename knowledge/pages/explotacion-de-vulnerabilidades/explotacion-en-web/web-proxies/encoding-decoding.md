
# Encoding / Decoding

A medida que modificamos y enviamos solicitudes HTTP personalizadas, es posible que tengamos que realizar varios tipos de codificación y decodificación para interactuar correctamente con el servidor web. Ambas herramientas tienen codificadores integrados que pueden ayudarnos a codificar y decodificar rápidamente varios tipos de texto.

***

## <mark style="color:purple;">Codificación de URL</mark>

Es esencial garantizar que los datos de nuestra solicitud estén codificados en la URL y que los encabezados de la solicitud estén configurados correctamente. De lo contrario, podemos recibir un error de servidor en la respuesta. Por eso, la codificación y decodificación de datos se vuelve esencial a medida que modificamos y repetimos solicitudes web. Algunos de los caracteres clave que necesitamos codificar son:

* `Espacios`: Puede indicar el final de los datos de la solicitud si no están codificados
* `&`: De lo contrario, se interpreta como un delimitador de parámetros.
* `#`: De lo contrario, se interpreta como un identificador de fragmento.

Para codificar texto en formato URL en Burp Repeater, podemos seleccionar ese texto y hacer clic derecho sobre él, luego seleccionar ( `Convert Selection > URL > URL encode key characters`), o seleccionar el texto y hacer clic en \[ `CTRL+U`]. Burp también admite la codificación de URL mientras escribimos si hacemos clic derecho y habilitamos esa opción, lo que codificará todo nuestro texto a medida que lo escribimos. Por otro lado, ZAP debería codificar automáticamente en formato URL todos los datos de nuestra solicitud en segundo plano antes de enviar la solicitud, aunque es posible que no lo veamos explícitamente.

Existen otros tipos de codificación de URL, como `Full URL-Encoding` o `Unicode URL`, que también pueden resultar útiles para solicitudes con muchos caracteres especiales.

***

## <mark style="color:purple;">Decodificación</mark>

Si bien la codificación de URL es fundamental para las solicitudes HTTP, no es el único tipo de codificación que encontraremos. Es muy común que las aplicaciones web codifiquen sus datos, por lo que deberíamos poder decodificarlos rápidamente para examinar el texto original. Por otro lado, los servidores back-end pueden esperar que los datos se codifiquen en un formato particular o con un codificador específico, por lo que debemos poder codificar rápidamente nuestros datos antes de enviarlos.

Los siguientes son algunos de los otros tipos de codificadores compatibles con ambas herramientas:

* `HTML`
* `Unicode`
* `Base64`
* `ASCII hex`

Para acceder al codificador completo en Burp, podemos ir a la pestaña `Decoder` . En ZAP, podemos utilizarlo haciendo clic en `Encoder/Decoder/Hash` o \[ `CTRL+E`]. Con estos codificadores, podemos introducir cualquier texto y codificarlo o decodificarlo rápidamente. Por ejemplo, tal vez nos encontramos con la siguiente cookie que está codificada en base64 y necesitamos decodificarla: `eyJ1c2VybmFtZSI6Imd1ZXN0IiwgImlzX2FkbWluIjpmYWxzZX0=`

Podemos ingresar la cadena anterior en Burp Decoder y seleccionar `Decode as > Base64`, y obtendremos el valor decodificado:

![Descodificación de Burp B64](https://academy.hackthebox.com/storage/modules/110/burp_b64_decode.jpg)

En versiones recientes de Burp, también podemos utilizar la herramienta `Burp Inspector` para realizar codificaciones y decodificaciones (entre otras cosas), las cuales podemos encontrar en varios lugares como `Burp Proxy` o `Burp Repeater`:

![Inspector de eructos](https://academy.hackthebox.com/storage/modules/110/burp_inspector.jpg)

En ZAP, podemos utilizar la herramienta `Encoder/Decoder/Hash`, que decodificará automáticamente cadenas utilizando varios decodificadores en la pestaña `Decode`:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/110/zap_b64_decode.jpg" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**Consejo**: Podemos crear pestañas personalizadas en el Codificador/Decodificador/Hash de ZAP con el botón "Agregar nueva pestaña", y luego podemos agregar cualquier tipo de codificador/decodificador en el que queramos que se muestre el texto. Intente crear su propia pestaña con algunos codificadores/decodificadores.
{% endhint %}

***

## <mark style="color:purple;">Codificación</mark>

Como podemos ver, el texto contiene el valor `{"username":"guest", "is_admin":false}`. Por lo tanto, si estuviéramos realizando una prueba de penetración en una aplicación web y descubriéramos que la cookie contiene este valor, podríamos querer probar modificándola para ver si cambia nuestros privilegios de usuario. Por lo tanto, podemos copiar el valor anterior, cambiarlo de `guest` a `admin` y `false` a `true`, e intentar codificarlo nuevamente utilizando su método de codificación original ( `base64`):

![Codificación Burp B64](https://academy.hackthebox.com/storage/modules/110/burp_b64_encode.jpg)

![Codificación ZAP B64](https://academy.hackthebox.com/storage/modules/110/zap_b64_encode.jpg)

{% hint style="info" %}
**Consejo**: la salida de Burp Decoder se puede codificar o decodificar directamente con un codificador diferente. Seleccione el nuevo método de codificación en el panel de salida en la parte inferior y se codificará o decodificará nuevamente. En ZAP, podemos copiar el texto de salida y pegarlo en el campo de entrada de arriba.
{% endhint %}

Luego podemos copiar la cadena codificada en base64 y usarla con nuestra solicitud en Burp `Repeater` o ZAP `Request Editor`. El mismo concepto se puede utilizar para codificar y decodificar varios tipos de texto codificado para realizar pruebas de penetración web efectivas sin utilizar otras herramientas para realizar la codificación.

***

## Ejercicio

La cadena que se encuentra en el archivo adjunto se ha codificado varias veces con distintos codificadores. Intente utilizar las herramientas de decodificación que analizamos para decodificarla y obtener la flag.

Esta es la cadena que tenemos que decodificar:

{% code overflow="wrap" %}

```
VTJ4U1VrNUZjRlZXVkVKTFZrWkdOVk5zVW10aFZYQlZWRmh3UzFaR2NITlRiRkphWld0d1ZWUllaRXRXUm10M1UyeFNUbVZGY0ZWWGJYaExWa1V3ZVZOc1VsZGlWWEJWVjIxNFMxWkZNVFJUYkZKaFlrVndWVmR0YUV0V1JUQjNVMnhTYTJGM1BUMD0=
```

{% endcode %}

Vamos a ir decodificándolo por fases con Burpsuite:

<figure><img src="/files/tZ7WPAyJ3MNOnzOL7htL" alt=""><figcaption></figcaption></figure>

Obtenemos la primera cadena de texto y decodificamos el resto de nuevo en base 64:

```
{"username":"guest", "is_admin":false}
```

<figure><img src="/files/0eO9Yx0pbAvkgLiofNVO" alt=""><figcaption></figcaption></figure>

Y una vez más:

<figure><img src="/files/w1Am7StVA2YWNdBb4buI" alt=""><figcaption></figcaption></figure>

Y otra vez:

<figure><img src="/files/mp8Gd9h8EV5J7AsCu7OG" alt=""><figcaption></figcaption></figure>

Aquí vemos que mete caracteres distintos en la cadena de texto, como `%` por ejemplo, lo que nos indica que en vez de decodificarlo como `base64` vamos a cambiar el tipo de decodificación a `URL`

<figure><img src="/files/mCLOtkaqT7ezZ7ckm8cF" alt=""><figcaption></figcaption></figure>

Y como veis obtenemos la flag! 🏆

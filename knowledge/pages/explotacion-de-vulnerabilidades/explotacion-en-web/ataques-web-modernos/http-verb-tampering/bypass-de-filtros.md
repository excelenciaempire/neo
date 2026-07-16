
# Bypass de Filtros

El otro tipo de vulnerabilidad de manipulación de verbos HTTP, más común, se debe a errores cometidos durante el desarrollo de la aplicación web, que hacen que esta no cubra todos los métodos HTTP en determinadas funcionalidades. Esto se encuentra comúnmente en los filtros de seguridad que detectan solicitudes maliciosas. Por ejemplo, si se estaba utilizando un filtro de seguridad para detectar vulnerabilidades de inyección y solo se buscaban inyecciones en parámetros `POST` (por ejemplo, `$_POST['parameter']`), es posible que se pueda evitar simplemente cambiando el método de solicitud a `GET`.

***

## <mark style="color:purple;">Identificación</mark>

En la aplicación web `File Manager`, si intentamos crear un nuevo nombre de archivo con caracteres especiales en su nombre (por ejemplo `test;`), obtenemos el siguiente mensaje:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_malicious_request.jpg" alt=""><figcaption></figcaption></figure>

Este mensaje muestra que la aplicación web utiliza ciertos filtros en el back-end para identificar intentos de inyección y luego bloquea cualquier solicitud maliciosa. Independientemente de lo que intentemos, la aplicación web bloquea correctamente nuestras solicitudes y está protegida contra intentos de inyección. Sin embargo, podemos intentar un ataque HTTP Verb Tampering para ver si podemos eludir el filtro de seguridad por completo.

***

## <mark style="color:purple;">Explotación</mark>

Para intentar explotar esta vulnerabilidad, interceptemos la solicitud en Burp Suite (Burp) y la cambiamos por otro método:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_tampering_GET_request.jpg" alt=""><figcaption></figcaption></figure>

Esta vez no recibimos el mensaje `Malicious Request Denied!` y nuestro archivo se creó correctamente:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_tampering_injected_request.jpg" alt=""><figcaption></figcaption></figure>

Para confirmar si hemos pasado por alto el filtro de seguridad, debemos intentar explotar la vulnerabilidad que el filtro está protegiendo: una vulnerabilidad de inyección de comandos, en este caso. Por lo tanto, podemos inyectar un comando que cree dos archivos y luego verificar si ambos archivos se crearon. Para ello, utilizaremos el siguiente nombre de archivo en nuestro ataque

```
file1; touch file2;
```

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_tampering_filter_bypass.jpg" alt=""><figcaption></figcaption></figure>

Luego, podemos volver a cambiar el método de solicitud a una solicitud `GET`:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_tampering_filter_bypass_request.jpg" alt=""><figcaption></figcaption></figure>

Una vez que enviamos nuestra solicitud, vemos que esta vez se crearon tanto `file1` como `file2`  :

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_verb_tampering_after_filter_bypass.jpg" alt=""><figcaption></figcaption></figure>

Esto demuestra que hemos logrado eludir el filtro mediante una vulnerabilidad HTTP Verb Tampering y hemos logrado la inyección de comandos. Sin la vulnerabilidad HTTP Verb Tampering, la aplicación web podría haber estado protegida contra ataques de inyección de comandos, y esta vulnerabilidad nos permitió eludir por completo los filtros implementados.

***

## Caso práctico

```
Objetivo: 94.237.61.202:41131
```

Para obtener la flag, intente omitir el filtro de inyección de comandos a través de HTTP Verb Tampering, mientras usa el siguiente nombre de archivo: `file; cp /flag.txt ./`

Al intentar ejecutar un comando como hemos visto en la sección nos da un error de validación:

<figure><img src="/files/F1CwsxxCSDpaIOuNPCPX" alt=""><figcaption></figcaption></figure>

Vamos a interceptar la petición con BurpSuite y campiar el request method a POST. Una vez hecho esto le damos a forward para enviar la petición:

<figure><img src="/files/2bPFXPBSrnDSNzvKSXxd" alt=""><figcaption></figcaption></figure>

Observamos que funciona y se ha copiado la flag al directorio `/`, pudiendo leerla desde el navegador:

<figure><img src="/files/qI54WYLPAARfwdvqYA0V" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/jMY1Aply5WJe0IBdMcdT" alt=""><figcaption></figcaption></figure>

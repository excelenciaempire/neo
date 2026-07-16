
# Burp Intruder

Tanto Burp como ZAP proporcionan funciones adicionales además del proxy web predeterminado, que son esenciales para las pruebas de penetración de aplicaciones web. Dos de las funciones adicionales más importantes son los `web fuzzers` y `web scanners`. Los fuzzers web integrados son herramientas potentes que actúan como herramientas de fuzzing web, enumeración y fuerza bruta. Esto también puede actuar como una alternativa para muchos de los fuzzers basados ​​en CLI que utilizamos, como `dirsearch`, `ffuf`, `dirbuster`, `gobuster`, `wfuzz`, entre otros.

El fuzzer web de Burp se llama `Burp Intruder` y se puede usar para fuzzear páginas, directorios, subdominios, parámetros, valores de parámetros y muchas otras cosas. Aunque es mucho más avanzado que la mayoría de las herramientas de fuzzing web basadas en CLI, la versión gratuita `Burp Community` está limitada a una velocidad de `1 solicitud por segundo`, lo que la hace extremadamente lenta en comparación con las herramientas de fuzzing web basadas en CLI, que generalmente pueden leer hasta `10k` solicitudes por segundo. Es por eso que solo usaríamos la versión gratuita de Burp Intruder para consultas cortas. La versión `Pro` tiene velocidad ilimitada, que puede rivalizar con las herramientas de fuzzing web comunes, además de las características muy útiles de Burp Intruder. Esto la convierte en una de las mejores herramientas de fuzzing web y fuerza bruta.

En esta sección, demostraremos los diversos usos de Burp Intruder para fuzzing y enumeración web.

***

## <mark style="color:purple;">Objetivo</mark>

Como es habitual, iniciaremos Burp y su navegador preconfigurado y luego visitaremos la aplicación web del ejercicio que se encuentra al final de esta sección. Una vez que lo hagamos, podemos ir al historial de proxy, ubicar nuestra solicitud, hacer clic derecho en la solicitud y seleccionar `Send to Intruder`, o usar el acceso directo \[ `CTRL+I`] para enviarla a `Intruder`.

Luego podemos hacker click en la pestaña `Intruder` o con el acceso directo \[ `CTRL+SHIFT+I`], que nos lleva directamente a `Burp Intruder`:

![objetivo\_intruso](https://academy.hackthebox.com/storage/modules/110/burp_intruder_target.jpg)

En la primera pestaña, ' `Target`', vemos los detalles del objetivo que vamos a fuzzear, que se alimenta de la solicitud que enviamos a `Intruder`.

***

## <mark style="color:purple;">Posiciones</mark>

La segunda pestaña, ' `Positions`', es donde colocamos el puntero de posición de la carga útil, que es el punto donde se colocarán las palabras de nuestra lista de palabras y se repetirán. Demostraremos cómo realizar un análisis fuzzing de directorios web, que es similar a lo que hacen herramientas como `ffuf`o `gobuster`.

Para comprobar si existe un directorio web, nuestro fuzzing debe estar en ' `GET /DIRECTORY/`', de modo que las páginas existentes devuelvan `200 OK`, de lo contrario obtendremos `404 NOT FOUND`. Por lo tanto, necesitaremos seleccionar `DIRECTORY` como posición de carga útil, ya sea envolviéndola con `§`o seleccionando la palabra `DIRECTORY` y haciendo clic en el botón `Add §`:

![posición del intruso](https://academy.hackthebox.com/storage/modules/110/burp_intruder_position.jpg)

{% hint style="info" %}
**Consejo**: `DIRECTORY`en este caso es el nombre del puntero, que puede ser cualquier cosa, y se puede usar para hacer referencia a cada puntero, en caso de que estemos usando más de una posición con diferentes listas de palabras para cada uno.
{% endhint %}

Lo último que hay que seleccionar en la pestaña de destino es el `Attack Type`. El tipo de ataque define cuántos punteros de carga útil se utilizan y determina qué carga útil se asigna a qué posición. Para simplificar, nos ceñiremos al primer tipo, `Sniper`, que utiliza solo una posición. Prueba a hacer clic en el `?`en la parte superior de la ventana para leer más sobre los tipos de ataque o consulta este [enlace](https://portswigger.net/burp/documentation/desktop/tools/intruder/positions#attack-type) .

{% hint style="warning" %}
**Nota**: Asegúrese de dejar las dos líneas adicionales al final de la solicitud, de lo contrario, podríamos recibir una respuesta de error del servidor.
{% endhint %}

***

## <mark style="color:purple;">Payloads</mark>

En la tercera pestaña, ' `Payloads`', podemos elegir y personalizar nuestras cargas útiles/listas de palabras. Esta carga útil/lista de palabras es lo que se iteraría, y cada elemento/línea de la misma se colocaría y probaría uno por uno en la posición de carga útil que elegimos anteriormente. Hay cuatro cosas principales que debemos configurar:

* `Payload Sets`
* `Opciones de Payload`
* `Procesamiento de Payload`
* `Codificación de Payload`

### **Payload Sets**

Lo primero que debemos configurar es el `Payload Set` o conjunto de payloads que identifica el número de Payload, dependiendo del tipo de ataque y del número de Payloads que utilizamos en los Punteros de Posición de Payload:

![Conjuntos de carga útil](https://academy.hackthebox.com/storage/modules/110/burp_intruder_payload_set.jpg)

En este caso, solo tenemos un Payload Set, ya que elegimos el tipo de ataque '`Sniper` ' con una sola posición de carga útil. Si elegimos el tipo de ataque ' `Cluster Bomb`', por ejemplo, y agregamos varias posiciones de carga útil, obtendremos más conjuntos de carga útil para elegir y elegiremos diferentes opciones para cada uno. En nuestro caso, seleccionaremos el conjunto `1` de Payload.

A continuación, debemos seleccionar el `Payload Type` o tipo de cargas útiles o listas de palabras que utilizaremos. Burp ofrece una variedad de tipos de cargas útiles, cada uno de los cuales actúa de una determinada manera. Por ejemplo:

* `Simple List`: El tipo básico y más fundamental. Proporcionamos una lista de palabras e Intruder itera sobre cada línea que contiene.
* `Runtime file`: Similar a `Simple List`, pero se carga línea por línea a medida que se ejecuta el escaneo para evitar el uso excesivo de memoria por parte de Burp.
* `Character Substitution`: Nos permite especificar una lista de caracteres y sus reemplazos, y Burp Intruder prueba todas las permutaci122
*
* 10ones potenciales.

Hay muchos otros tipos de carga útil, cada u1no con sus propias opciones, y muchos de los cuales pueden crear listas de palabras personaliz12adas para cada ataque. Intente hacer clic en junto `?` a `Payload Sets` y luego en `Payload Type` para obtener más información sobre cada tipo de carga útil. En nuestro caso, utilizaremos un tipo de carga útil básico `Simple List`.

### **Opciones de Payload**

A continuación, debemos especificar las Opciones de carga útil, que son diferentes para cada tipo de carga útil que seleccionemos en `Payload Sets`. Para un `Simple List`, tenemos que crear o cargar una lista de palabras. Para ello, podemos introducir cada elemento manualmente haciendo clic en `Add`, lo que crearía nuestra lista de palabras sobre la marcha. La otra opción más común es hacer clic en `Load` y, a continuación, seleccionar un archivo para cargar en Burp Intruder.

Seleccionaremos nuestra lista de palabras `/usr/share/seclists/Discovery/Web-Content/common.txt`. Podemos ver que Burp Intruder carga todas las líneas de nuestra lista de palabras en la tabla de Opciones de carga útil:

![Opciones de carga útil](https://academy.hackthebox.com/storage/modules/110/burp_intruder_payload_wordlist.jpg)

Podemos agregar otra lista de palabras o agregar manualmente algunos elementos, que se agregarán a la misma lista de elementos. Podemos usar esto para combinar varias listas de palabras o crear listas de palabras personalizadas. En Burp Pro, también podemos seleccionar de una lista de listas de palabras existentes contenidas en Burp eligiendo la opción del menú `Add from list`.

Consejo: en caso de que quieras utilizar una lista de palabras muy grande, es mejor utilizar `Runtime file` como Tipo de carga útil en lugar de `Simple List`, para que Burp Intruder no tenga que cargar la lista de palabras completa por adelantado, lo que puede limitar el uso de memoria.

### **Procesamiento de Payload**

Otra opción que podemos aplicar es `Payload Processing`, que nos permite determinar reglas de fuzzing sobre la lista de palabras cargada. Por ejemplo, si quisiéramos agregar una extensión después de nuestro elemento de carga útil, o si quisiéramos filtrar la lista de palabras en función de criterios específicos, podemos hacerlo con el procesamiento de carga útil.

Intentemos agregar una regla que omita todas las líneas que comiencen con a `.`(como se muestra en la captura de pantalla de la lista de palabras anterior). Podemos hacerlo haciendo clic en el botón `Add` y luego seleccionando `Skip if matches regex`, lo que nos permite proporcionar un patrón de expresión regular para los elementos que queremos omitir. Luego, podemos proporcionar un patrón de expresión regular que coincida con las líneas que comiencen con `.`, que es `^\..*$`:

![Procesamiento de Payload](https://academy.hackthebox.com/storage/modules/110/burp_intruder_payload_processing_1.jpg)

Podemos ver que nuestra regla se agrega y habilita:

<figure><img src="https://academy.hackthebox.com/storage/modules/110/burp_intruder_payload_processing_2.jpg" alt=""><figcaption></figcaption></figure>

### **Codificación de Payload**

La cuarta y última opción que podemos aplicar es `Payload Encoding`, que nos permite habilitar o deshabilitar la codificación de URL de carga útil.

![](https://academy.hackthebox.com/storage/modules/110/burp_intruder_payload_encoding.jpg)

Lo dejaremos habilitado.

***

## <mark style="color:purple;">Opciones</mark>

Por último, podemos personalizar nuestras opciones de ataque desde la pestaña `Options`. Hay muchas opciones que podemos personalizar (o dejar por defecto) para nuestro ataque. Por ejemplo, podemos establecer el número de `retried on failure` y `pause before retry` en 0.

Otra opción útil es la `Grep - Match`, que nos permite marcar solicitudes específicas según sus respuestas. Como estamos haciendo fuzzing en directorios web, solo nos interesan las respuestas con código HTTP `200 OK`. Por lo tanto, primero la habilitaremos y luego haremos click en `Clear` para borrar la lista actual. Después de eso, podemos escribir `200 OK` para que coincida con cualquier solicitud con esta cadena y hacer click en `Add` para agregar la nueva regla. Finalmente, también deshabilitaremos `Exclude HTTP Headers`, ya que lo que buscamos está en el encabezado HTTP:

![](https://academy.hackthebox.com/storage/modules/110/burp_intruder_options_match.jpg)

También podemos utilizar esta opción `Grep - Extract`, que resulta útil si las respuestas HTTP son extensas y solo nos interesa una parte determinada de la respuesta. Esto nos ayuda a mostrar solo una parte específica de la respuesta. Solo buscamos respuestas con código HTTP `200 OK`, independientemente de su contenido, por lo que no optaremos por esta opción.

Pruebe otras opciones de `Intruder` y 21utilice la ayuda de Burp haciendo clic en `?` junto a cada una para obtener más información sobre210ada opción.

{% hint style="info" %}
**Nota**: También podemos usar la pestaña `Resource Pool` para especificar cuántos recursos de red usará Intruder, lo que puede resultar útil para ataques muy grandes. Para nuestro ejemplo, la dejaremos con sus valores predeterminados.
{% endhint %}

***

## <mark style="color:purple;">Ataque</mark>

Ahora que todo está configurado correctamente, podemos hacer clic en el botón `Start Attack` y esperar a que finalice nuestro ataque. Una vez más, en la versión gratuita `Community Version`, estos ataques serían muy lentos y tomarían una cantidad considerable de tiempo para listas de palabras más largas.

Lo primero que notaremos es que se han omitido todas las líneas que comienzan con `.` y comenzamos directamente con las líneas posteriores:

![](https://academy.hackthebox.com/storage/modules/110/burp_intruder_attack_exclude.jpg)

También podemos ver la columna `200 OK`, que muestra las solicitudes que coinciden con el `200 OK`valor de grep que especificamos en la pestaña Opciones. Podemos hacer clic en ella para ordenar por ella, de modo que tengamos los resultados coincidentes en la parte superior. De lo contrario, podemos ordenar por `status` o por `Length`. Una vez que finaliza nuestro escaneo, vemos que obtenemos un resultado `/admin`:

![ataque de intruso](https://academy.hackthebox.com/storage/modules/110/burp_intruder_attack.jpg)

Ahora podemos visitar manualmente la página `<http://SERVER_IP:PORT/admin/>` para asegurarnos de que existe.

De manera similar, podemos usar `Burp Intruder` para realizar cualquier tipo de fuzzing web y fuerza bruta, incluyendo fuerza bruta para contraseñas, o fuzzing para ciertos parámetros PHP, etc. Incluso podemos usar `Intruder` para realizar rociado de contraseñas contra aplicaciones que usan autenticación de Active Directory (AD), como Outlook Web Access (OWA), portales SSL VPN, Servicios de Escritorio Remoto (RDS), Citrix, aplicaciones web personalizadas que usan autenticación AD, y más. Sin embargo, como la versión gratuita de ZAP `Intruder` está extremadamente limitada, en la siguiente sección, veremos el fuzzer de ZAP y sus diversas opciones, que no tienen un nivel de pago.

Para ver otras herramientas de fuzzing automáticas más potentes le puedes echar un ojo a la sección:

{% content-ref url="/pages/zIAtmEU0cp7fFcQmTGan" %}
[Fuzzing](/ethical-hacking-cheatsheet/recopilacion-de-informacion/fuzzing.md)
{% endcontent-ref %}


# Zap Fuzzer

El fuzzer de ZAP se llama ( `ZAP Fuzzer`). Puede ser muy potente para fuzzear varios puntos finales web, aunque carece de algunas de las características proporcionadas por Burp Intruder. Sin embargo, ZAP Fuzzer no limita la velocidad del fuzzing, lo que lo hace mucho más útil que el Intruder gratuito de Burp.

En esta sección, intentaremos replicar lo que hicimos en la sección anterior usando ZAP Fuzzer para tener una comparación y decidir cuál nos gusta más.

***

## <mark style="color:purple;">Fuzzing</mark>

Para comenzar con el fuzzing, visitaremos la URL del ejercicio que se encuentra al final de esta sección para capturar una solicitud de muestra. Como realizaremos el fuzzing en directorios, visitaremos `<http://SERVER_IP:PORT/test/>` para ubicar nuestra ubicación de fuzzing `test` más adelante. Una vez que localicemos nuestra solicitud en el historial del proxy, haremos clic derecho sobre ella y seleccionaremos ( `Attack > Fuzz`), lo que abrirá la ventana `Fuzzer`:

![](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer.jpg)

Las principales opciones que necesitamos configurar para nuestro ataque Fuzzer son:

* `Ubicación de Fuzz`
* `Payloads`
* `Procesadores`
* `Opciones`

Intentemos configurarlos para nuestro ataque de fuzzing de directorios web.

***

## <mark style="color:purple;">Ubicaciones</mark>

El `Fuzz Location` es muy similar a `Intruder Payload Position`, donde se colocarán nuestros payloads. Para colocar nuestra ubicación en una palabra determinada, podemos seleccionarla y hacer clic en el botón `Add` del panel derecho. Entonces, seleccionemos `test` y hagamos clic en `Add`:

![procesamiento de carga útil](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_add.jpg)

Como podemos ver, esto colocó un marcador `verde` en nuestra ubicación seleccionada y abrió la ventana `Payloads` para que configuremos nuestros payloads.

***

## <mark style="color:purple;">Payloads</mark>

Los payloads de ataque en Fuzzer de ZAP son similares en concepto a los payloads de Intruder, aunque no son tan avanzadas como las de Intruder. Podemos hacer click en el botón `Add` para agregar nuestros payloads y seleccionar entre 8 tipos de payloads diferentes. A continuación, se muestran algunos de ellos:

* `File`: Esto nos permite seleccionar una lista de palabras cómo payload.
* `File Fuzzers`: Esto nos permite seleccionar listas de palabras de bases de datos integradas de listas de palabras.
* `Numberzz`: Genera secuencias de números con incrementos personalizados.

<figure><img src="/files/PwJn7HK13zWxhTm9V7Ek" alt=""><figcaption></figcaption></figure>

Una de las ventajas de ZAP Fuzzer es que tiene listas de palabras integradas entre las que podemos elegir, de modo que no tenemos que proporcionar nuestra propia lista de palabras. Se pueden instalar más bases de datos desde ZAP Marketplace, como veremos en una sección posterior. Por lo tanto, podemos seleccionar `File Fuzzers` como `Type`, y luego seleccionaremos la primera lista de palabras de `dirbuster`:

![](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_add_payload.jpg)

Una vez que hacemos clic en el botón `Add`, se agregará nuestra lista de palabras cómo payload y podremos examinarla con el botón `Modify`.

***

## <mark style="color:purple;">Procesadores</mark>

También podemos querer realizar algún procesamiento en cada palabra de nuestra lista de palabras de payload. Los siguientes son algunos de los procesadores de payload que podemos utilizar:

* `Decodificación/codificación Base64`
* `Hash MD5`
* `Cadena de sufijo`
* `Cadena de prefijo`
* `Hash SHA-1/256/512`
* `Decodificación/codificación de URL`
* `Script`

Como podemos ver, tenemos una variedad de codificadores y algoritmos de hash para elegir. También podemos agregar una cadena personalizada antes del payload con `Prefix String` o una cadena personalizada con `Postfix String`. Finalmente, el tipo `Script` nos permite seleccionar un script personalizado que creamos y ejecutamos en cada carga útil antes de usarlo en el ataque.

Seleccionaremos el procesador `URL Encode` para nuestro ejercicio para asegurarnos de que nuestro payload se codifique correctamente y evitar errores del servidor si nuestro payload contiene caracteres especiales. Podemos hacer clic en el botón `Generate Preview` para obtener una vista previa de cómo se verá nuestra carga útil final en la solicitud:

![](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_add_processor.jpg)

Una vez hecho esto, podemos hacer clic en `Add` para agregar el procesador y hacer clic `Ok` en las ventanas de procesadores y payloads para cerrarlas.

***

## <mark style="color:purple;">Opciones</mark>

Por último, podemos configurar algunas opciones para nuestros fuzzers, de forma similar a lo que hicimos con Burp Intruder. Por ejemplo, podemos configurar el `Concurrent threads per scan` en `20`, para que nuestro análisis se ejecute muy rápido:

![](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_options.jpg)

La cantidad de subprocesos que configuremos puede estar limitada por la potencia de procesamiento de la computadora que queramos utilizar o por la cantidad de conexiones que el servidor nos permita establecer.

También podemos optar por ejecutar a través de los payloads `Depth first`, lo que intentaría todas las palabras de la lista de palabras en una sola posición de payload antes de pasar a la siguiente (por ejemplo, probar todas las contraseñas para un solo usuario antes de empezar el bruteforce del siguiente usuario). También podríamos usar `Breadth first`, que ejecutaría cada palabra de la lista de palabras en todas las posiciones de carga útil antes de pasar a la siguiente palabra (por ejemplo, intentar todas las contraseñas para todos los usuarios antes de pasar a la siguiente contraseña).

***

## <mark style="color:purple;">Comenzar</mark>

Con todas nuestras opciones configuradas, finalmente podemos hacer click en el botón `Start Fuzzer` para iniciar nuestro ataque. Una vez iniciado nuestro ataque, podemos ordenar los resultados por `Response`, ya que solo nos interesan las respuestas con código `200`:

![](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_attack.jpg)

Como podemos ver, obtuvimos un resultado con el código `200`con el payload `skills`, lo que significa que el directorio `/skills/` existe en el servidor y es accesible. Podemos hacer clic en la solicitud en la ventana de resultados para ver sus detalles:

<figure><img src="https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_dir.jpg" alt=""><figcaption></figcaption></figure>

Podemos ver en la respuesta que efectivamente podemos acceder a esta página. Hay otros campos que pueden indicar un ataque exitoso según el escenario del ataque, como `Size Resp. Body` que puede indicar que obtuvimos una página diferente si su tamaño era diferente al de otras respuestas, o `RTT` para ataques como `time-based SQL injections`, que se detectan por un retraso en la respuesta del servidor.

***

## Ejercicio

```
Objetivo: 94.237.59.16:55216
```

El directorio que encontramos arriba establece la cookie en el hash md5 del nombre de usuario, como podemos ver en la cookie md5 de la solicitud del usuario (invitado). Visita '`/skills/`' para obtener una solicitud con una cookie, luego intenta usar ZAP Fuzzer para analizar la cookie para diferentes nombres de usuario con hash md5 para obtener la flag. Usa la lista de palabras "top-usernames-shortlist.txt" de Seclists.

<figure><img src="/files/pEYjVKzh6tGowd1pRpqX" alt=""><figcaption></figcaption></figure>

Seleccionamos la lista `/usr/share/seclists/top-usernames-shortlist.txt`. Si no tienes seclists instaladas las puedes instalar con el siguiente comando

```bash
sudo apt-get install seclists
```

<figure><img src="/files/Og0jWJ3TlMb0mxedx2nR" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/PoiybfZR4ecV1jGizki4" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/LZKoW4M9nLvcr9DBQKW3" alt=""><figcaption></figcaption></figure>

El fuzzing se realiza correctamente y si vemos el tamaño de respuesta, hay una página que tiene un tamaño direfente, y se corresponde con la siguiente cookie y se corresponde con el usuario `guest`:

```
Cookie: cookie=084e0343a0486ff05530df6c705c8bb4
```

Volvemos a repetir el proceso de fuzzing, esta vez con esta cookie configurada, y observamos que hay una nueva cookie diferente, con un tamaño de respuesta superior al resto:

<figure><img src="/files/w458w4S7CqsVU9eCP9Lt" alt=""><figcaption></figcaption></figure>

Le damos `Click derecho > Reenviar` y nos saltará esta pantalla, donde le daremos a SEND:

<figure><img src="/files/2DAYBstu2XU1b9cAda8x" alt=""><figcaption></figcaption></figure>

Como observamos esto nos cambia de nuevo la cookie y nos devuelve la flag:

<figure><img src="/files/B8KlD7VLDdNAH7UT1iz5" alt=""><figcaption></figcaption></figure>

Podemos pegar igualmente la cookie en el navegador y ver la flag de forma visual:

<figure><img src="/files/BixHUqmmk7nVyyXiG4MG" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/MgPU8x4utqx362WHQEdB" alt=""><figcaption></figcaption></figure>

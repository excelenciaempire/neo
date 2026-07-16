
# Modificación automática

Es posible que queramos aplicar ciertas modificaciones a todas las solicitudes HTTP salientes o a todas las respuestas HTTP entrantes en determinadas situaciones. En estos casos, podemos utilizar modificaciones automáticas basadas en reglas que establezcamos, de modo que las herramientas de proxy web las apliquen automáticamente.

***

## <mark style="color:purple;">Modificación automática de solicitudes</mark>

Comencemos con un ejemplo de modificación automática de solicitudes. Podemos elegir que coincida con cualquier texto dentro de nuestras solicitudes, ya sea en el encabezado de la solicitud o en el cuerpo de la solicitud, y luego reemplazarlos con un texto diferente. A modo de demostración, reemplacemos nuestro `User-Agent`por `HackTheBox Agent 1.0`, lo que puede resultar útil en casos en los que podamos estar tratando con filtros que bloqueen ciertos agentes de usuario.

### **Burp Suite - Match & Replace**

Podemos ir a ( `Proxy > Options > Match and Replace`) y hacer click en `Add`en Burp. Como se muestra en la siguiente captura de pantalla, configuraremos las siguientes opciones:

![Reemplazar el eructo de cerillas](https://academy.hackthebox.com/storage/modules/110/burp_match_replace_user_agent_1.jpg)

<table><thead><tr><th width="351"></th><th></th></tr></thead><tbody><tr><td><code>Type</code>:<code>Request header</code></td><td>Ya que el cambio que queremos realizar será en el encabezado de la solicitud y no en el cuerpo de la misma.</td></tr><tr><td><code>Match</code>:<code>^User-Agent.*$</code></td><td>El patrón de expresión regular que coincide con toda la línea dentro de el <code>User-Agent</code>.</td></tr><tr><td><code>Replace</code>:<code>User-Agent: HackTheBox Agent 1.0</code></td><td>Este es el valor que reemplazará la línea que hicimos coincidir arriba.</td></tr><tr><td><code>Regex match</code>: Check</td><td>No sabemos la cadena de agente de usuario exacta que queremos reemplazar, por lo que usaremos expresiones regulares para que coincida con cualquier valor que coincida con el patrón que especificamos anteriormente.</td></tr></tbody></table>

Una vez que ingresamos las opciones anteriores y hacemos clic en `Ok`, se agregará y habilitará nuestra nueva opción Coincidir y reemplazar y comenzará a reemplazar automáticamente el encabezado `User-Agent` en nuestras solicitudes con nuestro nuevo User-Agent. Podemos verificarlo visitando cualquier sitio web utilizando el navegador Burp preconfigurado y revisando la solicitud interceptada. Veremos que nuestro User-Agent ha sido reemplazado automáticamente:

![](https://academy.hackthebox.com/storage/modules/110/burp_match_replace_user_agent_2.jpg)

### **ZAP Replacer**

ZAP tiene una función similar llamada `Replacer`, a la que podemos acceder presionando \[ `CTRL+R`] o haciendo clic en `Replacer` en el menú de opciones de ZAP. Es bastante similar a lo que hicimos anteriormente, por lo que podemos hacer clic en `Add` y agregar las mismas opciones que usamos anteriormente:

![Reemplazar ZAP Match](https://academy.hackthebox.com/storage/modules/110/zap_match_replace_user_agent_1.jpg)

* `Description`: `HTB User-Agent`
* `Match Type`: `Request Header (will add if not present)`
* `Match String`: `User-Agent` - Podemos seleccionar el encabezado que queramos del menú desplegable y ZAP reemplazará su valor
* `Replacement String`: `HackTheBox Agent 1.0`
* `Enable`: Check

ZAP también tiene la función `Request Header String` que podemos usar con un patrón Regex.

ZAP también ofrece la opción de configurar el `Initiators`, al que podemos acceder haciendo clic en la otra pestaña de las ventanas que se muestran arriba. Los iniciadores nos permiten seleccionar dónde se aplicará nuestra opción `Replacer`. Mantendremos la opción predeterminada de aplicar en todas partes: `Apply to all HTTP(S) messages`

Ahora podemos habilitar la intercepción de solicitudes presionando \[ `CTRL+B`], luego podemos visitar cualquier página en el navegador ZAP preconfigurado:

![Reemplazar ZAP Match](https://academy.hackthebox.com/storage/modules/110/zap_match_replace_user_agent_2.jpg)

***

### Modificación automática de la respuesta

El mismo concepto se puede utilizar también con respuestas HTTP. En la sección anterior, es posible que hayas notado que cuando interceptamos la respuesta, las modificaciones que hicimos en el campo `IP` eran temporales y no se aplicaban cuando actualizábamos la página a menos que interceptáramos la respuesta y las volviéramos a agregar. Para resolver esto, podemos automatizar la modificación de la respuesta de manera similar a lo que hicimos anteriormente para habilitar automáticamente cualquier carácter en el campo `IP` para facilitar la inyección de comandos.

Regresemos a ( `Proxy>Options>Match and Replace`) en Burp para agregar otra regla. Esta vez usaremos el tipo de `Response body` ya que el cambio que queremos hacer existe en el cuerpo de la respuesta y no en sus encabezados. En este caso, no tenemos que usar regex ya que conocemos la cadena exacta que queremos reemplazar, aunque es posible usar regex para hacer lo mismo si lo preferimos.

![Reemplazar el eructo de cerillas](https://academy.hackthebox.com/storage/modules/110/burp_match_replace_response_1.jpg)

* `Type`: `Response body`
* `Match`: `type="number"`
* `Replace`: `type="text"`
* `Regex match`: False

Ahora, una vez que actualizamos la página con \[ `CTRL+SHIFT+R`], veremos que podemos agregar cualquier entrada al campo de entrada, y esto también debería persistir entre actualizaciones de página:

![Reemplazar el eructo de cerillas](https://academy.hackthebox.com/storage/modules/110/burp_match_replace_response_2.jpg)

Ahora podemos hacer clic en `Ping` y nuestra inyección de comando debería funcionar sin interceptar ni modificar la solicitud.

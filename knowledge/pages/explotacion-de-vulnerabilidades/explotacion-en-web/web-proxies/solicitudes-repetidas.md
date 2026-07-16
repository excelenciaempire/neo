
# Solicitudes repetidas

En las secciones anteriores, hemos evitado con éxito la validación de entrada para utilizar una entrada no numérica para lograr la inyección de comandos en el servidor remoto. Si queremos repetir el mismo proceso con un comando diferente, tendríamos que interceptar la solicitud nuevamente, proporcionar un payload diferente, reenviarla nuevamente y, finalmente, verificar nuestro navegador para obtener el resultado final.

Como puedes imaginar, si hiciéramos esto para cada comando, nos llevaría una eternidad enumerar un sistema, ya que cada comando requeriría de 5 a 6 pasos para ejecutarse. Sin embargo, para tareas tan repetitivas, podemos utilizar la repetición de solicitudes para que este proceso sea mucho más sencillo.

La repetición de solicitudes nos permite reenviar cualquier solicitud web que haya pasado previamente por el proxy web. Esto nos permite realizar cambios rápidos en cualquier solicitud antes de enviarla y luego obtener la respuesta dentro de nuestras herramientas sin interceptar ni modificar cada solicitud.

***

## <mark style="color:purple;">Historial de proxy</mark>

Para comenzar, podemos ver el historial de solicitudes HTTP en `Burp`( `Proxy>HTTP History`):

![](https://academy.hackthebox.com/storage/modules/110/burp_history_tab.jpg)

En `ZAP` HUD, podemos encontrarlo en el panel Historial inferior o en la interfaz principal de ZAP en la pestaña `History` inferior también:

![](https://academy.hackthebox.com/storage/modules/110/zap_history_tab.jpg)

Ambas herramientas también proporcionan opciones de filtrado y clasificación para el historial de solicitudes, lo que puede ser útil si tratamos con una gran cantidad de solicitudes y queremos localizar una solicitud específica.

{% hint style="info" %}
**Nota**: Ambas herramientas también mantienen un historial de WebSockets, que muestra todas las conexiones iniciadas por la aplicación web incluso después de cargarse, como actualizaciones asincrónicas y obtención de datos. Los WebSockets pueden ser útiles al realizar pruebas de penetración web avanzadas y están fuera del alcance de este módulo.
{% endhint %}

Si hacemos clic en cualquier solicitud del historial en cualquiera de las herramientas, se mostrarán sus detalles:

#### Burp Suite

<figure><img src="https://academy.hackthebox.com/storage/modules/110/burp_history_details.jpg" alt=""><figcaption></figcaption></figure>

#### ZAP

<figure><img src="https://academy.hackthebox.com/storage/modules/110/zap_history_details.jpg" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**Consejo**: mientras que ZAP solo muestra la solicitud final o modificada que se envió, Burp ofrece la posibilidad de examinar tanto la solicitud original como la solicitud modificada. Si se editó una solicitud, el encabezado del panel indicaría `Original Request`, y podemos hacer clic en él y seleccionar examinar la solicitud final que se envió.
{% endhint %}

***

## <mark style="color:purple;">Solicitudes repetidas</mark>

### **Burp Suite**

Una vez que localizamos la solicitud que queremos repetir, podemos hacer clic en \[ `CTRL+R`] en Burp para enviarla a la pestaña `Repeater` y luego podemos navegar hasta `Repeater` o hacer clic en \[ `CTRL+SHIFT+R`] para ir directamente a ella. Una vez en `Repeater`, podemos hacer clic en `Send` para enviar la solicitud:

![](https://academy.hackthebox.com/storage/modules/110/burp_repeater_request.jpg)

{% hint style="info" %}
**Consejo**: También podemos hacer clic derecho en la solicitud y seleccionar `Change Request Method` para cambiar el método HTTP entre POST/GET sin tener que reescribir la solicitud completa.
{% endhint %}

### **ZAP**

En ZAP, una vez que localizamos nuestra solicitud, podemos hacer clic derecho sobre ella y seleccionar `Open/Resend with Request Editor`, lo que abriría la ventana del editor de solicitudes, y nos permitiría reenviar la solicitud con el botón `Send` para enviar nuestra solicitud:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/110/zap_repeater_request.jpg" alt=""><figcaption></figcaption></figure>

También podemos ver el menú desplegable `Method`, que nos permite cambiar rápidamente el método de solicitud a cualquier otro método HTTP.

{% hint style="info" %}
**Consejo**: De manera predeterminada, la ventana del Editor de solicitudes en ZAP tiene la solicitud y la respuesta en diferentes pestañas. Puede hacer clic en los botones de visualización para cambiar la forma en que están organizados. Para que coincida con el aspecto anterior, elija las mismas opciones de visualización que se muestran en la captura de pantalla.
{% endhint %}

Podemos lograr el mismo resultado dentro del navegador preconfigurado con `ZAP HUD`. Podemos ubicar la solicitud en el panel inferior Historial y, una vez que hagamos clic en ella, se mostrará la ventana `Request Editor` que nos permitirá volver a enviarla. Podemos seleccionar `Replay in Console` para obtener la respuesta en la misma ventana `HUD` o seleccionar `Replay in Browser` para ver la respuesta presentada en el navegador:

![](https://academy.hackthebox.com/storage/modules/110/zap_hud_resend.jpg)

Así pues, vamos a intentar modificar nuestra solicitud y enviarla. En las tres opciones ( `Burp Repeater`, `ZAP Request Editor`, y `ZAP HUD`), vemos que las solicitudes son modificables, y podemos seleccionar el texto que queremos cambiar y reemplazarlo por lo que queramos, y luego hacer clic en el botón `Send` para enviarlo nuevamente:

![](https://academy.hackthebox.com/storage/modules/110/burp_repeat_modify.jpg)

Como podemos ver, podríamos modificar fácilmente el comando y obtener instantáneamente su resultado usando Burp `Repeater`. Intenta hacer lo mismo en `ZAP Request Editor`y `ZAP HUD`para ver cómo funcionan.

Por último, podemos ver en nuestra solicitud POST anterior que los datos están codificados en URL. Esto es una parte esencial del envío de solicitudes HTTP personalizadas, que analizaremos en la siguiente sección.

***

## Ejercicio

Intente utilizar la repetición de solicitudes para poder probar comandos rápidamente. Con eso, intente buscar la otra flag (no está en el mismo directorio)

<figure><img src="/files/KnbhQWg5bjADKZZ7i5CA" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/pqcIjy37gpXB5LRcF8to" alt=""><figcaption></figcaption></figure>

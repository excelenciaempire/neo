
# Interceptando solicitudes

Ahora que hemos configurado nuestro proxy, podemos usarlo para interceptar y manipular varias solicitudes HTTP enviadas por la aplicación web que estamos probando. Comenzaremos por aprender a interceptar solicitudes web, modificarlas y luego enviarlas a su destino previsto.

***

## <mark style="color:purple;">Interceptar solicitudes</mark>

### **Burp Suite**

En Burp, podemos navegar hasta la pestaña `Proxy` y la interceptación de solicitudes debería estar activada de forma predeterminada. Si queremos activar o desactivar la interceptación de solicitudes, podemos ir a la subpestaña `Intercept` y hacer clic en el botón `Intercept is on/off` para hacerlo:

![Interceptación de eructos activada](https://academy.hackthebox.com/storage/modules/110/burp_intercept_htb_on.jpg)

Una vez que activamos la interceptación de solicitudes, podemos iniciar el navegador preconfigurado y luego visitar nuestro sitio web de destino después de generarlo a partir del ejercicio al final de esta sección. Luego, una vez que volvamos a Burp, veremos la solicitud interceptada esperando nuestra acción y podemos hacer clic en `forward` para reenviar la solicitud:

![Página de interceptación de Burp Suite](https://academy.hackthebox.com/storage/modules/110/burp_intercept_page.jpg)

{% hint style="info" %}
Nota: como en este caso se interceptará todo el tráfico de Firefox, es posible que veamos que se ha interceptado otra solicitud antes de esta. Si esto sucede, haga clic en "Reenviar" hasta que llegue la solicitud a nuestra IP de destino, como se muestra arriba.
{% endhint %}

***

### **ZAP**

En ZAP, la interceptación está desactivada de forma predeterminada, como lo muestra el botón verde en la barra superior (el verde indica que las solicitudes pueden pasar y no ser interceptadas). Podemos hacer clic en este botón para activar o desactivar la intercepción de solicitudes, o podemos usar el acceso directo \[ `CTRL+B`] para activarla o desactivarla:

![Interceptación ZAP activada](https://academy.hackthebox.com/storage/modules/110/zap_intercept_htb_on.jpg)

A continuación, podemos iniciar el navegador preconfigurado y volver a visitar la página web del ejercicio. Veremos la solicitud interceptada en el panel superior derecho y podemos hacer clic en el + (a la derecha del botón rojo `break`) para reenviar la solicitud:

![Página de interceptación de ZAP](https://academy.hackthebox.com/storage/modules/110/zap_intercept_page.jpg)

ZAP también tiene una característica poderosa llamada `Heads Up Display (HUD)`, que nos permite controlar la mayoría de las características principales de ZAP desde el navegador preconfigurado. Podemos habilitarla en el `HUD` haciendo clic en su botón al final de la barra de menú superior:

![ZAP HUD activado](https://academy.hackthebox.com/storage/modules/110/zap_enable_HUD.jpg)

El HUD tiene muchas funciones que cubriremos a medida que avancemos en el módulo. Para interceptar solicitudes, podemos hacer clic en el segundo botón desde la parte superior del panel izquierdo para activar la interceptación de solicitudes:

<figure><img src="https://academy.hackthebox.com/storage/modules/110/zap_hud_break.jpg" alt=""><figcaption></figcaption></figure>

Ahora, una vez que actualizamos la página o enviamos otra solicitud, el HUD interceptará la solicitud y nos la presentará para que tomemos acción:

<figure><img src="https://academy.hackthebox.com/storage/modules/110/zap_hud_break_request.jpg" alt=""><figcaption></figcaption></figure>

Podemos elegir `step` para enviar la solicitud y examinar su respuesta y deshacer las solicitudes posteriores, o podemos elegir `continue` y dejar que la página envíe las solicitudes restantes. El botón `step` es útil cuando queremos examinar cada paso de la funcionalidad de la página, mientras que `continue` es útil cuando solo nos interesa una única solicitud y podemos reenviar las solicitudes restantes una vez que alcanzamos nuestra solicitud objetivo.

{% hint style="info" %}
**Consejo**: La primera vez que utilices el navegador ZAP preconfigurado, se te presentará el tutorial del HUD. Puedes considerar realizar este tutorial después de esta sección, ya que te enseñará los conceptos básicos del HUD. Incluso si no comprendes todo, las próximas secciones deberían cubrir todo lo que te hayas perdido. Si no obtienes el tutorial, puedes hacer clic en el botón de configuración en la parte inferior derecha y elegir "Realizar el tutorial del HUD".
{% endhint %}

***

### Manipulación de solicitudes interceptadas

Una vez que interceptamos la solicitud, permanecerá bloqueada hasta que la reenviemos, como hicimos anteriormente. Podemos examinar la solicitud, manipularla para realizar los cambios que queramos y luego enviarla a su destino. Esto nos ayuda a comprender mejor qué información envía una aplicación web en particular en sus solicitudes web y cómo puede responder a los cambios que realicemos en esa solicitud.

Existen numerosas aplicaciones para esto en las pruebas de penetración web, como por ejemplo:

1. `Inyecciones SQL`
2. `Inyecciones de comandos`
3. `Bypass de subida de archivos`
4. `Omisión de autenticación`
5. `XSS`
6. `XXE`
7. `Manejo de errores`
8. `Deserialización`

Y muchas otras vulnerabilidades web potenciales, como veremos en otros módulos. Por lo tanto, vamos a mostrar esto con un ejemplo básico para demostrar cómo interceptar y manipular las solicitudes web.

Activemos nuevamente la interceptación de solicitudes en la herramienta que elijamos, establezcamos el valor `IP` en la página y luego hagamos clic en el botón `Ping`. Una vez que se intercepte nuestra solicitud, deberíamos obtener una solicitud HTTP similar a la siguiente:

```http
POST /ping HTTP/1.1
Host: 46.101.23.188:30820
Content-Length: 4
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://46.101.23.188:30820
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://46.101.23.188:30820/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

ip=1
```

Por lo general, solo podemos especificar números en el `IP`campo mediante el navegador, ya que la página web nos impide enviar caracteres no numéricos mediante JavaScript en el front-end. Sin embargo, con el poder de interceptar y manipular las solicitudes HTTP, podemos intentar usar otros caracteres para "romper" la aplicación ("romper" el flujo de solicitud/respuesta manipulando el parámetro de destino, sin dañar la aplicación web de destino). Si la aplicación web no verifica ni valida las solicitudes HTTP en el back-end, es posible que podamos manipularla y explotarla.

Entonces, cambiemos el valor `ip` del parámetro de `1` a `;ls;` y veamos cómo la aplicación web maneja nuestra entrada:

<figure><img src="/files/hrmhBq2QaN53lwcPwO4B" alt=""><figcaption></figcaption></figure>

En BurpSuite si hacemos click derecho y lo enviamos al Repeater podremos hacer pruebas de inyección de código enviando una y otra vez solicitudes manipuladas:

Una vez que hacemos clic en `Send`, veremos que la respuesta cambió de la salida de ping predeterminada a la salida `ls`, lo que significa que manipulamos con éxito la solicitud para inyectar nuestro comando:

<figure><img src="/files/kaSEYkulG3hlKxBHTekm" alt=""><figcaption></figcaption></figure>

De igual manera por ejemplo podríamos cambiar el comando `;ls;` por otro para leer la flag:

<figure><img src="/files/LqXMMm8n1PTQBz8TMEyM" alt=""><figcaption></figcaption></figure>

Hasta podríamos leer el archivo `/etc/passwd` donde se almacenan todos los usuarios del sistema:

<figure><img src="/files/VV6jKHx1QJqzWmyPEAHU" alt=""><figcaption></figcaption></figure>

Esto demuestra un ejemplo básico de cómo la interceptación y manipulación de solicitudes puede ayudar a probar aplicaciones web en busca de diversas vulnerabilidades, lo que se considera una herramienta esencial para poder probar diferentes aplicaciones web de manera efectiva.

{% hint style="info" %}
**Nota**: Como se mencionó anteriormente, en este módulo no cubriremos ataques web específicos, sino cómo los servidores proxy web pueden facilitar varios tipos de ataques. Otros módulos posteriores cubren este tipo de ataques en profundidad.
{% endhint %}

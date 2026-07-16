
# Zap Scanner

ZAP también viene con un escáner web similar a Burp Scanner. ZAP Scanner es capaz de crear mapas de sitios usando ZAP Spider y realizar escaneos pasivos y activos para buscar varios tipos de vulnerabilidades.

***

## <mark style="color:purple;">ZAP Spider</mark>

Comencemos con `ZAP Spider`, que es similar a la función Crawler de Burp. Para iniciar un análisis de Spider en cualquier sitio web, podemos localizar una solicitud en nuestra pestaña Historial y seleccionar ( `Attack > Spider`) en el menú contextual. Otra opción es utilizar el HUD en el navegador preconfigurado. Una vez que visitamos la página o el sitio web en el que queremos iniciar el análisis de Spider, podemos hacer clic en el segundo botón del panel derecho ( `Spider Start`), que nos indicará que iniciemos el análisis:

![Araña ZAP](https://academy.hackthebox.com/storage/modules/110/zap_spider.jpg)

{% hint style="info" %}
**Nota**: Cuando hacemos clic en el botón Spider, ZAP puede indicarnos que el sitio web actual no está dentro de nuestro alcance y nos pedirá que lo agreguemos automáticamente al alcance antes de comenzar el análisis, a lo que podemos decir "Sí". El alcance es el conjunto de URL que ZAP probará si iniciamos un análisis genérico y podemos personalizarlo para que escanee varios sitios web y URL. Intente agregar varios destinos al alcance para ver cómo se ejecutaría el análisis de manera diferente.
{% endhint %}

Una vez que hacemos click en la ventana emergente `Start`, nuestro análisis Spider debería comenzar a rastrear el sitio web buscando enlaces y validándolos, de manera muy similar a cómo funciona Burp Crawler. Podemos ver el progreso del análisis Spider tanto en el HUD del botón  `Spider` como en la interfaz de usuario principal de ZAP, que debería cambiar automáticamente a la pestaña Spider actual para mostrar el progreso y las solicitudes enviadas. Cuando nuestro análisis esté completo, podemos verificar la pestaña Sitios en la interfaz de usuario principal de ZAP, o podemos hacer clic en el primer botón en el panel derecho ( `Sites Tree`), que debería mostrarnos una vista de lista de árbol expandible de todos los sitios web identificados y sus subdirectorios:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/110/zap_sites.jpg" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
**Consejo**: ZAP también tiene un tipo diferente de Spider llamado `Ajax Spider`, que se puede iniciar desde el tercer botón en el panel derecho. La diferencia entre este y el escáner normal es que Ajax Spider también intenta identificar los enlaces solicitados a través de solicitudes AJAX de JavaScript, que pueden estar ejecutándose en la página incluso después de que se cargue. Intente ejecutarlo después de que el Spider normal finalice su escaneo, ya que esto puede brindar un mejor resultado y agregar algunos enlaces que el Spider normal puede haber pasado por alto, aunque puede demorar un poco más en finalizar.
{% endhint %}

***

## <mark style="color:purple;">Escáner pasivo</mark>

A medida que ZAP Spider se ejecuta y realiza solicitudes a varios puntos finales, ejecuta automáticamente su escáner pasivo en cada respuesta para ver si puede identificar posibles problemas en el código fuente, como encabezados de seguridad faltantes o vulnerabilidades XSS basadas en DOM. Es por eso que incluso antes de ejecutar el escáner activo, es posible que veamos que el botón de alertas comienza a llenarse con algunos problemas identificados. Las alertas en el panel izquierdo nos muestran los problemas identificados en la página actual que estamos visitando, mientras que el panel derecho nos muestra las alertas generales de esta aplicación web, que incluyen alertas encontradas en otras páginas:

![Araña ZAP](https://academy.hackthebox.com/storage/modules/110/zap_alerts.jpg)

También podemos consultar la pestaña `Alerts` de la interfaz principal de ZAP para ver todos los problemas identificados. Si hacemos clic en cualquier alerta, ZAP nos mostrará sus detalles y las páginas en las que se encontró:

![Araña ZAP](https://academy.hackthebox.com/storage/modules/110/zap_site_alerts.jpg)

***

## <mark style="color:purple;">Escáner activo</mark>

Una vez que el árbol de nuestro sitio esté lleno, podemos hacer clic en el botón `Active Scan` del panel derecho para iniciar un escaneo activo en todas las páginas identificadas. Si aún no hemos ejecutado un escaneo Spider en la aplicación web, ZAP lo ejecutará automáticamente para crear un árbol de sitio como objetivo del escaneo. Una vez que se inicia el escaneo activo, podemos ver su progreso de manera similar a como lo hicimos con el escaneo Spider:

![Araña ZAP](https://academy.hackthebox.com/storage/modules/110/zap_active_scan.jpg)

El escáner activo intentará varios tipos de ataques contra todas las páginas identificadas y los parámetros HTTP para identificar tantas vulnerabilidades como sea posible. Por este motivo, el escáner activo tardará más en completarse. A medida que se ejecuta el escaneo activo, veremos que el botón de alertas comienza a llenarse con más alertas a medida que ZAP descubre más problemas. Además, podemos consultar la interfaz de usuario principal de ZAP para obtener más detalles sobre el escaneo en ejecución y podemos ver las distintas solicitudes enviadas por ZAP:

![Araña ZAP](https://academy.hackthebox.com/storage/modules/110/zap_active_scan_progress.jpg)

Una vez finalizado el Active Scan, podemos visualizar las alertas para ver cuáles son las que debemos seguir. Si bien todas las alertas deben ser reportadas y tomadas en cuenta, las alertas `High` son las que generalmente llevan a comprometer directamente la aplicación web o el servidor back-end. Si hacemos clic en el botón `High Alerts`, nos mostrará la Alerta Alta identificada:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/110/zap_high_alert.jpg" alt=""><figcaption></figcaption></figure>

También podemos hacer clic en él para ver más detalles al respecto y ver cómo podemos replicar y parchear esta vulnerabilidad:

![Araña ZAP](https://academy.hackthebox.com/storage/modules/110/zap_alert_details.jpg)

En la ventana de detalles de la alerta, también podemos hacer clic en la URL para ver los detalles de la solicitud y la respuesta que ZAP utilizó para identificar esta vulnerabilidad, y también podemos repetir la solicitud a través de ZAP HUD o ZAP Request Editor:

![Araña ZAP](https://academy.hackthebox.com/storage/modules/110/zap_alert_evidence.jpg)

***

## <mark style="color:purple;">Informes</mark>

Finalmente, podemos generar un informe con todos los hallazgos identificados por ZAP a través de sus diferentes escaneos. Para ello, podemos seleccionar ( `Report > Generate HTML Report`) en la barra superior, que nos solicitará la ubicación donde guardar el informe. También podemos exportar el informe en otros formatos como `XML` o `Markdown`. Una vez que generemos nuestro informe, podemos abrirlo en cualquier navegador para visualizarlo:

![Araña ZAP](https://academy.hackthebox.com/storage/modules/110/zap_report.jpg)

Como podemos ver, el informe muestra todos los detalles identificados de manera organizada, lo que puede ser útil para mantener como registro las distintas aplicaciones web en las que ejecutamos nuestros análisis durante una prueba de penetración.

***

## <mark style="color:purple;">Ejercicio</mark>

Ejecute ZAP Scanner en el objetivo anterior para identificar directorios y vulnerabilidades potenciales. Una vez que encuentre la vulnerabilidad de alto nivel, intente usarlo para leer la bandera en '/flag.txt'

```
Objetivo: 94.237.49.212:53545
```

Iniciamos Zaproxy con el HUD y entramos al navegador, iniciando el módulo Spider y el Active Scan:

<figure><img src="/files/7TeoMzH5J5R9DuitryRM" alt=""><figcaption></figcaption></figure>

Una vez que termina, nos encuentra una vulnerabilidad crítica de `OS Command Inyection`, lo que nos permitiría inyectar comandos para conseguir información:

<figure><img src="/files/xHuhKyHXgeHnugII6CMP" alt=""><figcaption></figcaption></figure>

```
http://94.237.49.212:53545/devtools/ping.php?ip=127.0.0.1%26cat+%2Fetc%2Fpasswd%26
```

Al acceder efectivamente vemos que hace un `cat /etc/passwd` y obtenemos todos los usuarios del sistema:

<figure><img src="/files/soQr1cBWYX1vUIOms6FS" alt=""><figcaption></figcaption></figure>

Si modificamos la URL podemos leer la flag en el directorio root:

```
https://94.237.49.212:53545/devtools/ping.php?ip=127.0.0.1%26cat+%2Fflag.txt
```

<figure><img src="/files/Q3DhTdvkaUIIPbv6DxEH" alt=""><figcaption></figcaption></figure>


# Web Proxies

## <mark style="color:purple;">Introducción a los Web Proxies</mark>

En la actualidad, la mayoría de las aplicaciones web y móviles modernas funcionan conectándose continuamente a servidores back-end para enviar y recibir datos y luego procesarlos en el dispositivo del usuario, como sus navegadores web o teléfonos móviles. Dado que la mayoría de las aplicaciones dependen en gran medida de servidores back-end para procesar datos, probar y proteger dichos servidores se está volviendo cada vez más importante.

Las pruebas de solicitudes web a servidores back-end constituyen la mayor parte de las pruebas de penetración de aplicaciones web, que incluyen conceptos que se aplican tanto a aplicaciones web como móviles. Para capturar las solicitudes y el tráfico que pasan entre las aplicaciones y los servidores back-end y manipular este tipo de solicitudes con fines de prueba, necesitamos usar `Web Proxies`.

***

## <mark style="color:purple;">¿Qué son los Web Proxies?</mark>

Los servidores proxy web son herramientas especializadas que se pueden configurar entre un navegador o una aplicación móvil y un servidor back-end para capturar y visualizar todas las solicitudes web que se envían entre ambos extremos, actuando básicamente como herramientas de intermediario (MITM). Mientras que otras aplicaciones de `Network Sniffing`, como Wireshark, funcionan analizando todo el tráfico local para ver qué pasa por una red, los servidores proxy web funcionan principalmente con puertos web como, entre otros, `HTTP/80` y `HTTPS/443`.

Los servidores proxy web se consideran una de las herramientas más esenciales para cualquier pentester web. Simplifican significativamente el proceso de captura y reproducción de solicitudes web en comparación con las herramientas basadas en CLI anteriores. Una vez que se configura un servidor proxy web, podemos ver todas las solicitudes HTTP realizadas por una aplicación y todas las respuestas enviadas por el servidor back-end. Además, podemos interceptar una solicitud específica para modificar sus datos y ver cómo las maneja el servidor back-end, lo que es una parte esencial de cualquier prueba de penetración web.

***

## <mark style="color:purple;">Usos de los servidores Proxy Web</mark>

Si bien el uso principal de los servidores proxy web es capturar y reproducir solicitudes HTTP, tienen muchas otras funciones que permiten distintos usos para los servidores proxy web. La siguiente lista muestra algunas de las otras tareas para las que podemos usar servidores proxy web:

* `Análisis de vulnerabilidades de aplicaciones web`
* `Fuzzing en la web`
* `Crawling web`
* `Mapeo de aplicaciones web`
* `Análisis de solicitudes web`
* `Prueba de configuración web`
* `Revisiones de código`

En este módulo, no analizaremos ningún ataque web específico, ya que otros módulos cubren varios ataques web. Sin embargo, cubriremos en detalle cómo usar servidores proxy web y sus diversas funciones, y mencionaremos qué tipo de ataques web requieren qué función. Cubriremos las dos herramientas de proxy web más comunes: `Burp Suite` y`ZAP`.

***

## <mark style="color:purple;">Burp Suite</mark>

[Burp Suite (Burp)](https://portswigger.net/burp) es el proxy web más común para pruebas de penetración web. Tiene una excelente interfaz de usuario para sus diversas funciones e incluso proporciona un navegador Chromium integrado para probar aplicaciones web. Algunas funciones de Burp solo están disponibles en la versión comercial `Burp Pro/Enterprise`, pero incluso la versión gratuita es una herramienta de prueba extremadamente poderosa que debemos tener en nuestro arsenal.

Algunas de las características `paid-only` son:

* Escáner de aplicaciones web activo
* Burp Intruder rápido
* La capacidad de cargar ciertas extensiones de Burp

La versión `free` comunitaria de Burp Suite debería ser suficiente para la mayoría de los evaluadores de penetración. Una vez que comencemos con las pruebas de penetración de aplicaciones web más avanzadas, las funciones `pro` pueden resultar útiles. La mayoría de las funciones que cubriremos en este módulo están disponibles en la versión `free` comunitaria de Burp Suite, pero también abordaremos algunas de las funciones `pro`, como el escáner de aplicaciones web activas.

{% hint style="info" %}
**Consejo**: si tienes una dirección de correo electrónico educativa o comercial, puedes solicitar una prueba gratuita de Burp Pro en este [enlace](https://portswigger.net/burp/pro/trial) para poder seguir algunas de las funciones exclusivas de Burp Pro que se muestran más adelante en este módulo.
{% endhint %}

***

## <mark style="color:purple;">OWASP Zed Attack Proxy (ZAP)</mark>

[OWASP Zed Attack Proxy (ZAP)](https://www.zaproxy.org/) es otra herramienta de proxy web común para pruebas de penetración web. ZAP es un proyecto gratuito y de código abierto iniciado por el [Proyecto de seguridad de aplicaciones web abiertas (OWASP)](https://owasp.org/) y mantenido por la comunidad, por lo que no tiene funciones de pago exclusivas como Burp. Ha crecido significativamente en los últimos años y rápidamente está ganando reconocimiento en el mercado como la herramienta de proxy web de código abierto líder.

Al igual que Burp, ZAP ofrece varias funciones básicas y avanzadas que se pueden utilizar para realizar pruebas de penetración en la web. ZAP también tiene ciertas ventajas sobre Burp, que abordaremos a lo largo de este módulo. La principal ventaja de ZAP sobre Burp es que es un proyecto gratuito de código abierto, lo que significa que no enfrentaremos limitaciones en nuestros análisis que solo se eliminan con una suscripción paga. Además, con una creciente comunidad de colaboradores, ZAP está obteniendo muchas de las funciones de pago de Burp de forma gratuita.

Al final, aprender ambas herramientas puede resultar bastante similar y nos proporcionará opciones para cada situación a través de un pentest web, pudiendo optar por utilizar la que nos parezca más adecuada a nuestras necesidades. En algunos casos, puede que no veamos suficiente valor como para justificar una suscripción de pago a Burp, y puede que cambiemos a ZAP para tener una experiencia completamente abierta y gratuita. En otras situaciones en las que queramos una solución más madura para pentests avanzados o pentesting corporativo, puede que encontremos justificado el valor que nos proporciona Burp Pro y cambiemos a Burp por estas características.


# Cross Site Scripting (XSS)

## <mark style="color:purple;">Introducción</mark>

A medida que las aplicaciones web se vuelven más avanzadas y más comunes, también lo hacen las vulnerabilidades de las aplicaciones web. Entre los tipos más comunes de vulnerabilidades de las aplicaciones web se encuentran las vulnerabilidades [Cross-Site Scripting (XSS)](https://owasp.org/www-community/attacks/xss/) . Las vulnerabilidades XSS aprovechan una falla en la sanitización de los inputs para "escribir" código JavaScript en la página y ejecutarlo en el lado del cliente, lo que da lugar a varios tipos de ataques.

***

## <mark style="color:purple;">¿Qué es XSS?</mark>

Una aplicación web típica funciona recibiendo el código HTML del servidor back-end y mostrándolo en el navegador de Internet del lado del cliente. Cuando una aplicación web vulnerable no desinfecta adecuadamente la entrada del usuario, un usuario malintencionado puede inyectar código JavaScript adicional en un campo de entrada (por ejemplo, comentario/respuesta), de modo que, una vez que otro usuario vea la misma página, ejecute sin saberlo el código JavaScript malicioso.

Las vulnerabilidades XSS se ejecutan únicamente en el lado del cliente y, por lo tanto, no afectan directamente al servidor back-end. Solo pueden afectar al usuario que ejecuta la vulnerabilidad. El impacto directo de las vulnerabilidades XSS en el servidor back-end puede ser relativamente bajo, pero se encuentran con mucha frecuencia en aplicaciones web, por lo que esto equivale a un riesgo medio ( `bajo impacto + alta probabilidad = riesgo medio`), que siempre debemos intentar `reduce`controlar detectando, remediando y previniendo de forma proactiva este tipo de vulnerabilidades.

![riesgo xss](https://academy.hackthebox.com/storage/modules/103/xss_risk_chart_1.jpg)

***

## <mark style="color:purple;">Ataques XSS</mark>

Las vulnerabilidades XSS pueden facilitar una amplia gama de ataques, que pueden ser cualquier cosa que se pueda ejecutar a través del código JavaScript del navegador. Un ejemplo básico de un ataque XSS es que el usuario objetivo envíe sin saberlo su cookie de sesión al servidor web del atacante. Otro ejemplo es que el navegador del objetivo ejecute llamadas a la API que conduzcan a una acción maliciosa, como cambiar la contraseña del usuario por una contraseña elegida por el atacante. Existen muchos otros tipos de ataques XSS, desde la minería de Bitcoin hasta la visualización de anuncios.

Como los ataques XSS ejecutan código JavaScript dentro del navegador, están limitados al motor JS del navegador (es decir, V8 en Chrome). No pueden ejecutar código JavaScript en todo el sistema para hacer algo como la ejecución de código a nivel de sistema. En los navegadores modernos, también están limitados al mismo dominio del sitio web vulnerable. Sin embargo, poder ejecutar JavaScript en el navegador de un usuario aún puede conducir a una amplia variedad de ataques, como se mencionó anteriormente. Además de esto, si un investigador experto identifica una vulnerabilidad binaria en un navegador web (por ejemplo, un desbordamiento de Heap en Chrome), puede utilizar una vulnerabilidad XSS para ejecutar un exploit de JavaScript en el navegador del objetivo, que eventualmente sale del sandbox del navegador y ejecuta código en la máquina del usuario.

Las vulnerabilidades XSS se pueden encontrar en casi todas las aplicaciones web modernas y han sido explotadas activamente durante las últimas dos décadas. Un ejemplo de XSS muy conocido es el [gusano Samy](https://en.wikipedia.org/wiki/Samy_\(computer_worm\)) , que era un gusano basado en navegador que explotaba una vulnerabilidad XSS almacenada en el sitio web de redes sociales MySpace en 2005. Se ejecutaba al visualizar una página web infectada publicando un mensaje en la página de MySpace de la víctima que decía: "Samy es mi héroe". El mensaje en sí también contenía el mismo payload de JavaScript para volver a publicar el mismo mensaje cuando lo vieran otros. En un solo día, más de un millón de usuarios de MySpace tenían este mensaje publicado en sus páginas. Aunque este payload específico no causó ningún daño real, la vulnerabilidad podría haberse utilizado para fines mucho más nefastos, como robar la información de la tarjeta de crédito de los usuarios, instalar registradores de teclas en sus navegadores o incluso explotar una vulnerabilidad binaria en los navegadores web de los usuarios (que era más común en los navegadores web en ese entonces).

En 2014, un investigador de seguridad identificó accidentalmente una [vulnerabilidad XSS](https://blog.sucuri.net/2014/06/serious-cross-site-scripting-vulnerability-in-tweetdeck-twitter.html) en el panel TweetDeck de Twitter. Esta vulnerabilidad se explotó para crear un [tuit que se retuiteaba a sí mismo](https://twitter.com/derGeruhn/status/476764918763749376) en Twitter, lo que provocó que el tuit fuera retuiteado más de 38.000 veces en menos de dos minutos. Finalmente, Twitter se vio obligado a [cerrar temporalmente TweetDeck](https://www.theguardian.com/technology/2014/jun/11/twitter-tweetdeck-xss-flaw-users-vulnerable) mientras reparaban la vulnerabilidad.

Hasta el día de hoy, incluso las aplicaciones web más destacadas tienen vulnerabilidades XSS que pueden ser explotadas. Incluso la página del motor de búsqueda de Google tenía múltiples vulnerabilidades XSS en su barra de búsqueda, la más reciente de las cuales fue en [2019](https://www.acunetix.com/blog/web-security-zone/mutation-xss-in-google-search/) cuando se encontró una vulnerabilidad XSS en la biblioteca XML. Además, el servidor Apache, el servidor web más utilizado en Internet, informó una vez de una [vulnerabilidad XSS](https://blogs.apache.org/infra/entry/apache_org_04_09_2010) que estaba siendo explotada activamente para robar contraseñas de usuarios de ciertas empresas. Todo esto nos dice que las vulnerabilidades XSS deben tomarse en serio y que se debe dedicar una buena cantidad de esfuerzo a detectarlas y prevenirlas.

***

## <mark style="color:purple;">Tipos de XSS</mark>

Hay tres tipos principales de vulnerabilidades XSS:

<table data-header-hidden><thead><tr><th width="285"></th><th></th></tr></thead><tbody><tr><td>Tipo</td><td>Descripción</td></tr><tr><td><code>Stored (Persistent) XSS</code></td><td>El tipo más crítico de XSS, que ocurre cuando la entrada del usuario se almacena en la base de datos del back-end y luego se muestra al recuperarla (por ejemplo, publicaciones o comentarios)</td></tr><tr><td><code>Reflected (Non-Persistent) XSS</code></td><td>Se produce cuando la entrada del usuario se muestra en la página después de ser procesada por el servidor backend, pero sin almacenarse (por ejemplo, resultado de búsqueda o mensaje de error)</td></tr><tr><td><code>DOM-based XSS</code></td><td>Otro tipo de XSS no persistente que ocurre cuando la entrada del usuario se muestra directamente en el navegador y se procesa completamente en el lado del cliente, sin llegar al servidor back-end (por ejemplo, a través de parámetros HTTP del lado del cliente o etiquetas de anclaje)</td></tr></tbody></table>

Cubriremos cada uno de estos tipos en las próximas secciones y trabajaremos con ejercicios para ver cómo ocurre cada uno de ellos, y luego también veremos cómo se puede utilizar cada uno de ellos en los ataques.

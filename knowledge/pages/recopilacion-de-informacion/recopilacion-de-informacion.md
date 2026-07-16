
# Recopilación de información

La fase [de recopilación de información](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/01-Information_Gathering/README) es el primer paso en cada prueba de penetración en la que necesitamos simular atacantes externos sin información interna de la organización objetivo. Esta fase es crucial ya que la recopilación de información deficiente y apresurada podría dar lugar a que se omitan fallas que de otro modo se habrían descubierto con una enumeración exhaustiva.

![](https://academy.hackthebox.com/storage/modules/144/PT-process.png)

Esta fase nos ayuda a comprender la superficie de ataque, las tecnologías utilizadas y, en algunos casos, descubrir entornos de desarrollo o incluso infraestructuras olvidadas y sin mantenimiento que pueden conducirnos al acceso a redes internas, ya que suelen estar menos protegidas y monitoreadas. La recopilación de información suele ser un proceso iterativo. A medida que descubrimos activos (por ejemplo, un subdominio o un host virtual), necesitaremos tomar huellas digitales de las tecnologías en uso, buscar páginas/directorios ocultos, etc., lo que puede llevarnos a descubrir otro subdominio y comenzar el proceso de nuevo.

Por ejemplo, podemos pensar que nos topamos con nuevos subdominios durante una de nuestras pruebas de penetración basadas en el certificado SSL. Sin embargo, si observamos más de cerca estos subdominios, a menudo veremos tecnologías en uso diferentes a las del sitio web principal de la empresa. Los subdominios y vhosts se utilizan para presentar otra información y realizar otras tareas que se han separado de la página de inicio. Por tanto, es fundamental saber qué tecnologías se utilizan, para qué sirven y cómo funcionan.&#x20;

***

## <mark style="color:purple;">Áreas</mark>

Durante este proceso, nuestro objetivo es identificar la mayor cantidad de información posible de las siguientes áreas:

### Dominios y Subdominios

A menudo, se nos proporciona un único dominio o quizás una lista de dominios y subdominios que pertenecen a una organización. Muchas organizaciones no cuentan con un inventario de activos preciso y es posible que hayan olvidado tanto los dominios como los subdominios expuestos externamente. Esta es una parte esencial de la fase de reconocimiento. Es posible que nos encontremos con varios subdominios que se asignan a direcciones IP dentro del alcance, lo que aumenta la superficie de ataque general de nuestro compromiso (o programa de recompensas por errores). Los subdominios ocultos y olvidados pueden tener versiones antiguas/vulnerables de aplicaciones o versiones de desarrollo con funcionalidad adicional (una consola de depuración de Python, por ejemplo). Los programas de recompensas por errores a menudo establecerán el alcance como algo como `*.inlanefreight.com`, lo que significa que todos los subdominios de `inlanefreight.com`, en este ejemplo, están dentro del alcance (es decir, `acme.inlanefreight.com`, `admin.inlanefreight.com`, y así sucesivamente). También podremos descubrir subdominios de subdominios. Por ejemplo, supongamos que descubrimos algo como `admin.inlanefreight.com`. Luego podríamos ejecutar una enumeración adicional de subdominios contra este subdominio y tal vez encontrar `dev.admin.inlanefreight.com`un objetivo muy atractivo. Hay muchas formas de encontrar subdominios (tanto de forma pasiva como activa) que cubriremos más adelante en este módulo.

### Rangos de IP

A menos que estemos limitados a un alcance muy específico, queremos saber todo lo posible sobre nuestro objetivo. Encontrar rangos de IP adicionales propiedad de nuestro objetivo puede llevarnos a descubrir otros dominios y subdominios y abrir aún más nuestra posible superficie de ataque.

### Infraestructura

Queremos aprender tanto como sea posible sobre nuestro objetivo. Necesitamos saber qué tecnologías está utilizando nuestro objetivo. ¿Son todas sus aplicaciones ASP.NET? ¿Usan Django, PHP, Flask, etc.? ¿Qué tipo(s) de API/servicios web se utilizan? ¿Utilizan sistemas de gestión de contenidos (CMS) como WordPress, Joomla, Drupal o DotNetNuke, que tienen sus propios tipos de vulnerabilidades y configuraciones erróneas que podemos encontrar? También nos preocupamos por los servidores web en uso, como IIS, Nginx, Apache y los números de versión. Si nuestro objetivo ejecuta marcos o servidores web obsoletos, queremos profundizar en las aplicaciones web asociadas. También nos interesan los tipos de bases de datos back-end en uso (MSSQL, MySQL, PostgreSQL, SQLite, Oracle, etc.), ya que esto nos dará una indicación de los tipos de ataques que podemos realizar.

### Vhosts

Por último, queremos enumerar los hosts virtuales (vhosts), que son similares a los subdominios pero indican que una organización aloja múltiples aplicaciones en el mismo servidor web. También cubriremos la enumeración de vhost más adelante en el módulo.

***

## <mark style="color:purple;">Categorías</mark>

Podemos dividir el proceso de recopilación de información en dos categorías principales:

### Recopilación Pasiva

No interactuamos directamente con el objetivo en esta etapa. En cambio, recopilamos información disponible públicamente mediante motores de búsqueda, whois, información de certificados, etc. El objetivo es obtener la mayor cantidad de información posible para utilizarla como entrada en la fase de recopilación activa de información.

{% content-ref url="/pages/Cr8VUHF50vhiuVlAeAWi" %}
[Recopilación Pasiva](/ethical-hacking-cheatsheet/recopilacion-de-informacion/recopilacion-de-informacion/recopilacion-pasiva.md)
{% endcontent-ref %}

### Recopilación Activa

Interactuamos directamente con el objetivo en esta etapa. Antes de realizar la recopilación activa de información, debemos asegurarnos de tener la autorización requerida para realizar la prueba. De lo contrario, probablemente estemos participando en actividades ilegales. Algunas de las técnicas utilizadas en la etapa de recopilación activa de información incluyen escaneo de puertos, enumeración de DNS, fuerza bruta de directorios, enumeración de hosts virtuales y rastreo/spidering de aplicaciones web.

{% content-ref url="/pages/hwjfsZ7NgjxpBmha0uRA" %}
[Recopilación Activa](/ethical-hacking-cheatsheet/recopilacion-de-informacion/recopilacion-de-informacion/recopilacion-activa.md)
{% endcontent-ref %}

Es fundamental mantener bien organizada la información que recopilamos, ya que necesitaremos varios datos como entrada para fases posteriores del proceso de prueba. Dependiendo del tipo de evaluación que estemos realizando, es posible que necesitemos incluir algunos de estos datos de enumeración en nuestro informe final (como una prueba de penetración externa). Al redactar un informe de recompensas por errores, solo necesitaremos incluir detalles relevantes específicamente para el error que estamos informando (es decir, un subdominio oculto que descubrimos condujo a la divulgación de otro subdominio que aprovechamos para obtener ejecución remota de código (RCE) contra nuestro objetivo).

Vale la pena registrarse para obtener una cuenta en [Hackerone](https://hackerone.com/bug-bounty-programs) , examinar la lista de programas y elegir algunos objetivos para reproducir todos los ejemplos de este módulo. La práctica hace la perfección. La práctica continua de estas técnicas nos ayudará a perfeccionar nuestro oficio y a hacer que muchos de estos pasos de recopilación de información sean algo natural. A medida que nos sintamos más cómodos con las herramientas y técnicas que se muestran a lo largo de este módulo, deberíamos desarrollar nuestra propia metodología repetible. Es posible que descubramos que nos gustan herramientas específicas y técnicas de línea de comandos para algunas fases de recopilación de información y descubramos diferentes herramientas que preferimos para otras fases. Es posible que también queramos escribir nuestros propios scripts para automatizar algunas de estas fases.

***

## <mark style="color:purple;">Hacia adelante</mark>

Sigamos adelante y analicemos la recopilación pasiva de información. Para los ejemplos y ejercicios de la sección del módulo, nos centraremos en Facebook, que tiene su propio [programa de recompensas por errores](https://www.facebook.com/whitehat) , [PayPal](https://hackerone.com/paypal?type=team) , [Tesla](https://bugcrowd.com/tesla) y servidores de laboratorio internos. Al realizar los ejemplos de recopilación de información, debemos asegurarnos de no desviarnos del alcance del programa, que enumera sitios web y aplicaciones dentro y fuera del alcance y ataques fuera de alcance, como ataques a la seguridad física, ingeniería social, la uso de escáneres de vulnerabilidad automatizados, ataques de man-in-the-middle, etc.<br>

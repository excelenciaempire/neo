
# ColdFusion - Enumeración

ColdFusion es un lenguaje de programación y una plataforma de desarrollo de aplicaciones web basada en Java. ColdFusion fue desarrollado inicialmente por Allaire Corporation en 1995 y fue adquirido por Macromedia en 2001. Macromedia fue adquirida posteriormente por Adobe Systems, que ahora posee y desarrolla ColdFusion.

Se utiliza para crear aplicaciones web dinámicas e interactivas que se pueden conectar a varias API y bases de datos como MySQL, Oracle y Microsoft SQL Server. ColdFusion se lanzó por primera vez en 1995 y desde entonces ha evolucionado hasta convertirse en una plataforma potente y versátil para el desarrollo web.

ColdFusion Markup Language (`CFML`) es el lenguaje de programación propietario que se utiliza en ColdFusion para desarrollar aplicaciones web dinámicas. Tiene una sintaxis similar a HTML, lo que facilita su aprendizaje para los desarrolladores web. CFML incluye etiquetas y funciones para la integración de bases de datos, servicios web, gestión de correo electrónico y otras tareas comunes de desarrollo web. Su enfoque basado en etiquetas simplifica el desarrollo de aplicaciones al reducir la cantidad de código necesario para realizar tareas complejas. Por ejemplo, la etiqueta `cfquery` puede ejecutar instrucciones SQL para recuperar datos de una base de datos:

```html
<cfquery name="myQuery" datasource="myDataSource">
  SELECT *
  FROM myTable
</cfquery>
```

Los desarrolladores pueden luego usar la etiqueta `cfloop` para iterar a través de los registros recuperados de la base de datos:

```html
<cfloop query="myQuery">
  <p>#myQuery.firstName# #myQuery.lastName#</p>
</cfloop>
```

Gracias a sus funciones y características integradas, CFML permite a los desarrolladores crear una lógica empresarial compleja utilizando un código mínimo. Además, ColdFusion es compatible con otros lenguajes de programación, como JavaScript y Java, lo que permite a los desarrolladores utilizar su lenguaje de programación preferido dentro del entorno de ColdFusion.

ColdFusion también ofrece compatibilidad con correo electrónico, manipulación de PDF, gráficos y otras funciones de uso común. Las aplicaciones desarrolladas con ColdFusion pueden ejecutarse en cualquier servidor que admita su entorno de ejecución. Está disponible para descargar desde el sitio web de Adobe y se puede instalar en sistemas operativos Windows, Mac o Linux. Las aplicaciones de ColdFusion también se pueden implementar en plataformas en la nube como Amazon Web Services o Microsoft Azure. Algunos de los principales propósitos y beneficios de ColdFusion incluyen:

<table data-header-hidden><thead><tr><th width="223"></th><th></th></tr></thead><tbody><tr><td><strong>Beneficios</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>Desarrollo de aplicaciones web basadas en datos</code></td><td>ColdFusion permite a los desarrolladores crear fácilmente aplicaciones web completas y con capacidad de respuesta. Ofrece administración de sesiones, manejo de formularios, depuración y más funciones. ColdFusion le permite aprovechar su conocimiento existente del lenguaje y lo combina con funciones avanzadas para ayudarlo a crear aplicaciones web sólidas rápidamente.</td></tr><tr><td><code>Integración con bases de datos</code></td><td>ColdFusion se integra fácilmente con bases de datos como Oracle, SQL Server y MySQL. ColdFusion ofrece conectividad avanzada con bases de datos y está diseñado para facilitar la recuperación, manipulación y visualización de datos de una base de datos y de la Web.</td></tr><tr><td><code>Simplificar la gestión de contenidos web</code></td><td>Uno de los principales objetivos de ColdFusion es optimizar la gestión de contenido web. La plataforma ofrece generación dinámica de HTML y simplifica la creación de formularios, la reescritura de URL, la carga de archivos y el manejo de formularios de gran tamaño. Además, ColdFusion también es compatible con AJAX al gestionar automáticamente la serialización y deserialización de componentes habilitados para AJAX.</td></tr><tr><td><code>Performance</code></td><td>ColdFusion está diseñado para ofrecer un alto rendimiento y está optimizado para lograr baja latencia y alto rendimiento. Puede gestionar una gran cantidad de solicitudes simultáneas manteniendo un alto nivel de rendimiento.</td></tr><tr><td><code>Colaboración</code></td><td>ColdFusion ofrece funciones que permiten a los desarrolladores trabajar juntos en proyectos en tiempo real. Esto incluye el uso compartido de código, la depuración, el control de versiones y más. Esto permite un desarrollo más rápido y eficiente, un menor tiempo de comercialización y una entrega más rápida de los proyectos.</td></tr></tbody></table>

A pesar de ser menos popular que otras plataformas de desarrollo web, ColdFusion sigue siendo ampliamente utilizado por desarrolladores y organizaciones de todo el mundo. Gracias a su facilidad de uso, sus rápidas capacidades de desarrollo de aplicaciones y su integración con otras tecnologías web, es una opción ideal para crear aplicaciones web de forma rápida y eficiente. ColdFusion ha evolucionado y, desde su creación, se han publicado nuevas versiones periódicamente.

La última versión estable de ColdFusion, al momento de escribir este artículo, es ColdFusion 2021, y ColdFusion 2023 está a punto de entrar en la fase Alpha. Las versiones anteriores incluyen ColdFusion 2018, ColdFusion 2016 y ColdFusion 11, cada una con nuevas características y mejoras, como mejor rendimiento, integración más sencilla con otras plataformas, seguridad mejorada y mayor facilidad de uso.

Como cualquier tecnología orientada a la web, ColdFusion ha sido vulnerable históricamente a varios tipos de ataques, como inyección SQL, XSS, cruce de directorios, omisión de autenticación y cargas de archivos arbitrarias. Para mejorar la seguridad de ColdFusion, los desarrolladores deben implementar prácticas de codificación seguras, verificaciones de validación de entrada y configurar correctamente los servidores web y los firewalls. A continuación, se muestran algunas vulnerabilidades conocidas de ColdFusion:

1. `CVE-2021-21087`: Prohibición arbitraria de cargar código fuente JSP
2. `CVE-2020-24453`: Configuración incorrecta de la integración de Active Directory
3. `CVE-2020-24450`: vulnerabilidad de inyección de comandos
4. `CVE-2020-24449`: Vulnerabilidad de lectura arbitraria de archivos
5. `CVE-2019-15909`: vulnerabilidad de secuencias de comandos entre sitios (XSS)

ColdFusion expone una buena cantidad de puertos de forma predeterminada:

<table data-header-hidden><thead><tr><th width="121"></th><th width="128"></th><th></th></tr></thead><tbody><tr><td>Número de puerto</td><td>Protocolo</td><td>Descripción</td></tr><tr><td>80</td><td>HTTP</td><td>Se utiliza para la comunicación HTTP no segura entre el servidor web y el navegador web.</td></tr><tr><td>443</td><td>HTTPS</td><td>Se utiliza para la comunicación HTTP segura entre el servidor web y el navegador web. Encripta la comunicación entre el servidor web y el navegador web.</td></tr><tr><td>1935</td><td>RPC</td><td>Se utiliza para la comunicación entre cliente y servidor. El protocolo de llamada a procedimiento remoto (RPC) permite que un programa solicite información a otro programa en un dispositivo de red diferente.</td></tr><tr><td>25</td><td>SMTP</td><td>El Protocolo simple de transferencia de correo (SMTP) se utiliza para enviar mensajes de correo electrónico.</td></tr><tr><td>8500</td><td>SSL</td><td>Se utiliza para la comunicación del servidor a través de Secure Socket Layer (SSL).</td></tr><tr><td>5500</td><td>Monitor de servidor</td><td>Se utiliza para la administración remota del servidor ColdFusion.</td></tr></tbody></table>

Es importante tener en cuenta que los puertos predeterminados se pueden cambiar durante la instalación o configuración.

***

## <mark style="color:purple;">Enumeración</mark>

Durante una enumeración en pruebas de penetración, existen varias formas de identificar si una aplicación web utiliza ColdFusion. Estos son algunos métodos que se pueden utilizar:

<table data-header-hidden><thead><tr><th width="212"></th><th></th></tr></thead><tbody><tr><td><strong>Método</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>Escaneo de puertos</code></td><td>ColdFusion normalmente utiliza el puerto 80 para HTTP y el puerto 443 para HTTPS de forma predeterminada. Por lo tanto, el escaneo de estos puertos puede indicar la presencia de un servidor ColdFusion. Nmap podría identificar ColdFusion durante un escaneo de servicios específicamente.</td></tr><tr><td><code>Extensiones de archivos</code></td><td>Las páginas de ColdFusion suelen utilizar extensiones de archivo "<code>.cfm</code>" o "<code>.cfc</code>". Si encuentra páginas con estas extensiones de archivo, podría ser un indicador de que la aplicación utiliza ColdFusion.</td></tr><tr><td><code>HTTP Headers</code></td><td>Compruebe los encabezados de respuesta HTTP de la aplicación web. ColdFusion normalmente establece encabezados específicos, como "Server: ColdFusion" o "X-Powered-By: ColdFusion", que pueden ayudar a identificar la tecnología que se está utilizando.</td></tr><tr><td><code>Mensajes de error</code></td><td>Si la aplicación utiliza ColdFusion y hay errores, los mensajes de error pueden contener referencias a etiquetas o funciones específicas de ColdFusion.</td></tr><tr><td><code>Archivos por defecto</code></td><td>ColdFusion crea varios archivos predeterminados durante la instalación, como "<code>admin.cfm</code>" o "CFIDE/administrator/index.cfm". Encontrar estos archivos en el servidor web puede indicar que la aplicación web se ejecuta en ColdFusion.</td></tr></tbody></table>

### **Resultados de escaneo con NMap**

```shell-session
afsh4ck@kali$ nmap -p- -sC -Pn 10.129.247.30 --open

Starting Nmap 7.92 ( https://nmap.org ) at 2023-03-13 11:45 GMT
Nmap scan report for 10.129.247.30
Host is up (0.028s latency).
Not shown: 65532 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE
135/tcp   open  msrpc
8500/tcp  open  fmtp
49154/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 350.38 seconds
```

Los resultados del análisis de puertos muestran tres puertos abiertos. Dos servicios RPC de Windows y uno que se ejecuta en 8500. Como sabemos, 8500 es un puerto predeterminado que ColdFusion usa para SSL. Al navegar al puerto 8500 enumeramos 2 directorios, `CFIDE` y `cfdocs`, en la raíz, lo que indica además que ColdFusion se está ejecutando en el puerto 8500.

### Enumeración en directorios

Navegar un poco por la estructura muestra mucha información interesante, desde archivos con una extensión clara `.cfm` hasta mensajes de error y páginas de inicio de sesión.

![](https://academy.hackthebox.com/storage/modules/113/coldfusion/CFIDE.png)

![](https://academy.hackthebox.com/storage/modules/113/coldfusion/CFError.png)

### Ruta de administración

Sin embargo, la ruta `/CFIDE/administrator` carga la página de inicio de sesión del administrador de ColdFusion 8. Ahora sabemos con certeza que `ColdFusion 8`se está ejecutando en el servidor.

![](https://academy.hackthebox.com/storage/modules/113/coldfusion/CF8.png)

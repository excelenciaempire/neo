
# Tomcat - Enumeración

## <mark style="color:purple;">Tomcat - Descubrimiento y enumeración</mark>

***

[Apache Tomcat](https://tomcat.apache.org/) es un servidor web de código abierto que aloja aplicaciones escritas en Java. Tomcat fue diseñado inicialmente para ejecutar servlets de Java y scripts de Java Server Pages (JSP). Sin embargo, su popularidad aumentó en los marcos basados ​​en Java y ahora se usa ampliamente en marcos como Spring y herramientas como Gradle. Según los datos recopilados por [BuiltWith,](https://trends.builtwith.com/Web-Server/Apache-Tomcat-Coyote) en este momento hay más de 220.000 sitios web activos con Tomcat. A continuación, se muestran algunas estadísticas más interesantes:

* BuiltWith ha recopilado datos que muestran que más de 904.000 sitios web han utilizado Tomcat en algún momento.
* El 1,22% del millón de sitios web más importantes utilizan Tomcat, mientras que el 3,8% de los 100.000 sitios web más importantes utilizan Tomcat.
* Tomcat ocupa la posición [número 13](https://webtechsurvey.com/technology/apache-tomcat) entre los servidores web por participación de mercado
* Algunas organizaciones que utilizan Tomcat incluyen Alibaba, la Oficina de Patentes y Marcas de los Estados Unidos (USPTO), la Cruz Roja Estadounidense y el LA Times.

Sin embargo, Tomcat suele ser menos propenso a quedar expuesto a Internet. Lo vemos de vez en cuando en pruebas de penetración externas y puede ser un excelente punto de apoyo en la red interna. Es mucho más común ver Tomcat (y varias instancias, de hecho) durante pruebas de penetración internas. Por lo general, ocupará el primer lugar en "Objetivos de alto valor" dentro de un informe de EyeWitness y, en la mayoría de los casos, al menos una instancia interna está configurada con credenciales débiles o predeterminadas. Más sobre eso más adelante.

***

## <mark style="color:purple;">Discovery / Footprinting</mark>

Durante nuestra prueba de penetración externa, ejecutamos EyeWitness y vemos un host en la lista de "Objetivos de alto valor". La herramienta cree que el host está ejecutando Tomcat, pero debemos confirmarlo para planificar nuestros ataques. Si estamos tratando con Tomcat en la red externa, esto podría ser un punto de apoyo fácil en el entorno de la red interna.

Los servidores Tomcat se pueden identificar por el encabezado Server en la respuesta HTTP. Si el servidor está funcionando detrás de un proxy inverso, al solicitar una página no válida se debería revelar el servidor y la versión. Aquí podemos ver qué versión de Tomcat `9.0.30`está en uso.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/tomcat_invalid.png" alt=""><figcaption></figcaption></figure>

Es posible que se utilicen páginas de error personalizadas que no filtren esta información de versión. En este caso, otro método para detectar un servidor Tomcat y una versión es a través de la página `/docs`.

```shell-session
afsh4ck@kali$ curl -s http://app-dev.inlanefreight.local:8080/docs/ | grep Tomcat 

<html lang="en"><head><META http-equiv="Content-Type" content="text/html; charset=UTF-8"><link href="./images/docs-stylesheet.css" rel="stylesheet" type="text/css"><title>Apache Tomcat 9 (9.0.30) - Documentation Index</title><meta name="author" 

<SNIP>
```

Esta es la página de documentación predeterminada, que los administradores no pueden eliminar. Esta es la estructura general de carpetas de una instalación de Tomcat.

```shell-session
├── bin
├── conf
│   ├── catalina.policy
│   ├── catalina.properties
│   ├── context.xml
│   ├── tomcat-users.xml
│   ├── tomcat-users.xsd
│   └── web.xml
├── lib
├── logs
├── temp
├── webapps
│   ├── manager
│   │   ├── images
│   │   ├── META-INF
│   │   └── WEB-INF
|   |       └── web.xml
│   └── ROOT
│       └── WEB-INF
└── work
    └── Catalina
        └── localhost
```

* La carpeta `bin` almacena los scripts y los archivos binarios necesarios para iniciar y ejecutar un servidor Tomcat.&#x20;
* La carpeta `conf` almacena varios archivos de configuración utilizados por Tomcat.&#x20;
* El archivo  `tomcat-users.xml` almacena las credenciales de usuario y sus roles asignados.&#x20;
* La carpeta `lib` contiene los distintos archivos JAR necesarios para el correcto funcionamiento de Tomcat.&#x20;
* Las carpetas `logs` y `temp` almacenan archivos de registro temporales.&#x20;
* La carpeta `webapps` es la raíz web predeterminada de Tomcat y aloja todas las aplicaciones.&#x20;
* La carpeta `work` actúa como caché y se utiliza para almacenar datos durante el tiempo de ejecución.

Se espera que cada carpeta interna tenga `webapps` la siguiente estructura.

```shell-session
webapps/customapp
├── images
├── index.jsp
├── META-INF
│   └── context.xml
├── status.xsd
└── WEB-INF
    ├── jsp
    |   └── admin.jsp
    └── web.xml
    └── lib
    |    └── jdbc_drivers.jar
    └── classes
        └── AdminServlet.class   
```

* El archivo más importante de estos es `WEB-INF/web.xml`, que se conoce como descriptor de implementación. Este archivo almacena información sobre las rutas utilizadas por la aplicación y las clases que manejan estas rutas.&#x20;
* Todas las clases compiladas utilizadas por la aplicación deben almacenarse en la carpeta `WEB-INF/classes`. Estas clases pueden contener lógica empresarial importante, así como información confidencial. Cualquier vulnerabilidad en estos archivos puede provocar un compromiso total del sitio web.&#x20;
* La carpeta `lib` almacena las bibliotecas que necesita esa aplicación en particular.&#x20;
* La carpeta `jsp` almacena [Jakarta Server Pages (JSP)](https://en.wikipedia.org/wiki/Jakarta_Server_Pages) , anteriormente conocida como `JavaServer Pages`, que se puede comparar con los archivos PHP en un servidor Apache.

A continuación se muestra un ejemplo de archivo web.xml.

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>

<!DOCTYPE web-app PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN" "http://java.sun.com/dtd/web-app_2_3.dtd">

<web-app>
  <servlet>
    <servlet-name>AdminServlet</servlet-name>
    <servlet-class>com.inlanefreight.api.AdminServlet</servlet-class>
  </servlet>

  <servlet-mapping>
    <servlet-name>AdminServlet</servlet-name>
    <url-pattern>/admin</url-pattern>
  </servlet-mapping>
</web-app>   
```

La configuración `web.xml` anterior define un nuevo servlet llamado `AdminServlet` que se asigna a la clase `com.inlanefreight.api.AdminServlet`. Java utiliza la notación de puntos para crear nombres de paquetes, lo que significa que la ruta en el disco para la clase definida anteriormente sería:

* `classes/com/inlanefreight/api/AdminServlet.class`

A continuación, se crea una nueva asignación de servlet para asignar solicitudes a `/admin` con `AdminServlet`. Esta configuración enviará cualquier solicitud recibida en `/admin` a la clase `AdminServlet.class` para su procesamiento. El descriptor `web.xml` contiene mucha información confidencial y es un archivo importante que se debe verificar cuando se aprovecha una vulnerabilidad de inclusión de archivos locales (LFI).

El archivo `tomcat-users.xml` se utiliza para permitir o no permitir el acceso a las páginas `/manager` y `host-manager` de administración.

```xml
<?xml version="1.0" encoding="UTF-8"?>

<SNIP>
  
<tomcat-users xmlns="http://tomcat.apache.org/xml"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
              version="1.0">
<!--
  By default, no user is included in the "manager-gui" role required
  to operate the "/manager/html" web application.  If you wish to use this app,
  you must define such a user - the username and password are arbitrary.

  Built-in Tomcat manager roles:
    - manager-gui    - allows access to the HTML GUI and the status pages
    - manager-script - allows access to the HTTP API and the status pages
    - manager-jmx    - allows access to the JMX proxy and the status pages
    - manager-status - allows access to the status pages only

  The users below are wrapped in a comment and are therefore ignored. If you
  wish to configure one or more of these users for use with the manager web
  application, do not forget to remove the <!.. ..> that surrounds them. You
  will also need to set the passwords to something appropriate.
-->

   
 <SNIP>
  
!-- user manager can access only manager section -->
<role rolename="manager-gui" />
<user username="tomcat" password="tomcat" roles="manager-gui" />

<!-- user admin can access manager and admin section both -->
<role rolename="admin-gui" />
<user username="admin" password="admin" roles="manager-gui,admin-gui" />


</tomcat-users>
```

El archivo nos muestra a qué dan acceso cada uno de los roles `manager-gui`, `manager-script`, `manager-jmx` y `manager-status`. En este ejemplo, podemos ver que un usuario `tomcat` con la contraseña `tomcat` tiene el rol `manager-gui` y para el usuario `admin` se establece una segunda contraseña débil para la cuenta: `admin`

***

## <mark style="color:purple;">Enumeración</mark>

Después de identificar la instancia de Tomcat, a menos que tenga una vulnerabilidad conocida, normalmente buscaremos las páginas `/manager` y `/host-manager`. Podemos intentar localizarlas con una herramienta como `Gobuster` o simplemente navegar hasta ellas directamente.

```shell-session
afsh4ck@kali$ gobuster dir -u http://web01.inlanefreight.local:8180/ -w /usr/share/dirbuster/wordlists/directory-list-2.3-small.txt 

===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://web01.inlanefreight.local:8180/
[+] Threads:        10
[+] Wordlist:       /usr/share/dirbuster/wordlists/directory-list-2.3-small.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2021/09/21 17:34:54 Starting gobuster
===============================================================
/docs (Status: 302)
/examples (Status: 302)
/manager (Status: 302)
Progress: 49959 / 87665 (56.99%)^C
[!] Keyboard interrupt detected, terminating.
===============================================================
2021/09/21 17:44:29 Finished
===============================================================
```

Es posible que podamos iniciar sesión en uno de estos sitios utilizando credenciales débiles como `tomcat:tomcat`, `admin:admin`, etc. Si estos primeros intentos no funcionan, podemos intentar un ataque de fuerza bruta de contraseña contra la página de inicio de sesión, que se explica en la siguiente sección. Si logramos iniciar sesión, podemos cargar un archivo [de recursos de aplicación web o](https://en.wikipedia.org/wiki/WAR_\(file_format\)#:~:text=In%20software%20engineering%2C%20a%20WAR,that%20together%20constitute%20a%20web) un archivo de archivo de aplicación web (WAR) que contenga un shell web JSP y obtener la ejecución remota de código en el servidor Tomcat.

Ahora que hemos aprendido sobre la estructura y función de Tomcat, ataquémoslo abusando de la funcionalidad incorporada y explotando una vulnerabilidad bien conocida que afectó a versiones específicas de Tomcat.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo(s): 10.129.201.58 (ACADEMY-ATCKAPPS-APP02) 

vHosts necesarios para estas preguntas:

app-dev.inlanefreight.local
web01.inlanefreight.local
```

> ¿Qué versión de Tomcat se está ejecutando en la aplicación ubicada en <http://web01.inlanefreight.local:8180>?

Podemos hacer un curl del directorio `/docs` para intentar sacar la versión:

```bash
curl -s http://web01.inlanefreight.local:8180/docs/ | grep Tomcat 
<html lang="en"><head><META http-equiv="Content-Type" content="text/html; charset=UTF-8"><link href="./images/docs-stylesheet.css" rel="stylesheet" type="text/css">
<title>Apache Tomcat 10 (10.0.10) - Documentation Index</title><meta name="author" content="Craig R. McClanahan"><meta name="author" content="Remy Maucherat"><meta name="author" content="Yoav Shapira">
</head><body><div id="wrapper"><header><div id="header"><div><div><div class="logo noPrint"><a href="https://tomcat.apache.org/"><img alt="Tomcat Home" src="./images/tomcat.png"></a></div><div style="height: 1px;"></div><div class="asfLogo noPrint"><a href="https://www.apache.org/" target="_blank"><img src="./images/asf-logo.svg" alt="The Apache Software Foundation" style="width: 266px; height: 83px;"></a></div><h1>Apache Tomcat 10</h1><div class="versionInfo">
```

Obtenemos correctamente la versión: `10.0.10`

> ¿Qué rol tiene el usuario administrador en el ejemplo de configuración?

Concretamente tiene el rol admin-gui

```html
<user username="admin" password="admin" roles="manager-gui,admin-gui" />
```

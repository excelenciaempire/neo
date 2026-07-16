
# Jenkins - Enumeración

## <mark style="color:purple;">Jenkins - Descubrimiento y enumeración</mark>

***

[Jenkins](https://www.jenkins.io/) es un servidor de automatización de código abierto escrito en Java que ayuda a los desarrolladores a crear y probar sus proyectos de software de forma continua. Es un sistema basado en servidor que se ejecuta en contenedores de servlets como Tomcat. A lo largo de los años, los investigadores han descubierto varias vulnerabilidades en Jenkins, incluidas algunas que permiten la ejecución remota de código sin necesidad de autenticación. Jenkins es un servidor [de integración continua](https://en.wikipedia.org/wiki/Continuous_integration) . A continuación, se muestran algunos puntos interesantes sobre Jenkins:

* Jenkins se llamó originalmente Hudson (lanzado en 2005) y fue renombrado en 2011 después de una disputa con Oracle.
* [Los datos](https://discovery.hgdata.com/product/jenkins) muestran que más de 86.000 empresas utilizan Jenkins
* Jenkins es utilizado por empresas conocidas como Facebook, Netflix, Udemy, Robinhood y LinkedIn.
* Tiene más de 300 complementos para respaldar proyectos de creación y prueba.

***

## <mark style="color:purple;">Discovery / Footprinting</mark>

Supongamos que estamos trabajando en una prueba de penetración interna y hemos completado nuestros análisis de detección web. Observamos lo que creemos que es una instancia de Jenkins y sabemos que suele estar instalada en servidores Windows que se ejecutan como la poderosa cuenta SYSTEM. Si podemos obtener acceso a través de Jenkins y obtener ejecución remota de código como la cuenta SYSTEM, tendríamos un punto de apoyo en Active Directory para comenzar la enumeración del entorno del dominio.

Jenkins se ejecuta en el puerto 8080 de Tomcat de forma predeterminada. También utiliza el puerto 5000 para conectar servidores esclavos. Este puerto se utiliza para la comunicación entre servidores maestros y esclavos. Jenkins puede utilizar una base de datos local, LDAP, una base de datos de usuarios de Unix, delegar la seguridad a un contenedor de servlets o no utilizar ninguna autenticación. Los administradores también pueden permitir o prohibir que los usuarios creen cuentas.

***

## <mark style="color:purple;">Enumeración</mark>

<figure><img src="https://academy.hackthebox.com/storage/modules/113/jenkins_global_security.png" alt=""><figcaption></figcaption></figure>

La instalación predeterminada generalmente utiliza la base de datos de Jenkins para almacenar credenciales y no permite que los usuarios registren una cuenta. Podemos identificar rápidamente a Jenkins mediante la página de inicio de sesión.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/jenkins_login.png" alt=""><figcaption></figcaption></figure>

Es posible que nos encontremos con una instancia de Jenkins que utilice credenciales débiles o predeterminadas, como por ejemplo `admin:admin`, o que no tenga habilitado ningún tipo de autenticación. No es raro encontrar instancias de Jenkins que no requieran ninguna autenticación durante una prueba de penetración interna. Si bien es poco frecuente, nos hemos encontrado con Jenkins durante pruebas de penetración externas que pudimos atacar.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo(s): 10.129.201.58 (ACADEMY-ATCKAPPS-APP02) 

vHosts necesarios para estas preguntas:
jenkins.inlanefreight.local
```

> Inicia sesión en la instancia de Jenkins en <http://jenkins.inlanefreight.local:8000>. Navega por la instancia y envía el número de versión.

<figure><img src="/files/dziAxqLHc2OAwbZLdCOD" alt=""><figcaption></figcaption></figure>

Probamos con las credenciales por defecto: `admin:admin` y conseguimos acceder sin problema:

<figure><img src="/files/v47z4JnuoIQ5dXXd9jNH" alt=""><figcaption></figcaption></figure>

En la parte inferior de la página podemos observar que está explícita la versión: `2.303.1`

También podemos obtener la versión con curl:

```shell-session
afsh4ck@kali$ curl -I http://jenkins.inlanefreight.local:8000

HTTP/1.1 403 Forbidden
Date: Fri, 10 Jan 2025 15:51:26 GMT
X-Content-Type-Options: nosniff
Set-Cookie: JSESSIONID.8e925b92=node05rjk5n16av3r1lm8vzbbf7t572.node0; Path=/; HttpOnly
Expires: Thu, 01 Jan 1970 00:00:00 GMT
Content-Type: text/html;charset=utf-8
X-Hudson: 1.395
X-Jenkins: 2.303.1
X-Jenkins-Session: d60b8256
Content-Length: 541
Server: Jetty(9.4.42.v20210604)
```

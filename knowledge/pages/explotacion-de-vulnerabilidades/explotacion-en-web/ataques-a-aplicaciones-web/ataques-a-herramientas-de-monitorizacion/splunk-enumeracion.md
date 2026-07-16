
# Splunk - Enumeración

## <mark style="color:purple;">Splunk - Discovery y enumeración</mark>

***

Splunk es una herramienta de análisis de registros que se utiliza para recopilar, analizar y visualizar datos. Aunque originalmente no estaba pensada para ser una herramienta SIEM, Splunk se suele utilizar para la supervisión de la seguridad y el análisis empresarial. Las implementaciones de Splunk suelen utilizarse para almacenar datos confidenciales y podrían proporcionar una gran cantidad de información a un atacante si se ven comprometidas. Históricamente, Splunk no ha sufrido muchas vulnerabilidades conocidas aparte de una vulnerabilidad de divulgación de información (CVE-2018-11409) y una vulnerabilidad de ejecución remota de código autenticado en versiones muy antiguas (CVE-2011-4642). A continuación, se ofrecen algunos [detalles](https://www.splunk.com/en_us/customers.html) sobre Splunk:

* Splunk se fundó en 2003, comenzó a ser rentable en 2009 y tuvo su oferta pública inicial (IPO) en 2012 en NASDAQ bajo el símbolo SPLK.
* Splunk tiene más de 7500 empleados y unos ingresos anuales de casi 2400 millones de dólares.
* En 2020, Splunk fue incluido en la lista Fortune 1000
* Los clientes de Splunk incluyen 92 empresas de la lista Fortune 100
* [Splunkbase](https://splunkbase.splunk.com/) permite a los usuarios de Splunk descargar aplicaciones y complementos para Splunk. A partir de 2021, hay más de 2000 aplicaciones disponibles

En la mayoría de los casos, durante nuestras evaluaciones, veremos Splunk, especialmente en grandes entornos corporativos durante pruebas de penetración internas. Lo hemos visto expuesto externamente, pero esto es menos frecuente. Splunk no sufre muchas vulnerabilidades explotables y soluciona rápidamente cualquier problema. El principal objetivo de Splunk durante una evaluación sería la autenticación débil o nula, ya que el acceso de administrador a Splunk nos da la capacidad de implementar aplicaciones personalizadas que se pueden usar para comprometer rápidamente un servidor Splunk y posiblemente otros hosts en la red, según la forma en que esté configurado Splunk.

***

## <mark style="color:purple;">Discovery / Footprinting</mark>

Splunk está muy extendido en las redes internas y suele ejecutarse como raíz en Linux o como SYSTEM en sistemas Windows. Aunque no es habitual, a veces podemos encontrar Splunk en el exterior. Imaginemos que descubrimos una instancia olvidada de Splunk en nuestro informe de Aquatone que, desde entonces, se ha convertido automáticamente a la versión gratuita, que no requiere autenticación. Como todavía no hemos logrado afianzarnos en la red interna, centremos nuestra atención en Splunk y veamos si podemos convertir este acceso en RCE.

El servidor web Splunk se ejecuta de forma predeterminada en el puerto 8000. En versiones anteriores de Splunk, las credenciales predeterminadas son `admin:changeme`, que se muestran convenientemente en la página de inicio de sesión.

![imagen](https://academy.hackthebox.com/storage/modules/113/changme.png)

La última versión de Splunk establece las credenciales durante el proceso de instalación. Si las credenciales predeterminadas no funcionan, vale la pena comprobar si hay contraseñas débiles comunes como `admin`, `Welcome`, `Welcome1`, `Password123`, etc.

![imagen](https://academy.hackthebox.com/storage/modules/113/splunk_login.png)

Podemos descubrir Splunk con un escaneo rápido del servicio Nmap. Aquí podemos ver que Nmap identificó el servicio `Splunkd httpd` en el puerto 8000 y el puerto 8089, el puerto de administración de Splunk para la comunicación con la API REST de Splunk.

```shell-session
afsh4ck@kali$ sudo nmap -sV 10.129.201.50

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-22 08:43 EDT
Nmap scan report for 10.129.201.50
Host is up (0.11s latency).
Not shown: 991 closed ports
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
5357/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
8000/tcp open  ssl/http      Splunkd httpd
8080/tcp open  http          Indy httpd 17.3.33.2830 (Paessler PRTG bandwidth monitor)
8089/tcp open  ssl/http      Splunkd httpd
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 39.22 seconds
```

***

## <mark style="color:purple;">Enumeración</mark>

La versión de prueba de Splunk Enterprise se convierte en una versión gratuita después de 60 días, que no requiere autenticación. No es raro que los administradores de sistemas instalen una versión de prueba de Splunk para probarla, pero luego se olvidan de ella. Esto convertirá automáticamente a la versión gratuita que no tiene ningún tipo de autenticación, lo que introduce un agujero de seguridad en el entorno. Algunas organizaciones pueden optar por la versión gratuita debido a limitaciones presupuestarias, sin comprender completamente las implicaciones de no tener administración de usuarios/roles.

![imagen](https://academy.hackthebox.com/storage/modules/113/license_group.png)

Una vez iniciada la sesión en Splunk (o habiendo accedido a una instancia de Splunk Free), podemos explorar datos, ejecutar informes, crear paneles, instalar aplicaciones de la biblioteca Splunkbase e instalar aplicaciones personalizadas.  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/113/splunk_home.png" alt=""><figcaption></figcaption></figure>

Splunk tiene múltiples formas de ejecutar código, como aplicaciones Django del lado del servidor, puntos finales REST, entradas con scripts y scripts de alerta. Un método común para obtener ejecución remota de código en un servidor Splunk es mediante el uso de una entrada con scripts. Estos están diseñados para ayudar a integrar Splunk con fuentes de datos como API o servidores de archivos que requieren métodos personalizados para acceder. Las entradas con scripts están diseñadas para ejecutar estos scripts, con STDOUT proporcionado como entrada a Splunk.

Como Splunk se puede instalar en hosts de Windows o Linux, se pueden crear entradas con scripts para ejecutar scripts de Bash, PowerShell o Batch. Además, cada instalación de Splunk viene con Python instalado, por lo que los scripts de Python se pueden ejecutar en cualquier sistema Splunk. Una forma rápida de obtener RCE es crear una entrada con scripts que le indique a Splunk que ejecute un script de shell inverso de Python. Trataremos este tema en la siguiente sección.

Además de esta funcionalidad incorporada, Splunk ha sufrido varias vulnerabilidades públicas a lo largo de los años, como esta [SSRF](https://www.exploit-db.com/exploits/40895) que podría usarse para obtener acceso no autorizado a la API REST de Splunk. Al momento de escribir este artículo, Splunk tiene [47](https://www.cvedetails.com/vulnerability-list/vendor_id-10963/Splunk.html) CVE. Si realizamos un análisis de vulnerabilidades contra Splunk durante una prueba de penetración, a menudo veremos que se devuelven muchas vulnerabilidades no explotables. Por eso es importante comprender cómo abusar de la funcionalidad incorporada.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.174.130
```

> Enumera la instancia de Splunk como un usuario no autenticado. Envía el número de versión para continuar (formato 1.2.3).

<figure><img src="/files/G6FXkLo5GxigFgUOjZ5W" alt=""><figcaption></figcaption></figure>

Lo primero vamos a hacer un escaneo de puertos con nmap:

```shell-session
afsh4ck@kali$ sudo nmap -v -sV -T5 10.129.174.130

PORT      STATE    SERVICE        VERSION
79/tcp    filtered finger
80/tcp    open     http           Microsoft IIS httpd 10.0
135/tcp   open     msrpc          Microsoft Windows RPC
139/tcp   open     netbios-ssn    Microsoft Windows netbios-ssn
8000/tcp  open     ssl/http       Splunkd httpd
8080/tcp  open     http           Indy httpd 18.1.37.13946 (Paessler PRTG bandwidth monitor)
8089/tcp  open     ssl/http       Splunkd httpd

Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Vemos que por defecto Splunk está corriendo por el puerto 8000. Accedemos con las credenciales por defecto: `admin:changeme`. En el Monitoring Console obtenemos la versión de Splunk:

<figure><img src="/files/Cc88sVStkBOTZkEpOl85" alt=""><figcaption></figcaption></figure>

Si tiene credenciales por defecto podemos obtener la versión de Splunk con el siguiente comando:

```shell-session
afsh4ck@kali$ curl -k -u admin:changeme https://10.129.174.130:8089/services/server/info
 
<?xml version="1.0" encoding="UTF-8"?>
<!--This is to override browser formatting; see server.conf[httpServer] to disable. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .-->
<?xml-stylesheet type="text/xml" href="/static/atom.xsl"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:s="http://dev.splunk.com/ns/rest" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
  <title>server-info</title>
  <id>https://10.129.174.130:8089/services/server/info</id>
  <updated>2025-01-10T08:22:38-08:00</updated>
  <generator build="87344edfcdb4" version="8.2.2"/>
  <author>
    <name>Splunk</name>
```

Concretamente vemos que usa la versión `8.2.2`

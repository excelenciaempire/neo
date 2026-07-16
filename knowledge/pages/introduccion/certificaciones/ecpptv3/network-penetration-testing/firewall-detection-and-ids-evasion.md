
# Firewall Detection & IDS Evasion

### Introducción

Durante escaneos de red, los sistemas de seguridad como **firewalls, IDS (Intrusion Detection Systems) y EDR** pueden detectar y bloquear actividades sospechosas.

\
Nmap incluye múltiples técnicas para **evadir estos mecanismos** y realizar análisis más sigilosos.

***

### Nmap - Opciones de evasión

```bash
nmap -h
```

```bash
-f                     # Fragmenta los paquetes
--mtu <val>            # Define tamaño de fragmentación
-D <decoy1,decoy2,...> # Uso de IPs señuelo (decoys)
-S <IP_Address>        # Spoofing de IP origen
-e <iface>             # Especificar interfaz de red
-g <port>              # Usar puerto origen específico
--source-port <port>
--proxies <url1,...>   # Enviar tráfico a través de proxies
--data <hex>           # Añadir payload personalizado (hex)
--data-string <str>    # Añadir payload ASCII
--data-length <num>    # Añadir datos aleatorios
--ip-options <opts>    # Opciones IP personalizadas
--ttl <val>            # Modificar TTL
--spoof-mac <mac>      # Spoofing de dirección MAC
--badsum               # Enviar checksums inválidos
```

### Ejemplos prácticos

#### 🔹 Escaneo básico SYN (rápido)

```bash
nmap -v -Pn -sS -F 10.10.10.10
```

* `-Pn` → omite descubrimiento de host (evita ICMP block)
* `-sS` → escaneo SYN (más sigiloso)
* `-F` → escaneo rápido (menos puertos)

***

#### 🔹 Escaneo con fragmentación (evasión básica)

```bash
nmap -v -Pn -sV -F -f 10.10.10.10
```

* `-f` → fragmenta paquetes para evitar detección

***

#### 🔹 Escaneo con decoys + padding

```bash
nmap -v -Pn -sV --data-length 200 -D 10.10.10.1,10.10.10.2 10.10.10.3
```

* `--data-length 200` → añade ruido a paquetes
* `-D` → oculta tu IP real entre otras

***

### &#x20;Técnicas clave de evasión

<table><thead><tr><th width="192.66668701171875">Técnica</th><th>Descripción</th></tr></thead><tbody><tr><td>Fragmentación</td><td>Divide paquetes para evitar inspección profunda</td></tr><tr><td>Decoys</td><td>Oculta la IP real entre múltiples IPs falsas</td></tr><tr><td>Spoofing</td><td>Falsifica IP o MAC</td></tr><tr><td>Padding</td><td>Añade datos aleatorios para confundir firmas</td></tr><tr><td>TTL Manipulation</td><td>Cambia el comportamiento del paquete</td></tr><tr><td>Proxies</td><td>Redirige tráfico para ocultar origen</td></tr></tbody></table>

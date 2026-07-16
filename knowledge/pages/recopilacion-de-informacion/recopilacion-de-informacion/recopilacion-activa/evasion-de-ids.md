
# Evasión de IDS

***

## <mark style="color:purple;">Firewall</mark>

Un firewall es una medida de seguridad contra intentos de conexión no autorizados desde redes externas. Cada sistema de seguridad de firewall se basa en un componente de software que monitorea el tráfico de red entre el firewall y las conexiones de datos entrantes y decide cómo manejar la conexión según las reglas que se han establecido. Comprueba si se pasan, ignoran o bloquean paquetes de red individuales. Este mecanismo está diseñado para evitar conexiones no deseadas que podrían ser potencialmente peligrosas.

***

## <mark style="color:purple;">IDS/IPS</mark>

Al igual que el firewall, el sistema de detección de intrusiones (`IDS`) y el sistema de prevención de intrusiones ( `IPS`) también son componentes basados ​​en software. Un `IDS` escanea la red en busca de posibles ataques, los analiza e informa cualquier ataque detectado. Un `IPS` se complementa de `IDS` tomando medidas defensivas específicas si se hubiera detectado un posible ataque. El análisis de este tipo de ataques se basa en la coincidencia de patrones y firmas. Si se detectan patrones específicos, como un análisis de detección de servicios, el `IPS` es posible que se impida los intentos de conexión pendientes.

### Snort

**Snort** es un sistema de detección y prevención de intrusiones (IDS/IPS) basado en la red, que analiza el tráfico en tiempo real para detectar actividades sospechosas o maliciosas. Es desarrollado por **Cisco** y permite realizar análisis de tráfico, registro de paquetes y protección activa al bloquear o prevenir amenazas detectadas.

{% embed url="<https://www.snort.org/snort3>" %}

***

## <mark style="color:purple;">**Determinar los firewall y sus reglas**</mark>

Ya sabemos que cuando un puerto se muestra como filtrado puede deberse a varios motivos. En la mayoría de los casos, los firewalls tienen ciertas reglas establecidas para manejar conexiones específicas. Los paquetes pueden ser `dropped` o `rejected`.&#x20;

* Los paquetes `dropped` se ignoran y el host no devuelve ninguna respuesta.
* Los paquetes `rejected` se devuelven con una flag `RST`. Estos paquetes contienen diferentes tipos de códigos de error ICMP o no contienen nada en absoluto.

Tales errores pueden ser:

* Red inalcanzable
* Red prohibida
* Host inalcanzable
* Host prohibido
* Puerto inalcanzable
* Protocolo inalcanzable

El método de escaneo TCP ACK (`-sA`) de Nmap es mucho más difícil de filtrar para firewalls y sistemas IDS/IPS que los escaneos SYN (`-sS`) o Connect (`sT`) normales porque solo envían un paquete TCP con solo la flag `ACK`. Cuando un puerto está cerrado o abierto, el host debe responder con una flag `RST`. A diferencia de las conexiones salientes, todos los intentos de conexión (con la flag`SYN`) desde redes externas suelen estar bloqueados por firewalls. Sin embargo, los paquetes con la flag `ACK`a menudo pasan por el firewall porque el firewall no puede determinar si la conexión se estableció primero desde la red externa o la red interna.

### **Escaneo SYN-Scan**

Si observamos estos escaneos, veremos cómo los resultados difieren.

```bash
sudo nmap 10.129.2.28 -p 21,22,25 -sS -Pn -n --disable-arp-ping --packet-trace

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-21 14:56 CEST
SENT (0.0278s) TCP 10.10.14.2:57347 > 10.129.2.28:22 S ttl=53 id=22412 iplen=44  seq=4092255222 win=1024 <mss 1460>
SENT (0.0278s) TCP 10.10.14.2:57347 > 10.129.2.28:25 S ttl=50 id=62291 iplen=44  seq=4092255222 win=1024 <mss 1460>
SENT (0.0278s) TCP 10.10.14.2:57347 > 10.129.2.28:21 S ttl=58 id=38696 iplen=44  seq=4092255222 win=1024 <mss 1460>
RCVD (0.0329s) ICMP [10.129.2.28 > 10.10.14.2 Port 21 unreachable (type=3/code=3) ] IP [ttl=64 id=40884 iplen=72 ]
RCVD (0.0341s) TCP 10.129.2.28:22 > 10.10.14.2:57347 SA ttl=64 id=0 iplen=44  seq=1153454414 win=64240 <mss 1460>
RCVD (1.0386s) TCP 10.129.2.28:22 > 10.10.14.2:57347 SA ttl=64 id=0 iplen=44  seq=1153454414 win=64240 <mss 1460>
SENT (1.1366s) TCP 10.10.14.2:57348 > 10.129.2.28:25 S ttl=44 id=6796 iplen=44  seq=4092320759 win=1024 <mss 1460>
Nmap scan report for 10.129.2.28
Host is up (0.0053s latency).

PORT   STATE    SERVICE
21/tcp filtered ftp
22/tcp open     ssh
25/tcp filtered smtp
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 0.07 seconds
```

### **Escaneo ACK-Scan**

```bash
sudo nmap 10.129.2.28 -p 21,22,25 -sA -Pn -n --disable-arp-ping --packet-trace

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-21 14:57 CEST
SENT (0.0422s) TCP 10.10.14.2:49343 > 10.129.2.28:21 A ttl=49 id=12381 iplen=40  seq=0 win=1024
SENT (0.0423s) TCP 10.10.14.2:49343 > 10.129.2.28:22 A ttl=41 id=5146 iplen=40  seq=0 win=1024
SENT (0.0423s) TCP 10.10.14.2:49343 > 10.129.2.28:25 A ttl=49 id=5800 iplen=40  seq=0 win=1024
RCVD (0.1252s) ICMP [10.129.2.28 > 10.10.14.2 Port 21 unreachable (type=3/code=3) ] IP [ttl=64 id=55628 iplen=68 ]
RCVD (0.1268s) TCP 10.129.2.28:22 > 10.10.14.2:49343 R ttl=64 id=0 iplen=40  seq=1660784500 win=0
SENT (1.3837s) TCP 10.10.14.2:49344 > 10.129.2.28:25 A ttl=59 id=21915 iplen=40  seq=0 win=1024
Nmap scan report for 10.129.2.28
Host is up (0.083s latency).

PORT   STATE      SERVICE
21/tcp filtered   ftp
22/tcp unfiltered ssh
25/tcp filtered   smtp
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 0.15 seconds
```

<table data-header-hidden><thead><tr><th width="231"></th><th></th></tr></thead><tbody><tr><td><strong>Opciones de escaneo</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>10.129.2.28</code></td><td>Escanea el objetivo especificado.</td></tr><tr><td><code>-p 21,22,25</code></td><td>Explora sólo los puertos especificados.</td></tr><tr><td><code>-sS</code></td><td>Realiza un escaneo SYN en puertos específicos.</td></tr><tr><td><code>-sA</code></td><td>Realiza un escaneo ACK en puertos específicos.</td></tr><tr><td><code>-Pn</code></td><td>Deshabilita las solicitudes de eco ICMP.</td></tr><tr><td><code>-n</code></td><td>Desactiva la resolución DNS.</td></tr><tr><td><code>--disable-arp-ping</code></td><td>Deshabilita el ping ARP.</td></tr><tr><td><code>--packet-trace</code></td><td>Muestra todos los paquetes enviados y recibidos.</td></tr></tbody></table>

Presta atención a los paquetes RCVD y su bandera establecida que recibimos de nuestro objetivo. Con el escaneo SYN (`-sS`) nuestro objetivo intenta establecer la conexión TCP enviando un paquete de regreso con los indicadores  SYN-ACK (`SA`) configurados y con el escaneo ACK (`-sA`) obtenemos el indicador `RST` porque el puerto TCP 22 está abierto. Para el puerto TCP 25, no recibimos ningún paquete, lo que indica que los paquetes se descartarán.

***

## <mark style="color:purple;">Detectar IDS/IPS</mark>

A diferencia de los firewalls y sus reglas, la detección de sistemas IDS/IPS es mucho más difícil porque son sistemas pasivos de monitoreo de tráfico. Los sistemas `IDS` examinan todas las conexiones entre los hosts. Si el IDS encuentra paquetes que contienen los contenidos o especificaciones definidos, se notifica al administrador y, en el peor de los casos, toma las medidas adecuadas.

Los sistemas `IPS` toman medidas configuradas por el administrador de forma independiente para prevenir posibles ataques de forma automática. Es fundamental saber que IDS e IPS son aplicaciones diferentes y que IPS sirve como complemento de IDS.

Se recomiendan varios servidores privados virtuales (`VPS`) con diferentes direcciones IP para determinar si dichos sistemas están en la red de destino durante una prueba de penetración. Si el administrador detecta un ataque potencial de este tipo en la red objetivo, el primer paso es bloquear la dirección IP de donde proviene el ataque potencial. Como resultado, ya no podremos acceder a la red usando esa dirección IP y nuestro proveedor de servicios de Internet (`ISP`) será contactado y bloqueado de todo acceso a Internet.

* Los sistemas `IDS` por sí solos suelen estar ahí para ayudar a los administradores a detectar posibles ataques en su red. Luego pueden decidir cómo manejar dichas conexiones. Podemos activar ciertas medidas de seguridad desde un administrador, por ejemplo, escaneando agresivamente un único puerto y su servicio. En función de si se toman medidas de seguridad específicas podemos detectar si la red tiene algunas aplicaciones de monitoreo o no.
* Un método para determinar si un `IPS` está presente en la red de destino es escanear desde un único host (`VPS`). Si en algún momento este host se bloquea y no tiene acceso a la red objetivo, sabemos que el administrador ha tomado algunas medidas de seguridad. En consecuencia, podemos continuar nuestra prueba de penetración con otro `VPS`.

En consecuencia, sabemos que debemos ser más silenciosos con nuestros escaneos y, en el mejor de los casos, disfrazar todas las interacciones con la red de destino y sus servicios.

***

## <mark style="color:purple;">Señuelos</mark>

Hay casos en los que, en principio, los administradores bloquean subredes específicas de diferentes regiones. Esto impide cualquier acceso a la red de destino. Otro ejemplo es cuando IPS debería bloquearnos. Por esta razón, el método de escaneo Decoy (`-D`) es la elección correcta.&#x20;

Con este método, Nmap genera varias direcciones IP aleatorias insertadas en el encabezado IP para ocultar el origen del paquete enviado. Con este método, podemos generar aleatoriamente (`RND`) un número específico (por ejemplo: `5`) de direcciones IP separadas por dos puntos (`:`). Luego, nuestra dirección IP real se coloca aleatoriamente entre las direcciones IP generadas.&#x20;

Por tanto, en el siguiente ejemplo, nuestra dirección IP real se sitúa en la segunda posición. Otro punto crítico es que los señuelos deben estar vivos. De lo contrario, es posible que no se pueda acceder al servicio en el destino debido a los mecanismos de seguridad de inundación SYN.

### **Escanear usando señuelos**

```bash
sudo nmap 10.129.2.28 -p 80 -sS -Pn -n --disable-arp-ping --packet-trace -D RND:5

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-21 16:14 CEST
SENT (0.0378s) TCP 102.52.161.59:59289 > 10.129.2.28:80 S ttl=42 id=29822 iplen=44  seq=3687542010 win=1024 <mss 1460>
SENT (0.0378s) TCP 10.10.14.2:59289 > 10.129.2.28:80 S ttl=59 id=29822 iplen=44  seq=3687542010 win=1024 <mss 1460>
SENT (0.0379s) TCP 210.120.38.29:59289 > 10.129.2.28:80 S ttl=37 id=29822 iplen=44  seq=3687542010 win=1024 <mss 1460>
SENT (0.0379s) TCP 191.6.64.171:59289 > 10.129.2.28:80 S ttl=38 id=29822 iplen=44  seq=3687542010 win=1024 <mss 1460>
SENT (0.0379s) TCP 184.178.194.209:59289 > 10.129.2.28:80 S ttl=39 id=29822 iplen=44  seq=3687542010 win=1024 <mss 1460>
SENT (0.0379s) TCP 43.21.121.33:59289 > 10.129.2.28:80 S ttl=55 id=29822 iplen=44  seq=3687542010 win=1024 <mss 1460>
RCVD (0.1370s) TCP 10.129.2.28:80 > 10.10.14.2:59289 SA ttl=64 id=0 iplen=44  seq=4056111701 win=64240 <mss 1460>
Nmap scan report for 10.129.2.28
Host is up (0.099s latency).

PORT   STATE SERVICE
80/tcp open  http
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 0.15 seconds
```

<table data-header-hidden><thead><tr><th width="233"></th><th></th></tr></thead><tbody><tr><td><strong>Opciones de escaneo</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>10.129.2.28</code></td><td>Escanea el objetivo especificado.</td></tr><tr><td><code>-p 80</code></td><td>Explora sólo los puertos especificados.</td></tr><tr><td><code>-sS</code></td><td>Realiza un escaneo SYN en puertos específicos.</td></tr><tr><td><code>-Pn</code></td><td>Deshabilita las solicitudes de eco ICMP.</td></tr><tr><td><code>-n</code></td><td>Desactiva la resolución DNS.</td></tr><tr><td><code>--disable-arp-ping</code></td><td>Deshabilita el ping ARP.</td></tr><tr><td><code>--packet-trace</code></td><td>Muestra todos los paquetes enviados y recibidos.</td></tr><tr><td><code>-D RND:5</code></td><td>Genera cinco direcciones IP aleatorias que indican la IP de origen de la que proviene la conexión.</td></tr></tbody></table>

Los ISP y los enrutadores suelen filtrar los paquetes falsificados, aunque provengan del mismo rango de red. Por lo tanto, también podemos especificar las direcciones IP de nuestros servidores VPS y usarlas en combinación con "`IP ID`" manipulación en los encabezados IP para escanear el objetivo.

Otro escenario sería que sólo las subredes individuales no tuvieran acceso a los servicios específicos del servidor. Entonces también podemos especificar manualmente la dirección IP de origen ( `-S`) para probar si obtenemos mejores resultados con esta. Los señuelos se pueden utilizar para escaneos SYN, ACK, ICMP y escaneos de detección de sistema operativo. Entonces, veamos un ejemplo de este tipo y determinemos qué sistema operativo es más probable que sea.

### **Prueba de regla de firewall**

```bash
sudo nmap 10.129.2.28 -n -Pn -p445 -O

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-22 01:23 CEST
Nmap scan report for 10.129.2.28
Host is up (0.032s latency).

PORT    STATE    SERVICE
445/tcp filtered microsoft-ds
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)
Too many fingerprints match this host to give specific OS details
Network Distance: 1 hop

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 3.14 seconds
```

### **Escanear utilizando una IP de origen diferente**

```bash
sudo nmap 10.129.2.28 -n -Pn -p 445 -O -S 10.129.2.200 -e tun0

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-22 01:16 CEST
Nmap scan report for 10.129.2.28
Host is up (0.010s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 2.6.32 (96%), Linux 3.2 - 4.9 (96%), Linux 2.6.32 - 3.10 (96%), Linux 3.4 - 3.10 (95%), Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), Synology DiskStation Manager 5.2-5644 (94%), Linux 2.6.32 - 2.6.35 (94%), Linux 2.6.32 - 3.5 (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 4.11 seconds
```

<table data-header-hidden><thead><tr><th width="199"></th><th></th></tr></thead><tbody><tr><td><strong>Opciones de escaneo</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>10.129.2.28</code></td><td>Escanea el objetivo especificado.</td></tr><tr><td><code>-n</code></td><td>Desactiva la resolución DNS.</td></tr><tr><td><code>-Pn</code></td><td>Deshabilita las solicitudes de eco ICMP.</td></tr><tr><td><code>-p 445</code></td><td>Explora sólo los puertos especificados.</td></tr><tr><td><code>-O</code></td><td>Realiza un análisis de detección del sistema operativo.</td></tr><tr><td><code>-S</code></td><td>Escanea el objetivo utilizando una dirección IP de origen diferente.</td></tr><tr><td><code>10.129.2.200</code></td><td>Especifica la dirección IP de origen.</td></tr><tr><td><code>-e tun0</code></td><td>Envía todas las solicitudes a través de la interfaz especificada.</td></tr></tbody></table>

***

## <mark style="color:purple;">Proxy DNS</mark>

Por defecto, `Nmap` realiza una resolución DNS inversa a menos que se especifique lo contrario para encontrar información más importante sobre nuestro objetivo. Estas consultas de DNS también se pasan en la mayoría de los casos porque se supone que el servidor web determinado debe encontrarse y visitarse. Las consultas de DNS se realizan a través del archivo `UDP port 53`. Hasta ahora sólo se utilizaba el `TCP port 53` para el llamado "`Zone transfers`" entre servidores DNS o para transferencias de datos de más de 512 bytes. Esto está cambiando cada vez más debido a las expansiones de IPv6 y DNSSEC. Estos cambios hacen que muchas solicitudes de DNS se realicen a través del puerto TCP 53.

Sin embargo, `Nmap` todavía nos brinda una manera de especificar los servidores DNS nosotros mismos ( `--dns-server <ns>,<ns>`). Este método podría ser fundamental para nosotros si estamos en una zona desmilitarizada ( `DMZ`). Los servidores DNS de la empresa suelen ser más confiables que los de Internet. Así, por ejemplo, podríamos utilizarlos para interactuar con los hosts de la red interna. Como otro ejemplo, podemos utilizar `TCP port 53`como puerto de origen ( `--source-port`) para nuestros escaneos. Si el administrador usa el firewall para controlar este puerto y no filtra IDS/IPS correctamente, nuestros paquetes TCP serán confiables y se transmitirán.

### **SYN-Scan de un puerto filtrado**

```bash
sudo nmap 10.129.2.28 -p50000 -sS -Pn -n --disable-arp-ping --packet-trace

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-21 22:50 CEST
SENT (0.0417s) TCP 10.10.14.2:33436 > 10.129.2.28:50000 S ttl=41 id=21939 iplen=44  seq=736533153 win=1024 <mss 1460>
SENT (1.0481s) TCP 10.10.14.2:33437 > 10.129.2.28:50000 S ttl=46 id=6446 iplen=44  seq=736598688 win=1024 <mss 1460>
Nmap scan report for 10.129.2.28
Host is up.

PORT      STATE    SERVICE
50000/tcp filtered ibm-db2

Nmap done: 1 IP address (1 host up) scanned in 2.06 seconds
```

### **SYN-Scan desde el puerto DNS**

```bash
sudo nmap 10.129.2.28 -p50000 -sS -Pn -n --disable-arp-ping --packet-trace --source-port 53

SENT (0.0482s) TCP 10.10.14.2:53 > 10.129.2.28:50000 S ttl=58 id=27470 iplen=44  seq=4003923435 win=1024 <mss 1460>
RCVD (0.0608s) TCP 10.129.2.28:50000 > 10.10.14.2:53 SA ttl=64 id=0 iplen=44  seq=540635485 win=64240 <mss 1460>
Nmap scan report for 10.129.2.28
Host is up (0.013s latency).

PORT      STATE SERVICE
50000/tcp open  ibm-db2
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 0.08 seconds
```

<table data-header-hidden><thead><tr><th width="231"></th><th></th></tr></thead><tbody><tr><td><strong>Opciones de escaneo</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>10.129.2.28</code></td><td>Escanea el objetivo especificado.</td></tr><tr><td><code>-p 50000</code></td><td>Explora sólo los puertos especificados.</td></tr><tr><td><code>-sS</code></td><td>Realiza un escaneo SYN en puertos específicos.</td></tr><tr><td><code>-Pn</code></td><td>Deshabilita las solicitudes de eco ICMP.</td></tr><tr><td><code>-n</code></td><td>Desactiva la resolución DNS.</td></tr><tr><td><code>--disable-arp-ping</code></td><td>Deshabilita el ping ARP.</td></tr><tr><td><code>--packet-trace</code></td><td>Muestra todos los paquetes enviados y recibidos.</td></tr><tr><td><code>--source-port 53</code></td><td>Realiza los análisis desde el puerto de origen especificado.</td></tr></tbody></table>

Ahora que hemos descubierto que el firewall acepta el puerto `TCP 53`, es muy probable que los filtros IDS/IPS también estén configurados de manera mucho más débil que otros. Podemos probar esto intentando conectarnos a este puerto usando `Netcat`.

### **Conectarse al puerto filtrado**

```bash
ncat -nv --source-port 53 10.129.2.28 50000

Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Connected to 10.129.2.28:50000.
220 ProFTPd
```

***

## <mark style="color:purple;">Labs de Evasión de IDS</mark> <a href="#c12a" id="c12a"></a>

### <mark style="color:purple;">Easy Lab</mark> <a href="#c12a" id="c12a"></a>

Nuestro cliente quiere saber si podemos identificar en qué <mark style="color:purple;">sistema operativo</mark> se está ejecutando la máquina proporcionada. El sistema tiene un IDS activo.

Podemos usar varias técnicas cómo:

```bash
curl -I 10.129.92.110
                                              
HTTP/1.1 200 OK
Date: Tue, 10 Dec 2024 14:19:11 GMT
Server: Apache/2.4.29 (Ubuntu)  # Sistema operativo localizado
Last-Modified: Thu, 10 Sep 2020 02:14:12 GMT
ETag: "2c39-5aeec1fc9d59d"
Accept-Ranges: bytes
Content-Length: 11321
Vary: Accept-Encoding
Content-Type: text/html
```

```bash
whatweb -v http://10.129.96.19       
       
WhatWeb report for http://10.129.96.19
Status    : 200 OK
Title     : Apache2 Ubuntu Default Page: It works
IP        : 10.129.96.19
Country   : RESERVED, ZZ

Summary   : Apache[2.4.29], HTTPServer[Ubuntu Linux][Apache/2.4.29 (Ubuntu)]

[ HTTPServer ]
	HTTP server header string. This plugin also attempts to 
	identify the operating system from the server header. 

	OS           : Ubuntu Linux  # Sistema operativo localizado
	String       : Apache/2.4.29 (Ubuntu) (from server string)
```

```bash
sudo nmap --script smb-os-discovery 10.129.2.80

Starting Nmap 7.94 ( <https://nmap.org> ) at 2023-06-25 14:14 +03
Nmap scan report for 10.129.2.80
Host is up (0.31s latency).
Not shown: 993 closed tcp ports (reset)
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
110/tcp   open  pop3
139/tcp   open  netbios-ssn
143/tcp   open  imap
445/tcp   open  microsoft-ds
10001/tcp open  scp-config
Host script results:
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu) # Sistema operativo localizado
|   Computer name: nix-nmap-easy
|   NetBIOS computer name: NIX-NMAP-EASY\\x00
|   Domain name: \\x00
|   FQDN: nix-nmap-easy
|_  System time: 2023-06-25T13:16:13+02:00
Nmap done: 1 IP address (1 host up) scanned in 4.15 seconds
```

***

### <mark style="color:purple;">Medium Lab</mark> <a href="#c12a" id="c12a"></a>

Después de realizar la primera prueba y enviar nuestros resultados a nuestro cliente, los administradores realizaron algunos cambios y mejoras en el firewall `IDS/IPS`. Pudimos escuchar que los administradores no estaban satisfechos con sus configuraciones anteriores durante la reunión y pudieron ver que el tráfico de la red se podía filtrar de manera más estricta.

Después de que las configuraciones se transfieren al sistema, nuestro cliente quiere saber si es posible averiguar la versión del <mark style="color:purple;">servidor DNS</mark> de nuestro objetivo.

```bash
sudo nmap -sSU -p 53 -sA -f --script dns-nsid 10.129.75.161

Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-02-02 14:04 CET
Nmap scan report for 10.129.75.161
Host is up (0.057s latency).

PORT   STATE    SERVICE
53/tcp filtered domain
53/udp open     domain
| dns-nsid: 
|_  bind.version: HTB{GoTtgUnyze9Psw4vGjcuMpHRp}

Nmap done: 1 IP address (1 host up) scanned in 14.09 seconds
```

***

### <mark style="color:purple;">Hard Lab</mark> <a href="#c12a" id="c12a"></a>

Con la ayuda de nuestra segunda prueba, nuestro cliente pudo obtener nuevos conocimientos y envió a uno de sus administradores a un curso de sistemas `IDS/IPS`. Ahora el administrador ha tomado todas las precauciones necesarias y quiere que volvamos a probar esto porque se deben cambiar servicios específicos y se tuvo que modificar la comunicación para el software proporcionado.

Ahora nuestro cliente quiere saber si es posible averiguar la versión de los servicios en ejecución. Identifique la versión del servicio de la que hablaba nuestro cliente y envíe la flag como respuesta.

```bash
sudo nc -nv -p 53 10.129.69.215 50000 

(UNKNOWN) [10.129.69.215] 50000 (?) open
220 HTB{kjnsdf2n982n1827eh76238s98di1w6}
```

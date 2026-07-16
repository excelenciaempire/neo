
# ICMP Tunneling con SOCKS

El túnel ICMP encapsula su tráfico dentro de `ICMP packets`archivos que contienen `echo requests`y `responses`. El túnel ICMP solo funcionaría cuando se permitan respuestas de ping dentro de una red con firewall. Cuando a un host dentro de una red con firewall se le permite hacer ping a un servidor externo, puede encapsular su tráfico dentro de la solicitud de eco de ping y enviarlo a un servidor externo. El servidor externo puede validar este tráfico y enviar una respuesta adecuada, lo cual es extremadamente útil para la filtración de datos y la creación de túneles dinámicos hacia un servidor externo.

Usaremos la herramienta [ptunnel-ng](https://github.com/utoni/ptunnel-ng) para crear un túnel entre nuestro servidor Ubuntu y nuestro host de ataque. Una vez que se crea un túnel, podremos enviar nuestro tráfico a través del archivo `ptunnel-ng client`. Podemos iniciar el `ptunnel-ng server`host dinámico de destino. Comencemos configurando ptunnel-ng.

***

### Configuración y uso de ptunnel-ng

Si ptunnel-ng no está en nuestro host de ataque, podemos clonar el proyecto usando git.

**Clonación de Ptunnel-ng**

&#x20; Túnel ICMP con SOCKS

```shell-session
afsh4ck@kali$ git clone https://github.com/utoni/ptunnel-ng.git
```

Una vez que el repositorio de ptunnel-ng se clona en nuestro host de ataque, podemos ejecutar el `autogen.sh`script ubicado en la raíz del directorio de ptunnel-ng.

**Construyendo Ptunnel-ng con Autogen.sh**

```shell-session
afsh4ck@kali$ sudo ./autogen.sh 
```

Después de ejecutar autogen.sh, ptunnel-ng se puede utilizar desde el lado del cliente y del servidor. Ahora necesitaremos transferir el repositorio desde nuestro host de ataque al host de destino. Como en apartados anteriores, podemos utilizar SCP para transferir los archivos.&#x20;

{% hint style="warning" %}
Si queremos transferir todo el repositorio y los archivos que contiene, necesitaremos usar la opción `-r` con SCP.
{% endhint %}

### **Transferencia de Ptunnel-ng al host Pivot**

```shell-session
afsh4ck@kali$ scp -r ptunnel-ng ubuntu@10.129.202.64:~/
```

Con ptunnel-ng en el host de destino, podemos iniciar el lado del servidor del túnel ICMP usando el comando directamente debajo.

### **Iniciar el servidor ptunnel-ng en el host de destino**

```shell-session
ubuntu@WEB01:~/ptunnel-ng/src$ sudo ./ptunnel-ng -r10.129.202.64 -R22

[sudo] password for ubuntu: 
./ptunnel-ng: /lib/x86_64-linux-gnu/libselinux.so.1: no version information available (required by ./ptunnel-ng)
[inf]: Starting ptunnel-ng 1.42.
[inf]: (c) 2004-2011 Daniel Stoedle, <daniels@cs.uit.no>
[inf]: (c) 2017-2019 Toni Uhlig,     <matzeton@googlemail.com>
[inf]: Security features by Sebastien Raveau, <sebastien.raveau@epita.fr>
[inf]: Forwarding incoming ping packets over TCP.
[inf]: Ping proxy is listening in privileged mode.
[inf]: Dropping privileges now.
```

La siguiente dirección IP `-r` debe ser la IP en la que queremos que ptunnel-ng acepte conexiones. En este caso, cualquier IP a la que podamos acceder desde nuestro host de ataque sería la que usaríamos. Nos beneficiaríamos si usáramos este mismo pensamiento y consideración durante un compromiso real.

De vuelta en el host de ataque, podemos intentar conectarnos al servidor ptunnel-ng ( `-p <ipAddressofTarget>`), pero asegurarnos de que esto suceda a través del puerto local 2222 ( `-l2222`). Conectarnos a través del puerto local 2222 nos permite enviar tráfico a través del túnel ICMP.

### **Conexión al servidor ptunnel-ng desde el host de ataque**

```shell-session
afsh4ck@kali$ sudo ./ptunnel-ng -p10.129.202.64 -l2222 -r10.129.202.64 -R22

[inf]: Starting ptunnel-ng 1.42.
[inf]: (c) 2004-2011 Daniel Stoedle, <daniels@cs.uit.no>
[inf]: (c) 2017-2019 Toni Uhlig,     <matzeton@googlemail.com>
[inf]: Security features by Sebastien Raveau, <sebastien.raveau@epita.fr>
[inf]: Relaying packets from incoming TCP streams.
```

Con el túnel ICMP ptunnel-ng establecido exitosamente, podemos intentar conectarnos al objetivo usando SSH a través del puerto local 2222 ( `-p2222`).

### **Túnel de conexión SSH a través de un túnel ICMP**

```shell-session
afsh4ck@kali$ ssh -p2222 -lubuntu 127.0.0.1

ubuntu@127.0.0.1's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed 11 May 2022 03:10:15 PM UTC

  System load:             0.0
  Usage of /:              39.6% of 13.72GB
  Memory usage:            37%
  Swap usage:              0%
  Processes:               183
  Users logged in:         1
  IPv4 address for ens192: 10.129.202.64
  IPv6 address for ens192: dead:beef::250:56ff:feb9:52eb
  IPv4 address for ens224: 172.16.5.129

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

144 updates can be applied immediately.
97 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable


Last login: Wed May 11 14:53:22 2022 from 10.10.14.18
ubuntu@WEB01:~$ 
```

Si se configura correctamente, podremos ingresar credenciales y tener una sesión SSH a través del túnel ICMP.

En el lado del cliente y del servidor de la conexión, notaremos que ptunnel-ng nos brinda registros de sesión y estadísticas de tráfico asociadas con el tráfico que pasa a través del túnel ICMP. Esta es una forma en que podemos confirmar que nuestro tráfico pasa del cliente al servidor utilizando ICMP.

#### **Visualización de estadísticas de tráfico de túneles**

```shell-session
inf]: Incoming tunnel request from 10.10.14.18.
[inf]: Starting new session to 10.129.202.64:22 with ID 20199
[inf]: Received session close from remote peer.
[inf]: 
Session statistics:
[inf]: I/O:   0.00/  0.00 mb ICMP I/O/R:      248/      22/       0 Loss:  0.0%
[inf]: 
```

También podemos usar este túnel y SSH para realizar un reenvío de puertos dinámico que nos permita usar cadenas proxy de varias maneras.

### **Habilitar Port Forwarding a través de SSH**

```shell-session
afsh4ck@kali$ ssh -D 9050 -p2222 -lubuntu 127.0.0.1

ubuntu@127.0.0.1's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)
<snip>
```

Podríamos usar Proxychains con Nmap para escanear objetivos en la red interna (`172.16.5.x`). Según nuestros descubrimientos, podemos intentar conectarnos con el objetivo.

### **Proxychains a través del túnel ICMP**

```shell-session
afsh4ck@kali$ proxychains nmap -sV -sT 172.16.5.19 -p3389

ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.92 ( https://nmap.org ) at 2022-05-11 11:10 EDT
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:80-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK
Nmap scan report for 172.16.5.19
Host is up (0.12s latency).

PORT     STATE SERVICE       VERSION
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.78 seconds
```

***

## <mark style="color:purple;">Consideraciones sobre el análisis del tráfico de red</mark>

Es importante que confirmemos que las herramientas que estamos utilizando funcionan según lo anunciado y que las hemos configurado y estamos operando correctamente. En el caso de tunelizar el tráfico a través de diferentes protocolos que se enseñan en esta sección con tunelización ICMP, podemos beneficiarnos de analizar el tráfico que generamos con un analizador de paquetes como `Wireshark`. Mire de cerca el breve clip a continuación.

![](https://academy.hackthebox.com/storage/modules/158/analyzingTheTraffic.gif)

En la primera parte de este clip, se establece una conexión a través de SSH sin utilizar un túnel ICMP. Podemos notar que se captura tráfico `TCP` y `SSHv2`

El comando utilizado en el clip: `ssh ubuntu@10.129.202.64`

En la segunda parte de este clip, se establece una conexión a través de SSH mediante un túnel ICMP. Observe el tipo de tráfico que se captura cuando se realiza esto.

Comando utilizado en el clip: `ssh -p2222 -lubuntu 127.0.0.1`

***

## <mark style="color:purple;">Caso práctico</mark>

Utilizando los conceptos aprendidos hasta ahora, conéctate al objetivo y establece un túnel ICMP. Vaya al DC (`172.16.5.19`, `victor:pass@123`) y envía el contenido de `C:\Users\victor\Downloads\flag.txt` como respuesta.

### Paso 1: Envio de ptunnel-ng al host

```shell-session
afsh4ck@kali$ scp -r ptunnel-ng ubuntu@10.129.147.39:~/
```

### Paso 2: Conexión al host de pivoting por SSH

#### Ver interfaces de red en el host

```shell-session
ubuntu@WEB01:~$ ifconfig
ens192: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.129.202.64  netmask 255.255.0.0  broadcast 10.129.255.255
        inet6 dead:beef::250:56ff:fe94:6836  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::250:56ff:fe94:6836  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:94:68:36  txqueuelen 1000  (Ethernet)
        RX packets 11435  bytes 1079867 (1.0 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 3690  bytes 337823 (337.8 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

ens224: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.16.5.129  netmask 255.255.254.0  broadcast 172.16.5.255
        inet6 fe80::250:56ff:fe94:68b7  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:94:68:b7  txqueuelen 1000  (Ethernet)
        RX packets 519  bytes 38319 (38.3 KB)
        RX errors 0  dropped 14  overruns 0  frame 0
        TX packets 545  bytes 37213 (37.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 4102  bytes 333820 (333.8 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 4102  bytes 333820 (333.8 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Vemos que hay una red interna: `172.16.5.129`

### Paso 3: Verificar la conectividad entre el host de pivoting y el DC

En el host de pivoting (`10.129.147.39`), verifica si puedes acceder al puerto 3389 del DC (`172.16.5.19`) utilizando `telnet` o `nc`:

```sh
telnet 172.16.5.19 3389
```

```sh
nc -zv 172.16.5.19 3389
```

Si no hay respuesta, puede haber un problema de firewall o políticas de red bloqueando el acceso.

### Paso 4: Abrir el túnel desde el host de Pivoting hacia el DC

Nos aseguramos de estar utilizando la dirección correcta del DC. La configuración debe redirigir el tráfico hacia el DC (`172.16.5.19`).

```shell-session
ubuntu@WEB01:~$ ls
ptunnel-ng

ubuntu@WEB01:~$ sudo ./ptunnel-ng -r172.16.5.19 -R3389
./ptunnel-ng: /lib/x86_64-linux-gnu/libselinux.so.1: no version information available (required by ./ptunnel-ng)
[inf]: Starting ptunnel-ng 1.42.
[inf]: (c) 2004-2011 Daniel Stoedle, <daniels@cs.uit.no>
[inf]: (c) 2017-2019 Toni Uhlig,     <matzeton@googlemail.com>
[inf]: Security features by Sebastien Raveau, <sebastien.raveau@epita.fr>
[inf]: Forwarding incoming ping packets over TCP.
[inf]: Ping proxy is listening in privileged mode.
[inf]: Dropping privileges now.
```

### Paso 5: Conexión desde el host de atacante

```shell-session
afsh4ck@kali$ sudo ./ptunnel-ng -p10.129.147.39 -l13389 -r172.16.5.19 -R3389
[inf]: Starting ptunnel-ng 1.42.
[inf]: (c) 2004-2011 Daniel Stoedle, <daniels@cs.uit.no>
[inf]: (c) 2017-2019 Toni Uhlig,     <matzeton@googlemail.com>
[inf]: Security features by Sebastien Raveau, <sebastien.raveau@epita.fr>
[inf]: Relaying packets from incoming TCP streams.
```

<figure><img src="/files/VkVoQVs6gIgTv5K3KdN8" alt=""><figcaption></figcaption></figure>

### Paso 6: Conexión al DC por RDP

En una nueva terminal, ejecutamos xfreerdp a través del tunel ICMP: `localhost:13389`

```
xfreerdp /v:localhost:13389 /u:victor /p:pass@123
```

<figure><img src="/files/6JyBL6NqmxDHp6poCBej" alt=""><figcaption></figcaption></figure>

Bummm! Obtenemos una conexión con el DC y podemos leer la flag sin problema 🏆

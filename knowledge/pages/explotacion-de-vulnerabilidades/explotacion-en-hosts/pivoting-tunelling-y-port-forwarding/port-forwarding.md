
# Port Forwarding

## <mark style="color:purple;">Port Forwarding Dinámico con SSH y SOCKS Tunneling</mark>

### Port Forwarding: Contexto

`Port forwarding` es una técnica que nos permite redirigir una solicitud de comunicación de un puerto a otro. El reenvío de puertos utiliza TCP como capa de comunicación principal para proporcionar comunicación interactiva para el puerto reenviado. Sin embargo, se pueden utilizar diferentes protocolos de capa de aplicación, como SSH o incluso [SOCKS](https://en.wikipedia.org/wiki/SOCKS) (capa que no es de aplicación), para encapsular el tráfico reenviado. Esto puede resultar eficaz para eludir los firewalls y utilizar los servicios existentes en su host comprometido para pasar a otras redes.

***

### Port Forwarding Local con SSH

Tomemos un ejemplo de la imagen de abajo.

![](https://academy.hackthebox.com/storage/modules/158/11.png)

Tenemos nuestro host de ataque (10.10.15.x) y un servidor Ubuntu de destino (10.129.xx), que hemos comprometido. Escanearemos el servidor Ubuntu de destino usando Nmap para buscar puertos abiertos.

### **Escaneando el objetivo de pivoting**

```shell-session
afsh4ck@kali$ nmap -sT -p22,3306 10.129.202.64

Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-24 12:12 EST
Nmap scan report for 10.129.202.64
Host is up (0.12s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
3306/tcp closed mysql

Nmap done: 1 IP address (1 host up) scanned in 0.68 seconds
```

La salida de Nmap muestra que el puerto SSH está abierto. Para acceder al servicio MySQL, podemos ingresar mediante SSH al servidor y acceder a MySQL desde el interior del servidor Ubuntu, o podemos reenviarlo a nuestro puerto localhost `1234`y acceder a él localmente. Una ventaja de acceder a él localmente es que si queremos ejecutar un exploit remoto en el servicio MySQL, no podremos hacerlo sin el reenvío de puertos. Esto se debe a que MySQL está alojado localmente en el servidor Ubuntu en el puerto `3306`. Entonces, usaremos el siguiente comando para reenviar nuestro puerto local (1234) a través de SSH al servidor Ubuntu.

### **Ejecución del Port Forwarding Local**

```shell-session
afsh4ck@kali$ ssh -L 1234:localhost:3306 ubuntu@10.129.202.64

ubuntu@10.129.202.64's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu 24 Feb 2022 05:23:20 PM UTC

  System load:             0.0
  Usage of /:              28.4% of 13.72GB
  Memory usage:            34%
  Swap usage:              0%
  Processes:               175
  Users logged in:         1
  IPv4 address for ens192: 10.129.202.64
  IPv6 address for ens192: dead:beef::250:56ff:feb9:52eb
  IPv4 address for ens224: 172.16.5.129

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

66 updates can be applied immediately.
45 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable
```

El comando  `-L` le dice al cliente SSH que solicite al servidor SSH que reenvíe todos los datos que enviamos a través del puerto `1234` al servidor Ubuntu `localhost:3306`. Al hacer esto, deberíamos poder acceder al servicio MySQL localmente en el puerto 1234. Podemos usar Netstat o Nmap para consultar nuestro host local en el puerto 1234 para verificar si el servicio MySQL fue reenviado.

### **Confirmación de reenvío de puerto con Netstat**

```shell-session
afsh4ck@kali$ netstat -antp | grep 1234

(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 127.0.0.1:1234          0.0.0.0:*               LISTEN      4034/ssh            
tcp6       0      0 ::1:1234                :::*                    LISTEN      4034/ssh     
```

### **Confirmación de reenvío de puerto con Nmap**

```shell-session
afsh4ck@kali$ nmap -v -sV -p1234 localhost

Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-24 12:18 EST
NSE: Loaded 45 scripts for scanning.
Initiating Ping Scan at 12:18
Scanning localhost (127.0.0.1) [2 ports]
Completed Ping Scan at 12:18, 0.01s elapsed (1 total hosts)
Initiating Connect Scan at 12:18
Scanning localhost (127.0.0.1) [1 port]
Discovered open port 1234/tcp on 127.0.0.1
Completed Connect Scan at 12:18, 0.01s elapsed (1 total ports)
Initiating Service scan at 12:18
Scanning 1 service on localhost (127.0.0.1)
Completed Service scan at 12:18, 0.12s elapsed (1 service on 1 host)
NSE: Script scanning 127.0.0.1.
Initiating NSE at 12:18
Completed NSE at 12:18, 0.01s elapsed
Initiating NSE at 12:18
Completed NSE at 12:18, 0.00s elapsed
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0080s latency).
Other addresses for localhost (not scanned): ::1

PORT     STATE SERVICE VERSION
1234/tcp open  mysql   MySQL 8.0.28-0ubuntu0.20.04.3

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.18 seconds
```

De manera similar, si queremos reenviar múltiples puertos desde el servidor Ubuntu a su host local, puede hacerlo incluyendo el `local port:server:port`argumento en su comando ssh. Por ejemplo, el siguiente comando reenvía el puerto 80 del servidor web Apache al puerto local de su host de ataque en `8080`.

### **Port Forwarding de múltiples puertos**

```shell-session
afsh4ck@kali$ ssh -L 1234:localhost:3306 -L 8080:localhost:80 ubuntu@10.129.202.64
```

***

## <mark style="color:purple;">Configuración para pivotar</mark>

Ahora, si escribe `ifconfig` en el host Ubuntu, encontrará que este servidor tiene varias NIC:

* Uno conectado a nuestro host de ataque (`ens192`)
* Uno comunicándose con otros hosts dentro de una red diferente (`ens224`)
* La interfaz Loopback (`lo`).

### **Buscando oportunidades para pivotar usando ifconfig**

```shell-session
ubuntu@WEB01:~$ ifconfig 

ens192: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.129.202.64  netmask 255.255.0.0  broadcast 10.129.255.255
        inet6 dead:beef::250:56ff:feb9:52eb  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::250:56ff:feb9:52eb  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b9:52:eb  txqueuelen 1000  (Ethernet)
        RX packets 35571  bytes 177919049 (177.9 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10452  bytes 1474767 (1.4 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

ens224: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.16.5.129  netmask 255.255.254.0  broadcast 172.16.5.255
        inet6 fe80::250:56ff:feb9:a9aa  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b9:a9:aa  txqueuelen 1000  (Ethernet)
        RX packets 8251  bytes 1125190 (1.1 MB)
        RX errors 0  dropped 40  overruns 0  frame 0
        TX packets 1538  bytes 123584 (123.5 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 270  bytes 22432 (22.4 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 270  bytes 22432 (22.4 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

A diferencia del escenario anterior donde sabíamos a qué puerto acceder, en nuestro escenario actual no sabemos qué servicios se encuentran al otro lado de la red. Por lo tanto, podemos escanear rangos más pequeños de IP en la red ( `172.16.5.1-200`) o en toda la subred ( `172.16.5.0/23`). No podemos realizar este análisis directamente desde nuestro host de ataque porque no tiene rutas a la red `172.16.5.0/23`. Para ello tendremos que realizar `dynamic port forwarding` para que nuestros paquetes de red `pivoten` a través del servidor Ubuntu. Podemos hacer esto iniciando un `SOCKS listener` en nuestro `local host`(host de ataque personal) y luego configurar SSH para reenviar ese tráfico a través de SSH a la red (`172.16.5.0/23`) después de conectarnos al host de destino.

Esto se llama `SSH tunneling` con `SOCKS proxy`. SOCKS significa `Socket Secure`, un protocolo que ayuda a comunicarse con servidores donde existen restricciones de firewall. A diferencia de la mayoría de los casos en los que iniciaría una conexión para conectarse a un servicio, en el caso de SOCKS, el tráfico inicial lo genera un cliente SOCKS, que se conecta al servidor SOCKS controlado por el usuario que desea acceder a un servicio en el cliente. -lado. Una vez establecida la conexión, el tráfico de la red se puede enrutar a través del servidor SOCKS en nombre del cliente conectado.

Esta técnica se utiliza a menudo para eludir las restricciones impuestas por los cortafuegos y permitir que una entidad externa eluda el cortafuegos y acceda a un servicio dentro del entorno del cortafuegos. Un beneficio más de utilizar el proxy SOCKS para pivotar y reenviar datos es que los proxies SOCKS pueden pivotar mediante la creación de una ruta a un servidor externo desde `Redes NAT`. Los proxies SOCKS son actualmente de dos tipos: `SOCKS4` y `SOCKS5`. SOCKS4 no proporciona autenticación ni soporte UDP, mientras que SOCKS5 sí lo proporciona. Tomemos un ejemplo de la imagen a continuación donde tenemos una red NAT de `172.16.5.0/23`, a la que no podemos acceder directamente.

![](https://academy.hackthebox.com/storage/modules/158/22.png)

En la imagen de arriba, el host del ataque inicia el cliente SSH y solicita al servidor SSH que le permita enviar algunos datos TCP a través del socket ssh. El servidor SSH responde con un reconocimiento y el cliente SSH comienza a escuchar `localhost:9050`. Cualquier información que envíe aquí se transmitirá a toda la red (172.16.5.0/23) a través de SSH. Podemos usar el siguiente comando para realizar este reenvío de puerto dinámico.

### **Habilitación del Port Forwarding dinámico con SSH**

```shell-session
afsh4ck@kali$ ssh -D 9050 ubuntu@10.129.202.64
```

El `-D`argumento solicita al servidor SSH que habilite el reenvío de puertos dinámico. Una vez que tengamos esto habilitado, necesitaremos una herramienta que pueda enrutar los paquetes de cualquier herramienta a través del puerto `9050`. Esto lo podemos hacer usando la herramienta `proxychains`, que es capaz de redirigir conexiones TCP a través de servidores proxy TOR, SOCKS y HTTP/HTTPS y también nos permite encadenar múltiples servidores proxy. Al utilizar cadenas de proxy, también podemos ocultar la dirección IP del host solicitante, ya que el host receptor solo verá la IP del host dinámico. Proxychains se utiliza a menudo para obligar a una aplicación con `tráfico TCP` a pasar por servidores proxy como `SOCKS4`/ `SOCKS5`, `TOR`o `HTTP`/ `HTTPS` .

Para informar a proxychains que debemos usar el puerto 9050, debemos modificar el archivo de configuración de proxychains ubicado en `/etc/proxychains.conf`. Podemos agregar `socks4 127.0.0.1 9050`a la última línea si aún no está allí.

**Comprobando /etc/proxychains.conf**

```shell-session
afsh4ck@hkali$ tail -4 /etc/proxychains.conf

# meanwile
# defaults set to "tor"
socks4 	127.0.0.1 9050
```

Ahora, cuando inicie Nmap con proxychains usando el siguiente comando, enrutará todos los paquetes de Nmap al puerto local 9050, donde nuestro cliente SSH está escuchando, lo que reenviará todos los paquetes a través de SSH a la red 172.16.5.0/23.

**Usando Nmap con Proxychains**

```shell-session
afsh4ck@kali$ proxychains nmap -v -sn 172.16.5.1-200

ProxyChains-3.1 (http://proxychains.sf.net)

Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-24 12:30 EST
Initiating Ping Scan at 12:30
Scanning 10 hosts [2 ports/host]
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.2:80-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.5:80-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.6:80-<--timeout
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0

<SNIP>
```

Esta parte de empaquetar todos los datos de Nmap usando cadenas proxy y reenviarlos a un servidor remoto se llama `SOCKS tunneling`. Una nota más importante para recordar aquí es que solo podemos realizar overproxychains `full TCP connect scan`. La razón de esto es que las cadenas proxy no pueden comprender paquetes parciales. Si envía paquetes parciales, como escaneos de media conexión, arrojará resultados incorrectos. También debemos asegurarnos de que somos conscientes del hecho de que `host-alive`es posible que las comprobaciones no funcionen en objetivos de Windows porque el firewall de Windows Defender bloquea las solicitudes ICMP (pings tradicionales) de forma predeterminada.

[Un escaneo de conexión TCP completo](https://nmap.org/book/scan-methods-connect-scan.html) sin ping en todo un rango de red llevará mucho tiempo. Entonces, para este módulo, nos centraremos principalmente en escanear hosts individuales o rangos más pequeños de hosts que sabemos que están activos, que en este caso será un host de Windows en `172.16.5.19`.

Realizaremos un escaneo remoto del sistema usando el siguiente comando.

**Enumeración del destino de Windows a través de Proxychains**

```shell-session
afsh4ck@kali$ proxychains nmap -v -Pn -sT 172.16.5.19

ProxyChains-3.1 (http://proxychains.sf.net)
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times may be slower.
Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-24 12:33 EST
Initiating Parallel DNS resolution of 1 host. at 12:33
Completed Parallel DNS resolution of 1 host. at 12:33, 0.15s elapsed
Initiating Connect Scan at 12:33
Scanning 172.16.5.19 [1000 ports]
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:1720-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:587-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:445-<><>-OK
Discovered open port 445/tcp on 172.16.5.19
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:8080-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:23-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:135-<><>-OK
Discovered open port 135/tcp on 172.16.5.19
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:110-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:21-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:554-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-1172.16.5.19:25-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:5900-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:1025-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:143-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:199-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:993-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:995-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK
Discovered open port 3389/tcp on 172.16.5.19
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:443-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:80-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:113-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:8888-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:139-<><>-OK
Discovered open port 139/tcp on 172.16.5.19
```

El escaneo de Nmap muestra varios puertos abiertos, uno de los cuales es `RDP port`(3389). De manera similar al escaneo de Nmap, también podemos pivotar `msfconsole`a través de cadenas proxy para realizar escaneos RDP vulnerables usando módulos auxiliares de Metasploit. Podemos iniciar msfconsole con proxychains.

***

## <mark style="color:purple;">Usando Metasploit con Proxychains</mark>

También podemos abrir Metasploit usando proxychains y enviar todo el tráfico asociado a través del proxy que hayamos establecido.

```````shell-session
afsh4ck@kali$ proxychains msfconsole

ProxyChains-3.1 (http://proxychains.sf.net)


                                  .::::::::::-.                     .::::::-
                                .hmMMMMMMMMMMNddds\...//M\\.../hddddmMMMMMMNo
                                 :Nm-/NMMMMMMMMMMMMM$$NMMMMm&&MMMMMMMMMMMMMMy
                                 .sm/`-yMMMMMMMMMMMM$$MMMMMN&&MMMMMMMMMMMMMh`
                                  -Nd`  :MMMMMMMMMMM$$MMMMMN&&MMMMMMMMMMMMh`
                                   -Nh` .yMMMMMMMMMM$$MMMMMN&&MMMMMMMMMMMm/
    `oo/``-hd:  ``                 .sNd  :MMMMMMMMMM$$MMMMMN&&MMMMMMMMMMm/
      .yNmMMh//+syysso-``````       -mh` :MMMMMMMMMM$$MMMMMN&&MMMMMMMMMMd
    .shMMMMN//dmNMMMMMMMMMMMMs`     `:```-o++++oooo+:/ooooo+:+o+++oooo++/
    `///omh//dMMMMMMMMMMMMMMMN/:::::/+ooso--/ydh//+s+/ossssso:--syN///os:
          /MMMMMMMMMMMMMMMMMMd.     `/++-.-yy/...osydh/-+oo:-`o//...oyodh+
          -hMMmssddd+:dMMmNMMh.     `.-=mmk.//^^^\\.^^`:++:^^o://^^^\\`::
          .sMMmo.    -dMd--:mN/`           ||--X--||          ||--X--||
........../yddy/:...+hmo-...hdd:............\\=v=//............\\=v=//.........
================================================================================
=====================+--------------------------------+=========================
=====================| Session one died of dysentery. |=========================
=====================+--------------------------------+=========================
================================================================================

                     Press ENTER to size up the situation

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Date: April 25, 1848 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%% Weather: It's always cool in the lab %%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%% Health: Overweight %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%% Caffeine: 12975 mg %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%% Hacked: All the things %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

                        Press SPACE BAR to continue



       =[ metasploit v6.1.27-dev                          ]
+ -- --=[ 2196 exploits - 1162 auxiliary - 400 post       ]
+ -- --=[ 596 payloads - 45 encoders - 10 nops            ]
+ -- --=[ 9 evasion                                       ]

Metasploit tip: Adapter names can be used for IP params 
set LHOST eth0

msf6 > 
```````

Usemos el módulo auxiliar `rdp_scanner` para verificar si el host en la red interna está escuchando en 3389.

### **Usando el módulo rdp\_scanner**

```bash
msf6 > search rdp_scanner

Matching Modules
================

   #  Name                               Disclosure Date  Rank    Check  Description
   -  ----                               ---------------  ----    -----  -----------
   0  auxiliary/scanner/rdp/rdp_scanner                   normal  No     Identify endpoints speaking the Remote Desktop Protocol (RDP)


Interact with a module by name or index. For example info 0, use 0 or use auxiliary/scanner/rdp/rdp_scanner

msf6 > use 0
msf6 auxiliary(scanner/rdp/rdp_scanner) > set rhosts 172.16.5.19
rhosts => 172.16.5.19
msf6 auxiliary(scanner/rdp/rdp_scanner) > run
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK

[*] 172.16.5.19:3389      - Detected RDP on 172.16.5.19:3389      (name:DC01) (domain:DC01) (domain_fqdn:DC01) (server_fqdn:DC01) (os_version:10.0.17763) (Requires NLA: No)
[*] 172.16.5.19:3389      - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

En la parte inferior del resultado anterior, podemos ver el puerto RDP abierto con la versión del sistema operativo Windows.

Dependiendo del nivel de acceso que tengamos a este host durante una evaluación, podemos intentar ejecutar un exploit o iniciar sesión con las credenciales recopiladas. Para este módulo, iniciaremos sesión en el host remoto de Windows a través del túnel SOCKS. Esto se puede hacer usando `xfreerdp`. El usuario en nuestro caso es `victor,`y la contraseña es `pass@123`

### **Usando xfreerdp con Proxychains**

```shell-session
afsh4ck@kali$ proxychains xfreerdp /v:172.16.5.19 /u:victor /p:pass@123

ProxyChains-3.1 (http://proxychains.sf.net)
[13:02:42:481] [4829:4830] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state
[13:02:42:482] [4829:4830] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpdr
[13:02:42:482] [4829:4830] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpsnd
[13:02:42:482] [4829:4830] [INFO][com.freerdp.client.common.cmdline] - loading channelEx cliprdr
```

El comando xfreerdp requerirá que se acepte un certificado RDP antes de establecer exitosamente la sesión. Tras aceptarlo, deberíamos tener una sesión RDP, pivotando a través del servidor Ubuntu.

**Pivoting RDP exitoso**

![Pivote RDP](https://academy.hackthebox.com/storage/modules/158/proxychaining.png)

<br>

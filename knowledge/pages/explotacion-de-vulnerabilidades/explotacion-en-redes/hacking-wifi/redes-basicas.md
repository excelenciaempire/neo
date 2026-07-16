
# Redes Básicas

## <mark style="color:purple;">Cambio de MAC</mark>

La dirección MAC es un identificador único que cada fabricante le asigna a la tarjeta de red de sus dispositivos conectados, desde un ordenador o móvil hasta routers, impresoras u otros dispositivos.

Un cambio de MAC sirve para evadir por ejemplo un blacklist.

{% embed url="<https://dnschecker.org/mac-lookup.php>" %}

```sh
# Ver todas las interfaces de red
ifconfig
wlan0: flags=547<UP,BROADCAST,NOTRAILERS,ALLMULTI>  mtu 1500
        ether ae:ed:e9:df:1e:67  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 4188  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 47 overruns 0  carrier 0  collisions 0
        
sudo ifconfig wlan0 down # Eliminar interfaz de red
sudo ifconfig wlan0 up   # Levantar interfaz de red
```

`wlan0` es nuestra interfaz de red de la antena, conectada a Kali Linux.

Una buena práctica es cambiar el nombre de la red `wlan0` a `wlan0mon` para indicar visualmente que está en modo monitor. Para ello podemos hacer lo siguiente:

```bash
sudo ifconfig wlan0 name wlan0mon
```

### Cambiar la dirección MAC

```sh
# 1 - Apagar el adaptador wlan0
sudo ifconfig wlan0 down

# 2 - Cambiar MAC con macchanger
> macchanger -h
GNU MAC Changer
Usage: macchanger [options] device

  -h,  --help                   Print this help
  -V,  --version                Print version and exit
  -s,  --show                   Print the MAC address and exit
  -e,  --ending                 Don't change the vendor bytes
  -a,  --another                Set random vendor MAC of the same kind
  -A                            Set random vendor MAC of any kind
  -p,  --permanent              Reset to original, permanent hardware MAC
  -r,  --random                 Set fully random MAC
  -l,  --list[=keyword]         Print known vendors
  -b,  --bia                    Pretend to be a burned-in-address
  -m,  --mac=XX:XX:XX:XX:XX:XX
       --mac XX:XX:XX:XX:XX:XX  Set the MAC XX:XX:XX:XX:XX:XX

# Por defecto pondremos 00:A1:B2:C3:D4:E5
> macchanger -m 00:A1:B2:C3:D4:E5 wlan0
Current MAC:   34:7d:e4:40:18:27 (unknown)
Permanent MAC: 34:7d:e4:40:18:27 (unknown)
New MAC:       00:a1:b2:c3:d4:e5 (unknown)

# 3 - Levantar la interfaz de red wlan0
sudo ifconfig wlan0 up

# 4 - Comprobamos que ha cambiado la MAC
ifconfig
wlan0: flags=867<UP,BROADCAST,NOTRAILERS,RUNNING,PROMISC,ALLMULTI>  mtu 1500
        inet6 fe80::2a1:b2ff:fec3:d4e5  prefixlen 64  scopeid 0x20<link>
        ether 00:a1:b2:c3:d4:e5  txqueuelen 1000  (Ethernet)
             |-----------------|
        RX packets 38814  bytes 0 (0.0 B)
        RX errors 0  dropped 35282  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 28 overruns 0  carrier 0  collisions 0
```

## <mark style="color:purple;">Modo Managed vs Modo Monitor</mark>

El "`modo managed`" y el "`modo monitor`" son dos modos de operación de las tarjetas de red inalámbricas (Wi-Fi) que cumplen funciones diferentes:

### **Modo Managed**

* **`Descripción`:** Este es el modo de operación estándar para las tarjetas Wi-Fi. En este modo, la tarjeta se conecta a una red inalámbrica existente, ya sea una red doméstica, empresarial o pública.
* **`Función`:** La tarjeta en modo managed busca y se conecta a un punto de acceso (router) para acceder a la red. En este modo, la tarjeta puede enviar y recibir datos a través de la red Wi-Fi.

### **Modo Monitor**

* **`Descripción`:** En este modo, la tarjeta de red inalámbrica se configura para operar en modo de escucha pasiva. No se conecta a ninguna red específica.
* **`Función`:** El modo monitor se utiliza comúnmente para la captura de paquetes en redes Wi-Fi. Permite a una computadora monitorear todas las comunicaciones en el canal Wi-Fi sin asociarse a un punto de acceso específico. Es útil para tareas de análisis de red, pruebas de seguridad y depuración.

<pre class="language-bash"><code class="lang-bash"># 1 - Apagamos el adaptador wlan0
<strong>sudo ifconfig wlan0 down
</strong>
# 2 - Iniciamos airmon-ng
sudo airmon-ng start wlan0

PHY	Interface	Driver		Chipset
phy0	wlan0		rtl8821cu	Realtek Semiconductor Corp. 802.11ac NIC
		(monitor mode enabled)
		
# 3 - Comprobar el modo monitor
sudo airodump-ng wlan0

# 4 - Sniffing con wireshark
sudo wireshark -i wlan0 -k

# 5 - Detener modo monitor
sudo airmon-ng stop wlan0
</code></pre>

<figure><img src="/files/DwTvP5ApmAaUvi0MFL0p" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Identificar dispositivos en nuestra red</mark>

Podemos utilizar `arp-scan` y `arp-fingerprint` para identificar dispositivos conectados a nuestra red wifi:

```bash
sudo arp-scan -I eth0 --localnet

Interface: eth0, type: EN10MB, MAC: 00:0c:29:85:3f:5e, IPv4: 192.168.1.160
Starting arp-scan 1.10.0 with 256 hosts (https://github.com/royhills/arp-scan)
192.168.1.1	e4:66:ab:4c:31:ea	(Unknown)
192.168.1.133	8c:b0:e9:4b:1c:e9	(Unknown)
192.168.1.130	28:f0:76:4f:4e:3c	(Unknown)
192.168.1.129	28:f0:76:4f:4e:3c	(Unknown)
192.168.1.198	f4:d4:88:85:e8:74	(Unknown)
```

```bash
sudo arp-fingerprint -l eth0      

192.168.1.1	00010000000	UNKNOWN
192.168.1.133	00010000000	UNKNOWN
192.168.1.130	10110000000	UNKNOWN
192.168.1.129	00010000000	UNKNOWN
192.168.1.198	11110000000	Linux 2.0, MacOS 10.4, IPSO 3.2.1, Minix 3, Cisco VPN Concentrator 4.7, Catalyst 1900, BeOS, WIZnet W5100
192.168.1.202	No Response
```

## <mark style="color:purple;">Bettercap</mark>

Tiene un módulo específicamente para ataques WiFi

```bash
sudo airmon-ng start wlan0
sudo bettercap -iface eth0 -eval "set wifi.interface wlan0; wifi.recon on"
```

<table><thead><tr><th width="251">Comando</th><th>Descripción</th></tr></thead><tbody><tr><td><code>wifi.recon on</code></td><td>Inicia el descubrimiento de estaciones base y la captura de handshakes/PMKID</td></tr><tr><td><code>wifi.recon off</code></td><td>Detiene el descubrimiento de estaciones base</td></tr><tr><td><code>wifi.clear</code></td><td>Borra todas las estaciones base recopiladas por el módulo de descubrimiento WiFi</td></tr><tr><td><code>wifi.recon BSSID</code></td><td>Establece la dirección de la estación base para filtrar dispositivos</td></tr><tr><td><code>wifi.recon clear</code></td><td>Elimina el filtro de la dirección de la estación base</td></tr><tr><td><code>wifi.assoc BSSID</code></td><td>Envía una solicitud de asociación a la dirección BSSID seleccionada para recibir una clave RSN PMKID (usar all, * o ff:ff:ff:ff:ff:ff para iterar sobre todas las estaciones base)</td></tr><tr><td><code>wifi.deauth BSSID</code></td><td>Inicia un ataque de deautenticación. Si se proporciona la dirección BSSID de un punto de acceso, se deautenticará a todos los clientes; de lo contrario, solo al cliente seleccionado. (usar <code>all</code>, <code>*</code> o <code>ff:ff:ff:ff:ff:ff</code> para deautenticar todo)</td></tr><tr><td><code>wifi.probe BSSID ESSID</code></td><td>Envía una sonda de cliente falsa con la dirección BSSID de la estación dada, buscando el ESSID especificado</td></tr><tr><td><code>wifi.show</code></td><td>Muestra la lista actual de estaciones inalámbricas (clasificación predeterminada por RSSI)</td></tr><tr><td><code>wifi.show.wps BSSID</code></td><td>Muestra información de WPS sobre una estación dada (usar all, * o ff:ff:ff:ff:ff:ff para seleccionar todo)</td></tr><tr><td><code>wifi.recon.channel CHANNEL</code></td><td>Lista separada por comas de canales para realizar un salto</td></tr><tr><td><code>wifi.recon.channel clear</code></td><td>Habilita el salto de canal en todos los canales admitidos</td></tr><tr><td><code>wifi.ap</code></td><td>Inyecta balizas de administración falsas para crear un punto de acceso falso (requiere que se ejecute <code>wifi.recon</code>)</td></tr></tbody></table>

<figure><img src="/files/FQ9zCR8Gzj1YaZkV6YBO" alt=""><figcaption></figcaption></figure>

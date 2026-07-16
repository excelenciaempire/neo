
# Redes en Pivoting

## <mark style="color:purple;">La creación de redes detrás de Pivoting</mark>

Ser capaz de comprender el concepto de `pivoting` lo suficientemente bien como para tener éxito en un pentesting requiere una comprensión fundamental sólida de algunos conceptos clave de networking. Esta sección será un repaso rápido de los conceptos fundamentales de redes esenciales para comprender el pivoting.

## <mark style="color:purple;">Direcciones IP y NIC</mark>

Cada computadora que se comunica en una red necesita una dirección IP. Si no tiene uno, no está en una red. La dirección IP se asigna mediante software y normalmente se obtiene automáticamente de un servidor DHCP. También es común ver computadoras con direcciones IP asignadas estáticamente. La asignación de IP estática es común con:

* `Servidores`
* `Enrutadores`
* `Cambiar interfaces virtuales`
* `Impresoras`
* `Y cualquier dispositivo que proporcione servicios críticos a la red.`

Ya sea asignada `dynamically`o `statically`, la dirección IP se asigna a `Network Interface Controller`( `NIC`). Normalmente, la NIC se denomina `Network Interface Card`o `Network Adapter`. Una computadora puede tener múltiples NIC (físicas y virtuales), lo que significa que puede tener asignadas múltiples direcciones IP, lo que le permite comunicarse en varias redes. La identificación de oportunidades pivotantes a menudo dependerá de las IP específicas asignadas a los hosts que comprometemos porque pueden indicar las redes a las que pueden llegar los hosts comprometidos. Por eso es importante para nosotros comprobar siempre si hay NIC adicionales mediante comandos como `ifconfig`(en macOS y Linux) y `ipconfig`(en Windows).

### **Usando ifconfig**

```shell-session
afsh4ck@kali$ ifconfig

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 134.122.100.200  netmask 255.255.240.0  broadcast 134.122.111.255
        inet6 fe80::e973:b08d:7bdf:dc67  prefixlen 64  scopeid 0x20<link>
        ether 12:ed:13:35:68:f5  txqueuelen 1000  (Ethernet)
        RX packets 8844  bytes 803773 (784.9 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 5698  bytes 9713896 (9.2 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.106.0.172  netmask 255.255.240.0  broadcast 10.106.15.255
        inet6 fe80::a5bf:1cd4:9bca:b3ae  prefixlen 64  scopeid 0x20<link>
        ether 4e:c7:60:b0:01:8d  txqueuelen 1000  (Ethernet)
        RX packets 15  bytes 1620 (1.5 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 18  bytes 1858 (1.8 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 19787  bytes 10346966 (9.8 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 19787  bytes 10346966 (9.8 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500
        inet 10.10.15.54  netmask 255.255.254.0  destination 10.10.15.54
        inet6 fe80::c85a:5717:5e3a:38de  prefixlen 64  scopeid 0x20<link>
        inet6 dead:beef:2::1034  prefixlen 64  scopeid 0x0<global>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 7  bytes 336 (336.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

En el resultado anterior, cada NIC tiene un identificador ( `eth0`, `eth1`, `lo`, `tun0`) seguido de información de dirección y estadísticas de tráfico. La interfaz del túnel (tun0) indica que hay una conexión VPN activa. Cuando nos conectamos a cualquiera de los servidores VPN de HTB a través de Pwnbox o nuestro propio host de ataque, siempre notaremos que se crea una interfaz de túnel y se le asigna una dirección IP.&#x20;

La VPN nos permite acceder a los entornos de red del laboratorio alojados en HTB. Tenga en cuenta que no se puede acceder a estas redes de laboratorio sin tener un túnel establecido. La VPN cifra el tráfico y también establece un túnel a través de una red pública (a menudo Internet), a través `NAT`de un dispositivo de red público y hacia la red interna/privada. Además, observe las direcciones IP asignadas a cada NIC. La IP asignada a eth0 ( `134.122.100.200`) es una dirección IP enrutable públicamente. Lo que significa que los ISP enrutarán el tráfico que se origine desde esta IP a través de Internet.

Veremos IP públicas en dispositivos que están directamente frente a Internet, comúnmente alojados en DMZ. Las otras NIC tienen direcciones IP privadas, que se pueden enrutar dentro de las redes internas pero no a través de la Internet pública. Al momento de escribir este artículo, cualquiera que quiera comunicarse a través de Internet debe tener al menos una dirección IP pública asignada a una interfaz en el dispositivo de red que se conecta a la infraestructura física que se conecta a Internet. Recuerde que NAT se usa comúnmente para traducir direcciones IP privadas a direcciones IP públicas.

### **Usando ipconfig en Windows**

```powershell
PS C:\Users\htb-student> ipconfig

Windows IP Configuration

Unknown adapter NordLynx:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :

Ethernet adapter Ethernet0 2:

   Connection-specific DNS Suffix  . : .htb
   IPv6 Address. . . . . . . . . . . : dead:beef::1a9
   IPv6 Address. . . . . . . . . . . : dead:beef::f58b:6381:c648:1fb0
   Temporary IPv6 Address. . . . . . : dead:beef::dd0b:7cda:7118:3373
   Link-local IPv6 Address . . . . . : fe80::f58b:6381:c648:1fb0%8
   IPv4 Address. . . . . . . . . . . : 10.129.221.36
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
   Default Gateway . . . . . . . . . : fe80::250:56ff:feb9:df81%8
                                       10.129.0.1

Ethernet adapter Ethernet:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
```

El resultado directamente arriba proviene del comando `ipconfig` en un sistema Windows. Podemos ver que este sistema tiene múltiples adaptadores, pero solo uno de ellos tiene direcciones IP asignadas. Hay direcciones [IPv6](https://www.cisco.com/c/en/us/solutions/ipv6/overview.html) y una dirección [IPv4](https://en.wikipedia.org/wiki/IPv4) . Este módulo se centrará principalmente en redes que ejecutan IPv4, ya que sigue siendo el mecanismo de direccionamiento IP más común en las LAN empresariales. Notaremos que algunos adaptadores, como el del resultado anterior, tendrán una dirección IPv4 y una dirección IPv6 asignadas en una [configuración de doble pila,](https://www.cisco.com/c/dam/en_us/solutions/industries/docs/gov/IPV6at_a_glance_c45-625859.pdf) lo que permitirá acceder a los recursos a través de IPv4 o IPv6.

Cada dirección IPv4 tendrá una correspondiente `máscara de subred`. Si una dirección IP es como un número de teléfono, la máscara de subred es como el código de área. Recuerde que la máscara de subred define la parte `network` y `host` de una dirección IP. Cuando el tráfico de red está destinado a una dirección IP ubicada en una red diferente, la computadora enviará el tráfico a su dirección IP asignada (`Puerta de enlace predeterminada`).&#x20;

La puerta de enlace predeterminada suele ser la dirección IP asignada a una NIC en un dispositivo que actúa como enrutador para una LAN determinada. En el contexto del pivotamiento, debemos tener en cuenta a qué redes puede llegar un host al que aterrizamos, por lo que documentar la mayor cantidad posible de información de direcciones IP en un compromiso puede resultar útil.

***

## <mark style="color:purple;">Enrutamiento</mark>

Es común pensar en un dispositivo de red que nos conecta a Internet cuando pensamos en un enrutador, pero técnicamente cualquier computadora puede convertirse en enrutador y participar en el enrutamiento. Algunos de los desafíos que enfrentaremos en este módulo requieren que hagamos un host pivote para enrutar el tráfico a otra red. Una forma de ver esto es mediante el uso de AutoRoute, que permite que nuestro host de ataque tenga `rutas` como objetivo redes a las que se puede acceder a través de un host pivote. Una característica clave que define a un enrutador es que tiene una tabla de enrutamiento que utiliza para reenviar el tráfico según la dirección IP de destino. Veamos esto en Pwnbox usando los comandos `netstat -r` o `ip route`.

### **Tabla de enrutamiento en Pwnbox**

```shell-session
afsh4ck@kali$ netstat -r

Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
default         178.62.64.1     0.0.0.0         UG        0 0          0 eth0
10.10.10.0      10.10.14.1      255.255.254.0   UG        0 0          0 tun0
10.10.14.0      0.0.0.0         255.255.254.0   U         0 0          0 tun0
10.106.0.0      0.0.0.0         255.255.240.0   U         0 0          0 eth1
10.129.0.0      10.10.14.1      255.255.0.0     UG        0 0          0 tun0
178.62.64.0     0.0.0.0         255.255.192.0   U         0 0          0 eth0
```

Notaremos que Pwnbox, las distribuciones de Linux, Windows y muchos otros sistemas operativos tienen una tabla de enrutamiento para ayudar al sistema a tomar decisiones de enrutamiento. Cuando se crea un paquete y tiene un destino antes de salir de la computadora, la tabla de enrutamiento se utiliza para decidir dónde enviarlo. Por ejemplo, si intentamos conectarnos a un destino con la IP `10.129.10.25`, podríamos saber en la tabla de enrutamiento dónde se enviaría el paquete para llegar allí. Se reenviará a un `Gateway` fuera de la NIC correspondiente ( `Iface`).&#x20;

Pwnbox no utiliza ningún protocolo de enrutamiento (EIGRP, OSPF, BGP, etc.) para aprender cada una de esas rutas. Se enteró de esas rutas a través de sus propias interfaces conectadas directamente (eth0, eth1, tun0). Los dispositivos independientes designados como enrutadores normalmente aprenderán rutas mediante una combinación de creación de rutas estáticas, protocolos de enrutamiento dinámico e interfaces conectadas directamente.&#x20;

Cualquier tráfico destinado a redes que no estén presentes en la tabla de enrutamiento se enviará al `default route`, que también puede denominarse puerta de enlace predeterminada o puerta de enlace de último recurso. Al buscar oportunidades para pivotar, puede resultar útil consultar la tabla de enrutamiento de los hosts para identificar a qué redes podemos llegar o qué rutas debemos agregar.

***

## <mark style="color:purple;">Protocolos, Servicios y Puertos</mark>

Los `Protocolos` son las reglas que rigen las comunicaciones de la red. Muchos protocolos y servicios tienen correspondientes `puertos` que actúan como identificadores. Los puertos lógicos no son elementos físicos que podamos tocar o conectar. Están en el software asignado a las aplicaciones. Cuando vemos una dirección IP, sabemos que identifica una computadora a la que se puede acceder a través de una red. Cuando vemos un puerto abierto vinculado a esa dirección IP, sabemos que identifica una aplicación a la que podemos conectarnos. Conectarnos a puertos específicos en los que se encuentra un dispositivo `en escucha` a menudo puede permitirnos utilizar puertos y protocolos que se encuentran `permitidos` en el firewall para afianzarnos en la red.

Tomemos, por ejemplo, un servidor web que utiliza HTTP ( `normalmente escuchando en el puerto 80`). Los administradores no deben bloquear el tráfico entrante por el puerto 80. Esto impediría que cualquiera visite el sitio web. Esta suele ser una forma de acceder al entorno de red `a través del mismo puerto por el que pasa el tráfico legítimo`. No debemos pasar por alto el hecho de que el `puerto fuente` también se genera un para realizar un seguimiento de las conexiones establecidas en el lado del cliente de una conexión. Necesitamos ser conscientes de qué puertos estamos utilizando para asegurarnos de que cuando ejecutemos nuestras cargas útiles, se conecten nuevamente a los oyentes previstos que configuramos. Seremos creativos con el uso de puertos a lo largo de este módulo.

***

## <mark style="color:purple;">Para finalizar</mark>

En este módulo, practicaremos muchas herramientas y técnicas diferentes para pivotar a través de hosts y reenviar servicios locales o remotos a nuestro host de ataque para acceder a objetivos conectados a diferentes redes. Este módulo aumenta gradualmente en dificultad, proporcionando redes de múltiples hosts para practicar lo aprendido. Le recomiendo encarecidamente que practique muchos métodos diferentes de forma creativa a medida que empiece a comprender los conceptos. Tal vez incluso intente dibujar las topologías de la red utilizando herramientas de diagramación de red a medida que enfrenta desafíos. Cuando busco oportunidades para pivotar, me gusta usar herramientas como [Draw.io](https://draw.io/) para crear una imagen del entorno de red en el que estoy; también sirve como una excelente herramienta de documentación.

{% embed url="<https://draw.io>" %}

<figure><img src="/files/V3HeSaqOCvH0iANAkpAc" alt=""><figcaption></figcaption></figure>

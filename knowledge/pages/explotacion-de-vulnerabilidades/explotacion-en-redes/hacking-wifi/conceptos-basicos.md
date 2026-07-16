
# Conceptos básicos

## <mark style="color:purple;">Tipos de IPs</mark>

<table><thead><tr><th width="236">Tipo de IP</th><th>Ejemplo</th></tr></thead><tbody><tr><td>IPv4 Pública</td><td><code>203.0.113.1</code></td></tr><tr><td>IPv4 Privada (Clase A)</td><td><code>10.0.0.1 - 10.255.255.255</code></td></tr><tr><td>IPv4 Privada (Clase B)</td><td><code>172.16.0.1 - 172.31.255.255</code></td></tr><tr><td>IPv4 Privada (Clase C)</td><td><code>192.168.0.1 - 192.168.255.255</code></td></tr><tr><td>Loopback</td><td><code>127.0.0.0 - 127.255.255.255 (127.0.0.1)</code></td></tr><tr><td>IPv6 Global</td><td><code>2001:0db8:85a3:0000:0000:8a2e:0370:7334</code></td></tr><tr><td>IPv6 Enlace Local</td><td><code>fe80::1%eth0</code></td></tr><tr><td>IPv6 Sitio Único</td><td><code>fec0::1</code></td></tr></tbody></table>

* Las direcciones `IP privadas` (Clase A, B, C) son reservadas para redes internas y no se utilizan en Internet público.&#x20;
* Las direcciones `IPv6` son representadas en notación hexadecimal y pueden ser mucho más largas que las direcciones IPv4.

## <mark style="color:purple;">Dirección MAC</mark>

Una dirección MAC (Media Access Control) es una identificación única asignada a la interfaz de red de un dispositivo para su uso en la capa de enlace de datos de una red. Cada dispositivo que se conecta a una red, ya sea a través de Ethernet o Wi-Fi, tiene <mark style="color:purple;">una dirección MAC única</mark>.

La dirección MAC es un identificador de hardware y se utiliza para identificar de manera única un dispositivo en una red local. Esta dirección se asigna a la tarjeta de red o interfaz de red de un dispositivo durante su fabricación y generalmente está compuesta por 6 bytes (48 bits) de hexadecimal.

La dirección MAC se utiliza en la capa de enlace de datos del modelo OSI para dirigir el tráfico de red entre dispositivos en la misma red local. A diferencia de las direcciones IP, que pueden cambiar dinámicamente, la dirección MAC de un dispositivo suele ser estática y única para ese dispositivo específico.

```bash
# Ejemplo de una dirección MAC
00:1A:2B:3C:4D:5E
```

## <mark style="color:purple;">TCP vs UDP</mark>

<table><thead><tr><th width="209.33333333333331">Característica</th><th>TCP</th><th>UDP</th></tr></thead><tbody><tr><td><strong>Envío de datos</strong></td><td>Establece conexión antes de enviar</td><td>Envia los datos directamente sin verificar</td></tr><tr><td><strong>Verificación</strong></td><td>Usa un sistema de verificación (ACK)</td><td>No utiliza verificación</td></tr><tr><td><strong>Conexión</strong></td><td>Orientado a la conexión</td><td>Sin conexión</td></tr><tr><td><strong>Velocidad</strong> </td><td>Lento</td><td>Rápido</td></tr><tr><td><strong>Fiabilidad</strong></td><td>Garantiza la entrega de datos</td><td>No garantiza la entrega</td></tr><tr><td><strong>Tamaño de Cabecera</strong></td><td>Cabecera más grande</td><td>Cabecera más pequeña</td></tr><tr><td><strong>Control de Flujo</strong></td><td>Control de flujo mediante ventana</td><td>Sin control de flujo</td></tr><tr><td><strong>Congestión</strong></td><td>Control de congestión</td><td>Sin control de congestión</td></tr><tr><td><strong>Uso</strong></td><td>Aplicaciones que requieren fiabilidad</td><td>Aplicaciones en tiempo real y streaming</td></tr><tr><td><strong>Ejemplos de Aplicaciones</strong></td><td>Transferencia de archivos (FTP), correo electrónico (SMTP), navegación web (HTTP)</td><td>Transmisión de video, llamadas VoIP, juegos en línea</td></tr></tbody></table>

## <mark style="color:purple;">Three Way Handshake</mark>

El `Three-Way Handshake` es un proceso fundamental en el establecimiento de una conexión TCP (Protocolo de Control de Transmisión) entre dos dispositivos en una red. Este proceso se lleva a cabo para garantizar que ambos extremos de la conexión estén sincronizados antes de comenzar la transmisión de datos. Aquí están los tres pasos del handshake:

1. **`SYN (Synchronize)`:** El proceso comienza cuando un dispositivo (`Client`) envía un paquete SYN al otro dispositivo (`Server`). El paquete SYN indica que A desea establecer una conexión y sugiere un número de secuencia inicial.
2. **`SYN-ACK (Synchronize-Acknowledge)`:** Si el dispositivo `Server` está dispuesto a establecer la conexión, responde con un paquete SYN-ACK. Este paquete indica que `Server` está listo para la conexión, reconoce el número de secuencia de `Client` y sugiere su propio número de secuencia inicial.
3. **`ACK (Acknowledge)`:** Finalmente, el dispositivo `Client` envía un paquete de ACK al dispositivo `Server`. Este paquete reconoce el número de secuencia de `Server` y establece la conexión. A partir de este momento, ambas partes pueden comenzar a intercambiar datos de manera confiable.

<figure><img src="/files/QZHLr4QttP26MKiLHTUz" alt=""><figcaption></figcaption></figure>

En resumen, el Three-Way Handshake asegura que ambas partes estén de acuerdo en establecer la conexión, y establece los números de secuencia iniciales para que puedan entenderse entre sí durante la transmisión de datos. Este proceso es crucial para la confiabilidad y la integridad de las conexiones TCP.

## <mark style="color:purple;">Puertos comunes</mark>

| Servicio        | Puerto TCP | Puerto UDP |
| --------------- | ---------- | ---------- |
| HTTP            | 80         | -          |
| HTTPS           | 443        | -          |
| FTP Control     | 21         | -          |
| FTP Datos       | 20         | -          |
| SSH             | 22         | -          |
| Telnet          | 23         | -          |
| DNS             | 53         | 53         |
| DHCP            | 67-68      | 67-68      |
| SMTP            | 25         | -          |
| POP3            | 110        | -          |
| IMAP            | 143        | -          |
| SNMP            | 161        | 161        |
| LDAP            | 389        | -          |
| HTTPS (TLS/SSL) | 8443       | -          |
| MySQL           | 3306       | -          |
| RDP             | 3389       | -          |
| NTP             | 123        | 123        |
| HTTP Proxy      | 8080       | -          |

## <mark style="color:purple;">Modelo OSI</mark>

El Modelo OSI (Open Systems Interconnection) es un modelo conceptual que proporciona una estructura para comprender y describir las funcionalidades de un sistema de comunicación de red. Se divide en siete capas, cada una responsable de funciones específicas.&#x20;

#### Las siete capas del Modelo OSI:

<figure><img src="/files/HZetYoL0rT5hKBxmI6wu" alt=""><figcaption></figcaption></figure>

Este modelo ayuda a entender cómo se estructuran y gestionan las comunicaciones en una red, dividiendo las responsabilidades en capas que interactúan entre sí de manera organizada. Cada capa se encarga de funciones específicas para lograr la comunicación efectiva entre sistemas en una red.<br>

## <mark style="color:purple;">Bandas WiFi - 2.4 vs 5GHz</mark>

Los routers modernos suelen ser dual band, incluyen ambas. Aquí podemos ver una tabla con las comparaciones entre ambas bandas:

<table data-header-hidden><thead><tr><th width="202"></th><th></th><th></th></tr></thead><tbody><tr><td></td><td><strong>2.4 GHz</strong></td><td><strong>5 GHz</strong></td></tr><tr><td><strong>Velocidad</strong></td><td>Menor velocidad máxima (generalmente entre 50 y 150 Mbps)</td><td>Mayor velocidad máxima (hasta 1 Gbps o más)</td></tr><tr><td><strong>Alcance</strong></td><td>Mayor alcance debido a que las ondas de 2.4 GHz son más largas y penetran mejor obstáculos como paredes</td><td>Menor alcance, más susceptible a interferencias de obstáculos</td></tr><tr><td><strong>Interferencia</strong></td><td>Más susceptible a interferencias, ya que muchos dispositivos (microondas, teléfonos inalámbricos, Bluetooth) usan la banda de 2.4 GHz</td><td>Menos interferencias, ya que hay menos dispositivos que usan esta banda</td></tr><tr><td><strong>Canales disponibles</strong></td><td>Menos canales (generalmente 11), y más solapamiento entre ellos</td><td>Más canales (generalmente 23), con menor solapamiento</td></tr><tr><td><strong>Compatibilidad</strong></td><td>Mayor compatibilidad, ya que la mayoría de los dispositivos soportan 2.4 GHz</td><td>Menor compatibilidad en dispositivos antiguos, pero todos los modernos suelen soportarla</td></tr><tr><td><strong>Uso recomendado</strong></td><td>Ideal para áreas grandes con obstáculos o para dispositivos que no requieren altas velocidades (navegación web, IoT)</td><td>Ideal para áreas pequeñas o dispositivos que requieren alta velocidad (streaming, juegos en línea, videollamadas)</td></tr></tbody></table>

## <mark style="color:purple;">Subnetting</mark>

El subnetting es una técnica utilizada en redes de computadoras para dividir una red IP en subredes más pequeñas. Este proceso a los administradores de red dividir una red empresarial en varias subredes sin hacerlo público en internet. Así el número de hosts que están a disposición del administrador aumenta considerablemente.

### Ejemplo:

Supongamos que tienes la red `192.168.1.0/24`. Esto significa que tienes 256 direcciones IP disponibles en esa red (desde `192.168.1.0` hasta `192.168.1.255`). Ahora, si deseas subdividir esa red en subredes más pequeñas, puedes realizar el subnetting. Por ejemplo, podrías dividirla en cuatro subredes más pequeñas:

1. Subred 1: `192.168.1.0/26` (64 direcciones IP desde `192.168.1.0` hasta `192.168.1.63`).
2. Subred 2: `192.168.1.64/26` (64 direcciones IP desde `192.168.1.64` hasta `192.168.1.127`).
3. Subred 3: `192.168.1.128/26` (64 direcciones IP desde `192.168.1.128` hasta `192.168.1.191`).
4. Subred 4: `192.168.1.192/26` (64 direcciones IP desde `192.168.1.192` hasta `192.168.1.255`).

En este ejemplo, cada subred tiene 64 direcciones IP disponibles, y la máscara de subred `/26` indica cuántos bits están reservados para la red y cuántos para los hosts. Puedes ajustar el tamaño de las subredes según tus necesidades específicas.

El subnetting es esencial para optimizar el uso de direcciones IP y para segmentar la red de manera que se puedan aplicar políticas de seguridad y mejorar la eficiencia en la gestión de la red.


# SNMP

## <mark style="color:purple;">Cómo funciona</mark>

Además, este protocolo también se puede utilizar para gestionar tareas de configuración y cambiar ajustes de forma remota. El hardware habilitado para SNMP incluye enrutadores, conmutadores, servidores, dispositivos IoT y muchos otros dispositivos que también pueden consultarse y controlarse mediante este protocolo estándar. Por tanto, es un protocolo para monitorear y administrar dispositivos de red. Además, se pueden gestionar tareas de configuración y realizar ajustes de forma remota utilizando este estándar. La versión actual es `SNMPv3`, lo que aumenta la seguridad de SNMP en particular, pero también la complejidad del uso de este protocolo.

Además del puro intercambio de información, SNMP también transmite comandos de control utilizando agentes a través del puerto UDP `161`. El cliente puede establecer valores específicos en el dispositivo y cambiar opciones y configuraciones con estos comandos. Mientras que en la comunicación clásica siempre es el cliente quien solicita activamente información al servidor, SNMP también permite el uso del llamado `traps` por el puerto UDP `162`. Son paquetes de datos enviados desde el servidor SNMP al cliente sin ser solicitados explícitamente. Si un dispositivo está configurado en consecuencia, se envía una captura SNMP al cliente una vez que ocurre un evento específico en el lado del servidor.

Para que el cliente y el servidor SNMP intercambien los valores respectivos, los objetos SNMP disponibles deben tener direcciones únicas conocidas en ambos lados. Este mecanismo de direccionamiento es un requisito previo absoluto para la transmisión exitosa de datos y el monitoreo de la red mediante SNMP.

### **MIB**

Para garantizar que el acceso SNMP funcione entre fabricantes y con diferentes combinaciones de cliente-servidor, se creó `Management Information Base`( ). `MIB`MIB es un formato independiente para almacenar información del dispositivo. Una MIB es un archivo de texto en el que todos los objetos SNMP consultables de un dispositivo se enumeran en una jerarquía de árbol estandarizada. Contiene al menos un `Object Identifier`( `OID`) que, además de la dirección unívoca necesaria y un nombre, también proporciona información sobre el tipo, los derechos de acceso y una descripción del objeto respectivo. Los archivos MIB están escritos en formato de texto ASCII basado en `Abstract Syntax Notation One`( `ASN.1`). Las MIB no contienen datos, pero explican dónde encontrar qué información y cómo se ve, qué devuelve valores para el OID específico o qué tipo de datos se utiliza.

### **OID**

Un OID representa un nodo en un espacio de nombres jerárquico. Una secuencia de números identifica de forma única cada nodo, lo que permite determinar la posición del nodo en el árbol. Cuanto más larga sea la cadena, más específica será la información. Muchos nodos en el árbol OID no contienen nada excepto referencias a los que están debajo de ellos. Los OID constan de números enteros y normalmente están concatenados mediante notación de puntos. Podemos buscar muchas MIB para los OID asociados en el [Registro de identificadores de objetos](https://www.alvestrand.no/objectid/) .

### **SNMPv1**

SNMP versión 1 ( `SNMPv1`) se utiliza para la gestión y supervisión de la red. SNMPv1 es la primera versión del protocolo y todavía se utiliza en muchas redes pequeñas. Admite la recuperación de información de dispositivos de red, permite la configuración de dispositivos y proporciona trampas, que son notificaciones de eventos. Sin embargo, SNMPv1 tiene un mecanismo `no built-in authentication`, lo que significa que cualquiera que acceda a la red puede leer y modificar los datos de la red. Otro defecto principal de SNMPv1 `no soporta encriptación` y todos los datos se envían en texto plano y pueden interceptarse fácilmente.

### **SNMPv2**

SNMPv2 existía en diferentes versiones. La versión que todavía existe hoy es `v2c`, y la extensión `c`significa SNMP basado en la comunidad. En cuanto a la seguridad, SNMPv2 está a la par con SNMPv1 y se ha ampliado con funciones adicionales del SNMP basado en terceros que ya no se utiliza. Sin embargo, un problema importante con la ejecución inicial del protocolo SNMP es que el protocolo `community string`que proporciona seguridad sólo se transmite en texto plano, lo que significa que no tiene cifrado incorporado.

### **SNMPv3**

La seguridad se ha incrementado enormemente gracias `SNMPv3`a funciones de seguridad como `authentication`el uso de nombre de usuario y contraseña y la transmisión `encryption`(a través de `pre-shared key`) de los datos. Sin embargo, la complejidad también aumenta en la misma medida, con muchas más opciones de configuración que `v2c`.

### **Community Strings**

Las `Community Strings` pueden verse como contraseñas que se utilizan para determinar si la información solicitada se puede ver o no. Es importante tener en cuenta que muchas organizaciones todavía utilizan `SNMPv2`, ya que la transición `SNMPv3` puede ser muy compleja, pero los servicios aún deben permanecer activos. Esto preocupa mucho a muchos administradores y crea algunos problemas que desean evitar. La falta de conocimiento sobre cómo se puede obtener la información y cómo la utilizamos nosotros como atacantes hace que el enfoque de los administradores parezca inexplicable. Al mismo tiempo, la falta de cifrado de los datos enviados también supone un problema. Porque cada vez que las cadenas de comunidad se envían a través de la red, pueden ser interceptadas y leídas.

***

## <mark style="color:purple;">Configuración predeterminada</mark>

La configuración predeterminada del demonio SNMP define las configuraciones básicas para el servicio, que incluyen las direcciones IP, puertos, MIB, OID, autenticación y cadenas de comunidad.

### **SNMP Daemon Config**

```bash
afsh4ck$ cat /etc/snmp/snmpd.conf | grep -v "#" | sed -r '/^\s*$/d'

sysLocation    Sitting on the Dock of the Bay
sysContact     Me <me@example.org>
sysServices    72
master  agentx
agentaddress  127.0.0.1,[::1]
view   systemonly  included   .1.3.6.1.2.1.1
view   systemonly  included   .1.3.6.1.2.1.25.1
rocommunity  public default -V systemonly
rocommunity6 public default -V systemonly
rouser authPrivUser authpriv -V systemonly
```

La configuración de este servicio también se puede cambiar de muchas formas. Por lo tanto, recomendamos configurar una VM para instalar y configurar nosotros mismos el servidor SNMP. Todas las configuraciones que se pueden realizar para el demonio SNMP se definen y describen en la [página de manual](http://www.net-snmp.org/docs/man/snmpd.conf.html) .

***

## <mark style="color:purple;">Configuraciones peligrosas</mark>

Algunas configuraciones peligrosas que el administrador puede realizar con SNMP son:

<table data-header-hidden><thead><tr><th width="356"></th><th></th></tr></thead><tbody><tr><td><strong>Ajustes</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>rwuser noauth</code></td><td>Proporciona acceso al árbol OID completo sin autenticación.</td></tr><tr><td><code>rwcommunity &#x3C;community string> &#x3C;IPv4 address></code></td><td>Proporciona acceso al árbol OID completo independientemente de dónde se enviaron las solicitudes.</td></tr><tr><td><code>rwcommunity6 &#x3C;community string> &#x3C;IPv6 address></code></td><td>Mismo acceso que con <code>rwcommunity</code>la diferencia de usar IPv6.</td></tr></tbody></table>

***

## <mark style="color:purple;">Enumeración del servicio</mark>

Para realizar un seguimiento de SNMP, podemos utilizar herramientas como `snmpwalk`, `onesixtyone`y `braa`.&#x20;

`Snmpwalk` se utiliza para consultar los OID con su información. `Onesixtyone` se puede utilizar para forzar por fuerza bruta los nombres de las cadenas de la comunidad, ya que el administrador puede nombrarlas arbitrariamente. Dado que estas cadenas de comunidad pueden vincularse a cualquier fuente, identificar las cadenas de comunidad existentes puede llevar bastante tiempo.

### <mark style="color:purple;">Cheatsheet</mark>

<table data-header-hidden><thead><tr><th width="328"></th><th></th></tr></thead><tbody><tr><td><strong>Comando</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>snmpwalk -v2c -c &#x3C;community string> &#x3C;FQDN/IP></code></td><td>Consulta de OID mediante snmpwalk.</td></tr><tr><td><code>onesixtyone -c community-strings.list &#x3C;FQDN/IP></code></td><td>Community Strings de fuerza bruta del servicio SNMP.</td></tr><tr><td><code>braa &#x3C;community string>@&#x3C;FQDN/IP>:.1.*</code></td><td>OID del servicio SNMP de fuerza bruta.</td></tr></tbody></table>

### **SNMPwalk**

```bash
afsh4ck$ snmpwalk -v2c -c public 10.129.14.128

iso.3.6.1.2.1.1.1.0 = STRING: "Linux htb 5.11.0-34-generic #36~20.04.1-Ubuntu SMP Fri Aug 27 08:06:32 UTC 2021 x86_64"
iso.3.6.1.2.1.1.2.0 = OID: iso.3.6.1.4.1.8072.3.2.10
iso.3.6.1.2.1.1.3.0 = Timeticks: (5134) 0:00:51.34
iso.3.6.1.2.1.1.4.0 = STRING: "mrb3n@inlanefreight.htb"
iso.3.6.1.2.1.1.5.0 = STRING: "htb"
iso.3.6.1.2.1.1.6.0 = STRING: "Sitting on the Dock of the Bay"
iso.3.6.1.2.1.1.7.0 = INTEGER: 72
iso.3.6.1.2.1.1.8.0 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.2.1 = OID: iso.3.6.1.6.3.10.3.1.1
iso.3.6.1.2.1.1.9.1.2.2 = OID: iso.3.6.1.6.3.11.3.1.1
iso.3.6.1.2.1.1.9.1.2.3 = OID: iso.3.6.1.6.3.15.2.1.1
iso.3.6.1.2.1.1.9.1.2.4 = OID: iso.3.6.1.6.3.1
iso.3.6.1.2.1.1.9.1.2.5 = OID: iso.3.6.1.6.3.16.2.2.1
iso.3.6.1.2.1.1.9.1.2.6 = OID: iso.3.6.1.2.1.49
iso.3.6.1.2.1.1.9.1.2.7 = OID: iso.3.6.1.2.1.4
iso.3.6.1.2.1.1.9.1.2.8 = OID: iso.3.6.1.2.1.50
iso.3.6.1.2.1.1.9.1.2.9 = OID: iso.3.6.1.6.3.13.3.1.3
iso.3.6.1.2.1.1.9.1.2.10 = OID: iso.3.6.1.2.1.92
iso.3.6.1.2.1.1.9.1.3.1 = STRING: "The SNMP Management Architecture MIB."
iso.3.6.1.2.1.1.9.1.3.2 = STRING: "The MIB for Message Processing and Dispatching."
iso.3.6.1.2.1.1.9.1.3.3 = STRING: "The management information definitions for the SNMP User-based Security Model."
iso.3.6.1.2.1.1.9.1.3.4 = STRING: "The MIB module for SNMPv2 entities"
iso.3.6.1.2.1.1.9.1.3.5 = STRING: "View-based Access Control Model for SNMP."
iso.3.6.1.2.1.1.9.1.3.6 = STRING: "The MIB module for managing TCP implementations"
iso.3.6.1.2.1.1.9.1.3.7 = STRING: "The MIB module for managing IP and ICMP implementations"
iso.3.6.1.2.1.1.9.1.3.8 = STRING: "The MIB module for managing UDP implementations"
iso.3.6.1.2.1.1.9.1.3.9 = STRING: "The MIB modules for managing SNMP Notification, plus filtering."
iso.3.6.1.2.1.1.9.1.3.10 = STRING: "The MIB module for logging SNMP Notifications."
iso.3.6.1.2.1.1.9.1.4.1 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.2 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.3 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.4 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.5 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.6 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.7 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.8 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.9 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.10 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.25.1.1.0 = Timeticks: (3676678) 10:12:46.78
iso.3.6.1.2.1.25.1.2.0 = Hex-STRING: 07 E5 09 14 0E 2B 2D 00 2B 02 00 
iso.3.6.1.2.1.25.1.3.0 = INTEGER: 393216
iso.3.6.1.2.1.25.1.4.0 = STRING: "BOOT_IMAGE=/boot/vmlinuz-5.11.0-34-generic root=UUID=9a6a5c52-f92a-42ea-8ddf-940d7e0f4223 ro quiet splash"
iso.3.6.1.2.1.25.1.5.0 = Gauge32: 3
iso.3.6.1.2.1.25.1.6.0 = Gauge32: 411
iso.3.6.1.2.1.25.1.7.0 = INTEGER: 0
iso.3.6.1.2.1.25.1.7.0 = No more variables left in this MIB View (It is past the end of the MIB tree)

...SNIP...

iso.3.6.1.2.1.25.6.3.1.2.1232 = STRING: "printer-driver-sag-gdi_0.1-7_all"
iso.3.6.1.2.1.25.6.3.1.2.1233 = STRING: "printer-driver-splix_2.0.0+svn315-7fakesync1build1_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1234 = STRING: "procps_2:3.3.16-1ubuntu2.3_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1235 = STRING: "proftpd-basic_1.3.6c-2_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1236 = STRING: "proftpd-doc_1.3.6c-2_all"
iso.3.6.1.2.1.25.6.3.1.2.1237 = STRING: "psmisc_23.3-1_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1238 = STRING: "publicsuffix_20200303.0012-1_all"
iso.3.6.1.2.1.25.6.3.1.2.1239 = STRING: "pulseaudio_1:13.99.1-1ubuntu3.12_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1240 = STRING: "pulseaudio-module-bluetooth_1:13.99.1-1ubuntu3.12_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1241 = STRING: "pulseaudio-utils_1:13.99.1-1ubuntu3.12_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1242 = STRING: "python-apt-common_2.0.0ubuntu0.20.04.6_all"
iso.3.6.1.2.1.25.6.3.1.2.1243 = STRING: "python3_3.8.2-0ubuntu2_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1244 = STRING: "python3-acme_1.1.0-1_all"
iso.3.6.1.2.1.25.6.3.1.2.1245 = STRING: "python3-apport_2.20.11-0ubuntu27.21_all"
iso.3.6.1.2.1.25.6.3.1.2.1246 = STRING: "python3-apt_2.0.0ubuntu0.20.04.6_amd64" 

...SNIP...
```

En el caso de una mala configuración, obtendríamos aproximadamente los mismos resultados de `snmpwalk` que se muestran arriba. Una vez que conocemos la Community String y el servicio SNMP que no requiere autenticación (versiones 1, 2c), podemos consultar información interna del sistema como en el ejemplo anterior.

Aquí reconocemos algunos paquetes de Python que se han instalado en el sistema. Si no conocemos la Community String, podemos usar listas de palabras `onesixtyone`y `SecLists` para identificar estas cadenas de comunidad.

### **OneSixtyOne**

```bash
afsh4ck$ sudo apt install onesixtyone
afsh4ck$ onesixtyone -c /opt/useful/SecLists/Discovery/SNMP/snmp.txt 10.129.14.128

Scanning 1 hosts, 3220 communities
10.129.14.128 [public] Linux htb 5.11.0-37-generic #41~20.04.2-Ubuntu SMP Fri Sep 24 09:06:38 UTC 2021 x86_64
```

A menudo, cuando ciertas Community String están vinculadas a direcciones IP específicas, se nombran con el nombre de host del host y, a veces, incluso se agregan símbolos a estos nombres para que sean más difíciles de identificar.&#x20;

Sin embargo, si imaginamos una red extensa con más de 100 servidores diferentes gestionados mediante SNMP, las etiquetas, en ese caso, tendrán algún patrón. Por tanto, podemos utilizar diferentes reglas para adivinarlos. Podemos utilizar la herramienta [Crunch](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/diccionarios-custom/crunch.md) para crear listas de palabras personalizadas.

Una vez que conocemos una cadena de comunidad, podemos usarla con [braa](https://github.com/mteg/braa) para aplicar fuerza bruta a los OID individuales y enumerar la información detrás de ellos.

### **braa**

```bash
afsh4ck$ sudo apt install braa
afsh4ck$ braa <community string>@<IP>:.1.3.6.*   # Syntax
afsh4ck$ braa public@10.129.14.128:.1.3.6.*

10.129.14.128:20ms:.1.3.6.1.2.1.1.1.0:Linux htb 5.11.0-34-generic #36~20.04.1-Ubuntu SMP Fri Aug 27 08:06:32 UTC 2021 x86_64
10.129.14.128:20ms:.1.3.6.1.2.1.1.2.0:.1.3.6.1.4.1.8072.3.2.10
10.129.14.128:20ms:.1.3.6.1.2.1.1.3.0:548
10.129.14.128:20ms:.1.3.6.1.2.1.1.4.0:mrb3n@inlanefreight.htb
10.129.14.128:20ms:.1.3.6.1.2.1.1.5.0:htb
10.129.14.128:20ms:.1.3.6.1.2.1.1.6.0:US
10.129.14.128:20ms:.1.3.6.1.2.1.1.7.0:78
...SNIP...
```

Una vez más queremos señalar que la configuración independiente del servicio SNMP nos aportará una gran variedad de experiencias diferentes que ningún tutorial podrá sustituir. Por lo tanto, recomendamos encarecidamente configurar una máquina virtual con SNMP, experimentar con ella y probar diferentes configuraciones. SNMP puede ser una bendición para un administrador de sistemas de IT, así como una maldición tanto para los analistas como para los gerentes de seguridad.


# AD: Enumeración inicial del dominio

Estamos en el comienzo de nuestra prueba de penetración centrada en AD contra Inlanefreight. Hemos recopilado información básica y hemos obtenido una idea de qué esperar del cliente a través de los documentos de alcance.

***

## <mark style="color:purple;">Configuración</mark>

Para esta primera parte de la prueba, comenzaremos con un host de ataque ubicado dentro de la red. Esta es una forma común que un cliente puede seleccionar para que realicemos una prueba de penetración interna. Una lista de los tipos de configuraciones que un cliente puede elegir para realizar pruebas incluye:

* Una distribución de prueba de penetración (normalmente Linux) como una máquina virtual en su infraestructura interna que vuelve a llamar a un host de salto que controlamos a través de VPN y al que podemos acceder mediante SSH.
* Un dispositivo físico conectado a un puerto Ethernet que nos devuelve la llamada a través de VPN y al que podemos acceder mediante SSH.
* Una presencia física en su oficina con nuestra computadora portátil conectada a un puerto ethernet.
* Una máquina virtual Linux en Azure o AWS con acceso a la red interna a la que podemos acceder mediante SSH mediante autenticación de clave pública y nuestra dirección IP pública en la lista blanca.
* Acceso VPN a su red interna (un poco limitante porque no podremos realizar ciertos ataques como LLMNR/NBT-NS Poisoning).
* Desde un portátil corporativo conectado a la VPN del cliente.
* En una estación de trabajo administrada (normalmente Windows), sentado físicamente en su oficina con acceso a Internet limitado o nulo o capacidad para utilizar herramientas. También pueden elegir esta opción, pero le brindarán acceso completo a Internet, administración local y pondrán la protección del punto final en modo de monitor para que pueda utilizar herramientas a voluntad.
* En un VDI (escritorio virtual) al que se accede mediante Citrix o similar, con una de las configuraciones descritas para la estación de trabajo administrada generalmente accesible a través de VPN, ya sea de forma remota o desde una computadora portátil corporativa.

Estas son las configuraciones más comunes que he visto, aunque a un cliente se le puede ocurrir otra variación de una de ellas. El cliente también puede elegir entre un enfoque de "caja gris", donde nos dan solo una lista de direcciones IP/rangos de red CIDR dentro del alcance, o una "caja negra", donde tenemos que conectarnos y hacer todo el descubrimiento a ciegas utilizando varias técnicas. Finalmente, pueden elegir entre evasiva, no evasiva o evasiva híbrida (comenzando en "silencio" y aumentando lentamente el volumen para ver en qué umbral se nos detecta y luego cambiar a pruebas no evasivas. También pueden optar por que comencemos con sin credenciales o desde la perspectiva de un usuario de dominio estándar.

Nuestro cliente Inlanefreight ha elegido el siguiente enfoque porque busca una evaluación lo más completa posible. En este momento, su programa de seguridad no está lo suficientemente maduro como para beneficiarse de cualquier forma de prueba evasiva o de un enfoque de "caja negra".

* Una máquina virtual de pentest personalizada dentro de su red interna que vuelve a llamar a nuestro host de salto y podemos ingresar mediante SSH para realizar pruebas.
* También nos han proporcionado un host de Windows en el que podemos cargar herramientas si es necesario.
* Nos pidieron que comenzáramos desde un punto de vista no autenticado, pero también nos dieron una cuenta de usuario de dominio estándar ( `htb-student`) que puede usarse para acceder al host de ataque de Windows.
* Prueba de "caja gris". Nos han dado el rango de red `172.16.5.0/23` y ninguna otra información sobre la red.
* Pruebas no evasivas.

No se nos han proporcionado credenciales ni un mapa detallado de la red interna.

***

## <mark style="color:purple;">Tareas</mark>

Nuestras tareas a realizar para esta sección son:

* Enumerar la red interna, identificando hosts, servicios críticos y vías potenciales para establecerse.
* Esto puede incluir medidas activas y pasivas para identificar usuarios, hosts y vulnerabilidades que podamos aprovechar para ampliar nuestro acceso.
* Documentar cualquier hallazgo que encontremos para su uso posterior. ¡Extremadamente importante!

Comenzaremos desde nuestro host de ataque Linux sin credenciales de usuario de dominio. Es común comenzar un pentest de esta manera. Muchas organizaciones querrán ver qué puede hacer usted desde una perspectiva ciega, como esta, antes de brindarle más información para la prueba. Ofrece una visión más realista de las posibles vías que tendría que utilizar un adversario para infiltrarse en el dominio. Puede ayudarles a ver lo que podría hacer un atacante si obtiene acceso no autorizado a través de Internet (es decir, un ataque de phishing), acceso físico al edificio, acceso inalámbrico desde el exterior (si la red inalámbrica toca el entorno AD) o incluso un empleado deshonesto (insider). Dependiendo del éxito de esta fase, el cliente puede proporcionarnos acceso a un host unido a un dominio o un conjunto de credenciales para la red para acelerar las pruebas y permitirnos cubrir la mayor cantidad de terreno posible.

A continuación se detallan algunos de los puntos de datos clave que deberíamos buscar en este momento y anotarlos en nuestra herramienta para tomar notas de elección y guardar los resultados del escaneo/herramienta en archivos siempre que sea posible.

### **Puntos de datos clave**

<table data-header-hidden><thead><tr><th width="235"></th><th></th></tr></thead><tbody><tr><td><strong>Punto de datos</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>Usuarios AD</code></td><td>Estamos intentando enumerar cuentas de usuario válidas a las que podamos apuntar para la pulverización de contraseñas.</td></tr><tr><td><code>Máquinas unidas a AD</code></td><td>Las computadoras clave incluyen controladores de dominio, servidores de archivos, servidores SQL, servidores web, servidores de correo Exchange, servidores de bases de datos, etc.</td></tr><tr><td><code>Servicios clave</code></td><td>Kerberos, NetBIOS, LDAP, DNS</td></tr><tr><td><code>Hosts y Servicios vulnerables</code></td><td>Cualquier cosa que pueda ser una victoria rápida. (también conocido como un host fácil de explotar y afianzarse)</td></tr></tbody></table>

***

### <mark style="color:purple;">TTPs</mark>

Enumerar un entorno de AD puede resultar abrumador si se aborda sin un plan. Hay una gran cantidad de datos almacenados en AD, y puede llevar mucho tiempo examinarlos si no se analizan en etapas progresivas, y es probable que nos perdamos cosas. Necesitamos establecer un plan de acción y abordarlo pieza por pieza. Todos trabajan de maneras ligeramente diferentes, por lo que a medida que adquiramos más experiencia, comenzaremos a desarrollar nuestra propia metodología repetible que funcione mejor para nosotros.&#x20;

Independientemente de cómo procedamos, normalmente comenzamos en el mismo lugar y buscamos los mismos puntos de datos. Experimentaremos con muchas herramientas en esta sección y en las siguientes. Es importante reproducir cada ejemplo e incluso intentar recrear ejemplos con diferentes herramientas para ver cómo funcionan de manera diferente, aprender su sintaxis y encontrar qué enfoque funciona mejor para nosotros.

Comenzaremos con la identificación `pasiva` de los hosts en la red, seguido de la validación `activa` de los resultados para obtener más información sobre cada host (qué servicios se están ejecutando, nombres, vulnerabilidades potenciales, etc.). Una vez que sabemos qué hosts existen, podemos proceder a sondearlos en busca de datos interesantes que podamos obtener de ellos. Una vez que hayamos realizado estas tareas, debemos detenernos, reagruparnos y observar qué información tenemos. En este momento, es de esperar que tengamos un conjunto de credenciales o una cuenta de usuario a la que apuntar para establecernos en un host unido a un dominio o que tengamos la capacidad de comenzar la enumeración de credenciales desde nuestro host de ataque Linux.

Veamos algunas herramientas y técnicas que nos ayudarán con esta enumeración.

***

### <mark style="color:purple;">Identificar Hosts</mark>

Primero, tomemos un tiempo para escuchar la red y ver qué está pasando. Podemos usar `Wireshark` y `TCPDump` para "ponernos a la escucha" y ver qué hosts y tipos de tráfico de red podemos capturar. Esto es particularmente útil si el enfoque de evaluación es el de "caja negra". Notamos algunas solicitudes y respuestas [ARP , ](https://en.wikipedia.org/wiki/Address_Resolution_Protocol)[MDNS](https://en.wikipedia.org/wiki/Multicast_DNS) y otros paquetes básicos [de capa dos](https://www.juniper.net/documentation/us/en/software/junos/multicast-l2/topics/topic-map/layer-2-understanding.html) (dado que estamos en una red conmutada, estamos limitados al dominio de transmisión actual), algunos de los cuales podemos ver a continuación. Este es un gran comienzo que nos brinda algunos datos sobre la configuración de la red del cliente.

#### **Iniciar Wireshark en ea-attack01**

```shell-session
┌─[htb-student@ea-attack01]─[~]
└──╼ $sudo -E wireshark

11:28:20.487     Main Warn QStandardPaths: runtime directory '/run/user/1001' is not owned by UID 0, but a directory permissions 0700 owned by UID 1001 GID 1002
<SNIP>
```

#### **Salida de Wireshark**

![imagen](https://academy.hackthebox.com/storage/modules/143/ea-wireshark.png)

* Los paquetes ARP nos informan de los hosts: `172.16.5.5`, `172.16.5.25`, `172.16.5.50`, `172.16.5.100` y `172.16.5.125`

![imagen](https://academy.hackthebox.com/storage/modules/143/ea-wireshark-mdns.png)

* MDNS nos informa del host `ACADEMY-EA-WEB01`

Si estamos en un host sin GUI (lo cual es típico), podemos usar [tcpdump](https://linux.die.net/man/8/tcpdump) , [net-creds](https://github.com/DanMcInerney/net-creds) y [NetMiner](https://www.netminer.com/en/product/netminer.php) , etc., para realizar las mismas funciones. También podemos usar tcpdump para guardar una captura en un archivo .pcap, transferirla a otro host y abrirla en Wireshark.

#### **Salida tcpdump**

```shell-session
afsh4ck@kali$ sudo tcpdump -i ens224 
```

![imagen](https://academy.hackthebox.com/storage/modules/143/tcpdump-example.png)

No existe una única forma correcta de escuchar y capturar el tráfico de la red. Existen muchas herramientas que pueden procesar datos de la red. Wireshark y tcpdump son sólo algunos de los más fáciles de usar y más conocidos. Dependiendo del host en el que se encuentre, es posible que ya tenga incorporada una herramienta de monitoreo de red, como `pktmon.exe`, que se agregó a todas las ediciones de Windows 10. Como nota para las pruebas, siempre es una buena idea guardar el tráfico PCAP que captura. Puede revisarlo nuevamente más tarde para buscar más sugerencias y constituye una excelente información adicional que puede incluir al redactar sus informes.

Nuestro primer vistazo al tráfico de la red nos señaló un par de hosts a través de `MDNS`y `ARP`. Ahora utilicemos una herramienta llamada `Responder`para analizar el tráfico de la red y determinar si aparece algo más en el dominio.

[Responder](https://github.com/lgandx/Responder-Windows) es una herramienta creada para escuchar, analizar y envenenar `LLMNR`solicitudes `NBT-NS`y `MDNS`respuestas. Tiene muchas más funciones, pero por ahora lo único que estamos utilizando es la herramienta en su modo Analizar. Esto escuchará pasivamente la red y no enviará ningún paquete envenenado. Cubriremos esta herramienta con más profundidad en secciones posteriores.

#### **Iniciar Responder**

```bash
sudo responder -I ens224 -A 
```

![imagen](https://academy.hackthebox.com/storage/modules/143/responder-example.gif)

Cuando iniciamos Responder con el modo de análisis pasivo habilitado, veremos el flujo de solicitudes en nuestra sesión. Observe a continuación que encontramos algunos hosts únicos que no se mencionaron anteriormente en nuestras capturas de Wireshark. Vale la pena anotarlos a medida que comenzamos a crear una buena lista de objetivos de IP y nombres de host DNS.

Nuestras comprobaciones pasivas nos han proporcionado algunos hosts para anotar para una enumeración más detallada. Ahora realicemos algunas comprobaciones activas comenzando con un barrido ICMP rápido de la subred usando `fping`.

[Fping](https://fping.org/) nos proporciona una capacidad similar a la aplicación de ping estándar en el sentido de que utiliza solicitudes y respuestas ICMP para comunicarse con un host e interactuar con él. Donde brilla fping es en su capacidad de emitir paquetes ICMP contra una lista de múltiples hosts a la vez y su capacidad de programación. Además, funciona en forma circular, consultando hosts de manera cíclica en lugar de esperar a que regresen múltiples solicitudes a un solo host antes de continuar. Estas comprobaciones nos ayudarán a determinar si hay algo más activo en la red interna. ICMP no es una ventanilla única, pero es una manera fácil de tener una idea inicial de lo que existe. Otros puertos abiertos y protocolos activos pueden apuntar a nuevos hosts para su posterior localización. Veámoslo en acción.

#### **Realizar comprobaciones activas**

Aquí comenzaremos `fping` con algunas opciones: (`a`) mostrar objetivos que están vivos, (`s`) imprimir estadísticas al final del escaneo, (`g`) generar una lista de objetivos desde la red CIDR y (`q`) no mostrar resultados por objetivo.

```shell-session
afsh4ck@kali$ fping -asgq 172.16.5.0/23

172.16.5.5
172.16.5.25
172.16.5.50
172.16.5.100
172.16.5.125
172.16.5.200
172.16.5.225
172.16.5.238
172.16.5.240

     510 targets
       9 alive
     501 unreachable
       0 unknown addresses

    2004 timeouts (waiting for response)
    2013 ICMP Echos sent
       9 ICMP Echo Replies received
    2004 other ICMP received

 0.029 ms (min round trip time)
 0.396 ms (avg round trip time)
 0.799 ms (max round trip time)
       15.366 sec (elapsed real time)
```

El comando anterior valida qué hosts están activos en la red `/23` y lo hace silenciosamente en lugar de enviar spam al terminal con resultados para cada IP en la lista de objetivos. Podemos combinar los resultados exitosos y la información que obtuvimos de nuestras comprobaciones pasivas en una lista para un escaneo más detallado con Nmap. Desde el comando `fping`, podemos ver 9 "hosts activos", incluido nuestro host de ataque.

Nota: Los resultados del escaneo en la red de destino diferirán del resultado del comando en esta sección debido al tamaño de la red del laboratorio. Aún así vale la pena reproducir cada ejemplo para practicar cómo funcionan estas herramientas y anotar cada host que esté activo en este laboratorio.

#### **Escaneo de Nmap**

Ahora que tenemos una lista de hosts activos dentro de nuestra red, podemos enumerarlos más. Buscamos determinar qué servicios ejecuta cada host, identificar hosts críticos como `Domain Controllers` y `web servers` e identificar hosts potencialmente vulnerables para investigar más adelante. Con nuestro enfoque en AD, después de hacer un análisis amplio, sería prudente que nos concentráramos en los protocolos estándar que normalmente acompañan a los servicios AD, como DNS, SMB, LDAP y Kerberos, por nombrar algunos. A continuación se muestra un ejemplo rápido de un escaneo Nmap simple.

```bash
sudo nmap -v -A -iL hosts.txt -oN /home/htb-student/Documents/host-enum
```

El escaneo [-A (opciones de escaneo agresivo)](https://nmap.org/book/man-misc-options.html) realizará varias funciones. Uno de los más importantes es una enumeración rápida de puertos conocidos para incluir servicios web, servicios de dominio, etc. Para nuestro archivo `hosts.txt`, algunos de nuestros resultados de Responder y fping se superpusieron (encontramos el nombre y la dirección IP). Entonces, para hacerlo simple, solo se ingresó la dirección IP en hosts.txt para el escaneo.

#### **Aspectos destacados de los resultados de NMAP**

```shell-session
Nmap scan report for inlanefreight.local (172.16.5.5)
Host is up (0.069s latency).
Not shown: 987 closed tcp ports (conn-refused)
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2022-04-04 15:12:06Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: INLANEFREIGHT.LOCAL0., Site: Default-First-Site-Name)
|_ssl-date: 2022-04-04T15:12:53+00:00; -1s from scanner time.
| ssl-cert: Subject:
| Subject Alternative Name: DNS:ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
| Issuer: commonName=INLANEFREIGHT-CA
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2022-03-30T22:40:24
| Not valid after:  2023-03-30T22:40:24
| MD5:   3a09 d87a 9ccb 5498 2533 e339 ebe3 443f
|_SHA-1: 9731 d8ec b219 4301 c231 793e f913 6868 d39f 7920
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: INLANEFREIGHT.LOCAL0., Site: Default-First-Site-Name)
<SNIP>  
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: INLANEFREIGHT.LOCAL0., Site: Default-First-Site-Name)
3269/tcp open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: INLANEFREIGHT.LOCAL0., Site: Default-First-Site-Name)
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info:
|   Target_Name: INLANEFREIGHT
|   NetBIOS_Domain_Name: INLANEFREIGHT
|   NetBIOS_Computer_Name: ACADEMY-EA-DC01
|   DNS_Domain_Name: INLANEFREIGHT.LOCAL
|   DNS_Computer_Name: ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
|   DNS_Tree_Name: INLANEFREIGHT.LOCAL
|   Product_Version: 10.0.17763
|_  System_Time: 2022-04-04T15:12:45+00:00
<SNIP>
5357/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Service Unavailable
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: Host: ACADEMY-EA-DC01; OS: Windows; CPE: cpe:/o:microsoft:windows
```

Nuestros escaneos nos han proporcionado el estándar de nombres utilizado por NetBIOS y DNS, podemos ver que algunos hosts tienen RDP abierto y nos han indicado la dirección principal `Domain Controller` para el dominio INLANEFREIGHT.LOCAL (ACADEMY-EA-DC01.INLANEFREIGHT. LOCAL). Los resultados a continuación muestran algunos resultados interesantes sobre un host posiblemente desactualizado (no en nuestro laboratorio actual).

```shell-session
afsh4ck@kali$ nmap -A 172.16.5.100

Starting Nmap 7.92 ( https://nmap.org ) at 2022-04-08 13:42 EDT
Nmap scan report for 172.16.5.100
Host is up (0.071s latency).
Not shown: 989 closed tcp ports (conn-refused)
PORT      STATE SERVICE      VERSION
80/tcp    open  http         Microsoft IIS httpd 7.5
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Microsoft-IIS/7.5
| http-methods: 
|_  Potentially risky methods: TRACE
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
443/tcp   open  https?
445/tcp   open  microsoft-ds Windows Server 2008 R2 Standard 7600 microsoft-ds
1433/tcp  open  ms-sql-s     Microsoft SQL Server 2008 R2 10.50.1600.00; RTM
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2022-04-08T17:38:25
|_Not valid after:  2052-04-08T17:38:25
|_ssl-date: 2022-04-08T17:43:53+00:00; 0s from scanner time.
| ms-sql-ntlm-info: 
|   Target_Name: INLANEFREIGHT
|   NetBIOS_Domain_Name: INLANEFREIGHT
|   NetBIOS_Computer_Name: ACADEMY-EA-CTX1
|   DNS_Domain_Name: INLANEFREIGHT.LOCAL
|   DNS_Computer_Name: ACADEMY-EA-CTX1.INLANEFREIGHT.LOCAL
|_  Product_Version: 6.1.7600
Host script results:
| smb2-security-mode: 
|   2.1: 
|_    Message signing enabled but not required
| ms-sql-info: 
|   172.16.5.100:1433: 
|     Version: 
|       name: Microsoft SQL Server 2008 R2 RTM
|       number: 10.50.1600.00
|       Product: Microsoft SQL Server 2008 R2
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
|_nbstat: NetBIOS name: ACADEMY-EA-CTX1, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:b9:c7:1c (VMware)
| smb-os-discovery: 
|   OS: Windows Server 2008 R2 Standard 7600 (Windows Server 2008 R2 Standard 6.1)
|   OS CPE: cpe:/o:microsoft:windows_server_2008::-
|   Computer name: ACADEMY-EA-CTX1
|   NetBIOS computer name: ACADEMY-EA-CTX1\x00
|   Domain name: INLANEFREIGHT.LOCAL
|   Forest name: INLANEFREIGHT.LOCAL
|   FQDN: ACADEMY-EA-CTX1.INLANEFREIGHT.LOCAL
|_  System time: 2022-04-08T10:43:48-07:00

<SNIP>
```

Podemos ver en el resultado anterior que tenemos un host potencial que ejecuta un sistema operativo desactualizado (Windows 7, 8 o Server 2008 según el resultado). Esto es de interés para nosotros ya que significa que hay `sistemas operativos heredados` ejecutándose en este entorno AD. También significa que existe la posibilidad de que exploits más antiguos como `EternalBlue`, `MS08-067` y otros funcionen y nos proporcionen un shell a nivel de SYSTEM. Por extraño que parezca tener hosts que ejecuten software heredado o sistemas operativos al final de su vida útil, sigue siendo común en entornos de grandes empresas.&#x20;

A menudo, tendrá algún proceso o equipo, como una línea de producción o HVAC, construido en el sistema operativo más antiguo y que ha estado en funcionamiento durante mucho tiempo. Desconectar equipos como ese es costoso y puede perjudicar a una organización, por lo que los hosts heredados a menudo se dejan en su lugar. Probablemente intentarán construir una capa exterior dura de firewalls, IDS/IPS y otras soluciones de monitoreo y protección alrededor de esos sistemas.&#x20;

Si puede encontrar el camino hacia uno, es un gran problema y puede ser un punto de apoyo rápido y fácil. Sin embargo, antes de explotar sistemas heredados, debemos alertar a nuestro cliente y obtener su aprobación por escrito en caso de que un ataque provoque inestabilidad en el sistema o haga caer un servicio o el host. Es posible que prefieran que simplemente observemos, informemos y sigamos adelante sin explotar activamente el sistema.

Los resultados de estos análisis nos indicarán dónde empezaremos a buscar posibles vías de enumeración de dominios, no sólo el análisis de hosts. Necesitamos encontrar el camino hacia una cuenta de usuario de dominio. Al observar nuestros resultados, encontramos varios servidores que alojan servicios de dominio (DC01, MX01, WS01, etc.). Ahora que sabemos qué existe y qué servicios se están ejecutando, podemos sondear esos servidores e intentar enumerar los usuarios. Asegúrese de utilizar la opción `-oA` como práctica recomendada al realizar escaneos de Nmap. Esto garantizará que tengamos los resultados de nuestro escaneo en varios formatos para fines de registro y formatos que puedan manipularse e introducirse en otras herramientas.

Necesitamos ser conscientes de qué análisis realizamos y cómo funcionan. Algunos de los análisis programados por Nmap ejecutan comprobaciones activas de vulnerabilidad en un host que podrían causar inestabilidad en el sistema o desconectarlo, causando problemas al cliente o algo peor. Por ejemplo, ejecutar un análisis de descubrimiento de gran tamaño en una red con dispositivos como sensores o controladores lógicos podría sobrecargarlos e interrumpir el equipo industrial del cliente, provocando una pérdida de producto o capacidad. Tómese el tiempo para comprender los análisis que utiliza antes de ejecutarlos en el entorno de un cliente.

Lo más probable es que volvamos a estos resultados más adelante para realizar una enumeración más detallada, así que no los olvide. Necesitamos encontrar el camino hacia una cuenta de usuario de dominio o `SYSTEM`nivelar el acceso en un host unido a un dominio para poder afianzarnos y comenzar la verdadera diversión. Profundicemos en la búsqueda de una cuenta de usuario.

***

### <mark style="color:purple;">Identificar usuarios</mark>

Si nuestro cliente no nos proporciona un usuario con el que comenzar a realizar las pruebas (lo que suele ser el caso), necesitaremos encontrar una manera de establecer un punto de apoyo en el dominio obteniendo credenciales de texto sin cifrar o un hash de contraseña NTLM para un usuario. , un shell de SISTEMA en un host unido a un dominio o un shell en el contexto de una cuenta de usuario de dominio. Obtener un usuario válido con credenciales es fundamental en las primeras etapas de una prueba de penetración interna. Este acceso (incluso en el nivel más bajo) abre muchas oportunidades para realizar enumeraciones e incluso ataques. Veamos una forma en que podemos comenzar a recopilar una lista de usuarios válidos en un dominio para usarla más adelante en nuestra evaluación.

#### Kerbrute: Enumeración interna de nombres de usuario de AD

[Kerbrute](https://github.com/ropnop/kerbrute) puede ser una opción más sigilosa para la enumeración de cuentas de dominio. Aprovecha el hecho de que los errores de autenticación previa de Kerberos a menudo no activan registros ni alertas. Usaremos Kerbrute junto con las listas de usuarios `jsmith.txt` y `jsmith2.txt` de [Insidetrust](https://github.com/insidetrust/statistically-likely-usernames) . Este repositorio contiene muchas listas de usuarios diferentes que pueden resultar extremadamente útiles al intentar enumerar usuarios desde una perspectiva no autenticada. Podemos apuntar a Kerbrute al DC que encontramos anteriormente y alimentarlo con una lista de palabras. La herramienta es rápida y nos proporcionará resultados que nos permitirán saber si las cuentas encontradas son válidas o no, lo cual es un excelente punto de partida para lanzar ataques como la pulverización de contraseñas, que cubriremos en profundidad más adelante en este módulo.

Para comenzar con Kerbrute, podemos descargar [binarios precompilados](https://github.com/ropnop/kerbrute/releases/latest) para la herramienta para realizar pruebas desde Linux, Windows y Mac, o podemos compilarlo nosotros mismos. Esta es generalmente la mejor práctica para cualquier herramienta que introduzcamos en el entorno de un cliente. Para compilar los binarios que usaremos en el sistema que elijamos, primero clonamos el repositorio:

**Clonar el repositorio de Kerbrute**

```sh
sudo git clone https://github.com/ropnop/kerbrute.git
```

Al escribir `make help` nos mostrará las opciones de compilación disponibles.

```shell-session
afsh4ck@kali$ make help

help:            Show this help.
windows:  Make Windows x86 and x64 Binaries
linux:  Make Linux x86 and x64 Binaries
mac:  Make Darwin (Mac) x86 and x64 Binaries
clean:  Delete any binaries
all:  Make Windows, Linux and Mac x86/x64 Binaries
```

Podemos optar por compilar solo un binario o escribir `make all` y compilar uno para usar en sistemas Linux, Windows y Mac (una versión x86 y x64 para cada uno).

**Compilación para múltiples plataformas y arquitecturas**

```shell-session
afsh4ck@kali$ sudo make all

go: downloading github.com/spf13/cobra v1.1.1
go: downloading github.com/op/go-logging v0.0.0-20160315200505-970db520ece7
go: downloading github.com/ropnop/gokrb5/v8 v8.0.0-20201111231119-729746023c02
go: downloading github.com/spf13/pflag v1.0.5
go: downloading github.com/jcmturner/gofork v1.0.0
go: downloading github.com/hashicorp/go-uuid v1.0.2
go: downloading golang.org/x/crypto v0.0.0-20201016220609-9e8e0b390897
go: downloading github.com/jcmturner/rpc/v2 v2.0.2
go: downloading github.com/jcmturner/dnsutils/v2 v2.0.0
go: downloading github.com/jcmturner/aescts/v2 v2.0.0
go: downloading golang.org/x/net v0.0.0-20200114155413-6afb5195e5aa
cd /tmp/kerbrute
rm -f kerbrute kerbrute.exe kerbrute kerbrute.exe kerbrute.test kerbrute.test.exe kerbrute.test kerbrute.test.exe main main.exe
rm -f /root/go/bin/kerbrute
Done.
Building for windows amd64..

<SNIP>
```

El directorio recién creado `dist` contendrá nuestros archivos binarios compilados.

**Listado de los binarios compilados en dist**

```shell-session
afsh4ck@kali$ ls dist/

kerbrute_darwin_amd64  kerbrute_linux_386  kerbrute_linux_amd64  kerbrute_windows_386.exe  kerbrute_windows_amd64.exe
```

Luego podemos probar el binario para asegurarnos de que funciona correctamente. Usaremos la versión x64 en el host de ataque Parrot Linux suministrado en el entorno de destino.

**Probando el binario kerbrute\_linux\_amd64**

```shell-session
afsh4ck@kali$ ./kerbrute_linux_amd64 

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (9cfb81e) - 02/17/22 - Ronnie Flathers @ropnop

This tool is designed to assist in quickly bruteforcing valid Active Directory accounts through Kerberos Pre-Authentication.
It is designed to be used on an internal Windows domain with access to one of the Domain Controllers.
Warning: failed Kerberos Pre-Auth counts as a failed login and WILL lock out accounts

Usage:
  kerbrute [command]
  
  <SNIP>
```

Podemos agregar la herramienta a nuestro PATH para que sea fácilmente accesible desde cualquier lugar del host.

**Agregando la herramienta a nuestro PATH**

```shell-session
afsh4ck@kali$ echo $PATH
/home/htb-student/.local/bin:/snap/bin:/usr/sandbox/:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/usr/share/games:/usr/local/sbin:/usr/sbin:/sbin:/snap/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/home/htb-student/.dotnet/tools
```

**Moviendo el binario**

```shell-session
afsh4ck@kali$ sudo cp kerbrute_linux_amd64 /usr/local/bin/kerbrute
```

Ahora podremos escribir `kerbrute` desde cualquier ubicación del sistema y podremos acceder a la herramienta. Siéntase libre de seguir su sistema y practicar los pasos anteriores. Ahora veamos un ejemplo del uso de la herramienta para recopilar una lista de nombres de usuario inicial.

**Enumerar usuarios con Kerbrute**

```shell-session
afsh4ck@kali$ kerbrute userenum -d INLANEFREIGHT.LOCAL --dc 172.16.5.5 jsmith.txt -o valid_ad_users

2021/11/17 23:01:46 >  Using KDC(s):
2021/11/17 23:01:46 >   172.16.5.5:88
2021/11/17 23:01:46 >  [+] VALID USERNAME:       jjones@INLANEFREIGHT.LOCAL
2021/11/17 23:01:46 >  [+] VALID USERNAME:       sbrown@INLANEFREIGHT.LOCAL
2021/11/17 23:01:46 >  [+] VALID USERNAME:       tjohnson@INLANEFREIGHT.LOCAL
2021/11/17 23:01:50 >  [+] VALID USERNAME:       evalentin@INLANEFREIGHT.LOCAL

 <SNIP>
 
2021/11/17 23:01:51 >  [+] VALID USERNAME:       sgage@INLANEFREIGHT.LOCAL
2021/11/17 23:01:51 >  [+] VALID USERNAME:       jshay@INLANEFREIGHT.LOCAL
2021/11/17 23:01:51 >  [+] VALID USERNAME:       jhermann@INLANEFREIGHT.LOCAL
2021/11/17 23:01:51 >  [+] VALID USERNAME:       whouse@INLANEFREIGHT.LOCAL
2021/11/17 23:01:51 >  [+] VALID USERNAME:       emercer@INLANEFREIGHT.LOCAL
2021/11/17 23:01:52 >  [+] VALID USERNAME:       wshepherd@INLANEFREIGHT.LOCAL
2021/11/17 23:01:56 >  Done! Tested 48705 usernames (56 valid) in 9.940 seconds
```

Podemos ver en nuestro resultado que validamos 56 usuarios en el dominio INLANEFREIGHT.LOCAL y solo nos tomó unos segundos hacerlo. Ahora podemos tomar estos resultados y crear una lista para usar en ataques de pulverización de contraseñas dirigidos.

***

### <mark style="color:purple;">Identificación de posibles vulnerabilidades</mark>

La cuenta [del sistema local](https://docs.microsoft.com/en-us/windows/win32/services/localsystem-account) `NT AUTHORITY\SYSTEM` es una cuenta integrada en los sistemas operativos Windows. Tiene el nivel más alto de acceso en el sistema operativo y se utiliza para ejecutar la mayoría de los servicios de Windows. También es muy común que servicios de terceros se ejecuten en el contexto de esta cuenta de forma predeterminada. Una cuenta  en un host `unido a dominio` podrá enumerar Active Directory haciéndose pasar por la cuenta de la computadora, que es esencialmente otro tipo de cuenta de usuario. Tener acceso a nivel de `SYSTEM` dentro de un entorno de dominio es casi equivalente a tener una cuenta de usuario de dominio.

Hay varias formas de obtener acceso a nivel de `SYSTEM` en un host, incluidas, entre otras:

* Exploits remotos de Windows como MS08-067, EternalBlue o BlueKeep
* Abusar de un servicio que se ejecuta en el contexto de `SYSTEM account`, o abusar de los privilegios `SeImpersonate` de la cuenta de servicio utilizando [Juicy Potato](https://github.com/ohpe/juicy-potato) . Este tipo de ataque es posible en sistemas operativos Windows antiguos, pero no siempre es posible con Windows Server 2019
* Defectos de escalada de privilegios locales en sistemas operativos Windows como el Programador de tareas de Windows 10 de día 0
* Obtener acceso de administrador en un host unido a un dominio con una cuenta local y usar Psexec para iniciar una ventana de cmd de `SYSTEM`

Al obtener acceso a nivel de `SYSTEM` en un host unido a un dominio, podrá realizar acciones como, entre otras:

* Enumerar el dominio utilizando herramientas integradas o herramientas ofensivas como `BloodHound` y `PowerView`
* Realizar ataques `Kerberoasting`/`ASREPRoasting` dentro del mismo dominio
* Ejecutar herramientas como `Inveigh` para recopilar `hashes Net-NTLMv2` o realizar ataques de retransmisión SMB
* Realice una suplantación de tokens para secuestrar una cuenta de usuario de dominio privilegiado.
* Realizar ataques ACL

***

### <mark style="color:purple;">Unas palabras de precaución</mark>

Tenga en cuenta el alcance y el estilo de la prueba al elegir una herramienta para su uso. Si está realizando una prueba de penetración no evasiva, con todo a la vista y el personal del cliente sabiendo que está allí, normalmente no importa cuánto ruido haga. Sin embargo, durante una prueba de penetración evasiva, una evaluación adversaria o un compromiso con el equipo rojo, usted está tratando de imitar las herramientas, tácticas y procedimientos de un atacante potencial.&#x20;

Lanzar Nmap a una red completa no es exactamente silencioso, y muchas de las herramientas que usamos comúnmente en una prueba de penetración activarán alarmas para un SOC o Blue Teamer educado y preparado. Asegúrese siempre de aclarar el objetivo de su evaluación con el cliente por escrito antes de comenzar.

***

### <mark style="color:purple;">Busquemos un usuario</mark>

En las siguientes secciones, buscaremos una cuenta de usuario de dominio utilizando técnicas como el envenenamiento LLMNR/NBT-NS y la pulverización de contraseñas. Estos ataques son excelentes formas de afianzarse, pero deben realizarse con precaución y comprendiendo las herramientas y técnicas. Ahora busquemos una cuenta de usuario para poder pasar a la siguiente fase de nuestra evaluación y comenzar a separar el dominio pieza por pieza y a profundizar en busca de una multitud de configuraciones erróneas y fallas.

***

## <mark style="color:purple;">Caso Práctico</mark>

```
SSH a 10.129.180.102 (ACADEMY-EA-ATTACK01)
Usuario " htb-student "
Contraseña " HTB_@cademy_stdnt! "
```

### Pregunta 1

Según sus escaneos, ¿cuál es el "nombre común" del host `172.16.5.5`?

```shell-session
ssh htb-student@10.129.180.102               
htb-student@10.129.180.102's password: 
Linux ea-attack01 5.15.0-15parrot1-amd64 #1 SMP Debian 5.15.15-15parrot2 (2022-02-15) x86_64
 ____                      _     ____            
|  _ \ __ _ _ __ _ __ ___ | |_  / ___|  ___  ___ 
| |_) / _` | '__| '__/ _ \| __| \___ \ / _ \/ __|
|  __/ (_| | |  | | | (_) | |_   ___) |  __/ (__ 
|_|   \__,_|_|  |_|  \___/ \__| |____/ \___|\___|
                                                 
The programs included with the Parrot GNU/Linux are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Parrot GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Apr  9 18:29:27 2022 from 10.10.14.15
┌─[htb-student@ea-attack01]─[~]
└──╼ $
```

#### Hacemos un fping para comprobar los hosts internos

```
┌─[✗]─[htb-student@ea-attack01]─[~]
└──╼ $fping -asgq 172.16.5.0/23
172.16.5.5
172.16.5.130
172.16.5.225

     510 targets
       3 alive
     507 unreachable
       0 unknown addresses
```

Guardamos estos 3 hosts en un archivo `hosts.txt` para escanearlos con nmap a la vez.

#### Escaneo con Nmap

```
┌─[htb-student@ea-attack01]─[~]
└──╼ $sudo nmap -v -A -iL hosts.txt

Nmap scan report for inlanefreight.local (172.16.5.5)
Host is up (0.0011s latency).
Not shown: 988 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2024-06-25 13:35:07Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: INLANEFREIGHT.LOCAL0., Site: Default-First-Site-Name)
|_ssl-date: 2024-06-25T13:37:00+00:00; 0s from scanner time.
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL, DNS:INLANEFREIGHT.LOCAL, DNS:INLANEFREIGHT
| Issuer: commonName=INLANEFREIGHT-CA
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2023-10-27T13:11:32
| Not valid after:  2024-10-26T13:11:32
| MD5:   31bb 5869 5467 ea6b c85e 8018 7ed8 2c1e
|_SHA-1: 4fc1 ebe6 4995 0e8b 761b 38b5 d411 4162 5690 8d4c
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: INLANEFREIGHT.LOCAL0., Site: Default-First-Site-Name)
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL, DNS:INLANEFREIGHT.LOCAL, DNS:INLANEFREIGHT
| Issuer: commonName=INLANEFREIGHT-CA
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2023-10-27T13:11:32
| Not valid after:  2024-10-26T13:11:32
| MD5:   31bb 5869 5467 ea6b c85e 8018 7ed8 2c1e
|_SHA-1: 4fc1 ebe6 4995 0e8b 761b 38b5 d411 4162 5690 8d4c
|_ssl-date: 2024-06-25T13:37:00+00:00; 0s from scanner time.
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: INLANEFREIGHT.LOCAL0., Site: Default-First-Site-Name)
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL, DNS:INLANEFREIGHT.LOCAL, DNS:INLANEFREIGHT
| Issuer: commonName=INLANEFREIGHT-CA
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2023-10-27T13:11:32
| Not valid after:  2024-10-26T13:11:32
| MD5:   31bb 5869 5467 ea6b c85e 8018 7ed8 2c1e
|_SHA-1: 4fc1 ebe6 4995 0e8b 761b 38b5 d411 4162 5690 8d4c
|_ssl-date: 2024-06-25T13:37:00+00:00; 0s from scanner time.
3269/tcp open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: INLANEFREIGHT.LOCAL0., Site: Default-First-Site-Name)
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL, DNS:INLANEFREIGHT.LOCAL, DNS:INLANEFREIGHT
| Issuer: commonName=INLANEFREIGHT-CA
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2023-10-27T13:11:32
| Not valid after:  2024-10-26T13:11:32
| MD5:   31bb 5869 5467 ea6b c85e 8018 7ed8 2c1e
|_SHA-1: 4fc1 ebe6 4995 0e8b 761b 38b5 d411 4162 5690 8d4c
|_ssl-date: 2024-06-25T13:37:00+00:00; 0s from scanner time.
3389/tcp open  ms-wbt-server Microsoft Terminal Services
|_ssl-date: 2024-06-25T13:37:00+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
| Issuer: commonName=ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2024-06-24T13:17:45
| Not valid after:  2024-12-24T13:17:45
| MD5:   2016 8076 54f1 329d 6263 48c4 149e 1fc1
|_SHA-1: 27fe ce02 b257 1862 0d60 8eb5 17e7 d9c6 eacf 3bf2
| rdp-ntlm-info: 
|   Target_Name: INLANEFREIGHT
|   NetBIOS_Domain_Name: INLANEFREIGHT
|   NetBIOS_Computer_Name: ACADEMY-EA-DC01
|   DNS_Domain_Name: INLANEFREIGHT.LOCAL
|   DNS_Computer_Name: ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
|   Product_Version: 10.0.17763
|_  System_Time: 2024-06-25T13:35:56+00:00

Network Distance: 1 hop
TCP Sequence Prediction: Difficulty=259 (Good luck!)
IP ID Sequence Generation: Incremental
Service Info: Host: ACADEMY-EA-DC01; OS: Windows; CPE: cpe:/o:microsoft:windows
```

El nombre de este host es: `ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL`

### Pregunta 2

¿Qué host ejecuta "Microsoft SQL Server 2019 15.00.2000.00"? (Dirección IP, no nombre resuelto)

```
Nmap scan report for 172.16.5.130
Host is up (0.0015s latency).
Not shown: 992 closed tcp ports (reset)
PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
808/tcp   open  ccproxy-http?
1433/tcp  open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000.00; RTM
| ms-sql-ntlm-info: 
|   Target_Name: INLANEFREIGHT
|   NetBIOS_Domain_Name: INLANEFREIGHT
|   NetBIOS_Computer_Name: ACADEMY-EA-FILE
|   DNS_Domain_Name: INLANEFREIGHT.LOCAL
|   DNS_Computer_Name: ACADEMY-EA-FILE.INLANEFREIGHT.LOCAL
|   DNS_Tree_Name: INLANEFREIGHT.LOCAL
|_  Product_Version: 10.0.17763
```


# Credential Hunting en el tráfico de red

En el mundo actual, preocupado por la seguridad, la mayoría de las aplicaciones utilizan TLS para cifrar datos confidenciales en tránsito. Sin embargo, no todos los entornos son completamente seguros. Los sistemas heredados, los servicios mal configurados o las aplicaciones de prueba iniciadas sin HTTPS pueden dar lugar al uso de protocolos sin cifrar, como HTTP o SNMP. Estas brechas representan una valiosa oportunidad para los atacantes: `la oportunidad de capturar credenciales en plano en el tráfico de red.`

En esta sección, exploraremos técnicas prácticas para identificar información expuesta, como nombres de usuario y contraseñas, dentro de protocolos comunes de texto plano mediante Wireshark. También analizaremos brevemente [Pcredz](https://github.com/lgandx/PCredz) , una herramienta que puede escanear rápidamente el tráfico de red en busca de dichos datos.

La siguiente tabla enumera varios protocolos comunes junto con sus contrapartes cifradas. Si bien ahora es más común encontrar versiones seguras, hubo una época en que los protocolos de texto plano se usaban ampliamente.

<table data-header-hidden><thead><tr><th width="169"></th><th width="190"></th><th></th></tr></thead><tbody><tr><td>Protocolo sin cifrar</td><td>Contraparte cifrada</td><td>Descripción</td></tr><tr><td><code>HTTP</code></td><td><code>HTTPS</code></td><td>Se utiliza para transferir páginas web y recursos a través de Internet.</td></tr><tr><td><code>FTP</code></td><td><code>FTPS/SFTP</code></td><td>Se utiliza para transferir archivos entre un cliente y un servidor.</td></tr><tr><td><code>SNMP</code></td><td><code>SNMPv3 (with encryption)</code></td><td>Se utiliza para supervisar y administrar dispositivos de red como enrutadores y conmutadores.</td></tr><tr><td><code>POP3</code></td><td><code>POP3S</code></td><td>Recupera correos electrónicos de un servidor de correo a un cliente local.</td></tr><tr><td><code>IMAP</code></td><td><code>IMAPS</code></td><td>Accede y administra mensajes de correo electrónico directamente en el servidor de correo.</td></tr><tr><td><code>SMTP</code></td><td><code>SMTPS</code></td><td>Envía mensajes de correo electrónico desde el cliente al servidor o entre servidores de correo.</td></tr><tr><td><code>LDAP</code></td><td><code>LDAPS</code></td><td>Consulta y modifica servicios de directorio como credenciales de usuario y roles.</td></tr><tr><td><code>RDP</code></td><td><code>RDP (with TLS)</code></td><td>Proporciona acceso de escritorio remoto a sistemas Windows.</td></tr><tr><td><code>DNS (Traditional)</code></td><td><code>DNS over HTTPS (DoH)</code></td><td>Resuelve nombres de dominio en direcciones IP.</td></tr><tr><td><code>SMB</code></td><td><code>SMB over TLS (SMB 3.0)</code></td><td>Comparte archivos, impresoras y otros recursos a través de una red.</td></tr><tr><td><code>VNC</code></td><td><code>VNC with TLS/SSL</code></td><td>Permite el control remoto gráfico de otra computadora.</td></tr></tbody></table>

## <mark style="color:purple;">Wireshark</mark>

[Wireshark](https://www.wireshark.org/) es un conocido analizador de paquetes que viene preinstalado en casi todas las distribuciones de Linux para pruebas de penetración. Cuenta con un potente [motor de filtrado](https://www.wireshark.org/docs/man-pages/wireshark-filter.html) que permite una búsqueda eficiente en el tráfico de red, tanto en tiempo real como capturado. Algunos filtros básicos pero útiles incluyen:

<table data-header-hidden><thead><tr><th width="367"></th><th></th></tr></thead><tbody><tr><td>Filtro Wireshark</td><td>Descripción</td></tr><tr><td><code>ip.addr == 56.48.210.13</code></td><td>Filtra paquetes con una dirección IP específica</td></tr><tr><td><code>tcp.port == 80</code></td><td>Filtra paquetes por puerto (HTTP en este caso).</td></tr><tr><td><code>http</code></td><td>Filtros para tráfico HTTP.</td></tr><tr><td><code>dns</code></td><td>Filtra el tráfico DNS, lo que resulta útil para supervisar la resolución de nombres de dominio.</td></tr><tr><td><code>tcp.flags.syn == 1 &#x26;&#x26; tcp.flags.ack == 0</code></td><td>Filtra paquetes SYN (utilizados en protocolos de enlace TCP), útiles para detectar intentos de escaneo o conexión.</td></tr><tr><td><code>icmp</code></td><td>Filtra paquetes ICMP (usados para ping), lo que puede resultar útil para reconocimiento o problemas de red.</td></tr><tr><td><code>http.request.method == "POST"</code></td><td>Filtros para solicitudes HTTP POST. Si las solicitudes POST se envían mediante HTTP sin cifrar, es posible que contengan contraseñas u otra información confidencial.</td></tr><tr><td><code>tcp.stream eq 53</code></td><td>Filtros para un flujo TCP específico. Permite rastrear una conversación entre dos hosts.</td></tr><tr><td><code>eth.addr == 00:11:22:33:44:55</code></td><td>Filtra paquetes desde/hacia una dirección MAC específica.</td></tr><tr><td><code>ip.src == 192.168.24.3 &#x26;&#x26; ip.dst == 56.48.210.3</code></td><td>Filtra el tráfico entre dos direcciones IP específicas. Ayuda a rastrear la comunicación entre hosts específicos.</td></tr></tbody></table>

Por ejemplo, en la imagen a continuación estamos filtrando el tráfico `HTTP` no cifrado.

<figure><img src="/files/k6VPqTqg6zWBU7QySY3u" alt=""><figcaption></figcaption></figure>

En Wireshark, es posible localizar paquetes que contengan bytes o cadenas específicos. Una forma de hacerlo es usar un filtro de visualización como `http contains "passw"`. También podemos ir a `Edit > Find Packet` e introducir manualmente la consulta de búsqueda deseada. Por ejemplo, podríamos buscar paquetes que contengan la cadena `"passw"`:

<figure><img src="/files/1sjSKGZfoLu2nJIatx7L" alt=""><figcaption></figcaption></figure>

Vale la pena familiarizarse con la sintaxis del motor de filtrado de Wireshark, especialmente si alguna vez necesita realizar un análisis del tráfico de red.

***

## <mark style="color:purple;">Pcredz</mark>

{% embed url="<https://github.com/lgandx/PCredz>" %}

Pcredz es una herramienta que permite extraer credenciales del tráfico en tiempo real o de capturas de paquetes de red. En concreto, permite extraer la siguiente información:

* Números de tarjetas de crédito
* Credenciales POP
* Credenciales SMTP
* Credenciales IMAP
* SNMP community strings
* Credenciales FTP
* Credenciales de encabezados HTTP NTLM/Basic, así como formularios HTTP
* Hashes NTLMv1/v2 de varios tipos de tráfico, incluidos DCE-RPC, SMBv1/2, LDAP, MSSQL y HTTP
* Hashes Kerberos (AS-REQ Pre-Auth etype 23)

Para ejecutar `Pcredz`, se puede clonar el repositorio e instalar todas las dependencias o utilizar el contenedor Docker proporcionado que se detalla en la parte [de instalación](https://github.com/lgandx/PCredz?tab=readme-ov-file#install) del archivo README.

El siguiente comando se puede utilizar para ejecutar `Pcredz` sobre un archivo de captura de paquetes:

```shell-session
afsh4ck@kali$ ./Pcredz -f demo.pcapng -t -v

Pcredz 2.0.2
Author: Laurent Gaffie
Please send bugs/comments/pcaps to: laurent.gaffie@gmail.com
This script will extract NTLM (HTTP,LDAP,SMB,MSSQL,RPC, etc), Kerberos,
FTP, HTTP Basic and credit card data from a given pcap file or from a live interface.

CC number scanning activated

Unknown format, trying TCPDump format

[1746131482.601354] protocol: udp 192.168.31.211:59022 > 192.168.31.238:161
Found SNMPv2 Community string: s3cr...SNIP...

[1746131482.601640] protocol: udp 192.168.31.211:59022 > 192.168.31.238:161
Found SNMPv2 Community string: s3cr...SNIP...

<SNIP>

[1746131482.658938] protocol: tcp 192.168.31.243:55707 > 192.168.31.211:21
FTP User: le...SNIP...
FTP Pass: qw...SNIP...

demo.pcapng parsed in: 1.82 seconds (File size 15.5 Mo).
```

***

## <mark style="color:purple;">Caso práctico</mark>

Descarga el archivo adjunto `credential-hunting-in-network-traffic` y extrae el archivo `demo.pcapng`, luego utiliza Wireshark o PCredz para responder las siguientes preguntas.

{% file src="/files/ASo4IUz90b6PfrC7kESg" %}

### Pregunta 1

> La captura de paquetes contiene información de tarjeta de crédito en texto plano. ¿Cuál es el número transmitido?

Al filtrar por tráfico http observamos un request POST a /process\_payment sospechoso. Al ver los datos que se envían vemos todos los datos de la tarjeta de crédito:

<figure><img src="/files/1e9dUAyVevqZ9lqUiSf4" alt=""><figcaption></figcaption></figure>

### Pregunta 2

> ¿Cuál es la cadena de comunidad SNMPv2 que se utilizó?

Para esta pregunta usaremos Pcredz, por lo que lo instalaremos en nuestro Kali:

```bash
git clone https://github.com/lgandx/PCredz.git
cd PCredz
sudo apt install python3-pip && sudo apt-get install libpcap-dev && pip3 install Cython && pip3 install python-libpcap  
```

```bash
./Pcredz -f ../demo.pcapng -t -v
                                                                                  
Pcredz 2.0.2

Author: Laurent Gaffie <lgaffie@secorizon.com>

This script will extract NTLM (HTTP,LDAP,SMB,MSSQL,RPC, etc), Kerberos,
FTP, HTTP Basic and credit card data from a given pcap file or from a live interface.

CC number scanning activated

Unknown format, trying TCPDump format

[1753297429.914309] protocol: udp 192.168.31.211:59022 > 192.168.31.238:161
Found SNMPv2 Community string: s3cr3tSNMPC0mmun1ty

[1753297429.964927] protocol: tcp 192.168.31.243:55707 > 192.168.31.211:21
FTP User: leah
FTP Pass: qwerty123
```

### Pregunta 3

> ¿Cuál es la contraseña del usuario que inició sesión en FTP?

Cómo observamos en la imagen anterior, Pcredz encontró un usuario y contraseña de FTP:

```
FTP User: leah
FTP Pass: qwerty123
```

### Pregunta 4

> ¿Qué archivo descargó el usuario mediante FTP?

Filtrando por `ftp` en Wireshark encontramos el archivo `creds.txt` que se descargó el usuario `leah`:

<figure><img src="/files/RZRPirO0tgsQHjabXtHn" alt=""><figcaption></figcaption></figure>

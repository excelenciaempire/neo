
# DNS

Por ejemplo, a través de nombres de dominio, como `academy.hackthebox.com` o `hackthebox.com` , podemos llegar a los servidores web a los que el proveedor de hosting tiene asignadas una o más direcciones IP específicas. DNS es un sistema para resolver nombres de computadoras en direcciones IP y no tiene una base de datos central.&#x20;

Simplificado, podemos imaginarlo como una biblioteca con muchas guías telefónicas diferentes. La información se distribuye entre miles de servidores de nombres. Los servidores DNS distribuidos globalmente traducen los nombres de dominio en direcciones IP y controlan así a qué servidor puede acceder un usuario a través de un dominio en particular. Existen varios tipos de servidores DNS que se utilizan en todo el mundo:

El DNS prácticamente no está cifrado. De este modo, los dispositivos conectados a la WLAN local y a los proveedores de Internet pueden piratear y espiar las consultas DNS. Dado que esto supone un riesgo para la privacidad, ahora existen algunas soluciones para el cifrado DNS. De forma predeterminada, los profesionales de seguridad de TI aplican `DNS over TLS`( `DoT`) o `DNS over HTTPS`( `DoH`) aquí. Además, el protocolo de red `DNSCrypt`también cifra el tráfico entre la computadora y el servidor de nombres.

Sin embargo, el DNS no sólo vincula nombres de computadoras y direcciones IP. También almacena y genera información adicional sobre los servicios asociados con un dominio. Por lo tanto, mediante una consulta DNS también se puede determinar, por ejemplo, qué ordenador sirve como servidor de correo electrónico para el dominio en cuestión o cómo se llaman los servidores de nombres del dominio.

![](https://academy.hackthebox.com/storage/modules/27/tooldev-dns.png)

***

## <mark style="color:purple;">Conceptos clave de DNS</mark>

En `Domain Name System`( `DNS`), una `zona` es una parte distinta del espacio de nombres de dominio que administra una entidad o administrador específico. Piense en ello como un contenedor virtual para un conjunto de nombres de dominio. Por ejemplo, `example.com` todos sus subdominios (como `mail.example.com` o `blog.example.com`) normalmente pertenecerían a la misma zona DNS.

El archivo de zona, un archivo de texto que reside en un servidor DNS, define los registros de recursos (que se analizan a continuación) dentro de esta zona, proporcionando información crucial para traducir nombres de dominio en direcciones IP.

Para ilustrar, aquí hay un ejemplo simplificado de cómo `example.com` se vería un archivo de zona:

```dns-zone
$TTL 3600 ; Default Time-To-Live (1 hour)
@       IN SOA   ns1.example.com. admin.example.com. (
                2024060401 ; Serial number (YYYYMMDDNN)
                3600       ; Refresh interval
                900        ; Retry interval
                604800     ; Expire time
                86400 )    ; Minimum TTL

@       IN NS    ns1.example.com.
@       IN NS    ns2.example.com.
@       IN MX 10 mail.example.com.
www     IN A     192.0.2.1
mail    IN A     198.51.100.1
ftp     IN CNAME www.example.com.
```

Este archivo define los servidores de nombres autorizados (registros `NS`), el servidor de correo (registro `MX`) y las direcciones IP (registros `A`) para varios hosts dentro del dominio `example.com`.

Los servidores DNS almacenan varios registros de recursos, cada uno de los cuales tiene un propósito específico en el proceso de resolución de nombres de dominio. Exploremos algunos de los conceptos de DNS más comunes:

<table data-header-hidden><thead><tr><th width="204"></th><th></th><th></th></tr></thead><tbody><tr><td>Concepto DNS</td><td>Descripción</td><td>Ejemplo</td></tr><tr><td><code>Domain Name</code></td><td>Una etiqueta legible por humanos para un sitio web u otro recurso de Internet.</td><td><code>www.example.com</code></td></tr><tr><td><code>IP Address</code></td><td>Un identificador numérico único asignado a cada dispositivo conectado a Internet.</td><td><code>192.0.2.1</code></td></tr><tr><td><code>DNS Resolver</code></td><td>Un servidor que traduce nombres de dominio en direcciones IP.</td><td>El servidor DNS de su ISP o Public Resolvers como Google DNS ( <code>8.8.8.8</code>)</td></tr><tr><td><code>Root Name Server</code></td><td>Los servidores de nivel superior en la jerarquía DNS.</td><td>Hay 13 servidores raíz en todo el mundo, denominados AM:<code>a.root-servers.net</code></td></tr><tr><td><code>TLD Name Server</code></td><td>Servidores responsables de dominios de nivel superior específicos (por ejemplo, .com, .org).</td><td><a href="https://en.wikipedia.org/wiki/Verisign">Verisign</a> para <code>.com</code>, <a href="https://en.wikipedia.org/wiki/Public_Interest_Registry">PIR</a> para<code>.org</code></td></tr><tr><td><code>Authoritative Name Server</code></td><td>El servidor que contiene la dirección IP real de un dominio.</td><td>A menudo lo gestionan proveedores de alojamiento o registradores de dominios.</td></tr><tr><td><code>DNS Record Types</code></td><td>Diferentes tipos de información almacenada en DNS.</td><td>A, AAAA, CNAME, MX, NS, TXT, etc.</td></tr></tbody></table>

Ahora que hemos explorado los conceptos fundamentales de DNS, profundicemos en los componentes básicos de la información de DNS: los distintos tipos de registros. Estos registros almacenan diferentes tipos de datos asociados con los nombres de dominio, cada uno de los cuales tiene un propósito específico:

<table data-header-hidden><thead><tr><th width="107"></th><th width="151"></th><th></th><th></th></tr></thead><tbody><tr><td>Tipo de registro</td><td>Nombre completo</td><td>Descripción</td><td>Ejemplo de archivo de zona</td></tr><tr><td><code>A</code></td><td>Registro de dirección</td><td>Asigna un nombre de host a su dirección IPv4.</td><td><code>www.example.com.</code>EN UN<code>192.0.2.1</code></td></tr><tr><td><code>AAAA</code></td><td>Registro de direcciones IPv6</td><td>Asigna un nombre de host a su dirección IPv6.</td><td><code>www.example.com.</code>EN AAAA<code>2001:db8:85a3::8a2e:370:7334</code></td></tr><tr><td><code>CNAME</code></td><td>Registro de nombre canónico</td><td>Crea un alias para un nombre de host, apuntándolo a otro nombre de host.</td><td><code>blog.example.com.</code>EN NOMBRE<code>webserver.example.net.</code></td></tr><tr><td><code>MX</code></td><td>Registro de intercambio de correo</td><td>Especifica los servidores de correo responsables de manejar el correo electrónico del dominio.</td><td><code>example.com.</code>EN MX 10<code>mail.example.com.</code></td></tr><tr><td><code>NS</code></td><td>Registro del servidor de nombres</td><td>Delega una zona DNS a un servidor de nombres autorizado específico.</td><td><code>example.com.</code>EN NS<code>ns1.example.com.</code></td></tr><tr><td><code>TXT</code></td><td>Registro de texto</td><td>Almacena información de texto arbitraria, que a menudo se utiliza para la verificación de dominios o políticas de seguridad.</td><td><code>example.com.</code>EN TXT <code>"v=spf1 mx -all"</code>(registro SPF)</td></tr><tr><td><code>SOA</code></td><td>Inicio del Registro de Autoridad</td><td>Especifica información administrativa sobre una zona DNS, incluido el servidor de nombres principal, el correo electrónico de la persona responsable y otros parámetros.</td><td><code>example.com.</code>EN SOA<code>ns1.example.com. admin.example.com. 2024060301 10800 3600 604800 86400</code></td></tr><tr><td><code>SRV</code></td><td>Registro de servicio</td><td>Define el nombre de host y el número de puerto para servicios específicos.</td><td><code>_sip._udp.example.com.</code>EN SRV 10 5 5060<code>sipserver.example.com.</code></td></tr><tr><td><code>PTR</code></td><td>Registro de puntero</td><td>Se utiliza para búsquedas de DNS inversas, asignando una dirección IP a un nombre de host.</td><td><code>1.2.0.192.in-addr.arpa.</code>EN PTR<code>www.example.com.</code></td></tr></tbody></table>

" `IN`" en los ejemplos significa "Internet". Es un campo de clase en los registros DNS que especifica la familia de protocolos. En la mayoría de los casos, verá " `IN`" usado, ya que indica el conjunto de protocolos de Internet (IP) utilizado para la mayoría de los nombres de dominio. Existen otros valores de clase (por ejemplo, `CH` para Chaosnet, `HS` para Hesiod) pero rara vez se utilizan en configuraciones DNS modernas.

En esencia, " `IN`" es simplemente una convención que indica que el registro se aplica a los protocolos de Internet estándar que utilizamos hoy en día. Si bien puede parecer un detalle adicional, comprender su significado proporciona una comprensión más profunda de la estructura de los registros DNS.

El registro `SOA` se encuentra en el archivo de zona de un dominio y especifica quién es responsable del funcionamiento del dominio y cómo se administra la información DNS del dominio.

```bash
afsh4ck$ dig soa www.inlanefreight.com

; <<>> DiG 9.16.27-Debian <<>> soa www.inlanefreight.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 15876
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;www.inlanefreight.com.         IN      SOA

;; AUTHORITY SECTION:
inlanefreight.com.      900     IN      SOA     ns-161.awsdns-20.com. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400

;; Query time: 16 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Thu Jan 05 12:56:10 GMT 2023
;; MSG SIZE  rcvd: 128
```

El punto (.) se reemplaza por una arroba (@) en la dirección de correo electrónico. En este ejemplo, la dirección de correo electrónico del administrador es `awsdns-hostmaster@amazon.com`.

***

## <mark style="color:purple;">Cheatsheet</mark>

| **Comando**                                                                                                   | **Descripción**                                        |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `dig ns <domain.tld> @<nameserver>`                                                                           | Solicitud NS al servidor de nombres específico.        |
| `dig any <domain.tld> @<nameserver>`                                                                          | CUALQUIER solicitud al servidor de nombres específico. |
| `dig axfr <domain.tld> @<nameserver>`                                                                         | Solicitud AXFR al servidor de nombres específico.      |
| `dnsenum --dnsserver <nameserver> --enum -p 0 -s 0 -o found_subdomains.txt -f ~/subdomains.list <domain.tld>` | Fuerza bruta de subdominio.                            |

## <mark style="color:purple;">Configuración predeterminada</mark>

Existen muchos tipos diferentes de configuración para DNS. Por lo tanto, sólo discutiremos los más importantes para ilustrar mejor el principio funcional desde un punto de vista administrativo. Todos los servidores DNS funcionan con tres tipos diferentes de archivos de configuración:

1. `Archivos de configuración DNS locales`
2. `Archivos de zona`
3. `Archivos de resolución de nombres inversos`

El servidor DNS [Bind9](https://www.isc.org/bind/) se utiliza con mucha frecuencia en distribuciones basadas en Linux. Su archivo de configuración local ( `named.conf`) está dividido aproximadamente en dos secciones: en primer lugar, la sección de opciones para la configuración general y, en segundo lugar, las entradas de zona para los dominios individuales. Los archivos de configuración locales suelen ser:

* `named.conf.local`
* `named.conf.options`
* `named.conf.log`

Contiene el RFC asociado donde podemos personalizar el servidor según nuestras necesidades y nuestra estructura de dominio con las zonas individuales para diferentes dominios. El archivo de configuración `named.conf`se divide en varias opciones que controlan el comportamiento del servidor de nombres. Se hace una distinción entre `global options`y `zone options`.

Las opciones globales son generales y afectan a todas las zonas. Una opción de zona sólo afecta a la zona a la que está asignada. Las opciones que no aparecen en nombrado.conf tienen valores predeterminados. Si una opción es global y específica de una zona, entonces la opción de zona tiene prioridad.

### **Configuración DNS local**

```shell-session
root@bind9:~# cat /etc/bind/named.conf.local

//
// Do any local configuration here
//

// Consider adding the 1918 zones here, if they are not used in your
// organization
//include "/etc/bind/zones.rfc1918";
zone "domain.com" {
    type master;
    file "/etc/bind/db.domain.com";
    allow-update { key rndc-key; };
};
```

En este archivo podemos definir las diferentes zonas. Estas zonas se dividen en archivos individuales, que en la mayoría de los casos están destinados principalmente a un solo dominio. Las excepciones son los ISP y los servidores DNS públicos. Además, muchas opciones diferentes amplían o reducen la funcionalidad. Podemos buscarlos en la [documentación](https://wiki.debian.org/Bind9) de Bind9.

El `archivo de zona` es un archivo de texto que describe una zona DNS con el formato de archivo BIND. En otras palabras, es un punto de delegación en el árbol DNS. El formato de archivo BIND es el formato de archivo de zona preferido en la industria y ahora está bien establecido en el software de servidor DNS. Un archivo de zona describe una zona completamente. Debe haber precisamente un registro `SOA` y al menos un registro `NS`. El registro de recursos SOA normalmente se encuentra al principio de un archivo de zona. El objetivo principal de estas reglas globales es mejorar la legibilidad de los archivos de zona. Un error de sintaxis normalmente hace que todo el archivo de zona se considere inutilizable. El servidor de nombres se comporta de manera similar como si esta zona no existiera. Responde a consultas de DNS con un mensaje de error `SERVFAIL`.

En resumen, aquí todos `forward records` se introducen según el formato BIND. Esto permite que el servidor DNS identifique a qué dominio, nombre de host y función pertenecen las direcciones IP. En términos simples, esta es la guía telefónica donde el servidor DNS busca las direcciones de los dominios que está buscando.

### **Archivos de zona**

```shell-session
root@bind9:~# cat /etc/bind/db.domain.com

;
; BIND reverse data file for local loopback interface
;
$ORIGIN domain.com
$TTL 86400
@     IN     SOA    dns1.domain.com.     hostmaster.domain.com. (
                    2001062501 ; serial
                    21600      ; refresh after 6 hours
                    3600       ; retry after 1 hour
                    604800     ; expire after 1 week
                    86400 )    ; minimum TTL of 1 day

      IN     NS     ns1.domain.com.
      IN     NS     ns2.domain.com.

      IN     MX     10     mx.domain.com.
      IN     MX     20     mx2.domain.com.

             IN     A       10.129.14.5

server1      IN     A       10.129.14.5
server2      IN     A       10.129.14.7
ns1          IN     A       10.129.14.2
ns2          IN     A       10.129.14.3

ftp          IN     CNAME   server1
mx           IN     CNAME   server1
mx2          IN     CNAME   server2
www          IN     CNAME   server2
```

Para que la dirección IP se resuelva desde `Fully Qualified Domain Name`( `FQDN`), el servidor DNS debe tener un archivo de búsqueda inversa. En este archivo, el nombre de la computadora (FQDN) se asigna al último octeto de una dirección IP, que corresponde al host respectivo, mediante un registro `PTR`. Los registros PTR se encargan de la traducción inversa de direcciones IP a nombres, como ya hemos visto en la tabla anterior.

### **Archivos de zona de resolución de nombre inverso**

```shell-session
root@bind9:~# cat /etc/bind/db.10.129.14

;
; BIND reverse data file for local loopback interface
;
$ORIGIN 14.129.10.in-addr.arpa
$TTL 86400
@     IN     SOA    dns1.domain.com.     hostmaster.domain.com. (
                    2001062501 ; serial
                    21600      ; refresh after 6 hours
                    3600       ; retry after 1 hour
                    604800     ; expire after 1 week
                    86400 )    ; minimum TTL of 1 day

      IN     NS     ns1.domain.com.
      IN     NS     ns2.domain.com.

5    IN     PTR    server1.domain.com.
7    IN     MX     mx.domain.com.
...SNIP...
```

***

## <mark style="color:purple;">Configuraciones peligrosas</mark>

Hay muchas formas en que se puede atacar un servidor DNS. Por ejemplo, puede encontrar una lista de vulnerabilidades dirigidas al servidor BIND9 en [CVEdetails](https://www.cvedetails.com/product/144/ISC-Bind.html?vendor_id=64) . Además, SecurityTrails proporciona una breve [lista](https://securitytrails.com/blog/most-popular-types-dns-attacks) de los ataques más populares a servidores DNS.

Algunas de las configuraciones que podemos ver a continuación conducen a estas vulnerabilidades, entre otras. Porque el DNS puede volverse muy complicado y es muy fácil que se cuelen errores en este servicio, obligando a un administrador a trabajar alrededor del problema hasta encontrar una solución exacta. Esto a menudo conduce a que se liberen elementos para que partes de la infraestructura funcionen según lo planeado y deseado. En tales casos, la funcionalidad tiene mayor prioridad que la seguridad, lo que genera errores de configuración y vulnerabilidades.

<table data-header-hidden><thead><tr><th width="216"></th><th></th></tr></thead><tbody><tr><td><strong>Opción</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>allow-query</code></td><td>Define qué hosts pueden enviar solicitudes al servidor DNS.</td></tr><tr><td><code>allow-recursion</code></td><td>Define qué hosts pueden enviar solicitudes recursivas al servidor DNS.</td></tr><tr><td><code>allow-transfer</code></td><td>Define qué hosts pueden recibir transferencias de zona desde el servidor DNS.</td></tr><tr><td><code>zone-statistics</code></td><td>Recoge datos estadísticos de zonas.</td></tr></tbody></table>

***

## <mark style="color:purple;">Enumeración del servicio</mark>

La enumeración en los servidores DNS se realiza como resultado de las solicitudes que enviamos. Así, en primer lugar, se puede consultar al servidor DNS qué otros servidores de nombres se conocen. Hacemos esto usando el registro NS y la especificación del servidor DNS que queremos consultar usando el carácter `@`. Esto se debe a que si existen otros servidores DNS, también podremos utilizarlos y consultar los registros. Sin embargo, otros servidores DNS pueden configurarse de manera diferente y, además, pueden ser permanentes para otras zonas.

### **DIG - Consulta NS**

```bash
afsh4ck$ dig ns inlanefreight.htb @10.129.14.128

; <<>> DiG 9.16.1-Ubuntu <<>> ns inlanefreight.htb @10.129.14.128
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 45010
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 2

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: ce4d8681b32abaea0100000061475f73842c401c391690c7 (good)
;; QUESTION SECTION:
;inlanefreight.htb.             IN      NS

;; ANSWER SECTION:
inlanefreight.htb.      604800  IN      NS      ns.inlanefreight.htb.

;; ADDITIONAL SECTION:
ns.inlanefreight.htb.   604800  IN      A       10.129.34.136

;; Query time: 0 msec
;; SERVER: 10.129.14.128#53(10.129.14.128)
;; WHEN: So Sep 19 18:04:03 CEST 2021
;; MSG SIZE  rcvd: 107
```

A veces también es posible consultar la versión de un servidor DNS usando una consulta de clase CHAOS y escribiendo TXT. Sin embargo, esta entrada debe existir en el servidor DNS. Para esto podríamos usar el siguiente comando:

### **DIG - Consulta de versión**

```bash
afsh4ck$ dig CH TXT version.bind 10.129.120.85

; <<>> DiG 9.10.6 <<>> CH TXT version.bind
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 47786
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; ANSWER SECTION:
version.bind.       0       CH      TXT     "9.10.6-P1"

;; ADDITIONAL SECTION:
version.bind.       0       CH      TXT     "9.10.6-P1-Debian"

;; Query time: 2 msec
;; SERVER: 10.129.120.85#53(10.129.120.85)
;; WHEN: Wed Jan 05 20:23:14 UTC 2023
;; MSG SIZE  rcvd: 101
```

Podemos utilizar la opción `ANY` para ver todos los registros disponibles. Esto hará que el servidor nos muestre todas las entradas disponibles que está dispuesto a revelar. Es importante tener en cuenta que no se mostrarán todas las entradas de las zonas.

### **DIG - Cualquier consulta**

```bash
afsh4ck$ dig any inlanefreight.htb @10.129.14.128

; <<>> DiG 9.16.1-Ubuntu <<>> any inlanefreight.htb @10.129.14.128
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7649
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 2

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 064b7e1f091b95120100000061476865a6026d01f87d10ca (good)
;; QUESTION SECTION:
;inlanefreight.htb.             IN      ANY

;; ANSWER SECTION:
inlanefreight.htb.      604800  IN      TXT     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.124.8 ip4:10.129.127.2 ip4:10.129.42.106 ~all"
inlanefreight.htb.      604800  IN      TXT     "atlassian-domain-verification=t1rKCy68JFszSdCKVpw64A1QksWdXuYFUeSXKU"
inlanefreight.htb.      604800  IN      TXT     "MS=ms97310371"
inlanefreight.htb.      604800  IN      SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
inlanefreight.htb.      604800  IN      NS      ns.inlanefreight.htb.

;; ADDITIONAL SECTION:
ns.inlanefreight.htb.   604800  IN      A       10.129.34.136

;; Query time: 0 msec
;; SERVER: 10.129.14.128#53(10.129.14.128)
;; WHEN: So Sep 19 18:42:13 CEST 2021
;; MSG SIZE  rcvd: 437
```

### Transferencia de zona

`Zone transfer` se refiere a la transferencia de zonas a otro servidor en DNS, que generalmente ocurre a través del puerto TCP 53. Este procedimiento se abrevia `Asynchronous Full Transfer Zone`( `AXFR`). Dado que un fallo de DNS suele tener graves consecuencias para una empresa, el archivo de zona casi siempre se mantiene idéntico en varios servidores de nombres. Cuando se realizan cambios, se debe garantizar que todos los servidores tengan los mismos datos. La sincronización entre los servidores involucrados se realiza mediante transferencia de zona. Utilizando una clave secreta `rndc-key`, que hemos visto inicialmente en la configuración por defecto, los servidores se aseguran de comunicarse con su propio maestro o esclavo. La transferencia de zona implica la mera transferencia de archivos o registros y la detección de discrepancias en los conjuntos de datos de los servidores involucrados.

Los datos originales de una zona se encuentran en un servidor DNS, que se denomina `primary`servidor de nombres para esta zona. Sin embargo, para aumentar la fiabilidad, realizar una distribución sencilla de la carga o proteger el primario de ataques, en la práctica se instalan en la práctica en casi todos los casos uno o varios servidores adicionales, que se denominan `secondary`servidores de nombres para esta zona. Para algunos `Top-Level Domains`( `TLDs`), es obligatorio hacer que los archivos de zona sean `Second Level Domains`accesibles en al menos dos servidores.

Las entradas DNS generalmente solo se crean, modifican o eliminan en el principal. Esto se puede hacer editando manualmente el archivo de zona relevante o automáticamente mediante una actualización dinámica desde una base de datos. Un servidor DNS que sirve como fuente directa para sincronizar un archivo de zona se llama maestro. Un servidor DNS que obtiene datos de zona de un maestro se llama esclavo. Un primario es siempre un maestro, mientras que un secundario puede ser tanto esclavo como maestro.

El esclavo obtiene el registro `SOA` de la zona relevante del maestro en ciertos intervalos, el llamado tiempo de actualización, generalmente una hora, y compara los números de serie. Si el número de serie del registro SOA del maestro es mayor que el del esclavo, los conjuntos de datos ya no coinciden.

### **DIG - Transferencia de zona AXFR**

```bash
afsh4ck$ dig axfr inlanefreight.htb @10.129.14.128

; <<>> DiG 9.16.1-Ubuntu <<>> axfr inlanefreight.htb @10.129.14.128
;; global options: +cmd
inlanefreight.htb.      604800  IN      SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
inlanefreight.htb.      604800  IN      TXT     "MS=ms97310371"
inlanefreight.htb.      604800  IN      TXT     "atlassian-domain-verification=t1rKCy68JFszSdCKVpw64A1QksWdXuYFUeSXKU"
inlanefreight.htb.      604800  IN      TXT     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.124.8 ip4:10.129.127.2 ip4:10.129.42.106 ~all"
inlanefreight.htb.      604800  IN      NS      ns.inlanefreight.htb.
app.inlanefreight.htb.  604800  IN      A       10.129.18.15
internal.inlanefreight.htb. 604800 IN   A       10.129.1.6
mail1.inlanefreight.htb. 604800 IN      A       10.129.18.201
ns.inlanefreight.htb.   604800  IN      A       10.129.34.136
inlanefreight.htb.      604800  IN      SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
;; Query time: 4 msec
;; SERVER: 10.129.14.128#53(10.129.14.128)
;; WHEN: So Sep 19 18:51:19 CEST 2021
;; XFR size: 9 records (messages 1, bytes 520)
```

Si el administrador usara una subred para la opción `allow-transfer` con fines de prueba o como solución alternativa o la configurara en `any`, todos consultarían el archivo de zona completo en el servidor DNS. Además, se pueden consultar otras zonas, que pueden incluso mostrar direcciones IP internas y nombres de host.

### **DIG - Transferencia de zona AXFR - Interna**

```bash
afsh4ck$ dig axfr internal.inlanefreight.htb @10.129.14.128

; <<>> DiG 9.16.1-Ubuntu <<>> axfr internal.inlanefreight.htb @10.129.14.128
;; global options: +cmd
internal.inlanefreight.htb. 604800 IN   SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
internal.inlanefreight.htb. 604800 IN   TXT     "MS=ms97310371"
internal.inlanefreight.htb. 604800 IN   TXT     "atlassian-domain-verification=t1rKCy68JFszSdCKVpw64A1QksWdXuYFUeSXKU"
internal.inlanefreight.htb. 604800 IN   TXT     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.124.8 ip4:10.129.127.2 ip4:10.129.42.106 ~all"
internal.inlanefreight.htb. 604800 IN   NS      ns.inlanefreight.htb.
dc1.internal.inlanefreight.htb. 604800 IN A     10.129.34.16
dc2.internal.inlanefreight.htb. 604800 IN A     10.129.34.11
mail1.internal.inlanefreight.htb. 604800 IN A   10.129.18.200
ns.internal.inlanefreight.htb. 604800 IN A      10.129.34.136
vpn.internal.inlanefreight.htb. 604800 IN A     10.129.1.6
ws1.internal.inlanefreight.htb. 604800 IN A     10.129.1.34
ws2.internal.inlanefreight.htb. 604800 IN A     10.129.1.35
wsus.internal.inlanefreight.htb. 604800 IN A    10.129.18.2
internal.inlanefreight.htb. 604800 IN   SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
;; Query time: 0 msec
;; SERVER: 10.129.14.128#53(10.129.14.128)
;; WHEN: So Sep 19 18:53:11 CEST 2021
;; XFR size: 15 records (messages 1, bytes 664)
```

Los registros individuales `A` con los nombres de host también se pueden descubrir mediante un ataque de fuerza bruta. Para hacer esto, necesitamos una lista de posibles nombres de host, que usamos para enviar las solicitudes en orden. Estas listas las proporciona, por ejemplo, [SecLists](https://github.com/danielmiessler/SecLists/blob/master/Discovery/DNS/subdomains-top1million-5000.txt) .

Una opción sería ejecutar un `for-loop` en bash que enumere estas entradas y envíe la consulta correspondiente al servidor DNS deseado.

### **Fuerza bruta de subdominios**

{% code overflow="wrap" %}

```bash
afsh4ck$ for sub in $(cat /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-110000.txt);do dig $sub.inlanefreight.htb @10.129.14.128 | grep -v ';\|SOA' | sed -r '/^\s*$/d' | grep $sub | tee -a subdomains.txt;done

ns.inlanefreight.htb.   604800  IN      A       10.129.34.136
mail1.inlanefreight.htb. 604800 IN      A       10.129.18.201
app.inlanefreight.htb.  604800  IN      A       10.129.18.15
```

{% endcode %}

Se pueden utilizar muchas herramientas diferentes para esto y la mayoría funcionan de la misma manera. Una de estas herramientas es, por ejemplo, [DNSenum](https://github.com/fwaeytens/dnsenum) .

### DNSenum

{% code overflow="wrap" %}

```bash
dnsenum --dnsserver 10.129.14.128 --enum -p 0 -s 0 -o subdomains.txt -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt inlanefreight.htb

dnsenum VERSION:1.2.6

-----   inlanefreight.htb   -----

Host's addresses:
__________________

Name Servers:
______________

ns.inlanefreight.htb.                    604800   IN    A        10.129.34.136

Mail (MX) Servers:
___________________

Trying Zone Transfers and getting Bind Versions:
_________________________________________________

unresolvable name: ns.inlanefreight.htb at /usr/bin/dnsenum line 900 thread 1.

Trying Zone Transfer for inlanefreight.htb on ns.inlanefreight.htb ...
AXFR record query failed: no nameservers

Brute forcing with /home/cry0l1t3/Pentesting/SecLists/Discovery/DNS/subdomains-top1million-110000.txt:
____________________________________________________________________________________

ns.inlanefreight.htb.                    604800   IN    A        10.129.34.136
mail1.inlanefreight.htb.                 604800   IN    A        10.129.18.201
app.inlanefreight.htb.                   604800   IN    A        10.129.18.15
ns.inlanefreight.htb.                    604800   IN    A        10.129.34.136

...SNIP...
done.
```

{% endcode %}

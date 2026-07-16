
# Ataques a DNS

El [Domain Name System](https://www.cloudflare.com/learning/dns/what-is-dns/) (`DNS`) traduce los nombres de dominio (por ejemplo, google.com) a direcciones IP numéricas (por ejemplo, 104.17.42.72). DNS siempre ha sido diseñado para usar el puerto `53 UDP` y TCP desde el principio, siendo UDP el predeterminado, y recurre a TCP cuando no puede comunicarse en UDP, generalmente cuando el tamaño del paquete es demasiado grande para enviarlo en un solo Paquete UDP. Dado que casi todas las aplicaciones de red utilizan DNS, los ataques contra servidores DNS representan una de las amenazas más frecuentes e importantes en la actualidad.

***

## <mark style="color:purple;">Enumeración</mark>

DNS contiene información interesante para una organización. Como se analiza en la sección Información de dominio en el módulo [Enumeración](/ethical-hacking-cheatsheet/recopilacion-de-informacion/enumeracion.md), podemos comprender cómo opera una empresa y los servicios que brinda, así como proveedores de servicios externos, como correos electrónicos.

Las opciones de Nmap `-sC` (scripts predeterminados) y `-sV` (escaneo de versiones) se pueden usar para realizar la enumeración inicial en los servidores DNS de destino:

```shell-session
afsh4ck@kali# nmap -p53 -Pn -sV -sC 10.10.110.213

Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-29 03:47 EDT
Nmap scan report for 10.10.110.213
Host is up (0.017s latency).

PORT    STATE  SERVICE     VERSION
53/tcp  open   domain      ISC BIND 9.11.3-1ubuntu1.2 (Ubuntu Linux)
```

***

## <mark style="color:purple;">Transferencia de zona DNS</mark>

Una zona DNS es una parte del espacio de nombres DNS que administra una organización o administrador específico. Dado que DNS comprende múltiples zonas DNS, los servidores DNS utilizan transferencias de zonas DNS para copiar una parte de su base de datos a otro servidor DNS. A menos que un servidor DNS esté configurado correctamente (lo que limita qué IP pueden realizar una transferencia de zona DNS), cualquiera puede solicitarle a un servidor DNS una copia de la información de su zona, ya que las transferencias de zona DNS no requieren ninguna autenticación. Además, el servicio DNS suele ejecutarse en un puerto UDP; sin embargo, al realizar la transferencia de zona DNS, utiliza un puerto TCP para una transmisión de datos confiable.

Un atacante podría aprovechar esta vulnerabilidad de transferencia de zona DNS para obtener más información sobre el espacio de nombres DNS de la organización objetivo, aumentando la superficie de ataque. Para explotarlo, podemos usar la utilidad `dig` con la opción de tipo de consulta DNS `AXFR` para volcar todos los espacios de nombres DNS desde un servidor DNS vulnerable:

### **DIG - Transferencia de zona AXFR**

```shell-session
afsh4ck@hkali# dig AXFR @ns1.inlanefreight.htb inlanefreight.htb

; <<>> DiG 9.11.5-P1-1-Debian <<>> axfr inlanefrieght.htb @10.129.110.213
;; global options: +cmd
inlanefrieght.htb.         604800  IN      SOA     localhost. root.localhost. 2 604800 86400 2419200 604800
inlanefrieght.htb.         604800  IN      AAAA    ::1
inlanefrieght.htb.         604800  IN      NS      localhost.
inlanefrieght.htb.         604800  IN      A       10.129.110.22
admin.inlanefrieght.htb.   604800  IN      A       10.129.110.21
hr.inlanefrieght.htb.      604800  IN      A       10.129.110.25
support.inlanefrieght.htb. 604800  IN      A       10.129.110.28
inlanefrieght.htb.         604800  IN      SOA     localhost. root.localhost. 2 604800 86400 2419200 604800
;; Query time: 28 msec
;; SERVER: 10.129.110.213#53(10.129.110.213)
;; WHEN: Mon Oct 11 17:20:13 EDT 2020
;; XFR size: 8 records (messages 1, bytes 289)
```

También se pueden utilizar herramientas como [Fierce](https://github.com/mschwager/fierce) para enumerar todos los servidores DNS del dominio raíz y buscar una transferencia de zona DNS:

```shell-session
afsh4ck@kali# fierce --domain zonetransfer.me

NS: nsztm2.digi.ninja. nsztm1.digi.ninja.
SOA: nsztm1.digi.ninja. (81.4.108.41)
Zone: success
{<DNS name @>: '@ 7200 IN SOA nsztm1.digi.ninja. robin.digi.ninja. 2019100801 '
               '172800 900 1209600 3600\n'
               '@ 300 IN HINFO "Casio fx-700G" "Windows XP"\n'
               '@ 301 IN TXT '
               '"google-site-verification=tyP28J7JAUHA9fw2sHXMgcCC0I6XBmmoVi04VlMewxA"\n'
               '@ 7200 IN MX 0 ASPMX.L.GOOGLE.COM.\n'
               '@ 7200 IN MX 10 ALT1.ASPMX.L.GOOGLE.COM.\n'
               '@ 7200 IN MX 10 ALT2.ASPMX.L.GOOGLE.COM.\n'
               '@ 7200 IN MX 20 ASPMX2.GOOGLEMAIL.COM.\n'
               '@ 7200 IN MX 20 ASPMX3.GOOGLEMAIL.COM.\n'
               '@ 7200 IN MX 20 ASPMX4.GOOGLEMAIL.COM.\n'
               '@ 7200 IN MX 20 ASPMX5.GOOGLEMAIL.COM.\n'
               '@ 7200 IN A 5.196.105.14\n'
               '@ 7200 IN NS nsztm1.digi.ninja.\n'
               '@ 7200 IN NS nsztm2.digi.ninja.',
 <DNS name _acme-challenge>: '_acme-challenge 301 IN TXT '
                             '"6Oa05hbUJ9xSsvYy7pApQvwCUSSGgxvrbdizjePEsZI"',
 <DNS name _sip._tcp>: '_sip._tcp 14000 IN SRV 0 0 5060 www',
 <DNS name 14.105.196.5.IN-ADDR.ARPA>: '14.105.196.5.IN-ADDR.ARPA 7200 IN PTR '
                                       'www',
 <DNS name asfdbauthdns>: 'asfdbauthdns 7900 IN AFSDB 1 asfdbbox',
 <DNS name asfdbbox>: 'asfdbbox 7200 IN A 127.0.0.1',
 <DNS name asfdbvolume>: 'asfdbvolume 7800 IN AFSDB 1 asfdbbox',
 <DNS name canberra-office>: 'canberra-office 7200 IN A 202.14.81.230',
 <DNS name cmdexec>: 'cmdexec 300 IN TXT "; ls"',
 <DNS name contact>: 'contact 2592000 IN TXT "Remember to call or email Pippa '
                     'on +44 123 4567890 or pippa@zonetransfer.me when making '
                     'DNS changes"',
 <DNS name dc-office>: 'dc-office 7200 IN A 143.228.181.132',
 <DNS name deadbeef>: 'deadbeef 7201 IN AAAA dead:beaf::',
 <DNS name dr>: 'dr 300 IN LOC 53 20 56.558 N 1 38 33.526 W 0.00m',
 <DNS name DZC>: 'DZC 7200 IN TXT "AbCdEfG"',
 <DNS name email>: 'email 2222 IN NAPTR 1 1 "P" "E2U+email" "" '
                   'email.zonetransfer.me\n'
                   'email 7200 IN A 74.125.206.26',
 <DNS name Hello>: 'Hello 7200 IN TXT "Hi to Josh and all his class"',
 <DNS name home>: 'home 7200 IN A 127.0.0.1',
 <DNS name Info>: 'Info 7200 IN TXT "ZoneTransfer.me service provided by Robin '
                  'Wood - robin@digi.ninja. See '
                  'http://digi.ninja/projects/zonetransferme.php for more '
                  'information."',
 <DNS name internal>: 'internal 300 IN NS intns1\ninternal 300 IN NS intns2',
 <DNS name intns1>: 'intns1 300 IN A 81.4.108.41',
 <DNS name intns2>: 'intns2 300 IN A 167.88.42.94',
 <DNS name office>: 'office 7200 IN A 4.23.39.254',
 <DNS name ipv6actnow.org>: 'ipv6actnow.org 7200 IN AAAA '
                            '2001:67c:2e8:11::c100:1332',
...SNIP...
```

***

## <mark style="color:purple;">Domain Takeovers y enumeración de subdominios</mark>

Los `domain takeovers` se refieren al proceso de explorar y explotar vulnerabilidades en la configuración de dominios que permiten a un atacante tomar control de un dominio que ha sido mal configurado, expirado o abandonado por su propietario original.

Si los atacantes encuentran un dominio caducado, pueden reclamarlo para realizar más ataques, como alojar contenido malicioso en un sitio web o enviar un correo electrónico de phishing aprovechando el dominio reclamado.

El domain takeover también es posible con subdominios, llamado `subdomain takeover`. El registro de nombre canónico (`CNAME`) de un DNS se utiliza para asignar diferentes dominios a un dominio principal. Muchas organizaciones utilizan servicios de terceros como AWS, GitHub, Akamai, Fastly y otras redes de entrega de contenido (CDN) para alojar su contenido. En este caso, suelen crear un subdominio y hacer que apunte a esos servicios. Por ejemplo,

```shell-session
sub.target.com.   60   IN   CNAME   anotherdomain.com
```

El nombre de dominio (por ejemplo, `sub.target.com`) utiliza un registro CNAME  para otro dominio (por ejemplo, `anotherdomain.com`). Supongamos que `anotherdomain.com` caduca y está disponible para que cualquiera pueda reclamar el dominio ya que el servidor DNS `target.com` tiene el registro `CNAME`. En ese caso, cualquiera que se registre en `anotherdomain.com` tendrá control total de `sub.target.com` hasta que se actualice el registro DNS.

### **Enumeración de subdominios**

Antes de realizar una adquisición de subdominio, debemos enumerar los subdominios para un dominio de destino utilizando herramientas como [Subfinder](https://github.com/projectdiscovery/subfinder) . Esta herramienta puede extraer subdominios de fuentes abiertas como [DNSdumpster](https://dnsdumpster.com/) . También se pueden utilizar otras herramientas como [Sublist3r](https://github.com/aboul3la/Sublist3r) para aplicar fuerza bruta a subdominios proporcionando una lista de palabras pregenerada:

```shell-session
afsh4ck@kali# subfinder -d inlanefreight.com -v       
                                                                       
        _     __ _         _                                           
____  _| |__ / _(_)_ _  __| |___ _ _          
(_-< || | '_ \  _| | ' \/ _  / -_) '_|                 
/__/\_,_|_.__/_| |_|_||_\__,_\___|_| v2.4.5                                                                                                                                                                                                                                                 
                projectdiscovery.io                    
                                                                       
[WRN] Use with caution. You are responsible for your actions
[WRN] Developers assume no liability and are not responsible for any misuse or damage.
[WRN] By using subfinder, you also agree to the terms of the APIs used. 
                                   
[INF] Enumerating subdomains for inlanefreight.com
[alienvault] www.inlanefreight.com
[dnsdumpster] ns1.inlanefreight.com
[dnsdumpster] ns2.inlanefreight.com
...snip...
[bufferover] Source took 2.193235338s for enumeration
ns2.inlanefreight.com
www.inlanefreight.com
ns1.inlanefreight.com
support.inlanefreight.com
[INF] Found 4 subdomains for inlanefreight.com in 20 seconds 11 milliseconds
```

### **Subbrute**

Una excelente alternativa es una herramienta llamada [Subbrute](https://github.com/TheRook/subbrute) . Esta herramienta nos permite utilizar resolvers autodefinidos y realizar ataques de fuerza bruta DNS puros durante pruebas de penetración internas en hosts que no tienen acceso a Internet.

```shell-session
afsh4ck@kali$ git clone https://github.com/TheRook/subbrute.git >> /dev/null 2>&1
afsh4ck@kali$ cd subbrute
afsh4ck@kali$ echo "ns1.inlanefreight.com" > resolvers.txt
afsh4ck@kali$ subbrute inlanefreight.com -s names.txt -r resolvers.txt

Warning: Fewer than 16 resolvers per process, consider adding more nameservers to resolvers.txt.
inlanefreight.com
ns2.inlanefreight.com
www.inlanefreight.com
ns1.inlanefreight.com
support.inlanefreight.com

<SNIP>
```

A veces las configuraciones físicas internas están mal aseguradas, lo que podemos aprovechar para cargar nuestras herramientas desde una memoria USB. Otro escenario sería que hayamos llegado a un host interno mediante el pivote y queramos trabajar desde allí. Por supuesto, existen otras alternativas, pero no está de más conocer formas y posibilidades alternativas.

La herramienta ha encontrado cuatro subdominios asociados con `inlanefreight.com`. Usando el comando `nslookup` o `host`, podemos enumerar los registros `CNAME` de esos subdominios.

```shell-session
afsh4ck@kali# host support.inlanefreight.com

support.inlanefreight.com is an alias for inlanefreight.s3.amazonaws.com
```

El subdominio `support` tiene un registro de alias que apunta a un AWS S3 Bucket. Sin embargo, la URL `https://support.inlanefreight.com` muestra un error `NoSuchBucket` que indica que el subdominio es potencialmente vulnerable a una adquisición del subdominio. Ahora podemos tomar el control del subdominio creando un AWS S3 Bucket con el mismo nombre de subdominio.

![](https://academy.hackthebox.com/storage/modules/116/s3.png)

El repositorio [can-i-take-over-xyz](https://github.com/EdOverflow/can-i-take-over-xyz) también es una excelente referencia para una vulnerabilidad de adquisición de subdominio. Muestra si los servicios de destino son vulnerables a una adquisición de subdominio y proporciona pautas para evaluar la vulnerabilidad.

***

## <mark style="color:purple;">DNS Spoofing</mark>

La suplantación de DNS también se conoce como envenenamiento de caché de DNS. Este ataque implica alterar registros DNS legítimos con información falsa para que puedan usarse para redirigir el tráfico en línea a un sitio web fraudulento. A continuación se muestran ejemplos de rutas de ataque para el envenenamiento de la caché de DNS:

* Un atacante podría interceptar la comunicación entre un usuario y un servidor DNS para dirigir al usuario a un destino fraudulento en lugar de uno legítimo mediante la realización de un ataque Man-in-the-Middle (`MITM` ).
* Explotar una vulnerabilidad encontrada en un servidor DNS podría permitir que un atacante controle el servidor para modificar los registros DNS.

Vemos esta técnica en detalle en una sección dedicada:

{% content-ref url="/pages/0x2WmfWDN2mlbhDlgB30" %}
[Man in the middle](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/man-in-the-middle.md)
{% endcontent-ref %}

### **Local DNS Cache Poisoning**

Desde la perspectiva de la red local, un atacante también puede realizar envenenamiento de la caché de DNS utilizando herramientas MITM como [Ettercap](https://www.ettercap-project.org/) o [Bettercap](https://www.bettercap.org/) .

Para explotar el envenenamiento de la caché de DNS a través de `Ettercap`, primero debemos editar el archivo  `/etc/ettercap/etter.dns` para asignar el nombre de dominio de destino (por ejemplo, `inlanefreight.com`) que quieren falsificar y la dirección IP del atacante (por ejemplo, `192.168.225.110`) a la que quieren redirigir a un usuario:

```shell-session
afsh4ck@kali# cat /etc/ettercap/etter.dns

inlanefreight.com      A   192.168.225.110
*.inlanefreight.com    A   192.168.225.110
```

A continuación, inicia la herramienta `Ettercap` y busca hosts activos dentro de la red navegando a `Hosts > Scan for Hosts`. Una vez completado, agregue la dirección IP de destino (p. ej., `192.168.152.129`) a Target1 y agregue una IP de puerta de enlace predeterminada (p. ej., `192.168.152.2`) a Target2.

![](https://academy.hackthebox.com/storage/modules/116/target.png)

Active el ataque `dns_spoof` navegando a `Plugins > Manage Plugins`. Esto envía a la máquina de destino respuestas DNS falsas que resolverán `inlanefreight.com` en la dirección IP `192.168.225.110`:

![](https://academy.hackthebox.com/storage/modules/116/etter_plug.png)

Después de un ataque de suplantación de DNS exitoso, si un usuario víctima procedente de la máquina de destino `192.168.152.129` visita el dominio `inlanefreight.com` en un navegador web, será redirigido a una `Fake page` alojada en la dirección IP `192.168.225.110`:

![](https://academy.hackthebox.com/storage/modules/116/etter_site.png)

Además, un ping proveniente de la dirección IP de destino `192.168.152.129` hacia `inlanefreight.com` debe resolverse en `192.168.225.110`:

```
C:\> ping inlanefreight.com

Pinging inlanefreight.com [192.168.225.110] with 32 bytes of data:
Reply from 192.168.225.110: bytes=32 time<1ms TTL=64
Reply from 192.168.225.110: bytes=32 time<1ms TTL=64
Reply from 192.168.225.110: bytes=32 time<1ms TTL=64
Reply from 192.168.225.110: bytes=32 time<1ms TTL=64

Ping statistics for 192.168.225.110:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 0ms, Average = 0ms
```

Estos son algunos ejemplos de ataques DNS comunes. Hay otros ataques más avanzados que se tratarán en módulos posteriores.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.6.87
Host: inlanefreight.htb
```

> Busca todos los registros DNS disponibles para el dominio "`inlanefreight.htb`" en el nameserver de destino y envía la flag encontrada como registro DNS como respuesta.

Lo primero añadimos la IP y host al archivo `/etc/hosts`:

```bash
sudo echo "10.129.6.87 inlanefreight.htb" | sudo tee -a /etc/hosts
```

Podemos usar dig o dnsenum para enumerar el dominio:

```bash
dig @10.129.6.87 inlanefreight.htb ANY

; <<>> DiG 9.19.21-1-Debian <<>> @10.129.6.87 inlanefreight.htb ANY
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 8517
;; flags: qr aa rd; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 2
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 4280d9a1398989b501000000678e8a62d41c7348c093a38c (good)
;; QUESTION SECTION:
;inlanefreight.htb.		IN	ANY

;; ANSWER SECTION:
inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
inlanefreight.htb.	604800	IN	NS	ns.inlanefreight.htb.

;; ADDITIONAL SECTION:
ns.inlanefreight.htb.	604800	IN	A	127.0.0.1

;; Query time: 1944 msec
;; SERVER: 10.129.6.87#53(10.129.6.87) (TCP)
;; WHEN: Mon Jan 20 18:38:13 CET 2025
;; MSG SIZE  rcvd: 148
```

```
dnsenum --enum --dnsserver 10.129.6.87 inlanefreight.htb

dnsenum VERSION:1.2.6

-----   inlanefreight.htb   -----

Name Servers:
______________

ns.inlanefreight.htb.                    604800   IN    A         127.0.0.1
```

Encontramos el nameserver `ns.inlanefreight.htb`, que lo añadiremos también al /etc/hosts. Cuando hay un subdominio de este tipo lo más normal es que haya un `ns1` y un `ns2`, por lo que también los añadiremos al /etc/hosts.

```bash
sudo echo "10.129.6.87 inlanefreight.htb ns.inlanefreight.htb ns1.inlanefreight.htb ns2.inlanefreight.htb" | sudo tee -a /etc/hosts
```

Ahora vamos a usar [SubBrute](https://github.com/TheRook/subbrute) para enumerar los nameservers, pero antes añadimos estos dominios al archivo resolvers.txt:

{% code title="resolvers.txt" %}

```
inlanefreight.htb
ns.inlanefreight.htb
ns1.inlanefreight.htb
ns2.inlanefreight.htb
```

{% endcode %}

```bash
python3 subbrute.py inlanefreight.com -s names.txt -r resolvers.txt

Warning: Fewer than 16 resolvers per process, consider adding more nameservers to resolvers.txt.
Warning: No nameservers found, trying fallback list.
inlanefreight.com
hr.inlanefreight.com
```

Encontramos un subdominio interesante: `hr.inlanefreight.htb`, por lo que intentaremos una transferencia de zona sobre este subdominio:

```bash
dig AXFR @ns.inlanefreight.htb hr.inlanefreight.htb

; <<>> DiG 9.19.21-1-Debian <<>> AXFR @ns1.inlanefreight.htb hr.inlanefreight.htb
; (1 server found)
;; global options: +cmd
hr.inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
hr.inlanefreight.htb.	604800	IN	TXT	"HTB{LUIHNFAS2871SJK1259991}"
hr.inlanefreight.htb.	604800	IN	NS	ns.inlanefreight.htb.
ns.hr.inlanefreight.htb. 604800	IN	A	127.0.0.1
hr.inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
;; Query time: 39 msec
;; SERVER: 10.129.203.6#53(ns1.inlanefreight.htb) (TCP)
;; WHEN: Mon Apr 29 10:31:20 CEST 2024
;; XFR size: 5 records (messages 1, bytes 230)
```

Y bumm!! La transferencia de zona ha sido un éxito y obtenemos todos los registros, y subdominios privados de la organización, y en un registro TXT encontramos la flag.

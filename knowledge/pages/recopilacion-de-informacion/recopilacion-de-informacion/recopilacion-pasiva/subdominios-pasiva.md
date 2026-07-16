
# Subdominios - Pasiva

## <mark style="color:purple;">Enumeración pasiva de subdominios</mark>

***

La enumeración de subdominios se refiere al mapeo de todos los subdominios disponibles dentro de un nombre de dominio. Aumenta nuestra superficie de ataque y puede descubrir paneles de administración ocultos o aplicaciones web de intranet que los administradores de red esperaban mantener ocultos mediante la estrategia de "seguridad por oscuridad". En este punto, solo realizaremos una enumeración pasiva de subdominios utilizando servicios de terceros o información disponible públicamente. Aún así, ampliaremos la información que recopilamos en futuras actividades de enumeración de subdominios activos.

***

### VirusTotal

VirusTotal mantiene su servicio de replicación de DNS, que se desarrolla preservando las resoluciones de DNS realizadas cuando los usuarios visitan las URL proporcionadas por ellos. Para recibir información sobre un dominio, escriba el nombre del dominio en la barra de búsqueda y haga clic en la pestaña "Relaciones".

![imagen](https://academy.hackthebox.com/storage/modules/144/virustotal.png)

***

### Certificados

Otra fuente interesante de información que podemos utilizar para extraer subdominios son los certificados SSL/TLS. La razón principal es la Transparencia de Certificados (CT), un proyecto que requiere que cada certificado SSL/TLS emitido por una Autoridad Certificadora (CA) se publique en un registro de acceso público.

Aprenderemos cómo examinar los registros de CT para descubrir nombres de dominio y subdominios adicionales para una organización objetivo utilizando dos recursos principales:

* [https://censys.io](https://censys.io/)
* [https://crt.sh](https://crt.sh/)

Podemos navegar hasta <https://search.censys.io/certificates> o <https://crt.sh> e introducir el nombre de dominio de nuestra organización objetivo para comenzar a descubrir nuevos subdominios.

![censys.io/certificates](https://academy.hackthebox.com/storage/modules/144/censys_facebook.png)

<figure><img src="/files/oQ811VE8EcsMhL3ymZan" alt=""><figcaption><p>crt.sh</p></figcaption></figure>

Aunque el sitio web es excelente, nos gustaría tener esta información organizada y poder combinarla con otras fuentes encontradas durante el proceso de recopilación de información. Realicemos una solicitud curl al sitio web de destino solicitando una salida JSON, ya que nos resulta más manejable procesarla. Podemos hacer esto a través de los siguientes comandos:

**Transparencia del certificado**

```bash
afsh4ck$ export TARGET="facebook.com"
afsh4ck$ curl -s "https://crt.sh/?q=${TARGET}&output=json" | jq -r '.[] | "\(.name_value)\n\(.common_name)"' | sort -u > "${TARGET}_crt.sh.txt"
```

```bash
afsh4ck$ head -n20 facebook.com_crt.sh.txt

*.adtools.facebook.com
*.ak.facebook.com
*.ak.fbcdn.net
*.alpha.facebook.com
*.assistant.facebook.com
*.beta.facebook.com
*.channel.facebook.com
*.cinyour.facebook.com
*.cinyourrc.facebook.com
*.connect.facebook.com
*.cstools.facebook.com
*.ctscan.facebook.com
*.dev.facebook.com
*.dns.facebook.com
*.extern.facebook.com
*.extools.facebook.com
*.f--facebook.com
*.facebook.com
*.facebookcorewwwi.onion
*.facebookmail.com
```

<table><thead><tr><th width="345"></th><th></th></tr></thead><tbody><tr><td><code>curl -s</code></td><td>Emita la solicitud con un resultado mínimo.</td></tr><tr><td><code>https://crt.sh/?q=&#x3C;DOMAIN>&#x26;output=json</code></td><td>Solicite la salida json.</td></tr><tr><td><code>jq -r '.[]' "\(.name_value)\n\(.common_name)"'</code></td><td>Procese la salida json e imprima el valor del nombre del certificado y el nombre común uno por línea.</td></tr><tr><td><code>sort -u</code></td><td>Ordene alfabéticamente el resultado proporcionado y elimine duplicados.</td></tr></tbody></table>

También podemos realizar esta operación manualmente contra un objetivo usando OpenSSL:

```bash
afsh4ck$ export TARGET="facebook.com"
afsh4ck$ export PORT="443"
afsh4ck$ openssl s_client -ign_eof 2>/dev/null <<<$'HEAD / HTTP/1.0\r\n\r' -connect "${TARGET}:${PORT}" | openssl x509 -noout -text -in - | grep 'DNS' | sed -e 's|DNS:|\n|g' -e 's|^\*.*||g' | tr -d ',' | sort -u

*.facebook.com
*.facebook.net
*.fbcdn.net
*.fbsbx.com
*.m.facebook.com
*.messenger.com
*.xx.fbcdn.net
*.xy.fbcdn.net
*.xz.fbcdn.net
facebook.com
messenger.com
```

***

## <mark style="color:purple;">Automatización de la enumeración pasiva de subdominios</mark>

Hemos aprendido cómo adquirir información útil de nuestra organización objetivo, como subdominios, patrones de nombres, TLD alternativos, rangos de IP, etc., utilizando servicios de terceros sin interactuar directamente con su infraestructura ni depender de herramientas automatizadas. Ahora aprenderemos a enumerar subdominios utilizando herramientas e información obtenida previamente.

### The Harvester

{% embed url="<https://github.com/laramies/theHarvester>" %}

The Harvester es una herramienta fácil de usar pero potente y eficaz para pruebas de penetración en etapas iniciales y ejercicios de Red Team. Podemos usarlo para recopilar información que ayude a identificar la superficie de ataque de una empresa. La herramienta recopila `emails`, `nombres`, `subdominios`, `direcciones IP`y `URLs` de varias fuentes de datos públicos para la recopilación de información pasiva. Por ahora, usaremos los siguientes módulos:

<table data-header-hidden><thead><tr><th width="181"></th><th></th></tr></thead><tbody><tr><td><a href="http://www.baidu.com/">Baidu</a></td><td>Motor de búsqueda Baidu</td></tr><tr><td><code>Bufferoverun</code></td><td>Utiliza datos del Proyecto Sonar de Rapid7: <a href="http://www.rapid7.com/research/project-sonar/">www.rapid7.com/research/project-sonar/</a></td></tr><tr><td><a href="https://crt.sh/">Crtsh</a></td><td>Búsqueda de certificados de Comodo.</td></tr><tr><td><a href="https://hackertarget.com/">Hackertarget</a></td><td>Escáneres de vulnerabilidades online e inteligencia de red</td></tr><tr><td><code>Otx</code></td><td>Intercambio abierto de amenazas de AlienVault: <a href="https://otx.alienvault.com/">https://otx.alienvault.com</a></td></tr><tr><td><a href="https://rapiddns.io/">Rapiddns</a></td><td>Herramienta de consulta DNS, que facilita la consulta de subdominios o sitios que utilizan la misma IP</td></tr><tr><td><a href="https://github.com/aboul3la/Sublist3r">Sublist3r</a></td><td>Herramienta rápida de enumeración de subdominios para penetration testers</td></tr><tr><td><a href="http://www.threatcrowd.org/">Threatcrowd</a></td><td>Inteligencia sobre amenazas de código abierto</td></tr><tr><td><a href="https://www.threatminer.org/">Threatminer</a></td><td>Minería de datos para inteligencia sobre amenazas</td></tr><tr><td><code>Trello</code></td><td>Buscar tableros de Trello (utiliza la búsqueda de Google)</td></tr><tr><td><a href="https://urlscan.io/">Urlscan</a></td><td>Un sandbox web para estanear webs y URLs</td></tr><tr><td><code>Vhost</code></td><td>Búsqueda de hosts virtuales de Bing</td></tr><tr><td><a href="https://www.virustotal.com/gui/home/search">Virustotal</a></td><td>Búsqueda de dominios</td></tr><tr><td><a href="https://www.zoomeye.org/">Zoomeye</a></td><td>Versión china de Shodan</td></tr></tbody></table>

Para automatizar esto, crearemos un archivo llamado `sources.txt` con el siguiente contenido.

```bash
afsh4ck$ cat sources.txt

baidu
bufferoverun
crtsh
hackertarget
otx
projectdiscovery
rapiddns
sublist3r
threatcrowd
trello
urlscan
vhost
virustotal
zoomeye
```

Una vez creado el archivo, ejecutaremos los siguientes comandos para recopilar información de estas fuentes.

{% code overflow="wrap" %}

```bash
export TARGET="facebook.com"
cat sources.txt | while read source; do theHarvester -d "${TARGET}" -b $source -f "${source}_${TARGET}";done

<SNIP>
*******************************************************************
*  _   _                                            _             *
* | |_| |__   ___    /\  /\__ _ _ ____   _____  ___| |_ ___ _ __  *
* | __|  _ \ / _ \  / /_/ / _` | '__\ \ / / _ \/ __| __/ _ \ '__| *
* | |_| | | |  __/ / __  / (_| | |   \ V /  __/\__ \ ||  __/ |    *
*  \__|_| |_|\___| \/ /_/ \__,_|_|    \_/ \___||___/\__\___|_|    *
*                                                                 *
* theHarvester 4.0.0                                              *
* Coded by Christian Martorella                                   *
* Edge-Security Research                                          *
* cmartorella@edge-security.com                                   *
*                                                                 *
*******************************************************************


[*] Target: facebook.com

[*] Searching Urlscan.

[*] ASNS found: 29
--------------------
AS12578
AS13335
AS13535
AS136023
AS14061
AS14618
AS15169
AS15817

<SNIP>
```

{% endcode %}

Cuando finalice el proceso, podemos extraer todos los subdominios encontrados y ordenarlos mediante el siguiente comando:

```bash
cat *.json | jq -r '.hosts[]' 2>/dev/null | cut -d':' -f 1 | sort -u > "${TARGET}_theHarvester.txt"
```

Ahora podemos fusionar todos los archivos de reconocimiento pasivo mediante:

```bash
cat facebook.com_*.txt | sort -u > facebook.com_subdomains_passive.txt
cat facebook.com_subdomains_passive.txt | wc -l

11947
```

También podemos ejecutar theHarvester de una forma simple con el siguiente comando:

```bash
theHarvester -d facebook.com -l 400 -b all
```

### Sublist3r

Sublist3r es una herramienta de línea de comandos que utiliza múltiples fuentes de datos públicas para buscar subdominios asociados a un dominio principal. Esta herramienta es fácil de usar y proporciona resultados precisos de manera rápida. Sublist3r también admite la integración con otras herramientas de seguridad, como Nmap y Maltego

```bash
sudo apt install sublist3r

# el parámetro -b es para hacer fuerza bruta
sublist3r -d hackthissite.org -v -b -o output.txt

# Encuentra puertos abiertos en subdominios. (Recon. Activo)
sublist3r -d hackthissite.org -v -p 80,443 
```

<figure><img src="/files/xSS8lvP7MB9YydHrAE67" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Reconocimiento Activo de Subdominios</mark>

En la siguiente sección veremos técnicas de reconocimiento activo de subdominios:

{% content-ref url="/pages/ykFGPdWcgerB2RKpLB3w" %}
[Subdominios - Activa](/ethical-hacking-cheatsheet/recopilacion-de-informacion/recopilacion-de-informacion/recopilacion-activa/subdominios-activa.md)
{% endcontent-ref %}

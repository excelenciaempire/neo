
# Reconocimiento automatizado

Si bien el reconocimiento manual puede ser eficaz, también puede llevar mucho tiempo y ser propenso a errores humanos. La automatización de las tareas de reconocimiento web puede mejorar significativamente nuestra eficiencia y precisión, permitiéndonos recopilar información a escala e identificar vulnerabilidades potenciales más rápidamente.

{% hint style="danger" %}
**Nota:** Este tipo de búsquedas son muy invasivas, ya que hacen muchas peticiones al servidor del objetivo, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">¿Por qué automatizar el reconocimiento?</mark>

La automatización ofrece varias ventajas clave para el reconocimiento web:

* `Eficiencia`: Las herramientas automatizadas pueden realizar tareas repetitivas mucho más rápido que los humanos, liberando tiempo valioso para el análisis y la toma de decisiones.
* `Escalabilidad`: La automatización le permite escalar sus esfuerzos de reconocimiento en una gran cantidad de objetivos o dominios, descubriendo un alcance más amplio de información.
* `Consistencia`: Las herramientas automatizadas siguen reglas y procedimientos predefinidos, lo que garantiza resultados consistentes y reproducibles y minimiza el riesgo de error humano.
* `Cobertura completa`: La automatización se puede programar para realizar una amplia gama de tareas de reconocimiento, incluida la enumeración de DNS, el descubrimiento de subdominios, el rastreo web, el escaneo de puertos y más, lo que garantiza una cobertura exhaustiva de posibles vectores de ataque.
* `Integración`: Muchos frameworks de automatización permiten una fácil integración con otras herramientas y plataformas, creando un flujo de trabajo fluido desde el reconocimiento hasta la evaluación y explotación de vulnerabilidades.

## <mark style="color:purple;">Frameworks de reconocimiento</mark>

Estos frameworks tienen como objetivo proporcionar un conjunto completo de herramientas para el reconocimiento web:

* [FinalRecon](https://github.com/thewhiteh4t/FinalRecon) : una herramienta de reconocimiento basada en Python que ofrece una variedad de módulos para diferentes tareas como verificación de certificados SSL, recopilación de información Whois, análisis de encabezados y rastreo. Su estructura modular permite una fácil personalización para necesidades específicas.
* [Recon-ng](https://github.com/lanmaster53/recon-ng) : un potente framework escrito en Python que ofrece una estructura modular con varios módulos para diferentes tareas de reconocimiento. Puede realizar enumeraciones de DNS, descubrimiento de subdominios, escaneo de puertos, rastreo web e incluso explotar vulnerabilidades conocidas.
* [theHarvester](https://github.com/laramies/theHarvester) : Diseñado específicamente para recopilar direcciones de correo electrónico, subdominios, hosts, nombres de empleados, puertos abiertos y pancartas de diferentes fuentes públicas como motores de búsqueda, servidores de claves PGP y la base de datos SHODAN. Es una herramienta de línea de comandos escrita en Python.
* [SpiderFoot](https://github.com/smicallef/spiderfoot) : una herramienta de automatización de inteligencia de código abierto que se integra con varias fuentes de datos para recopilar información sobre un objetivo, incluidas direcciones IP, nombres de dominio, direcciones de correo electrónico y perfiles de redes sociales. Puede realizar búsquedas de DNS, rastreo web, escaneo de puertos y más.
* [OSINT Framework](https://osintframework.com/): una colección de diversas herramientas y recursos para la recopilación de inteligencia de código abierto. Cubre una amplia gama de fuentes de información, incluidas redes sociales, motores de búsqueda, registros públicos y más.

### FinalRecon

{% embed url="<https://github.com/thewhiteh4t/FinalRecon>" %}

`FinalRecon` ofrece una gran cantidad de información de reconocimiento:

* `Header Information`: revela detalles del servidor, tecnologías utilizadas y posibles errores de configuración de seguridad.
* `Whois Lookup`: descubre los detalles de registro del dominio, incluida la información del registrante y los detalles de contacto.
* `SSL Certificate Information`: examina el certificado SSL/TLS para verificar su validez, emisor y otros detalles relevantes.
* `Crawler`:
  * HTML, CSS, JavaScript: extrae enlaces, recursos y posibles vulnerabilidades de estos archivos.
  * Enlaces internos/externos: traza la estructura del sitio web e identifica conexiones a otros dominios.
  * Imágenes, robots.txt, sitemap.xml: recopila información sobre las rutas de rastreo permitidas o no permitidas y la estructura del sitio web.
  * Enlaces en JavaScript, Wayback Machine: descubre enlaces ocultos y datos históricos del sitio web.
* `DNS Enumeration`: Consulta más de 40 tipos de registros DNS, incluidos registros DMARC para evaluación de seguridad del correo electrónico.
* `Subdomain Enumeration`: Aprovecha múltiples fuentes de datos (crt.sh, AnubisDB, ThreatMiner, CertSpotter, API de Facebook, API VirusTotal, API Shodan, API BeVigil) para descubrir subdominios.
* `Directory Enumeration`: Admite listas de palabras personalizadas y extensiones de archivos para descubrir directorios y archivos ocultos.
* `Wayback Machine`: recupera URL de los últimos cinco años para analizar cambios en el sitio web y posibles vulnerabilidades.

### Instalación

Podemos hacer un git clone del repositorio o directamente instalarlo con apt en kali Linux:

```shell-session
afsh4ck@kali$ sudo apt install finalrecon
```

```shell-session
afsh4ck@kali$ finalrecon -h

usage: finalrecon.py [-h] [--url URL] [--headers] [--sslinfo] [--whois]
                     [--crawl] [--dns] [--sub] [--dir] [--wayback] [--ps]
                     [--full] [-nb] [-dt DT] [-pt PT] [-T T] [-w W] [-r] [-s]
                     [-sp SP] [-d D] [-e E] [-o O] [-cd CD] [-k K]

FinalRecon - All in One Web Recon | v1.1.6

optional arguments:
  -h, --help  show this help message and exit
  --url URL   Target URL
  --headers   Header Information
  --sslinfo   SSL Certificate Information
  --whois     Whois Lookup
  --crawl     Crawl Target
  --dns       DNS Enumeration
  --sub       Sub-Domain Enumeration
  --dir       Directory Search
  --wayback   Wayback URLs
  --ps        Fast Port Scan
  --full      Full Recon

Extra Options:
  -nb         Hide Banner
  -dt DT      Number of threads for directory enum [ Default : 30 ]
  -pt PT      Number of threads for port scan [ Default : 50 ]
  -T T        Request Timeout [ Default : 30.0 ]
  -w W        Path to Wordlist [ Default : wordlists/dirb_common.txt ]
  -r          Allow Redirect [ Default : False ]
  -s          Toggle SSL Verification [ Default : True ]
  -sp SP      Specify SSL Port [ Default : 443 ]
  -d D        Custom DNS Servers [ Default : 1.1.1.1 ]
  -e E        File Extensions [ Example : txt, xml, php ]
  -o O        Export Format [ Default : txt ]
  -cd CD      Change export directory [ Default : ~/.local/share/finalrecon ]
  -k K        Add API key [ Example : shodan@key ]
```

#### Opciones

<table data-header-hidden><thead><tr><th width="175"></th><th></th></tr></thead><tbody><tr><td>Opción</td><td>Descripción</td></tr><tr><td><code>-h</code>,<code>--help</code></td><td>Muestra el mensaje de ayuda y sal.</td></tr><tr><td><code>--url</code></td><td>Especifique la URL de destino.</td></tr><tr><td><code>--headers</code></td><td>Recuperar información del encabezado de la URL de destino.</td></tr><tr><td><code>--sslinfo</code></td><td>Obtenga información del certificado SSL para la URL de destino.</td></tr><tr><td><code>--whois</code></td><td>Realice una búsqueda Whois para el dominio de destino.</td></tr><tr><td><code>--crawl</code></td><td>Rastree el sitio web de destino.</td></tr><tr><td><code>--dns</code></td><td>Realice una enumeración de DNS en el dominio de destino.</td></tr><tr><td><code>--sub</code></td><td>Enumere los subdominios para el dominio de destino.</td></tr><tr><td><code>--dir</code></td><td>Busque directorios en el sitio web de destino.</td></tr><tr><td><code>--wayback</code></td><td>Recuperar URL Wayback para el objetivo.</td></tr><tr><td><code>--ps</code></td><td>Realice un escaneo rápido de puertos en el objetivo.</td></tr><tr><td><code>--full</code></td><td>Realice un escaneo de reconocimiento completo del objetivo.</td></tr></tbody></table>

Por ejemplo, si queremos recopilar información del encabezado y realizar una búsqueda Whois de `inlanefreight.com`, usaríamos las banderas correspondientes ( `--headers` y `--whois`), o usar `--full` para hacer un escaneo completo:

```shell-session
afsh4ck@kali$ finalrecon --full --url http://inlanefreight.com

 ______  __   __   __   ______   __
/\  ___\/\ \ /\ "-.\ \ /\  __ \ /\ \
\ \  __\\ \ \\ \ \-.  \\ \  __ \\ \ \____
 \ \_\   \ \_\\ \_\\"\_\\ \_\ \_\\ \_____\
  \/_/    \/_/ \/_/ \/_/ \/_/\/_/ \/_____/
 ______   ______   ______   ______   __   __
/\  == \ /\  ___\ /\  ___\ /\  __ \ /\ "-.\ \
\ \  __< \ \  __\ \ \ \____\ \ \/\ \\ \ \-.  \
 \ \_\ \_\\ \_____\\ \_____\\ \_____\\ \_\\"\_\
  \/_/ /_/ \/_____/ \/_____/ \/_____/ \/_/ \/_/

[>] Created By   : thewhiteh4t
 |---> Twitter   : https://twitter.com/thewhiteh4t
 |---> Community : https://twc1rcle.com/
[>] Version      : 1.1.6

[+] Target : http://inlanefreight.com

[+] IP Address : 134.209.24.248

[!] Headers :

Date : Tue, 11 Jun 2024 10:08:00 GMT
Server : Apache/2.4.41 (Ubuntu)
Link : <https://www.inlanefreight.com/index.php/wp-json/>; rel="https://api.w.org/", <https://www.inlanefreight.com/index.php/wp-json/wp/v2/pages/7>; rel="alternate"; type="application/json", <https://www.inlanefreight.com/>; rel=shortlink
Vary : Accept-Encoding
Content-Encoding : gzip
Content-Length : 5483
Keep-Alive : timeout=5, max=100
Connection : Keep-Alive
Content-Type : text/html; charset=UTF-8

[!] Whois Lookup : 

   Domain Name: INLANEFREIGHT.COM
   Registry Domain ID: 2420436757_DOMAIN_COM-VRSN
   Registrar WHOIS Server: whois.registrar.amazon.com
   Registrar URL: http://registrar.amazon.com
   Updated Date: 2023-07-03T01:11:15Z
   Creation Date: 2019-08-05T22:43:09Z
   Registry Expiry Date: 2024-08-05T22:43:09Z
   Registrar: Amazon Registrar, Inc.
   Registrar IANA ID: 468
   Registrar Abuse Contact Email: abuse@amazonaws.com
   Registrar Abuse Contact Phone: +1.2024422253
   Domain Status: clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited
   Domain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited
   Domain Status: clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited
   Name Server: NS-1303.AWSDNS-34.ORG
   Name Server: NS-1580.AWSDNS-05.CO.UK
   Name Server: NS-161.AWSDNS-20.COM
   Name Server: NS-671.AWSDNS-19.NET
   DNSSEC: unsigned
   URL of the ICANN Whois Inaccuracy Complaint Form: https://www.icann.org/wicf/


[+] Completed in 0:00:00.257780

[+] Exported : /home/htb-ac-643601/.local/share/finalrecon/dumps/fr_inlanefreight.com_11-06-2024_11:07:59
```

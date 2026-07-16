
# Web Crawlers

El rastreo web es vasto e intrincado, pero no es necesario que usted se embarque en este viaje solo. Hay una gran cantidad de herramientas de rastreo web disponibles para ayudarlo, cada una con sus propias fortalezas y especialidades. Estas herramientas automatizan el proceso de rastreo, haciéndolo más rápido y eficiente, permitiéndole concentrarse en analizar los datos extraídos.

## <mark style="color:purple;">Rastreadores web populares</mark>

1. `Burp Suite Spider`: Burp Suite, una plataforma de prueba de aplicaciones web ampliamente utilizada, incluye un potente rastreador activo llamado Spider. Spider se destaca en el mapeo de aplicaciones web, la identificación de contenido oculto y el descubrimiento de vulnerabilidades potenciales.
2. `OWASP ZAP (Zed Attack Proxy)`: ZAP es un escáner de seguridad de aplicaciones web gratuito y de código abierto. Se puede utilizar en modo automatizado y manual e incluye un componente de araña para rastrear aplicaciones web e identificar posibles vulnerabilidades.
3. `Scrapy (Python Framework)`: Scrapy es un framework de Python versátil y escalable para crear rastreadores web personalizados. Proporciona funciones completas para extraer datos estructurados de sitios web, manejar escenarios de rastreo complejos y automatizar el procesamiento de datos. Su flexibilidad lo hace ideal para tareas de reconocimiento personalizadas.
4. `Apache Nutch (Scalable Crawler)`: Nutch es un rastreador web de código abierto altamente extensible y escalable escrito en Java. Está diseñado para manejar rastreos masivos en toda la web o centrarse en dominios específicos. Si bien requiere más experiencia técnica para instalarlo y configurarlo, su potencia y flexibilidad lo convierten en un activo valioso para proyectos de reconocimiento a gran escala.

Adherirse a prácticas de rastreo éticas y responsables es crucial sin importar la herramienta que elija. Obtenga siempre permiso antes de rastrear un sitio web, especialmente si planea realizar análisis extensos o intrusivos. Tenga en cuenta los recursos del servidor del sitio web y evite sobrecargarlos con solicitudes excesivas.

## <mark style="color:purple;">Scrapy</mark>

Aprovecharemos Scrapy y un spider personalizado diseñado para el reconocimiento web. Si está interesado en obtener más información sobre técnicas de rastreo/spidering, consulte el módulo:

{% content-ref url="/pages/3LGp4oBig6eV0uxB4QPN" %}
[Web Proxies](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/web-proxies.md)
{% endcontent-ref %}

### Instalación de Scrapy

Antes de comenzar, asegúrese de tener Scrapy instalado en su sistema. Si no lo hace, puede instalarlo fácilmente usando pip, el instalador del paquete Python:

```shell-session
afsh4ck@kali$ pip3 install scrapy
```

Este comando descargará e instalará Scrapy junto con sus dependencias, preparando su entorno para construir nuestra araña.

## <mark style="color:purple;">ReconSpider</mark>

Primero, ejecuta este comando en la terminal para descargar el spider scrapy personalizado `ReconSpider` y extráelo en tu directorio de trabajo actual:

```shell-session
afsh4ck@kali$ wget https://academy.hackthebox.com/storage/modules/279/ReconSpider.zip
afsh4ck@kali$ unzip ReconSpider.zip 
```

{% hint style="success" %}
Esto nos descarga una versión de ReconSpider preinstalada. Es recomendable ya que el repositorio original está fuera de mantenimiento y da algunos errores.
{% endhint %}

O también podemos hacer un git clone de su repositorio de GitHub:

{% embed url="<https://github.com/bhavsec/reconspider>" %}

Con los archivos extraídos, podemos ejecutar `ReconSpider.py` usando el siguiente comando:

```shell-session
afsh4ck@kali$ python3 ReconSpider.py http://inlanefreight.com
```

Reemplaza `inlanefreight.com` con el dominio que deseas analizar. La araña rastreará el objetivo y recopilará información valiosa.

### resultados.json

Después de ejecutar `ReconSpider.py`, los datos se guardarán en un archivo `results.json`. Este archivo se puede explorar usando cualquier editor de texto.&#x20;

<figure><img src="/files/VDLTWANn24qtq399AWFv" alt=""><figcaption></figcaption></figure>

A continuación se muestra la estructura del archivo JSON producido:

```json
{
    "emails": [
        "lily.floid@inlanefreight.com",
        "cvs@inlanefreight.com",
        ...
    ],
    "links": [
        "https://www.themeansar.com",
        "https://www.inlanefreight.com/index.php/offices/",
        ...
    ],
    "external_files": [
        "https://www.inlanefreight.com/wp-content/uploads/2020/09/goals.pdf",
        ...
    ],
    "js_files": [
        "https://www.inlanefreight.com/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.3.2",
        ...
    ],
    "form_fields": [],
    "images": [
        "https://www.inlanefreight.com/wp-content/uploads/2021/03/AboutUs_01-1024x810.png",
        ...
    ],
    "videos": [],
    "audio": [],
    "comments": [
        "<!-- #masthead -->",
        ...
    ]
}
```

Cada clave en el archivo JSON representa un tipo diferente de datos extraídos del sitio web de destino:

<table data-header-hidden><thead><tr><th width="192"></th><th></th></tr></thead><tbody><tr><td>Clave JSON</td><td>Descripción</td></tr><tr><td><code>emails</code></td><td>Enumera las direcciones de correo electrónico encontradas en el dominio.</td></tr><tr><td><code>links</code></td><td>Enumera las URL de los enlaces encontrados dentro del dominio.</td></tr><tr><td><code>external_files</code></td><td>Enumera las URL de archivos externos, como archivos PDF.</td></tr><tr><td><code>js_files</code></td><td>Enumera las URL de los archivos JavaScript utilizados por el sitio web.</td></tr><tr><td><code>form_fields</code></td><td>Enumera los campos de formulario que se encuentran en el dominio (vacíos en este ejemplo).</td></tr><tr><td><code>images</code></td><td>Enumera las URL de las imágenes encontradas en el dominio.</td></tr><tr><td><code>videos</code></td><td>Enumera las URL de los vídeos encontrados en el dominio (vacíos en este ejemplo).</td></tr><tr><td><code>audio</code></td><td>Enumera las URL de los archivos de audio encontrados en el dominio (vacíos en este ejemplo).</td></tr><tr><td><code>comments</code></td><td>Enumera los comentarios HTML que se encuentran en el código fuente.</td></tr></tbody></table>

Al explorar esta estructura JSON, puede obtener información valiosa sobre la arquitectura, el contenido y los posibles puntos de interés de la aplicación web para una mayor investigación.

## <mark style="color:purple;">Final Recon</mark>

Final Recon es una herramienta de reconocimiento web automática todo en uno escrita en Python. El objetivo de FinalRecon es proporcionar una descripción general del objetivo en un corto período de tiempo manteniendo la precisión de los resultados. En lugar de ejecutar varias herramientas una tras otra, podemos usar este programa.

{% embed url="<https://github.com/thewhiteh4t/FinalRecon>" %}

Lo podemos instalar en Kali Linux con:

```bash
sudo apt install finalrecon
```

```shell-session
afsh4ck@kali$ finalrecon -h

usage: finalrecon [-h] [--url URL] [--headers] [--sslinfo] [--whois] [--crawl] [--dns] [--sub] [--dir] [--wayback] [--ps] [--full] [-nb] [-dt DT] [-pt PT] [-T T]
                  [-w W] [-r] [-s] [-sp SP] [-d D] [-e E] [-o O] [-cd CD] [-k K]

FinalRecon - All in One Web Recon | v1.1.7

options:
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
```

```shell-session
afsh4ck@kali$ finalrecon --url https://inlanefreight.com/ --full

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
[>] Version      : 1.1.7

[+] Target : https://inlanefreight.com

[+] IP Address : 134.209.24.248

[!] Headers :

Date : Wed, 04 Dec 2024 15:21:16 GMT
Server : Apache/2.4.41 (Ubuntu)
Link : <https://www.inlanefreight.com/index.php/wp-json/>; rel="https://api.w.org/", <https://www.inlanefreight.com/index.php/wp-json/wp/v2/pages/7>; rel="alternate"; type="application/json", <https://www.inlanefreight.com/>; rel=shortlink
Vary : Accept-Encoding
Content-Encoding : gzip
Content-Length : 5483
Keep-Alive : timeout=5, max=100
Connection : Keep-Alive
Content-Type : text/html; charset=UTF-8

[!] SSL Certificate Information : 

/usr/share/finalrecon/modules/sslinfo.py:102: CryptographyDeprecationWarning: Properties that return a naïve datetime object have been deprecated. Please switch to not_valid_before_utc.
  'notBefore': decoded_cert.not_valid_before.strftime("%b %d %H:%M:%S %Y GMT"),
/usr/share/finalrecon/modules/sslinfo.py:103: CryptographyDeprecationWarning: Properties that return a naïve datetime object have been deprecated. Please switch to not_valid_after_utc.
  'notAfter': decoded_cert.not_valid_after.strftime("%b %d %H:%M:%S %Y GMT"),
[+] protocol : TLSv1.3
[+] cipher
	└╴0: TLS_AES_256_GCM_SHA384
	└╴1: TLSv1.3
	└╴2: 256
[+] subject
	└╴commonName: inlanefreight.com
[+] issuer
	└╴countryName: US
	└╴organizationName: Let's Encrypt
	└╴commonName: R11
[+] version : Version.v3
[+] serialNumber : 343144780368253881689242976665259000982667
[+] notBefore : Nov 12 04:16:18 2024 GMT
[+] notAfter : Feb 10 04:16:17 2025 GMT
[+] subjectAltName
	└╴0: inlanefreight.com
	└╴1: www.inlanefreight.com

[!] Whois Lookup : 

   Domain Name: INLANEFREIGHT.COM
   Registry Domain ID: 2420436757_DOMAIN_COM-VRSN
   Registrar WHOIS Server: whois.registrar.amazon.com
   Registrar URL: http://registrar.amazon.com
   Updated Date: 2024-07-02T22:07:11Z
   Creation Date: 2019-08-05T22:43:09Z
   Registry Expiry Date: 2025-08-05T22:43:09Z
   Registrar: Amazon Registrar, Inc.
   Registrar IANA ID: 468
   Registrar Abuse Contact Email: trustandsafety@support.aws.com
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


[!] Starting DNS Enumeration...

A 	: 134.209.24.248
AAAA 	: 2a03:b0c0:1:e0::32c:b001
MX 	: 10 mail1.inlanefreight.com.
NS 	: ns1.inlanefreight.com.
NS 	: ns2.inlanefreight.com.
SOA 	: ns-161.awsdns-20.com. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400
TXT 	: "HTB{5Fz6UPNUFFzqjdg0AzXyxCjMZ}"
DMARC 	: "v=DMARC1; p=reject; rua=mailto:master@inlanefreight.com; ruf=mailto:master@inlanefreight.com; fo=1;"

[!] Starting Sub-Domain Enumeration...

<----SNIP---->
```

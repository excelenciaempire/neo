
# Nmap Scripting Engine

{% hint style="danger" %}
**Nota:** Este tipo de búsquedas son muy invasivas, ya que hacen muchas peticiones al servidor del objetivo, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Categorías de scripts</mark>

Todos los scripts de NSE se encuentran en la siguiente ruta:

```bash
cd /usr/share/nmap/scripts/
```

Hay un total de 14 categorías en las que se pueden dividir estos scripts:

<table data-header-hidden><thead><tr><th width="157"></th><th></th></tr></thead><tbody><tr><td><strong>Categoría</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>auth</code></td><td>Determinación de credenciales de autenticación.</td></tr><tr><td><code>broadcast</code></td><td>Los scripts, que se utilizan para el descubrimiento de hosts mediante la transmisión y los hosts descubiertos, se pueden agregar automáticamente a los análisis restantes.</td></tr><tr><td><code>brute</code></td><td>Ejecuta scripts que intentan iniciar sesión en el servicio respectivo mediante fuerza bruta con credenciales.</td></tr><tr><td><code>default</code></td><td>Scripts predeterminados ejecutados usando la opción <code>-sC</code></td></tr><tr><td><code>discovery</code></td><td>Evaluación de servicios accesibles.</td></tr><tr><td><code>dos</code></td><td>Estos scripts se utilizan para comprobar los servicios en busca de vulnerabilidades de denegación de servicio y se utilizan menos porque dañan los servicios.</td></tr><tr><td><code>exploit</code></td><td>Esta categoría de scripts intenta explotar vulnerabilidades conocidas del puerto escaneado.</td></tr><tr><td><code>external</code></td><td>Scripts que utilizan servicios externos para su posterior procesamiento.</td></tr><tr><td><code>fuzzer</code></td><td>Utiliza scripts para identificar vulnerabilidades y manejo inesperado de paquetes mediante el envío de diferentes campos, lo que puede llevar mucho tiempo.</td></tr><tr><td><code>intrusive</code></td><td>Scripts intrusivos que podrían afectar negativamente al sistema de destino.</td></tr><tr><td><code>malware</code></td><td>Comprueba si algún malware infecta el sistema de destino.</td></tr><tr><td><code>safe</code></td><td>Scripts defensivos que no realizan accesos intrusivos y destructivos.</td></tr><tr><td><code>version</code></td><td>Extensión para detección de servicios.</td></tr><tr><td><code>vuln</code></td><td>Identificación de vulnerabilidades específicas.</td></tr></tbody></table>

## <mark style="color:purple;">**Secuencias de comandos predeterminadas**</mark>

```bash
sudo nmap $TARGET -sC
```

## <mark style="color:purple;">**Categoría de scripts específicos**</mark>

```bash
sudo nmap $TARGET --script <category>
```

## <mark style="color:purple;">**Scripts definidos**</mark>

```bash
sudo nmap $TARGET --script <script-name>,<script-name>,...
```

Por ejemplo, sigamos trabajando con el puerto SMTP de destino y veamos los resultados que obtenemos con dos scripts definidos.

### **Nmap: especificación de scripts**

```bash
sudo nmap $TARGET -p 25 --script banner,smtp-commands

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-16 23:21 CEST
Nmap scan report for 10.129.2.28
Host is up (0.050s latency).

PORT   STATE SERVICE
25/tcp open  smtp
|_banner: 220 inlane ESMTP Postfix (Ubuntu)
|_smtp-commands: inlane, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8,
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)
```

<table data-header-hidden><thead><tr><th width="338"></th><th></th></tr></thead><tbody><tr><td><strong>Opciones de escaneo</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>10.129.2.28</code></td><td>Escanea el objetivo especificado.</td></tr><tr><td><code>-p 25</code></td><td>Explora sólo el puerto especificado.</td></tr><tr><td><code>--script banner,smtp-commands</code></td><td>Utiliza scripts NSE específicos.</td></tr></tbody></table>

Vemos que podemos reconocer la distribución **Ubuntu** de Linux usando el script '`banner`'.&#x20;

El `smtp-commands`script nos muestra qué comandos podemos usar al interactuar con el servidor SMTP de destino. En este ejemplo, dicha información puede ayudarnos a encontrar usuarios existentes en el objetivo.&#x20;

Nmap También nos da la posibilidad de escanear nuestro objetivo con la opción agresiva ( `-A`). Esto escanea el objetivo con múltiples opciones como detección de servicio ( `-sV`), detección de sistema operativo ( `-O`), traceroute ( `--traceroute`) y con los scripts NSE predeterminados ( `-sC`).

## <mark style="color:purple;">**Nmap - Escaneo agresivo**</mark>

```bash
sudo nmap $TARGET -p 80 -A

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-17 01:38 CEST
Nmap scan report for 10.129.2.28
Host is up (0.012s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-generator: WordPress 5.3.4
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: blog.inlanefreight.com
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 2.6.32 (96%), Linux 3.2 - 4.9 (96%), Linux 2.6.32 - 3.10 (96%), Linux 3.4 - 3.10 (95%), Linux 3.1 (95%), Linux 3.2 (95%), 
AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), Synology DiskStation Manager 5.2-5644 (94%), Netgear RAIDiator 4.2.28 (94%), 
Linux 2.6.32 - 2.6.35 (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop

TRACEROUTE
HOP RTT      ADDRESS
1   11.91 ms 10.129.2.28

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.36 seconds
```

<table data-header-hidden><thead><tr><th width="220"></th><th></th></tr></thead><tbody><tr><td><strong>Opciones de escaneo</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>10.129.2.28</code></td><td>Escanea el objetivo especificado.</td></tr><tr><td><code>-p 25</code></td><td>Explora sólo el puerto especificado.</td></tr><tr><td><code>-A</code></td><td>Realiza detección de servicios, detección de sistema operativo, traceroute y utiliza scripts predeterminados para escanear el objetivo.</td></tr></tbody></table>

Con la ayuda de la opción de escaneo usado ( `-A`), descubrimos qué tipo de servidor web ( `Apache 2.4.29`) se está ejecutando en el sistema, qué aplicación web ( `WordPress 5.3.4`) se utiliza y el título ( `blog.inlanefreight.com`) de la página web. Además, `Nmap` muestra que es probable que sea `Linux`( `96%`) sistema operativo.

***

## <mark style="color:purple;">Analizar vulnerabilidades</mark>

Ahora pasemos al puerto HTTP 80 y veamos qué información y vulnerabilidades podemos encontrar usando la categoría `vuln` de `NSE`.

```bash
sudo nmap $TARGET -p 80 -sV --script vuln 

Nmap scan report for 10.129.2.28
Host is up (0.036s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-enum:
|   /wp-login.php: Possible admin folder
|   /readme.html: Wordpress version: 2
|   /: WordPress version: 5.3.4
|   /wp-includes/images/rss.png: Wordpress version 2.2 found.
|   /wp-includes/js/jquery/suggest.js: Wordpress version 2.5 found.
|   /wp-includes/images/blank.gif: Wordpress version 2.6 found.
|   /wp-includes/js/comment-reply.js: Wordpress version 2.7 found.
|   /wp-login.php: Wordpress login page.
|   /wp-admin/upgrade.php: Wordpress login page.
|_  /readme.html: Interesting, a readme.
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
| http-wordpress-users:
| Username found: admin
|_Search stopped at ID #25. Increase the upper limit if necessary with 'http-wordpress-users.limit'
| vulners:
|   cpe:/a:apache:http_server:2.4.29:
|     	CVE-2019-0211	7.2	https://vulners.com/cve/CVE-2019-0211
|     	CVE-2018-1312	6.8	https://vulners.com/cve/CVE-2018-1312
|     	CVE-2017-15715	6.8	https://vulners.com/cve/CVE-2017-15715
<SNIP>
```

<table data-header-hidden><thead><tr><th width="210"></th><th></th></tr></thead><tbody><tr><td><strong>Opciones de escaneo</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>10.129.2.28</code></td><td>Escanea el objetivo especificado.</td></tr><tr><td><code>-p 80</code></td><td>Explora sólo el puerto especificado.</td></tr><tr><td><code>-sV</code></td><td>Realiza la detección de la versión del servicio en puertos específicos.</td></tr><tr><td><code>--script vuln</code></td><td>Utiliza todos los scripts relacionados de la categoría especificada.</td></tr></tbody></table>

Los scripts utilizados para el último escaneo interactúan con el servidor web y su aplicación web para obtener más información sobre sus versiones y verificar varias bases de datos para ver si existen vulnerabilidades conocidas. Más información sobre los scripts NSE y las categorías correspondientes la podemos encontrar en: <https://nmap.org/nsedoc/index.html>

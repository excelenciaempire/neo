
# Wordpress - Enumeración

## <mark style="color:purple;">Introducción</mark>

[WordPress](https://wordpress.org/) , lanzado en 2003, es un Content Management System (CMS) de código abierto que se puede utilizar para múltiples propósitos. A menudo se utiliza para alojar blogs, foros o ecommerces. WordPress es altamente personalizable y compatible con SEO, lo que lo hace popular entre las empresas. Sin embargo, su capacidad de personalización y naturaleza extensible lo hacen propenso a vulnerabilidades a través de temas y plugins de terceros. WordPress está escrito en PHP y generalmente se ejecuta en Apache con MySQL como backend.

En el momento de redactar este artículo, WordPress representa alrededor del 43,6% de todos los sitios web a nivel mundial, lo que equivale a más de 506 millones de sitios y es el CMS más popular por cuota de mercado. A continuación, se ofrecen algunos [datos](https://hostingtribunal.com/blog/wordpress-statistics/) interesantes sobre WordPress.

* WordPress ofrece más de 50.000 complementos y más de 4.000 temas con licencia GPL
* Se han lanzado 317 versiones independientes de WordPress desde su lanzamiento inicial
* Se crean aproximadamente 661 nuevos sitios web de WordPress cada día
* Los blogs de WordPress están escritos en más de 120 idiomas.
* Un estudio mostró que aproximadamente el 8% de los ataques a WordPress ocurren debido a contraseñas débiles, mientras que el 60% se deben a una versión desactualizada de WordPress.
* Según WPScan, de casi 4.000 vulnerabilidades conocidas, el 54% proviene de plugins, el 31,5% proviene del núcleo de WordPress y el 14,5% proviene de temas de WordPress.
* Algunas de las principales marcas que utilizan WordPress incluyen The New York Times, eBay, Sony, Forbes, Disney, Facebook, Mercedes-Benz y muchas más.

Como podemos ver en estas estadísticas, WordPress es muy común en Internet y presenta una amplia superficie de ataque. Tenemos la garantía de encontrarnos con WordPress durante muchas de nuestras evaluaciones de pruebas de penetración externas, y debemos entender cómo funciona, cómo enumerarlo y las distintas formas en que puede ser atacado.

Imaginemos que durante un test de penetración externo nos topamos con una empresa que aloja su página web principal basada en WordPress. Como muchas otras aplicaciones, WordPress cuenta con archivos individuales que nos permiten identificar dicha aplicación. Además, los archivos, la estructura de carpetas, los nombres de los archivos y la funcionalidad de cada script PHP pueden utilizarse para descubrir incluso la versión instalada de WordPress. En esta aplicación web, por defecto, los metadatos se añaden por defecto en el código fuente HTML de la página web, que en ocasiones incluso ya contiene la versión. Por tanto, veamos qué posibilidades tenemos para averiguar información más detallada sobre WordPress.

***

## <mark style="color:purple;">Discovery / Footprinting</mark>

Una forma rápida de identificar un sitio de WordPress es buscar el archivo `/robots.txt`. Un archivo robots.txt típico en una instalación de WordPress puede tener el siguiente aspecto:

```shell-session
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /wp-content/uploads/wpforms/

Sitemap: https://inlanefreight.local/wp-sitemap.xml
```

En este caso, la presencia de los directorios `/wp-admin` y `/wp-content` sería una clara señal de que estamos tratando con WordPress. Normalmente, al intentar navegar hasta el directorio `wp-admin`, se nos redireccionará a la página `wp-login.php`. Este es el portal de inicio de sesión en el back-end de la instancia de WordPress.  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/113/wp-login2.png" alt=""><figcaption></figcaption></figure>

WordPress almacena sus plugins en el directorio `wp-content/plugins`. Esta carpeta es útil para enumerar los plugins vulnerables. Los temas se almacenan en el directorio `wp-content/themes`. Estos archivos deben enumerarse con cuidado, ya que pueden provocar errores de ejecución de comandos (RCE).

Hay cinco tipos de usuarios en una instalación estándar de WordPress.

1. `Administrador`: este usuario tiene acceso a funciones administrativas dentro del sitio web. Esto incluye agregar y eliminar usuarios y publicaciones, así como editar el código fuente.
2. `Editor`: Un editor puede publicar y administrar publicaciones, incluidas las publicaciones de otros usuarios.
3. `Autor`: Pueden publicar y administrar sus propias publicaciones.
4. `Colaborador`: Estos usuarios pueden escribir y administrar sus propias publicaciones, pero no pueden publicarlas.
5. `Suscriptor`: Son usuarios estándar que pueden explorar publicaciones y editar sus perfiles.

Generalmente, obtener acceso a un administrador es suficiente para obtener la ejecución de código en el servidor. Los editores y autores pueden tener acceso a ciertos complementos vulnerables, algo que los usuarios normales no tienen.

***

## <mark style="color:purple;">Enumeración</mark>

Otra forma rápida de identificar un sitio de WordPress es mirar el código fuente de la página. Ver la página con `cURL` y filtrar por `WordPress` puede ayudarnos a confirmar que WordPress está en uso y a identificar el número de versión, que debemos anotar para más adelante. Podemos enumerar WordPress utilizando una variedad de tácticas manuales y automatizadas.

```shell-session
afsh4ck@kali$ curl -s http://blog.inlanefreight.local | grep WordPress

<meta name="generator" content="WordPress 5.8" /
```

Explorar el sitio y examinar el código fuente de la página nos dará pistas sobre el tema en uso, los complementos instalados e incluso los nombres de usuario si los nombres de los autores se publican con las publicaciones. Deberíamos dedicar algo de tiempo a explorar manualmente el sitio y a examinar el código fuente de cada página, a buscar el directorio `wp-content`, `themes`y `plugin`, y a comenzar a crear una lista de puntos de datos interesantes.

Si observamos el código fuente de la página, podemos ver que se está utilizando el tema [Business Gravity](https://wordpress.org/themes/business-gravity/) . Podemos ir más allá e intentar identificar el número de versión del tema y buscar vulnerabilidades conocidas que lo afecten.

#### Búsqueda de temas instalados

```shell-session
afsh4ck@kali$ curl -s http://blog.inlanefreight.local/ | grep themes

<link rel='stylesheet' id='bootstrap-css'  href='http://blog.inlanefreight.local/wp-content/themes/business-gravity/assets/vendors/bootstrap/css/bootstrap.min.css' type='text/css' media='all' />
```

#### Búsqueda de plugins instalados

```shell-session
afsh4ck@kali$ curl -s http://blog.inlanefreight.local/ | grep plugins

<link rel='stylesheet' id='contact-form-7-css'  href='http://blog.inlanefreight.local/wp-content/plugins/contact-form-7/includes/css/styles.css?ver=5.4.2' type='text/css' media='all' />
<script type='text/javascript' src='http://blog.inlanefreight.local/wp-content/plugins/mail-masta/lib/subscriber.js?ver=5.8' id='subscriber-js-js'></script>
<script type='text/javascript' src='http://blog.inlanefreight.local/wp-content/plugins/mail-masta/lib/jquery.validationEngine-en.js?ver=5.8' id='validation-engine-en-js'></script>
<script type='text/javascript' src='http://blog.inlanefreight.local/wp-content/plugins/mail-masta/lib/jquery.validationEngine.js?ver=5.8' id='validation-engine-js'></script>
		<link rel='stylesheet' id='mm_frontend-css'  href='http://blog.inlanefreight.local/wp-content/plugins/mail-masta/lib/css/mm_frontend.css?ver=5.8' type='text/css' media='all' />
<script type='text/javascript' src='http://blog.inlanefreight.local/wp-content/plugins/contact-form-7/includes/js/index.js?ver=5.4.2' id='contact-form-7-js'></script>
```

A partir del resultado anterior, sabemos que los complementos [Contact Form 7](https://wordpress.org/plugins/contact-form-7/) y [mail-masta](https://wordpress.org/plugins/mail-masta/) están instalados. El siguiente paso sería enumerar las versiones.

Al navegar hasta el sitio web, `http://blog.inlanefreight.local/wp-content/plugins/mail-masta/` se nos muestra que la lista de directorios está habilitada y que hay un archivo `readme.txt` presente. Estos archivos suelen ser muy útiles para identificar los números de versión. Según el archivo README, parece que está instalada la versión 1.0.0 del complemento, que sufre una vulnerabilidad [Local File Inclusion](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/local-file-inclusion.md) que se publicó en agosto de 2021.

Investiguemos un poco más. Al revisar el código fuente de otra página, podemos ver que el complemento [wpDiscuz](https://wpdiscuz.com/) está instalado y parece ser la versión 7.0.4.

```shell-session
afsh4ck@kali$ curl -s http://blog.inlanefreight.local/?p=1 | grep plugins

<link rel='stylesheet' id='contact-form-7-css'  href='http://blog.inlanefreight.local/wp-content/plugins/contact-form-7/includes/css/styles.css?ver=5.4.2' type='text/css' media='all' />
<link rel='stylesheet' id='wpdiscuz-frontend-css-css'  href='http://blog.inlanefreight.local/wp-content/plugins/wpdiscuz/themes/default/style.css?ver=7.0.4' type='text/css' media='all' />
```

Una búsqueda rápida de esta versión del complemento muestra [esta](https://www.exploit-db.com/exploits/49967) vulnerabilidad de ejecución remota de código no autenticado de junio de 2021. Tomaremos nota de esto y seguiremos adelante. Es importante en esta etapa no adelantarnos y comenzar a explotar la primera falla posible que veamos, ya que hay muchas otras vulnerabilidades potenciales y configuraciones erróneas posibles en WordPress que no queremos pasar por alto.

***

## <mark style="color:purple;">Enumeración de usuarios</mark>

También podemos realizar una enumeración manual de usuarios. Como se mencionó anteriormente, la página de inicio de sesión predeterminada de WordPress se puede encontrar en `/wp-login.php`.

Un nombre de usuario válido y una contraseña no válida dan como resultado el siguiente mensaje:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/113/valid_user.png" alt=""><figcaption></figcaption></figure>

Sin embargo, un nombre de usuario no válido devuelve que no se encontró el usuario.  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/113/invalid_user.png" alt=""><figcaption></figcaption></figure>

Esto hace que WordPress sea vulnerable a la enumeración de nombres de usuario, que puede utilizarse para obtener una lista de posibles nombres de usuario.

Recapitulemos. En esta etapa, hemos recopilado los siguientes puntos de datos:

* El sitio parece estar ejecutando la versión 5.8 del núcleo de WordPress
* El tema instalado es Business Gravity
* Se utilizan los siguientes complementos: Contact Form 7, mail-masta, wpDiscuz
* La versión de wpDiscuz parece ser 7.0.4, que sufre una vulnerabilidad de ejecución remota de código no autenticado.
* La versión de mail-masta parece ser 1.0.0, que sufre una vulnerabilidad de inclusión de archivos locales.
* El sitio de WordPress es vulnerable a la enumeración de usuarios y `admin`se confirma que el usuario es un usuario válido.

Vamos a dar un paso más y validar o completar algunos de nuestros puntos de datos con algunos análisis de enumeración automatizados del sitio de WordPress. Una vez que completemos esto, deberíamos tener suficiente información a mano para comenzar a planificar y montar nuestros ataques.

***

## <mark style="color:purple;">WPScan</mark>

[WPScan](https://github.com/wpscanteam/wpscan) es una herramienta de enumeración y escaneo automático de WordPress. Determina si los distintos temas y complementos que utiliza un blog están desactualizados o son vulnerables. Se instala de manera predeterminada en Kali Linux, pero también se puede instalar manualmente con `gem`.

```shell-session
afsh4ck@kali$ sudo gem install wpscan
```

WPScan también puede obtener información sobre vulnerabilidades de fuentes externas. Podemos obtener un token API de [WPVulnDB](https://wpvulndb.com/) , que WPScan utiliza para buscar PoC e informes. El plan gratuito permite hasta 75 solicitudes por día. Para utilizar la base de datos WPVulnDB, solo tienes que crear una cuenta y copiar el token API de la página de usuarios. Luego, puedes proporcionar este token a wpscan mediante el parámetro `--api-token`.

Al escribir `wpscan -h` aparecerá el menú de ayuda.

```shell-session
afsh4ck@kali$ wpscan -h

_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.7
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

Usage: wpscan [options]
        --url URL                                 The URL of the blog to scan
                                                  Allowed Protocols: http, https
                                                  Default Protocol if none provided: http
                                                  This option is mandatory unless update or help or hh or version is/are supplied
    -h, --help                                    Display the simple help and exit
        --hh                                      Display the full help and exit
        --version                                 Display the version and exit
    -v, --verbose                                 Verbose mode
        --[no-]banner                             Whether or not to display the banner
                                                  Default: true
    -o, --output FILE                             Output to FILE
    -f, --format FORMAT                           Output results in the format supplied
                                                  Available choices: json, cli-no-colour, cli-no-color, cli
        --detection-mode MODE                     Default: mixed
                                                  Available choices: mixed, passive, aggressive

<SNIP>
```

La flag `--enumerate` se utiliza para enumerar varios componentes de la aplicación WordPress, como complementos, temas y usuarios. De forma predeterminada, WPScan enumera complementos, temas, usuarios, medios y copias de seguridad vulnerables. Sin embargo, se pueden proporcionar argumentos específicos para restringir la enumeración a plugins específicos. Por ejemplo, todos los plugins se pueden enumerar utilizando los argumentos `--enumerate ap`. Invoquemos un escaneo de enumeración normal contra un sitio web de WordPress con la flag `--enumerate` y pasémosle un token de API de WPVulnDB con la flag `--api-token`.

```shell-session
afsh4ck@kali$ sudo wpscan --url http://blog.inlanefreight.local --enumerate --api-token dEOFB<SNIP>

<SNIP>

[+] URL: http://blog.inlanefreight.local/ [10.129.42.195]
[+] Started: Thu Sep 16 23:11:43 2021

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.41 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://blog.inlanefreight.local/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access

[+] WordPress readme found: http://blog.inlanefreight.local/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://blog.inlanefreight.local/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] WordPress version 5.8 identified (Insecure, released on 2021-07-20).
 | Found By: Rss Generator (Passive Detection)
 |  - http://blog.inlanefreight.local/?feed=rss2, <generator>https://wordpress.org/?v=5.8</generator>
 |  - http://blog.inlanefreight.local/?feed=comments-rss2, <generator>https://wordpress.org/?v=5.8</generator>
 |
 | [!] 3 vulnerabilities identified:
 |
 | [!] Title: WordPress 5.4 to 5.8 - Data Exposure via REST API
 |     Fixed in: 5.8.1
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/38dd7e87-9a22-48e2-bab1-dc79448ecdfb
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-39200
 |      - https://wordpress.org/news/2021/09/wordpress-5-8-1-security-and-maintenance-release/
 |      - https://github.com/WordPress/wordpress-develop/commit/ca4765c62c65acb732b574a6761bf5fd84595706
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-m9hc-7v5q-x8q5
 |
 | [!] Title: WordPress 5.4 to 5.8 - Authenticated XSS in Block Editor
 |     Fixed in: 5.8.1
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/5b754676-20f5-4478-8fd3-6bc383145811
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-39201
 |      - https://wordpress.org/news/2021/09/wordpress-5-8-1-security-and-maintenance-release/
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-wh69-25hr-h94v
 |
 | [!] Title: WordPress 5.4 to 5.8 -  Lodash Library Update
 |     Fixed in: 5.8.1
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/5d6789db-e320-494b-81bb-e678674f4199
 |      - https://wordpress.org/news/2021/09/wordpress-5-8-1-security-and-maintenance-release/
 |      - https://github.com/lodash/lodash/wiki/Changelog
 |      - https://github.com/WordPress/wordpress-develop/commit/fb7ecd92acef6c813c1fde6d9d24a21e02340689

[+] WordPress theme in use: transport-gravity
 | Location: http://blog.inlanefreight.local/wp-content/themes/transport-gravity/
 | Latest Version: 1.0.1 (up to date)
 | Last Updated: 2020-08-02T00:00:00.000Z
 | Readme: http://blog.inlanefreight.local/wp-content/themes/transport-gravity/readme.txt
 | [!] Directory listing is enabled
 | Style URL: http://blog.inlanefreight.local/wp-content/themes/transport-gravity/style.css
 | Style Name: Transport Gravity
 | Style URI: https://keonthemes.com/downloads/transport-gravity/
 | Description: Transport Gravity is an enhanced child theme of Business Gravity. Transport Gravity is made for tran...
 | Author: Keon Themes
 | Author URI: https://keonthemes.com/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 | Confirmed By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.0.1 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://blog.inlanefreight.local/wp-content/themes/transport-gravity/style.css, Match: 'Version: 1.0.1'

[+] Enumerating Vulnerable Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] mail-masta
 | Location: http://blog.inlanefreight.local/wp-content/plugins/mail-masta/
 | Latest Version: 1.0 (up to date)
 | Last Updated: 2014-09-19T07:52:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | [!] 2 vulnerabilities identified:
 |
 | [!] Title: Mail Masta <= 1.0 - Unauthenticated Local File Inclusion (LFI)

<SNIP>

| [!] Title: Mail Masta 1.0 - Multiple SQL Injection
      
 <SNIP
 
 | Version: 1.0 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://blog.inlanefreight.local/wp-content/plugins/mail-masta/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://blog.inlanefreight.local/wp-content/plugins/mail-masta/readme.txt

<SNIP>

[i] User(s) Identified:

[+] by:
									admin
 | Found By: Author Posts - Display Name (Passive Detection)

[+] admin
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] john
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)
```

WPScan utiliza varios métodos pasivos y activos para determinar versiones y vulnerabilidades, como se muestra en el informe anterior. El número predeterminado de subprocesos utilizados es `5`. Sin embargo, este valor se puede cambiar utilizando la flag `-t` .

Este análisis nos ayudó a confirmar algunas de las cosas que descubrimos a partir de la enumeración manual (versión 5.8 del núcleo de WordPress y listado de directorios habilitado), nos mostró que el tema que identificamos no era exactamente correcto (se está utilizando Transport Gravity, que es un tema secundario de Business Gravity), descubrió otro nombre de usuario (john) y mostró que la enumeración automática por sí sola a menudo no es suficiente (se pasaron por alto los complementos wpDiscuz y Contact Form 7). WPScan proporciona información sobre vulnerabilidades conocidas. El resultado del informe también contiene URL de PoC, que nos permitirían explotar estas vulnerabilidades.

El enfoque que adoptamos en esta sección, que combina la enumeración manual y automatizada, se puede aplicar a casi cualquier aplicación que descubramos. Los escáneres son geniales y muy útiles, pero no pueden reemplazar el toque humano ni una mente curiosa. Perfeccionar nuestras habilidades de enumeración puede diferenciarnos del resto como excelentes evaluadores de penetración.

***

## <mark style="color:purple;">CMSeek</mark>

{% embed url="<https://github.com/Tuhinshubhra/CMSeeK>" %}

CMSeek es una herramienta de línea de comandos para la detección de contenido sensible y la exploración de directorios y archivos en sitios web construidos con CMS (Content Management Systems). Esta herramienta puede ayudarte a encontrar información sensible como credenciales de acceso, claves de API y archivos de configuración que se han dejado expuestos.

<figure><img src="/files/yUcKueeEI3kmYYd6FMWc" alt=""><figcaption><p>CMSeek Scan</p></figcaption></figure>

#### Instalación y uso

Para instalar y utilizar CMSeek en Kali Linux, sigue los siguientes pasos:

```bash
git clone https://github.com/Tuhinshubhra/CMSeeK.git
cd CMSeeK
pip3 install -r requirements.txt
python3 cmseek.py  # Modo interactivo
python3 cmseek.py -u http://example.com # Escaneo simple
```

### <mark style="color:purple;">Bruteforce con CMSeek</mark>

Podemos usar CMSeek para hacer bruteforce de un usuario y contraseña de un sitio wordpress. Para ello accedemos a CMSeek en modo interactivo:

```bash
python3 cmseek.py
```

```bash
 ___ _  _ ____ ____ ____ _  _
|    |\/| [__  |___ |___ |_/  by @r3dhax0r
|___ |  | ___| |___ |___ | \_ Version 1.1.3 K-RONA

 [+]  Tip: You can use cmseek via arguments as well check the help menu for more information  [+] 

 Input    Description
=======  ==============================
  [1]    CMS detection and Deep scan
  [2]    Scan Multiple Sites
  [3]    Bruteforce CMSs
  [U]    Update CMSeeK
  [R]    Rebuild Cache (Use only when you add any custom module)
  [0]    Exit CMSeeK :( 

Enter Your Desired Option: 3
```

Seleccionamos la opción 3 de Bruteforce CMSs:

```bash
 ___ _  _ ____ ____ ____ _  _
|    |\/| [__  |___ |___ |_/  by @r3dhax0r
|___ |  | ___| |___ |___ | \_ Version 1.1.3 K-RONA

 [+]  WordPress XML-RPC Bruteforce Module  [+] 

Enter target site (https://example.tld): http://172.17.0.2/wordpress
[i] Checking for WordPress
[*] WordPress Confirmed... validating xmlrpc interface
[*] Login form found.. Detecting Username For Bruteforce
[i] Starting Username Harvest
[i] Harvesting usernames from wp-json api
[!] Json api method failed trying with next
[i] Harvesting usernames from jetpack public api
[!] No results from jetpack api... maybe the site doesn't use jetpack
[i] Harvesting usernames from wordpress author Parameter
[*] Found user from redirection: mario
[*] 1 Usernames was enumerated

[i] Bruteforcing User: mario
[*] Password found: love
 |
 |--[username]--> mario
 |
 |--[password]--> love
 |
[*] Enjoy The Hunt!

[*] Credentials stored at: /home/kali/Escritorio/hack-tools/CMS/CMSeeK/Result/172.17.0.2_wordp
```

***

## <mark style="color:purple;">WPAT (Wordpress Professional Audit Tool)</mark>

WPAT es una herramienta de auditoría y pentesting enfocada en entornos WordPress. Incluye módulos especializados para detectar vulnerabilidades, configuraciones inseguras y credenciales débiles. Está diseñada para facilitar tanto la enumeración como la explotación controlada en pruebas de seguridad.

{% embed url="<https://github.com/Santitub/WPAT>" %}

#### Instalación (CLI)

```bash
# Instalar pipx si no está disponible
python -m pip install --user pipx
python -m pipx ensurepath

# Instalar WPAT (solo CLI)
pipx install wpat

# Ejecutar
wpat
```

<figure><img src="/files/0t3rjS6cPAaDMMPO711N" alt=""><figcaption></figcaption></figure>

#### Instalación (GUI)

```bash
# Versión GUI usando pipx (con dependencias gráficas)
pipx install "wpat[gui]"

# Ejecutar GUI
wpat --gui
```

***

## <mark style="color:purple;">WP Config Scan</mark>

Esta herramienta en bash nos permite enumerar rápidamente un objetivo en Wordpress, listar los usuarios de la web y encontrar malas configuraciones como XML-RPC:

{% embed url="<https://github.com/micro-joan/wp-config-scan/blob/main/wp-config-scan.sh>" %}

<figure><img src="/files/SeaB4lgA0BuhA0GVMG6S" alt=""><figcaption></figcaption></figure>

#### Instalación y uso

```bash
git clone https://github.com/micro-joan/wp-config-scan
chmod +x wp-config-scan.sh
bash wp-config-scan.sh https://wordpress_site.com
```

***

## <mark style="color:purple;">Hacia delante</mark>

A partir de los datos que recopilamos manualmente y mediante WPScan, ahora sabemos lo siguiente:

* El sitio ejecuta la versión 5.8 del núcleo de WordPress, que sufre algunas vulnerabilidades que no parecen interesantes en este momento.
* El tema instalado es Transport Gravity
* Se utilizan los siguientes complementos: Contact Form 7, mail-masta, wpDiscuz
* La versión de wpDiscuz es 7.0.4, que sufre una vulnerabilidad de ejecución remota de código no autenticado
* La versión de mail-masta es 1.0.0, que sufre una vulnerabilidad de inclusión de archivos locales, así como una inyección SQL.
* El sitio de WordPress es vulnerable a la enumeración de usuarios, y se confirma que los usuarios `admin`y `john`son usuarios válidos.
* El listado de directorios está habilitado en todo el sitio, lo que puede provocar la exposición de datos confidenciales.
* Está habilitado XML-RPC, que puede aprovecharse para realizar un ataque de fuerza bruta de contraseña contra la página de inicio de sesión usando WPScan, [Metasploit](https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login) , etc.

Con esta información anotada, pasemos a la parte divertida: ¡atacar WordPress!

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.122.15 blog.inlanefreight.local
```

### Pregunta 1

> Enumere el host y busque una flag.txt en un directorio accesible.

Añadimos el hosts a /etc/hosts.&#x20;

<figure><img src="/files/TKJIfCXSuK4q34wkB5w9" alt=""><figcaption></figcaption></figure>

Vamos a ejecutar WPScan para encontrar datos relevantes:

```bash
wpscan --url http://blog.inlanefreight.local --enumerate u,vp
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.27
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: http://blog.inlanefreight.local/ [10.129.122.15]
[+] Started: Tue Nov 26 20:33:54 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.41 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://blog.inlanefreight.local/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://blog.inlanefreight.local/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://blog.inlanefreight.local/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 
 <---SNIP--->
```

Encontramos un directorio de subidas de archivos expuesto:

```
http://blog.inlanefreight.local/wp-content/uploads/
```

Al acceder encontramos varios directorios accesibles, y en uno de ellos encontramos la flag:

<figure><img src="/files/RR2CIdjq6mxRB1LZb7uS" alt=""><figcaption></figcaption></figure>

### Pregunta 2

> Realiza una enumeración manual para descubrir un plugin oculto instalado. Envía el nombre del plugin y su versión como respuesta

```shell-session
afsh4ck@kali$ curl -s http://blog.inlanefreight.local/ | grep plugins

<link rel='stylesheet' id='contact-form-7-css'  href='http://blog.inlanefreight.loca
l/wp-content/plugins/contact-form-7/includes/css/styles.css?ver=5.4.2' type='text/css' media='all' />
<script type='text/javascript' src='http://blog.inlanefreight.local/wp-content/plugins/mail-masta/lib/subscriber.js?ver=5.8' id='subscriber-js-js'></script>
<script type='text/javascript' src='http://blog.inlanefreight.local/wp-content/plugins/mail-masta/lib/jquery.validationEngine-en.js?ver=5.8' id='validation-engine-en-js'></script>
<script type='text/javascript' src='http://blog.inlanefreight.local/wp-content/plugins/mail-masta/lib/jquery.validationEngine.js?ver=5.8' id='validation-engine-js'></script>
		<link rel='stylesheet' id='mm_frontend-css'  href='http://blog.inlanefreight.local/wp-content/plugins/mail-masta/lib/css/mm_frontend.css?ver=5.8' type='text/css' media='all' />
<script type='text/javascript' src='http://blog.inlanefreight.local/wp-content/plugins/contact-form-7/includes/js/index.js?ver=5.4.2' id='contact-form-7-js'></script>
```

Enumerando manualmente los plugins encontramos:

* Mail Masta
* Contact Form 7
* Pero ninguno de ellos es la respuesta que esperamos, ya que el plugin que buscamos está oculto.

Vamos a buscar más en la propia web. Al acceder a un post vemos que pone `Powered by "Wp Sitemap Page"`, un plugin válido que no conseguimos enumerar con WPScan, aunque no obtenemos la versión en plano, tendremos que buscarla:

<figure><img src="/files/cMofUVo132LNuv8AHYGU" alt=""><figcaption></figcaption></figure>

Podemos acceder a la siguiente url para leer el archivo readme del plugin, donde obtenemos la versión:

```
http://blog.inlanefreight.local/wp-content/plugins/wp-sitemap-page/readme.txt
```

```
=== WP Sitemap Page ===
Contributors: funnycat
Donate link: http://www.infowebmaster.fr/dons.php
Tags: sitemap, generator, page list, site map, html sitemap, sitemap generator, dynamic sitemap, seo
Requires at least: 3.0
Tested up to: 5.6.2
Stable tag: 1.6.4
License: GPLv2 or later
```

Concretamente vemos que usa la versión `1.6.4`.

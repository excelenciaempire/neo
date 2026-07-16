
# Joomla - Enumeración

## <mark style="color:purple;">Introducción</mark>

[Joomla](https://www.joomla.org/) , lanzado en agosto de 2005, es otro CMS gratuito y de código abierto que se utiliza para foros de debate, galerías de fotos, comercio electrónico, comunidades de usuarios y más. Está escrito en PHP y utiliza MySQL en el backend. Al igual que WordPress, Joomla se puede mejorar con más de 7000 extensiones y más de 1000 plantillas. Hay hasta 2,5 millones de sitios en Internet que utilizan Joomla. A continuación, se muestran algunas [estadísticas](https://websitebuilder.org/blog/joomla-statistics/) interesantes sobre Joomla:

* Joomla representa el 3,5% de la cuota de mercado de CMS
* Joomla es 100% gratuito y significa "todos juntos" en suajili (escritura fonética de "Jumla").
* La comunidad Joomla tiene cerca de 700.000 miembros en sus foros en línea.
* Joomla impulsa el 3% de todos los sitios web en Internet, casi 25.000 del millón de sitios más importantes del mundo (solo el 10% del alcance de WordPress)
* Algunas organizaciones notables que utilizan Joomla incluyen eBay, Yamaha, la Universidad de Harvard y el gobierno del Reino Unido.
* A lo largo de los años, 770 desarrolladores diferentes han contribuido a Joomla.

Joomla recopila algunas [estadísticas de uso](https://developer.joomla.org/about/stats.html) anónimas , como el desglose de las versiones de Joomla, PHP y de la base de datos y los sistemas operativos del servidor que se utilizan en las instalaciones de Joomla. Estos datos se pueden consultar a través de su [API](https://developer.joomla.org/about/stats/api.html) pública .

¡Al consultar esta API, podemos ver más de 2,7 millones de instalaciones de Joomla!

```shell-session
afsh4ck@kali$ curl -s https://developer.joomla.org/stats/cms_version | python3 -m json.tool

{
    "data": {
        "cms_version": {
            "3.0": 0,
            "3.1": 0,
            "3.10": 3.49,
            "3.2": 0.01,
            "3.3": 0.02,
            "3.4": 0.05,
            "3.5": 13,
            "3.6": 24.29,
            "3.7": 8.5,
            "3.8": 18.84,
            "3.9": 30.28,
            "4.0": 1.52,
            "4.1": 0
        },
        "total": 2776276
    }
}
```

***

## <mark style="color:purple;">Discovery / Footprinting</mark>

Supongamos que nos topamos con un ecommerce durante una prueba de penetración externa. A primera vista, no estamos seguros exactamente de qué se está ejecutando, pero no parece que esté totalmente personalizado. Si podemos identificar qué se está ejecutando en el sitio, es posible que podamos descubrir vulnerabilidades o configuraciones incorrectas. Con base en la información limitada, asumimos que el sitio está ejecutando Joomla, pero debemos confirmar ese hecho y luego averiguar el número de versión y otra información, como temas y complementos instalados.

A menudo podemos identificar a Joomla mirando el código fuente de la página, lo que nos indica que estamos tratando con un sitio Joomla.

```shell-session
afsh4ck@kali$ curl -s http://dev.inlanefreight.local/ | grep Joomla

	<meta name="generator" content="Joomla! - Open Source Content Management" />


<SNIP>
```

El archivo `robots.txt` de un sitio Joomla generalmente se verá así:

```shell-session
# If the Joomla site is installed within a folder
# eg www.example.com/joomla/ then the robots.txt file
# MUST be moved to the site root
# eg www.example.com/robots.txt
# AND the joomla folder name MUST be prefixed to all of the
# paths.
# eg the Disallow rule for the /administrator/ folder MUST
# be changed to read
# Disallow: /joomla/administrator/
#
# For more information about the robots.txt standard, see:
# https://www.robotstxt.org/orig.html

User-agent: *
Disallow: /administrator/
Disallow: /bin/
Disallow: /cache/
Disallow: /cli/
Disallow: /components/
Disallow: /includes/
Disallow: /installation/
Disallow: /language/
Disallow: /layouts/
Disallow: /libraries/
Disallow: /logs/
Disallow: /modules/
Disallow: /plugins/
Disallow: /tmp/
```

También podemos ver a menudo el favicon de Joomla (pero no siempre). Podemos identificar la versión de Joomla si el archivo `README.txt` está presente.

```shell-session
afsh4ck@kali$ curl -s http://dev.inlanefreight.local/README.txt | head -n 5

1- What is this?
	* This is a Joomla! installation/upgrade package to version 3.x
	* Joomla! Official site: https://www.joomla.org
	* Joomla! 3.9 version history - https://docs.joomla.org/Special:MyLanguage/Joomla_3.9_version_history
	* Detailed changes in the Changelog: https://github.com/joomla/joomla-cms/commits/staging
```

En ciertas instalaciones de Joomla, es posible que podamos obtener la huella digital de la versión a partir de los archivos JavaScript en el directorio `media/system/js/` o navegando a `administrator/manifests/files/joomla.xml`.

```shell-session
afsh4ck@htb[/htb]$ curl -s http://dev.inlanefreight.local/administrator/manifests/files/joomla.xml | xmllint --format -

<?xml version="1.0" encoding="UTF-8"?>
<extension version="3.6" type="file" method="upgrade">
  <name>files_joomla</name>
  <author>Joomla! Project</author>
  <authorEmail>admin@joomla.org</authorEmail>
  <authorUrl>www.joomla.org</authorUrl>
  <copyright>(C) 2005 - 2019 Open Source Matters. All rights reserved</copyright>
  <license>GNU General Public License version 2 or later; see LICENSE.txt</license>
  <version>3.9.4</version>
  <creationDate>March 2019</creationDate>
  
 <SNIP>
```

El archivo `cache.xml` puede ayudarnos a obtener la versión aproximada. Se encuentra en `plugins/system/cache/cache.xml`.

***

## <mark style="color:purple;">Enumeración</mark>

### Droopescan

Probemos [droopescan](https://github.com/droope/droopescan) , un escáner basado en complemento que funciona para SilverStripe, WordPress y Drupal con funcionalidad limitada para Joomla y Moodle.

Podemos clonar el repositorio Git e instalarlo manualmente o instalarlo mediante `pip`.

```shell-session
afsh4ck@kali$ sudo pip3 install droopescan
```

```shell-session
afsh4ck@kali$ droopescan -h

usage: droopescan (sub-commands ...) [options ...] {arguments ...}

    |
 ___| ___  ___  ___  ___  ___  ___  ___  ___  ___
|   )|   )|   )|   )|   )|___)|___ |    |   )|   )
|__/ |    |__/ |__/ |__/ |__   __/ |__  |__/||  /
                    |
=================================================

commands:

  scan
    cms scanning functionality.

  stats
    shows scanner status & capabilities.

optional arguments:
  -h, --help  show this help message and exit
  --debug     toggle debug output
  --quiet     suppress all output

Example invocations: 
  droopescan scan drupal -u URL_HERE
  droopescan scan silverstripe -u URL_HERE

More info: 
  droopescan scan --help
 
Please see the README file for information regarding proxies.
```

Podemos acceder a un menú de ayuda más detallado escribiendo `droopescan scan --help`.

Ejecutemos un escaneo y veamos qué encontramos:

```shell-session
afsh4ck@kali$ droopescan scan joomla --url http://dev.inlanefreight.local/

[+] Possible version(s):                                                        
    3.8.10
    3.8.11
    3.8.11-rc
    3.8.12
    3.8.12-rc
    3.8.13
    3.8.7
    3.8.7-rc
    3.8.8
    3.8.8-rc
    3.8.9
    3.8.9-rc

[+] Possible interesting urls found:
    Detailed version information. - http://dev.inlanefreight.local/administrator/manifests/files/joomla.xml
    Login page. - http://dev.inlanefreight.local/administrator/
    License file. - http://dev.inlanefreight.local/LICENSE.txt
    Version attribute contains approx version - http://dev.inlanefreight.local/plugins/system/cache/cache.xml

[+] Scan finished (0:00:01.523369 elapsed)
```

Como podemos ver, no se ha obtenido mucha información aparte del posible número de versión.&#x20;

### Joomscan

Podemos usar este programa para enumerar de forma efectiva un host joomla. Lo podemos instalar en kali con apt:

```shell-session
afsh4ck@kali$ sudo apt install joomscan
```

```shell-session
afsh4ck@kali$ joomscan -h

Usage:	joomscan [options]

--url | -u <URL>                |   The Joomla URL/domain to scan.
--enumerate-components | -ec    |   Try to enumerate components.
--cookie <String>               |   Set cookie.
--user-agent | -a <User-Agent>  |   Use the specified User-Agent.
--random-agent | -r             |   Use a random User-Agent.
--timeout <Time-Out>            |   Set timeout.
--proxy=PROXY                   |   Use a proxy to connect to the target URL
           Proxy example: --proxy http://127.0.0.1:8080
                                  https://127.0.0.1:443
                                  socks://127.0.0.1:414
--about                         |   About Author
--help | -h                     |   This help screen.
--version                       |   Output the current version and exit.
```

```shell-session
afsh4ck@kali$ joomscan -u http://app.inlanefreight.local/

   ____  _____  _____  __  __  ___   ___    __    _  _ 
   (_  _)(  _  )(  _  )(  \/  )/ __) / __)  /__\  ( \( )
  .-_)(   )(_)(  )(_)(  )    ( \__ \( (__  /(__)\  )  ( 
  \____) (_____)(_____)(_/\/\_)(___/ \___)(__)(__)(_)\_)
			(1337.today)
   
    --=[OWASP JoomScan
    +---++---==[Version : 0.0.7
    +---++---==[Update Date : [2018/09/23]
    +---++---==[Authors : Mohammad Reza Espargham , Ali Razmjoo
    --=[Code name : Self Challenge
    @OWASP_JoomScan , @rezesp , @Ali_Razmjo0 , @OWASP

Processing http://app.inlanefreight.local/ ...

[+] FireWall Detector
[++] Firewall not detected

[+] Detecting Joomla Version
[++] Joomla 3.10.0

[+] Core Joomla Vulnerability
[++] PHPMailer Remote Code Execution Vulnerability
CVE : CVE-2016-10033
https://www.rapid7.com/db/modules/exploit/multi/http/phpmailer_arg_injection
https://github.com/opsxcq/exploit-CVE-2016-10033
EDB : https://www.exploit-db.com/exploits/40969/

PPHPMailer Incomplete Fix Remote Code Execution Vulnerability
CVE : CVE-2016-10045
https://www.rapid7.com/db/modules/exploit/multi/http/phpmailer_arg_injection
EDB : https://www.exploit-db.com/exploits/40969/

[+] Checking Directory Listing
[++] directory has directory listing : 
http://app.inlanefreight.local/administrator/components
http://app.inlanefreight.local/administrator/modules
http://app.inlanefreight.local/administrator/templates
http://app.inlanefreight.local/images/banners

[+] Checking apache info/status files
[++] Readable info/status files are not found

[+] admin finder
[++] Admin page : http://app.inlanefreight.local/administrator/

[+] Checking robots.txt existing
[++] robots.txt is found
path : http://app.inlanefreight.local/robots.txt 

Interesting path found from robots.txt
http://app.inlanefreight.local/joomla/administrator/
http://app.inlanefreight.local/administrator/
http://app.inlanefreight.local/bin/
http://app.inlanefreight.local/cache/
http://app.inlanefreight.local/cli/
http://app.inlanefreight.local/components/
http://app.inlanefreight.local/includes/
http://app.inlanefreight.local/installation/
http://app.inlanefreight.local/language/
http://app.inlanefreight.local/layouts/
http://app.inlanefreight.local/libraries/
http://app.inlanefreight.local/logs/
http://app.inlanefreight.local/modules/
http://app.inlanefreight.local/plugins/
http://app.inlanefreight.local/tmp/

[+] Finding common backup files name
[++] Backup files are not found

[+] Finding common log files name
[++] error log is not found

[+] Checking sensitive config.php.x file
[++] Readable config files are not found

Your Report : reports/app.inlanefreight.local/
```

### Joomlascan

También podemos probar [JoomlaScan](https://github.com/drego85/JoomlaScan) , que es una herramienta de Python inspirada en la herramienta [Joomscan](https://github.com/OWASP/joomscan) de OWASP. Está un poco desactualizada y requiere Python 2.7 para ejecutarse. Podemos ponerla en funcionamiento asegurándonos primero de que estén instaladas algunas dependencias.

```shell-session
afsh4ck@kali$ sudo python2.7 -m pip install urllib3
afsh4ck@kali$ sudo python2.7 -m pip install certifi
afsh4ck@kali$ sudo python2.7 -m pip install bs4
```

Aunque está un poco desactualizado, puede ser útil para nuestra enumeración. Hagamos un análisis.

```shell-session
afsh4ck@kali$ python2.7 joomlascan.py -u http://dev.inlanefreight.local

-------------------------------------------
      	     Joomla Scan                  
   Usage: python joomlascan.py <target>    
    Version 0.5beta - Database Entries 1233
         created by Andrea Draghetti       
-------------------------------------------
Robots file found: 	 	 > http://dev.inlanefreight.local/robots.txt
No Error Log found

Start scan...with 10 concurrent threads!
Component found: com_actionlogs	 > http://dev.inlanefreight.local/index.php?option=com_actionlogs
	 On the administrator components
Component found: com_admin	 > http://dev.inlanefreight.local/index.php?option=com_admin
	 On the administrator components
Component found: com_ajax	 > http://dev.inlanefreight.local/index.php?option=com_ajax
	 But possibly it is not active or protected
	 LICENSE file found 	 > http://dev.inlanefreight.local/administrator/components/com_actionlogs/actionlogs.xml
	 LICENSE file found 	 > http://dev.inlanefreight.local/administrator/components/com_admin/admin.xml
	 LICENSE file found 	 > http://dev.inlanefreight.local/administrator/components/com_ajax/ajax.xml
	 Explorable Directory 	 > http://dev.inlanefreight.local/components/com_actionlogs/
	 Explorable Directory 	 > http://dev.inlanefreight.local/administrator/components/com_actionlogs/
	 Explorable Directory 	 > http://dev.inlanefreight.local/components/com_admin/
	 Explorable Directory 	 > http://dev.inlanefreight.local/administrator/components/com_admin/
Component found: com_banners	 > http://dev.inlanefreight.local/index.php?option=com_banners
	 But possibly it is not active or protected
	 Explorable Directory 	 > http://dev.inlanefreight.local/components/com_ajax/
	 Explorable Directory 	 > http://dev.inlanefreight.local/administrator/components/com_ajax/
	 LICENSE file found 	 > http://dev.inlanefreight.local/administrator/components/com_banners/banners.xml


<SNIP>
```

Si bien no es tan valiosa como droopescan, esta herramienta puede ayudarnos a encontrar directorios y archivos accesibles y puede ayudarnos a identificar las extensiones instaladas. En este punto, sabemos que estamos tratando con Joomla `3.9.4`. El portal de inicio de sesión del administrador se encuentra en `http://dev.inlanefreight.local/administrator/index.php`. Los intentos de enumeración de usuarios devuelven un mensaje de error genérico.

```shell-session
Warning
Username and password do not match or you do not have an account yet.
```

## <mark style="color:purple;">Bruteforce de Joomla</mark>

La cuenta de administrador predeterminada en las instalaciones de Joomla es `admin`, pero la contraseña se establece en el momento de la instalación, por lo que la única forma en que podemos esperar ingresar al back-end de administración es si la cuenta está configurada con una contraseña muy débil/común y podemos ingresar con algunas conjeturas o con un ataque de fuerza bruta leve.

&#x20;Podemos usar este script para intentar forzar el inicio de sesión.

{% embed url="<https://github.com/ajnik/joomla-bruteforce>" %}

```shell-session
afsh4ck@kali$ sudo python3 joomla-brute.py -u http://dev.inlanefreight.local -w /usr/share/metasploit-framework/data/wordlists/http_default_pass.txt -usr admin
 
admin:admin
```

Y nos encontramos con un problema con las credenciales `admin:admin`. ¡Alguien no ha seguido las mejores prácticas!

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.136.207    app.inlanefreight.local
```

### Ejercicio 1

> Enumera la versión de Joomla en uso en `http://app.inlanefreight.local`

```shell-session
afsh4ck@kali$ droopescan scan joomla --url http://app.inlanefreight.local/

[+] Possible version(s):
    3.10.0-alpha1

[+] Possible interesting urls found:
    Detailed version information. - http://app.inlanefreight.local/administrator/manifests/files/joomla.xml
    Login page. - http://app.inlanefreight.local/administrator/
    License file. - http://app.inlanefreight.local/LICENSE.txt
    Version attribute contains approx version - http://app.inlanefreight.local/plugins/system/cache/cache.xml

[+] Scan finished (0:00:01.400014 elapsed)
```

Obtenemos la versión 3.10.0

### Ejercicio 2

> Encuentra la contraseña del usuario administrador en `http://app.inlanefreight.local`

Vamos a usar el script de [joomla-bruteforce](https://github.com/ajnik/joomla-bruteforce.git):

```shell-session
afsh4ck@kali$ sudo python3 joomla-brute.py -u http://app.inlanefreight.local -w /usr/share/metasploit-framework/data/wordlists/http_default_pass.txt -usr admin
admin:turnkey
```

Bingo! Obtenemos las credenciales del usuario adminstrador.

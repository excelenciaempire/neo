
# Infraestructura - Activa

La infraestructura de una aplicación web es lo que la mantiene en funcionamiento y le permite funcionar. Los servidores web están directamente involucrados en el funcionamiento de cualquier aplicación web. Algunos de los más populares son Apache, Nginx y Microsoft IIS, entre otros.

Si descubrimos el servidor web detrás de la aplicación de destino, podemos darnos una buena idea de qué sistema operativo se está ejecutando en el servidor back-end. Por ejemplo, si descubrimos que  versión de IIS se está ejecutando, podemos inferir la versión del sistema operativo Windows en uso asignando la versión de IIS a la versión de Windows que viene instalada de forma predeterminada.&#x20;

Algunas instalaciones predeterminadas son:

* IIS 6.0: Servidor Windows 2003
* IIS 7.0-8.5: Servidor Windows 2008/Servidor Windows 2008R2
* IIS 10.0 (v1607-v1709): Servidor Windows 2016
* IIS 10.0 (v1809-): Servidor Windows 2019

Aunque esto suele ser correcto cuando se trata de Windows, no podemos estar seguros en el caso de distribuciones basadas en Linux o BSD ya que pueden ejecutar diferentes versiones de servidor web en el caso de Nginx o Apache. Este tipo de tecnología podría interferir o alterar nuestras futuras actividades de prueba. Sin embargo, si tratamos con un servidor web, no podremos encontrar ninguna huella digital sobre el servidor en HTML o JS.

***

## <mark style="color:purple;">Servidores Web</mark>

Necesitamos descubrir la mayor cantidad de información posible del servidor web para comprender su funcionalidad, lo que puede afectar las pruebas futuras. Por ejemplo, la funcionalidad de reescritura de URL, un balanceador de carga, los motores de secuencias de comandos utilizados en el servidor o un `Intrusion detection system`( `IDS`) implementado pueden impedir algunas de nuestras actividades de prueba.

### <mark style="color:purple;">**HTTP Headers**</mark>

Lo primero que podemos hacer para identificar la versión del servidor web es mirar los encabezados de respuesta.

```shell-session
afsh4ck@kali$ curl -I "http://$TARGET"

HTTP/1.1 200 OK
Date: Thu, 23 Sep 2021 15:10:42 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.3.5
Link: <http://192.168.10.10/wp-json/>; rel="https://api.w.org/"
Content-Type: text/html; charset=UTF-8
```

También hay otras características a tener en cuenta al tomar huellas digitales de los servidores web en los encabezados de respuesta. Estos son:

* Encabezado X-Powered-By: este encabezado puede indicarnos qué está utilizando la aplicación web. Podemos ver valores como PHP, ASP.NET, JSP, etc.
* Cookies: las cookies son otro valor atractivo a tener en cuenta, ya que cada tecnología tiene sus propias cookies de forma predeterminada. Algunos de los valores de cookies predeterminados son:
  * .NET: `ASPSESSIONID<RANDOM>=<COOKIE_VALUE>`
  * PHP: `PHPSESSID=<COOKIE_VALUE>`
  * JAVA: `JSESSION=<COOKIE_VALUE>`

```shell-session
afsh4ck@kali$ curl -I http://$TARGET

HTTP/1.1 200 OK
Host: randomtarget.com
Date: Thu, 23 Sep 2021 15:12:21 GMT
Connection: close
X-Powered-By: PHP/7.4.21
Set-Cookie: PHPSESSID=gt02b1pqla35cvmmb2bcli96ml; path=/ 
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Content-type: text/html; charset=UTF-8
```

Otras herramientas disponibles analizan las características comunes de los servidores web sondeándolas y comparando sus respuestas con una base de datos de firmas para adivinar información como la versión del servidor web, los módulos instalados y los servicios habilitados. Algunas de estas herramientas son:

### <mark style="color:purple;">Whatweb</mark>

[Whatweb](https://www.morningstarsecurity.com/research/whatweb) reconoce tecnologías web, incluidos sistemas de gestión de contenidos (CMS), plataformas de blogs, paquetes de estadísticas/análisis, bibliotecas de JavaScript, servidores web y dispositivos integrados. Podemos leer el menú de ayuda con `whatweb -h` para comprender las opciones disponibles, como los controles de nivel de agresión o la salida detallada. En este caso, usaremos un nivel de agresión de 3 mediante la flag `-a` y una salida detallada mediante `-v`.

```shell-session
afsh4ck@kali$ whatweb -v -a3 $TARGET

WhatWeb report for https://www.facebook.com
Status    : 200 OK
Title     : <None>
IP        : 31.13.92.36
Country   : IRELAND, IE

Summary   : Strict-Transport-Security[max-age=15552000; preload], PasswordField[pass], Script[text/javascript], X-XSS-Protection[0], HTML5, X-Frame-Options[DENY], Meta-Refresh-Redirect[/?_fb_noscript=1], UncommonHeaders[x-fb-rlafr,x-content-type-options,x-fb-debug,alt-svc]

Detected Plugins:
[ HTML5 ]
	HTML version 5, detected by the doctype declaration


[ Meta-Refresh-Redirect ]
	Meta refresh tag is a deprecated URL element that can be
	used to optionally wait x seconds before reloading the
	current page or loading a new page. More info:
	https://secure.wikimedia.org/wikipedia/en/wiki/Meta_refresh

	String       : /?_fb_noscript=1

[ PasswordField ]
	find password fields

	String       : pass (from field name)

[ Script ]
	This plugin detects instances of script HTML elements and
	returns the script language/type.

	String       : text/javascript

[ Strict-Transport-Security ]
	Strict-Transport-Security is an HTTP header that restricts
	a web browser from accessing a website without the security
	of the HTTPS protocol.

	String       : max-age=15552000; preload

[ UncommonHeaders ]
	Uncommon HTTP server headers. The blacklist includes all
	the standard headers and many non standard but common ones.
	Interesting but fairly common headers should have their own
	plugins, eg. x-powered-by, server and x-aspnet-version.
	Info about headers can be found at www.http-stats.com

	String       : x-fb-rlafr,x-content-type-options,x-fb-debug,alt-svc (from headers)

[ X-Frame-Options ]
	This plugin retrieves the X-Frame-Options value from the
	HTTP header. - More Info:
	http://msdn.microsoft.com/en-us/library/cc288472%28VS.85%29.
	aspx

	String       : DENY

[ X-XSS-Protection ]
	This plugin retrieves the X-XSS-Protection value from the
	HTTP header. - More Info:
	http://msdn.microsoft.com/en-us/library/cc288472%28VS.85%29.
	aspx

	String       : 0

HTTP Headers:
	HTTP/1.1 200 OK
	Vary: Accept-Encoding
	Content-Encoding: gzip
	x-fb-rlafr: 0
	Pragma: no-cache
	Cache-Control: private, no-cache, no-store, must-revalidate
	Expires: Sat, 01 Jan 2000 00:00:00 GMT
	X-Content-Type-Options: nosniff
	X-XSS-Protection: 0
	X-Frame-Options: DENY
	Strict-Transport-Security: max-age=15552000; preload
	Content-Type: text/html; charset="utf-8"
	X-FB-Debug: r2w+sMJ7lVrMjS/ETitC6cNpJXma0r3fbt0rIlnTPAfQqTc+U4PQopVL7sR/6YA/ZKRkqP1wMPoFdUfMBP1JSA==
	Date: Wed, 06 Oct 2021 09:04:27 GMT
	Alt-Svc: h3=":443"; ma=3600, h3-29=":443"; ma=3600,h3-27=":443"; ma=3600
	Connection: close

WhatWeb report for https://www.facebook.com/?_fb_noscript=1
Status    : 200 OK
Title     : <None>
IP        : 31.13.92.36
Country   : IRELAND, IE

Summary   : Cookies[noscript], Strict-Transport-Security[max-age=15552000; preload], PasswordField[pass], Script[text/javascript], X-XSS-Protection[0], HTML5, X-Frame-Options[DENY], UncommonHeaders[x-fb-rlafr,x-content-type-options,x-fb-debug,alt-svc]

Detected Plugins:
[ Cookies ]
	Display the names of cookies in the HTTP headers. The
	values are not returned to save on space.

	String       : noscript

[ HTML5 ]
	HTML version 5, detected by the doctype declaration


[ PasswordField ]
	find password fields

	String       : pass (from field name)

[ Script ]
	This plugin detects instances of script HTML elements and
	returns the script language/type.

	String       : text/javascript

[ Strict-Transport-Security ]
	Strict-Transport-Security is an HTTP header that restricts
	a web browser from accessing a website without the security
	of the HTTPS protocol.

	String       : max-age=15552000; preload

[ UncommonHeaders ]
	Uncommon HTTP server headers. The blacklist includes all
	the standard headers and many non standard but common ones.
	Interesting but fairly common headers should have their own
	plugins, eg. x-powered-by, server and x-aspnet-version.
	Info about headers can be found at www.http-stats.com

	String       : x-fb-rlafr,x-content-type-options,x-fb-debug,alt-svc (from headers)

[ X-Frame-Options ]
	This plugin retrieves the X-Frame-Options value from the
	HTTP header. - More Info:
	http://msdn.microsoft.com/en-us/library/cc288472%28VS.85%29.
	aspx

	String       : DENY

[ X-XSS-Protection ]
	This plugin retrieves the X-XSS-Protection value from the
	HTTP header. - More Info:
	http://msdn.microsoft.com/en-us/library/cc288472%28VS.85%29.
	aspx

	String       : 0

HTTP Headers:
	HTTP/1.1 200 OK
	Vary: Accept-Encoding
	Content-Encoding: gzip
	Set-Cookie: noscript=1; path=/; domain=.facebook.com; secure
	x-fb-rlafr: 0
	Pragma: no-cache
	Cache-Control: private, no-cache, no-store, must-revalidate
	Expires: Sat, 01 Jan 2000 00:00:00 GMT
	X-Content-Type-Options: nosniff
	X-XSS-Protection: 0
	X-Frame-Options: DENY
	Strict-Transport-Security: max-age=15552000; preload
	Content-Type: text/html; charset="utf-8"
	X-FB-Debug: 7bEryjJ3tsTb/ap562d5L6KUJyJJ3bJh9XoamIo2lCVrX4cK/VAGbLx7muaAwnyobVm9myC3fQ+CXJqkk0eacg==
	Date: Wed, 06 Oct 2021 09:04:31 GMT
	Alt-Svc: h3=":443"; ma=3600, h3-29=":443"; ma=3600,h3-27=":443"; ma=3600
	Connection: close
```

### <mark style="color:purple;">Wappalizer</mark>

También recomiendo instalar [Wappalyzer](https://www.wappalyzer.com/) como extensión del navegador. Tiene una funcionalidad similar a Whatweb, pero los resultados se muestran mientras navega por la URL de destino.

<figure><img src="/files/3h7I3RQYzNwvPlTb5kos" alt=""><figcaption></figcaption></figure>

### <mark style="color:purple;">WafW00f</mark>

[WafW00f](https://github.com/EnableSecurity/wafw00f) es una herramienta de enumeración de Web Aplication Firewalls ( `WAF`) que envía solicitudes y analiza respuestas para determinar si existe una solución de seguridad. Podemos instalarlo con el siguiente comando:

**Instalación de WafW00f**

```bash
sudo apt install wafw00f -y
```

Podemos usar opciones como `-a` para verificar todos los WAF posibles en su lugar en lugar de detener el escaneo en la primera coincidencia, leer objetivos de un archivo de entrada a través de la opción `-i` o representar las solicitudes usando la opción `-p`.

```shell-session
afsh4ck@kali$ wafw00f -v https://www.kali.org    

                   ______
                  /      \
                 (  Woof! )
                  \  ____/                      )
                  ,,                           ) (_
             .-. -    _______                 ( |__|
            ()``; |==|_______)                .)|__|
            / ('        /|\                  (  |__|
        (  /  )        / | \                  . |__|
         \(_)_))      /  |  \                   |__|

                    ~ WAFW00F : v2.2.0 ~
    The Web Application Firewall Fingerprinting Toolkit
    
[*] Checking https://www.kali.org
[+] The site https://www.kali.org is behind Cloudflare (Cloudflare Inc.) WAF.
[~] Number of requests: 2
```

## <mark style="color:purple;">Aquatone</mark>

[Aquatone](https://github.com/michenriksen/aquatone) es una herramienta para la inspección visual y automática de sitios web en muchos hosts. Sirve para obtener rápidamente una descripción general de la superficie de ataque escaneando una lista de puertos configurables, visitando cada sitio web con un navegador Chrome sin header y tomando una captura de pantalla. Esto es útil, especialmente cuando se trata de listas de subdominios enormes.

`Aquatone` no está instalado de forma predeterminada en Kali Linux, por lo que necesitaremos instalarlo mediante los siguientes comandos.

### **Instalación de Aquatone**

```bash
sudo apt install golang chromium-driver
go install github.com/michenriksen/aquatone@latest
export PATH="$PATH":"$HOME/go/bin"
```

o tambien podemos instalarlo de la siguiente manera:

* Descargar la última release de Aquatone : <https://github.com/michenriksen/aquatone/releases/>

```bash
unzip aquatone_linux_amd64_<version>.zip
mv aquatone /usr/bin/
aquatone -version
cat subdomain_list.txt | aquatone
```

### **Opciones de Aquatone**

```shell-session
afsh4ck@kali$ aquatone --help

Usage of aquatone:
  -chrome-path string
    	Full path to the Chrome/Chromium executable to use. By default, aquatone will search for Chrome or Chromium
  -debug
    	Print debugging information
  -http-timeout int
    	Timeout in miliseconds for HTTP requests (default 3000)
  -nmap
    	Parse input as Nmap/Masscan XML
  -out string
    	Directory to write files to (default ".")
  -ports string
    	Ports to scan on hosts. Supported list aliases: small, medium, large, xlarge (default "80,443,8000,8080,8443")
  -proxy string
    	Proxy to use for HTTP requests
  -resolution string
    	screenshot resolution (default "1440,900")
  -save-body
    	Save response bodies to files (default true)
  -scan-timeout int
    	Timeout in miliseconds for port scans (default 100)
  -screenshot-timeout int
    	Timeout in miliseconds for screenshots (default 30000)
  -session string
    	Load Aquatone session file and generate HTML report
  -silent
    	Suppress all output except for errors
  -template-path string
    	Path to HTML template to use for report
  -threads int
    	Number of concurrent threads (default number of logical CPUs)
  -version
    	Print current Aquatone version
```

Ahora es el momento de usar `cat` con nuestra lista de subdominios y canalizar el comando a través de `aquatone`:

```bash
afsh4ck@kali$ cat facebook_subdomains.txt | aquatone -out ./aquatone -screenshot-timeout 1000

aquatone v1.7.0 started at 2021-10-06T10:14:42+01:00

Targets    : 30
Threads    : 2
Ports      : 80, 443, 8000, 8080, 8443
Output dir : aquatone

edge-star-shv-01-cdg2.facebook.com: port 80 open
edge-extern-shv-01-waw1.facebook.com: port 80 open
whatsapp-chatd-edge-shv-01-ams4.facebook.com: port 80 open
edge-secure-shv-01-ham3.facebook.com: port 80 open
sv-se.facebook.com: port 80 open
ko.facebook.com: port 80 open
whatsapp-chatd-msgr-mini-edge-shv-01-lis1.facebook.com: port 80 open
synthetic-e2e-elbprod-sli-shv-01-otp1.facebook.com: port 80 open
edge-star-shv-01-cdg2.facebook.com: port 443 open
edge-extern-shv-01-waw1.facebook.com: port 443 open
whatsapp-chatd-edge-shv-01-ams4.facebook.com: port 443 open
http://edge-star-shv-01-cdg2.facebook.com/: 200 OK
http://edge-extern-shv-01-waw1.facebook.com/: 200 OK
edge-secure-shv-01-ham3.facebook.com: port 443 open
ondemand-edge-shv-01-cph2.facebook.com: port 443 open
sv-se.facebook.com: port 443 open
http://edge-secure-shv-01-ham3.facebook.com/: 200 OK
ko.facebook.com: port 443 open
whatsapp-chatd-msgr-mini-edge-shv-01-lis1.facebook.com: port 443 open
http://sv-se.facebook.com/: 200 OK
http://ko.facebook.com/: 200 OK
synthetic-e2e-elbprod-sli-shv-01-otp1.facebook.com: port 443 open
http://synthetic-e2e-elbprod-sli-shv-01-otp1.facebook.com/: 400 default_vip_400
https://edge-star-shv-01-cdg2.facebook.com/: 200 OK
https://edge-extern-shv-01-waw1.facebook.com/: 200 OK
http://edge-star-shv-01-cdg2.facebook.com/: screenshot timed out
http://edge-extern-shv-01-waw1.facebook.com/: screenshot timed out
https://edge-secure-shv-01-ham3.facebook.com/: 200 OK
https://sv-se.facebook.com/: 200 OK
https://ko.facebook.com/: 200 OK
http://edge-secure-shv-01-ham3.facebook.com/: screenshot timed out
http://sv-se.facebook.com/: screenshot timed out
http://ko.facebook.com/: screenshot timed out
https://synthetic-e2e-elbprod-sli-shv-01-otp1.facebook.com/: 400 default_vip_400
http://synthetic-e2e-elbprod-sli-shv-01-otp1.facebook.com/: screenshot successful
https://edge-star-shv-01-cdg2.facebook.com/: screenshot timed out
https://edge-extern-shv-01-waw1.facebook.com/: screenshot timed out
https://edge-secure-shv-01-ham3.facebook.com/: screenshot timed out
https://sv-se.facebook.com/: screenshot timed out
https://ko.facebook.com/: screenshot timed out
https://synthetic-e2e-elbprod-sli-shv-01-otp1.facebook.com/: screenshot successful
Calculating page structures... done
Clustering similar pages... done
Generating HTML report... done

Writing session file...Time:
 - Started at  : 2021-10-06T10:14:42+01:00
 - Finished at : 2021-10-06T10:15:01+01:00
 - Duration    : 19s

Requests:
 - Successful : 12
 - Failed     : 5

 - 2xx : 10
 - 3xx : 0
 - 4xx : 2
 - 5xx : 0

Screenshots:
 - Successful : 2
 - Failed     : 10

Wrote HTML report to: aquatone/aquatone_report.html
```

Cuando finalice tendremos un archivo llamado `aquatone_report.html`donde podremos ver capturas de pantalla, tecnologías identificadas, encabezados de respuesta del servidor y HTML.

<figure><img src="/files/Vwh2kYua1uast9HDwNAT" alt=""><figcaption></figcaption></figure>

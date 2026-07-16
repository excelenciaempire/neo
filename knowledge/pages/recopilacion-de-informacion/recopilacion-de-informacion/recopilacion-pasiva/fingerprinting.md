
# Fingerprinting

## <mark style="color:purple;">Introducción</mark>

El `fingerprinting` se centra en extraer detalles técnicos sobre las tecnologías que impulsan un sitio web o una aplicación web. De manera similar a cómo una `huella digital` identifica de manera única a una persona, las firmas digitales de servidores web, sistemas operativos y componentes de software pueden revelar información crítica sobre la infraestructura de un objetivo y posibles debilidades de seguridad. Este conocimiento permite a los atacantes personalizar los ataques y explotar vulnerabilidades específicas de las tecnologías identificadas.

El fingerprinting sirve como piedra angular del reconocimiento web por varias razones:

* `Ataque dirigidos`: Al conocer las tecnologías específicas en uso, los atacantes pueden centrar sus esfuerzos en exploits y vulnerabilidades que se sabe que afectan a esos sistemas. Esto aumenta significativamente las posibilidades de lograr un compromiso exitoso.
* `Identificar malas configuraciones`: La toma de huellas dactilares puede exponer software mal configurado u obsoleto, configuraciones predeterminadas u otras debilidades que podrían no ser evidentes mediante otros métodos de reconocimiento.
* `Priorizar Targets`: Cuando se enfrenta a múltiples objetivos potenciales, la toma de huellas digitales ayuda a priorizar los esfuerzos al identificar los sistemas que tienen más probabilidades de ser vulnerables o contener información valiosa.
* `Construir un perfil completo`: La combinación de datos de huellas dactilares con otros hallazgos de reconocimiento crea una visión holística de la infraestructura del objetivo, lo que ayuda a comprender su postura de seguridad general y sus posibles vectores de ataque.

## <mark style="color:purple;">Técnicas de Fingerprinting</mark>

Existen varias técnicas utilizadas para la toma de huellas digitales de tecnología y servidores web:

* `Banner Grabbing`: La captura de banners implica analizar los banners presentados por los servidores web y otros servicios. Estos carteles suelen revelar el software del servidor, los números de versión y otros detalles.
* `Analizar HTTP Headers`: Los encabezados HTTP transmitidos con cada solicitud y respuesta de una página web contienen una gran cantidad de información. El encabezado `Server` generalmente revela el software del servidor web, mientras que el encabezado  `X-Powered-By` puede revelar tecnologías adicionales como lenguajes de secuencias de comandos o marcos.
* `Sondeo de respuestas específicas`: Enviar solicitudes especialmente diseñadas al objetivo puede generar respuestas únicas que revelen tecnologías o versiones específicas. Por ejemplo, ciertos mensajes de error o comportamientos son característicos de determinados servidores web o componentes de software.
* `Analizar el Contenido de Páginas`: El contenido de una página web, incluida su estructura, secuencias de comandos y otros elementos, a menudo puede proporcionar pistas sobre las tecnologías subyacentes. Puede haber un encabezado de derechos de autor que indique que se está utilizando un software específico, por ejemplo.

Existe una variedad de herramientas que automatizan el proceso de toma de huellas digitales, combinando varias técnicas para identificar servidores web, sistemas operativos, sistemas de gestión de contenidos y otras tecnologías:

<table data-header-hidden><thead><tr><th width="160"></th><th></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Descripción</td><td>Características</td></tr><tr><td><a href="/pages/tJy7DwMM7xKe9I9jPo3d"><code>Wappalyzer</code></a></td><td>Extensión de navegador y servicio en línea para creación de perfiles tecnológicos de sitios web.</td><td>Identifica una amplia gama de tecnologías web, incluidos CMS, marcos, herramientas de análisis y más.</td></tr><tr><td><code>BuiltWith</code></td><td>Perfilador de tecnología web que proporciona informes detallados sobre el stack tecnológico de un sitio web.</td><td>Ofrece planes gratuitos y de pago con distintos niveles de detalle.</td></tr><tr><td><a href="/pages/tJy7DwMM7xKe9I9jPo3d"><code>WhatWeb</code></a></td><td>Herramienta de línea de comandos para la toma de huellas digitales de sitios web.</td><td>Utiliza una amplia base de datos de firmas para identificar diversas tecnologías web.</td></tr><tr><td><a href="/pages/hbs35mOjMMP01gN0RuPl"><code>Nmap</code></a></td><td>Escáner de red versátil que se puede utilizar para diversas tareas de reconocimiento, incluidas las huellas digitales del sistema operativo y del servicio.</td><td>Se puede utilizar con scripts (NSE) para realizar footprintings más especializados.</td></tr><tr><td><a href="/pages/cklidacb33KDcJpIAoiH"><code>Netcraft</code></a></td><td>Ofrece una gama de servicios de seguridad web, que incluyen tomas de huellas digitales de sitios web e informes de seguridad.</td><td>Proporciona informes detallados sobre la tecnología de un sitio web, el proveedor de alojamiento y la situación de seguridad.</td></tr><tr><td><a href="/pages/6DGYBALnhpaOfU4mdu7C"><code>wafw00f</code></a></td><td>Herramienta de línea de comandos diseñada específicamente para identificar firewalls de aplicaciones web (WAF).</td><td>Ayuda a determinar si hay un WAF presente y, de ser así, su tipo y configuración.</td></tr></tbody></table>

### Footprinting en inlanefreight.com

Apliquemos nuestro conocimiento sobre huellas dactilares para descubrir el ADN digital de nuestro host especialmente diseñado `inlanefreight.com`. Aprovecharemos técnicas tanto manuales como automatizadas para recopilar información sobre su servidor web, tecnologías y vulnerabilidades potenciales.

#### Banner Grabbing

Nuestro primer paso es recopilar información directamente desde el propio servidor web. Podemos hacer esto usando el `curl`comando con la `-I`bandera (o `--head`) para recuperar solo los encabezados HTTP, no todo el contenido de la página.

```shell-session
afsh4ck@kali$ curl -I inlanefreight.com
```

El resultado incluirá el banner del servidor, que revelará el software del servidor web y el número de versión:

```shell-session
afsh4ck@kali$ curl -I inlanefreight.com

HTTP/1.1 301 Moved Permanently
Date: Fri, 31 May 2024 12:07:44 GMT
Server: Apache/2.4.41 (Ubuntu)
Location: https://inlanefreight.com/
Content-Type: text/html; charset=iso-8859-1
```

En este caso vemos que en `inlanefreight.com` se está ejecutando `Apache/2.4.41`, concretamente la versión `Ubuntu`. Esta información es nuestra primera pista, que insinúa el stack tecnológico subyacente. También está intentando redirigir, `https://inlanefreight.com/`así que toma esos banners también.

```shell-session
afsh4ck@kali$ curl -I https://inlanefreight.com

HTTP/1.1 301 Moved Permanently
Date: Fri, 31 May 2024 12:12:12 GMT
Server: Apache/2.4.41 (Ubuntu)
X-Redirect-By: WordPress
Location: https://www.inlanefreight.com/
Content-Type: text/html; charset=UTF-8
```

Ahora obtenemos un encabezado realmente interesante, el servidor está intentando redirigirnos nuevamente, pero esta vez vemos que es `WordPress` el que está haciendo la redirección a `https://www.inlanefreight.com/`

```shell-session
afsh4ck@kali$ curl -I https://www.inlanefreight.com

HTTP/1.1 200 OK
Date: Fri, 31 May 2024 12:12:26 GMT
Server: Apache/2.4.41 (Ubuntu)
Link: <https://www.inlanefreight.com/index.php/wp-json/>; rel="https://api.w.org/"
Link: <https://www.inlanefreight.com/index.php/wp-json/wp/v2/pages/7>; rel="alternate"; type="application/json"
Link: <https://www.inlanefreight.com/>; rel=shortlink
Content-Type: text/html; charset=UTF-8
```

Algunos encabezados más interesantes, incluida una ruta interesante que contiene `wp-json`. El prefijo `wp-` es común a WordPress.

### wafw00f

`Web Application Firewalls`( `WAFs`) son soluciones de seguridad diseñadas para proteger las aplicaciones web de diversos ataques. Antes de continuar con el footprinting, es crucial determinar si `inlanefreight.com` emplea un WAF, ya que podría interferir con nuestras sondas o potencialmente bloquear nuestras solicitudes.

Para detectar la presencia de un WAF, usaremos la herramienta `wafw00f`. Para instalar `wafw00f`, puedes usar pip3:

```shell-session
afsh4ck@kali$ pip3 install git+https://github.com/EnableSecurity/wafw00f
```

Una vez instalado, pasa el dominio que deseas verificar como argumento a la herramienta:

```shell-session
afsh4ck@kali$ wafw00f inlanefreight.com

                ______
               /      \
              (  W00f! )
               \  ____/
               ,,    __            404 Hack Not Found
           |`-.__   / /                      __     __
           /"  _/  /_/                       \ \   / /
          *===*    /                          \ \_/ /  405 Not Allowed
         /     )__//                           \   /
    /|  /     /---`                        403 Forbidden
    \\/`   \ |                                 / _ \
    `\    /_\\_              502 Bad Gateway  / / \ \  500 Internal Error
      `_____``-`                             /_/   \_\

                        ~ WAFW00F : v2.2.0 ~
        The Web Application Firewall Fingerprinting Toolkit
    
[*] Checking https://inlanefreight.com
[+] The site https://inlanefreight.com is behind Wordfence (Defiant) WAF.
[~] Number of requests: 2
```

El escaneo `wafw00f` de `inlanefreight.com` revela que el sitio web está protegido por `Wordfence Web Application Firewall`( `WAF`), desarrollado por Defiant.

Esto significa que el sitio tiene una capa de seguridad adicional que podría bloquear o filtrar nuestros intentos de reconocimiento. En un escenario del mundo real, sería crucial tener esto en cuenta a medida que se continúa con la investigación, ya que es posible que sea necesario adaptar técnicas para eludir o evadir los mecanismos de detección del WAF.

### Nikto

`Nikto` es un potente escáner de servidores web de código abierto. Además de su función principal como herramienta de evaluación de vulnerabilidades, las capacidades de toma de huellas digitales de  `Nikto` brindan información sobre la pila tecnológica de un sitio web.

`Nikto` está preinstalado en Kali Linux, pero si necesitas instalarlo, puedes ejecutar los siguientes comandos:

```shell-session
afsh4ck@kali$ sudo apt update && sudo apt install -y perl
afsh4ck@kali$ git clone https://github.com/sullo/nikto
afsh4ck@kali$ cd nikto/program
afsh4ck@kali$ chmod +x ./nikto.pl
```

Para escanear `inlanefreight.com` usando `Nikto`, ejecutando únicamente los módulos de huellas digitales, ejecute el siguiente comando:

```shell-session
afsh4ck@kali$ nikto -h inlanefreight.com -Tuning b
```

La flag `-h` especifica el host de destino. La flag `-Tuning b` indica a `Nikto` que solo se ejecuten los módulos de identificación de software.

`Nikto` iniciará una serie de pruebas, intentando identificar software obsoleto, archivos o configuraciones inseguros y otros riesgos potenciales de seguridad.

```shell-session
afsh4ck@kali$ nikto -h inlanefreight.com -Tuning b

- Nikto v2.5.0
---------------------------------------------------------------------------
+ Multiple IPs found: 134.209.24.248, 2a03:b0c0:1:e0::32c:b001
+ Target IP:          134.209.24.248
+ Target Hostname:    www.inlanefreight.com
+ Target Port:        443
---------------------------------------------------------------------------
+ SSL Info:        Subject:  /CN=inlanefreight.com
                   Altnames: inlanefreight.com, www.inlanefreight.com
                   Ciphers:  TLS_AES_256_GCM_SHA384
                   Issuer:   /C=US/O=Let's Encrypt/CN=R3
+ Start Time:         2024-05-31 13:35:54 (GMT0)
---------------------------------------------------------------------------
+ Server: Apache/2.4.41 (Ubuntu)
+ /: Link header found with value: ARRAY(0x558e78790248). See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Link
+ /: The site uses TLS and the Strict-Transport-Security HTTP header is not defined. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
+ /: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type. See: https://www.netsparker.com/web-vulnerability-scanner/vulnerabilities/missing-content-type-header/
+ /index.php?: Uncommon header 'x-redirect-by' found, with contents: WordPress.
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ /: The Content-Encoding header is set to "deflate" which may mean that the server is vulnerable to the BREACH attack. See: http://breachattack.com/
+ Apache/2.4.41 appears to be outdated (current is at least 2.4.59). Apache 2.2.34 is the EOL for the 2.x branch.
+ /: Web Server returns a valid response with junk HTTP methods which may cause false positives.
+ /license.txt: License file found may identify site software.
+ /: A Wordpress installation was found.
+ /wp-login.php?action=register: Cookie wordpress_test_cookie created without the httponly flag. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
+ /wp-login.php:X-Frame-Options header is deprecated and has been replaced with the Content-Security-Policy HTTP header with the frame-ancestors directive instead. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
+ /wp-login.php: Wordpress login found.
+ 1316 requests: 0 error(s) and 12 item(s) reported on remote host
+ End Time:           2024-05-31 13:47:27 (GMT0) (693 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

El escaneo de reconocimiento `inlanefreight.com` revela varios hallazgos clave:

* `IPs`: El sitio web resuelve tanto en direcciones IPv4 ( `134.209.24.248`) como IPv6 ( `2a03:b0c0:1:e0::32c:b001`).
* `Technología del Servidor`: El sitio web se ejecuta en`Apache/2.4.41 (Ubuntu)`
* `Presencia de WordPress`: El escaneo identificó una instalación de WordPress, incluida la página de inicio de sesión ( `/wp-login.php`). Esto sugiere que el sitio podría ser un objetivo potencial para exploits comunes relacionados con WordPress.
* `Information Disclosure`: La presencia de un archivo `license.txt` podría revelar detalles adicionales sobre los componentes de software del sitio web.
* `Headers`: Se encontraron varios encabezados no estándar o inseguros, incluido un encabezado `Strict-Transport-Security` faltante y un encabezado `x-redirect-by` potencialmente inseguro.

***

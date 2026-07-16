
# Enumeración del entorno

La enumeración es la clave para la escalada de privilegios. Existen varios scripts auxiliares (como [LinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS) y [LinEnum)](https://github.com/rebootuser/LinEnum) que ayudan con la enumeración. Sin embargo, también es importante comprender qué información buscar y poder realizar la enumeración manualmente. Cuando obtenga acceso inicial al host a través del shell, es importante verificar varios detalles clave.

`Versión del S.O`: Conocer la distribución (Ubuntu, Debian, FreeBSD, Fedora, SUSE, Red Hat, CentOS, etc.) le dará una idea de los tipos de herramientas que pueden estar disponibles. Esto también identificará la versión del sistema operativo para la que puede haber exploits públicos disponibles.

`Versión del Kernel`: Al igual que con la versión del sistema operativo, puede haber exploits públicos que tengan como objetivo una vulnerabilidad en una versión específica del kernel. Los exploits del kernel pueden provocar inestabilidad del sistema o incluso un bloqueo total. Tenga cuidado al ejecutarlos en cualquier sistema de producción y asegúrese de comprender completamente el exploit y las posibles ramificaciones antes de ejecutar uno.

`Servicios corriendo`: Es importante saber qué servicios se están ejecutando en el host, especialmente aquellos que se ejecutan como root. Un servicio mal configurado o vulnerable que se ejecute como root puede ser una victoria fácil para la escalada de privilegios. Se han descubierto fallas en muchos servicios comunes como Nagios, Exim, Samba, ProFTPd, etc. Existen PoC de explotación pública para muchos de ellos, como CVE-2016-9566, una falla de escalada de privilegios local en Nagios Core < 4.2.4.

***

## <mark style="color:purple;">Adquirir conciencia situacional</mark>

Digamos que acabamos de obtener acceso a un host Linux aprovechando una vulnerabilidad de carga de archivos sin restricciones durante una prueba de penetración externa. Después de establecer nuestro shell inverso (y, idealmente, algún tipo de persistencia), deberíamos comenzar por recopilar algunos conceptos básicos sobre el sistema con el que estamos trabajando.

Primero, responderemos la pregunta fundamental: ¿Con qué sistema operativo estamos tratando? Si aterrizamos en un host CentOS o Red Hat Enterprise Linux, nuestra enumeración probablemente sería ligeramente diferente que si aterrizamos en un host basado en Debian como Ubuntu. Si aterrizamos en un host como FreeBSD, Solaris o algo más oscuro como el sistema operativo propietario HP HP-UX o el sistema operativo IBM AIX, los comandos con los que trabajaríamos probablemente serán diferentes. Aunque los comandos pueden ser diferentes, e incluso puede que necesitemos buscar una referencia de comandos en algunos casos, los principios son los mismos. Para nuestros propósitos, comenzaremos con un objetivo Ubuntu para cubrir tácticas y técnicas generales. Una vez que aprendamos los conceptos básicos y los combinemos con una nueva forma de pensar y las etapas del proceso de prueba de penetración, no debería importar qué tipo de sistema Linux elijamos porque tendremos un proceso completo y repetible.

Existen muchas hojas de trucos que ayudan a enumerar sistemas Linux y algunos datos que nos interesan tendrán dos o más formas de obtenerse. En este módulo, cubriremos una metodología que probablemente se pueda usar para la mayoría de los sistemas Linux que encontramos en el mundo real. Dicho esto, asegúrese de comprender qué hacen los comandos y cómo modificarlos o encontrar la información que necesita de una manera diferente si un comando en particular no funciona. Desafíese durante este módulo para probar varias formas de practicar su metodología y lo que funcione mejor para usted. Cualquiera puede volver a escribir comandos de una hoja de trucos, pero una comprensión profunda de lo que está buscando y cómo obtenerlo nos ayudará a tener éxito en cualquier entorno.

Normalmente necesitaremos ejecutar algunos comandos básicos para orientarnos:

* `whoami` : ¿Con qué usuario estamos corriendo?
* `id` : ¿A qué grupos pertenece nuestro usuario?
* `hostname` : ¿Cómo se llama el servidor? ¿Podemos deducir algo de la convención de nombres?
* `ifconfig` o `ip -a` : ¿en qué subred aterrizamos?, ¿el host tiene NIC adicionales en otras subredes?
* `sudo -l` : ¿Puede nuestro usuario ejecutar cualquier cosa con sudo (como otro usuario como root) sin necesidad de una contraseña? A veces, esta puede ser la forma más fácil de hacerlo y podemos hacer algo como `sudo su` para ingresar directamente a un shell de root.

Incluir capturas de pantalla de la información anterior puede resultar útil en un informe de cliente para proporcionar evidencia de una ejecución de código remoto (RCE) exitosa y para identificar claramente el sistema afectado. Ahora, pasemos a nuestra enumeración más detallada, paso a paso.

Comenzaremos comprobando con qué sistema operativo y versión estamos tratando.

```shell-session
afsh4ck@kali$ cat /etc/os-release

NAME="Ubuntu"
VERSION="20.04.4 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.4 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal
```

Podemos ver que el objetivo está ejecutando [Ubuntu 20.04.4 LTS ("Focal Fossa")](https://releases.ubuntu.com/20.04/) . Sea cual sea la versión que encontremos, es importante ver si estamos tratando con algo desactualizado o mantenido. Ubuntu publica su [ciclo de lanzamiento](https://ubuntu.com/about/release-cycle) y, a partir de esto, podemos ver que "Focal Fossa" no llega al final de su vida útil hasta abril de 2030. A partir de esta información, podemos suponer que no encontraremos una vulnerabilidad de kernel conocida porque el cliente ha estado manteniendo su activo con conexión a Internet parcheado, pero de todos modos buscaremos.

A continuación, queremos comprobar la PATH de nuestro usuario actual, que es donde el sistema Linux busca cada vez que se ejecuta un comando para encontrar archivos ejecutables que coincidan con el nombre de lo que escribimos, es decir, que `id` en este sistema se encuentra en `/usr/bin/id`. Como veremos más adelante en este módulo, si la variable PATH de un usuario de destino está mal configurada, es posible que podamos aprovecharla para aumentar los privilegios. Por ahora, la anotaremos y la agregaremos a nuestra herramienta de toma de notas preferida.

```shell-session
afsh4ck@kali$ echo $PATH

/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

También podemos consultar todas las variables de entorno que están configuradas para nuestro usuario actual. Puede que tengamos suerte y encontremos algo confidencial, como una contraseña. Lo anotaremos y seguiremos adelante.

```shell-session
afsh4ck@kali$ env

SHELL=/bin/bash
PWD=/home/htb-student
LOGNAME=htb-student
XDG_SESSION_TYPE=tty
MOTD_SHOWN=pam
HOME=/home/htb-student
LANG=en_US.UTF-8

<SNIP>
```

A continuación, anotemos la versión del kernel. Podemos realizar algunas búsquedas para ver si el objetivo está ejecutando un kernel vulnerable (que aprovecharemos más adelante en el módulo) que tenga alguna prueba de concepto de explotación pública conocida. Podemos hacer esto de varias maneras, otra forma sería con `cat /proc/version` o usar el comando `uname -a`.

```shell-session
afsh4ck@kali$ uname -a

Linux nixlpe02 5.4.0-122-generic #138-Ubuntu SMP Wed Jun 22 15:00:31 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux
```

A continuación, podemos recopilar información adicional sobre el propio host, como el tipo/versión de la CPU:

```shell-session
afsh4ck@kali$ lscpu 

Architecture:                    x86_64
CPU op-mode(s):                  32-bit, 64-bit
Byte Order:                      Little Endian
Address sizes:                   43 bits physical, 48 bits virtual
CPU(s):                          2
On-line CPU(s) list:             0,1
Thread(s) per core:              1
Core(s) per socket:              2
Socket(s):                       1
NUMA node(s):                    1
Vendor ID:                       AuthenticAMD
CPU family:                      23
Model:                           49
Model name:                      AMD EPYC 7302P 16-Core Processor
Stepping:                        0
CPU MHz:                         2994.375
BogoMIPS:                        5988.75
Hypervisor vendor:               VMware

<SNIP>
```

¿Qué shells de inicio de sesión existen en el servidor? Anótelos y resalte que tanto Tmux como Screen están disponibles para nosotros.

```shell-session
afsh4ck@kali$ cat /etc/shells

# /etc/shells: valid login shells
/bin/sh
/bin/bash
/usr/bin/bash
/bin/rbash
/usr/bin/rbash
/bin/dash
/usr/bin/dash
/usr/bin/tmux
/usr/bin/screen
```

También debemos comprobar si existen defensas y podemos enumerar cualquier información sobre ellas. Algunas cosas que debemos buscar incluyen:

* [Exec Shield](https://en.wikipedia.org/wiki/Exec_Shield)
* [iptables](https://linux.die.net/man/8/iptables)
* [AppArmor](https://apparmor.net/)
* [SELinux](https://www.redhat.com/en/topics/linux/what-is-selinux)
* [Fail2ban](https://github.com/fail2ban/fail2ban)
* [Snort](https://www.snort.org/faq/what-is-snort)
* [Uncomplicated Firewall (ufw)](https://wiki.ubuntu.com/UncomplicatedFirewall)

A menudo no tendremos los privilegios para enumerar las configuraciones de estas protecciones, pero saber cuáles están implementadas, si las hay, puede ayudarnos a no perder tiempo en ciertas tareas.

A continuación, podemos echar un vistazo a las unidades y a los recursos compartidos del sistema. En primer lugar, podemos utilizar el comando `lsblk` para enumerar información sobre los dispositivos de bloque del sistema (discos duros, unidades USB, unidades ópticas, etc.). Si descubrimos y podemos montar una unidad adicional o un sistema de archivos desmontado, es posible que encontremos archivos confidenciales, contraseñas o copias de seguridad que se puedan aprovechar para aumentar los privilegios.

```shell-session
afsh4ck@kali$ lsblk

NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
loop0                       7:0    0   55M  1 loop /snap/core18/1705
loop1                       7:1    0   69M  1 loop /snap/lxd/14804
loop2                       7:2    0   47M  1 loop /snap/snapd/16292
loop3                       7:3    0  103M  1 loop /snap/lxd/23339
loop4                       7:4    0   62M  1 loop /snap/core20/1587
loop5                       7:5    0 55.6M  1 loop /snap/core18/2538
sda                         8:0    0   20G  0 disk 
├─sda1                      8:1    0    1M  0 part 
├─sda2                      8:2    0    1G  0 part /boot
└─sda3                      8:3    0   19G  0 part 
  └─ubuntu--vg-ubuntu--lv 253:0    0   18G  0 lvm  /
sr0                        11:0    1  908M  0 rom 
```

El comando `lpstat` se puede utilizar para buscar información sobre cualquier impresora conectada al sistema. Si hay trabajos de impresión activos o en cola, ¿podemos obtener acceso a algún tipo de información confidencial?

También deberíamos comprobar si hay unidades montadas y desmontadas. ¿Podemos montar una unidad desmontada y obtener acceso a datos confidenciales? ¿Podemos encontrar cualquier tipo de credenciales en `fstab`las unidades montadas buscando palabras comunes como contraseña, nombre de usuario, credenciales, etc. `/etc/fstab`?

```shell-session
afsh4ck@kali$ cat /etc/fstab

# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
# / was on /dev/ubuntu-vg/ubuntu-lv during curtin installation
/dev/disk/by-id/dm-uuid-LVM-BdLsBLE4CvzJUgtkugkof4S0dZG7gWR8HCNOlRdLWoXVOba2tYUMzHfFQAP9ajul / ext4 defaults 0 0
# /boot was on /dev/sda2 during curtin installation
/dev/disk/by-uuid/20b1770d-a233-4780-900e-7c99bc974346 /boot ext4 defaults 0 0
```

Consulte la tabla de enrutamiento escribiendo `route` o `netstat -rn`. Aquí podemos ver qué otras redes están disponibles a través de qué interfaz.

```shell-session
afsh4ck@kali$ route

Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         _gateway        0.0.0.0         UG    0      0        0 ens192
10.129.0.0      0.0.0.0         255.255.0.0     U     0      0        0 ens192
```

En un entorno de dominio, definitivamente querremos verificar `/etc/resolv.conf` para ver si el host está configurado para usar DNS interno; es posible que podamos usar esto como punto de partida para consultar el entorno de Active Directory.

También querremos verificar la tabla arp para ver con qué otros hosts se ha estado comunicando el objetivo.

```shell-session
afsh4ck@kali$ arp -a

_gateway (10.129.0.1) at 00:50:56:b9:b9:fc [ether] on ens192
```

La enumeración del entorno también incluye información sobre los usuarios que existen en el sistema de destino. Esto se debe a que, durante la instalación de aplicaciones y servicios, los usuarios individuales suelen configurarse para limitar los privilegios del servicio. El motivo de esto es mantener la seguridad del propio sistema. Porque si un servicio se está ejecutando con los privilegios más altos ( `root`) y un atacante lo controla, automáticamente el atacante tiene los derechos más altos sobre todo el sistema. Todos los usuarios del sistema se almacenan en el archivo `/etc/passwd`. El formato nos brinda cierta información, como:

1. Nombre de usuario
2. Contraseña
3. Identificación de usuario (UID)
4. Identificación de grupo (GID)
5. Información de identificación del usuario
6. Directorio de inicio
7. Shell

**Ver usuarios existentes**

```shell-session
afsh4ck@kali$ cat /etc/passwd

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
tcpdump:x:108:115::/nonexistent:/usr/sbin/nologin
mrb3n:x:1000:1000:mrb3n:/home/mrb3n:/bin/bash
bjones:x:1001:1001::/home/bjones:/bin/sh
administrator.ilfreight:x:1002:1002::/home/administrator.ilfreight:/bin/sh
backupsvc:x:1003:1003::/home/backupsvc:/bin/sh
cliff.moore:x:1004:1004::/home/cliff.moore:/bin/bash
logger:x:1005:1005::/home/logger:/bin/sh
shared:x:1006:1006::/home/shared:/bin/sh
stacey.jenkins:x:1007:1007::/home/stacey.jenkins:/bin/bash
htb-student:x:1008:1008::/home/htb-student:/bin/bash
<SNIP>
```

Ocasionalmente, veremos hashes de contraseñas directamente en el archivo `/etc/passwd`. Este archivo es legible para todos los usuarios y, al igual que con los hashes en el archivo `/etc/shadow`, estos pueden estar sujetos a un ataque de descifrado de contraseñas fuera de línea. Esta configuración, aunque no es común, a veces se puede ver en dispositivos integrados y enrutadores.

```shell-session
afsh4ck@kali$ cat /etc/passwd | cut -f1 -d:

root
daemon
bin
sys

...SNIP...

mrb3n
lxd
bjones
administrator.ilfreight
backupsvc
cliff.moore
logger
shared
stacey.jenkins
htb-student
```

Con Linux se pueden utilizar varios algoritmos hash diferentes para hacer que las contraseñas sean irreconocibles. Identificarlos a partir de los primeros bloques hash puede ayudarnos a utilizarlos y trabajar con ellos más adelante si es necesario. A continuación, se incluye una lista de los más utilizados:

| **Algoritmo** | **Hash**       |
| ------------- | -------------- |
| Salted MD5    | `$1$`...       |
| SHA-256       | `$5$`...       |
| SHA-512       | `$6$`...       |
| BCrypt        | `$2a$`...      |
| Scrypt        | `$7$`...       |
| Argon2        | `$argon2i$`... |

También queremos comprobar qué usuarios tienen shells de inicio de sesión. Una vez que veamos qué shells hay en el sistema, podemos comprobar cada versión en busca de vulnerabilidades. Las versiones obsoletas, como la versión 4.1 de Bash, son vulnerables a un exploit `shellshock`.

```shell-session
afsh4ck@kali$ grep "*sh$" /etc/passwd

root:x:0:0:root:/root:/bin/bash
mrb3n:x:1000:1000:mrb3n:/home/mrb3n:/bin/bash
bjones:x:1001:1001::/home/bjones:/bin/sh
administrator.ilfreight:x:1002:1002::/home/administrator.ilfreight:/bin/sh
backupsvc:x:1003:1003::/home/backupsvc:/bin/sh
cliff.moore:x:1004:1004::/home/cliff.moore:/bin/bash
logger:x:1005:1005::/home/logger:/bin/sh
shared:x:1006:1006::/home/shared:/bin/sh
stacey.jenkins:x:1007:1007::/home/stacey.jenkins:/bin/bash
htb-student:x:1008:1008::/home/htb-student:/bin/bash
```

Cada usuario en sistemas Linux está asignado a un grupo o grupos específicos y por lo tanto recibe privilegios especiales. Por ejemplo, si tenemos una carpeta nombrada `dev` solo para desarrolladores, un usuario debe estar asignado al grupo apropiado para acceder a esa carpeta. La información sobre los grupos disponibles la podemos encontrar en el archivo `/etc/group`, que nos muestra tanto el nombre del grupo como los nombres de usuario asignados.

**Grupos existentes**

```shell-session
afsh4ck@kali$ cat /etc/group

root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:
adm:x:4:syslog,htb-student
tty:x:5:syslog
disk:x:6:
lp:x:7:
mail:x:8:
news:x:9:
uucp:x:10:
man:x:12:
proxy:x:13:
kmem:x:15:
dialout:x:20:
fax:x:21:
voice:x:22:
cdrom:x:24:htb-student
floppy:x:25:
tape:x:26:
sudo:x:27:mrb3n,htb-student
audio:x:29:pulse
dip:x:30:htb-student
www-data:x:33:
...SNIP...
```

El archivo `/etc/group` enumera todos los grupos del sistema. Luego podemos usar el comando [getent](https://man7.org/linux/man-pages/man1/getent.1.html) para enumerar los miembros de cualquier grupo que nos interese.

```shell-session
afsh4ck@kali$ getent group sudo

sudo:x:27:mrb3n
```

También podemos comprobar qué usuarios tienen una carpeta en el `/home`directorio. Queremos enumerar cada uno de ellos para ver si alguno de los usuarios del sistema está almacenando datos confidenciales, archivos que contienen contraseñas. Deberíamos comprobar si los archivos como el archivo `.bash_history` son legibles y contienen comandos interesantes y buscar archivos de configuración. No es raro encontrar archivos que contienen credenciales que se pueden aprovechar para acceder a otros sistemas o incluso obtener acceso al entorno de Active Directory. También es importante comprobar las claves SSH de todos los usuarios, ya que podrían usarse para lograr la persistencia en el sistema, potencialmente para escalar privilegios o para ayudar con el pivoteo y el reenvío de puertos en la red interna. Como mínimo, verifique la caché ARP para ver a qué otros hosts se está accediendo y haga una referencia cruzada de estos con cualquier clave privada SSH utilizable.

```shell-session
afsh4ck@kali$ ls /home

administrator.ilfreight  bjones       htb-student  mrb3n   stacey.jenkins
backupsvc                cliff.moore  logger       shared
```

Por último, podemos buscar cualquier "objetivo fácil", como archivos de configuración y otros archivos que puedan contener información confidencial. Los archivos de configuración pueden contener una gran cantidad de información. Vale la pena buscar nombres de usuario, contraseñas y otros secretos en todos los archivos que terminan en extensiones como .conf y .config.

Si hemos recopilado alguna contraseña, deberíamos probarla ahora para todos los usuarios presentes en el sistema. La reutilización de contraseñas es algo habitual, así que ¡quizás tengamos suerte!

En Linux, existen muchos lugares diferentes donde se pueden almacenar dichos archivos, incluidos los sistemas de archivos montados. Un sistema de archivos montado es un sistema de archivos que está conectado a un directorio particular del sistema y al que se accede a través de ese directorio. Se pueden montar muchos sistemas de archivos, como ext4, NTFS y FAT32. Cada tipo de sistema de archivos tiene sus propias ventajas y desventajas. Por ejemplo, algunos sistemas de archivos solo pueden ser leídos por el sistema operativo, mientras que otros pueden ser leídos y escritos por el usuario. Los sistemas de archivos que pueden ser leídos y escritos por el usuario se denominan sistemas de archivos de lectura/escritura. Montar un sistema de archivos permite al usuario acceder a los archivos y carpetas almacenados en ese sistema de archivos. Para montar un sistema de archivos, el usuario debe tener privilegios de root. Una vez que se monta un sistema de archivos, el usuario con privilegios de root puede desmontarlo. Es posible que tengamos acceso a dichos sistemas de archivos y que encontremos allí información, documentación o aplicaciones confidenciales.

**Sistemas de archivos montados**

```shell-session
afsh4ck@kali$ df -h

Filesystem      Size  Used Avail Use% Mounted on
udev            1,9G     0  1,9G   0% /dev
tmpfs           389M  1,8M  388M   1% /run
/dev/sda5        20G  7,9G   11G  44% /
tmpfs           1,9G     0  1,9G   0% /dev/shm
tmpfs           5,0M  4,0K  5,0M   1% /run/lock
tmpfs           1,9G     0  1,9G   0% /sys/fs/cgroup
/dev/loop0      128K  128K     0 100% /snap/bare/5
/dev/loop1       62M   62M     0 100% /snap/core20/1611
/dev/loop2       92M   92M     0 100% /snap/gtk-common-themes/1535
/dev/loop4       55M   55M     0 100% /snap/snap-store/558
/dev/loop3      347M  347M     0 100% /snap/gnome-3-38-2004/115
/dev/loop5       47M   47M     0 100% /snap/snapd/16292
/dev/sda1       511M  4,0K  511M   1% /boot/efi
tmpfs           389M   24K  389M   1% /run/user/1000
/dev/sr0        3,6G  3,6G     0 100% /media/htb-student/Ubuntu 20.04.5 LTS amd64
/dev/loop6       50M   50M     0 100% /snap/snapd/17576
/dev/loop7       64M   64M     0 100% /snap/core20/1695
/dev/loop8       46M   46M     0 100% /snap/snap-store/599
/dev/loop9      347M  347M     0 100% /snap/gnome-3-38-2004/119
```

Cuando se desmonta un sistema de archivos, el sistema ya no puede acceder a él. Esto puede ocurrir por diversos motivos, como cuando se extrae un disco o cuando ya no se necesita un sistema de archivos. Otro motivo puede ser que los archivos, scripts, documentos y otra información importante no puedan ser montados y vistos por un usuario estándar. Por lo tanto, si podemos extender nuestros privilegios al `root`usuario, podríamos montar y leer estos sistemas de archivos nosotros mismos. Los sistemas de archivos desmontados se pueden ver de la siguiente manera:

**Sistemas de archivos desmontados**

```shell-session
afsh4ck@kali$ cat /etc/fstab | grep -v "#" | column -t

UUID=5bf16727-fcdf-4205-906c-0620aa4a058f  /          ext4  errors=remount-ro  0  1
UUID=BE56-AAE0                             /boot/efi  vfat  umask=0077         0  1
/swapfile                                  none       swap  sw                 0  0
```

En un sistema Linux, muchas carpetas y archivos se mantienen ocultos para que no sean evidentes y se evite la edición accidental. Existen muchas más razones por las que se mantienen ocultos estos archivos y carpetas que las mencionadas hasta ahora. Sin embargo, debemos poder localizar todos los archivos y carpetas ocultos porque a menudo pueden contener información confidencial, incluso si tenemos permisos de solo lectura.

**Todos los archivos ocultos**

```shell-session
afsh4ck@kali$ find / -type f -name ".*" -exec ls -l {} \; 2>/dev/null | grep htb-student

-rw-r--r-- 1 htb-student htb-student 3771 Nov 27 11:16 /home/htb-student/.bashrc
-rw-rw-r-- 1 htb-student htb-student 180 Nov 27 11:36 /home/htb-student/.wget-hsts
-rw------- 1 htb-student htb-student 387 Nov 27 14:02 /home/htb-student/.bash_history
-rw-r--r-- 1 htb-student htb-student 807 Nov 27 11:16 /home/htb-student/.profile
-rw-r--r-- 1 htb-student htb-student 0 Nov 27 11:31 /home/htb-student/.sudo_as_admin_successful
-rw-r--r-- 1 htb-student htb-student 220 Nov 27 11:16 /home/htb-student/.bash_logout
-rw-rw-r-- 1 htb-student htb-student 162 Nov 28 13:26 /home/htb-student/.notes
```

**Todos los directorios ocultos**

```shell-session
afsh4ck@kali$ find / -type d -name ".*" -ls 2>/dev/null

   684822      4 drwx------   3 htb-student htb-student     4096 Nov 28 12:32 /home/htb-student/.gnupg
   790793      4 drwx------   2 htb-student htb-student     4096 Okt 27 11:31 /home/htb-student/.ssh
   684804      4 drwx------  10 htb-student htb-student     4096 Okt 27 11:30 /home/htb-student/.cache
   790827      4 drwxrwxr-x   8 htb-student htb-student     4096 Okt 27 11:32 /home/htb-student/CVE-2021-3156/.git
   684796      4 drwx------  10 htb-student htb-student     4096 Okt 27 11:30 /home/htb-student/.config
   655426      4 drwxr-xr-x   3 htb-student htb-student     4096 Okt 27 11:19 /home/htb-student/.local
   524808      4 drwxr-xr-x   7 gdm         gdm             4096 Okt 27 11:19 /var/lib/gdm3/.cache
   544027      4 drwxr-xr-x   7 gdm         gdm             4096 Okt 27 11:19 /var/lib/gdm3/.config
   544028      4 drwxr-xr-x   3 gdm         gdm             4096 Aug 31 08:54 /var/lib/gdm3/.local
   524938      4 drwx------   2 colord      colord          4096 Okt 27 11:19 /var/lib/colord/.cache
     1408      2 dr-xr-xr-x   1 htb-student htb-student     2048 Aug 31 09:17 /media/htb-student/Ubuntu\ 20.04.5\ LTS\ amd64/.disk
   280101      4 drwxrwxrwt   2 root        root            4096 Nov 28 12:31 /tmp/.font-unix
   262364      4 drwxrwxrwt   2 root        root            4096 Nov 28 12:32 /tmp/.ICE-unix
   262362      4 drwxrwxrwt   2 root        root            4096 Nov 28 12:32 /tmp/.X11-unix
   280103      4 drwxrwxrwt   2 root        root            4096 Nov 28 12:31 /tmp/.Test-unix
   262830      4 drwxrwxrwt   2 root        root            4096 Nov 28 12:31 /tmp/.XIM-unix
   661820      4 drwxr-xr-x   5 root        root            4096 Aug 31 08:55 /usr/lib/modules/5.15.0-46-generic/vdso/.build-id
   666709      4 drwxr-xr-x   5 root        root            4096 Okt 27 11:18 /usr/lib/modules/5.15.0-52-generic/vdso/.build-id
   657527      4 drwxr-xr-x 170 root        root            4096 Aug 31 08:55 /usr/lib/debug/.build-id
```

Además, hay tres carpetas predeterminadas destinadas a los archivos temporales. Estas carpetas son visibles para todos los usuarios y se pueden leer. Además, se pueden encontrar allí registros temporales o salidas de scripts. Tanto `/tmp` y `/var/tmp` se utilizan para almacenar datos temporalmente. Sin embargo, la diferencia clave es el tiempo durante el cual se almacenan los datos en estos sistemas de archivos. El tiempo de retención de datos para `/var/tmp`es mucho más largo que el del `/tmp`directorio. De forma predeterminada, todos los archivos y datos almacenados en /var/tmp se conservan hasta 30 días. En cambio, en /tmp, los datos se eliminan automáticamente después de diez días.

Además, todos los archivos temporales almacenados en el directorio `/tmp` se eliminan inmediatamente cuando se reinicia el sistema. Por lo tanto, los programas utilizan el directorio `/var/tmp` para almacenar datos que deben conservarse temporalmente entre reinicios.

**Archivos temporales**

```shell-session
afsh4ck@kali$ ls -l /tmp /var/tmp /dev/shm

/dev/shm:
total 0

/tmp:
total 52
-rw------- 1 htb-student htb-student    0 Nov 28 12:32 config-err-v8LfEU
drwx------ 3 root        root        4096 Nov 28 12:37 snap.snap-store
drwx------ 2 htb-student htb-student 4096 Nov 28 12:32 ssh-OKlLKjlc98xh
<SNIP>
drwx------ 2 htb-student htb-student 4096 Nov 28 12:37 tracker-extract-files.1000
drwx------ 2 gdm         gdm         4096 Nov 28 12:31 tracker-extract-files.125

/var/tmp:
total 28
drwx------ 3 root root 4096 Nov 28 12:31 systemd-private-7b455e62ec09484b87eff41023c4ca53-colord.service-RrPcyi
drwx------ 3 root root 4096 Nov 28 12:31 systemd-private-7b455e62ec09484b87eff41023c4ca53-ModemManager.service-4Rej9e
...SNIP...
```

***

### Seguimos adelante

Hemos obtenido una idea inicial del terreno y (con suerte) algunos puntos de datos útiles o sensibles que pueden ayudarnos a escalar privilegios o incluso a movernos lateralmente en la red interna. A continuación, nos centraremos en los permisos y comprobaremos qué directorios, scripts, archivos binarios, etc. podemos leer y escribir con nuestros privilegios de usuario actuales.

Aunque en este módulo nos centraremos en la enumeración manual, vale la pena ejecutar el script [linPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS) en este punto en una evaluación del mundo real para que tengamos la mayor cantidad de datos posibles para analizar. A menudo podemos encontrar una solución fácil, pero tener este resultado a mano a veces puede revelar problemas matizados que nuestra enumeración manual pasó por alto.&#x20;

Sin embargo, deberíamos practicar nuestra enumeración manual tanto como sea posible y crear (y seguir ampliando) nuestra propia hoja de trucos de comandos clave (y alternativas para diferentes sistemas operativos Linux). Comenzaremos a desarrollar nuestro propio estilo, preferencia de comandos e incluso veremos algunas áreas que podemos comenzar a programar nosotros mismos. Las herramientas son geniales y tienen su lugar, pero donde muchas fallan es en la capacidad de realizar una tarea determinada cuando una herramienta falla o no podemos incorporarla al sistema.

***

### Caso práctico

```
SSH a 10.129.205.110 (ACADEMY-LLPE-SUDO)
Usuario " htb-student "
Contraseña " HTB_@cademy_stdnt! "
```

Enumere el entorno Linux y busque archivos interesantes que puedan contener datos confidenciales. Envíe la flag como respuesta.

```bash
$ sudo -l
[sudo] password for htb-student: 
Matching Defaults entries for htb-student on ubuntu:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User htb-student may run the following commands on ubuntu:
    (ALL, !root) /bin/ncdu
```

Es un archivo ejecutable. `ncdu` es una herramienta de línea de comandos para analizar el uso del disco, pero también puede tener vulnerabilidades si no se gestiona correctamente. Lo primero que podemos hacer es ver el menú de opciones o probar si hay alguna opción que permita ejecutar comandos adicionales o abrir un shell.

Como está en el directorio `/bin` podemos ejecutarla directamente desde la terminal:

```shell-session
htb-student@ubuntu:/$ ncdu --help
ncdu <options> <directory>

  -h,--help                  This help message
  -q                         Quiet mode, refresh interval 2 seconds
  -v,-V,--version            Print version
  -x                         Same filesystem
  -e                         Enable extended information
  -r                         Read only
  -o FILE                    Export scanned directory to FILE
  -f FILE                    Import scanned directory from FILE
  -0,-1,-2                   UI to use when scanning (0=none,2=full ncurses)
  --si                       Use base 10 (SI) prefixes instead of base 2
  --exclude PATTERN          Exclude files that match PATTERN
  -X, --exclude-from FILE    Exclude files that match any pattern in FILE
  -L, --follow-symlinks      Follow symbolic links (excluding directories)
  --exclude-caches           Exclude directories containing CACHEDIR.TAG
  --confirm-quit             Confirm quitting ncdu
  --color SCHEME             Set color scheme
```

Buscando en GTFOBins podemos probar alguna de las técnicas que menciona:

{% embed url="<https://gtfobins.github.io/gtfobins/ncdu/>" %}

Siempre que nos salga algo que podemos ejecutar con el comando `sudo -l` el primer paso que deberíamos hacer siempre es buscarlo en GTFOBins.

De igual manera podríamos probar a buscar archivos que contengan la cadena '`HTB{}`' que es el formato de las flags de Hack the Box:

```bash
$ grep -r -l 'HTB{' / 2>/dev/null           
/usr/lib/int-check.sh
```

Al abrir este archivo efectivamente nos encontramos la flag:

```bash
$ cat /usr/lib/int-check.sh
HTB{1nt3rn4l_5cr1p7_l34k}
```

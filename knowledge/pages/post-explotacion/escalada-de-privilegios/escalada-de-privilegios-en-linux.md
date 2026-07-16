
# Escalada de privilegios en Linux

## <mark style="color:purple;">Introducción a la escalada de privilegios en Linux</mark>

***

La cuenta raíz en los sistemas Linux proporciona acceso administrativo completo al sistema operativo. Durante una evaluación, es posible que obtenga un shell con pocos privilegios en un host Linux y deba realizar una escalada de privilegios a la cuenta raíz. Si comprometemos por completo el host, podremos capturar el tráfico y acceder a archivos confidenciales, que pueden usarse para acceder más dentro del entorno. Además, si la máquina Linux está unida a un dominio, podemos obtener el hash NTLM y comenzar a enumerar y atacar Active Directory.

***

## <mark style="color:purple;">Enumeración</mark>

La enumeración es la clave para la escalada de privilegios. Existen varios scripts auxiliares (como [LinEnum](https://github.com/rebootuser/LinEnum) ) para ayudar con la enumeración. Sin embargo, también es importante comprender qué información buscar y poder realizar la enumeración manualmente. Cuando obtenga acceso inicial al host a través del shell, es importante verificar varios detalles clave.

### Versión del S.O

Conocer la distribución (Ubuntu, Debian, FreeBSD, Fedora, SUSE, Red Hat, CentOS, etc.) le dará una idea de los tipos de herramientas que pueden estar disponibles. Esto también identificará la versión del sistema operativo para la que puede haber exploits públicos disponibles.

### Versión del Kernel

&#x20;Al igual que con la versión del sistema operativo, puede haber exploits públicos que tengan como objetivo una vulnerabilidad en una versión específica del kernel. Los exploits del kernel pueden provocar inestabilidad del sistema o incluso un bloqueo total. Tenga cuidado al ejecutarlos en cualquier sistema de producción y asegúrese de comprender completamente el exploit y las posibles ramificaciones antes de ejecutar uno.

```bash
afsh4ck@kali$ uname -a
Linux ubuntu 5.4.0-148-generic #165-Ubuntu SMP Tue Apr 18 08:53:12 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```

### Servicios corriendo

Es importante saber qué servicios se están ejecutando en el host, especialmente aquellos que se ejecutan como root. Un servicio mal configurado o vulnerable que se ejecute como root puede ser una victoria fácil para la escalada de privilegios. Se han descubierto fallas en muchos servicios comunes como Nagios, Exim, Samba, ProFTPd, etc. Existen PoC de explotación pública para muchos de ellos, como CVE-2016-9566, una falla de escalada de privilegios local en Nagios Core < 4.2.4.

**Lista de procesos actuales**

```shell-session
afsh4ck@kali$ ps aux | grep root

root         1  1.3  0.1  37656  5664 ?        Ss   23:26   0:01 /sbin/init
root         2  0.0  0.0      0     0 ?        S    23:26   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        S    23:26   0:00 [ksoftirqd/0]
root         4  0.0  0.0      0     0 ?        S    23:26   0:00 [kworker/0:0]
root         5  0.0  0.0      0     0 ?        S<   23:26   0:00 [kworker/0:0H]
root         6  0.0  0.0      0     0 ?        S    23:26   0:00 [kworker/u8:0]
root         7  0.0  0.0      0     0 ?        S    23:26   0:00 [rcu_sched]
root         8  0.0  0.0      0     0 ?        S    23:26   0:00 [rcu_bh]
root         9  0.0  0.0      0     0 ?        S    23:26   0:00 [migration/0]

<SNIP>
```

### Paquetes instalados y versiones

Al igual que con los servicios en ejecución, es importante comprobar si hay paquetes desactualizados o vulnerables que puedan aprovecharse fácilmente para la escalada de privilegios. Un ejemplo es Screen, que es un multiplexor de terminal común (similar a tmux). Le permite iniciar una sesión y abrir muchas ventanas o terminales virtuales en lugar de abrir varias sesiones de terminal. La versión 4.05.00 de Screen sufre una vulnerabilidad de escalada de privilegios que puede aprovecharse fácilmente para escalar privilegios.

### Usuarios logueados

Saber qué otros usuarios están conectados al sistema y qué están haciendo puede brindar mayor información sobre posibles movimientos laterales locales y rutas de escalada de privilegios.

**Lista de procesos actuales**

```shell-session
afsh4ck@kali]$ ps au

USER       		PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root      		1256  0.0  0.1  65832  3364 tty1     Ss   23:26   0:00 /bin/login --
cliff.moore     1322  0.0  0.1  22600  5160 tty1     S    23:26   0:00 -bash
shared     		1367  0.0  0.1  22568  5116 pts/0    Ss   23:27   0:00 -bash
root      		1384  0.0  0.1  52700  3812 tty1     S    23:29   0:00 sudo su
root      		1385  0.0  0.1  52284  3448 tty1     S    23:29   0:00 su
root      		1386  0.0  0.1  21224  3764 tty1     S+   23:29   0:00 bash
shared     		1397  0.0  0.1  37364  3428 pts/0    R+   23:30   0:00 ps au
```

### Directorios de usuario

¿Se puede acceder a los directorios personales de otros usuarios? Las carpetas personales de los usuarios también pueden contener claves SSH que se pueden utilizar para acceder a otros sistemas o scripts y archivos de configuración que contienen credenciales. No es raro encontrar archivos que contienen credenciales que se pueden utilizar para acceder a otros sistemas o incluso para ingresar al entorno de Active Directory.

**Enumeración del directorio /home**

```shell-session
afsh4ck@kali$ ls /home

backupsvc  bob.jones  cliff.moore  logger  mrb3n  shared  stacey.jenkins
```

Podemos revisar directorios de usuarios individuales y verificar si archivos como el `.bash_history` si son legibles y contienen comandos interesantes, buscar archivos de configuración y verificar si podemos obtener copias de las claves SSH de un usuario.

**Contenido del directorio de inicio del usuario**

```shell-session
afsh4ck@kali$ ls -la /home/stacey.jenkins/

total 32
drwxr-xr-x 3 stacey.jenkins stacey.jenkins 4096 Aug 30 23:37 .
drwxr-xr-x 9 root           root           4096 Aug 30 23:33 ..
-rw------- 1 stacey.jenkins stacey.jenkins   41 Aug 30 23:35 .bash_history
-rw-r--r-- 1 stacey.jenkins stacey.jenkins  220 Sep  1  2015 .bash_logout
-rw-r--r-- 1 stacey.jenkins stacey.jenkins 3771 Sep  1  2015 .bashrc
-rw-r--r-- 1 stacey.jenkins stacey.jenkins   97 Aug 30 23:37 config.json
-rw-r--r-- 1 stacey.jenkins stacey.jenkins  655 May 16  2017 .profile
drwx------ 2 stacey.jenkins stacey.jenkins 4096 Aug 30 23:35 .ssh
```

Si encuentra una clave SSH para su usuario actual, podría usarla para abrir una sesión SSH en el host (si SSH está expuesto externamente) y obtener una sesión estable y completamente interactiva. Las claves SSH también podrían aprovecharse para acceder a otros sistemas dentro de la red. Como mínimo, verifique la caché ARP para ver a qué otros hosts se está accediendo y haga una referencia cruzada de estas claves con cualquier clave privada SSH que se pueda utilizar.

**Contenido del directorio SSH**

```shell-session
afsh4ck@kali]$ ls -l ~/.ssh

total 8
-rw------- 1 mrb3n mrb3n 1679 Aug 30 23:37 id_rsa
-rw-r--r-- 1 mrb3n mrb3n  393 Aug 30 23:37 id_rsa.pub
```

### **Historial de Bash**

También es importante comprobar el historial de bash de un usuario, ya que puede estar pasando contraseñas como argumento en la línea de comandos, trabajando con repositorios git, configurando tareas cron y más. Revisar lo que ha estado haciendo el usuario puede brindarle una idea considerable sobre el tipo de servidor en el que se encuentra y darle una pista sobre las rutas de escalada de privilegios.

```shell-session
afsh4ck@kali$ history

    1  id
    2  cd /home/cliff.moore
    3  exit
    4  touch backup.sh
    5  tail /var/log/apache2/error.log
    6  ssh ec2-user@dmz02.inlanefreight.local
    7  history
```

### Privilegios Sudo

¿Puede el usuario ejecutar cualquier comando como otro usuario o como root? Si no tiene credenciales para el usuario, es posible que no sea posible aprovechar los permisos de sudo. Sin embargo, a menudo las entradas de sudoer incluyen `NOPASSWD`, lo que significa que el usuario puede ejecutar el comando especificado sin que se le solicite una contraseña. No todos los comandos, incluso los que podemos ejecutar como root, darán lugar a una escalada de privilegios. No es raro obtener acceso como un usuario con privilegios sudo completos, lo que significa que puede ejecutar cualquier comando como root. Emitir un comando`sudo su` simple le otorgará inmediatamente una sesión de root.

**Sudo - Lista de privilegios del usuario**

```shell-session
afsh4ck@kali$ sudo -l

Matching Defaults entries for sysadm on NIX02:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User sysadm may run the following commands on NIX02:
    (root) NOPASSWD: /usr/sbin/tcpdump
```

### Archivos de configuración

Los archivos de configuración pueden contener una gran cantidad de información. Vale la pena buscar nombres de usuario, contraseñas y otros secretos en todos los archivos que terminan en extensiones como `.conf` y `.config`

### Archivo Shadow legible

Si el archivo `/etc/shadow` es legible, podrá recopilar los hashes de contraseñas de todos los usuarios que tengan una contraseña configurada. Si bien esto no garantiza un mayor acceso, estos hashes pueden estar sujetos a un ataque de fuerza bruta sin conexión para recuperar la contraseña en texto simple.

{% content-ref url="/pages/TRZKCtXVALGrKxJ5dmfE" %}
[Cracking de Contraseñas](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/cracking-de-contrasenas.md)
{% endcontent-ref %}

### Password Hashes en /etc/passwd

En ocasiones, verás hashes de contraseñas directamente en el archivo `/etc/passwd`. Todos los usuarios pueden leer este archivo y, al igual que con los hashes en el archivo `shadow`, estos pueden estar sujetos a un ataque de descifrado de contraseñas sin conexión. Esta configuración, si bien no es común, a veces se puede ver en dispositivos integrados y enrutadores.

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
<...SNIP...>
dnsmasq:x:109:65534:dnsmasq,,,:/var/lib/misc:/bin/false
sshd:x:110:65534::/var/run/sshd:/usr/sbin/nologin
mrb3n:x:1000:1000:mrb3n,,,:/home/mrb3n:/bin/bash
colord:x:111:118:colord colour management daemon,,,:/var/lib/colord:/bin/false
backupsvc:x:1001:1001::/home/backupsvc:
bob.jones:x:1002:1002::/home/bob.jones:
cliff.moore:x:1003:1003::/home/cliff.moore:
logger:x:1004:1004::/home/logger:
shared:x:1005:1005::/home/shared:
stacey.jenkins:x:1006:1006::/home/stacey.jenkins:
sysadm:$6$vdH7vuQIv6anIBWg$Ysk.UZzI7WxYUBYt8WRIWF0EzWlksOElDE0HLYinee38QI1A.0HW7WZCrUhZ9wwDz13bPpkTjNuRoUGYhwFE11:1007:1007::/home/sysadm:
```

### Cron Jobs

Los trabajos cron en sistemas Linux son similares a las tareas programadas de Windows. A menudo se configuran para realizar tareas de mantenimiento y copia de seguridad. Junto con otras configuraciones incorrectas, como rutas relativas o permisos débiles, pueden aprovecharse para aumentar los privilegios cuando se ejecuta el trabajo cron programado.

```shell-session
afsh4ck@kali$ ls -la /etc/cron.daily/

total 60
drwxr-xr-x  2 root root 4096 Aug 30 23:49 .
drwxr-xr-x 93 root root 4096 Aug 30 23:47 ..
-rwxr-xr-x  1 root root  376 Mar 31  2016 apport
-rwxr-xr-x  1 root root 1474 Sep 26  2017 apt-compat
-rwx--x--x  1 root root  379 Aug 30 23:49 backup
-rwxr-xr-x  1 root root  355 May 22  2012 bsdmainutils
-rwxr-xr-x  1 root root 1597 Nov 27  2015 dpkg
-rwxr-xr-x  1 root root  372 May  6  2015 logrotate
-rwxr-xr-x  1 root root 1293 Nov  6  2015 man-db
-rwxr-xr-x  1 root root  539 Jul 16  2014 mdadm
-rwxr-xr-x  1 root root  435 Nov 18  2014 mlocate
-rwxr-xr-x  1 root root  249 Nov 12  2015 passwd
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder
-rwxr-xr-x  1 root root 3449 Feb 26  2016 popularity-contest
-rwxr-xr-x  1 root root  214 May 24  2016 update-notifier-common
```

### Sistemas de archivos desmontados y unidades adicionales

Si descubre y puede montar una unidad adicional o un sistema de archivos desmontado, es posible que encuentre archivos confidenciales, contraseñas o copias de seguridad que se puedan aprovechar para aumentar los privilegios.

**Sistemas de archivos y unidades adicionales**

```shell-session
afsh4ck@kali$ lsblk

NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0   30G  0 disk 
├─sda1   8:1    0   29G  0 part /
├─sda2   8:2    0    1K  0 part 
└─sda5   8:5    0  975M  0 part [SWAP]
sr0     11:0    1  848M  0 rom  
```

### Permisos SETUID y SETGID

Los archivos binarios se configuran con estos permisos para permitir que un usuario ejecute un comando como root, sin tener que otorgarle acceso de nivel root. Muchos archivos binarios contienen funciones que se pueden aprovechar para obtener un shell root.

### Directorios con permisos de escritura

Es importante descubrir qué directorios son editables si necesita descargar herramientas al sistema. Puede descubrir un directorio editable donde un trabajo cron coloca archivos, lo que proporciona una idea de la frecuencia con la que se ejecuta el trabajo cron y podría usarse para elevar privilegios si el script que ejecuta el trabajo cron también es editable.

**Encontrar directorios en los que se pueda escribir**

```shell-session
afsh4ck@kali$ find / -path /proc -prune -o -type d -perm -o+w 2>/dev/null

/dmz-backups
/tmp
/tmp/VMwareDnD
/tmp/.XIM-unix
/tmp/.Test-unix
/tmp/.X11-unix
/tmp/systemd-private-8a2c51fcbad240d09578916b47b0bb17-systemd-timesyncd.service-TIecv0/tmp
/tmp/.font-unix
/tmp/.ICE-unix
/proc
/dev/mqueue
/dev/shm
/var/tmp
/var/tmp/systemd-private-8a2c51fcbad240d09578916b47b0bb17-systemd-timesyncd.service-hm6Qdl/tmp
/var/crash
/run/lock
```

### Archivos con permisos de escritura

¿Hay scripts o archivos de configuración que puedan ser modificados por todo el mundo? Si bien alterar los archivos de configuración puede ser extremadamente destructivo, puede haber casos en los que una modificación menor pueda abrir más acceso. Además, cualquier script que se ejecute como root mediante trabajos de cron se puede modificar ligeramente para agregar un comando.

**Buscar archivos editables**

```shell-session
afsh4ck@kali$ find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null

/etc/cron.daily/backup
/dmz-backups/backup.sh
/proc
/sys/fs/cgroup/memory/init.scope/cgroup.event_control

<SNIP>

/home/backupsvc/backup.sh

<SNIP>
```

***

## <mark style="color:purple;">Cheatsheet</mark> <a href="#cheatsheet" id="cheatsheet"></a>

| **Comando**                                                                         | **Descripción**                                                 |
| ----------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `ssh htb-student@<target IP>`                                                       | SSH al objetivo del laboratorio                                 |
| `ps aux \| grep root`                                                               | Ver procesos ejecutándose como root                             |
| `ps au`                                                                             | Ver usuarios registrados                                        |
| `ls /home`                                                                          | Ver directorios personales de usuarios                          |
| `ls -l ~/.ssh`                                                                      | Comprobar las claves SSH para el usuario actual                 |
| `history`                                                                           | Verificar el historial de Bash del usuario actual               |
| `sudo -l`                                                                           | ¿Puede el usuario ejecutar algo como otro usuario?              |
| `ls -la /etc/cron.daily`                                                            | Comprobar trabajos cron diarios                                 |
| `lsblk`                                                                             | Comprobar si hay sistemas de archivos o unidades desmontados    |
| `find / -path /proc -prune -o -type d -perm -o+w 2>/dev/null`                       | Encuentre directorios que permitan la escritura a nivel mundial |
| `find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null`                       | Buscar archivos que puedan ser escritos por todo el mundo       |
| `uname -a`                                                                          | Comprueba la versión del Kernel                                 |
| `cat /etc/lsb-release`                                                              | Compruebe la versión del sistema operativo                      |
| `gcc kernel_expoit.c -o kernel_expoit`                                              | Compilar un exploit escrito en C                                |
| `screen -v`                                                                         | Compruebe la versión instalada de`Screen`                       |
| `./pspy64 -pf -i 1000`                                                              | Ver procesos en ejecución con `pspy`                            |
| `find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null`                     | Buscar binarios con el bit SUID establecido                     |
| `find / -user root -perm -6000 -exec ls -ldb {} \; 2>/dev/null`                     | Buscar binarios con el bit SETGID establecido                   |
| `sudo /usr/sbin/tcpdump -ln -i ens192 -w /dev/null -W 1 -G 1 -z /tmp/.test -Z root` | Priv esc con`tcpdump`                                           |
| `echo $PATH`                                                                        | Verifique el contenido de la variable PATH del usuario actual   |
| `PATH=.:${PATH}`                                                                    | Añade un `.` al comienzo de la RUTA del usuario actual          |
| `find / ! -path "*/proc/*" -iname "*config*" -type f 2>/dev/null`                   | Buscar archivos de configuración                                |
| `ldd /bin/ls`                                                                       | Ver los objetos compartidos requeridos por un binario           |
| `sudo LD_PRELOAD=/tmp/root.so /usr/sbin/apache2 restart`                            | Escalar privilegios usando`LD_PRELOAD`                          |
| `readelf -d payroll \| grep PATH`                                                   | Comprobar el RUNPATH de un binario                              |
| `gcc src.c -fPIC -shared -o /development/libshared.so`                              | Compiló una biblioteca compartida                               |
| `lxd init`                                                                          | Iniciar el proceso de inicialización de LXD                     |
| `lxc image import alpine.tar.gz alpine.tar.gz.root --alias alpine`                  | Importar una imagen local                                       |
| `lxc init alpine r00t -c security.privileged=true`                                  | Iniciar un contenedor LXD privilegiado                          |
| `lxc config device add r00t mydev disk source=/ path=/mnt/root recursive=true`      | Montar el sistema de archivos del host en un contenedor         |
| `lxc start r00t`                                                                    | Iniciar el contenedor                                           |
| `showmount -e 10.129.2.12`                                                          | Mostrar la lista de exportaciones de NFS                        |
| `sudo mount -t nfs 10.129.2.12:/tmp /mnt`                                           | Montar un recurso compartido NFS localmente                     |
| `tmux -S /shareds new -s debugsess`                                                 | Crear un socket de sesión `tmux` compartido                     |
| `./lynis audit system`                                                              | Realizar una auditoría del sistema con`Lynis`                   |

***

## Seguimos adelante

Como hemos visto, existen varias técnicas de enumeración manual que podemos llevar a cabo para obtener información que sirva de base para diversos ataques de escalada de privilegios. Existe una variedad de técnicas que se pueden aprovechar para realizar una escalada de privilegios local en Linux, que abordaremos en las siguientes secciones.

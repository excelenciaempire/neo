
# Enumeración de servicios y componentes internos

Ahora que hemos investigado el entorno, nos hemos familiarizado con él y hemos descubierto todo lo que hemos podido sobre los permisos de usuario y grupo en relación con los archivos, scripts, archivos binarios, directorios, etc., daremos un paso más y analizaremos más a fondo los aspectos internos del sistema operativo anfitrión. En esta fase, enumeraremos lo siguiente, que ayudará a informar sobre muchos de los ataques que se analizarán en las secciones posteriores de este módulo.

* ¿Qué servicios y aplicaciones están instalados?
* ¿Qué servicios están en ejecución?
* ¿Qué enchufes están en uso?
* ¿Qué usuarios, administradores y grupos existen en el sistema?
* ¿Quién ha iniciado sesión actualmente? ¿Qué usuarios han iniciado sesión recientemente?
* ¿Qué políticas de contraseñas, si las hay, se aplican en el host?
* ¿El host está unido a un dominio de Active Directory?
* ¿Qué tipos de información interesante podemos encontrar en los archivos de historial, registro y copia de seguridad?
* ¿Qué archivos se han modificado recientemente y con qué frecuencia? ¿Existen patrones interesantes en la modificación de archivos que podrían indicar que se está utilizando un trabajo de cron que podríamos piratear?
* Información de dirección IP actual
* ¿Hay algo interesante en e archivol `/etc/hosts`?
* ¿Existen conexiones de red interesantes con otros sistemas en la red interna o incluso fuera de la red?
* ¿Qué herramientas están instaladas en el sistema que podamos aprovechar? (Netcat, Perl, Python, Ruby, Nmap, tcpdump, gcc, etc.)
* ¿Podemos acceder al archivo `bash_history` para cualquier usuario y podemos descubrir algo interesante de su historial de línea de comandos registrado, como contraseñas?
* ¿Hay algún trabajo Cron ejecutándose en el sistema que podamos secuestrar?

En este momento, también queremos recopilar la mayor cantidad posible de información de red. ¿Cuál es nuestra dirección IP actual? ¿El sistema tiene otras interfaces y, por lo tanto, podría usarse para pasar a otra subred que antes no era accesible desde nuestro host de ataque? Lo hacemos con el comando `ip a` o `ifconfig`, pero este comando a veces no funcionará en ciertos sistemas si el paquete [net-tools](https://packages.ubuntu.com/search?keywords=net-tools) no está presente.

***

## <mark style="color:purple;">Internals</mark>

Cuando hablamos de `internals`, nos referimos a la configuración interna y la forma de trabajar, incluidos los procesos integrados diseñados para realizar tareas específicas. Por lo tanto, comenzamos con las interfaces a través de las cuales nuestro sistema de destino puede comunicarse.

### **Interfaces de red**

```bash
afsh4ck@kali$ ip a

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:50:56:b9:ed:2a brd ff:ff:ff:ff:ff:ff
    inet 10.129.203.168/16 brd 10.129.255.255 scope global dynamic ens192
       valid_lft 3092sec preferred_lft 3092sec
    inet6 dead:beef::250:56ff:feb9:ed2a/64 scope global dynamic mngtmpaddr 
       valid_lft 86400sec preferred_lft 14400sec
    inet6 fe80::250:56ff:feb9:ed2a/64 scope link 
       valid_lft forever preferred_lft forever
```

¿Hay algo interesante en el archivo `/etc/hosts`?

### **Hosts**

```bash
afsh4ck@kali$ cat /etc/hosts

127.0.0.1 localhost
127.0.1.1 nixlpe02
# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

También puede resultar útil comprobar la última hora de inicio de sesión de cada usuario para intentar ver cuándo suelen iniciar sesión en el sistema y con qué frecuencia. Esto puede darnos una idea de cuán ampliamente se utiliza este sistema, lo que puede abrir la posibilidad de más configuraciones erróneas o directorios o historiales de comandos "desordenados".

### **Último inicio de sesión del usuario**

```bash
afsh4ck@kali$ lastlog

Username         Port     From             Latest
root                                       **Never logged in**
daemon                                     **Never logged in**
bin                                        **Never logged in**
sys                                        **Never logged in**
sync                                       **Never logged in**
...SNIP...
systemd-coredump                           **Never logged in**
mrb3n            pts/1    10.10.14.15      Tue Aug  2 19:33:16 +0000 2022
lxd                                        **Never logged in**
bjones                                     **Never logged in**
administrator.ilfreight                           **Never logged in**
backupsvc                                  **Never logged in**
cliff.moore      pts/0    127.0.0.1        Tue Aug  2 19:32:29 +0000 2022
logger                                     **Never logged in**
shared                                     **Never logged in**
stacey.jenkins   pts/0    10.10.14.15      Tue Aug  2 18:29:15 +0000 2022
htb-student      pts/0    10.10.14.15      Wed Aug  3 13:37:22 +0000 2022                          
```

Además, veamos si hay alguien más en el sistema con nosotros. Hay algunas formas de hacerlo, como el comando `who`. El comando  `finger` funcionará para mostrar esta información en algunos sistemas Linux. Podemos ver que el usuario `cliff.moore` está conectado al sistema con nosotros.

### **Usuarios registrados**

```bash
afsh4ck@kali$ who

 12:27:21 up 1 day, 16:55,  1 user,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
cliff.mo pts/0    10.10.14.16      Tue19   40:54m  0.02s  0.02s -bash
```

También es importante comprobar el historial de bash de un usuario, ya que puede estar pasando contraseñas como argumento en la línea de comandos, trabajando con repositorios git, configurando tareas cron y más. Revisar lo que ha estado haciendo el usuario puede brindarle una idea considerable sobre el tipo de servidor en el que se encuentra y darle una pista sobre las rutas de escalada de privilegios.

### **Historial de comandos**

```bash
afsh4ck@kali$ history

    1  id
    2  cd /home/cliff.moore
    3  exit
    4  touch backup.sh
    5  tail /var/log/apache2/error.log
    6  ssh ec2-user@dmz02.inlanefreight.local
    7  history
```

En ocasiones también podemos encontrar archivos de historial especiales creados por scripts o programas. Esto se puede encontrar, entre otros, en scripts que monitorean ciertas actividades de los usuarios y verifican actividades sospechosas.

### **Cómo encontrar archivos de historial**

```bash
afsh4ck@kali$ find / -type f \( -name *_hist -o -name *_history \) -exec ls -l {} \; 2>/dev/null

-rw------- 1 htb-student htb-student 387 Nov 27 14:02 /home/htb-student/.bash_history
```

También es una buena idea comprobar si hay trabajos cron en el sistema. Los trabajos cron en los sistemas Linux son similares a las tareas programadas de Windows. A menudo se configuran para realizar tareas de mantenimiento y copia de seguridad. Junto con otras configuraciones incorrectas, como rutas relativas o permisos débiles, pueden aprovecharse para aumentar los privilegios cuando se ejecuta el trabajo cron programado.

### **Cron**

```bash
afsh4ck@kali$ ls -la /etc/cron.daily/

total 48
drwxr-xr-x  2 root root 4096 Aug  2 17:36 .
drwxr-xr-x 96 root root 4096 Aug  2 19:34 ..
-rwxr-xr-x  1 root root  376 Dec  4  2019 apport
-rwxr-xr-x  1 root root 1478 Apr  9  2020 apt-compat
-rwxr-xr-x  1 root root  355 Dec 29  2017 bsdmainutils
-rwxr-xr-x  1 root root 1187 Sep  5  2019 dpkg
-rwxr-xr-x  1 root root  377 Jan 21  2019 logrotate
-rwxr-xr-x  1 root root 1123 Feb 25  2020 man-db
-rw-r--r--  1 root root  102 Feb 13  2020 .placeholder
-rwxr-xr-x  1 root root 4574 Jul 18  2019 popularity-contest
-rwxr-xr-x  1 root root  214 Apr  2  2020 update-notifier-common
```

El [sistema de archivos proc](https://man7.org/linux/man-pages/man5/proc.5.html) ( `proc`/ `procfs`) es un sistema de archivos particular de Linux que contiene información sobre los procesos del sistema, el hardware y otra información del sistema. Es la forma principal de acceder a la información de los procesos y se puede utilizar para ver y modificar la configuración del núcleo. Es virtual y no existe como un sistema de archivos real, sino que el núcleo lo genera dinámicamente. Se puede utilizar para buscar información del sistema, como el estado de los procesos en ejecución, los parámetros del núcleo, la memoria del sistema y los dispositivos. También establece ciertos parámetros del sistema, como la prioridad del proceso, la programación y la asignación de memoria.

### **Proc**

```bash
afsh4ck@kali$ find /proc -name cmdline -exec cat {} \; 2>/dev/null | tr " " "\n"

...SNIP...
startups/usr/lib/packagekit/packagekitd/usr/lib/packagekit/packagekitd/usr/lib/packagekit/packagekitd/usr/lib/packagekit/packagekitdroot@10.129.14.200sshroot@10.129.14.200sshd:
htb-student
[priv]sshd:
htb-student
[priv]/usr/bin/ssh-agent-D-a/run/user/1000/keyring/.ssh/usr/bin/ssh-agent-D-a/run/user/1000/keyring/.sshsshd:
htb-student@pts/2sshd:
```

***

## <mark style="color:purple;">Servicios</mark>

Si se trata de un sistema Linux un poco más antiguo, aumenta la probabilidad de que podamos encontrar paquetes instalados que puedan tener ya al menos una vulnerabilidad. Sin embargo, las versiones actuales de las distribuciones Linux también pueden tener paquetes o software más antiguos instalados que puedan tener dichas vulnerabilidades. Por ello, en breve veremos un método que nos ayudará a detectar paquetes potencialmente peligrosos. Para ello, primero debemos crear una lista de paquetes instalados con los que trabajar.

### **Paquetes instalados**

```bash
afsh4ck@kali$ apt list --installed | tr "/" " " | cut -d" " -f1,3 | sed 's/[0-9]://g' | tee -a installed_pkgs.list

Listing...                                                 
accountsservice-ubuntu-schemas 0.0.7+17.10.20170922-0ubuntu1                                                          
accountsservice 0.6.55-0ubuntu12~20.04.5                   
acl 2.2.53-6                                               
acpi-support 0.143                                         
acpid 2.0.32-1ubuntu1                                      
adduser 3.118ubuntu2                                       
adwaita-icon-theme 3.36.1-2ubuntu0.20.04.2                 
alsa-base 1.0.25+dfsg-0ubuntu5                             
alsa-topology-conf 1.2.2-1                                                                                            
alsa-ucm-conf 1.2.2-1ubuntu0.13                            
alsa-utils 1.2.2-1ubuntu2.1                                                                                           
amd64-microcode 3.20191218.1ubuntu1
anacron 2.3-29
apg 2.2.3.dfsg.1-5
app-install-data-partner 19.04
apparmor 2.13.3-7ubuntu5.1
apport-gtk 2.20.11-0ubuntu27.24
apport-symptoms 0.23
apport 2.20.11-0ubuntu27.24
appstream 0.12.10-2
apt-config-icons-hidpi 0.12.10-2
apt-config-icons 0.12.10-2
apt-utils 2.0.9
...SNIP...
```

### **Versión de sudo**

También es una buena idea verificar si la versión de `sudo` instalada en el sistema es vulnerable a algún exploit heredado o reciente.

```bash
afsh4ck@kali$ sudo -V

Sudo version 1.8.31
Sudoers policy plugin version 1.8.31
Sudoers file grammar version 46
Sudoers I/O plugin version 1.8.31
```

### **Binarios**

En ocasiones también puede ocurrir que no se instalen paquetes directos en el sistema, sino programas compilados en forma de binarios. Éstos no requieren instalación y pueden ser ejecutados directamente por el propio sistema.

```bash
afsh4ck@kali$ ls -l /bin /usr/bin/ /usr/sbin/

lrwxrwxrwx 1 root root     7 Oct 27 11:14 /bin -> usr/bin

/usr/bin/:
total 175160
-rwxr-xr-x 1 root root       31248 May 19  2020  aa-enabled
-rwxr-xr-x 1 root root       35344 May 19  2020  aa-exec
-rwxr-xr-x 1 root root       22912 Apr 14  2021  aconnect
-rwxr-xr-x 1 root root       19016 Nov 28  2019  acpi_listen
-rwxr-xr-x 1 root root        7415 Oct 26  2021  add-apt-repository
-rwxr-xr-x 1 root root       30952 Feb  7  2022  addpart
lrwxrwxrwx 1 root root          26 Oct 20  2021  addr2line -> x86_64-linux-gnu-addr2line
...SNIP...

/usr/sbin/:
total 32500
-rwxr-xr-x 1 root root      3068 Mai 19  2020 aa-remove-unknown
-rwxr-xr-x 1 root root      8839 Mai 19  2020 aa-status
-rwxr-xr-x 1 root root       139 Jun 18  2019 aa-teardown
-rwxr-xr-x 1 root root     14728 Feb 25  2020 accessdb
-rwxr-xr-x 1 root root     60432 Nov 28  2019 acpid
-rwxr-xr-x 1 root root      3075 Jul  4 18:20 addgnupghome
lrwxrwxrwx 1 root root         7 Okt 27 11:14 addgroup -> adduser
-rwxr-xr-x 1 root root       860 Dez  7  2019 add-shell
-rwxr-xr-x 1 root root     37785 Apr 16  2020 adduser
-rwxr-xr-x 1 root root     69000 Feb  7  2022 agetty
-rwxr-xr-x 1 root root      5576 Jul 31  2015 alsa
-rwxr-xr-x 1 root root      4136 Apr 14  2021 alsabat-test
-rwxr-xr-x 1 root root    118176 Apr 14  2021 alsactl
-rwxr-xr-x 1 root root     26489 Apr 14  2021 alsa-info
-rwxr-xr-x 1 root root     39088 Jul 16  2019 anacron
...SNIP...
```

### **GTFOBins**

[GTFObins](https://gtfobins.github.io/) ofrece una excelente plataforma que incluye una lista de archivos binarios que pueden explotarse potencialmente para aumentar nuestros privilegios en el sistema de destino. Con el siguiente resumen, podemos comparar los archivos binarios existentes con los de GTFObins para ver qué archivos binarios debemos investigar más adelante.

```bash
afsh4ck@kali$ for i in $(curl -s https://gtfobins.github.io/ | html2text | cut -d" " -f1 | sed '/^[[:space:]]*$/d');do if grep -q "$i" installed_pkgs.list;then echo "Check GTFO for: $i";fi;done

Check GTFO for: ab                                         
Check GTFO for: apt                                        
Check GTFO for: ar                                         
Check GTFO for: as         
Check GTFO for: ash                                        
Check GTFO for: aspell                                     
Check GTFO for: at     
Check GTFO for: awk      
Check GTFO for: bash                                       
Check GTFO for: bridge
Check GTFO for: busybox
Check GTFO for: bzip2
Check GTFO for: cat
Check GTFO for: comm
Check GTFO for: cp
Check GTFO for: cpio
Check GTFO for: cupsfilter
Check GTFO for: curl
Check GTFO for: dash
Check GTFO for: date
Check GTFO for: dd
Check GTFO for: diff
```

Podemos utilizar la herramienta de diagnóstico `strace` en sistemas operativos basados ​​en Linux para rastrear y analizar las llamadas del sistema y el procesamiento de señales. Nos permite seguir el flujo de un programa y comprender cómo accede a los recursos del sistema, procesa señales y recibe y envía datos del sistema operativo. Además, también podemos utilizar la herramienta para supervisar las actividades relacionadas con la seguridad e identificar posibles vectores de ataque, como solicitudes específicas a hosts remotos que utilizan contraseñas o tokens.

La salida `strace` se puede escribir en un archivo para su posterior análisis y proporciona una gran cantidad de opciones que permiten un seguimiento detallado del comportamiento del programa.

**Seguimiento de llamadas al sistema**

```bash
afsh4ck@kali$ strace ping -c1 10.129.112.20

execve("/usr/bin/ping", ["ping", "-c1", "10.129.112.20"], 0x7ffdc8b96cc0 /* 80 vars */) = 0
access("/etc/suid-debug", F_OK)         = -1 ENOENT (No such file or directory)
brk(NULL)                               = 0x56222584c000
arch_prctl(0x3001 /* ARCH_??? */, 0x7fffb0b2ea00) = -1 EINVAL (Invalid argument)
...SNIP...
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
...SNIP...
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libidn2.so.0", O_RDONLY|O_CLOEXEC) = 3
...SNIP...
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\237\2\0\0\0\0\0"..., 832) = 832
pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
pread64(3, "\4\0\0\0 \0\0\0\5\0\0\0GNU\0\2\0\0\300\4\0\0\0\3\0\0\0\0\0\0\0"..., 48, 848) = 48
...SNIP...
socket(AF_INET, SOCK_DGRAM, IPPROTO_ICMP) = 3
socket(AF_INET6, SOCK_DGRAM, IPPROTO_ICMPV6) = 4
capget({version=_LINUX_CAPABILITY_VERSION_3, pid=0}, NULL) = 0
capget({version=_LINUX_CAPABILITY_VERSION_3, pid=0}, {effective=0, permitted=0, inheritable=0}) = 0
openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache", O_RDONLY) = 5
...SNIP...
socket(AF_INET, SOCK_DGRAM, IPPROTO_IP) = 5
connect(5, {sa_family=AF_INET, sin_port=htons(1025), sin_addr=inet_addr("10.129.112.20")}, 16) = 0
getsockname(5, {sa_family=AF_INET, sin_port=htons(39885), sin_addr=inet_addr("10.129.112.20")}, [16]) = 0
close(5)                                = 0
...SNIP...
sendto(3, "\10\0\31\303\0\0\0\1eX\327c\0\0\0\0\330\254\n\0\0\0\0\0\20\21\22\23\24\25\26\27"..., 64, 0, {sa_family=AF_INET, sin_port=htons(0), sin_addr=inet_addr("10.129.112.20")}, 16) = 64
...SNIP...
recvmsg(3, {msg_name={sa_family=AF_INET, sin_port=htons(0), sin_addr=inet_addr("10.129.112.20")}, msg_namelen=128 => 16, msg_iov=[{iov_base="\0\0!\300\0\3\0\1eX\327c\0\0\0\0\330\254\n\0\0\0\0\0\20\21\22\23\24\25\26\27"..., iov_len=192}], msg_iovlen=1, msg_control=[{cmsg_len=32, cmsg_level=SOL_SOCKET, cmsg_type=SO_TIMESTAMP_OLD, cmsg_data={tv_sec=1675057253, tv_usec=699895}}, {cmsg_len=20, cmsg_level=SOL_IP, cmsg_type=IP_TTL, cmsg_data=[64]}], msg_controllen=56, msg_flags=0}, 0) = 64
write(1, "64 bytes from 10.129.112.20: icmp_se"..., 57) = 57
write(1, "\n", 1)                       = 1
write(1, "--- 10.129.112.20 ping statistics --"..., 34) = 34
write(1, "1 packets transmitted, 1 receive"..., 60) = 60
write(1, "rtt min/avg/max/mdev = 0.287/0.2"..., 50) = 50
close(1)                                = 0
close(2)                                = 0
exit_group(0)                           = ?
+++ exited with 0 +++
```

### **Archivos de configuración**

Los usuarios pueden leer casi todos los archivos de configuración en un sistema operativo Linux si el administrador los ha mantenido iguales. Estos archivos de configuración a menudo pueden revelar cómo se instala y configura el servicio para comprender mejor cómo podemos usarlo para nuestros fines. Además, estos archivos pueden contener información confidencial, como claves y rutas de archivos en carpetas que no podemos ver. Sin embargo, si el archivo tiene permisos de lectura para todos, aún podemos leer el archivo incluso si no tenemos permiso para leer la carpeta.

```bash
afsh4ck@kali$ find / -type f \( -name *.conf -o -name *.config \) -exec ls -l {} \; 2>/dev/null

-rw-r--r-- 1 root root 448 Nov 28 12:31 /run/tmpfiles.d/static-nodes.conf
-rw-r--r-- 1 root root 71 Nov 28 12:31 /run/NetworkManager/resolv.conf
-rw-r--r-- 1 root root 72 Nov 28 12:31 /run/NetworkManager/no-stub-resolv.conf
-rw-r--r-- 1 root root 0 Nov 28 12:37 /run/NetworkManager/conf.d/10-globally-managed-devices.conf
-rw-r--r-- 1 systemd-resolve systemd-resolve 736 Nov 28 12:31 /run/systemd/resolve/stub-resolv.conf
-rw-r--r-- 1 systemd-resolve systemd-resolve 607 Nov 28 12:31 /run/systemd/resolve/resolv.conf
...SNIP...
```

### **Scripts**

Los scripts son similares a los archivos de configuración. A menudo, los administradores son perezosos y están convencidos de la seguridad de la red y descuidan la seguridad interna de sus sistemas. Estos scripts, en algunos casos, tienen privilegios tan erróneos que trataremos más adelante, pero su contenido es de gran importancia incluso sin estos privilegios. Porque a través de ellos, podemos descubrir procesos internos e individuales que pueden sernos de gran utilidad.

```bash
afsh4ck@kali$ find / -type f -name "*.sh" 2>/dev/null | grep -v "src\|snap\|share"

/home/htb-student/automation.sh
/etc/wpa_supplicant/action_wpa.sh
/etc/wpa_supplicant/ifupdown.sh
/etc/wpa_supplicant/functions.sh
/etc/init.d/keyboard-setup.sh
/etc/init.d/console-setup.sh
/etc/init.d/hwclock.sh
...SNIP...
```

### **Servicios en ejecución por usuario**

Además, si miramos la lista de procesos, nos puede dar información sobre qué scripts o binarios están en uso y por qué usuario. Así, por ejemplo, si se trata de un script creado por el administrador en su ruta y cuyos derechos no han sido restringidos, podemos ejecutarlo sin necesidad de entrar en el directorio `root`.

```shell-session
afsh4ck@kali$ ps aux | grep root

...SNIP...
root           1  2.0  0.2 168196 11364 ?        Ss   12:31   0:01 /sbin/init splash
root         378  0.5  0.4  62648 17212 ?        S<s  12:31   0:00 /lib/systemd/systemd-journald
root         409  0.8  0.1  25208  7832 ?        Ss   12:31   0:00 /lib/systemd/systemd-udevd
root         457  0.0  0.0 150668   284 ?        Ssl  12:31   0:00 vmware-vmblock-fuse /run/vmblock-fuse -o rw,subtype=vmware-vmblock,default_permissions,allow_other,dev,suid
root         752  0.0  0.2  58780 10608 ?        Ss   12:31   0:00 /usr/bin/VGAuthService
root         755  0.0  0.1 248088  7448 ?        Ssl  12:31   0:00 /usr/bin/vmtoolsd
root         772  0.0  0.2 250528  9388 ?        Ssl  12:31   0:00 /usr/lib/accountsservice/accounts-daemon
root         773  0.0  0.0   2548   768 ?        Ss   12:31   0:00 /usr/sbin/acpid
root         774  0.0  0.0  16720   708 ?        Ss   12:31   0:00 /usr/sbin/anacron -d -q -s
root         778  0.0  0.0  18052  2992 ?        Ss   12:31   0:00 /usr/sbin/cron -f
root         779  0.0  0.2  37204  8964 ?        Ss   12:31   0:00 /usr/sbin/cupsd -l
root         784  0.4  0.5 273512 21680 ?        Ssl  12:31   0:00 /usr/sbin/NetworkManager --no-daemon
root         790  0.0  0.0  81932  3648 ?        Ssl  12:31   0:00 /usr/sbin/irqbalance --foreground
root         792  0.1  0.5  48244 20540 ?        Ss   12:31   0:00 /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers
root         793  1.3  0.2 239180 11832 ?        Ssl  12:31   0:00 /usr/lib/policykit-1/polkitd --no-debug
root         806  2.1  1.1 1096292 44976 ?       Ssl  12:31   0:01 /usr/lib/snapd/snapd
root         807  0.0  0.1 244352  6516 ?        Ssl  12:31   0:00 /usr/libexec/switcheroo-control
root         811  0.1  0.2  17412  8112 ?        Ss   12:31   0:00 /lib/systemd/systemd-logind
root         817  0.0  0.3 396156 14352 ?        Ssl  12:31   0:00 /usr/lib/udisks2/udisksd
root         818  0.0  0.1  13684  4876 ?        Ss   12:31   0:00 /sbin/wpa_supplicant -u -s -O /run/wpa_supplicant
root         871  0.1  0.3 319236 13828 ?        Ssl  12:31   0:00 /usr/sbin/ModemManager
root         875  0.0  0.3 178392 12748 ?        Ssl  12:31   0:00 /usr/sbin/cups-browsed
root         889  0.1  0.5 126676 22888 ?        Ssl  12:31   0:00 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
root         906  0.0  0.2 248244  8736 ?        Ssl  12:31   0:00 /usr/sbin/gdm3
root        1137  0.0  0.2 252436  9424 ?        Ssl  12:31   0:00 /usr/lib/upower/upowerd
root        1257  0.0  0.4 293736 16316 ?        Ssl  12:31   0:00 /usr/lib/packagekit/packagekitd
```

***

Esto nos daría una visión general bastante buena de nuestro sistema de destino, para que podamos entrar en más detalles a continuación y determinar los permisos individuales para los componentes que encontramos.

***

## <mark style="color:purple;">Caso práctico</mark>

¿Cúal es la versión de python instalada en el sistema?

```bash
$ python -v
-sh: 20: python: not found
```

Tenemos el siguiente caso, un entorno en el que python está instalado pero no sabemos su versión. Podemos usar el siguiente comando para saber su versión concreta:

```bash
$ ls -l /bin /usr/bin/ /usr/sbin/ | grep python
lrwxrwxrwx 1 root   root          24 Apr  5  2023 pdb3.11 -> ../lib/python3.11/pdb.py
lrwxrwxrwx 1 root   root          23 Mar 13  2023 pdb3.8 -> ../lib/python3.8/pdb.py
lrwxrwxrwx 1 root   root          31 Mar 13  2020 py3versions -> ../share/python3/py3versions.py
lrwxrwxrwx 1 root   root           9 Mar 13  2020 python3 -> python3.8
-rwxr-xr-x 1 root   root     7130776 Apr  5  2023 python3.11
-rwxr-xr-x 1 root   root     5494552 Mar 13  2023 python3.8
```

Vemos varias versiones de python pero concretamente la que tenemos disponible es la `3.11`

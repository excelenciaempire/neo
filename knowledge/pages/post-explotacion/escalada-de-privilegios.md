
# Escalada de Privilegios

Para obtener acceso completo, necesitaremos encontrar una vulnerabilidad interna/local que aumente nuestros privilegios al usuario `root` de `Linux` o al usuario `administrator`/ `SYSTEM` de `Windows`. Repasemos algunos métodos comunes para aumentar nuestros privilegios.

{% content-ref url="/pages/8Y87pQwoQovtYdYAzJbJ" %}
[Escalada de privilegios en Linux](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-linux.md)
{% endcontent-ref %}

{% content-ref url="/pages/Z4DL779ttBN4GOIDDnwC" %}
[Escalada de privilegios en Windows](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-windows.md)
{% endcontent-ref %}

***

{% hint style="danger" %}
**Nota:** Vamos a aumentar privilegios en un host, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

### <mark style="color:purple;">Checklists</mark>

Una vez que obtenemos acceso inicial a un cuadro, queremos enumerarlo minuciosamente para encontrar posibles vulnerabilidades que podamos explotar para lograr un nivel de privilegio más alto. Podemos encontrar muchas checklists online que tienen una colección de comprobaciones que podemos ejecutar y los comandos para ejecutarlas. Un recurso excelente es [HackTricks](https://book.hacktricks.xyz/) , que tiene una excelente lista de verificación para la escalada de privilegios locales tanto [de Linux](https://book.hacktricks.xyz/linux-unix/linux-privilege-escalation-checklist) como [de Windows](https://book.hacktricks.xyz/windows/checklist-windows-privilege-escalation) . Otro repositorio excelente es [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) , que también tiene checklists tanto para [Linux](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation.md) como [para Windows.](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md). Debemos comenzar a experimentar con varios comandos y técnicas y familiarizarnos con ellos para comprender las múltiples debilidades que pueden conducir a una escalada de nuestros privilegios.

***

### <mark style="color:purple;">Scripts de enumeración</mark>

Muchos de los comandos anteriores se pueden ejecutar automáticamente con un script para revisar el informe y buscar puntos débiles. Podemos ejecutar muchos scripts para enumerar automáticamente el servidor ejecutando comandos comunes que devuelvan hallazgos interesantes. Algunos de los scripts de enumeración comunes de Linux incluyen [LinEnum](https://github.com/rebootuser/LinEnum.git) y [linuxprivchecker](https://github.com/sleventyeleven/linuxprivchecker) , y para Windows incluyen [Seatbelt](https://github.com/GhostPack/Seatbelt) y [JAWS](https://github.com/411Hall/JAWS) .

Otra herramienta útil que podemos usar para la enumeración de servidores es [Privilege Escalation Awesome Scripts SUITE (PEASS)](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite) , ya que está bien mantenida para mantenerse actualizada e incluye secuencias de comandos para enumerar tanto Linux como Windows.

{% hint style="warning" %}
**Nota**: Estos scripts ejecutarán muchos comandos conocidos por identificar vulnerabilidades y crearán mucho "ruido" que puede activar software antivirus o software de monitoreo de seguridad que busca este tipo de eventos. Esto puede impedir que los scripts se ejecuten o incluso activar una alarma de que el sistema se ha visto comprometido. En algunos casos, es posible que deseemos realizar una enumeración manual en lugar de ejecutar scripts.
{% endhint %}

Tomemos un ejemplo de cómo ejecutar el script de Linux desde `PEASS` llamado `LinPEAS`:

{% content-ref url="/pages/H66BqVhSzHLPvQFclWwC" %}
[Linpeas](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-linux/linpeas.md)
{% endcontent-ref %}

```shell-session
afsh4ck@kali$ ./linpeas.sh
...SNIP...

Linux Privesc Checklist: https://book.hacktricks.xyz/linux-unix/linux-privilege-escalation-checklist
 LEYEND:
  RED/YELLOW: 99% a PE vector
  RED: You must take a look at it
  LightCyan: Users with console
  Blue: Users without console & mounted devs
  Green: Common things (users, groups, SUID/SGID, mounts, .sh scripts, cronjobs)
  LightMangenta: Your username

====================================( Basic information )=====================================
OS: Linux version 3.9.0-73-generic
User & Groups: uid=33(www-data) gid=33(www-data) groups=33(www-data)
...SNIP...
```

Como podemos ver, una vez que se ejecuta el script, comienza a recopilar información y a mostrarla en un excelente informe. Analicemos algunas de las vulnerabilidades que debemos buscar en el resultado de estos scripts.

***

### <mark style="color:purple;">Explotaciones del kernel</mark>

Siempre que nos encontremos con un servidor que ejecuta un sistema operativo antiguo, debemos comenzar buscando posibles vulnerabilidades del kernel que puedan existir. Supongamos que el servidor no se mantiene con las últimas actualizaciones y parches. En ese caso, es probable que sea vulnerable a vulnerabilidades específicas del kernel que se encuentran en versiones sin parches de Linux y Windows.

Por ejemplo, el script anterior nos mostró que la versión de Linux era `3.9.0-73-generic`. Si buscamos en Google exploits para esta versión o uso `searchsploit`, encontraríamos un `CVE-2016-5195`, también conocido como `DirtyCow`. Podemos buscar y descargar el exploit [DirtyCow](https://github.com/dirtycow/dirtycow.github.io/wiki/PoCs) y ejecutarlo en el servidor para obtener acceso de root.

El mismo concepto también se aplica a Windows, ya que hay muchas vulnerabilidades en versiones anteriores o sin parches de Windows, con varias vulnerabilidades que pueden usarse para escalar privilegios. Debemos tener en cuenta que los exploits del kernel pueden provocar inestabilidad en el sistema y debemos tener mucho cuidado antes de ejecutarlos en sistemas de producción. Lo mejor es probarlos en un entorno de laboratorio y ejecutarlos únicamente en sistemas de producción con la aprobación y coordinación explícita de nuestro cliente.

***

### <mark style="color:purple;">Software vulnerable</mark>

Otra cosa que debemos buscar es el software instalado. Por ejemplo, podemos usar el comando `dpkg -l` en Linux o mirar `C:\Program Files` en Windows para ver qué software está instalado en el sistema. Deberíamos buscar exploits públicos para cualquier software instalado, especialmente si se están utilizando versiones anteriores que contengan vulnerabilidades sin parches.

***

### <mark style="color:purple;">Privilegios de usuario</mark>

Otro aspecto crítico a buscar después de obtener acceso a un servidor son los privilegios disponibles para el usuario al que tenemos acceso. Supongamos que se nos permite ejecutar comandos específicos como root (o como otro usuario). En ese caso, es posible que podamos escalar nuestros privilegios a usuarios raíz/del sistema u obtener acceso como un usuario diferente. A continuación se muestran algunas formas comunes de explotar ciertos privilegios de usuario:

1. `sudo`
2. `SUIDO`
3. `Privilegios de tokens de Windows`

* Ver la versión de sudo que se está ejecutando

```bash
sudo --version
sudo -V
```

El comando `sudo` en Linux permite a un usuario ejecutar comandos como un usuario diferente. Por lo general, se usa para permitir que los usuarios con menos privilegios ejecuten comandos como root sin darles acceso al usuario root. Esto generalmente se hace porque los comandos específicos solo se pueden ejecutar como raíz `tcpdump`o permitir al usuario acceder a ciertos directorios solo raíz. Podemos comprobar qué privilegios `sudo` tenemos con el comando `sudo -l`:

```shell-session
afsh4ck@kali$ sudo -l

[sudo] password for user1:
...SNIP...

User user1 may run the following commands on ExampleServer:
    (ALL : ALL) ALL
```

El resultado anterior dice que podemos ejecutar todos los comandos con `sudo`, lo que nos da acceso completo, y podemos usar el comando `su` con `sudo`para cambiar al usuario root:

```shell-session
afsh4ck@kali$ sudo su -

[sudo] password for user1:
whoami
root
```

El comando anterior requiere una contraseña para ejecutar cualquier comando con `sudo`. Hay determinadas ocasiones en las que se nos puede permitir ejecutar determinadas aplicaciones, o todas las aplicaciones, sin tener que proporcionar una contraseña:

```shell-session
afsh4ck@kali$ sudo -l

    (user : user) NOPASSWD: /bin/echo
```

La entrada  `NOPASSWD` muestra que el comando `/bin/echo` se puede ejecutar sin contraseña. Esto sería útil si obtuviéramos acceso al servidor a través de una vulnerabilidad y no tuviéramos la contraseña del usuario.&#x20;

***

### <mark style="color:purple;">Movimiento Lateral</mark>

Como dice `user`, podemos ejecutar `sudo` como ese usuario y no como root. Para hacerlo, podemos especificar el usuario con `-u user`:

```shell-session
afsh4ck@kali$ sudo -u user /bin/echo Hello World!

    Hello World!
```

Una vez que encontramos una aplicación particular con la que podemos ejecutar `sudo`, podemos buscar formas de explotarla para obtener un shell como usuario root. [GTFOBins](https://gtfobins.github.io/) contiene una lista de comandos y cómo se pueden explotar a través de `sudo`. Podemos buscar la aplicación `sudo` sobre la que tenemos privilegios y, si existe, puede indicarnos el comando exacto que debemos ejecutar para obtener acceso de root utilizando el privilegio `sudo` que tenemos.

{% content-ref url="/pages/cwk8zNlCxAUKvjeVPAd3" %}
[GTFOBins](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/gtfobins.md)
{% endcontent-ref %}

[LOLBAS](https://lolbas-project.github.io/#) también contiene una lista de aplicaciones de Windows que podemos aprovechar para realizar determinadas funciones, como descargar archivos o ejecutar comandos en el contexto de un usuario privilegiado.

***

### <mark style="color:purple;">Tareas programadas</mark>

Tanto en Linux como en Windows, existen métodos para ejecutar scripts a intervalos específicos para realizar una tarea. Algunos ejemplos son un análisis antivirus que se ejecuta cada hora o un script de copia de seguridad que se ejecuta cada 30 minutos. Generalmente existen dos formas de aprovechar las tareas programadas (Windows) o los trabajos cron (Linux) para escalar nuestros privilegios:

1. Agregar nuevas tareas programadas/trabajos cron
2. Engañarlos para ejecutar un software malicioso

La forma más sencilla es comprobar si podemos añadir nuevas tareas programadas. En Linux, una forma común de mantener las tareas programadas es mediante `Cron Jobs`. Hay directorios específicos que podemos utilizar para agregar nuevos trabajos cron si tenemos permisos `write` sobre ellos. Éstas incluyen:

1. `/etc/crontab`
2. `/etc/cron.d`
3. `/var/spool/cron/crontabs/root`

Si podemos escribir en un directorio llamado por un trabajo cron, podemos escribir un script bash con un comando de shell inverso, que debería enviarnos un shell inverso cuando se ejecute.

***

### <mark style="color:purple;">Credenciales expuestas</mark>

A continuación, podemos buscar archivos que podamos leer y ver si contienen credenciales expuestas. Esto es muy común con archivos `configuration`, archivos `log` y archivos de historial de usuario (`bash_history`en Linux y `PSReadLine`Windows). Los scripts de enumeración que analizamos al principio normalmente buscan posibles contraseñas en archivos y nos las proporcionan, como se muestra a continuación:

```bash
...SNIP...
[+] Searching passwords in config PHP files
[+] Finding passwords inside logs (limit 70)
...SNIP...
/var/www/html/config.php: $conn = new mysqli(localhost, 'db_user', 'password123');
```

Como podemos ver, la contraseña de la base de datos ' `password123`' está expuesta, lo que nos permitiría iniciar sesión en las bases de datos locales `mysql` y buscar información interesante. También podemos verificar `Password Reuse`, ya que el usuario del sistema puede haber usado su contraseña para las bases de datos, lo que puede permitirnos usar la misma contraseña para cambiar a ese usuario, de la siguiente manera:

```shell-session
afsh4ck@kali$ su -

Password: password123
whoami

root
```

También podemos utilizar las credenciales del usuario para ingresar por `ssh` al servidor como ese usuario.

***

### <mark style="color:purple;">Claves SSH</mark>

Finalmente, analicemos las claves SSH. Si tenemos acceso de lectura al directorio `.ssh` para un usuario específico, podemos leer sus claves ssh privadas que se encuentran en `/home/user/.ssh/id_rsa` o `/root/.ssh/id_rsa`y usarlas para iniciar sesión en el servidor. Si podemos leer el `/root/.ssh/`directorio y el archivo `id_rsa`, podemos copiarlo a nuestra máquina y usar la bandera `-i` para iniciar sesión con él:

<pre class="language-shell-session"><code class="lang-shell-session"># En el server
-----------------------------------------
find / -name authorized_keys 2> /dev/null
find / -name id_rsa 2> /dev/null 
cat /root/.ssh/id_rsa

# En Kali
-----------------------------------------
<strong>afsh4ck@kali$ nano id_rsa
</strong>afsh4ck@kali$ chmod 600 id_rsa
afsh4ck@kali$ ssh root@10.10.10.10 -i id_rsa

root@remotehost#
</code></pre>

Tenga en cuenta que utilizamos el comando 'chmod 600 id\_rsa' en la clave después de crearla en nuestra máquina para cambiar los permisos del archivo para que sean más restrictivos. Si las claves ssh tienen permisos laxos, es decir, pueden ser leídas por otras personas, el servidor ssh impediría que funcionen.

Si tenemos acceso de escritura a un `/.ssh/`directorio de usuarios, podemos colocar nuestra clave pública en el directorio ssh del usuario en `/home/user/.ssh/authorized_keys`. Esta técnica generalmente se usa para obtener acceso ssh después de obtener un shell como ese usuario. La configuración SSH actual no aceptará claves escritas por otros usuarios, por lo que solo funcionará si ya hemos obtenido el control sobre ese usuario. Primero debemos crear una nueva clave con `ssh-keygen`y la bandera `-f` para especificar el archivo de salida:

```shell-session
afsh4ck@kali$ ssh-keygen -f key

Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase): *******
Enter same passphrase again: *******

Your identification has been saved in key
Your public key has been saved in key.pub
The key fingerprint is:
SHA256:...SNIP... user@parrot
The key's randomart image is:
+---[RSA 3072]----+
|   ..o.++.+      |
...SNIP...
|     . ..oo+.    |
+----[SHA256]-----+
```

Esto nos dará dos archivos: `key`(que usaremos con `ssh -i`) y `key.pub`, que copiaremos a la máquina remota. Copiemos `key.pub`, luego en la máquina remota, lo agregaremos a `/root/.ssh/authorized_keys`:

```shell-session
user@remotehost$ echo "ssh-rsa AAAAB...SNIP...M= user@parrot" >> /root/.ssh/authorized_keys
```

Ahora, el servidor remoto debería permitirnos iniciar sesión como ese usuario utilizando nuestra clave privada:

```shell-session
afsh4ck@kali$ ssh root@10.10.10.10 -i key

root@remotehost# 
```

Vamos a ver en detalle técnicas de elevación de privilegios en sistemas Linux.

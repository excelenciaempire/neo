
# Shells restringidos

## <mark style="color:purple;">Cómo escapar de los shells restringidos</mark>

Un shell restringido es un tipo de shell que limita la capacidad del usuario para ejecutar comandos. En un shell restringido, el usuario solo puede ejecutar un conjunto específico de comandos o solo puede ejecutar comandos en directorios específicos. Los shells restringidos se utilizan a menudo para proporcionar un entorno seguro para los usuarios que pueden dañar el sistema de forma accidental o intencional, o para proporcionar una forma de que los usuarios accedan solo a determinadas funciones del sistema. Algunos ejemplos comunes de shells restringidos incluyen el shell `rbash` en Linux y el "Shell de acceso restringido" en Windows.

### **RBA**

[Bourne shell restringido](https://www.gnu.org/software/bash/manual/html_node/The-Restricted-Shell.html) (`rbash`) es una versión restringida de Bourne shell, un intérprete de línea de comandos estándar en Linux que limita la capacidad del usuario para utilizar ciertas funciones de Bourne shell, como cambiar directorios, configurar o modificar variables de entorno y ejecutar comandos en otros directorios. Se utiliza a menudo para proporcionar un entorno seguro y controlado para los usuarios que pueden dañar el sistema de forma accidental o intencionada.

### **RKSHS**

[El shell Korn restringido](https://www.ibm.com/docs/en/aix/7.2?topic=r-rksh-command) (`rksh`) es una versión restringida del shell Korn, otro intérprete de línea de comandos estándar. El shell `rksh` limita la capacidad del usuario para utilizar ciertas funciones del shell Korn, como ejecutar comandos en otros directorios, crear o modificar funciones del shell y modificar el entorno del shell.

### **RZSH**

[El shell Z restringido](https://manpages.debian.org/experimental/zsh/rzsh.1.en.html) (`rzsh`) es una versión restringida del shell Z y es el intérprete de línea de comandos más potente y flexible. El shell `rzsh` limita la capacidad del usuario para utilizar ciertas funciones del shell Z, como ejecutar scripts de shell, definir alias y modificar el entorno del shell.

Por ejemplo, los administradores suelen utilizar shells restringidos en redes empresariales para proporcionar un entorno seguro y controlado a los usuarios que puedan dañar el sistema de forma accidental o intencionada. Al limitar la capacidad del usuario para ejecutar comandos específicos o acceder a determinados directorios, los administradores pueden garantizar que los usuarios no puedan realizar acciones que puedan dañar el sistema o comprometer la seguridad de la red. Además, los shells restringidos pueden dar a los usuarios acceso únicamente a determinadas funciones del sistema, lo que permite a los administradores controlar qué recursos y funciones están disponibles para cada usuario.

Imagine una empresa con una red de servidores Linux que alojan aplicaciones y servicios empresariales críticos. Muchos usuarios, incluidos empleados, contratistas y socios externos, acceden a la red. Para proteger la seguridad y la integridad de la red, el equipo de TI de la organización decidió implementar shells restringidos para todos los usuarios.

Para ello, el equipo de TI configura varios shells `rbash`, `rksh`, y `rzsh` en la red y asigna a cada usuario un shell específico. Por ejemplo, a los socios externos que necesitan acceder solo a determinadas funciones de la red, como el correo electrónico y el uso compartido de archivos, se les asignan shells `rbash`, lo que limita su capacidad para ejecutar comandos específicos y acceder a determinados directorios. A los contratistas que necesitan acceder a funciones de red más avanzadas, como servidores de bases de datos y servidores web, se les asignan shells `rksh`, que les proporcionan más flexibilidad pero aún limitan sus capacidades. Por último, a los empleados que necesitan acceder a la red para fines específicos, como ejecutar aplicaciones o scripts específicos, se les asignan shells `rzsh`, que les proporcionan la mayor flexibilidad pero aún limitan su capacidad para ejecutar comandos específicos y acceder a determinados directorios.

Se pueden utilizar varios métodos para escapar de un shell restringido. Algunos de estos métodos implican explotar vulnerabilidades en el propio shell, mientras que otros implican el uso de técnicas creativas para eludir las restricciones impuestas por el shell. A continuación se muestran algunos ejemplos de métodos que se pueden utilizar para escapar de un shell restringido.

***

### <mark style="color:purple;">Escapando</mark>

En algunos casos, es posible escapar de un shell restringido inyectando comandos en la línea de comandos u otras entradas que el shell acepta. Por ejemplo, supongamos que el shell permite a los usuarios ejecutar comandos pasándolos como argumentos a un comando integrado. En ese caso, es posible escapar del shell inyectando comandos adicionales en el argumento.

### **Inyección de comandos**

Imaginemos que estamos en un shell restringido que nos permite ejecutar comandos pasándolos como argumentos al comando `ls`. Desafortunadamente, el shell solo nos permite ejecutar el comando `ls` con un conjunto específico de argumentos, como `ls -l` o `ls -a`, pero no nos permite ejecutar ningún otro comando. En esta situación, podemos usar la inyección de comandos para escapar del shell inyectando comandos adicionales en el argumento del `ls`comando.

Por ejemplo, podríamos usar el siguiente comando para inyectar un comando `pwd` en el argumento del comando `ls`:

```shell-session
afsh4ck@kali$ ls -l `pwd` 
```

Este comando haría que se ejecute el comando `ls` con el argumento `-l`, seguido de la salida del comando `pwd`. Dado que el comando `pwd` no está restringido por el shell, esto nos permitiría ejecutar el comando `pwd` y ver el directorio de trabajo actual, aunque el shell no nos permita ejecutar el comando `pwd` directamente.

### **Sustitución de comandos**

Otro método para escapar de un shell restringido es utilizar la sustitución de comandos. Esto implica utilizar la sintaxis de sustitución de comandos del shell para ejecutar un comando. Por ejemplo, imagine que el shell permite a los usuarios ejecutar comandos encerrándolos entre comillas simples invertidas (`` ` ``). En ese caso, es posible escapar del shell ejecutando un comando en una sustitución de comillas simples invertidas que no esté restringida por el shell.

### **Encadenamiento de comandos**

En algunos casos, puede ser posible escapar de un shell restringido mediante el uso de encadenamiento de comandos. Necesitaríamos utilizar varios comandos en una sola línea de comandos, separados por un metacarácter de shell, como un punto y coma ( `;`) o una barra vertical ( `|`), para ejecutar un comando. Por ejemplo, si el shell permite a los usuarios ejecutar comandos separados por punto y coma, puede ser posible escapar del shell mediante el uso de un punto y coma para separar dos comandos, uno de los cuales no está restringido por el shell.

### **Variables de entorno**

Para escapar de un shell restringido y utilizar variables de entorno, es necesario modificar o crear variables de entorno que el shell utiliza para ejecutar comandos que no están restringidos por el shell. Por ejemplo, si el shell utiliza una variable de entorno para especificar el directorio en el que se ejecutan los comandos, es posible escapar del shell modificando el valor de la variable de entorno para especificar un directorio diferente.

### **Funciones de Shell**

En algunos casos, es posible escapar de un shell restringido mediante el uso de funciones de shell. Para ello, podemos definir y llamar a funciones de shell que ejecuten comandos no restringidos por el shell. Supongamos que el shell permite a los usuarios definir y llamar a funciones de shell; es posible escapar del shell mediante la definición de una función de shell que ejecute un comando.

***

## Caso práctico

Utilice diferentes métodos para escapar del shell restringido y leer el archivo flag.txt. Envíe el contenido como respuesta.

```
SSH a 10.129.64.30 (ACADEMY-LLPE-RSH)
Usuario "htb-user"
Contraseña "HTB_@cademy_us3r!"
```

Accedemos por SSH:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ ssh htb-user@10.129.64.30
</strong>The authenticity of host '10.129.64.30 (10.129.64.30)' can't be established.
ED25519 key fingerprint is SHA256:HfXWue9Dnk+UvRXP6ytrRnXKIRSijm058/zFrj/1LvY.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:1: [hashed name]
    ~/.ssh/known_hosts:5: [hashed name]
    ~/.ssh/known_hosts:6: [hashed name]
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.64.30' (ED25519) to the list of known hosts.
htb-user@10.129.64.30's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-88-generic x86_64)

htb-user@ubuntu:~$ ls
-rbash: /usr/lib/command-not-found: restricted: cannot specify `/' in command names
</code></pre>

Nos encontramos ante una shell restrictiva en la que no podemos ejecutar el comando `ls` por ejemplo. Podemos usar echo para listar los archivos de la siguiente manera

```shell-session
htb-user@ubuntu:~$ echo $PATH
/home/htb-user/bin
htb-user@ubuntu:~$ echo *
bin flag.txt
```

Tampoco podemos redirigir el output a un archivo como en el ejemplo siguiente, por lo que tendremos que buscar una alternativa:

```shell-session
htb-user@ubuntu:~$ echo 'cat flag.txt' > /home/htb-user/bin/mycat
-rbash: /home/htb-user/bin/mycat: restricted: cannot redirect output
```

Con el siguiente script en bash conseguimos leer el archivo:

```shell-session
htb-user@ubuntu:~$ while read line; do echo $line; done < flag.txt
HTB{35c4p3_7h3_r3strict3d_5h311}
```

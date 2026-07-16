
# NFS

Su propósito es acceder a sistemas de archivos a través de una red como si fueran locales. Sin embargo, utiliza un protocolo completamente diferente. [NFS](https://en.wikipedia.org/wiki/Network_File_System) se utiliza entre sistemas Linux y Unix. Esto significa que los clientes NFS no pueden comunicarse directamente con los servidores SMB.&#x20;

NFS es un estándar de Internet que rige los procedimientos en un sistema de archivos distribuido. Si bien la versión 3.0 ( ) del protocolo NFS `NFSv3`, que se ha utilizado durante muchos años, autentica la computadora cliente, esto cambia con `NFSv4`. Aquí, al igual que ocurre con el protocolo SMB de Windows, el usuario debe autenticarse.

<table data-header-hidden><thead><tr><th width="118"></th><th></th></tr></thead><tbody><tr><td><strong>Versión</strong></td><td><strong>Características</strong></td></tr><tr><td><code>NFSv2</code></td><td>Es más antiguo pero es compatible con muchos sistemas e inicialmente funcionaba completamente a través de UDP.</td></tr><tr><td><code>NFSv3</code></td><td>Tiene más funciones, incluido el tamaño de archivo variable y mejores informes de errores, pero no es totalmente compatible con los clientes NFSv2.</td></tr><tr><td><code>NFSv4</code></td><td>Incluye Kerberos, funciona a través de firewalls y en Internet, ya no requiere asignadores de puertos, admite ACL, aplica operaciones basadas en estados y proporciona mejoras de rendimiento y alta seguridad. También es la primera versión que tiene un protocolo con estado.</td></tr></tbody></table>

NFS versión 4.1 ( [RFC 8881](https://datatracker.ietf.org/doc/html/rfc8881) ) tiene como objetivo proporcionar soporte de protocolo para aprovechar las implementaciones de servidores en clúster, incluida la capacidad de proporcionar acceso paralelo escalable a archivos distribuidos en múltiples servidores (extensión pNFS). Además, NFSv4.1 incluye un mecanismo de enlace troncal de sesiones, también conocido como rutas múltiples NFS. Una ventaja significativa de NFSv4 sobre sus predecesores es que sólo `2049`se utiliza un puerto UDP o TCP para ejecutar el servicio, lo que simplifica el uso del protocolo a través de firewalls.

NFS se basa en el protocolo [de llamada a procedimiento remoto de Open Network Computing](https://en.wikipedia.org/wiki/Sun_RPC) ( `ONC-RPC`/ `SUN-RPC`) expuesto en los puertos `TCP`y `UDP 111`, que utiliza [representación de datos externos](https://en.wikipedia.org/wiki/External_Data_Representation) ( `XDR`) para el intercambio de datos independiente del sistema. El protocolo NFS tiene `no`un mecanismo para `authentication`o `authorization`. En cambio, la autenticación se traslada completamente a las opciones del protocolo RPC. La autorización se deriva de la información disponible del sistema de archivos. En este proceso, el servidor es responsable de traducir la información del usuario del cliente al formato del sistema de archivos y convertir los detalles de autorización correspondientes a la sintaxis UNIX requerida con la mayor precisión posible.

La autenticación más común es a través de UNIX `UID`/ `GID`y `group memberships`, por lo que es más probable que esta sintaxis se aplique al protocolo NFS. Un problema es que el cliente y el servidor no necesariamente tienen que tener las mismas asignaciones de UID/GID para usuarios y grupos, y el servidor no necesita hacer nada más. No se pueden realizar más comprobaciones por parte del servidor. Es por eso que NFS solo debe usarse con este método de autenticación en redes confiables.

***

## <mark style="color:purple;">Cheatsheet</mark>

<table data-header-hidden><thead><tr><th width="355"></th><th></th></tr></thead><tbody><tr><td><strong>Comando</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>showmount -e &#x3C;target></code></td><td>Mostrar recursos compartidos NFS disponibles.</td></tr><tr><td><code>mount -t nfs &#x3C;target>:/&#x3C;share> ./target-NFS/ -o nolock</code></td><td>Monte el NFS share.umount ./target-NFS específico</td></tr><tr><td><code>umount ./target-NFS</code></td><td>Desmonte el recurso compartido NFS específico.</td></tr></tbody></table>

***

## <mark style="color:purple;">Configuración predeterminada</mark>

NFS no es difícil de configurar porque no hay tantas opciones como FTP o SMB. El `/etc/exports`archivo contiene una tabla de sistemas de archivos físicos en un servidor NFS al que pueden acceder los clientes. La [Tabla de Exportaciones de NFS](http://manpages.ubuntu.com/manpages/trusty/man5/exports.5.html) muestra qué opciones acepta y así indica qué opciones están disponibles para nosotros.

### **Archivo de exportaciones**

```bash
afsh4ck$ cat /etc/exports 

# /etc/exports: the access control list for filesystems which may be exported
#               to NFS clients.  See exports(5).
#
# Example for NFSv2 and NFSv3:
# /srv/homes       hostname1(rw,sync,no_subtree_check) hostname2(ro,sync,no_subtree_check)
#
# Example for NFSv4:
# /srv/nfs4        gss/krb5i(rw,sync,fsid=0,crossmnt,no_subtree_check)
# /srv/nfs4/homes  gss/krb5i(rw,sync,no_subtree_check)
```

El archivo predeterminado `exports` también contiene algunos ejemplos de configuración de recursos compartidos NFS. Primero, la carpeta se especifica y se pone a disposición de otros, y luego los derechos que tendrán sobre este recurso compartido NFS se conectan a un host o una subred. Finalmente, se pueden agregar opciones adicionales a los hosts o subredes.

<table data-header-hidden><thead><tr><th width="212"></th><th></th></tr></thead><tbody><tr><td><strong>Opción</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>rw</code></td><td>Permisos de lectura y escritura.</td></tr><tr><td><code>ro</code></td><td>Permisos de sólo lectura.</td></tr><tr><td><code>sync</code></td><td>Transferencia de datos sincrónica. (Un poco más lento)</td></tr><tr><td><code>async</code></td><td>Transferencia de datos asincrónica. (Un poco más rápido)</td></tr><tr><td><code>secure</code></td><td>No se utilizarán puertos superiores a 1024.</td></tr><tr><td><code>insecure</code></td><td>Se utilizarán puertos superiores a 1024.</td></tr><tr><td><code>no_subtree_check</code></td><td>Esta opción desactiva la comprobación de árboles de subdirectorios.</td></tr><tr><td><code>root_squash</code></td><td>Asigna todos los permisos a los archivos de raíz UID/GID 0 al UID/GID de anónimo, lo que impide <code>root</code>acceder a archivos en un montaje NFS.</td></tr></tbody></table>

Creemos una entrada de este tipo con fines de prueba y juguemos con la configuración.

### **Export FS**

```shell-session
root@nfs:~# echo '/mnt/nfs  10.129.14.0/24(sync,no_subtree_check)' >> /etc/exports
root@nfs:~# systemctl restart nfs-kernel-server 
root@nfs:~# exportfs

/mnt/nfs      	10.129.14.0/24
```

Hemos compartido la carpeta `/mnt/nfs` con la subred `10.129.14.0/24` con la configuración que se muestra arriba. Esto significa que todos los hosts de la red podrán montar este recurso compartido NFS e inspeccionar el contenido de esta carpeta.

***

## <mark style="color:purple;">Configuraciones peligrosas</mark>

Sin embargo, incluso con NFS, algunas configuraciones pueden resultar peligrosas para la empresa y su infraestructura. A continuación se enumeran algunos de ellos:

<table data-header-hidden><thead><tr><th width="195"></th><th></th></tr></thead><tbody><tr><td><strong>Opción</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>rw</code></td><td>Permisos de lectura y escritura.</td></tr><tr><td><code>insecure</code></td><td>Se utilizarán puertos superiores a 1024.</td></tr><tr><td><code>nohide</code></td><td>Si se montó otro sistema de archivos debajo de un directorio exportado, este directorio se exporta mediante su propia entrada de exportaciones.</td></tr><tr><td><code>no_root_squash</code></td><td>Todos los archivos creados por root se mantienen con el UID/GID 0.</td></tr></tbody></table>

Se recomienda encarecidamente crear una máquina virtual local y experimentar con la configuración. Descubriremos métodos que nos mostrarán cómo está configurado el servidor NFS. Para ello podemos crear varias carpetas y asignar diferentes opciones a cada una. Luego podemos inspeccionarlos y ver qué configuraciones pueden tener qué efecto en el recurso compartido NFS y sus permisos y el proceso de enumeración.

Podemos echar un vistazo a la `insecure`opción. Esto es peligroso porque los usuarios pueden usar puertos superiores a 1024. Los primeros 1024 puertos solo pueden ser utilizados por root. Esto evita el hecho de que ningún usuario pueda utilizar sockets por encima del puerto 1024 para el servicio NFS e interactuar con él.

***

## <mark style="color:purple;">Enumeración del servicio</mark>

Al enumerar NFS, los puertos TCP `111`y `2049` son esenciales. También podemos obtener información sobre el servicio NFS y el host a través de RPC, como se muestra a continuación en el ejemplo.

### **Nmap**

```bash
afsh4ck$ sudo nmap 10.129.14.128 -p 111,2049 -sV -sC

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-19 17:12 CEST
Nmap scan report for 10.129.14.128
Host is up (0.00018s latency).

PORT    STATE SERVICE VERSION
111/tcp open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  3           2049/udp   nfs
|   100003  3           2049/udp6  nfs
|   100003  3,4         2049/tcp   nfs
|   100003  3,4         2049/tcp6  nfs
|   100005  1,2,3      41982/udp6  mountd
|   100005  1,2,3      45837/tcp   mountd
|   100005  1,2,3      47217/tcp6  mountd
|   100005  1,2,3      58830/udp   mountd
|   100021  1,3,4      39542/udp   nlockmgr
|   100021  1,3,4      44629/tcp   nlockmgr
|   100021  1,3,4      45273/tcp6  nlockmgr
|   100021  1,3,4      47524/udp6  nlockmgr
|   100227  3           2049/tcp   nfs_acl
|   100227  3           2049/tcp6  nfs_acl
|   100227  3           2049/udp   nfs_acl
|_  100227  3           2049/udp6  nfs_acl
2049/tcp open  nfs_acl 3 (RPC #100227)
MAC Address: 00:00:00:00:00:00 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.58 seconds
```

El `rpcinfo`script NSE recupera una lista de todos los servicios RPC que se ejecutan actualmente, sus nombres y descripciones, y los puertos que utilizan. Esto nos permite verificar si el recurso compartido de destino está conectado a la red en todos los puertos requeridos.&#x20;

### Nmap - Scripts para NFS

Además, para NFS, Nmap tiene algunos scripts NSE que pueden usarse para los escaneos. Estos luego nos pueden mostrar, por ejemplo, el valor  `contents`de la acción y su `stats`.

```bash
    afsh4ck$ sudo nmap --script nfs* 10.129.14.128 -sV -p 111,2049

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-19 17:37 CEST
Nmap scan report for 10.129.14.128
Host is up (0.00021s latency).

PORT     STATE SERVICE VERSION
111/tcp  open  rpcbind 2-4 (RPC #100000)
| nfs-ls: Volume /mnt/nfs
|   access: Read Lookup NoModify NoExtend NoDelete NoExecute
| PERMISSION  UID    GID    SIZE  TIME                 FILENAME
| rwxrwxrwx   65534  65534  4096  2021-09-19T15:28:17  .
| ??????????  ?      ?      ?     ?                    ..
| rw-r--r--   0      0      1872  2021-09-19T15:27:42  id_rsa
| rw-r--r--   0      0      348   2021-09-19T15:28:17  id_rsa.pub
| rw-r--r--   0      0      0     2021-09-19T15:22:30  nfs.share
|_
| nfs-showmount: 
|_  /mnt/nfs 10.129.14.0/24
| nfs-statfs: 
|   Filesystem  1K-blocks   Used       Available   Use%  Maxfilesize  Maxlink
|_  /mnt/nfs    30313412.0  8074868.0  20675664.0  29%   16.0T        32000
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  3           2049/udp   nfs
|   100003  3           2049/udp6  nfs
|   100003  3,4         2049/tcp   nfs
|   100003  3,4         2049/tcp6  nfs
|   100005  1,2,3      41982/udp6  mountd
|   100005  1,2,3      45837/tcp   mountd
|   100005  1,2,3      47217/tcp6  mountd
|   100005  1,2,3      58830/udp   mountd
|   100021  1,3,4      39542/udp   nlockmgr
|   100021  1,3,4      44629/tcp   nlockmgr
|   100021  1,3,4      45273/tcp6  nlockmgr
|   100021  1,3,4      47524/udp6  nlockmgr
|   100227  3           2049/tcp   nfs_acl
|   100227  3           2049/tcp6  nfs_acl
|   100227  3           2049/udp   nfs_acl
|_  100227  3           2049/udp6  nfs_acl
2049/tcp open  nfs_acl 3 (RPC #100227)
MAC Address: 00:00:00:00:00:00 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.45 seconds
```

Una vez que hayamos descubierto dicho servicio NFS, podemos montarlo en nuestra máquina local. Para ello, podemos crear una nueva carpeta vacía en la que se montará el recurso compartido NFS. Una vez montado, podemos navegar por él y ver el contenido como si fuera nuestro sistema local.

### **Mostrar recursos compartidos NFS disponibles**

```bash
afsh4ck$ showmount -e 10.129.14.128

Export list for 10.129.14.128:
/mnt/nfs 10.129.14.0/24
```

### **Montaje del recurso compartido NFS**

```bash
afsh4ck$ mkdir target-NFS
afsh4ck$ sudo mount -t nfs 10.129.14.128:/ ./target-NFS/ -o nolock
afsh4ck$ cd target-NFS
afsh4ck$ tree .

.
└── mnt
    └── nfs
        ├── id_rsa
        ├── id_rsa.pub
        └── nfs.share

2 directories, 3 files
```

Allí tendremos la oportunidad de acceder a los derechos y los nombres de usuario y grupos a los que pertenecen los archivos mostrados y visibles. Porque una vez que tengamos los nombres de usuario, nombres de grupos, UID y GUID, podemos crearlos en nuestro sistema y adaptarlos al recurso compartido NFS para ver y modificar los archivos.

### **Listar contenidos con nombres de usuario y nombres de grupos**

```bash
afsh4ck$ ls -l mnt/nfs/

total 16
-rw-r--r-- 1 cry0l1t3 cry0l1t3 1872 Sep 25 00:55 cry0l1t3.priv
-rw-r--r-- 1 cry0l1t3 cry0l1t3  348 Sep 25 00:55 cry0l1t3.pub
-rw-r--r-- 1 root     root     1872 Sep 19 17:27 id_rsa
-rw-r--r-- 1 root     root      348 Sep 19 17:28 id_rsa.pub
-rw-r--r-- 1 root     root        0 Sep 19 17:22 nfs.share
```

### **Listar contenidos con UID y GUID**

```bash
afsh4ck$ ls -n mnt/nfs/

total 16
-rw-r--r-- 1 1000 1000 1872 Sep 25 00:55 cry0l1t3.priv
-rw-r--r-- 1 1000 1000  348 Sep 25 00:55 cry0l1t3.pub
-rw-r--r-- 1    0 1000 1221 Sep 19 18:21 backup.sh
-rw-r--r-- 1    0    0 1872 Sep 19 17:27 id_rsa
-rw-r--r-- 1    0    0  348 Sep 19 17:28 id_rsa.pub
-rw-r--r-- 1    0    0    0 Sep 19 17:22 nfs.share
```

Es importante tener en cuenta que si la opción `root_squash` está activada, no podremos editar el archivo `backup.sh` ni siquiera como `root`.

También podemos usar NFS para una mayor escalada. Por ejemplo, si tenemos acceso al sistema a través de SSH y queremos leer archivos de otra carpeta que un usuario específico pueda leer, necesitaríamos cargar un shell en el recurso compartido NFS que tiene el de ese usuario `SUID` y luego ejecutar el shell a través de el usuario SSH.

Una vez que hayamos realizado todos los pasos necesarios y obtenido la información que necesitamos, podemos desmontar el recurso compartido NFS.

### **Desmontaje**

```bash
afsh4ck$ cd ..
afsh4ck$ sudo umount ./target-NFS
```

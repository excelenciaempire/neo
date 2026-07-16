
# SMB

## <mark style="color:purple;">Protocolo SMB</mark>

`Server Message Block`( `SMB`) es un protocolo cliente-servidor que regula el acceso a archivos y directorios completos y otros recursos de la red, como impresoras, enrutadores o interfaces liberadas para la red. El intercambio de información entre diferentes procesos del sistema también se puede manejar según el protocolo SMB. [SMB](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-smb/f210069c-7086-4dc2-885e-861d837df688) estuvo por primera vez disponible para un público más amplio, por ejemplo, como parte del sistema operativo de red OS/2 LAN Manager y LAN Server.&#x20;

Desde entonces, el principal campo de aplicación del protocolo ha sido en particular la serie de sistemas operativos Windows, cuyos servicios de red soportan SMB de manera compatible con versiones anteriores, lo que significa que los dispositivos con ediciones más recientes pueden comunicarse fácilmente con dispositivos que tienen una versión anterior de Microsoft. sistema instalado. Con el proyecto de software libre Samba también existe una solución que permite el uso de SMB en distribuciones Linux y Unix y, con ello, la comunicación multiplataforma a través de SMB.

El protocolo SMB permite al cliente comunicarse con otros participantes en la misma red para acceder a archivos o servicios compartidos con él en la red. El otro sistema también debe haber implementado el protocolo de red y haber recibido y procesado la solicitud del cliente utilizando una aplicación de servidor SMB. Pero antes ambas partes deben establecer una conexión, por lo que primero intercambian los mensajes correspondientes.

En las redes IP, SMB utiliza el protocolo TCP para este propósito, que proporciona un protocolo de enlace de tres vías entre el cliente y el servidor antes de que finalmente se establezca una conexión. Las especificaciones del protocolo TCP también rigen el transporte posterior de datos. Podemos echar un vistazo a algunos ejemplos [aquí](https://winprotocoldoc.blob.core.windows.net/productionwindowsarchives/MS-SMB2/%5bMS-SMB2%5d.pdf#%5B%7B%22num%22%3A920%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C69%2C738%2C0%5D) .

Un servidor SMB puede proporcionar partes arbitrarias de su sistema de archivos local como recursos compartidos. Por lo tanto, la jerarquía visible para un cliente es parcialmente independiente de la estructura del servidor. Los derechos de acceso están definidos por `Access Control Lists`( `ACL`). Se pueden controlar de manera detallada en función de atributos como `execute`, `read`y `full access`para usuarios individuales o grupos de usuarios. Las ACL se definen en función de los recursos compartidos y, por lo tanto, no corresponden a los derechos asignados localmente en el servidor.

***

## <mark style="color:purple;">Cheatsheet</mark>

<table data-header-hidden><thead><tr><th width="344"></th><th></th></tr></thead><tbody><tr><td><strong>Comando</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>smbclient -N -L //&#x3C;FQDN/IP></code></td><td>Autenticación de sesión nula en SMB.</td></tr><tr><td><code>smbclient //&#x3C;FQDN/IP>/&#x3C;share></code></td><td>Conéctese a un recurso compartido SMB específico.</td></tr><tr><td><code>rpcclient -U "" &#x3C;FQDN/IP></code></td><td>Interacción con el objetivo mediante RPC.</td></tr><tr><td><code>samrdump.py &#x3C;FQDN/IP></code></td><td>Enumeración de nombres de usuario mediante scripts Impacket.</td></tr><tr><td><code>smbmap -H &#x3C;FQDN/IP></code></td><td>Enumeración de acciones de PYMES.</td></tr><tr><td><code>crackmapexec smb &#x3C;FQDN/IP> --shares -u '' -p ''</code></td><td>Enumeración de recursos compartidos de SMB mediante autenticación de sesión nula.</td></tr><tr><td><code>enum4linux-ng.py &#x3C;FQDN/IP> -A</code></td><td>Enumeración SMB usando enum4linux.</td></tr></tbody></table>

***

## <mark style="color:purple;">Samba</mark>

Como se mencionó anteriormente, existe una variante alternativa al servidor SMB, llamada Samba, desarrollada para el sistema operativo basado en Unix. Samba implementa el protocolo de red `Common Internet File System`( `CIFS`). [CIFS](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-cifs/934c2faa-54af-4526-ac74-6a24d126724e) es un "dialecto" de SMB. En otras palabras, CIFS es una implementación muy específica del protocolo SMB, que a su vez fue creado por Microsoft. Esto permite a Samba comunicarse con sistemas Windows más nuevos. Por eso se suele denominar `SMB / CIFS`. Sin embargo, CIFS es la extensión del protocolo SMB. Entonces, cuando pasamos comandos SMB a través de Samba a un servicio NetBIOS anterior, generalmente se conecta al servidor Samba a través de los puertos TCP `137`, `138` y `139` pero CIFS usa solo el puerto `TCP 445`. Existen varias versiones de SMB, incluidas versiones obsoletas que todavía se utilizan en infraestructuras específicas.

<table data-header-hidden><thead><tr><th width="165.33333333333331"></th><th></th><th></th></tr></thead><tbody><tr><td><strong>Versión PYME</strong></td><td><strong>Soportado</strong></td><td><strong>Características</strong></td></tr><tr><td>CIFS</td><td>windows nt 4.0</td><td>Comunicación a través de la interfaz NetBIOS</td></tr><tr><td>PyME 1.0</td><td>ventana 2000</td><td>Conexión directa vía TCP</td></tr><tr><td>Pymes 2.0</td><td>Windows Vista, servidor Windows 2008</td><td>Actualizaciones de rendimiento, firma de mensajes mejorada, función de almacenamiento en caché</td></tr><tr><td>PyME 2.1</td><td>Windows 7, servidor Windows 2008 R2</td><td>Mecanismos de bloqueo</td></tr><tr><td>Pymes 3.0</td><td>Windows 8, servidor Windows 2012</td><td>Conexiones multicanal, cifrado de extremo a extremo, acceso a almacenamiento remoto</td></tr><tr><td>PyME 3.0.2</td><td>Windows 8.1, servidor Windows 2012 R2</td><td></td></tr><tr><td>PyME 3.1.1</td><td>Windows 10, servidor Windows 2016</td><td>Comprobación de integridad, cifrado AES-128</td></tr></tbody></table>

Con la versión 3, el servidor Samba obtuvo la capacidad de ser miembro de pleno derecho de un dominio de Active Directory. Con la versión 4, Samba incluso proporciona un controlador de dominio Active Directory. Para ello contiene varios de los llamados demonios, que son programas en segundo plano de Unix. El demonio del servidor SMB ( `smbd`) perteneciente a Samba proporciona las dos primeras funcionalidades, mientras que el demonio de bloque de mensajes NetBIOS ( `nmbd`) implementa las dos últimas funcionalidades. El servicio SMB controla estos dos programas en segundo plano.

Sabemos que Samba es adecuado tanto para sistemas Linux como Windows. En una red, cada anfitrión participa en la misma `workgroup`. Un grupo de trabajo es un nombre de grupo que identifica una colección arbitraria de computadoras y sus recursos en una red SMB. Puede haber varios grupos de trabajo en la red en un momento dado. IBM desarrolló un `application programming interface`( `API`) para computadoras en red llamado `Network Basic Input/Output System`( `NetBIOS`). La API de NetBIOS proporcionó un modelo para que una aplicación se conectara y compartiera datos con otras computadoras. En un entorno NetBIOS, cuando una máquina se conecta, necesita un nombre, lo cual se realiza mediante el llamado `name registration`procedimiento. Cada host reserva su nombre de host en la red o se utiliza el [servidor de nombres NetBIOS](https://networkencyclopedia.com/netbios-name-server-nbns/) ( ) para este propósito. `NBNS`También se ha mejorado para [el Servicio de nombres de Internet de Windows](https://networkencyclopedia.com/windows-internet-name-service-wins/) ( `WINS`).

***

## <mark style="color:purple;">Configuración predeterminada</mark>

Como podemos imaginar, Samba ofrece una amplia gama de [ajustes](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html) que podemos configurar. Nuevamente, definimos la configuración a través de un archivo de texto donde podemos obtener una descripción general de algunas de las configuraciones. Estas configuraciones se ven similares a las siguientes cuando se filtran:

```bash
afsh4ck$ cat /etc/samba/smb.conf | grep -v "#\|\;" 

[global]
   workgroup = DEV.INFREIGHT.HTB
   server string = DEVSMB
   log file = /var/log/samba/log.%m
   max log size = 1000
   logging = file
   panic action = /usr/share/samba/panic-action %d

   server role = standalone server
   obey pam restrictions = yes
   unix password sync = yes

   passwd program = /usr/bin/passwd %u
   passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n *password\supdated\ssuccessfully* .

   pam password change = yes
   map to guest = bad user
   usershare allow guests = yes

[printers]
   comment = All Printers
   browseable = no
   path = /var/spool/samba
   printable = yes
   guest ok = no
   read only = yes
   create mask = 0700

[print$]
   comment = Printer Drivers
   path = /var/lib/samba/printers
   browseable = yes
   read only = yes
   guest ok = no
```

Vemos configuraciones globales y dos recursos compartidos destinados a impresoras. La configuración global es la configuración del servidor SMB disponible que se utiliza para todos los recursos compartidos. Sin embargo, en los recursos compartidos individuales se pueden sobrescribir los ajustes globales, que probablemente incluso se configuren incorrectamente. Veamos algunas de las configuraciones para comprender cómo se configuran los recursos compartidos en Samba.

<table data-header-hidden><thead><tr><th width="331"></th><th></th></tr></thead><tbody><tr><td><strong>Configuración</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>[sharename]</code></td><td>El nombre del recurso compartido de red.</td></tr><tr><td><code>workgroup = WORKGROUP/DOMAIN</code></td><td>Grupo de trabajo que aparecerá cuando los clientes consulten.</td></tr><tr><td><code>path = /path/here/</code></td><td>El directorio al que se le dará acceso al usuario.</td></tr><tr><td><code>server string = STRING</code></td><td>La cadena que aparecerá cuando se inicie una conexión.</td></tr><tr><td><code>unix password sync = yes</code></td><td>¿Sincronizar la contraseña de UNIX con la contraseña de SMB?</td></tr><tr><td><code>usershare allow guests = yes</code></td><td>¿Permitir que los usuarios no autenticados accedan al recurso compartido definido?</td></tr><tr><td><code>map to guest = bad user</code></td><td>¿Qué hacer cuando la solicitud de inicio de sesión de un usuario no coincide con un usuario UNIX válido?</td></tr><tr><td><code>browseable = yes</code></td><td>¿Esta acción debería aparecer en la lista de acciones disponibles?</td></tr><tr><td><code>guest ok = yes</code></td><td>¿Permitir conectarse al servicio sin usar contraseña?</td></tr><tr><td><code>read only = yes</code></td><td>¿Permitir a los usuarios leer solo archivos?</td></tr><tr><td><code>create mask = 0700</code></td><td>¿Qué permisos se deben establecer para los archivos recién creados?</td></tr></tbody></table>

***

## <mark style="color:purple;">Configuraciones peligrosas</mark>

Algunas de las configuraciones anteriores ya traen algunas opciones sensibles. Sin embargo, supongamos que cuestionamos las configuraciones que se enumeran a continuación y nos preguntamos qué podrían ganar los empleados con ellas, así como los atacantes. En ese caso veremos qué ventajas y desventajas traen consigo los ajustes.&#x20;

Tomemos el escenario `browseable = yes` como ejemplo. Si nosotros, como administradores, adoptamos esta configuración, los empleados de la empresa tendrán la comodidad de poder consultar las carpetas individuales con el contenido. Eventualmente se utilizan muchas carpetas para una mejor organización y estructura. Si el empleado puede navegar a través de los recursos compartidos, el atacante también podrá hacerlo después de acceder con éxito.

<table data-header-hidden><thead><tr><th width="293"></th><th></th></tr></thead><tbody><tr><td><strong>Configuración</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>browseable = yes</code></td><td>¿Permitir listar acciones disponibles en la acción actual?</td></tr><tr><td><code>read only = no</code></td><td>¿Prohibir la creación y modificación de archivos?</td></tr><tr><td><code>writable = yes</code></td><td>¿Permitir a los usuarios crear y modificar archivos?</td></tr><tr><td><code>guest ok = yes</code></td><td>¿Permitir conectarse al servicio sin usar contraseña?</td></tr><tr><td><code>enable privileges = yes</code></td><td>¿Respetar los privilegios asignados a un SID específico?</td></tr><tr><td><code>create mask = 0777</code></td><td>¿Qué permisos se deben asignar a los archivos recién creados?</td></tr><tr><td><code>directory mask = 0777</code></td><td>¿Qué permisos se deben asignar a los directorios recién creados?</td></tr><tr><td><code>logon script = script.sh</code></td><td>¿Qué script debe ejecutarse al iniciar sesión el usuario?</td></tr><tr><td><code>magic script = script.sh</code></td><td>¿Qué script debe ejecutarse cuando se cierra el script?</td></tr><tr><td><code>magic output = script.out</code></td><td>¿Dónde se debe almacenar la salida del script mágico?</td></tr></tbody></table>

Creemos un recurso compartido llamado `[notes]`y algunos otros y veamos cómo la configuración afecta nuestro proceso de enumeración. Usaremos todas las configuraciones anteriores y las aplicaremos a este recurso compartido. Por ejemplo, esta configuración se aplica a menudo, aunque sólo sea con fines de prueba. Si se trata de una subred interna de un equipo pequeño en un departamento grande, esta configuración a menudo se conserva o se olvida para restablecerla. Esto lleva al hecho de que podemos navegar por todos los recursos compartidos y, con una alta probabilidad, incluso descargarlos e inspeccionarlos.

### **Ejemplo de Share**

```shell-session
...SNIP...

[notes]
	comment = CheckIT
	path = /mnt/notes/

	browseable = yes
	read only = no
	writable = yes
	guest ok = yes

	enable privileges = yes
	create mask = 0777
	directory mask = 0777
```

Se recomienda encarecidamente consultar las páginas de manual de Samba, configurarlo nosotros mismos y experimentar con los ajustes. Luego descubriremos aspectos potenciales que nos resultarán interesantes como probadores de penetración. Además, cuanto más nos familiaricemos con el servidor Samba y SMB, más fácil será orientarnos en el entorno y utilizarlo para nuestros propósitos. Una vez nos hayamos ajustado `/etc/samba/smb.conf`a nuestras necesidades, tenemos que reiniciar el servicio en el servidor.

### **Reiniciar Samba**

```shell-session
root@samba:~# sudo systemctl restart smbd
```

Ahora podemos mostrar una lista ( `-L`) de los recursos compartidos del servidor con el comando `smbclient` de nuestro host. Usamos el llamado `null session`( `-N`), que es el acceso `anonymous` sin el ingreso de usuarios existentes o contraseñas válidas.

### **SMBclient - Conexión al recurso compartido**

```shell-session
afsh4ck@kali$ smbclient -N -L //10.129.14.128

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        home            Disk      INFREIGHT Samba
        dev             Disk      DEVenv
        notes           Disk      CheckIT
        IPC$            IPC       IPC Service (DEVSM)
SMB1 disabled -- no workgroup available
```

Podemos ver que ahora tenemos cinco recursos compartidos diferentes en el servidor Samba según el resultado. Por tanto `print$` y `IPC$`ya están incluidos por defecto en la configuración básica, como ya hemos visto. Ya que nos ocupamos del recurso compartido `[notes]`, iniciemos sesión e inspeccionemos usando el mismo programa cliente. Si no estamos familiarizados con el programa cliente, podemos usar el comando `help` al iniciar sesión correctamente, enumerando todos los comandos posibles que podemos ejecutar.

```shell-session
afsh4ck@kali$ smbclient //10.129.14.128/notes

Enter WORKGROUP\<username>'s password: 
Anonymous login successful
Try "help" to get a list of possible commands.

smb: \> help

?              allinfo        altname        archive        backup         
blocksize      cancel         case_sensitive cd             chmod          
chown          close          del            deltree        dir            
du             echo           exit           get            getfacl        
geteas         hardlink       help           history        iosize         
lcd            link           lock           lowercase      ls             
l              mask           md             mget           mkdir          
more           mput           newer          notify         open           
posix          posix_encrypt  posix_open     posix_mkdir    posix_rmdir    
posix_unlink   posix_whoami   print          prompt         put            
pwd            q              queue          quit           readlink       
rd             recurse        reget          rename         reput          
rm             rmdir          showacls       setea          setmode        
scopy          stat           symlink        tar            tarmode        
timeout        translate      unlock         volume         vuid           
wdel           logon          listconnect    showconnect    tcon           
tdis           tid            utimes         logoff         ..             
!            

smb: \> ls

  .                                   D        0  Wed Sep 22 18:17:51 2021
  ..                                  D        0  Wed Sep 22 12:03:59 2021
  prep-prod.txt                       N       71  Sun Sep 19 15:45:21 2021

                30313412 blocks of size 1024. 16480084 blocks available
```

Una vez que hayamos descubierto archivos o carpetas interesantes, podemos descargarlos usando el `get`comando. Smbclient también nos permite ejecutar comandos del sistema local usando un signo de exclamación al principio ( `!<cmd>`) sin interrumpir la conexión.

### **Descargar archivos desde SMB**

```bash
smb: \> get prep-prod.txt 

getting file \prep-prod.txt of size 71 as prep-prod.txt (8,7 KiloBytes/sec) 
(average 8,7 KiloBytes/sec)


smb: \> !ls

prep-prod.txt


smb: \> !cat prep-prod.txt

[] check your code with the templates
[] run code-assessment.py
[] …	
```

Desde el punto de vista administrativo, podemos comprobar estas conexiones mediante `smbstatus`. Además de la versión Samba, también podemos ver quién, desde qué host y qué recurso compartido está conectado el cliente. Esto es especialmente importante una vez que hemos entrado en una subred (quizás incluso aislada) a la que los demás aún pueden acceder.

Por ejemplo, con seguridad a nivel de dominio, el servidor samba actúa como miembro de un dominio de Windows. Cada dominio tiene al menos un controlador de dominio, normalmente un servidor Windows NT que proporciona autenticación de contraseña. Este controlador de dominio proporciona al grupo de trabajo un servidor de contraseñas definitivo. Los controladores de dominio realizan un seguimiento de los usuarios y las contraseñas en su propio `Security Authentication Module`( `SAM`) y autentican a cada usuario cuando inician sesión por primera vez y desean acceder al recurso compartido de otra máquina.

### **Estado de samba**

```shell-session
root@samba:~# smbstatus

Samba version 4.11.6-Ubuntu
PID     Username     Group        Machine                                   Protocol Version  Encryption           Signing              
----------------------------------------------------------------------------------------------------------------------------------------
75691   sambauser    samba        10.10.14.4 (ipv4:10.10.14.4:45564)      SMB3_11           -                    -                    

Service      pid     Machine       Connected at                     Encryption   Signing     
---------------------------------------------------------------------------------------------
notes        75691   10.10.14.4   Do Sep 23 00:12:06 2021 CEST     -            -           

No locked files
```

***

## <mark style="color:purple;">Enumeración del servicio</mark>

Volvamos a una de nuestras herramientas de enumeración. Nmap también tiene muchas opciones y scripts NSE que pueden ayudarnos a examinar más de cerca el servicio SMB del objetivo y obtener más información. La desventaja, sin embargo, es que estas exploraciones pueden llevar mucho tiempo. Por tanto, también es recomendable mirar el servicio manualmente, principalmente porque podemos encontrar muchos más detalles de los que Nmap podría mostrarnos. Sin embargo, primero veamos qué puede encontrar Nmap en nuestro servidor Samba de destino, donde creamos el recurso compartido `[notes]`con fines de prueba.

### **Nmap**

```bash
afsh4ck$ sudo nmap 10.129.14.128 -sV -sC -p139,445

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-19 15:15 CEST
Nmap scan report for sharing.inlanefreight.htb (10.129.14.128)
Host is up (0.00024s latency).

PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
MAC Address: 00:00:00:00:00:00 (VMware)

Host script results:
|_nbstat: NetBIOS name: HTB, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2021-09-19T13:16:04
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.35 seconds
```

Podemos ver en los resultados que Nmap no nos proporcionó mucho aquí. Por tanto, deberíamos recurrir a otras herramientas que nos permitan interactuar manualmente con la PYME y enviar solicitudes específicas de información. Una de las herramientas útiles para esto es `rpcclient`. Esta es una herramienta para realizar funciones de MS-RPC.

La [Llamada a Procedimiento Remoto](https://www.geeksforgeeks.org/remote-procedure-call-rpc-in-operating-system/) ( `RPC`) es un concepto y, por tanto, también una herramienta central para realizar estructuras operativas y de trabajo compartido en redes y arquitecturas cliente-servidor. El proceso de comunicación vía RPC incluye el paso de parámetros y la devolución de un valor de función.

### **RPC Client**

```bash
afsh4ck$ rpcclient -U "" 10.129.14.128

Enter WORKGROUP\'s password:
rpcclient $> 
```

Rpcclient nos ofrece muchas solicitudes diferentes con las que podemos ejecutar funciones específicas en el servidor SMB para obtener información. Puede encontrar una lista completa de todas estas funciones en la [página de manual](https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html) de rpcclient.

<table data-header-hidden><thead><tr><th width="277"></th><th></th></tr></thead><tbody><tr><td><strong>Consulta</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>srvinfo</code></td><td>Información del servidor.</td></tr><tr><td><code>enumdomains</code></td><td>Enumere todos los dominios que están implementados en la red.</td></tr><tr><td><code>querydominfo</code></td><td>Proporciona información de dominio, servidor y usuario de los dominios implementados.</td></tr><tr><td><code>netshareenumall</code></td><td>Enumera todas las acciones disponibles.</td></tr><tr><td><code>netsharegetinfo &#x3C;share></code></td><td>Proporciona información sobre una acción específica.</td></tr><tr><td><code>enumdomusers</code></td><td>Enumera todos los usuarios del dominio.</td></tr><tr><td><code>queryuser &#x3C;RID></code></td><td>Proporciona información sobre un usuario específico.</td></tr></tbody></table>

### **RPC Client: Enumeración**

```shell-session
rpcclient $> srvinfo

        DEVSMB         Wk Sv PrQ Unx NT SNT DEVSM
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03
		
		
rpcclient $> enumdomains

name:[DEVSMB] idx:[0x0]
name:[Builtin] idx:[0x1]


rpcclient $> querydominfo

Domain:         DEVOPS
Server:         DEVSMB
Comment:        DEVSM
Total Users:    2
Total Groups:   0
Total Aliases:  0
Sequence No:    1632361158
Force Logoff:   -1
Domain Server State:    0x1
Server Role:    ROLE_DOMAIN_PDC
Unknown 3:      0x1


rpcclient $> netshareenumall

netname: print$
        remark: Printer Drivers
        path:   C:\var\lib\samba\printers
        password:
netname: home
        remark: INFREIGHT Samba
        path:   C:\home\
        password:
netname: dev
        remark: DEVenv
        path:   C:\home\sambauser\dev\
        password:
netname: notes
        remark: CheckIT
        path:   C:\mnt\notes\
        password:
netname: IPC$
        remark: IPC Service (DEVSM)
        path:   C:\tmp
        password:
		
		
rpcclient $> netsharegetinfo notes

netname: notes
        remark: CheckIT
        path:   C:\mnt\notes\
        password:
        type:   0x0
        perms:  0
        max_uses:       -1
        num_uses:       1
revision: 1
type: 0x8004: SEC_DESC_DACL_PRESENT SEC_DESC_SELF_RELATIVE 
DACL
        ACL     Num ACEs:       1       revision:       2
        ---
        ACE
                type: ACCESS ALLOWED (0) flags: 0x00 
                Specific bits: 0x1ff
                Permissions: 0x101f01ff: Generic all access SYNCHRONIZE_ACCESS WRITE_OWNER_ACCESS WRITE_DAC_ACCESS READ_CONTROL_ACCESS DELETE_ACCESS 
                SID: S-1-1-0
```

Estos ejemplos nos muestran qué información se puede filtrar a usuarios anónimos. Una vez que un usuario`anónimo` tiene acceso a un servicio de red, solo se necesita un error para otorgarle demasiados permisos o demasiada visibilidad para poner en riesgo significativo a toda la red.

Lo más importante es que el acceso anónimo a dichos servicios también puede conducir al descubrimiento de otros usuarios, que pueden ser atacados con fuerza bruta en el caso más agresivo. Los seres humanos son más propensos a errores que los procesos informáticos configurados correctamente, y la falta de conciencia de seguridad y la pereza a menudo conducen a contraseñas débiles que pueden descifrarse fácilmente. Veamos cómo podemos enumerar usuarios usando `rpcclient`.

### **RPC Client - Enumeración de usuarios**

```shell-session
rpcclient $> enumdomusers

user:[mrb3n] rid:[0x3e8]
user:[cry0l1t3] rid:[0x3e9]


rpcclient $> queryuser 0x3e9

        User Name   :   cry0l1t3
        Full Name   :   cry0l1t3
        Home Drive  :   \\devsmb\cry0l1t3
        Dir Drive   :
        Profile Path:   \\devsmb\cry0l1t3\profile
        Logon Script:
        Description :
        Workstations:
        Comment     :
        Remote Dial :
        Logon Time               :      Do, 01 Jan 1970 01:00:00 CET
        Logoff Time              :      Mi, 06 Feb 2036 16:06:39 CET
        Kickoff Time             :      Mi, 06 Feb 2036 16:06:39 CET
        Password last set Time   :      Mi, 22 Sep 2021 17:50:56 CEST
        Password can change Time :      Mi, 22 Sep 2021 17:50:56 CEST
        Password must change Time:      Do, 14 Sep 30828 04:48:05 CEST
        unknown_2[0..31]...
        user_rid :      0x3e9
        group_rid:      0x201
        acb_info :      0x00000014
        fields_present: 0x00ffffff
        logon_divs:     168
        bad_password_count:     0x00000000
        logon_count:    0x00000000
        padding1[0..7]...
        logon_hrs[0..21]...


rpcclient $> queryuser 0x3e8

        User Name   :   mrb3n
        Full Name   :
        Home Drive  :   \\devsmb\mrb3n
        Dir Drive   :
        Profile Path:   \\devsmb\mrb3n\profile
        Logon Script:
        Description :
        Workstations:
        Comment     :
        Remote Dial :
        Logon Time               :      Do, 01 Jan 1970 01:00:00 CET
        Logoff Time              :      Mi, 06 Feb 2036 16:06:39 CET
        Kickoff Time             :      Mi, 06 Feb 2036 16:06:39 CET
        Password last set Time   :      Mi, 22 Sep 2021 17:47:59 CEST
        Password can change Time :      Mi, 22 Sep 2021 17:47:59 CEST
        Password must change Time:      Do, 14 Sep 30828 04:48:05 CEST
        unknown_2[0..31]...
        user_rid :      0x3e8
        group_rid:      0x201
        acb_info :      0x00000010
        fields_present: 0x00ffffff
        logon_divs:     168
        bad_password_count:     0x00000000
        logon_count:    0x00000000
        padding1[0..7]...
        logon_hrs[0..21]...
```

Luego podemos usar los resultados para identificar el RID del grupo, que luego podemos usar para recuperar información de todo el grupo.

### **RPC Client - Información del grupo**

```shell-session
rpcclient $> querygroup 0x201

        Group Name:     None
        Description:    Ordinary Users
        Group Attribute:7
        Num Members:2
```

Sin embargo, también puede ocurrir que no todos los comandos estén disponibles para nosotros, y tengamos ciertas restricciones en función del usuario. Sin embargo, la consulta `queryuser <RID>`se permite principalmente según el RID. Entonces podemos usar rpcclient para aplicar fuerza bruta a los RID para obtener información.&#x20;

Debido a que es posible que no sepamos a quién se le ha asignado qué RID, sabemos que obtendremos información al respecto tan pronto como consultemos un RID asignado. Hay varias formas y herramientas que podemos utilizar para esto. Para seguir con la herramienta, podemos crear un `For-loop`uso `Bash`donde enviamos un comando al servicio usando rpcclient y filtramos los resultados.

### Brute Force a **User RIDs**

{% code overflow="wrap" %}

```bash
afsh4ck@kali$ for i in $(seq 500 1100);do rpcclient -N -U "" 10.129.14.128 -c "queryuser 0x$(printf '%x\n' $i)" | grep "User Name\|user_rid\|group_rid" && echo "";done

        User Name   :   sambauser
        user_rid :      0x1f5
        group_rid:      0x201
		
        User Name   :   mrb3n
        user_rid :      0x3e8
        group_rid:      0x201
		
        User Name   :   cry0l1t3
        user_rid :      0x3e9
        group_rid:      0x201
```

{% endcode %}

Una alternativa a esto sería un script Python de [Impacket](https://github.com/SecureAuthCorp/impacket) llamado [samrdump.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/samrdump.py) .

### **Impacket - Samrdump.py**

```bash
afsh4ck$ samrdump.py 10.129.14.128

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Retrieving endpoint list from 10.129.14.128
Found domain(s):
 . DEVSMB
 . Builtin
[*] Looking up users in domain DEVSMB
Found user: mrb3n, uid = 1000
Found user: cry0l1t3, uid = 1001
mrb3n (1000)/FullName: 
mrb3n (1000)/UserComment: 
mrb3n (1000)/PrimaryGroupId: 513
mrb3n (1000)/BadPasswordCount: 0
mrb3n (1000)/LogonCount: 0
mrb3n (1000)/PasswordLastSet: 2021-09-22 17:47:59
mrb3n (1000)/PasswordDoesNotExpire: False
mrb3n (1000)/AccountIsDisabled: False
mrb3n (1000)/ScriptPath: 
cry0l1t3 (1001)/FullName: cry0l1t3
cry0l1t3 (1001)/UserComment: 
cry0l1t3 (1001)/PrimaryGroupId: 513
cry0l1t3 (1001)/BadPasswordCount: 0
cry0l1t3 (1001)/LogonCount: 0
cry0l1t3 (1001)/PasswordLastSet: 2021-09-22 17:50:56
cry0l1t3 (1001)/PasswordDoesNotExpire: False
cry0l1t3 (1001)/AccountIsDisabled: False
cry0l1t3 (1001)/ScriptPath: 
[*] Received 2 entries.
```

La información que ya hemos obtenido con `rpcclient`también la podemos obtener utilizando otras herramientas. Por ejemplo, las herramientas [SMBMap](https://github.com/ShawnDEvans/smbmap) y [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) también se utilizan ampliamente y son útiles para la enumeración de servicios SMB.

### **SMB Map**

```shell-session
afsh4ck@kali$ smbmap -H 10.129.14.128

[+] Finding open SMB ports....
[+] User SMB session established on 10.129.14.128...
[+] IP: 10.129.14.128:445       Name: 10.129.14.128                                     
        Disk                                    Permissions     Comment
        ----                                    -----------     -------
        print$                                  NO ACCESS       Printer Drivers
        home                                    NO ACCESS       INFREIGHT Samba
        dev                                     NO ACCESS       DEVenv
        notes                                   NO ACCESS       CheckIT
        IPC$                                    NO ACCESS       IPC Service (DEVSM)
```

### **CrackMapExec**

```shell-session
afsh4ck@kali$ crackmapexec smb 10.129.14.128 --shares -u '' -p ''

SMB         10.129.14.128   445    DEVSMB           [*] Windows 6.1 Build 0 (name:DEVSMB) (domain:) (signing:False) (SMBv1:False)
SMB         10.129.14.128   445    DEVSMB           [+] \: 
SMB         10.129.14.128   445    DEVSMB           [+] Enumerated shares
SMB         10.129.14.128   445    DEVSMB           Share           Permissions     Remark
SMB         10.129.14.128   445    DEVSMB           -----           -----------     ------
SMB         10.129.14.128   445    DEVSMB           print$                          Printer Drivers
SMB         10.129.14.128   445    DEVSMB           home                            INFREIGHT Samba
SMB         10.129.14.128   445    DEVSMB           dev                             DEVenv
SMB         10.129.14.128   445    DEVSMB           notes           READ,WRITE      CheckIT
SMB         10.129.14.128   445    DEVSMB           IPC$                            IPC Service (DEVSM)
```

Otra herramienta que vale la pena mencionar es la llamada [enum4linux-ng](https://github.com/cddmp/enum4linux-ng) , que se basa en una herramienta más antigua, enum4linux. Esta herramienta automatiza muchas de las consultas, pero no todas, y puede devolver una gran cantidad de información.

### **Enum4Linux-ng - Instalación**

```bash
git clone https://github.com/cddmp/enum4linux-ng.git
cd enum4linux-ng
pip3 install -r requirements.txt
```

### **Enum4Linux-ng - Enumeración**

```bash
afsh4ck@kali$ ./enum4linux-ng.py 10.129.14.128 -A

ENUM4LINUX - next generation

 ==========================
|    Target Information    |
 ==========================
[*] Target ........... 10.129.14.128
[*] Username ......... ''
[*] Random Username .. 'juzgtcsu'
[*] Password ......... ''
[*] Timeout .......... 5 second(s)

 =====================================
|    Service Scan on 10.129.14.128    |
 =====================================
[*] Checking LDAP
[-] Could not connect to LDAP on 389/tcp: connection refused
[*] Checking LDAPS
[-] Could not connect to LDAPS on 636/tcp: connection refused
[*] Checking SMB
[+] SMB is accessible on 445/tcp
[*] Checking SMB over NetBIOS
[+] SMB over NetBIOS is accessible on 139/tcp

 =====================================================
|    NetBIOS Names and Workgroup for 10.129.14.128    |
 =====================================================
[+] Got domain/workgroup name: DEVOPS
[+] Full NetBIOS names information:
- DEVSMB          <00> -         H <ACTIVE>  Workstation Service
- DEVSMB          <03> -         H <ACTIVE>  Messenger Service
- DEVSMB          <20> -         H <ACTIVE>  File Server Service
- ..__MSBROWSE__. <01> - <GROUP> H <ACTIVE>  Master Browser
- DEVOPS          <00> - <GROUP> H <ACTIVE>  Domain/Workgroup Name
- DEVOPS          <1d> -         H <ACTIVE>  Master Browser
- DEVOPS          <1e> - <GROUP> H <ACTIVE>  Browser Service Elections
- MAC Address = 00-00-00-00-00-00

 ==========================================
|    SMB Dialect Check on 10.129.14.128    |
 ==========================================
[*] Trying on 445/tcp
[+] Supported dialects and settings:
SMB 1.0: false
SMB 2.02: true
SMB 2.1: true
SMB 3.0: true
SMB1 only: false
Preferred dialect: SMB 3.0
SMB signing required: false

 ==========================================
|    RPC Session Check on 10.129.14.128    |
 ==========================================
[*] Check for null session
[+] Server allows session using username '', password ''
[*] Check for random user session
[+] Server allows session using username 'juzgtcsu', password ''
[H] Rerunning enumeration with user 'juzgtcsu' might give more results

 ====================================================
|    Domain Information via RPC for 10.129.14.128    |
 ====================================================
[+] Domain: DEVOPS
[+] SID: NULL SID
[+] Host is part of a workgroup (not a domain)

 ============================================================
|    Domain Information via SMB session for 10.129.14.128    |
 ============================================================
[*] Enumerating via unauthenticated SMB session on 445/tcp
[+] Found domain information via SMB
NetBIOS computer name: DEVSMB
NetBIOS domain name: ''
DNS domain: ''
FQDN: htb

 ================================================
|    OS Information via RPC for 10.129.14.128    |
 ================================================
[*] Enumerating via unauthenticated SMB session on 445/tcp
[+] Found OS information via SMB
[*] Enumerating via 'srvinfo'
[+] Found OS information via 'srvinfo'
[+] After merging OS information we have the following result:
OS: Windows 7, Windows Server 2008 R2
OS version: '6.1'
OS release: ''
OS build: '0'
Native OS: not supported
Native LAN manager: not supported
Platform id: '500'
Server type: '0x809a03'
Server type string: Wk Sv PrQ Unx NT SNT DEVSM

 ======================================
|    Users via RPC on 10.129.14.128    |
 ======================================
[*] Enumerating users via 'querydispinfo'
[+] Found 2 users via 'querydispinfo'
[*] Enumerating users via 'enumdomusers'
[+] Found 2 users via 'enumdomusers'
[+] After merging user results we have 2 users total:
'1000':
  username: mrb3n
  name: ''
  acb: '0x00000010'
  description: ''
'1001':
  username: cry0l1t3
  name: cry0l1t3
  acb: '0x00000014'
  description: ''

 =======================================
|    Groups via RPC on 10.129.14.128    |
 =======================================
[*] Enumerating local groups
[+] Found 0 group(s) via 'enumalsgroups domain'
[*] Enumerating builtin groups
[+] Found 0 group(s) via 'enumalsgroups builtin'
[*] Enumerating domain groups
[+] Found 0 group(s) via 'enumdomgroups'

 =======================================
|    Shares via RPC on 10.129.14.128    |
 =======================================
[*] Enumerating shares
[+] Found 5 share(s):
IPC$:
  comment: IPC Service (DEVSM)
  type: IPC
dev:
  comment: DEVenv
  type: Disk
home:
  comment: INFREIGHT Samba
  type: Disk
notes:
  comment: CheckIT
  type: Disk
print$:
  comment: Printer Drivers
  type: Disk
[*] Testing share IPC$
[-] Could not check share: STATUS_OBJECT_NAME_NOT_FOUND
[*] Testing share dev
[-] Share doesn't exist
[*] Testing share home
[+] Mapping: OK, Listing: OK
[*] Testing share notes
[+] Mapping: OK, Listing: OK
[*] Testing share print$
[+] Mapping: DENIED, Listing: N/A

 ==========================================
|    Policies via RPC for 10.129.14.128    |
 ==========================================
[*] Trying port 445/tcp
[+] Found policy:
domain_password_information:
  pw_history_length: None
  min_pw_length: 5
  min_pw_age: none
  max_pw_age: 49710 days 6 hours 21 minutes
  pw_properties:
  - DOMAIN_PASSWORD_COMPLEX: false
  - DOMAIN_PASSWORD_NO_ANON_CHANGE: false
  - DOMAIN_PASSWORD_NO_CLEAR_CHANGE: false
  - DOMAIN_PASSWORD_LOCKOUT_ADMINS: false
  - DOMAIN_PASSWORD_PASSWORD_STORE_CLEARTEXT: false
  - DOMAIN_PASSWORD_REFUSE_PASSWORD_CHANGE: false
domain_lockout_information:
  lockout_observation_window: 30 minutes
  lockout_duration: 30 minutes
  lockout_threshold: None
domain_logoff_information:
  force_logoff_time: 49710 days 6 hours 21 minutes

 ==========================================
|    Printers via RPC for 10.129.14.128    |
 ==========================================
[+] No printers returned (this is not an error)

Completed after 0.61 seconds
```

Necesitamos utilizar más de dos herramientas para la enumeración. Porque puede suceder que debido a la programación de las herramientas, obtengamos información diferente que tengamos que comprobar manualmente. Por lo tanto, nunca debemos confiar únicamente en herramientas automatizadas de las que no sabemos exactamente cómo fueron escritas.

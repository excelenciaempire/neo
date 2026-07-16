
# Protocolos de Administración Remota - Linux

## <mark style="color:purple;">Introducción</mark>

***

En el mundo de las distribuciones de Linux, existen muchas formas de administrar los servidores de forma remota. Por ejemplo, imaginemos que estamos en una de muchas ubicaciones y uno de nuestros empleados que acaba de acudir a un cliente en otra ciudad necesita nuestra ayuda debido a un error que no puede solucionar. En la mayoría de los casos, la resolución de problemas eficiente parecerá difícil a través de una llamada telefónica, por lo que es beneficioso si sabemos cómo iniciar sesión en el sistema remoto para administrarlo.

Estas aplicaciones y servicios se pueden encontrar en casi todos los servidores de la red pública. Ahorra tiempo ya que no tenemos que estar físicamente presentes en el servidor y el entorno de trabajo sigue teniendo el mismo aspecto. Estos protocolos y aplicaciones para la gestión remota de sistemas son un objetivo interesante por estos motivos. Si la configuración es incorrecta, nosotros, como probadores de penetración, podemos incluso acceder rápidamente al sistema remoto. Por tanto, conviene que nos familiaricemos con los protocolos, servidores y aplicaciones más importantes para este fin.

***

## <mark style="color:purple;">SSH</mark>

[Secure Shell](https://en.wikipedia.org/wiki/Secure_Shell) ( `SSH`) permite que dos computadoras establezcan una conexión directa y cifrada dentro de una red posiblemente insegura en el puerto estándar `TCP 22`. Esto es necesario para evitar que terceros intercepten el flujo de datos y, por tanto, intercepten datos confidenciales. El servidor SSH también se puede configurar para permitir solo conexiones de clientes específicos. Una ventaja de SSH es que el protocolo se ejecuta en todos los sistemas operativos comunes.&#x20;

Dado que originalmente es una aplicación Unix, también se implementa de forma nativa en todas las distribuciones de Linux y MacOS. SSH también se puede utilizar en Windows, siempre que instalemos un programa adecuado. El conocido servidor [OpenBSD SSH](https://www.openssh.com/) ( `OpenSSH`) en distribuciones de Linux es una bifurcación de código abierto del servidor `SSH` original y comercial de SSH Communication Security. En consecuencia, existen dos protocolos en competencia: `SSH-1`y `SSH-2`.

`SSH-2`, también conocido como SSH versión 2, es un protocolo más avanzado que SSH versión 1 en cifrado, velocidad, estabilidad y seguridad. Por ejemplo, `SSH-1` es vulnerable a [ataques `MITM`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/man-in-the-middle.md), mientras que SSH-2 no lo es.

Podemos imaginar que queremos administrar un host remoto. Esto se puede hacer a través de la línea de comando o GUI. Además, también podemos utilizar el protocolo SSH para enviar comandos al sistema deseado, transferir archivos o reenviar puertos. Por lo tanto, debemos conectarnos mediante el protocolo SSH y autenticarnos en él. En total, OpenSSH tiene seis métodos de autenticación diferentes:

1. `Password authentication`
2. `Public-key authentication`
3. `Host-based authentication`
4. `Keyboard authentication`
5. `Challenge-response authentication`
6. `GSSAPI authentication`

Examinaremos más de cerca y analizaremos uno de los métodos de autenticación más utilizados. Además, podemos aprender más sobre los otros métodos de autenticación [aquí](https://www.golinuxcloud.com/openssh-authentication-methods-sshd-config/) entre otros.

### **Autenticación de clave pública**

En un primer paso, el servidor SSH y el cliente se autentican entre sí. El servidor envía un certificado al cliente para verificar que es el servidor correcto. Sólo cuando se establece el contacto por primera vez existe el riesgo de que un tercero se interponga entre los dos participantes e intercepte así la conexión. Dado que el certificado en sí también está cifrado, no se puede imitar. Una vez que el cliente conoce el certificado correcto, nadie más puede pretender establecer contacto a través del servidor correspondiente.

Sin embargo, después de la autenticación del servidor, el cliente también debe demostrar al servidor que tiene autorización de acceso. Sin embargo, el servidor SSH ya posee el valor hash cifrado de la contraseña establecida para el usuario deseado. Como resultado, los usuarios deben ingresar la contraseña cada vez que inician sesión en otro servidor durante la misma sesión. Por este motivo, una opción alternativa para la autenticación del lado del cliente es el uso de un par de claves públicas y privadas.

La clave privada se crea individualmente para la computadora del usuario y se protege con una frase de contraseña que debe ser más larga que una contraseña típica. La clave privada se almacena exclusivamente en nuestro propio ordenador y siempre permanece secreta. Si queremos establecer una conexión SSH, primero ingresamos la frase de contraseña y así abrimos el acceso a la clave privada.

Las claves públicas también se almacenan en el servidor. El servidor crea un problema criptográfico con la clave pública del cliente y se lo envía al cliente. El cliente, a su vez, descifra el problema con su propia clave privada, devuelve la solución y así informa al servidor que puede establecer una conexión legítima. Durante una sesión, los usuarios solo necesitan ingresar la frase de contraseña una vez para conectarse a cualquier número de servidores. Al final de la sesión, los usuarios cierran la sesión de sus máquinas locales, lo que garantiza que ningún tercero que obtenga acceso físico a la máquina local pueda conectarse al servidor.

***

### <mark style="color:purple;">Configuración predeterminada</mark>

El archivo [sshd\_config](https://www.ssh.com/academy/ssh/sshd_config) , responsable del servidor OpenSSH, tiene solo algunas de las configuraciones configuradas de forma predeterminada. Sin embargo, la configuración predeterminada incluye el reenvío X11, que contenía una vulnerabilidad de inyección de comandos en la versión 7.2p1 de OpenSSH en 2016. Sin embargo, no necesitamos una GUI para administrar nuestros servidores.

```bash
afsh4ck$ cat /etc/ssh/sshd_config  | grep -v "#" | sed -r '/^\s*$/d'

Include /etc/ssh/sshd_config.d/*.conf
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding yes
PrintMotd no
AcceptEnv LANG LC_*
Subsystem       sftp    /usr/lib/openssh/sftp-server
```

La mayoría de las configuraciones en este archivo de configuración están comentadas y requieren configuración manual.

***

### <mark style="color:purple;">Configuraciones peligrosas</mark>

A pesar de que el protocolo SSH es uno de los protocolos más seguros disponibles en la actualidad, algunas configuraciones erróneas aún pueden hacer que el servidor SSH sea vulnerable a ataques fáciles de ejecutar. Echemos un vistazo a las siguientes configuraciones:

<table data-header-hidden><thead><tr><th width="310"></th><th></th></tr></thead><tbody><tr><td><strong>Configuración</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>PasswordAuthentication yes</code></td><td>Permite la autenticación basada en contraseña.</td></tr><tr><td><code>PermitEmptyPasswords yes</code></td><td>Permite el uso de contraseñas vacías.</td></tr><tr><td><code>PermitRootLogin yes</code></td><td>Permite iniciar sesión como usuario root.</td></tr><tr><td><code>Protocol 1</code></td><td>Utiliza una versión desactualizada de cifrado.</td></tr><tr><td><code>X11Forwarding yes</code></td><td>Permite el reenvío X11 para aplicaciones GUI.</td></tr><tr><td><code>AllowTcpForwarding yes</code></td><td>Permite el reenvío de puertos TCP.</td></tr><tr><td><code>PermitTunnel</code></td><td>Permite hacer túneles.</td></tr><tr><td><code>DebianBanner yes</code></td><td>Muestra un banner específico al iniciar sesión.</td></tr></tbody></table>

Los patrones de autorización `password authentication` nos `permite forzar por fuerza bruta` un nombre de usuario conocido para posibles contraseñas. Se pueden utilizar muchos métodos diferentes para adivinar las contraseñas de los usuarios. Para ello se especificanse suelen utilizar para mutar las contraseñas más utilizadas y, aterradoramente, corregirlas. Esto se debe a que los humanos somos vagos y no queremos recordar contraseñas complejas y complicadas. Por lo tanto, creamos contraseñas que podemos recordar fácilmente, y esto lleva a que, por ejemplo, se agreguen números o caracteres solo al final de la contraseña. Creyendo que la contraseña es segura, los patrones mencionados se utilizan para adivinar precisamente tales "ajustes" de estas contraseñas. Sin embargo, se pueden utilizar algunas instrucciones y [guías de refuerzo para reforzar nuestros servidores SSH.](https://www.ssh-audit.com/hardening_guides.html)

***

## <mark style="color:purple;">Enumeración del servicio</mark>

Una de las herramientas que podemos utilizar para tomar huellas dactilares del servidor SSH es [ssh-audit](https://github.com/jtesta/ssh-audit) . Comprueba la configuración del lado del cliente y del servidor y muestra información general y qué algoritmos de cifrado todavía utilizan el cliente y el servidor. Por supuesto, esto podría explotarse atacando al servidor o al cliente a un nivel críptico más adelante.

### **SSH Audit**

```bash
afsh4ck$ git clone https://github.com/jtesta/ssh-audit.git && cd ssh-audit
afsh4ck$ ./ssh-audit.py 10.129.14.132

# general
(gen) banner: SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3
(gen) software: OpenSSH 8.2p1
(gen) compatibility: OpenSSH 7.4+, Dropbear SSH 2018.76+
(gen) compression: enabled (zlib@openssh.com)                                   

# key exchange algorithms
(kex) curve25519-sha256                     -- [info] available since OpenSSH 7.4, Dropbear SSH 2018.76                            
(kex) curve25519-sha256@libssh.org          -- [info] available since OpenSSH 6.5, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp256                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp384                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp521                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) diffie-hellman-group-exchange-sha256 (2048-bit) -- [info] available since OpenSSH 4.4
(kex) diffie-hellman-group16-sha512         -- [info] available since OpenSSH 7.3, Dropbear SSH 2016.73
(kex) diffie-hellman-group18-sha512         -- [info] available since OpenSSH 7.3
(kex) diffie-hellman-group14-sha256         -- [info] available since OpenSSH 7.3, Dropbear SSH 2016.73

# host-key algorithms
(key) rsa-sha2-512 (3072-bit)               -- [info] available since OpenSSH 7.2
(key) rsa-sha2-256 (3072-bit)               -- [info] available since OpenSSH 7.2
(key) ssh-rsa (3072-bit)                    -- [fail] using weak hashing algorithm
                                            `- [info] available since OpenSSH 2.5.0, Dropbear SSH 0.28
                                            `- [info] a future deprecation notice has been issued in OpenSSH 8.2: https://www.openssh.com/txt/release-8.2
(key) ecdsa-sha2-nistp256                   -- [fail] using weak elliptic curves
                                            `- [warn] using weak random number generator could reveal the key
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(key) ssh-ed25519                           -- [info] available since OpenSSH 6.5
...SNIP...
```

Lo primero que podemos ver en las primeras líneas del resultado es el banner que revela la versión del servidor OpenSSH. Las versiones anteriores tenían algunas vulnerabilidades, como [CVE-2020-14145](https://www.cvedetails.com/cve/CVE-2020-14145/) , que permitía al atacante la capacidad de realizar Man-In-The-Middle y atacar el intento de conexión inicial. El resultado detallado de la configuración de la conexión con el servidor OpenSSH a menudo también puede proporcionar información importante, como qué métodos de autenticación puede utilizar el servidor.

### **Cambiar método de autenticación**

```bash
afsh4ck$ ssh -v cry0l1t3@10.129.14.132

OpenSSH_8.2p1 Ubuntu-4ubuntu0.3, OpenSSL 1.1.1f  31 Mar 2020
debug1: Reading configuration data /etc/ssh/ssh_config 
...SNIP...
debug1: Authentications that can continue: publickey,password,keyboard-interactive
```

Para posibles ataques de fuerza bruta, podemos especificar el método de autenticación con la opción de cliente SSH `PreferredAuthentications`.

```bash
afsh4ck$ ssh -v cry0l1t3@10.129.14.132 -o PreferredAuthentications=password

OpenSSH_8.2p1 Ubuntu-4ubuntu0.3, OpenSSL 1.1.1f  31 Mar 2020
debug1: Reading configuration data /etc/ssh/ssh_config
...SNIP...
debug1: Authentications that can continue: publickey,password,keyboard-interactive
debug1: Next authentication method: password

cry0l1t3@10.129.14.132's password:
```

Incluso con este servicio obvio y seguro, recomendamos configurar nuestro propio servidor OpenSSH en nuestra VM, experimentar con él y familiarizarnos con las diferentes configuraciones y opciones.

Es posible que nos encontremos con varios banners para el servidor SSH durante nuestras pruebas de penetración. De forma predeterminada, los banners comienzan con la versión del protocolo que se puede aplicar y luego la versión del propio servidor. Por ejemplo, con `SSH-1.99-OpenSSH_3.9p1`, sabemos que podemos usar ambas versiones del protocolo SSH-1 y SSH-2, y estamos tratando con la versión 3.9p1 del servidor OpenSSH. Por otro lado, para un banner con `SSH-2.0-OpenSSH_8.2p1`, estamos ante una versión OpenSSH 8.2p1 que sólo acepta la versión del protocolo SSH-2.

***

## <mark style="color:purple;">Rsync</mark>

[Rsync](https://linux.die.net/man/1/rsync) es una herramienta rápida y eficiente para copiar archivos de forma local y remota. Se puede utilizar para copiar archivos localmente en una máquina determinada y hacia/desde hosts remotos. Es muy versátil y conocido por su algoritmo de transferencia delta. Este algoritmo reduce la cantidad de datos transmitidos a través de la red cuando ya existe una versión del archivo en el host de destino. Para ello, envía solo las diferencias entre los archivos de origen y la versión anterior de los archivos que residen en el servidor de destino. A menudo se utiliza para copias de seguridad y duplicación. Encuentra archivos que deben transferirse observando los archivos que han cambiado de tamaño o la hora de la última modificación. De forma predeterminada, utiliza un puerto `873`y se puede configurar para usar SSH para transferencias seguras de archivos al utilizar una conexión de servidor SSH establecida.

Esta [guía](https://book.hacktricks.xyz/network-services-pentesting/873-pentesting-rsync) cubre algunas de las formas en que se puede abusar de Rsync, en particular enumerando el contenido de una carpeta compartida en un servidor de destino y recuperando archivos. A veces esto se puede hacer sin autenticación. Otras veces necesitaremos credenciales. Si encuentra credenciales durante un pentest y ejecuta Rsync en un host interno (o externo), siempre vale la pena verificar la reutilización de la contraseña, ya que es posible que pueda extraer algunos archivos confidenciales que podrían usarse para obtener acceso remoto a el objetivo.

Hagamos un poco de enumeración rápida. Podemos ver que Rsync está en uso usando el protocolo 31.

### **Buscando Rsync**

```bash
afsh4ck$ sudo nmap -sV -p 873 127.0.0.1

Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-19 09:31 EDT
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0058s latency).

PORT    STATE SERVICE VERSION
873/tcp open  rsync   (protocol version 31)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.13 seconds
```

### **Probando servicios accesibles**

A continuación podemos probar un poco el servicio para ver a qué podemos acceder.

```bash
afsh4ck$ nc -nv 127.0.0.1 873

(UNKNOWN) [127.0.0.1] 873 (rsync) open
@RSYNCD: 31.0
@RSYNCD: 31.0
#list
dev            	Dev Tools
@RSYNCD: EXIT
```

### **Enumerar un recurso compartido abierto**

```bash
afsh4ck$ rsync -av --list-only rsync://127.0.0.1/dev

receiving incremental file list
drwxr-xr-x             48 2022/09/19 09:43:10 .
-rw-r--r--              0 2022/09/19 09:34:50 build.sh
-rw-r--r--              0 2022/09/19 09:36:02 secrets.yaml
drwx------             54 2022/09/19 09:43:10 .ssh

sent 25 bytes  received 221 bytes  492.00 bytes/sec
total size is 0  speedup is 0.00
```

En el resultado anterior, podemos ver algunos archivos interesantes que pueden valer la pena consultar para investigar más a fondo. También podemos ver que se puede acceder a un directorio que probablemente contenga claves SSH. Desde aquí, podríamos sincronizar todos los archivos con nuestro host de ataque con el comando `rsync -av rsync://127.0.0.1/dev`. Si Rsync está configurado para usar SSH para transferir archivos, podríamos modificar nuestros comandos para incluir la flag `-e ssh`, o `-e "ssh -p2222"`si se usa un puerto no estándar para SSH. Esta [guía](https://phoenixnap.com/kb/how-to-rsync-over-ssh) es útil para comprender la sintaxis para usar Rsync sobre SSH.

***

## <mark style="color:purple;">R-Services</mark>

Los R-Services son un conjunto de servicios alojados para permitir el acceso remoto o emitir comandos entre hosts Unix a través de TCP/IP. Desarrollados inicialmente por el Computer Systems Research Group ( `CSRG`) de la Universidad de California, Berkeley, `r-services` fueron el estándar de facto para el acceso remoto entre sistemas operativos Unix hasta que fueron reemplazados por los protocolos `SSH` y comandos Secure Shell ( ) debido a fallas de seguridad inherentes incorporadas. a ellos. Al igual que `telnet`, los R-Services transmiten información del cliente al servidor (y viceversa) a través de la red en un formato no cifrado, lo que permite a los atacantes interceptar el tráfico de la red (contraseñas, información de inicio de sesión, etc.) mediante la realización de operaciones man-in-. ataques del medio ( [`MITM`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/man-in-the-middle.md)).

Los `R-services` abarcan los puertos `512`, `513`y `514`solo se puede acceder a ellos a través de un conjunto de programas conocidos como `r-commands`. Se utilizan con mayor frecuencia en sistemas operativos comerciales como Solaris, HP-UX y AIX. Aunque son menos comunes hoy en día, nos topamos con ellos de vez en cuando durante nuestras pruebas de penetración internas, por lo que vale la pena entender cómo abordarlos.

La suite [R-commands](https://en.wikipedia.org/wiki/Berkeley_r-commands) consta de los siguientes programas:

* rcp (`remote copy`)
* rexec (`remote execution`)
* rlogin (`remote login`)
* rsh (`remote shell`)
* rstat
* ruptime
* rwho (`remote who`)

Cada comando tiene su funcionalidad prevista; sin embargo, solo cubriremos los más comúnmente abusados `r-commands`. La siguiente tabla proporcionará una descripción general rápida de los comandos de los que se abusa con más frecuencia, incluido el demonio de servicio con el que interactúan, a qué puerto y método de transporte se puede acceder y una breve descripción de cada uno.

<table data-header-hidden><thead><tr><th width="114"></th><th width="97"></th><th width="89"></th><th width="107"></th><th></th></tr></thead><tbody><tr><td><strong>Comando</strong></td><td><strong>Daemon</strong></td><td><strong>Puerto</strong></td><td><strong>Protocolo</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>rcp</code></td><td><code>rshd</code></td><td>514</td><td>tcp</td><td>Copia un archivo o directorio bidireccionalmente desde el sistema local al sistema remoto (o viceversa) o de un sistema remoto a otro. Funciona como el comando <code>cp</code> en Linux pero <code>no hay advertencia para el usuario por sobrescribir archivos existentes en un sistema..</code></td></tr><tr><td><code>rsh</code></td><td><code>rshd</code></td><td>514</td><td>tcp</td><td>Abre un shell en una máquina remota sin un procedimiento de inicio de sesión. Se basa en las entradas confiables en los archivos <code>/etc/hosts.equiv</code>y <code>.rhosts</code>para su validación.</td></tr><tr><td><code>rexec</code></td><td><code>rexecd</code></td><td>512</td><td>tcp</td><td>Permite a un usuario ejecutar comandos de shell en una máquina remota. Requiere autenticación mediante el uso de un <code>username</code>y <code>password</code> a través de un socket de red no cifrado. La autenticación es anulada por las entradas confiables en los archivos <code>/etc/hosts.equiv</code>y <code>.rhosts</code>.</td></tr><tr><td><code>rlogin</code></td><td><code>rlogind</code></td><td>513</td><td>tcp</td><td>Permite a un usuario iniciar sesión en un host remoto a través de la red. Funciona de manera similar a <code>telnet</code> pero sólo puede conectarse a hosts tipo Unix. La autenticación es anulada por las entradas confiables en los archivos <code>/etc/hosts.equiv</code>y <code>.rhosts</code>.</td></tr></tbody></table>

El archivo `/etc/hosts.equiv` contiene una lista de hosts confiables y se utiliza para otorgar acceso a otros sistemas en la red. Cuando los usuarios de uno de estos hosts intentan acceder al sistema, se les concede acceso automáticamente sin necesidad de autenticación adicional.

### **/etc/hosts.equiv**

```bash
afsh4ck$ cat /etc/hosts.equiv

# <hostname> <local username>
pwnbox cry0l1t3
```

Ahora que tenemos un conocimiento básico de `r-commands`, hagamos una enumeración rápida usando `Nmap` para determinar si todos los puertos necesarios están abiertos.

### **Escaneo en busca de R-Services**

```bash
afsh4ck$ sudo nmap -sV -p 512,513,514 10.0.17.2

Starting Nmap 7.80 ( https://nmap.org ) at 2022-12-02 15:02 EST
Nmap scan report for 10.0.17.2
Host is up (0.11s latency).

PORT    STATE SERVICE    VERSION
512/tcp open  exec?
513/tcp open  login?
514/tcp open  tcpwrapped

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 145.54 seconds
```

### **Control de acceso y relaciones de confianza**

La principal preocupación de `r-services`, y una de las principales razones por `SSH`las que se introdujo para reemplazarlo, son los problemas inherentes relacionados con el control de acceso a estos protocolos. Los servicios R se basan en información confiable enviada desde el cliente remoto a la máquina host en la que intentan autenticarse.&#x20;

De forma predeterminada, estos servicios utilizan [módulos de autenticación conectables (PAM)](https://debathena.mit.edu/trac/wiki/PAM) para la autenticación del usuario en un sistema remoto; sin embargo, también omiten esta autenticación mediante el uso de archivos `/etc/hosts.equiv`y `.rhosts`en el sistema. Los archivos `hosts.equiv`y `.rhosts`contienen una lista de hosts ( `IPs`o `Hostnames`) y usuarios que se encuentran `trusted`junto al host local cuando se realiza un intento de conexión mediante `r-commands`. Las entradas en cualquiera de los archivos pueden tener el siguiente aspecto:

{% hint style="info" %}
**Nota:** El archivo `hosts.equiv`se reconoce como la configuración global de todos los usuarios de un sistema, mientras que `.rhosts`proporciona una configuración por usuario.
{% endhint %}

### **Archivo .rhosts de muestra**

```shell-session
afsh4ck@kali$ cat .rhosts

htb-student     10.0.17.5
+               10.0.17.10
+               +
```

Como podemos ver en este ejemplo, ambos archivos siguen la sintaxis específica de `<username> <ip address>`o `<username> <hostname>` . Además, el modificador `+` se puede utilizar dentro de estos archivos como comodín para especificar cualquier cosa. En este ejemplo, el modificador `+` permite que cualquier usuario externo acceda a los comandos r desde la cuenta `htb-student` de usuario a través del host con la dirección IP `10.0.17.10`.

Las configuraciones incorrectas en cualquiera de estos archivos pueden permitir que un atacante se autentique como otro usuario sin credenciales, con el potencial de obtener la ejecución del código. Ahora que entendemos cómo podemos potencialmente abusar de las configuraciones erróneas en estos archivos, intentemos iniciar sesión en un host de destino usando `rlogin`.

### **Iniciar sesión usando Rlogin**

```shell-session
afsh4ck@kali$ rlogin 10.0.17.2 -l htb-student

Last login: Fri Dec  2 16:11:21 from localhost

[htb-student@localhost ~]$
```

Hemos iniciado sesión correctamente con la cuenta `htb-student` en el host remoto debido a configuraciones erróneas en el archivo `.rhosts`. Una vez que hayamos iniciado sesión correctamente, también podemos abusar del comando `rwho` para enumerar todas las sesiones interactivas en la red local enviando solicitudes al `puerto UDP 513`.

### **Listado de usuarios autenticados mediante Rwho**

```shell-session
afsh4ck@kali$ rwho

root     web01:pts/0 Dec  2 21:34
htb-student     workstn01:tty1  Dec  2 19:57  2:25       
```

A partir de esta información, podemos ver que el usuario  `htb-student`está actualmente autenticado en el host `workstn01`, mientras que el usuario `root` está autenticado en el host. `web01` Podemos usar esto a nuestro favor al buscar posibles nombres de usuario para usar durante futuros ataques a hosts en la red. Sin embargo, el demonio `rwho` transmite periódicamente información sobre los usuarios que han iniciado sesión, por lo que podría resultar beneficioso observar el tráfico de la red.

### **Listado de usuarios autenticados que utilizan Rusers**

Para proporcionar información adicional junto con `rwho`, podemos emitir el comando `rusers`. Esto nos brindará una cuenta más detallada de todos los usuarios que iniciaron sesión en la red, incluida información como el nombre de usuario, el nombre de host de la máquina a la que se accede, el TTY en el que el usuario inició sesión, la fecha y hora en que el usuario inició sesión, el cantidad de tiempo desde que el usuario escribió en el teclado y el host remoto desde el que inició sesión (si corresponde).

```shell-session
afsh4ck@kali$ rusers -al 10.0.17.5

htb-student     10.0.17.5:console          Dec 2 19:57     2:25
```

Como podemos ver, los servicios R se utilizan con menos frecuencia hoy en día debido a sus fallos de seguridad inherentes y a la disponibilidad de protocolos más seguros como SSH. Para ser un profesional completo de seguridad de la información, debemos tener un conocimiento amplio y profundo de muchos sistemas, aplicaciones, protocolos, etc. Por lo tanto, guarde este conocimiento sobre los servicios R porque nunca se sabe cuándo puede encontrarlos.

***

## <mark style="color:purple;">Reflexiones finales</mark>

Los servicios de gestión remota pueden proporcionarnos un tesoro de datos y, a menudo, se puede abusar de ellos para acceder sin autorización a través de credenciales débiles o predeterminadas o de la reutilización de contraseñas. Siempre debemos investigar estos servicios para obtener toda la información que podamos recopilar y no dejar piedra sin remover, especialmente cuando hemos compilado una lista de credenciales de otras partes de la red de destino.

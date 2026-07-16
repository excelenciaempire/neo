
# FTP

Por lo tanto, está en la misma capa que `HTTP`o `POP`. Estos protocolos también funcionan con el soporte de navegadores o clientes de correo electrónico para realizar sus servicios. También existen programas FTP especiales para el Protocolo de transferencia de archivos.

## <mark style="color:purple;">Introducción</mark>

Imaginemos que queremos subir archivos locales a un servidor y descargar otros archivos mediante el protocolo [FTP](https://datatracker.ietf.org/doc/html/rfc959) . En una conexión FTP se abren dos canales. Primero, el cliente y el servidor establecen un canal de control a través de `TCP port 21`. El cliente envía comandos al servidor y el servidor devuelve códigos de estado. Entonces ambos participantes de la comunicación pueden establecer el canal de datos a través de `TCP port 20`. Este canal se utiliza exclusivamente para la transmisión de datos y el protocolo vigila los errores durante este proceso. Si se interrumpe una conexión durante la transmisión, el transporte se puede reanudar después de restablecer el contacto.

Se hace una distinción entre enumeración `activa` y `pasiva` de FTP. En la variante activa, el cliente establece la conexión como se describe a través del puerto TCP 21 y así informa al servidor a través de qué puerto del cliente el servidor puede transmitir sus respuestas. Sin embargo, si un firewall protege al cliente, el servidor no puede responder porque todas las conexiones externas están bloqueadas. Para ello se ha desarrollado el `passive mode`. Aquí, el servidor anuncia un puerto a través del cual el cliente puede establecer el canal de datos. Dado que el cliente inicia la conexión con este método, el firewall no bloquea la transferencia.

El FTP conoce diferentes [comandos](https://www.smartfile.com/blog/the-ultimate-ftp-commands-list/) y códigos de estado. No todos estos comandos se implementan de forma consistente en el servidor. Por ejemplo, el lado del cliente indica al lado del servidor que cargue o descargue archivos, organice directorios o elimine archivos. El servidor responde en cada caso con un código de estado que indica si el comando se implementó correctamente. Puede encontrar una lista de posibles códigos de estado [aquí](https://en.wikipedia.org/wiki/List_of_FTP_server_return_codes) .

Normalmente, necesitamos credenciales para utilizar FTP en un servidor. También necesitamos saber que FTP es un `clear-text`protocolo que a veces puede detectarse si las condiciones de la red son las adecuadas. Sin embargo, también existe la posibilidad que ofrece un servidor `anonymous FTP`. Luego, el operador del servidor permite que cualquier usuario cargue o descargue archivos a través de FTP sin utilizar una contraseña. Dado que existen riesgos de seguridad asociados con un servidor FTP público de este tipo, las opciones para los usuarios suelen ser limitadas.

***

## <mark style="color:purple;">TFTP</mark>

`Trivial File Transfer Protocol`( `TFTP`) es más simple que FTP y realiza transferencias de archivos entre procesos de cliente y servidor. Sin embargo, `no proporciona autenticación de usuario` y otras funciones valiosas compatibles con FTP. Además, mientras FTP usa TCP, TFTP usa `UDP`, lo que lo convierte en un protocolo poco confiable y hace que use recuperación de capa de aplicación asistida por UDP.

Esto se refleja, por ejemplo, en el hecho de que TFTP, a diferencia de FTP, no requiere autenticación del usuario. No admite el inicio de sesión protegido mediante contraseñas y establece límites de acceso basados ​​únicamente en los permisos de lectura y escritura de un archivo en el sistema operativo. En la práctica, esto lleva a que TFTP opere exclusivamente en directorios y con archivos que han sido compartidos con todos los usuarios y pueden leerse y escribirse globalmente. Debido a la falta de seguridad, TFTP, a diferencia de FTP, sólo puede utilizarse en redes locales y protegidas.

Echemos un vistazo a algunos comandos de `TFTP`:

<table data-header-hidden><thead><tr><th width="147"></th><th></th></tr></thead><tbody><tr><td><strong>Comandos</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>connect</code></td><td>Establece el host remoto y, opcionalmente, el puerto para transferencias de archivos.</td></tr><tr><td><code>get</code></td><td>Transfiere un archivo o conjunto de archivos desde el host remoto al host local.</td></tr><tr><td><code>put</code></td><td>Transfiere un archivo o conjunto de archivos desde el host local al host remoto.</td></tr><tr><td><code>quit</code></td><td>Sale de tftp.</td></tr><tr><td><code>status</code></td><td>Muestra el estado actual de tftp, incluido el modo de transferencia actual (ascii o binario), el estado de la conexión, el valor de tiempo de espera, etc.</td></tr><tr><td><code>verbose</code></td><td>Activa o desactiva el modo detallado, que muestra información adicional durante la transferencia de archivos.</td></tr></tbody></table>

A diferencia del cliente FTP, `TFTP` no tiene funcionalidad de listado de directorios.

***

## <mark style="color:purple;">Configuración predeterminada</mark>

Uno de los servidores FTP más utilizados en distribuciones basadas en Linux es [vsFTPd](https://security.appspot.com/vsftpd.html) . La configuración predeterminada de vsFTPd se puede encontrar en `/etc/vsftpd.conf`y algunas configuraciones ya están predefinidas de forma predeterminada. Se recomienda encarecidamente instalar el servidor vsFTPd en una máquina virtual y observar más de cerca esta configuración.

### **Instalar vsFTPd**

```bash
sudo apt install vsftpd 
```

El servidor vsFTPd es sólo uno de los pocos servidores FTP disponibles para nosotros. Existen muchas alternativas diferentes, que además traen consigo, entre otras cosas, muchas más funciones y opciones de configuración. Usaremos el servidor vsFTPd porque es una excelente manera de mostrar las posibilidades de configuración de un servidor FTP de una manera sencilla y fácil de entender sin entrar en los detalles de las páginas del manual. Si miramos el archivo de configuración de vsFTPd, veremos muchas opciones y configuraciones que están comentadas o no. Sin embargo, el archivo de configuración no contiene todas las configuraciones posibles que se pueden realizar. Los existentes y los que faltan se pueden encontrar en la [página de manual](http://vsftpd.beasts.org/vsftpd_conf.html) .

### **Archivo de configuración vsFTPd**

```bash
cat /etc/vsftpd.conf | grep -v "#"
```

<table data-header-hidden><thead><tr><th width="294"></th><th></th></tr></thead><tbody><tr><td><strong>Configuración</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>listen=NO</code></td><td>¿Ejecutar desde inetd o como un demonio independiente?</td></tr><tr><td><code>listen_ipv6=YES</code></td><td>¿Escuchar en IPv6?</td></tr><tr><td><code>anonymous_enable=NO</code></td><td>¿Habilitar acceso anónimo?</td></tr><tr><td><code>local_enable=YES</code></td><td>¿Permitir que los usuarios locales inicien sesión?</td></tr><tr><td><code>dirmessage_enable=YES</code></td><td>¿Mostrar mensajes del directorio activo cuando los usuarios acceden a determinados directorios?</td></tr><tr><td><code>use_localtime=YES</code></td><td>¿Usar la hora local?</td></tr><tr><td><code>xferlog_enable=YES</code></td><td>¿Activar el registro de cargas/descargas?</td></tr><tr><td><code>connect_from_port_20=YES</code></td><td>¿Conectar desde el puerto 20?</td></tr><tr><td><code>secure_chroot_dir=/var/run/vsftpd/empty</code></td><td>Nombre de un directorio vacío</td></tr><tr><td><code>pam_service_name=vsftpd</code></td><td>Esta cadena es el nombre del servicio PAM que utilizará vsftpd.</td></tr><tr><td><code>rsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem</code></td><td>Las últimas tres opciones especifican la ubicación del certificado RSA que se utilizará para conexiones cifradas SSL.</td></tr><tr><td><code>rsa_private_key_file=/etc/ssl/private/ssl-cert-snakeoil.key</code></td><td></td></tr><tr><td><code>ssl_enable=NO</code></td><td></td></tr></tbody></table>

Además, hay un archivo llamado `/etc/ftpusers` al que también debemos prestar atención, ya que este archivo se utiliza para denegar el acceso al servicio FTP a ciertos usuarios. En el siguiente ejemplo, los usuarios `guest`, `john`y `kevin` no pueden iniciar sesión en el servicio FTP, incluso si existen en el sistema Linux.

### **ftpusers**

```bash
cat /etc/ftpusers

guest
john
kevin
```

***

## <mark style="color:purple;">Configuraciones peligrosas</mark>

Hay muchas configuraciones diferentes relacionadas con la seguridad que podemos realizar en cada servidor FTP. Estos pueden tener varios propósitos, como probar conexiones a través de firewalls, probar rutas y mecanismos de autenticación. Uno de estos mecanismos de autenticación es el `anonymous` usuario. Esto se utiliza a menudo para permitir que todos en la red interna compartan archivos y datos sin acceder a las computadoras de los demás. Con vsFTPd, las [configuraciones opcionales](http://vsftpd.beasts.org/vsftpd_conf.html) que se pueden agregar al archivo de configuración para el inicio de sesión anónimo tienen este aspecto:

<table data-header-hidden><thead><tr><th width="334"></th><th></th></tr></thead><tbody><tr><td><strong>Configuración</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>anonymous_enable=YES</code></td><td>¿Permitir el inicio de sesión anónimo?</td></tr><tr><td><code>anon_upload_enable=YES</code></td><td>¿Permitir que anónimo cargue archivos?</td></tr><tr><td><code>anon_mkdir_write_enable=YES</code></td><td>¿Permitir que anónimo cree nuevos directorios?</td></tr><tr><td><code>no_anon_password=YES</code></td><td>¿No pedir contraseña a un anónimo?</td></tr><tr><td><code>anon_root=/home/username/ftp</code></td><td>Directorio para anónimos.</td></tr><tr><td><code>write_enable=YES</code></td><td>¿Permitir el uso de comandos FTP: STOR, DELE, RNFR, RNTO, MKD, RMD, APPE y SITE?</td></tr></tbody></table>

Con el cliente FTP estándar ( `ftp`), podemos acceder al servidor FTP en consecuencia e iniciar sesión con el usuario anónimo si se han utilizado las configuraciones que se muestran arriba. El uso de la cuenta anónima puede ocurrir en entornos e infraestructuras internos donde todos los participantes son conocidos. El acceso a este tipo de servicio se puede configurar de forma temporal o con la configuración para acelerar el intercambio de archivos.

Tan pronto como nos conectamos al servidor vsFTPd, se muestra un `response code 220` con el banner del servidor FTP. A menudo este banner contiene la descripción del mismo servicio e incluso la `versión` del mismo. También nos indica qué tipo de sistema es el servidor FTP. Una de las configuraciones más comunes de los servidores FTP es permitir el acceso `anonymous`, lo que no requiere credenciales legítimas pero proporciona acceso a algunos archivos. Aunque no podamos descargarlos, a veces basta con enumerar los contenidos para generar más ideas y anotar información que nos ayudará en otro enfoque.

### **Inicio de sesión anónimo**

```bash
ftp 10.129.14.136

Connected to 10.129.14.136.
220 "Welcome to the HTB Academy vsFTP service."
Name (10.129.14.136:cry0l1t3): anonymous

230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.

ftp> ls

200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-rw-r--    1 1002     1002      8138592 Sep 14 16:54 Calender.pptx
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Clients
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Documents
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Employees
-rw-rw-r--    1 1002     1002           41 Sep 14 16:45 Important Notes.txt
226 Directory send OK.
```

Sin embargo, para obtener una primera descripción general de la configuración del servidor, podemos usar el siguiente comando:

### **Estado vsFTPd**

```bash
ftp> status

Connected to 10.129.14.136.
No proxy connection.
Connecting using address family: any.
Mode: stream; Type: binary; Form: non-print; Structure: file
Verbose: on; Bell: off; Prompting: on; Globbing: on
Store unique: off; Receive unique: off
Case: off; CR stripping: on
Quote control characters: on
Ntrans: off
Nmap: off
Hash mark printing: off; Use of PORT cmds: on
Tick counter printing: off
```

Algunos comandos conviene utilizarlos ocasionalmente, ya que estos harán que el servidor nos muestre más información que podemos utilizar para nuestros propósitos. Estos comandos incluyen `debug`y `trace`.

### **Salida detallada de vsFTPd**

```bash
ftp> debug

Debugging on (debug=1).

ftp> trace

Packet tracing on.

ftp> ls

---> PORT 10,10,14,4,188,195
200 PORT command successful. Consider using PASV.
---> LIST
150 Here comes the directory listing.
-rw-rw-r--    1 1002     1002      8138592 Sep 14 16:54 Calender.pptx
drwxrwxr-x    2 1002     1002         4096 Sep 14 17:03 Clients
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Documents
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Employees
-rw-rw-r--    1 1002     1002           41 Sep 14 16:45 Important Notes.txt
226 Directory send OK.
```

<table data-header-hidden><thead><tr><th width="301"></th><th></th></tr></thead><tbody><tr><td><strong>Configuración</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>dirmessage_enable=YES</code></td><td>¿Mostrar un mensaje cuando ingresan por primera vez a un nuevo directorio?</td></tr><tr><td><code>chown_uploads=YES</code></td><td>¿Cambiar la propiedad de los archivos cargados de forma anónima?</td></tr><tr><td><code>chown_username=username</code></td><td>Usuario al que se le otorga la propiedad de los archivos cargados de forma anónima.</td></tr><tr><td><code>local_enable=YES</code></td><td>¿Permitir que los usuarios locales inicien sesión?</td></tr><tr><td><code>chroot_local_user=YES</code></td><td>¿Colocar a los usuarios locales en su directorio de inicio?</td></tr><tr><td><code>chroot_list_enable=YES</code></td><td>¿Utilizar una lista de usuarios locales que se colocarán en su directorio de inicio?</td></tr><tr><td><code>hide_ids=YES</code></td><td>Toda la información de usuarios y grupos en los listados de directorios se mostrará como "ftp".</td></tr><tr><td><code>ls_recurse_enable=YES</code></td><td>Permite el uso de listados recurrentes.</td></tr></tbody></table>

En el siguiente ejemplo, podemos ver que si la configuración `hide_ids=YES` está presente, la representación UID y GUID del servicio se sobrescribirá, lo que nos hará más difícil identificar con qué derechos se escriben y cargan estos archivos.

### hide\_ids=YES

```bash
ftp> ls

---> TYPE A
200 Switching to ASCII mode.
ftp: setsockopt (ignored): Permission denied
---> PORT 10,10,14,4,223,101
200 PORT command successful. Consider using PASV.
---> LIST
150 Here comes the directory listing.
-rw-rw-r--    1 ftp     ftp      8138592 Sep 14 16:54 Calender.pptx
drwxrwxr-x    2 ftp     ftp         4096 Sep 14 17:03 Clients
drwxrwxr-x    2 ftp     ftp         4096 Sep 14 16:50 Documents
drwxrwxr-x    2 ftp     ftp         4096 Sep 14 16:50 Employees
-rw-rw-r--    1 ftp     ftp           41 Sep 14 16:45 Important Notes.txt
-rw-------    1 ftp     ftp            0 Sep 15 14:57 testupload.txt
226 Directory send OK.
```

Esta configuración es una característica de seguridad para evitar que se revelen los nombres de usuario locales. Con los nombres de usuario, podríamos atacar servicios como FTP y SSH y muchos otros con un ataque de fuerza bruta en teoría. Sin embargo, en realidad, las soluciones [fail2ban](https://en.wikipedia.org/wiki/Fail2ban) son ahora una implementación estándar de cualquier infraestructura que registra la dirección IP y bloquea todo acceso a la infraestructura después de una cierta cantidad de intentos fallidos de inicio de sesión.

Otra configuración útil que podemos utilizar para nuestros propósitos es `ls_recurse_enable=YES`. Esto suele configurarse en el servidor vsFTPd para tener una mejor visión general de la estructura del directorio FTP, ya que nos permite ver todo el contenido visible a la vez.

### **Listado recursivo**

```bash
ftp> ls -R

---> PORT 10,10,14,4,222,149
200 PORT command successful. Consider using PASV.
---> LIST -R
150 Here comes the directory listing.
.:
-rw-rw-r--    1 ftp      ftp      8138592 Sep 14 16:54 Calender.pptx
drwxrwxr-x    2 ftp      ftp         4096 Sep 14 17:03 Clients
drwxrwxr-x    2 ftp      ftp         4096 Sep 14 16:50 Documents
drwxrwxr-x    2 ftp      ftp         4096 Sep 14 16:50 Employees
-rw-rw-r--    1 ftp      ftp           41 Sep 14 16:45 Important Notes.txt
-rw-------    1 ftp      ftp            0 Sep 15 14:57 testupload.txt

./Clients:
drwx------    2 ftp      ftp          4096 Sep 16 18:04 HackTheBox
drwxrwxrwx    2 ftp      ftp          4096 Sep 16 18:00 Inlanefreight

./Clients/HackTheBox:
-rw-r--r--    1 ftp      ftp         34872 Sep 16 18:04 appointments.xlsx
-rw-r--r--    1 ftp      ftp        498123 Sep 16 18:04 contract.docx
-rw-r--r--    1 ftp      ftp        478237 Sep 16 18:04 contract.pdf
-rw-r--r--    1 ftp      ftp           348 Sep 16 18:04 meetings.txt

./Clients/Inlanefreight:
-rw-r--r--    1 ftp      ftp         14211 Sep 16 18:00 appointments.xlsx
-rw-r--r--    1 ftp      ftp         37882 Sep 16 17:58 contract.docx
-rw-r--r--    1 ftp      ftp            89 Sep 16 17:58 meetings.txt
-rw-r--r--    1 ftp      ftp        483293 Sep 16 17:59 proposal.pptx

./Documents:
-rw-r--r--    1 ftp      ftp         23211 Sep 16 18:05 appointments-template.xlsx
-rw-r--r--    1 ftp      ftp         32521 Sep 16 18:05 contract-template.docx
-rw-r--r--    1 ftp      ftp        453312 Sep 16 18:05 contract-template.pdf

./Employees:
226 Directory send OK.

```

`Descargar` los archivos de dicho servidor FTP son una de las características principales, así como `subir` los archivos creados por nosotros. Esto nos permite, por ejemplo, utilizar vulnerabilidades LFI para hacer que el host ejecute comandos del sistema. Aparte de los archivos, podemos ver, descargar e inspeccionar. Los ataques también son posibles con los registros FTP, lo que lleva a `Remote Command Execution`( `RCE`). Esto se aplica a los servicios FTP y a todos aquellos que podamos detectar durante nuestra fase de enumeración.

### **Descargar un archivo**

```bash
ftp> ls

200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rwxrwxrwx    1 ftp      ftp             0 Sep 16 17:24 Calendar.pptx
drwxrwxrwx    4 ftp      ftp          4096 Sep 16 17:57 Clients
drwxrwxrwx    2 ftp      ftp          4096 Sep 16 18:05 Documents
drwxrwxrwx    2 ftp      ftp          4096 Sep 16 17:24 Employees
-rwxrwxrwx    1 ftp      ftp            41 Sep 18 15:58 Important Notes.txt
226 Directory send OK.

ftp> get Important\ Notes.txt

local: Important Notes.txt remote: Important Notes.txt
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for Important Notes.txt (41 bytes).
226 Transfer complete.
41 bytes received in 0.00 secs (606.6525 kB/s)

ftp> exit

221 Goodbye.
```

```bash
ls | grep Notes.txt

'Important Notes.txt'
```

También podemos descargar todos los archivos y carpetas a los que tenemos acceso a la vez. Esto es especialmente útil si el servidor FTP tiene muchos archivos diferentes en una estructura de carpetas más grande. Sin embargo, esto puede generar alarmas porque normalmente nadie de la empresa quiere descargar todos los archivos y contenidos de una vez.

### **Descargar todos los archivos disponibles**

```bash
wget -m --no-passive ftp://anonymous:anonymous@10.129.14.136

--2021-09-19 14:45:58--  ftp://anonymous:*password*@10.129.14.136/                                         
           => ‘10.129.14.136/.listing’                                                                     
Connecting to 10.129.14.136:21... connected.                                                               
Logging in as anonymous ... Logged in!
==> SYST ... done.    ==> PWD ... done.
==> TYPE I ... done.  ==> CWD not needed.
==> PORT ... done.    ==> LIST ... done.                                                                 
12.12.1.136/.listing           [ <=>                                  ]     466  --.-KB/s    in 0s       
                                                                                                         
2021-09-19 14:45:58 (65,8 MB/s) - ‘10.129.14.136/.listing’ saved [466]                                     
--2021-09-19 14:45:58--  ftp://anonymous:*password*@10.129.14.136/Calendar.pptx   
           => ‘10.129.14.136/Calendar.pptx’                                       
==> CWD not required.                                                           
==> SIZE Calendar.pptx ... done.                                                                                                                            
==> PORT ... done.    ==> RETR Calendar.pptx ... done.       

...SNIP...

2021-09-19 14:45:58 (48,3 MB/s) - ‘10.129.14.136/Employees/.listing’ saved [119]

FINISHED --2021-09-19 14:45:58--
Total wall clock time: 0,03s
Downloaded: 15 files, 1,7K in 0,001s (3,02 MB/s)
```

Una vez hayamos descargado todos los archivos, con `wget` crearemos un directorio con el nombre de la dirección IP de nuestro objetivo. Todos los archivos descargados se almacenan allí, que luego podemos inspeccionar localmente.

```bash
afsh4ck$ tree .

.
└── 10.129.14.136
    ├── Calendar.pptx
    ├── Clients
    │   └── Inlanefreight
    │       ├── appointments.xlsx
    │       ├── contract.docx
    │       ├── meetings.txt
    │       └── proposal.pptx
    ├── Documents
    │   ├── appointments-template.xlsx
    │   ├── contract-template.docx
    │   └── contract-template.pdf
    ├── Employees
    └── Important Notes.txt

5 directories, 9 files
```

A continuación, podemos comprobar si tenemos los permisos para subir archivos al servidor FTP. Especialmente con los servidores web, es común que los archivos se sincronicen y los desarrolladores tengan acceso rápido a los archivos. FTP se utiliza a menudo para este propósito y, la mayoría de las veces, los errores de configuración se encuentran en servidores que los administradores creen que no son detectables. La actitud de que no se puede acceder a los componentes internos de la red desde el exterior significa que a menudo se descuida el refuerzo de los sistemas internos y conduce a configuraciones erróneas.

La capacidad de cargar archivos al servidor FTP conectado a un servidor web aumenta la probabilidad de obtener acceso directo al servidor web e incluso a un shell inverso que nos permite ejecutar comandos internos del sistema y tal vez incluso aumentar nuestros privilegios.

### **Cargar un archivo**

```bash
afsh4ck$ touch testupload.txt
```

Con el comando `put`, podemos cargar archivos en la carpeta actual al servidor FTP.

```bash
ftp> put testupload.txt 

local: testupload.txt remote: testupload.txt
---> PORT 10,10,14,4,184,33
200 PORT command successful. Consider using PASV.
---> STOR testupload.txt
150 Ok to send data.
226 Transfer complete.

ftp> ls

---> TYPE A
200 Switching to ASCII mode.
---> PORT 10,10,14,4,223,101
200 PORT command successful. Consider using PASV.
---> LIST
150 Here comes the directory listing.
-rw-rw-r--    1 1002     1002      8138592 Sep 14 16:54 Calender.pptx
drwxrwxr-x    2 1002     1002         4096 Sep 14 17:03 Clients
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Documents
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Employees
-rw-rw-r--    1 1002     1002           41 Sep 14 16:45 Important Notes.txt
-rw-------    1 1002     133             0 Sep 15 14:57 testupload.txt
226 Directory send OK.

```

***

## <mark style="color:purple;">Enumeración del servicio</mark>

La enumeración utilizando varios escáneres de red también es un método práctico y generalizado. Estas herramientas nos facilitan la identificación de diferentes servicios, incluso si no son accesibles en puertos estándar. Una de las herramientas más utilizadas para este fin es Nmap. Nmap también incluye [Nmap Scripting Engine](https://nmap.org/book/nse.html) ( `NSE`), un conjunto de muchos scripts diferentes escritos para servicios específicos. Puede encontrar más información sobre las capacidades de Nmap y NSE en el módulo [Enumeración de redes con Nmap](https://academy.hackthebox.com/course/preview/network-enumeration-with-nmap) . Podemos actualizar esta base de datos de scripts NSE con el comando que se muestra.

### **Scripts FTP de Nmap**

```bash
afsh4ck$ sudo nmap --script-updatedb

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-19 13:49 CEST
NSE: Updating rule database.
NSE: Script Database updated successfully.
Nmap done: 0 IP addresses (0 hosts up) scanned in 0.28 seconds
```

Todos los scripts NSE se encuentran en en `/usr/share/nmap/scripts/`, pero en nuestros sistemas, podemos encontrarlos usando un comando simple en nuestro sistema.

```bash
afsh4ck$ find / -type f -name ftp* 2>/dev/null | grep scripts

/usr/share/nmap/scripts/ftp-syst.nse
/usr/share/nmap/scripts/ftp-vsftpd-backdoor.nse
/usr/share/nmap/scripts/ftp-vuln-cve2010-4221.nse
/usr/share/nmap/scripts/ftp-proftpd-backdoor.nse
/usr/share/nmap/scripts/ftp-bounce.nse
/usr/share/nmap/scripts/ftp-libopie.nse
/usr/share/nmap/scripts/ftp-anon.nse
/usr/share/nmap/scripts/ftp-brute.nse
```

Como ya sabemos, el servidor FTP suele ejecutarse en el puerto TCP estándar 21, que podemos escanear mediante Nmap. También utilizamos el escaneo de versión ( `-sV`), el escaneo agresivo ( `-A`) y el escaneo de script predeterminado ( `-sC`) contra nuestro objetivo `10.129.14.136`.

### **Nmap**

```bash
afsh4ck$ sudo nmap -sV -p 21 -sC -A 10.129.14.136

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-16 18:12 CEST
Nmap scan report for 10.129.14.136
Host is up (0.00013s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.0.8 or later
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rwxrwxrwx    1 ftp      ftp       8138592 Sep 16 17:24 Calendar.pptx [NSE: writeable]
| drwxrwxrwx    4 ftp      ftp          4096 Sep 16 17:57 Clients [NSE: writeable]
| drwxrwxrwx    2 ftp      ftp          4096 Sep 16 18:05 Documents [NSE: writeable]
| drwxrwxrwx    2 ftp      ftp          4096 Sep 16 17:24 Employees [NSE: writeable]
| -rwxrwxrwx    1 ftp      ftp            41 Sep 16 17:24 Important Notes.txt [NSE: writeable]
|_-rwxrwxrwx    1 ftp      ftp             0 Sep 15 14:57 testupload.txt [NSE: writeable]
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.10.14.4
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
```

El escaneo de script predeterminado se basa en la enumeración, las respuestas y los puertos estándar de los servicios. Una vez que Nmap ha detectado el servicio, ejecuta los scripts marcados uno tras otro, proporcionando información diferente. Por ejemplo, el script [ftp-anon](https://nmap.org/nsedoc/scripts/ftp-anon.html) NSE comprueba si el servidor FTP permite el acceso anónimo. Si es así, el contenido del directorio raíz FTP se representa para el usuario anónimo.

### Scripts NSE para FTP

```bash
ls -al /usr/share/nmap/scripts/ | grep -e "ftp" 
.rw-r--r-- root root 4.4 KB Thu Nov  2 03:10:47 2023 ftp-anon.nse
.rw-r--r-- root root 3.2 KB Thu Nov  2 03:10:47 2023 ftp-bounce.nse
.rw-r--r-- root root 3.0 KB Thu Nov  2 03:10:47 2023 ftp-brute.nse
.rw-r--r-- root root 3.2 KB Thu Nov  2 03:10:47 2023 ftp-libopie.nse
.rw-r--r-- root root 3.2 KB Thu Nov  2 03:10:47 2023 ftp-proftpd-backdoor.nse
.rw-r--r-- root root 3.7 KB Thu Nov  2 03:10:47 2023 ftp-syst.nse
.rw-r--r-- root root 5.9 KB Thu Nov  2 03:10:47 2023 ftp-vsftpd-backdoor.nse
.rw-r--r-- root root 5.8 KB Thu Nov  2 03:10:47 2023 ftp-vuln-cve2010-4221.nse
.rw-r--r-- root root 5.6 KB Thu Nov  2 03:10:47 2023 tftp-enum.nse
.rw-r--r-- root root 9.8 KB Thu Nov  2 03:10:47 2023 tftp-version.nse
```

`ftp-syst` por ejemplo, ejecuta el comando `STAT` que muestra información sobre el estado del servidor FTP. Esto incluye configuraciones así como la versión del servidor FTP. Nmap también brinda la capacidad de rastrear el progreso de los scripts NSE a nivel de red si usamos la opción `--script-trace` en nuestros escaneos. Esto nos permite ver qué comandos envía Nmap, qué puertos se utilizan y qué respuestas recibimos del servidor escaneado.

### **Seguimiento de script de Nmap**

```bash
sudo nmap -sV -p21 -sC -A 10.129.14.136 --script-trace

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-19 13:54 CEST                                                                                                                                                   
NSOCK INFO [11.4640s] nsock_trace_handler_callback(): Callback: CONNECT SUCCESS for EID 8 [10.129.14.136:21]                                   
NSOCK INFO [11.4640s] nsock_trace_handler_callback(): Callback: CONNECT SUCCESS for EID 16 [10.129.14.136:21]             
NSOCK INFO [11.4640s] nsock_trace_handler_callback(): Callback: CONNECT SUCCESS for EID 24 [10.129.14.136:21]
NSOCK INFO [11.4640s] nsock_trace_handler_callback(): Callback: CONNECT SUCCESS for EID 32 [10.129.14.136:21]
NSOCK INFO [11.4640s] nsock_read(): Read request from IOD #1 [10.129.14.136:21] (timeout: 7000ms) EID 42
NSOCK INFO [11.4640s] nsock_read(): Read request from IOD #2 [10.129.14.136:21] (timeout: 9000ms) EID 50
NSOCK INFO [11.4640s] nsock_read(): Read request from IOD #3 [10.129.14.136:21] (timeout: 7000ms) EID 58
NSOCK INFO [11.4640s] nsock_read(): Read request from IOD #4 [10.129.14.136:21] (timeout: 11000ms) EID 66
NSE: TCP 10.10.14.4:54226 > 10.129.14.136:21 | CONNECT
NSE: TCP 10.10.14.4:54228 > 10.129.14.136:21 | CONNECT
NSE: TCP 10.10.14.4:54230 > 10.129.14.136:21 | CONNECT
NSE: TCP 10.10.14.4:54232 > 10.129.14.136:21 | CONNECT
NSOCK INFO [11.4660s] nsock_trace_handler_callback(): Callback: READ SUCCESS for EID 50 [10.129.14.136:21] (41 bytes): 220 Welcome to HTB-Academy FTP service...
NSOCK INFO [11.4660s] nsock_trace_handler_callback(): Callback: READ SUCCESS for EID 58 [10.129.14.136:21] (41 bytes): 220 Welcome to HTB-Academy FTP service...
NSE: TCP 10.10.14.4:54228 < 10.129.14.136:21 | 220 Welcome to HTB-Academy FTP service.
```

El historial de análisis muestra que se están ejecutando cuatro análisis paralelos diferentes en el servicio, con varios tiempos de espera. Para los scripts NSE, vemos que nuestra máquina local usa otros puertos de salida ( ,,, `54226`) y primero inicia la conexión con el comando.&#x20;

Desde la primera respuesta del servidor, podemos ver que estamos recibiendo el banner del servidor en nuestro segundo script NSE ( ) del servidor FTP de destino. Si es necesario, por supuesto podemos utilizar otras aplicaciones como o para interactuar con el servidor FTP.

### **Interacción de servicio**

```bash
afsh4ck$ nc -nv 10.129.14.136 21
```

```bash
afsh4ck$ telnet 10.129.14.136 21
```

Se ve ligeramente diferente si el servidor FTP se ejecuta con cifrado TLS/SSL. Porque entonces necesitamos un cliente que pueda manejar TLS/SSL. Para ello podemos utilizar el cliente `openssl` y comunicarnos con el servidor FTP. Lo bueno de usar `openssl` es que podemos ver el certificado SSL, lo que también puede ser de ayuda.

```bash
openssl s_client -connect 10.129.14.136:21 -starttls ftp

CONNECTED(00000003)                                                                                      
Can't use SSL_get_servername                        
depth=0 C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Dev, CN = master.inlanefreight.htb, emailAddress = admin@inlanefreight.htb
verify error:num=18:self signed certificate
verify return:1

depth=0 C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Dev, CN = master.inlanefreight.htb, emailAddress = admin@inlanefreight.htb
verify return:1
---                                                 
Certificate chain
 0 s:C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Dev, CN = master.inlanefreight.htb, emailAddress = admin@inlanefreight.htb
 
 i:C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Dev, CN = master.inlanefreight.htb, emailAddress = admin@inlanefreight.htb
---
 
Server certificate

-----BEGIN CERTIFICATE-----

MIIENTCCAx2gAwIBAgIUD+SlFZAWzX5yLs2q3ZcfdsRQqMYwDQYJKoZIhvcNAQEL
...SNIP...
```

Esto se debe a que el certificado SSL nos permite reconocer el nombre del `host`, por ejemplo, y en la mayoría de los casos también la `dirección de email` de la organización o empresa. Además, si la empresa tiene varias ubicaciones en todo el mundo, también se pueden crear certificados para ubicaciones específicas, que también se pueden identificar mediante el certificado SSL.

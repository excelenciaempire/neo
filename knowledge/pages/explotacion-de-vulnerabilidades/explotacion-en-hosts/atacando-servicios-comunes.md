
# Atacando Servicios Comunes

Las vulnerabilidades suelen ser descubiertas por personas que utilizan y comprenden la tecnología, un protocolo o un servicio. A medida que evolucionemos en este campo, encontraremos diferentes servicios con los que interactuar y necesitaremos evolucionar y aprender nuevas tecnologías constantemente.

{% hint style="info" %}
Para tener éxito al atacar un servicio, necesitamos conocer su propósito, cómo interactuar con él, qué herramientas podemos usar y qué podemos hacer con él. Esta sección se centrará en los servicios comunes y en cómo podemos interactuar con ellos.
{% endhint %}

***

## <mark style="color:purple;">Servicios para compartir archivos</mark>

Un servicio para compartir archivos es un tipo de servicio que proporciona, media y supervisa la transferencia de archivos informáticos. Hace años, las empresas solían utilizar solo servicios internos para compartir archivos, como SMB, NFS, FTP, TFTP, SFTP, pero a medida que crece la adopción de la nube, la mayoría de las empresas ahora también cuentan con servicios de nube de terceros como Dropbox, Google Drive, OneDrive, SharePoint u otras formas de almacenamiento de archivos como AWS S3, Azure Blob Storage o Google Cloud Storage. Estaremos expuestos a una combinación de servicios de intercambio de archivos internos y externos, y debemos estar familiarizados con ellos.

Esta sección se centrará en los servicios internos, pero esto puede aplicarse al almacenamiento en la nube sincronizado localmente con servidores y estaciones de trabajo.

***

## <mark style="color:purple;">Server Message Block (SMB)</mark>

SMB se usa comúnmente en redes Windows y, a menudo, encontraremos carpetas compartidas en una red Windows. Podemos interactuar con SMB utilizando la GUI, CLI o herramientas. Cubramos algunas formas comunes de interactuar con SMB usando Windows y Linux.

## <mark style="color:purple;">**SMB en Windows**</mark>

Hay diferentes formas en que podemos interactuar con una carpeta compartida usando Windows y exploraremos algunas de ellas. En la GUI de Windows, podemos presionar `[WINKEY] + [R]` para abrir el cuadro de diálogo Ejecutar y escribir la ubicación del archivo compartido, por ejemplo:`\\192.168.220.129\Finance\`

![texto](https://academy.hackthebox.com/storage/modules/116/windows_run_sharefolder2.jpg)

Supongamos que la carpeta compartida permite la autenticación anónima, o estamos autenticados con un usuario que tiene privilegios sobre esa carpeta compartida. En ese caso, no recibiremos ningún tipo de solicitud de autenticación y mostrará el contenido de la carpeta compartida.

![imagen](https://academy.hackthebox.com/storage/modules/116/finance_share_folder2.jpg)

Si no tenemos acceso, recibiremos una solicitud de autenticación.

![texto](https://academy.hackthebox.com/storage/modules/116/auth_request_share_folder2.jpg)

Windows tiene dos shells de línea de comandos: el [shell de comandos](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands) y [PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/overview) . Cada shell es un programa de software que proporciona comunicación directa entre nosotros y el sistema operativo o la aplicación, proporcionando un entorno para automatizar las operaciones de TI.

Analicemos algunos comandos para interactuar con archivos compartidos usando Command Shell ( `CMD`) y `PowerShell`. El comando [dir](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/dir) muestra una lista de los archivos y subdirectorios de un directorio.

### **Windows CMD - DIR**

```powershell
C:\afsh4ck> dir \\192.168.220.129\Finance\

Volume in drive \\192.168.220.129\Finance has no label.
Volume Serial Number is ABCD-EFAA

Directory of \\192.168.220.129\Finance

02/23/2022  11:35 AM    <DIR>          Contracts
               0 File(s)          4,096 bytes
               1 Dir(s)  15,207,469,056 bytes free
```

El comando [net use](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/gg651155\(v=ws.11\)) conecta o desconecta una computadora de un recurso compartido o muestra información sobre las conexiones de la computadora. Podemos conectarnos a un archivo compartido con el siguiente comando y asignar su contenido a la letra de la unidad `n`.

### **Windows CMD - Net Use**

```powershell
C:\afsh4ck> net use n: \\192.168.220.129\Finance

The command completed successfully.
```

También podemos proporcionar un nombre de usuario y contraseña para autenticarse en el recurso compartido.

```powershell
C:\afsh4ck> net use n: \\192.168.220.129\Finance /user:plaintext Password123

The command completed successfully.
```

Con la carpeta compartida asignada como unidad `n`, podemos ejecutar comandos de Windows como si esta carpeta compartida estuviera en nuestra computadora local. Busquemos cuántos archivos contiene la carpeta compartida y sus subdirectorios.

### **Windows CMD - DIR**

```powershell
C:\afsh4ck> dir n: /a-d /s /b | find /c ":\"

29302
```

Encontramos 29.302 archivos. Repasemos el comando:

```powershell
dir n: /a-d /s /b | find /c ":\"
```

<table data-header-hidden><thead><tr><th width="133"></th><th></th></tr></thead><tbody><tr><td><strong>Sintaxis</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>dir</code></td><td>Comando para listar archivos</td></tr><tr><td><code>n:</code></td><td>Directorio o unidad para buscar</td></tr><tr><td><code>/a-d</code></td><td><code>/a</code> es el atributo y <code>-d</code> significa no directorios</td></tr><tr><td><code>/s</code></td><td>Muestra archivos en un directorio específico y todos los subdirectorios</td></tr><tr><td><code>/b</code></td><td>Utiliza formato simple (sin información de encabezado ni resumen)</td></tr></tbody></table>

El siguiente comando `| find /c ":\\"` procesa la salida de `dir n: /a-d /s /b` para contar cuántos archivos existen en el directorio y los subdirectorios. Puede utilizar `dir /?` para ver la ayuda completa. Buscar entre 29.302 archivos lleva mucho tiempo; las utilidades de línea de comandos y secuencias de comandos pueden ayudarnos a acelerar la búsqueda. Con `dir` podemos buscar nombres específicos en archivos como:

* cred
* password
* users
* secrets
* key
* Extensiones de archivos comunes para código fuente como: .cs, .c, .go, .java, .php, .asp, .aspx, .html.

```powershell
C:\afsh4ck> dir n:\*cred* /s /b

n:\Contracts\private\credentials.txt


C:\afsh4ck> dir n:\*secret* /s /b

n:\Contracts\private\secret.txt
```

Si queremos buscar una palabra específica dentro de un archivo de texto, podemos usar [findtr](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/findstr) .

### **Windows CMD - Findstr**

```powershell
c:\afsh4ck> findstr /s /i cred n:\*.*

n:\Contracts\private\secret.txt:file with all credentials
n:\Contracts\private\credentials.txt:admin:SecureCredentials!
```

Podemos encontrar más ejemplos de `findstr` [aquí](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/findstr#examples) .

### **Windows PowerShell**

PowerShell fue diseñado para ampliar las capacidades del shell de comandos para ejecutar comandos de PowerShell llamados `cmdlets`. Los cmdlets son similares a los comandos de Windows pero proporcionan un lenguaje de secuencias de comandos más extensible. Podemos ejecutar comandos de Windows y cmdlets de PowerShell en PowerShell, pero el shell de comandos solo puede ejecutar comandos de Windows y no cmdlets de PowerShell. Replicamos los mismos comandos ahora usando Powershell.

```powershell
PS C:\afsh4ck> Get-ChildItem \\192.168.220.129\Finance\

    Directory: \\192.168.220.129\Finance

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         2/23/2022   3:27 PM                Contracts
```

En lugar de `net use`, podemos usar `New-PSDrive` en PowerShell.

```powershell
PS C:\afsh4ck> New-PSDrive -Name "N" -Root "\\192.168.220.129\Finance" -PSProvider "FileSystem"

Name           Used (GB)     Free (GB) Provider      Root                                               CurrentLocation
----           ---------     --------- --------      ----                                               ---------------
N                                      FileSystem    \\192.168.220.129\Finance
```

Para proporcionar un nombre de usuario y contraseña con Powershell, necesitamos crear un [objeto PSCredential](https://docs.microsoft.com/en-us/dotnet/api/system.management.automation.pscredential) . Ofrece una forma centralizada de administrar nombres de usuario, contraseñas y credenciales.

### **PowerShell - PSCredential Object**

```powershell
PS C:\afsh4ck> $username = 'plaintext'
PS C:\afsh4ck> $password = 'Password123'
PS C:\afsh4ck> $secpassword = ConvertTo-SecureString $password -AsPlainText -Force
PS C:\afsh4ck> $cred = New-Object System.Management.Automation.PSCredential $username, $secpassword
PS C:\afsh4ck> New-PSDrive -Name "N" -Root "\\192.168.220.129\Finance" -PSProvider "FileSystem" -Credential $cred

Name           Used (GB)     Free (GB) Provider      Root                                                              CurrentLocation
----           ---------     --------- --------      ----                                                              ---------------
N                                      FileSystem    \\192.168.220.129\Finance
```

En PowerShell, podemos usar el comando `Get-ChildItem` o la variante corta `gci` en lugar del comando `dir`.

### **PowerShell - GCI**

```powershell
PS C:\afsh4ck> N:
PS N:\> (Get-ChildItem -File -Recurse | Measure-Object).Count

29302
```

Podemos usar la propiedad `-Include` para buscar elementos específicos del directorio especificado por el parámetro Ruta.

```powershell
PS C:\afsh4ck> Get-ChildItem -Recurse -Path N:\ -Include *cred* -File

    Directory: N:\Contracts\private

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         2/23/2022   4:36 PM             25 credentials.txt
```

El cmdlet `Select-String` utiliza la coincidencia de expresiones regulares para buscar patrones de texto en archivos y cadenas de entrada. Podemos usar `Select-String` similar a `grep` en UNIX o `findstr.exe` en Windows.

### **PowerShell - Select-String**

```powershell
PS C:\afsh4ck> Get-ChildItem -Recurse -Path N:\ | Select-String "cred" -List

N:\Contracts\private\secret.txt:1:file with all credentials
N:\Contracts\private\credentials.txt:1:admin:SecureCredentials!
```

CLI permite que las operaciones de TI automaticen tareas rutinarias como la administración de cuentas de usuario, copias de seguridad nocturnas o la interacción con muchos archivos. Podemos realizar operaciones de manera más eficiente utilizando scripts que la interfaz de usuario o GUI.

***

## <mark style="color:purple;">**SMB en Linux**</mark>

Las máquinas Linux (UNIX) también se pueden utilizar para explorar y montar recursos compartidos SMB. Tenga en cuenta que esto se puede hacer ya sea que el servidor de destino sea una máquina Windows o un servidor Samba. Aunque algunas distribuciones de Linux admiten una GUI, nos centraremos en las utilidades y herramientas de línea de comandos de Linux para interactuar con SMB. Veamos cómo montar recursos compartidos SMB para interactuar con directorios y archivos localmente.

### **Linux - Mount**

```shell-session
afsh4ck@kali$ sudo mkdir /mnt/Finance
afsh4ck@kali$ sudo mount -t cifs -o username=plaintext,password=Password123,domain=. //192.168.220.129/Finance /mnt/Finance
```

Como alternativa, podemos utilizar un credentialfile.

```shell-session
afsh4ck@kali$ mount -t cifs //192.168.220.129/Finance /mnt/Finance -o credentials=/path/credentialfile
```

El archivo `credentialfile` tiene que estar estructurado así:

### **Credentialfile**

```txt
username=plaintext
password=Password123
domain=.
```

{% hint style="info" %}
**Nota**: Necesitamos instalar `cifs-utils`para conectarnos a una carpeta compartida SMB. Para instalarlo podemos ejecutar desde la línea de comandos `sudo apt install cifs-utils`.
{% endhint %}

Una vez montada una carpeta compartida, puede utilizar herramientas comunes de Linux, como `find`o `grep` para interactuar con la estructura de archivos. Busquemos un nombre de archivo que contenga la cadena `cred`:

### **Linux - Find**

```shell-session
afsh4ck@kali$ find /mnt/Finance/ -name *cred*

/mnt/Finance/Contracts/private/credentials.txt
```

A continuación, busquemos archivos que contengan la cadena `cred`:

```shell-session
afsh4ck@kali$ grep -rn /mnt/Finance/ -ie cred

/mnt/Finance/Contracts/private/credentials.txt:1:admin:SecureCredentials!
/mnt/Finance/Contracts/private/secret.txt:1:file with all credentials
```

***

## <mark style="color:purple;">Otros servicios</mark>

Existen otros servicios para compartir archivos como FTP, TFTP y NFS que podemos adjuntar (montar) usando diferentes herramientas y comandos. Sin embargo, una vez montamos un servicio para compartir archivos, debemos entender que podemos utilizar las herramientas disponibles en Linux o Windows para interactuar con archivos y directorios. A medida que descubramos nuevos servicios para compartir archivos, necesitaremos investigar cómo funcionan y qué herramientas podemos utilizar para interactuar con ellos.

### **Correo electrónico**

Normalmente necesitamos dos protocolos para enviar y recibir mensajes, uno para enviar y otro para recibir. El Protocolo simple de transferencia de correo (SMTP) es un protocolo de entrega de correo electrónico que se utiliza para enviar correo a través de Internet. Asimismo, se debe utilizar un protocolo de soporte para recuperar un correo electrónico de un servicio. Hay dos protocolos principales que podemos utilizar:&#x20;

* [`POP3`](/ethical-hacking-cheatsheet/recopilacion-de-informacion/enumeracion/imap-pop3.md)
* [`IMAP`](/ethical-hacking-cheatsheet/recopilacion-de-informacion/enumeracion/imap-pop3.md)

Podemos utilizar un cliente de correo como [Evolution](https://wiki.gnome.org/Apps/Evolution) , el gestor de información personal oficial, y cliente de correo para el Entorno de Escritorio GNOME. Podemos interactuar con un servidor de correo electrónico para enviar o recibir mensajes con un cliente de correo. Para instalar Evolution, podemos usar el siguiente comando:

### **Linux - Instalar evolution**

```bash
sudo apt-get install evolution
```

{% hint style="info" %}
Nota: Si aparece un error al iniciar Evolution que indica "bwrap: No se puede crear el archivo en ...", use este comando para iniciar Evolution `export WEBKIT_FORCE_SANDBOX=0 && evolution`.
{% endhint %}

#### **Vídeo: Conexión a IMAP y SMTP mediante Evolution**

Haga clic en la imagen a continuación para ver una breve demostración en video.

[![Evolución](https://academy.hackthebox.com/storage/modules/116/ConnectToIMAPandSMTP.jpg)](https://www.youtube.com/watch?v=xelO2CiaSVs)

Podemos utilizar el nombre de dominio o la dirección IP del servidor de correo. Si el servidor usa SMTPS o IMAPS, necesitaremos el método de cifrado adecuado (TLS en un puerto dedicado o STARTTLS  después de conectarnos). Podemos usar la opción `Check for Supported Types` en autenticación para confirmar si el servidor admite nuestro método seleccionado.

***

## <mark style="color:purple;">**Bases de datos**</mark>

Las bases de datos se utilizan normalmente en las empresas y la mayoría de ellas las utilizan para almacenar y gestionar información. Existen diferentes tipos de bases de datos, como bases de datos jerárquicas, bases de datos NoSQL (o no relacionales) y bases de datos relacionales SQL. Nos centraremos en las bases de datos relacionales SQL y las dos bases de datos relacionales más comunes llamadas MySQL y MSSQL. Tenemos tres formas comunes de interactuar con bases de datos:

<table><thead><tr><th width="105"></th><th></th></tr></thead><tbody><tr><td><code>1.</code></td><td>Utilidades de línea de comando ( <code>mysql</code>o <code>sqsh</code>)</td></tr><tr><td><code>2.</code></td><td>Una aplicación GUI para interactuar con bases de datos como HeidiSQL, MySQL Workbench o SQL Server Management Studio.</td></tr><tr><td><code>3.</code></td><td>Lenguajes de programación</td></tr></tbody></table>

Exploremos las utilidades de línea de comandos y una aplicación GUI.

### **MSSQL**

Para interactuar con [MSSQL (Microsoft SQL Server)](https://www.microsoft.com/en-us/sql-server/sql-server-downloads) con Linux podemos usar [sqsh](https://en.wikipedia.org/wiki/Sqsh) o [sqlcmd](https://docs.microsoft.com/en-us/sql/tools/sqlcmd-utility) si estás usando Windows. El objetivo de `Sqsh` es proporcionar gran parte de la funcionalidad proporcionada por un shell de comandos, como variables, alias, redirección, canalizaciones, antecedentes, control de trabajos, historial, sustitución de comandos y configuración dinámica. Podemos iniciar una sesión SQL interactiva de la siguiente manera:

### **Linux-SQSH**

```shell-session
afsh4ck@kali$ sqsh -S 10.129.20.13 -U username -P Password123
```

La utilidad `sqlcmd` le permite ingresar declaraciones Transact-SQL, procedimientos del sistema y archivos de script a través de una variedad de modos disponibles:

* En el símbolo del sistema.
* En el Editor de consultas en modo SQLCMD.
* En un archivo de script de Windows.
* En un paso de trabajo del sistema operativo (Cmd.exe) de un trabajo del Agente SQL Server.

### **Windows-SQLCMD**

```powershell
C:\kali> sqlcmd -S 10.129.20.13 -U username -P Password123
```

Para obtener más información sobre el uso de `sqlcmd`, puedes consultar [la documentación de Microsoft](https://docs.microsoft.com/en-us/sql/ssms/scripting/sqlcmd-use-the-utility) .

### **MySQL**

Para interactuar con [MySQL](https://en.wikipedia.org/wiki/MySQL) , podemos usar binarios de MySQL para Linux ( `mysql`) o Windows ( `mysql.exe`). MySQL viene preinstalado en algunas distribuciones de Linux, pero podemos instalar binarios de MySQL para Linux o Windows usando esta [guía](https://dev.mysql.com/doc/mysql-getting-started/en/#mysql-getting-started-installing) . Inicie una sesión SQL interactiva usando Linux:

#### **Linux-MySQL**

```shell-session
afsh4ck@kali$ mysql -u username -pPassword123 -h 10.129.20.13
```

**Windows-MySQL**

```powershell
C:\kali> mysql.exe -u username -pPassword123 -h 10.129.20.13
```

**Aplicación GUI**

Los motores de bases de datos suelen tener su propia aplicación GUI. MySQL tiene [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) y MSSQL tiene [SQL Server Management Studio o SSMS](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms) , podemos instalar esas herramientas en nuestro host de ataque y conectarnos a la base de datos. SSMS solo es compatible con Windows. Una alternativa es utilizar herramientas comunitarias como [dbeaver](https://github.com/dbeaver/dbeaver) . [dbeaver](https://github.com/dbeaver/dbeaver) es una herramienta de base de datos multiplataforma para Linux, macOS y Windows que admite la conexión a múltiples motores de bases de datos como MSSQL, MySQL, PostgreSQL, entre otros, lo que nos facilita, como atacante, interactuar con servidores de bases de datos comunes.

Para instalar [dbeaver](https://github.com/dbeaver/dbeaver) usando un paquete Debian, podemos descargar el paquete de versión .deb desde <https://github.com/dbeaver/dbeaver/releases> y ejecutar el siguiente comando:

**Instalar dbeaver**

```shell-session
afsh4ck@kali$ sudo dpkg -i dbeaver-<version>.deb
```

Para iniciar el uso de la aplicación:

```shell-session
afsh4ck@kali$ dbeaver &
```

Para conectarnos a una base de datos, necesitaremos un conjunto de credenciales, la IP de destino y el número de puerto de la base de datos, y el motor de la base de datos al que intentamos conectarnos (MySQL, MSSQL u otro).

**Vídeo: Conexión a MSSQL DB usando dbeaver**

Haga clic en la imagen a continuación para ver un breve video de demostración sobre cómo conectarse a una base de datos MSSQL usando `dbeaver`.

[![MSSQL](https://academy.hackthebox.com/storage/modules/116/ConnectToMSSQL.jpg)](https://www.youtube.com/watch?v=gU6iQP5rFMw)

Haga clic en la imagen a continuación para ver un breve video de demostración sobre cómo conectarse a una base de datos MySQL usando `dbeaver`.

**Vídeo: Conexión a MySQL DB usando dbeaver**

[![MySQL](https://academy.hackthebox.com/storage/modules/116/ConnectToMYSQL.jpg)](https://www.youtube.com/watch?v=PeuWmz8S6G8)

Una vez que tengamos acceso a la base de datos mediante una utilidad de línea de comandos o una aplicación GUI, podemos usar [declaraciones Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/statements/statements?view=sql-server-ver15) comunes para enumerar bases de datos y tablas que contienen información confidencial, como nombres de usuarios y contraseñas. Si tenemos los privilegios correctos, podríamos ejecutar comandos como la cuenta de servicio MSSQL. Más adelante en este módulo, analizaremos declaraciones y ataques comunes de Transact-SQL para bases de datos MSSQL y MySQL.

***

## <mark style="color:purple;">**Herramientas**</mark>

Es fundamental familiarizarse con las utilidades de línea de comandos predeterminadas disponibles para interactuar con diferentes servicios. Sin embargo, a medida que avancemos en el campo, encontraremos herramientas que pueden ayudarnos a ser más eficientes. La comunidad comúnmente crea esas herramientas.&#x20;

Aunque con el tiempo tendremos ideas sobre cómo mejorar una herramienta o para crear nuestras propias herramientas, aunque no seamos desarrolladores a tiempo completo, cuanto más nos familiaricemos con el hacking. Cuanto más aprendemos, más nos encontramos buscando una herramienta que no existe, lo que puede ser una oportunidad para aprender y crear nuestras herramientas.

**Herramientas para interactuar con servicios comunes**

| **SMB**                                                                                  | **FTP**                                     | **Email**                                          | **Bases de datos**                                                                                                           |
| ---------------------------------------------------------------------------------------- | ------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| [smbclient](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html)          | [ftp](https://linux.die.net/man/1/ftp)      | [Thunderbird](https://www.thunderbird.net/en-US/)  | [mssql-cli](https://github.com/dbcli/mssql-cli)                                                                              |
| [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec)                              | [lftp](https://lftp.yar.ru/)                | [Claws](https://www.claws-mail.org/)               | [mycli](https://github.com/dbcli/mycli)                                                                                      |
| [SMBMap](https://github.com/ShawnDEvans/smbmap)                                          | [ncftp](https://www.ncftp.com/)             | [Geary](https://wiki.gnome.org/Apps/Geary)         | [mssqlclient.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/mssqlclient.py)                             |
| [Impacket](https://github.com/SecureAuthCorp/impacket)                                   | [filezilla](https://filezilla-project.org/) | [MailSpring](https://getmailspring.com/)           | [dbeaver](https://github.com/dbeaver/dbeaver)                                                                                |
| [psexec.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/psexec.py)   | [crossftp](http://www.crossftp.com/)        | [mutt](http://www.mutt.org/)                       | [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)                                                                |
| [smbexec.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/smbexec.py) |                                             | [mailutils](https://mailutils.org/)                | [SQL Server Management Studio or SSMS](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms) |
|                                                                                          |                                             | [sendEmail](https://github.com/mogaal/sendemail)   |                                                                                                                              |
|                                                                                          |                                             | [swaks](http://www.jetmore.org/john/code/swaks/)   |                                                                                                                              |
|                                                                                          |                                             | [sendmail](https://en.wikipedia.org/wiki/Sendmail) |                                                                                                                              |

## <mark style="color:purple;">Solución de problemas generales</mark>

Dependiendo de la versión de Windows o Linux con la que estemos trabajando o a la que nos dirigimos, podemos encontrar diferentes problemas al intentar conectarnos a un servicio.

Algunas razones por las que es posible que no tengamos acceso a un recurso:

* Autenticación
* Privilegios
* Conexión de red
* Reglas del cortafuegos
* Soporte de protocolo

Tenga en cuenta que podemos encontrarnos con diferentes errores dependiendo del servicio al que nos dirigimos. Podemos utilizar los códigos de error a nuestro favor y buscar documentación oficial o foros donde la gente resolvió un problema similar al nuestro.

***

## <mark style="color:purple;">**El concepto de ataque**</mark>

![](https://academy.hackthebox.com/storage/modules/116/attack_concept2.png)

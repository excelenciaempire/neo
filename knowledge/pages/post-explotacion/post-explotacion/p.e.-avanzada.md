
# P.E. Avanzada

## <mark style="color:purple;">Port Forwarding</mark>

Port Forwarding (reenvío de puertos) es una técnica utilizada en redes informáticas para permitir que los paquetes de datos que llegan a un puerto específico de un router o firewall sean redirigidos hacia un dispositivo o servidor específico en la red local.

Hace que la conexión que se establece en una máquina concreta se redirija a un puerto que nosotros especifiquemos.

#### Caso de uso:

* En la máquina WS03 tenemos un servicio que es vulnerable, pero ese servicio tiene limitaciones por un firewall local
* Descargar netcat en Windows para emular un servicio corriendo en localhost

### Ver puertos abiertos en máquina destino

```
sudo nmap -v -sS TARGET
```

### En Meterpreter Kali:

```
portfwd add -l 135 -p 23 -r TARGET
```

* Si queremos eliminar el relay:&#x20;

```
portfwd delete -i 1
```

### Netcat Kali

```
netcat 127.0.0.1 135
```

* Lo que escribamos ahora le llega al Netcat Windows al puerto 23 donde estaba escuchando&#x20;

## <mark style="color:purple;">Pivoting</mark>

Pivoting es una técnica utilizada para <mark style="color:purple;">moverse lateralmente</mark> a través de una red comprometida a fin de acceder a recursos adicionales que no son directamente accesibles desde el punto de entrada inicial. Por lo general, se utiliza cuando un atacante ha logrado comprometer un equipo o servidor en una red pero <mark style="color:purple;">no puede acceder directamente</mark> a otros sistemas o recursos de la red. El atacante utiliza el equipo comprometido como un punto de pivote para moverse a través de la red y acceder a otros recursos.

Sirve para evadir firewalls y ejecutar acciones como si se hicieran desde otro ordenador del dominio.

* Llevar sesión de Meterpreter al background
* Ctrl + Z&#x20;
* sessions
* route add IP\_EMPLEADO\_X 255.255.255.0 1

### <mark style="color:purple;">Netcat Port-Pivot Relay</mark>

Acceder a un servicio al que no se puede acceder desde fuera porque hay un firewall que lo bloquea. El port pivot lo ponemos en la máquina que queremos atacar y exponemos el puerto 40 p.e.

#### Windows Terminal 1:

```
.\ncat.exe -lvp 23
```

#### Windows Terminal 2:

```
.\ncat.exe -lvp 40 | .\ncat.exe TARGET 23
```

### En Kali (ejemplo en Linux)

```
mknod pivot p
```

#### Terminal 1:

```
nc -lvp 23
```

#### Terminal 2:

```
nc -lvp 40 0<pivot | nc 127.0.0.1 23 1>pivot
```

#### Terminal 3:

```
nc 127.0.0.1 40
```

* Lo que pongamos llega a la terminal 1

## <mark style="color:purple;">Local Tunneling</mark>

El local tunneling establece una conexión segura entre el dispositivo del usuario y un servidor remoto que actúa como intermediario. El usuario inicia el túnel localmente en su computadora, especificando el puerto local y el puerto remoto que deben conectarse. Luego, el servidor remoto redirige cualquier tráfico que llegue a su dirección IP y puerto asociado al usuario a través del túnel seguro, lo que permite que el servicio alojado en la computadora del usuario sea accesible desde cualquier lugar del mundo.

### NGrok

{% embed url="<https://ngrok.com/>" %}

Ngrok es una herramienta que permite crear túneles seguros desde internet hacia un servidor local, permitiendo que los servicios alojados en una computadora local sean accesibles desde cualquier lugar en la web.

Para utilizar Ngrok en Kali Linux, puedes seguir los siguientes pasos:

1. Descarga la versión correspondiente de Ngrok para Linux desde su sitio web oficial.
2. Descomprime el archivo descargado en una carpeta de tu elección.
3. En una terminal, navega hasta la carpeta donde se encuentra el archivo ngrok.
4. Ejecuta el siguiente comando para iniciar Ngrok: `./ngrok authtoken <tu_token_de_autenticación>`. Este comando establece la autenticación de tu cuenta Ngrok en la terminal. Puedes encontrar tu token de autenticación en tu cuenta de Ngrok en línea.
5. A continuación, para crear un túnel, ejecuta el comando `./ngrok http <puerto_local>`. Este comando creará un túnel seguro desde internet hacia el puerto local especificado. Por ejemplo, si tu servidor local ejecuta un servicio web en el puerto 80, puedes ejecutar `./ngrok http 80` para crear un túnel a ese puerto.
6. Ngrok mostrará la dirección URL del túnel en la terminal. Puedes copiar esta URL y compartirla con otros usuarios para que puedan acceder a tu servicio local a través de internet.

### Local Tunnel Github

{% embed url="<https://github.com/localtunnel/localtunnel>" %}

Alternativa a Ngrok. LocalTunnel es una herramienta de código abierto que permite exponer un servidor local hacia internet a través de un túnel seguro sin necesidad de configurar el enrutamiento de puertos o la configuración de NAT en tu router.

#### Instalación

```
sudo apt install rpm
sudo npm install -g localtunnel
```

#### Crear un túnel local

```
lt -p 80
```

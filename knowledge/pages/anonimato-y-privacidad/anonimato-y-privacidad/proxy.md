
# Proxy

<figure><img src="/files/zNtJj5ft4q604bvngIDn" alt=""><figcaption><p>Esquema de conexión por Proxy</p></figcaption></figure>

## <mark style="color:purple;">Proxy VS VPN</mark>

* Una VPN cifra y encapsula el tráfico, un Proxy no
* Una VPN suele trabajar a nivel sistema operativo y redirige todo el tráfico de red, el proxy funciona a nivel de aplicación.
* La conexión por VPN suele ser más estable que con un Proxy
* Los servicios VPN suelen ser de pago, los Proxy gratuitos
* Las conexiones por VPN pueden ser más lentas que con un proxy porque requieren cifrar y encapsular la información

## <mark style="color:purple;">Configurar proxy publico en Kali Linux</mark>

Encontrar un proxy público, hay multitud de servicios de proxy gratis online.

{% embed url="<https://free-proxy-list.net/anonymous-proxy.html>" %}

* Buscar en Google: anonymous proxy list
* Abrir firefox > preferencias
* Network Settings&#x20;
* Manual proxy settings&#x20;
* Meter los proxys que queramos

## <mark style="color:purple;">Privoxy</mark>&#x20;

{% embed url="<https://github.com/unisx/privoxy>" %}

Privoxy es un software libre y de código abierto que actúa como un filtro de proxy web. Su objetivo es proteger la privacidad del usuario y mejorar la seguridad en línea al filtrar y bloquear contenido no deseado en la web.

Privoxy funciona como un <mark style="color:purple;">proxy local</mark> que se ejecuta en el equipo del usuario y filtra el tráfico de Internet antes de enviarlo a la red. El software utiliza una serie de reglas y patrones de filtrado para bloquear anuncios, scripts maliciosos, cookies y otros tipos de contenido no deseado en la web.

```python
sudo apt-get install privoxy
sudo emacs /etc/privoxy/config
Forwarding # Copiar el example y pegar al final del todo descomentado 
Cambiar la IP y el puerto en formato IP:PUERTO
sudo service privoxy start
```

* En el navegador: configurar proxy manual
* 127.0.0.1 puerto 8118

## <mark style="color:purple;">ProxySite</mark>

{% embed url="<https://www.proxysite.com/es/>" %}

ProxySite es un servicio en línea que permite a los usuarios navegar por Internet de forma anónima y acceder a contenido restringido geográficamente. ProxySite actúa como un servidor proxy remoto que enmascara la dirección IP real del usuario y permite acceder a sitios web y servicios que de otra manera estarían bloqueados geográficamente.

Para utilizar ProxySite, los usuarios simplemente deben ingresar la URL del sitio web que quieren visitar en el campo de búsqueda del sitio web de ProxySite. El tráfico de Internet se enruta a través del servidor proxy remoto de ProxySite, lo que oculta la dirección IP real del usuario y enmascara su ubicación geográfica.

## <mark style="color:purple;">ProxyChains</mark>

{% embed url="<https://github.com/haad/proxychains>" %}

ProxyChains es un software libre y de código abierto que permite a los usuarios redirigir el tráfico de Internet a través de múltiples servidores proxy. El software utiliza una serie de proxies para ocultar la dirección IP real del usuario y enmascarar su ubicación geográfica.

ProxyChains funciona como un proxy local que se ejecuta en el equipo del usuario y redirige el tráfico de Internet a través de una cadena de proxies remotos. El software también ofrece opciones de encriptación para proteger la privacidad y la seguridad del usuario en línea.

* Encadena varios múltiples proxys para que sea muy difícil saber la dirección de origen
* Viene por defecto en Kali

### Configuración&#x20;

<pre class="language-php"><code class="lang-php">sudo emacs /etc/proxychains4.conf
<strong># Al final añadir proxys
</strong># Buscar listado de proxys socks5
# Copiar listado de proxys y pegar en emacs 
<strong># Limpiar el texto con el formato de ProxyChains:
</strong>socks5  192.168.67.78  1080
</code></pre>

<figure><img src="/files/ib9WihXePHPlXPQh1x3a" alt=""><figcaption></figcaption></figure>

### Activar función

Descomentar el inicio de una función para que actúe de ese modo

{% hint style="warning" %}
Solo puede haber una función descomentada
{% endhint %}

Vamos a usar el modo dynamic\_chain

<figure><img src="/files/D1g82UGE5v4typwWfZMc" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
Comentar las líneas de remote dns subnet y proxy dns
{% endhint %}

### Usar ProxyChains

Solamente tenemos que poner proxychains4 delante del comando que queremos utilizar, por ejemplo un nmap

```
proxychains4 nmap -v -sV hackthissite.org
```

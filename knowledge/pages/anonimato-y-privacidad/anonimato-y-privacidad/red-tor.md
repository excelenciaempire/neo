
# Red TOR

## <mark style="color:purple;">¿Que es TOR?</mark>

TOR (The Onion Routing Protocol) es un proyecto desarrollado por el laboratorio de investigación naval de los EEUU para proteger sus comunicaciones.

El principio básico de Tor es el "enrutamiento de cebolla" que consiste en encapsular en varias capas de cifrado el tráfico de red para garantizar su seguridad y privacidad.

La red TOR esta formada por un conjunto de servidores operados por voluntarios que establecen túneles virtuales entre ellos utilizando este protocolo de enrutamiento.

<figure><img src="/files/H84ZoZUPndtUAcnp5eRV" alt=""><figcaption><p>Esquema de cifrado en la Red TOR</p></figcaption></figure>

## <mark style="color:purple;">TOR Hidden Services</mark>

* Los hidden services de TOR se corresponden con todas esas páginas web que se encuentran en la dark web y en muchas ocasiones realizan actividades ilegales
* Los hidden services son servidores que solo pueden ser accedidos a través de nodos de la red TOR que se conocen como entry points
* Una vez seleccionados los entry points, el servidor (hidden service) crea un hidden service descriptor que contiene una clave pública y la dirección IP de los entry points
* Esta información se almacena en una tabla hash distribuida y para acceder a ella se utiliza la onion address que se deriva de la clave pública del hidden service

## <mark style="color:purple;">TOR Browser</mark>

El navegador TOR es un navegador web gratuito y de código abierto que permite a los usuarios navegar por Internet de forma anónima y segura. El navegador TOR utiliza la red TOR para enmascarar la dirección IP real del usuario y ocultar su ubicación geográfica. Además, el navegador ofrece opciones de seguridad y privacidad avanzadas, como la encriptación de extremo a extremo, la protección contra seguimiento en línea y la eliminación automática de cookies y datos de navegación.

#### Instalar en Kali Linux

```bash
sudo apt-get install tor torbrowser-launcher
```

## <mark style="color:purple;">Brave Browser con TOR</mark>

{% embed url="<https://brave.com/es/>" %}

Brave Browser con TOR es una versión del navegador web Brave que incluye la funcionalidad de navegación anónima de la red TOR. ofrece una mayor velocidad y rendimiento en comparación con otros navegadores web que utilizan la red TOR. La versión del navegador utiliza un enfoque de "circuito extendido" para enrutar el tráfico de Internet a través de la red TOR de manera más eficiente y rápida.

* Instalar siguiendo los pasos de su web
* Ventana privada con navegación por TOR

## <mark style="color:purple;">ProxyChains con TOR</mark>

ProxyChains con TOR es una técnica que combina el uso de ProxyChains y la red TOR para proporcionar una mayor privacidad y seguridad en línea. Al utilizar ProxyChains con TOR, el tráfico de Internet se enruta a través de una cadena de servidores proxy remotos antes de pasar a través de la red TOR, lo que proporciona una mayor capa de anonimato y encriptación.

### Configuración

```bash
sudo service tor status
sudo service tor start
sudo gedit /etc/proxychains4.conf

# Añadir al final:
socks5 127.0.0.1:9050
```

{% hint style="warning" %}
Usar el modo Strict Chain
{% endhint %}

{% hint style="success" %}
Ahora al usar ProxyChains lo redirige por TOR
{% endhint %}

## <mark style="color:purple;">SQLmap con TOR</mark>

Podemos lanzar SQLmap a través de la red TOR  usando el flag `--proxy`

```bash
sudo service tor status
sudo service tor start
sqlmap -u TARGET --proxy socks5://127.0.0.1:9050
```

## <mark style="color:purple;">WPscan con TOR</mark>

De igual manera, podemos utilizar WPscan proxificado por TOR.

```bash
wpscan -u TARGET --proxy socks5://127.0.0.1:9050
```

## <mark style="color:purple;">TOR sobre VPN</mark>

Al utilizar TOR sobre VPN, el tráfico de Internet se enruta primero a través de la VPN antes de pasar a través de la red TOR. Esto proporciona una capa adicional de encriptación y anonimato al ocultar la dirección IP real del usuario y enmascarar su ubicación geográfica.

1. Conectarse a una VPN cómo ProtonVPN
2. Hacer peticiones con TOR desde Brave o con ProxyChains configurado

{% hint style="info" %}
Es lo más anónimo pero lo más lento
{% endhint %}

## <mark style="color:purple;">IP Quality Score</mark>

{% embed url="<https://www.ipqualityscore.com/tor-ip-address-check>" %}

IP Quality Score es un servicio en línea que permite a los usuarios verificar la calidad y la seguridad de una dirección IP. El servicio utiliza una serie de herramientas y técnicas de análisis para evaluar la reputación de una dirección IP y determinar si se ha utilizado para actividades malintencionadas en el pasado.

{% hint style="info" %}
Podemos detectar si una IP se está redirigiendo por TOR
{% endhint %}

## <mark style="color:purple;">Servicios que bloquean TOR</mark>

{% embed url="<https://www.google.com/search?q=List+of+services+blocking+Tor&rlz=1C5CHFA_enES991ES991&sxsrf=APwXEddTr9WO2vHMGNMDh_gjqbRPlQDtJg%3A1687878921849&ei=Cf2aZN6-M7uZkdUPvfWU0AM&ved=0ahUKEwie57383uP_AhW7TKQEHb06BToQ4dUDCA8&uact=5&oq=List+of+services+blocking+Tor&gs_lp=Egxnd3Mtd2l6LXNlcnAiHUxpc3Qgb2Ygc2VydmljZXMgYmxvY2tpbmcgVG9yMgoQABhHGNYEGLADMgoQABhHGNYEGLADMgoQABhHGNYEGLADMgoQABhHGNYEGLADMgoQABhHGNYEGLADMgoQABhHGNYEGLADMgoQABhHGNYEGLADMgoQABhHGNYEGLADSN0HUPEFWPEFcAF4AZABAJgBAKABAKoBALgBA8gBAPgBAeIDBBgAIEGIBgGQBgg&sclient=gws-wiz-serp>" %}

## <mark style="color:purple;">Onion Links</mark>

Podemos encontrar Onion Links para navegar por la Deep Web fácilmente con herramientas online cómo `Ahmia` o `OnionLand`:

{% embed url="<https://ahmia.fi/>" %}

{% embed url="<https://www.onionland.to/>" %}

También podemos utilizar la siguiente herramienta para comprobar si un Onion Link está activo:

{% embed url="<https://onion.live/site/onionland-search>" %}

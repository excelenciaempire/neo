
# Herramientas de Phising

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a realizar ataques de phishing para conseguir datos sensibles como la ubicación o credenciales de una persona, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">PyPhisher</mark>

PyPhisher es una herramienta que automatiza el proceso de phising, creando páginas fake con tunelling. Tiene incluidas por defecto un montón de plantillas de redes sociales y servicios online. Cuando los usuarios introducen las credenciales las recibimos por pantalla, y se guardan automáticamente en un archivo .txt.

{% hint style="warning" %}
Esta herramienta fue eliminada de GitHub y solamente está disponible en GitLab
{% endhint %}

{% embed url="<https://gitlab.com/KasRoudra/PyPhisher>" %}

<figure><img src="/files/LXjZFpw7RF67LkraglpY" alt=""><figcaption></figcaption></figure>

#### Instalación y uso

```bash
git clone https://github.com/KasRoudra/PyPhisher.git
cd PyPhisher
python pyphiser.py
```

O podemos instalarlo con pip3:

```bash
sudo pip3 install pyphisher --break-system-packages
pyphisher
```

## <mark style="color:purple;">ZPhisher</mark>

Es una herramienta similar a PyPhisher, con plantillas predefinidas y tunelling para phishing. Funciona bien, aunque nos da algo menos de información que PyPhisher.

{% embed url="<https://github.com/htr-tech/zphisher>" %}

<figure><img src="/files/mbDdylUvomLFD9K8IDa8" alt=""><figcaption></figcaption></figure>

#### Instalación y uso

```bash
git clone --depth=1 https://github.com/htr-tech/zphisher.git
cd zphisher
bash zphisher.sh
```

## <mark style="color:purple;">SocialSploit</mark>

SocialSploit es una herramienta de hacking ético diseñada para la simulación de ataques de phishing. Permite a los usuarios crear fácilmente páginas de phishing y obtener credenciales de prueba para auditorías de seguridad. Con una interfaz sencilla y comandos preconfigurados, facilita la ejecución de pruebas controladas en redes y aplicaciones.

{% embed url="<https://github.com/Cesar-Hack-Gray/SocialSploit>" %}

<figure><img src="/files/rt7OI084D2AYyuljtiQ8" alt=""><figcaption></figcaption></figure>

#### Instalación y uso

```bash
git clone https://github.com/Cesar-Hack-Gray/SocialSploit
cd SocialSploit
bash install.sh
./Sploit
```

Para que esta herramienta funcione correctamente necesitamos hacer forwarding con Ngrok. Una vez configurado nos dará información relevante sobre la víctima:

<figure><img src="/files/fk2o29eDPPPt7iK6ApnL" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Cyber Phish</mark>

Cyber Phish es una herramienta en python que nos permite crear plantillas de email para campañas de phising, seleccionando una de las plantillas que tiene disponibles, y introduciendo nuestro link de phising generado con otras herramientas. Además nos permite introducir el nombre de una persona para un ataque dirigido.

{% embed url="<https://github.com/Cyber-Dioxide/CyberPhish>" %}

<figure><img src="/files/idzYjIBP5CF3XcaV3b7F" alt=""><figcaption></figcaption></figure>

#### Instalación y uso

```bash
git clone https://github.com/Cyber-Dioxide/CyberPhish
cd CyberPhish
pip install -r requirements.txt
python3 CyberPhish.py
```

#### Ejemplo de email en html generado

{% hint style="success" %}
El programa introduce el link de phising en todos los links y botones del mail en html..
{% endhint %}

<figure><img src="/files/z3oB4TnZKboR5OrFfPDf" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Wifi Phisher</mark>

Wifiphisher es una poderosa herramienta de seguridad diseñada para automatizar ataques de ingeniería social sobre redes Wi-Fi, con el objetivo de capturar credenciales o realizar otras acciones de phishing. Una de sus principales funcionalidades es la generación de portales cautivos que imitan servicios legítimos, engañando a los usuarios para que ingresen información personal. Al aprovechar esta técnica, Wifiphisher crea puntos de acceso falsos que simulan ser redes conocidas, lo cual es especialmente efectivo en entornos concurridos, permitiendo a los atacantes obtener credenciales y datos valiosos de manera eficaz.

{% embed url="<https://github.com/wifiphisher/wifiphisher>" %}

<figure><img src="/files/DKXhpdFuOsxSK1E5HU0E" alt=""><figcaption></figcaption></figure>

#### Instalación

```bash
git clone https://github.com/wifiphisher/wifiphisher.git
cd wifiphisher
sudo python3 setup.py install
```

```bash
sudo wifiphisher
```

## <mark style="color:purple;">Maskphish</mark>

Maskphish es una herramienta para camuflar links de phishing, para hacer creer al usuario que es un link legítimo. Incluso estos links pueden empezar por https e incluir las palabras que queramos.

{% embed url="<https://github.com/jaykali/maskphish>" %}

<figure><img src="/files/YanJECvhBbvyMlDEoqJ8" alt=""><figcaption></figcaption></figure>

#### Instalación y uso

```bash
git clone https://github.com/jaykali/maskphish
cd maskphish
bash maskphish.sh
```

## <mark style="color:purple;">MaskURL</mark>

Es una herramienta similar a Maskphish, que funciona perfectamente en 2025.

{% embed url="<https://github.com/Euronymou5/MaskURL>" %}

<figure><img src="/files/WxmN3XOOehi4tLFpAd6z" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Serveo</mark>

Serveo es un servicio que permite a los usuarios exponer fácilmente sus aplicaciones web locales a internet sin la necesidad de configurar un servidor público o modificar la configuración del firewall. Funciona mediante la creación de un túnel seguro que conecta el puerto local de la aplicación al dominio de Serveo, lo que permite el acceso externo a través de una URL única proporcionada por el servicio.&#x20;

{% hint style="warning" %}
Debemos ajustar el **puerto** para que coincida con el de nuestra aplicación corriendo en localhost
{% endhint %}

#### Forwarding del puerto 80 en localhost

```shell-session
afsh4ck@kali$ ssh -R 80:localhost:3000 serveo.net

Forwarding HTTP traffic from https://melioris.serveo.net
```

#### Personalizar URL

```shell-session
afsh4ck@kali$ ssh -R instagram-login:80:localhost:3000 serveo.net

Forwarding HTTP traffic from https://instagram-login.serveo.net
```


# DDoS Attack

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a deshabilitar servicios en red, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

Existen diferentes formas de llevar a cabo un ataque DDoS, pero todos comparten el objetivo de inundar la infraestructura de destino. Algunos ejemplos de técnicas utilizadas en ataques DDoS incluyen el envío masivo de tráfico web, el envío de solicitudes de conexión excesivas a servicios específicos, y la explotación de vulnerabilidades en sistemas de red para agotar sus recursos.

## <mark style="color:purple;">Low Carbon Ion Cannon (LOIC)</mark>

{% embed url="<https://github.com/NewEraCracker/LOIC>" %}

LOIC (Low Orbit Ion Cannon) es una herramienta de código abierto que se ha utilizado en el pasado para llevar a cabo ataques DDoS. LOIC permite que múltiples computadoras envíen tráfico simultáneamente a un objetivo específico, lo que puede sobrecargar los recursos del objetivo y hacer que sea inaccesible para los usuarios legítimos. LOIC fue diseñado inicialmente como una herramienta de prueba de estrés para ayudar a los administradores de sistemas a evaluar la capacidad de sus sistemas para manejar cargas de tráfico pesadas, pero también ha sido utilizada con fines maliciosos por individuos y grupos de hackers.

<figure><img src="/files/ZDQsvDqGKmtPta0mZFiV" alt=""><figcaption><p>Interfaz de LOIC</p></figcaption></figure>

## <mark style="color:purple;">MHDDoS</mark>

{% embed url="<https://github.com/MatrixTM/MHDDoS>" %}

Es la herramienta más descargada en GitHub para realizar ataques DDoS. Tiene varios modos de ataque y bypass de defensas.

#### Instalación

```
git clone https://github.com/MatrixTM/MHDDoS.git
cd MHDDoS
pip install -r requirements.txt
```

## <mark style="color:purple;">**GoldenEye**</mark>

{% embed url="<https://github.com/jseidl/GoldenEye>" %}

GoldenEye es una herramienta de prueba de estrés de red de código abierto que se utiliza para realizar ataques de denegación de servicio distribuido (DDoS). Esta herramienta está diseñada para generar una gran cantidad de tráfico de red falso desde una <mark style="color:purple;">botnet</mark> y saturar los recursos de un servidor o red objetivo, lo que puede provocar una caída del servicio o una degradación significativa del rendimiento.

<figure><img src="/files/JF913iF36rDD9JAz17oM" alt=""><figcaption><p>GoldenEye capturado con Wireshark</p></figcaption></figure>

**Instalación y uso**

```html
git clone https://github.com/jseidl/GoldenEye.git
cd GoldenEye
./goldeneye.py -h <!-- Mostrar ayuda y opciones -->
./goldeneye.py <URL_del_objetivo> <!-- Ataque por defecto -->
./goldeneye.py <URL_del_objetivo> -s 1000 <!-- Especificar número de sockets -->
./goldeneye.py <URL_del_objetivo> -s 10 -m random <!-- Ataque en random mode -->
```

## <mark style="color:purple;">**Slowloris**</mark>

{% embed url="<https://github.com/gkbrk/slowloris>" %}

<figure><img src="/files/VEKhPivKNP4eSbv2G0Pp" alt=""><figcaption><p>Slowloris Attack</p></figcaption></figure>

Slowloris es una técnica y herramienta de ataque de denegación de servicio (DoS) diseñada para saturar y agotar los recursos de un servidor web, lo que hace que el sitio web sea inaccesible para los usuarios legítimos. Fue creado por el hacker RSnake (Robert "RSnake" Hansen) y es conocido por ser un ataque de bajo y lento consumo de ancho de banda.

El funcionamiento de Slowloris es relativamente simple pero efectivo. En lugar de inundar el servidor objetivo con una gran cantidad de tráfico como en los ataques DDoS tradicionales, Slowloris mantiene un gran número de conexiones HTTP abiertas al servidor, pero las mantiene activas de manera lenta, enviando continuamente encabezados HTTP parciales o incompletos. El servidor web mantiene estas conexiones abiertas, esperando a que se completen los encabezados, y este proceso agota gradualmente los recursos del servidor, como los puertos de conexión y los hilos del servidor. Como resultado, el servidor web se satura y no puede atender a las solicitudes legítimas de los usuarios.

#### Instalación y uso

Puedes clonar el repositorio o usar **pip:**

```
sudo pip3 install slowloris
slowloris example.com
```

## <mark style="color:purple;">**R.U.D.Y (R-U-Dead-Yet)**</mark>

{% embed url="<https://github.com/loganhasson/r-u-dead-yet>" %}

R.U.D.Y es otra herramienta de ataque lento que consume poco ancho de banda, cuyo objetivo es permitir al usuario lanzar ataques fácilmente mediante una interfaz interactiva sencilla. Al abrir múltiples solicitudes HTTP POST y luego mantener esas conexiones abiertas el máximo de tiempo posible, el objetivo del ataque es saturar lentamente al servidor de destino.


# Load Balancing Detector

## <mark style="color:purple;">LBD - Load Balancing Detector</mark>

LBD es el acrónimo de Load Balancing Detector, que se refiere a una herramienta de seguridad utilizada para detectar balanceadores de carga en una red.

La herramienta LBD escanea la red en busca de dispositivos de balanceo de carga y recopila información sobre su configuración, incluyendo el número de servidores que están siendo equilibrados, el tipo de algoritmo de balanceo utilizado y el estado de los servidores.

```
lbd IP_O_DOMINIO
```

{% hint style="danger" %}
Genera mucho tráfico de red (escaneo activo). No utilizar esta técnica sin autorización del objetivo.
{% endhint %}

## <mark style="color:purple;">Halberd</mark>

Halberd es una herramienta de análisis de seguridad de código abierto utilizada para identificar aplicaciones web y servicios en una red. Esta herramienta utiliza técnicas avanzadas de análisis de protocolos de red para identificar los servicios que se están ejecutando en los puertos abiertos de un sistema. Halberd localiza el servidor real detrás de un balanceador de carga.

{% embed url="<https://github.com/jmbr/halberd>" %}

### Empleo

```
git clone https://github.com/jmbr/halberd.git
cd halberd
sudo python2 setup.py install
halberd IP_TARGET
```


# Escaneo Avanzado

{% hint style="danger" %}
**Nota:** Este tipo de búsquedas son muy invasivas, ya que hacen muchas peticiones al servidor del objetivo, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Reconocimiento avanzado de Hosts</mark>

Nos localiza todos los host de una infraestructura sin ser detectados por IDS

```bash
sudo nmap -n -sn -PS 172.16.123.0/24
```

{% hint style="info" %}
El `-sn` hace que no haga un escaneo de puertos
{% endhint %}

## <mark style="color:purple;">Escaneo avanzado de puertos</mark>

Se puede utilizar el comando `--top-ports 5` para limitar el número de peticiones a puertos. Esto hace que no se detecte por herramientas de seguridad. Al superar el número 5 suele ser detectado:

```bash
sudo nmap -v -n -sS --top-ports 5 {IP}
```

## <mark style="color:purple;">Fragmentación de paquetes con Nmap</mark>

Al fragmentar los paquetes en un escaneo con nmap podemos evadir los firewall y IDS&#x20;

* Parámetro -ff

```bash
sudo nmap -v -n -ff -sS --top-ports 5 IP-TARGET
```

## <mark style="color:purple;">Escaneo de S.O evitando IDS</mark>

```bash
sudo nmap -v -n -ff -O --top-ports 5 IP-TARGET
```

## <mark style="color:purple;">Escaneo usando señuelos con Nmap</mark>

Cambia nuestra IP varias veces al escanear

* Parámetro -D {IPs falsas}

```bash
sudo nmap -v -D IP1,IP2,IP3,IP4,IP5 IP-TARGET
```

* Las IP deberían coincidir con las activas en una organización, así no sabría cual es la IP que hace es escaneo de puertos, por ejemplo terminado en .1, .2, .3…
* No usar la misma IP que la máquina objetivo

## <mark style="color:purple;">Spoofing de la identidad del atacante</mark>

* Parámetro -S

```bash
sudo nmap -Pn -S {IP de la misma red, e.j .1} -n -e eth0 IP-TARGET
```

```bash
--source-port 80 # Esto indica el puerto desde el que se hace el escaneo
```

## <mark style="color:purple;">Control de tiempos en los escaneos</mark>

* Parámetro -T (del 0 al 5, de más lento a más rápido)
* nmap usa el -T 3 por defectoB
* Del 0 al 1 puede evadir los IDS

{% code title="Escaneo más lento" %}

```bash
sudo nmap -v -sV -T0 IP-TARGET
```

{% endcode %}

{% code title="Escaneo más rápido" %}

```bash
sudo nmap -v -sV -T5 IP-TARGE
```

{% endcode %}

## <mark style="color:purple;">Custom script de escaneo con delay</mark>

Ejecutar la siguiente sentencia en la terminal:

{% code overflow="wrap" %}

```bash
for i in {0..30..2}; do; sudo nmap -sS -p$(($i+1))-$(($i+2)) -n IP-TARGET; sleep 30; done
```

{% endcode %}

* Podemos aumentar el parámetro sleep para evitar ser detectados, por ejemplo a 40

## <mark style="color:purple;">Escaneos en IPV6 con Nmap</mark>

* Parámetro -6
* Hay que referenciar el host con el protocolo IPV6 mediante las direcciones multicast
* [Multicast adress en Wikipedia](https://en.wikipedia.org/wiki/Multicast_address), vemos todas las direcciones multicast en IPV6

```bash
nmap -6 <dirección IPv6 de la red>
```

```bash
ping6 ff02::1
```

```bash
ip neight
```

## <mark style="color:purple;">Escaneo avanzado de servicios</mark>

Escaneo dirigido a puertos específicos para evitar ser detectados por un ID

```bash
sudo nmap -sV -n -p21,22,80 IP-TARGET
```

## <mark style="color:purple;">Alternativas a Nmap</mark>

### Naabu

Naabu es una herramienta de escaneo de puertos y detección de servicios de red de código abierto, desarrollada en el lenguaje Go. Naabu utiliza técnicas de escaneo rápido y eficiente para identificar los puertos abiertos y los servicios de red en hosts específicos o en rangos de direcciones IP.

```bash
sudo apt install naabu
```

```bash
naabu -top-ports 5 IP-TARGET
```

### Netcat

```bash
netcat -nv IP-TARGET 80
```

* Si nos devuelve un “No route to host” significa que no está activo ese host en nuestra infraestructura

### Masscan

Herramienta de escaneo hiperrápido, que sirve para escanear muchas máquinas a la vez de una organización.

```bash
sudo masscan {ip .0/24} -p80 —interface eth0
```

```bash
--rate 10000 (esto sirve para aumentar la velocidad de escaneo)
```

```bash
sudo masscan {ip.0/24} —top-ports 100 —interface eth0 —rate 10000
```

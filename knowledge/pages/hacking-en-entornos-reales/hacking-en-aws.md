
# Hacking en AWS

## <mark style="color:purple;">Recopilación de información en AWS</mark>

{% hint style="info" %}
Tiene limitaciones por la plataforma. No están permitidos ataques DDOS
{% endhint %}

```csharp
ping BALANCEADOR
# Puede que no responda a Ping 
sudo nmap -sn BALANCEADOR
sudo nmap -sS BALANCEADOR
sudo nmap -sV BALANCEADOR
sudo nmap -O BALANCEADOR
```

### Load balancing detector

Load Balancing Detector es una herramienta de seguridad que se utiliza para identificar y analizar la configuración de balanceadores de carga en una red. Un balanceador de carga se utiliza para distribuir el tráfico de red entre múltiples servidores o dispositivos para mejorar el rendimiento y la disponibilidad de los servicios en línea.

```
lbd TARGET
```

{% hint style="warning" %}
Esto genera mucho tráfico de red, en planes gratuitos de AWS podría resultar en cobros indeseados
{% endhint %}

## <mark style="color:purple;">Controles de seguridad en AWS</mark>

Buscar IP públicas en un host que no estén detrás de un balanceador

* Podemos usar Shodan o Censys

```
nmap -sV IP-INSTANCIA
```

* Suele tener abiertos los puertos 22 y 80 (SSH y HTTP)

```
netcat -v IP-INSTANCIA 22
```

* Esto nos devuelve la versión de SSH si no aparece en el anterior escaneo

### Configuración de la instancia segura

#### En editar reglas de entrada:

* Conexiones por SSH y HTTP con el origen el LB-SG (Load balancing security group)

## <mark style="color:purple;">Auditoría de infraestructura interna</mark>

Este tipo de auditoría se realiza cuando ya hemos comprometido un servidor y estamos dentro:

### Instalar nmap en el servidor

```
sudo yum install nmap
```

### Descubrimiento de infraestructura

```
nmap -sn 10.0.0.0/24
nmap -sS IPS-INFRAESTRUCTURA
```

### Identificar bases de datos MySQL

```php
nmap -sS -p 3306 10.0.0.0/24
# El puerto 3306 es el de la base de datos MySQL
```

<figure><img src="/files/4NQFNLHxSEGNmqSs0ewz" alt=""><figcaption><p>Identificación de bases de datos en un red</p></figcaption></figure>

* Ver host levantados e intentar conectarse con Netcat

```
nc 10.0.0.210 3306
```

## <mark style="color:purple;">Tipos de auditorías de seguridad</mark>&#x20;

### Externa

* Te dan un nombre de dominio y buscas todas las vulnerabilidades que puedas

### Infraestructura interna

* Te crean una máquina dentro de la infraestructura y te dan acceso
* Por ejemplo en AWS con una security group

<br>

